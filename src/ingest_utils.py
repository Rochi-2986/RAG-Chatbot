from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


def create_vectorstore(pdf_path):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("Pages loaded:", len(documents))

    all_text = ""

    for i, doc in enumerate(documents):
        print(f"Page {i+1} chars:", len(doc.page_content))
        all_text += doc.page_content

    if len(all_text.strip()) == 0:

        print("No text found. Running OCR...")

        images = convert_from_path(
            pdf_path,
            poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
        )

        ocr_text = ""

        for image in images:
            ocr_text += pytesseract.image_to_string(image)

        if len(ocr_text.strip()) == 0:
            raise Exception("No text found in PDF and OCR failed.")

        documents = [
            Document(page_content=ocr_text)
        ]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300
    )

    chunks = splitter.split_documents(documents)

    print("Chunks created:", len(chunks))

    import pickle

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    import os

    db = FAISS.from_documents(
        chunks,
        embeddings
    )

    print("Saving vectorstore...")

    db.save_local("vectorstore")

    print("Vectorstore saved!")

    print("Current directory:", os.getcwd())
    print("Vectorstore exists:", os.path.exists("vectorstore"))
    print("FAISS file exists:", os.path.exists("vectorstore/index.faiss"))
    print("PKL file exists:", os.path.exists("vectorstore/index.pkl"))

    return len(chunks)