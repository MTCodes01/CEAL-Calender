"""
Celery configuration for ceal_calendar project.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ceal_calendar.settings')

app = Celery('ceal_calendar')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'run-notifications-every-minute': {
        'task': 'notifications.tasks.dispatch_notifications',
        'schedule': crontab(minute='*'),  # Every minute
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
