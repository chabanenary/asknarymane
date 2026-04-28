# Project — AI / AskNarymane

## Overview
AskNarymane is a RAG-powered chatbot that answers recruiters' questions about Narymane's professional profile, projects, and experience. It features an intelligent agent system that combines static profile data, real-time GitHub information, contact facilitation, and job matching analysis. It is designed as a portfolio showcase and a demonstration of advanced AI/ML engineering skills.

GitHub: https://github.com/chabanenary/asknarymane
Website (planned): https://asknarymane.dev

## Architecture
- **LLM Provider**: Dual-provider system — Groq API (Llama 3.3 70B) for production, Ollama (qwen2:1.5b) for local development. Switchable via environment variable.
- **Embedding model**: nomic-embed-text via Ollama for document vectorization
- **Vector database**: ChromaDB for storing and retrieving document embeddings
- **Backend**: Python FastAPI with async endpoints for chat, config, and health check
- **Frontend**: Next.js / React / Tailwind CSS — interactive chat interface with model selector, markdown rendering, clickable links, and metadata display (sources, tokens, duration)
- **Containerization**: Docker Compose (Podman compatible) orchestrating 4 services: Ollama, ChromaDB, FastAPI backend, Next.js frontend

## Intelligent Agent System
The backend uses an agent router that detects the user's intent and routes to the appropriate data sources:

### Agent 1 — RAG (Profile)
- Bilingual document ingestion (English + French markdown files)
- Chunking by markdown H2 sections with context prefixing
- Language detection (FR/EN) with deduplication of cross-language results
- Category-based filtering (experience, education, projects, cv, blog)
- Re-ranking by keyword overlap + known entity boosting
- Context compression to reduce noise
- In-memory caching (TTL 5 min)

### Agent 2 — GitHub (Real-time)
- Queries GitHub API for public repositories of chabanenary
- Returns repo names, descriptions, languages, last update dates, stars
- Clickable markdown links in responses
- In-memory caching (TTL 10 min) to respect GitHub rate limits

### Agent 3 — Contact
- Generates a pre-filled mailto link (subject + body) for recruiters to contact Narymane
- Provides LinkedIn profile link
- One click opens the recruiter's email client with a draft ready to send

### Agent 4 — Job Matching
- Detects when a recruiter pastes a job description (keyword analysis + text length heuristics)
- Retrieves Narymane's full profile across all RAG categories
- Instructs the LLM to generate a structured matching report:
  - Compatibility score (percentage)
  - Matching strengths
  - Transferable skills
  - Identified gaps
  - Recommendation

## AI/ML Skills Demonstrated
This project showcases the following AI/ML competencies:

- **LLM Serving & Integration**: Multi-provider LLM abstraction (Ollama local + Groq cloud), model switching at runtime, OpenAI-compatible API consumption
- **RAG Pipeline Engineering**: End-to-end retrieval-augmented generation — document ingestion, chunking strategies, embedding generation, vector storage, semantic search, context injection, prompt engineering
- **Embedding Models**: Deploying and using nomic-embed-text via Ollama for document vectorization, custom EmbeddingFunction implementation for ChromaDB
- **Prompt Engineering**: System prompt design for instruction-following, fake-exchange pattern for context injection with small models, language-aware prompting
- **Agent Architecture**: Intent detection, multi-source routing, context combination, structured output generation (job matching reports)
- **AI Application Development**: Full-stack AI app (Python backend + React frontend), async API design, real-time data integration (GitHub API), containerized deployment
- **MLOps Practices**: Environment-based configuration, model selection via UI, token/duration tracking, test-driven development with mocked LLM calls

## Knowledge Base
The chatbot's knowledge base consists of Narymane's own documents in both English and French:
- CV and professional profile
- 13+ years experience at Ekinops/OneAccess (2007–2020): embedded systems, VxWorks RTOS, Linux, Yocto, Virtual CPE
- Previous roles: Eolices (2007–2011), STMicroelectronics (2006–2007)
- AI/ML projects: GalleryKeeper (Android + YOLO), YoloGK Serving API (multi-platform ML deployment), AskNarymane (RAG chatbot)
- Education: Polytechnique d'Alger, Télécom Paris
- Technical skills and competencies
- Blog posts and community contributions

## Production Deployment
This project is deployed in production at asknarymane.net, demonstrating Narymane's ability to design, develop, and deploy a complete AI application with intelligent agents in real-world conditions. The full pipeline — from document ingestion to LLM serving to agent routing — runs in production.

Narymane designed a dual-mode architecture that allows the same codebase to run in two environments:
- **Development**: Docker Compose (Podman) with 4 containers — Ollama (embeddings + LLM), ChromaDB server, FastAPI backend, Next.js frontend
- **Production**: Render.com with 2 services — FastAPI backend (ChromaDB embedded + Groq API), Next.js static site (CDN)

Key deployment skills demonstrated:
- **Cloud deployment**: Render.com Web Service + Static Site configuration
- **Infrastructure as Code**: `render.yaml` blueprint for declarative deployment
- **Environment-driven configuration**: Same code, different behavior via environment variables (LLM_PROVIDER, EMBEDDING_PROVIDER, CHROMA_MODE)
- **Auto-ingestion**: Backend automatically ingests documents at startup if the vector database is empty
- **Dual embedding strategy**: Ollama (nomic-embed-text) for dev, ChromaDB built-in (all-MiniLM-L6-v2) for prod — no external dependency in production
- **Static site export**: Next.js configured for both standalone (Docker) and static export (CDN) modes
- **CORS management**: Dynamic origin configuration for dev and prod environments
