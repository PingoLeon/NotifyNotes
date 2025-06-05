# NotifyNotes

Simple script Python à self-host soi-même via Docker pour vérifier régulièrement si des nouvelles notes sont disponibles. Envoie une notification à une instance ntfy à préciser.

## Structure du projet

```
notes-monitor
├── src
│   └── notes.py        # Script Python pour surveiller les notes
├── requirements.txt     # Dépendances nécessaires
├── Dockerfile           # Instructions pour construire l'image Docker
└── README.md            # Documentation du projet
```

## Prérequis

- Docker installé sur votre host
- Une instance self-host de ntfy de préférence, sinon ntfy.sh est utilisé avec une URL fournie dans les logs
- 

## Installation

1. Clonez ce dépôt sur votre machine :

   ```
   git clone <URL_DU_DEPOT>
   cd notes-monitor
   ```
2. Construisez l'image Docker :

   ```
   docker build -t notes-monitor .
   ```

## Exécution

Pour exécuter le script dans un conteneur Docker, utilisez la commande suivante :

```
docker run -e WEBHOOK_URL=<URL_DU_WEBHOOK> notes-monitor
```

Remplacez `<URL_DU_WEBHOOK>` par l'URL de votre webhook.

## Fonctionnalités

- Surveillance des notes avec détection de changements.
- Envoi de notifications via un webhook lorsque des changements sont détectés.
- Exécution périodique configurable.

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une demande de tirage pour toute amélioration ou correction.
