from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm import chat_completion
from app.services.rag import retrieve_context

router = APIRouter()

SYSTEM_PROMPT = """Tu es l'assistant de Narymane Chabane. Narymane est une femme, utilise le féminin.
Réponds aux questions des recruteurs sur son parcours. Sois concise et factuelle.
Utilise UNIQUEMENT les informations ci-dessous. Si tu ne sais pas, dis-le."""


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

        # Get the last user message for retrieval
        last_user_msg = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break

        # Retrieve relevant context from ChromaDB
        context = retrieve_context(last_user_msg) if last_user_msg else ""

        # Inject context as a fake assistant-provided document, then re-ask
        # This pattern works better with small models than system prompt injection
        augmented_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]
        if context:
            augmented_messages.append(
                {"role": "user", "content": "Voici les informations sur Narymane :\n\n" + context}
            )
            augmented_messages.append(
                {"role": "assistant", "content": "Merci, j'ai bien pris note de ces informations sur Narymane. Je vais répondre aux questions en me basant uniquement sur ces données."}
            )
        augmented_messages.extend(messages)

        reply = await chat_completion(augmented_messages)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")
