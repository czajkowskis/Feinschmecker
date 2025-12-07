"""
Celery task definitions for Feinschmecker.

This module contains background task definitions for async processing,
including parallel graph search operations.
"""

from backend.celery_config import celery  # keeps 'celery' in namespace

# Import concrete task modules so their @celery.task decorators register tasks
from .recipe_tasks import search_recipes_async  # noqa: F401

__all__ = ["search_recipes_async"]