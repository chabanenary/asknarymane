# Projet — IA / GalleryKeeper App (application Android avec IA embarquée, 2024–2026)

## Présentation
GalleryKeeper est une application Android open source qui détecte et trie les photos sensibles de la galerie — documents d'identité, cartes bancaires, photos d'enfants, nudité — entièrement sur l'appareil, sans aucun envoi vers un serveur. Elle est publiée sur le Play Store et compte plus de 1 000 téléchargements. Narymane l'a démarrée en 2024, sans assistance d'IA générative.

- GitHub : https://github.com/chabanenary/GalleryKeeper-App
- Article technique : https://dev.to/chabanenary/my-first-android-app-as-a-beginner-what-i-learned-building-an-offline-ml-gallery-organizer-and-3d1k
- Démo (anglais) : https://www.youtube.com/watch?v=jnUaWvC-wpw
- Démo (français) : https://www.youtube.com/watch?v=V_BQd_TGrLw

## Fonctionnalités
- Détecte automatiquement l'apparition de nouvelles photos dans la galerie, grâce à un service de premier plan qui tourne en arrière-plan
- Classifie les photos sensibles par IA dans 4 catégories : nudité, enfants, documents d'identité (cartes d'identité, passeports), cartes bancaires
- Organise les images en les déplaçant dans des dossiers selon des règles définies par l'utilisateur
- Suggère des suppressions (doublons, images inutiles)
- Toute action destructive (déplacement, suppression) est soumise à la confirmation de l'utilisateur

## Vie privée et fonctionnement hors ligne
- Fonctionne entièrement hors ligne : aucune connexion internet requise pour l'analyse
- Aucune photo n'est jamais envoyée vers un serveur ni copiée dans le stockage de l'application
- Les médias sont traités sur l'appareil via l'API Android MediaStore
- Android affiche des écrans de confirmation pour toute modification ou suppression : l'utilisateur garde le contrôle

## Architecture de l'application
- Java : environ 29 classes, environ 5 100 lignes
- Architecture MVVM, base de données Room, API MediaStore, permissions à l'exécution
- Service de premier plan qui surveille les nouvelles photos
- Inférence avec LiteRT (TensorFlow Lite) et délégué GPU
- Firebase Auth et Firebase Analytics
- minSdk 24, targetSdk 35
- 53 tests unitaires

## Modèle de vision
- YOLO11n : 2,6 millions de paramètres, entrée 640×640, 5 classes
- Entraîné de zéro sur Google Colab (GPU T4), sur un dataset collecté et annoté par Narymane (1 400 images au départ)
- Exporté en TFLite float32 (10,2 Mo) pour l'inférence sur l'appareil
- Le même modèle est servi sur CPU, Jetson Nano et Kubernetes par le projet YoloGK

## Cycle d'évaluation du modèle (novembre 2026) — audit
À partir de retours d'utilisateurs, Narymane a d'abord audité l'évaluation avant de toucher au modèle. Constats :
- 79 des 429 images de validation figuraient aussi dans l'entraînement, ce qui surestimait le score
- Un bug du script de ré-étiquetage décalait des boîtes jusqu'à 30 % de la largeur de l'image : 198 annotations corrigées
- Un dossier entier de la classe la plus difficile n'avait jamais atteint l'entraînement : 117 boîtes vues au lieu de 630 disponibles
- 73 images « sans annotation » contenaient en fait des objets

## Cycle d'évaluation du modèle (novembre 2026) — nouveau dataset et ré-entraînement
- Dataset reconstruit : de 2 530 à 6 712 images d'entraînement, à partir de six sources — Open Images, images synthétiques (perspective, rotation, reflets, ombres, flou), photos annotées dans Label Studio après pré-annotation par l'ancien modèle, fonds vides
- Dédoublonnage par empreinte d'image pour qu'aucune photo ne soit à la fois en entraînement et en validation, et manifeste de provenance pour chaque image
- Nouvel entraînement : 126 epochs, 4 h 20 sur Colab gratuit
- Résultat sur la même validation de 652 photos : mAP50 passé de 0,657 à 0,746, avec la plus forte progression sur les classes les plus faibles

## Cycle d'évaluation (novembre 2026) — diagnostic côté application
- Reproduction hors ligne de toute la chaîne de décision de l'application (détecteur, sélection de boîte, classification, seuils) sur les 652 photos de validation
- Découverte : la majorité des documents « ratés » étaient détectés à plus de 90 %, puis rejetés parce que leur boîte dépassait du bord de l'image, même de 1 % (27 cas sur 30)
- Correction : une classe de géométrie qui ramène les boîtes dans le cadre, et 6 tests unitaires ajoutés
- Résultat : documents d'identité et cartes bancaires correctement classés à 98 %, contre 81-83 % auparavant, avec une baisse de précision mesurée et assumée (de 97 % à 88 %) sur un dossier
- Vérification de parité : le modèle TFLite prend exactement les mêmes décisions que le modèle PyTorch sur chaque image de validation ; amélioration confirmée sur appareil

## Limites documentées et prochaines étapes
- Les seuils ont été ajustés sur la validation qui les mesure, donc les scores sont optimistes
- La classe la plus faible reste sous-représentée
- Prochaines étapes : ciblage d'Android 16, enrichissement des données de la classe faible, version float16 du modèle

## Pourquoi ce projet est significatif
GalleryKeeper est la première application Android de Narymane, construite entièrement en autodidacte : elle n'avait aucune expérience préalable en Java ni en Android. Le projet couvre tout le cycle — collecte et annotation de données, entraînement, évaluation, déploiement mobile, publication sur le Play Store, puis amélioration à partir des retours utilisateurs — et montre sa rigueur : auditer l'évaluation avant de modifier le modèle, mesurer chaque compromis, vérifier la parité entre formats.
