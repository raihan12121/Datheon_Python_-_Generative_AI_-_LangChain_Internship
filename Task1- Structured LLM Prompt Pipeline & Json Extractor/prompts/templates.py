"""
Parameterized Prompt Templates with Few-Shot Injection and Strict JSON Schema Enforcement.
"""

import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
from prompts.few_shot_examples import (
    INVOICE_FEW_SHOT_INPUT,
    INVOICE_FEW_SHOT_OUTPUT,
    RESUME_FEW_SHOT_INPUT,
    RESUME_FEW_SHOT_OUTPUT,
)


class ParameterizedPromptTemplate:
    """Base class for parameterized prompt generation with few-shot exemplars and JSON schema anchoring."""

    def __init__(
        self,
        system_instruction: str,
        user_template: str,
        few_shot_input: Optional[str] = None,
        few_shot_output: Optional[Dict[str, Any]] = None,
    ):
        self.system_instruction = system_instruction.strip()
        self.user_template = user_template.strip()
        self.few_shot_input = few_shot_input
        self.few_shot_output = few_shot_output

    def format_system_prompt(self, pydantic_model: Optional[type[BaseModel]] = None) -> str:
        """Construct the system instruction including JSON schema rules."""
        schema_clause = ""
        if pydantic_model:
            schema_json = json.dumps(pydantic_model.model_json_schema(), indent=2)
            schema_clause = f"\n\nYou MUST adhere strictly to this JSON Schema:\n```json\n{schema_json}\n```"

        return f"{self.system_instruction}{schema_clause}"

    def format_user_prompt(
        self,
        document_text: str,
        include_few_shot: bool = True,
        extra_context: Optional[str] = None,
    ) -> str:
        """Render parameterized prompt with document text, few-shot examples, and custom instructions."""
        parts = []

        if include_few_shot and self.few_shot_input and self.few_shot_output:
            parts.append("### EXAMPLE DEMONSTRATION")
            parts.append("Input Document:")
            parts.append(self.few_shot_input.strip())
            parts.append("\nExtracted Ground-Truth JSON:")
            parts.append(json.dumps(self.few_shot_output, indent=2))
            parts.append("\n--- END OF EXAMPLE ---\n")

        if extra_context:
            parts.append(f"### ADDITIONAL CONTEXT / INSTRUCTIONS:\n{extra_context}\n")

        # Ingest target document using the template
        rendered_target = self.user_template.format(document_text=document_text.strip())
        parts.append(rendered_target)

        return "\n\n".join(parts)


INVOICE_SYSTEM_PROMPT = """
You are an expert Document Understanding and Financial Document Extraction AI.
Your role is to extract all structured data from unstructured corporate invoices, receipts, and billing statements into strictly validated JSON.

RULES:
1. Output MUST be a valid JSON object matching the requested schema.
2. Do NOT output markdown code fences (like ```json), commentary, or explanations. Return ONLY the raw parseable JSON string.
3. Normalize all monetary numbers to float (e.g. "$1,250.00" -> 1250.0).
4. Parse dates into ISO YYYY-MM-DD format whenever unambiguous.
5. If an optional field is missing, set its value to null.
6. Calculate or preserve line item accuracy: total_price = (quantity * unit_price) - discount.
"""

INVOICE_USER_TEMPLATE = """
### TARGET DOCUMENT TO EXTRACT
Please extract all invoice details from the following document into the required JSON structure:

```
{document_text}
```

Return ONLY the completed JSON object.
"""

RESUME_SYSTEM_PROMPT = """
You are an expert Talent Intelligence and Resume Parsing AI.
Your task is to analyze complex unstructured resumes, CVs, and biographical profiles to extract comprehensive candidate information into strictly validated JSON.

RULES:
1. Output MUST be a valid JSON object matching the requested schema.
2. Do NOT output markdown code fences (like ```json), commentary, or notes. Return ONLY the raw parseable JSON string.
3. Categorize technical skills logically (e.g. Languages, Frameworks, Databases, Cloud & DevOps).
4. Dissect each work experience into clear roles, achievements, responsibilities, and technologies used.
5. Identify candidate contact details, educational background, certifications, and projects accurately.
6. If an optional field is not present in the text, set its value to null or an empty list where appropriate.
"""

RESUME_USER_TEMPLATE = """
### TARGET RESUME TO EXTRACT
Please parse the following resume into the required structured JSON format:

```
{document_text}
```

Return ONLY the completed JSON object.
"""


def get_invoice_prompt_template() -> ParameterizedPromptTemplate:
    """Factory for the Invoice prompt template."""
    return ParameterizedPromptTemplate(
        system_instruction=INVOICE_SYSTEM_PROMPT,
        user_template=INVOICE_USER_TEMPLATE,
        few_shot_input=INVOICE_FEW_SHOT_INPUT,
        few_shot_output=INVOICE_FEW_SHOT_OUTPUT,
    )


def get_resume_prompt_template() -> ParameterizedPromptTemplate:
    """Factory for the Resume prompt template."""
    return ParameterizedPromptTemplate(
        system_instruction=RESUME_SYSTEM_PROMPT,
        user_template=RESUME_USER_TEMPLATE,
        few_shot_input=RESUME_FEW_SHOT_INPUT,
        few_shot_output=RESUME_FEW_SHOT_OUTPUT,
    )
