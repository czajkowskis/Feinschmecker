import json
import re

import requests
from bs4 import BeautifulSoup

from utils import separate_nutrition, get_time, parse_ingredients

BROWSER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}


DUMMY_IMAGE_URL = "https://images.immediate.co.uk/production/volatile/sites/30/2024/03/cropped-GF-new-teal-1-7004649-a80b70d.png?quality=90&webp=true&resize=265,65"


def scrape_single_recipe(url, meal_type: str):
    response = requests.get(url, headers=BROWSER)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract recipe details
    title = soup.select_one('.post-header__title').text.strip()
    image_url = soup.select_one('.post-header-image picture img')
    image_url = image_url['src'] if image_url else DUMMY_IMAGE_URL
    author = soup.select_one('.author-link').text.strip()
    cooking_time = soup.select('li.body-copy-small.list-item span time')
    ingredients = [li.text.strip() for li in soup.select('.ingredients-list__item')]
    instructions = [li.text.strip() for li in soup.select('.method-steps__list-item')]
    nutrition = [li.text.strip() for li in soup.select('.nutrition-list__item')]
    properties = soup.select('span.terms-icons-list__text')

    is_vegan = any("Vegan" in item.text for item in properties)
    is_vegetarian = any("Vegetarian" in item.text for item in properties)

    return {
        'title': title,
        'image': image_url,
        'source': url,
        'time': get_time(cooking_time),
        'ingredients': parse_ingredients(ingredients),
        'instructions': instructions,
        'nutrients': separate_nutrition(nutrition),
        'author': author,
        'vegan': is_vegan,
        'vegetarian': is_vegetarian,
        'meal type': meal_type
    }


def scrape_multi_recipes(mother_url, meal_type):
    response = requests.get(mother_url, headers=BROWSER)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("a", {"class": "link d-block", "href": re.compile("/recipes/*")})
    urls = map(lambda link: "https://www.bbcgoodfood.com" + link["href"], links)
    recipes = []
    for url in urls:
        recipes.append(scrape_single_recipe(url, meal_type))
    
    print(len(recipes))
    return recipes


meal_type_sites = {"Breakfast": "https://www.bbcgoodfood.com/recipes/collection/breakfast-recipes",
                   "Lunch": "https://www.bbcgoodfood.com/recipes/collection/quick-lunch-recipes",
                   "Dinner": "https://www.bbcgoodfood.com/recipes/collection/easy-dinner-recipes",
                   "misc": "https://www.bbcgoodfood.com/recipes/collection/family-meal-recipes"
                   }

# List to store all recipe data
all_recipes = []

# Loop over URLs and scrape each recipe
for meal_type in meal_type_sites:
    try:
        print(f"Scraping category: {meal_type_sites[meal_type]}")
        all_recipes += scrape_multi_recipes(meal_type_sites[meal_type], meal_type)
    except Exception as e:
        print(f"Failed to scrape {meal_type_sites[meal_type]}: {e}")

# Save all recipes to a single JSON file
output_file = 'recipes.json'
with open(output_file, 'w') as f:
    json.dump(all_recipes, f, indent=4)

print(f"All recipes saved to {output_file}")
