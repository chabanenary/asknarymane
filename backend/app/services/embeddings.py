import httpx
from chromadb import Documents, EmbeddingFunction, Embeddings

from app.config import settings

EMBED_MODEL = "nomic-embed-text"


class OllamaEmbeddingFunction(EmbeddingFunction):
    """Use Ollama to generate embeddings (dev local with Ollama container)."""

    def __init__(self) -> None:
        pass

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        with httpx.Client(timeout=120.0) as client:
            for text in input:
                response = client.post(
                    f"{settings.ollama_base_url}/api/embed",
                    json={"model": EMBED_MODEL, "input": text},
                )
                response.raise_for_status()
                embeddings.append(response.json()["embeddings"][0])
        return embeddings


def get_embedding_function() -> EmbeddingFunction | None:
    """Return the appropriate embedding function based on config.

    - "ollama" → OllamaEmbeddingFunction (dev, needs Ollama container)
    - "default" → None (ChromaDB's built-in all-MiniLM-L6-v2, prod)
    """
    if settings.embedding_provider == "ollama":
        return OllamaEmbeddingFunction()
    # None = ChromaDB uses its default ONNX embedding model
    return None
