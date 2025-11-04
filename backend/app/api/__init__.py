"""
API Blueprint for Feinschmecker recipe endpoints.

This module defines the API routes and registers them as a Flask blueprint.
"""

from flask import Blueprint

# Create API blueprint
api_bp = Blueprint('api', __name__)

# Import routes to register them with the blueprint
from backend.app.api import recipes

