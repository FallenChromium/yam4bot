#!/bin/sh
mkdir -p /app/data
touch bot.db
chown -R appuser:root /app/data
chmod -R 700 /app/data
exec runuser -u appuser -- "$@"
