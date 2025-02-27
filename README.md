# Project Overview

## General Information
Feinschmecker is designed as a companion for everybody interested in cooking their own meals. It provides tools to retrieve culinary recipes with specified properties (e.g., amount of macronutrients, amount of calories, presence of meat, etc.) based on individual needs. Due to its focus on meal nutrition values, it is especially suitable for people during their weight loss or strength training journey. The possibility of filtering recipes based on the list of available ingredients helps to prevent waste of food.

## Key Questions
Feinschmecker uses a knowledge graph created using OWL to answer the following key questions:
- What ingredients are required for a given recipe?
- Which recipes contain at least the specified amount of protein / fats / carbohydrates?
- Which recipes contain at most the specified amount of calories?
- Which recipes are vegetarian / vegan?
- Which recipes are good for breakfast / lunch / dinner 
- Which recipes can be made using the list of specified ingredients?
- Which recipes are easy / moderately hard / hard to make?
- Which recipes can be prepared within a specific amount of time?

# How to use the application?
First install the necessery dependencies for the backend:
```console
pip install -r requirements.txt
```
Run the local backend server:
```console
python3 website.py
```

Install the necessery dependencies for the frontend:
```console
cd webui
npm install
```

Run local frontend server:
```console
npm run preview
```

Open a browser and go to the adress specified in the terminal.
