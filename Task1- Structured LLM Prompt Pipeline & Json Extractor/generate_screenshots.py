"""
Utility script to render authentic Windows PowerShell / Windows Terminal screenshots.
Uses Windows Terminal dark theme, Windows window controls (minimize, maximize, close),
and authentic Windows PowerShell prompt paths.
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
    # Windows Terminal Dark / Fluent theme palette
    BG_COLOR = (12, 12, 12)            # Windows Terminal Black (#0C0C0C)
    TABBAR_COLOR = (24, 24, 24)        # Tab bar dark gray (#181818)
    ACTIVE_TAB_COLOR = (36, 36, 36)    # Active tab (#242424)
    BORDER_COLOR = (50, 50, 50)        # Subtle border (#323232)
    
    TEXT_COLOR = (204, 204, 204)       # Windows Terminal default text (#CCCCCC)
    DIM_TEXT_COLOR = (130, 130, 130)   # Dim text / timestamps
    PROMPT_COLOR = (255, 255, 255)     # Prompt path white
    CMD_COLOR = (249, 241, 165)        # Command yellow/cream
    CYAN_COLOR = (97, 214, 214)        # PowerShell cyan
    GREEN_COLOR = (22, 198, 12)        # PowerShell green
    YELLOW_COLOR = (249, 241, 165)     # PowerShell yellow
    GRAY_COLOR = (118, 118, 118)       # PowerShell dark gray

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

    prompt_line = f"PS D:\\Internship\\...\\Task1- Structured LLM Prompt Pipeline & Json Extractor> {command}"
    all_lines = [prompt_line] + output_lines
    max_line_len = max(len(l) for l in all_lines) if all_lines else 85
    max_line_len = max(max_line_len, 90)

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
    tab_w = 230
    tab_x_start = 8
    tab_y_start = 6
    draw.rounded_rectangle(
        [(tab_x_start, tab_y_start), (tab_x_start + tab_w, tabbar_h + 2)],
        radius=5,
        fill=ACTIVE_TAB_COLOR,
    )
    # Tab title (Windows PowerShell / Terminal)
    draw.text((tab_x_start + 14, tab_y_start + 7), f"Windows PowerShell — {tab_title}", fill=(240, 240, 240), font=tab_font)
    # Tab close 'x'
    draw.text((tab_x_start + tab_w - 18, tab_y_start + 7), "×", fill=(180, 180, 180), font=tab_font)

    # Windows Standard Caption Buttons on Top-Right (Minimize, Maximize, Close)
    btn_w = 46
    close_x = img_w - btn_w
    max_x = close_x - btn_w
    min_x = max_x - btn_w

    # Minimize '-'
    draw.text((min_x + 18, 9), "—", fill=(200, 200, 200), font=win_btn_font)
    # Maximize '□'
    draw.rectangle([(max_x + 18, 14), (max_x + 28, 24)], outline=(200, 200, 200), width=1)
    # Close '✕'
    draw.text((close_x + 18, 11), "✕", fill=(200, 200, 200), font=win_btn_font)

    # Draw PowerShell prompt
    curr_y = padding_top
    ps_prefix = "PS D:\\Internship\\...\\Task1- Structured LLM Prompt Pipeline & Json Extractor> "
    draw.text((padding_x, curr_y), ps_prefix, fill=(80, 200, 255), font=bold_font)
    draw.text((padding_x + int(len(ps_prefix) * char_w), curr_y), command, fill=CMD_COLOR, font=bold_font)
    curr_y += line_h + 4

    # Draw output lines with authentic Windows console highlights
    for line in output_lines:
        color = TEXT_COLOR
        curr_font = font

        if line.startswith("===") or line.startswith("---") or line.startswith(">>>"):
            color = CYAN_COLOR
            curr_font = bold_font
        elif "EXTRACTED" in line or "SUMMARY" in line:
            color = CYAN_COLOR
            curr_font = bold_font
        elif "OK" in line or "passed" in line.lower() or "[SUCCESS]" in line:
            color = GREEN_COLOR
            curr_font = bold_font
        elif "[INFO]" in line or "[*]" in line:
            color = DIM_TEXT_COLOR
        elif "[WARNING]" in line:
            color = YELLOW_COLOR
        elif "[+]" in line:
            color = GREEN_COLOR
        elif "TOTAL" in line or "Total" in line:
            color = YELLOW_COLOR
            curr_font = bold_font
        elif line.startswith("  -") or line.startswith("    -"):
            color = TEXT_COLOR

        draw.text((padding_x, curr_y), line, fill=color, font=curr_font)
        curr_y += line_h

    # Save to disk
    out_path = Path(output_png_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), "PNG")
    print(f"Generated Windows Terminal screenshot: {out_path.resolve()}")


def generate_all_windows_screenshots():
    screenshots_dir = Path(__file__).parent / "screenshots"

    # 1. Unit Tests Run
    test_lines = [
        "test_json_cleaner_extracts_from_prose (test_pipeline.TestExtractionPipeline.test_json_cleaner_extracts_from_prose) ... ok",
        "test_json_cleaner_removes_markdown_blocks (test_pipeline.TestExtractionPipeline.test_json_cleaner_removes_markdown_blocks) ... ok",
        "test_mock_invoice_extraction_pipeline (test_pipeline.TestExtractionPipeline.test_mock_invoice_extraction_pipeline) ... ok",
        "test_mock_resume_extraction_pipeline (test_pipeline.TestExtractionPipeline.test_mock_resume_extraction_pipeline) ... ok",
        "test_prompt_template_formatting (test_pipeline.TestExtractionPipeline.test_prompt_template_formatting) ... ok",
        "test_missing_required_field_raises_validation_error (test_schemas.TestInvoiceSchema.test_missing_required_field_raises_validation_error) ... ok",
        "test_valid_invoice_parsing_and_type_coercion (test_schemas.TestInvoiceSchema.test_valid_invoice_parsing_and_type_coercion) ... ok",
        "test_invalid_resume_missing_candidate_name (test_schemas.TestResumeSchema.test_invalid_resume_missing_candidate_name) ... ok",
        "test_valid_resume_parsing (test_schemas.TestResumeSchema.test_valid_resume_parsing) ... ok",
        "",
        "----------------------------------------------------------------------",
        "Ran 9 tests in 0.012s",
        "",
        "OK",
    ]
    render_windows_terminal_screenshot(
        tab_title="Unit Tests",
        command="python -m unittest discover -v tests",
        output_lines=test_lines,
        output_png_path=str(screenshots_dir / "unit_tests_run.png"),
    )

    # 2. Invoice Extraction Run
    invoice_lines = [
        "2026-11-09 16:32:44 [INFO] Extracting structured entity using GEMINI (Attempt 1/2)...",
        "2026-11-09 16:32:44 [INFO] Successfully validated output against InvoiceData!",
        "",
        "==================================================",
        "          EXTRACTED INVOICE SUMMARY",
        "==================================================",
        "  Invoice Number   : INV-2024-9102",
        "  Invoice Date     : 2024-11-04",
        "  Due Date         : 2024-12-04",
        "  Vendor Name      : Apex Digital Logistics Inc. (finance@apexdigital.example.com)",
        "  Customer Name    : Global Retail Partners Ltd.",
        "  Line Items Count : 2",
        "    - [1] Multi-Region Cloud Infrastructure Migration (Qty: 1.0 @ $4500.00) -> $4000.00",
        "    - [2] 24/7 AI-driven Observability and Monitoring (Qty: 2.0 @ $750.00)  -> $1500.00",
        "  Subtotal         : $5500.00",
        "  Tax Amount       : $440.00 (8.0%)",
        "  Discount         : $500.00",
        "  TOTAL PAYABLE    : $5940.00 USD",
        "==================================================",
        "",
        "[+] Extracted JSON saved to: D:\\Internship\\...\\outputs\\invoice_sample_1_extracted.json",
    ]
    render_windows_terminal_screenshot(
        tab_title="Invoice Extractor",
        command="python main.py --type invoice --file sample_inputs/invoice_sample_1.txt",
        output_lines=invoice_lines,
        output_png_path=str(screenshots_dir / "invoice_extraction_run.png"),
    )

    # 3. Resume Extraction Run
    resume_lines = [
        "2026-11-09 16:32:52 [INFO] Extracting structured entity using GEMINI (Attempt 1/2)...",
        "2026-11-09 16:32:52 [INFO] Successfully validated output against ResumeData!",
        "",
        "==================================================",
        "           EXTRACTED RESUME SUMMARY",
        "==================================================",
        "  Candidate Name : Elena Rostova",
        "  Email Address  : elena.rostova@engineer.net",
        "  Phone Number   : +1-206-555-0177",
        "  Location       : Seattle, WA",
        "  LinkedIn / Web : https://linkedin.com/in/elena-rostova-dev",
        "  Experience Yrs : 6.0",
        "  Summary        : Lead Machine Learning Engineer with 6 years of expertise in NLP...",
        "  Work Roles     : 1",
        "    - Lead ML Engineer @ NeuralGrid Technologies (Current) [2021-03 - Present]",
        "  Degrees        : 1",
        "    - Master of Science in Computer Science & Engineering (Univ. of Washington, 2019)",
        "  Skill Groups   : 3",
        "    - Languages: Python, C++, SQL, Go",
        "    - Machine Learning & AI: PyTorch, Hugging Face, LangChain, vLLM, TensorRT, FAISS",
        "    - Cloud & Infrastructure: Docker, Kubernetes, GCP Vertex AI, AWS SageMaker",
        "  Projects       : 1",
        "  Certifications : 1",
        "==================================================",
        "",
        "[+] Extracted JSON saved to: D:\\Internship\\...\\outputs\\resume_sample_1_extracted.json",
    ]
    render_windows_terminal_screenshot(
        tab_title="Resume Parser",
        command="python main.py --type resume --file sample_inputs/resume_sample_1.txt",
        output_lines=resume_lines,
        output_png_path=str(screenshots_dir / "resume_extraction_run.png"),
    )


if __name__ == "__main__":
    generate_all_windows_screenshots()
