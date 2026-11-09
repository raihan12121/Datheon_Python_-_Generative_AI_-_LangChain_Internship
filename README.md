# Datheon AI & LangChain Internship Projects

Repository containing 4 enterprise AI engineering projects covering LLM prompt pipelines, retrieval-augmented generation (RAG), autonomous multi-tool AI agents, and full-stack interactive applications.

---

## 📋 Project Directory & Status

| Task # | Project Name | Status | Tech Stack |
| :---: | :--- | :---: | :--- |
| **Task 1** | **[Structured LLM Prompt Pipeline & JSON Extractor](./Task1-%20Structured%20LLM%20Prompt%20Pipeline%20%26%20Json%20Extractor)** | ✅ **Completed** | Python 3, Pydantic v2, Google Gemini, OpenAI, Few-Shot Prompting |
| **Task 2** | **[Document Q&A Assistant with RAG & Vector Embeddings](./Task2-%20Document%20Q%26A%20Assistant%20with%20Rag%20%26%20Vector%20Embeddings)** | ✅ **Completed** | LangChain, ChromaDB, RecursiveCharacterTextSplitter, Source Page Citations |
| **Task 3** | **[Multi-Tool Autonomous AI Agent](./Task3-%20Multi-Tool%20Autonomous%20AI%20Agent)** | ✅ **Completed** | LangChain, ReAct Engine, DuckDuckGo Search, Safe Math AST, Local File Reader |
| **Task 4** | **[Interactive Full-Stack AI ChatBot with Streamlit](./Task4-%20Interactive%20Full-Stack%20AI%20ChatBot%20with%20Stramlit)** | ✅ **Completed** | Streamlit, Real-Time Token Streaming, Session Memory, RAG & Agent Integration |

---

## 🌟 Task 1: Structured LLM Prompt Pipeline & JSON Extractor

### Overview
Extracts strictly validated structured entities from complex unstructured documents (invoices and resumes) using Google Gemini or OpenAI with parameterized prompt templates, few-shot exemplars, and strict Pydantic v2 schemas.

👉 **Full Project Documentation & Source Code**: [Task 1 Directory](./Task1-%20Structured%20LLM%20Prompt%20Pipeline%20%26%20Json%20Extractor)

### 📸 Execution Screenshots & Test Results

#### 1. Unit Test Suite (All 9 Tests Passing)
![Unit Tests Passing](./Task1-%20Structured%20LLM%20Prompt%20Pipeline%20%26%20Json%20Extractor/screenshots/unit_tests_run.png)

#### 2. Complex Unstructured Invoice Extraction
![Invoice Extraction Output](./Task1-%20Structured%20LLM%20Prompt%20Pipeline%20%26%20Json%20Extractor/screenshots/invoice_extraction_run.png)

#### 3. Resume / CV Parsing & Pydantic Validation
![Resume Extraction Output](./Task1-%20Structured%20LLM%20Prompt%20Pipeline%20%26%20Json%20Extractor/screenshots/resume_extraction_run.png)

---

### Quick Start for Task 1

```powershell
# Navigate to Task 1 directory
cd "Task1- Structured LLM Prompt Pipeline & Json Extractor"

# Install dependencies
pip install -r requirements.txt

# Run the automated unit tests
python -m unittest discover tests

# Run end-to-end demonstration
python main.py --demo
```

---

## 🌟 Task 2: Document Q&A Assistant with RAG & Vector Embeddings

### Overview
Builds an end-to-end Retrieval-Augmented Generation (RAG) system using LangChain, ChromaDB, and Python. Ingests multi-page PDFs and text files, performs recursive semantic chunking with metadata preservation, generates dense vector embeddings, and answers user queries strictly grounded in retrieved document snippets with **exact source page citations**.

👉 **Full Project Documentation & Source Code**: [Task 2 Directory](./Task2-%20Document%20Q%26A%20Assistant%20with%20Rag%20%26%20Vector%20Embeddings)

### 📸 Windows Terminal Execution Screenshots & Proof

#### 1. Unit Test Suite (7/7 Tests Passing)
![Task 2 Unit Tests Passing](./Task2-%20Document%20Q%26A%20Assistant%20with%20Rag%20%26%20Vector%20Embeddings/screenshots/rag_tests_run.png)

#### 2. Multi-Page PDF Q&A with Exact Page Citations
![Task 2 PDF Q&A Run](./Task2-%20Document%20Q%26A%20Assistant%20with%20Rag%20%26%20Vector%20Embeddings/screenshots/rag_pdf_qa_run.png)

#### 3. Interactive CLI Q&A Mode
![Task 2 Interactive Session](./Task2-%20Document%20Q%26A%20Assistant%20with%20Rag%20%26%20Vector%20Embeddings/screenshots/rag_interactive_run.png)

---

### Quick Start for Task 2

```powershell
# Navigate to Task 2 directory
cd "Task2- Document Q&A Assistant with Rag & Vector Embeddings"

# Install dependencies
pip install -r requirements.txt

# Run automated unit tests
python -m unittest discover -v tests

# Run end-to-end demonstration
python main.py --demo

# Ask a specific question against indexed knowledge base
python main.py --query "What is the mandatory retention period for inference metadata?"

# Start interactive Q&A session
python main.py --interactive
```

---

## 🌟 Task 3: Multi-Tool Autonomous AI Agent

### Overview
Builds an autonomous AI agent capable of multi-step reasoning using the ReAct (Reasoning + Acting) loop. The agent dynamically plans, chooses, and executes tools to solve compound research and calculation problems:
- **Real-time Web Search** via DuckDuckGo
- **Safe Python Math Calculator** evaluating mathematical expressions securely
- **Local File Reader** inspecting local JSON, CSV, and text files

👉 **Full Project Documentation & Source Code**: [Task 3 Directory](./Task3-%20Multi-Tool%20Autonomous%20AI%20Agent)

### 📸 Windows Terminal Execution Screenshots & Proof

#### 1. Unit Test Suite (12/12 Tests Passing)
![Task 3 Unit Tests Passing](./Task3-%20Multi-Tool%20Autonomous%20AI%20Agent/screenshots/agent_tests_run.png)

#### 2. Multi-Step Compound Research Query Run
![Task 3 Compound Query](./Task3-%20Multi-Tool%20Autonomous%20AI%20Agent/screenshots/agent_compound_query_run.png)

#### 3. Interactive Console REPL Session
![Task 3 Interactive Session](./Task3-%20Multi-Tool%20Autonomous%20AI%20Agent/screenshots/agent_interactive_run.png)

---

### Quick Start for Task 3

```powershell
# Navigate to Task 3 directory
cd "Task3- Multi-Tool Autonomous AI Agent"

# Install dependencies
pip install -r requirements.txt

# Run automated unit tests
python -m unittest discover -v tests

# Run end-to-end demonstration
python main.py --demo

# Run custom compound query
python main.py --query "Find the 2025 engineering budget in enterprise_budget_2025.json and calculate the allocated budget per engineer based on headcount."

# Start interactive console REPL
python main.py --interactive
```

---

## 🌟 Task 4: Interactive Full-Stack AI ChatBot with Streamlit

### Overview
Wraps the enterprise Knowledge RAG and Autonomous Multi-Tool Agent pipelines into an interactive, full-stack browser-based web application using Streamlit:
- **Real-time token streaming** via `st.write_stream` and generator pipelines
- **Multi-turn conversation memory** with session state management (`st.session_state`) and sliding window pruning
- **Knowledge RAG Mode** with dynamic PDF upload and expandable source citations
- **Autonomous Agent Mode** with live ReAct reasoning trace status updates
- **Chat export** in structured JSON and Markdown formats

👉 **Full Project Documentation & Source Code**: [Task 4 Directory](./Task4-%20Interactive%20Full-Stack%20AI%20ChatBot%20with%20Stramlit)

### 📸 Windows Terminal & Browser UI Screenshots & Proof

#### 1. Interactive Full-Stack Streamlit Web Application (Browser View)
![Streamlit Web UI](./Task4-%20Interactive%20Full-Stack%20AI%20ChatBot%20with%20Stramlit/screenshots/streamlit_ui_rag_chat.png)

#### 2. Streamlit Web Server Launch on Windows
![Streamlit Launch Terminal](./Task4-%20Interactive%20Full-Stack%20AI%20ChatBot%20with%20Stramlit/screenshots/streamlit_terminal_launch.png)

#### 3. Automated Test Suite (8/8 Tests Passing)
![Streamlit App Tests](./Task4-%20Interactive%20Full-Stack%20AI%20ChatBot%20with%20Stramlit/screenshots/streamlit_tests_run.png)

---

### Quick Start for Task 4

```powershell
# Navigate to Task 4 directory
cd "Task4- Interactive Full-Stack AI ChatBot with Stramlit"

# Install dependencies
pip install -r requirements.txt

# Run automated unit tests
python -m unittest discover -v tests

# Launch the Streamlit Web Application
streamlit run app.py
```
*(Open your browser at `http://localhost:8501` to start chatting!)*
