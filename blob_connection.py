# STEP 1: Read PDFs from Azure Blob Storage

import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()

# Get connection string from .env
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME")


def extract_text_from_pdf(pdf_bytes):
    """Extract text from PDF using PyMuPDF"""
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def read_documents_from_blob():
    """Read all documents from blob storage"""
    
    blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service.get_container_client(CONTAINER_NAME)

    documents = []

    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob)

        file_bytes = blob_client.download_blob().readall()

        if blob.name.endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        else:
            text = file_bytes.decode("utf-8")

        documents.append({
            "file_name": blob.name,
            "content": text
        })

    return documents


# # Run
# docs = read_documents_from_blob()

# # Debug print
# for doc in docs:
#     print(f"\n File: {doc['file_name']}")
#     print(doc["content"][:500])