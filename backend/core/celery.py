import os

from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery(
    main='core',
    broker='amqp://guest:guest@localhost:5672/',
    backend='redis://127.0.0.1:6379'
)

app.config_from_object(obj='django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # Load task modules from django apps.
