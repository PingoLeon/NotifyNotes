from bs4 import BeautifulSoup
import json

def fix_encoding(s):
    return s.replace('�', 'é').replace('Ã©', 'é').replace('Ã¨', 'è').replace('ï¿½', 'Á')

with open("notes.html", "rb") as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, "lxml", from_encoding="windows-1252")

header_row = soup.find("thead").find_all("tr")[1]
headers = [fix_encoding(th.get_text(separator=" ", strip=True).split("\n")[0]) for th in header_row.find_all("th")]

rows = [
    [fix_encoding(td.get_text(separator=" ", strip=True)) for td in row.find_all("td")]
    for row in soup.find("tbody").find_all("tr")
    if "master-1" in row.get("class", [])
]

print(f"Found {len(rows)} rows with {len(headers)} headers.")
data = [dict(zip(headers, cells)) for cells in rows if any(cells[1:])]

section_map = {
    "Projet": "Projet",
    "Contrôle Continu": "Contrôle Continu",
    "ContrÃ´le Continu": "Contrôle Continu",
    "Examen": "Examen"
}

organized = []
i = 0
while i < len(data):
    ligne = data[i]
    if ligne.get("Coef."):
        matiere_nom = ligne[headers[0]]
        coef = ligne["Coef."]
        sections = {"Projet": [], "Contrôle Continu": [], "Examen": []}
        i += 1
        while i < len(data) and not data[i].get("Coef."):
            sous_ligne = data[i].copy()
            titre = sous_ligne[headers[0]].strip()
            section = section_map.get(titre)
            if section:
                # Supprimer la clé inutile
                sous_ligne.pop("Coef.", None)
                sous_ligne.pop("Rattrapage Re-sit session", None)
                sous_ligne.pop("Cours et Ávaluations Courses and evaluations", None)
                # Renommer la pondération
                if "Pondï¿½ration Weight" in sous_ligne:
                    sous_ligne["pondération"] = sous_ligne.pop("Pondï¿½ration Weight")
                if "PondÁration Weight" in sous_ligne:
                    sous_ligne["pondération"] = sous_ligne.pop("PondÁration Weight")
                if "Notes Grades" in sous_ligne:
                    sous_ligne["note"] = sous_ligne.pop("Notes Grades")
                sections[section].append(sous_ligne)
            i += 1
        organized.append({
            "matiere": matiere_nom,
            "coef": coef,
            "sections": sections
        })
    else:
        i += 1

with open("notes_clean.json", "w", encoding="utf-8") as f:
    json.dump(organized, f, ensure_ascii=False, indent=2)