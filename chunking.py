from blob_connection import read_documents_from_blob

docs = read_documents_from_blob()

# STEP 2: Chunking

def chunk_text(text, chunk_size=10000, overlap=500):
    """
    Splits text into overlapping chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(documents):
    """
    Convert documents into chunked format
    """
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{doc['file_name']}_{i}",
                "content": chunk,
                "file_name": doc["file_name"]
            })

    return all_chunks


# # Run
# chunked_docs = create_chunks(docs)

# # Debug
# print(f"Total chunks: {len(chunked_docs)}")
# print("\nSample chunk:\n", chunked_docs[0]["content"][:300])