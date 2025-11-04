"""
Feinschmecker Recipe Ontology

A comprehensive OWL ontology for recipe knowledge representation using owlready2.
This package provides classes, properties, and utilities for managing recipe data
in a semantic web format.

The ontology supports multiple knowledge graphs:
- schema_onto: Contains the TBox (classes, properties, constraints)
- Multiple KG ontologies: Each contains ABox (individuals/instances) and imports the schema
- create_kg(): Factory function to create new knowledge graphs for different sources

Basic Usage:
    from ontology import schema_onto, kg_onto, Recipe, load_recipes_from_json
    from ontology import recipesWithMaxCalories
    
    # Load recipe data into default KG
    load_recipes_from_json('path/to/recipes.json')
    
    # Query recipes
    low_cal_recipes = recipesWithMaxCalories(300)
    
    # Save files
    schema_onto.save('feinschmecker-schema.rdf')
    kg_onto.save('feinschmecker-kg.rdf')

Multi-Source Usage:
    from ontology import create_kg, load_recipes_from_json, recipesWithMaxCalories
    
    # Create source-specific KGs
    kg_bbc = create_kg("bbc")
    kg_allrecipes = create_kg("allrecipes")
    
    # Load data into specific KGs
    load_recipes_from_json('bbc_recipes.json', target_kg=kg_bbc)
    load_recipes_from_json('allrecipes.json', target_kg=kg_allrecipes)
    
    # Query specific KG
    bbc_low_cal = recipesWithMaxCalories(300, kg=kg_bbc)
    
    # Save separately
    kg_bbc.save('kg-bbc.rdf')
    kg_allrecipes.save('kg-allrecipes.rdf')
"""

# Core ontology setup
from .setup import schema_onto, kg_onto, onto, NAMESPACE, create_kg, knowledge_graphs

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
    # Core - Schema and multiple KGs
    'schema_onto',  # Schema ontology (TBox): classes, properties, constraints
    'kg_onto',      # Default knowledge graph ontology (ABox): individuals/instances
    'onto',         # Alias for kg_onto (deprecated, for backward compatibility)
    'NAMESPACE',
    'create_kg',    # Factory function to create new knowledge graphs
    'knowledge_graphs',  # Registry of all created knowledge graphs
    
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

