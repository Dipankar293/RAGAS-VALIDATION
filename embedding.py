from blob_connection import read_documents_from_blob
from chunking import create_chunks

import re
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


# 🔹 STEP 1: Clean ID (VERY IMPORTANT)
def clean_id(text):
    """
    Convert string to Azure-safe ID
    """
    text = text.replace(" ", "_")  # replace spaces
    text = re.sub(r"[^a-zA-Z0-9_\-=]", "", text)  # remove invalid chars
    return text


# 🔹 STEP 2: Attach Clean IDs to chunks
def prepare_chunks_with_safe_ids(docs):
    chunked_docs = create_chunks(docs)

    for chunk in chunked_docs:
        raw_id = chunk["id"]
        chunk["id"] = clean_id(raw_id)

    return chunked_docs


# 🔹 STEP 3: Generate embeddings
def generate_embeddings(chunked_docs):
    """Generate embeddings for all chunks"""

    texts = [chunk["content"] for chunk in chunked_docs]

    # Batch embedding (FAST)
    embeddings = model.encode(texts, show_progress_bar=True)

    embedded_docs = []

    for i, chunk in enumerate(chunked_docs):
        embedded_docs.append({
            "id": chunk["id"],  # already cleaned
            "content": chunk["content"],
            "embedding": embeddings[i].tolist(),
            "file_name": chunk["file_name"]
        })

    return embedded_docs


# # 🔹 RUN PIPELINE (END-TO-END)

# # Step 1: Read documents from blob
# docs = read_documents_from_blob()

# # Step 2: Chunk + clean IDs
# chunked_docs = prepare_chunks_with_safe_ids(docs)

# # Debug: check IDs
# print("Sample Clean ID:", chunked_docs[0]["id"])

# # Step 3: Generate embeddings
# embedded_docs = generate_embeddings(chunked_docs)

# # Debug
# print(f"Total embedded docs: {len(embedded_docs)}")
# print("Embedding length:", len(embedded_docs[0]["embedding"]))