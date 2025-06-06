import requests
import time
import hashlib
import os
import random

#* Activer ou non le dotenv si le fichier .env est présent
if os.path.exists(".env"):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Le module python-dotenv n'est pas installé, mais .env détecté.")

#* Variables d'environnement
STORAGE_FILE = os.getenv("STORAGE_FILE", "/config/last_notes_hash.txt")
STORAGE_FILE_URL = os.getenv("STORAGE_FILE_URL", "/config/ntfy_url.txt")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "7200"))

#* Ajout de la gestion du timezone
TZ = os.getenv("TZ", "Europe/Paris")
os.environ["TZ"] = TZ
try:
    time.tzset()
except AttributeError:
    print("Avertissement : time.tzset() non supporté sur cette plateforme.")


#! Chargement des variables d'environnement importantes
#? URL des notes à surveiller
URL = os.getenv("URL") 
if not URL:
    print("Erreur: La variable URL doit être définie dans le fichier .env ou en ENV docker. (ex:https://campusonline.inseec.net/note/note_ajax.php?AccountName=)")
    exit(1)
elif not URL.startswith("https://campusonline.inseec.net/note/note_ajax.php?AccountName="):
    print("Erreur: L'URL doit commencer par 'https://campusonline.inseec.net/note/note_ajax.php?AccountName='")
    exit(1)

#? Vérification de l'authentification
NTFY_AUTH = os.getenv("NTFY_AUTH", "False").lower() == "true" 
if NTFY_AUTH:
    NTFY_USER = os.getenv("NTFY_USER")
    NTFY_PASS = os.getenv("NTFY_PASS")
    auth = (NTFY_USER, NTFY_PASS)
    if not NTFY_USER or not NTFY_PASS:
        print("Erreur: Les variables d'environnement NTFY_USER et NTFY_PASS doivent être définies si NTFY_AUTH est activé.")
        exit(1)

#? Endpoint de notification NTFY
NTFY_URL = os.getenv("NTFY_URL") 
if NTFY_URL:
    print("URL ntfy custom utilisée :", NTFY_URL)
else:
    # Si pas de variable d'env, on regarde dans le fichier STORAGE_FILE_URL
    if os.path.exists(STORAGE_FILE_URL):
        with open(STORAGE_FILE_URL, "r") as f:
            NTFY_URL = f.read().strip()
        print("URL ntfy récupérée depuis le fichier :", NTFY_URL)
        NTFY_AUTH = False
    else:
        # Sinon, on en génère une nouvelle et on la sauvegarde
        random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=9))
        NTFY_URL = f"https://ntfy.sh/notes-{random_suffix}"
        with open(STORAGE_FILE_URL, "w") as f:
            f.write(NTFY_URL)
        print("URL ntfy par défaut générée :", NTFY_URL)
        NTFY_AUTH = False

#? Niveau de log
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
if LOG_LEVEL == "DEBUG": # Adapter l'intervalle de vérification en fonction du niveau de log
    CHECK_INTERVAL = 30

#? Fonction pour récupérer le contenu des notes
def get_notes_content():
    response = requests.get(URL)
    
    if response.status_code != 200:
        raise Exception(f"Erreur lors de la récupération des notes: {response.status_code} - {response.text}")
    response.raise_for_status()
    return response.text

#? Fonction pour calculer le hash du contenu des notes (et check si le hash est correct)
def get_content_hash(content):
    hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    if hash == "9c287ec0f172e07215c5af2f96445968c266bcc24519ee0cf70f43f178fa613e":
        print("A priori, le AccountName dans l'URL est incorrect...")
        exit(1)     
    return hash

#? Chargement du dernier hash depuis un fichier
def load_last_hash():
    if not os.path.exists(STORAGE_FILE):
        return None
    with open(STORAGE_FILE, "r") as f:
        return f.read().strip()

#? Sauvegarde du hash dans un fichier
def save_hash(hash_value):
    with open(STORAGE_FILE, "w") as f:
        f.write(hash_value)

#! Envoi de notification via NTFY (Amélioration possible)
def send_notification(msg):
    if NTFY_AUTH:
        response = requests.post(NTFY_URL, data=msg, auth=auth)
    else:
        response = requests.post(NTFY_URL, data=msg)
    if response.status_code != 200:
        print(f"Erreur lors de l'envoi de la notification: {response.status_code} - {response.text}")

def main():
    while True:
        # Récupérer le contenu des notes et calculer le hash
        content = get_notes_content()
        current_hash = get_content_hash(content)
        last_hash = load_last_hash()
        
        # Afficher l'heure actuelle et vérifier les changements
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Vérification des notes à {current_time}...")
        
        # Vérifier si le hash précédent existe
        if last_hash is None:
            print("Aucun hash précédent trouvé, enregistrement du hash actuel.")
            save_hash(current_hash)
            send_notification("Initialisation des notes, aucun changement détecté.")
            continue
        
        # Comparaison des hash
        if last_hash != current_hash:
            print("\n#####❗ Changement détecté dans les notes !####")
            send_notification("❗Changement détecté dans les notes !")
            save_hash(current_hash)
        else:
            print("\n🫠 Aucun changement détecté.")
            if LOG_LEVEL == "DEBUG" :
                send_notification("🫠 Aucun changement détecté.") # Envoyer une notif si le debug est activé
        
        # Afficher le prochain check et attendre
        next_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + CHECK_INTERVAL))
        print("Prochain check à", next_time)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()