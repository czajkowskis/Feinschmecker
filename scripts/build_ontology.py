#!/usr/bin/env python3
"""
Build the Feinschmecker recipe ontology from JSON data.

This script replaces the Jupyter notebook workflow for building the ontology.
It loads recipe data from JSON and saves the complete ontology to an RDF file.

Usage:
    python build_ontology.py [--recipes RECIPES_JSON] [--output OUTPUT_RDF]
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path to import ontology package
sys.path.insert(0, str(Path(__file__).parent.parent))

from ontology import onto, load_recipes_from_json
from owlready2 import default_world


def main():
    parser = argparse.ArgumentParser(description='Build Feinschmecker ontology from recipe data')
    parser.add_argument(
        '--recipes',
        default='../data/recipes.json',
        help='Path to recipes JSON file (default: ../data/recipes.json)'
    )
    parser.add_argument(
        '--output',
        default='../data/feinschmecker.rdf',
        help='Output RDF file path (default: ../data/feinschmecker.rdf)'
    )
    parser.add_argument(
        '--check-consistency',
        action='store_true',
        help='Check for inconsistent classes'
    )
    
    args = parser.parse_args()
    
    # Resolve paths relative to script location
    script_dir = Path(__file__).parent
    recipes_path = (script_dir / args.recipes).resolve()
    output_path = (script_dir / args.output).resolve()
    
    print(f"Building Feinschmecker ontology...")
    print(f"Reading recipes from: {recipes_path}")
    
    # Check if recipes file exists
    if not recipes_path.exists():
        print(f"Error: Recipe file not found: {recipes_path}")
        sys.exit(1)
    
    # Load recipes from JSON
    try:
        num_recipes = load_recipes_from_json(str(recipes_path))
        print(f"Successfully loaded {num_recipes} recipes")
    except Exception as e:
        print(f"Error loading recipes: {e}")
        sys.exit(1)
    
    # Count total individuals
    total_individuals = len(list(onto.individuals()))
    print(f"Total individuals in ontology: {total_individuals}")
    
    # Check consistency if requested
    if args.check_consistency:
        print("Checking for inconsistent classes...")
        inconsistent = list(default_world.inconsistent_classes())
        if inconsistent:
            print(f"Warning: Found {len(inconsistent)} inconsistent classes:")
            for cls in inconsistent:
                print(f"  - {cls}")
        else:
            print("No inconsistent classes found.")
    
    # Save ontology
    print(f"Saving ontology to: {output_path}")
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        onto.save(str(output_path))
        print("Ontology saved successfully!")
    except Exception as e:
        print(f"Error saving ontology: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

