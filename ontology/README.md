# Ontology

The ontology directory is intended to contain the OWL ontology definitions that define the schema for the Feinschmecker knowledge graph.

## Purpose

This directory will store the ontology schema files that define the classes, properties, and relationships used in the Feinschmecker knowledge graph. Separating the ontology (schema) from the knowledge graph (data) enables independent updates and easier maintenance.

## Intended Contents

Currently empty, this directory is planned to include:

- **OWL Schema Files** - Class definitions for Recipe, Ingredient, Author, etc.
- **Object Properties** - Relationships like `has_ingredient`, `authored_by`, `requires_time`
- **Data Properties** - Attributes like `has_recipe_name`, `has_numeric_difficulty`, `amount_of_calories`
- **Annotation Properties** - Metadata about the ontology
- **Version Information** - Semantic versioning for ontology updates

## Current Ontology Status

The ontology schema is currently embedded in the RDF data file (`data/feinschmecker.rdf`). Key classes include:

- **Recipe** - Main entity representing a recipe
- **IngredientWithAmount** - Ingredients with quantities
- **Author** - Recipe authors
- **Source** - Recipe sources/websites
- **Time** - Cooking time requirements
- **Difficulty** - Recipe difficulty levels
- **MealType** - Breakfast, Lunch, Dinner classifications

## Namespace

```
https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker/
```

## Future Enhancements

Based on the project roadmap, this directory will support:

- Separation of ontology schema from instance data
- Version management for ontology updates
- Multiple ontology versions with backward compatibility
- Validation layer to ensure graph data conforms to ontology
- Abstract interfaces for different ontology implementations
- Diff tools to compare ontology versions
- Documentation of schema changes between versions
