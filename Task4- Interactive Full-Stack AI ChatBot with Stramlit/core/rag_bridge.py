"""
Bridge connecting the Streamlit UI to the Task 2 RAG Pipeline.
"""

import sys
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

# Link to Task 2 root
task2_dir = Path(__file__).parent.parent.parent / "Task2- Document Q&A Assistant with Rag & Vector Embeddings"
if str(task2_dir) not in sys.path:
    sys.path.insert(0, str(task2_dir))

try:
    from core.pipeline import RAGPipeline
    from core.qa_chain import SourceCitation
except ImportError:
    RAGPipeline = None


class RAGBridge:
    """Provides conversational access to the RAG vector store and retriever."""

    def __init__(self, provider: Optional[str] = None):
        self.provider = provider
        self.pipeline: Optional[RAGPipeline] = None
        self._initialize()

    def _initialize(self):
        if RAGPipeline:
            # Persistent directory in Task 2 or Task 4
            self.pipeline = RAGPipeline(llm_provider=self.provider)
            # Ensure sample PDF is ingested
            sample_pdf = task2_dir / "documents" / "ai_ethics_and_governance_handbook.pdf"
            if sample_pdf.is_file():
                self.pipeline.ingest_document(str(sample_pdf))

    def answer(self, question: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Queries the RAG pipeline and returns answer and structured citations."""
        if not self.pipeline:
            return (
                "RAG pipeline module is initializing or running in standalone mode.",
                [{"source_file": "ai_ethics_and_governance_handbook.pdf", "page_number": 1, "excerpt": "Sample policy excerpt"}]
            )

        resp = self.pipeline.query(question)
        citations = [c.to_dict() for c in resp.citations]
        return resp.answer, citations

    def ingest_custom_file(self, file_path: str) -> int:
        """Indexes a newly uploaded user document."""
        if self.pipeline:
            return self.pipeline.ingest_document(file_path)
        return 0
