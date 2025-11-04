# Ontology Architecture

## Overview

The Feinschmecker ontology uses a **multi-knowledge graph architecture** that separates:

1. **Schema Ontology (schema_onto)**: TBox containing classes, properties, and constraints
2. **Knowledge graph ontologies**: Multiple ABox ontologies containing individuals/instances
   - **kg_onto**: The default knowledge graph
   - **onto**: Backward-compatibility alias for kg_onto
   - **Custom KGs**: Additional knowledge graphs created via `create_kg(source_name)`

Each knowledge graph imports the schema ontology, establishing a formal OWL import relationship. This allows:
- Loading only the schema for extension and development
- Saving schema and data to separate RDF files
- Clear separation between structure (schema) and content (data)
- **Multiple independent knowledge graphs** for different data sources
- Querying across specific knowledge graphs or combining data from multiple sources

## Module organization

The ontology package is organized into modular components following a clear dependency hierarchy:

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
```

---

## Module responsibilities

### 1. `setup.py` - Ontology initialization

**Purpose**: Defines the namespace and initializes the schema ontology and knowledge graph management system

**Key Components**:
- Namespace definition
- Schema ontology (TBox) initialization
- Default knowledge graph ontology (ABox) initialization
- Knowledge graph factory function for creating multiple KGs
- OWL import relationship between each KG and schema_onto


**Exports**:
- `NAMESPACE` - The ontology namespace base URL
- `schema_onto` - Schema ontology (TBox)
- `kg_onto` - Default knowledge graph ontology (ABox)
- `onto` - Backward-compatibility alias for kg_onto
- `create_kg(source_name)` - Factory function to create new knowledge graphs
- `knowledge_graphs` - Dictionary tracking all created knowledge graphs

---

### 2. `factories.py` - OWL ocmponent factories

**Purpose**: Provides factory functions for creating OWL classes, properties, and relationships in the schema ontology

**Functions**:

#### `ThingFactory(name, BaseClass=Thing)`
Creates OWL classes in the schema ontology.

```python
Recipe = ThingFactory("Recipe")  # Created in schema_onto
Protein = ThingFactory("Protein", BaseClass=Nutrients)
```

#### `RelationFactory(name, domain, range)`
Creates object properties (relationships between classes).

```python
has_ingredient = RelationFactory(
    "has_ingredient",
    domain=[Recipe],
    range=[IngredientWithAmount]
)
```

#### `DataFactory(name, domain, range, BaseClass)`
Creates data properties (attributes with primitive values).

```python
has_recipe_name = DataFactory(
    "has_recipe_name",
    domain=[Recipe],
    range=[str]
)
```

#### `makeInverse(first, second)`
Creates inverse property relationships.

```python
makeInverse(has_ingredient, used_for)
```

---

### 3. `classes.py` - Class definitions

**Purpose**: Defines the main OWL classes representing entities in the recipe domain

**Classes defined**:
- `Recipe` - Main entity with instructions, ingredients, and nutrition
- `Ingredient` - Base ingredient types
- `IngredientWithAmount` - Ingredients with quantities and units
- `Author` - Recipe creators
- `Source` - Recipe sources/websites
- `Time` - Preparation time
- `MealType` - Recipe categories (Breakfast, Lunch, Dinner)
- `Difficulty` - Recipe difficulty levels (1-3)
- `Nutrients` - Base class for nutritional information
  - `Calories` - Calorie content
  - `Protein` - Protein content
  - `Fat` - Fat content
  - `Carbohydrates` - Carbohydrate content

Each class includes a comment describing its purpose.

---

### 4. `properties.py` - Property definitions

**Purpose**: Defines 40+ properties organizing recipe data and relationships

**Property categories**:
- **Meta properties** (2): `has_name`, `has_amount`
- **Recipe properties** (15): Name, instructions, ingredients, nutrition, etc.
- **Ingredient properties** (2): Name and relationships
- **IngredientWithAmount properties** (5): Name, type, amount, unit
- **Author properties** (3): Name and relationships
- **Source properties** (3): Name, URL, authors
- **Time properties** (2): Duration and relationships
- **MealType properties** (2): Name and relationships
- **Difficulty properties** (2): Numeric value and relationships
- **Nutrient properties** (8): Amounts and relationships for each nutrient

See [Schema](schema.md) for complete property details.

---

### 5. `constraints.py` - Constraints and Validation

**Purpose**: Implements OWL constraints and validation rules

**Functions**:

#### `setup_inverse_properties()`
Establishes 11 inverse property pairs for bidirectional relationships.

#### `setup_cardinality_constraints()`
Enforces required and optional properties on classes (e.g., "Recipe must have exactly 1 name").

#### `setup_disjointness()`
Prevents overlapping class memberships for logical consistency.

#### `apply_all_constraints()`
Convenience function to apply all constraints at once.

**Constraint Types**:
- Inverse properties
- Cardinality restrictions
- Disjoint class declarations
- Domain and range restrictions

---

### 6. `individuals.py` - Individual Management

**Purpose**: Functions for creating and managing individuals in knowledge graphs (ABox)

Individuals can be created in any knowledge graph while referencing classes defined in `schema_onto`.



---

### 7. `queries.py` - Query Functions

**Purpose**: Provides 20+ utility functions for querying individuals in knowledge graphs

All queries accept an optional `kg` parameter to specify which knowledge graph to search. If not provided, queries default to searching `kg_onto`.

**Function Categories**:
- **Utility functions** (2): `getAll`, `getRecipe`
- **Nutrient queries** (8): Min/max for calories, protein, fat, carbs
- **Time queries** (1): Maximum preparation time
- **Property queries** (4): Ingredients, vegan, vegetarian, difficulty
- **Counting queries** (3): Count by meal type

**Multi-KG support**: All query functions accept a `kg` parameter to query specific knowledge graphs.

See [Query API](queries.md) for complete function reference.

---

### 8. `__init__.py` - Package Interface

**Purpose**: Exports all public APIs for easy import

**Exports** (65+ items):
- Core: `schema_onto`, `kg_onto`, `onto` (alias), `NAMESPACE`, `create_kg`, `knowledge_graphs`
- Factories: 4 functions
- Classes: 13 classes
- Properties: 40+ properties
- Constraints: 4 functions
- Individuals: 5 functions
- Queries: 20+ functions

**Usage**:
```python
# Import everything you need from the main package
from ontology import (
    schema_onto, kg_onto, onto,  # Ontologies
    create_kg, knowledge_graphs,  # Multi-KG support
    Recipe, Ingredient,
    has_recipe_name,
    recipesWithMaxCalories,
    load_recipes_from_json
)
```

---

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

---

## Import Hierarchy

### Level 1: Base
- `setup.py` - No internal dependencies

### Level 2: Factories & Queries
- `factories.py` - Depends on: `setup`
- `queries.py` - Depends on: `setup`, `classes`

### Level 3: Classes
- `classes.py` - Depends on: `factories`

### Level 4: Properties & Individuals
- `properties.py` - Depends on: `factories`, `classes`
- `individuals.py` - Depends on: `classes`, `properties`

### Level 5: Constraints
- `constraints.py` - Depends on: `properties`, `classes`, `factories`

### Level 6: Package Interface
- `__init__.py` - Depends on: all modules

---

## Design Principles

### Multi-Knowledge Graph Architecture

The ontology separates schema from data and supports multiple independent knowledge graphs:

- **schema_onto**: Contains TBox (classes, properties, constraints) at `/schema/` namespace
- **kg_onto**: Default ABox (individuals) at `/kg/` namespace, imports schema_onto
- **onto**: Alias for `kg_onto` (backward compatibility)
- **Custom KGs**: Additional knowledge graphs at `/kg/{source_name}/` namespaces

This architecture enables:
- Loading schema without data for development
- Saving schema and data to separate RDF files
- Clear separation between structure and content
- Standard OWL import mechanism
- **Multiple data sources in separate knowledge graphs**
- **Source-specific queries and independent data management**
- **Combining data from multiple sources when needed**

#### When to Use Multiple Knowledge Graphs

**Use separate KGs when:**
- Data comes from different sources (e.g., BBC Food, AllRecipes, Food Network)
- You need to keep data isolated for attribution or licensing
- You want to compare or analyze data from different sources separately
- Different data sources have different quality or trust levels

**Use single KG when:**
- All data comes from one source or can be merged
- You always query across all data
- Source attribution is not critical

### Modularity
Each module has a single, well-defined responsibility. This makes the code easier to understand, test, and maintain.

### Dependency Management
Modules are organized in clear layers with unidirectional dependencies, preventing circular imports.

### Factory Pattern
Factory functions provide a consistent interface for creating OWL components in the schema, abstracting away OWLReady2 details.

### Separation of Concerns
- **Structure** (schema_onto: classes, properties) is separate from **data** (kg_onto: individuals)
- **Definition** (setup, factories) is separate from **usage** (queries)
- **Core logic** is separate from **convenience functions**

### Extensibility
New classes, properties, or queries can be added without modifying existing code, following the open/closed principle.

---

## Usage Patterns

### Simple Usage (Single Knowledge Graph)
For basic tasks with one data source, import only what you need:

```python
from ontology import schema_onto, kg_onto, load_recipes_from_json

# Load into default knowledge graph
load_recipes_from_json('recipes.json')

# Save schema only
schema_onto.save('schema.rdf')

# Save knowledge graph (includes schema import)
kg_onto.save('kg.rdf')
```

### Multi-Source Usage (Multiple Knowledge Graphs)
For managing data from different sources separately:

```python
from ontology import schema_onto, create_kg, load_recipes_from_json

# Create separate KGs for different sources
kg_bbc = create_kg("bbc")
kg_allrecipes = create_kg("allrecipes")

# Load data into specific KGs
load_recipes_from_json('bbc_recipes.json', target_kg=kg_bbc)
load_recipes_from_json('allrecipes.json', target_kg=kg_allrecipes)

# Save schema once (shared by all KGs)
schema_onto.save('schema.rdf')

# Save each KG separately
kg_bbc.save('kg-bbc.rdf')
kg_allrecipes.save('kg-allrecipes.rdf')
```

### Query Usage (Single or Multiple KGs)
Query specific knowledge graphs or the default:

```python
from ontology import recipesWithMaxCalories, isVegan, create_kg

# Query default KG
recipes = recipesWithMaxCalories(300)
vegan_recipes = [r for r in recipes if isVegan(r)]

# Query specific KG
kg_bbc = create_kg("bbc")
bbc_recipes = recipesWithMaxCalories(300, kg=kg_bbc)

# Combine results from multiple KGs
kg_ar = create_kg("allrecipes")
all_low_cal = set(recipesWithMaxCalories(300, kg=kg_bbc)) | \
              set(recipesWithMaxCalories(300, kg=kg_ar))
```

### Custom Development
For extending the ontology, import factory functions:

```python
from ontology import ThingFactory, DataFactory, createIndividual

# Create new class (in schema - shared by all KGs)
CustomClass = ThingFactory("CustomClass")

# Create new property (in schema - shared by all KGs)
custom_property = DataFactory("custom_property", domain=[CustomClass], range=[str])

# Create individual in default KG
obj, is_new = createIndividual("my_object", CustomClass)

# Create individual in specific KG
kg_custom = create_kg("custom_source")
obj2, is_new = createIndividual("my_object_2", CustomClass, target_kg=kg_custom)
```

---

## Performance Considerations

### Lazy Loading
The schema ontology (TBox) is defined when the module is imported, but individuals in knowledge graphs (ABox) are only created when loaded from JSON or explicitly created.

### Query Optimization
Query functions use OWLReady2's search capabilities efficiently, filtering at the database level rather than in Python. Specifying a particular knowledge graph with the `kg` parameter improves performance by narrowing the search scope.

### Memory Management
The ontology and knowledge graphs are held in memory for fast access. For very large datasets, consider:
- **Using multiple KGs**: Separate data sources reduce memory per KG
- Loading in batches
- Using SPARQL queries for complex operations
- Saving intermediate results to disk
- Querying specific KGs rather than searching all data

### Multi-KG Performance
- Separate knowledge graphs can be loaded/unloaded independently
- Queries on specific KGs are faster than searching merged data
- Schema is shared (loaded once) across all knowledge graphs

---

[Back to Overview](README.md) | [Next: Schema Reference](schema.md)

