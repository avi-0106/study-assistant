import ollama  # type: ignore

def generate(query, chunks, metadatas):
    context = ""
    for chunk, meta in zip(chunks, metadatas):
        context += f"[Page {meta['page']} - {meta['source']}]\n{chunk}\n\n"

    prompt = f"""You are a helpful study assistant. Use the following context from the lecture materials to answer the question. If the answer is not in the context, say so honestly.

    Context:
    {context}

    Question: {query}

    Answer:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']