"""Tests for API endpoints."""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# --- Health ---


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- Config ---


@patch("app.routers.chat.settings")
def test_config_groq(mock_settings):
    mock_settings.llm_provider = "groq"
    mock_settings.groq_model = "llama-3.3-70b-versatile"
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "groq"
    assert len(data["models"]) > 0
    assert data["current_model"] == "llama-3.3-70b-versatile"


@patch("app.routers.chat.settings")
def test_config_ollama(mock_settings):
    mock_settings.llm_provider = "ollama"
    mock_settings.ollama_model = "qwen2:1.5b"
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "ollama"
    assert data["models"] == []
    assert data["current_model"] == "qwen2:1.5b"


# --- Chat ---


@patch("app.routers.chat.retrieve_context")
@patch("app.routers.chat.chat_completion", new_callable=AsyncMock)
def test_chat_success(mock_llm, mock_rag):
    mock_rag.return_value = {
        "context": "Narymane worked at Ekinops for 13 years.",
        "sources": ["experience/ekinops_oneaccess.md"],
    }
    mock_llm.return_value = {
        "content": "Narymane a travaillé chez Ekinops pendant 13 ans.",
        "prompt_tokens": 100,
        "completion_tokens": 20,
        "total_tokens": 120,
        "duration_ms": 500,
        "model": "llama-3.3-70b-versatile",
    }

    response = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "Quelle est son expérience ?"}]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "Ekinops" in data["reply"]
    assert data["sources"] == ["experience/ekinops_oneaccess.md"]
    assert data["model"] == "llama-3.3-70b-versatile"
    assert data["total_tokens"] == 120
    assert data["duration_ms"] == 500


@patch("app.routers.chat.retrieve_context")
@patch("app.routers.chat.chat_completion", new_callable=AsyncMock)
def test_chat_with_model_override(mock_llm, mock_rag):
    mock_rag.return_value = {"context": "Some context", "sources": []}
    mock_llm.return_value = {
        "content": "Response",
        "prompt_tokens": 50,
        "completion_tokens": 10,
        "total_tokens": 60,
        "duration_ms": 200,
        "model": "llama-3.1-8b-instant",
    }

    response = client.post(
        "/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "model": "llama-3.1-8b-instant",
        },
    )
    assert response.status_code == 200
    # Verify model override was passed
    mock_llm.assert_called_once()
    call_kwargs = mock_llm.call_args
    assert call_kwargs.kwargs["model_override"] == "llama-3.1-8b-instant"


@patch("app.routers.chat.retrieve_context")
@patch("app.routers.chat.chat_completion", new_callable=AsyncMock)
def test_chat_empty_context(mock_llm, mock_rag):
    mock_rag.return_value = {"context": "", "sources": []}
    mock_llm.return_value = {
        "content": "Je n'ai pas d'information sur ce sujet.",
        "prompt_tokens": 30,
        "completion_tokens": 10,
        "total_tokens": 40,
        "duration_ms": 100,
        "model": "llama-3.3-70b-versatile",
    }

    response = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "Quel est son plat préféré ?"}]},
    )
    assert response.status_code == 200
    assert response.json()["sources"] == []


@patch("app.routers.chat.retrieve_context")
@patch("app.routers.chat.chat_completion", new_callable=AsyncMock)
def test_chat_llm_error(mock_llm, mock_rag):
    mock_rag.return_value = {"context": "Some context", "sources": []}
    mock_llm.side_effect = Exception("Connection refused")

    response = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "Hello"}]},
    )
    assert response.status_code == 502
    assert "LLM error" in response.json()["detail"]


def test_chat_invalid_request():
    response = client.post("/chat", json={})
    assert response.status_code == 422


@patch("app.routers.chat.retrieve_context")
@patch("app.routers.chat.chat_completion", new_callable=AsyncMock)
def test_chat_empty_messages(mock_llm, mock_rag):
    mock_rag.return_value = {"context": "", "sources": []}
    mock_llm.return_value = {
        "content": "Bonjour !",
        "prompt_tokens": 10,
        "completion_tokens": 5,
        "total_tokens": 15,
        "duration_ms": 50,
        "model": "llama-3.3-70b-versatile",
    }
    response = client.post("/chat", json={"messages": []})
    assert response.status_code == 200
