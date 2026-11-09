# Composants tiers

TranscriPilote est un logiciel gratuit, © 2026 Mike DANSOU, tous droits réservés ([conditions d'utilisation](LICENSE)).
Il s'appuie sur les composants suivants,
qui restent sous leur propre licence.

## Inclus dans l'installateur

| Composant | Licence | Source |
|---|---|---|
| uv (Astral) | MIT ou Apache-2.0 | <https://github.com/astral-sh/uv> |

## Installés au premier lancement (dépendances Python)

| Composant | Licence | Source |
|---|---|---|
| faster-whisper | MIT | <https://github.com/SYSTRAN/faster-whisper> |
| CTranslate2 | MIT | <https://github.com/OpenNMT/CTranslate2> |
| pyannote.audio | MIT | <https://github.com/pyannote/pyannote-audio> |
| PyTorch / torchaudio | BSD-3-Clause | <https://pytorch.org> |
| pywebview | BSD-3-Clause | <https://github.com/r0x0r/pywebview> |
| Qt for Python (PySide6) | LGPL-3.0 | <https://www.qt.io/qt-for-python> |
| sounddevice, soundfile | MIT, BSD-3-Clause | <https://github.com/spatialaudio> / <https://github.com/bastibe> |
| requests | Apache-2.0 | <https://github.com/psf/requests> |

La liste complète et figée des dépendances est dans [uv.lock](uv.lock).

## Téléchargés à la demande depuis leur site officiel

| Composant | Licence | Source |
|---|---|---|
| FFmpeg (build gyan.dev) | GPL-3.0 | <https://www.gyan.dev/ffmpeg/builds/> |
| rclone | MIT | <https://rclone.org> |

## Modèles d'IA

| Modèle | Licence | Remarque |
|---|---|---|
| Whisper (OpenAI), via faster-whisper | MIT | Téléchargé depuis HuggingFace |
| pyannote speaker-diarization-3.1 | MIT | Accès soumis à acceptation des conditions sur HuggingFace |
| Mistral 7B Instruct (via Ollama) | Apache-2.0 | Modèle par défaut, modifiable dans Réglages |

Ollama est un logiciel séparé (MIT) installé par l'utilisateur : <https://ollama.com>.
