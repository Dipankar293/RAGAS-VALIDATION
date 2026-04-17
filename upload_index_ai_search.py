from blob_connection import read_documents_from_blob
from chunking import create_chunks
from embedding import generate_embeddings, prepare_chunks_with_safe_ids

# STEP 4B: Upload documents to Azure AI Search

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv



load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")

AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

search_client = SearchClient(
    endpoint=endpoint,
    index_name=AZURE_SEARCH_INDEX_NAME,
    credential=AzureKeyCredential(key)
)


docs = read_documents_from_blob()
print("Reading Done")
chunked_docs = prepare_chunks_with_safe_ids(docs)
print("Chunking Done")
embedded_docs = generate_embeddings(chunked_docs)
print("Embedding Done")
# Upload documents
result = search_client.upload_documents(documents=embedded_docs)

print("Uploaded:", len(result))