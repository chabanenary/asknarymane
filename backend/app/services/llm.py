import httpx

from app.config import settings


async def _ollama_chat(messages: list[dict], model: str) -> dict:
    """Call Ollama local API."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.ollama_base_url}/api/chat",
            json={
                "model": model,
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
            "model": model,
        }


async def _groq_chat(messages: list[dict], model: str) -> dict:
    """Call Groq cloud API (OpenAI-compatible)."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.groq_api_key}"},
            json={
                "model": model,
                "messages": messages,
            },
        )
        response.raise_for_status()
        data = response.json()

        usage = data.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_time_ms = round(usage.get("total_time", 0) * 1000)

        return {
            "content": data["choices"][0]["message"]["content"],
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "duration_ms": total_time_ms,
            "model": model,
        }


async def chat_completion(messages: list[dict], model_override: str | None = None) -> dict:
    """Route to the configured LLM provider."""
    if settings.llm_provider == "groq":
        model = model_override or settings.groq_model
        return await _groq_chat(messages, model)
    model = model_override or settings.ollama_model
    return await _ollama_chat(messages, model)
