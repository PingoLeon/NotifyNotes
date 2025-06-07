from bs4 import BeautifulSoup
import json

def fix_encoding(s):
    return s.replace('�', 'é').replace('Ã©', 'é').replace('Ã¨', 'è').replace('ï¿½', 'Á')

with open("notes.html", "rb") as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, "lxml", from_encoding="windows-1252")

header_row = soup.find("thead").find_all("tr")[1]
headers = [fix_encoding(th.get_text(separator=" ", strip=True).split("\n")[0]) for th in header_row.find_all("th")]

split_data = []
data = []
recording = True

for row in soup.find("tbody").find_all("tr"):
    classes = row.get("class", [])
    # Si on tombe sur slave master-2, on split et on arrête d'enregistrer
    if "slave" in classes and "master-2" in classes:
        if data:
            split_data.append(data)
            data = []
        recording = False
        continue
    # Tant qu'on n'a pas rencontré slave master-2, on enregistre tout (y compris slave master-1)
    if recording:
        cells = [fix_encoding(td.get_text(separator=" ", strip=True)) for td in row.find_all("td")]
        if any(cells[1:]):
            data.append(dict(zip(headers, cells)))

if data:
    split_data.append(data)

# Regroupement par matière et sous-sections
organized = []
i = 0
while i < len(split_data[0]):
    ligne = split_data[0][i]
    if ligne["Coef."]:
        matiere_nom = ligne[headers[0]]
        coef = ligne["Coef."]
        sections = {"Projet": [], "Contrôle Continu": [], "Examen": []}
        i += 1
        while i < len(split_data[0]) and not split_data[0][i]["Coef."]:
            sous_ligne = split_data[0][i].copy()
            titre = sous_ligne[headers[0]].strip()
            # On trie d'abord
            if titre == "Projet":
                cible = sections["Projet"]
            elif titre == "Contrôle Continu" or titre == "ContrÃ´le Continu":
                cible = sections["Contrôle Continu"]
            elif titre == "Examen":
                cible = sections["Examen"]
            else:
                i += 1
                continue
            # Supprime les clés inutiles
            sous_ligne.pop("Rattrapage Re-sit session", None)
            sous_ligne.pop("Coef.", None)
            sous_ligne.pop("Cours et ï¿½valuations Courses and evaluations", None)
            # Renomme les clés importantes
            if "Pondï¿½ration Weight" in sous_ligne:
                sous_ligne["pondération"] = sous_ligne.pop("Pondï¿½ration Weight")
            if "Notes Grades" in sous_ligne:
                sous_ligne["note"] = sous_ligne.pop("Notes Grades")
            cible.append(sous_ligne)
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

print(json.dumps(organized, ensure_ascii=False, indent=2))