# LLM, RAG et routage d'agents — Compétences en IA appliquée

## Contexte
Depuis 2026, Narymane construit et exploite des systèmes à base de LLM en conditions réelles. C'est la suite logique de son parcours en IA : après l'entraînement et le déploiement de modèles de vision (YOLO sur Android, Jetson Nano et Kubernetes), elle a conçu AskNarymane, un assistant RAG multi-agents en production, puis, en mission freelance, l'orchestration temps réel entre perception embarquée et LLM cloud.

## Intégration d'API LLM
- API Groq (compatible OpenAI) en production, avec plusieurs modèles ouverts sélectionnables par l'utilisateur
- Ollama pour l'inférence locale en développement (API native)
- LLM cloud en streaming, phrase par phrase, avec cache de contexte (mission IA embarquée)
- Gestion des contraintes des fournisseurs : limites de débit du free tier, retrait de modèles par le fournisseur, formats de réponse spécifiques à certains modèles
- Configuration par variables d'environnement pour basculer entre développement et production

## Ce qu'elle maîtrise sur les LLM
- Fonctionnement des LLM : architecture transformer, prédiction de tokens, fenêtre de contexte
- Compromis entre familles et tailles de modèles : qualité, vitesse, mémoire, support linguistique
- Quantization et impact sur la taille et la qualité du modèle (4 bits, GGUF, Q8, FP16), mise en pratique avec llama.cpp
- Différence entre entraîner un modèle et le servir ou le déployer
- Déploiement local, sur l'appareil ou dans le cloud : compromis vie privée, latence, coût

## RAG — Génération augmentée par récupération
Le RAG augmente un LLM généraliste avec des connaissances spécifiques à un domaine : on récupère les documents pertinents au moment de la question et on les injecte dans le prompt. Narymane a conçu et mis en production le pipeline RAG d'AskNarymane :
- Base de connaissances Markdown bilingue découpée sur les titres de sections, avec métadonnées (source, catégorie, section, langue)
- Base vectorielle ChromaDB ; embeddings all-MiniLM-L6-v2 en production, nomic-embed-text en développement
- Détection de la langue et de la catégorie de la question, filtrage par catégorie, seuil de distance
- Dédoublonnage FR/EN, re-ranking personnalisé (recouvrement lexical, bonus d'entités connues, distance), compression du contexte, cache des requêtes

## Routage d'agents
- Dans AskNarymane, un routeur déterministe par mots-clés (FR/EN) orchestre 5 agents spécialisés : RAG, dépôts GitHub en temps réel, contact, matching avec une fiche de poste, génération de CV PDF ; le LLM est appelé une seule fois, à la fin
- Le LLM ne fait pas d'appel d'outils lui-même : le routage déterministe est un choix assumé pour la fiabilité et le coût
- Sur sa mission IA embarquée, l'orchestrateur Python asyncio route la perception vers l'appareil et le raisonnement vers le LLM cloud

## Conception de prompts
- Prompt système strict anti-hallucination, avec réponse de repli explicite quand l'information manque
- Réponse dans la langue de la question (français ou anglais)
- Fenêtre de conversation et enrichissement de la requête de recherche à partir des tours précédents
- Prompt de matching structuré (score, points forts, compétences transférables, écarts, recommandation) avec consigne de ne pas gonfler le score

## Évaluation et observabilité des systèmes IA
- Benchmarks à protocole défini pour comparer des modèles (mission IA embarquée)
- Tests automatisés avec LLM mocké (pytest)
- Suivi des tokens, de la latence et des erreurs ; affichage du modèle, des sources, des tokens et de la durée de chaque réponse dans AskNarymane
- Monitoring embarqué (mémoire, GPU, températures, latences) et tests d'endurance

## Le lien avec son parcours
Le background en systèmes embarqués de Narymane lui donne une perspective particulière sur les systèmes IA :
- **Conscience des ressources** : des années sur des équipements contraints la font raisonner en mémoire, latence et efficacité de calcul — critique pour déployer des LLM et des modèles de vision
- **Vision système** : comprendre comment les composants (LLM, embeddings, base vectorielle, API, appareil) interagissent et où se situent les goulots d'étranglement
- **Mentalité production** : la discipline CMMI niveau 3 se traduit directement en systèmes IA fiables, documentés et testés
- **Conteneurisation et API** : l'expérience FastAPI et Docker de ses projets de serving est réutilisée dans ses applications LLM

## Résumé des outils
| Catégorie | Outils |
|-----------|--------|
| API LLM | Groq (compatible OpenAI), Ollama, LLM cloud en streaming |
| Inférence locale | llama.cpp, ONNX Runtime, quantization 4 bits / GGUF |
| Base vectorielle | ChromaDB |
| Embeddings | all-MiniLM-L6-v2, nomic-embed-text |
| API et backend | FastAPI, Uvicorn, pydantic-settings, httpx |
| Tests | pytest avec LLM mocké |
| Conteneurisation | Docker, Podman Compose |
