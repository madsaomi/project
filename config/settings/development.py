from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Optional: SQLite is already configured in base.py, which is fine for local dev
# Celery settings for dev
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

# Email backend for dev
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
