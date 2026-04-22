import chromadb  # type: ignore
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction # type: ignore

#reusable setup function that returns a ready-to-use connection to the local embedding model(nomic-embed-text)
def get_embedding_function():
    return OllamaEmbeddingFunction(
        url = "http://localhost:11434/api/embeddings",
        model_name = "nomic-embed-text"
    )

def store_chunks(chunks, collection_name = "study_assistant"):
    client = chromadb.PersistentClient(path="vectorstore") # DB client to keep the vectors

    collection = client.get_or_create_collection(
        name = collection_name,
        embedding_function = get_embedding_function() # fetching the model being used for embedding
    )
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk["text"]],
            metadatas=[{"page": chunk["page"], "source": chunk["source"]}],
            ids=[f"chunk_{i}"]
        )
    print(f"Stored {len(chunks)} chunks in Chroma")
    return collection