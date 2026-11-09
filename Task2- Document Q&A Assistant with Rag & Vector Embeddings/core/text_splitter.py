"""
Recursive text chunking with metadata preservation.
"""

from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGTextSplitter:
    """Configurable recursive character text splitter."""

    def __init__(
        self,
        chunk_size: int = 750,
        chunk_overlap: int = 150,
        separators: List[str] = None,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Splits documents into overlapping chunks while preserving source & page metadata."""
        chunks = self._splitter.split_documents(documents)

        # Annotate each chunk with a unique chunk_id
        for idx, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = idx
            page_num = chunk.metadata.get("page_number", 1)
            source = chunk.metadata.get("source_file", "unknown")
            chunk.metadata["citation_label"] = f"{source} (Page {page_num})"

        return chunks
