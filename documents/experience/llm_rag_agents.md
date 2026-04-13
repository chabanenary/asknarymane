# LLM, RAG & AI Agents — Current Skills & Experience

## Context
Since 2025, Narymane has been actively building hands-on experience with Large Language Models (LLMs), Retrieval Augmented Generation (RAG), and AI Agents. This is the natural next step in her AI journey: after mastering ML model training and edge deployment (YOLO on Jetson Nano and Android), she is now learning to build complete AI-powered applications and intelligent systems.

## LLM Serving — Ollama

### What She Uses
- Ollama as the local LLM serving platform on Mac (Apple Silicon M1)
- Models: Qwen2 1.5B for development/testing, Mistral 7B and Qwen2.5 7B for production-quality responses
- Ollama API (OpenAI-compatible) for programmatic integration

### What She Understands
- How LLMs work at a high level: transformer architecture, token prediction, context windows
- The difference between model families (Mistral, Llama, Qwen) and their trade-offs (size, quality, speed, language support)
- Quantization and its impact on model size and quality (Q4, Q8, FP16)
- The difference between training a model and serving/deploying one
- Local vs cloud LLM deployment: privacy, latency, cost trade-offs
- Ollama's architecture: model management, Metal acceleration on Apple Silicon, REST API

### Practical Skills
- Setting up Ollama and managing models (pull, run, serve)
- Building FastAPI applications that communicate with Ollama's API
- Implementing chat endpoints with conversation history management
- Streaming responses for real-time user experience
- Making the LLM model configurable via environment variables for easy switching between dev and production

## RAG — Retrieval Augmented Generation

### What It Is
RAG is a technique that augments a generic LLM with domain-specific knowledge by retrieving relevant documents at query time and injecting them into the prompt. This allows the LLM to answer questions about content it was never trained on — like Narymane's own professional profile.

### Technology Stack
- LangChain: framework for building RAG pipelines (document loading, text splitting, chain orchestration)
- ChromaDB: lightweight vector database for storing and querying document embeddings
- Embedding model: nomic-embed-text via Ollama — runs locally, no external API needed
- Text splitting: RecursiveCharacterTextSplitter for chunking documents into optimal-sized pieces

### What She Understands
- How embeddings work: transforming text into numerical vectors that capture semantic meaning
- How vector similarity search works: comparing query embeddings with document embeddings to find relevant content
- The RAG pipeline: ingestion (chunk → embed → store) and query (embed question → search → augment prompt → generate response)
- Chunking strategies: why chunk size and overlap matter for retrieval quality
- The importance of document quality: better source documents = better chatbot answers

### Practical Skills
- Building a complete RAG pipeline from scratch with LangChain + ChromaDB
- Writing ingestion scripts that process Markdown documents
- Creating FastAPI endpoints for document ingestion and RAG-powered chat
- Preparing domain-specific documents (structured Markdown) for optimal RAG performance
- Containerizing the full RAG stack (Ollama + ChromaDB + FastAPI) with Docker Compose

## AI Agents & MCP (Model Context Protocol)

### What MCP Is
MCP (Model Context Protocol) is a standard protocol developed by Anthropic that allows AI agents to use external tools. Instead of the LLM trying to answer everything from its training data, it can call tools (search the web, read files, query databases, call APIs) to get real-time information.

### What She Is Building
- MCP servers that expose tools to the LLM agent (weather, document search, GitHub repo reading)
- An agent layer that decides when to use tools vs when to answer directly
- Integration of MCP tool calling with the RAG pipeline — the agent can search the knowledge base as one of its tools

### What She Understands
- The agent paradigm: LLM as reasoning engine that decides which tools to use
- Tool calling / function calling: how the LLM generates structured requests for external tools
- MCP protocol: server-client architecture, tool registration, request/response flow
- The difference between RAG (passive knowledge retrieval) and agents (active tool use)

### Technology Stack
- MCP SDK for Python
- FastAPI for MCP server implementation
- Integration with Ollama and LangChain

## How This Connects to Her Background

Narymane's embedded systems background gives her a unique perspective on AI systems:

- **Resource awareness**: from years of working on constrained devices, she naturally thinks about memory usage, latency, and compute efficiency — critical when deploying LLMs
- **Systems thinking**: understanding how all components (LLM, embedding model, vector DB, API server) interact and where bottlenecks occur
- **Production mindset**: CMMI Level 3 discipline translates directly to building reliable, well-documented, testable AI systems
- **Containerization**: Docker experience from her ML serving projects transfers directly to orchestrating multi-service LLM applications
- **API design**: FastAPI experience from her YOLO serving projects is directly reused for the chatbot API

## Tools & Frameworks Summary

| Category | Tools |
|----------|-------|
| LLM Serving | Ollama, Groq API |
| Models | Mistral 7B, Qwen2.5, Qwen2 1.5B, nomic-embed-text |
| RAG Framework | LangChain, LangChain Community |
| Vector Database | ChromaDB |
| API Framework | FastAPI, Uvicorn |
| Agent Protocol | MCP (Model Context Protocol) |
| Containerization | Docker, Docker Compose |
| Development | Python, VS Code, Claude Code |
