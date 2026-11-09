"""
Persistent ChromaDB Vector Store management for indexing, persistence, and semantic retrieval.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Tuple, Optional
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma

logger = logging.getLogger("RAGVectorStore")


class ChromaVectorStore:
    """Manages persistent ChromaDB vector store collections for RAG."""

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: str = "datheon_rag_documents",
        embedding_function: Optional[Embeddings] = None,
    ):
        if not persist_directory:
            base_dir = Path(__file__).parent.parent
            persist_directory = str(base_dir / "chroma_db")

        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_function = embedding_function

        # Initialize or load existing collection
        self._vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_function,
            persist_directory=self.persist_directory,
        )

    @property
    def vector_store(self) -> Chroma:
        return self._vector_store

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Indexes document chunks into ChromaDB."""
        if not documents:
            return []
        ids = self._vector_store.add_documents(documents)
        logger.info(f"Indexed {len(documents)} chunks into collection '{self.collection_name}'.")
        return ids

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Retrieves top-k most similar document chunks."""
        return self._vector_store.similarity_search(query, k=k)

    def similarity_search_with_scores(self, query: str, k: int = 3) -> List[Tuple[Document, float]]:
        """Retrieves top-k chunks along with cosine similarity/distance scores."""
        return self._vector_store.similarity_search_with_score(query, k=k)

    def max_marginal_relevance_search(self, query: str, k: int = 3, fetch_k: int = 10) -> List[Document]:
        """Retrieves diverse chunks using Maximal Marginal Relevance (MMR)."""
        return self._vector_store.max_marginal_relevance_search(query, k=k, fetch_k=fetch_k)

    def as_retriever(self, search_type: str = "similarity", k: int = 3):
        """Returns a LangChain compatible retriever."""
        return self._vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k},
        )

    def reset_collection(self):
        """Clears all vectors and recreates the collection."""
        try:
            self._vector_store.delete_collection()
            if os.path.exists(self.persist_directory):
                shutil.rmtree(self.persist_directory, ignore_errors=True)
            logger.info("Chroma collection reset successfully.")
        except Exception as e:
            logger.warning(f"Error resetting collection: {e}")

        # Re-initialize
        self._vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_function,
            persist_directory=self.persist_directory,
        )
