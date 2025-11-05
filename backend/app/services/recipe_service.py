"""
Business logic for recipe operations.

This module handles the core recipe querying logic, data transformation,
and interaction with the ontology.
"""

import logging
import time
from typing import Dict, Any, List, Tuple
from owlready2 import default_world

from backend.app.services.query_builder import RecipeQueryBuilder, build_count_query

logger = logging.getLogger(__name__)


class RecipeService:
    """Service class for recipe operations."""
    
    def __init__(self, ontology):
        """
        Initialize the recipe service.
        
        Args:
            ontology: Loaded ontology instance
        """
        self.ontology = ontology
        self.query_builder = RecipeQueryBuilder()
    
    def get_recipes(
        self,
        filters: Dict[str, Any],
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Retrieve recipes based on filters with pagination.
        
        Args:
            filters: Dictionary of filter parameters
            page: Page number (1-indexed)
            per_page: Number of items per page
        
        Returns:
            Tuple of (list of recipe dictionaries, total count)
        """
        start_time = time.time()
        
        # Calculate pagination offset
        offset = (page - 1) * per_page
        
        # Get total count (for pagination metadata)
        total_count = self._get_total_count(filters)
        logger.info(f"Found {total_count} total recipes matching filters")
        
        # Build and execute main query
        query = self.query_builder.build_query(filters, limit=per_page, offset=offset)
        
        try:
            with self.ontology:
                recipe_list = list(default_world.sparql(query))
        except Exception as e:
            logger.error(f"SPARQL query failed: {str(e)}")
            raise
        
        # Transform results to dictionaries
        recipes = self._transform_results(recipe_list)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Retrieved {len(recipes)} recipes in {elapsed_time:.3f}s")
        
        if elapsed_time > 1.0:
            logger.warning(f"Slow query detected: {elapsed_time:.3f}s")
        
        return recipes, total_count
    
    def _get_total_count(self, filters: Dict[str, Any]) -> int:
        """
        Get the total count of recipes matching the filters.
        
        Args:
            filters: Dictionary of filter parameters
        
        Returns:
            Total number of matching recipes
        """
        count_query = build_count_query(filters)
        
        try:
            with self.ontology:
                result = list(default_world.sparql(count_query))
                if result and len(result) > 0:
                    return int(result[0][0])
                return 0
        except Exception as e:
            logger.error(f"Count query failed: {str(e)}")
            # Fall back to returning 0 if count fails
            return 0
    
    def _transform_results(self, recipe_list: List[tuple]) -> List[Dict[str, Any]]:
        """
        Transform SPARQL query results into recipe dictionaries.
        
        Args:
            recipe_list: List of tuples from SPARQL query
        
        Returns:
            List of recipe dictionaries with proper types
        """
        field_order = [
            "name", "link", "image_link", "instructions", "ingredients",
            "vegan", "vegetarian", "meal_type", "time", "difficulty",
            "calories", "protein", "fat", "carbohydrates",
            "author", "source_name", "source_link"
        ]
        
        recipes = []
        for result in recipe_list:
            recipe = {}
            
            # Map result tuple to dictionary
            for i, field in enumerate(field_order):
                if i < len(result):
                    recipe[field] = result[i]
            
            # Transform data types and formats
            recipe = self._normalize_recipe(recipe)
            
            recipes.append(recipe)
        
        return recipes
    
    def _normalize_recipe(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize recipe data types and formats.
        
        Args:
            recipe: Raw recipe dictionary from SPARQL
        
        Returns:
            Normalized recipe dictionary
        """
        # Parse instructions from string representation of list
        if 'instructions' in recipe and isinstance(recipe['instructions'], str):
            recipe['instructions'] = self._parse_instructions(recipe['instructions'])
        
        # Parse ingredients from concatenated string
        if 'ingredients' in recipe and isinstance(recipe['ingredients'], str):
            recipe['ingredients'] = recipe['ingredients'].split('#')
        
        # Convert boolean strings to actual booleans
        for bool_field in ['vegan', 'vegetarian']:
            if bool_field in recipe:
                recipe[bool_field] = self._parse_boolean(recipe[bool_field])
        
        # Convert numeric fields to proper types
        if 'time' in recipe:
            recipe['time'] = self._parse_number(recipe['time'])
        
        if 'difficulty' in recipe:
            recipe['difficulty'] = self._parse_number(recipe['difficulty'])
        
        for nutrient in ['calories', 'protein', 'fat', 'carbohydrates']:
            if nutrient in recipe:
                recipe[nutrient] = self._parse_number(recipe[nutrient])
        
        return recipe
    
    def _parse_instructions(self, instructions_str: str) -> List[str]:
        """
        Parse instructions from string representation.
        
        Args:
            instructions_str: String representation of instructions list
        
        Returns:
            List of instruction steps
        """
        # Remove outer brackets and quotes
        cleaned = instructions_str.strip("[]'\"")
        
        # Split by delimiter
        steps = cleaned.split("', '")
        
        # Clean up each step
        cleaned_steps = []
        for step in steps:
            # Remove "step X" prefix and leading digits
            step = step.lstrip("step ").lstrip("0123456789").strip()
            if step:
                cleaned_steps.append(step)
        
        return cleaned_steps
    
    def _parse_boolean(self, value: Any) -> bool:
        """
        Parse a value into a boolean.
        
        Args:
            value: Value to parse
        
        Returns:
            Boolean value
        """
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes')
        return bool(value)
    
    def _parse_number(self, value: Any) -> float:
        """
        Parse a value into a number.
        
        Args:
            value: Value to parse
        
        Returns:
            Numeric value
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

