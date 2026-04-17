"""GitHub API service — fetches real-time data from chabanenary's public repos."""

import time

import httpx

from app.config import settings

GITHUB_API = "https://api.github.com"
USERNAME = "chabanenary"

# --- Cache ---
_cache: dict[str, dict] = {}


def _get_cached(key: str):
    if key in _cache:
        entry = _cache[key]
        if time.time() - entry["time"] < settings.github_cache_ttl:
            return entry["data"]
    return None


def _set_cached(key: str, data):
    _cache[key] = {"data": data, "time": time.time()}


def _github_get(path: str) -> dict | list | None:
    """Make a GET request to GitHub API."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{GITHUB_API}{path}", headers=headers)
            if response.status_code == 200:
                return response.json()
    except httpx.HTTPError:
        pass
    return None


def get_repos() -> list[dict]:
    """Get all public repos for chabanenary."""
    cached = _get_cached("repos")
    if cached is not None:
        return cached

    data = _github_get(f"/users/{USERNAME}/repos?sort=updated&per_page=30")
    if not data:
        return []

    repos = []
    for r in data:
        if r.get("fork"):
            continue
        repos.append({
            "name": r["name"],
            "description": r.get("description") or "",
            "url": r["html_url"],
            "language": r.get("language") or "",
            "stars": r.get("stargazers_count", 0),
            "updated_at": r.get("pushed_at", r.get("updated_at", "")),
            "topics": r.get("topics", []),
        })

    _set_cached("repos", repos)
    return repos


def get_repo_readme(repo_name: str) -> str:
    """Get the README content of a specific repo."""
    cache_key = f"readme_{repo_name}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    data = _github_get(f"/repos/{USERNAME}/{repo_name}/readme")
    if not data:
        return ""

    # README is base64 encoded
    import base64
    content = base64.b64decode(data.get("content", "")).decode("utf-8", errors="replace")

    # Truncate long READMEs
    if len(content) > 2000:
        content = content[:2000] + "\n\n[... truncated]"

    _set_cached(cache_key, content)
    return content


def get_repo_languages(repo_name: str) -> dict[str, int]:
    """Get language breakdown for a repo."""
    cache_key = f"langs_{repo_name}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    data = _github_get(f"/repos/{USERNAME}/{repo_name}/languages")
    if not data:
        return {}

    _set_cached(cache_key, data)
    return data


def format_repos_context(repos: list[dict]) -> str:
    """Format repo list as context for the LLM."""
    if not repos:
        return "[GitHub] No public repositories found."

    lines = [f"[GitHub - Real-time data from github.com/{USERNAME}]\nIMPORTANT: Always include the clickable markdown links in your response.\n"]
    for i, r in enumerate(repos, 1):
        line = f"{i}. [**{r['name']}**]({r['url']})"
        if r["description"]:
            line += f" — {r['description']}"
        if r["language"]:
            line += f"\n   Language: {r['language']}"
        if r["stars"]:
            line += f"\n   Stars: {r['stars']}"
        if r["updated_at"]:
            date = r["updated_at"][:10]
            line += f"\n   Last updated: {date}"
        if r["topics"]:
            line += f"\n   Topics: {', '.join(r['topics'])}"
        lines.append(line)

    return "\n\n".join(lines)


def get_github_context() -> dict:
    """Get formatted GitHub context + source list."""
    repos = get_repos()
    context = format_repos_context(repos)
    sources = [f"github:{USERNAME}/{r['name']}" for r in repos]
    return {"context": context, "sources": sources}
