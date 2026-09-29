import os
from functools import lru_cache

from dotenv import load_dotenv

from gemini_client import generate_text

load_dotenv()

LOCAL_MODEL = "MBZUAI/LaMini-Flan-T5-783M"
USE_LOCAL = os.getenv("USE_LOCAL_EXPLANATION", "false").lower() == "true"


@lru_cache(maxsize=1)
def _get_local_pipeline():
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation requires transformers and torch. Install requirements.txt or set USE_LOCAL_EXPLANATION=false."
        ) from exc

    return pipeline(
        "text2text-generation",
        model=LOCAL_MODEL,
        tokenizer=LOCAL_MODEL,
        max_new_tokens=220,
    )


def _local_explain(topic: str) -> str:
    generator = _get_local_pipeline()
    prompt = (
        "Explain this concept for a beginner in simple language. "
        "Use a short definition, key idea, and one example. Keep it concise.\n"
        f"Concept: {topic}"
    )
    result = generator(prompt, do_sample=False)
    return result[0]["generated_text"].strip()


def _gemini_explain(topic: str) -> str:
    prompt = f"""
You are EduGenie's concept explanation module.
Explain the concept below for a beginner using simple, readable language.
Structure the answer as: What it is, How it works, Example, Key takeaway.
Avoid unnecessary jargon and do not invent unsupported facts.

Concept:
{topic}
"""
    return generate_text(prompt)


def explain_concept(topic: str) -> str:
    if USE_LOCAL:
        try:
            return _local_explain(topic)
        except Exception:
            # Keep the prototype usable even when the optional local model is unavailable.
            return _gemini_explain(topic)
    return _gemini_explain(topic)
