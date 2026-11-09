"""
Unit and integration tests for extraction pipeline, prompt generation, and JSON cleaning.
"""

import unittest
from extractors.llm_client import LLMClient
from extractors.pipeline import StructuredExtractionPipeline
from prompts.templates import get_invoice_prompt_template, get_resume_prompt_template
from schemas.invoice_schema import InvoiceData
from schemas.resume_schema import ResumeData


class TestExtractionPipeline(unittest.TestCase):
    def setUp(self):
        self.mock_client = LLMClient(provider="mock")
        self.pipeline = StructuredExtractionPipeline(llm_client=self.mock_client)

    def test_json_cleaner_removes_markdown_blocks(self):
        raw_markdown = '```json\n{"invoice_number": "INV-100", "subtotal": 100.0}\n```'
        cleaned = StructuredExtractionPipeline.clean_json_string(raw_markdown)
        self.assertEqual(cleaned, '{"invoice_number": "INV-100", "subtotal": 100.0}')

    def test_json_cleaner_extracts_from_prose(self):
        prose_with_json = 'Here is your extracted output:\n{"invoice_number": "INV-100"}\nThank you!'
        cleaned = StructuredExtractionPipeline.clean_json_string(prose_with_json)
        self.assertEqual(cleaned, '{"invoice_number": "INV-100"}')

    def test_prompt_template_formatting(self):
        template = get_invoice_prompt_template()
        system_p = template.format_system_prompt(pydantic_model=InvoiceData)
        user_p = template.format_user_prompt(
            document_text="Vendor: Acme Inc. Total: $500",
            include_few_shot=True,
        )
        self.assertIn("JSON Schema", system_p)
        self.assertIn("EXAMPLE DEMONSTRATION", user_p)
        self.assertIn("Acme Inc.", user_p)

    def test_mock_invoice_extraction_pipeline(self):
        sample_text = "Urgent invoice INV-2024-9102 from Apex Digital Logistics Inc. Total: $5,940.00"
        result = self.pipeline.extract_invoice(sample_text)
        self.assertIsInstance(result, InvoiceData)
        self.assertEqual(result.invoice_number, "INV-2024-9102")
        self.assertEqual(result.vendor.name, "Apex Digital Logistics Inc.")
        self.assertEqual(result.total_amount, 5940.0)

    def test_mock_resume_extraction_pipeline(self):
        sample_text = "Elena Rostova, Lead ML Engineer with 6 years experience in NLP and PyTorch."
        result = self.pipeline.extract_resume(sample_text)
        self.assertIsInstance(result, ResumeData)
        self.assertEqual(result.candidate.full_name, "Elena Rostova")
        self.assertEqual(result.total_years_experience, 6.0)
        self.assertTrue(len(result.work_experience) > 0)


if __name__ == "__main__":
    unittest.main()
