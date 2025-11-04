"""
Application factory for Feinschmecker API.

This module provides the Flask application factory pattern for creating
and configuring the API application with proper extensions and blueprints.
"""

import logging
import uuid
from flask import Flask, request, g
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger, swag_from
from owlready2 import get_ontology, default_world

from backend.config import get_config


# Initialize extensions
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[]
)

# Global ontology instance
onto = None


def setup_logging(app):
    """Configure application logging."""
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper())
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=app.config['LOG_FORMAT'],
        datefmt=app.config['LOG_DATE_FORMAT']
    )
    
    # Set Flask logger level
    app.logger.setLevel(log_level)


def load_ontology(app):
    """Load the ontology at application startup."""
    global onto
    
    try:
        app.logger.info(f"Loading ontology from {app.config['ONTOLOGY_URL']}")
        onto = get_ontology(app.config['ONTOLOGY_URL']).load()
        app.logger.info("Ontology loaded successfully")
        return onto
    except Exception as e:
        app.logger.error(f"Failed to load ontology: {str(e)}")
        raise


def create_app(config_name=None):
    """
    Application factory for creating Flask app instances.
    
    Args:
        config_name: Configuration environment name ('development', 'production', 'testing')
                    If None, uses FLASK_ENV environment variable
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         methods=app.config['CORS_METHODS'],
         allow_headers=app.config['CORS_ALLOW_HEADERS'])
    
    cache.init_app(app)
    
    if app.config['RATELIMIT_ENABLED']:
        limiter.init_app(app)
        app.logger.info(f"Rate limiting enabled: {app.config['RATELIMIT_DEFAULT']}")
    
    # Initialize Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Feinschmecker API",
            "description": "RESTful API for querying recipe data from an OWL/RDF knowledge graph. "
                         "Supports advanced filtering by nutritional values, dietary restrictions, "
                         "ingredients, cooking time, and difficulty level.",
            "version": app.config['API_VERSION'],
            "contact": {
                "name": "Feinschmecker Team"
            }
        },
        "host": "127.0.0.1:5000",
        "basePath": "/",
        "schemes": ["http"],
        "consumes": ["application/json"],
        "produces": ["application/json"]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    app.logger.info("Swagger documentation initialized at /apidocs/")
    
    # Load ontology
    with app.app_context():
        load_ontology(app)
    
    # Request ID middleware
    @app.before_request
    def before_request():
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    
    # Inject request ID into log records
    old_factory = logging.getLogRecordFactory()
    
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.request_id = getattr(g, 'request_id', 'N/A')
        return record
    
    logging.setLogRecordFactory(record_factory)
    
    # Register blueprints
    from backend.app.api import api_bp
    app.register_blueprint(api_bp)
    
    # Root endpoint
    @app.route('/')
    @swag_from('api/swagger_specs/index.yml')
    def index():
        return {
            'message': 'Welcome to the Feinschmecker API!',
            'version': app.config['API_VERSION'],
            'endpoints': {
                'recipes': '/recipes'
            }
        }
    
    app.logger.info(f"Feinschmecker API initialized in {config_name or 'default'} mode")
    
    return app


def get_ontology():
    """
    Get the loaded ontology instance.
    
    Returns:
        The loaded ontology object
    """
    return onto

