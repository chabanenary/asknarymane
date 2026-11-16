# Project — AI / AskNarymane (multi-agent RAG assistant in production, 2026)

## Overview
AskNarymane is a web assistant for recruiters. It answers in French or English questions about Narymane's background, skills and projects, shows her GitHub repositories in real time, makes it easy to get in touch, generates her CV as a PDF and evaluates how well her profile matches a job description. Narymane designed, built and deployed it, and operates it end to end. The project started in April 2026.

- Website: https://asknarymane.com
- Repository: https://github.com/chabanenary/asknarymane

## How It Works in Brief: the Path of a Question
In one sentence: AskNarymane relies on 5 specialized agents (RAG, GitHub, contact, matching, CV), orchestrated by a deterministic keyword-based router; the LLM is called only once, at the end, to write the answer.
1. The recruiter asks a question on the website (Next.js), which sends the conversation to the server (FastAPI)
2. The router reads the question and chooses which of five agents to call on: RAG (profile), GitHub, contact, job description matching, CV PDF
3. Each agent called on produces information; it is all gathered into a single "context"
4. The server makes a single call to the LLM with the rules, the context and the end of the conversation
5. The answer goes back to the website with the sources used, the model, the number of tokens and the duration

## The Router: the Conductor
- Role: decide which agents to call on for each question
- How it works: it looks for keywords in the question, in French and English ("github", "contact", "cv", "job description"…). No AI makes this decision: it is a list of rules, so it is fast, free and predictable
- It recognizes keywords at the start of a word: "projet" matches "projets", but "écrire" does not match "décrire"; 2-letter keywords ("ia", "ai", "cv") must be whole words
- Just before it, the server enriches the question: if it contains a word that refers back to the conversation ("ça", "cela", "this", "that"…) and there have already been exchanges, it adds the 2 previous messages
- The matching agent takes priority: when it triggers, it works alone
- The RAG agent is called on for every question, except a pure contact request
- Model call: none. The LLM does not call tools itself: deterministic routing is a deliberate choice for reliability and cost

## Agent 1 — RAG: Narymane's Profile
- Role: find the passages of the profile that answer the question
- Step 1: detection of the question's language (French or English) and topic (experience, education, projects, CV, blog)
- Step 2: the question is turned into a vector by the embedding model
- Step 3: search for the 12 closest passages in ChromaDB, filtered by topic; if nothing close enough is found in those topics, a new search without the filter
- Step 4: passages that are too distant are discarded; when a passage exists in both French and English, only the language of the question is kept
- Step 5: re-ranking by words shared with the question, presence of known names (companies, schools, projects) and distance; the best 5 are kept and the longest are shortened
- The result is kept in memory for 5 minutes for identical questions
- Model call: yes, to the embedding model, not the LLM — all-MiniLM-L6-v2, built into ChromaDB, in production; nomic-embed-text via Ollama in development

## Agent 2 — GitHub: Projects in Real Time
- Role: list Narymane's public repositories (github.com/chabanenary)
- How it works: query to the GitHub API, forks excluded, formatting of the name, description, language, last update date and a clickable link
- The result is kept in memory for 10 minutes
- Model call: none

## Agent 3 — Contact
- Role: help the recruiter write to Narymane
- How it works: a ready-made text with an email link that opens a pre-filled draft (subject and message), plus the link to her LinkedIn profile
- Model call: none

## Agent 4 — Job Description Matching
- Role: assess whether Narymane's profile fits a position
- Detection: the recruiter pasted a job description (at least 3 typical words such as "missions" or "requirements", or a long text containing at least one of them)
- How it works: extraction of the technical terms of the offer, in order of appearance (Python, C++, CUDA, GStreamer, MLOps, Kubernetes…), then up to 8 searches in the profile: first up to 4 targeted at those terms, then 4 general ones
- Searches run only in the language of the offer; duplicate passages are dropped and the profile sent is capped at about 3,000 tokens, to stay under the Groq limit (8,000 tokens per minute)
- It prepares an instruction for a 5-point report: compatibility score, strengths, transferable skills, gaps, recommendation, with the instruction not to inflate the score
- Model call: to the embedding model for each search; the LLM writes the report during the final call

## Agent 5 — CV PDF
- Role: provide Narymane's CV as a PDF
- How it works: when the CV is requested, a download link in the language of the question is added to the context, with the instruction to include it in the answer
- Both PDFs (French and English) are built with fpdf2 from the CV Markdown files as soon as the server starts
- Model call: none

## The Final LLM Call: the Only One per Question
The server assembles a message that contains:
- the rules: use only the information provided, invent nothing, answer "Cette information n'est pas disponible dans mon contexte" (this information is not available in my context) when it is missing, answer in the language of the question, never give or guess her date of birth or age
- the context gathered by the agents, presented as an exchange that already took place before the conversation
- the last 6 messages of the conversation

Then it makes a single call to the LLM:
- in production: Groq API (OpenAI-compatible), with Qwen 3.8 27B by default, or GPT OSS 120B / GPT OSS 20B if the recruiter picks another one in the selector
- in development: Ollama running locally (Qwen2 1.5B), through its native API

## At Server Startup
- Ingestion: the profile documents (French and English) are split into sections, turned into vectors by the embedding model, then stored in ChromaDB with their source, topic, section and language
- In production, ingestion runs again at every startup, which guarantees up-to-date data after each deployment; in development, only if the database is empty
- Both CV PDFs are generated and kept in memory
- Model call: the embedding model, once per section; not the LLM

## Backend
- Python, FastAPI, Uvicorn, pydantic-settings (configuration through environment variables), httpx
- Endpoints: /chat, /health, /config (provider and available models), /cv (CV as a PDF, French or English)
- ChromaDB vector database: embedded in the server in production, containerized ChromaDB server in development
- A single codebase, two modes (development / production), driven by environment variables
- pytest tests of the endpoints, the routing and the RAG pipeline functions, with a simulated LLM
- Maintenance: replacement of models retired by Groq, support for the specific response format of the GPT OSS models; Groq free-tier rate limits identified and signaled to the user

## Frontend
- Next.js 16 (App Router), React 19, TypeScript
- Tailwind CSS 4 with the typography plugin, Markdown rendering of answers (react-markdown), clickable links
- LLM model selector
- For each answer: display of the sources, the model used, the number of tokens and the duration

## Technologies Used
| Part | Technologies |
|------|-------------|
| Website | Next.js 16, React 19, TypeScript, Tailwind CSS 4, react-markdown |
| Server | Python, FastAPI, Uvicorn, pydantic-settings, httpx |
| Search | ChromaDB; all-MiniLM-L6-v2 embeddings (production) and nomic-embed-text (development) |
| LLM | Groq API (production), Ollama (development) |
| PDF | fpdf2, DejaVu fonts |
| Tests | pytest, with a simulated LLM |
| Hosting | Docker; Podman Compose locally; Railway in production |

## Deployment and Operations
- Docker for the server and the website
- Development: Podman Compose with 4 containers (Ollama, ChromaDB, FastAPI server, Next.js website)
- Production: Railway with 2 services (FastAPI server with embedded ChromaDB, Next.js website in standalone mode), automatic redeployment on every push to GitHub
- Custom domain asknarymane.com (DNS at Namecheap), HTTPS

## Known and Accepted Limitations
- Responses are returned in one piece, without progressive display
- No authentication or rate limiting on the API
- Vector database rebuilt at every startup
- Conversation not kept after a page reload

## Skills Demonstrated
- **RAG engineering**: ingestion, chunking, embeddings, vector search, re-ranking, compression, context injection
- **LLM integration**: multi-provider abstraction (Groq / Ollama), on-the-fly model switching, handling of provider constraints
- **Agent architecture**: deterministic keyword-based router orchestrating 5 specialized agents, structured outputs (matching report)
- **Full-stack development**: asynchronous FastAPI API, Next.js / React / TypeScript website
- **Operations**: environment-based configuration, continuous deployment, domain and HTTPS, tests with a simulated LLM
