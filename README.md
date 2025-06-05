# NotifyNotes

Simple script Python à self-host soi-même via Docker pour vérifier régulièrement si des nouvelles notes sont disponibles. Envoie une notification à une instance ntfy

## Structure du projet

```
NotifyNotes
├── src
│   └── notes.py        # Script Python pour surveiller les notes
├── requirements.txt     # Dépendances nécessaires
├── Dockerfile           # Instructions pour construire l'image Docker
└── README.md            # Documentation du projet
```

## Prérequis

- Docker installé sur votre host
- l'app ntfy installée (IOS/Android)

## Utilisation

- Renseigner les variables d'env (voir section après) pour que l'application fonctionne correctement
- Si pas d'instance NTFY self-hostée, une URL est donnée dans les logs docker et stockée dans un fichier dans /config/ et est à renseigner sur l'app ntfy

## Installation

1. Clonez ce dépôt sur votre machine :

   ```
   git clone https://github.com/PingoLeon/NotifyNotes

   ```
2. Build l'image Docker :

   ```
   docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/pingoleon/notifynotes:latest .
   ```

## Variables d'environnement

| Variable         | Description                                                    | Par défaut / Exemple                                              | Obligatoire |
| ---------------- | -------------------------------------------------------------- | ------------------------------------------------------------------ | ----------- |
| URL              | **REQUIS : URL de la page à surveiller pour les notes** | https://campusonline.inseec.net/note/note_ajax.php?AccountName=... | Oui         |
| NTFY_URL         | URL du serveur ntfy pour envoyer les notifications             | https://ntfy.xxxxxxx.com/notifs                                    | Non         |
| NTFY_AUTH        | Active l'authentification ntfy (true/false)                    | false                                                              | Non         |
| NTFY_USER        | Nom d'utilisateur pour l'authentification ntfy                 | superbanane123                                                     | Non         |
| NTFY_PASS        | Mot de passe pour l'authentification ntfy                      | supermdp1234indevinable                                            | Non         |
| CHECK_INTER      | Intervalle de vérification en secondes                        | 3600 (en secondes)                                                 | Non         |
| STORAGE_FILE     | Chemin du fichier de stockage du hash des notes                | /config/last_notes_hash.txt                                        | Non         |
| STORAGE_FILE_URL | Chemin du fichier de stockage de l'URL ntfy                    | /config/ntfy_url.txt                                               | Non         |

**Si aucune instance self-host n'est disponible, ça ne sert à rien de mettre les variables facultatives**

## Utilisation avec Docker Compose

Voici un exemple de fichier `docker-compose.yml` :

```yaml
# filepath: c:\Users\leon\Downloads\testpy\NotifyNotes\docker-compose.yml
version: '3.8'
services:
  notifynotes:
    image: ghcr.io/pingoleon/notifynotes:latest
    container_name: notifynotes
    environment:
      - URL=https://campusonline.inseec.net/note/note_ajax.php?AccountName=[redacted]
      - NTFY_URL=[redacted] #Facultatif
      - NTFY_AUTH=[redacted] 
      - NTFY_USER=[redacted]
      - NTFY_PASS=[redacted]
    volumes:
      - /config/notifynotes:/config
    restart: unless-stopped
    network_mode: host
```

Ou en ligne de commande Docker :

```bash
docker run -d \
  --name notifynotes \
  --env URL="https://campusonline.inseec.net/note/note_ajax.php?AccountName=[redacted]" \
  --env NTFY_URL=[redacted] \
  --env NTFY_AUTH=[redacted] \
  --env NTFY_USER=[redacted] \
  --env NTFY_PASS=[redacted] \
  --volume /config/notifynotes:/config \
  --restart unless-stopped \
  --network host \
  ghcr.io/pingoleon/notifynotes:latest
```

Vous pouvez aussi lancer le conteneur avec la commande :

```bash
docker compose up -d
```

## Contribuer

Les contributions sont les bienvenues ! Une pull request ça fait toujours plaisir
