export database=172.31.1.180
gunicorn --env DJANGO_SETTINGS_MODULE=questionnaire.settings --worker-class gevent --timeout 30 --graceful-timeout 20 --max-requests-jitter 2000 --max-requests 2000 --capture-output -b 0.0.0.0:8000 -w=50 questionnaire.wsgi
