# Data

The data directory contains the knowledge graph data files used by Feinschmecker.

## Purpose

This directory stores the structured recipe data in various formats. The knowledge graph represents recipes, ingredients, nutritional information, and relationships between entities according to the Feinschmecker ontology.

## Structure

- **`feinschmecker.rdf`** - Main RDF knowledge graph containing recipe instances in OWL/RDF format
- **`recipes.json`** - JSON format representation of scraped recipe data

## Key Files

### feinschmecker.rdf
- RDF/XML format knowledge graph
- Loaded from remote URL: `https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker/feinschmecker.rdf`
- Contains recipe instances with:
  - Ingredients with amounts
  - Nutritional values (calories, protein, fat, carbohydrates)
  - Cooking time requirements
  - Difficulty levels
  - Meal type classifications (Breakfast, Lunch, Dinner)
  - Dietary flags (vegan, vegetarian)
  - Instructions and metadata (author, source, links)
- Uses custom Feinschmecker namespace
- Created by: Jaron Sprute, Bhuvenesh Verma, Szymon Czajkowski
- Current version: 1.1

### recipes.json
- JSON array format for raw recipe data
- Used for data processing and conversion workflows
- Contains structured recipe information scraped from BBC Good Food
- Format includes: title, image, source URL, cooking time, ingredients, instructions, nutrients, author, dietary flags, and meal type

## Usage

The RDF file is the primary data source and is loaded by the backend Flask application using owlready2 for SPARQL querying. The JSON file may be used for data processing scripts or as a format for conversion into the knowledge graph.

## Future Enhancements

Based on the project roadmap, this directory is intended to support:
- Multiple knowledge graph datasets in different formats
- Version management for recipe data updates
- Sample datasets for testing and development
- Data validation scripts
