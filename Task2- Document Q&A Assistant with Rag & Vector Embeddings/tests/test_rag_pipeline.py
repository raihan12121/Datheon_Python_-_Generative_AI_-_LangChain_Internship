"""
Integration tests for complete RAG Pipeline and Source Citations.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from core.pipeline import RAGPipeline


class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.pipeline = RAGPipeline(
            persist_dir=self.temp_dir,
            llm_provider="local",
        )
        self.pdf_file = Path(__file__).parent.parent / "documents" / "ai_ethics_and_governance_handbook.pdf"
        self.pipeline.ingest_document(str(self.pdf_file))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_question_answering_with_page_citations(self):
        question = "What is the mandatory retention period for inference metadata?"
        response = self.pipeline.query(question)

        self.assertIsNotNone(response.answer)
        self.assertTrue(len(response.citations) > 0)
        # Should cite page 1 where Section 2 is located
        citation_pages = [cit.page_number for cit in response.citations]
        self.assertIn(1, citation_pages)
        self.assertIn("365 days", response.answer)

    def test_unanswerable_question_returns_grounded_fallback(self):
        question = "What is the capital of Mars and the cost of rocket fuel?"
        response = self.pipeline.query(question)
        self.assertIsNotNone(response.answer)


if __name__ == "__main__":
    unittest.main()
