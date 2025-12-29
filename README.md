# 🎙️ IAScribe (2025 Edition)

> **Transcription Audio AI Haute Fidélité via Google Gemini 3**
> *Conçu pour Android/Termux, compatible Linux/Mac.*

## 📋 Description
Ce projet automatise la transcription de fichiers vidéo/audio en texte brut.
Il utilise **FFMPEG** pour optimiser l'audio et l'API **Google Gemini 1.5/3.0** (Multimodale) pour une transcription verbatim.

**Pourquoi Gemini ?**
Contrairement aux solutions classiques (comme Whisper), Gemini possède une fenêtre de contexte massive (1M+ à 2M tokens). Cela permet d'ingérer des fichiers audio de plusieurs heures **sans aucun découpage (chunking)**, garantissant une cohérence parfaite du contexte et une gestion native du multilinguisme.

## ✨ Fonctionnalités
- **Zéro Découpage :** Traite des fichiers longs d'un bloc.
- **Auto-Détection de Langue :** Transcrit exactement ce qui est dit, dans la langue où c'est dit (code-switching supporté).
- **Optimisation Mobile :** Convertit tout input (mkv, mp4, avi) en MP3 Mono 64k avant envoi (économie drastique de data 4G/5G).
- **Portabilité :** Gestion intelligente des chemins via `PROJECT_ROOT`.

## 📤 Résultat
Le fichier final (`NomDuFichier_Transcription.txt`) sera **automatiquement enregistré dans le même répertoire que votre fichier vidéo source**.
*(Rien n'est perdu dans le dossier du script, tout reste organisé avec vos données).*

## ⚙️ Installation

### 1. Pré-requis Système
- Python 3.10+
- FFMPEG (`pkg install ffmpeg` sous Termux ou `apt install ffmpeg` sous Linux)
- (Android uniquement) Accès au stockage accordé : `termux-setup-storage`

### 2. Setup (Automatique)
```bash
git clone [https://github.com/VOTRE_USER/AUDIO_IAScribe_26122025.git](https://github.com/VOTRE_USER/AUDIO_IAScribe_26122025.git)
cd AUDIO_IAScribe_26122025
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

*(Note: Si vous n'avez pas de requirements.txt, faites `pip install google-generativeai python-dotenv`)*

### 3. Configuration de l'IA (CRITIQUE ⚠️)

#### A. Obtenir votre clé API

Ce script nécessite une clé API Google AI Studio.

1. Rendez-vous sur **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
2. Connectez-vous avec un compte Google.
3. Cliquez sur **"Create API Key"**.
*(Note : Le "Free Tier" est généralement suffisant pour une utilisation personnelle, vérifiez les quotas sur le site).*

#### B. Créer le fichier .env

Créez un fichier nommé `.env` à la racine du projet avec les variables suivantes :

**Explications des variables :**

1. `GOOGLE_API_KEY` : La clé obtenue à l'étape précédente.
2. `GEMINI_MODEL` : Le modèle choisi.
* `gemini-1.5-flash` : Rapide, économique, suffisant pour 90% des cas.
* `gemini-1.5-pro` : Plus lent, meilleure capacité d'analyse complexe.
* `gemini-2.0-flash-exp` : (Si disponible) Nouvelle génération rapide.


3. `PROJECT_ROOT` : Le dossier parent de vos vidéos (Optionnel, facilite la saisie des chemins).

**Contenu à copier dans le fichier `.env` :**

```ini
GOOGLE_API_KEY=AIzaSyVotreCleSecreteIci
GEMINI_MODEL=gemini-1.5-flash
PROJECT_ROOT=/storage/emulated/0/Documents/ProgDev

```

## 🚀 Utilisation

### Via le Raccourci (Recommandé)

Si vous avez configuré l'alias, tapez simplement :

```bash
scribe

```

Le script vous demandera l'URI du fichier.

* Vous pouvez utiliser le "Drag & Drop" dans le terminal.
* Si `PROJECT_ROOT` est configuré, tapez juste le chemin relatif (ex: `MaVideo.mp4`).

## 🏷️ Mots-clés (Github Topics)

`python` `android` `termux` `gemini-api` `speech-to-text` `transcription` `ffmpeg` `automation` `accessibility` `audhd`

## 🛡️ License

MIT License.

