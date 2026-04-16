"""RAG quality evaluation tests.

These tests verify that the retrieval pipeline returns relevant chunks
for typical recruiter questions. They require a running ChromaDB with
ingested documents — run against the live container.
"""

from unittest.mock import patch, MagicMock

import pytest

from app.services.rag import (
    detect_language,
    detect_categories,
    rerank_score,
    compress_chunk,
    deduplicate,
)


# --- Unit tests (no container needed) ---


class TestDetectLanguage:
    def test_french_question(self):
        assert detect_language("Quelle est son expérience ?") == "fr"

    def test_english_question(self):
        assert detect_language("What is her experience?") == "en"

    def test_french_projects(self):
        assert detect_language("Quels sont ses projets ?") == "fr"

    def test_english_projects(self):
        assert detect_language("What are her projects?") == "en"

    def test_french_education(self):
        assert detect_language("Où a-t-elle étudié ?") == "fr"

    def test_mixed_defaults_english(self):
        assert detect_language("Narymane?") == "en"


class TestDetectCategories:
    def test_experience_fr(self):
        cats = detect_categories("quelle est son expérience professionnelle ?")
        assert "experience" in cats

    def test_experience_en(self):
        cats = detect_categories("what is her work experience?")
        assert "experience" in cats

    def test_education(self):
        cats = detect_categories("where did she study?")
        assert "education" in cats

    def test_projects(self):
        cats = detect_categories("quels sont ses projets ?")
        assert "projects" in cats

    def test_skills(self):
        cats = detect_categories("what are her skills?")
        assert "cv" in cats

    def test_no_category(self):
        cats = detect_categories("who is narymane?")
        assert cats == []

    def test_multiple_categories(self):
        cats = detect_categories("her experience and education")
        assert "experience" in cats
        assert "education" in cats


class TestRerankScore:
    def test_high_overlap(self):
        score = rerank_score(
            "experience embedded linux",
            "She has 13 years of experience in embedded Linux systems",
        )
        assert score > 0.5

    def test_no_overlap(self):
        score = rerank_score("cooking recipes", "Some random text about weather")
        assert score == 0.0

    def test_partial_overlap(self):
        score = rerank_score(
            "projects machine learning",
            "GalleryKeeper is a machine learning Android app",
        )
        assert 0.0 < score < 1.0


class TestCompressChunk:
    def test_keeps_headers(self):
        chunk = "## Experience\nLine 1\nLine 2\nLine 3"
        result = compress_chunk("experience", chunk)
        assert "## Experience" in result

    def test_keeps_relevant_lines(self):
        chunk = "## Profile\n- Expert in Python\n- Likes hiking\n- Knows Docker"
        result = compress_chunk("Python Docker", chunk)
        assert "Python" in result
        assert "Docker" in result

    def test_limits_lines(self):
        lines = "\n".join([f"Line {i} about topic" for i in range(20)])
        result = compress_chunk("topic", lines, max_lines=5)
        assert len(result.split("\n")) <= 5


class TestDeduplicate:
    def test_keeps_preferred_language(self):
        docs = [
            {"text": "English version", "meta": {"source": "cv/profile.md", "section": "Info", "lang": "en"}, "dist": 0.5},
            {"text": "Version française", "meta": {"source": "cv/profile.md", "section": "Info", "lang": "fr"}, "dist": 0.6},
        ]
        result = deduplicate(docs, preferred_lang="fr")
        assert len(result) == 1
        assert result[0]["meta"]["lang"] == "fr"

    def test_keeps_only_available(self):
        docs = [
            {"text": "Only English", "meta": {"source": "blog/post.md", "section": "Intro", "lang": "en"}, "dist": 0.5},
        ]
        result = deduplicate(docs, preferred_lang="fr")
        assert len(result) == 1

    def test_different_sections_kept(self):
        docs = [
            {"text": "Section A", "meta": {"source": "cv/profile.md", "section": "Skills", "lang": "fr"}, "dist": 0.5},
            {"text": "Section B", "meta": {"source": "cv/profile.md", "section": "Contact", "lang": "fr"}, "dist": 0.6},
        ]
        result = deduplicate(docs, preferred_lang="fr")
        assert len(result) == 2
