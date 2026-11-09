"""
Prompts module exports.
"""

from prompts.few_shot_examples import (
    INVOICE_FEW_SHOT_INPUT,
    INVOICE_FEW_SHOT_OUTPUT,
    RESUME_FEW_SHOT_INPUT,
    RESUME_FEW_SHOT_OUTPUT,
)
from prompts.templates import (
    ParameterizedPromptTemplate,
    get_invoice_prompt_template,
    get_resume_prompt_template,
)

__all__ = [
    "ParameterizedPromptTemplate",
    "get_invoice_prompt_template",
    "get_resume_prompt_template",
    "INVOICE_FEW_SHOT_INPUT",
    "INVOICE_FEW_SHOT_OUTPUT",
    "RESUME_FEW_SHOT_INPUT",
    "RESUME_FEW_SHOT_OUTPUT",
]
