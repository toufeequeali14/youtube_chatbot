import uvicorn

import common.config  # noqa: F401  (must be first)

import re

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.pipeline import get_or_build_vector_store
from core.rag_engine import answer_question

app = FastAPI(title="YouTube Chatbot")

VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")
_vector_stores = {}  # in-memory cache: video_id -> vector store


class AskRequest(BaseModel):
    video_id: str
    question: str


class AskResponse(BaseModel):
    video_id: str
    question: str
    answer: str


def get_store(video_id: str):
    if video_id not in _vector_stores:
        _vector_stores[video_id] = get_or_build_vector_store(video_id)
    return _vector_stores[video_id]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not VIDEO_ID_PATTERN.match(request.video_id):
        raise HTTPException(status_code=400, detail="Invalid YouTube video id")
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty")

    try:
        vector_store = get_store(request.video_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not get transcript: {e}")

    try:
        answer = answer_question(vector_store, request.question)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e}")

    return AskResponse(
        video_id=request.video_id, question=request.question, answer=answer
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)