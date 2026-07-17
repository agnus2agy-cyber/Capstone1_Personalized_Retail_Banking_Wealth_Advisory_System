from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import os
from code.db import get_vector_store

load_dotenv()


def ingest_pdf(file_path):
    print("Ingesting started")

    # 1. Load pdf
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 2. Metadata enreachement(for citataion)
    for doc in docs:
        doc.metadata.update(
            {
                "source": file_path,
                "document_extentions": "pdf",
                "page": doc.metadata.get("page"),
                "last_updated": os.path.getmtime(file_path),
            }
        )

    print(docs)
    print("before chucking")

    # 3. Chunk
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(docs)
    print("total chunks")
    print(len(chunks))

    # 4. Load the embedding model
    # 5. generate the embeddings
    vector_store = get_vector_store(collection_name="financial_advisor_support_desk")
    vector_store.add_documents(chunks)

    # 6. Save the embeddings into vector DB
    print("Ingestion Completed")


ingest_pdf("data/")
