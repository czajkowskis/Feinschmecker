# backend/app/tasks/recipe_tasks.py
"""
Celery tasks for recipe search.

This module moves the expensive ontology/SPARQL queries to background
Celery workers.
"""

import logging
from typing import Any, Dict
import time
from owlready2 import get_ontology
from celery.exceptions import SoftTimeLimitExceeded
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


# typy błędów, które traktujemy jako „chwilowe” i warto spróbować ponownie
TRANSIENT_EXCEPTIONS = (
    TimeoutError,
    ConnectionError,
    OSError,
)


@celery.task(
    name="recipes.search_recipes",
    bind=True,
    max_retries=3,  # maksymalnie 3 próby
)
def search_recipes_async(
    self,
    filters: Dict[str, Any],
    page: int,
    per_page: int,
) -> Dict[str, Any]:
    """
    Asynchronous recipe search task with retries and logging.

    Returns a JSON-serializable dict with recipes and pagination metadata.

    Retries:
    - for TRANSIENT_EXCEPTIONS: exponential backoff, max 3 attempts
    """
    try:
        logger.info(
            "[Celery] Starting recipe search task "
            f"(task_id={self.request.id}, page={page}, per_page={per_page})"
        )
        
        
        # === TEST HOOKS (DEV ONLY) ===
        # 1) wymuszenie chwilowego błędu -> sprawdzamy retry
        # if filters.get("force_transient_error") == "1":
        #     raise TimeoutError("Simulated transient error for retry testing")

        # # 2) wymuszenie timeoutu -> sprawdzamy SoftTimeLimitExceeded
        # if filters.get("force_soft_timeout") == "1":
        #     # śpimy dłużej niż soft_time_limit (20s), żeby Celery zabił task
        #     time.sleep(25)
        # === KONIEC TEST HOOKS ===
        
        
        
        ontology = _get_ontology_for_tasks()
        service = RecipeService(ontology)

        recipes, total_count = service.get_recipes(filters, page, per_page)

        logger.info(
            "[Celery] Recipe search completed "
            f"(task_id={self.request.id}, total={total_count})"
        )

        return {
            "recipes": recipes,
            "page": page,
            "per_page": per_page,
            "total": total_count,
        }

    except TRANSIENT_EXCEPTIONS as exc:
        # FEIN-68 + FEIN-69: log i retry przy chwilowych problemach
        retry_no = self.request.retries + 1
        # prosty exponential backoff: 2,4,8 sekund (max 30)
        countdown = min(2 ** retry_no, 30)

        logger.warning(
            "[Celery] Transient error in recipe search "
            f"(task_id={self.request.id}, retry={retry_no}/{self.max_retries}, "
            f"countdown={countdown}s): {exc}"
        )

        # jeśli przekroczymy max_retries, Celery podbije MaxRetriesExceededError
        raise self.retry(exc=exc, countdown=countdown)

    except SoftTimeLimitExceeded as exc:
        # czas taska się skończył – logujemy i zwracamy FAILURE
        logger.error(
            "[Celery] Soft time limit exceeded in recipe search "
            f"(task_id={self.request.id}): {exc}",
            exc_info=True,
        )
        # nie retryujemy, bo już przekroczyliśmy limit czasu
        raise

    except Exception as exc:
        # FEIN-69: logowanie wszystkich innych błędów jako permanent failure
        logger.error(
            "[Celery] Permanent failure in recipe search "
            f"(task_id={self.request.id}): {exc}",
            exc_info=True,
        )
        # nie retry – to raczej bug w logice niż chwilowy problem
        raise
