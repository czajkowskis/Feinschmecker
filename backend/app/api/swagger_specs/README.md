# Swagger API Specifications

This directory contains OpenAPI/Swagger specification files in YAML format for the Feinschmecker API endpoints.

## Structure

Each endpoint has its own YAML file containing:
- Parameter definitions
- Request/response schemas
- Example values
- Error responses

## Files

- `index.yml` - Root endpoint (`/`) specification
- `recipes_get.yml` - Recipe search endpoint (`/recipes`) specification

## Usage

These YAML files are referenced in the endpoint decorators using `@swag_from()`:

```python
@app.route('/recipes')
@swag_from('swagger_specs/recipes_get.yml')
def get_recipes():
    # endpoint implementation
```

## Benefits

- **Cleaner Code**: Separates documentation from implementation
- **Easier Maintenance**: Update docs without touching Python code
- **Better Organization**: All API specs in one location
- **Version Control**: Easier to track changes to API documentation

## Adding New Endpoints

1. Create a new YAML file in this directory (e.g., `new_endpoint.yml`)
2. Define the OpenAPI specification following the existing format
3. Reference it in your endpoint using `@swag_from('swagger_specs/new_endpoint.yml')`

## Viewing Documentation

Start the API server and visit: `http://127.0.0.1:5000/apidocs/`

