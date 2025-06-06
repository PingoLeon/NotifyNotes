#!/bin/sh
if [ "$(stat -c %u /config)" != "1000" ]; then
  chown -R appuser /config
fi
exec "$@"