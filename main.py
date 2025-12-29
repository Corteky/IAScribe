import os
import time
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
PROJECT_ROOT = os.getenv("PROJECT_ROOT") 

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
        # L'invite explicite demandée
        user_input = input("\n📁 Entrez l'URI du fichier (ou 'q' pour quitter) : ").strip()
        
        if user_input.lower() == 'q':
            return None

        # Nettoyage (guillemets du copier-coller)
        clean_input = user_input.replace("'", "").replace('"', "").strip()
        path = Path(clean_input)

        # 1. Test direct (Chemin absolu ou relatif simple)
        if path.exists() and path.is_file():
            return path
        
        # 2. Test via PROJECT_ROOT (si configuré dans .env)
        if PROJECT_ROOT:
            root_path = Path(PROJECT_ROOT)
            combined_path = root_path / clean_input
            if combined_path.exists() and combined_path.is_file():
                print(f"   🔍 Fichier trouvé dans vos projets : {combined_path}")
                return combined_path

        print(f"❌ Fichier introuvable : {clean_input}")
        print("   Essayez de glisser-déposer le fichier dans le terminal.")

def convert_to_optimized_mp3(input_path):
    output_filename = input_path.stem + "_optimized.mp3"
    # On met le temporaire dans le dossier du script pour ne pas polluer le dossier source
    output_path = Path(os.getcwd()) / output_filename
    
    print_step("🎧", f"Optimisation audio (Mono 64k)...")
    # -vn: no video, -ac 1: mono, -b:a 64k: bitrate voix
    cmd = ["ffmpeg", "-i", str(input_path), "-vn", "-ac", "1", "-b:a", "64k", str(output_path), "-y"]
    
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
        return output_path
    except subprocess.CalledProcessError:
        print("   ❌ Erreur FFMPEG. Le fichier est-il valide ?")
        return None

def main():
    print(f"\n🤖 \033[1mIAScribe\033[0m (Modele: {MODEL_NAME})")
    
    if not API_KEY:
        print("❌ ERREUR : Clé API manquante dans .env")
        return

    check_dependencies()

    # 1. Demande explicite
    input_path = get_file_path()
    if not input_path: return # Quitter

    # 2. Conversion
    mp3_path = convert_to_optimized_mp3(input_path)
    if not mp3_path: return

    # 3. Traitement IA
    genai.configure(api_key=API_KEY)
    
    print_step("☁️", "Envoi à Gemini...")
    try:
        gemini_file = genai.upload_file(path=mp3_path)
        
        # Attente active
        while gemini_file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(1)
            gemini_file = genai.get_file(gemini_file.name)
        
        if gemini_file.state.name == "FAILED":
            print("\n❌ Échec du traitement par Google.")
            return

        print_step("📝", "Transcription en cours...")
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Prompt "Brut & Multilingue"
        prompt = "Transcris cet audio verbatim. Si plusieurs langues, conserve la langue d'origine. Ne traduis pas."
        
        response = model.generate_content([gemini_file, prompt])
        
        # 4. Sauvegarde (A côté du fichier original)
        output_txt = input_path.parent / (input_path.stem + "_Transcription.txt")
        
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print_step("🎉", f"Terminé ! Fichier : {output_txt.name}")
        
        # Nettoyage
        os.remove(mp3_path)
        genai.delete_file(gemini_file.name)

    except Exception as e:
        print(f"\n❌ Erreur : {e}")

if __name__ == "__main__":
    main()
