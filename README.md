# RAG Chatbot using FastAPI, FAISS, Gemini & React

## Overview

This project is a Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and ask questions about their contents. The system retrieves relevant information from the uploaded document using semantic search and generates context-aware responses using Google's Gemini LLM.

The chatbot supports both text-based PDFs and scanned PDFs through OCR, making it suitable for academic notes, reports, research papers, manuals, and other document collections.

---

## Features

* PDF document upload
* Automatic text extraction
* OCR support for scanned PDFs
* Semantic search using FAISS vector database
* Hybrid retrieval using:

  * FAISS Vector Search
  * BM25 Keyword Search
  * Cross-Encoder Re-ranking
* Conversational question answering
* Source page references
* React-based chat interface
* FastAPI backend
* Gemini 2.5 Flash integration

---

## Tech Stack

### Backend

* FastAPI
* LangChain
* FAISS
* HuggingFace Embeddings
* Sentence Transformers
* Gemini API
* BM25
* PyPDF
* Tesseract OCR

### Frontend

* React
* Vite
* Axios

### Models

* Embedding Model:

  * BAAI/bge-small-en-v1.5

* Re-ranking Model:

  * cross-encoder/ms-marco-MiniLM-L-6-v2

* LLM:

  * Gemini 2.5 Flash

---

## System Architecture

1. User uploads a PDF.
2. PDF text is extracted.
3. If text extraction fails, OCR is applied.
4. Document is split into chunks.
5. Chunks are embedded using BGE embeddings.
6. Embeddings are stored in FAISS.
7. User asks a question.
8. FAISS retrieves semantically similar chunks.
9. BM25 retrieves keyword-based chunks.
10. Cross-Encoder re-ranks retrieved results.
11. Top chunks are sent to Gemini.
12. Gemini generates a grounded response.
13. Sources are displayed to the user.

---

## Project Structure

```text
rag-chatbot/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── Message.jsx
│   │   │   └── UploadPDF.jsx
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   └── package.json
│
├── src/
│   ├── app.py
│   ├── rag.py
│   ├── ingest_utils.py
│   ├── ingest.py
│   ├── ocr_utils.py
│   └── chat.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-chatbot.git
cd rag-chatbot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Running the Backend

```bash
uvicorn src.app:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## Running the Frontend

```bash
cd frontend
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

## API Endpoints

### Upload PDF

```http
POST /upload
```

Uploads and indexes a PDF document.

### Ask Question

```http
POST /chat
```

Example Request:

```json
{
  "question": "What is clustering?"
}
```

Example Response:

```json
{
  "answer": "Clustering is an unsupervised learning problem...",
  "sources": [1, 3, 5]
}
```

---

## Future Improvements

* Multi-document support
* Chat history persistence
* User authentication
* PDF preview panel
* Streaming responses
* Docker deployment
* Cloud deployment (AWS/GCP/Azure)
* Citation highlighting
* Vector database migration to Pinecone/Weaviate

---

## Resume Highlights

This project demonstrates:

* Retrieval-Augmented Generation (RAG)
* Large Language Model Integration
* Semantic Search
* Information Retrieval
* Vector Databases
* OCR Processing
* Full Stack Development
* API Development
* React Frontend Development
* FastAPI Backend Development

---

## Author

Rochi Sri

B.Tech Information Technology

IIIT Allahabad
