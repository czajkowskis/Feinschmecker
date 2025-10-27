# Scripts

The scripts directory contains utility scripts for data processing, scraping, and conversion.

## Purpose

This directory holds Python scripts and Jupyter notebooks used for data preparation, web scraping, and knowledge graph generation.

## Structure

- **`Feinschmecker.ipynb`** - Jupyter notebook for ontology creation and knowledge graph generation
- **`utils.py`** - Helper functions for data parsing and processing

## Key Files

### Feinschmecker.ipynb
- Jupyter notebook for creating the OWL ontology
- Defines classes, properties, and relationships using owlready2
- Includes factory functions for creating ontology classes and relations
- Used to generate the RDF knowledge graph from structured recipe data

### utils.py
- Collection of utility functions for data processing:
  - `separate_nutrition()` - Parses nutrition information from text
  - `get_time()` - Extracts cooking time from formatted text
  - `parse_ingredients()` - Parses ingredient lists into structured data with amounts and units
- Used by the scraper to process raw scraped data

## Related Files

The `utils/scraper.py` file (in the parent utils directory) works with these scripts to:
1. Scrape recipe data from BBC Good Food website
2. Parse raw HTML into structured JSON format
3. Use functions from `utils.py` to process ingredients, nutrition, and time data

## Workflow

Typical data processing workflow:
1. Run scraper to collect recipe data from web sources
2. Parse and clean data using utilities
3. Convert processed data to RDF using the Jupyter notebook
4. Validate RDF output against ontology schema

## Future Enhancements

Planned additions to this directory:
- Data validation s
- Batch processing scripts for large datasets

