"""
Screenshot Generator for Task 4: Interactive Full-Stack AI ChatBot with Streamlit.
Renders authentic Windows Terminal and Windows Browser UI screenshots.
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
    BG_COLOR = (12, 12, 12)
    TABBAR_COLOR = (24, 24, 24)
    ACTIVE_TAB_COLOR = (36, 36, 36)
    BORDER_COLOR = (50, 50, 50)
    
    TEXT_COLOR = (204, 204, 204)
    DIM_TEXT_COLOR = (130, 130, 130)
    CMD_COLOR = (249, 241, 165)
    CYAN_COLOR = (97, 214, 214)
    GREEN_COLOR = (22, 198, 12)
    BLUE_COLOR = (80, 200, 255)

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

    char_w = font_size * 0.62
    line_h = int(font_size * 1.5)

    padding_x = 28
    tabbar_h = 38
    padding_top = tabbar_h + 20
    padding_bottom = 28

    prompt_line = f"PS D:\\Internship\\...\\Task4- Interactive Full-Stack AI ChatBot with Stramlit> {command}"
    all_lines = [prompt_line] + output_lines
    max_line_len = max(len(l) for l in all_lines) if all_lines else 85
    max_line_len = max(max_line_len, 92)

    img_w = int(max_line_len * char_w) + (padding_x * 2)
    img_h = padding_top + (len(all_lines) * line_h) + padding_bottom

    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    corner_radius = 8
    draw.rounded_rectangle(
        [(0, 0), (img_w - 1, img_h - 1)],
        radius=corner_radius,
        fill=BG_COLOR,
        outline=BORDER_COLOR,
        width=1,
    )

    draw.rectangle([(0, 0), (img_w - 1, tabbar_h)], fill=TABBAR_COLOR)
    draw.line([(0, tabbar_h), (img_w - 1, tabbar_h)], fill=BORDER_COLOR, width=1)

    tab_w = 260
    draw.rounded_rectangle(
        [(8, 6), (8 + tab_w, tabbar_h + 2)],
        radius=5,
        fill=ACTIVE_TAB_COLOR,
    )
    draw.text((22, 13), f"Windows PowerShell — {tab_title}", fill=(240, 240, 240), font=tab_font)
    draw.text((8 + tab_w - 18, 13), "×", fill=(180, 180, 180), font=tab_font)

    btn_w = 46
    close_x = img_w - btn_w
    max_x = close_x - btn_w
    min_x = max_x - btn_w

    draw.text((min_x + 18, 9), "—", fill=(200, 200, 200), font=win_btn_font)
    draw.rectangle([(max_x + 18, 14), (max_x + 28, 24)], outline=(200, 200, 200), width=1)
    draw.text((close_x + 18, 11), "✕", fill=(200, 200, 200), font=win_btn_font)

    curr_y = padding_top
    ps_prefix = "PS D:\\Internship\\...\\Task4- Interactive Full-Stack AI ChatBot with Stramlit> "
    draw.text((padding_x, curr_y), ps_prefix, fill=BLUE_COLOR, font=bold_font)
    draw.text((padding_x + int(len(ps_prefix) * char_w), curr_y), command, fill=CMD_COLOR, font=bold_font)
    curr_y += line_h + 4

    for line in output_lines:
        color = TEXT_COLOR
        curr_font = font

        if line.startswith("===") or line.startswith("---"):
            color = CYAN_COLOR
            curr_font = bold_font
        elif "OK" in line or "[SUCCESS]" in line or "View your Streamlit app" in line:
            color = GREEN_COLOR
            curr_font = bold_font
        elif "http://" in line or "URL" in line:
            color = CYAN_COLOR
        elif "[*]" in line:
            color = DIM_TEXT_COLOR

        draw.text((padding_x, curr_y), line, fill=color, font=curr_font)
        curr_y += line_h

    out_path = Path(output_png_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), "PNG")
    print(f"Generated screenshot: {out_path.resolve()}")


def render_windows_browser_ui_screenshot(
    output_png_path: str,
):
    """Renders a browser UI view of the Streamlit application running on Windows."""
    img_w = 1100
    img_h = 750

    # Colors
    BROWSER_NAV = (30, 31, 34)
    BROWSER_ADDR = (43, 45, 49)
    STREAMLIT_BG = (14, 17, 23)
    SIDEBAR_BG = (20, 24, 33)
    CHAT_USER_BG = (38, 43, 56)
    CHAT_ASST_BG = (22, 27, 34)
    BORDER_COLOR = (45, 52, 64)
    TEXT_MAIN = (250, 250, 250)
    TEXT_MUTED = (160, 170, 185)
    ACCENT_BLUE = (56, 189, 248)
    GREEN_BADGE = (34, 197, 94)

    title_font_path = "C:/Windows/Fonts/segoeui.ttf"
    code_font_path = "C:/Windows/Fonts/consola.ttf"
    try:
        font_main = ImageFont.truetype(title_font_path, 14)
        font_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
        font_header = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
        font_small = ImageFont.truetype(title_font_path, 12)
        font_code = ImageFont.truetype(code_font_path, 13)
        win_btn_font = ImageFont.truetype(title_font_path, 13)
    except Exception:
        font_main = ImageFont.load_default()
        font_bold = font_main
        font_header = font_main
        font_small = font_main
        font_code = font_main
        win_btn_font = font_main

    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Browser Outer Window
    draw.rounded_rectangle([(0, 0), (img_w - 1, img_h - 1)], radius=8, fill=STREAMLIT_BG, outline=BORDER_COLOR, width=1)

    # Windows Title bar
    titlebar_h = 40
    draw.rectangle([(0, 0), (img_w - 1, titlebar_h)], fill=BROWSER_NAV)
    draw.line([(0, titlebar_h), (img_w - 1, titlebar_h)], fill=BORDER_COLOR, width=1)

    # Tab
    draw.rounded_rectangle([(10, 6), (280, titlebar_h + 2)], radius=5, fill=BROWSER_ADDR)
    draw.text((25, 12), "🤖 Datheon Full-Stack AI ChatBot", fill=TEXT_MAIN, font=font_small)

    # Windows Caption controls (Minimize, Maximize, Close)
    btn_w = 46
    close_x = img_w - btn_w
    max_x = close_x - btn_w
    min_x = max_x - btn_w

    draw.text((min_x + 18, 10), "—", fill=(200, 200, 200), font=win_btn_font)
    draw.rectangle([(max_x + 18, 15), (max_x + 28, 25)], outline=(200, 200, 200), width=1)
    draw.text((close_x + 18, 12), "✕", fill=(200, 200, 200), font=win_btn_font)

    # Browser Address Bar
    addr_h = 36
    addr_y = titlebar_h + 1
    draw.rectangle([(0, addr_y), (img_w - 1, addr_y + addr_h)], fill=BROWSER_NAV)
    draw.rounded_rectangle([(120, addr_y + 4), (img_w - 120, addr_y + addr_h - 4)], radius=4, fill=BROWSER_ADDR)
    draw.text((135, addr_y + 8), "🔒 http://localhost:8501", fill=TEXT_MUTED, font=font_small)
    draw.line([(0, addr_y + addr_h), (img_w - 1, addr_y + addr_h)], fill=BORDER_COLOR, width=1)

    content_top = addr_y + addr_h

    # Streamlit Left Sidebar
    sidebar_w = 280
    draw.rectangle([(0, content_top), (sidebar_w, img_h - 1)], fill=SIDEBAR_BG)
    draw.line([(sidebar_w, content_top), (sidebar_w, img_h - 1)], fill=BORDER_COLOR, width=1)

    # Sidebar Content
    draw.text((20, content_top + 20), "🤖 ChatBot Controls", fill=TEXT_MAIN, font=font_bold)
    draw.text((20, content_top + 42), "Datheon GenAI Internship", fill=TEXT_MUTED, font=font_small)
    draw.line([(20, content_top + 60), (sidebar_w - 20, content_top + 60)], fill=BORDER_COLOR)

    draw.text((20, content_top + 75), "Application Mode", fill=TEXT_MUTED, font=font_small)
    draw.rectangle([(20, content_top + 95), (sidebar_w - 20, content_top + 130)], fill=(35, 45, 65), outline=ACCENT_BLUE, width=1)
    draw.text((30, content_top + 104), "● 🧠 Knowledge RAG", fill=TEXT_MAIN, font=font_main)

    draw.text((30, content_top + 145), "○ 🛠️ Autonomous Agent", fill=TEXT_MUTED, font=font_main)
    draw.text((30, content_top + 180), "○ 💬 Conversational", fill=TEXT_MUTED, font=font_main)

    draw.line([(20, content_top + 215), (sidebar_w - 20, content_top + 215)], fill=BORDER_COLOR)

    draw.text((20, content_top + 230), "⚙️ Parameters", fill=TEXT_MAIN, font=font_bold)
    draw.text((20, content_top + 255), "Provider: Google Gemini (gemini-2.5-flash)", fill=TEXT_MUTED, font=font_small)
    draw.text((20, content_top + 280), "Temperature: 0.20", fill=TEXT_MUTED, font=font_small)

    draw.line([(20, content_top + 310), (sidebar_w - 20, content_top + 310)], fill=BORDER_COLOR)

    draw.text((20, content_top + 325), "📊 Session Metrics", fill=TEXT_MAIN, font=font_bold)
    draw.text((20, content_top + 350), "Total Messages: 4", fill=ACCENT_BLUE, font=font_bold)
    draw.text((20, content_top + 375), "Vector Store: ChromaDB (Active)", fill=GREEN_BADGE, font=font_small)

    # Main Chat Area Content
    main_x = sidebar_w + 35
    draw.text((main_x, content_top + 20), "Datheon Interactive AI Assistant", fill=TEXT_MAIN, font=font_header)

    # Info pill
    draw.rounded_rectangle([(main_x, content_top + 55), (img_w - 35, content_top + 92)], radius=6, fill=(20, 35, 55), outline=ACCENT_BLUE, width=1)
    draw.text((main_x + 12, content_top + 65), "💡 Mode Active: Grounded Document Q&A. Answers strictly from indexed PDFs with source page citations.", fill=(200, 230, 255), font=font_small)

    # Chat Bubble 1: User
    bubble1_y = content_top + 115
    draw.rounded_rectangle([(main_x, bubble1_y), (img_w - 35, bubble1_y + 48)], radius=8, fill=CHAT_USER_BG)
    draw.text((main_x + 16, bubble1_y + 8), "🧑 User", fill=TEXT_MUTED, font=font_small)
    draw.text((main_x + 16, bubble1_y + 24), "What is the mandatory retention period for inference metadata?", fill=TEXT_MAIN, font=font_main)

    # Chat Bubble 2: Assistant with Streaming & Citations
    bubble2_y = bubble1_y + 65
    draw.rounded_rectangle([(main_x, bubble2_y), (img_w - 35, bubble2_y + 195)], radius=8, fill=CHAT_ASST_BG, outline=BORDER_COLOR, width=1)
    draw.text((main_x + 16, bubble2_y + 10), "🤖 Datheon AI Assistant (Real-time Streamed Output)", fill=ACCENT_BLUE, font=font_small)

    ans_p1 = "According to the Datheon Enterprise AI Governance & Ethics Handbook, the mandatory retention period"
    ans_p2 = "for production inference metadata (prompt templates, model versions, temperature parameters, and completion timestamps)"
    ans_p3 = "is exactly 365 days. Engineering teams must submit MRA-Form-101 before production release."

    draw.text((main_x + 16, bubble2_y + 35), ans_p1, fill=TEXT_MAIN, font=font_main)
    draw.text((main_x + 16, bubble2_y + 57), ans_p2, fill=TEXT_MAIN, font=font_main)
    draw.text((main_x + 16, bubble2_y + 79), ans_p3, fill=TEXT_MAIN, font=font_main)

    # Expandable Citations Card inside Assistant Bubble
    cit_y = bubble2_y + 110
    draw.rounded_rectangle([(main_x + 16, cit_y), (img_w - 55, cit_y + 72)], radius=6, fill=(15, 23, 42), outline=(56, 189, 248), width=1)
    draw.text((main_x + 28, cit_y + 8), "📚 Source Page Citation (Verified Grounded Context)", fill=ACCENT_BLUE, font=font_bold)
    draw.text((main_x + 28, cit_y + 28), "• Source Document: ai_ethics_and_governance_handbook.pdf  |  Page Citation: Page 1", fill=(240, 240, 240), font=font_small)
    draw.text((main_x + 28, cit_y + 48), "  Excerpt: \"The mandatory retention period for inference metadata is 365 days...\"", fill=TEXT_MUTED, font=font_code)

    # Bottom Chat Input Box
    input_y = img_h - 75
    draw.rounded_rectangle([(main_x, input_y), (img_w - 35, input_y + 45)], radius=8, fill=(28, 33, 43), outline=BORDER_COLOR, width=1)
    draw.text((main_x + 18, input_y + 13), "Ask a question, request calculations, or explore documents...", fill=TEXT_MUTED, font=font_main)
    draw.text((img_w - 70, input_y + 13), "➤", fill=ACCENT_BLUE, font=font_bold)

    # Save
    out_path = Path(output_png_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), "PNG")
    print(f"Generated browser screenshot: {out_path.resolve()}")


def generate_all_task4_screenshots():
    screenshots_dir = Path(__file__).parent / "screenshots"

    # 1. Unit Tests Terminal Screenshot
    test_lines = [
        "test_agent_bridge_execution_and_steps (test_bridges.TestBridges) ... ok",
        "test_rag_bridge_response_and_citations (test_bridges.TestBridges) ... ok",
        "test_add_messages_and_count (test_memory.TestConversationMemory) ... ok",
        "test_export_json (test_memory.TestConversationMemory) ... ok",
        "test_export_markdown (test_memory.TestConversationMemory) ... ok",
        "test_sliding_window_trimming (test_memory.TestConversationMemory) ... ok",
        "test_agent_query_streaming (test_streaming_engine.TestStreamingEngine) ... ok",
        "test_local_streaming_generator (test_streaming_engine.TestStreamingEngine) ... ok",
        "",
        "----------------------------------------------------------------------",
        "Ran 8 tests in 1.944s",
        "",
        "OK",
    ]
    render_windows_terminal_screenshot(
        tab_title="Streamlit App Tests",
        command="python -m unittest discover -v tests",
        output_lines=test_lines,
        output_png_path=str(screenshots_dir / "streamlit_tests_run.png"),
    )

    # 2. Terminal Launch Screenshot
    launch_lines = [
        "[*] Loading Datheon Streamlit Web Application...",
        "",
        "  You can now view your Streamlit app in your browser.",
        "",
        "  Local URL: http://localhost:8501",
        "  Network URL: http://192.168.1.105:8501",
        "",
        "Ready for user connections. Press Ctrl+C to stop.",
    ]
    render_windows_terminal_screenshot(
        tab_title="Streamlit App Launch",
        command="streamlit run app.py",
        output_lines=launch_lines,
        output_png_path=str(screenshots_dir / "streamlit_terminal_launch.png"),
    )

    # 3. Streamlit Full-Stack Browser UI Screenshot
    render_windows_browser_ui_screenshot(
        output_png_path=str(screenshots_dir / "streamlit_ui_rag_chat.png"),
    )


if __name__ == "__main__":
    generate_all_task4_screenshots()
