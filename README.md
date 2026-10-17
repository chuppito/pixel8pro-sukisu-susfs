# Pixel 8 Pro — SukiSU Ultra + SUSFS

Projet de recherche et de compilation **expérimental** pour Google Pixel 8 Pro (**husky**).

## Appareil cible
- Modèle : Pixel 8 Pro (husky), **pas** Pixel 8 (shiba)
- Android : 17
- Build : `CP3A.261005.005`
- Noyau observé : `6.1.162-android14-11-g9dd05a3a1de-ab16261587`
- KMI : `android14-6.1`
- Root actuellement fonctionnel : SukiSU Ultra en LKM (init_boot patché)
- Image boot actuellement utilisée : boot Google officiel
- SUSFS : **absent du noyau actuel** ; module userspace SUSFS désactivé

## État

**Aucune image de noyau compilée ou validée. Ne rien flasher depuis ce dépôt pour le moment.**

La correspondance KMI ne suffit pas à prouver la compatibilité avec un firmware Pixel donné. Avant compilation et publication :
1. Identifier la révision exacte des sources du noyau et les artefacts de référence du build Google.
2. Vérifier les patchs SukiSU Ultra et SUSFS, leur provenance, leur licence et leurs versions.
3. Valider la configuration et les ABI/KMI, puis compiler.
4. Vérifier les artefacts générés (type, taille, hachages, métadonnées) et documenter le retour arrière.
5. Ne proposer de flash qu'après vérification de compatibilité **husky / CP3A.261005.005**.

Ne jamais flasher un boot d'un autre appareil, un noyau générique non vérifié, ni reverrouiller le bootloader avec des partitions modifiées.

## Note Play Integrity

SUSFS n'assure ni DEVICE_INTEGRITY ni STRONG_INTEGRITY ; les verdicts sont déterminés par Google et peuvent dépendre de l'état de l'appareil et des clés d'attestation.
