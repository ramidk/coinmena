#!/bin/sh

echo "Wait for migration."

while ./manage.py showmigrations | grep '\[ \]' >&2; do
    sleep 1
    echo "Waiting for migration..."
done

echo "Migration completed."

exec "$@"
