import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coinmena.settings")

app = Celery("coinmena")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "update_quotes_task-every-hour": {
        "task": "quotes.update_quotes_task",
        "schedule": 60 * 60,
        "args": (settings.ALPHAVANTAGE_LOAD_CURRENCY_EXCHANGE_RATE_PAIRS,),
        "options": {
            "expires": 60 * 60,
            "retry": True,
            "retry_policy": dict(
                max_retries=None, interval_start=3, interval_step=1, interval_max=6
            ),
        },
    },
}
