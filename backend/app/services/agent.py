"""Agent router — decides which data sources to query based on the user's question."""

from app.services.rag import retrieve_context
from app.services.github import get_github_context

GITHUB_KEYWORDS = [
    # French
    "github", "repo", "dépôt", "code source", "derniers projets",
    "commits", "contributions", "readme", "repositories",
    # English
    "repository", "source code", "latest projects", "codebase",
    "open source",
]


def is_github_query(query: str) -> bool:
    """Detect if the query is about GitHub."""
    query_lower = query.lower()
    return any(kw in query_lower for kw in GITHUB_KEYWORDS)


def resolve_query(query: str) -> dict:
    """Route the query to the appropriate data source(s).

    Returns:
        {"context": str, "sources": list[str]}
    """
    contexts = []
    sources = []

    use_github = is_github_query(query)

    # Always query RAG for profile context
    rag_result = retrieve_context(query)
    if rag_result["context"]:
        contexts.append(rag_result["context"])
        sources.extend(rag_result["sources"])

    # Add GitHub data if relevant
    if use_github:
        gh_result = get_github_context()
        if gh_result["context"]:
            contexts.append(gh_result["context"])
            sources.extend(gh_result["sources"])

    return {
        "context": "\n\n---\n\n".join(contexts),
        "sources": sources,
    }
