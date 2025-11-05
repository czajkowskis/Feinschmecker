# Development Guide

This guide covers extending the ontology schema with new classes and properties, populating the knowledge graph with data, and using the available tools and scripts.

**Key Concepts**:
- **Ontology (TBox)**: Schema - classes, properties, constraints
- **Knowledge Graph (ABox)**: Data - individual recipes, ingredients, etc.

---

## Extending the Ontology

### Adding New Classes

To add a new class to the ontology, use the `ThingFactory`:

```python
from ontology.factories import ThingFactory

# Create a new class
Equipment = ThingFactory("Equipment")
Equipment.comment = "Kitchen equipment required for recipe preparation"

# Create a subclass
Appliance = ThingFactory("Appliance", BaseClass=Equipment)
Appliance.comment = "Electrical kitchen appliances"

# Create another subclass
Utensil = ThingFactory("Utensil", BaseClass=Equipment)
Utensil.comment = "Manual kitchen utensils"
```

**Best Practices**:
- Always add a comment describing the class purpose
- Use clear, descriptive names
- Consider the class hierarchy carefully
- Follow naming conventions (PascalCase for classes)

---

### Adding New Properties

#### Data Properties

Data properties link individuals to primitive values (strings, numbers, booleans):

```python
from ontology.factories import DataFactory
from ontology.classes import Recipe, Equipment

# Simple data property
servings = DataFactory("servings", domain=[Recipe], range=[int])
servings.comment = "Number of servings the recipe yields"

# Property extending a base property
from ontology.properties import has_name

has_equipment_name = DataFactory(
    "has_equipment_name",
    domain=[Equipment],
    range=[str],
    BaseClass=has_name
)
has_equipment_name.comment = "The name of the equipment"
```

**Best Practices**:
- Specify domain and range explicitly
- Add descriptive comments
- Use snake_case for property names
- Extend meta-properties when appropriate

---

#### Object Properties

Object properties link individuals to other individuals:

```python
from ontology.factories import RelationFactory
from ontology.classes import Recipe

# Create object property
requires_equipment = RelationFactory(
    "requires_equipment",
    domain=[Recipe],
    range=[Equipment]
)
requires_equipment.comment = "Equipment needed for this recipe"

# Create inverse
equipment_used_for = RelationFactory(
    "equipment_used_for",
    domain=[Equipment],
    range=[Recipe]
)
equipment_used_for.comment = "Recipes that use this equipment"
```

---

### Adding Inverse Relationships

Always create inverse relationships for bidirectional navigation:

```python
from ontology.factories import makeInverse

# Link the properties as inverses
makeInverse(requires_equipment, equipment_used_for)
```

After this, setting one property automatically updates the other:

```python
recipe.requires_equipment.append(blender)
# Automatically sets: blender.equipment_used_for contains recipe
```

---

### Adding Constraints

#### Cardinality Constraints

Enforce how many values a property can have:

```python
from ontology import schema_onto

with schema_onto:
    # Recipe must have exactly 1 servings value
    Recipe.is_a.append(servings.exactly(1, int))
    
    # Recipe can have any number of equipment items
    Recipe.is_a.append(requires_equipment.min(0, Equipment))
    
    # Recipe must have at least 1 ingredient
    Recipe.is_a.append(has_ingredient.min(1, IngredientWithAmount))
    
    # Author can have at most 1 associated source
    Author.is_a.append(is_author_of.max(1, Source))
```

**Cardinality Methods**:
- `.exactly(n, range)` - Exactly n values
- `.min(n, range)` - At least n values
- `.max(n, range)` - At most n values
- `.some(range)` - At least 1 value (equivalent to `.min(1, range)`)

---

#### Disjoint Classes

Prevent individuals from belonging to multiple incompatible classes:

```python
from owlready2 import AllDisjoint
from ontology import schema_onto

with schema_onto:
    # Make Equipment subclasses mutually exclusive
    AllDisjoint([Appliance, Utensil])
```

---

### Adding Custom Query Functions

Create specialized query functions for common searches. Always include a `kg` parameter to support querying specific knowledge graphs:

```python
from ontology import kg_onto, Recipe

def recipesRequiringEquipment(equipment_name: str, kg=None) -> list:
    """
    Find recipes requiring specific equipment.
    
    Args:
        equipment_name: Name of the equipment
        kg: Knowledge graph to search (defaults to kg_onto)
    
    Returns:
        List of recipes using this equipment
    """
    if kg is None:
        kg = kg_onto
    
    equipment = kg.search(
        type=kg.Equipment,
        has_equipment_name=equipment_name
    )
    
    if equipment:
        return list(equipment[0].equipment_used_for)
    return []

def recipesWithMaxIngredients(max_count: int, kg=None) -> list:
    """
    Find recipes with at most max_count ingredients.
    
    Args:
        max_count: Maximum number of ingredients
        kg: Knowledge graph to search (defaults to kg_onto)
    
    Returns:
        List of recipes with few ingredients
    """
    if kg is None:
        kg = kg_onto
    
    recipes = list(kg.search(type=Recipe))
    return [r for r in recipes if len(r.has_ingredient) <= max_count]
```

**Best Practices**:
- Add comprehensive docstrings
- Type hint parameters and return values
- Handle edge cases (empty results, None values)
- Return consistent types

---

## Scripts and Tools

### `build_ontology.py`

Builds the complete system: defines the ontology schema and populates the knowledge graph from JSON recipe data.

**Location**: `scripts/build_ontology.py`

**Usage**:
```bash
cd scripts
python build_ontology.py --recipes ../data/recipes.json --output ../data/feinschmecker.rdf
```

**Arguments**:
- `--recipes` (required): Path to input JSON file with recipe data
- `--output` (required): Path to output RDF file

**What it does**:
1. Initializes the ontology schema (TBox)
2. Loads recipes from JSON into the knowledge graph (ABox)
3. Creates all individuals and relationships
4. Applies ontology constraints
5. Saves both ontology and knowledge graph to RDF file

**Example**:
```bash
# Build from sample data
python build_ontology.py \
    --recipes ../data/recipes.json \
    --output ../data/feinschmecker.rdf

# Output:
# Loading recipes from ../data/recipes.json
# Loaded 50 recipes
# Applying constraints...
# Saving to ../data/feinschmecker.rdf
# Done!
```

---

### `example_queries.py`

Demonstrates ontology query capabilities with practical examples.

**Location**: `scripts/example_queries.py`

**Usage**:
```bash
cd scripts
python example_queries.py
```

**What it demonstrates**:
1. Loading recipes from JSON
2. Counting recipes by meal type
3. Nutritional queries (calories, protein, fat, carbs)
4. Time-based queries
5. Accessing detailed recipe information
6. Filtering by dietary restrictions

**Example Output**:
```
============================================================
Feinschmecker Ontology Query Examples
============================================================

1. Loading recipes from JSON...
   Loaded 50 recipes

2. Counting recipes by meal type...
   Breakfast recipes: 15
   Lunch recipes: 18
   Dinner recipes: 17

3. Finding recipes with max 300 calories...
   Found 12 recipes
   Examples: ['green_smoothie', 'egg_white_omelet', 'fruit_salad']

4. Finding recipes with at least 30g protein...
   Found 23 recipes
   Examples: ['grilled_chicken', 'tuna_salad', 'protein_pancakes']

5. Finding recipes with max 15g fat...
   Found 18 recipes
   Examples: ['vegetable_soup', 'chicken_breast', 'rice_bowl']

6. Finding recipes that take 30 minutes or less...
   Found 32 recipes
   Examples: ['quick_pasta', 'stir_fry', 'sandwich']

7. Detailed information about a specific recipe...
   Recipe: Breakfast Burrito
   Vegan: False
   Vegetarian: True
   Difficulty: 1
   Calories: 350 kcal
   Protein: 20g
   Fat: 15g
   Carbs: 35g
   Time: 15 minutes
   Number of ingredients: 8

============================================================
Query examples completed!
============================================================
```

---

### Creating Custom Scripts

You can create your own scripts that use the ontology:

#### Single Knowledge Graph Script

```python
#!/usr/bin/env python3
"""
Custom script for analyzing recipes from a single source.
"""
import sys
from pathlib import Path

# Add parent directory to path to import ontology
sys.path.insert(0, str(Path(__file__).parent.parent))

from ontology import (
    load_recipes_from_json,
    kg_onto,
    recipesWithMaxCalories
)

def main():
    # Load data into default KG
    recipes_path = Path(__file__).parent.parent / "data" / "recipes.json"
    load_recipes_from_json(str(recipes_path))
    
    # Query default KG
    low_cal = recipesWithMaxCalories(300)
    
    for recipe in low_cal:
        print(f"{recipe.has_recipe_name[0]}: "
              f"{recipe.has_calories[0].amount_of_calories[0]} kcal")

if __name__ == '__main__':
    main()
```

#### Multi-Source Knowledge Graph Script

```python
#!/usr/bin/env python3
"""
Custom script for comparing recipes from multiple sources.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ontology import (
    create_kg,
    load_recipes_from_json,
    recipesWithMaxCalories
)

def main():
    # Create separate KGs for different sources
    kg_bbc = create_kg("bbc")
    kg_allrecipes = create_kg("allrecipes")
    
    # Load data into specific KGs
    data_dir = Path(__file__).parent.parent / "data"
    load_recipes_from_json(str(data_dir / "bbc.json"), target_kg=kg_bbc)
    load_recipes_from_json(str(data_dir / "allrecipes.json"), target_kg=kg_allrecipes)
    
    # Query each KG separately
    bbc_low_cal = recipesWithMaxCalories(300, kg=kg_bbc)
    ar_low_cal = recipesWithMaxCalories(300, kg=kg_allrecipes)
    
    print(f"BBC Food: {len(bbc_low_cal)} low-calorie recipes")
    print(f"AllRecipes: {len(ar_low_cal)} low-calorie recipes")
    
    # Compare sources
    print(f"\nTotal unique low-calorie recipes: "
          f"{len(set(bbc_low_cal) | set(ar_low_cal))}")

if __name__ == '__main__':
    main()
```

---

## JSON Data Format

### Expected Format

The `load_recipes_from_json` function expects this structure:

```json
{
  "recipes": [
    {
      "name": "Recipe Name",
      "instructions": "Step-by-step instructions...",
      "ingredients": [
        {
          "name": "ingredient name",
          "amount": 2.0,
          "unit": "cups"
        }
      ],
      "calories": 350.0,
      "protein": 20.0,
      "fat": 15.0,
      "carbohydrates": 35.0,
      "time": 15,
      "difficulty": 1,
      "vegan": false,
      "vegetarian": true,
      "meal_type": "Breakfast",
      "author": "Chef Name",
      "source": "Website Name",
      "link": "https://example.com/recipe",
      "image": "https://example.com/image.jpg"
    }
  ]
}
```

### Field Descriptions

**Required Fields**:
- `name` (string): Recipe name/title
- `instructions` (string): Cooking instructions
- `ingredients` (array): List of ingredient objects
  - `name` (string): Ingredient name
  - `amount` (number): Quantity
  - `unit` (string): Unit of measurement
- `calories` (number): Calories in kcal
- `protein` (number): Protein in grams
- `fat` (number): Fat in grams
- `carbohydrates` (number): Carbohydrates in grams
- `time` (integer): Preparation time in minutes
- `difficulty` (integer): 1 (easy), 2 (moderate), or 3 (difficult)
- `vegan` (boolean): Is the recipe vegan?
- `vegetarian` (boolean): Is the recipe vegetarian?

**Optional Fields**:
- `meal_type` (string): "Breakfast", "Lunch", or "Dinner"
- `author` (string): Recipe author name
- `source` (string): Source website name
- `link` (string): URL to recipe
- `image` (string): URL to recipe image

---

## Testing

### Manual Testing

Test your extensions interactively:

```python
from ontology import onto, Recipe, createIndividual

# Create test individual
test_recipe, _ = createIndividual("test_recipe", Recipe)

# Set properties
test_recipe.has_recipe_name.append("Test Recipe")
# ... set other properties ...

# Verify
print(f"Recipe name: {test_recipe.has_recipe_name[0]}")
print(f"Properties set correctly: {len(test_recipe.has_recipe_name) == 1}")

# Clean up
onto.destroy_entity(test_recipe)
```

---

### Validation

Validate ontology consistency:

```python
from ontology import kg_onto, schema_onto, apply_all_constraints

# Apply all constraints (applies to schema, affects all KGs)
apply_all_constraints()

# Check for inconsistencies
try:
    schema_onto.save("test_schema.rdf")
    kg_onto.save("test_kg.rdf")
    print("Ontology is consistent!")
except Exception as e:
    print(f"Ontology has issues: {e}")
```

---

## Best Practices

### Code Organization

1. **Modular Design**: Keep related functionality together
2. **Single Responsibility**: Each function should do one thing well
3. **Documentation**: Always add docstrings and comments
4. **Type Hints**: Use type hints for better code clarity

### Naming Conventions

- **Classes**: PascalCase (e.g., `Recipe`, `IngredientWithAmount`)
- **Properties**: snake_case (e.g., `has_recipe_name`, `amount_of_calories`)
- **Functions**: snake_case (e.g., `recipesWithMaxCalories`, `load_recipes_from_json`)
- **Individuals**: snake_case (e.g., `breakfast_burrito`, `difficulty_1`)

### Performance

1. **Batch Operations**: Group multiple operations together
   ```python
   with onto:
       # Multiple operations
       pass
   ```

2. **Cache Queries**: Store frequently accessed results
   ```python
   all_recipes = list(onto.search(type=Recipe))  # Cache this
   # Reuse all_recipes multiple times
   ```

3. **Use Specific Queries**: Don't load everything if you only need specific items
   ```python
   # Good
   vegan_recipes = onto.search(type=Recipe, is_vegan=True)
   
   # Less efficient
   all_recipes = onto.search(type=Recipe)
   vegan_recipes = [r for r in all_recipes if r.is_vegan[0]]
   ```

### Error Handling

Always handle potential errors:

```python
def safe_get_recipe(title, kg=None):
    """Safely retrieve a recipe"""
    try:
        return getRecipe(title=title, kg=kg)
    except (KeyError, ValueError) as e:
        print(f"Recipe not found: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## Troubleshooting

### Common Issues

**Issue**: Property values are lists, not single values

**Explanation**: OWLReady2 stores all property values as lists, even if cardinality is 1.

**Solution**: Always access using index `[0]`:
```python
# Correct
name = recipe.has_recipe_name[0]

# Wrong
name = recipe.has_recipe_name  # This is a list
```

---

**Issue**: Cannot find newly created individuals

**Solution**: Ensure you're searching in the correct knowledge graph:
```python
from ontology import kg_onto, create_kg

# Make sure the individual was created in the right KG
recipe, is_new = createIndividual("my_recipe", Recipe)
print(f"Is new: {is_new}")  # Should be True

# Search in the correct KG
found = kg_onto.search(has_recipe_name="My Recipe")
print(f"Found: {len(found)} recipes")

# If using multiple KGs, search the right one
kg_custom = create_kg("custom")
recipe2, is_new = createIndividual("recipe2", Recipe, target_kg=kg_custom)
found2 = kg_custom.search(has_recipe_name="Recipe2")
```

---

**Issue**: Inverse properties not working

**Solution**: Make sure you called `setup_inverse_properties()` or `apply_all_constraints()`:
```python
from ontology import apply_all_constraints

apply_all_constraints()
```

---

**Issue**: Changes not saved

**Solution**: Always call save() on the appropriate ontology after making changes:
```python
from ontology import kg_onto, schema_onto

# Make changes to individuals
recipe.has_recipe_name[0] = "New Name"

# Save the knowledge graph
kg_onto.save("feinschmecker.rdf")

# If you made schema changes, save schema too
schema_onto.save("schema.rdf")
```

---

## Version Control

When modifying the ontology:

1. **Update Version**: Increment version in schema ontology
   ```python
   from ontology import schema_onto
   schema_onto.metadata.versionInfo.append("Version: 1.2 - Added equipment support")
   ```

2. **Document Changes**: Keep CHANGELOG or update comments
3. **Test Thoroughly**: Verify all existing functionality still works
4. **Backup Data**: Save current RDF files before making changes
5. **Schema vs Data**: Remember that schema changes affect all knowledge graphs

---

## Contributing

### Suggested Extensions

Ideas for extending the ontology:

1. **Equipment System**: Add kitchen equipment and requirements
2. **Dietary Tags**: Expand beyond vegan/vegetarian (gluten-free, dairy-free, etc.)
3. **Cuisine Types**: Add cuisine classification (Italian, Mexican, Chinese, etc.)
4. **User Ratings**: Add recipe ratings and reviews
5. **Substitutions**: Track ingredient substitutions
6. **Nutrition Details**: Add micronutrients (vitamins, minerals)
7. **Allergens**: Track common allergens
8. **Seasons**: Link recipes to seasonal ingredients
9. **Cost**: Add estimated recipe cost
10. **Serving Sizes**: Track servings and scaling

---

## Advanced Topics

### SPARQL Queries

For complex queries, use SPARQL directly on any knowledge graph:

```python
from ontology import kg_onto, create_kg

query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX : <https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker/>
    
    SELECT ?recipe ?name ?calories ?protein
    WHERE {
        ?recipe rdf:type :Recipe .
        ?recipe :has_recipe_name ?name .
        ?recipe :has_calories ?cal_obj .
        ?cal_obj :amount_of_calories ?calories .
        ?recipe :has_protein ?prot_obj .
        ?prot_obj :amount_of_protein ?protein .
        FILTER (?calories <= 300 && ?protein >= 20)
    }
    ORDER BY ?calories
"""

# Query default KG
results = list(kg_onto.world.sparql(query))
for recipe, name, calories, protein in results:
    print(f"{name}: {calories} kcal, {protein}g protein")

# Query specific KG
kg_bbc = create_kg("bbc")
results_bbc = list(kg_bbc.world.sparql(query))
```

---

### Reasoning

Enable reasoning to infer new relationships. Note that reasoning applies to all ontologies in the world:

```python
from owlready2 import sync_reasoner_pellet
from ontology import schema_onto, kg_onto

# Run reasoner on schema and default KG
with schema_onto:
    sync_reasoner_pellet([schema_onto, kg_onto])

# Now inferred relationships are available
# (requires Pellet reasoner installed)

# For multiple KGs, include all in reasoning
from ontology import create_kg
kg_custom = create_kg("custom")
with schema_onto:
    sync_reasoner_pellet([schema_onto, kg_onto, kg_custom])
```

---

[Back to Overview](README.md) | [Previous: Usage Guide](usage.md)

