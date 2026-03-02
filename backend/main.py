import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rag import process_document, ask_question, clear_all_documents, UPLOADS_PATH

app = FastAPI(title="Local RAG Chatbot", version="1.0.0")

# Allow browser to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list
    mode: str

@app.get("/health")
def health_check():
    """Simple endpoint to verify the server is running."""
    return {"status": "ok", "message": "RAG Chatbot is running!"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Accept a PDF or TXT file, process it into ChromaDB.
    """
    # Validate file type
    allowed_types = [".pdf", ".txt"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not supported. Use PDF or TXT."
        )
    
    # Save file to disk
    file_path = os.path.join(UPLOADS_PATH, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    try:
        chunks = process_document(file_path)
        return {
            "message": f"Successfully processed '{file.filename}'",
            "chunks_created": chunks,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint. Performs RAG if documents exist, direct LLM otherwise.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        result = ask_question(request.question)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.delete("/clear")
def clear_documents():
    """Remove all uploaded document embeddings."""
    return clear_all_documents()

# Serve frontend files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))
