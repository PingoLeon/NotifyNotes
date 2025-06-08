import requests
import time
import os
import compare_json as comparator
import parse

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

#! Envoi de notification via NTFY (Amélioration possible)
def send_notification(change):
    if change == []:
        if LOG_LEVEL == "DEBUG":
            response = requests.post(NTFY_URL, data=":(", headers={ "Title": "Aucun changement" }, auth=auth)
        return
    
    matiere, section, note, ponderation = change
    title = parse.strip_accents(f"{matiere} - {section}")
    text = f"➡️ Note: {note} - Pondération: {ponderation}"
    print(title)
    if NTFY_AUTH:
        response = requests.post(
            NTFY_URL, 
            data=text,
            headers={ "Title": title,
                      "Tags" : "new"},
            auth=auth)
    else:
        response = requests.post(
            NTFY_URL, 
            data=text,
            headers={ "Title": title,
                    "Tags" : "new"})
    if response.status_code != 200:
        print(f"Erreur lors de l'envoi de la notification: {response.status_code} - {response.text}")

def main():
    while True:
        # Récupérer le contenu des notes
        content = get_notes_content()
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Vérification des notes à {current_time}...")

        # Charger l'ancien JSON
        old_notes = comparator.load_notes_json("old_notes.json") if os.path.exists("old_notes.json") else []
        
        # Convertir le content dans new_notes.json
        parse.convert_notes_to_json(content, "new_notes.json")
        new_notes = comparator.load_notes_json("new_notes.json")
        
        if not old_notes: # Si aucun ancien JSON, on initialise
            print("Aucun ancien JSON trouvé, initialisation des notes")
            # Renommer le json nouveau en ancien
            if os.path.exists("old_notes.json"):
                os.remove("old_notes.json")
            os.rename("new_notes.json", "old_notes.json")
        else: # Si un ancien JSON existe, on compare les notes
            # Comparer
            changes = comparator.find_new_notes(old_notes, new_notes)
            if changes:
                print("\n#####❗ Changement détecté dans les notes !####")
                for change in changes:
                    print(f"\n ")
                    send_notification(change)
            else:
                print("\n🫠 Aucun changement détecté.")
                if LOG_LEVEL == "DEBUG":
                    send_notification([])
            if os.path.exists("old_notes.json"):
                os.remove("old_notes.json")
            os.rename("new_notes.json", "old_notes.json")

        next_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + CHECK_INTERVAL))
        print("Prochain check à", next_time)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()