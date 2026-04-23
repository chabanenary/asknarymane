from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.services.llm import chat_completion
from app.services.agent import resolve_query

GROQ_MODELS = [
    {"id": "llama-3.3-70b-versatile", "name": "Llama 3.3 70B"},
    {"id": "qwen/qwen3-32b", "name": "Qwen 3 32B"},
    {"id": "meta-llama/llama-4-scout-17b-16e-instruct", "name": "Llama 4 Scout 17B"},
    {"id": "llama-3.1-8b-instant", "name": "Llama 3.1 8B"},
]

router = APIRouter()

SYSTEM_PROMPT = """You are the virtual assistant of Narymane Chabane. Narymane is a woman — always use feminine pronouns and adjectives when referring to her.
You answer recruiters' questions about her professional background, education, skills, and projects.
You have access to two data sources:
- Her professional profile (CV, experience, education, projects)
- Her GitHub repositories in real-time (github.com/chabanenary)
Rules:
- Answer ONLY based on the provided context. Never make up information.
- If the context does not contain the answer, say so honestly.
- Reply in the same language as the user's question (French or English).
- Be concise, professional, and factual.
- Use markdown formatting (bold, lists) for readability.
- When showing GitHub data, mention that it is real-time information."""


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    model: str | None = None


class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = []
    model: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    duration_ms: int = 0


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/config")
async def get_config():
    """Return provider info and available models."""
    return {
        "provider": settings.llm_provider,
        "models": GROQ_MODELS if settings.llm_provider == "groq" else [],
        "current_model": settings.groq_model if settings.llm_provider == "groq" else settings.ollama_model,
    }


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

        # Build enriched query: if the last message is short or contains
        # references (ça, this, these), combine with previous exchange for better retrieval
        search_query = last_user_msg
        if last_user_msg and len(messages) >= 3:
            prev_messages = []
            for msg in messages[-4:-1]:  # last 2 messages before current
                prev_messages.append(msg["content"])
            if any(ref in last_user_msg.lower() for ref in ["ça", "cela", "this", "these", "that", "it", "les", "ces", "c'est"]):
                search_query = " ".join(prev_messages[-2:]) + " " + last_user_msg

        # Resolve query via agent (RAG + GitHub)
        agent_result = resolve_query(search_query) if last_user_msg else {"context": "", "sources": []}
        context = agent_result["context"]
        sources = agent_result["sources"]

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
        # Send recent conversation history (last 3 exchanges) for context continuity
        # This allows the LLM to understand references like "ça", "this", etc.
        recent = messages[-6:]  # last 3 exchanges (user+assistant pairs)
        augmented_messages.extend(recent)

        result = await chat_completion(augmented_messages, model_override=request.model)
        return ChatResponse(
            reply=result["content"],
            sources=sources,
            model=result.get("model", ""),
            prompt_tokens=result["prompt_tokens"],
            completion_tokens=result["completion_tokens"],
            total_tokens=result["total_tokens"],
            duration_ms=result["duration_ms"],
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")
