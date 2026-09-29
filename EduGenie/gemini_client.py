import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
API_KEY = os.getenv("GEMINI_API_KEY")


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your Google AI Studio API key."
        )
    return genai.Client(api_key=API_KEY)


def generate_text(prompt: str, *, response_schema=None) -> str:
    client = get_client()
    config = {
        "temperature": 0.4,
        "max_output_tokens": 1200,
    }
    if response_schema is not None:
        config.update(
            {
                "response_mime_type": "application/json",
                "response_schema": response_schema,
            }
        )

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config,
    )

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
