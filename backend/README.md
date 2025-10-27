# Backend

The backend directory contains the Flask API server and core business logic for Feinschmecker.

## Purpose

This directory provides the RESTful API that handles recipe queries against the OWL/RDF knowledge graph. It uses SPARQL queries to filter recipes based on various criteria including nutritional values, dietary preferences, ingredients, cooking time, difficulty, and meal type.

## Structure

- **`app/`** - Application module structure (intended for future modularization)
  - `api/` - API endpoint definitions (empty, intended for organized route handling)
  - `services/` - Business logic services (empty, intended for separating concerns from routes)
  - `tasks/` - Background task definitions (empty, intended for Celery async task processing)
  - `utils/` - Utility modules
    - `parsers/` - Data parsing utilities (empty, intended for format conversions)
    - `validators/` - Data validation utilities (empty, intended for input validation)
- **`config.py`** - Configuration file for the Flask application (currently empty)
- **`requirements.txt`** - Python dependencies (Flask, Flask-CORS, gunicorn, owlready2)
- **`website.py`** - Main Flask application with SPARQL query builder and recipe filtering logic


## Dependencies

- `Flask` - Web framework
- `Flask-CORS` - Cross-origin resource sharing support
- `owlready2` - OWL ontology and SPARQL query processing
- `gunicorn` - WSGI HTTP server for production deployment

## Future Enhancements

Based on the project roadmap, this directory is intended to support:
- Parallel graph search with Celery task queue
- Separation of ontology and knowledge graph data
- Support for multiple graph formats (RDF/XML, JSON-LD, Turtle, N-Triples)
- Update mechanisms for ontology and graph versioning
- Enhanced query capabilities with SPARQL endpoint
- Performance optimization for large graphs
