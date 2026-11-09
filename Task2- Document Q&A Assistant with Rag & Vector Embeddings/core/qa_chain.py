"""
RetrievalQA Chain with Strict Context Grounding and Source Page Citations.
"""

import os
import re
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain_core.documents import Document
from core.vector_store import ChromaVectorStore

logger = logging.getLogger("RAGQAChain")


@dataclass
class SourceCitation:
    source_file: str
    page_number: int
    excerpt: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_file": self.source_file,
            "page_number": self.page_number,
            "excerpt": self.excerpt,
        }

    def format_citation(self) -> str:
        return f"- {self.source_file} (Page {self.page_number}): \"{self.excerpt}\""


@dataclass
class RAGAnswer:
    question: str
    answer: str
    citations: List[SourceCitation]
    source_documents: List[Document]

    def format_full_response(self) -> str:
        lines = [
            f"Question: {self.question}",
            "",
            f"Answer:\n{self.answer}",
            "",
            "Sources & Citations:",
        ]
        if self.citations:
            for cit in self.citations:
                lines.append(f"  * {cit.source_file} [Page {cit.page_number}]")
                lines.append(f"    Excerpt: \"{cit.excerpt}\"")
        else:
            lines.append("  * No relevant sources retrieved.")
        return "\n".join(lines)


RAG_SYSTEM_PROMPT = """
You are an expert Document Q&A Assistant.
Answer the user's question STRICTLY and ONLY based on the context snippets provided below.

CRITICAL INSTRUCTIONS:
1. Ground every claim directly in the provided context.
2. If the context does not contain the answer, explicitly state: "Based on the provided documents, I could not find the answer to this question."
3. Do NOT make up, assume, or hallucinate information outside the provided text.
4. Keep the answer clear, professional, and factual.
"""

RAG_USER_TEMPLATE = """
### CONTEXT FROM DOCUMENTS:
{context}

### USER QUESTION:
{question}

### GROUNDED ANSWER:
"""


class GroundedRAGChain:
    """RAG chain enforcing strict context grounding and source page citations."""

    def __init__(
        self,
        vector_store: ChromaVectorStore,
        llm_provider: Optional[str] = None,
        top_k: int = 3,
    ):
        self.vector_store = vector_store
        self.top_k = top_k
        self.llm_provider = (
            llm_provider
            or os.getenv("DEFAULT_LLM_PROVIDER")
            or ("gemini" if os.getenv("GEMINI_API_KEY") else ("openai" if os.getenv("OPENAI_API_KEY") else "local"))
        ).lower()

    def _format_context(self, documents: List[Document]) -> str:
        """Formats retrieved documents into a labeled context block."""
        parts = []
        for idx, doc in enumerate(documents, 1):
            source = doc.metadata.get("source_file", "Document")
            page = doc.metadata.get("page_number", 1)
            parts.append(f"[Snippet {idx} | Source: {source} | Page: {page}]\n{doc.page_content.strip()}")
        return "\n\n".join(parts)

    def _extract_citations(self, documents: List[Document]) -> List[SourceCitation]:
        """Extracts unique source citations with page numbers and excerpts."""
        citations = []
        seen = set()

        for doc in documents:
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page_number", 1)
            key = (source, page)

            if key not in seen:
                seen.add(key)
                clean_text = doc.page_content.replace("\n", " ").strip()
                excerpt = (clean_text[:140] + "...") if len(clean_text) > 140 else clean_text
                citations.append(SourceCitation(source_file=source, page_number=page, excerpt=excerpt))

        return citations

    def _generate_answer(self, context_str: str, question: str) -> str:
        """Dispatches question + context to selected LLM or local grounded extractor."""
        if not context_str.strip():
            return "Based on the provided documents, I could not find the answer to this question."

        user_prompt = RAG_USER_TEMPLATE.format(context=context_str, question=question)

        # Gemini
        if self.llm_provider == "gemini" and (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
            try:
                from google import genai
                client = genai.Client(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
                resp = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_prompt,
                    config={"system_instruction": RAG_SYSTEM_PROMPT, "temperature": 0.0},
                )
                if resp.text:
                    return resp.text.strip()
            except Exception as e:
                logger.warning(f"Gemini call error: {e}. Falling back to local grounded response.")

        # OpenAI
        if self.llm_provider == "openai" and os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": RAG_SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.0,
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                logger.warning(f"OpenAI call error: {e}. Falling back to local grounded response.")

        # Local Grounded Extractor (Deterministic Offline Fallback)
        return self._local_grounded_answer(context_str, question)

    def _local_grounded_answer(self, context: str, question: str) -> str:
        """
        Synthesizes a strictly grounded answer from matching sentences in retrieved context
        when running locally without active cloud API keys.
        """
        # Clean context: strip snippet tags and normalize whitespace
        cleaned_context = re.sub(r"\[Snippet \d+ \|[^\]]+\]", "", context)
        cleaned_context = cleaned_context.replace("—", " - ").replace("–", " - ").strip()

        q_words = set(re.findall(r"\w+", question.lower()))
        stop_words = {"what", "is", "the", "are", "how", "for", "in", "of", "and", "to", "a", "an", "does", "do", "when", "with"}
        key_words = q_words - stop_words

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned_context) if s.strip()]
        scored_sentences = []

        for sent in sentences:
            s_words = set(re.findall(r"\w+", sent.lower()))
            overlap = len(key_words & s_words)
            if overlap > 0:
                scored_sentences.append((overlap, sent))

        scored_sentences.sort(key=lambda x: x[0], reverse=True)

        if not scored_sentences:
            return "Based on the provided documents, I could not find the answer to this question."

        # Return top matching unique sentences
        top_sentences = []
        for _, s in scored_sentences[:2]:
            if s not in top_sentences:
                top_sentences.append(s)

        return " ".join(top_sentences)

    def answer_question(self, question: str) -> RAGAnswer:
        """Executes full RAG workflow: Retrieve -> Augment -> Generate -> Cite."""
        retrieved_docs = self.vector_store.similarity_search(question, k=self.top_k)
        context_str = self._format_context(retrieved_docs)
        answer_text = self._generate_answer(context_str, question)
        citations = self._extract_citations(retrieved_docs)

        return RAGAnswer(
            question=question,
            answer=answer_text,
            citations=citations,
            source_documents=retrieved_docs,
        )
