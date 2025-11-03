"""
Feinschmecker Recipe Ontology

A comprehensive OWL ontology for recipe knowledge representation using owlready2.
This package provides classes, properties, and utilities for managing recipe data
in a semantic web format.

Usage:
    from ontology import onto, Recipe, load_recipes_from_json
    from ontology import recipesWithMaxCalories
    
    # Load recipe data
    load_recipes_from_json('path/to/recipes.json')
    
    # Query recipes
    low_cal_recipes = recipesWithMaxCalories(300)
    
    # Save ontology
    onto.save('feinschmecker.rdf')
"""

# Core ontology setup
from .setup import onto, NAMESPACE

# Factory functions
from .factories import ThingFactory, RelationFactory, DataFactory, makeInverse

# Classes
from .classes import (
    Recipe, Ingredient, IngredientWithAmount, Author, Source,
    Time, MealType, Difficulty, Nutrients, Calories, Protein, Fat, Carbohydrates
)

# Properties
from .properties import (
    # Meta properties
    has_name, has_amount,
    
    # Recipe properties
    has_recipe_name, has_instructions, has_ingredient, authored_by, requires_time,
    is_meal_type, has_difficulty, is_vegan, is_vegetarian, has_calories, has_protein,
    has_fat, has_carbohydrates, has_link, has_image_link,
    
    # Ingredient properties
    has_ingredient_name, is_ingredient_of,
    
    # IngredientWithAmount properties
    has_ingredient_with_amount_name, used_for, type_of_ingredient,
    amount_of_ingredient, unit_of_ingredient,
    
    # Author properties
    has_author_name, authored, is_author_of,
    
    # Source properties
    has_source_name, has_author, is_website,
    
    # Time properties
    time_required_by, amount_of_time,
    
    # MealType properties
    meal_type_of, has_meal_type_name,
    
    # Difficulty properties
    difficulty_of, has_numeric_difficulty,
    
    # Nutrient properties
    calories_of, amount_of_calories, protein_of, amount_of_protein,
    fat_of, amount_of_fat, carbohydrates_of, amount_of_carbohydrates
)

# Constraints
from .constraints import (
    setup_inverse_properties, setup_cardinality_constraints,
    setup_disjointness, apply_all_constraints
)

# Individual creation
from .individuals import (
    onthologifyName, createIndividual, create_meal_types, create_difficulties,
    load_recipes_from_json
)

# Query functions
from .queries import (
    getAll, getRecipe, requiredIngredients,
    recipesWithMaxCalories, recipesWithMinCalories,
    recipesWithMaxProtein, recipesWithMinProtein,
    recipesWithMaxFat, recipesWithMinFat,
    recipesWithMaxCarbohydrates, recipesWithMinCarbohydrates,
    recipesWithMaxTime,
    isVegan, isVegetarian, getDifficulty,
    breakfastRecipesCount, lunchRecipesCount, dinnerRecipesCount
)

# Apply all constraints when the module is imported
apply_all_constraints()

__all__ = [
    # Core
    'onto', 'NAMESPACE',
    
    # Factories
    'ThingFactory', 'RelationFactory', 'DataFactory', 'makeInverse',
    
    # Classes
    'Recipe', 'Ingredient', 'IngredientWithAmount', 'Author', 'Source',
    'Time', 'MealType', 'Difficulty', 'Nutrients', 'Calories', 'Protein', 'Fat', 'Carbohydrates',
    
    # Properties (main ones - full list available in .properties)
    'has_recipe_name', 'has_instructions', 'has_ingredient', 'authored_by',
    'requires_time', 'is_meal_type', 'has_difficulty', 'is_vegan', 'is_vegetarian',
    'has_calories', 'has_protein', 'has_fat', 'has_carbohydrates',
    
    # Constraints
    'apply_all_constraints',
    
    # Individual creation
    'createIndividual', 'onthologifyName', 'load_recipes_from_json',
    
    # Queries
    'getRecipe', 'requiredIngredients',
    'recipesWithMaxCalories', 'recipesWithMinCalories',
    'recipesWithMaxProtein', 'recipesWithMinProtein',
    'recipesWithMaxFat', 'recipesWithMinFat',
    'recipesWithMaxCarbohydrates', 'recipesWithMinCarbohydrates',
    'recipesWithMaxTime',
    'isVegan', 'isVegetarian', 'getDifficulty',
    'breakfastRecipesCount', 'lunchRecipesCount', 'dinnerRecipesCount'
]

