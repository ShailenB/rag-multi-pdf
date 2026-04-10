import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_faiss_for_pdf(pdf_path):
    pdf_name = os.path.splitext(
        os.path.basename(pdf_path)
    )[0]

    db_path = os.path.join(
        "vector_db",
        pdf_name
    )

    os.makedirs(db_path, exist_ok=True)

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(
        docs,
        embeddings
    )

    vector_store.save_local(db_path)


def build_all_databases():
    books_dir = "Books"

    for file_name in os.listdir(books_dir):
        if file_name.lower().endswith(".pdf"):
            pdf_path = os.path.join(
                books_dir,
                file_name
            )

            print(f"Processing {file_name}")

            create_faiss_for_pdf(pdf_path)

            print(f"Done {file_name}")


if __name__ == "__main__":
    build_all_databases()