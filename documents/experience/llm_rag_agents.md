# LLMs, RAG and Agent Routing — Applied AI Skills

## Context
Since 2026, Narymane has been building and operating LLM-based systems in real-world conditions. It is the logical continuation of her AI journey: after training and deploying vision models (YOLO on Android, Jetson Nano and Kubernetes), she designed AskNarymane, a multi-source RAG assistant in production, then, on a freelance mission, the real-time orchestration between embedded perception and a cloud LLM.

## LLM API Integration
- Groq API (OpenAI-compatible) in production, with several open models selectable by the user
- Ollama for local inference in development (native API)
- Streaming cloud LLM, sentence by sentence, with context caching (embedded AI mission)
- Handling provider constraints: free-tier rate limits, models retired by the provider, model-specific response formats
- Configuration through environment variables to switch between development and production

## What She Masters About LLMs
- How LLMs work: transformer architecture, token prediction, context window
- Trade-offs between model families and sizes: quality, speed, memory, language support
- Quantization and its impact on model size and quality (4-bit, GGUF, Q8, FP16), put into practice with llama.cpp
- The difference between training a model and serving or deploying it
- Local, on-device or cloud deployment: privacy, latency and cost trade-offs

## RAG — Retrieval-Augmented Generation
RAG augments a general-purpose LLM with domain-specific knowledge: relevant documents are retrieved at question time and injected into the prompt. Narymane designed and put into production the RAG pipeline of AskNarymane:
- Bilingual Markdown knowledge base split on section headings, with metadata (source, category, section, language)
- ChromaDB vector database; all-MiniLM-L6-v2 embeddings in production, nomic-embed-text in development
- Detection of the question's language and category, category filtering, distance threshold
- FR/EN deduplication, custom re-ranking (lexical overlap, known-entity bonus, distance), context compression, query caching

## Agent Routing
- In AskNarymane, a deterministic keyword-based router (FR/EN) builds the context from five sources: RAG, real-time GitHub repositories, contact, job description matching, CV PDF generation
- The LLM does not call tools itself: deterministic routing is a deliberate choice for reliability and cost
- On her embedded AI mission, the Python asyncio orchestrator routes perception to the device and reasoning to the cloud LLM

## Prompt Design
- Strict anti-hallucination system prompt, with an explicit fallback answer when information is missing
- Answers in the language of the question (French or English)
- Conversation window and enrichment of the search query from previous turns
- Structured matching prompt (score, strengths, transferable skills, gaps, recommendation) with an instruction not to inflate the score

## Evaluation and Observability of AI Systems
- Benchmarks with a defined protocol to compare models (embedded AI mission)
- Automated tests with a mocked LLM (pytest)
- Tracking of tokens, latency and errors; display of the model, sources, tokens and duration of each answer in AskNarymane
- Embedded monitoring (memory, GPU, temperatures, latencies) and endurance tests

## How It Connects to Her Background
Narymane's embedded systems background gives her a particular perspective on AI systems:
- **Resource awareness**: years on constrained devices make her reason in terms of memory, latency and compute efficiency — critical for deploying LLMs and vision models
- **Systems view**: understanding how the components (LLM, embeddings, vector database, API, device) interact and where the bottlenecks are
- **Production mindset**: CMMI Level 3 discipline translates directly into reliable, documented and tested AI systems
- **Containerization and APIs**: the FastAPI and Docker experience from her serving projects is reused in her LLM applications

## Tools Summary
| Category | Tools |
|-----------|--------|
| LLM APIs | Groq (OpenAI-compatible), Ollama, streaming cloud LLM |
| Local inference | llama.cpp, ONNX Runtime, 4-bit quantization / GGUF |
| Vector database | ChromaDB |
| Embeddings | all-MiniLM-L6-v2, nomic-embed-text |
| API and backend | FastAPI, Uvicorn, pydantic-settings, httpx |
| Testing | pytest with a mocked LLM |
| Containerization | Docker, Podman Compose |
