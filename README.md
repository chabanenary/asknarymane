# Ask Narymane

Chatbot IA destiné aux recruteurs pour explorer le parcours professionnel et la formation de Narymane.

## Stack

- **Backend** : Python / FastAPI
- **Frontend** : Next.js / React / Tailwind CSS
- **LLM** : Groq API (Llama 3.3 70B) en prod / Ollama (qwen2:1.5b) en dev local
- **Embeddings** : nomic-embed-text via Ollama (dev) / all-MiniLM-L6-v2 intégré (prod)
- **Vector DB** : ChromaDB (serveur en dev, embedded en prod)
- **Conteneurisation** : Docker Compose (Podman compatible) en dev
- **Hébergement** : Render.com (gratuit) en prod

## Architecture

Le même code supporte deux modes, pilotés par les variables d'environnement :

```
DEV LOCAL (Docker Compose)              PROD (Render.com)
──────────────────────────              ─────────────────
4 containers :                          2 services :
  Frontend (Next.js :3000)                Static Site (CDN)
  Backend (FastAPI :8080)                 Web Service (FastAPI)
  ChromaDB (serveur :8000)                ChromaDB embedded (in-process)
  Ollama (embeddings + LLM)               Pas d'Ollama (Groq + built-in)

LLM_PROVIDER=ollama                     LLM_PROVIDER=groq
EMBEDDING_PROVIDER=ollama               EMBEDDING_PROVIDER=default
CHROMA_MODE=http                        CHROMA_MODE=embedded
```

Le backend utilise un **agent routeur** qui combine plusieurs sources de données :

**RAG** (Retrieval-Augmented Generation) — profil statique :
1. La question du recruteur est convertie en vecteur (embedding)
2. Les sections les plus pertinentes du profil sont récupérées dans ChromaDB (FR + EN)
3. Le contexte est injecté dans le prompt envoyé au LLM

**Agent GitHub** — données temps réel :
- Interroge l'API GitHub en temps réel pour les repos publics de [github.com/chabanenary](https://github.com/chabanenary)
- Liens cliquables, langages, dates de dernière mise à jour
- Cache de 10 minutes

**Agent Contact** — prise de contact :
- Génère un lien mailto cliquable avec un brouillon d'email pré-rempli
- Lien LinkedIn inclus

**Agent Matching** — comparaison profil vs fiche de poste :
- Le recruteur colle une fiche de poste → rapport structuré de compatibilité
- Score, points forts, compétences transférables, écarts, recommandation

Le chatbot répond dans la langue de la question (français ou anglais).

## Prérequis (dev local)

- [Podman](https://podman.io/) ou [Docker](https://www.docker.com/)
- podman-compose ou docker-compose
- VM Podman avec au moins 8 Go de RAM (`podman machine set --memory 8192`)

## Installation

```bash
git clone https://github.com/chabanenary/asknarymane.git
cd asknarymane
cp .env.example .env
```

## Configuration

Tout se configure dans `.env`. Deux profils types :

### Dev local (Docker Compose + Ollama)

```env
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
CHROMA_MODE=http
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2:1.5b
```

### Production (Render + Groq)

```env
LLM_PROVIDER=groq
EMBEDDING_PROVIDER=default
CHROMA_MODE=embedded
GROQ_API_KEY=gsk_votre_clé_ici
GROQ_MODEL=llama-3.3-70b-versatile
```

Modèles Groq disponibles via le sélecteur dans l'interface :
- `llama-3.3-70b-versatile` (par défaut)
- `qwen/qwen3-32b`
- `meta-llama/llama-4-scout-17b-16e-instruct`
- `llama-3.1-8b-instant`

## Lancement (dev local)

```bash
# Démarrer les services
podman compose up --build -d

# Télécharger les modèles (première fois uniquement)
podman compose exec ollama ollama pull nomic-embed-text
podman compose exec ollama ollama pull qwen2:1.5b    # si LLM_PROVIDER=ollama

# Ingérer les documents (ou automatique au démarrage si base vide)
podman compose exec backend python -m app.scripts.ingest
```

Frontend : **http://localhost:3000** | API : **http://localhost:8080**

## Déploiement (Render.com)

Le fichier `render.yaml` configure automatiquement les deux services :
1. Connecter le repo GitHub sur [render.com](https://render.com)
2. Créer les services via "New > Blueprint" et sélectionner le repo
3. Ajouter `GROQ_API_KEY` dans le dashboard Render (Environment)
4. L'ingestion se fait automatiquement au premier démarrage

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
│   │   ├── main.py       # App + auto-ingestion au startup
│   │   ├── config.py     # Settings (dual-mode dev/prod)
│   │   ├── routers/      # Endpoints (chat, health, config)
│   │   ├── services/     # LLM, RAG, GitHub, Contact, Matching, agent routeur
│   │   └── scripts/      # Ingestion des documents
│   ├── tests/            # Tests endpoints + RAG (pytest)
│   └── Dockerfile
├── frontend/             # Interface chat Next.js
│   └── Dockerfile
├── documents/            # Profil Narymane en anglais
├── documents_fr/         # Profil Narymane en français
├── docker-compose.yml    # Dev local (4 containers)
├── render.yaml           # Déploiement Render (2 services)
├── .env.example
└── Makefile
```

## Documents du profil

La base de connaissances est composée de fichiers markdown dans `documents/` (EN) et `documents_fr/` (FR). Les deux versions sont indexées dans ChromaDB. L'ingestion est automatique au démarrage si la base est vide.

Pour forcer une ré-ingestion :

```bash
# Dev local
podman compose exec backend python -m app.scripts.ingest

# Prod (redéployer le backend sur Render suffit)
```
