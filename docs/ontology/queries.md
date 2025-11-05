# Query API Reference

The ontology package provides a comprehensive query API for retrieving and filtering recipes from knowledge graphs based on various criteria.

These queries operate on **knowledge graphs** (individuals/ABox) using the **ontology schema** (TBox) as the structure.

**Multi-KG Support**: All query functions accept an optional `kg` parameter to specify which knowledge graph to search. If not provided, they default to searching `kg_onto` (the default knowledge graph).

---

## Utility Functions

### `getAll(objects, attribute)`

Get all values of a specific attribute from a list of objects.

**Parameters**:
- `objects` (list[Thing]): List of OWL individuals
- `attribute` (str): Name of the attribute to retrieve

**Returns**: list - All attribute values from all objects

**Example**:
```python
from ontology import getAll, onto, Recipe

# Get all recipe names
recipes = onto.search(type=Recipe)
names = getAll(recipes, "has_recipe_name")
print(f"Found {len(names)} recipes: {names}")
```

---

### `getRecipe(recipe_name=None, title=None, kg=None)`

Retrieve a recipe by its ontology name or title.

**Parameters**:
- `recipe_name` (str, optional): Ontology identifier for the recipe
- `title` (str, optional): Human-readable title of the recipe
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: Recipe individual

**Raises**:
- `ValueError` - If neither recipe_name nor title is provided
- `KeyError` - If no matching recipe is found

**Example**:
```python
from ontology import getRecipe, create_kg

# Get by title from default KG
recipe = getRecipe(title="Breakfast Burrito")

# Get by ontology name
recipe = getRecipe(recipe_name="breakfast_burrito")

# Get from specific KG
kg_bbc = create_kg("bbc")
recipe = getRecipe(title="Breakfast Burrito", kg=kg_bbc)

# Access properties
print(recipe.has_recipe_name[0])
print(recipe.is_vegan[0])
```

---

## Nutrient Queries

### Calorie Queries

#### `recipesWithMaxCalories(amount, kg=None)`

Find recipes with calories at or below a maximum amount.

**Parameters**:
- `amount` (float): Maximum calorie amount (in kcal)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[Recipe] - Recipes with ≤ specified calories

**Example**:
```python
from ontology import recipesWithMaxCalories, create_kg

# Find recipes with ≤300 kcal in default KG
low_cal = recipesWithMaxCalories(300)
print(f"Found {len(low_cal)} low-calorie recipes")

for recipe in low_cal:
    cal = recipe.has_calories[0].amount_of_calories[0]
    print(f"  {recipe.has_recipe_name[0]}: {cal} kcal")

# Find in specific KG
kg_bbc = create_kg("bbc")
bbc_low_cal = recipesWithMaxCalories(300, kg=kg_bbc)
```

---

#### `recipesWithMinCalories(amount, kg=None)`

Find recipes with calories at or above a minimum amount.

**Parameters**:
- `amount` (float): Minimum calorie amount (in kcal)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[Recipe] - Recipes with ≥ specified calories

**Example**:
```python
from ontology import recipesWithMinCalories

# Find high-calorie recipes (≥500 kcal)
high_cal = recipesWithMinCalories(500)

# Find in specific KG
high_cal_bbc = recipesWithMinCalories(500, kg=kg_bbc)
```

---

### Protein Queries

#### `recipesWithMaxProtein(amount, kg=None)`

Find recipes with protein at or below a maximum amount.

**Parameters**:
- `amount` (float): Maximum protein amount (in grams)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[Recipe] - Recipes with ≤ specified protein

**Example**:
```python
from ontology import recipesWithMaxProtein

# Find low-protein recipes (≤10g)
low_protein = recipesWithMaxProtein(10)
```

---

#### `recipesWithMinProtein(amount, kg=None)`

Find recipes with protein at or above a minimum amount.

**Parameters**:
- `amount` (float): Minimum protein amount (in grams)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[Recipe] - Recipes with ≥ specified protein

**Example**:
```python
from ontology import recipesWithMinProtein

# Find high-protein recipes (≥30g)
protein_rich = recipesWithMinProtein(30)
print(f"Found {len(protein_rich)} high-protein recipes")

for recipe in protein_rich:
    prot = recipe.has_protein[0].amount_of_protein[0]
    print(f"  {recipe.has_recipe_name[0]}: {prot}g protein")
```

---

### Fat Queries

#### `recipesWithMaxFat(amount, kg=None)`

Find recipes with fat at or below a maximum amount.

**Parameters**:
- `amount` (float): Maximum fat amount (in grams)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[Recipe] - Recipes with ≤ specified fat

**Example**:
```python
from ontology import recipesWithMaxFat

# Find low-fat recipes (≤15g)
low_fat = recipesWithMaxFat(15)
```

---

#### `recipesWithMinFat(amount, kg=None)`

Find recipes with fat at or above a minimum amount.

**Parameters**:
- `amount` (float): Minimum fat amount (in grams)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[Recipe] - Recipes with ≥ specified fat

**Example**:
```python
from ontology import recipesWithMinFat

# Find high-fat recipes (≥25g)
high_fat = recipesWithMinFat(25)
```

---

### Carbohydrate Queries

#### `recipesWithMaxCarbohydrates(amount, kg=None)`

Find recipes with carbohydrates at or below a maximum amount.

**Parameters**:
- `amount` (float): Maximum carbohydrate amount (in grams)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[Recipe] - Recipes with ≤ specified carbohydrates

**Example**:
```python
from ontology import recipesWithMaxCarbohydrates

# Find low-carb recipes (≤20g)
low_carb = recipesWithMaxCarbohydrates(20)
```

---

#### `recipesWithMinCarbohydrates(amount, kg=None)`

Find recipes with carbohydrates at or above a minimum amount.

**Parameters**:
- `amount` (float): Minimum carbohydrate amount (in grams)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[Recipe] - Recipes with ≥ specified carbohydrates

**Example**:
```python
from ontology import recipesWithMinCarbohydrates

# Find carb-rich recipes (≥50g)
carb_rich = recipesWithMinCarbohydrates(50)
```

---

## Time Queries

### `recipesWithMaxTime(amount, kg=None)`

Find recipes with preparation time at or below a maximum duration.

**Parameters**:
- `amount` (float): Maximum time in minutes
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[Recipe] - Recipes taking ≤ specified time

**Example**:
```python
from ontology import recipesWithMaxTime

# Find quick recipes (≤30 minutes)
quick_recipes = recipesWithMaxTime(30)
print(f"Found {len(quick_recipes)} quick recipes")

for recipe in quick_recipes:
    time = recipe.requires_time[0].amount_of_time[0]
    print(f"  {recipe.has_recipe_name[0]}: {time} min")
```

---

## Property Queries

### `requiredIngredients(recipe=None, title=None, kg=None)`

Get the list of ingredients required for a recipe.

**Parameters**:
- `recipe` (Recipe, optional): Recipe individual
- `title` (str, optional): Recipe title (alternative to recipe)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: list[str] - List of ingredient names with amounts

**Example**:
```python
from ontology import requiredIngredients

# By recipe object
ingredients = requiredIngredients(recipe=my_recipe)

# By title
ingredients = requiredIngredients(title="Breakfast Burrito")

print("Ingredients:")
for ing in ingredients:
    print(f"  - {ing}")
```

---

### `isVegan(recipe=None, title=None, kg=None)`

Check if a recipe is vegan.

**Parameters**:
- `recipe` (Recipe, optional): Recipe individual
- `title` (str, optional): Recipe title (alternative to recipe)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: bool - True if recipe is vegan, False otherwise

**Example**:
```python
from ontology import isVegan

# By recipe object
if isVegan(recipe=my_recipe):
    print("This recipe is vegan!")

# By title
if isVegan(title="Breakfast Burrito"):
    print("Breakfast Burrito is vegan!")
```

---

### `isVegetarian(recipe=None, title=None, kg=None)`

Check if a recipe is vegetarian.

**Parameters**:
- `recipe` (Recipe, optional): Recipe individual
- `title` (str, optional): Recipe title (alternative to recipe)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: bool - True if recipe is vegetarian, False otherwise

**Example**:
```python
from ontology import isVegetarian

if isVegetarian(title="Pasta Primavera"):
    print("This recipe is vegetarian!")
```

---

### `getDifficulty(recipe=None, title=None, kg=None)`

Get the difficulty level of a recipe.

**Parameters**:
- `recipe` (Recipe, optional): Recipe individual
- `title` (str, optional): Recipe title (alternative to recipe)
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: int - Difficulty level (1=easy, 2=moderate, 3=difficult)

**Example**:
```python
from ontology import getDifficulty

difficulty = getDifficulty(recipe=my_recipe)

if difficulty == 1:
    print("This is an easy recipe!")
elif difficulty == 2:
    print("This recipe has moderate difficulty")
else:
    print("This is a difficult recipe")
```

---

## Counting Queries

### `breakfastRecipesCount(kg=None)`

Count the number of breakfast recipes.

**Parameters**:
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: int - Number of breakfast recipes

**Example**:
```python
from ontology import breakfastRecipesCount

count = breakfastRecipesCount()
print(f"We have {count} breakfast recipes")
```

---

### `lunchRecipesCount(kg=None)`

Count the number of lunch recipes.

**Parameters**:
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: int - Number of lunch recipes

**Example**:
```python
from ontology import lunchRecipesCount

count = lunchRecipesCount()
print(f"We have {count} lunch recipes")
```

---

### `dinnerRecipesCount(kg=None)`

Count the number of dinner recipes.

**Parameters**:
- `kg` (Ontology, optional): Knowledge graph to search (defaults to kg_onto)

**Returns**: int - Number of dinner recipes

**Example**:
```python
from ontology import dinnerRecipesCount

count = dinnerRecipesCount()
print(f"We have {count} dinner recipes")
```

---

## Multi-Knowledge Graph Queries

When working with multiple knowledge graphs from different sources, you can query each separately or combine results.

### Querying Specific Knowledge Graphs

```python
from ontology import create_kg, recipesWithMaxCalories, isVegan

# Create separate KGs for different sources
kg_bbc = create_kg("bbc")
kg_allrecipes = create_kg("allrecipes")

# Query each KG separately
bbc_low_cal = recipesWithMaxCalories(300, kg=kg_bbc)
ar_low_cal = recipesWithMaxCalories(300, kg=kg_allrecipes)

print(f"BBC: {len(bbc_low_cal)} low-calorie recipes")
print(f"AllRecipes: {len(ar_low_cal)} low-calorie recipes")
```

### Combining Results from Multiple KGs

```python
# Union: All low-calorie recipes from both sources
all_low_cal = set(bbc_low_cal) | set(ar_low_cal)
print(f"Total unique: {len(all_low_cal)} recipes")

# Intersection: Recipes found in both sources (unlikely, but possible)
common = set(bbc_low_cal) & set(ar_low_cal)
print(f"Found in both: {len(common)} recipes")
```

### Comparing Sources

```python
# Compare recipe counts by source
kg_sources = {
    "BBC Food": kg_bbc,
    "AllRecipes": kg_allrecipes
}

for source_name, kg in kg_sources.items():
    vegan_count = len([r for r in kg.search(type=Recipe) if isVegan(r, kg=kg)])
    total_count = len(list(kg.search(type=Recipe)))
    percentage = (vegan_count / total_count * 100) if total_count > 0 else 0
    print(f"{source_name}: {vegan_count}/{total_count} ({percentage:.1f}%) vegan recipes")
```

### Source-Specific Statistics

```python
from ontology import breakfastRecipesCount, lunchRecipesCount, dinnerRecipesCount

def analyze_kg(kg, source_name):
    """Analyze a knowledge graph and print statistics"""
    print(f"\n{source_name} Statistics:")
    print(f"  Breakfast: {breakfastRecipesCount(kg=kg)}")
    print(f"  Lunch: {lunchRecipesCount(kg=kg)}")
    print(f"  Dinner: {dinnerRecipesCount(kg=kg)}")
    
    # Nutritional stats
    all_recipes = list(kg.search(type=Recipe))
    if all_recipes:
        avg_cal = sum(r.has_calories[0].amount_of_calories[0] for r in all_recipes) / len(all_recipes)
        print(f"  Average calories: {avg_cal:.1f} kcal")

analyze_kg(kg_bbc, "BBC Food")
analyze_kg(kg_allrecipes, "AllRecipes")
```

---

## Advanced Query Patterns

### Combining Multiple Filters

```python
from ontology import (
    recipesWithMaxCalories,
    recipesWithMinProtein,
    recipesWithMaxTime,
    isVegan
)

# Find quick, high-protein, low-calorie recipes
low_cal = recipesWithMaxCalories(400)
high_protein = recipesWithMinProtein(25)
quick = recipesWithMaxTime(30)

# Intersection of all three
results = set(low_cal) & set(high_protein) & set(quick)
print(f"Found {len(results)} recipes matching all criteria")

# Further filter by vegan
vegan_results = [r for r in results if isVegan(r)]
print(f"{len(vegan_results)} of those are vegan")
```

---

### Complex Filtering with Python

```python
from ontology import onto, Recipe

# Get all recipes
all_recipes = list(onto.search(type=Recipe))

# Complex filter: Easy vegan breakfast recipes under 400 calories
filtered = [
    r for r in all_recipes
    if r.is_vegan[0]
    and r.has_difficulty[0].has_numeric_difficulty[0] == 1
    and r.has_calories[0].amount_of_calories[0] <= 400
    and any(mt.has_meal_type_name[0] == "Breakfast" 
            for mt in r.is_meal_type)
]

print(f"Found {len(filtered)} easy vegan breakfast recipes under 400 kcal")
```

---

### Macronutrient Ratios

```python
from ontology import onto, Recipe

def get_macro_ratio(recipe):
    """Calculate protein:fat:carb ratio"""
    protein = recipe.has_protein[0].amount_of_protein[0]
    fat = recipe.has_fat[0].amount_of_fat[0]
    carbs = recipe.has_carbohydrates[0].amount_of_carbohydrates[0]
    return (protein, fat, carbs)

# Find high-protein recipes (protein > fat + carbs)
all_recipes = list(onto.search(type=Recipe))
high_protein_ratio = []

for recipe in all_recipes:
    p, f, c = get_macro_ratio(recipe)
    if p > (f + c):
        high_protein_ratio.append((recipe, p, f, c))

print(f"Found {len(high_protein_ratio)} recipes with protein > fat+carbs")
for recipe, p, f, c in high_protein_ratio[:5]:
    print(f"  {recipe.has_recipe_name[0]}: P={p}g F={f}g C={c}g")
```

---

### Finding Recipes by Ingredient

```python
from ontology import onto

def recipes_with_ingredient(ingredient_name):
    """Find all recipes containing a specific ingredient"""
    # Search for the ingredient
    ingredients = onto.search(
        type=onto.Ingredient,
        has_ingredient_name=ingredient_name
    )
    
    if not ingredients:
        return []
    
    ingredient = ingredients[0]
    recipes = []
    
    # Get all IngredientWithAmount instances for this ingredient
    for ing_with_amt in ingredient.is_ingredient_of:
        recipes.extend(ing_with_amt.used_for)
    
    return recipes

# Find all recipes with chicken
chicken_recipes = recipes_with_ingredient("chicken")
print(f"Found {len(chicken_recipes)} recipes with chicken")
```

---

### Nutritional Summaries

```python
from ontology import onto, Recipe

def print_nutrition_summary(recipe):
    """Print a complete nutritional summary of a recipe"""
    print(f"\n{recipe.has_recipe_name[0]}")
    print("=" * 50)
    
    # Basic info
    print(f"Difficulty: {recipe.has_difficulty[0].has_numeric_difficulty[0]}/3")
    print(f"Time: {recipe.requires_time[0].amount_of_time[0]} minutes")
    print(f"Vegan: {'Yes' if recipe.is_vegan[0] else 'No'}")
    print(f"Vegetarian: {'Yes' if recipe.is_vegetarian[0] else 'No'}")
    
    # Nutrition
    print("\nNutrition:")
    print(f"  Calories: {recipe.has_calories[0].amount_of_calories[0]} kcal")
    print(f"  Protein: {recipe.has_protein[0].amount_of_protein[0]}g")
    print(f"  Fat: {recipe.has_fat[0].amount_of_fat[0]}g")
    print(f"  Carbs: {recipe.has_carbohydrates[0].amount_of_carbohydrates[0]}g")
    
    # Meal types
    if recipe.is_meal_type:
        meal_types = [mt.has_meal_type_name[0] for mt in recipe.is_meal_type]
        print(f"\nMeal Types: {', '.join(meal_types)}")
    
    # Ingredients
    print(f"\nIngredients ({len(recipe.has_ingredient)}):")
    for ing in recipe.has_ingredient:
        print(f"  - {ing.has_ingredient_with_amount_name[0]}")

# Example usage
recipes = list(onto.search(type=Recipe))
if recipes:
    print_nutrition_summary(recipes[0])
```

---

## Query Performance Tips

### 1. Use Specific Queries

Instead of retrieving all recipes and filtering in Python, use the built-in query functions:

**❌ Inefficient**:
```python
all_recipes = list(onto.search(type=Recipe))
low_cal = [r for r in all_recipes if r.has_calories[0].amount_of_calories[0] <= 300]
```

**✅ Efficient**:
```python
low_cal = recipesWithMaxCalories(300)
```

### 2. Cache Frequent Lookups

If you're accessing the same data multiple times, cache it:

```python
# Cache all recipes once
all_recipes = list(onto.search(type=Recipe))

# Reuse the cached list
vegan_recipes = [r for r in all_recipes if r.is_vegan[0]]
vegetarian_recipes = [r for r in all_recipes if r.is_vegetarian[0]]
```

### 3. Combine Queries Strategically

Start with the most restrictive query to minimize the result set:

```python
# Start with the smallest set
quick_recipes = recipesWithMaxTime(15)  # Likely fewest results

# Then filter further
quick_vegan = [r for r in quick_recipes if isVegan(r)]
```

### 4. Use Sets for Intersections

When combining multiple queries, use sets for efficient intersection:

```python
set1 = set(recipesWithMaxCalories(400))
set2 = set(recipesWithMinProtein(25))
set3 = set(recipesWithMaxTime(30))

# Efficient intersection
results = set1 & set2 & set3
```

---

## SPARQL Queries

For more advanced queries, you can use SPARQL directly with OWLReady2:

```python
from ontology import onto

# Example SPARQL query
query = """
    SELECT ?recipe ?name ?calories
    WHERE {
        ?recipe rdf:type :Recipe .
        ?recipe :has_recipe_name ?name .
        ?recipe :has_calories ?cal_obj .
        ?cal_obj :amount_of_calories ?calories .
        FILTER (?calories <= 300)
    }
"""

results = list(onto.world.sparql(query))
for recipe, name, calories in results:
    print(f"{name}: {calories} kcal")
```

**Note**: Replace `:` with the actual namespace prefix when running SPARQL queries.

---

[Back to Overview](README.md) | [Previous: Schema](schema.md) | [Next: Usage Guide](usage.md)

