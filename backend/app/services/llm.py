import httpx

from app.config import settings


async def chat_completion(messages: list[dict]) -> dict:
    """Call Ollama and return reply + metadata."""
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
        data = response.json()

        total_duration_ms = data.get("total_duration", 0) / 1_000_000
        prompt_tokens = data.get("prompt_eval_count", 0)
        completion_tokens = data.get("eval_count", 0)

        return {
            "content": data["message"]["content"],
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "duration_ms": round(total_duration_ms),
        }
