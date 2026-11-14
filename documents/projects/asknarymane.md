# Project — AI / AskNarymane (multi-source RAG assistant in production, 2026)

## Overview
AskNarymane is a web assistant for recruiters. It answers in French or English questions about Narymane's background, skills and projects, shows her GitHub repositories in real time, makes it easy to get in touch, generates her CV as a PDF and evaluates how well her profile matches a job description. Narymane designed, built and deployed it, and operates it end to end. The project started in April 2026.

- Website: https://asknarymane.com
- Repository: https://github.com/chabanenary/asknarymane

## Backend
- Python, FastAPI, Uvicorn, pydantic-settings (configuration through environment variables), httpx
- Endpoints: /chat, /health, /config (provider and available models), /cv (CV as a PDF, French or English)
- CV PDF generation with fpdf2 from a bilingual Markdown file, DejaVu fonts for Unicode; both PDFs are pre-generated at startup
- pytest tests of the endpoints, the routing and the RAG pipeline functions, with a mocked LLM

## Frontend
- Next.js 16 (App Router), React 19, TypeScript
- Tailwind CSS 4 with the typography plugin, Markdown rendering of answers (react-markdown), clickable links
- LLM model selector
- For each answer: display of the sources, the model used, the number of tokens and the duration

## RAG Pipeline
- Knowledge base: bilingual Markdown documents (French and English) split on section headings, with metadata (source, category, title, section, language)
- ChromaDB vector database: embedded in the backend in production, containerized ChromaDB server in development
- Embeddings: all-MiniLM-L6-v2 (built into ChromaDB) in production, nomic-embed-text via Ollama in development
- Search: detection of the question's language and category, category filtering, 12 candidates retrieved then a distance threshold
- Post-processing: FR/EN deduplication, custom re-ranking (lexical overlap, known-entity bonus, distance), 5 excerpts kept, context compression
- In-memory query cache (5 minutes)

## Agent Routing
A deterministic, keyword-based router in French and English builds the context sent to the LLM from five sources:
1. **RAG**: Narymane's profile
2. **GitHub**: her public repositories in real time through the GitHub API (forks excluded, 10-minute cache), with clickable links
3. **Contact**: a mailto link that opens a pre-filled email draft, and a LinkedIn link
4. **Matching**: when a recruiter pastes a job description, extraction of technical terms, targeted RAG queries, then a structured report (compatibility score, strengths, transferable skills, gaps, recommendation) with an instruction not to inflate the score; this source takes priority and is exclusive
5. **CV PDF**: download link for the CV in the language of the question

The LLM does not call tools itself: deterministic routing is a deliberate choice for reliability and cost.

## LLM and Prompt
- Production: Groq API (OpenAI-compatible) with several open models selectable by the user (Qwen 3.8 27B by default, GPT OSS 120B, GPT OSS 20B)
- Development: Ollama running locally (Qwen2 1.5B), through its native API
- A single codebase, two modes (development / production), driven by environment variables
- Strict anti-hallucination system prompt, with an explicit fallback answer when information is missing; answers in the language of the question; never disclose or deduce her date of birth or age
- Context injected as a simulated exchange before the conversation; window of the last 6 messages; enrichment of the search query from previous turns
- Maintenance: replacement of models retired by Groq, support for the specific response format of the GPT OSS models; Groq free-tier rate limits identified and signaled to the user

## Deployment and Operations
- Docker for the backend and the frontend
- Development: Podman Compose with 4 containers (Ollama, ChromaDB, FastAPI backend, Next.js frontend)
- Production: Railway with 2 services (FastAPI backend with embedded ChromaDB, Next.js frontend in standalone mode), automatic redeployment on every push to GitHub
- Custom domain asknarymane.com (DNS at Namecheap), HTTPS
- The vector database is re-ingested at every backend startup in production, which guarantees up-to-date data after each deployment

## Known and Accepted Limitations
- Responses are returned in one piece, without progressive display
- No authentication or rate limiting on the API
- Vector database rebuilt at every startup
- Conversation not kept after a page reload

## Skills Demonstrated
- **RAG engineering**: ingestion, chunking, embeddings, vector search, re-ranking, compression, context injection
- **LLM integration**: multi-provider abstraction (Groq / Ollama), on-the-fly model switching, handling of provider constraints
- **Agent architecture**: keyword-based intent detection, source composition, structured outputs (matching report)
- **Full-stack development**: asynchronous FastAPI API, Next.js / React / TypeScript frontend
- **Operations**: environment-based configuration, continuous deployment, domain and HTTPS, tests with a mocked LLM
