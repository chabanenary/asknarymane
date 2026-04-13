# Phase 2 — RAG : Explications détaillées

## Qu'est-ce que le RAG ?

**RAG** = Retrieval-Augmented Generation (Génération Augmentée par Récupération)

Le principe : au lieu d'envoyer directement la question de l'utilisateur au LLM, on cherche d'abord les informations pertinentes dans une base de données, puis on les injecte dans le prompt avant d'envoyer au LLM.

```
Sans RAG :
  Question → LLM → Réponse (inventée ou générique)

Avec RAG :
  Question → Recherche dans la base → Contexte trouvé → Question + Contexte → LLM → Réponse (factuelle)
```

---

## Architecture Phase 2

```
                        Tout tourne dans des containers (Podman/Docker)
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌──────────┐   POST /chat   ┌──────────────────────────────────┐           │
│  │ Frontend │ ─────────────→ │ Backend FastAPI                  │           │
│  │ Next.js  │                │                                  │           │
│  │ :3000    │ ←───────────── │  1. Reçoit la question           │           │
│  │          │    { reply }   │  2. Demande embeddings à Ollama  │           │
│  └──────────┘                │  3. Cherche dans ChromaDB        │           │
│                              │  4. Construit le prompt enrichi  │           │
│                              │  5. Envoie à Ollama (LLM)       │           │
│                              │  6. Retourne la réponse          │           │
│                              └──────┬──────────┬───────────────┘           │
│                                     │          │                            │
│                                     ▼          ▼                            │
│                              ┌──────────┐  ┌──────────────────────┐        │
│                              │ ChromaDB │  │ Ollama               │        │
│                              │ :8000    │  │ :11434               │        │
│                              │ (stocke  │  │ - qwen2:1.5b (LLM)  │        │
│                              │ vecteurs)│  │ - nomic-embed-text   │        │
│                              │          │  │   (embeddings)       │        │
│                              └──────────┘  └──────────────────────┘        │
│                                                                             │
│  Réseau interne Docker : les containers communiquent entre eux via HTTP     │
│  Seuls les ports 3000, 8080, 8000, 11434 sont exposés sur la machine hôte  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Les outils et leur rôle

### 1. ChromaDB — Base de données vectorielle

**Rôle** : Stocker les documents du profil sous forme de vecteurs (embeddings) et permettre la recherche par similarité sémantique.

**Pourquoi une base vectorielle ?** Une recherche classique (par mots-clés) ne comprend pas le sens. Si un recruteur demande "quelle est son expérience en intelligence artificielle ?", une recherche par mots-clés ne trouverait pas un paragraphe qui parle de "YOLO11" ou "TensorRT". La recherche vectorielle, elle, comprend que ces concepts sont liés.

**Comment ça marche :**
1. Chaque morceau de texte est converti en un vecteur (une liste de nombres) par un modèle d'embedding
2. Ces vecteurs sont stockés dans ChromaDB
3. Quand une question arrive, elle est aussi convertie en vecteur
4. ChromaDB trouve les vecteurs les plus proches (= les textes les plus pertinents)

**Dans le docker-compose :**
```yaml
chromadb:
  image: chromadb/chroma:latest
  ports:
    - "8000:8000"
  volumes:
    - chroma_data:/chroma/chroma   # Persistance des données
```

ChromaDB stocke les vecteurs mais ne génère pas les embeddings lui-même. C'est le backend qui s'en charge en appelant Ollama (voir section Embeddings ci-dessous).

---

### 2. Script d'ingestion (`app/scripts/ingest.py`)

**Rôle** : Lire les fichiers markdown du dossier `documents/`, les découper en morceaux (chunks), et les stocker dans ChromaDB.

**Étapes du script :**

```
documents/
├── cv/profile.md
├── experience/ekinops_oneaccess.md
├── experience/llm_rag_agents.md
├── ...
```

#### Étape 1 — Lecture des fichiers
Parcourt récursivement le dossier `documents/` et lit tous les `.md`. Pour chaque fichier, on garde le contenu + des métadonnées (catégorie, nom du fichier source).

#### Étape 2 — Chunking (découpage)
Un LLM a une limite de contexte. On ne peut pas envoyer tous les documents d'un coup. Le chunking découpe chaque document en morceaux de ~500 caractères.

```
Document original (2000 caractères)
  → Chunk 1 (500 car.) : "Narymane a travaillé chez Ekinops..."
  → Chunk 2 (500 car.) : "...développement de drivers VxWorks..."
  → Chunk 3 (500 car.) : "...migration vers Linux embarqué..."
  → Chunk 4 (500 car.) : "...projet Virtual CPE..."
```

**Overlap (chevauchement)** : Les chunks se chevauchent de 50 caractères pour ne pas couper une idée en plein milieu. Le début du chunk 2 reprend la fin du chunk 1.

#### Étape 3 — Embedding via Ollama
Chaque chunk est envoyé à Ollama (modèle `nomic-embed-text`) qui le convertit en vecteur. Le backend envoie ensuite le vecteur + le texte original + les métadonnées à ChromaDB pour stockage.

---

### 3. Embeddings via Ollama (`app/services/embeddings.py`)

**Rôle** : Convertir du texte en vecteurs (embeddings) en utilisant Ollama comme fournisseur d'embeddings.

**Pourquoi Ollama plutôt que le modèle par défaut de ChromaDB ?**
ChromaDB embarque par défaut un modèle ONNX (`all-MiniLM-L6-v2`) pour générer les embeddings côté client. Problème : ce modèle de 79 Mo doit être téléchargé dans le container backend au premier lancement, ce qui provoque des timeouts réseau dans un environnement containerisé.

En utilisant Ollama, on mutualise : Ollama héberge à la fois le LLM (`qwen2:1.5b`) et le modèle d'embedding (`nomic-embed-text`). Tout reste dans les containers, pas de téléchargement externe au runtime.

**Le modèle `nomic-embed-text`** : un modèle d'embedding open-source performant (~274 Mo). Il convertit du texte en vecteurs de 768 dimensions. Deux textes sémantiquement proches auront des vecteurs proches.

**Implémentation** : une classe `OllamaEmbeddingFunction` qui implémente l'interface `EmbeddingFunction` de ChromaDB. Elle appelle l'endpoint `/api/embed` d'Ollama pour chaque texte :

```python
class OllamaEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Pour chaque texte, appelle Ollama /api/embed
        # Retourne les vecteurs correspondants
```

Cette classe est utilisée à deux endroits :
- **À l'ingestion** : pour convertir les chunks en vecteurs avant stockage dans ChromaDB
- **À la recherche (RAG)** : pour convertir la question du recruteur en vecteur avant de chercher les chunks similaires

---

### 4. Service RAG (`app/services/rag.py`)

**Rôle** : Interroger ChromaDB pour trouver les chunks les plus pertinents par rapport à la question du recruteur.

```python
def retrieve_context(query: str, n_results: int = 5) -> str:
```

- Prend la question de l'utilisateur
- Interroge ChromaDB (qui convertit la question en vecteur et cherche les 5 vecteurs les plus proches)
- Retourne les textes correspondants, séparés par `---`

**Exemple :**
- Question : "Quelle est son expérience en systèmes embarqués ?"
- ChromaDB retourne les 5 chunks les plus pertinents (ceux sur Ekinops, VxWorks, Linux embarqué, etc.)

---

### 5. Prompt augmenté (`app/routers/chat.py`)

**Rôle** : Assembler le system prompt + le contexte récupéré + la question, puis envoyer le tout au LLM.

**Le system prompt** définit la personnalité et les règles du chatbot :
- C'est l'assistant de Narymane Chabane
- Il répond aux recruteurs
- Il se base UNIQUEMENT sur le contexte fourni (pas d'hallucination)
- Il répond en français ou anglais selon la question
- Il utilise le féminin pour parler de Narymane

**Ce qui est envoyé au LLM :**
```
[System] Tu es l'assistant virtuel de Narymane Chabane...
         Contexte : {les 5 chunks pertinents trouvés par ChromaDB}

[User]   Quelle est son expérience en embarqué ?

[Assistant] → Réponse basée sur le contexte
```

---

### 6. Volume monté pour les documents

```yaml
backend:
  volumes:
    - ./documents:/app/documents:ro   # :ro = read-only
```

Le dossier `documents/` de la machine hôte est monté en lecture seule dans le container backend. Le script d'ingestion peut ainsi lire les markdown sans les copier dans l'image Docker.

---

## Flux complet d'une question

```
1. Le recruteur tape : "Quels projets a réalisé Narymane ?"

2. Le frontend envoie POST /chat au backend

3. Le backend extrait la dernière question utilisateur

4. Le service RAG :
   → Envoie la question à Ollama (nomic-embed-text) pour obtenir le vecteur
   → Interroge ChromaDB avec ce vecteur
   → ChromaDB trouve les 5 chunks les plus proches sémantiquement
   → Retourne les textes sur GalleryKeeper, YoloGK, AskNarymane...

5. Le backend construit le prompt :
   [System] Tu es l'assistant de Narymane... Contexte : {chunks}
   [User] Quels projets a réalisé Narymane ?

6. Le prompt est envoyé à Ollama (qwen2:1.5b)

7. Le LLM génère une réponse basée sur le contexte

8. La réponse est renvoyée au frontend
```

---

## Fichiers modifiés/créés dans cette phase

| Fichier | Action | Rôle |
|---------|--------|------|
| `docker-compose.yml` | Modifié | Ajout service ChromaDB + volume documents |
| `backend/pyproject.toml` | Modifié | Ajout dépendance `chromadb` |
| `backend/app/config.py` | Modifié | Ajout settings `chroma_host`, `chroma_port`, `documents_dir` |
| `backend/app/scripts/ingest.py` | Créé | Script d'ingestion markdown → ChromaDB |
| `backend/app/services/embeddings.py` | Créé | Embedding via Ollama (nomic-embed-text) |
| `backend/app/services/rag.py` | Créé | Service de recherche dans ChromaDB |
| `backend/app/routers/chat.py` | Modifié | Intégration RAG + system prompt |
| `Makefile` | Modifié | Ajout commande `make ingest` |
