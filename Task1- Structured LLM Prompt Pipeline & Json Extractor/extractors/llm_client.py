"""
Unified Multi-Provider LLM Client.
Supports Google Gemini (via google-genai and google-generativeai) and OpenAI (via openai).
Includes structured JSON mode enforcement, graceful provider fallback, and offline mock capability.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

logger = logging.getLogger("LLMClient")


class LLMClient:
    """Unified wrapper around Gemini and OpenAI APIs with structured JSON output enforcement."""

    def __init__(
        self,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
    ):
        self.gemini_api_key = (
            gemini_api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )
        self.openai_api_key = (
            openai_api_key
            or os.getenv("OPENAI_API_KEY")
        )

        requested_provider = (
            provider
            or os.getenv("DEFAULT_LLM_PROVIDER")
            or ("gemini" if self.gemini_api_key else ("openai" if self.openai_api_key else "gemini"))
        ).lower()

        self.provider = requested_provider
        self.model_name = model_name

    def generate_json_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        max_output_tokens: int = 4096,
    ) -> str:
        """
        Dispatches request to configured LLM provider and returns raw JSON text response.
        """
        if self.provider == "gemini":
            if not self.gemini_api_key:
                logger.warning("No GEMINI_API_KEY detected. Checking OpenAI or mock fallback.")
                if self.openai_api_key:
                    return self._call_openai(system_prompt, user_prompt, temperature, max_output_tokens)
                return self._call_mock_fallback(user_prompt)
            return self._call_gemini(system_prompt, user_prompt, temperature, max_output_tokens)

        elif self.provider == "openai":
            if not self.openai_api_key:
                logger.warning("No OPENAI_API_KEY detected. Checking Gemini or mock fallback.")
                if self.gemini_api_key:
                    return self._call_gemini(system_prompt, user_prompt, temperature, max_output_tokens)
                return self._call_mock_fallback(user_prompt)
            return self._call_openai(system_prompt, user_prompt, temperature, max_output_tokens)

        elif self.provider == "mock":
            return self._call_mock_fallback(user_prompt)

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}. Use 'gemini' or 'openai'.")

    def _call_gemini(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_output_tokens: int,
    ) -> str:
        """Call Google Gemini API using google-genai or google-generativeai."""
        model = self.model_name or os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"
        
        # Try google.genai (new SDK) first
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=self.gemini_api_key)
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            )
            response = client.models.generate_content(
                model=model,
                contents=user_prompt,
                config=config,
            )
            if response.text:
                return response.text
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"google.genai call encountered error: {e}. Trying google.generativeai fallback.")

        # Fallback to google.generativeai (classic SDK)
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=self.gemini_api_key)
            gen_model = legacy_genai.GenerativeModel(
                model_name=self.model_name or "gemini-1.5-flash",
                system_instruction=system_prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": temperature,
                    "max_output_tokens": max_output_tokens,
                },
            )
            response = gen_model.generate_content(user_prompt)
            if response.text:
                return response.text
        except Exception as e:
            logger.error(f"Gemini API execution failed: {e}")
            raise RuntimeError(f"Gemini API request failed: {e}")

        raise RuntimeError("No response returned from Gemini API.")

    def _call_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_output_tokens: int,
    ) -> str:
        """Call OpenAI Chat Completions API with JSON mode."""
        from openai import OpenAI

        model = self.model_name or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
        client = OpenAI(api_key=self.openai_api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=temperature,
            max_tokens=max_output_tokens,
        )

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("Received empty response from OpenAI.")
        return content

    def _call_mock_fallback(self, user_prompt: str) -> str:
        """
        Deterministic mock extractor fallback when no active API key is set in .env.
        Enables seamless local dry-run, testing, and portfolio demonstration.
        """
        logger.info("[Mock LLM Fallback] Simulating structured extraction without live API key...")

        # Detect whether target document is an invoice or resume based on keywords
        prompt_lower = user_prompt.lower()
        if "invoice" in prompt_lower or "bill to" in prompt_lower or "subtotal" in prompt_lower or "payable" in prompt_lower:
            mock_data = {
                "invoice_number": "INV-2024-9102",
                "invoice_date": "2024-11-04",
                "due_date": "2024-12-04",
                "purchase_order_number": "PO-44810",
                "currency": "USD",
                "vendor": {
                    "name": "Apex Digital Logistics Inc.",
                    "tax_id": "US-88410294",
                    "email": "finance@apexdigital.example.com",
                    "phone": "+1-800-555-0144",
                    "address": "450 Industrial Parkway, Suite 200, Dallas, TX 75201"
                },
                "customer": {
                    "name": "Global Retail Partners Ltd.",
                    "tax_id": "EU-3310948",
                    "email": "invoicing@globalretail.example.com",
                    "phone": "+1-212-555-0182",
                    "billing_address": "742 Evergreen Terrace, New York, NY 10001",
                    "shipping_address": "Warehouse 4, 12 Pier Rd, Elizabeth, NJ 07201"
                },
                "line_items": [
                    {
                        "item_code": "SRV-CLOUD-MIG",
                        "description": "Multi-Region Cloud Infrastructure Migration",
                        "quantity": 1.0,
                        "unit_price": 4500.0,
                        "discount": 500.0,
                        "total_price": 4000.0
                    },
                    {
                        "item_code": "SRV-AI-OPS",
                        "description": "24/7 AI-driven Observability and Monitoring",
                        "quantity": 2.0,
                        "unit_price": 750.0,
                        "discount": 0.0,
                        "total_price": 1500.0
                    }
                ],
                "subtotal": 5500.0,
                "tax_rate_percent": 8.0,
                "tax_amount": 440.0,
                "shipping_fee": 0.0,
                "discount_amount": 500.0,
                "total_amount": 5940.0,
                "payment": {
                    "payment_method": "Wire Transfer",
                    "bank_name": "Chase Manhattan Bank",
                    "account_number": "10492847291",
                    "routing_or_swift": "CHASUS33",
                    "payment_terms": "Net 30"
                },
                "notes_or_terms": "Payment due within 30 days of invoice date."
            }
            return json.dumps(mock_data)

        else:
            # Resume mock fallback
            mock_data = {
                "candidate": {
                    "full_name": "Elena Rostova",
                    "email": "elena.rostova@engineer.net",
                    "phone": "+1-206-555-0177",
                    "location": "Seattle, WA",
                    "linkedin_url": "https://linkedin.com/in/elena-rostova-dev",
                    "github_url": "https://github.com/elena-rostova",
                    "portfolio_url": "https://elenarostova.dev"
                },
                "professional_summary": "Lead Machine Learning Engineer with 6 years of expertise in NLP, agentic workflows, LLM fine-tuning, and scalable inference infrastructure.",
                "total_years_experience": 6.0,
                "work_experience": [
                    {
                        "company": "NeuralGrid Technologies",
                        "role_title": "Lead ML Engineer",
                        "location": "Seattle, WA",
                        "start_date": "2021-03",
                        "end_date": "Present",
                        "is_current": True,
                        "responsibilities": [
                            "Lead a team of 6 engineers developing LLM reasoning pipelines",
                            "Optimized PyTorch inference latency by 45% using TensorRT and vLLM"
                        ],
                        "key_achievements": [
                            "Scaled vector database search across 50M embeddings with sub-50ms latency",
                            "Reduced model deployment cycle from 2 weeks to 2 hours"
                        ],
                        "technologies_used": ["Python", "PyTorch", "vLLM", "Docker", "Kubernetes", "PostgreSQL", "GCP"]
                    }
                ],
                "education": [
                    {
                        "institution": "University of Washington",
                        "degree": "Master of Science",
                        "field_of_study": "Computer Science & Engineering",
                        "start_year": "2017",
                        "graduation_year": "2019",
                        "gpa": "3.91 / 4.0",
                        "honors": ["Graduate Fellowship Award"]
                    }
                ],
                "skills": [
                    {
                        "category": "Languages",
                        "skills": ["Python", "C++", "SQL", "Go"]
                    },
                    {
                        "category": "Machine Learning & AI",
                        "skills": ["PyTorch", "Hugging Face", "LangChain", "vLLM", "TensorRT", "FAISS"]
                    },
                    {
                        "category": "Cloud & Infrastructure",
                        "skills": ["Docker", "Kubernetes", "GCP Vertex AI", "AWS SageMaker", "Terraform"]
                    }
                ],
                "projects": [
                    {
                        "title": "AgenticCodeReviewer",
                        "description": "Multi-agent repository review system catching semantic bugs using AST analysis and LLMs.",
                        "role": "Creator & Lead Maintainer",
                        "technologies": ["Python", "AST", "LangChain"],
                        "github_or_live_url": "https://github.com/elena-rostova/agentic-reviewer"
                    }
                ],
                "certifications": [
                    {
                        "name": "AWS Certified Machine Learning - Specialty",
                        "issuing_organization": "Amazon Web Services",
                        "issue_date": "2023",
                        "credential_id_or_url": "AWS-MLS-88219"
                    }
                ],
                "languages": ["English", "Russian", "German"]
            }
            return json.dumps(mock_data)
