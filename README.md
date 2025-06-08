# 📢 NotifyNotes

**NotifyNotes** est un script Python simple à auto-héberger (notamment via Docker) qui vérifie régulièrement si de nouvelles notes sont disponibles sur votre espace étudiant, puis vous envoie une notification via [ntfy](https://ntfy.sh/).

---

## 🚀 Fonctionnalités principales

- **Surveillance automatique** de vos notes en ligne du groupe OMNES
- **Notifications instantanées** sur votre téléphone ou navigateur via ntfy
- **Configuration simple** via variables d'environnement ou fichier `.env`
- **Compatible Docker** pour un déploiement facile partout

---

## 🗂️ Structure du projet

```
NotifyNotes
├── src/
│   ├── main.py              # Script principal
│   ├── parse.py             # Parsing HTML → JSON
│   ├── compare_json.py      # Détection des changements
│   └── env.py               # Gestion des variables d'environnement
├── requirements.txt         # Dépendances Python
├── Dockerfile               # Image Docker
├── entrypoint.sh            # Script d'entrée Docker
├── .env                     # (optionnel) Variables d'environnement
└── README.md                # Ce fichier !
```

---

## 🛠️ Prérequis

- **Docker** installé sur votre machine (ou Python 3.9+ si usage sans Docker)
- **Un accès à votre page de notes** via une URL spécifique (`ex : campusonline.inseec.net/note/note_ajax.php?AccountName=[ID]`)
  - Comment l'obtenir :
    - Aller sur `https://VOTREECOLE.campusonline.me/fr-fr/scolarité/`, naviguez dans le relevé de notes, puis allez dans l'onglet `Network` de Devtools (Chrome), la dernière requête est celle qui fetch le fichier de notes avec un id qui vous appartient.
    - L'URL à obtenir est dans l'onglet `Headers`, à la ligne `request_url` de la requete qui charge vos notes
- **L'application ntfy** installée sur votre smartphone (Android/iOS) ou accès à une instance ntfy

---

## ⚡ Installation rapide

### 1. Lancez le conteneur

#### Avec Docker Compose (recommandé)

```yaml
services:
  notifynotes:
    image: ghcr.io/pingoleon/notifynotes:latest
    container_name: notifynotes
    environment:
      - URL=https://campusonline.inseec.net/note/note_ajax.php?AccountName=VOTRE_ID #REQUIS
      - NTFY_URL=https://ntfy.votre-instance.org/notifs # Facultatif
      - NTFY_AUTH=true # Facultatif
      - NTFY_USER=monuser # Facultatif
      - NTFY_PASS=monmotdepasse # Facultatif
    volumes:
      - /config/notifynotes:/config
    restart: unless-stopped
    network_mode: host
```

Lancez avec :

```bash
docker compose up -d
```

#### Ou en ligne de commande

```bash
docker run -d \
  --name notifynotes \
  --env URL="https://campusonline.inseec.net/note/note_ajax.php?AccountName=VOTRE_ID" \
  --env NTFY_URL=https://ntfy.votre-instance.org/notifs \
  --env NTFY_AUTH=true \
  --env NTFY_USER=monuser \
  --env NTFY_PASS=monmotdepasse \
  --volume /config/notifynotes:/config \
  --restart unless-stopped \
  --network host \
  ghcr.io/pingoleon/notifynotes:latest
```
---
 ## 📲 Recevoir les notifications

1. Installez l'application ntfy sur votre smartphone :

   <a href="https://play.google.com/store/apps/details?id=io.heckel.ntfy">
     <img src="https://play.google.com/intl/en_us/badges/static/images/badges/fr_badge_web_generic.png" alt="Disponible sur Google Play" height="30" style="margin-right:8px;"/>
   </a>
   <a href="https://apps.apple.com/us/app/ntfy/id1625396347">
     <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" alt="Télécharger sur l'App Store" height="30"/>
   </a>
2. Ajoutez le topic (ex: `notes-xxxxxxx`) affiché dans les logs Docker ou celui que vous avez défini dans `NTFY_URL`.
3. Recevez vos notifications dès qu'une nouvelle note est détectée ! 🎉
---    

## ⚙️ Variables d'environnement

| Variable                 | Description              | Exemple / Valeur par défaut                                       | Obligatoire |
| ------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------ | ----------- |
| `URL`                  | **URL de la page de notes à surveiller**               | https://campusonline.inseec.net/note/note_ajax.php?AccountName=... | ✅ Oui      |
| `NTFY_URL`             | URL de votre serveur ntfy (notifications)                     | https://ntfy.sh/mon-topic                                          | Non         |
| `NTFY_AUTH`            | Active l'authentification ntfy (`true`/`false`)           | false                                                              | Non         |
| `NTFY_USER`            | Identifiant ntfy (si auth activée)                           | monuser                                                            | Non         |
| `NTFY_PASS`            | Mot de passe ntfy (si auth activée)                          | monmotdepasse                                                      | Non         |
| `CHECK_INTERVAL`       | Intervalle de vérification entre Minuit et 7H (en secondes)  | 1800 (30 minutes)                                                  | Non         |
| `STORAGE_NOTES_JSON`   | Chemin du fichier de stockage des notes précédentes         | /config/old_notes.json                                             | Non         |
| `STORAGE_NOTES_JSON_2` | Chemin du fichier temporaire pour les nouvelles notes         | /config/new_notes.json                                             | Non         |
| `STORAGE_FILE_URL`     | Chemin du fichier où stocker l'URL ntfy générée si besoin | /config/ntfy_url.txt                                               | Non         |
| `LOG_LEVEL`            | Niveau de log (`INFO` ou `DEBUG`)                         | INFO                                                               | Non         |
| `TZ`                   | Fuseau horaire                                                | Europe/Paris                                                       | Non         |

> **Astuce :** Si vous ne renseignez pas `NTFY_URL`, une URL ntfy aléatoire sera générée et affichée dans les logs. elle sera en plus enregistrée dans un fichier txt persistant pour ne pas changer d'adresse dans votre app à chaque fois.
>
> ---
>
>

## 📲 Recevoir les notifications

1. Installez l'application ntfy sur votre smartphone :

   /p
l---ip install -r requirements.txt
```

### 2. Configurez les variables d'environnement

- **Méthode recommandée :** créez un fichier `.env` à la racine du projet (voir exemple plus bas)

### 3. Construisez l'image Docker

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/pingoleon/notifynotes:latest .
```

## 📝 Exemple de fichier `.env`

```
URL=https://campusonline.inseec.net/note/note_ajax.php?AccountName=[VOTRE_ID]
NTFY_URL=https://ntfy.xxxx.com/sujet
NTFY_AUTH=true # BESOIN SEULEMENT SI INSTANCE NTFY PRIVEE
NTFY_USER=[USERNAME]
NTFY_PASS=[CHOUETTE_MDP]
STORAGE_NOTES_JSON=old_notes.json
STORAGE_NOTES_JSON_2=new_notes.json
STORAGE_FILE_URL=ntfy_url.txt
```

---

## ❓ FAQ

- **Q : Est-ce que je peux utiliser ce script sans ntfy ?**

  - Non, ntfy, via l'app officielle disponible sur IOS et Android est nécessaire pour recevoir les notifications.
- **Q : Est-ce que mes identifiants sont stockés ?**

  - Non, seules les notes sont stockées localement pour comparaison.

---

## 🤝 Contribuer

Les contributions sont **bienvenues** !
N'hésitez pas à ouvrir une *issue* ou une *pull request* pour toute suggestion, bug ou amélioration.

---

## 📝 Licence

Ce projet est sous licence Unlicense, parce que le partage c'est cool
