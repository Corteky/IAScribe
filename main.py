import os
import time
import subprocess
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from dotenv import load_dotenv
from pathlib import Path

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
PROJECT_ROOT = os.getenv("PROJECT_ROOT") 

# Configuration du Timeout (Essentiel pour les longs fichiers sur mobile)
# 600 secondes (10 min) d'attente max pour la réponse HTTP, pas le traitement.
REQUEST_OPTIONS = {"timeout": 600} 

def print_step(emoji, message):
    print(f"\n{emoji} \033[1m{message}\033[0m")

def check_dependencies():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ Erreur : FFMPEG n'est pas installé (pkg install ffmpeg).")
        exit(1)

def get_file_path():
    """Demande l'URI à l'utilisateur et résout le chemin."""
    while True:
        user_input = input("\n📁 Entrez l'URI du fichier (ou 'q' pour quitter) : ").strip()
        if user_input.lower() == 'q': return None

        clean_input = user_input.replace("'", "").replace('"', "").strip()
        path = Path(clean_input)

        if path.exists() and path.is_file():
            return path
        
        if PROJECT_ROOT:
            root_path = Path(PROJECT_ROOT)
            combined_path = root_path / clean_input
            if combined_path.exists() and combined_path.is_file():
                print(f"   🔍 Trouvé dans PROJECT_ROOT : {combined_path.name}")
                return combined_path

        print(f"❌ Fichier introuvable : {clean_input}")

def convert_to_optimized_mp3(input_path):
    output_filename = input_path.stem + "_optimized.mp3"
    output_path = Path(os.getcwd()) / output_filename
    
    print_step("🎧", f"Optimisation audio (Mono 64k)...")
    # Retrait de stderr=DEVNULL pour voir les erreurs si ça plante
    cmd = ["ffmpeg", "-i", str(input_path), "-vn", "-ac", "1", "-b:a", "64k", str(output_path), "-y"]
    
    try:
        # Capture de l'erreur pour affichage propre uniquement si échec
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, text=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erreur FFMPEG :\n{e.stderr}")
        return None

def wait_for_processing(file_obj):
    """Boucle d'attente robuste"""
    print("   État : ", end="", flush=True)
    while file_obj.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        file_obj = genai.get_file(file_obj.name)
    print(f" [{file_obj.state.name}]")
    return file_obj

def main():
    print(f"\n🤖 \033[1mIAScribe\033[0m (Modèle: {MODEL_NAME})")
    
    if not API_KEY:
        print("❌ ERREUR : Clé API manquante dans .env")
        return

    check_dependencies()

    input_path = get_file_path()
    if not input_path: return

    mp3_path = convert_to_optimized_mp3(input_path)
    if not mp3_path: return

    genai.configure(api_key=API_KEY)
    gemini_file = None # Initialisation pour le bloc finally

    try:
        print_step("☁️", "Upload vers Gemini (Google Server)...")
        gemini_file = genai.upload_file(path=mp3_path)
        
        # Attente du traitement côté Google
        gemini_file = wait_for_processing(gemini_file)
        
        if gemini_file.state.name == "FAILED":
            print("\n❌ Échec du traitement interne Google (Encodage non supporté ?).")
            return

        print_step("📝", "Génération de la transcription...")
        model = genai.GenerativeModel(MODEL_NAME)
        
        prompt = "Transcris cet audio verbatim. Si plusieurs langues, conserve la langue d'origine. Ne traduis pas. Aère le texte avec des paragraphes."
        
        # AJOUT : Retry logic simple et Timeout augmenté
        try:
            response = model.generate_content(
                [gemini_file, prompt],
                request_options=REQUEST_OPTIONS
            )
            
            output_txt = input_path.parent / (input_path.stem + "_Transcription.txt")
            with open(output_txt, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            print_step("🎉", f"Succès ! Fichier : {output_txt.name}")

        except google_exceptions.DeadlineExceeded:
            print("\n❌ Timeout : L'API a mis trop de temps à répondre (connexion lente ou fichier trop gros).")
        except google_exceptions.InternalServerError:
            print("\n❌ Erreur serveur Google (500). Réessayez plus tard.")

    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")

    finally:
        # NETTOYAGE SYSTÉMATIQUE (Même en cas de Crash/Ctrl+C)
        print("\n🧹 Nettoyage des fichiers temporaires...")
        if mp3_path and mp3_path.exists():
            os.remove(mp3_path)
            print("   - Fichier MP3 local supprimé.")
        
        if gemini_file:
            try:
                genai.delete_file(gemini_file.name)
                print("   - Fichier Cloud Google supprimé.")
            except Exception:
                pass

if __name__ == "__main__":
    main()
