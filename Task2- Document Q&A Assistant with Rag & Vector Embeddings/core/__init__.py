"""
Core module exports for Document Q&A RAG Assistant.
"""

from core.document_loader import DocumentLoader
from core.text_splitter import RAGTextSplitter
from core.embeddings import (
    LocalChromaEmbeddings,
    GeminiEmbeddings,
    OpenAIEmbeddingsModel,
    get_embeddings_generator,
)
from core.vector_store import ChromaVectorStore
from core.qa_chain import GroundedRAGChain, RAGAnswer, SourceCitation
from core.pipeline import RAGPipeline

__all__ = [
    "DocumentLoader",
    "RAGTextSplitter",
    "LocalChromaEmbeddings",
    "GeminiEmbeddings",
    "OpenAIEmbeddingsModel",
    "get_embeddings_generator",
    "ChromaVectorStore",
    "GroundedRAGChain",
    "RAGAnswer",
    "SourceCitation",
    "RAGPipeline",
]
