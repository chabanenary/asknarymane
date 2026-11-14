# IA embarquée multimodale — Mission freelance en cours (depuis juin 2026)

## Contexte de la mission
- Client : une start-up (nom confidentiel). Contrat freelance, full remote
- Début le 1er juin 2026 ; mission toujours en cours en novembre 2026, en phase d'intégration d'un nouveau matériel et de préparation du prototype final
- Produit : un produit conversationnel multimodal temps réel — l'appareil écoute, voit et répond à la voix en moins d'une seconde
- Plateforme : ordinateur embarqué NVIDIA Jetson Orin Nano de 8 Go, avec de fortes contraintes de mémoire, de latence et de température, et une conception privacy by design
- Les noms du client, du produit et des modèles d'IA utilisés sont confidentiels

## Rôle de Narymane sur la mission
- Responsable du logiciel embarqué et de l'IA côté appareil, du POC au prototype produit
- Travaille en binôme avec le développeur cloud du client, qui gère le serveur IA cloud et l'avatar 3D du frontend ; elle n'est pas la seule développeuse du produit
- Son rôle est logiciel : IA, intégration, validation, et conseil sur le choix des composants matériels (elle ne fait ni câblage ni assemblage)

## Architecture hybride edge / cloud
- Perception (voix et vision) traitée localement sur le Jetson
- Raisonnement délégué à un LLM cloud, en streaming
- Seul du texte anonymisé quitte l'appareil, jamais d'image ni d'audio brut

## Audio temps réel
- Pipeline full-duplex avec détection d'activité vocale (modèle ONNX)
- Reconnaissance vocale open source exécutée sur le GPU local, analyse de prosodie
- Synthèse vocale locale et synthèse vocale cloud en streaming, lecture à faible latence
- Interruption naturelle de l'appareil par l'utilisateur (barge-in)
- Annulation d'écho logicielle (PipeWire, WebRTC), puis matérielle avec un micro array : 7 configurations évaluées, 0 faux déclenchement sur la configuration retenue

## Bluetooth et audio système
- Intégration et tests de casques audio Bluetooth (A2DP via BlueZ / PipeWire / WirePlumber)
- Appairage, reconnexion, latence, coexistence avec le micro array

## Vision embarquée
- Flux caméra analysé en tâche de fond, sans bloquer la conversation
- Modèle vision-langage de 2 milliards de paramètres, quantifié
- Benchmark de plusieurs modèles de cette taille, quantization 4 bits
- Migration de PyTorch vers llama.cpp, libérant 1,5 à 2,5 Go de mémoire

## Orchestration et intégration
- Orchestrateur Python asyncio (et threads) qui route la perception vers l'appareil et le raisonnement vers le LLM cloud
- Streaming phrase par phrase, cache de contexte
- Gestion du cycle de vie des sessions : démarrage, inactivité, quota
- Passerelle Socket.IO vers le backend du client et vers une interface React / Three.js (avatar 3D synchronisé sur la voix)
- Respect du budget de coût cloud fixé pour le produit
- Exploration d'un codec audio neuronal : latence de fin de tour réduite de 3,7 s à 1,5 s

## Système embarqué
- JetPack 6 / L4T, CUDA, boot sur NVMe
- systemd, udev, provisioning reproductible, étude de conteneurisation
- Provisioning Wi-Fi grand public : point d'accès temporaire, QR code, portail captif, NetworkManager

## Observabilité et fiabilité
- Monitoring embarqué (mémoire, GPU, températures, latences) exposé par une API JSON et un tableau de bord web
- Diagnostic et correction d'une saturation mémoire de 5,3 Go sur 8 Go
- Dégradation gracieuse sous contrainte thermique et mémoire

## Résultats mesurés
- Test d'endurance de 30 minutes : 75 tours de conversation, 0 crash, 39 interruptions, 0 faux positif, température inférieure à 65 °C
- Test d'endurance de 2 heures : 263 tours, 0 crash, pas de fuite mémoire
- Latence de traitement inférieure à 1 seconde
- POC validé en trois mois

## Conseil matériel et livrables
- Analyse du cahier des charges
- Sélection et validation de la caméra, du micro array, de l'écran tactile 7 pouces et de l'audio Bluetooth
- Chiffrages, rapports techniques, synthèses comparatives, documentation d'exploitation

## Environnement technique de la mission
Python (asyncio), C, llama.cpp, ONNX Runtime, CUDA, TensorRT, PipeWire, BlueZ, NetworkManager, Socket.IO, React / Three.js, JetPack 6, systemd.
