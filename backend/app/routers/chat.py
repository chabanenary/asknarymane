from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm import chat_completion

router = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


class ChatResponse(BaseModel):
    reply: str


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        messages = [m.model_dump() for m in request.messages]
        reply = await chat_completion(messages)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")
