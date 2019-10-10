import logging

import os

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ownlittleworld.settings')

import django

django.setup()

from celery import Celery

logger = logging.getLogger(__name__)
redis_dsn = f'redis://{"redis" if os.environ.get("BACKEND_ENV") == "prod" else "localhost"}:6379'

# NOTE: there's should another celery instance running in separated container
app = Celery('backend_app', backend=redis_dsn, broker=redis_dsn)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


