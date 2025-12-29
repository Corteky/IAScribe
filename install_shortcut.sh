#!/bin/bash
PROJECT_DIR="$HOME/ProgDev/AUDIO_GeminiScribe_26122025"

# Définition de la fonction bash (plus puissant qu'un simple alias)
SCRIBE_FUNC="
# --- Raccourci GeminiScribe ---
scribe() {
    # 1. Sauvegarder le dossier actuel
    current_dir=\$(pwd)
    
    # 2. Aller au projet
    cd \"$PROJECT_DIR\" || return

    # 3. Activer venv et lancer (silencieusement pour l'activation)
    source venv/bin/activate
    
    # 4. Lancer le script python
    python main.py
    
    # 5. Nettoyage et retour
    deactivate
    cd \"\$current_dir\"
}
"

# Vérifie si 'scribe' existe déjà pour éviter les doublons
if grep -q "scribe()" ~/.bashrc; then
    echo "⚠️  Le raccourci 'scribe' semble déjà exister dans .bashrc"
else
    echo "$SCRIBE_FUNC" >> ~/.bashrc
    echo "✅ Raccourci 'scribe' ajouté à ~/.bashrc"
    echo "🔄 Rechargement de la configuration..."
    source ~/.bashrc
    echo "🚀 Prêt ! Tape simplement 'scribe' pour tester."
fi
