#  RAG PDF Chatbot

A modern **Retrieval-Augmented Generation (RAG)** chatbot that allows users to upload PDF documents and ask natural language questions. The system combines semantic search, keyword retrieval, re-ranking, OCR, and Google's Gemini LLM to provide accurate, context-aware answers with source citations.

---

#  Features

-  Upload multiple PDF documents
-  Separate chat history for each uploaded PDF
-  Hybrid Retrieval
  - FAISS Semantic Search
  - BM25 Keyword Search
  - Cross-Encoder Re-ranking
-  Gemini 2.5 Flash for answer generation
-  Source page citations
-  Clickable source previews
-  OCR support for scanned PDFs
-  Automatic formatting
  - Bullet Points
  - Numbered Lists
  - Tables
  - Paragraph Summaries
-  FastAPI backend
-  Modern React Dark UI
-  Auto-scroll chat
-  Persistent chat history using Local Storage

---

#  Demo

> Add screenshots or GIFs here.

Example:

```
frontend/screenshots/demo.png
```

---

#  System Architecture

```
                  PDF Upload
                       │
                       ▼
               Text Extraction
                       │
          ┌────────────┴────────────┐
          │                         │
      Text PDF                Scanned PDF
          │                         │
          ▼                         ▼
     PyPDFLoader                  OCR
                              (Tesseract)
          │
          ▼
      Text Chunking
          │
          ▼
 HuggingFace Embeddings
          │
          ▼
      FAISS Vector DB
          │
 ┌────────┴─────────┐
 │                  │
 ▼                  ▼
FAISS           BM25 Search
Search
 │                  │
 └────────┬─────────┘
          ▼
 Cross Encoder Re-ranking
          ▼
     Top Relevant Chunks
          ▼
     Gemini 2.5 Flash
          ▼
Formatted Response + Sources
```

---

#  Tech Stack

## Backend

- FastAPI
- LangChain
- FAISS
- Google Gemini API
- BM25
- Sentence Transformers
- HuggingFace Embeddings
- Tesseract OCR
- PyPDFLoader

---

## Frontend

- React
- Vite
- Axios
- CSS3

---

## Models

### Embedding Model

```
BAAI/bge-small-en-v1.5
```

### Re-ranking Model

```
cross-encoder/ms-marco-MiniLM-L-6-v2
```

### LLM

```
Gemini 2.5 Flash
```

---

#  Project Structure

```
rag-chatbot/

│
├── frontend/
│   ├── src/
│   │
│   ├── components/
│   │      ChatBox.jsx
│   │      UploadPDF.jsx
│   │      SourceCard.jsx
│   │
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
│
├── src/
│      app.py
│      rag.py
│      ingest_utils.py
│
├── documents/
│
├── vectorstores/
│
├── requirements.txt
│
├── .env
│
└── README.md
```

---

#  Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-chatbot.git
cd rag-chatbot
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

#  Environment Variables

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

#  Run Backend

```bash
uvicorn src.app:app --reload
```

Backend

```
http://localhost:8000
```

Swagger Docs

```
http://localhost:8000/docs
```

---

#  Run Frontend

```bash
cd frontend
npm run dev
```

Frontend

```
http://localhost:5173
```

---

#  API Endpoints

## Upload PDF

```
POST /upload
```

Response

```json
{
  "message": "PDF processed",
  "filename": "Notes.pdf",
  "chunks": 45
}
```

---

## Ask Question

```
POST /chat
```

Request

```json
{
  "question":"What is DNA?",
  "pdf":"Biology.pdf"
}
```

Response

```json
{
  "answer":"DNA is Deoxyribonucleic Acid...",
  "sources":[
    {
      "page":8,
      "file":"Biology.pdf",
      "preview":"DNA is a double helix..."
    }
  ]
}
```

---

#  Retrieval Pipeline

```
User Question
      │
      ▼
Semantic Search (FAISS)

      +
Keyword Search (BM25)

      ▼

Merge Results

      ▼

Cross Encoder Re-ranking

      ▼

Top Relevant Chunks

      ▼

Gemini 2.5 Flash

      ▼

Grounded Answer
```

---

#  Key Features

### Hybrid Retrieval

- FAISS retrieves semantically similar chunks.
- BM25 retrieves exact keyword matches.
- CrossEncoder re-ranks the retrieved chunks.

---

### OCR Support

If a PDF contains scanned pages or images,

the chatbot automatically switches to OCR using Tesseract.

---

### Multi PDF Support

Each uploaded PDF gets

- Separate vector database
- Separate chat history
- Independent retrieval

---

### Source References

Every answer displays

- PDF name
- Page number
- Clickable preview of retrieved content

---

### Smart Formatting

The chatbot automatically formats responses into

- Bullet Points
- Numbered Lists
- Tables
- Summaries
- Paragraphs

based on the user's query.

---

# Future Improvements

- Multi-document querying
- Streaming responses
- Authentication
- PDF viewer with highlighted citations
- Drag & Drop upload
- Pinecone / ChromaDB support
- Docker deployment
- AWS deployment
- User accounts

---

#  Skills Demonstrated

- Retrieval-Augmented Generation (RAG)
- Large Language Models
- Information Retrieval
- Semantic Search
- Hybrid Search
- OCR
- Prompt Engineering
- Vector Databases
- FastAPI
- React
- REST APIs
- Full Stack Development

---

#  Author

**Rochi Sri**

B.Tech Information Technology

Indian Institute of Information Technology Allahabad (IIIT Allahabad)

GitHub: https://github.com/Rochi-2986

LinkedIn: https://www.linkedin.com/in/Rochi-2986/