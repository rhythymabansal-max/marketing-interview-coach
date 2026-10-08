
import json
import os
import re
from dataclasses import dataclass
from typing import Any

try:
    from google import genai
    from google.genai import types
    from pydantic import BaseModel, Field
except ImportError:
    genai = None
    types = None
    class BaseModel: pass
    def Field(*args, **kwargs): return None

from .prompts import SYSTEM_PROMPT, EVALUATION_PROMPT

class Evaluation(BaseModel):
    score: int = Field(ge=0, le=10)
    strengths: list[str]
    missing_points: list[str]
    feedback: str
    improved_answer: str
    tip: str

@dataclass
class EvaluationResult:
    ok: bool
    data: dict[str, Any]
    error: str = ""
    fallback: bool = False

OFF_TOPIC_PATTERNS = [
    r"ignore (all|your|the) instructions", r"reveal (your|the) system prompt", r"show me your prompt",
    r"hack (a|the|this) website", r"malware", r"medical advice", r"diagnos", r"political speech",
    r"write (a|the) political speech", r"bypass your rules", r"jailbreak"
]

def is_off_topic(text: str) -> bool:
    t = text.lower().strip()
    return any(re.search(p, t) for p in OFF_TOPIC_PATTERNS)

def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None

def fallback_evaluation(answer: str, ideal_points: str, question: str) -> EvaluationResult:
    a = answer.strip()
    if len(a) < 20:
        score = 2
        strengths=[]
        missing=["A complete response with a clear definition or approach", "Evidence or practical application"]
        feedback="The response is too brief to demonstrate enough understanding for a fair interview evaluation."
    else:
        tokens = {w.strip(".,;:()[]{}?!").lower() for w in a.split()}
        points=[p.strip() for p in ideal_points.split(";") if p.strip()]
        matched=sum(1 for p in points if any(x.lower() in tokens for x in p.split() if len(x)>4))
        score=min(8, max(4, 4 + matched))
        strengths=["The response addresses the question at a basic level."]
        missing=[f"Consider covering: {p}" for p in points[:3] if p.lower().split()[0] not in a.lower()]
        feedback="A basic fallback evaluation was used because live AI evaluation was unavailable. The response should be made more structured and specific."
    improved=f"A stronger answer would directly answer the question, cover the key concepts ({ideal_points}), and add one practical example or implication."
    data={"score":score,"strengths":strengths,"missing_points":missing or ["Add more specificity and evidence."],"feedback":feedback,"improved_answer":improved,"tip":"Use a simple structure: direct answer → 2–3 key points → practical example → concise conclusion."}
    return EvaluationResult(True,data,"",True)

def evaluate_answer(category, difficulty, question, ideal_points, answer, history=None):
    if is_off_topic(answer):
        return EvaluationResult(True,{"score":0,"strengths":[],"missing_points":["The response is outside the app's interview-preparation scope."],"feedback":"I'm designed to help with marketing and sales interview preparation. Let's continue with your interview practice.","improved_answer":"","tip":"Please answer the interview question shown above."})
    key=get_api_key()
    if not key or genai is None:
        return fallback_evaluation(answer, ideal_points, question)
    try:
        client=genai.Client(api_key=key)
        history_text = history or "No previous answer context."
        prompt=EVALUATION_PROMPT.format(category=category,difficulty=difficulty,question=question,ideal_points=ideal_points,answer=answer,history=history_text[-4000:])
        response=client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=Evaluation,
            ),
        )
        if getattr(response,"parsed",None) is not None:
            parsed=response.parsed
            data=parsed.model_dump() if hasattr(parsed,"model_dump") else dict(parsed)
        else:
            raw=(response.text or "").strip()
            data=json.loads(raw)
        data["score"]=max(0,min(10,int(data.get("score",0))))
        for key2 in ["strengths","missing_points"]:
            if not isinstance(data.get(key2),list): data[key2]=[str(data.get(key2,""))]
        for key2 in ["feedback","improved_answer","tip"]:
            data[key2]=str(data.get(key2,""))
        return EvaluationResult(True,data)
    except Exception as exc:
        return fallback_evaluation(answer, ideal_points, question)
