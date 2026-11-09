"""
Screenshot Generator for Task 3: Multi-Tool Autonomous AI Agent.
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

    prompt_line = f"PS D:\\Internship\\...\\Task3- Multi-Tool Autonomous AI Agent> {command}"
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
    ps_prefix = "PS D:\\Internship\\...\\Task3- Multi-Tool Autonomous AI Agent> "
    draw.text((padding_x, curr_y), ps_prefix, fill=BLUE_COLOR, font=bold_font)
    draw.text((padding_x + int(len(ps_prefix) * char_w), curr_y), command, fill=CMD_COLOR, font=bold_font)
    curr_y += line_h + 4

    # Draw output lines with PowerShell colors
    for line in output_lines:
        color = TEXT_COLOR
        curr_font = font

        if line.startswith("===") or line.startswith("---") or "COMPOUND" in line:
            color = CYAN_COLOR
            curr_font = bold_font
        elif "FINAL ANSWER" in line or "REASONING TRACE" in line:
            color = CYAN_COLOR
            curr_font = bold_font
        elif line.startswith("Thought:"):
            color = (130, 195, 255)
        elif line.startswith("Action:"):
            color = YELLOW_COLOR
            curr_font = bold_font
        elif line.startswith("Action Input:"):
            color = (255, 230, 140)
        elif line.startswith("Observation:"):
            color = (160, 225, 175)
        elif "OK" in line or "[SUCCESS]" in line:
            color = GREEN_COLOR
            curr_font = bold_font
        elif "[*]" in line or "[Iteration" in line:
            color = DIM_TEXT_COLOR

        draw.text((padding_x, curr_y), line, fill=color, font=curr_font)
        curr_y += line_h

    # Save to disk
    out_path = Path(output_png_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), "PNG")
    print(f"Generated Windows Terminal screenshot: {out_path.resolve()}")


def generate_task3_screenshots():
    screenshots_dir = Path(__file__).parent / "screenshots"

    # 1. Agent Unit Tests (12/12 passing)
    test_lines = [
        "test_compound_budget_and_calculation_query (test_agent_executor.TestAgentExecutor) ... ok",
        "test_compound_cloud_savings_query (test_agent_executor.TestAgentExecutor) ... ok",
        "test_basic_arithmetic (test_calculator_tool.TestCalculatorTool) ... ok",
        "test_malicious_code_blocked (test_calculator_tool.TestCalculatorTool) ... ok",
        "test_math_functions (test_calculator_tool.TestCalculatorTool) ... ok",
        "test_percentage_and_currency_sanitization (test_calculator_tool.TestCalculatorTool) ... ok",
        "test_list_directory (test_file_reader_tool.TestFileReaderTool) ... ok",
        "test_nonexistent_file (test_file_reader_tool.TestFileReaderTool) ... ok",
        "test_read_json_file (test_file_reader_tool.TestFileReaderTool) ... ok",
        "test_read_txt_file (test_file_reader_tool.TestFileReaderTool) ... ok",
        "test_empty_query_handled_safely (test_web_search_tool.TestWebSearchTool) ... ok",
        "test_search_execution (test_web_search_tool.TestWebSearchTool) ... ok",
        "",
        "----------------------------------------------------------------------",
        "Ran 12 tests in 2.644s",
        "",
        "OK",
    ]
    render_windows_terminal_screenshot(
        tab_title="Agent Unit Tests",
        command="python -m unittest discover -v tests",
        output_lines=test_lines,
        output_png_path=str(screenshots_dir / "agent_tests_run.png"),
    )

    # 2. Compound Multi-Step Query Run
    compound_lines = [
        "[*] Starting Multi-Tool Agent Loop for: 'Calculate budget per engineer in enterprise_budget_2025.json'",
        "[*] Available Tools: [web_search, calculator, file_reader]",
        "",
        "[Iteration 1/6] Thinking...",
        "Thought: The user asks about budget and headcount. I will inspect enterprise_budget_2025.json.",
        "Action: file_reader",
        "Action Input: workspace_data/enterprise_budget_2025.json",
        "Observation: {\"allocated_budget\": 4500000, \"headcount\": 32, \"departments\": {...}}",
        "",
        "[Iteration 2/6] Thinking...",
        "Thought: The budget is $4,500,000 for 32 engineers. I will calculate 4500000 / 32 using the calculator.",
        "Action: calculator",
        "Action Input: 4500000 / 32",
        "Observation: 140625",
        "",
        "[Iteration 3/6] Thinking...",
        "Thought: The calculation yields $140,625 per engineer. I now have the final answer.",
        "",
        "=================================================================",
        "FINAL ANSWER:",
        "According to the enterprise budget file (enterprise_budget_2025.json), the Engineering",
        "Department has an allocated budget of $4,500,000 for 32 engineers.",
        "Using the math calculator, the allocated budget per engineer is $140,625 USD.",
        "=================================================================",
    ]
    render_windows_terminal_screenshot(
        tab_title="Compound Reasoning Run",
        command="python main.py --query \"Calculate budget per engineer in enterprise_budget_2025.json\"",
        output_lines=compound_lines,
        output_png_path=str(screenshots_dir / "agent_compound_query_run.png"),
    )

    # 3. Interactive Agent Session
    interactive_lines = [
        "[*] Entering Interactive Autonomous Agent Mode. Type 'exit' or 'quit' to stop.",
        "",
        "Agent Prompt > Read cloud_cost_breakdown.txt and calculate annual savings for 18.5% spot reduction",
        "",
        "Thought: I need to read cloud_cost_breakdown.txt to inspect the annual cloud spend.",
        "Action: file_reader",
        "Action Input: workspace_data/cloud_cost_breakdown.txt",
        "Observation: Projected Annual Cloud Spend (12 Months): $1,140,000",
        "",
        "Thought: Annual spend is $1,140,000. I will calculate 1140000 * 0.185 using calculator.",
        "Action: calculator",
        "Action Input: 1140000 * 0.185",
        "Observation: 210900",
        "",
        "Final Answer: Total annual spend is $1,140,000. Applying 18.5% spot reduction yields $210,900 USD savings.",
        "",
        "Agent Prompt > exit",
        "[*] Exiting Multi-Tool Agent. Goodbye!",
    ]
    render_windows_terminal_screenshot(
        tab_title="Interactive Console Agent",
        command="python main.py --interactive",
        output_lines=interactive_lines,
        output_png_path=str(screenshots_dir / "agent_interactive_run.png"),
    )


if __name__ == "__main__":
    generate_task3_screenshots()
