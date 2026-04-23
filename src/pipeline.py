import sys
sys.path.append("src")

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

if __name__ == "__main__":
    collection = "glm"
    ingest("data/sample/0_Fundamental_concepts.pdf", collection)
    
    query = "What is a generalized linear model?"
    answer = ask(query, collection)
    
    print(f"\nQuestion: {query}")
    print(f"\nAnswer: {answer}")