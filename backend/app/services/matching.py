"""Job matching service — compares Narymane's profile against a job description."""

import re

from app.services.rag import retrieve_context

# Keywords that suggest the user is pasting a job description
JOB_KEYWORDS = [
    # French
    "fiche de poste", "offre d'emploi", "profil recherché", "missions",
    "compétences requises", "expérience souhaitée", "correspond", "poste",
    "candidature", "recrutement", "cdi", "cdd", "freelance",
    "responsabilités", "qualifications", "rémunération", "salaire",
    "télétravail", "remote", "hybride",
    # English
    "job description", "job offer", "requirements", "qualifications",
    "responsibilities", "we are looking for", "you will", "must have",
    "nice to have", "experience required", "match", "fit", "position",
    "role", "hiring", "full-time", "part-time", "contract",
]

# Minimum length to consider a message as a job description
MIN_JOB_DESC_LENGTH = 150

# Non-technical acronyms to ignore during keyword extraction
_NOISE_TERMS = {
    "cdi", "cdd", "rtt", "mba", "pdf", "ceo", "cto", "bac", "get", "post",
    "type", "lieu", "requis", "par", "des", "les",
}


def is_job_matching_query(query: str) -> bool:
    """Detect if the query contains a job description for matching."""
    query_lower = query.lower()
    keyword_count = sum(1 for kw in JOB_KEYWORDS if kw in query_lower)
    # Either multiple job keywords or long text with at least one keyword
    if keyword_count >= 3:
        return True
    if len(query) >= MIN_JOB_DESC_LENGTH and keyword_count >= 1:
        return True
    return False


def extract_job_terms(job_description: str) -> list[str]:
    """Extract technical keywords from a job description."""
    terms: set[str] = set()

    # Acronyms and uppercase terms (2+ chars): CUDA, GNSS, CNN, TCP/IP
    for m in re.finditer(r"\b[A-Z][A-Z0-9/+#.]{1,}\b", job_description):
        terms.add(m.group())

    # CamelCase / branded terms: TensorRT, DeepStream, OpenCV, DeepSORT
    for m in re.finditer(r"\b[A-Z][a-z]+(?:[A-Z][a-z]*)+\b", job_description):
        terms.add(m.group())

    # Known tech terms that may appear lowercase
    tech_re = (
        r"\b(?:python|linux|docker|git|bash|pytorch|tensorflow|opencv|"
        r"yolo\w*|onnx|ros2?|deepstream|tensorrt|cuda|lidar|radar)\b"
    )
    for m in re.finditer(tech_re, job_description, re.IGNORECASE):
        terms.add(m.group())

    # Filter noise
    terms = {t for t in terms if t.lower() not in _NOISE_TERMS and len(t) >= 2}
    return list(terms)


def build_job_queries(job_description: str) -> list[str]:
    """Build targeted RAG queries from job description keywords."""
    terms = extract_job_terms(job_description)
    if not terms:
        return []

    # Group terms into queries of ~5 terms each
    queries = []
    batch: list[str] = []
    for term in terms:
        batch.append(term)
        if len(batch) >= 5:
            queries.append(" ".join(batch))
            batch = []
    if batch:
        queries.append(" ".join(batch))

    return queries[:4]


def get_matching_context(job_description: str) -> dict:
    """Retrieve Narymane's full profile and format for job matching."""

    # Generic profile queries
    profile_queries = [
        "compétences techniques skills programming languages",
        "expérience professionnelle experience work",
        "formation éducation education degree",
        "projets projects réalisations",
    ]

    # Targeted queries extracted from the job description
    job_queries = build_job_queries(job_description)

    all_context = []
    all_sources = set()
    seen_chunks: set[str] = set()

    for q in profile_queries + job_queries:
        result = retrieve_context(q)
        if result["context"] and result["context"] not in seen_chunks:
            seen_chunks.add(result["context"])
            all_context.append(result["context"])
            all_sources.update(result["sources"])

    profile_context = "\n\n".join(all_context)

    context = f"""[Job Matching — Profile vs Job Description Analysis]

INSTRUCTIONS FOR THE LLM:
You must analyze the job description provided by the recruiter and compare it against Narymane's profile below.
Generate a structured matching report with:
1. **Score de compatibilité** — a percentage (e.g., 75%) based on how well the profile matches
2. **Points forts** — skills and experience that directly match the requirements
3. **Compétences transférables** — skills that are not exact matches but relevant
4. **Écarts identifiés** — requirements not covered by the profile
5. **Recommandation** — a brief conclusion for the recruiter

Be honest and factual. Do not inflate the match.

---

NARYMANE'S PROFILE:
{profile_context}

---

JOB DESCRIPTION TO ANALYZE:
{job_description}"""

    return {
        "context": context,
        "sources": list(all_sources),
    }
