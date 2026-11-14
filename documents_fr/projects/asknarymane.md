# Projet — IA / AskNarymane (assistant RAG multi-sources en production, 2026)

## Présentation
AskNarymane est un assistant web destiné aux recruteurs. Il répond en français ou en anglais aux questions sur le parcours, les compétences et les projets de Narymane, donne ses dépôts GitHub en temps réel, facilite la prise de contact, génère son CV en PDF et évalue l'adéquation de son profil à une fiche de poste. Narymane l'a conçu, développé, déployé et l'exploite de bout en bout. Le projet a démarré en avril 2026.

- Site : https://asknarymane.com
- Dépôt : https://github.com/chabanenary/asknarymane

## Backend
- Python, FastAPI, Uvicorn, pydantic-settings (configuration par variables d'environnement), httpx
- Endpoints : /chat, /health, /config (fournisseur et modèles disponibles), /cv (CV en PDF, français ou anglais)
- Génération du CV PDF avec fpdf2 à partir d'un Markdown bilingue, polices DejaVu pour l'Unicode ; les deux PDF sont pré-générés au démarrage
- Tests pytest des endpoints, du routage et des fonctions du pipeline RAG, avec LLM mocké

## Frontend
- Next.js 16 (App Router), React 19, TypeScript
- Tailwind CSS 4 avec le plugin typography, rendu Markdown des réponses (react-markdown), liens cliquables
- Sélecteur de modèle LLM
- Pour chaque réponse : affichage des sources, du modèle utilisé, du nombre de tokens et de la durée

## Pipeline RAG
- Base de connaissances : documents Markdown bilingues (français et anglais) découpés sur les titres de sections, avec métadonnées (source, catégorie, titre, section, langue)
- Base vectorielle ChromaDB : embarquée dans le backend en production, serveur ChromaDB conteneurisé en développement
- Embeddings : all-MiniLM-L6-v2 (intégré à ChromaDB) en production, nomic-embed-text via Ollama en développement
- Recherche : détection de la langue et de la catégorie de la question, filtrage par catégorie, 12 candidats récupérés puis seuil de distance
- Post-traitement : dédoublonnage FR/EN, re-ranking personnalisé (recouvrement lexical, bonus d'entités connues, distance), 5 extraits conservés, compression du contexte
- Cache des requêtes en mémoire (5 minutes)

## Routage d'agents
Un routeur déterministe, par mots-clés en français et en anglais, compose le contexte envoyé au LLM à partir de cinq sources :
1. **RAG** : le profil de Narymane
2. **GitHub** : ses dépôts publics en temps réel via l'API GitHub (forks exclus, cache de 10 minutes), avec liens cliquables
3. **Contact** : lien mailto qui ouvre un brouillon d'email pré-rempli, et lien LinkedIn
4. **Matching** : quand un recruteur colle une fiche de poste, extraction des termes techniques, requêtes RAG ciblées, puis rapport structuré (score de compatibilité, points forts, compétences transférables, écarts, recommandation) avec consigne de ne pas gonfler le score ; cette source est prioritaire et exclusive
5. **CV PDF** : lien de téléchargement du CV dans la langue de la question

Le LLM ne fait pas d'appel d'outils lui-même : le routage déterministe est un choix assumé pour la fiabilité et le coût.

## LLM et prompt
- Production : API Groq (compatible OpenAI) avec plusieurs modèles ouverts au choix de l'utilisateur (Qwen 3.8 27B par défaut, GPT OSS 120B, GPT OSS 20B)
- Développement : Ollama en local (Qwen2 1.5B), via son API native
- Un seul codebase, deux modes (développement / production), pilotés par variables d'environnement
- Prompt système strict anti-hallucination, avec réponse de repli explicite quand l'information manque ; réponse dans la langue de la question ; interdiction de communiquer ou de déduire la date de naissance ou l'âge
- Contexte injecté sous forme d'un échange simulé avant la conversation ; fenêtre des 6 derniers messages ; enrichissement de la requête de recherche à partir des tours précédents
- Maintenance : remplacement des modèles retirés par Groq, prise en charge du format de réponse spécifique des modèles GPT OSS ; limites de débit du free tier Groq identifiées et signalées à l'utilisateur

## Déploiement et exploitation
- Docker pour le backend et le frontend
- Développement : Podman Compose avec 4 conteneurs (Ollama, ChromaDB, backend FastAPI, frontend Next.js)
- Production : Railway avec 2 services (backend FastAPI avec ChromaDB embarqué, frontend Next.js en mode standalone), redéploiement automatique à chaque push sur GitHub
- Domaine personnalisé asknarymane.com (DNS chez Namecheap), HTTPS
- La base vectorielle est ré-ingérée à chaque démarrage du backend en production, ce qui garantit des données à jour après chaque déploiement

## Limites connues et assumées
- Les réponses sont renvoyées en une seule fois, sans affichage progressif
- Pas d'authentification ni de limitation de débit sur l'API
- Base vectorielle reconstruite à chaque démarrage
- Conversation non conservée après rechargement de la page

## Compétences démontrées
- **Ingénierie RAG** : ingestion, découpage, embeddings, recherche vectorielle, re-ranking, compression, injection de contexte
- **Intégration LLM** : abstraction multi-fournisseur (Groq / Ollama), changement de modèle à la volée, gestion des contraintes des fournisseurs
- **Architecture d'agents** : détection d'intention par mots-clés, composition de sources, sorties structurées (rapport de matching)
- **Développement full-stack** : API asynchrone FastAPI, frontend Next.js / React / TypeScript
- **Exploitation** : configuration par environnement, déploiement continu, domaine et HTTPS, tests avec LLM mocké
