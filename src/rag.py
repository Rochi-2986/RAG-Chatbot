import os
import pickle

from dotenv import load_dotenv
import google.generativeai as genai

from rank_bm25 import BM25Okapi

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from sentence_transformers import CrossEncoder

from google.api_core.exceptions import ResourceExhausted

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

llm = genai.GenerativeModel(
    "gemini-2.5-flash"
)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

chat_history = []

def ask_question(query):
    if not os.path.exists("vectorstore"):
         return {
        "answer": "Please upload a PDF first.",
        "sources": []
    }

    db = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    all_chunks = []
    bm25 = None

    if os.path.exists("chunks.pkl"):

        with open("chunks.pkl", "rb") as f:
            all_chunks = pickle.load(f)

        tokenized_chunks = [
            doc.page_content.lower().split()
            for doc in all_chunks
        ]

        bm25 = BM25Okapi(tokenized_chunks)

    history_text = ""

    for item in chat_history:
        history_text += f"""
User: {item['question']}
Assistant: {item['answer']}
"""

    faiss_docs = db.max_marginal_relevance_search(
        query,
        k=10,
        fetch_k=50
    )


    bm25_results = []

    if bm25 is not None:

        bm25_results = bm25.get_top_n(
            query.lower().split(),
            all_chunks,
            n=5
        )


    candidate_docs = []
    seen = set()

    for doc in faiss_docs + bm25_results:

        text = doc.page_content.strip()

        if text not in seen:
            candidate_docs.append(doc)
            seen.add(text)

    if len(candidate_docs) == 0:

        return {
            "answer": "I could not find that information in the uploaded document.",
            "sources": []
        }


    pairs = [
        (query, doc.page_content)
        for doc in candidate_docs
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(candidate_docs, scores),
        key=lambda x: x[1],
        reverse=True
    )

    docs = [
        doc
        for doc, score in ranked[:8]
    ]


    context = ""
    sources = []

    for i, doc in enumerate(docs):

        page = doc.metadata.get("page")

        if page is not None:
            sources.append(page + 1)

        context += f"\n[Chunk {i+1}]\n"
        context += doc.page_content
        context += "\n"

    print("\nRETRIEVED CONTEXT:\n")
    print(context[:3000])

    print("\nQUESTION:")
    print(query)

    prompt = f"""
You are a Retrieval-Augmented Generation (RAG) assistant.

Use ONLY the information present in the provided context.

Conversation History:
{history_text}

Context:
{context}

Question:
{query}

Rules:

1. Answer ONLY from the context.
2. Combine information from multiple chunks when needed.
3. Do NOT invent facts.
4. If the answer is not found, respond exactly:

I could not find that information in the uploaded document.

5. For summaries, summarize the retrieved content.
6. Answer clearly and naturally.

Answer:
"""

    try:

        response = llm.generate_content(
    prompt,
    generation_config={
        "temperature": 0.1
    }
)

        answer = response.text

    except ResourceExhausted:

        return {
            "answer": "Gemini quota exceeded. Please try again later.",
            "sources": sorted(list(set(sources)))
        }

    except Exception as e:

        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }

    chat_history.append({
        "question": query,
        "answer": answer
    })

    if len(chat_history) > 10:
        chat_history.pop(0)

    print("\nANSWER:\n")
    print(answer)

    return {
        "answer": answer,
        "sources": sorted(list(set(sources)))
    }