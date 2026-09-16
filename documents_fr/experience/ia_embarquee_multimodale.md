# IA Embarquée Multimodale — Mission Freelance

## Contexte
Depuis juin 2026, Narymane travaille en freelance sur un projet de développement d'un produit IA embarqué multimodal sur NVIDIA Jetson Orin Nano Super 8GB. Elle intervient du POC au prototype, avec une responsabilité couvrant l'ensemble du produit : choix hardware, architecture logicielle et sélection des modèles d'IA.

## Rôle & Responsabilités
- Conception et développement d'un système IA multimodal embarqué de bout en bout
- Contribution aux choix hardware (plateforme edge, capteurs, audio, vidéo)
- Définition de l'architecture logicielle du système (edge + cloud)
- Sélection, évaluation et intégration des modèles d'IA (STT, vision, LLM, TTS)
- Mise en place du pipeline temps réel complet : capture → analyse → inférence → restitution
- Optimisation des performances sous contraintes de ressources (8 Go RAM, GPU partagé, thermique)

## Architecture & Compétences techniques

### Edge Computing (Jetson Orin Nano)
- Orchestration multi-thread asynchrone (Python asyncio + threads)
- Pipeline audio temps réel : capture micro, annulation d'écho (PipeWire AEC), détection d'activité vocale (VAD Silero)
- Speech-to-Text embarqué avec Whisper sur GPU
- Analyse de prosodie vocale (Librosa) pour l'évaluation de l'état utilisateur
- Vision par ordinateur : capture webcam (OpenCV), inférence modèle vision multimodal (Qwen-VL via llama.cpp sur GPU)
- Gestion audio avancée : PipeWire, annulation d'écho matériel, streaming audio, mécanisme de barge-in (interruption utilisateur temps réel)
- Monitoring thermique et gestion des ressources GPU/RAM

### Architecture hybride Edge-Cloud
- Communication temps réel bidirectionnelle via Socket.IO
- Gateway de relais entre composants edge et services cloud
- Intégration de LLM cloud (Gemini) avec context caching pour optimiser les coûts
- Synthèse vocale cloud avec streaming audio retour vers l'edge
- Frontend React avec rendu 3D (Three.js) et synchronisation labiale

### DevOps & Déploiement embarqué
- Provisioning automatisé du Jetson (scripts bash one-shot)
- Services systemd pour les composants critiques (STT GPU)
- Règles udev pour la configuration audio automatique
- Configuration PipeWire pour l'annulation d'écho
- Cross-compilation et déploiement du frontend (build sur Mac, déploiement sur Jetson)
- Mode kiosk Firefox avec configuration audio spécifique

### Conteneurisation & Provisioning
- Conteneurisation du provisioning du Jetson Orin Nano
- Automatisation du déploiement des services et dépendances via conteneurs

### Privacy-by-Design
- Aucune donnée brute (image, audio) ne quitte le device edge
- Seuls des résumés textuels sont transmis au cloud (transcriptions, descriptions)
- Base de données locale sur tmpfs (pas d'écriture SSD)

## Résultats mesurés
- Latence perçue médiane < 1 seconde
- Coût API cloud optimisé (context caching)
- Zéro faux positif de barge-in
- Température GPU maîtrisée (55-57°C, seuil critique 80°C)
- Démarrage complet du système en ~30 secondes

## Stack technique

| Catégorie | Technologies |
|-----------|-------------|
| Plateforme edge | NVIDIA Jetson Orin Nano Super 8GB |
| Langages | Python, JavaScript/TypeScript, Bash |
| IA / ML | Whisper (STT), Qwen-VL (vision), Silero (VAD), llama.cpp, Gemini |
| Audio | PipeWire, AEC (annulation d'écho), Librosa (prosodie) |
| Vision | OpenCV, llama.cpp (modèles multimodaux) |
| Communication | Socket.IO (temps réel bidirectionnel) |
| Frontend | React, Three.js (3D), Vite |
| Infrastructure | systemd, udev, PipeWire, tmpfs, Firefox kiosk |
| Outils | Git, SSH, SCP, Claude Code |

## Disponibilité
Narymane est actuellement disponible pour des missions freelance. Son profil est consultable sur Malt.
