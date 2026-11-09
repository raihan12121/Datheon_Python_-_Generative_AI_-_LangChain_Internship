"""
Unit tests for Pydantic v2 schemas: InvoiceData and ResumeData.
"""

import unittest
from pydantic import ValidationError
from schemas.invoice_schema import InvoiceData, InvoiceLineItem, VendorDetails, CustomerDetails
from schemas.resume_schema import ResumeData, ContactInfo, WorkExperienceEntry, EducationEntry, SkillGroup


class TestInvoiceSchema(unittest.TestCase):
    def setUp(self):
        self.valid_invoice_payload = {
            "invoice_number": "INV-TEST-001",
            "invoice_date": "2024-11-01",
            "due_date": "2024-12-01",
            "currency": "USD",
            "vendor": {
                "name": "Acme Software Corp",
                "tax_id": "VAT-998811",
                "email": "billing@acme.com",
            },
            "customer": {
                "name": "Global Logistics LLC",
                "billing_address": "123 Business Rd, Chicago, IL",
            },
            "line_items": [
                {
                    "item_code": "SKU-01",
                    "description": "Cloud API Subscription",
                    "quantity": "$2.00",  # Tests string currency parsing
                    "unit_price": "$500.00",
                    "discount": "0.0",
                    "total_price": "$1,000.00",
                }
            ],
            "subtotal": "$1,000.00",
            "tax_rate_percent": 10.0,
            "tax_amount": "$100.00",
            "shipping_fee": 0.0,
            "discount_amount": 0.0,
            "total_amount": "$1,100.00",
        }

    def test_valid_invoice_parsing_and_type_coercion(self):
        invoice = InvoiceData.model_validate(self.valid_invoice_payload)
        self.assertEqual(invoice.invoice_number, "INV-TEST-001")
        self.assertEqual(invoice.vendor.name, "Acme Software Corp")
        self.assertEqual(len(invoice.line_items), 1)
        self.assertEqual(invoice.line_items[0].quantity, 2.0)
        self.assertEqual(invoice.line_items[0].unit_price, 500.0)
        self.assertEqual(invoice.subtotal, 1000.0)
        self.assertEqual(invoice.tax_amount, 100.0)
        self.assertEqual(invoice.total_amount, 1100.0)

    def test_missing_required_field_raises_validation_error(self):
        invalid_payload = self.valid_invoice_payload.copy()
        del invalid_payload["invoice_number"]
        with self.assertRaises(ValidationError):
            InvoiceData.model_validate(invalid_payload)


class TestResumeSchema(unittest.TestCase):
    def setUp(self):
        self.valid_resume_payload = {
            "candidate": {
                "full_name": "Jordan Lee",
                "email": "jordan.lee@example.com",
                "phone": "+1-555-0199",
                "location": "New York, NY",
                "github_url": "https://github.com/jordanlee",
            },
            "professional_summary": "Staff Engineer with 7+ years building distributed databases.",
            "total_years_experience": "7.5 years",  # Tests regex string parsing
            "work_experience": [
                {
                    "company": "DataStream Labs",
                    "role_title": "Lead Backend Engineer",
                    "start_date": "2020-01",
                    "end_date": "Present",
                    "is_current": "current",  # Tests bool string coercion
                    "responsibilities": ["Scale database ingestion"],
                    "key_achievements": ["Reduced latency by 40%"],
                    "technologies_used": ["Python", "Go", "PostgreSQL"],
                }
            ],
            "education": [
                {
                    "institution": "Columbia University",
                    "degree": "B.S.",
                    "field_of_study": "Computer Science",
                    "graduation_year": "2016",
                }
            ],
            "skills": [
                {
                    "category": "Languages",
                    "skills": ["Python", "Go", "SQL"],
                }
            ],
            "languages": ["English", "Mandarin"],
        }

    def test_valid_resume_parsing(self):
        resume = ResumeData.model_validate(self.valid_resume_payload)
        self.assertEqual(resume.candidate.full_name, "Jordan Lee")
        self.assertEqual(resume.total_years_experience, 7.5)
        self.assertTrue(resume.work_experience[0].is_current)
        self.assertEqual(len(resume.skills[0].skills), 3)

    def test_invalid_resume_missing_candidate_name(self):
        invalid_payload = {
            "candidate": {"email": "no.name@example.com"}
        }
        with self.assertRaises(ValidationError):
            ResumeData.model_validate(invalid_payload)


if __name__ == "__main__":
    unittest.main()
