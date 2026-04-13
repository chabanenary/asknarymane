# ============================================
# Makefile - asknarymane
# ============================================

.PHONY: dev down build test pull-model check-no-claude-auth git-push git-login git-config

# --- Dev ---
dev:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

pull-model:
	docker compose exec ollama ollama pull qwen2:1.5b

ingest:
	docker compose exec backend python -m app.scripts.ingest

test:
	cd backend && uv run pytest
	cd frontend && npm test
