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


def get_matching_context(job_description: str) -> dict:
    """Retrieve Narymane's full profile and format for job matching."""

    # Retrieve broad profile context with multiple queries
    queries = [
        "compétences techniques skills programming languages",
        "expérience professionnelle experience work",
        "formation éducation education degree",
        "projets projects réalisations",
    ]

    all_context = []
    all_sources = set()
    for q in queries:
        result = retrieve_context(q)
        if result["context"]:
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
