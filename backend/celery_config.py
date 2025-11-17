import os
from celery import Celery

# Use Docker service name if available, fallback to localhost
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

celery = Celery(
    "feinschmecker",
    broker=REDIS_URL,
    backend=RESULT_BACKEND,
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    enable_utc=True,
    timezone="Europe/Warsaw",
    # Task discovery - auto-discover tasks from app.tasks module
    imports=("backend.app.tasks",),
    # Task routing
    task_routes={
        "backend.app.tasks.*": {"queue": "default"},
    },
)
