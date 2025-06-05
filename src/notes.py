import requests
import time
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
STORAGE_FILE = os.getenv("STORAGE_FILE", "last_notes_hash.txt")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "3600"))
NTFY_URL = os.getenv("NTFY_URL")
NTFY_USER = os.getenv("NTFY_USER")
NTFY_PASS = os.getenv("NTFY_PASS")
auth = (NTFY_USER, NTFY_PASS)

def get_notes_content():
    response = requests.get(URL)
    response.raise_for_status()
    return response.text

def get_content_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def load_last_hash():
    if not os.path.exists(STORAGE_FILE):
        return None
    with open(STORAGE_FILE, "r") as f:
        return f.read().strip()

def save_hash(hash_value):
    with open(STORAGE_FILE, "w") as f:
        f.write(hash_value)

def send_notification(msg):
    requests.post(NTFY_URL, data=msg, auth=auth)

def main():
    while True:
        content = get_notes_content()
        current_hash = get_content_hash(content)
        last_hash = load_last_hash()
        if last_hash != current_hash:
            print("Changement détecté dans les notes.")
            send_notification("Changement détecté dans les notes.")
            save_hash(current_hash)
        else:
            print("Aucun changement détecté.")
            send_notification("Aucun changement détecté.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()