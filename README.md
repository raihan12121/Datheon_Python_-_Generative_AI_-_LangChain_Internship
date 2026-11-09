# Datheon AI & LangChain Internship Projects

Repository containing 4 enterprise AI engineering projects covering LLM prompt pipelines, retrieval-augmented generation (RAG), autonomous multi-tool AI agents, and full-stack interactive applications.

---

## 📋 Project Directory & Status

| Task # | Project Name | Status | Tech Stack |
| :---: | :--- | :---: | :--- |
| **Task 1** | **[Structured LLM Prompt Pipeline & JSON Extractor](./Task1-%20Structured%20LLM%20Prompt%20Pipeline%20%26%20Json%20Extractor)** | ✅ **Completed** | Python 3, Pydantic v2, Google Gemini, OpenAI, Few-Shot Prompting |
| **Task 2** | **Document Q&A Assistant with RAG & Vector Embeddings** | 🔄 *Upcoming* | LangChain, Vector DB, Embeddings, Document Loaders |
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

```bash
# Navigate to Task 1 directory
cd "Task1- Structured LLM Prompt Pipeline & Json Extractor"

# Install dependencies
pip install -r requirements.txt

# Run the automated unit tests
python -m unittest discover tests

# Run end-to-end demonstration
python main.py --demo

# Parse a specific invoice or resume
python main.py --type invoice --file sample_inputs/invoice_sample_1.txt
python main.py --type resume --file sample_inputs/resume_sample_1.txt
```
