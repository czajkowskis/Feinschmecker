# Feinschmecker Ontology Documentation

## Introduction

The Feinschmecker ontology is an OWL-based schema for culinary recipes, defining the structure and relationships that enable a recipe knowledge graph. The ontology has been refactored from a Jupyter notebook into modular Python files for better maintainability and reusability.

The **ontology** defines the schema (classes, properties, constraints), while **knowledge graphs** contain the actual recipe data (individuals/instances) that conform to this schema.

### Purpose

The ontology provides the semantic foundation for recipe knowledge graphs, enabling intelligent search and recommendation. It defines:

**Schema (Ontology)**:
- Classes for recipes, ingredients, authors, nutrients, etc.
- Properties linking and describing these classes
- Constraints ensuring data integrity
- Shared structure for all knowledge graphs

**Use Cases (Knowledge Graphs)**:
- Query recipes by nutritional values, dietary restrictions, meal types
- Filter by difficulty, preparation time, and ingredients
- Analyze relationships between recipes, ingredients, and nutrition
- **Manage data from multiple sources** in separate knowledge graphs
- **Compare and combine** recipes from different sources

### Version Information

- **Current Version**: 1.1
- **Description**: Working ontology with individuals, initial feedback included
- **Namespace**: `https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker/`

### Authors

This ontology was created by:
- Jaron Sprute
- Bhuvenesh Verma
- Szymon Czajkowski

---

## Documentation Structure

This documentation is organized into the following sections:

- **[Architecture](architecture.md)** - Module organization, dependencies, and package structure
- **[Schema](schema.md)** - Complete reference of classes, properties, and constraints
- **[Query API](queries.md)** - Query functions and filtering capabilities
- **[Usage Guide](usage.md)** - Comprehensive examples and patterns
- **[Development](development.md)** - Extending the ontology and available tools

---

## Quick Start

### Basic Setup and Usage (Single Knowledge Graph)

```python
from ontology import kg_onto, load_recipes_from_json

# Load recipe data from JSON file into default KG
load_recipes_from_json('path/to/recipes.json')

# Save knowledge graph to RDF file
kg_onto.save('feinschmecker.rdf')
```

### Multi-Source Setup (Multiple Knowledge Graphs)

```python
from ontology import create_kg, load_recipes_from_json, schema_onto

# Create separate KGs for different sources
kg_bbc = create_kg("bbc")
kg_allrecipes = create_kg("allrecipes")

# Load data into specific KGs
load_recipes_from_json('bbc_recipes.json', target_kg=kg_bbc)
load_recipes_from_json('allrecipes.json', target_kg=kg_allrecipes)

# Save schema (shared) and each KG separately
schema_onto.save('schema.rdf')
kg_bbc.save('kg-bbc.rdf')
kg_allrecipes.save('kg-allrecipes.rdf')
```

### Simple Queries

```python
from ontology import (
    recipesWithMaxCalories,
    recipesWithMinProtein,
    isVegan,
    getDifficulty,
    create_kg
)

# Find low-calorie recipes (≤300 kcal) in default KG
low_cal_recipes = recipesWithMaxCalories(300)

# Find high-protein recipes (≥30g)
protein_recipes = recipesWithMinProtein(30)

# Query specific KG
kg_bbc = create_kg("bbc")
bbc_low_cal = recipesWithMaxCalories(300, kg=kg_bbc)

# Check recipe properties
recipe = low_cal_recipes[0]
print(f"Vegan: {isVegan(recipe)}")
print(f"Difficulty: {getDifficulty(recipe)}")
```

### Creating Custom Individuals

```python
from ontology import Recipe, createIndividual, create_kg

# Create in default KG
recipe, is_new = createIndividual("my_custom_recipe", Recipe)
recipe.has_recipe_name.append("My Custom Recipe")

# Create in specific KG
kg_custom = create_kg("custom")
recipe2, is_new = createIndividual("another_recipe", Recipe, target_kg=kg_custom)
```

---

## Key Concepts

### Classes

The ontology defines entities like `Recipe`, `Ingredient`, `Author`, `Nutrients`, and more. See the [Schema](schema.md) for complete details.

### Properties

Properties connect classes (object properties) or define attributes (data properties). The ontology includes 40+ properties for organizing recipe data.

### Queries

Pre-built query functions allow filtering recipes by nutritional content, time, difficulty, and dietary restrictions. All queries support the `kg` parameter to query specific knowledge graphs. See [Query API](queries.md).

### Constraints

The ontology uses OWL constraints (cardinality, inverse properties, disjointness) to ensure data integrity and enable reasoning. Constraints are defined in the schema and apply to all knowledge graphs.

### Multi-Knowledge Graph Architecture

- **Schema Ontology (schema_onto)** = TBox: Classes like `Recipe`, `Ingredient`, properties like `has_ingredient`
- **Knowledge Graphs (kg_onto, custom KGs)** = ABox: Actual recipe data
  - `kg_onto` - Default knowledge graph
  - `onto` - Alias for `kg_onto` (backward compatibility)
  - Custom KGs created via `create_kg("source_name")`
- **Use Multiple KGs** for different data sources (BBC Food, AllRecipes, etc.)
- **Schema is shared**, data is separate per KG
- Together they form a flexible semantic system for recipe data from multiple sources
