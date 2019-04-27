#api: python smack/frontend.py
queue: rq worker
web: ngrok http -subdomain $NGROK_HOSTNAME 5300
redis: scripts/honcho_service_check.bash redis
fe: gunicorn smack.wsgi
