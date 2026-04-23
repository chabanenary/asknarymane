"""Tests for GitHub service, contact service, and agent router."""

from unittest.mock import patch, MagicMock

import pytest

from app.services.github import format_repos_context
from app.services.contact import get_contact_context
from app.services.matching import is_job_matching_query
from app.services.agent import is_github_query, is_contact_query, resolve_query


# --- Intent detection ---


class TestIsGithubQuery:
    def test_github_fr(self):
        assert is_github_query("montre-moi ses repos GitHub") is True

    def test_github_en(self):
        assert is_github_query("show me her GitHub repositories") is True

    def test_code_source(self):
        assert is_github_query("où est son code source ?") is True

    def test_latest_projects(self):
        assert is_github_query("quels sont ses derniers projets ?") is True

    def test_readme(self):
        assert is_github_query("show me the readme of asknarymane") is True

    def test_not_github(self):
        assert is_github_query("quelle est son expérience ?") is False

    def test_not_github_education(self):
        assert is_github_query("where did she study?") is False

    def test_open_source(self):
        assert is_github_query("does she contribute to open source?") is True


# --- Format repos ---


class TestFormatReposContext:
    def test_empty_repos(self):
        result = format_repos_context([])
        assert "No public repositories" in result

    def test_format_single_repo(self):
        repos = [{
            "name": "asknarymane",
            "description": "RAG chatbot",
            "url": "https://github.com/chabanenary/asknarymane",
            "language": "Python",
            "stars": 3,
            "updated_at": "2026-04-17T10:00:00Z",
            "topics": ["rag", "chatbot"],
        }]
        result = format_repos_context(repos)
        assert "asknarymane" in result
        assert "RAG chatbot" in result
        assert "Python" in result
        assert "2026-04-17" in result
        assert "rag" in result

    def test_format_multiple_repos(self):
        repos = [
            {"name": "repo1", "description": "", "url": "https://github.com/chabanenary/repo1", "language": "Python", "stars": 0, "updated_at": "", "topics": []},
            {"name": "repo2", "description": "Test", "url": "https://github.com/chabanenary/repo2", "language": "Java", "stars": 1, "updated_at": "2026-01-01T00:00:00Z", "topics": []},
        ]
        result = format_repos_context(repos)
        assert "1." in result
        assert "2." in result


# --- Agent resolve ---


class TestResolveQuery:
    @patch("app.services.agent.get_github_context")
    @patch("app.services.agent.retrieve_context")
    def test_rag_only(self, mock_rag, mock_gh):
        mock_rag.return_value = {"context": "RAG context", "sources": ["cv/profile.md"]}
        result = resolve_query("quelle est son expérience ?")
        assert "RAG context" in result["context"]
        assert "cv/profile.md" in result["sources"]
        mock_gh.assert_not_called()

    @patch("app.services.agent.get_github_context")
    @patch("app.services.agent.retrieve_context")
    def test_github_and_rag(self, mock_rag, mock_gh):
        mock_rag.return_value = {"context": "RAG context", "sources": ["projects/asknarymane.md"]}
        mock_gh.return_value = {"context": "GitHub repos list", "sources": ["github:chabanenary/asknarymane"]}
        result = resolve_query("montre-moi ses repos GitHub")
        assert "RAG context" in result["context"]
        assert "GitHub repos list" in result["context"]
        assert "github:chabanenary/asknarymane" in result["sources"]
        mock_gh.assert_called_once()

    @patch("app.services.agent.get_github_context")
    @patch("app.services.agent.retrieve_context")
    def test_empty_results(self, mock_rag, mock_gh):
        mock_rag.return_value = {"context": "", "sources": []}
        result = resolve_query("something random")
        assert result["context"] == ""
        assert result["sources"] == []

    @patch("app.services.agent.get_contact_context")
    @patch("app.services.agent.retrieve_context")
    def test_contact_query(self, mock_rag, mock_contact):
        mock_contact.return_value = {"context": "Contact info", "sources": ["contact:email"]}
        result = resolve_query("comment contacter narymane ?")
        assert "Contact info" in result["context"]
        assert "contact:email" in result["sources"]
        mock_rag.assert_not_called()


# --- Contact detection ---


class TestIsContactQuery:
    def test_contact_fr(self):
        assert is_contact_query("comment contacter narymane ?") is True

    def test_contact_en(self):
        assert is_contact_query("how can I reach narymane?") is True

    def test_email_fr(self):
        assert is_contact_query("je voudrais lui envoyer un email") is True

    def test_hire(self):
        assert is_contact_query("I want to hire her") is True

    def test_linkedin(self):
        assert is_contact_query("quel est son linkedin ?") is True

    def test_not_contact(self):
        assert is_contact_query("quelle est son expérience ?") is False


# --- Contact context ---


class TestContactContext:
    def test_has_email(self):
        result = get_contact_context()
        assert "chabanenarymane@gmail.com" in result["context"]

    def test_has_linkedin(self):
        result = get_contact_context()
        assert "linkedin" in result["context"].lower()

    def test_has_mailto(self):
        result = get_contact_context()
        assert "mailto:" in result["context"]

    def test_sources(self):
        result = get_contact_context()
        assert "contact:email" in result["sources"]
        assert "contact:linkedin" in result["sources"]


# --- Job matching detection ---


class TestIsJobMatchingQuery:
    def test_short_question_not_matching(self):
        assert is_job_matching_query("est-ce qu'elle correspond ?") is False

    def test_job_description_fr(self):
        jd = """Nous recherchons un ingénieur systèmes embarqués Linux pour un poste en CDI.
        Missions : développement de drivers, intégration BSP, gestion de projet.
        Compétences requises : C, Linux, Yocto, Git.
        Expérience souhaitée : 5 ans minimum. Télétravail possible."""
        assert is_job_matching_query(jd) is True

    def test_job_description_en(self):
        jd = """We are looking for a Senior Embedded Linux Engineer. Full-time position.
        Requirements: 5+ years experience, C programming, Linux kernel, device drivers.
        Nice to have: Python, Docker, CI/CD.
        Responsibilities: BSP development, board bring-up, code review."""
        assert is_job_matching_query(jd) is True

    def test_normal_question(self):
        assert is_job_matching_query("quelle est son expérience en embarqué ?") is False

    def test_few_keywords_short(self):
        assert is_job_matching_query("poste CDI") is False


# --- Job matching in agent ---


class TestResolveJobMatching:
    @patch("app.services.matching.retrieve_context")
    def test_matching_returns_structured_context(self, mock_rag):
        mock_rag.return_value = {"context": "Narymane has 13 years experience", "sources": ["experience/ekinops_oneaccess.md"]}
        jd = """Nous recherchons un ingénieur Linux embarqué en CDI.
        Compétences requises : C, Linux, Yocto, drivers.
        Missions : développement firmware, intégration BSP.
        Expérience souhaitée : 5 ans. Télétravail hybride."""
        result = resolve_query(jd)
        assert "Job Matching" in result["context"]
        assert "JOB DESCRIPTION TO ANALYZE" in result["context"]
        assert "NARYMANE'S PROFILE" in result["context"]
