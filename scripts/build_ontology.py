#!/usr/bin/env python3
"""
Build the Feinschmecker recipe ontology from JSON data and a remote source.

This script merges recipe data from a local JSON file and a remote RDF source,
then saves the complete ontology to a local file in N-Triples (.nt) format.

Usage:
    python scripts/build_ontology.py [--recipes RECIPES_JSON] [--output OUTPUT_NT] [--url REMOTE_URL]
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path to import ontology package
sys.path.insert(0, str(Path(__file__).parent.parent))

from ontology import onto, load_recipes_from_json
from owlready2 import default_world, get_ontology, sync_reasoner_pellet


def main():
    parser = argparse.ArgumentParser(description='Build Feinschmecker ontology from recipe data')
    parser.add_argument(
        '--recipes',
        default='../data/recipes.json',
        help='Path to recipes JSON file (default: ../data/recipes.json)'
    )
    parser.add_argument(
        '--url',
        default='https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker/feinschmecker.rdf',
        help='URL of the remote ontology to merge'
    )
    parser.add_argument(
        '--output',
        default='../data/feinschmecker.nt',
        help='Output N-Triples file path (default: ../data/feinschmecker.nt)'
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

    # Load remote ontology
    if args.url:
        try:
            print(f"Loading remote ontology from: {args.url}")
            get_ontology(args.url).load()
            print("Successfully loaded remote ontology.")
        except Exception as e:
            print(f"Warning: Could not load remote ontology: {e}. Continuing with local data only.")
    
    # Check if recipes file exists
    print(f"Reading local recipes from: {recipes_path}")
    if not recipes_path.exists():
        print(f"Error: Recipe file not found: {recipes_path}")
        sys.exit(1)
    
    # Load recipes from JSON
    try:
        num_recipes = load_recipes_from_json(str(recipes_path))
        print(f"Successfully loaded and merged {num_recipes} recipes from JSON.")
    except Exception as e:
        print(f"Error loading recipes: {e}")
        sys.exit(1)
    
    # Count total individuals
    total_individuals = len(list(onto.individuals()))
    print(f"Total individuals in merged ontology: {total_individuals}")
    
    # Check consistency if requested
    if args.check_consistency:
        print("Checking for inconsistent classes...")
        try:
            with onto:
                sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            inconsistent = list(default_world.inconsistent_classes())
            if inconsistent:
                print(f"Warning: Found {len(inconsistent)} inconsistent classes:")
                for cls in inconsistent:
                    print(f"  - {cls}")
            else:
                print("No inconsistent classes found.")
        except Exception as e:
            print(f"Could not run consistency check. Make sure a reasoner like Pellet is installed. Error: {e}")
    
    # Save ontology
    print(f"Saving merged ontology to: {output_path}")
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Save in N-Triples format
        onto.save(str(output_path), format="nt")
        print("Ontology saved successfully in N-Triples (.nt) format!")
    except Exception as e:
        print(f"Error saving ontology: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
