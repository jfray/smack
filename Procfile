queue: python manage.py rqworker
web: ngrok http -subdomain $NGROK_HOSTNAME 5300
redis: scripts/honcho_service_check.bash redis
api: gunicorn smores.wsgi
