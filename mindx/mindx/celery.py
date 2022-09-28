import os


from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mindx.settings")
app = Celery("mindx")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# create scheduler task with crontab every minute to send report to admin
# create crontab run every beginning of monday and wednesday
app.conf.beat_schedule = {
    "send-report-every-monday-and-wednesday": {
        "task": "unity.tasks.report_scheduler",
        "schedule": crontab(minute=0, hour=0, day_of_week="mon,wed"),
    },
}
