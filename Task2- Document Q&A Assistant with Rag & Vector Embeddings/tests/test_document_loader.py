"""
Unit tests for DocumentLoader module (PDF and TXT loading).
"""

import unittest
from pathlib import Path
from core.document_loader import DocumentLoader


class TestDocumentLoader(unittest.TestCase):
    def setUp(self):
        self.docs_dir = Path(__file__).parent.parent / "documents"
        self.pdf_file = self.docs_dir / "ai_ethics_and_governance_handbook.pdf"
        self.txt_file = self.docs_dir / "cloud_architecture_spec.txt"

    def test_load_pdf_preserves_pages(self):
        docs = DocumentLoader.load(str(self.pdf_file))
        self.assertTrue(len(docs) >= 4, f"Expected 4 pages, got {len(docs)}")
        self.assertEqual(docs[0].metadata["page_number"], 1)
        self.assertEqual(docs[1].metadata["page_number"], 2)
        self.assertEqual(docs[0].metadata["source_file"], "ai_ethics_and_governance_handbook.pdf")

    def test_load_txt(self):
        docs = DocumentLoader.load(str(self.txt_file))
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].metadata["page_number"], 1)
        self.assertIn("Datheon Cloud Infrastructure Specification", docs[0].page_content)

    def test_unsupported_file_raises_value_error(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
            temp_path = f.name
        try:
            with self.assertRaises(ValueError):
                DocumentLoader.load(temp_path)
        finally:
            import os
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
