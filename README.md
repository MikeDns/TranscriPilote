<div align="center">

<img src="assets/icon.svg" alt="" width="96">

# TranscriPilote

**Transcription, résumé et analyse de vos réunions, 100 % sur votre PC.**
Aucun cloud, aucun abonnement, aucune donnée envoyée à un tiers.

[![Dernière version](https://img.shields.io/github/v/release/MikeDns/TranscriPilote?label=version&color=7c6cf0)](https://github.com/MikeDns/TranscriPilote/releases/latest)
[![Téléchargements](https://img.shields.io/github/downloads/MikeDns/TranscriPilote/total?label=t%C3%A9l%C3%A9chargements&color=4f46e5)](https://github.com/MikeDns/TranscriPilote/releases)
![Windows 10/11](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6)
![Hors ligne](https://img.shields.io/badge/fonctionne-hors%20ligne-3ddc84)
![Gratuit](https://img.shields.io/badge/gratuit-oui-7c6cf0)

### [Télécharger TranscriPilote](https://mikedns.github.io/TranscriPilote/telecharger.html)

**Site officiel : [mikedns.github.io/TranscriPilote](https://mikedns.github.io/TranscriPilote/)**

[Signaler un problème](https://github.com/MikeDns/TranscriPilote/issues/new?template=bug_report.yml) ·
[Proposer une idée](https://github.com/MikeDns/TranscriPilote/issues/new?template=feature_request.yml) ·
[Nouveautés](https://mikedns.github.io/TranscriPilote/nouveautes.html)

</div>

---

## Pourquoi TranscriPilote ?

Les outils de transcription en ligne envoient vos réunions sur des serveurs tiers.
TranscriPilote fait tout sur votre ordinateur, même un PC de bureau ordinaire **sans carte graphique**
et **sans droits administrateur** : idéal pour un poste professionnel ou des échanges confidentiels.

## Fonctionnalités

| | |
|---|---|
| **Enregistrement** | Vos réunions en salle et en ligne (Teams, Zoom, Meet…), en un clic |
| **Transcription** | Texte horodaté, en français ou en anglais, plusieurs niveaux de précision |
| **Qui a dit quoi** *(bêta)* | Chaque intervenant est repéré dans la transcription |
| **Résumés** | Résumé, points clés et actions à faire, rédigés par une IA installée sur votre PC |
| **Discussion** | Posez vos questions à une réunion (« qui a validé le budget ? ») |
| **Import** | Fichiers audio et vidéo : MP3, M4A, WAV, MP4, MKV, MOV… |
| **Historique** | Toutes vos réunions, avec recherche dans ce qui a été dit |
| **Exports** | Markdown, Excel, texte et sous-titres |
| **Sauvegarde** | Facultative, vers **votre** Google Drive ou OneDrive |
| **Mises à jour** | Proposées dans l'application, installées quand vous le décidez, retour arrière possible |

## Installation

**Configuration requise :** Windows 10 ou 11 (64 bits), 16 Go de RAM recommandés (8 Go minimum),
environ 10 Go d'espace disque. Pour les résumés et la discussion, installez aussi
[Ollama](https://ollama.com/download), gratuit : TranscriPilote le configure tout seul.

1. Téléchargez l'installateur depuis la [page de téléchargement](https://mikedns.github.io/TranscriPilote/telecharger.html).
2. Lancez-le : l'installation se fait dans votre profil Windows, sans droits administrateur.
3. Au premier lancement, TranscriPilote se prépare : quelques minutes, une seule fois.
   Une visite guidée facultative vous présente ensuite chaque fonction.

> Windows peut afficher « Windows a protégé votre ordinateur » : cliquez sur
> **Informations complémentaires → Exécuter quand même**. Chaque version est publiée avec
> `SHA256SUMS.txt` pour vérifier que le fichier n'a pas été modifié.

**Qui a dit quoi (bêta) :** activez-le dans **Réglages → Identifier qui parle**, qui vous guide pas à pas.

## Confidentialité

Vos réunions, transcriptions, résumés et réglages restent sur votre PC, dans `%LOCALAPPDATA%\TranscriPilote\`.
TranscriPilote se connecte à internet uniquement pour se préparer, vérifier les mises à jour
et sauvegarder vers votre cloud **si vous l'activez**.

**Désinstaller :** Paramètres Windows → Applications → TranscriPilote. La désinstallation liste ce qu'elle
supprime et vous demande si vous souhaitez aussi effacer vos réunions.

## Questions fréquentes

<details>
<summary><b>« Ollama non détecté »</b></summary>

Installez [Ollama](https://ollama.com/download), puis relancez TranscriPilote : il s'occupe du reste.
</details>

<details>
<summary><b>Les résumés sont imprécis</b></summary>

Ajoutez du contexte avant de générer le résumé (participants, sujet, points à surveiller),
ou choisissez un autre modèle d'IA dans **Réglages → Résumés**.
</details>

<details>
<summary><b>La transcription est lente</b></summary>

Sans carte graphique, comptez de la moitié à deux fois la durée de l'enregistrement.
La qualité « Équilibré » est le meilleur compromis ; « Précis » et « Très précis » prennent plus de temps.
</details>

<details>
<summary><b>Le premier lancement a échoué</b></summary>

Vérifiez votre connexion internet puis relancez TranscriPilote : la préparation reprend là où elle s'est arrêtée.
</details>

Plus de réponses dans la [FAQ du site](https://mikedns.github.io/TranscriPilote/faq.html).

## Assistance

Un problème ou une idée ? [Ouvrez un signalement](https://github.com/MikeDns/TranscriPilote/issues/new/choose).
Pour un problème de sécurité, utilisez le [signalement privé](https://github.com/MikeDns/TranscriPilote/security/advisories/new).

---

<div align="center">

TranscriPilote est un logiciel gratuit, créé par **Mike DANSOU**.
© 2026 Mike DANSOU, tous droits réservés · [Conditions d'utilisation](LICENSE) · [Composants tiers](THIRD_PARTY_NOTICES.md)

</div>
