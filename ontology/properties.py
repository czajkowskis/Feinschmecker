"""
OWL property definitions (data and object properties) for the Feinschmecker recipe ontology.
"""

from .factories import DataFactory, RelationFactory
from .classes import (
    Recipe, Ingredient, IngredientWithAmount, Author, Source, 
    Time, MealType, Difficulty, Calories, Protein, Fat, Carbohydrates
)

# Meta properties
has_name = DataFactory("has_name", range=[str])
has_name.comment = "A meta class of all descriptions that are identical to their name."

has_amount = DataFactory("has_amount", range=[float])
has_amount.comment = "A meta class of all descriptions that are identical to their amount."

# Recipe properties
has_recipe_name = DataFactory("has_recipe_name", domain=[Recipe], range=[str], BaseClass=has_name)
has_recipe_name.comment = "A description of the name/title of the recipe."

has_instructions = DataFactory("has_instructions", domain=[Recipe], range=[str])
has_instructions.comment = "A description of the instructions one has to follow according to the recipe in form of a text."

has_ingredient = RelationFactory("has_ingredient", domain=[Recipe], range=[IngredientWithAmount])
has_ingredient.comment = "A link from the recipe to one of the ingredients including their amount required for it."

authored_by = RelationFactory("authored_by", domain=[Recipe], range=[Author])
authored_by.comment = "A link from the recipe to its author."

requires_time = RelationFactory("requires_time", domain=[Recipe], range=[Time])
requires_time.comment = "A link from the recipe to the time required in order to create the in the recipe specified meal."

is_meal_type = RelationFactory("is_meal_type", domain=[Recipe], range=[MealType])
is_meal_type.comment = "A link from the recipe to the meal type of which meals can be grouped into."

has_difficulty = RelationFactory("has_difficulty", domain=[Recipe], range=[Difficulty])
has_difficulty.comment = "A link from the recipes to its difficulty."

is_vegan = DataFactory("is_vegan", domain=[Recipe], range=[bool])
is_vegan.comment = "A description of whether the recipe is vegan or not."

is_vegetarian = DataFactory("is_vegetarian", domain=[Recipe], range=[bool])
is_vegetarian.comment = "A description of whether the recipe is vegetarian or not."

has_calories = RelationFactory("has_calories", domain=[Recipe], range=[Calories])
has_calories.comment = "A link from the recipe to the amount of calories a meal created according to it approximately has"

has_protein = RelationFactory("has_protein", domain=[Recipe], range=[Protein])
has_protein.comment = "A link from the recipe to the amount of protein a meal created according to it approximately has"

has_fat = RelationFactory("has_fat", domain=[Recipe], range=[Fat])
has_fat.comment = "A link from the recipe to the amount of fat a meal created according to it approximately has"

has_carbohydrates = RelationFactory("has_carbohydrates", domain=[Recipe], range=[Carbohydrates])
has_carbohydrates.comment = "A link from the recipe to the amount of carbohydrates a meal created according to it approximately has"

has_link = DataFactory("has_link", domain=[Recipe], range=[str])
has_link.comment = "A description of the URL the recipe was found on. Since URLs are not supported by owlready2 in form of a text."

has_image_link = DataFactory("has_image_link", domain=[Recipe], range=[str])
has_image_link.comment = "A description of the URL the image of the recipe can be found on. Since URLs are not supported by owlready2 in form of a text."

# Ingredient properties
has_ingredient_name = DataFactory("has_ingredient_name", domain=[Ingredient], range=[str], BaseClass=has_name)
has_ingredient_name.comment = "A description of the name of the ingredient."

is_ingredient_of = RelationFactory("is_ingredient_of", domain=[Ingredient], range=[IngredientWithAmount])
is_ingredient_of.comment = "A link from the ingredient to the ingredient with amount which is required for at least one recipe."

# IngredientWithAmount properties
has_ingredient_with_amount_name = DataFactory("has_ingredient_with_amount_name", domain=[IngredientWithAmount], range=[str], BaseClass=has_name)
has_ingredient_with_amount_name.comment = "A description of the name of the ingredient including its amount and unit."

used_for = RelationFactory("used_for", domain=[IngredientWithAmount], range=[Recipe])
used_for.comment = "A link from the ingredient with amount to the recipe which requires that specific amount of the ingredient."

type_of_ingredient = RelationFactory("type_of_ingredient", domain=[IngredientWithAmount], range=[Ingredient])
type_of_ingredient.comment = "A link from the ingredient with amount to the ingredient it has the amount of."

amount_of_ingredient = DataFactory("amount_of_ingredient", domain=[IngredientWithAmount], range=[float], BaseClass=has_amount)
amount_of_ingredient.comment = "A description of the numeric quantity the ingredient with amount has the ingredient as a floating point number."

unit_of_ingredient = DataFactory("unit_of_ingredient", domain=[IngredientWithAmount], range=[str])
unit_of_ingredient.comment = "A description of the unit the ingredient with amount has the ingredient as a text."

# Author properties
has_author_name = DataFactory("has_author_name", domain=[Author], range=[str], BaseClass=has_name)
has_author_name.comment = "A description of the name of the author."

authored = RelationFactory("authored", domain=[Author], range=[Recipe])
authored.comment = "A link from the author to the recipe the author authored."

is_author_of = RelationFactory("is_author_of", domain=[Author], range=[Source])
is_author_of.comment = "A link from the author in form of a user to the source/website he is part of."

# Source properties
has_source_name = DataFactory("has_source_name", domain=[Source], range=[str], BaseClass=has_name)
has_source_name.comment = "A description of the name of the source/website."

has_author = RelationFactory("has_author", domain=[Source], range=[Author])
has_author.comment = "A link from the source/website to the author in form of a user using this website."

is_website = DataFactory("is_website", domain=[Source], range=[str])
is_website.comment = "A description of the URL the source/website uses. Since URLs are not supported by owlready2 in form of a text."

# Time properties
time_required_by = RelationFactory("time_required_by", domain=[Time], range=[Recipe])
time_required_by.comment = "A link from the time to the recipe which requires the time to complete its meal."

amount_of_time = DataFactory("amount_of_time", domain=[Time], range=[int], BaseClass=has_amount)
amount_of_time.comment = "A description of the duration of the time in minutes as a number."

# MealType properties
meal_type_of = RelationFactory("meal_type_of", domain=[MealType], range=[Recipe])
meal_type_of.comment = "A link from the meal type to a recipe whose meal belongs to it."

has_meal_type_name = DataFactory("has_meal_type_name", domain=[MealType], range=[str], BaseClass=has_name)
has_meal_type_name.comment = "A description of the name of the meal type."

# Difficulty properties
difficulty_of = RelationFactory("difficulty_of", domain=[Difficulty], range=[Recipe])
difficulty_of.comment = "A link from the difficulty to a recipe having this difficulty."

has_numeric_difficulty = DataFactory("has_numeric_difficulty", domain=[Difficulty], range=[int])
has_numeric_difficulty.comment = "A description of the difficulty in form of an int from 1 to 3 according to the difficulties description."

# Nutrient properties
calories_of = RelationFactory("calories_of", domain=[Calories], range=[Recipe])
calories_of.comment = "A link from the calories to the recipe whose meal approximately has the amount of calories of."

amount_of_calories = DataFactory("amount_of_calories", domain=[Calories], range=[float], BaseClass=has_amount)
amount_of_calories.comment = "A description of the amount the calories has in kilocalorie as a floating point number."

protein_of = RelationFactory("protein_of", domain=[Protein], range=[Recipe])
protein_of.comment = "A link from the protein to the recipe whose meal approximately has the amount of protein of."

amount_of_protein = DataFactory("amount_of_protein", domain=[Protein], range=[float], BaseClass=has_amount)
amount_of_protein.comment = "A description of the amount the protein has in gram as a floating point number."

fat_of = RelationFactory("fat_of", domain=[Fat], range=[Recipe])
fat_of.comment = "A link from the fat to the recipe whose meal approximately has the amount of fat of."

amount_of_fat = DataFactory("amount_of_fat", domain=[Fat], range=[float], BaseClass=has_amount)
amount_of_fat.comment = "A description of the amount the fat has in gram as a floating point number."

carbohydrates_of = RelationFactory("carbohydrates_of", domain=[Carbohydrates], range=[Recipe])
carbohydrates_of.comment = "A link from the carbohydrates to the recipe whose meal approximately has the amount of carbohydrates of."

amount_of_carbohydrates = DataFactory("amount_of_carbohydrates", domain=[Carbohydrates], range=[float], BaseClass=has_amount)
amount_of_carbohydrates.comment = "A description of the amount the carbohydrates has in gram as a floating point number."

