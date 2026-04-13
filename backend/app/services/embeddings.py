import httpx
from chromadb import Documents, EmbeddingFunction, Embeddings

from app.config import settings

EMBED_MODEL = "nomic-embed-text"


class OllamaEmbeddingFunction(EmbeddingFunction):
    """Use Ollama to generate embeddings instead of ChromaDB's default ONNX model."""

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
