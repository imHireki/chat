import os

from celery import Celery
from celery.schedules import crontab
from celery import shared_task


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery(main='core')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # Load task modules from django apps.

app.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'apps.chat.tasks.add',
        'schedule': 5.0,
        'args': (16, 16)
    },
    'sunday': {
        'task': 'apps.chat.tasks.test',
        'schedule': crontab(day_of_week='wednesday'),
        'args': ('sunday!', ),
    }
}

