# Expérience professionnelle — Narymane Chabane

Narymane a travaillé dans les entreprises suivantes : Ekinops / OneAccess (2007–2020), Eolices / Société de services (2007–2011), STMicroelectronics (2006–2007, stage).

## Entreprise principale : Ekinops / OneAccess (2007–2020)
Ekinops (anciennement OneAccess Networks) est un fabricant français d'équipements télécom, produisant des routeurs CPE de grade entreprise et opérateur, des passerelles résidentielles, des répéteurs Wi-Fi/4G, et des équipements réseau à base de SFP. Les produits sont déployés par des opérateurs télécom de premier plan : Orange, SFR, et Telefonica, servant des dizaines de milliers de clients.

## Poste
Ingénieure R&D Systèmes Embarqués — Ingénieure Linux embarqué senior au sein d'une équipe R&D pluridisciplinaire.

## Projets VxWorks RTOS (2007–2012)

### Développement et maintenance de drivers
- Développement et maintenance de drivers bas niveau sur VxWorks RTOS : NAND Flash, interfaces mémoire, connexions série, drivers ATM/xDSL
- Mesure et optimisation des performances QoS ATM (Qualité de Service) sur des plateformes CPE xDSL
- Réglage de l'implémentation logicielle du GCRA (Generic Cell Rate Algorithm)
- Optimisation de la couche SAR (Segmentation and Reassembly) pour réduire l'overhead lors de la fragmentation AAL5
- Ajustement de l'allocation de buffers par classe de service pour équilibrer le Cell Transfer Delay et le Cell Delay Variation entre les catégories CBR, VBR et ABR
- Optimisation de l'ordonnancement des tâches au niveau OS pour un scheduling cellulaire précis sous charge
- Corrélation des métriques côté CPE (drops en sortie, pression mémoire, utilisation CPU) avec les mesures QoS côté réseau pour isoler les dégradations d'origine logicielle

### Boot loaders et Board Bring-Up
- Développement et maintenance des boot loaders sur processeurs Freescale (MIPS, PowerPC)
- Responsable de la programmation initiale des cartes avec bootloaders et images OS via JTAG
- Utilisation de débogueurs matériels : Lauterbach Trace32, BDI2000, CodeWarrior, WindRiver Power ICE
- Adaptation des BSP pour les nouvelles révisions matérielles

### Système de défense logicielle / Crash logging
- Conception et implémentation d'un système de défense logicielle sur un processeur bi-cœur Freescale P1021
- Extraction de la pile d'exception en langage assembleur PowerPC
- Formatage des données d'exception pour exploitation dans le crash log
- Implémentation d'une tâche de supervision sur le cœur 0 pour détecter et rapporter les plantages du cœur 1
- Intégration des données de core dump du cœur 1 dans le crash log
- Nécessitait une compréhension approfondie de l'architecture processeur, de la gestion des interruptions et du layout mémoire

### Moteur de chargement de firmware
- Direction du développement d'un moteur de chargement automatique de firmware pour cartes réseau (cartes xDSL)
- Rédaction complète de la spécification de besoin, du design logiciel et du plan de tests avant l'implémentation
- Développement de la commande CLI pour le chargement dynamique de firmware
- Développement des outils de production pour le packaging de firmware embarqué
- Gestion des évolutions et de la maintenance
- Ce projet est un exemple concret d'ingénierie logicielle « documentation d'abord »

### Optimisation de l'écriture NAND Flash
- Optimisation de l'algorithme d'écriture sur NAND Flash pour la programmation des cartes
- Amélioration de l'allocation de blocs, minimisation des cycles d'effacement inutiles, amélioration du débit d'écriture séquentielle
- Réduction significative du temps de programmation — critique pour l'efficacité de la ligne de production quand des milliers de cartes passent en fabrication

### Coordination d'équipe
- Coordination de sous-traitants offshore (3 personnes) pour les mises à jour de drivers, les patchs de bootloaders et le développement de fonctionnalités
- Gestion des cycles de maintenance corrective et évolutive

## Projets Linux embarqué (2013–2016)

### Stack Linux embarqué complète
- Portage et personnalisation du bootloader U-Boot pour plusieurs révisions de cartes
- Configuration et patching du noyau, gestion du device tree
- Développement de drivers matériels en kernel-space et user-space :
  - Contrôleurs Ethernet, transceivers optiques SFP
  - Chipsets Wi-Fi, modems 4G/LTE
  - Interfaces mémoire NAND Flash
  - LEDs, timers watchdog, circuits de gestion d'alimentation
- Board bring-up de nouvelles plateformes de bout en bout — de la programmation JTAG à la validation système complète

### Système de build Yocto
- Maintenance d'environnements de build Yocto
- Gestion des couches BSP, recettes BitBake, chaînes de cross-compilation
- Génération d'images de production pour plateformes ARM (Freescale/NXP QorIQ) et x86

### Processus d'ingénierie
- Rédaction de spécifications fonctionnelles, documents d'architecture et plans de tests (CMMI Niveau 3)
- Revues de code et intégration gérées via un dépôt Git interne partagé
- Rédaction de guides utilisateur pour les outils de flashage, utilitaires de programmation firmware et procédures de débogage

## Projet Virtual CPE (2017–2020)

### Routeur virtuel sur VM Linux
- Développement d'un routeur virtuel — une solution de routage complète tournant comme une distribution Linux Debian dans une machine virtuelle
- Intégration de composants système en C : daemons userspace, gestion de services systemd
- Spécification, conception et implémentation complète d'un framework de gestion de licences logicielles
- CI/CD avec Jenkins : builds et tests d'intégration automatisés, compilation multi-cibles, génération d'images prêtes pour la production

### Feature Requests et support client
- Traitement des besoins d'évolution produit sur les aspects système avec le support client (Orange, SFR, Telefonica)
- Aide à la rédaction des documents PRQ (Product Requirement)
- Évaluation des charges en développement, intégration et tests
- Gestion du suivi de développement ou d'intégration des évolutions

## Expériences antérieures

### Eolices / Société de services (2007–2011)
- Développement de composants système bas niveau et de drivers matériels pour des routeurs xDSL/Wi-Fi sous VxWorks
- Contribution à l'intégration firmware, l'adaptation BSP et la validation pour des équipements CPE télécom

### STMicroelectronics (2006–2007)
- Stage de 6 mois dans le cadre du Master à Télécom Paris
- Conception et développement d'un outil d'évaluation de la qualité des IPs (Intellectual Properties) avant leur intégration dans des ASICs de bande passante 3G
- Développement de l'interface graphique en Perl/Tk
- Développement des méthodes d'extraction en scripts Shell et Perl
- Rédaction du Guide Utilisateur
