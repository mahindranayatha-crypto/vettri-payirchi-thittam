from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
You are EduGenie's summarization module.
Summarize the educational passage below for quick revision.
Keep the core information, remove repetition, and use clear bullet points when helpful.
Do not add facts that are not supported by the passage.

Passage:
{text}
"""
    return generate_text(prompt)
