import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Paths
CHROMA_PATH = "./chromadb_data"
UPLOADS_PATH = "./uploads"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma:2b")

os.makedirs(CHROMA_PATH, exist_ok=True)
os.makedirs(UPLOADS_PATH, exist_ok=True)

# Embedding model (runs locally, no API needed)
embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def get_vectorstore():
    """Load or create ChromaDB vector store."""
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )

def process_document(file_path: str) -> int:
    """
    Load a document, split into chunks, embed, and store in ChromaDB.
    Returns number of chunks created.
    """
    # 1. Load the document
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
    
    documents = loader.load()
    
    # 2. Split into chunks
    # Why? LLMs have limited context windows. We break docs into ~500 char pieces.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,  # Overlap prevents losing meaning at chunk boundaries
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(documents)
    
    # 3. Store in ChromaDB (embeddings are computed automatically)
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    vectorstore.persist()
    
    print(f"✅ Processed {len(chunks)} chunks from {file_path}")
    return len(chunks)

def ask_question(question: str) -> dict:
    """
    RAG pipeline: retrieve relevant chunks, then ask Gemma.
    """
    vectorstore = get_vectorstore()
    
    # Check if we have any documents stored
    collection = vectorstore._collection
    if collection.count() == 0:
        # No documents uploaded yet — just use the LLM directly
        llm = OllamaLLM(model=MODEL_NAME, base_url=OLLAMA_BASE_URL)
        answer = llm.invoke(question)
        return {
            "answer": answer,
            "sources": [],
            "mode": "direct"
        }
    
    # RAG mode: retrieve then generate
    llm = OllamaLLM(
        model=MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        temperature=0.1  # Lower = more factual, less creative
    )
    
    # Custom prompt that forces the LLM to use the retrieved context
    prompt_template = """You are a helpful assistant. Use the following context from uploaded documents to answer the question. 
If the answer is not in the context, say "I don't have information about that in the uploaded documents."

Context:
{context}

Question: {question}

Answer:"""
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # Build RAG chain
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" = put all chunks into one prompt
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    
    result = qa_chain.invoke({"query": question})
    
    # Extract source info for display
    sources = []
    for doc in result.get("source_documents", []):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "")
        sources.append(f"{os.path.basename(source)}" + (f" (page {page+1})" if page != "" else ""))
    
    return {
        "answer": result["result"],
        "sources": list(set(sources)),  # Deduplicate
        "mode": "rag"
    }

def clear_all_documents() -> dict:
    """Delete all stored embeddings."""
    import shutil
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        os.makedirs(CHROMA_PATH, exist_ok=True)
    return {"message": "All documents cleared successfully"}
