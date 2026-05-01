# Narymane Chabane

**Ingénieure IA/ML | Linux Embarqué & Edge AI | MLOps**

Sanary-sur-Mer, France | chabanenarymane@gmail.com | [LinkedIn](https://www.linkedin.com/in/narymane-chabane/) | [GitHub](https://github.com/chabanenary) | [asknarymane.com](https://asknarymane.com)

---

## Profil

Ingénieure IA/ML avec plus de 12 ans d'expérience en R&D systèmes embarqués, désormais spécialisée dans le développement d'applications IA en production. Expertise approfondie en serving LLM, pipelines RAG, déploiement de modèles ML sur edge et cloud, et développement full-stack d'applications IA. Vision système, rigueur de production, et expérience pratique sur l'ensemble du cycle ML — de l'entraînement de modèles au déploiement Kubernetes.

---

## Compétences IA/ML

| Domaine | Technologies |
|---------|-------------|
| **LLM & RAG** | Ollama, API Groq, LangChain, ChromaDB, nomic-embed-text, ingénierie de prompts, gestion de conversations |
| **Agents IA** | MCP (Model Context Protocol), appel d'outils, routage multi-agents, détection d'intention |
| **ML / Deep Learning** | YOLO11 (entraînement, optimisation), TensorFlow/TFLite, ONNX, OpenCV |
| **ML Serving** | FastAPI, ONNX Runtime (CPU & GPU), TensorRT |
| **MLOps & DevOps** | Docker, Kubernetes, OpenShift, GitHub Actions, pipelines CI/CD |
| **Programmation** | Python (5+ ans, avancé), C (10+ ans, expert), Bash, Java |
| **Edge / Embarqué** | NVIDIA Jetson Nano, SoC ARM, noyau Linux, Yocto, RTOS VxWorks |

---

## Projets IA

### AskNarymane — Chatbot RAG pour recruteurs
[asknarymane.com](https://asknarymane.com) | [GitHub](https://github.com/chabanenary/asknarymane)

Chatbot RAG déployé en production avec système multi-agents intelligent.

- **Pipeline RAG** : ingestion bilingue, recherche vectorielle ChromaDB, re-ranking, compression de contexte
- **4 agents** : profil RAG, API GitHub temps réel, facilitation de contact, analyse de matching poste
- **Intégration LLM** : dual-provider (Ollama local / Groq cloud), changement de modèle à la volée
- **Stack** : Python, FastAPI, Next.js, ChromaDB, Docker, Railway.app
- **Déploiement** : architecture dual-mode (Docker Compose dev / Railway prod), auto-ingestion, gestion CORS

### YoloGK Serving API — Déploiement ML multi-plateforme
[GitHub](https://github.com/chabanenary/yoloGK-serving-api)

Serving de modèle ML sur 3 environnements avec un code identique.

- **CPU/Cloud** : FastAPI + ONNX Runtime, Docker, pytest
- **Edge GPU** : NVIDIA Jetson Nano, accélération CUDA/TensorRT, NVIDIA L4T
- **Orchestration** : Kubernetes/OpenShift avec replicas, probes, limites de ressources
- Write once, deploy everywhere — pattern MLOps clé démontré

### GalleryKeeper — IA embarquée pour la vie privée
[GitHub](https://github.com/chabanenary/GalleryKeeper-App) | [Pipeline d'entraînement](https://github.com/chabanenary/Yolo11_training_GK) | [Blog](https://dev.to/chabanenary) | [Démo EN](https://www.youtube.com/watch?v=jnUaWvC-wpw) | [Démo FR](https://www.youtube.com/watch?v=V_BQd_TGrLw)

Application Android privacy-first qui détecte et organise les photos sensibles (nudité, enfants, documents d'identité, cartes bancaires) via un modèle YOLO11 entraîné sur mesure — 100% hors ligne, zéro upload cloud.

- **Première application Android**, entièrement autodidacte (Java, Android SDK, architecture MVVM, base Room)
- **Modèle YOLO11 custom** entraîné de zéro : curation et annotation du dataset (1 400+ images, 4 classes), entraînement avec Ultralytics, évaluation, quantization, export TFLite
- **Inférence on-device** avec TFLite — classification temps réel, aucune connexion internet requise
- **Monitoring en arrière-plan** via un service Android foreground avec notifications
- **Privacy by design** : utilise l'API MediaStore, les photos ne quittent jamais l'appareil, l'utilisateur confirme toutes les actions
- **Pipeline ML complet** : collecte de données → annotation → entraînement → optimisation → déploiement mobile → API de serving (YoloGK)
- Article technique publié sur Dev.to détaillant tout le parcours d'apprentissage

---

## Expérience professionnelle

### Ingénieure R&D Linux Embarqué — Ekinops / OneAccess, Paris (2011–2020)
- Pilotage du développement de la solution Virtual CPE (vCPE) sur plateformes x86 — Linux, containers Docker, CI/CD
- Développement et maintenance de firmware Linux pour équipements télécom opérateur (routeurs, passerelles)
- Développement BSP, configuration noyau, systèmes de build Yocto/OpenEmbedded
- Coordination d'équipes offshore, revues de code, documentation technique

### Ingénieure logiciel embarqué — Eolices, Paris (2007–2011)
- Développement firmware RTOS VxWorks pour équipements réseau
- Multitâche temps réel, gestion d'interruptions, drivers matériels (Ethernet, SFP, Wi-Fi, 4G)
- Portage et personnalisation du bootloader U-Boot

### Stage — STMicroelectronics, Paris (2006–2007)
- Développement logiciel embarqué dans le cadre du Master à Télécom Paris

---

## Formation

- **Master — Télécom Paris** (2006) — Dispositifs et Techniques de Communication, Mention Très Bien
- **Ingénieure — École Nationale Polytechnique d'Alger** (2000–2005) — Électronique et Télécommunications, Mention Très Bien
- **Formation continue** — Hands-On ML (Aurélien Géron), MOOCs IA Générative, autodidacte en FastAPI, Docker, Kubernetes

---

## Langues

- Français (langue maternelle) | Arabe (langue maternelle) | Anglais (courant)

---

## Publications

- [Building GalleryKeeper: an AI-powered Android app](https://dev.to/chabanenary) — Article technique sur Dev.to
- Contributrice open source — tous les projets IA/ML publiés sur GitHub
