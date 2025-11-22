# backend/app/tasks/recipe_tasks.py
"""
Celery tasks for recipe search.

This module moves the expensive ontology/SPARQL queries to background
Celery workers.
"""

import logging
from typing import Any, Dict

from owlready2 import get_ontology
from backend.celery_config import celery
from backend.config import get_config
from backend.app.services.recipe_service import RecipeService

logger = logging.getLogger(__name__)


# cache na poziomie workera, żeby nie ładować ontologii przy każdym tasku
_ontology = None


def _get_ontology_for_tasks():
    """
    Lazily load ontology in Celery worker process.

    This keeps the task stateless from the caller perspective:
    the only inputs are function arguments, ontology is read-only.
    """
    global _ontology
    if _ontology is None:
        config = get_config()
        if not config.ONTOLOGY_URL:
            raise RuntimeError("ONTOLOGY_URL is not configured")
        logger.info(f"[Celery] Loading ontology from {config.ONTOLOGY_URL}")
        _ontology = get_ontology(config.ONTOLOGY_URL).load()
        logger.info("[Celery] Ontology loaded successfully in worker")
    return _ontology


@celery.task(name="recipes.search_recipes", bind=True)
def search_recipes_async(
    self,
    filters: Dict[str, Any],
    page: int,
    per_page: int,
) -> Dict[str, Any]:
    """
    Asynchronous recipe search task.

    Returns a JSON-serializable dict with recipes and pagination metadata.
    
    Idempotent, stateless task:
    - input fully determined by arguments
    - ontology loaded read-only
    - no DB/file writes, no Flask globals
    """
    ontology = _get_ontology_for_tasks()
    service = RecipeService(ontology)

    recipes, total_count = service.get_recipes(filters, page, per_page)

    return {
        "recipes": recipes,
        "page": page,
        "per_page": per_page,
        "total": total_count,
    }
