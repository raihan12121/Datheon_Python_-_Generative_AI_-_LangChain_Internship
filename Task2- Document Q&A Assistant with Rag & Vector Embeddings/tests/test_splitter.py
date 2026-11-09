"""
Unit tests for RAGTextSplitter module.
"""

import unittest
from langchain_core.documents import Document
from core.text_splitter import RAGTextSplitter


class TestRAGTextSplitter(unittest.TestCase):
    def setUp(self):
        self.splitter = RAGTextSplitter(chunk_size=100, chunk_overlap=20)
        self.sample_doc = Document(
            page_content="Sentence one is here. Sentence two is longer and provides details. Sentence three completes this paragraph with more information.",
            metadata={"source_file": "test.pdf", "page_number": 2},
        )

    def test_chunking_creates_multiple_chunks(self):
        chunks = self.splitter.split_documents([self.sample_doc])
        self.assertTrue(len(chunks) > 1)
        for chunk in chunks:
            self.assertEqual(chunk.metadata["page_number"], 2)
            self.assertEqual(chunk.metadata["source_file"], "test.pdf")
            self.assertIn("citation_label", chunk.metadata)


if __name__ == "__main__":
    unittest.main()
