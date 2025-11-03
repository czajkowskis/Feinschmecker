# Ontology

The ontology directory contains the OWL ontology implementation for the Feinschmecker recipe knowledge graph. The code has been refactored from the Jupyter notebook into modular Python files for better maintainability and reusability.

## Structure

The ontology package is organized into the following modules:

### Core Modules

- **`setup.py`** - Ontology initialization, namespace configuration, and metadata
- **`factories.py`** - Factory functions for creating OWL classes, properties, and relationships
- **`classes.py`** - Class definitions (Recipe, Ingredient, Author, Source, etc.)
- **`properties.py`** - Data and object property definitions
- **`constraints.py`** - Inverse relationships, cardinality constraints, and disjointness axioms
- **`individuals.py`** - Functions for creating and populating ontology individuals from JSON data
- **`queries.py`** - Utility functions for querying the ontology
- **`__init__.py`** - Main package interface exposing all components

## Usage

### Basic Import and Setup

```python
from ontology import onto, load_recipes_from_json

# Load recipe data
load_recipes_from_json('path/to/recipes.json')

# Save ontology
onto.save('feinschmecker.rdf')
```

### Querying Recipes

```python
from ontology import (
    recipesWithMaxCalories,
    recipesWithMinProtein,
    isVegan,
    getDifficulty
)

# Find low-calorie recipes
low_cal_recipes = recipesWithMaxCalories(300)

# Find high-protein recipes
protein_recipes = recipesWithMinProtein(30)

# Check recipe properties
recipe = low_cal_recipes[0]
print(f"Vegan: {isVegan(recipe)}")
print(f"Difficulty: {getDifficulty(recipe)}")
```

### Creating Custom Individuals

```python
from ontology import Recipe, createIndividual, has_recipe_name

# Create a new recipe
recipe, is_new = createIndividual("my_custom_recipe", Recipe)
recipe.has_recipe_name.append("My Custom Recipe")
```

## Key Classes

The ontology defines the following main classes:

- **Recipe** - Main entity representing a recipe with instructions, ingredients, and nutritional information
- **Ingredient** - Base ingredient types (e.g., "tomato", "chicken")
- **IngredientWithAmount** - Ingredients with specific quantities and units
- **Author** - Recipe authors/creators
- **Source** - Recipe sources/websites
- **Time** - Cooking/preparation time requirements
- **MealType** - Recipe categories (Breakfast, Lunch, Dinner)
- **Difficulty** - Recipe difficulty levels (1=easy, 2=moderate, 3=difficult)
- **Nutrients** - Nutritional information (Calories, Protein, Fat, Carbohydrates)

## Properties

### Object Properties (Relationships)

- `has_ingredient` - Links recipes to ingredients with amounts
- `authored_by` - Links recipes to their authors
- `requires_time` - Links recipes to preparation time
- `is_meal_type` - Categorizes recipes by meal type
- `has_difficulty` - Associates recipes with difficulty levels

### Data Properties (Attributes)

- `has_recipe_name` - Recipe title/name
- `has_instructions` - Cooking instructions
- `is_vegan` - Boolean flag for vegan recipes
- `is_vegetarian` - Boolean flag for vegetarian recipes
- `amount_of_calories` - Calorie content
- `amount_of_protein` - Protein content (grams)
- `amount_of_fat` - Fat content (grams)
- `amount_of_carbohydrates` - Carbohydrate content (grams)

## Scripts

The `scripts/` directory contains utilities for working with the ontology:

- **`build_ontology.py`** - Build the ontology from JSON recipe data
- **`example_queries.py`** - Examples of querying the ontology

### Building the Ontology

```bash
cd scripts
python build_ontology.py --recipes ../data/recipes.json --output ../data/feinschmecker.rdf
```

### Running Example Queries

```bash
cd scripts
python example_queries.py
```

## Namespace

```
https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker/
```

## Constraints and Validation

The ontology includes:

- **Cardinality constraints** - Enforce required and optional properties
- **Inverse properties** - Bidirectional relationships (e.g., `has_ingredient` ↔ `used_for`)
- **Disjoint classes** - Prevent overlapping class memberships
- **Domain and range restrictions** - Type safety for properties

## Development

### Adding New Classes

```python
from ontology.factories import ThingFactory

NewClass = ThingFactory("NewClass")
NewClass.comment = "Description of the new class"
```

### Adding New Properties

```python
from ontology.factories import DataFactory, RelationFactory

# Data property
new_property = DataFactory("new_property", domain=[SomeClass], range=[str])

# Object property (relationship)
new_relation = RelationFactory("new_relation", domain=[ClassA], range=[ClassB])
```

### Adding Constraints

```python
from ontology.setup import onto

with onto:
    SomeClass.is_a.append(some_property.exactly(1, str))
```

## Version Information

Current version: 1.1 - Existing and working ontology with sparse individuals, initial feedback included

## Authors

This ontology was created by:
- Jaron Sprute
- Bhuvenesh Verma
- Szymon Czajkowski
