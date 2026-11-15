# [Ask Narymane](https://asknarymane.com)

**Un chatbot pour les recruteurs : posez vos questions sur le parcours de Narymane Chabane, il répond à partir de son profil.**

👉 **https://asknarymane.com**

## Ce que fait le chatbot

- Répond aux questions sur son **parcours, ses compétences, sa formation et ses projets**, en français ou en anglais (dans la langue de la question)
- Affiche ses **dépôts GitHub en temps réel**
- Aide à la **contacter** : lien email avec un brouillon pré-rempli, lien LinkedIn
- Donne son **CV en PDF** (français ou anglais)
- **Compare son profil à une fiche de poste** collée par le recruteur : score, points forts, écarts, recommandation

Le chatbot ne répond qu'à partir de son profil et de ses dépôts GitHub. S'il ne sait pas, il le dit au lieu d'inventer.

## Comment ça marche (en 30 secondes)

```
Recruteur
   │ pose une question
   ▼
Site web (Next.js) ───────▶ Serveur (FastAPI)
                               │
                  1. Le ROUTEUR lit la question et choisit les agents
                               │
        ┌──────────┬───────────┼───────────┬──────────┐
        ▼          ▼           ▼           ▼          ▼
       RAG       GitHub     Contact     Matching      CV
        └──────────┴───────────┼───────────┴──────────┘
                               ▼
                  2. Les infos sont regroupées en un « contexte »
                               ▼
                  3. UN SEUL appel au LLM, qui rédige la réponse
                               ▼
              Réponse + sources + modèle + tokens + durée
```

AskNarymane repose sur **5 agents spécialisés** (RAG, GitHub, contact, matching, CV), **orchestrés par un routeur déterministe à mots-clés**.

Le point clé : **le LLM n'est appelé qu'une seule fois par question, à la toute fin**. Avant lui, tout est fait par du code classique : le routeur et les agents. C'est rapide, peu coûteux et prévisible.

## Le routeur et les 5 agents

**Le routeur** cherche des mots-clés dans la question, en français et en anglais (« github », « contact », « cv », « fiche de poste »…), et décide quels agents solliciter. Ce n'est pas une IA qui décide, c'est une liste de règles.

| Agent | Ce qu'il fait | Appelle un modèle ? |
|---|---|---|
| **Agent 1 — RAG** (profil) | Cherche dans le profil les 5 passages les plus proches de la question | Oui, le **modèle d'embeddings** (pas le LLM) |
| **Agent 2 — GitHub** | Liste les dépôts publics de [chabanenary](https://github.com/chabanenary) via l'API GitHub (cache de 10 min) | Non |
| **Agent 3 — Contact** | Fournit un lien email avec un brouillon pré-rempli et le lien LinkedIn | Non |
| **Agent 4 — Matching** | Détecte une fiche de poste, en extrait les termes techniques et lance jusqu'à 8 recherches dans le profil. Le LLM rédige ensuite le rapport. | Oui, le **modèle d'embeddings** pour les recherches |
| **Agent 5 — CV** | Ajoute un lien de téléchargement du CV en PDF, dans la langue de la question | Non |

Quand une fiche de poste est détectée, l'agent matching passe en priorité et travaille seul.

### Comment travaille l'agent RAG

1. Le serveur détecte la **langue** de la question (FR/EN) et son **thème** (expérience, formation, projets, CV, blog).
2. Le **modèle d'embeddings** transforme la question en vecteur.
3. **ChromaDB** renvoie les 12 passages les plus proches, filtrés par thème.
4. Le serveur écarte les passages trop éloignés et garde une seule langue quand un passage existe en FR et en EN.
5. Il **reclasse** le reste selon les mots en commun, la présence de noms connus (entreprises, écoles, projets) et la distance.
6. Il garde les **5 meilleurs** et raccourcit les plus longs.

### L'appel final au LLM

Le serveur envoie au LLM, en un seul appel :
- **des règles strictes** : n'utiliser que le contexte fourni, ne rien inventer, répondre dans la langue de la question, ne jamais donner ni deviner l'âge ;
- **le contexte** rassemblé par les agents ;
- **les 6 derniers messages** de la conversation.

## Technologies

| Partie | Technologies |
|---|---|
| Site web | Next.js 16, React 19, TypeScript, Tailwind CSS 4, react-markdown |
| Serveur | Python, FastAPI, Uvicorn, pydantic-settings, httpx |
| Base vectorielle | ChromaDB |
| Embeddings | all-MiniLM-L6-v2 intégré à ChromaDB (prod), nomic-embed-text via Ollama (local) |
| LLM | API Groq (prod), Ollama (local) |
| CV PDF | fpdf2 (polices DejaVu), PDF générés au démarrage du serveur |
| Tests | pytest, avec un LLM simulé |
| Hébergement | Docker, Podman Compose (local), Railway (prod), domaine chez Namecheap |

## Deux modes, un seul code

Le même code tourne en local et en production. Seules les variables d'environnement changent :

| | Local (Podman / Docker Compose) | Production (Railway) |
|---|---|---|
| LLM | Ollama, `qwen2:1.5b` | Groq, `qwen/qwen3.8-27b` par défaut (sélecteur : GPT OSS 120B, GPT OSS 20B) |
| Embeddings | `nomic-embed-text` via Ollama | all-MiniLM-L6-v2 intégré à ChromaDB |
| ChromaDB | Conteneur séparé | Intégré au serveur |
| Conteneurs / services | 4 : site, serveur, ChromaDB, Ollama | 2 : site, serveur |
| `LLM_PROVIDER` | `ollama` | `groq` |
| `EMBEDDING_PROVIDER` | `ollama` | `default` |
| `CHROMA_MODE` | `http` | `embedded` |

## Lancer le projet en local

### Prérequis

- [Podman](https://podman.io/) avec podman-compose, ou [Docker](https://www.docker.com/) avec Docker Compose
- Au moins 8 Go de RAM pour la VM Podman (`podman machine set --memory 8192`), à cause d'Ollama

### Installation et démarrage

```bash
git clone https://github.com/chabanenary/asknarymane.git
cd asknarymane
cp .env.example .env              # les valeurs par défaut sont celles du mode local

podman compose up --build -d      # avec Docker : make dev

# Première fois uniquement : télécharger les modèles dans Ollama
podman compose exec ollama ollama pull nomic-embed-text
podman compose exec ollama ollama pull qwen2:1.5b
```

Au premier démarrage, le serveur charge automatiquement les documents du profil dans ChromaDB si la base est vide.

| Service | Adresse |
|---|---|
| Site web | http://localhost:3000 |
| API | http://localhost:8080 |
| CV PDF | http://localhost:8080/cv?lang=fr (ou `lang=en`) |

Arrêt : `podman compose down` (avec Docker : `make down`).

### Variables d'environnement (`.env`)

| Variable | Rôle | Local | Prod |
|---|---|---|---|
| `LLM_PROVIDER` | Fournisseur du LLM | `ollama` | `groq` |
| `OLLAMA_MODEL` | Modèle Ollama | `qwen2:1.5b` | — |
| `GROQ_API_KEY` | Clé API Groq ([console.groq.com](https://console.groq.com)), à garder secrète | — | votre clé |
| `GROQ_MODEL` | Modèle Groq par défaut | — | `qwen/qwen3.8-27b` |
| `EMBEDDING_PROVIDER` | Modèle d'embeddings | `ollama` | `default` |
| `CHROMA_MODE` | ChromaDB séparé ou intégré | `http` | `embedded` |

Le fichier `.env` n'est jamais commité. Le modèle de fichier est `.env.example`.

## Déploiement en production (Railway)

- Le repo GitHub est connecté à [Railway](https://railway.app) avec **2 services** :
  - **serveur** : construit avec le `Dockerfile` à la racine (voir `railway.json`) ;
  - **site web** : construit avec `frontend/Dockerfile`.
- **Chaque push sur `main` redéploie automatiquement** les deux services. Les tests ne sont pas lancés pendant ce déploiement : lancez-les avant de pousser (voir [Tests](#tests)).
- Variables à définir dans le dashboard Railway, pour le serveur : `LLM_PROVIDER=groq`, `EMBEDDING_PROVIDER=default`, `CHROMA_MODE=embedded`, `GROQ_API_KEY`, `GROQ_MODEL`.
- À chaque démarrage, le serveur recharge tous les documents du profil et régénère les deux CV PDF.
- Le domaine **asknarymane.com** (Namecheap) pointe vers Railway via un CNAME. Le HTTPS est géré par Railway.

Bon à savoir :
- L'adresse du serveur en prod (`https://asknarymane-production.up.railway.app`) est écrite en dur à deux endroits : dans `frontend/Dockerfile`, où elle est intégrée au site au moment du build, et dans `backend/app/routers/chat.py`, pour le lien du CV. Si elle change, il faut la modifier aux deux endroits.
- Si un déploiement reste bloqué, relancez-le depuis le dashboard Railway.

## Mettre à jour le contenu du chatbot

Tout ce que le chatbot sait vient des fichiers Markdown de `documents/` (anglais) et `documents_fr/` (français).

- Modifiez **les deux langues** à chaque fois.
- Découpez chaque fichier en sections `## ` courtes, de 13 lignes maximum : le serveur découpe sur ces titres et raccourcit les sections trop longues.
- Le nom du dossier (`cv`, `experience`, `education`, `projects`, `blog`) sert de thème pour la recherche.
- Le CV PDF est généré à partir de `cv/CV_Narymane_Chabane.md`.

Pour appliquer les changements :

```bash
# En local : recharger les documents, puis redémarrer le serveur pour régénérer les CV PDF
podman compose exec backend python -m app.scripts.ingest
podman compose restart backend

# En production : il suffit de pousser sur main
```

## Tests

```bash
# Dans le conteneur
podman compose exec backend pip install pytest pytest-asyncio -q
podman compose exec backend pytest tests/ -v

# Ou sans conteneur
cd backend
python -m venv .venv
.venv/bin/pip install ".[dev]"
.venv/bin/python -m pytest -v
```

Les tests couvrent les endpoints, le routeur et les fonctions de recherche RAG, avec un LLM simulé. Il n'y a pas encore de tests pour le site web.

## Structure du projet

```
asknarymane/
├── backend/                  # Serveur FastAPI
│   ├── app/
│   │   ├── main.py           # Démarrage : chargement des documents + génération des CV PDF
│   │   ├── config.py         # Variables d'environnement (mode local / prod)
│   │   ├── routers/chat.py   # Endpoints /chat, /health, /config, /cv + règles envoyées au LLM
│   │   ├── services/
│   │   │   ├── agent.py      # Le routeur : choisit les agents selon les mots-clés
│   │   │   ├── rag.py        # Agent RAG : recherche dans le profil (ChromaDB)
│   │   │   ├── embeddings.py # Choix du modèle d'embeddings
│   │   │   ├── llm.py        # Appel au LLM (Groq ou Ollama)
│   │   │   ├── github.py     # Agent GitHub
│   │   │   ├── contact.py    # Agent contact
│   │   │   ├── matching.py   # Agent matching avec une fiche de poste
│   │   │   └── cv_pdf.py     # Agent CV : génération des CV PDF
│   │   └── scripts/ingest.py # Chargement des documents dans ChromaDB
│   ├── tests/                # Tests pytest
│   └── Dockerfile            # Image du serveur en local
├── frontend/                 # Site web Next.js (src/components/ChatWidget.tsx = l'interface de chat)
│   └── Dockerfile
├── documents/                # Profil de Narymane en anglais
├── documents_fr/             # Profil de Narymane en français
├── Dockerfile                # Image du serveur en production (inclut les documents)
├── railway.json              # Configuration Railway du serveur
├── docker-compose.yml        # Les 4 conteneurs du mode local
├── .env.example              # Modèle de configuration
└── Makefile                  # Raccourcis Docker (make dev, make down, make ingest)
```

## Limites connues

- Les réponses arrivent en une seule fois, sans affichage progressif.
- L'API n'a ni authentification ni limitation de débit.
- Le free tier de Groq limite le nombre d'appels : il faut parfois patienter quelques secondes entre deux questions.
- La conversation n'est pas conservée après un rechargement de la page.
