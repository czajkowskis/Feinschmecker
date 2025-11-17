"""
Configuration management for Feinschmecker API.

Provides environment-based configuration for development and production environments.
"""

import os
from pathlib import Path


class Config:
    """Base configuration class with common settings."""
    
    # Base directory
    BASE_DIR = Path(__file__).parent.parent
    
    # Ontology settings
    ONTOLOGY_URL = os.getenv(
        'ONTOLOGY_URL',
        'https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker/feinschmecker.rdf'
    )
    ONTOLOGY_CACHE_DIR = os.getenv('ONTOLOGY_CACHE_DIR', '/tmp/owlready2_cache')
    
    # API settings
    API_TITLE = 'Feinschmecker API'
    API_VERSION = '1.0'
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Timeout settings (in seconds)
    QUERY_TIMEOUT = int(os.getenv('QUERY_TIMEOUT', '30'))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '60'))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    CORS_METHODS = ['GET', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    
    # Cache settings
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))  # 5 minutes
    CACHE_THRESHOLD = 500  # Maximum number of items the cache will store
    
    # Rate limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per minute')
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # Known meal types for validation
    VALID_MEAL_TYPES = ['Breakfast', 'Lunch', 'Dinner']
    
    # Difficulty range
    MIN_DIFFICULTY = 1
    MAX_DIFFICULTY = 3


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    
    # More verbose logging in development
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    
    # Shorter cache timeout for development
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '60'))
    
    # Relaxed rate limiting for development
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '1000 per minute')
    
    # Allow all origins in development, but include Vite dev server
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')


class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    
    # Strict logging in production
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')
    
    # Longer cache timeout for production
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '600'))  # 10 minutes
    
    # Stricter rate limiting for production
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '60 per minute')
    
    # Use Redis for caching in production if available
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'SimpleCache')
    # Default to Docker service name, fallback to localhost
    CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    
    # Specific CORS origins in production (should be set via env var)
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000')


class TestingConfig(Config):
    """Testing environment configuration."""
    
    DEBUG = True
    TESTING = True
    
    # Disable rate limiting for tests
    RATELIMIT_ENABLED = False
    
    # Disable caching for tests
    CACHE_TYPE = 'NullCache'
    
    # Use in-memory ontology for testing
    ONTOLOGY_URL = None  # Can be set to test fixtures


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env_name=None):
    """
    Get configuration object based on environment name.
    
    Args:
        env_name: Environment name ('development', 'production', 'testing')
                 If None, uses FLASK_ENV environment variable or defaults to 'development'
    
    Returns:
        Configuration class for the specified environment
    """
    if env_name is None:
        env_name = os.getenv('FLASK_ENV', 'development')
    
    return config.get(env_name, config['default'])

