# LLM, RAG & Agents IA — Compétences actuelles

## Contexte
Depuis 2025, Narymane construit activement une expérience pratique avec les grands modèles de langage (LLM), la génération augmentée par récupération (RAG), et les agents IA. C'est la suite logique de son parcours en IA : après avoir maîtrisé l'entraînement de modèles ML et le déploiement edge (YOLO sur Jetson Nano et Android), elle apprend maintenant à construire des applications IA complètes et des systèmes intelligents.

## Serving LLM — Ollama

### Ce qu'elle utilise
- Ollama comme plateforme de serving LLM locale sur Mac (Apple Silicon M1)
- Modèles : Qwen2 1.5B pour le développement/test, Mistral 7B et Qwen2.5 7B pour des réponses de qualité production
- API Ollama (compatible OpenAI) pour l'intégration programmatique

### Ce qu'elle maîtrise
- Fonctionnement des LLM à haut niveau : architecture transformer, prédiction de tokens, fenêtre de contexte
- Les différences entre les familles de modèles (Mistral, Llama, Qwen) et leurs compromis (taille, qualité, vitesse, support linguistique)
- La quantization et son impact sur la taille et la qualité du modèle (Q4, Q8, FP16)
- La différence entre entraîner un modèle et le servir/déployer
- Déploiement LLM local vs cloud : compromis vie privée, latence, coût
- Architecture d'Ollama : gestion des modèles, accélération Metal sur Apple Silicon, API REST

### Compétences pratiques
- Installation d'Ollama et gestion des modèles (pull, run, serve)
- Construction d'applications FastAPI qui communiquent avec l'API Ollama
- Implémentation d'endpoints de chat avec gestion de l'historique de conversation
- Réponses en streaming pour une expérience utilisateur temps réel
- Configuration du modèle LLM via variables d'environnement pour basculer facilement entre dev et production

## RAG — Génération Augmentée par Récupération

### De quoi s'agit-il
Le RAG est une technique qui augmente un LLM générique avec des connaissances spécifiques à un domaine en récupérant des documents pertinents au moment de la requête et en les injectant dans le prompt. Cela permet au LLM de répondre à des questions sur du contenu sur lequel il n'a jamais été entraîné — comme le profil professionnel de Narymane.

### Stack technologique
- LangChain : framework pour construire des pipelines RAG (chargement de documents, découpage de texte, orchestration de chaînes)
- ChromaDB : base de données vectorielle légère pour stocker et interroger les embeddings de documents
- Modèle d'embedding : nomic-embed-text via Ollama — tourne en local, pas besoin d'API externe
- Découpage de texte : RecursiveCharacterTextSplitter pour découper les documents en morceaux de taille optimale

### Ce qu'elle maîtrise
- Fonctionnement des embeddings : transformer du texte en vecteurs numériques qui capturent le sens sémantique
- Fonctionnement de la recherche par similarité vectorielle : comparer les embeddings de la requête avec ceux des documents pour trouver le contenu pertinent
- Le pipeline RAG : ingestion (découpe → vectorisation → stockage) et requête (vectoriser la question → rechercher → augmenter le prompt → générer la réponse)
- Stratégies de chunking : pourquoi la taille des morceaux et le chevauchement importent pour la qualité de la récupération
- L'importance de la qualité des documents : de meilleurs documents sources = de meilleures réponses du chatbot

### Compétences pratiques
- Construction d'un pipeline RAG complet from scratch avec LangChain + ChromaDB
- Écriture de scripts d'ingestion qui traitent des documents Markdown
- Création d'endpoints FastAPI pour l'ingestion de documents et le chat alimenté par RAG
- Préparation de documents spécifiques à un domaine (Markdown structuré) pour des performances RAG optimales
- Conteneurisation de la stack RAG complète (Ollama + ChromaDB + FastAPI) avec Docker Compose

## Agents IA & MCP (Model Context Protocol)

### Qu'est-ce que MCP
MCP (Model Context Protocol) est un protocole standard développé par Anthropic qui permet aux agents IA d'utiliser des outils externes. Au lieu que le LLM essaie de tout répondre depuis ses données d'entraînement, il peut appeler des outils (rechercher sur le web, lire des fichiers, interroger des bases de données, appeler des APIs) pour obtenir des informations en temps réel.

### Ce qu'elle construit
- Des serveurs MCP qui exposent des outils au LLM agent (météo, recherche documentaire, lecture de repos GitHub)
- Une couche agent qui décide quand utiliser des outils vs quand répondre directement
- Intégration de l'appel d'outils MCP avec le pipeline RAG — l'agent peut rechercher dans la base de connaissances comme un de ses outils

### Ce qu'elle maîtrise
- Le paradigme agent : le LLM comme moteur de raisonnement qui décide quels outils utiliser
- L'appel d'outils / function calling : comment le LLM génère des requêtes structurées vers des outils externes
- Le protocole MCP : architecture client-serveur, enregistrement d'outils, flux requête/réponse
- La différence entre RAG (récupération passive de connaissances) et agents (utilisation active d'outils)

### Stack technologique
- SDK MCP pour Python
- FastAPI pour l'implémentation de serveurs MCP
- Intégration avec Ollama et LangChain

## Le lien avec son parcours

Le background en systèmes embarqués de Narymane lui donne une perspective unique sur les systèmes IA :

- **Conscience des ressources** : des années de travail sur des dispositifs contraints la font naturellement réfléchir à l'utilisation mémoire, la latence et l'efficacité de calcul — critique quand on déploie des LLM
- **Vision système** : comprendre comment tous les composants (LLM, modèle d'embedding, base vectorielle, serveur API) interagissent et où se situent les goulots d'étranglement
- **Mentalité production** : la discipline CMMI Niveau 3 se traduit directement dans la construction de systèmes IA fiables, bien documentés et testables
- **Conteneurisation** : l'expérience Docker de ses projets ML serving se transfère directement à l'orchestration d'applications LLM multi-services
- **Conception d'API** : l'expérience FastAPI de ses projets YOLO serving est directement réutilisée pour l'API du chatbot

## Résumé des outils et frameworks

| Catégorie | Outils |
|-----------|--------|
| Serving LLM | Ollama, API Groq |
| Modèles | Mistral 7B, Qwen2.5, Qwen2 1.5B, nomic-embed-text |
| Framework RAG | LangChain, LangChain Community |
| Base vectorielle | ChromaDB |
| Framework API | FastAPI, Uvicorn |
| Protocole agent | MCP (Model Context Protocol) |
| Conteneurisation | Docker, Docker Compose |
| Développement | Python, VS Code, Claude Code |
