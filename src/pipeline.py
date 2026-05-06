import sys
sys.path.append("src")

import chromadb  # type: ignore
from ingestor import load_pdf, chunk_text, extract_image_chunks
from embedder import store_chunks
from retriever import retrieve
from generator import generate

def ingest(file_path, collection_name):
    # Text chunks
    pages = load_pdf(file_path)
    chunks = chunk_text(pages)
    store_chunks(chunks, collection_name=collection_name)
    
    # Image chunks
    image_chunks = extract_image_chunks(file_path)
    print(f"Found {len(image_chunks)} image chunks")
    if image_chunks:
        store_chunks(image_chunks, collection_name=collection_name)
        print(f"Stored {len(image_chunks)} image chunks from {file_path}")
    
    print(f"Ingested {file_path} into collection '{collection_name}'")

def ask(query, collection_name):
    chunks, metadatas, distances = retrieve(query, collection_name=collection_name)
    answer = generate(query, chunks, metadatas)
    return answer

def reset_collection(collection_name):
    client = chromadb.PersistentClient(path="vectorstore")
    try:
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' cleared")
    except:
        print(f"Collection '{collection_name}' didn't exist, starting fresh")

if __name__ == "__main__":
    collection = "glm"

    reset_collection(collection)

    pdfs = [
        "data/sample/2_1_model_binary_outcome - commented3.pdf",
    ]

    for pdf in pdfs:
        ingest(pdf, collection)

    query = "What did the handwritten notes say about the three choices of F?"
    answer = ask(query, collection)

    print(f"\nQuestion: {query}")
    print(f"\nAnswer: {answer}")