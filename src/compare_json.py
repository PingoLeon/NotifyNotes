import json
from parse import convert_notes_to_json
import os

def load_notes_json(filepath):
    if not os.path.exists(filepath):
        print(f"Le fichier {filepath} n'existe pas. Retourne une liste vide.")
        return []   
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_notes_json(data, filepath):
    data.replace('�', 'é').replace('Ã©', 'é').replace('Ã¨', 'è').replace('ï¿½', 'Á')
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def find_new_notes(old_notes, new_notes):
    changes = []
    old_map = {(m['matiere'], m['coef']): m for m in old_notes}
    for new_matiere in new_notes:
        key = (new_matiere['matiere'], new_matiere['coef'])
        old_matiere = old_map.get(key)
        if not old_matiere:
            continue
        for section in ["Projet", "Contrôle Continu", "Examen"]:
            old_section = old_matiere['sections'].get(section, [])
            new_section = new_matiere['sections'].get(section, [])
            for idx, new_block in enumerate(new_section):
                old_block = old_section[idx] if idx < len(old_section) else None
                new_notes_list = new_block.get("notes", [])
                old_notes_list = old_block.get("notes", []) if old_block else []
                for n_idx, new_note in enumerate(new_notes_list):
                    old_note = old_notes_list[n_idx] if n_idx < len(old_notes_list) else None
                    if old_note != new_note:
                        matiere_tronquee = new_matiere['matiere'].split('/')[0].strip()
                        note = new_note.get("note", "")
                        ponderation = new_note.get("pondération", "")
                        changes.append([matiere_tronquee, section, note, ponderation])
                        print(f"Changement détecté : {matiere_tronquee}, catégorie={section}, note={note}, pondération={ponderation}")
    return changes