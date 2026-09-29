from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie",
    description="A Google Gemini powered learning assistant based on the supplied project specification.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
def qa(payload: TextRequest):
    try:
        return {"result": answer_question(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain")
def explain(payload: TextRequest):
    try:
        return {"result": explain_concept(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz")
def quiz(payload: QuizRequest):
    try:
        return generate_quiz(payload.text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize")
def summarize(payload: TextRequest):
    try:
        return {"result": summarize_text(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations")
def learn(payload: TextRequest):
    try:
        return {"result": get_learning_recommendations(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
