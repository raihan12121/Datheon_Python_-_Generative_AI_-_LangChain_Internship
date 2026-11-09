"""
Structured LLM Prompt Pipeline & JSON Extractor - CLI & Executable Runner.

Usage Examples:
  python main.py --demo
  python main.py --type invoice --file sample_inputs/invoice_sample_1.txt
  python main.py --type resume --file sample_inputs/resume_sample_1.txt
  python main.py --type invoice --file sample_inputs/invoice_sample_2.txt --provider gemini
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extractors.llm_client import LLMClient
from extractors.pipeline import StructuredExtractionPipeline
from schemas.invoice_schema import InvoiceData
from schemas.resume_schema import ResumeData


def print_banner():
    banner = """
========================================================================
    STRUCTURED LLM PROMPT PIPELINE & JSON EXTRACTOR
    Strict Pydantic Schema Enforcement with Parameterized Few-Shot Prompts
========================================================================
"""
    print(banner)


def save_output(data: dict, output_path: str):
    """Save dictionary to formatted JSON file."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n[+] Extracted JSON saved to: {out_file.resolve()}")


def process_document(
    doc_type: str,
    file_path: str,
    provider: Optional[str] = None,
    output_path: Optional[str] = None,
    include_few_shot: bool = True,
):
    """Processes a single unstructured text document and validates output with Pydantic."""
    path = Path(file_path)
    if not path.is_file():
        print(f"[!] Error: File not found: {file_path}")
        sys.exit(1)

    print(f"[*] Reading document: {path.name} (Type: {doc_type.upper()})")
    with open(path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    client = LLMClient(provider=provider)
    pipeline = StructuredExtractionPipeline(llm_client=client)

    print(f"[*] Invoking extraction pipeline with LLM Provider: '{client.provider}'...")
    print(f"[*] Parameterized few-shot exemplars enabled: {include_few_shot}")

    if doc_type.lower() == "invoice":
        result_model: InvoiceData = pipeline.extract_invoice(
            document_text=raw_text,
            include_few_shot=include_few_shot,
        )
        data_dict = result_model.model_dump()

        print("\n" + "=" * 50)
        print("          EXTRACTED INVOICE SUMMARY")
        print("=" * 50)
        print(f"  Invoice Number : {result_model.invoice_number}")
        print(f"  Invoice Date   : {result_model.invoice_date}")
        print(f"  Due Date       : {result_model.due_date}")
        print(f"  Vendor Name    : {result_model.vendor.name} ({result_model.vendor.email or 'N/A'})")
        print(f"  Customer Name  : {result_model.customer.name}")
        print(f"  Line Items Count: {len(result_model.line_items)}")
        for idx, item in enumerate(result_model.line_items, 1):
            print(f"    - [{idx}] {item.description} (Qty: {item.quantity} @ ${item.unit_price:.2f}) -> ${item.total_price:.2f}")
        print(f"  Subtotal       : ${result_model.subtotal:.2f}")
        print(f"  Tax Amount     : ${result_model.tax_amount:.2f} ({result_model.tax_rate_percent or 0}%)")
        print(f"  Discount       : ${result_model.discount_amount:.2f}")
        print(f"  TOTAL PAYABLE  : ${result_model.total_amount:.2f} {result_model.currency}")
        print("=" * 50)

    elif doc_type.lower() == "resume":
        result_model: ResumeData = pipeline.extract_resume(
            document_text=raw_text,
            include_few_shot=include_few_shot,
        )
        data_dict = result_model.model_dump()

        print("\n" + "=" * 50)
        print("           EXTRACTED RESUME SUMMARY")
        print("=" * 50)
        print(f"  Candidate Name : {result_model.candidate.full_name}")
        print(f"  Email Address  : {result_model.candidate.email}")
        print(f"  Phone Number   : {result_model.candidate.phone}")
        print(f"  Location       : {result_model.candidate.location}")
        print(f"  LinkedIn / Web : {result_model.candidate.linkedin_url or result_model.candidate.portfolio_url}")
        print(f"  Experience Yrs : {result_model.total_years_experience or 'N/A'}")
        print(f"  Summary        : {result_model.professional_summary[:120]}..." if result_model.professional_summary else "  Summary: N/A")
        print(f"  Work Roles     : {len(result_model.work_experience)}")
        for exp in result_model.work_experience:
            status = "(Current)" if exp.is_current else ""
            print(f"    - {exp.role_title} @ {exp.company} {status} [{exp.start_date} - {exp.end_date}]")
        print(f"  Degrees        : {len(result_model.education)}")
        for edu in result_model.education:
            print(f"    - {edu.degree} in {edu.field_of_study} ({edu.institution}, {edu.graduation_year})")
        print(f"  Skill Groups   : {len(result_model.skills)}")
        for sg in result_model.skills:
            print(f"    - {sg.category}: {', '.join(sg.skills[:6])}")
        print(f"  Projects       : {len(result_model.projects)}")
        print(f"  Certifications : {len(result_model.certifications)}")
        print("=" * 50)
    else:
        raise ValueError(f"Unknown document type: {doc_type}. Must be 'invoice' or 'resume'.")

    # Determine default destination
    if not output_path:
        out_name = f"{path.stem}_extracted.json"
        output_path = os.path.join(os.path.dirname(__file__), "outputs", out_name)

    save_output(data_dict, output_path)
    return result_model


def run_demo(provider: Optional[str] = None):
    """Executes full automated demonstration across invoice and resume samples."""
    print("[*] Running Complete Extraction Pipeline Demonstration...\n")

    base_dir = Path(__file__).parent
    samples = [
        ("invoice", base_dir / "sample_inputs" / "invoice_sample_1.txt"),
        ("resume", base_dir / "sample_inputs" / "resume_sample_1.txt"),
    ]

    for doc_type, sample_path in samples:
        print(f"\n>>> Running Demo for Document Type: {doc_type.upper()}")
        process_document(
            doc_type=doc_type,
            file_path=str(sample_path),
            provider=provider,
            include_few_shot=True,
        )

    print("\n[SUCCESS] Demo completed successfully! All entities validated against Pydantic schemas.")


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Structured LLM Prompt Pipeline & JSON Extractor for Invoices and Resumes."
    )
    parser.add_argument(
        "--type",
        choices=["invoice", "resume"],
        help="Type of document to parse ('invoice' or 'resume')",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to the unstructured text document to extract",
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai", "offline", "mock"],
        default=None,
        help="LLM provider override ('gemini', 'openai', or 'offline')",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output file path for the extracted JSON",
    )
    parser.add_argument(
        "--no-few-shot",
        action="store_true",
        help="Disable few-shot exemplars in prompt",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run full end-to-end demo parsing both invoice and resume samples",
    )

    args = parser.parse_args()

    if args.demo:
        run_demo(provider=args.provider)
    elif args.type and args.file:
        process_document(
            doc_type=args.type,
            file_path=args.file,
            provider=args.provider,
            output_path=args.output,
            include_few_shot=not args.no_few_shot,
        )
    else:
        print("[!] No action specified. Running demo by default.")
        print("    Tip: Run with --help to see custom CLI options.")
        run_demo(provider=args.provider)


if __name__ == "__main__":
    main()
