# Project — AI / AskNarymane (in progress)

## Overview
AskNarymane is a RAG-powered (Retrieval Augmented Generation) chatbot that answers questions about Narymane's professional profile, projects, and experience. It is designed as a portfolio showcase and a demonstration of LLM deployment and RAG implementation skills.

GitHub: https://github.com/chabanenary/asknarymane
Website (planned): https://asknarymane.dev

## Architecture
- LLM: Ollama serving Mistral 7B (or Qwen2.5 7B) for response generation
- Embedding model: nomic-embed-text via Ollama for document vectorization
- Vector database: ChromaDB for storing and retrieving document embeddings
- API: FastAPI with endpoints for chat, RAG-powered chat, and document ingestion
- Frontend: Streamlit or simple HTML/JS chat interface
- Containerization: Docker Compose orchestrating Ollama, ChromaDB, and the FastAPI app

## Knowledge Base
The chatbot is trained on Narymane's own documents:
- CV and professional profile
- Detailed experience at Ekinops/OneAccess (2007–2020)
- Project descriptions: GalleryKeeper, Edge AI on Jetson Nano, ML Serving APIs
- Education: Polytechnique d'Alger, Télécom Paris
- Technical skills and competencies
- Blog posts and community contributions

## What This Project Demonstrates
- LLM serving (Ollama + open source models)
- RAG implementation (LangChain + ChromaDB + embeddings)
- API development (FastAPI)
- Containerization (Docker Compose, multi-service orchestration)
- Full-stack AI application development
- MLOps practices: model management, deployment, monitoring

## Deployment Strategy
- Development: Ollama locally on Mac (Apple Silicon M1), qwen2:1.5b for fast iteration
- Production: Groq API (free, fast) for the online version at asknarymane.dev
- Hosting: Render.com or Railway.app (free tier)
