# Ontology Package Structure

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
- Ontology initialization with metadata
- Version: 1.1
```

### 2. factories.py
```python
- ThingFactory(name, BaseClass=Thing)
- RelationFactory(name, domain, range)
- DataFactory(name, domain, range, BaseClass)
- makeInverse(first, second)
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
# Functions
- onthologifyName(name) -> str
- createIndividual(name, BaseClass, unique) -> (Thing, bool)
- create_meal_types() -> dict
- create_difficulties() -> list
- load_recipes_from_json(json_path) -> int
```

### 7. queries.py
```python
# Utility Functions
- getAll(objects, attribute)
- getRecipe(recipe_name, title)

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
- Core: onto, NAMESPACE
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
from ontology import onto, load_recipes_from_json

load_recipes_from_json('recipes.json')
onto.save('output.rdf')
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
```

## Statistics

- **Total Modules:** 8
- **Total Classes:** 13
- **Total Properties:** 40+
- **Total Constraints:** 30+
- **Total Query Functions:** 20+
- **Total Utility Functions:** 10+
- **Lines of Code:** ~800
- **Documentation:** 4 markdown files

