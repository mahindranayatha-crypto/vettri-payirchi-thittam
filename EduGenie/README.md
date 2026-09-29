# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant implemented from the supplied project specification. The specification describes a FastAPI backend, HTML/CSS frontend, Gemini-powered Q&A, quiz, summary, and learning-path features, plus a LaMini-Flan-T5 concept-explanation module.

## Project structure

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_smoke.py
```

## What the prototype does

- Q&A at `POST /qa`
- Concept explanation at `POST /explain`
- Three-question, four-option quiz at `POST /quiz`
- Summarization at `POST /summarize`
- Learning recommendations at `POST /learn/recommendations`
- Simple browser UI at `/`
- Health check at `/health`

## Setup in VS Code

### 1. Open the project

Open the `EduGenie` folder in VS Code.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy `.env.example` to `.env` and add your Google AI Studio API key:

```text
GEMINI_API_KEY=your_real_key_here
```

Do not put the key in `index.html`, `app.js`, or other frontend files.

### 5. Run

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Which is the largest ocean?\"}"
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"The water cycle includes evaporation, condensation and precipitation.\"}"
```

## Optional local concept explanation

The source specification calls for `MBZUAI/LaMini-Flan-T5-783M` locally. Set:

```text
USE_LOCAL_EXPLANATION=true
```

The model is loaded lazily on the first explanation request. If it cannot load, EduGenie falls back to Gemini so the prototype remains usable.

For a laptop demo, keeping `USE_LOCAL_EXPLANATION=false` is the simplest path because it avoids the extra local-model download on first use.

## Testing

Run the smoke tests without calling Gemini:

```bash
python -m pytest
```

## Notes on the original specification

The supplied document names Gemini 1.5 Pro and a legacy-style integration approach. This implementation keeps the requested feature set and module names but uses Google's current `google-genai` SDK. The Gemini model is configurable through `GEMINI_MODEL` in `.env` so the prototype can follow the currently available model for your account.
