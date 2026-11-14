# Expérience IoT & IA Edge

## Les systèmes embarqués comme fondation IoT
Toute la carrière de Narymane s'est construite autour de ce que l'on appelle aujourd'hui l'infrastructure IoT et edge : développer le logiciel qui tourne sur des équipements réseau déployés par milliers en bordure des réseaux télécom (13 ans chez OneAccess / Ekinops), puis, depuis juin 2026, le logiciel et l'IA d'un appareil conversationnel embarqué sur NVIDIA Jetson Orin Nano.

## Expérience matérielle
- Processeurs NXP/Freescale PowerPC et QorIQ (P1021, T1040, PowerPC 83xx), MIPS, ARM, x86 embarqué et virtualisé
- Équipements avec interfaces Ethernet, Wi-Fi, 4G/LTE, xDSL, SFP optique
- NVIDIA Jetson Nano et Jetson Orin Nano pour l'inférence edge accélérée par GPU
- À l'aise avec la lecture de schémas électriques et de datasheets pour écrire des drivers
- Board bring-up de bout en bout : de la programmation JTAG à la validation système
- Intégration de périphériques sur Jetson : caméra, micro array, écran tactile, audio Bluetooth

## Systèmes d'exploitation
- Linux : Debian, Ubuntu, Yocto/OpenEmbedded (configuration noyau, patchs, device tree, images custom), JetPack 6 / L4T
- VxWorks RTOS : multitâche temps réel, gestion des interruptions, IPC
- U-Boot, mécanismes de mise à jour firmware, secure boot
- systemd, udev, NetworkManager, séquences d'initialisation pour environnements de boot contraints

## Réseaux & Protocoles
- Expérience approfondie : TCP/IP, xDSL (ADSL/VDSL), ATM/QoS, commutation Ethernet, Wi-Fi, 4G/LTE
- DHCP, DNS, HTTP/REST, RTSP, SIP, Socket.IO / WebSocket
- Connaissance de MQTT
- Équipements multi-services gérant simultanément données, voix et vidéo

## IA Edge (depuis 2024)
- Entraînement de modèles YOLO avec Ultralytics / PyTorch
- Chaîne d'optimisation de modèles : PyTorch → ONNX → TensorRT (Jetson), TFLite / LiteRT (Android), llama.cpp et quantization 4 bits (Jetson Orin Nano)
- Pipelines vidéo temps réel : GStreamer, RTSP, OpenCV
- Déploiement sous contraintes strictes de mémoire, de GPU, de température et de consommation
- Inférence on-device sur Android avec TFLite / LiteRT et délégué GPU
- Voix et vision temps réel sur Jetson Orin Nano, avec moins d'une seconde de latence

## Connaissances IoT
Narymane possède des bases solides pour l'IoT grâce à sa carrière en systèmes embarqués :
- Intégration matériel-logiciel à tous les niveaux
- Contraintes temps réel et comportement déterministe
- Environnements à ressources limitées (CPU, RAM, énergie)
- Protocoles de communication (REST, WebSocket, série ; connaissance de MQTT)
- Provisioning d'appareils grand public : Wi-Fi par point d'accès temporaire, QR code, portail captif
- Monitoring embarqué et tests d'endurance
- Déploiement conteneurisé sur matériel edge (Docker sur Jetson Nano)

Ses 13 ans d'expérience en systèmes embarqués et sa mission actuelle sur un appareil connecté signifient qu'elle maîtrise les défis fondamentaux de l'IoT : matériel contraint, logiciel fiable, communications et gestion d'équipements à distance. Elle apprend très rapidement les technologies spécifiques (MQTT, packaging Snap, Ubuntu Core), parce que les principes sous-jacents sont ceux qu'elle applique depuis le début de sa carrière.
