"""
Unit tests for ChromaVectorStore module.
"""

import unittest
import tempfile
import shutil
from langchain_core.documents import Document
from core.embeddings import LocalChromaEmbeddings
from core.vector_store import ChromaVectorStore


class TestChromaVectorStore(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.embeddings = LocalChromaEmbeddings()
        self.store = ChromaVectorStore(
            persist_directory=self.temp_dir,
            collection_name="test_collection",
            embedding_function=self.embeddings,
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_indexing_and_similarity_retrieval(self):
        docs = [
            Document(page_content="PostgreSQL database replication recovery point objective is 5 minutes.", metadata={"source_file": "db.txt", "page_number": 1}),
            Document(page_content="The machine learning model must be reviewed by ethics committee.", metadata={"source_file": "ai.pdf", "page_number": 3}),
        ]
        self.store.add_documents(docs)

        results = self.store.similarity_search("database replication RPO", k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("PostgreSQL", results[0].page_content)
        self.assertEqual(results[0].metadata["page_number"], 1)


if __name__ == "__main__":
    unittest.main()
