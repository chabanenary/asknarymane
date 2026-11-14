# Expérience professionnelle — Narymane Chabane

Parcours professionnel de Narymane, dans l'ordre chronologique :
- STMicroelectronics, Paris — stage ingénieure de fin d'études (juillet à décembre 2006)
- OneAccess / Ekinops, Paris — une seule expérience continue de 13 ans (mai 2007 à mars 2020), dont 2007-2011 en prestation via l'ESN Eolices, puis salariée de OneAccess, rachetée par Ekinops en 2017
- Pause parentale et reconversion autodidacte vers l'IA (2020 à 2024)
- Projets IA et développement Android en indépendante (septembre 2024 à mai 2026)
- Mission freelance en IA embarquée multimodale pour une start-up (depuis juin 2026, en cours)

## OneAccess / Ekinops (mai 2007 – mars 2020) — vue d'ensemble
- Postes : ingénieure R&D systèmes embarqués, puis ingénieure Linux embarqué senior
- Une seule expérience continue sur le même site et les mêmes produits. Eolices n'est pas une expérience séparée : de 2007 à 2011, Narymane travaillait chez OneAccess en tant que prestataire de l'ESN Eolices, puis elle a été embauchée par OneAccess, où elle est restée salariée jusqu'en mars 2020
- OneAccess Networks, fabricant français d'équipements réseau, a été rachetée par Ekinops en 2017 (rachat finalisé en octobre 2017) ; Narymane a donc travaillé environ deux ans et demi chez OneAccess au sein du groupe Ekinops
- Produits : logiciels de production pour des équipements réseau de grade opérateur — routeurs physiques et virtuels, passerelles, répéteurs Wi-Fi / 4G, modules SFP — déployés par milliers chez des opérateurs télécom (dont Orange, SFR et Telefonica), sous Linux et VxWorks
- Équipe R&D pluridisciplinaire, processus qualité CMMI niveau 3
- Périmètre : des bootloaders et drivers jusqu'aux couches système et applicatives — jamais « uniquement du firmware »

## Responsable du composant bootloader de toute l'entreprise (2007–2020)
- Propriétaire des bootloaders (U-Boot et loaders VxWorks) pour l'ensemble des gammes OneAccess / Ekinops pendant 13 ans
- Une dizaine de cartes différentes au fil des évolutions des technologies télécom et des processeurs : du MIPS mono-cœur aux QorIQ multiprocesseurs et au x86
- Portage sur chaque nouvelle plateforme, mise à jour firmware, secure boot, validation, support des équipes produit
- Programmation initiale des cartes (bootloaders et images OS) via JTAG

## Lead technique et gestion de projets
- Lead technique d'une équipe de 4 ingénieurs (internes et offshore) sur le développement et les tests, de 2009 à 2012 : affectation et suivi des tâches, revues de code, arbitrages techniques
- Conduite de projets du cahier des charges à la recette, avec chiffrage et planification — par exemple l'outil de chargement dynamique de firmwares xDSL
- Pilotage de la maintenance confiée à une équipe offshore de 3 personnes (2011-2013) : mises à jour de drivers, patchs de bootloaders, maintenance corrective et évolutive

## Boucle qualité de bout en bout sur l'OS complet
- Développement de drivers bas niveau et de bibliothèques système et applicatives
- Fourniture des tests fonctionnels de ses composants ; participation à la spécification des tests d'intégration et des tests fonctionnels
- Suivi de la non-régression de l'OS entier
- Pilotage de la boucle défauts : fiches d'anomalie (trouble reports) créées automatiquement à partir des échecs de tests, correction suivie, tests réintégrés en non-régression
- Rédaction de spécifications fonctionnelles, documents d'architecture, plans de test et matrices de conformité (CMMI niveau 3)

## Routeurs virtuels sur x86 (2019–2020)
- Développement de l'OS du routeur virtuel : une solution de routage complète tournant comme une distribution Linux Debian dans une machine virtuelle x86
- Couches système : journalisation, monitoring, gestion mémoire ; daemons userspace et services systemd
- Couches applicatives : CLI, framework de gestion des licences logicielles (spécification, conception et implémentation complètes)
- Monitoring système réalisé de bout en bout : spécification du besoin, choix des fonctions à surveiller et des mesures pertinentes, conception, codage, tests, intégration, et évaluation de l'intégration dans tout l'OS
- CI/CD avec Jenkins : builds et tests d'intégration automatisés, génération d'images prêtes pour la production
- Langages : C et Python

## Routeurs Gigabit VoIP (2014–2017) — Freescale T1040, Yocto Linux
- Drivers Ethernet, switch SFP, mémoire, LEDs et alimentation
- Spécifications, plans de test, matrices de conformité, suivi d'intégration
- Système de build Yocto : couches BSP, recettes BitBake, chaînes de cross-compilation, génération d'images de production
- Scripts Shell et Perl

## Routeurs Ethernet/IP Gigabit (2011–2013) — Freescale P1021, VxWorks
- Bootloader bi-cœur sur le processeur Freescale P1021
- Conception et implémentation d'un système de défense logicielle et de crash logs : extraction de la pile d'exception en assembleur PowerPC, formatage des données d'exception pour le crash log
- Tâche de supervision sur le cœur 0 qui détecte et rapporte les plantages du cœur 1, avec intégration du core dump du cœur 1 dans le crash log
- Suivi des drivers Wi-Fi, switch et fibre
- Modélisation UML

## Routeurs xDSL hautes performances (2007–2011) — MIPS, PowerPC 83xx, VxWorks
- Drivers xDSL, ATM, série et cartes mémoire, bootloaders sur processeurs MIPS et PowerPC
- QoS ATM : mesure et optimisation des performances sur des CPE xDSL — réglage du GCRA (Generic Cell Rate Algorithm), optimisation de la couche SAR pour la fragmentation AAL5, allocation des buffers par classe de service (CBR, VBR, ABR), ordonnancement des tâches pour un scheduling cellulaire précis sous charge
- Corrélation des métriques côté CPE (drops, pression mémoire, CPU) avec les mesures QoS côté réseau pour isoler les dégradations d'origine logicielle
- Interopérabilité avec les DSLAM Alcatel

## Outil de chargement dynamique de firmwares xDSL (2007–2011)
- Cheffe de projet de l'outil de chargement automatique de firmwares pour les cartes xDSL
- Rédaction du cahier des charges, de la spécification de besoin, du design logiciel et du plan de tests avant l'implémentation — un exemple concret d'ingénierie « documentation d'abord »
- Développement de la commande CLI de chargement dynamique et des outils de production pour le packaging des firmwares
- Suivi de l'équipe offshore, conformité, évolutions et maintenance

## Autres réalisations sous VxWorks (2007–2013)
- Optimisation de l'algorithme d'écriture NAND Flash pour la programmation des cartes : meilleure allocation de blocs, moins de cycles d'effacement inutiles, débit d'écriture séquentielle amélioré — réduction significative du temps de programmation en production
- Adaptation des BSP aux nouvelles révisions matérielles
- Débogage matériel avec Lauterbach Trace32, BDI2000, CodeWarrior, WindRiver Power ICE

## Linux embarqué — compétences transversales (2007–2020)
- Yocto / OpenEmbedded, Debian
- Kernel : configuration, patchs, device tree ; drivers en kernel-space et en user-space
- U-Boot : portage et personnalisation pour plusieurs révisions de cartes
- Bring-up de nouvelles plateformes de bout en bout, de la programmation JTAG à la validation système ; développement BSP
- Mise à jour firmware, secure boot, CI/CD, revues de code, estimation de charges, coordination offshore
- Rédaction de guides utilisateur pour les outils de flashage, les utilitaires de programmation firmware et les procédures de débogage

## Évolutions produit et support client
- Traitement des demandes d'évolution produit sur les aspects système, avec le support client des opérateurs (Orange, SFR, Telefonica)
- Aide à la rédaction des documents PRQ (Product Requirement)
- Évaluation des charges de développement, d'intégration et de tests ; suivi du développement et de l'intégration des évolutions

## Environnement technique chez OneAccess / Ekinops
C, C++, Python, Bash, Perl, Linux (Yocto, Debian), VxWorks, U-Boot, TCP/IP, UML/SDL, Git, SVN, Mercurial, Jenkins, Jira, Bugzilla.

## Stage — STMicroelectronics, Paris (juillet – décembre 2006)
- Stage ingénieure de fin d'études du master Télécom Paris (6 mois)
- Développement d'un outil d'évaluation (Perl/Tk) d'une base de données de milliers de blocs de propriété intellectuelle (IP) destinés à des chipsets mobiles 3G
- Recherche et définition des critères d'une IP non corrompue, bien conçue et sans défaut de fabrication ; implémentation de ces critères en vérifications automatiques ; production de rapports d'évaluation
- Interface graphique en Perl/Tk, méthodes d'extraction en scripts Shell et Perl, rédaction du guide utilisateur
- Première expérience de la démarche qui la caractérise : définir les critères de qualité, les coder, les appliquer à grande échelle, rapporter
