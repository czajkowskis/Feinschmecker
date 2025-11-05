#!/usr/bin/python3.11

"""
Feinschmecker API - Main application entry point.

This module provides the Flask application instance using the application
factory pattern. The application is configured based on the FLASK_ENV
environment variable.

Feinschmecker, 2024-12-20
Updated: 2025-11-04 - Refactored with improved architecture
"""

import os
import sys

# Add parent directory to path to import backend module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app

# Create application instance
app = create_app()

if __name__ == "__main__":
    # Run the application
    # In production, use gunicorn or another WSGI server instead
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", 5000)),
        debug=app.config["DEBUG"],
    )
