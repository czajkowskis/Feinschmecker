# Ontology Package Structure

## Architecture Overview

The ontology uses a **two-ontology architecture**:
- **schema_onto**: Schema ontology (TBox) with classes, properties, constraints
- **kg_onto**: Knowledge graph (ABox) with individuals, imports schema_onto

This separation allows loading schema without data, saving to separate files, and clear TBox/ABox distinction.

## Module Organization

```
ontology/
├── __init__.py           # Main package interface (exports all public APIs)
├── setup.py              # Ontology initialization and namespace
├── factories.py          # Factory functions for creating OWL components
├── classes.py            # OWL class definitions (Recipe, Ingredient, etc.)
├── properties.py         # Data and object property definitions
├── constraints.py        # Constraints, inverses, and axioms
├── individuals.py        # Individual creation and JSON loading
├── queries.py            # Query utility functions
├── README.md             # Comprehensive documentation
└── STRUCTURE.md          # This file
```

## Module Responsibilities

### 1. setup.py
```python
- Namespace: "https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker"
- schema_onto: TBox at {NAMESPACE}/schema/
- kg_onto: ABox at {NAMESPACE}/kg/ (imports schema_onto)
- onto: Alias for kg_onto (backward compatibility)
- Version: 2.0
```

### 2. factories.py
```python
- ThingFactory(name, BaseClass=Thing)        # Creates classes in schema_onto
- RelationFactory(name, domain, range)       # Creates object properties in schema_onto
- DataFactory(name, domain, range, BaseClass) # Creates data properties in schema_onto
- makeInverse(first, second)                 # Defines inverse properties in schema_onto
```

### 3. classes.py
```python
# Main Classes
- Recipe
- Ingredient
- IngredientWithAmount
- Author
- Source
- Time
- MealType
- Difficulty

# Nutrient Classes
- Nutrients (base class)
  ├── Calories
  ├── Protein
  ├── Fat
  └── Carbohydrates
```

### 4. properties.py
```python
# Meta Properties
- has_name
- has_amount

# Recipe Properties (15 properties)
- has_recipe_name, has_instructions
- has_ingredient, authored_by, requires_time
- is_meal_type, has_difficulty
- is_vegan, is_vegetarian
- has_calories, has_protein, has_fat, has_carbohydrates
- has_link, has_image_link

# Ingredient Properties (2 properties)
- has_ingredient_name
- is_ingredient_of

# IngredientWithAmount Properties (5 properties)
- has_ingredient_with_amount_name
- used_for, type_of_ingredient
- amount_of_ingredient, unit_of_ingredient

# Author Properties (3 properties)
- has_author_name, authored, is_author_of

# Source Properties (3 properties)
- has_source_name, has_author, is_website

# Time Properties (2 properties)
- time_required_by, amount_of_time

# MealType Properties (2 properties)
- meal_type_of, has_meal_type_name

# Difficulty Properties (2 properties)
- difficulty_of, has_numeric_difficulty

# Nutrient Properties (8 properties)
- calories_of, amount_of_calories
- protein_of, amount_of_protein
- fat_of, amount_of_fat
- carbohydrates_of, amount_of_carbohydrates
```

### 5. constraints.py
```python
# Functions
- setup_inverse_properties()      # 11 inverse property pairs
- setup_cardinality_constraints() # Restrictions on all classes
- setup_disjointness()            # Disjoint class declarations
- apply_all_constraints()         # Apply all constraints at once
```

### 6. individuals.py
```python
# Functions (all create individuals in kg_onto)
- onthologifyName(name) -> str
- createIndividual(name, BaseClass, unique) -> (Thing, bool)  # Creates in kg_onto
- create_meal_types() -> dict                                  # Creates in kg_onto
- create_difficulties() -> list                                # Creates in kg_onto
- load_recipes_from_json(json_path) -> int                     # Creates in kg_onto
```

### 7. queries.py
```python
# Utility Functions (all search kg_onto)
- getAll(objects, attribute)
- getRecipe(recipe_name, title)  # Searches kg_onto

# Nutrient Queries (10 functions)
- recipesWithMaxCalories(amount)
- recipesWithMinCalories(amount)
- recipesWithMaxProtein(amount)
- recipesWithMinProtein(amount)
- recipesWithMaxFat(amount)
- recipesWithMinFat(amount)
- recipesWithMaxCarbohydrates(amount)
- recipesWithMinCarbohydrates(amount)

# Time Queries
- recipesWithMaxTime(amount)

# Property Queries (4 functions)
- requiredIngredients(recipe, title)
- isVegan(recipe, title)
- isVegetarian(recipe, title)
- getDifficulty(recipe, title)

# Counting Queries (3 functions)
- breakfastRecipesCount()
- lunchRecipesCount()
- dinnerRecipesCount()
```

### 8. __init__.py
```python
# Exports (60+ public APIs)
- Core: schema_onto, kg_onto, onto (alias), NAMESPACE
- Factories: 4 functions
- Classes: 13 classes
- Properties: 40+ properties
- Constraints: 4 functions
- Individuals: 5 functions
- Queries: 20+ functions
```

## Dependency Graph

```
                    setup.py
                       │
                       ├──────────────┐
                       ↓              ↓
                  factories.py    queries.py
                       ↓
                   classes.py
                       ↓
          ┌────────────┴────────────┐
          ↓                         ↓
    properties.py             individuals.py
          ↓
    constraints.py
          ↓
      __init__.py (imports all, applies constraints)
```

## Import Hierarchy

### Level 1: Base
- `setup.py` - No internal dependencies

### Level 2: Factories & Queries
- `factories.py` - Depends on: setup
- `queries.py` - Depends on: setup, classes

### Level 3: Classes
- `classes.py` - Depends on: factories

### Level 4: Properties & Individuals
- `properties.py` - Depends on: factories, classes
- `individuals.py` - Depends on: classes, properties

### Level 5: Constraints
- `constraints.py` - Depends on: properties, classes, factories

### Level 6: Package Interface
- `__init__.py` - Depends on: all modules

## Usage Patterns

### Simple Usage
```python
from ontology import schema_onto, kg_onto, load_recipes_from_json

load_recipes_from_json('recipes.json')

# Save schema only (TBox)
schema_onto.save('schema.rdf')

# Save knowledge graph (ABox + imports)
kg_onto.save('kg.rdf')

# Backward compatibility
from ontology import onto  # Alias for kg_onto
```

### Query Usage
```python
from ontology import recipesWithMaxCalories, isVegan

recipes = recipesWithMaxCalories(300)
vegan_recipes = [r for r in recipes if isVegan(r)]
```

### Custom Development
```python
from ontology import ThingFactory, DataFactory, createIndividual

# Create new class
CustomClass = ThingFactory("CustomClass")

# Create new property
custom_property = DataFactory("custom_property", domain=[CustomClass], range=[str])

# Create individual
obj, is_new = createIndividual("my_object", CustomClass)

