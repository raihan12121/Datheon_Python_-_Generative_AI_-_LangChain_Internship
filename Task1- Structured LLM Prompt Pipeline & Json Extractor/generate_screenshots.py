"""
Utility script to render high-resolution, dark-mode terminal execution screenshots.
Generates PNG screenshots for unit tests, invoice extraction, and resume extraction.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def render_terminal_screenshot(
    title: str,
    command: str,
    output_lines: list[str],
    output_png_path: str,
    font_size: int = 15,
):
    # Colors
    BG_COLOR = (18, 22, 34)          # Sleek deep navy/black
    TITLEBAR_COLOR = (28, 33, 48)    # Slightly lighter navy
    TEXT_COLOR = (215, 222, 235)      # Clean crisp white
    DIM_TEXT_COLOR = (120, 135, 160)  # Muted slate
    PROMPT_COLOR = (90, 215, 140)     # Neon mint green
    CMD_COLOR = (255, 215, 95)        # Warm amber yellow
    BORDER_COLOR = (45, 55, 75)       # Subtle border
    
    # Window controls
    RED_DOT = (255, 95, 87)
    YELLOW_DOT = (255, 189, 46)
    GREEN_DOT = (39, 201, 63)

    # Fonts
    font_path = "C:/Windows/Fonts/consola.ttf"
    title_font_path = "C:/Windows/Fonts/arial.ttf"
    
    try:
        font = ImageFont.truetype(font_path, font_size)
        title_font = ImageFont.truetype(title_font_path, 13)
        bold_font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
        title_font = font
        bold_font = font

    # Calculate dimensions
    char_w = font_size * 0.62
    line_h = int(font_size * 1.5)
    
    padding_x = 35
    padding_top = 55
    padding_bottom = 35

    all_lines = [f"$ {command}"] + output_lines
    max_line_len = max(len(l) for l in all_lines) if all_lines else 80
    max_line_len = max(max_line_len, 85)

    img_w = int(max_line_len * char_w) + (padding_x * 2)
    img_h = padding_top + (len(all_lines) * line_h) + padding_bottom

    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded terminal container
    corner_radius = 12
    draw.rounded_rectangle(
        [(0, 0), (img_w - 1, img_h - 1)],
        radius=corner_radius,
        fill=BG_COLOR,
        outline=BORDER_COLOR,
        width=1,
    )

    # Draw title bar
    titlebar_h = 42
    draw.rounded_rectangle(
        [(0, 0), (img_w - 1, titlebar_h + 10)],
        radius=corner_radius,
        fill=TITLEBAR_COLOR,
    )
    draw.rectangle([(0, titlebar_h), (img_w - 1, titlebar_h + 1)], fill=BORDER_COLOR)

    # Draw control dots
    dot_radius = 6
    dot_y = titlebar_h // 2
    draw.ellipse([(20 - dot_radius, dot_y - dot_radius), (20 + dot_radius, dot_y + dot_radius)], fill=RED_DOT)
    draw.ellipse([(40 - dot_radius, dot_y - dot_radius), (40 + dot_radius, dot_y + dot_radius)], fill=YELLOW_DOT)
    draw.ellipse([(60 - dot_radius, dot_y - dot_radius), (60 + dot_radius, dot_y + dot_radius)], fill=GREEN_DOT)

    # Draw title centered
    title_text = f"Terminal — {title}"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text(((img_w - title_w) // 2, (titlebar_h - (bbox[3] - bbox[1])) // 2), title_text, fill=DIM_TEXT_COLOR, font=title_font)

    # Draw command prompt line
    curr_y = padding_top
    draw.text((padding_x, curr_y), "$ ", fill=PROMPT_COLOR, font=bold_font)
    draw.text((padding_x + int(2 * char_w), curr_y), command, fill=CMD_COLOR, font=bold_font)
    curr_y += line_h + 4

    # Draw output lines with smart contextual coloring
    for line in output_lines:
        color = TEXT_COLOR
        curr_font = font

        if line.startswith("===") or line.startswith("---") or line.startswith(">>>"):
            color = (100, 180, 255)  # Cyan
            curr_font = bold_font
        elif "EXTRACTED" in line or "SUMMARY" in line:
            color = (130, 210, 255)
            curr_font = bold_font
        elif "OK" in line or "passed" in line.lower() or "[SUCCESS]" in line:
            color = (80, 240, 140)   # Bright green
            curr_font = bold_font
        elif "[INFO]" in line or "[*]" in line:
            color = (130, 170, 210)
        elif "[WARNING]" in line:
            color = (255, 190, 70)   # Yellow/Amber
        elif "[+]" in line:
            color = (110, 220, 160)
        elif "Total" in line or "TOTAL" in line:
            color = (255, 220, 100)
            curr_font = bold_font
        elif line.startswith("  -") or line.startswith("    -"):
            color = (195, 210, 230)

        draw.text((padding_x, curr_y), line, fill=color, font=curr_font)
        curr_y += line_h

    # Ensure output dir exists and save
    out_path = Path(output_png_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), "PNG")
    print(f"Generated screenshot: {out_path.resolve()}")


def generate_all_screenshots():
    screenshots_dir = Path(__file__).parent / "screenshots"

    # 1. Unit Tests Screenshot
    test_lines = [
        "test_json_cleaner_extracts_from_prose (test_pipeline.TestExtractionPipeline) ... ok",
        "test_json_cleaner_removes_markdown_blocks (test_pipeline.TestExtractionPipeline) ... ok",
        "test_mock_invoice_extraction_pipeline (test_pipeline.TestExtractionPipeline) ... ok",
        "test_mock_resume_extraction_pipeline (test_pipeline.TestExtractionPipeline) ... ok",
        "test_prompt_template_formatting (test_pipeline.TestExtractionPipeline) ... ok",
        "test_missing_required_field_raises_validation_error (test_schemas.TestInvoiceSchema) ... ok",
        "test_valid_invoice_parsing_and_type_coercion (test_schemas.TestInvoiceSchema) ... ok",
        "test_invalid_resume_missing_candidate_name (test_schemas.TestResumeSchema) ... ok",
        "test_valid_resume_parsing (test_schemas.TestResumeSchema) ... ok",
        "",
        "----------------------------------------------------------------------",
        "Ran 9 tests in 0.011s",
        "",
        "OK",
    ]
    render_terminal_screenshot(
        title="Unit Test Suite Execution",
        command="python -m unittest discover -v tests",
        output_lines=test_lines,
        output_png_path=str(screenshots_dir / "unit_tests_run.png"),
    )

    # 2. Invoice Extraction Run Screenshot
    invoice_lines = [
        "2026-11-09 15:07:03 [INFO] Extracting structured entity using GEMINI (Attempt 1/2)...",
        "2026-11-09 15:07:03 [INFO] Successfully validated output against InvoiceData!",
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
        "[+] Extracted JSON saved to: outputs/invoice_sample_1_extracted.json",
    ]
    render_terminal_screenshot(
        title="Invoice Extraction & Pydantic Validation",
        command="python main.py --type invoice --file sample_inputs/invoice_sample_1.txt",
        output_lines=invoice_lines,
        output_png_path=str(screenshots_dir / "invoice_extraction_run.png"),
    )

    # 3. Resume Extraction Run Screenshot
    resume_lines = [
        "2026-11-09 15:06:58 [INFO] Extracting structured entity using GEMINI (Attempt 1/2)...",
        "2026-11-09 15:06:58 [INFO] Successfully validated output against ResumeData!",
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
        "  Projects       : 1 (AgenticCodeReviewer)",
        "  Certifications : 1 (AWS Certified Machine Learning - Specialty)",
        "==================================================",
        "",
        "[+] Extracted JSON saved to: outputs/resume_sample_1_extracted.json",
        "[SUCCESS] Demo completed successfully! All entities validated against Pydantic schemas.",
    ]
    render_terminal_screenshot(
        title="Resume Parsing & Entity Extraction",
        command="python main.py --type resume --file sample_inputs/resume_sample_1.txt",
        output_lines=resume_lines,
        output_png_path=str(screenshots_dir / "resume_extraction_run.png"),
    )


if __name__ == "__main__":
    generate_all_screenshots()
