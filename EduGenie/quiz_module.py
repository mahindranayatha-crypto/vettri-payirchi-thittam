from pydantic import BaseModel, Field

from gemini_client import generate_text


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


def generate_quiz(passage: str) -> dict:
    prompt = f"""
You are EduGenie's quiz generation module.
Create exactly 3 multiple-choice questions from the passage below.
Each question must have exactly 4 plausible options.
The correct_answer must exactly match one of the four options.
Questions must be answerable from the passage, not from outside knowledge.
Return only the requested JSON structure.

Passage:
{passage}
"""
    raw = generate_text(prompt, response_schema=QuizResponse)
    quiz = QuizResponse.model_validate_json(raw)
    return quiz.model_dump()
