"""
OWL constraints including inverse relationships, cardinality restrictions, and disjointness.
"""

from owlready2 import AllDisjoint
from .setup import onto
from .classes import (
    Recipe, Ingredient, IngredientWithAmount, Author, Source,
    Time, MealType, Difficulty, Nutrients, Calories, Protein, Fat, Carbohydrates
)
from .properties import (
    has_ingredient, used_for, is_ingredient_of, type_of_ingredient,
    authored_by, authored, is_author_of, has_author, requires_time, time_required_by,
    is_meal_type, meal_type_of, has_difficulty, difficulty_of,
    has_calories, calories_of, has_protein, protein_of, has_fat, fat_of,
    has_carbohydrates, carbohydrates_of,
    has_recipe_name, has_instructions, is_vegan, is_vegetarian, has_link,
    has_ingredient_name, has_ingredient_with_amount_name, amount_of_ingredient,
    unit_of_ingredient, has_author_name, has_source_name, is_website,
    amount_of_time, has_meal_type_name, has_numeric_difficulty,
    amount_of_calories, amount_of_protein, amount_of_fat, amount_of_carbohydrates
)
from .factories import makeInverse


def setup_inverse_properties():
    """Define inverse relationships between object properties."""
    makeInverse(has_ingredient, used_for)
    makeInverse(is_ingredient_of, type_of_ingredient)
    makeInverse(authored_by, authored)
    makeInverse(is_author_of, has_author)
    makeInverse(requires_time, time_required_by)
    makeInverse(is_meal_type, meal_type_of)
    makeInverse(has_difficulty, difficulty_of)
    makeInverse(has_calories, calories_of)
    makeInverse(has_protein, protein_of)
    makeInverse(has_fat, fat_of)
    makeInverse(has_carbohydrates, carbohydrates_of)


def setup_cardinality_constraints():
    """Define cardinality and other restrictions on classes."""
    with onto:
        # Recipe constraints
        Recipe.is_a.append(has_recipe_name.exactly(1, str))
        Recipe.is_a.append(has_instructions.exactly(1, str))
        Recipe.is_a.append(has_ingredient.some(IngredientWithAmount))
        Recipe.is_a.append(authored_by.exactly(1, Author))
        Recipe.is_a.append(requires_time.exactly(1, Time))
        Recipe.is_a.append(is_vegan.max(1, bool))
        Recipe.is_a.append(is_vegetarian.max(1, bool))
        Recipe.is_a.append(is_meal_type.max(1, MealType))
        Recipe.is_a.append(has_difficulty.exactly(1, Difficulty))
        Recipe.is_a.append(has_calories.exactly(1, Calories))
        Recipe.is_a.append(has_protein.exactly(1, Protein))
        Recipe.is_a.append(has_fat.exactly(1, Fat))
        Recipe.is_a.append(has_carbohydrates.exactly(1, Carbohydrates))
        Recipe.is_a.append(has_link.exactly(1, str))

        # Ingredient constraints
        Ingredient.is_a.append(has_ingredient_name.exactly(1, str))

        # IngredientWithAmount constraints
        IngredientWithAmount.is_a.append(has_ingredient_with_amount_name.exactly(1, str))
        IngredientWithAmount.is_a.append(used_for.some(Recipe))
        IngredientWithAmount.is_a.append(type_of_ingredient.exactly(1, Ingredient))
        IngredientWithAmount.is_a.append(amount_of_ingredient.exactly(1, float))
        IngredientWithAmount.is_a.append(unit_of_ingredient.exactly(1, str))

        # Author constraints
        Author.is_a.append(has_author_name.exactly(1, str))
        Author.is_a.append(is_author_of.exactly(1, Source))

        # Source constraints
        Source.is_a.append(has_source_name.exactly(1, str))
        Source.is_a.append(is_website.exactly(1, str))

        # Time constraints
        Time.is_a.append(amount_of_time.exactly(1, int))
        
        # MealType constraints
        MealType.is_a.append(has_meal_type_name.exactly(1, str))
        
        # Difficulty constraints
        Difficulty.is_a.append(has_numeric_difficulty.exactly(1, int))

        # Nutrient constraints
        Calories.is_a.append(amount_of_calories.exactly(1, float))
        Protein.is_a.append(amount_of_protein.exactly(1, float))
        Fat.is_a.append(amount_of_fat.exactly(1, float))
        Carbohydrates.is_a.append(amount_of_carbohydrates.exactly(1, float))


def setup_disjointness():
    """Define disjoint classes (classes that cannot overlap)."""
    with onto:
        AllDisjoint([Recipe, Ingredient, IngredientWithAmount, Author, Source, Time, MealType, Difficulty, Nutrients])
        AllDisjoint([Calories, Protein, Fat, Carbohydrates])


def apply_all_constraints():
    """Apply all constraints to the ontology."""
    setup_inverse_properties()
    setup_cardinality_constraints()
    setup_disjointness()

