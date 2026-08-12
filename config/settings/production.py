from .base import *
import environ
import os

env = environ.Env()
# In production, read from .env
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['yourdomain.com'])

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': env.db('DATABASE_URL')
}

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://redis:6379/1')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://redis:6379/2')

# Production-specific settings (like secure cookies, static roots, etc.)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
