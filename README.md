# Notes Monitor

Ce projet est un script Python qui surveille les notes sur une plateforme en ligne. Lorsqu'un changement est détecté dans le contenu des notes, une notification est envoyée via un webhook.

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

- Docker installé sur votre machine.
- Un webhook configuré pour recevoir les notifications.

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