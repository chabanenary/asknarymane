# Ask Narymane

Chatbot IA destiné aux recruteurs pour explorer le parcours professionnel et la formation de Narymane.

## Stack

- **Backend** : Python / FastAPI
- **Frontend** : Next.js / React / Tailwind CSS
- **LLM** : Ollama (qwen2:1.5b en dev)
- **Embeddings** : nomic-embed-text via Ollama
- **Vector DB** : ChromaDB
- **Conteneurisation** : Docker Compose (Podman compatible)

## Architecture

```
Frontend (Next.js :3000)
    │
    ▼
Backend (FastAPI :8080)
    ├──→ ChromaDB (:8000)     — stockage des vecteurs
    └──→ Ollama (:11434)      — LLM (qwen2:1.5b) + embeddings (nomic-embed-text)
```

Le backend utilise un pipeline **RAG** (Retrieval-Augmented Generation) :
1. La question du recruteur est convertie en vecteur via Ollama (nomic-embed-text)
2. Les sections les plus pertinentes du profil sont récupérées dans ChromaDB
3. Le contexte est injecté dans le prompt envoyé au LLM
4. Le LLM génère une réponse factuelle basée sur les données du profil

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

## Lancement

```bash
# Démarrer les services (Ollama + ChromaDB + Backend + Frontend)
podman compose up --build -d

# Télécharger les modèles (première fois uniquement)
podman compose exec ollama ollama pull qwen2:1.5b
podman compose exec ollama ollama pull nomic-embed-text

# Ingérer les documents du profil dans ChromaDB
podman compose exec backend python -m app.scripts.ingest
```

Le frontend est accessible sur **http://localhost:3000** et l'API sur **http://localhost:8080**.

## Arrêt

```bash
podman compose down
```

## Structure du projet

```
asknarymane/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── routers/      # Endpoints (chat, health)
│   │   ├── services/     # LLM, RAG, embeddings
│   │   └── scripts/      # Ingestion des documents
│   └── Dockerfile
├── frontend/             # Interface chat Next.js
│   └── Dockerfile
├── documents/            # Profil Narymane (markdown)
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

Les fichiers markdown dans `documents/` constituent la base de connaissances du chatbot. Ils sont découpés par sections et indexés dans ChromaDB lors de l'ingestion. Pour mettre à jour le profil, modifier les fichiers puis relancer :

```bash
podman compose exec backend python -m app.scripts.ingest
```
