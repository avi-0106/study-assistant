import ollama # type: ignore
import json
import re

def generate_questions(chunks, metadatas, question_type="mcq", count=5, model="llama3.2"):
    
    # Build context from chunks (same pattern as generator.py)
    context = ""
    for chunk, meta in zip(chunks, metadatas):
        context += f"[Page {meta['page']} - {meta['source']}]\n{chunk}\n\n"

    if question_type == "mcq":
        prompt = f"""You are an exam question generator for a Master's level Data Science course.

Generate exactly {count} multiple choice questions based on the context below.

Rules:
- Each question must have exactly 4 options: A, B, C, D
- Only one option is correct
- For each option, write a short explanation (5-6 words) of why it is correct or incorrect
- Base questions strictly on the provided context

Return ONLY a JSON array. No extra text, no markdown. Format:
[
  {{
    "question": "...",
    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "correct": "A",
    "explanations": {{
      "A": "why A is correct or incorrect",
      "B": "why B is correct or incorrect",
      "C": "why C is correct or incorrect",
      "D": "why D is correct or incorrect"
    }}
  }}
]

Context:
{context}"""

    else:
        prompt = f"""You are an exam question generator for a Master's level Data Science course.

Generate exactly {count} long-form exam questions based on the context below.

Rules:
- Questions should require detailed written answers
- Each question must have a model answer
- Base questions strictly on the provided context

Return ONLY a JSON array. No extra text, no markdown. Format:
[
  {{
    "question": "...",
    "model_answer": "..."
  }}
]

Context:
{context}"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response['message']['content']
    
    # LLMs sometimes wrap JSON in ```json ... ``` so we strip that
    raw = re.sub(r"```json|```", "", raw).strip()
    raw = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', raw)
    
    questions = json.loads(raw)
    return questions