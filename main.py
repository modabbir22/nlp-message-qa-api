# main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import requests
import re

# ---------- Config ----------

BASE_URL = "https://november7-730026606190.europe-west1.run.app"
MESSAGES_ENDPOINT = f"{BASE_URL}/messages"  # no trailing slash to be safe

# ---------- FastAPI App ----------

app = FastAPI(
    title="Member QA Service",
    description="Simple question-answering API over member messages.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

# ---------- NLP Utilities ----------

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "to", "of", "and", "or",
    "for", "in", "on", "at", "with", "from", "by", "when", "what", "how",
    "does", "do", "have", "has", "had", "about", "planning", "plan", "who",
    "where", "which", "this", "that", "it", "their", "his", "her", "many",
    "favorite", "favorites"
}

WORD_PATTERN = re.compile(r"[a-zA-Z]+")


def tokenize(text: str) -> List[str]:
    """Lowercase tokenization with basic stopword filtering."""
    words = WORD_PATTERN.findall(text.lower())
    return [w for w in words if w not in STOPWORDS]

# ---------- Upstream API Access ----------

def fetch_messages() -> List[Dict[str, Any]]:
    try:
        resp = requests.get(MESSAGES_ENDPOINT, timeout=10)
        # If upstream returns 402, handle it explicitly
        if resp.status_code == 402:
            raise HTTPException(
                status_code=503,
                detail="Upstream /messages API returned 402 Payment Required. "
                       "Cannot fetch member messages at this time."
            )
        resp.raise_for_status()
    except HTTPException:
        # Re-raise our explicit HTTPException above
        raise
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error calling /messages API: {e}")

    data = resp.json()

    if isinstance(data, dict) and "items" in data:
        return data["items"]
    if isinstance(data, list):
        return data

    raise HTTPException(status_code=500, detail="Unexpected /messages API format")


# ---------- Message Processing ----------

def build_searchable_text(message: Dict[str, Any]) -> str:
    """
    Build a searchable string from a message:
    combine user_name + message text.
    """
    parts = []

    user_name = message.get("user_name")
    if user_name:
        parts.append(str(user_name))

    text = message.get("message")
    if text:
        parts.append(str(text))

    if not parts:
        parts.append(str(message))

    return " ".join(parts)


def extract_answer_from_message(message: Dict[str, Any]) -> str:
    """
    Return a human-readable answer from the best-matching message.
    """
    user = message.get("user_name", "")
    text = message.get("message", "")

    if user and text:
        return f"{user}: {text}"
    if text:
        return text
    return str(message)


def score_message(question_tokens: List[str], message_text: str) -> int:
    """Simple keyword-overlap score between question tokens and message tokens."""
    message_tokens = set(tokenize(message_text))
    question_set = set(question_tokens)
    return len(question_set & message_tokens)

# ---------- Core QA Logic ----------

def _handle_question(question: str) -> AskResponse:
    question = question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty")

    question_tokens = tokenize(question)
    if not question_tokens:
        raise HTTPException(
            status_code=400,
            detail="Could not parse meaningful tokens from question",
        )

    messages = fetch_messages()
    if not messages:
        raise HTTPException(
            status_code=500,
            detail="No messages available from upstream API",
        )

    best_score = -1
    best_message = None

    for msg in messages:
        searchable = build_searchable_text(msg)
        score = score_message(question_tokens, searchable)
        if score > best_score:
            best_score = score
            best_message = msg

    if best_message is None or best_score <= 0:
        return AskResponse(
            answer="Sorry, I couldn't find an answer to that question in the member messages."
        )

    answer_text = extract_answer_from_message(best_message)
    return AskResponse(answer=answer_text)

# ---------- API Endpoints ----------

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/ask", response_model=AskResponse)
def ask_get(
    question: str = Query(..., description="Natural-language question about members"),
):
    """GET /ask?question=..."""
    return _handle_question(question)


@app.post("/ask", response_model=AskResponse)
def ask_post(payload: AskRequest):
    """POST /ask with JSON body { "question": "..." }"""
    return _handle_question(payload.question)
