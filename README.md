# 📋 AskMyReport

**A privacy-first, Retrieval-Augmented Generation (RAG) chatbot that lets clinicians ask natural-language questions over anonymized medical reports—powered by Groq Cloud for ultra-fast inference.**

---

## 📁 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Data Pipeline](#data-pipeline)
- [Evaluation](#evaluation)
- [Docker](#docker)
- [Security & Compliance](#security--compliance)
- [Contributing](#contributing)

---

## Overview
AskMyReport ingests **de-identified PDF medical reports** (labs, imaging, discharge summaries) into a vector database, then exposes a conversational Gradio UI.  
Questions like *“Which patients had CKD stage 3?”* or *“List all pneumonias”* return concise answers plus **source document citations**.

---

## Features
| ✅ | Description |
|---|---|
| **RAG** | LangChain `RetrievalQA` + Chroma vector store |
| **LLM** | Groq Cloud (Llama-3-8B/70B) – sub-second latency |
| **Privacy** | Runs 100 % locally; only anonymized text leaves for LLM |
| **Multi-format** | Accepts any searchable PDF |
| **Eval** | Built-in golden-set hit-rate & faithfulness metrics |
| **Docker** | One-command containerized deployment |

---

## Tech Stack
| Layer | Tool |
|---|---|
| PDF → Text | `pdfplumber` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector DB | Chroma |
| Orchestration | LangChain |
| LLM | Groq Cloud |
| UI | Gradio |
| De-identification | Presidio (optional) |
| Container | Docker / Docker Compose |

---

## Quick Start 
> ⚠️ **Prerequisites**: Python ≥3.10, 8 GB RAM, Groq API key.

```bash
# 1. Clone
git clone https://github.com/sudheersivakumar/AskMyReport
cd askmyreport

# 2. Virtual env
python -m venv venv
source venv/bin/activate   # Windows venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Secrets
cp .env.example .env
# Edit .env → add GROQ_API_KEY

# 5. Drop anonymized PDFs into data/raw/

# 6. Ingest
python -m src.ingest

# 7. Chat
python -m src.app
# Browser opens http://127.0.0.1:7860
```
---
## Usage
> CLI
```bash
# Re-ingest after adding new reports
python -m src.ingest --chunk-size 600 --chunk-overlap 100
# Evaluate against golden set
python scripts/eval.py
```
---
## Data Pipeline
1. Extract `src/extract.py` → JSON
2. Chunk `src/chunk.py`
3. Embed `src/embed.py` → Chroma
4. Serve `src/app.py`
```mermaid
graph LR
    A[PDF] -->|pdfplumber| B[JSON]
    B -->|chunk| C[CHUNKS]
    C -->|embed| D[CHROMA]
    D -->|LangChain| E[LLM]
    E -->|answer| F[UI]
    
    style A fill:#0a0400
    style B fill:#0a0400
    style C fill:#0a0400
    style D fill:#0a0400
    style E fill:#0a0400
    style F fill:#0a0400
```
---
## Evaluation
 Golden-set questions live in `tests/gold.json`.
 ```bash
python scripts/eval.py
# Output:
# Golden-set size: 10
# Hit-rate      : 90 %
# Faithfulness  : 100 %
```
---
## Docker
```bash
docker compose up --build
# http://localhost:7860
```
---
## Security & Compliance
- No PHI leaves the host (only anonymized text).
- HIPAA-ready:
  - De-identify with `scripts/scrub.py` (Presidio).
  - Run entirely offline; if cloud is required, use customer-managed keys.
- `.env` & `db/` are `.gitignore` -d.
---
## Contributing
1. Fork & branch (`feature/your-feature`).
2. Ensure `pytest && python scripts/eval.py` pass.
3. Open a PR with clear description.
---


