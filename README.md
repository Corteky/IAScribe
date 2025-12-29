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
git clone https://github.com/Corteky/IAScribe.git
cd AUDIO_GeminiScribe_26122025
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuration de l'IA (CRITIQUE ⚠️)
Créez un fichier nommé `.env` à la racine du projet contenant votre clé API (obtenue sur Google AI Studio) :
```ini
GOOGLE_API_KEY=AIzaSyVotreCleSecreteIci
GEMINI_MODEL=gemini-1.5-flash
PROJECT_ROOT=/storage/emulated/0/Documents/ProgDev
```

### 4. Création du Raccourci (Recommandé)
Pour lancer le script depuis n'importe où avec la commande `scribe`, exécutez ces lignes **en étant situé dans le dossier du projet** :

```bash
# La commande $(pwd) récupère automatiquement le chemin complet actuel
echo "alias scribe='python $(pwd)/main.py'" >> ~/.bashrc
source ~/.bashrc
```

*(Si vous utilisez zsh ou un autre shell, adaptez le fichier de config, ex: .zshrc)*

## 🚀 Utilisation

Une fois l'alias configuré, tapez simplement :
```bash
scribe
```
Le script vous demandera l'URI du fichier.
- Vous pouvez utiliser le "Drag & Drop" dans le terminal.
- Si `PROJECT_ROOT` est configuré, tapez juste le chemin relatif (ex: `MaVideo.mp4`).

## 🛡️ License
MIT License.
