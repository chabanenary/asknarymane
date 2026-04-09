# Ask Narymane

Chatbot IA destiné aux recruteurs pour explorer le parcours professionnel et la formation de Narymane.

## Stack

- **Backend** : Python / FastAPI
- **Frontend** : Next.js / React / Tailwind CSS
- **LLM** : Ollama (qwen2:1.5b en dev)
- **Conteneurisation** : Docker Compose (Podman compatible)

## Prérequis

- [Podman](https://podman.io/) ou [Docker](https://www.docker.com/)
- podman-compose ou docker-compose

## Installation

```bash
git clone https://github.com/chabanenary/asknarymane.git
cd asknarymane
cp .env.example .env
```

## Lancement

```bash
# Démarrer les services (Ollama + Backend + Frontend)
podman compose up --build -d

# Télécharger le modèle LLM (première fois uniquement)
podman compose exec ollama ollama pull qwen2:1.5b
```

Le frontend est accessible sur **http://localhost:3000** et l'API sur **http://localhost:8080**.

## Arrêt

```bash
podman compose down
```

## Structure du projet

```
asknarymane/
├── backend/          # API FastAPI
├── frontend/         # Interface chat Next.js
├── docker-compose.yml
├── .env.example      # Template des variables d'environnement
└── Makefile
```
