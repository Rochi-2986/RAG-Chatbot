from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil

from src.rag import ask_question
from src.ingest_utils import create_vectorstore
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "RAG Chatbot API"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    pdf_path = f"documents/{file.filename}"

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = create_vectorstore(pdf_path)

    return {
        "message": "PDF processed",
        "filename": file.filename,
        "chunks": chunks
    }

@app.post("/chat")
def chat(data: Question):

    result = ask_question(data.question)

    return result