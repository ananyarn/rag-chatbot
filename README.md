# RAG TERMINAL

> A fully local AI chatbot with document upload and RAG. No API keys. No internet. Runs entirely on your machine.

## What it does

Upload a PDF or TXT file and ask questions about it. The chatbot retrieves relevant sections from your document and uses **Gemma 2B** (via Ollama) to answer — all locally, all private.

Without a document, it works as a general-purpose AI assistant.

---

## Stack

| Layer | Tool |
|---|---|
| LLM | Gemma 2B · Ollama |
| Backend | Python · FastAPI · LangChain |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers |
| Frontend | HTML · CSS · JS |
| Deploy | Docker · docker-compose |

---

## Setup

> Full walkthrough → **[SETUP.txt](./SETUP.txt)**

```bash
# 1. Pull the model
ollama pull gemma:2b

# 2. Create environment
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
source venv/bin/activate       # Mac/Linux

# 3. Install and run
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000**

**Docker alternative:**
```bash
docker-compose up --build
```

---

## Project structure

```
rag-chatbot/
├── backend/
│   ├── main.py            API server
│   ├── rag.py             RAG pipeline
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── index.html         Chat UI
├── chromadb_data/         Auto-created · stores embeddings
├── uploads/               Auto-created · stores your files
├── docker-compose.yml
├── README.md
└── SETUP.txt              Full setup guide
```

---

## Common errors

| Error | Fix |
|---|---|
| Connection refused :11434 | `ollama serve` |
| model not found | `ollama pull gemma:2b` |
| Activate.ps1 blocked | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Slow responses | Normal on CPU — just wait |

---

*Built for AI Advanced Skill Development Lab*
