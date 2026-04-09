import httpx

from app.config import settings


async def chat_completion(messages: list[dict]) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.ollama_base_url}/api/chat",
            json={
                "model": settings.ollama_model,
                "messages": messages,
                "stream": False,
            },
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
