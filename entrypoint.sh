#!/bin/sh
sed -i "1s/.*/from .production import \*/" papusa/settings/__init__.py # Use production settings
python3 manage.py migrate                  # Apply database migrations
python3 manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn papusa.wsgi:application \
    --name papusa \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    -t 3600
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
    "$@"
