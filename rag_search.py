# STEP 5: Query + Retrieval

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

# Create client
search_client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(key)
)

# Load same embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

from azure.search.documents.models import VectorizedQuery

def search(query):
    # Step 1: Convert query → embedding
    query_vector = model.encode(query).tolist()

    # Step 2: Create vector query
    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=5,
        fields="embedding"
    )

    # Step 3: Search (NEW SYNTAX)
    results = search_client.search(
        search_text="",  # must NOT be None
        vector_queries=[vector_query]
    )

    retrieved_chunks = []

    for result in results:
        retrieved_chunks.append({
            "content": result["content"],
            "file_name": result["file_name"]
        })

    return retrieved_chunks

