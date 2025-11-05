"""
Recipe API endpoints.

This module defines the recipe search endpoint with filtering, pagination,
validation, and caching support.
"""

import logging
from flask import request, current_app
from flasgger import swag_from

from backend.app.api import api_bp
from backend.app import limiter, cache, get_ontology_instance
from backend.app.services.recipe_service import RecipeService
from backend.app.utils.validators.recipe_validator import (
    validate_recipe_filters,
    ValidationError,
)
from backend.app.utils.response import (
    success_response,
    validation_error_response,
    internal_error_response,
)

logger = logging.getLogger(__name__)


def make_cache_key():
    """Generate cache key based on request parameters."""
    # Sort parameters for consistent cache keys
    params = sorted(request.args.items())
    return f"recipes:{str(params)}"


@api_bp.route("/recipes", methods=["GET"])
@limiter.limit(lambda: current_app.config.get("RATELIMIT_DEFAULT", "100 per minute"))
@cache.cached(timeout=None, key_prefix=make_cache_key)  # Use config timeout
@swag_from("swagger_specs/recipes_get.yml")
def get_recipes():
    """
    Retrieve recipes based on filter parameters.

    Query Parameters:
        - ingredients (str): Comma-separated or JSON list of ingredient names
        - vegan (bool): Filter for vegan recipes
        - vegetarian (bool): Filter for vegetarian recipes
        - meal_type (str): Type of meal (Breakfast, Lunch, Dinner)
        - time (int): Maximum preparation time in minutes
        - difficulty (int): Difficulty level (1=easy, 2=moderate, 3=difficult)
        - calories_bigger/calories_min (float): Minimum calories
        - calories_smaller/calories_max (float): Maximum calories
        - protein_bigger/protein_min (float): Minimum protein (grams)
        - protein_smaller/protein_max (float): Maximum protein (grams)
        - fat_bigger/fat_min (float): Minimum fat (grams)
        - fat_smaller/fat_max (float): Maximum fat (grams)
        - carbohydrates_bigger/carbohydrates_min (float): Minimum carbs (grams)
        - carbohydrates_smaller/carbohydrates_max (float): Maximum carbs (grams)
        - page (int): Page number (default: 1)
        - per_page (int): Items per page (default: 20, max: 100)

    Returns:
        JSON response with recipe data and pagination metadata

    Response Format:
        {
            "data": [...],
            "meta": {
                "total": 150,
                "page": 1,
                "per_page": 20,
                "total_pages": 8
            }
        }

    Error Response:
        {
            "error": {
                "code": "ERROR_CODE",
                "message": "Error description",
                "details": [...]
            }
        }
    """
    logger.info(f"Received recipe search request with params: {request.args.to_dict()}")

    try:
        # Get raw filters from request
        raw_filters = request.args.to_dict()

        # Validate and normalize filters
        try:
            validated_filters = validate_recipe_filters(raw_filters)
        except ValidationError as e:
            logger.warning(f"Validation error: {e.errors}")
            return validation_error_response(e.errors)

        # Extract pagination parameters
        page = validated_filters.pop("page", 1)
        per_page = validated_filters.pop(
            "per_page", current_app.config["DEFAULT_PAGE_SIZE"]
        )

        # Get ontology instance
        ontology = get_ontology_instance()
        if ontology is None:
            logger.error("Ontology not loaded")
            return internal_error_response("Service not ready")

        # Create service and fetch recipes
        service = RecipeService(ontology)
        recipes, total_count = service.get_recipes(validated_filters, page, per_page)

        logger.info(
            f"Returning {len(recipes)} recipes (page {page}/{total_count // per_page + 1})"
        )

        return success_response(
            data=recipes, page=page, per_page=per_page, total=total_count
        )

    except Exception as e:
        logger.error(f"Error processing recipe request: {str(e)}", exc_info=True)
        return internal_error_response(
            "An error occurred while processing your request"
        )
