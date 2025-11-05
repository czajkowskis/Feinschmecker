"""
OWL class definitions for the Feinschmecker recipe ontology.
"""

from .factories import ThingFactory

# Main classes
Recipe = ThingFactory("Recipe")
Recipe.comment = "A list of steps needed to prepare a meal, along with time of preparation, amount of calories, amounts of macroelements and information about it being vegetarian or vegan"

Ingredient = ThingFactory("Ingredient")
Ingredient.comment = "The ingredient type or name used within a recipe."

IngredientWithAmount = ThingFactory("IngredientWithAmount")
IngredientWithAmount.comment = "Technically required class in order to save the amount of a certain ingredient required for a certain recipe"

Author = ThingFactory("Author")
Author.comment = "The name (or username) of the author of the recipe written on a certain website."

Source = ThingFactory("Source")
Source.comment = "The website name including URL on which the recipe is found."

Time = ThingFactory("Time")
Time.comment = "The time required to finish the preparations of a meal according to a specific recipe. The unit is minutes."

MealType = ThingFactory("MealType")
MealType.comment = "The meal type meals can be categorized into. This includes \"Dinner\", \"Lunch\" and \"Breakfast\". Not every recipe can be categorized to belong to one of the categories."

Difficulty = ThingFactory("Difficulty")
Difficulty.comment = "A difficulty level a certain the preparation of a certain recipe is categorized as. It is differentiated between 1(easy), 2(moderate) and 3(difficult). This is a differentiated number depending on the required time and number of ingredients."

# Nutrient classes
Nutrients = ThingFactory("Nutrients")
Nutrients.comment = "The nutrients one can expect to find within the meal according to a certain recipe, divided into Proteins, Fats, Carbohydrates and optionally Calories."

Calories = ThingFactory("Calories", BaseClass=Nutrients)
Calories.comment = "The calories one can expect to find within the meal according to a certain recipe. The unit is kilocalorie."

Protein = ThingFactory("Protein", BaseClass=Nutrients)
Protein.comment = "The protein one can expect to find within the meal according to a certain recipe. The unit is gram."

Fat = ThingFactory("Fat", BaseClass=Nutrients)
Fat.comment = "The fat one can expect to find within the meal according to a certain recipe. The unit is gram."

Carbohydrates = ThingFactory("Carbohydrates", BaseClass=Nutrients)
Carbohydrates.comment = "The carbohydrates one can expect to find within the meal according to a certain recipe. The unit is gram."

