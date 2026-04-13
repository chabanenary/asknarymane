# Projet — AskNarymane (en cours)

## Présentation
AskNarymane est un chatbot alimenté par RAG (Retrieval Augmented Generation) qui répond aux questions sur le profil professionnel, les projets et l'expérience de Narymane. Il est conçu comme une vitrine portfolio et une démonstration de compétences en déploiement LLM et implémentation RAG.

GitHub : https://github.com/chabanenary/asknarymane
Site web (prévu) : https://asknarymane.dev

## Architecture
- LLM : Ollama servant Mistral 7B (ou Qwen2.5 7B) pour la génération de réponses
- Modèle d'embedding : nomic-embed-text via Ollama pour la vectorisation des documents
- Base vectorielle : ChromaDB pour le stockage et la récupération des embeddings
- API : FastAPI avec endpoints pour le chat, le chat alimenté par RAG, et l'ingestion de documents
- Frontend : Next.js / React / Tailwind CSS — interface de chat interactive
- Conteneurisation : Docker Compose orchestrant Ollama, ChromaDB, le backend FastAPI et le frontend Next.js

## Base de connaissances
Le chatbot est entraîné sur les propres documents de Narymane :
- CV et profil professionnel
- Expérience détaillée chez Ekinops/OneAccess (2007–2020)
- Descriptions de projets : GalleryKeeper, IA Edge sur Jetson Nano, APIs ML Serving, démonstrateur IoT
- Formation : Polytechnique d'Alger, Télécom Paris
- Compétences techniques
- Articles de blog et contributions communautaires

## Ce que ce projet démontre
- Serving LLM (Ollama + modèles open source)
- Implémentation RAG (LangChain + ChromaDB + embeddings)
- Développement d'API (FastAPI)
- Développement frontend (Next.js / React)
- Conteneurisation (Docker Compose, orchestration multi-services)
- Développement d'application IA full-stack
- Pratiques MLOps : gestion de modèles, déploiement, monitoring

## Stratégie de déploiement
- Développement : Ollama localement sur Mac (Apple Silicon M1), qwen2:1.5b pour l'itération rapide
- Production : API Groq (gratuit, rapide) pour la version en ligne sur asknarymane.dev
- Hébergement : Render.com ou Railway.app (offre gratuite)
