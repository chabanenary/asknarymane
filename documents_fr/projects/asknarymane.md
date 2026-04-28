# Projet — IA / AskNarymane

## Présentation
AskNarymane est un chatbot alimenté par RAG qui répond aux questions des recruteurs sur le profil professionnel, les projets et l'expérience de Narymane. Il intègre un système d'agents intelligent combinant données de profil statiques, informations GitHub en temps réel, facilitation de contact, et analyse de correspondance avec des fiches de poste. C'est une vitrine portfolio et une démonstration de compétences avancées en ingénierie IA/ML.

GitHub : https://github.com/chabanenary/asknarymane
Site web (prévu) : https://asknarymane.dev

## Architecture
- **Fournisseur LLM** : Système dual — API Groq (Llama 3.3 70B) en production, Ollama (qwen2:1.5b) en développement local. Commutable via variable d'environnement.
- **Modèle d'embedding** : nomic-embed-text via Ollama pour la vectorisation des documents
- **Base vectorielle** : ChromaDB pour le stockage et la récupération des embeddings
- **Backend** : Python FastAPI avec endpoints asynchrones pour le chat, la configuration et le health check
- **Frontend** : Next.js / React / Tailwind CSS — interface de chat interactive avec sélecteur de modèle, rendu markdown, liens cliquables et affichage des métadonnées (sources, tokens, durée)
- **Conteneurisation** : Docker Compose (compatible Podman) orchestrant 4 services : Ollama, ChromaDB, backend FastAPI, frontend Next.js

## Système d'agents intelligent
Le backend utilise un routeur d'agents qui détecte l'intention de l'utilisateur et oriente vers les sources de données appropriées :

### Agent 1 — RAG (Profil)
- Ingestion bilingue de documents (fichiers markdown anglais + français)
- Découpage par sections H2 markdown avec préfixe contextuel
- Détection de langue (FR/EN) avec déduplication des résultats inter-langues
- Filtrage par catégorie (expérience, formation, projets, cv, blog)
- Re-ranking par chevauchement de mots-clés + boost des entités connues
- Compression du contexte pour réduire le bruit
- Cache en mémoire (TTL 5 min)

### Agent 2 — GitHub (Temps réel)
- Interroge l'API GitHub pour les dépôts publics de chabanenary
- Retourne noms, descriptions, langages, dates de dernière mise à jour, étoiles
- Liens markdown cliquables dans les réponses
- Cache en mémoire (TTL 10 min) pour respecter les limites de l'API GitHub

### Agent 3 — Contact
- Génère un lien mailto pré-rempli (sujet + corps) pour que les recruteurs contactent Narymane
- Fournit le lien du profil LinkedIn
- Un clic ouvre le client mail du recruteur avec un brouillon prêt à envoyer

### Agent 4 — Matching de poste
- Détecte quand un recruteur colle une fiche de poste (analyse de mots-clés + heuristiques de longueur)
- Récupère le profil complet de Narymane dans toutes les catégories RAG
- Demande au LLM de générer un rapport de correspondance structuré :
  - Score de compatibilité (pourcentage)
  - Points forts correspondants
  - Compétences transférables
  - Écarts identifiés
  - Recommandation

## Compétences IA/ML démontrées
Ce projet met en valeur les compétences IA/ML suivantes :

- **Serving & Intégration LLM** : Abstraction multi-fournisseur LLM (Ollama local + Groq cloud), changement de modèle à la volée, consommation d'API compatible OpenAI
- **Ingénierie de pipeline RAG** : RAG de bout en bout — ingestion de documents, stratégies de chunking, génération d'embeddings, stockage vectoriel, recherche sémantique, injection de contexte, prompt engineering
- **Modèles d'embedding** : Déploiement et utilisation de nomic-embed-text via Ollama, implémentation custom d'EmbeddingFunction pour ChromaDB
- **Prompt Engineering** : Conception de system prompts pour le suivi d'instructions, pattern de fake-exchange pour l'injection de contexte avec petits modèles, prompting adapté à la langue
- **Architecture d'agents** : Détection d'intention, routage multi-sources, combinaison de contextes, génération de sorties structurées (rapports de matching)
- **Développement d'applications IA** : Application IA full-stack (backend Python + frontend React), conception d'API asynchrone, intégration de données temps réel (API GitHub), déploiement conteneurisé
- **Pratiques MLOps** : Configuration par environnement, sélection de modèle via UI, suivi des tokens/durée, développement piloté par les tests avec appels LLM mockés

## Base de connaissances
La base de connaissances du chatbot est constituée des propres documents de Narymane en anglais et en français :
- CV et profil professionnel
- 13+ ans d'expérience chez Ekinops/OneAccess (2007–2020) : systèmes embarqués, VxWorks RTOS, Linux, Yocto, Virtual CPE
- Postes précédents : Eolices (2007–2011), STMicroelectronics (2006–2007)
- Projets IA/ML : GalleryKeeper (Android + YOLO), YoloGK Serving API (déploiement ML multi-plateforme), AskNarymane (chatbot RAG)
- Formation : Polytechnique d'Alger, Télécom Paris
- Compétences techniques
- Articles de blog et contributions communautaires

## Déploiement en production
Ce projet est déployé en production sur asknarymane.net, démontrant la capacité de Narymane à concevoir, développer et déployer une application IA complète avec des agents intelligents en conditions réelles. Le pipeline complet — de l'ingestion de documents au serving LLM en passant par le routage d'agents — tourne en production.

Narymane a conçu une architecture dual-mode qui permet au même code de tourner dans deux environnements :
- **Développement** : Docker Compose (Podman) avec 4 containers — Ollama (embeddings + LLM), serveur ChromaDB, backend FastAPI, frontend Next.js
- **Production** : Render.com avec 2 services — backend FastAPI (ChromaDB embedded + API Groq), site statique Next.js (CDN)

Compétences de déploiement démontrées :
- **Déploiement cloud** : configuration Render.com Web Service + Static Site
- **Infrastructure as Code** : blueprint `render.yaml` pour un déploiement déclaratif
- **Configuration pilotée par l'environnement** : même code, comportement différent via variables d'environnement (LLM_PROVIDER, EMBEDDING_PROVIDER, CHROMA_MODE)
- **Auto-ingestion** : le backend ingère automatiquement les documents au démarrage si la base vectorielle est vide
- **Stratégie d'embedding duale** : Ollama (nomic-embed-text) en dev, ChromaDB intégré (all-MiniLM-L6-v2) en prod — aucune dépendance externe en production
- **Export de site statique** : Next.js configuré pour le mode standalone (Docker) et l'export statique (CDN)
- **Gestion CORS** : configuration dynamique des origines pour les environnements dev et prod
