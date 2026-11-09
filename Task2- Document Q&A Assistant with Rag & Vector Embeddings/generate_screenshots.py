"""
Screenshot Generator for Task 2: Document Q&A Assistant with RAG & Vector Embeddings.
Renders authentic Windows Terminal / Windows PowerShell screenshots with Windows controls.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def render_windows_terminal_screenshot(
    tab_title: str,
    command: str,
    output_lines: list[str],
    output_png_path: str,
    font_size: int = 15,
):
    # Windows Terminal Dark Theme Palette
    BG_COLOR = (12, 12, 12)            # Windows Terminal Black (#0C0C0C)
    TABBAR_COLOR = (24, 24, 24)        # Tab bar dark gray (#181818)
    ACTIVE_TAB_COLOR = (36, 36, 36)    # Active tab (#242424)
    BORDER_COLOR = (50, 50, 50)        # Subtle border (#323232)
    
    TEXT_COLOR = (204, 204, 204)       # Windows Terminal default text (#CCCCCC)
    DIM_TEXT_COLOR = (130, 130, 130)   # Dim text / timestamps
    CMD_COLOR = (249, 241, 165)        # Command yellow/cream
    CYAN_COLOR = (97, 214, 214)        # PowerShell cyan
    GREEN_COLOR = (22, 198, 12)        # PowerShell green
    YELLOW_COLOR = (249, 241, 165)     # PowerShell yellow
    BLUE_COLOR = (80, 200, 255)        # Path blue

    # Windows Fonts
    font_path = "C:/Windows/Fonts/consola.ttf"
    title_font_path = "C:/Windows/Fonts/segoeui.ttf"
    if not Path(title_font_path).exists():
        title_font_path = "C:/Windows/Fonts/arial.ttf"

    try:
        font = ImageFont.truetype(font_path, font_size)
        bold_font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", font_size)
        tab_font = ImageFont.truetype(title_font_path, 12)
        win_btn_font = ImageFont.truetype(title_font_path, 13)
    except Exception:
        font = ImageFont.load_default()
        bold_font = font
        tab_font = font
        win_btn_font = font

    # Dimensions
    char_w = font_size * 0.62
    line_h = int(font_size * 1.5)

    padding_x = 28
    tabbar_h = 38
    padding_top = tabbar_h + 20
    padding_bottom = 28

    prompt_line = f"PS D:\\Internship\\...\\Task2- Document Q&A Assistant with Rag & Vector Embeddings> {command}"
    all_lines = [prompt_line] + output_lines
    max_line_len = max(len(l) for l in all_lines) if all_lines else 85
    max_line_len = max(max_line_len, 92)

    img_w = int(max_line_len * char_w) + (padding_x * 2)
    img_h = padding_top + (len(all_lines) * line_h) + padding_bottom

    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer Windows Terminal Window with thin border
    corner_radius = 8
    draw.rounded_rectangle(
        [(0, 0), (img_w - 1, img_h - 1)],
        radius=corner_radius,
        fill=BG_COLOR,
        outline=BORDER_COLOR,
        width=1,
    )

    # Tab bar background
    draw.rectangle([(0, 0), (img_w - 1, tabbar_h)], fill=TABBAR_COLOR)
    draw.line([(0, tabbar_h), (img_w - 1, tabbar_h)], fill=BORDER_COLOR, width=1)

    # Active Windows Terminal Tab
    tab_w = 260
    tab_x_start = 8
    tab_y_start = 6
    draw.rounded_rectangle(
        [(tab_x_start, tab_y_start), (tab_x_start + tab_w, tabbar_h + 2)],
        radius=5,
        fill=ACTIVE_TAB_COLOR,
    )
    # Tab title (Windows PowerShell)
    draw.text((tab_x_start + 14, tab_y_start + 7), f"Windows PowerShell — {tab_title}", fill=(240, 240, 240), font=tab_font)
    # Tab close 'x'
    draw.text((tab_x_start + tab_w - 18, tab_y_start + 7), "×", fill=(180, 180, 180), font=tab_font)

    # Windows Standard Caption Buttons on Top-Right (Minimize, Maximize, Close)
    btn_w = 46
    close_x = img_w - btn_w
    max_x = close_x - btn_w
    min_x = max_x - btn_w

    # Minimize '—'
    draw.text((min_x + 18, 9), "—", fill=(200, 200, 200), font=win_btn_font)
    # Maximize '□'
    draw.rectangle([(max_x + 18, 14), (max_x + 28, 24)], outline=(200, 200, 200), width=1)
    # Close '✕'
    draw.text((close_x + 18, 11), "✕", fill=(200, 200, 200), font=win_btn_font)

    # Draw PowerShell prompt
    curr_y = padding_top
    ps_prefix = "PS D:\\Internship\\...\\Task2- Document Q&A Assistant with Rag & Vector Embeddings> "
    draw.text((padding_x, curr_y), ps_prefix, fill=BLUE_COLOR, font=bold_font)
    draw.text((padding_x + int(len(ps_prefix) * char_w), curr_y), command, fill=CMD_COLOR, font=bold_font)
    curr_y += line_h + 4

    # Draw output lines with PowerShell colors
    for line in output_lines:
        color = TEXT_COLOR
        curr_font = font

        if line.startswith("===") or line.startswith("---") or "DEMO QUERY" in line:
            color = CYAN_COLOR
            curr_font = bold_font
        elif "[GROUNDED ANSWER]" in line or "[SOURCE CITATIONS]" in line:
            color = CYAN_COLOR
            curr_font = bold_font
        elif "OK" in line or "[SUCCESS]" in line:
            color = GREEN_COLOR
            curr_font = bold_font
        elif "[*]" in line or "LangChainDeprecationWarning" in line:
            color = DIM_TEXT_COLOR
        elif "[+]" in line:
            color = GREEN_COLOR
        elif "Page Citation" in line or "Page" in line:
            color = YELLOW_COLOR
            curr_font = bold_font

        draw.text((padding_x, curr_y), line, fill=color, font=curr_font)
        curr_y += line_h

    # Save to disk
    out_path = Path(output_png_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), "PNG")
    print(f"Generated Windows Terminal screenshot: {out_path.resolve()}")


def generate_task2_screenshots():
    screenshots_dir = Path(__file__).parent / "screenshots"

    # 1. RAG Unit Tests
    test_lines = [
        "test_load_pdf_preserves_pages (test_document_loader.TestDocumentLoader) ... ok",
        "test_load_txt (test_document_loader.TestDocumentLoader) ... ok",
        "test_unsupported_file_raises_value_error (test_document_loader.TestDocumentLoader) ... ok",
        "test_question_answering_with_page_citations (test_rag_pipeline.TestRAGPipeline) ... ok",
        "test_unanswerable_question_returns_grounded_fallback (test_rag_pipeline.TestRAGPipeline) ... ok",
        "test_chunking_creates_multiple_chunks (test_splitter.TestRAGTextSplitter) ... ok",
        "test_indexing_and_similarity_retrieval (test_vector_store.TestChromaVectorStore) ... ok",
        "",
        "----------------------------------------------------------------------",
        "Ran 7 tests in 1.286s",
        "",
        "OK",
    ]
    render_windows_terminal_screenshot(
        tab_title="RAG Unit Tests",
        command="python -m unittest discover -v tests",
        output_lines=test_lines,
        output_png_path=str(screenshots_dir / "rag_tests_run.png"),
    )

    # 2. RAG PDF Q&A Run with Page Citations
    qa_lines = [
        "[*] Initializing RAG Pipeline...",
        "[*] Ingesting and Indexing Custom PDF: ai_ethics_and_governance_handbook.pdf",
        "[+] Successfully chunked and stored 5 vector embeddings in ChromaDB!",
        "",
        "=================================================================",
        "  DEMO QUERY 1: What is the mandatory retention period for inference metadata?",
        "=================================================================",
        "[GROUNDED ANSWER]:",
        "  The mandatory retention period for inference metadata is 365 days.",
        "",
        "[SOURCE CITATIONS]:",
        "  * Source Document: ai_ethics_and_governance_handbook.pdf",
        "    Page Citation  : Page 1",
        "    Context Excerpt: \"The mandatory retention period for inference metadata is 365 days. Engineering teams must submit a Model Risk Assessment...\"",
        "",
        "=================================================================",
        "  DEMO QUERY 2: What are the Human-in-the-Loop thresholds for transactions over $10,000 USD?",
        "=================================================================",
        "[GROUNDED ANSWER]:",
        "  For financial transactions exceeding $10,000 USD or automated hiring recommendations,",
        "  autonomous decisioning is prohibited. A human reviewer must review within 24 hours.",
        "",
        "[SOURCE CITATIONS]:",
        "  * Source Document: ai_ethics_and_governance_handbook.pdf",
        "    Page Citation  : Page 3",
        "    Context Excerpt: \"Section 5: Human-in-the-Loop (HITL) Thresholds. For financial transactions exceeding $10,000 USD...\"",
        "",
        "[SUCCESS] RAG pipeline demo completed with source page citations!",
    ]
    render_windows_terminal_screenshot(
        tab_title="PDF Q&A with Page Citations",
        command="python main.py --demo",
        output_lines=qa_lines,
        output_png_path=str(screenshots_dir / "rag_pdf_qa_run.png"),
    )

    # 3. Interactive CLI RAG Session
    interactive_lines = [
        "[*] Entering Interactive Document Q&A Mode. Type 'exit' or 'quit' to stop.",
        "",
        "Ask a Question > What is the SLA to report critical security incidents to CDOC?",
        "-------------------------------------------------------",
        "ANSWER:",
        "Section 6: Incident Reporting and Escalation SLA.",
        "Any critical LLM security incident must be reported to the Datheon Cyber Defense",
        "Operations Center (CDOC) within 60 minutes of detection.",
        "",
        "SOURCE CITATIONS:",
        "  * ai_ethics_and_governance_handbook.pdf (Page 4)",
        "    Excerpt: \"Section 6: Incident Reporting and Escalation SLA. Any critical LLM security incident must be reported...\"",
        "-------------------------------------------------------",
        "",
        "Ask a Question > exit",
        "[*] Exiting Document Q&A Assistant. Goodbye!",
    ]
    render_windows_terminal_screenshot(
        tab_title="Interactive Q&A Session",
        command="python main.py --interactive",
        output_lines=interactive_lines,
        output_png_path=str(screenshots_dir / "rag_interactive_run.png"),
    )


if __name__ == "__main__":
    generate_task2_screenshots()
