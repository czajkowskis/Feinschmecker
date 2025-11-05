"""
Response formatting utilities for standardized API responses.

This module provides helper functions for creating consistent JSON responses
with proper structure, pagination metadata, and error handling.
"""

from typing import Any, Dict, List, Optional
from flask import jsonify
import math


def success_response(
    data: Any,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    total: Optional[int] = None,
    message: Optional[str] = None
) -> tuple:
    """
    Create a standardized success response.
    
    Args:
        data: The response data (list of items or single item)
        page: Current page number (for paginated responses)
        per_page: Items per page (for paginated responses)
        total: Total number of items (for paginated responses)
        message: Optional success message
    
    Returns:
        Tuple of (response_dict, status_code)
    """
    response = {'data': data}
    
    # Add pagination metadata if provided
    if page is not None and per_page is not None and total is not None:
        total_pages = math.ceil(total / per_page) if per_page > 0 else 0
        response['meta'] = {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }
    
    if message:
        response['message'] = message
    
    return jsonify(response), 200


def error_response(
    message: str,
    code: str = 'ERROR',
    details: Optional[List[str]] = None,
    status_code: int = 400
) -> tuple:
    """
    Create a standardized error response.
    
    Args:
        message: Human-readable error message
        code: Machine-readable error code
        details: Optional list of detailed error messages
        status_code: HTTP status code
    
    Returns:
        Tuple of (response_dict, status_code)
    """
    error = {
        'code': code,
        'message': message
    }
    
    if details:
        error['details'] = details
    
    return jsonify({'error': error}), status_code


def validation_error_response(
    errors: Dict[str, List[str]],
    message: str = 'Validation failed'
) -> tuple:
    """
    Create a standardized validation error response.
    
    Args:
        errors: Dictionary mapping field names to lists of error messages
        message: General validation error message
    
    Returns:
        Tuple of (response_dict, status_code)
    """
    details = []
    for field, messages in errors.items():
        for msg in messages:
            details.append(f"{field}: {msg}")
    
    return error_response(
        message=message,
        code='VALIDATION_ERROR',
        details=details,
        status_code=400
    )


def not_found_response(resource: str = 'Resource') -> tuple:
    """
    Create a standardized 404 not found response.
    
    Args:
        resource: Name of the resource that was not found
    
    Returns:
        Tuple of (response_dict, status_code)
    """
    return error_response(
        message=f'{resource} not found',
        code='NOT_FOUND',
        status_code=404
    )


def internal_error_response(message: str = 'Internal server error') -> tuple:
    """
    Create a standardized 500 internal error response.
    
    Args:
        message: Error message
    
    Returns:
        Tuple of (response_dict, status_code)
    """
    return error_response(
        message=message,
        code='INTERNAL_ERROR',
        status_code=500
    )

