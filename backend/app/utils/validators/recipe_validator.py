"""
Request parameter validation for recipe endpoints.

This module provides validation functions for all recipe filter parameters,
ensuring data types, ranges, and formats are correct before processing.
"""

import json
from typing import Dict, List, Tuple, Any, Optional
from flask import current_app


class ValidationError(Exception):
    """Custom exception for validation errors."""
    
    def __init__(self, errors: Dict[str, List[str]]):
        self.errors = errors
        super().__init__("Validation failed")


def validate_positive_number(
    value: Any,
    field_name: str,
    allow_zero: bool = False
) -> Tuple[Optional[float], Optional[str]]:
    """
    Validate that a value is a positive number.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        allow_zero: Whether to allow zero as a valid value
    
    Returns:
        Tuple of (validated_value, error_message)
    """
    if value is None or value == '':
        return None, None
    
    try:
        num = float(value)
        if num < 0:
            return None, f"{field_name} must be non-negative"
        if not allow_zero and num == 0:
            return None, f"{field_name} must be greater than zero"
        return num, None
    except (ValueError, TypeError):
        return None, f"{field_name} must be a valid number"


def validate_integer(
    value: Any,
    field_name: str,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None
) -> Tuple[Optional[int], Optional[str]]:
    """
    Validate that a value is an integer within an optional range.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
    
    Returns:
        Tuple of (validated_value, error_message)
    """
    if value is None or value == '':
        return None, None
    
    try:
        num = int(value)
        if min_val is not None and num < min_val:
            return None, f"{field_name} must be at least {min_val}"
        if max_val is not None and num > max_val:
            return None, f"{field_name} must be at most {max_val}"
        return num, None
    except (ValueError, TypeError):
        return None, f"{field_name} must be a valid integer"


def validate_boolean(
    value: Any,
    field_name: str
) -> Tuple[Optional[bool], Optional[str]]:
    """
    Validate that a value is a boolean.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (validated_value, error_message)
    """
    if value is None or value == '':
        return None, None
    
    if isinstance(value, bool):
        return value, None
    
    if isinstance(value, str):
        if value.lower() in ('true', '1', 'yes', 'on'):
            return True, None
        elif value.lower() in ('false', '0', 'no', 'off'):
            return False, None
    
    return None, f"{field_name} must be a boolean value (true/false)"


def validate_meal_type(value: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Validate that a meal type is one of the known types.
    
    Args:
        value: Meal type value to validate
    
    Returns:
        Tuple of (validated_value, error_message)
    """
    if value is None or value == '':
        return None, None
    
    valid_types = current_app.config.get('VALID_MEAL_TYPES', ['Breakfast', 'Lunch', 'Dinner'])
    
    if value not in valid_types:
        return None, f"meal_type must be one of: {', '.join(valid_types)}"
    
    return value, None


def validate_ingredients(value: str) -> Tuple[Optional[List[str]], Optional[str]]:
    """
    Validate and parse ingredients parameter.
    
    Args:
        value: Ingredients value (JSON string or comma-separated)
    
    Returns:
        Tuple of (validated_list, error_message)
    """
    if value is None or value == '':
        return None, None
    
    # Try parsing as JSON first
    if value.startswith('['):
        try:
            ingredients = json.loads(value)
            if not isinstance(ingredients, list):
                return None, "ingredients must be a list"
            if not all(isinstance(i, str) for i in ingredients):
                return None, "all ingredients must be strings"
            return ingredients, None
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON format for ingredients: {str(e)}"
    
    # Otherwise treat as comma-separated string
    ingredients = [i.strip() for i in value.split(',') if i.strip()]
    return ingredients, None


def validate_recipe_filters(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate all recipe filter parameters.
    
    Args:
        filters: Dictionary of filter parameters from request
    
    Returns:
        Dictionary of validated and normalized filters
    
    Raises:
        ValidationError: If any validation fails
    """
    errors = {}
    validated = {}
    
    # Validate numeric filters (support both old and new naming)
    nutrient_params = [
        ('calories', 'Calories'),
        ('protein', 'Protein'),
        ('fat', 'Fat'),
        ('carbohydrates', 'Carbohydrates')
    ]
    
    for param, display_name in nutrient_params:
        # Support both old naming (bigger/smaller) and new naming (min/max)
        for suffix, new_suffix in [('bigger', 'min'), ('smaller', 'max')]:
            old_key = f"{param}_{suffix}"
            new_key = f"{param}_{new_suffix}"
            
            # Check both old and new parameter names
            value = filters.get(old_key) or filters.get(new_key)
            
            if value is not None:
                val, err = validate_positive_number(value, f"{display_name} {suffix}")
                if err:
                    errors[old_key] = [err]
                elif val is not None:
                    validated[old_key] = val  # Keep old naming internally for now
    
    # Validate time
    if 'time' in filters:
        val, err = validate_positive_number(filters['time'], 'Time')
        if err:
            errors['time'] = [err]
        elif val is not None:
            validated['time'] = val
    
    # Validate difficulty
    if 'difficulty' in filters:
        min_diff = current_app.config.get('MIN_DIFFICULTY', 1)
        max_diff = current_app.config.get('MAX_DIFFICULTY', 3)
        val, err = validate_integer(filters['difficulty'], 'Difficulty', min_diff, max_diff)
        if err:
            errors['difficulty'] = [err]
        elif val is not None:
            validated['difficulty'] = val
    
    # Validate booleans
    for bool_field in ['vegan', 'vegetarian']:
        if bool_field in filters:
            val, err = validate_boolean(filters[bool_field], bool_field.capitalize())
            if err:
                errors[bool_field] = [err]
            elif val is not None:
                validated[bool_field] = val
    
    # Validate meal type
    if 'meal_type' in filters:
        val, err = validate_meal_type(filters['meal_type'])
        if err:
            errors['meal_type'] = [err]
        elif val is not None:
            validated['meal_type'] = val
    
    # Validate ingredients
    if 'ingredients' in filters:
        val, err = validate_ingredients(filters['ingredients'])
        if err:
            errors['ingredients'] = [err]
        elif val is not None:
            validated['ingredients'] = val
    
    # Validate pagination parameters
    if 'page' in filters:
        val, err = validate_integer(filters['page'], 'Page', min_val=1)
        if err:
            errors['page'] = [err]
        elif val is not None:
            validated['page'] = val
    
    if 'per_page' in filters:
        max_page_size = current_app.config.get('MAX_PAGE_SIZE', 100)
        val, err = validate_integer(filters['per_page'], 'Per page', min_val=1, max_val=max_page_size)
        if err:
            errors['per_page'] = [err]
        elif val is not None:
            validated['per_page'] = val
    
    if errors:
        raise ValidationError(errors)
    
    return validated

