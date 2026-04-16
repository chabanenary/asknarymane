# Projet — IA / GalleryKeeper App

## Présentation
GalleryKeeper est une application Android open source qui détecte, classifie et organise les photos sensibles (« délicates ») dans la galerie de l'utilisateur. Elle utilise un modèle IA YOLO11 entraîné sur mesure, fonctionnant entièrement sur l'appareil — aucune connexion internet requise, aucune photo n'est jamais envoyée vers le cloud.

GitHub : https://github.com/chabanenary/GalleryKeeper-App
Article de blog : https://dev.to/chabanenary/my-first-android-app-as-a-beginner-what-i-learned-building-an-offline-ml-gallery-organizer-and-3d1k
Démo (anglais) : https://www.youtube.com/watch?v=jnUaWvC-wpw
Démo (français) : https://www.youtube.com/watch?v=V_BQd_TGrLw

## Fonctionnalités
- Détecte automatiquement l'apparition de nouvelles photos dans la galerie
- Classifie les photos « délicates » par IA dans 4 catégories : photos de nudité, photos d'enfants, documents d'identité (cartes d'identité, passeports), photos de cartes bancaires
- Organise les images en les déplaçant dans des dossiers selon des règles définies par l'utilisateur
- Suggère des suppressions (doublons, images inutiles) après confirmation de l'utilisateur
- Mode surveillance : continue de fonctionner en arrière-plan via un service de notification Android

## Vie privée & Fonctionnement hors ligne
- Fonctionne entièrement hors ligne — aucune connexion internet requise
- Aucune photo n'est jamais sauvegardée par l'application — ni dans le stockage de l'app, ni dans le cloud
- Traite les médias sur l'appareil via les API Android (MediaStore)
- Android affiche des écrans de confirmation pour toute modification/suppression — l'utilisateur garde le contrôle

## Architecture technique
- Langage : Java (100%)
- Architecture : MVVM (Model-View-ViewModel)
- Base de données : Room (SQLite)
- Modèle IA : YOLO11 entraîné sur mesure, exporté en TFLite pour l'inférence on-device
- Service en arrière-plan : service de premier plan Android avec notification
- Accès aux médias : API MediaStore
- SDK minimum : 24, SDK cible : 35

## Pipeline ML (entièrement réalisé par Narymane)
- Curation et annotation du dataset
- Entraînement du modèle avec Ultralytics YOLO11
- Évaluation et analyse des performances du modèle
- Quantization pour le déploiement mobile
- Export au format TFLite
- Intégration dans l'application Android pour l'inférence en temps réel

## Pourquoi ce projet est significatif
C'était la première application Android de Narymane, construite entièrement en autodidacte. Elle n'avait aucune expérience préalable en Java ni en Android — tout a été appris par la documentation, l'expérimentation et la persévérance. Le projet démontre sa capacité à acquérir rapidement de nouvelles compétences et à livrer un produit complet et abouti.

Le projet combine plusieurs disciplines : développement mobile (Java/Android), machine learning (pipeline d'entraînement YOLO), inférence on-device (TFLite), et conception d'architecture orientée respect de la vie privée.
