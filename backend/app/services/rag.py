import chromadb

from app.config import settings
from app.services.embeddings import OllamaEmbeddingFunction

COLLECTION_NAME = "narymane_profile"
MAX_DISTANCE = 1.2

# Map keywords to document categories
CATEGORY_KEYWORDS = {
    "experience": ["expérience", "experience", "travail", "poste", "emploi", "entreprise", "ekinops", "oneaccess", "vxworks", "embarqué", "embedded", "career", "job", "work"],
    "education": ["études", "formation", "diplôme", "école", "université", "master", "bac", "polytechnique", "telecom", "education", "degree", "school"],
    "projects": ["projet", "project", "gallerykeeper", "yologk", "asknarymane", "application", "app", "github"],
    "cv": ["compétence", "skill", "profil", "cv", "résumé", "contact", "langue", "language", "aspiration"],
    "blog": ["blog", "article", "publication", "open source", "communauté", "community"],
}


def detect_categories(query: str) -> list[str]:
    """Detect relevant categories from the query."""
    query_lower = query.lower()
    matched = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            matched.append(category)
    return matched


def get_collection():
    client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=OllamaEmbeddingFunction(),
    )


def retrieve_context(query: str, n_results: int = 6) -> dict:
    """Retrieve relevant chunks, filtered by category and similarity."""
    collection = get_collection()
    categories = detect_categories(query)

    where_filter = None
    if categories:
        if len(categories) == 1:
            where_filter = {"category": categories[0]}
        else:
            where_filter = {"category": {"$in": categories}}

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    if not results["documents"] or not results["documents"][0]:
        if where_filter:
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"],
            )

    if not results["documents"] or not results["documents"][0]:
        return {"context": "", "sources": []}

    formatted = []
    sources = []
    seen_sources = set()
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        if dist > MAX_DISTANCE:
            continue
        formatted.append(doc)
        src = meta.get("source", "")
        if src and src not in seen_sources:
            seen_sources.add(src)
            sources.append(src)

    return {"context": "\n\n".join(formatted), "sources": sources}
