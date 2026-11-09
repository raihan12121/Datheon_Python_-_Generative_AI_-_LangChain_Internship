"""
Core Structured Extraction Pipeline.
Orchestrates prompt formatting, LLM execution, JSON sanitization,
Pydantic validation, error recovery, and serialization.
"""

import re
import json
import logging
from typing import Type, TypeVar, Optional, Tuple, Dict, Any
from pydantic import BaseModel, ValidationError

from schemas.invoice_schema import InvoiceData
from schemas.resume_schema import ResumeData
from prompts.templates import (
    ParameterizedPromptTemplate,
    get_invoice_prompt_template,
    get_resume_prompt_template,
)
from extractors.llm_client import LLMClient

logger = logging.getLogger("ExtractionPipeline")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

T = TypeVar("T", bound=BaseModel)


class StructuredExtractionPipeline:
    """
    End-to-end pipeline extracting validated structured data from unstructured text
    using parameterized prompts and strict Pydantic models.
    """

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()

    @staticmethod
    def clean_json_string(raw_text: str) -> str:
        """
        Strips markdown code blocks, extraneous whitespace, and trailing commas from LLM output.
        """
        text = raw_text.strip()
        # Remove markdown code fences e.g. ```json ... ```
        if "```" in text:
            # Look for content within ```json ... ``` or ``` ... ```
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
            if match:
                text = match.group(1).strip()
            else:
                text = text.replace("```json", "").replace("```", "").strip()

        # Find first '{' or '[' and last '}' or ']'
        start_idx = -1
        for idx, char in enumerate(text):
            if char in ("{", "["):
                start_idx = idx
                break

        end_idx = -1
        for idx in range(len(text) - 1, -1, -1):
            if text[idx] in ("}", "]"):
                end_idx = idx + 1
                break

        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            text = text[start_idx:end_idx]

        return text

    def extract(
        self,
        document_text: str,
        template: ParameterizedPromptTemplate,
        schema_model: Type[T],
        include_few_shot: bool = True,
        extra_context: Optional[str] = None,
        max_retries: int = 2,
    ) -> T:
        """
        Executes structured extraction pipeline on unstructured document text with automatic error recovery.
        """
        system_prompt = template.format_system_prompt(pydantic_model=schema_model)
        user_prompt = template.format_user_prompt(
            document_text=document_text,
            include_few_shot=include_few_shot,
            extra_context=extra_context,
        )

        last_error = None
        current_user_prompt = user_prompt

        for attempt in range(1, max_retries + 1):
            logger.info(f"Extracting structured entity using {self.llm_client.provider.upper()} (Attempt {attempt}/{max_retries})...")
            try:
                raw_response = self.llm_client.generate_json_response(
                    system_prompt=system_prompt,
                    user_prompt=current_user_prompt,
                )

                cleaned_json_str = self.clean_json_string(raw_response)

                # Attempt validation
                validated_model = schema_model.model_validate_json(cleaned_json_str)
                logger.info(f"Successfully validated output against {schema_model.__name__}!")
                return validated_model

            except (ValidationError, json.JSONDecodeError) as e:
                last_error = e
                logger.warning(f"Validation attempt {attempt} failed: {e}")

                if attempt < max_retries:
                    # Self-correction prompt for retry
                    current_user_prompt = (
                        f"{user_prompt}\n\n"
                        f"### PREVIOUS ATTEMPT FAILED WITH ERROR:\n{str(e)}\n"
                        f"Please rectify the JSON according to the schema rules and return ONLY valid JSON."
                    )

        raise RuntimeError(
            f"Failed to extract and validate {schema_model.__name__} after {max_retries} attempts. Last error: {last_error}"
        )

    def extract_invoice(
        self,
        document_text: str,
        include_few_shot: bool = True,
        extra_context: Optional[str] = None,
    ) -> InvoiceData:
        """Extract validated InvoiceData from raw text."""
        template = get_invoice_prompt_template()
        return self.extract(
            document_text=document_text,
            template=template,
            schema_model=InvoiceData,
            include_few_shot=include_few_shot,
            extra_context=extra_context,
        )

    def extract_resume(
        self,
        document_text: str,
        include_few_shot: bool = True,
        extra_context: Optional[str] = None,
    ) -> ResumeData:
        """Extract validated ResumeData from raw text."""
        template = get_resume_prompt_template()
        return self.extract(
            document_text=document_text,
            template=template,
            schema_model=ResumeData,
            include_few_shot=include_few_shot,
            extra_context=extra_context,
        )
