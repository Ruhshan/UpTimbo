import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_url = 'redis://localhost:6379'

app.conf.beat_schedule = {
    'every-minute': {
        'task': 'check_and_notify',
        'schedule':10.0,

    },
}



"""
celery multi start single-worker -n worker1@staging -A circle_back.celery:app --pidfile=/tmp/circle-back-celery-single.pid --beat --logfile=/tmp/circle-back-celery-single.log "-l INFO"

"""

"""
celery multi start single-worker --pidfile=/tmp/circle-back-celery-single.pid  -A project.celery:app --beat --logfile = /home/ruhshan/celery.log "-l INFO"
"""
