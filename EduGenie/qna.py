from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a concise educational assistant for students.
Answer the question accurately and clearly.
Use simple language, define unfamiliar terms, and use a short example when useful.
Do not invent citations or sources.

Student question:
{question}
"""
    return generate_text(prompt)
