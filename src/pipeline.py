import sys
sys.path.append("src")

import chromadb  # type: ignore
from ingestor import load_pdf, chunk_text
from embedder import store_chunks
from retriever import retrieve
from generator import generate

def ingest(file_path, collection_name):
    pages = load_pdf(file_path)
    chunks = chunk_text(pages)
    store_chunks(chunks, collection_name=collection_name)
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
        "data/sample/0_Fundamental_concepts.pdf",
        "data/sample/0_Fundamental_concepts - commented4.pdf",
        "data/sample/0_Introduction - commented.pdf",
        "data/sample/GLM_Intro_Spezialgebiete_SoSe2026.pdf",
        "data/sample/2_1_model_binary_outcome.pdf",
        "data/sample/2_1_model_binary_outcome - commented3.pdf",
    ]

    for pdf in pdfs:
        ingest(pdf, collection)

    query = "What is a generalized linear model?"
    answer = ask(query, collection)

    print(f"\nQuestion: {query}")
    print(f"\nAnswer: {answer}")