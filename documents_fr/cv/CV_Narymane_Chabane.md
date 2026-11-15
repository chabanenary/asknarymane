# Narymane Chabane

**Ingénieure logiciel embarqué et IA | Edge AI, LLM, systèmes fiables en production**

Sanary-sur-Mer, France (full remote) | chabanenarymane@gmail.com | [LinkedIn](https://www.linkedin.com/in/narymane-chabane/) | [GitHub](https://github.com/chabanenary) | [asknarymane.com](https://asknarymane.com)

---

## Profil

Ingénieure logiciel avec 13 ans de R&D sur des équipements télécom de grade opérateur chez OneAccess / Ekinops, des bootloaders et drivers jusqu'aux couches système et applicatives d'un OS de routeur virtuel. Reconvertie depuis 2024 vers l'IA appliquée : modèles de vision entraînés et déployés sur Android, systèmes LLM/RAG en production, et depuis juin 2026 IA embarquée temps réel (voix + vision) sur NVIDIA Jetson pour une start-up. Fil conducteur : la fiabilité des systèmes en conditions réelles — spécifier, mesurer, tester, monitorer. Consultante freelance (Malt), ouverte aux CDI, en full remote.

---

## Compétences

| Domaine | Technologies |
|---------|-------------|
| IA embarquée | PyTorch, YOLO, TFLite / LiteRT, ONNX Runtime, TensorRT, CUDA, llama.cpp, quantization 4 bits / GGUF, OpenCV, GStreamer, NVIDIA Jetson Nano et Orin Nano, Android |
| IA appliquée & LLM | API Groq et Ollama, LLM cloud en streaming, RAG (ChromaDB, embeddings, re-ranking, compression de contexte), routage d'agents, conception de prompts, évaluation |
| Évaluation de modèles | Datasets, dédoublonnage, détection de fuites train/validation, Label Studio, données synthétiques, mAP, parité entre formats de modèle |
| Audio temps réel | Pipelines full-duplex, détection d'activité vocale, reconnaissance et synthèse vocales, annulation d'écho, barge-in, PipeWire, BlueZ |
| Linux embarqué | Yocto / OpenEmbedded, Debian, kernel et device tree, U-Boot, systemd, udev, NetworkManager, BSP, secure boot, VxWorks |
| Déploiement & cloud | FastAPI, Docker, Podman, Kubernetes, OpenShift (AWS), Railway, GitHub Actions, Jenkins |
| Langages | C (13 ans, expert), C++, Python, Java, Bash, Perl, SQL, TypeScript |
| Méthode | CMMI niveau 3, spécifications, plans de test, lead technique, coordination offshore, rapports techniques |

---

## Expérience professionnelle

### Ingénieure IA embarquée — Mission freelance (juin 2026 – aujourd'hui)
- Responsable du logiciel embarqué et de l'IA côté appareil d'un produit conversationnel multimodal temps réel pour une start-up, du POC au prototype, sur NVIDIA Jetson Orin Nano 8 Go, en binôme avec le développeur cloud du client
- Architecture hybride edge / cloud : voix et vision traitées sur l'appareil, raisonnement par un LLM cloud en streaming ; seul du texte anonymisé quitte l'appareil
- Audio full-duplex : détection d'activité vocale, reconnaissance vocale sur GPU, synthèse vocale locale et cloud, barge-in, annulation d'écho (7 configurations évaluées, 0 faux déclenchement retenu), audio Bluetooth
- Vision : modèle vision-langage de 2 milliards de paramètres quantifié en 4 bits ; migration de PyTorch vers llama.cpp libérant 1,5 à 2,5 Go de mémoire
- Orchestrateur Python asyncio, passerelle Socket.IO vers le backend du client et une interface React / Three.js ; JetPack 6, systemd, udev, provisioning Wi-Fi
- Monitoring embarqué (mémoire, GPU, températures, latences) ; endurance de 2 heures sans crash ni fuite mémoire, latence inférieure à 1 seconde, POC validé en trois mois
- Conseil matériel (caméra, micro array, écran tactile, audio Bluetooth), chiffrages, rapports techniques

### Projets IA et développement Android en indépendante (septembre 2024 – mai 2026)
- Portfolio public d'applications d'IA en production : GalleryKeeper, AskNarymane, YoloGK (voir Projets IA)
- Pipelines vidéo sur Jetson Nano : GStreamer, RTSP, OpenCV, PyTorch → ONNX → TensorRT, profiling des FPS sous contraintes thermiques

### Pause parentale et reconversion vers l'IA (2020 – 2024)
- Reconversion autodidacte : Python, Java/Android, machine learning, deep learning, IA générative

### OneAccess / Ekinops, Paris (mai 2007 – mars 2020)
- Ingénieure R&D systèmes embarqués, puis ingénieure Linux embarqué senior
- Une seule expérience de 13 ans : de 2007 à 2011 en prestation via l'ESN Eolices, puis salariée de OneAccess (rachetée par Ekinops en 2017)
- Responsable du composant bootloader de toute l'entreprise (U-Boot et loaders VxWorks) sur une dizaine de cartes, du MIPS aux QorIQ multiprocesseurs et au x86 : portage, mise à jour firmware, secure boot
- Lead technique d'une équipe de 4 ingénieurs (2009-2012) ; pilotage d'une équipe offshore de 3 personnes (2011-2013)
- Boucle qualité sur l'OS complet : tests fonctionnels, non-régression, fiches d'anomalie créées automatiquement à partir des échecs de tests
- 2019-2020 — Routeurs virtuels sur x86 (Debian) : journalisation, monitoring de bout en bout, gestion mémoire, CLI, framework de licences ; C et Python
- 2014-2017 — Routeurs Gigabit VoIP (Freescale T1040, Yocto) : drivers Ethernet, switch SFP, mémoire, LEDs, alimentation
- 2011-2013 — Routeurs Ethernet/IP Gigabit (Freescale P1021, VxWorks) : bootloader bi-cœur, système de défense et de crash logs
- 2007-2011 — Routeurs xDSL (MIPS, PowerPC 83xx, VxWorks) : QoS ATM, drivers xDSL ; cheffe de projet de l'outil de chargement dynamique de firmwares xDSL

### Stage ingénieure — STMicroelectronics, Paris (juillet – décembre 2006)
- Outil d'évaluation (Perl/Tk) d'une base de milliers de blocs de propriété intellectuelle destinés à des chipsets mobiles 3G : définition des critères de qualité, vérifications automatiques, rapports

---

## Projets IA

### GalleryKeeper — Application Android avec IA embarquée (2024 – 2026)
[GitHub](https://github.com/chabanenary/GalleryKeeper-App) | [Pipeline d'entraînement](https://github.com/chabanenary/Yolo11_training_GK) | [Article Dev.to](https://dev.to/chabanenary/my-first-android-app-as-a-beginner-what-i-learned-building-an-offline-ml-gallery-organizer-and-3d1k) | [Démo FR](https://www.youtube.com/watch?v=V_BQd_TGrLw) | [Démo EN](https://www.youtube.com/watch?v=jnUaWvC-wpw)

- Détection et tri des photos sensibles entièrement sur l'appareil ; publiée sur le Play Store, plus de 1 000 téléchargements
- Java, MVVM, Room, MediaStore, service de premier plan, LiteRT avec délégué GPU ; 53 tests unitaires
- Modèle YOLO11n entraîné de zéro sur un dataset collecté et annoté par Narymane, exporté en TFLite
- Audit de l'évaluation (fuites train/validation, annotations décalées) et dataset reconstruit de 2 530 à 6 712 images : mAP50 de 0,657 à 0,746
- Diagnostic de la chaîne de décision de l'application : documents d'identité et cartes bancaires correctement classés de 81-83 % à 98 %, parité TFLite / PyTorch vérifiée

### AskNarymane — Assistant RAG multi-agents en production (2026)
[asknarymane.com](https://asknarymane.com) | [GitHub](https://github.com/chabanenary/asknarymane)

- Assistant pour recruteurs, en français et en anglais : RAG sur un profil bilingue, dépôts GitHub en temps réel, contact, CV PDF, matching avec une fiche de poste
- 5 agents spécialisés (RAG, GitHub, contact, matching, CV) orchestrés par un routeur déterministe à mots-clés ; LLM appelé une seule fois ; prompt strict anti-hallucination
- FastAPI, ChromaDB, API Groq (production) et Ollama (développement), Next.js 16, React 19, TypeScript, Tailwind CSS 4
- Docker, Podman Compose, production sur Railway avec déploiement continu, domaine personnalisé et HTTPS

### YoloGK — Serving d'un modèle de vision sur CPU, Jetson et Kubernetes (2026)
[GitHub](https://github.com/chabanenary/yoloGK-kubernetes-serving-api)

- Le modèle de GalleryKeeper servi depuis un seul codebase : Nginx → FastAPI + ONNX Runtime → PostgreSQL 16
- CPU (Docker, pytest), Jetson Nano (CUDA, TensorRT), Kubernetes et OpenShift sur AWS (kustomize, HPA, probes, NetworkPolicy, PV/PVC, ingress)

---

## Formation

- **Master — Télécom Paris** (2006) — Dispositifs et techniques de communication, Mention Très Bien
- **Diplôme d'ingénieure en électronique — École Nationale Polytechnique d'Alger** (2000–2005) — Mention Très Bien
- **Formation en gestion de projet — Université de Marne-la-Vallée** (2007)
- **Autoformation en IA** (2020–2024, en continu depuis) — Python, Java/Android, machine learning (Aurélien Géron, MOOCs), deep learning, IA générative

---

## Langues

- Français (langue maternelle) | Arabe (langue maternelle) | Anglais (courant, usage professionnel quotidien)

