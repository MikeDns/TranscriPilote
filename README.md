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

### [Télécharger TranscriPilote](https://github.com/MikeDns/TranscriPilote/releases/latest)

**Site officiel : [mikedns.github.io/TranscriPilote](https://mikedns.github.io/TranscriPilote/)**

[Signaler un problème](https://github.com/MikeDns/TranscriPilote/issues/new?template=bug_report.yml) ·
[Proposer une idée](https://github.com/MikeDns/TranscriPilote/issues/new?template=feature_request.yml) ·
[Nouveautés](https://github.com/MikeDns/TranscriPilote/releases)

</div>

---

## Pourquoi TranscriPilote ?

Les outils de transcription en ligne envoient vos réunions sur des serveurs tiers.
TranscriPilote fait tout localement, sur un PC de bureau ordinaire **sans carte graphique**
et **sans droits administrateur** : idéal pour un poste professionnel verrouillé ou des échanges confidentiels.

## Fonctionnalités

| | |
|---|---|
| **Enregistrement** | Micro ou audio système (réunions Teams, Zoom, Meet), en parallèle d'autres traitements |
| **Transcription** | Locale et horodatée, plusieurs niveaux de précision |
| **Locuteurs** | Identification de qui parle (optionnel) |
| **Résumés** | Résumé, points clés et actions à faire, avec un modèle d'IA local et un contexte personnalisable |
| **Discussion** | Posez des questions sur une réunion (« qui a validé le budget ? ») |
| **Import** | Fichiers audio et vidéo : MP3, M4A, WAV, MP4, MKV, MOV… |
| **Historique** | Base locale consultable, export TXT et SRT |
| **Tâches en arrière-plan** | Transcriptions et résumés en file d'attente, annulables à tout moment |
| **Sauvegarde** | Optionnelle, vers **votre** Google Drive ou OneDrive personnel |
| **Mises à jour** | Proposées dans l'appli, installées seulement quand vous le décidez, retour arrière possible |

## Installation

### Configuration requise

- Windows 10 ou 11, 64 bits
- 16 Go de RAM recommandés (8 Go minimum avec les modèles les plus légers)
- Environ 10 Go d'espace disque (composants et modèles d'IA)
- [Ollama](https://ollama.com/download) pour les résumés et la discussion (s'installe aussi sans droits admin)

### Étapes

1. Téléchargez `TranscriPilote-Setup-x.y.z.exe` depuis la [dernière version](https://github.com/MikeDns/TranscriPilote/releases/latest).
2. Lancez-le : l'installation se fait dans votre profil Windows, sans droits administrateur.
3. Au premier lancement, TranscriPilote prépare ses composants : **5 à 15 minutes, une seule fois**.
4. Les modèles d'IA se téléchargent automatiquement à la première utilisation.

> Windows SmartScreen peut afficher « Windows a protégé votre ordinateur » : cliquez sur
> **Informations complémentaires → Exécuter quand même**. Chaque version est publiée avec
> `SHA256SUMS.txt` pour vérifier que le fichier n'a pas été modifié.

### Identification des locuteurs (optionnel)

Cette fonction utilise un modèle hébergé sur HuggingFace, qui demande un token gratuit :
1. Créez un token sur <https://huggingface.co/settings/tokens> (lecture seule suffit).
2. Acceptez les conditions de [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1).
3. Collez le token dans **Réglages → Diarization**.

## Mises à jour

TranscriPilote vous prévient au démarrage quand une nouvelle version est disponible
(en bas de la barre latérale, et dans **Réglages → Version et mises à jour**) :

1. **Télécharger** prépare la nouvelle version.
2. **Actualiser l'appli** l'installe au moment que vous choisissez.
3. **Revenir à la version précédente** reste possible en un clic.

Vos données ne sont jamais modifiées par une mise à jour.

## Confidentialité

Tout reste sur votre PC, dans `%LOCALAPPDATA%\TranscriPilote\` : enregistrements, transcriptions,
résumés et réglages. TranscriPilote se connecte à internet uniquement pour télécharger ses composants
et modèles, vérifier les mises à jour, et sauvegarder vers votre cloud **si vous l'activez**.

**Désinstaller** : Paramètres Windows → Applications → TranscriPilote → Désinstaller.
Vos données restent dans `%LOCALAPPDATA%\TranscriPilote\` ; supprimez ce dossier pour tout effacer.

## Questions fréquentes

<details>
<summary><b>« Ollama non détecté »</b></summary>

Installez [Ollama](https://ollama.com/download). TranscriPilote le démarre ensuite tout seul
et télécharge le modèle choisi dans **Réglages → Résumés**.
</details>

<details>
<summary><b>Les résumés sont imprécis</b></summary>

Ajoutez du contexte avant de générer le résumé (participants, sujet, points à surveiller),
ou essayez un autre modèle dans **Réglages → Résumés**.
</details>

<details>
<summary><b>La transcription est lente</b></summary>

Sans carte graphique, comptez de 0,5 à 2 fois la durée de l'audio selon le niveau de précision.
Le modèle `small` est un bon compromis ; `medium` et `large-v3` sont plus précis mais plus lents.
</details>

<details>
<summary><b>Le premier lancement a échoué</b></summary>

Vérifiez votre connexion internet puis relancez TranscriPilote : la préparation reprend là où elle s'est arrêtée.
</details>

## Assistance

Un problème ou une idée ? [Ouvrez un signalement](https://github.com/MikeDns/TranscriPilote/issues/new/choose).
Pour un problème de sécurité, utilisez le [signalement privé](https://github.com/MikeDns/TranscriPilote/security/advisories/new).

---

<div align="center">

TranscriPilote est un logiciel gratuit, créé par **Mike DANSOU**.
© 2026 Mike DANSOU, tous droits réservés · [Conditions d'utilisation](LICENSE) · [Composants tiers](THIRD_PARTY_NOTICES.md)

</div>
