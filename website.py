#!/usr/bin/python3.11

#############################################################################
##                                                                         ##
## Feinschmecker website                                                   ##
##                                                                         ##
## Feinschmecker, 2024-12-20                                               ##
##                                                                         ##
#############################################################################
# Imports

from owlready2 import *
from flask import Flask, jsonify, request
from flask_cors import CORS

# Flask app setup
app = Flask(__name__)
CORS(app)

#############################################################################
# Get recipes from filter

onto = get_ontology(
    "https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker/feinschmecker.rdf").load()


def addNutrientFilter(nutrient, filter, header, body):
    header += "?" + nutrient + "_amount "
    body += "?res feinschmecker:has_" + nutrient + " ?" + nutrient + " . \n"
    body += "?" + nutrient + " feinschmecker:amount_of_" + nutrient + " ?" + nutrient + "_amount . \n"
    if nutrient + "_bigger" in filter:
        body += "FILTER (?" + nutrient + "_amount > " + str(filter[nutrient + "_bigger"]) + ") . \n"
    if nutrient + "_smaller" in filter:
        body += "FILTER (?" + nutrient + "_amount < " + str(filter[nutrient + "_smaller"]) + ") . \n"
    return header, body


# Universal filter
def getRequest(filter):
    
    if "vegan" in filter and isinstance(filter["vegan"], str):
        filter["vegan"] = filter["vegan"].lower() == "true"
    if "vegetarian" in filter and isinstance(filter["vegetarian"], str):
        filter["vegetarian"] = filter["vegetarian"].lower() == "true"
    
    header = "SELECT ?name ?instructions ?vegan ?vegetarian ?type ?time_amount ?difficulty_amount "
    body = "{?res rdf:type feinschmecker:Recipe . \n"
    if "vegan" in filter:
        if filter["vegan"]:
            body += "?res feinschmecker:is_vegan true . \n"
        else:
            body += "?res feinschmecker:is_vegan false . \n"
    body += "?res feinschmecker:is_vegan ?vegan . \n"
    if "vegetarian" in filter:
        if filter["vegetarian"]:
            body += "?res feinschmecker:is_vegetarian true . \n"
        else:
            body += "?res feinschmecker:is_vegetarian false . \n"
    body += "?res feinschmecker:is_vegetarian ?vegetarian . \n"
    if "meal_type" in filter:
        body += "?res feinschmecker:is_meal_type \"" + filter["meal_type"] + "\" . \n"
    body += "OPTIONAL {?res feinschmecker:is_meal_type ?type}. \n"
    body += "?res feinschmecker:requires_time ?time . \n"
    body += "?time feinschmecker:amount_of_time ?time_amount . \n"
    if "time" in filter:
        body += "FILTER (?time_amount < " + str(filter["time"]) + ") . \n"
    body += "?res feinschmecker:has_difficulty ?difficulty . \n"
    body += "?difficulty feinschmecker:has_numeric_difficulty ?difficulty_amount . \n"
    if "difficulty" in filter:
        body += "FILTER (?difficulty_amount = " + str(filter["difficulty"]) + ") . \n"

    header, body = addNutrientFilter("calories", filter, header, body)
    header, body = addNutrientFilter("protein", filter, header, body)
    header, body = addNutrientFilter("fat", filter, header, body)
    header, body = addNutrientFilter("carbohydrates", filter, header, body)

    # Remaining elements for head
    body += "?res feinschmecker:has_recipe_name ?name . \n"
    body += "?res feinschmecker:has_instructions ?instructions . \n"

    body += """}"""

    recipe_list = list(default_world.sparql(header + body))
    order = ["name", "instructions", "vegan", "vegetarian", "meal_type", "time", "difficulty", "calories", "protein",
             "fat", "carbohydrates"]
    recipe_list_dict = []
    for r in recipe_list:
        tmp = {}
        for i in range(len(order)):
            tmp[order[i]] = r[i]
        tmp["instructions"] = tmp["instructions"].strip("[]\'").split("\', \'")
        for i, step in enumerate(tmp["instructions"]):
            tmp["instructions"][i] = step.lstrip("step ").lstrip("0123456789")
        recipe_list_dict.append(tmp)
    with onto:
        return recipe_list_dict

# API Routes
    
@app.route('/')
def index():
    return "Welcome to the Feinschmecker API!"
    
@app.route('/recipes', methods=['GET'])
def get_recipes():
    """API endpoint to retrieve recipes based on filters."""
    filters = request.args.to_dict()
    try:
        recipes = getRequest(filters)
    
        return jsonify(recipes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500    


#############################################################################
# Initial method


if __name__ == '__main__':
    app.run(debug=True)

#############################################################################


