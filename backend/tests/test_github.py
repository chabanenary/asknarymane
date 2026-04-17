"""Tests for GitHub service and agent router."""

from unittest.mock import patch, MagicMock

import pytest

from app.services.github import format_repos_context
from app.services.agent import is_github_query, resolve_query


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
