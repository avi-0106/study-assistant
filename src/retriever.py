import chromadb  # type: ignore
from embedder import get_embedding_function

def retrieve(query, collection_name="study_assistant", n_results=3):
    client = chromadb.PersistentClient(path="vectorstore")
    collection = client.get_collection(
        name=collection_name,
        embedding_function=get_embedding_function()
    )
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0], results["distances"][0]