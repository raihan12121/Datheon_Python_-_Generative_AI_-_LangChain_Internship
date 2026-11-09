"""
Document Loader module supporting PDF, Text, and Markdown documents.
Preserves file source metadata and page numbers for accurate citations.
"""

import os
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


class DocumentLoader:
    """Unified document loader for RAG ingestion."""

    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}

    @classmethod
    def load(cls, file_path: str) -> List[Document]:
        """Loads a document and normalizes page metadata for citations."""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Document not found at: {file_path}")

        ext = path.suffix.lower()
        if ext not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file format '{ext}'. Supported formats: {cls.SUPPORTED_EXTENSIONS}")

        if ext == ".pdf":
            loader = PyPDFLoader(str(path))
            docs = loader.load()
            # Normalize page metadata to 1-indexed page numbers
            for doc in docs:
                raw_page = doc.metadata.get("page", 0)
                doc.metadata["page_number"] = int(raw_page) + 1
                doc.metadata["source_file"] = path.name
                doc.metadata["file_path"] = str(path.resolve())
            return docs

        else:
            # Text / Markdown loader
            loader = TextLoader(str(path), encoding="utf-8")
            docs = loader.load()
            for doc in docs:
                doc.metadata["page_number"] = 1
                doc.metadata["source_file"] = path.name
                doc.metadata["file_path"] = str(path.resolve())
            return docs

    @classmethod
    def load_directory(cls, dir_path: str) -> List[Document]:
        """Loads all supported documents from a directory."""
        path = Path(dir_path)
        if not path.is_dir():
            raise NotADirectoryError(f"Directory not found: {dir_path}")

        all_docs = []
        for file in sorted(path.iterdir()):
            if file.suffix.lower() in cls.SUPPORTED_EXTENSIONS:
                all_docs.extend(cls.load(str(file)))
        return all_docs
