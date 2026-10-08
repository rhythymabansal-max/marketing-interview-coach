
# Marketing Interview Coach AI

A Streamlit + Google Gemini application for marketing and sales interview preparation. It asks one question at a time, evaluates answers with a fixed rubric, provides improvement feedback, and produces a final performance summary.

## Features
- 40-question built-in CSV question bank across 7 categories
- Beginner / Intermediate / Advanced difficulty
- Quick Quiz, Mock Interview, Practice by Topic
- Structured 0–10 AI evaluation: relevance, accuracy, conceptual understanding, structure, practical application, communication clarity
- Strengths, missing points, feedback, improved answer, actionable tip
- Guardrails for off-topic/adversarial inputs
- Input validation and graceful API fallback
- Streamlit session-state interview continuity
- Final performance summary and TXT download
- No hard-coded API key

## Architecture
`app.py` → `question_manager.py` → `evaluator.py` → Gemini API → structured JSON feedback.

The app does **not** use RAG, fine-tuning, or a persistent database.

## Local setup
1. Install Python 3.12.
2. Create a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`, or export it in your shell. The code also supports Streamlit secrets on Community Cloud.
5. Run: `streamlit run app.py`

If using `.env` locally, export the variable in your shell because this minimal project intentionally avoids adding another dependency just for dotenv handling. On Windows PowerShell:
`$env:GEMINI_API_KEY="YOUR_KEY"`

## Streamlit Community Cloud deployment
Streamlit Community Cloud deploys from GitHub. Push this folder to a GitHub repository with `app.py` and `requirements.txt` at the repository root. In `share.streamlit.io`, choose Create app, select the repository/branch and `app.py`, then deploy. In Advanced settings → Secrets, add:

```toml
GEMINI_API_KEY = "YOUR_KEY"
```

Never commit `.env` or `secrets.toml`.

## Getting the Gemini API key
Create an API key in Google AI Studio, copy it once, and store it only in the local environment or Streamlit Secrets. Never paste it into `app.py`, CSV files, README, screenshots, or the GitHub repository.

## Demo flow
Marketing Fundamentals → Intermediate → Mock Interview/Quick Quiz → Start → answer a question → show AI evaluation → Next Question → demonstrate an adversarial answer → continue → finish → download summary.

## Privacy disclosure
When live AI evaluation is enabled, the candidate's answer and relevant question context are sent to Google's Gemini API. Users should avoid entering sensitive personal information.
