def separate_nutrition(nutritions):
    nutrients = {}

    for item in nutritions:
        item = item.replace('low', '').replace('high', '').strip()

        nutrient, amount = "", ""

        for i, char in enumerate(item):
            if char.isdigit():
                nutrient = item[:i].strip()
                amount_with_unit = item[i:].strip()
                break

        if not nutrient or not amount_with_unit:
            continue

        amount = ""
        for char in amount_with_unit:
            if char.isdigit() or char == '.':
                amount += char
            else:
                break

        try:
            amount = float(amount)
        except ValueError:
            continue  # Skip if conversion fails

        nutrients[nutrient] = amount

    return nutrients


def get_time(cooking_time):
    total_minutes = 0
    
    for item in cooking_time[:2]:
        time_text = item.text.lower() 
        parts = time_text.split()

        minutes = 0
        for i, part in enumerate(parts):
            if "hr" in part:  
                minutes += int(parts[i - 1]) * 60
            elif "min" in part:  
                minutes += int(parts[i - 1])

        total_minutes += minutes

    return total_minutes


def parse_ingredients(ingredient_texts):
    parsed_ingredients = []

    for ingredient_text in ingredient_texts:
        # Initialize variables
        amount = ""
        unit = ""
        ingredient = ""

        for i, char in enumerate(ingredient_text):
            if char.isdigit() or char == '.':
                amount += char
            elif char.isalpha() or char.isspace():
                ingredient = ingredient_text[i:].strip()
                break

        words = ingredient.split()
        for i, word in enumerate(words):
            if word.isalpha() and word.lower() in ["g", "kg", "ml", "l", "tsp", "tbsp", "zest", "juice"]:
                unit = word
                ingredient = " ".join(words[i + 1:]).strip()
                break

        if not amount:
            amount = 1
        else:
            amount = float(amount) if '.' in amount else int(amount)

        parsed_ingredients.append({
            "id": ingredient_text,
            "ingredient": ingredient,
            "amount": amount,
            "unit": unit
        })

    return parsed_ingredients
