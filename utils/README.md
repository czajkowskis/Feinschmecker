# Utils

The utils directory contains shared utility functions used across the project.

## Purpose

This directory provides common utility functions for data processing, web scraping, and other shared operations that are used by multiple components of the Feinschmecker project.

## Structure

- **`scraper.py`** - Web scraping module for collecting recipe data

## Key Files

### scraper.py
Python script that scrapes recipe data from BBC Good Food website.

**Key Functions:**
- `scrape_single_recipe(url, meal_type)` - Scrapes a single recipe page
- `scrape_multi_recipes(mother_url, meal_type)` - Scrapes multiple recipes from a category page

**Features:**
- Extracts recipe details: title, image, author, cooking time, ingredients, instructions, nutrition
- Identifies dietary flags (vegan, vegetarian)
- Handles different meal types (Breakfast, Lunch, Dinner, misc)
- Uses BeautifulSoup for HTML parsing
- Saves collected recipes to JSON format

**Data Sources:**
- BBC Good Food recipe collections for breakfast, lunch, dinner, and family meals
- Parses structured recipe pages with consistent HTML structure

**Dependencies:**
- `requests` - HTTP library for fetching web pages
- `BeautifulSoup4` - HTML parsing library
- Custom utility functions from `scripts/utils.py`

## Usage

The scraper is typically run standalone to collect recipe data:
```python
python utils/scraper.py
```

Output is saved to `data/recipes.json` for further processing.

## Integration

This scraper works in conjunction with:
- **`scripts/Feinschmecker.ipynb`** - Converts scraped JSON to RDF knowledge graph
- **`scripts/utils.py`** - Provides parsing utilities for ingredients, nutrition, and time data
- **`data/recipes.json`** - Storage location for scraped data

## Future Enhancements

Potential additions to this directory:
- Additional scraper modules for other recipe sources
- Data cleaning and normalization utilities
- Common helper functions for file I/O
- Logging and error handling utilities
- Configuration management utilities
- Validation helper functions

