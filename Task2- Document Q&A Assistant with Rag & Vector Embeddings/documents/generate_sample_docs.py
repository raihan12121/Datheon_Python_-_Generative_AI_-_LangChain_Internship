"""
Generates realistic multi-page PDF and text documents for testing RAG ingestion and page citation retrieval.
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_sample_pdf(pdf_path: str):
    """Generates a structured 4-page PDF with clear section boundaries for testing page citations."""
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=15,
    )
    h1_style = ParagraphStyle(
        "Heading1",
        parent=styles["Heading1"],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=14,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=8,
    )

    story = []

    # PAGE 1: Policy Scope & Model Registration
    story.append(Paragraph("Enterprise AI Governance & Ethics Handbook", title_style))
    story.append(Paragraph("Document Version: 2.4 | Classification: Restricted Internal | Effective: Q4 2024", body_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Section 1: Executive Summary and Scope", h1_style))
    story.append(Paragraph(
        "This policy governs all machine learning models, generative AI applications, and autonomous agents "
        "deployed across Datheon enterprise infrastructure. All models interacting with customer data or operational "
        "decision systems must be cataloged in the Datheon Central Model Registry prior to staging deployment.",
        body_style,
    ))
    story.append(Paragraph("Section 2: Model Registration and Lineage Tracking", h1_style))
    story.append(Paragraph(
        "Every production LLM prompt pipeline must retain immutable audit logs containing prompt templates, model versions, "
        "temperature parameters, and completion timestamps. The mandatory retention period for inference metadata is 365 days. "
        "Engineering teams must submit a Model Risk Assessment (MRA-Form-101) to the AI Ethics Board before production release.",
        body_style,
    ))
    story.append(PageBreak())

    # PAGE 2: Data Privacy, Redaction Protocols, and PII Standards
    story.append(Paragraph("Section 3: Data Privacy, Redaction, and PII Protection", h1_style))
    story.append(Paragraph(
        "Direct ingestion of Personally Identifiable Information (PII) into public LLM endpoints is strictly prohibited. "
        "All incoming user prompts must traverse the PII Masking Gateway (Datheon SafeGuard Engine) which automatically "
        "replaces Social Security Numbers, credit card numbers, and patient health identifiers with cryptographic tokens.",
        body_style,
    ))
    story.append(Paragraph(
        "Data retention on third-party cloud LLM providers must be contractually configured to zero-day retention (ZDR). "
        "Model training on proprietary corporate customer datasets requires explicit bilateral consent from the Legal & Compliance Department.",
        body_style,
    ))
    story.append(PageBreak())

    # PAGE 3: Bias Mitigation & Human-in-the-Loop Thresholds
    story.append(Paragraph("Section 4: Bias Mitigation & Demographic Parity", h1_style))
    story.append(Paragraph(
        "Automated evaluation suites must assess LLM outputs against standard demographic parity and disparate impact metrics. "
        "Any pipeline demonstrating adverse impact ratios below 0.80 across protected classes will trigger an automated deployment freeze.",
        body_style,
    ))
    story.append(Paragraph("Section 5: Human-in-the-Loop (HITL) Thresholds", h1_style))
    story.append(Paragraph(
        "For financial transactions exceeding $10,000 USD or automated hiring recommendations, autonomous decisioning is prohibited. "
        "A qualified human reviewer must review and countersign the decision within 24 hours. "
        "If model confidence falls below 85% (confidence score < 0.85), the query must be automatically escalated to Level 2 support.",
        body_style,
    ))
    story.append(PageBreak())

    # PAGE 4: Incident Reporting & Compliance Sanctions
    story.append(Paragraph("Section 6: Incident Reporting and Escalation SLA", h1_style))
    story.append(Paragraph(
        "Any critical LLM security incident - such as prompt injection exploits, jailbreaks, or unauthorized data exfiltration - "
        "must be reported to the Datheon Cyber Defense Operations Center (CDOC) within 60 minutes of detection. "
        "Severity-1 incidents trigger immediate revocation of model API keys and dynamic failover to deterministic fallback services.",
        body_style,
    ))
    story.append(Paragraph("Section 7: Compliance Violations and Sanctions", h1_style))
    story.append(Paragraph(
        "Failure to adhere to this governance framework may result in disciplinary action up to and including termination of employment, "
        "revocation of developer repository access, and external regulatory disclosures in accordance with ISO/IEC 42001 standards.",
        body_style,
    ))

    doc.build(story)
    print(f"[+] Sample PDF created at: {pdf_path}")


def generate_sample_txt(txt_path: str):
    """Generates an unstructured technical document."""
    content = """Datheon Cloud Infrastructure Specification - Core Microservices Architecture
Document ID: ARCH-SPEC-2024-v3
Lead Architect: Cloud Operations Team

1. Service Level Agreements (SLAs)
The Datheon core microservices tier guarantees a 99.95% monthly uptime SLA. 
Peak API latency must not exceed 120 milliseconds for p95 requests and 250 milliseconds for p99 requests.

2. Caching Strategy and In-Memory Data Store
All read-heavy entity lookups are cached through Redis Enterprise cluster (v7.2).
Cache time-to-live (TTL) is strictly bounded to 15 minutes (900 seconds) for dynamic financial records,
and 24 hours for static product catalogs.
Eviction policy is configured as allkeys-lru (Least Recently Used).

3. Database Replication and Disaster Recovery (DR)
The primary transactional database is PostgreSQL with active-passive read replica clusters deployed across US-East and US-West.
Recovery Point Objective (RPO) is configured for under 5 minutes.
Recovery Time Objective (RTO) for automated region failover is under 15 minutes.
"""
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"[+] Sample TXT created at: {txt_path}")


if __name__ == "__main__":
    docs_dir = Path(__file__).parent
    docs_dir.mkdir(parents=True, exist_ok=True)
    generate_sample_pdf(str(docs_dir / "ai_ethics_and_governance_handbook.pdf"))
    generate_sample_txt(str(docs_dir / "cloud_architecture_spec.txt"))
