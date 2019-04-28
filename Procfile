queue: rq worker
web: ngrok http -subdomain $NGROK_HOSTNAME 5300
redis: scripts/honcho_service_check.bash redis
api: gunicorn smack.wsgi
