# Scripts

The scripts directory contains utility scripts for data processing, ontology building, and querying.

## Purpose

This directory holds Python scripts and Jupyter notebooks used for data preparation, web scraping, ontology creation, and knowledge graph generation.

## Structure

- **`Feinschmecker.ipynb`** - Original Jupyter notebook for ontology creation (now deprecated in favor of modular Python files)
- **`build_ontology.py`** - Command-line script to build the ontology from JSON data
- **`example_queries.py`** - Example script demonstrating ontology queries
- **`utils.py`** - Helper functions for data parsing and processing

## Key Files

### build_ontology.py

A command-line script that replaces the Jupyter notebook workflow for building the ontology.

**Usage:**
```bash
python build_ontology.py [--recipes RECIPES_JSON] [--output OUTPUT_RDF] [--check-consistency]
```

**Options:**
- `--recipes` - Path to recipes JSON file (default: `../data/recipes.json`)
- `--output` - Output RDF file path (default: `../data/feinschmecker.rdf`)
- `--check-consistency` - Check for inconsistent classes in the ontology

**Example:**
```bash
python build_ontology.py --recipes ../data/recipes.json --output ../data/feinschmecker.rdf --check-consistency
```

### example_queries.py

Demonstrates how to query the ontology using the refactored Python package.

**Usage:**
```bash
python example_queries.py
```

**Features:**
- Loads recipes from JSON
- Counts recipes by meal type
- Filters by nutritional content (calories, protein, fat)
- Finds quick recipes (by time)
- Displays detailed recipe information

### Feinschmecker.ipynb

The original Jupyter notebook for creating the OWL ontology. This has been refactored into modular Python files in the `ontology/` directory for better maintainability.

**Note:** This notebook is now deprecated. Use `build_ontology.py` instead for production use.

### utils.py

Collection of utility functions for data processing:

- `separate_nutrition()` - Parses nutrition information from text
- `get_time()` - Extracts cooking time from formatted text
- `parse_ingredients()` - Parses ingredient lists into structured data with amounts and units

Used by the scraper to process raw scraped data.

## Related Files

The `utils/scraper.py` file (in the parent utils directory) works with these scripts to:
1. Scrape recipe data from BBC Good Food website
2. Parse raw HTML into structured JSON format
3. Use functions from `utils.py` to process ingredients, nutrition, and time data

## Workflow

### Data Processing Workflow

1. **Scrape data** - Run scraper to collect recipe data from web sources
   ```bash
   python ../utils/scraper.py
   ```

2. **Build ontology** - Convert processed JSON data to RDF ontology
   ```bash
   python build_ontology.py --recipes ../data/recipes.json --output ../data/feinschmecker.rdf
   ```

3. **Query ontology** - Use example queries or create custom queries
   ```bash
   python example_queries.py
   ```

### Development Workflow

For working with the ontology programmatically:

```python
from ontology import onto, load_recipes_from_json, recipesWithMaxCalories

# Load recipes
load_recipes_from_json('../data/recipes.json')

# Query
low_cal = recipesWithMaxCalories(300)

# Save
onto.save('../data/feinschmecker.rdf')
```

## Migration from Jupyter Notebook

The ontology code has been refactored from the Jupyter notebook into the `ontology/` package:

| Notebook Cell | Refactored Module |
|---------------|-------------------|
| Cell 2: Namespace & setup | `ontology/setup.py` |
| Cell 4: Factory functions | `ontology/factories.py` |
| Cell 6: Class definitions | `ontology/classes.py` |
| Cell 8: Property definitions | `ontology/properties.py` |
| Cell 10: Constraints | `ontology/constraints.py` |
| Cell 12: Individual creation | `ontology/individuals.py` |
| Cell 20: Query functions | `ontology/queries.py` |

**Benefits of refactoring:**
- Better code organization and modularity
- Easier to test individual components
- Reusable in other projects or scripts
- Better IDE support and type hints
- Version control friendly (no large notebook diffs)

## Future Enhancements

Planned additions to this directory:
- Data validation scripts
- Batch processing scripts for large datasets
- Ontology migration/update scripts for schema changes
- Performance benchmarking tools
