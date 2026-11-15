# Projet — IA / AskNarymane (assistant RAG multi-sources en production, 2026)

## Présentation
AskNarymane est un assistant web destiné aux recruteurs. Il répond en français ou en anglais aux questions sur le parcours, les compétences et les projets de Narymane, donne ses dépôts GitHub en temps réel, facilite la prise de contact, génère son CV en PDF et évalue l'adéquation de son profil à une fiche de poste. Narymane l'a conçu, développé, déployé et l'exploite de bout en bout. Le projet a démarré en avril 2026.

- Site : https://asknarymane.com
- Dépôt : https://github.com/chabanenary/asknarymane

## Fonctionnement en bref : le parcours d'une question
En une phrase : AskNarymane trie d'abord la question avec des mots-clés, rassemble les informations utiles depuis plusieurs sources, puis appelle le LLM une seule fois, à la toute fin, pour rédiger la réponse.
1. Le recruteur pose sa question sur le site web (Next.js), qui envoie la conversation au serveur (FastAPI)
2. Le routeur lit la question et choisit les sources à consulter parmi cinq : RAG (profil), GitHub, contact, matching avec une fiche de poste, CV PDF
3. Chaque source choisie produit des informations ; elles sont regroupées en un seul « contexte »
4. Le serveur fait un seul appel au LLM avec les règles, le contexte et la fin de la conversation
5. La réponse revient au site avec les sources utilisées, le modèle, le nombre de tokens et la durée

## Le routeur : le chef d'orchestre
- Rôle : décider quelles sources consulter pour chaque question
- Fonctionnement : il cherche des mots-clés dans la question, en français et en anglais (« github », « contact », « cv », « fiche de poste »…). Ce n'est pas une IA qui décide : c'est une liste de règles, donc rapide, gratuite et prévisible
- Si la question contient un mot qui renvoie à ce qui précède (« ça », « cela », « this », « that »…) et qu'il y a déjà eu des échanges, il ajoute les 2 messages précédents à la recherche pour mieux la comprendre
- Le matching avec une fiche de poste est prioritaire : quand il se déclenche, il travaille seul
- Le RAG est consulté pour toutes les questions, sauf une demande de contact pure
- Appel au modèle : aucun. Le LLM ne fait pas d'appel d'outils lui-même : le routage déterministe est un choix assumé pour la fiabilité et le coût

## Source 1 — RAG : le profil de Narymane
- Rôle : retrouver les passages du profil qui répondent à la question
- Étape 1 : détection de la langue de la question (français ou anglais) et de son thème (expérience, formation, projets, CV, blog)
- Étape 2 : la question est transformée en vecteur par le modèle d'embeddings
- Étape 3 : recherche des 12 passages les plus proches dans ChromaDB, filtrés par thème ; si le filtre ne donne rien, nouvelle recherche sans filtre
- Étape 4 : les passages trop éloignés sont écartés ; quand un passage existe en français et en anglais, seule la langue de la question est gardée
- Étape 5 : reclassement selon les mots en commun avec la question, la présence de noms connus (entreprises, écoles, projets) et la distance ; les 5 meilleurs sont conservés et les plus longs sont raccourcis
- Le résultat est gardé 5 minutes en mémoire pour les questions identiques
- Appel au modèle : oui, au modèle d'embeddings, pas au LLM — all-MiniLM-L6-v2, intégré à ChromaDB, en production ; nomic-embed-text via Ollama en développement

## Source 2 — GitHub : les projets en temps réel
- Rôle : lister les dépôts publics de Narymane (github.com/chabanenary)
- Fonctionnement : interrogation de l'API GitHub, forks écartés, mise en forme du nom, de la description, du langage, de la date de dernière mise à jour et d'un lien cliquable
- Le résultat est gardé 10 minutes en mémoire
- Appel au modèle : aucun

## Source 3 — Contact
- Rôle : aider le recruteur à écrire à Narymane
- Fonctionnement : un texte tout prêt avec un lien email qui ouvre un brouillon pré-rempli (sujet et message), plus le lien de son profil LinkedIn
- Appel au modèle : aucun

## Source 4 — Matching avec une fiche de poste
- Rôle : évaluer si le profil de Narymane correspond à un poste
- Détection : le recruteur a collé une fiche de poste (au moins 3 mots typiques comme « missions » ou « requirements », ou un texte long contenant au moins l'un d'eux)
- Fonctionnement : extraction des termes techniques de l'offre (Python, CUDA, Kubernetes…), puis jusqu'à 8 recherches dans le profil (4 générales et jusqu'à 4 ciblées sur ces termes)
- Il prépare une consigne pour un rapport en 5 points : score de compatibilité, points forts, compétences transférables, écarts, recommandation, avec l'instruction de ne pas gonfler le score
- Appel au modèle : au modèle d'embeddings pour chaque recherche ; c'est le LLM qui rédige le rapport, lors de l'appel final

## Source 5 — CV PDF
- Rôle : donner le CV de Narymane en PDF
- Fonctionnement : quand on demande le CV, un lien de téléchargement est ajouté au contexte, dans la langue de la question, avec la consigne de l'inclure dans la réponse
- Les deux PDF (français et anglais) sont fabriqués avec fpdf2 à partir des fichiers Markdown du CV, dès le démarrage du serveur
- Appel au modèle : aucun

## L'appel final au LLM : le seul de la question
Le serveur assemble un message qui contient :
- les règles : n'utiliser que les informations fournies, ne rien inventer, répondre « Cette information n'est pas disponible dans mon contexte » quand elle manque, répondre dans la langue de la question, ne jamais donner ni deviner la date de naissance ou l'âge
- le contexte rassemblé par les sources, présenté comme un échange déjà fait avant la conversation
- les 6 derniers messages de la conversation

Puis il fait un seul appel au LLM :
- en production : API Groq (compatible OpenAI), avec Qwen 3.8 27B par défaut, ou GPT OSS 120B / GPT OSS 20B si le recruteur en choisit un autre dans le sélecteur
- en développement : Ollama en local (Qwen2 1.5B), via son API native

## Au démarrage du serveur
- Ingestion : les documents du profil (français et anglais) sont découpés en sections, transformés en vecteurs par le modèle d'embeddings, puis rangés dans ChromaDB avec leur source, leur thème, leur section et leur langue
- En production, l'ingestion est refaite à chaque démarrage, ce qui garantit des données à jour après chaque déploiement ; en développement, seulement si la base est vide
- Les deux CV PDF sont générés et gardés en mémoire
- Appel au modèle : le modèle d'embeddings, une fois par section ; pas le LLM

## Backend
- Python, FastAPI, Uvicorn, pydantic-settings (configuration par variables d'environnement), httpx
- Endpoints : /chat, /health, /config (fournisseur et modèles disponibles), /cv (CV en PDF, français ou anglais)
- Base vectorielle ChromaDB : embarquée dans le serveur en production, serveur ChromaDB conteneurisé en développement
- Un seul codebase, deux modes (développement / production), pilotés par variables d'environnement
- Tests pytest des endpoints, du routage et des fonctions du pipeline RAG, avec un LLM simulé
- Maintenance : remplacement des modèles retirés par Groq, prise en charge du format de réponse spécifique des modèles GPT OSS ; limites de débit du free tier Groq identifiées et signalées à l'utilisateur

## Frontend
- Next.js 16 (App Router), React 19, TypeScript
- Tailwind CSS 4 avec le plugin typography, rendu Markdown des réponses (react-markdown), liens cliquables
- Sélecteur de modèle LLM
- Pour chaque réponse : affichage des sources, du modèle utilisé, du nombre de tokens et de la durée

## Technologies utilisées
| Partie | Technologies |
|--------|-------------|
| Site web | Next.js 16, React 19, TypeScript, Tailwind CSS 4, react-markdown |
| Serveur | Python, FastAPI, Uvicorn, pydantic-settings, httpx |
| Recherche | ChromaDB ; embeddings all-MiniLM-L6-v2 (production) et nomic-embed-text (développement) |
| LLM | API Groq (production), Ollama (développement) |
| PDF | fpdf2, polices DejaVu |
| Tests | pytest, avec un LLM simulé |
| Hébergement | Docker ; Podman Compose en local ; Railway en production |

## Déploiement et exploitation
- Docker pour le serveur et le site web
- Développement : Podman Compose avec 4 conteneurs (Ollama, ChromaDB, serveur FastAPI, site Next.js)
- Production : Railway avec 2 services (serveur FastAPI avec ChromaDB embarqué, site Next.js en mode standalone), redéploiement automatique à chaque push sur GitHub
- Domaine personnalisé asknarymane.com (DNS chez Namecheap), HTTPS

## Limites connues et assumées
- Les réponses sont renvoyées en une seule fois, sans affichage progressif
- Pas d'authentification ni de limitation de débit sur l'API
- Base vectorielle reconstruite à chaque démarrage
- Conversation non conservée après rechargement de la page

## Compétences démontrées
- **Ingénierie RAG** : ingestion, découpage, embeddings, recherche vectorielle, reclassement, compression, injection de contexte
- **Intégration LLM** : abstraction multi-fournisseur (Groq / Ollama), changement de modèle à la volée, gestion des contraintes des fournisseurs
- **Architecture d'agents** : détection d'intention par mots-clés, composition de sources, sorties structurées (rapport de matching)
- **Développement full-stack** : API asynchrone FastAPI, site Next.js / React / TypeScript
- **Exploitation** : configuration par environnement, déploiement continu, domaine et HTTPS, tests avec un LLM simulé
