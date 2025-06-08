#!/bin/sh
# filepath: entrypoint.sh

# Changer le propriétaire du dossier monté
chown -R 1000:1000 /config

# Exécuter l’application avec l’utilisateur non-root
exec su-exec 1000:1000 "$@"