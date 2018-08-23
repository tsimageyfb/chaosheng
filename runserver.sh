export database=127.0.0.1
gunicorn --env DJANGO_SETTINGS_MODULE=questionnaire.settings --worker-class gevent --timeout 30 --graceful-timeout 20 --max-requests-jitter 2000 --max-requests 2000 --log-level DEBUG --capture-output -b 0.0.0.0:8000 -w=50 questionnaire.wsgi
