# Usage Guide

This guide provides comprehensive examples of working with the Feinschmecker ontology and knowledge graphs, from basic operations to advanced patterns.

**Note**: 
- The **schema ontology (schema_onto)** defines classes and properties
- **Knowledge graphs (kg_onto, custom KGs)** contain the actual recipe data (individuals)
- `onto` is an alias for `kg_onto` (backward compatibility)

---

## Complete Workflow Example

### Loading and Querying Recipes

```python
from pathlib import Path
from ontology import (
    load_recipes_from_json, kg_onto,  # kg_onto is the default knowledge graph
    recipesWithMaxCalories, recipesWithMinProtein,
    recipesWithMaxTime, isVegan, getDifficulty,
    breakfastRecipesCount, lunchRecipesCount, dinnerRecipesCount
)

# Load recipe data from JSON (populates the default knowledge graph)
recipes_path = Path("data/recipes.json")
num_recipes = load_recipes_from_json(str(recipes_path))
print(f"Loaded {num_recipes} recipes into the knowledge graph")

# Count by meal type (queries default KG)
print(f"\nRecipes by meal type:")
print(f"  Breakfast: {breakfastRecipesCount()}")
print(f"  Lunch: {lunchRecipesCount()}")
print(f"  Dinner: {dinnerRecipesCount()}")

# Find recipes matching criteria (queries default KG)
low_cal = recipesWithMaxCalories(300)
high_protein = recipesWithMinProtein(30)
quick = recipesWithMaxTime(30)

print(f"\nFound {len(low_cal)} low-calorie recipes")
print(f"Found {len(high_protein)} high-protein recipes")
print(f"Found {len(quick)} quick recipes")

# Combine filters
quick_protein = [r for r in high_protein if r in quick]
print(f"\n{len(quick_protein)} recipes are both quick and high-protein")

# Filter by dietary restrictions
vegan_low_cal = [r for r in low_cal if isVegan(r)]
print(f"{len(vegan_low_cal)} low-calorie recipes are vegan")

# Save knowledge graph
kg_onto.save("feinschmecker.rdf")
print("\nKnowledge graph saved!")
```

---

## Examining Recipe Details

### Accessing Recipe Properties

```python
from ontology import kg_onto, Recipe

# Get all recipes from default KG
all_recipes = list(kg_onto.search(type=Recipe))

if all_recipes:
    recipe = all_recipes[0]
    
    # Basic information
    print(f"Recipe: {recipe.has_recipe_name[0]}")
    print(f"Difficulty: {recipe.has_difficulty[0].has_numeric_difficulty[0]}/3")
    print(f"Time: {recipe.requires_time[0].amount_of_time[0]} minutes")
    
    # Dietary properties
    print(f"\nDietary Information:")
    print(f"  Vegan: {recipe.is_vegan[0]}")
    print(f"  Vegetarian: {recipe.is_vegetarian[0]}")
    
    # Nutritional information
    print(f"\nNutritional Information:")
    print(f"  Calories: {recipe.has_calories[0].amount_of_calories[0]} kcal")
    print(f"  Protein: {recipe.has_protein[0].amount_of_protein[0]}g")
    print(f"  Fat: {recipe.has_fat[0].amount_of_fat[0]}g")
    print(f"  Carbs: {recipe.has_carbohydrates[0].amount_of_carbohydrates[0]}g")
    
    # Ingredients
    print(f"\nIngredients ({len(recipe.has_ingredient)}):")
    for ing in recipe.has_ingredient:
        print(f"  - {ing.has_ingredient_with_amount_name[0]}")
    
    # Instructions
    print(f"\nInstructions:")
    print(recipe.has_instructions[0])
    
    # Links (if available)
    if recipe.has_link:
        print(f"\nSource: {recipe.has_link[0]}")
    if recipe.has_image_link:
        print(f"Image: {recipe.has_image_link[0]}")
```

---

## Creating Custom Recipes

### Step-by-Step Recipe Creation

```python
from ontology import (
    kg_onto, Recipe, Ingredient, IngredientWithAmount,
    createIndividual, create_meal_types, create_difficulties
)

# Ensure meal types and difficulties exist in default KG
meal_types = create_meal_types()
difficulties = create_difficulties()

# Create a new recipe in default KG
recipe, is_new = createIndividual("green_smoothie_bowl", Recipe)

# Set basic properties
recipe.has_recipe_name.append("Green Smoothie Bowl")
recipe.has_instructions.append(
    "1. Blend spinach, frozen banana, and almond milk until smooth. "
    "2. Pour into a bowl. "
    "3. Top with granola, fresh berries, and chia seeds. "
    "4. Serve immediately."
)

# Set dietary properties
recipe.is_vegan.append(True)
recipe.is_vegetarian.append(True)

# Set meal type
recipe.is_meal_type.append(meal_types["Breakfast"])

# Set difficulty (easy)
recipe.has_difficulty.append(difficulties[0])

# Set preparation time
time_obj, _ = createIndividual("green_smoothie_bowl_time", onto.Time)
time_obj.amount_of_time.append(10)
recipe.requires_time.append(time_obj)

# Add nutritional information
cal_obj, _ = createIndividual("green_smoothie_bowl_calories", onto.Calories)
cal_obj.amount_of_calories.append(350.0)
recipe.has_calories.append(cal_obj)

prot_obj, _ = createIndividual("green_smoothie_bowl_protein", onto.Protein)
prot_obj.amount_of_protein.append(12.0)
recipe.has_protein.append(prot_obj)

fat_obj, _ = createIndividual("green_smoothie_bowl_fat", onto.Fat)
fat_obj.amount_of_fat.append(8.0)
recipe.has_fat.append(fat_obj)

carb_obj, _ = createIndividual("green_smoothie_bowl_carbs", onto.Carbohydrates)
carb_obj.amount_of_carbohydrates.append(55.0)
recipe.has_carbohydrates.append(carb_obj)

# Add ingredients
def add_ingredient(recipe_name, ing_name, amount, unit):
    """Helper function to add ingredients"""
    # Create or get base ingredient
    base_ing, _ = createIndividual(ing_name.replace(" ", "_"), Ingredient)
    base_ing.has_ingredient_name.append(ing_name)
    
    # Create ingredient with amount
    ing_id = f"{recipe_name}_{ing_name.replace(' ', '_')}"
    ing_with_amt, _ = createIndividual(ing_id, IngredientWithAmount)
    ing_with_amt.has_ingredient_with_amount_name.append(f"{amount} {unit} {ing_name}")
    ing_with_amt.amount_of_ingredient.append(float(amount))
    ing_with_amt.unit_of_ingredient.append(unit)
    ing_with_amt.type_of_ingredient.append(base_ing)
    
    return ing_with_amt

# Add all ingredients
recipe.has_ingredient.append(add_ingredient("green_smoothie_bowl", "spinach", 2, "cups"))
recipe.has_ingredient.append(add_ingredient("green_smoothie_bowl", "banana", 1, "whole"))
recipe.has_ingredient.append(add_ingredient("green_smoothie_bowl", "almond milk", 0.5, "cup"))
recipe.has_ingredient.append(add_ingredient("green_smoothie_bowl", "granola", 0.25, "cup"))
recipe.has_ingredient.append(add_ingredient("green_smoothie_bowl", "berries", 0.5, "cup"))
recipe.has_ingredient.append(add_ingredient("green_smoothie_bowl", "chia seeds", 1, "tbsp"))

print("Recipe created successfully!")

# Save
kg_onto.save("feinschmecker_extended.rdf")
```

---

## Working with Multiple Knowledge Graphs

The ontology supports managing recipes from different sources in separate knowledge graphs while sharing the same schema.

### Creating and Loading Multiple Sources

```python
from ontology import create_kg, load_recipes_from_json, schema_onto

# Create separate KGs for different recipe sources
kg_bbc = create_kg("bbc")
kg_allrecipes = create_kg("allrecipes")
kg_foodnetwork = create_kg("foodnetwork")

# Load data into each KG
load_recipes_from_json("data/bbc_recipes.json", target_kg=kg_bbc)
load_recipes_from_json("data/allrecipes.json", target_kg=kg_allrecipes)
load_recipes_from_json("data/foodnetwork.json", target_kg=kg_foodnetwork)

# Save schema once (shared by all)
schema_onto.save("feinschmecker_schema.rdf")

# Save each KG separately
kg_bbc.save("kg_bbc.rdf")
kg_allrecipes.save("kg_allrecipes.rdf")
kg_foodnetwork.save("kg_foodnetwork.rdf")
```

### Querying Specific Knowledge Graphs

```python
from ontology import recipesWithMaxCalories, recipesWithMinProtein, create_kg

# Get KG references
kg_bbc = create_kg("bbc")
kg_ar = create_kg("allrecipes")

# Query each source separately
bbc_low_cal = recipesWithMaxCalories(300, kg=kg_bbc)
ar_low_cal = recipesWithMaxCalories(300, kg=kg_ar)

print(f"BBC Food: {len(bbc_low_cal)} low-calorie recipes")
print(f"AllRecipes: {len(ar_low_cal)} low-calorie recipes")

# Find high-protein recipes in each source
bbc_protein = recipesWithMinProtein(30, kg=kg_bbc)
ar_protein = recipesWithMinProtein(30, kg=kg_ar)
```

### Combining Results from Multiple Sources

```python
# Union: All unique low-calorie recipes from both sources
all_low_cal = set(bbc_low_cal) | set(ar_low_cal)
print(f"Total unique low-calorie recipes: {len(all_low_cal)}")

# Find recipes that meet criteria in both sources
bbc_matches = set(recipesWithMaxCalories(400, kg=kg_bbc))
ar_matches = set(recipesWithMaxCalories(400, kg=kg_ar))
combined = bbc_matches | ar_matches

# Filter combined results
from ontology import isVegan
vegan_combined = [r for r in combined if isVegan(r)]
print(f"Vegan recipes across both sources: {len(vegan_combined)}")
```

### Comparing Recipe Sources

```python
from ontology import kg_onto, Recipe, isVegan, isVegetarian

def analyze_source(kg, source_name):
    """Analyze recipes from a specific source"""
    all_recipes = list(kg.search(type=Recipe))
    
    if not all_recipes:
        print(f"{source_name}: No recipes found")
        return
    
    # Count by dietary restrictions
    vegan_count = len([r for r in all_recipes if isVegan(r, kg=kg)])
    vegetarian_count = len([r for r in all_recipes if isVegetarian(r, kg=kg)])
    
    # Calculate nutritional averages
    avg_calories = sum(r.has_calories[0].amount_of_calories[0] 
                      for r in all_recipes) / len(all_recipes)
    avg_protein = sum(r.has_protein[0].amount_of_protein[0] 
                     for r in all_recipes) / len(all_recipes)
    
    # Print analysis
    print(f"\n{source_name} Analysis:")
    print(f"  Total recipes: {len(all_recipes)}")
    print(f"  Vegan: {vegan_count} ({vegan_count/len(all_recipes)*100:.1f}%)")
    print(f"  Vegetarian: {vegetarian_count} ({vegetarian_count/len(all_recipes)*100:.1f}%)")
    print(f"  Avg calories: {avg_calories:.1f} kcal")
    print(f"  Avg protein: {avg_protein:.1f}g")

# Analyze each source
kg_bbc = create_kg("bbc")
kg_ar = create_kg("allrecipes")

analyze_source(kg_bbc, "BBC Food")
analyze_source(kg_ar, "AllRecipes")
```

### Creating Individuals in Specific KGs

```python
from ontology import Recipe, createIndividual, create_kg

# Create a custom KG for user-submitted recipes
kg_user = create_kg("user_submissions")

# Create recipe in specific KG
user_recipe, is_new = createIndividual("user_chocolate_cake", Recipe, target_kg=kg_user)
user_recipe.has_recipe_name.append("User's Chocolate Cake")
# ... set other properties ...

# Save user KG separately
kg_user.save("kg_user_submissions.rdf")
```

---

## Advanced Filtering Patterns

### Multi-Criteria Recipe Search

```python
from ontology import kg_onto, Recipe

def find_recipes(
    max_calories=None,
    min_protein=None,
    max_time=None,
    vegan=None,
    vegetarian=None,
    difficulty=None,
    meal_type=None
):
    """
    Find recipes matching multiple criteria.
    
    Args:
        max_calories: Maximum calories (kcal)
        min_protein: Minimum protein (grams)
        max_time: Maximum preparation time (minutes)
        vegan: Boolean for vegan recipes
        vegetarian: Boolean for vegetarian recipes
        difficulty: Difficulty level (1, 2, or 3)
        meal_type: Meal type ("Breakfast", "Lunch", or "Dinner")
    
    Returns:
        List of matching recipes
    """
    recipes = list(kg_onto.search(type=Recipe))
    
    # Apply filters
    if max_calories is not None:
        recipes = [r for r in recipes 
                  if r.has_calories[0].amount_of_calories[0] <= max_calories]
    
    if min_protein is not None:
        recipes = [r for r in recipes 
                  if r.has_protein[0].amount_of_protein[0] >= min_protein]
    
    if max_time is not None:
        recipes = [r for r in recipes 
                  if r.requires_time[0].amount_of_time[0] <= max_time]
    
    if vegan is not None:
        recipes = [r for r in recipes if r.is_vegan[0] == vegan]
    
    if vegetarian is not None:
        recipes = [r for r in recipes if r.is_vegetarian[0] == vegetarian]
    
    if difficulty is not None:
        recipes = [r for r in recipes 
                  if r.has_difficulty[0].has_numeric_difficulty[0] == difficulty]
    
    if meal_type is not None:
        recipes = [r for r in recipes 
                  if any(mt.has_meal_type_name[0] == meal_type 
                        for mt in r.is_meal_type)]
    
    return recipes

# Example: Find easy vegan breakfast recipes under 400 calories
results = find_recipes(
    max_calories=400,
    vegan=True,
    difficulty=1,
    meal_type="Breakfast"
)

print(f"Found {len(results)} matching recipes:")
for recipe in results:
    print(f"  - {recipe.has_recipe_name[0]}")
```

---

### Nutritional Analysis

```python
from ontology import kg_onto, Recipe
import statistics

def analyze_nutrition():
    """Analyze nutritional statistics across all recipes"""
    recipes = list(kg_onto.search(type=Recipe))
    
    calories = [r.has_calories[0].amount_of_calories[0] for r in recipes]
    protein = [r.has_protein[0].amount_of_protein[0] for r in recipes]
    fat = [r.has_fat[0].amount_of_fat[0] for r in recipes]
    carbs = [r.has_carbohydrates[0].amount_of_carbohydrates[0] for r in recipes]
    
    print("Nutritional Statistics Across All Recipes")
    print("=" * 50)
    
    print(f"\nCalories (kcal):")
    print(f"  Average: {statistics.mean(calories):.1f}")
    print(f"  Median: {statistics.median(calories):.1f}")
    print(f"  Min: {min(calories):.1f}")
    print(f"  Max: {max(calories):.1f}")
    
    print(f"\nProtein (g):")
    print(f"  Average: {statistics.mean(protein):.1f}")
    print(f"  Median: {statistics.median(protein):.1f}")
    print(f"  Min: {min(protein):.1f}")
    print(f"  Max: {max(protein):.1f}")
    
    print(f"\nFat (g):")
    print(f"  Average: {statistics.mean(fat):.1f}")
    print(f"  Median: {statistics.median(fat):.1f}")
    print(f"  Min: {min(fat):.1f}")
    print(f"  Max: {max(fat):.1f}")
    
    print(f"\nCarbohydrates (g):")
    print(f"  Average: {statistics.mean(carbs):.1f}")
    print(f"  Median: {statistics.median(carbs):.1f}")
    print(f"  Min: {min(carbs):.1f}")
    print(f"  Max: {max(carbs):.1f}")

analyze_nutrition()
```

---

### Finding Similar Recipes

```python
from ontology import kg_onto, Recipe

def find_similar_recipes(recipe, tolerance=0.1, kg=None):
    """
    Find recipes with similar nutritional profiles.
    
    Args:
        recipe: The reference recipe
        tolerance: Allowed deviation (0.1 = 10%)
        kg: Knowledge graph to search (defaults to kg_onto)
    
    Returns:
        List of similar recipes
    """
    if kg is None:
        kg = kg_onto
    
    ref_cal = recipe.has_calories[0].amount_of_calories[0]
    ref_prot = recipe.has_protein[0].amount_of_protein[0]
    ref_fat = recipe.has_fat[0].amount_of_fat[0]
    ref_carb = recipe.has_carbohydrates[0].amount_of_carbohydrates[0]
    
    all_recipes = list(kg.search(type=Recipe))
    similar = []
    
    for r in all_recipes:
        if r == recipe:
            continue
        
        cal = r.has_calories[0].amount_of_calories[0]
        prot = r.has_protein[0].amount_of_protein[0]
        fat = r.has_fat[0].amount_of_fat[0]
        carb = r.has_carbohydrates[0].amount_of_carbohydrates[0]
        
        # Check if all nutrients are within tolerance
        if (abs(cal - ref_cal) <= ref_cal * tolerance and
            abs(prot - ref_prot) <= ref_prot * tolerance and
            abs(fat - ref_fat) <= ref_fat * tolerance and
            abs(carb - ref_carb) <= ref_carb * tolerance):
            similar.append(r)
    
    return similar

# Example usage
recipes = list(kg_onto.search(type=Recipe))
if recipes:
    ref_recipe = recipes[0]
    similar = find_similar_recipes(ref_recipe, tolerance=0.15)
    
    print(f"Recipes similar to {ref_recipe.has_recipe_name[0]}:")
    for r in similar:
        print(f"  - {r.has_recipe_name[0]}")
```

---

## Working with Ingredients

### Listing All Ingredients

```python
from ontology import kg_onto, Ingredient

# Get all unique ingredients from default KG
ingredients = list(kg_onto.search(type=Ingredient))

print(f"Total unique ingredients: {len(ingredients)}")
print("\nIngredients:")
for ing in sorted(ingredients, key=lambda x: x.has_ingredient_name[0]):
    print(f"  - {ing.has_ingredient_name[0]}")
```

---

### Finding Recipes by Ingredient

```python
from ontology import kg_onto, Ingredient

def recipes_containing_ingredient(ingredient_name, kg=None):
    """Find all recipes containing a specific ingredient"""
    if kg is None:
        kg = kg_onto
    
    # Search for the ingredient
    ingredients = kg.search(
        type=Ingredient,
        has_ingredient_name=ingredient_name
    )
    
    if not ingredients:
        print(f"Ingredient '{ingredient_name}' not found")
        return []
    
    ingredient = ingredients[0]
    recipes = []
    
    # Get all IngredientWithAmount instances for this ingredient
    for ing_with_amt in ingredient.is_ingredient_of:
        # Each IngredientWithAmount is used for recipes
        recipes.extend(ing_with_amt.used_for)
    
    return recipes

# Example usage
chicken_recipes = recipes_containing_ingredient("chicken")
print(f"Found {len(chicken_recipes)} recipes with chicken:")
for recipe in chicken_recipes:
    print(f"  - {recipe.has_recipe_name[0]}")
```

---

### Ingredient Frequency Analysis

```python
from ontology import kg_onto, Ingredient
from collections import Counter

def analyze_ingredient_frequency(kg=None):
    """Analyze which ingredients are most commonly used"""
    if kg is None:
        kg = kg_onto
    
    ingredients = list(kg.search(type=Ingredient))
    
    ingredient_counts = {}
    for ing in ingredients:
        name = ing.has_ingredient_name[0]
        # Count how many recipes use this ingredient
        count = sum(len(ing_amt.used_for) 
                   for ing_amt in ing.is_ingredient_of)
        ingredient_counts[name] = count
    
    # Sort by frequency
    sorted_ingredients = sorted(
        ingredient_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    print("Most Common Ingredients:")
    print("=" * 50)
    for ing, count in sorted_ingredients[:20]:
        print(f"  {ing}: {count} recipes")

analyze_ingredient_frequency()
```

---

## Batch Operations

### Updating Multiple Recipes

```python
from ontology import kg_onto, Recipe

def update_difficulty_based_on_time(kg=None):
    """Update difficulty based on preparation time"""
    if kg is None:
        kg = kg_onto
    
    recipes = list(kg.search(type=Recipe))
    
    for recipe in recipes:
        time = recipe.requires_time[0].amount_of_time[0]
        num_ingredients = len(recipe.has_ingredient)
        
        # Calculate difficulty based on time and ingredients
        if time <= 20 and num_ingredients <= 5:
            new_difficulty = 1  # Easy
        elif time <= 45 and num_ingredients <= 10:
            new_difficulty = 2  # Moderate
        else:
            new_difficulty = 3  # Difficult
        
        # Update if different
        current_difficulty = recipe.has_difficulty[0].has_numeric_difficulty[0]
        if current_difficulty != new_difficulty:
            print(f"Updating {recipe.has_recipe_name[0]}: "
                  f"{current_difficulty} -> {new_difficulty}")
            recipe.has_difficulty[0].has_numeric_difficulty[0] = new_difficulty
    
    kg.save("feinschmecker_updated.rdf")
    print("Batch update complete!")
```

---

## Export and Reporting

### Generate Recipe Report

```python
from ontology import kg_onto, Recipe
import json

def export_recipes_to_json(filename, kg=None):
    """Export all recipes to a JSON file"""
    if kg is None:
        kg = kg_onto
    
    recipes = list(kg.search(type=Recipe))
    
    data = []
    for recipe in recipes:
        recipe_data = {
            "name": recipe.has_recipe_name[0],
            "instructions": recipe.has_instructions[0],
            "vegan": recipe.is_vegan[0],
            "vegetarian": recipe.is_vegetarian[0],
            "difficulty": recipe.has_difficulty[0].has_numeric_difficulty[0],
            "time": recipe.requires_time[0].amount_of_time[0],
            "nutrition": {
                "calories": recipe.has_calories[0].amount_of_calories[0],
                "protein": recipe.has_protein[0].amount_of_protein[0],
                "fat": recipe.has_fat[0].amount_of_fat[0],
                "carbohydrates": recipe.has_carbohydrates[0].amount_of_carbohydrates[0]
            },
            "ingredients": [
                ing.has_ingredient_with_amount_name[0]
                for ing in recipe.has_ingredient
            ],
            "meal_types": [
                mt.has_meal_type_name[0]
                for mt in recipe.is_meal_type
            ]
        }
        
        if recipe.has_link:
            recipe_data["link"] = recipe.has_link[0]
        if recipe.has_image_link:
            recipe_data["image"] = recipe.has_image_link[0]
        
        data.append(recipe_data)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Exported {len(data)} recipes to {filename}")

export_recipes_to_json("recipes_export.json")
```

---

### Generate HTML Report

```python
from ontology import kg_onto, Recipe

def generate_html_report(filename, kg=None):
    """Generate an HTML report of all recipes"""
    if kg is None:
        kg = kg_onto
    
    recipes = list(kg.search(type=Recipe))
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Feinschmecker Recipe Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .recipe { border: 1px solid #ddd; padding: 15px; margin: 10px 0; }
            .nutrition { background: #f5f5f5; padding: 10px; margin: 10px 0; }
            .tag { display: inline-block; background: #4CAF50; color: white; 
                   padding: 3px 8px; margin: 2px; border-radius: 3px; font-size: 12px; }
        </style>
    </head>
    <body>
        <h1>Feinschmecker Recipe Report</h1>
        <p>Total recipes: {}</p>
    """.format(len(recipes))
    
    for recipe in sorted(recipes, key=lambda r: r.has_recipe_name[0]):
        html += f"""
        <div class="recipe">
            <h2>{recipe.has_recipe_name[0]}</h2>
            <p><strong>Time:</strong> {recipe.requires_time[0].amount_of_time[0]} minutes | 
               <strong>Difficulty:</strong> {recipe.has_difficulty[0].has_numeric_difficulty[0]}/3</p>
        """
        
        # Tags
        if recipe.is_vegan[0]:
            html += '<span class="tag">Vegan</span>'
        if recipe.is_vegetarian[0]:
            html += '<span class="tag">Vegetarian</span>'
        
        # Nutrition
        html += f"""
            <div class="nutrition">
                <strong>Nutrition:</strong>
                {recipe.has_calories[0].amount_of_calories[0]:.0f} kcal | 
                P: {recipe.has_protein[0].amount_of_protein[0]:.1f}g | 
                F: {recipe.has_fat[0].amount_of_fat[0]:.1f}g | 
                C: {recipe.has_carbohydrates[0].amount_of_carbohydrates[0]:.1f}g
            </div>
        """
        
        # Ingredients
        html += "<p><strong>Ingredients:</strong></p><ul>"
        for ing in recipe.has_ingredient:
            html += f"<li>{ing.has_ingredient_with_amount_name[0]}</li>"
        html += "</ul>"
        
        html += "</div>"
    
    html += "</body></html>"
    
    with open(filename, 'w') as f:
        f.write(html)
    
    print(f"Generated HTML report: {filename}")

generate_html_report("recipe_report.html")
```

---

## Best Practices

### 1. Always Check for Existing Individuals

```python
from ontology import createIndividual, Recipe

# Use unique=True to avoid duplicates
recipe, is_new = createIndividual("my_recipe", Recipe, unique=True)

if is_new:
    print("Created new recipe")
else:
    print("Recipe already exists, retrieved existing one")
```

### 2. Validate Data Before Adding

```python
def add_recipe_safely(name, **kwargs):
    """Add a recipe with validation"""
    required_fields = ['instructions', 'calories', 'protein', 'fat', 'carbohydrates']
    
    for field in required_fields:
        if field not in kwargs:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate numeric values
    if kwargs['calories'] < 0 or kwargs['protein'] < 0:
        raise ValueError("Nutritional values must be non-negative")
    
    # Proceed with creation...
    # (recipe creation code here)
```

### 3. Use Context Managers for Bulk Operations

```python
from ontology import kg_onto

# For performance, batch updates
with kg_onto:
    for i in range(100):
        # Create many individuals
        pass

# Save once after all updates
kg_onto.save("output.rdf")
```

---

[Back to Overview](README.md) | [Previous: Query API](queries.md) | [Next: Development](development.md)

