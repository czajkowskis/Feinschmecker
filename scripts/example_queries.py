#!/usr/bin/env python3
"""
Example script demonstrating how to query the Feinschmecker ontology.

This script shows how to use the refactored ontology package to:
- Load and query recipes
- Filter by nutritional content
- Check dietary properties
- Count recipes by meal type
"""

import sys
from pathlib import Path

# Add parent directory to path to import ontology package
sys.path.insert(0, str(Path(__file__).parent.parent))

from ontology import (
    load_recipes_from_json, onto,
    recipesWithMaxCalories, recipesWithMinProtein,
    recipesWithMaxFat, recipesWithMaxTime,
    breakfastRecipesCount, lunchRecipesCount, dinnerRecipesCount,
    getRecipe, isVegan, isVegetarian, getDifficulty, requiredIngredients
)


def main():
    print("=" * 60)
    print("Feinschmecker Ontology Query Examples")
    print("=" * 60)
    
    # Load recipes
    print("\n1. Loading recipes from JSON...")
    recipes_path = Path(__file__).parent.parent / "data" / "recipes.json"
    if not recipes_path.exists():
        print(f"Error: Recipe file not found at {recipes_path}")
        return
    
    num_recipes = load_recipes_from_json(str(recipes_path))
    print(f"   Loaded {num_recipes} recipes")
    
    # Count recipes by meal type
    print("\n2. Counting recipes by meal type...")
    print(f"   Breakfast recipes: {breakfastRecipesCount()}")
    print(f"   Lunch recipes: {lunchRecipesCount()}")
    print(f"   Dinner recipes: {dinnerRecipesCount()}")
    
    # Find low-calorie recipes
    print("\n3. Finding recipes with max 300 calories...")
    low_cal = recipesWithMaxCalories(300)
    print(f"   Found {len(low_cal)} recipes")
    if low_cal:
        print(f"   Examples: {[r.name for r in low_cal[:3]]}")
    
    # Find high-protein recipes
    print("\n4. Finding recipes with at least 30g protein...")
    high_protein = recipesWithMinProtein(30)
    print(f"   Found {len(high_protein)} recipes")
    if high_protein:
        print(f"   Examples: {[r.name for r in high_protein[:3]]}")
    
    # Find low-fat recipes
    print("\n5. Finding recipes with max 15g fat...")
    low_fat = recipesWithMaxFat(15)
    print(f"   Found {len(low_fat)} recipes")
    if low_fat:
        print(f"   Examples: {[r.name for r in low_fat[:3]]}")
    
    # Find quick recipes
    print("\n6. Finding recipes that take 30 minutes or less...")
    quick_recipes = recipesWithMaxTime(30)
    print(f"   Found {len(quick_recipes)} recipes")
    if quick_recipes:
        print(f"   Examples: {[r.name for r in quick_recipes[:3]]}")
    
    # Query specific recipe (if available)
    print("\n7. Detailed information about a specific recipe...")
    all_recipes = list(onto.search(type=onto.Recipe))
    if all_recipes:
        example_recipe = all_recipes[0]
        print(f"   Recipe: {example_recipe.has_recipe_name[0]}")
        print(f"   Vegan: {example_recipe.is_vegan[0]}")
        print(f"   Vegetarian: {example_recipe.is_vegetarian[0]}")
        print(f"   Difficulty: {example_recipe.has_difficulty[0].has_numeric_difficulty[0]}")
        print(f"   Calories: {example_recipe.has_calories[0].amount_of_calories[0]} kcal")
        print(f"   Protein: {example_recipe.has_protein[0].amount_of_protein[0]}g")
        print(f"   Fat: {example_recipe.has_fat[0].amount_of_fat[0]}g")
        print(f"   Carbs: {example_recipe.has_carbohydrates[0].amount_of_carbohydrates[0]}g")
        print(f"   Time: {example_recipe.requires_time[0].amount_of_time[0]} minutes")
        print(f"   Number of ingredients: {len(example_recipe.has_ingredient)}")
    
    print("\n" + "=" * 60)
    print("Query examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()

