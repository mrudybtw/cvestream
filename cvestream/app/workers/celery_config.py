import os
from celery import Celery

def make_celery(app_name=__name__):
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    celery = Celery(app_name, broker=redis_url)
    celery.conf.update(
        result_backend=redis_url
    )
    return celery

celery_app = make_celery()
