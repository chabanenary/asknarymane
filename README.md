# Ask Narymane

Chatbot IA destiné aux recruteurs pour explorer le parcours professionnel et la formation de Narymane.

## Stack

- **Backend** : Python / FastAPI
- **Frontend** : Next.js / React / Tailwind CSS
- **LLM** : Groq API (Llama 3.3 70B) en prod / Ollama (qwen2:1.5b) en dev local
- **Embeddings** : nomic-embed-text via Ollama
- **Vector DB** : ChromaDB
- **Conteneurisation** : Docker Compose (Podman compatible)

## Architecture

```
Frontend (Next.js :3000)
    |
    v
Backend (FastAPI :8080)
    |---> Agent routeur           -- decide RAG, GitHub, ou les deux
    |       |---> ChromaDB (:8000)    -- RAG (profil statique)
    |       +---> GitHub API          -- repos temps reel
    |---> Ollama (:11434)        -- embeddings (nomic-embed-text)
    +---> LLM Provider           -- configurable :
          - Groq API (cloud)        llama-3.3-70b-versatile (defaut)
          - Ollama (local)          qwen2:1.5b
```

Le backend utilise un **agent routeur** qui combine deux sources de données :

**RAG** (Retrieval-Augmented Generation) — profil statique :
1. La question du recruteur est convertie en vecteur via Ollama (nomic-embed-text)
2. Les sections les plus pertinentes du profil sont récupérées dans ChromaDB (FR + EN)
3. Le contexte est injecté dans le prompt envoyé au LLM

**Agent GitHub** — données temps réel :
- Quand la question concerne GitHub (repos, code, contributions), l'agent interroge l'API GitHub en temps réel
- Les repos publics de [github.com/chabanenary](https://github.com/chabanenary) sont récupérés avec langages, dates, descriptions
- Les liens sont cliquables dans la réponse
- Cache de 10 minutes pour éviter le rate limiting

Le chatbot répond dans la langue de la question (français ou anglais).

## Prérequis

- [Podman](https://podman.io/) ou [Docker](https://www.docker.com/)
- podman-compose ou docker-compose
- VM Podman avec au moins 8 Go de RAM (`podman machine set --memory 8192`)

## Installation

```bash
git clone https://github.com/chabanenary/asknarymane.git
cd asknarymane
cp .env.example .env
```

## Configuration du LLM

Le provider LLM est configurable via la variable `LLM_PROVIDER` dans `.env` :

### Option 1 — Groq API (recommandé)

Modèle cloud performant, gratuit (30 req/min). Créer une clé sur [console.groq.com](https://console.groq.com).

```env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_votre_clé_ici
GROQ_MODEL=llama-3.3-70b-versatile
```

Modèles disponibles via le sélecteur dans l'interface :
- `llama-3.3-70b-versatile` (par défaut, le plus performant)
- `qwen/qwen3-32b`
- `meta-llama/llama-4-scout-17b-16e-instruct`
- `llama-3.1-8b-instant`

### Option 2 — Ollama (dev local)

Modèle local, pas besoin de clé API ni d'internet. Plus lent et moins performant.

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2:1.5b
```

## Lancement

```bash
# Démarrer les services (Ollama + ChromaDB + Backend + Frontend)
podman compose up --build -d

# Télécharger le modèle d'embedding (toujours nécessaire)
podman compose exec ollama ollama pull nomic-embed-text

# Télécharger le modèle LLM local (uniquement si LLM_PROVIDER=ollama)
podman compose exec ollama ollama pull qwen2:1.5b

# Ingérer les documents du profil dans ChromaDB
podman compose exec backend python -m app.scripts.ingest
```

Le frontend est accessible sur **http://localhost:3000** et l'API sur **http://localhost:8080**.

## Tests

```bash
podman compose exec backend pip install pytest pytest-asyncio -q
podman compose exec backend pytest tests/ -v
```

## Arrêt

```bash
podman compose down
```

## Structure du projet

```
asknarymane/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── routers/      # Endpoints (chat, health, config)
│   │   ├── services/     # LLM (Ollama/Groq), RAG, GitHub, agent routeur, embeddings
│   │   └── scripts/      # Ingestion des documents
│   ├── tests/            # Tests endpoints (pytest)
│   └── Dockerfile
├── frontend/             # Interface chat Next.js
│   └── Dockerfile
├── documents/            # Profil Narymane en anglais (markdown)
├── documents_fr/         # Profil Narymane en français (markdown)
│   ├── cv/               # Profil, aspirations
│   ├── experience/       # Expériences pro
│   ├── education/        # Parcours académique
│   ├── projects/         # Projets personnels
│   └── blog/             # Publications
├── docs/                 # Documentation technique
├── docker-compose.yml
├── .env.example
└── Makefile
```

## Documents du profil

La base de connaissances du chatbot est composée de fichiers markdown dans `documents/` (anglais) et `documents_fr/` (français). Les deux versions sont indexées dans ChromaDB pour un matching optimal quelle que soit la langue de la question.

Pour mettre à jour le profil, modifier les fichiers puis relancer :

```bash
podman compose exec backend python -m app.scripts.ingest
```
