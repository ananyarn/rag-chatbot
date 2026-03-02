================================================================
        RAG//TERMINAL — SETUP GUIDE
================================================================

WHAT YOU NEED INSTALLED BEFORE STARTING
-----------------------------------------
1. Python 3.11+       https://www.python.org/downloads/
2. Ollama             https://ollama.com/download
3. Docker (optional)  https://www.docker.com/products/docker-desktop


================================================================
STEP 1 — DOWNLOAD THE PROJECT
================================================================

Option A: Clone with Git
    git clone https://github.com/YOUR-USERNAME/rag-chatbot.git
    cd rag-chatbot

Option B: Download ZIP from GitHub
    - Click the green "Code" button on GitHub
    - Click "Download ZIP"
    - Extract the folder
    - Open a terminal inside the extracted folder


================================================================
STEP 2 — PULL THE AI MODEL
================================================================

Make sure Ollama is installed, then run:

    ollama pull gemma:2b

This downloads the Gemma AI model (~1.5GB). Wait for it to finish.
You only need to do this once.


================================================================
STEP 3 — SET UP PYTHON ENVIRONMENT
================================================================

Navigate into the backend folder:

    cd backend

Create a virtual environment:

    python -m venv venv

Activate it:

    Windows (PowerShell):   .\venv\Scripts\Activate.ps1
    Windows (CMD):          venv\Scripts\activate.bat
    Mac / Linux:            source venv/bin/activate

You should see (venv) appear at the start of your terminal line.

Install dependencies:

    pip install -r requirements.txt

This takes 5-10 minutes. Let it finish.


================================================================
STEP 4 — START THE CHATBOT
================================================================

Make sure you are still in the backend/ folder with (venv) active.

Start Ollama (if it is not already running):

    ollama serve

Open a second terminal, go to backend/, activate venv again, then run:

    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

You should see:
    INFO: Uvicorn running on http://0.0.0.0:8000


================================================================
STEP 5 — OPEN THE CHATBOT
================================================================

Open your browser and go to:

    http://localhost:8000

The hacker terminal UI will load.


================================================================
STEP 6 — USE THE CHATBOT
================================================================

Without a document:
    - Just type a question and press ENTER
    - The AI answers from its general knowledge (Direct LLM mode)

With a document (RAG mode):
    - Drag and drop a PDF or TXT file into the left sidebar
    - Wait for the "MODE: RAG" indicator to appear
    - Now ask questions — the AI answers from YOUR document


================================================================
DOCKER SETUP (Alternative to Steps 3 & 4)
================================================================

If you have Docker installed, skip Steps 3 & 4 entirely.
From the root rag-chatbot/ folder, just run:

    docker-compose up --build

Then open http://localhost:8000 in your browser.

To stop:
    docker-compose down


================================================================
FOLDER STRUCTURE — WHAT GOES WHERE
================================================================

rag-chatbot/
│
├── backend/              PUT NOTHING HERE MANUALLY
│   ├── main.py           The API server (do not edit unless needed)
│   ├── rag.py            The RAG logic (do not edit unless needed)
│   ├── requirements.txt  Python packages list
│   └── Dockerfile        Docker build instructions
│
├── frontend/
│   └── index.html        The chat UI — open this in a browser
│                         if not using the FastAPI server
│
├── chromadb_data/        AUTO-CREATED when you upload a document
│                         Stores your document embeddings locally
│                         Do not delete unless you want to reset
│
├── uploads/              AUTO-CREATED when you upload a document
│                         Stores your uploaded PDF/TXT files
│
├── docker-compose.yml    Used only if running with Docker
├── README.md             Project overview
└── SETUP.txt             This file


================================================================
COMMON ERRORS AND FIXES
================================================================

Error: "Connection refused on port 11434"
Fix:   Ollama is not running. Run: ollama serve

Error: "model gemma:2b not found"
Fix:   Run: ollama pull gemma:2b

Error: "venv\Scripts\Activate.ps1 cannot be loaded"
Fix:   Run first: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

Error: "ModuleNotFoundError"
Fix:   You forgot to activate venv, or pip install did not finish.
       Activate venv and run: pip install -r requirements.txt again

Error: "host.docker.internal not found" (Linux only)
Fix:   In docker-compose.yml, set network_mode: host
       and change OLLAMA_BASE_URL to http://localhost:11434

Error: Responses are very slow
Fix:   Normal on CPU. gemma:2b is the smallest/fastest model.
       Just wait — it will respond.


================================================================
TO STOP THE CHATBOT
================================================================

In the terminal running uvicorn, press:

    Ctrl + C

That's it.


================================================================
EVERY TIME YOU WANT TO START AGAIN
================================================================

1.  ollama serve                          (in any terminal)
2.  cd rag-chatbot/backend
3.  .\venv\Scripts\Activate.ps1          (Windows PowerShell)
    or: source venv/bin/activate         (Mac/Linux)
4.  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
5.  Open http://localhost:8000

================================================================
