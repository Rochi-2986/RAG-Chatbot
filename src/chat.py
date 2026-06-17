import os
from dotenv import load_dotenv
import google.generativeai as genai

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

llm = genai.GenerativeModel("gemini-2.5-flash")

print("Loading vector database...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

while True:

    query = input("\nAsk a question: ")

    if query.lower() == "quit":
        break

    docs = db.similarity_search(
        query,
        k=8
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a helpful RAG assistant.

Answer using the provided context.

If the context contains enough information,
provide a complete answer.

If the answer is not found,
say that the information is unavailable.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.generate_content(prompt)

    print("\nANSWER:")
    print("-" * 50)
    print(response.text)