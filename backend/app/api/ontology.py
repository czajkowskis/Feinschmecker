"""
Ontology management API endpoints.

This module provides endpoints for uploading and managing knowledge graph files.
Supports multiple RDF formats (RDF/XML, Turtle, N3, N-Triples, JSON-LD) and
converts them to a unified RDF/XML format.
"""

import os
import logging
from werkzeug.utils import secure_filename
from flask import request, current_app
from rdflib import Graph
from owlready2 import get_ontology, default_world

from backend.app.api import api_bp
from backend.app import limiter
from backend.app.utils.response import (
    success_response,
    validation_error_response,
    error_response,
)

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'rdf', 'owl', 'ttl', 'n3', 'nt', 'jsonld', 'xml'}
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    'data',
    'uploads'
)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def detect_format(filename):
    """Detect RDF format from file extension."""
    ext = filename.rsplit('.', 1)[1].lower()
    format_map = {
        'rdf': 'xml',
        'owl': 'xml',
        'xml': 'xml',
        'ttl': 'turtle',
        'n3': 'n3',
        'nt': 'nt',
        'jsonld': 'json-ld'
    }
    return format_map.get(ext, 'xml')


def reload_ontology(ontology_file):
    """
    Reload the application ontology from a new file.
    
    Args:
        ontology_file: Path to the new ontology file
    
    Returns:
        Tuple of (success: bool, error_message: str)
    """
    try:
        # Clear existing ontology
        default_world.ontologies.clear()
        
        # Load new ontology
        logger.info(f"Loading new ontology from {ontology_file}")
        file_url = f"file://{ontology_file.replace(os.sep, '/')}"
        new_onto = get_ontology(file_url).load()
        
        # Update global ontology instance
        import backend.app as app_module
        app_module.onto = new_onto
        
        logger.info("Ontology reloaded successfully")
        return True, None
        
    except Exception as e:
        error_msg = f"Error reloading ontology: {str(e)}"
        logger.error(error_msg)
        return False, error_msg


def convert_to_rdfxml(input_file, output_file, input_format):
    """
    Convert RDF file to RDF/XML format (better supported by OWLReady2).
    
    Args:
        input_file: Path to input RDF file
        output_file: Path to output RDF/XML file
        input_format: Source RDF format (xml, turtle, n3, nt, json-ld)
    
    Returns:
        Tuple of (success: bool, triple_count: int, error_message: str)
    """
    try:
        # Create RDF graph
        g = Graph()
        
        # Parse input file
        logger.info(f"Parsing {input_file} as {input_format}")
        g.parse(input_file, format=input_format)
        
        triple_count = len(g)
        logger.info(f"Parsed {triple_count} triples")
        
        # Serialize to RDF/XML (best supported by OWLReady2)
        logger.info(f"Converting to RDF/XML format: {output_file}")
        g.serialize(destination=output_file, format='xml')
        
        logger.info(f"Successfully converted to RDF/XML")
        return True, triple_count, None
        
    except Exception as e:
        error_msg = f"Error converting to RDF/XML: {str(e)}"
        logger.error(error_msg)
        return False, 0, error_msg


@api_bp.route("/ontology/upload", methods=["POST"])
@limiter.limit("10 per hour")  # Limit uploads to prevent abuse
def upload_ontology():
    """
    Upload and replace the knowledge graph.
    
    Accepts RDF files in various formats (RDF/XML, Turtle, N3, N-Triples, JSON-LD)
    and converts them to RDF/XML format before loading (best supported by OWLReady2).
    
    Form Data:
        file: The RDF file to upload
        target_format: (optional) Target format, default is 'xml' (RDF/XML)
    
    Returns:
        JSON response with upload status and metadata
        
    Example Success Response:
        {
            "data": {
                "filename": "uploaded_ontology.rdf",
                "format": "xml",
                "path": "/path/to/file.rdf",
                "triple_count": 1523
            },
            "message": "Knowledge graph uploaded and loaded successfully"
        }
    
    Example Error Response:
        {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "No file provided"
            }
        }
    """
    logger.info("Received ontology upload request")
    
    # Check if file is present
    if 'file' not in request.files:
        logger.warning("No file in request")
        return validation_error_response([{
            'field': 'file',
            'message': 'No file provided'
        }])
    
    file = request.files['file']
    
    if file.filename == '':
        logger.warning("Empty filename")
        return validation_error_response([{
            'field': 'file',
            'message': 'No file selected'
        }])
    
    if not allowed_file(file.filename):
        logger.warning(f"Invalid file type: {file.filename}")
        return validation_error_response([{
            'field': 'file',
            'message': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
        }])
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)
        logger.info(f"File saved to {input_path}")
        
        # Detect format
        input_format = detect_format(filename)
        logger.info(f"Detected format: {input_format}")
        
        # Convert to RDF/XML (better OWLReady2 support)
        rdf_filename = filename.rsplit('.', 1)[0] + '.rdf'
        rdf_path = os.path.join(UPLOAD_FOLDER, rdf_filename)
        
        success, triple_count, error_msg = convert_to_rdfxml(input_path, rdf_path, input_format)
        
        if not success:
            return error_response(
                message=error_msg or "Failed to convert file to RDF/XML format",
                code="CONVERSION_ERROR",
                status_code=500
            )
        
        # Reload ontology
        success, error_msg = reload_ontology(rdf_path)
        
        if not success:
            return error_response(
                message=error_msg or "Failed to reload ontology",
                code="RELOAD_ERROR",
                status_code=500
            )
        
        # Success response
        return success_response(
            data={
                'filename': rdf_filename,
                'format': 'xml',
                'path': rdf_path,
                'triple_count': triple_count
            },
            message="Knowledge graph uploaded and loaded successfully"
        )
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}", exc_info=True)
        return error_response(
            message=f"Error processing upload: {str(e)}",
            code="UPLOAD_ERROR",
            status_code=500
        )


@api_bp.route("/ontology/info", methods=["GET"])
def get_ontology_info():
    """
    Get information about the currently loaded ontology.
    
    Returns:
        JSON response with ontology metadata
    """
    try:
        from backend.app import get_ontology_instance
        
        onto = get_ontology_instance()
        
        if not onto:
            return error_response(
                message="No ontology loaded",
                code="NO_ONTOLOGY",
                status_code=500
            )
        
        # Collect basic stats
        classes = list(onto.classes())
        individuals = list(onto.individuals())
        properties = list(onto.properties())
        
        return success_response(
            data={
                'base_iri': onto.base_iri,
                'name': onto.name,
                'class_count': len(classes),
                'individual_count': len(individuals),
                'property_count': len(properties)
            },
            message="Ontology information retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error getting ontology info: {str(e)}", exc_info=True)
        return error_response(
            message=f"Error getting ontology info: {str(e)}",
            code="INFO_ERROR",
            status_code=500
        )
