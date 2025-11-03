"""
Query utility functions for retrieving information from the ontology.
"""

from tornado.web import MissingArgumentError
from tornado.gen import UnknownKeyError
from owlready2 import Thing
from .setup import onto
from .classes import Recipe, MealType, Calories, Protein, Fat, Carbohydrates, Time


# Utility functions
def getAll(objects: list[Thing], attribute: str) -> list:
    """
    Get all values of a specific attribute from a list of objects.
    
    Args:
        objects: List of OWL individuals
        attribute: Name of the attribute to retrieve
    
    Returns:
        List of all attribute values from all objects
    """
    result = []
    for obj in objects:
        for att in getattr(obj, attribute):
            result.append(att)
    return result


def getRecipe(recipe_name: str = None, title: str = None) -> Recipe:
    """
    Retrieve a recipe by its ontology name or title.
    
    Args:
        recipe_name: Ontology identifier for the recipe
        title: Human-readable title of the recipe
    
    Returns:
        Recipe individual
    
    Raises:
        MissingArgumentError: If neither recipe_name nor title is provided
        UnknownKeyError: If no matching recipe is found
    """
    recipe = None
    if recipe_name is None and title is None:
        raise MissingArgumentError("You must specify a recipe or title")
    if title is not None:
        recipe_tmp = onto.search(type=Recipe, has_recipe_name=title)
        if len(recipe_tmp) != 0:
            recipe = recipe_tmp[0]
    if recipe is not None and recipe_name is not None and onto[recipe_name] is not None and type(onto[recipe_name]) is Recipe:
        recipe = onto[recipe_name]
    if recipe is None:
        raise UnknownKeyError("No recipe found. Recipe name: ", recipe_name, ", title: ", title)
    return recipe


# Selection questions
def requiredIngredients(recipe: Recipe = None, title: str = None) -> list[str]:
    """
    Get the list of ingredients required for a recipe.
    
    Args:
        recipe: Recipe individual
        title: Recipe title (alternative to recipe)
    
    Returns:
        List of ingredient names with amounts
    """
    if recipe is not None:
        return getAll(recipe.has_ingredient, "has_ingredient_with_amount_name")
    return getAll(getRecipe(title=title).has_ingredient, "has_ingredient_with_amount_name")


def recipesWithMaxCalories(amount: float = 0) -> list[Recipe]:
    """
    Find recipes with calories at or below a maximum amount.
    
    Args:
        amount: Maximum calorie amount
    
    Returns:
        List of matching recipes
    """
    return getAll(filter(lambda x: (x if x.amount_of_calories[0] <= amount else None), onto.search(type=Calories)),
                  "calories_of")


def recipesWithMinCalories(amount: float = 0) -> list[Recipe]:
    """
    Find recipes with calories at or above a minimum amount.
    
    Args:
        amount: Minimum calorie amount
    
    Returns:
        List of matching recipes
    """
    return getAll(filter(lambda x: (x if x.amount_of_calories[0] >= amount else None), onto.search(type=Calories)),
                  "calories_of")


def recipesWithMaxProtein(amount: float = 0) -> list[Recipe]:
    """
    Find recipes with protein at or below a maximum amount.
    
    Args:
        amount: Maximum protein amount (grams)
    
    Returns:
        List of matching recipes
    """
    return getAll(filter(lambda x: (x if x.amount_of_protein[0] <= amount else None), onto.search(type=Protein)),
                  "protein_of")


def recipesWithMinProtein(amount: float = 0) -> list[Recipe]:
    """
    Find recipes with protein at or above a minimum amount.
    
    Args:
        amount: Minimum protein amount (grams)
    
    Returns:
        List of matching recipes
    """
    return getAll(filter(lambda x: (x if x.amount_of_protein[0] >= amount else None), onto.search(type=Protein)),
                  "protein_of")


def recipesWithMaxFat(amount: float = 0) -> list[Recipe]:
    """
    Find recipes with fat at or below a maximum amount.
    
    Args:
        amount: Maximum fat amount (grams)
    
    Returns:
        List of matching recipes
    """
    return getAll(filter(lambda x: (x if x.amount_of_fat[0] <= amount else None), onto.search(type=Fat)), "fat_of")


def recipesWithMinFat(amount: float = 0) -> list[Recipe]:
    """
    Find recipes with fat at or above a minimum amount.
    
    Args:
        amount: Minimum fat amount (grams)
    
    Returns:
        List of matching recipes
    """
    return getAll(filter(lambda x: (x if x.amount_of_fat[0] >= amount else None), onto.search(type=Fat)), "fat_of")


def recipesWithMaxCarbohydrates(amount: float = 0) -> list[Recipe]:
    """
    Find recipes with carbohydrates at or below a maximum amount.
    
    Args:
        amount: Maximum carbohydrate amount (grams)
    
    Returns:
        List of matching recipes
    """
    return getAll(
        filter(lambda x: (x if x.amount_of_carbohydrates[0] <= amount else None), onto.search(type=Carbohydrates)),
        "carbohydrates_of")


def recipesWithMinCarbohydrates(amount: float = 0) -> list[Recipe]:
    """
    Find recipes with carbohydrates at or above a minimum amount.
    
    Args:
        amount: Minimum carbohydrate amount (grams)
    
    Returns:
        List of matching recipes
    """
    return getAll(
        filter(lambda x: (x if x.amount_of_carbohydrates[0] >= amount else None), onto.search(type=Carbohydrates)),
        "carbohydrates_of")


def recipesWithMaxTime(amount: float = 0) -> list[Recipe]:
    """
    Find recipes with preparation time at or below a maximum duration.
    
    Args:
        amount: Maximum time in minutes
    
    Returns:
        List of matching recipes
    """
    return getAll(filter(lambda x: (x if x.amount_of_time[0] <= amount else None), onto.search(type=Time)),
                  "time_required_by")


# Binary questions
def isVegan(recipe: Recipe = None, title: str = None) -> bool:
    """
    Check if a recipe is vegan.
    
    Args:
        recipe: Recipe individual
        title: Recipe title (alternative to recipe)
    
    Returns:
        True if recipe is vegan, False otherwise
    """
    if recipe is not None:
        return recipe.is_vegan[0]
    return getRecipe(title=title).is_vegan[0]


def isVegetarian(recipe: Recipe = None, title: str = None) -> bool:
    """
    Check if a recipe is vegetarian.
    
    Args:
        recipe: Recipe individual
        title: Recipe title (alternative to recipe)
    
    Returns:
        True if recipe is vegetarian, False otherwise
    """
    if recipe is not None:
        return recipe.is_vegetarian[0]
    return getRecipe(title=title).is_vegetarian[0]


def getDifficulty(recipe: Recipe = None, title: str = None) -> int:
    """
    Get the difficulty level of a recipe.
    
    Args:
        recipe: Recipe individual
        title: Recipe title (alternative to recipe)
    
    Returns:
        Difficulty level (1=easy, 2=moderate, 3=difficult)
    """
    if recipe is not None:
        return recipe.has_difficulty[0].has_numeric_difficulty[0]
    return getRecipe(title=title).has_difficulty[0].has_numeric_difficulty[0]


# Counting questions
def breakfastRecipesCount() -> int:
    """
    Count the number of breakfast recipes.
    
    Returns:
        Number of breakfast recipes
    """
    return len(onto.search(type=MealType, has_meal_type_name="Breakfast")[0].meal_type_of)


def lunchRecipesCount() -> int:
    """
    Count the number of lunch recipes.
    
    Returns:
        Number of lunch recipes
    """
    return len(onto.search(type=MealType, has_meal_type_name="Lunch")[0].meal_type_of)


def dinnerRecipesCount() -> int:
    """
    Count the number of dinner recipes.
    
    Returns:
        Number of dinner recipes
    """
    return len(onto.search(type=MealType, has_meal_type_name="Dinner")[0].meal_type_of)

