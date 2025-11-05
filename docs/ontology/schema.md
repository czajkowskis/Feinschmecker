# Ontology Schema Reference

This document provides a complete reference of all classes, properties, and constraints in the Feinschmecker ontology (TBox).

**Important**: The schema is **shared across all knowledge graphs**. Classes, properties, and constraints defined in `schema_onto` apply to all knowledge graphs (`kg_onto` and custom KGs created via `create_kg()`).

The ontology defines the **schema** (structure), while individual recipes form **knowledge graphs** (data/ABox).

---

## Classes

### Core Classes

#### `Recipe`

**Description**: A list of steps needed to prepare a meal, along with time of preparation, nutritional information, and dietary properties.

**Properties**:
- Name, instructions, image, link
- Ingredients (with amounts)
- Author and source
- Preparation time
- Meal type and difficulty
- Dietary flags (vegan, vegetarian)
- Nutritional content (calories, macronutrients)

**Example**:
```python
from ontology import Recipe, createIndividual, create_kg

# Create in default KG
recipe, _ = createIndividual("breakfast_burrito", Recipe)
recipe.has_recipe_name.append("Breakfast Burrito")

# Create in specific KG (uses same Recipe class from schema)
kg_bbc = create_kg("bbc")
recipe2, _ = createIndividual("bbc_burrito", Recipe, target_kg=kg_bbc)
```

---

#### `Ingredient`

**Description**: The ingredient type or name used within a recipe (e.g., "tomato", "chicken").

**Properties**:
- Ingredient name
- Links to recipes using this ingredient

**Note**: This represents the base ingredient type, not specific quantities. For amounts, see `IngredientWithAmount`.

---

#### `IngredientWithAmount`

**Description**: A specific quantity of an ingredient required for a recipe. This intermediate class is necessary to store ingredient amounts for specific recipes.

**Properties**:
- Name (ingredient with amount description)
- Type of ingredient (link to base `Ingredient`)
- Amount (numeric value)
- Unit (e.g., "cup", "gram", "tablespoon")
- Recipe using this ingredient

**Why this class exists**: OWL doesn't support n-ary relationships directly. This class allows us to associate both an ingredient and its quantity with a recipe.

---

#### `Author`

**Description**: The name or username of the recipe creator on a website.

**Properties**:
- Author name
- Recipes authored
- Associated source/website

---

#### `Source`

**Description**: The website including URL where the recipe is found.

**Properties**:
- Source name
- Website URL
- Associated authors

---

#### `Time`

**Description**: The time required to finish meal preparation according to a recipe. Unit is minutes.

**Properties**:
- Duration in minutes
- Associated recipe

---

#### `MealType`

**Description**: Categories for meal classification: "Breakfast", "Lunch", or "Dinner". Not all recipes belong to these categories.

**Properties**:
- Meal type name
- Associated recipes

**Individuals**: The ontology includes three predefined meal type individuals:
- `breakfast` - Breakfast meals
- `lunch` - Lunch meals
- `dinner` - Dinner meals

---

#### `Difficulty`

**Description**: Recipe difficulty level differentiated as 1 (easy), 2 (moderate), or 3 (difficult), based on required time and number of ingredients.

**Properties**:
- Numeric difficulty (1-3)
- Associated recipes

**Difficulty Scale**:
- **1** - Easy: Simple recipes with few ingredients and short preparation time
- **2** - Moderate: Recipes requiring some skill or more ingredients
- **3** - Difficult: Complex recipes requiring advanced techniques or many steps

**Individuals**: The ontology includes three predefined difficulty individuals.

---

### Nutrient Classes

#### `Nutrients` (Base Class)

**Description**: Base class for nutrients found within a meal according to a recipe.

**Subclasses**: `Calories`, `Protein`, `Fat`, `Carbohydrates`

---

#### `Calories` (extends Nutrients)

**Description**: The calories in a meal. Unit is kilocalorie (kcal).

**Properties**:
- Amount of calories (float)
- Associated recipe

---

#### `Protein` (extends Nutrients)

**Description**: The protein content in a meal. Unit is gram.

**Properties**:
- Amount of protein (float)
- Associated recipe

---

#### `Fat` (extends Nutrients)

**Description**: The fat content in a meal. Unit is gram.

**Properties**:
- Amount of fat (float)
- Associated recipe

---

#### `Carbohydrates` (extends Nutrients)

**Description**: The carbohydrate content in a meal. Unit is gram.

**Properties**:
- Amount of carbohydrates (float)
- Associated recipe

---

## Properties

### Property Hierarchy

The ontology uses meta-properties to organize related properties:

- **`has_name`** - Base property for all name-related properties
  - `has_recipe_name`
  - `has_ingredient_name`
  - `has_ingredient_with_amount_name`
  - `has_author_name`
  - `has_source_name`
  - `has_meal_type_name`

- **`has_amount`** - Base property for all amount-related properties
  - `amount_of_ingredient`
  - `amount_of_time`
  - `amount_of_calories`
  - `amount_of_protein`
  - `amount_of_fat`
  - `amount_of_carbohydrates`

---

### Recipe Properties

#### Object Properties (Relationships)

**`has_ingredient`**
- **Domain**: Recipe
- **Range**: IngredientWithAmount
- **Inverse**: `used_for`
- **Cardinality**: 0..*
- **Description**: Links recipes to ingredients with their required amounts

**`authored_by`**
- **Domain**: Recipe
- **Range**: Author
- **Inverse**: `authored`
- **Cardinality**: 0..1
- **Description**: Links recipes to their authors

**`requires_time`**
- **Domain**: Recipe
- **Range**: Time
- **Inverse**: `time_required_by`
- **Cardinality**: 1
- **Description**: Links recipes to preparation time

**`is_meal_type`**
- **Domain**: Recipe
- **Range**: MealType
- **Inverse**: `meal_type_of`
- **Cardinality**: 0..*
- **Description**: Categorizes recipes by meal type (can be multiple)

**`has_difficulty`**
- **Domain**: Recipe
- **Range**: Difficulty
- **Inverse**: `difficulty_of`
- **Cardinality**: 1
- **Description**: Associates recipes with difficulty levels

**`has_calories`**
- **Domain**: Recipe
- **Range**: Calories
- **Inverse**: `calories_of`
- **Cardinality**: 1
- **Description**: Links recipes to calorie information

**`has_protein`**
- **Domain**: Recipe
- **Range**: Protein
- **Inverse**: `protein_of`
- **Cardinality**: 1
- **Description**: Links recipes to protein information

**`has_fat`**
- **Domain**: Recipe
- **Range**: Fat
- **Inverse**: `fat_of`
- **Cardinality**: 1
- **Description**: Links recipes to fat information

**`has_carbohydrates`**
- **Domain**: Recipe
- **Range**: Carbohydrates
- **Inverse**: `carbohydrates_of`
- **Cardinality**: 1
- **Description**: Links recipes to carbohydrate information

#### Data Properties (Attributes)

**`has_recipe_name`** (extends `has_name`)
- **Domain**: Recipe
- **Range**: string
- **Cardinality**: 1
- **Description**: The title/name of the recipe

**`has_instructions`**
- **Domain**: Recipe
- **Range**: string
- **Cardinality**: 1
- **Description**: Cooking instructions as text

**`is_vegan`**
- **Domain**: Recipe
- **Range**: boolean
- **Cardinality**: 1
- **Description**: Whether the recipe is vegan

**`is_vegetarian`**
- **Domain**: Recipe
- **Range**: boolean
- **Cardinality**: 1
- **Description**: Whether the recipe is vegetarian

**`has_link`**
- **Domain**: Recipe
- **Range**: string
- **Cardinality**: 0..1
- **Description**: URL where the recipe was found

**`has_image_link`**
- **Domain**: Recipe
- **Range**: string
- **Cardinality**: 0..1
- **Description**: URL of the recipe image

---

### Ingredient Properties

**`has_ingredient_name`** (extends `has_name`)
- **Domain**: Ingredient
- **Range**: string
- **Description**: The name of the ingredient

**`is_ingredient_of`**
- **Domain**: Ingredient
- **Range**: IngredientWithAmount
- **Inverse**: `type_of_ingredient`
- **Description**: Links base ingredients to their amount-specific instances

---

### IngredientWithAmount Properties

**`has_ingredient_with_amount_name`** (extends `has_name`)
- **Domain**: IngredientWithAmount
- **Range**: string
- **Description**: Name including amount and unit (e.g., "2 cups flour")

**`used_for`**
- **Domain**: IngredientWithAmount
- **Range**: Recipe
- **Inverse**: `has_ingredient`
- **Description**: Links ingredient amounts to recipes that require them

**`type_of_ingredient`**
- **Domain**: IngredientWithAmount
- **Range**: Ingredient
- **Inverse**: `is_ingredient_of`
- **Description**: Links to the base ingredient type

**`amount_of_ingredient`** (extends `has_amount`)
- **Domain**: IngredientWithAmount
- **Range**: float
- **Description**: Numeric quantity of the ingredient

**`unit_of_ingredient`**
- **Domain**: IngredientWithAmount
- **Range**: string
- **Description**: Unit of measurement (e.g., "cup", "gram", "tsp")

---

### Author Properties

**`has_author_name`** (extends `has_name`)
- **Domain**: Author
- **Range**: string
- **Description**: The name of the author

**`authored`**
- **Domain**: Author
- **Range**: Recipe
- **Inverse**: `authored_by`
- **Description**: Links authors to recipes they created

**`is_author_of`**
- **Domain**: Author
- **Range**: Source
- **Inverse**: `has_author`
- **Description**: Links authors to their websites/sources

---

### Source Properties

**`has_source_name`** (extends `has_name`)
- **Domain**: Source
- **Range**: string
- **Description**: The name of the source/website

**`has_author`**
- **Domain**: Source
- **Range**: Author
- **Inverse**: `is_author_of`
- **Description**: Links sources to their authors

**`is_website`**
- **Domain**: Source
- **Range**: string
- **Description**: The URL of the source website

---

### Time Properties

**`time_required_by`**
- **Domain**: Time
- **Range**: Recipe
- **Inverse**: `requires_time`
- **Description**: Links time to recipes that require it

**`amount_of_time`** (extends `has_amount`)
- **Domain**: Time
- **Range**: integer
- **Description**: Duration in minutes

---

### MealType Properties

**`meal_type_of`**
- **Domain**: MealType
- **Range**: Recipe
- **Inverse**: `is_meal_type`
- **Description**: Links meal types to recipes

**`has_meal_type_name`** (extends `has_name`)
- **Domain**: MealType
- **Range**: string
- **Description**: The name of the meal type (e.g., "Breakfast")

---

### Difficulty Properties

**`difficulty_of`**
- **Domain**: Difficulty
- **Range**: Recipe
- **Inverse**: `has_difficulty`
- **Description**: Links difficulty levels to recipes

**`has_numeric_difficulty`**
- **Domain**: Difficulty
- **Range**: integer
- **Description**: Difficulty as a number (1=easy, 2=moderate, 3=difficult)

---

### Nutrient Properties

**Calories Properties**:
- **`calories_of`** - Links calories to recipe
- **`amount_of_calories`** (extends `has_amount`) - Calorie amount (float)

**Protein Properties**:
- **`protein_of`** - Links protein to recipe
- **`amount_of_protein`** (extends `has_amount`) - Protein amount in grams (float)

**Fat Properties**:
- **`fat_of`** - Links fat to recipe
- **`amount_of_fat`** (extends `has_amount`) - Fat amount in grams (float)

**Carbohydrates Properties**:
- **`carbohydrates_of`** - Links carbohydrates to recipe
- **`amount_of_carbohydrates`** (extends `has_amount`) - Carbohydrate amount in grams (float)

---

## Constraints & Validation

**Note**: All constraints are defined in the schema and apply to **all knowledge graphs**. When you create individuals in any KG, they must conform to the constraints defined in `schema_onto`.

### Inverse Properties

The ontology defines 11 inverse property pairs for bidirectional relationships:

| Property | Inverse Property | Purpose |
|----------|------------------|---------|
| `has_ingredient` | `used_for` | Recipe ↔ Ingredient relationship |
| `authored_by` | `authored` | Recipe ↔ Author relationship |
| `requires_time` | `time_required_by` | Recipe ↔ Time relationship |
| `is_meal_type` | `meal_type_of` | Recipe ↔ MealType relationship |
| `has_difficulty` | `difficulty_of` | Recipe ↔ Difficulty relationship |
| `has_calories` | `calories_of` | Recipe ↔ Calories relationship |
| `has_protein` | `protein_of` | Recipe ↔ Protein relationship |
| `has_fat` | `fat_of` | Recipe ↔ Fat relationship |
| `has_carbohydrates` | `carbohydrates_of` | Recipe ↔ Carbohydrates relationship |
| `type_of_ingredient` | `is_ingredient_of` | IngredientWithAmount ↔ Ingredient |
| `is_author_of` | `has_author` | Author ↔ Source relationship |

**Usage**: When you set a property, the inverse is automatically updated:
```python
recipe.has_ingredient.append(ingredient_with_amount)
# Automatically sets: ingredient_with_amount.used_for contains recipe
```

---

### Cardinality Constraints

Cardinality constraints enforce required and optional properties on classes. These constraints apply to all individuals in any knowledge graph:

#### Recipe Constraints
- **Required** (exactly 1):
  - `has_recipe_name`
  - `has_instructions`
  - `has_difficulty`
  - `requires_time`
  - `has_calories`
  - `has_protein`
  - `has_fat`
  - `has_carbohydrates`
  - `is_vegan`
  - `is_vegetarian`

- **Optional** (0 or more):
  - `has_ingredient`
  - `is_meal_type`
  - `has_link`
  - `has_image_link`

- **Optional** (0 or 1):
  - `authored_by`

#### Nutrient Constraints
Each nutrient class (Calories, Protein, Fat, Carbohydrates) must have:
- **Exactly 1** amount value
- **Exactly 1** associated recipe (via inverse property)

#### Other Class Constraints
- **Time**: Must have exactly 1 `amount_of_time`
- **Difficulty**: Must have exactly 1 `has_numeric_difficulty`
- **MealType**: Must have exactly 1 `has_meal_type_name`
- **Author**: Must have exactly 1 `has_author_name`
- **Source**: Must have exactly 1 `has_source_name`

---

### Disjoint Classes

Disjoint class declarations prevent individuals from belonging to multiple incompatible classes simultaneously. These rules apply across all knowledge graphs:

- Recipe, Ingredient, Author, Source, Time, MealType, and Difficulty are all mutually disjoint
- Nutrient subclasses (Calories, Protein, Fat, Carbohydrates) are mutually disjoint

This ensures logical consistency - for example, a Recipe cannot also be an Ingredient, regardless of which KG it's in.

---

### Domain and Range Restrictions

All properties specify their domain (which classes can have this property) and range (what type of values the property can have). These restrictions are defined in the schema and apply to all knowledge graphs:

**Example**:
```python
# has_recipe_name can only be used on Recipe instances
# and can only have string values
# This applies to Recipe individuals in any KG
has_recipe_name = DataFactory("has_recipe_name", domain=[Recipe], range=[str])
```

This provides type safety and enables reasoning engines to infer relationships and detect inconsistencies across all knowledge graphs.

---

### Applying Constraints

Constraints are automatically applied when importing the ontology package. They are applied to the **schema** and therefore affect **all knowledge graphs**.

To apply them manually:

```python
from ontology import apply_all_constraints

# Applies to schema - affects all KGs
apply_all_constraints()
```

Or apply them individually:

```python
from ontology import (
    setup_inverse_properties,
    setup_cardinality_constraints,
    setup_disjointness
)

# All of these operate on the schema
setup_inverse_properties()
setup_cardinality_constraints()
setup_disjointness()
```

---

## Schema Visualization

### Recipe Structure

```
Recipe
├── has_recipe_name (string)
├── has_instructions (string)
├── has_link (string, optional)
├── has_image_link (string, optional)
├── is_vegan (boolean)
├── is_vegetarian (boolean)
├── has_ingredient → IngredientWithAmount (0..*)
├── authored_by → Author (0..1)
├── requires_time → Time (1)
├── is_meal_type → MealType (0..*)
├── has_difficulty → Difficulty (1)
├── has_calories → Calories (1)
├── has_protein → Protein (1)
├── has_fat → Fat (1)
└── has_carbohydrates → Carbohydrates (1)
```

### Ingredient Structure

```
Ingredient
├── has_ingredient_name (string)
└── is_ingredient_of → IngredientWithAmount (0..*)

IngredientWithAmount
├── has_ingredient_with_amount_name (string)
├── type_of_ingredient → Ingredient (1)
├── amount_of_ingredient (float)
├── unit_of_ingredient (string)
└── used_for → Recipe (1)
```

### Nutrient Structure

```
Nutrients (abstract)
├── Calories
│   ├── amount_of_calories (float)
│   └── calories_of → Recipe (1)
├── Protein
│   ├── amount_of_protein (float)
│   └── protein_of → Recipe (1)
├── Fat
│   ├── amount_of_fat (float)
│   └── fat_of → Recipe (1)
└── Carbohydrates
    ├── amount_of_carbohydrates (float)
    └── carbohydrates_of → Recipe (1)
```

---

[Back to Overview](README.md) | [Previous: Architecture](architecture.md) | [Next: Query API](queries.md)

