# Projet — IA / YoloGK Serving API (déploiement ML multi-plateforme, 2026)

## Présentation
YoloGK sert le modèle de détection YOLO11 de GalleryKeeper, entraîné par Narymane, via une API REST, selon le principe « write once, deploy everywhere » : le même modèle et le même code applicatif sont déployés sur CPU, sur NVIDIA Jetson Nano et sur Kubernetes / OpenShift. Seuls le Dockerfile et la configuration de déploiement changent selon la cible.

## Architecture 3 tiers
- Nginx en frontal
- API FastAPI qui exécute le modèle YOLO11 via ONNX Runtime
- Base de données PostgreSQL 16

## Cible 1 — CPU (yoloGK-serving-api)
GitHub : https://github.com/chabanenary/yoloGK-serving-api
- API FastAPI servant le modèle YOLO11 via ONNX Runtime (CPU)
- Conteneurisée avec Docker ; Docker / Podman Compose
- Documentation Swagger automatique à /docs
- Tests avec pytest
- Stack : Python, FastAPI, ONNX Runtime, Pillow, Docker, pytest

## Cible 2 — GPU NVIDIA Jetson Nano (yoloGK-jetson-serving-api)
GitHub : https://github.com/chabanenary/yoloGK-jetson-serving-api
- Même application FastAPI, adaptée au Jetson Nano
- Inférence accélérée par GPU via ONNX Runtime avec CUDA / TensorRT
- Basée sur l'image Docker NVIDIA L4T (Linux for Tegra), conteneur avec runtime nvidia
- Détection automatique du GPU : CUDA si disponible, repli sur CPU sinon
- Optimisée pour un matériel contraint (4 Go de RAM, GPU Maxwell), avec profiling des FPS sous contraintes thermiques

## Cible 3 — Kubernetes et OpenShift sur AWS (yoloGK-kubernetes-serving-api)
GitHub : https://github.com/chabanenary/yoloGK-kubernetes-serving-api
- Kubernetes et OpenShift déployés sur un serveur AWS
- Manifests organisés avec kustomize : Deployment avec réplicas, HPA (autoscaling horizontal), sondes liveness / readiness, limites de ressources
- NetworkPolicy, volumes persistants (PV / PVC), Service ClusterIP
- Accès externe par ingress Kubernetes et route OpenShift

## Endpoints API (communs à tous les déploiements)
- GET /health — sonde de vie, rapporte le statut du modèle
- GET /device — disponibilité GPU / CUDA et provider d'inférence actif
- POST /classify — classifie une image (upload + seuil de confiance)
- POST /classify/batch — classifie plusieurs images en une requête, avec résultats par image et résumé

## Ce que cela prouve
Narymane sait prendre un modèle ML qu'elle a entraîné et le déployer sur tout le spectre des environnements : développement local (CPU), appareil edge avec GPU (Jetson Nano) et orchestration cloud (Kubernetes / OpenShift sur AWS), avec une architecture 3 tiers complète. C'est l'ensemble de compétences attendu d'une ingénieure déploiement ML ou MLOps.
