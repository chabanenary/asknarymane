from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm import chat_completion
from app.services.rag import retrieve_context

router = APIRouter()

SYSTEM_PROMPT = """You are the virtual assistant of Narymane Chabane. Narymane is a woman — always use feminine pronouns and adjectives when referring to her.
You answer recruiters' questions about her professional background, education, skills, and projects.
Rules:
- Answer ONLY based on the provided context. Never make up information.
- If the context does not contain the answer, say so honestly.
- Reply in the same language as the user's question (French or English).
- Be concise, professional, and factual.
- Use markdown formatting (bold, lists) for readability."""


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = []
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    duration_ms: int = 0


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        messages = [m.model_dump() for m in request.messages]

        # Get the last user message for retrieval
        last_user_msg = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break

        # Retrieve relevant context from ChromaDB
        rag_result = retrieve_context(last_user_msg) if last_user_msg else {"context": "", "sources": []}
        context = rag_result["context"]
        sources = rag_result["sources"]

        # Inject context as a fake assistant-provided document
        augmented_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]
        if context:
            augmented_messages.append(
                {"role": "user", "content": "Here is the information about Narymane:\n\n" + context}
            )
            augmented_messages.append(
                {"role": "assistant", "content": "Understood. I will answer questions based only on the provided information about Narymane."}
            )
        augmented_messages.extend(messages)

        result = await chat_completion(augmented_messages)
        return ChatResponse(
            reply=result["content"],
            sources=sources,
            prompt_tokens=result["prompt_tokens"],
            completion_tokens=result["completion_tokens"],
            total_tokens=result["total_tokens"],
            duration_ms=result["duration_ms"],
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")
