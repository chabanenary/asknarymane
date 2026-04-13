import chromadb

from app.config import settings
from app.services.embeddings import OllamaEmbeddingFunction

COLLECTION_NAME = "narymane_profile"


def get_collection():
    client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=OllamaEmbeddingFunction(),
    )


def retrieve_context(query: str, n_results: int = 6) -> str:
    """Retrieve relevant chunks from ChromaDB for a given query."""
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=n_results)

    if not results["documents"] or not results["documents"][0]:
        return ""

    # Format each chunk with its source for clarity
    formatted = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        formatted.append(doc)

    return "\n\n".join(formatted)
