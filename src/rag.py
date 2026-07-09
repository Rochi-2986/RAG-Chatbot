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

llm = genai.GenerativeModel("gemini-2.5-flash")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

chat_history = []


def ask_question(query, pdf_name):

    pdf_folder = os.path.splitext(pdf_name)[0]

    vectorstore_path = os.path.join(
        "vectorstores",
        pdf_folder
    )

    if not os.path.exists(vectorstore_path):
        return {
            "answer": "Please upload a PDF first.",
            "sources": []
        }

    db = FAISS.load_local(
        vectorstore_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    all_chunks = []
    bm25 = None

    chunks_path = os.path.join(
        vectorstore_path,
        "chunks.pkl"
    )

    if os.path.exists(chunks_path):

        with open(chunks_path, "rb") as f:
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
        fetch_k=40
    )

    bm25_results = []

    if bm25 is not None:

        bm25_results = bm25.get_top_n(
            query.lower().split(),
            all_chunks,
            n=10
        )

    candidate_docs = []
    seen = set()

    for doc in faiss_docs + bm25_results:

        text = doc.page_content.strip()

        if text not in seen:
            candidate_docs.append(doc)
            seen.add(text)

    print("Candidate documents:", len(candidate_docs))

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
        for doc, score in ranked[:12]
    ]

    context = ""
    sources = []
    seen_pages = set()

    for i, doc in enumerate(docs):

        page = doc.metadata.get("page")
        preview = doc.page_content.replace("\n", " ")
        if len(preview) > 300:
            preview = preview[:300] + "..."

        if page is not None and page not in seen_pages:
            sources.append({
                "page": page + 1,
                "file": pdf_name,
                "preview": preview
            })
            seen_pages.add(page)
        
        context += f"\n[Chunk {i+1}]\n"
        context += doc.page_content
        context += "\n"

    print("Context length:", len(context))
    print("\nRETRIEVED CONTEXT:\n")
    print(context[:3000])

    print("\nQUESTION:")
    print(query)

    q = query.lower()

    format_instruction = ""

    if any(word in q for word in [
        "bullet",
        "bullets",
        "point",
        "points",
        "list"
    ]):

        format_instruction = """
Return ONLY markdown bullet points.

Example:

- Point 1
- Point 2
- Point 3

Do NOT write paragraphs.
"""

    elif any(word in q for word in [
        "number",
        "numbered",
        "steps"
    ]):

        format_instruction = """
Return a numbered list.

Example:

1. First point
2. Second point
3. Third point
"""

    elif "table" in q:

        format_instruction = """
Return the answer as a markdown table.
"""

    elif "compare" in q:

        format_instruction = """
Return the answer as a comparison table.
"""

    elif "summary" in q:

        format_instruction = """
Return a short summary in one paragraph.
"""

    else:

        format_instruction = """
Return a clear explanation in paragraphs.
"""

    prompt = f"""
You are a Retrieval-Augmented Generation (RAG) assistant.

Use the retrieved context as the PRIMARY source.

If the retrieved context contains only partial information, you may use widely accepted general knowledge to complete the explanation.

Never contradict the retrieved context.

Conversation History:
{history_text}

Context:
{context}

Question:
{query}

Formatting Instructions:
{format_instruction}

Rules:

1. Use the retrieved context as your primary source.
2. Combine information from multiple retrieved chunks when appropriate.
3. If the context provides only partial information, supplement it with widely accepted general knowledge.
4. Never contradict the retrieved context.
5. If the answer cannot be determined from either the context or common knowledge, reply exactly:

I could not find that information in the uploaded document.

6. Follow the formatting instructions exactly.

Answer:
"""

    print("Prompt length:", len(prompt))

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
            "sources": sources
        }

    except Exception as e:

        print(e)

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

    if sources:
        print("Last source:", sources[-1])

    return {
        "answer": answer,
        "sources": sources
    }
    