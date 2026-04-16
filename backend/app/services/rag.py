import hashlib
import re
import time

import chromadb

from app.config import settings
from app.services.embeddings import OllamaEmbeddingFunction

COLLECTION_NAME = "narymane_profile"
MAX_DISTANCE = 1.2
FETCH_COUNT = 12  # Fetch more, then re-rank and keep best
RETURN_COUNT = 5  # Final number of chunks to send to LLM

# --- Cache ---
_cache: dict[str, dict] = {}
CACHE_TTL = 300  # 5 minutes


# --- Language detection ---

FR_MARKERS = [
    "quel", "quelle", "quels", "quelles", "comment", "pourquoi", "est-ce",
    "où", "qui est", "qu'est", "sur quoi", "dans quel", "son ", "sa ", "ses ",
    "elle ", "travaillé", "étudié", "projets", "expérience", "formation",
    "compétence", "parcours", "diplôme",
]


def detect_language(text: str) -> str:
    """Detect if query is French or English."""
    text_lower = text.lower()
    fr_score = sum(1 for m in FR_MARKERS if m in text_lower)
    return "fr" if fr_score >= 2 else "en"


# --- Category detection ---

CATEGORY_KEYWORDS = {
    "experience": [
        "expérience", "experience", "travail", "poste", "emploi", "entreprise",
        "ekinops", "oneaccess", "vxworks", "embarqué", "embedded", "career",
        "job", "work", "worked", "company", "companies",
    ],
    "education": [
        "études", "formation", "diplôme", "école", "université", "master",
        "bac", "polytechnique", "telecom", "education", "degree", "school",
        "studied", "study",
    ],
    "projects": [
        "projet", "project", "gallerykeeper", "yologk", "asknarymane",
        "application", "app", "github",
    ],
    "cv": [
        "compétence", "skill", "profil", "cv", "résumé", "contact",
        "langue", "language", "aspiration",
    ],
    "blog": [
        "blog", "article", "publication", "open source", "communauté",
        "community",
    ],
}


def detect_categories(query: str) -> list[str]:
    """Detect relevant categories from the query."""
    query_lower = query.lower()
    matched = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            matched.append(category)
    return matched


# --- Re-ranking ---

# Known entities that should boost ranking when present
KNOWN_ENTITIES = [
    "ekinops", "oneaccess", "eolices", "stmicroelectronics",
    "polytechnique", "telecom paris", "gallerykeeper", "yologk",
]


def rerank_score(query: str, doc: str) -> float:
    """Score a document by keyword overlap + entity presence."""
    query_words = set(re.findall(r"\w{3,}", query.lower()))
    doc_lower = doc.lower()
    doc_words = set(re.findall(r"\w{3,}", doc_lower))
    if not query_words:
        return 0.0
    overlap = query_words & doc_words
    base_score = len(overlap) / len(query_words)

    # Bonus for documents containing known entities (names, companies, schools)
    entity_bonus = sum(0.15 for e in KNOWN_ENTITIES if e in doc_lower)

    return base_score + entity_bonus


# --- Context compression ---

def compress_chunk(query: str, chunk: str, max_lines: int = 15) -> str:
    """Lightly compress a chunk, keeping structure and key content."""
    lines = [l.strip() for l in chunk.split("\n") if l.strip()]

    # If chunk is already short enough, return as-is
    if len(lines) <= max_lines:
        return "\n".join(lines)

    query_words = set(re.findall(r"\w{3,}", query.lower()))

    # Score each line but keep all structural elements
    scored = []
    for line in lines:
        line_words = set(re.findall(r"\w{3,}", line.lower()))
        overlap = len(query_words & line_words)
        is_structural = line.startswith("#") or line.startswith("[") or line.startswith("-") or line.startswith("*")
        # Structural lines (headers, bullets) always kept
        score = overlap + (100 if is_structural else 0)
        scored.append((score, line))

    scored.sort(key=lambda x: x[0], reverse=True)
    kept = [l for _, l in scored[:max_lines]]

    return "\n".join(kept)


# --- Deduplication ---

def deduplicate(docs: list[dict], preferred_lang: str) -> list[dict]:
    """Remove duplicate FR/EN chunks, keeping the preferred language version."""
    seen = {}  # key: (source, section) -> doc
    for doc in docs:
        source = doc["meta"].get("source", "")
        section = doc["meta"].get("section", "")
        lang = doc["meta"].get("lang", "en")
        key = (source, section)

        if key not in seen:
            seen[key] = doc
        else:
            # Keep the version in the preferred language
            existing_lang = seen[key]["meta"].get("lang", "en")
            if existing_lang != preferred_lang and lang == preferred_lang:
                seen[key] = doc

    return list(seen.values())


# --- Collection ---

def get_collection():
    client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=OllamaEmbeddingFunction(),
    )


# --- Main retrieve ---

def retrieve_context(query: str) -> dict:
    """Full RAG retrieval pipeline with dedup, re-ranking, and compression."""

    # 1. Check cache
    cache_key = hashlib.md5(query.lower().strip().encode()).hexdigest()
    if cache_key in _cache:
        entry = _cache[cache_key]
        if time.time() - entry["time"] < CACHE_TTL:
            return entry["result"]

    # 2. Detect language
    lang = detect_language(query)

    # 3. Detect categories
    categories = detect_categories(query)

    # 4. Search ChromaDB (fetch more than needed)
    collection = get_collection()

    where_filter = None
    if categories:
        if len(categories) == 1:
            where_filter = {"category": categories[0]}
        else:
            where_filter = {"category": {"$in": categories}}

    results = collection.query(
        query_texts=[query],
        n_results=FETCH_COUNT,
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    # Fallback without category filter
    if not results["documents"] or not results["documents"][0]:
        if where_filter:
            results = collection.query(
                query_texts=[query],
                n_results=FETCH_COUNT,
                include=["documents", "metadatas", "distances"],
            )

    if not results["documents"] or not results["documents"][0]:
        result = {"context": "", "sources": []}
        _cache[cache_key] = {"result": result, "time": time.time()}
        return result

    # 5. Filter by distance
    candidates = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        if dist > MAX_DISTANCE:
            continue
        candidates.append({"text": doc, "meta": meta, "dist": dist})

    # 6. Deduplicate FR/EN
    candidates = deduplicate(candidates, preferred_lang=lang)

    # 7. Re-rank by keyword overlap + distance
    for c in candidates:
        keyword_score = rerank_score(query, c["text"])
        # Combined score: lower distance is better, higher keyword overlap is better
        c["final_score"] = keyword_score - (c["dist"] * 0.5)

    candidates.sort(key=lambda x: x["final_score"], reverse=True)

    # 8. Keep top N
    top = candidates[:RETURN_COUNT]

    # 9. Compress each chunk
    compressed = []
    sources = []
    seen_sources = set()
    for c in top:
        compressed_text = compress_chunk(query, c["text"])
        compressed.append(compressed_text)
        src = c["meta"].get("source", "")
        if src and src not in seen_sources:
            seen_sources.add(src)
            sources.append(src)

    result = {"context": "\n\n".join(compressed), "sources": sources}

    # 10. Cache result
    _cache[cache_key] = {"result": result, "time": time.time()}

    return result
