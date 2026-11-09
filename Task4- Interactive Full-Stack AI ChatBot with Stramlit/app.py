"""
Datheon Interactive Full-Stack AI ChatBot with Streamlit.
Features real-time token streaming, multi-turn conversation memory,
RAG document Q&A with page citations, autonomous multi-tool agent execution, and session state management.
"""

import os
import sys
import time
from pathlib import Path
import streamlit as st

# Add current folder to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.memory import ConversationMemory, ChatMessage
from core.streaming_engine import StreamingEngine
from core.rag_bridge import RAGBridge
from core.agent_bridge import AgentBridge

# -----------------------------------------------------------------------------
# Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Datheon Full-Stack AI ChatBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished typography, badges, and responsive containers
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        color: #60a5fa !important;
    }
    /* Citation Box */
    .citation-box {
        background-color: #1e293b;
        border-left: 4px solid #38bdf8;
        padding: 10px 14px;
        margin-top: 8px;
        border-radius: 4px;
        font-size: 0.88rem;
    }
    /* Reasoning Step Box */
    .step-box {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 6px;
        font-family: monospace;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory(max_history_turns=25)

if "streaming_engine" not in st.session_state:
    st.session_state.streaming_engine = StreamingEngine()

if "rag_bridge" not in st.session_state:
    st.session_state.rag_bridge = RAGBridge()

if "agent_bridge" not in st.session_state:
    st.session_state.agent_bridge = AgentBridge()

if "total_tokens_streamed" not in st.session_state:
    st.session_state.total_tokens_streamed = 0


# -----------------------------------------------------------------------------
# Sidebar Configuration & Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🤖 ChatBot Controls")
    st.caption("Datheon Generative AI & LangChain Internship")
    st.divider()

    # Operating Mode Selection
    mode = st.radio(
        "Application Mode",
        options=[
            "🧠 Knowledge RAG (Document Q&A)",
            "🛠️ Autonomous Multi-Tool Agent",
            "💬 Conversational Assistant",
        ],
        index=0,
    )

    st.divider()

    # Provider & Model Settings
    st.subheader("⚙️ Model Parameters")
    provider = st.selectbox(
        "LLM Provider",
        options=["gemini", "openai", "local"],
        index=0,
        help="Select live Google Gemini, OpenAI, or Local Offline mode.",
    )
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

    # Dynamic Persona selection for conversational mode
    persona = "Helpful Datheon AI Assistant"
    if "Conversational" in mode:
        persona = st.selectbox(
            "System Persona",
            options=[
                "Senior AI Engineer & Architect",
                "Financial Document Analyst",
                "Helpful Datheon AI Assistant",
            ],
            index=0,
        )

    st.divider()

    # Document Ingestion Widget (For RAG Mode)
    if "RAG" in mode:
        st.subheader("📄 Knowledge Base Ingestion")
        uploaded_file = st.file_uploader("Upload custom PDF / TXT", type=["pdf", "txt"])
        if uploaded_file is not None:
            # Save uploaded file temporarily and ingest
            temp_path = Path(__file__).parent / "temp_uploads" / uploaded_file.name
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Chunking & indexing into ChromaDB..."):
                count = st.session_state.rag_bridge.ingest_custom_file(str(temp_path))
                st.success(f"Indexed {count} vector chunks from '{uploaded_file.name}'!")

    # Conversation Management
    st.subheader("🧹 Session Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Chat", type="secondary", use_container_width=True):
            st.session_state.memory.clear()
            st.session_state.total_tokens_streamed = 0
            st.rerun()

    with col2:
        export_format = st.selectbox("Format", options=["Markdown", "JSON"], label_visibility="collapsed")

    # Export Download Button
    if st.session_state.memory.messages:
        if export_format == "Markdown":
            data = st.session_state.memory.export_markdown()
            mime = "text/markdown"
            fname = "chat_export.md"
        else:
            data = st.session_state.memory.export_json()
            mime = "application/json"
            fname = "chat_export.json"

        st.download_button(
            label="📥 Export Chat",
            data=data,
            file_name=fname,
            mime=mime,
            use_container_width=True,
        )

    st.divider()
    # Metrics
    st.metric("Total Messages", len(st.session_state.memory.messages))


# -----------------------------------------------------------------------------
# Main Chat Area
# -----------------------------------------------------------------------------
st.header("Datheon Interactive AI Assistant", anchor=False)

if "RAG" in mode:
    st.info("💡 **Mode Active**: Grounded Document Q&A. Answers questions strictly from indexed PDFs with source page citations.")
elif "Autonomous" in mode:
    st.info("💡 **Mode Active**: ReAct Agent. Uses live DuckDuckGo Search, Safe Math Calculator, and Workspace File Reader.")
else:
    st.info("💡 **Mode Active**: Multi-turn Conversational AI with persistent session memory.")

# Render Conversation History
for msg in st.session_state.memory.messages:
    with st.chat_message(msg.role):
        st.markdown(msg.content)

        # Render Citations if present (RAG mode)
        if msg.metadata and "citations" in msg.metadata and msg.metadata["citations"]:
            with st.expander("📚 Source Page Citations", expanded=False):
                for cit in msg.metadata["citations"]:
                    st.markdown(
                        f"**Source Document**: `{cit.get('source_file')}` | **Page**: `{cit.get('page_number')}`\n\n"
                        f"> *\"{cit.get('excerpt')}\"*"
                    )

        # Render Tool Execution Trace if present (Agent mode)
        if msg.metadata and "steps" in msg.metadata and msg.metadata["steps"]:
            with st.expander("🛠️ ReAct Autonomous Reasoning Trace", expanded=False):
                for idx, step in enumerate(msg.metadata["steps"], 1):
                    st.markdown(f"**Step {idx}:**")
                    if step.get("thought"):
                        st.markdown(f"*Thought:* `{step['thought']}`")
                    if step.get("action"):
                        st.markdown(f"*Action:* `{step['action']}` (Input: `{step.get('action_input')}`)")
                    if step.get("observation"):
                        obs = step["observation"][:200] + "..." if len(step["observation"]) > 200 else step["observation"]
                        st.markdown(f"*Observation:* `{obs}`")
                    st.divider()


# -----------------------------------------------------------------------------
# Chat Input & Streaming Execution
# -----------------------------------------------------------------------------
user_input = st.chat_input("Ask a question, request calculations, or explore documents...")

if user_input:
    # 1. Display & Store User Message
    st.session_state.memory.add_user_message(user_input)
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Assistant Response Processing
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # CASE 1: Knowledge RAG Mode
        if "RAG" in mode:
            with st.spinner("Searching vector index & verifying citations..."):
                answer_text, citations = st.session_state.rag_bridge.answer(user_input)

            # Stream the RAG answer tokens
            def stream_words():
                for word in answer_text.split(" "):
                    yield word + " "
                    time.sleep(0.015)

            full_response = st.write_stream(stream_words())

            # Display citations expander
            if citations:
                with st.expander("📚 Source Page Citations", expanded=True):
                    for cit in citations:
                        st.markdown(
                            f"**Source Document**: `{cit.get('source_file')}` | **Page**: `{cit.get('page_number')}`\n\n"
                            f"> *\"{cit.get('excerpt')}\"*"
                        )

            # Save in memory
            st.session_state.memory.add_assistant_message(
                full_response,
                metadata={"citations": citations},
            )

        # CASE 2: Multi-Tool Autonomous Agent Mode
        elif "Autonomous" in mode:
            with st.status("Agent planning and executing tools...", expanded=True) as status:
                st.write("Initializing ReAct cognitive loop...")
                final_answer, steps = st.session_state.agent_bridge.execute_query(user_input)

                for idx, step in enumerate(steps, 1):
                    if step.get("action"):
                        st.write(f"🔧 Invoking Tool: `{step['action']}` with input: `{step.get('action_input')}`")
                status.update(label="Reasoning complete!", state="complete", expanded=False)

            # Stream final answer
            def stream_words():
                for word in final_answer.split(" "):
                    yield word + " "
                    time.sleep(0.015)

            full_response = st.write_stream(stream_words())

            # Display trace
            if steps:
                with st.expander("🛠️ ReAct Autonomous Reasoning Trace", expanded=False):
                    for idx, step in enumerate(steps, 1):
                        st.markdown(f"**Step {idx}:**")
                        if step.get("thought"):
                            st.markdown(f"*Thought:* `{step['thought']}`")
                        if step.get("action"):
                            st.markdown(f"*Action:* `{step['action']}` (Input: `{step.get('action_input')}`)")
                        if step.get("observation"):
                            obs = step["observation"][:200] + "..." if len(step["observation"]) > 200 else step["observation"]
                            st.markdown(f"*Observation:* `{obs}`")

            st.session_state.memory.add_assistant_message(
                full_response,
                metadata={"steps": steps},
            )

        # CASE 3: General Conversational Assistant Mode
        else:
            history_dicts = [
                {"role": m.role, "content": m.content}
                for m in st.session_state.memory.messages
            ]

            stream_gen = st.session_state.streaming_engine.stream_chat(
                messages=history_dicts,
                system_instruction=f"You are a {persona} at Datheon AI.",
                temperature=temperature,
            )

            full_response = st.write_stream(stream_gen)
            st.session_state.memory.add_assistant_message(full_response)

    st.rerun()
