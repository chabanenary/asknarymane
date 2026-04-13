# Projet — YoloGK Serving API (Déploiement ML multi-plateforme)

## Présentation
Une suite de projets démontrant le déploiement multi-plateforme du modèle YOLO11 GalleryKeeper entraîné par Narymane, via une API REST. Le même modèle et le même code applicatif sont déployés sur trois environnements différents, illustrant les bonnes pratiques MLOps.

## Trois cibles de déploiement

### 1. yoloGK-serving-api — Déploiement CPU/Mac
GitHub : https://github.com/chabanenary/yoloGK-serving-api

- API REST FastAPI servant le modèle YOLO11 GalleryKeeper
- ONNX Runtime pour l'inférence (CPU)
- Conteneurisé avec Docker
- Conçu pour le développement, les tests et le déploiement cloud
- Endpoints : /health, /device, /classify, /classify/batch
- Documentation Swagger automatique à /docs
- Tests avec pytest

Stack technique : Python, FastAPI, ONNX Runtime, Pillow, Docker, pytest

### 2. yoloGK-jetson-serving-api — Déploiement GPU Jetson Nano
GitHub : https://github.com/chabanenary/yoloGK-jetson-serving-api

- Même application FastAPI adaptée pour NVIDIA Jetson Nano
- Inférence accélérée par GPU via ONNX Runtime avec CUDA/TensorRT
- Basé sur l'image Docker NVIDIA L4T (Linux for Tegra)
- Détection automatique du GPU : utilise CUDA si disponible, repli sur CPU sinon
- Optimisé pour du matériel contraint (4 Go de RAM, GPU Maxwell)
- Container Docker avec runtime nvidia

Stack technique : Python, FastAPI, ONNX Runtime GPU, CUDA, TensorRT, Docker, NVIDIA L4T

### 3. yoloGK-kubernetes-serving-api — Déploiement Kubernetes/OpenShift
GitHub : https://github.com/chabanenary/yoloGK-kubernetes-serving-api

- Manifestes de déploiement Kubernetes pour l'API de serving
- Deployment avec réplicas, limites de ressources, sondes liveness/readiness
- Configuration Service avec ClusterIP
- Route OpenShift pour l'accès externe
- Conçu pour un déploiement orchestré de grade production

Stack technique : Kubernetes, OpenShift, Docker, manifestes YAML

## Endpoints API (communs à tous les déploiements)
- GET /health — Sonde de vie, rapporte le statut du modèle
- GET /device — Retourne la disponibilité GPU/CUDA et le provider d'inférence actif
- POST /classify — Classifier une image unique (upload + seuil de confiance)
- POST /classify/batch — Classifier plusieurs images en une requête, retourne les résultats par image et un résumé

## Architecture
Le modèle (format ONNX) est identique sur les trois déploiements. Le code applicatif (FastAPI + logique d'inférence) est aussi identique. Seuls le Dockerfile et la configuration de déploiement changent par cible. Cela illustre un pattern clé en MLOps : écrire une fois, déployer partout.

## Ce que cela prouve
Narymane sait prendre un modèle ML entraîné et le déployer sur tout le spectre des environnements : développement local (Mac/CPU), device edge avec GPU (Jetson Nano), et orchestration cloud (Kubernetes/OpenShift). C'est exactement l'ensemble de compétences attendu d'une ingénieure déploiement ML ou MLOps.
