import ollama  # type: ignore

def generate(query, chunks, metadatas, model="llama3.2"):
    context = ""
    for chunk, meta in zip(chunks, metadatas):
        context += f"[Page {meta['page']} - {meta['source']}]\n{chunk}\n\n"

    prompt = f"""You are an expert academic tutor helping a Master's student in Data Science at TU Dortmund understand their course material.

Your job is to:
- Answer questions clearly and precisely using the provided context
- Explain concepts in a way that builds genuine understanding, not just memorization
- Use examples where helpful
- If the answer is not fully in the context, say so honestly but still help with what you know
- Keep answers focused and structured
- Keep answers concise and under 200 words unless the question genuinely requires more detail

Context from lecture materials:
{context}

Question: {query}

Answer:"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']