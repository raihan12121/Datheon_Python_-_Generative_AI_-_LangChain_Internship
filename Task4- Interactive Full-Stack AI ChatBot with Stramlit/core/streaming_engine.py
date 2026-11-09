"""
Real-time Token Streaming Engine supporting Gemini, OpenAI, and Local Fallback Generators.
"""

import os
import time
import logging
from typing import Generator, List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("StreamingEngine")


class StreamingEngine:
    """Manages real-time streaming token generation for Streamlit chat."""

    def __init__(self, provider: Optional[str] = None, model_name: Optional[str] = None):
        self.gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

        requested = (
            provider
            or os.getenv("DEFAULT_LLM_PROVIDER")
            or ("gemini" if self.gemini_key else ("openai" if self.openai_key else "local"))
        ).lower()

        self.provider = requested
        self.model_name = model_name

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str = "You are an intelligent, helpful Datheon AI Assistant.",
        temperature: float = 0.3,
    ) -> Generator[str, None, None]:
        """Yields streaming tokens as they arrive from the active LLM provider."""
        if self.provider == "gemini" and self.gemini_key:
            yield from self._stream_gemini(messages, system_instruction, temperature)
        elif self.provider == "openai" and self.openai_key:
            yield from self._stream_openai(messages, system_instruction, temperature)
        else:
            yield from self._stream_local(messages)

    def _stream_gemini(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        temperature: float,
    ) -> Generator[str, None, None]:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.gemini_key)
            model = self.model_name or "gemini-2.5-flash"

            # Format history for Gemini
            contents = []
            for m in messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
            )

            stream = client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=config,
            )

            for chunk in stream:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.warning(f"Gemini streaming error: {e}. Falling back to local streaming.")
            yield from self._stream_local(messages)

    def _stream_openai(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        temperature: float,
    ) -> Generator[str, None, None]:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.openai_key)
            model = self.model_name or "gpt-4o-mini"

            formatted_msgs = [{"role": "system", "content": system_instruction}]
            for m in messages:
                formatted_msgs.append({"role": m["role"], "content": m["content"]})

            response = client.chat.completions.create(
                model=model,
                messages=formatted_msgs,
                temperature=temperature,
                stream=True,
            )

            for chunk in response:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content

        except Exception as e:
            logger.warning(f"OpenAI streaming error: {e}. Falling back to local streaming.")
            yield from self._stream_local(messages)

    def _stream_local(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """Deterministic local streaming token generator for testing without external API calls."""
        last_user_query = messages[-1]["content"] if messages else "Hello"
        q_lower = last_user_query.lower()

        if "rag" in q_lower or "document" in q_lower or "retention" in q_lower:
            response_text = (
                "Based on the Datheon Enterprise AI Governance policy, all production LLM metadata—including "
                "prompt templates, hyperparameters, and completion timestamps—must be retained for a mandatory "
                "period of 365 days. In addition, user prompts containing Personally Identifiable Information (PII) "
                "must traverse the PII Masking Gateway to ensure zero-day retention on public endpoints."
            )
        elif "agent" in q_lower or "tool" in q_lower or "budget" in q_lower or "calculate" in q_lower:
            response_text = (
                "I am equipped with autonomous tools: DuckDuckGo live search, an AST-evaluated safe math calculator, "
                "and a local filesystem reader. For multi-step queries, I execute a structured ReAct loop: "
                "first gathering local context or web data, evaluating any required mathematical metrics, "
                "and synthesizing a verifiable final answer."
            )
        else:
            response_text = (
                f"Hello! I am your Datheon Full-Stack AI Assistant. I have received your request: '{last_user_query}'. "
                "I am fully integrated with our Knowledge RAG pipeline and Autonomous Tool suite. "
                "Feel free to ask questions about uploaded documents, run calculations, or search the web!"
            )

        # Stream words with slight realistic delay
        for word in response_text.split(" "):
            yield word + " "
            time.sleep(0.02)
