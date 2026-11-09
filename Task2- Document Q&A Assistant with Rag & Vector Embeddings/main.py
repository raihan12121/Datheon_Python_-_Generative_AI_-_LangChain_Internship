"""
Document Q&A Assistant with RAG & Vector Embeddings - CLI & Executable Runner.

Usage Examples:
  python main.py --demo
  python main.py --index documents/ai_ethics_and_governance_handbook.pdf
  python main.py --query "What is the mandatory retention period for inference metadata?"
  python main.py --query "What is the policy for financial transactions exceeding $10,000?"
  python main.py --interactive
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.pipeline import RAGPipeline


def print_banner():
    banner = """
========================================================================
    DOCUMENT Q&A ASSISTANT WITH RAG & VECTOR EMBEDDINGS
    LangChain Document Loaders | ChromaDB | Source Page Citations
========================================================================
"""
    print(banner)


def run_demo(provider: str = None):
    """Executes a full automated demonstration answering questions with source page citations."""
    print("[*] Initializing RAG Pipeline...")
    pipeline = RAGPipeline(llm_provider=provider)

    pdf_sample = Path(__file__).parent / "documents" / "ai_ethics_and_governance_handbook.pdf"
    if not pdf_sample.is_file():
        from documents.generate_sample_docs import generate_sample_pdf
        generate_sample_pdf(str(pdf_sample))

    print(f"[*] Ingesting and Indexing Custom PDF: {pdf_sample.name}")
    chunk_count = pipeline.ingest_document(str(pdf_sample))
    print(f"[+] Successfully chunked and stored {chunk_count} vector embeddings in ChromaDB!\n")

    demo_questions = [
        "What is the mandatory retention period for inference metadata?",
        "How is Personally Identifiable Information (PII) handled when sending queries to LLMs?",
        "What are the Human-in-the-Loop thresholds for transactions over $10,000 USD?",
        "What is the maximum SLA time to report a critical security incident to CDOC?",
    ]

    for idx, q in enumerate(demo_questions, 1):
        print("=" * 65)
        print(f"  DEMO QUERY {idx}: {q}")
        print("=" * 65)

        answer_obj = pipeline.query(q)

        print("\n[GROUNDED ANSWER]:")
        print(f"  {answer_obj.answer}\n")

        print("[SOURCE CITATIONS]:")
        if answer_obj.citations:
            for cit in answer_obj.citations:
                print(f"  * Source Document: {cit.source_file}")
                print(f"    Page Citation  : Page {cit.page_number}")
                print(f"    Context Excerpt: \"{cit.excerpt}\"\n")
        else:
            print("  * No citations found.\n")

    print("[SUCCESS] RAG pipeline demo completed with source page citations!")


def run_interactive(pipeline: RAGPipeline):
    """Interactive CLI Q&A Loop."""
    print("\n[*] Entering Interactive Document Q&A Mode. Type 'exit' or 'quit' to stop.\n")
    while True:
        try:
            query = input("Ask a Question > ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit", "q"):
                print("[*] Exiting Document Q&A Assistant. Goodbye!")
                break

            answer_obj = pipeline.query(query)
            print("\n" + "-" * 55)
            print(f"ANSWER:\n{answer_obj.answer}\n")
            print("SOURCE CITATIONS:")
            for cit in answer_obj.citations:
                print(f"  * {cit.source_file} (Page {cit.page_number})")
                print(f"    Excerpt: \"{cit.excerpt}\"")
            print("-" * 55 + "\n")

        except (KeyboardInterrupt, EOFError):
            print("\n[*] Exiting.")
            break


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Document Q&A Assistant with RAG & Vector Embeddings."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run complete automated demo with multi-page PDF and page citations",
    )
    parser.add_argument(
        "--index",
        type=str,
        help="Path to custom PDF or text document to chunk and index into ChromaDB",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Query question to retrieve context and answer with citations",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Launch interactive terminal Q&A session",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear persistent ChromaDB index",
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai", "local"],
        default=None,
        help="LLM provider override ('gemini', 'openai', or 'local')",
    )

    args = parser.parse_args()

    pipeline = RAGPipeline(llm_provider=args.provider)

    if args.reset:
        pipeline.reset_index()
        print("[+] ChromaDB index cleared successfully.")
        if not (args.index or args.query or args.interactive or args.demo):
            return

    if args.index:
        count = pipeline.ingest_document(args.index)
        print(f"[+] Successfully indexed {count} chunks from '{args.index}' into ChromaDB.")

    if args.query:
        ans = pipeline.query(args.query)
        print("\n" + "=" * 55)
        print(ans.format_full_response())
        print("=" * 55)

    elif args.interactive:
        run_interactive(pipeline)

    elif args.demo or not (args.index or args.query):
        run_demo(provider=args.provider)


if __name__ == "__main__":
    main()
