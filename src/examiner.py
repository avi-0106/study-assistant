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
- Write a detailed explanation paragraph covering why the correct answer is right and why each of the other options is wrong
- Base questions strictly on the provided context

Return ONLY a JSON array. No extra text, no markdown. Format:
[
  {{
    "question": "...",
    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "correct": "A",
    "explanation": "A detailed paragraph explaining why the correct answer is right and why each wrong option is incorrect"
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
    
    try:
        questions = json.loads(raw)
        return questions
    except json.JSONDecodeError:
        # Retry once if JSON is malformed
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response['message']['content']
        raw = re.sub(r"```json|```", "", raw).strip()
        raw = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', raw)
        questions = json.loads(raw)
        return questions
    
    
def grade_answers(questions_text, answers_text, chunks, metadatas, model="llama3.2"):
    context = ""
    for chunk, meta in zip(chunks, metadatas):
        context += f"[Page {meta['page']} - {meta['source']}]\n{chunk}\n\n"

    prompt = f"""You are a university exam grader for a Master's level Data Science course.

You have been given:
1. The exam questions
2. A student's handwritten answers (transcribed)
3. Relevant lecture material as reference

Your job:
- Grade each answer
- Tell the student what they got right
- Tell them where they went wrong and why
- Point them in the right direction without giving the full correct answer
- Be fair but rigorous

Do NOT give the complete correct answer. Only guide them.

Exam Questions:
{questions_text}

Student's Answers (transcribed from handwriting):
{answers_text}

Lecture Material (reference):
{context}

Provide feedback for each question separately. Be specific and constructive."""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']