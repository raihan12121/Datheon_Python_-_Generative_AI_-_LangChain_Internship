"""
High-level RAG Pipeline Orchestrator.
Coordinates document ingestion, chunking, embedding generation, vector storage, and Q&A.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any

from core.document_loader import DocumentLoader
from core.text_splitter import RAGTextSplitter
from core.embeddings import get_embeddings_generator
from core.vector_store import ChromaVectorStore
from core.qa_chain import GroundedRAGChain, RAGAnswer


class RAGPipeline:
    """End-to-end RAG Document Assistant Pipeline."""

    def __init__(
        self,
        persist_dir: Optional[str] = None,
        llm_provider: Optional[str] = None,
        chunk_size: int = 750,
        chunk_overlap: int = 150,
        top_k: int = 3,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.llm_provider = llm_provider

        # Components
        self.loader = DocumentLoader()
        self.splitter = RAGTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        self.embeddings = get_embeddings_generator(provider=self.llm_provider)
        self.vector_store = ChromaVectorStore(
            persist_directory=persist_dir,
            embedding_function=self.embeddings,
        )
        self.qa_chain = GroundedRAGChain(
            vector_store=self.vector_store,
            llm_provider=self.llm_provider,
            top_k=self.top_k,
        )

    def ingest_document(self, file_path: str) -> int:
        """Loads, chunks, and indexes a single document into the vector store."""
        docs = self.loader.load(file_path)
        chunks = self.splitter.split_documents(docs)
        self.vector_store.add_documents(chunks)
        return len(chunks)

    def ingest_directory(self, dir_path: str) -> int:
        """Loads and indexes all documents from a directory."""
        docs = self.loader.load_directory(dir_path)
        chunks = self.splitter.split_documents(docs)
        self.vector_store.add_documents(chunks)
        return len(chunks)

    def query(self, question: str) -> RAGAnswer:
        """Queries the RAG pipeline and returns grounded answer with page citations."""
        return self.qa_chain.answer_question(question)

    def reset_index(self):
        """Clears the persistent vector store index."""
        self.vector_store.reset_collection()
