# Datheon AI & LangChain Internship Projects

Repository containing 4 enterprise AI engineering projects covering LLM prompt pipelines, retrieval-augmented generation (RAG), autonomous multi-tool AI agents, and full-stack interactive applications.

---

## 📋 Project Directory & Status

| Task # | Project Name | Status | Tech Stack |
| :---: | :--- | :---: | :--- |
| **Task 1** | **[Structured LLM Prompt Pipeline & JSON Extractor](./Task1-%20Structured%20LLM%20Prompt%20Pipeline%20%26%20Json%20Extractor)** | ✅ **Completed** | Python 3, Pydantic v2, Google Gemini, OpenAI, Few-Shot Prompting |
| **Task 2** | **[Document Q&A Assistant with RAG & Vector Embeddings](./Task2-%20Document%20Q%26A%20Assistant%20with%20Rag%20%26%20Vector%20Embeddings)** | ✅ **Completed** | LangChain, ChromaDB, RecursiveCharacterTextSplitter, Source Page Citations |
| **Task 3** | **Multi-Tool Autonomous AI Agent** | 🔄 *Upcoming* | LangChain / LangGraph, Tool Calling, Agent Reasoning |
| **Task 4** | **Interactive Full-Stack AI ChatBot with Streamlit** | 🔄 *Upcoming* | Streamlit, Multi-turn Chat, LLMs, UI/UX |

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
