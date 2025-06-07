import requests
import time
import hashlib
import os

from env import (
    STORAGE_FILE, STORAGE_FILE_URL, CHECK_INTERVAL, TZ,
    URL, NTFY_AUTH, NTFY_USER, NTFY_PASS, NTFY_URL, auth, LOG_LEVEL, ERROR_HASH
)

os.environ["TZ"] = TZ
try:
    time.tzset()
except AttributeError:
    print("Avertissement : time.tzset() non supporté sur cette plateforme.")

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
    if hash == ERROR_HASH:
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
                send_notification("🫠 Aucun changement détecté.") # Envoyer une notif même si échec si le debug est activé
        
        # Afficher le prochain check et attendre
        next_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + CHECK_INTERVAL))
        print("Prochain check à", next_time)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()