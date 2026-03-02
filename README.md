<div align="center">

<img src="https://img.shields.io/badge/STATUS-ONLINE-39ff14?style=for-the-badge&labelColor=050508"/>
<img src="https://img.shields.io/badge/LICENSE-MIT-9b30ff?style=for-the-badge&labelColor=050508"/>
<img src="https://img.shields.io/badge/PYTHON-3.11-bf6fff?style=for-the-badge&labelColor=050508&logo=python&logoColor=bf6fff"/>
<img src="https://img.shields.io/badge/DOCKER-READY-0db7ed?style=for-the-badge&labelColor=050508&logo=docker&logoColor=0db7ed"/>

<br/><br/>

```
██████╗  █████╗  ██████╗    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     
██╔══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     
██████╔╝███████║██║  ███╗      ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     
██╔══██╗██╔══██║██║   ██║      ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     
██║  ██║██║  ██║╚██████╔╝      ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
```

### `// LOCAL AI · RAG · NO API KEYS · 100% OFFLINE`

*A fully local Retrieval-Augmented Generation chatbot powered by **Gemma** + **Ollama***

</div>

---

## ◈ Overview

A fully local **Retrieval-Augmented Generation (RAG)** chatbot built as part of an **AI Advanced Skill Development Lab**. It runs entirely on your machine — no OpenAI, no paid APIs, no internet required after setup.

Upload **PDF** or **TXT** documents and ask questions about them. The chatbot splits your documents into chunks, stores them as vector embeddings in **ChromaDB**, and retrieves the most relevant context before passing it to **Gemma** (via Ollama) to generate accurate, grounded answers.

> Built with FastAPI · LangChain · ChromaDB · and a custom **purple hacker-terminal UI**. Dockerized for easy deployment.

---

## ◈ Features

| Feature | Description |
|---|---|
| 🧠 **Local LLM** | Runs Gemma 2B entirely on your machine via Ollama |
| 📄 **Document Upload** | Drag-and-drop PDF and TXT file support |
| 🔍 **RAG Pipeline** | Retrieves relevant chunks before answering |
| 🗄️ **Vector Storage** | ChromaDB stores embeddings locally as files |
| 🐳 **Dockerized** | One command setup with docker-compose |
| 🔒 **100% Private** | No data leaves your machine, ever |
| 💜 **Hacker UI** | Purple terminal aesthetic with matrix rain |

---

## ◈ Tech Stack

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   FRONTEND        HTML · CSS · Vanilla JS           │
│   BACKEND         Python · FastAPI · Uvicorn        │
│   LLM RUNTIME     Ollama · Gemma 2B                 │
│   RAG FRAMEWORK   LangChain                         │
│   VECTOR DB       ChromaDB                          │
│   EMBEDDINGS      sentence-transformers (local)     │
│   CONTAINERS      Docker · docker-compose           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## ◈ Project Structure

```
rag-chatbot/
├── backend/
│   ├── main.py               # FastAPI routes
│   ├── rag.py                # RAG pipeline logic
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile
├── frontend/
│   └── index.html            # Hacker terminal UI
├── chromadb_data/            # Persisted vector embeddings
├── uploads/                  # Uploaded documents
└── docker-compose.yml
```

---

## ◈ Getting Started

### Prerequisites
- [Ollama](https://ollama.com) installed and running
- [Docker](https://docker.com) installed (optional)
- Python 3.11+

### 1 · Pull the model

```bash
ollama pull gemma:2b
```

### 2 · Install dependencies

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Mac / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3 · Run the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4 · Open the chatbot

Navigate to **http://localhost:8000** in your browser.

---

## ◈ Docker Setup

```bash
# Build and start everything
docker-compose up --build

# Stop
docker-compose down
```

> **Linux users:** If `host.docker.internal` fails, set `network_mode: host` in `docker-compose.yml` and use `OLLAMA_BASE_URL=http://localhost:11434`

---

## ◈ How RAG Works

```
  [ Your PDF / TXT ]
         │
         ▼
  [ Split into chunks ]  ◄─ 500 chars, 50 overlap
         │
         ▼
  [ Embed with MiniLM ]  ◄─ Runs locally
         │
         ▼
  [ Store in ChromaDB ]
         │
    (query time)
         │
  [ Embed your question ]
         │
         ▼
  [ Find top-4 similar chunks ]
         │
         ▼
  [ Feed chunks + question → Gemma ]
         │
         ▼
  [ Answer grounded in your document ]
```

---

## ◈ Usage

1. Start Ollama — `ollama serve`
2. Start backend — `uvicorn main:app --port 8000 --reload`
3. Open `http://localhost:8000`
4. **Drag and drop** a PDF or TXT file into the sidebar
5. Wait for the `MODE: RAG` indicator to activate
6. Ask questions about your document

---

## ◈ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `MODEL_NAME` | `gemma:2b` | Model to use |

---

## ◈ Common Issues

| Error | Fix |
|---|---|
| `Connection refused :11434` | Run `ollama serve` |
| `model not found` | Run `ollama pull gemma:2b` |
| `host.docker.internal` fails | Use `network_mode: host` on Linux |
| Slow responses | Normal on CPU — gemma:2b is the fastest option |

---

<div align="center">

`Built for AI Advanced Skill Development Lab`

<img src="https://img.shields.io/badge/GEMMA-2B-9b30ff?style=flat-square&labelColor=050508"/>
<img src="https://img.shields.io/badge/OLLAMA-LOCAL-bf6fff?style=flat-square&labelColor=050508"/>
<img src="https://img.shields.io/badge/CHROMADB-VECTOR_STORE-7b10df?style=flat-square&labelColor=050508"/>
<img src="https://img.shields.io/badge/LANGCHAIN-RAG-c77dff?style=flat-square&labelColor=050508"/>

</div>
