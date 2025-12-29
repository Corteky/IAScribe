# 🎙️ GeminiScribe (2025 Edition)

> **Transcription Audio AI Haute Fidélité via Google Gemini 3**
> *Conçu pour Android/Termux, compatible Linux/Mac.*

## 📋 Description
Ce projet automatise la transcription de fichiers vidéo/audio en texte brut.
Il utilise **FFMPEG** pour optimiser l'audio et l'API **Google Gemini 1.5/3.0** (Multimodale) pour une transcription verbatim, gérant nativement le multilinguisme (code-switching) sans traduction forcée.

## ✨ Fonctionnalités
- **Zéro Découpage :** Traite des fichiers longs d'un bloc (grâce à la fenêtre de contexte de 1M+ tokens).
- **Auto-Détection de Langue :** Transcrit exactement ce qui est dit, dans la langue où c'est dit.
- **Optimisation Mobile :** Convertit tout input (mkv, mp4, avi) en MP3 Mono 64k avant envoi (économie de data 4G/5G).
- **Portabilité :** Gestion intelligente des chemins via \`PROJECT_ROOT\`.

## 📤 Résultat
Le fichier final (`NomDuFichier_Transcription.txt`) sera **automatiquement enregistré dans le même répertoire que votre fichier vidéo source**.
*(Rien n'est perdu dans le dossier du script, tout reste organisé avec vos données).*

## ⚙️ Installation

### 1. Pré-requis
- Python 3.10+
- FFMPEG (\`pkg install ffmpeg\` sous Termux)
- Avoir accordé l'accès à la mémoire interne Android à Termux (\`termux-setup-storage\`) 

### 2. Setup (Automatique)
\`\`\`bash
git clone https://github.com/VOTRE_USER/AUDIO_GeminiScribe_26122025.git
cd AUDIO_GeminiScribe_26122025
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`
*(Note: Si vous n'avez pas de requirements.txt, faites \`pip install google-generativeai python-dotenv\`)*

### 3. Configuration (CRITIQUE ⚠️)
Créez un fichier nommé \`.env\` à la racine du projet.

**Explications des variables :**
1.  `GOOGLE_API_KEY` : Votre clé privée (Obligatoire).
2.  `GEMINI_MODEL` : Le modèle (Ex: `gemini-1.5-flash` ou `gemini-3-flash-preview`).
3.  `PROJECT_ROOT` : Le dossier parent de vos vidéos (Optionnel, pour éviter de taper le chemin complet).

**Contenu à copier dans le fichier \`.env\` :**
\`\`\`ini
GOOGLE_API_KEY=AIzaSyVotreCleSecreteIci
GEMINI_MODEL=gemini-3-flash-preview
PROJECT_ROOT=/storage/emulated/0/Documents/ProgDev
\`\`\`

## 🚀 Utilisation

### Via le Raccourci (Recommandé)
Si vous avez installé l'alias \`scribe\`, tapez simplement :
\`\`\`bash
scribe
\`\`\`
Le script vous demandera l'URI du fichier.
- Vous pouvez utiliser le "Drag & Drop" dans le terminal.
- Si \`PROJECT_ROOT\` est configuré, vous pouvez juste taper le chemin relatif (ex: \`MaVideo.mp4\`).

## 🏷️ Mots-clés (Github Topics)
\`python\` \`android\` \`termux\` \`gemini-api\` \`speech-to-text\` \`transcription\` \`ffmpeg\` \`automation\` \`accessibility\` \`audhd\`

## 🛡️ License
MIT License.
