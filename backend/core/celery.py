import os

from celery import Celery
from celery.schedules import crontab
from celery import shared_task


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery(
    main='core',
    broker='amqp://guest:guest@localhost:5672/',
    backend='redis://127.0.0.1:6379'
)

app.config_from_object(obj='django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # Load task modules from django apps.

app.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'core.celery.add',
        'schedule': 5.0,
        'args': (16, 16)
    },
    'sunday': {
        'task': 'core.celery.test',
        'schedule': crontab(day_of_week='sunday'),
        'args': ('sunday!', ),
    }
}

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Call test('hello') every 2s.
    sender.add_periodic_task(2.0, test.s('hello'), name='add every 2s')

    # Call test('word') every 3s.
    sender.add_periodic_task(3.0, test.s('word'), expires=10)

@shared_task
def test(x):
    print(x)

@shared_task
def add(x, y):
    print(x + y)
