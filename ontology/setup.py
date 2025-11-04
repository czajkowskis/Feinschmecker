"""
Ontology initialization and namespace setup for the Feinschmecker recipe ontology.

This module supports multiple knowledge graphs:
- schema_onto: Contains the TBox (classes, properties, constraints)
- Multiple KG ontologies: Each contains ABox (individuals/instances) and imports the schema
- create_kg(): Factory function to create new knowledge graphs for different sources
"""

from owlready2 import get_ontology

# Namespace base
NAMESPACE = "https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker"

# Schema ontology (TBox) - classes, properties, constraints
schema_onto = get_ontology(NAMESPACE + "/schema/")
schema_onto.destroy(update_relation=True, update_is_a=True)
schema_onto = get_ontology(NAMESPACE + "/schema/")

# Add schema metadata
schema_onto.metadata.comment.append("Schema (TBox) for the Feinschmecker recipe ontology.")
schema_onto.metadata.comment.append("This ontology defines classes, properties, and constraints for recipe knowledge representation.")
schema_onto.metadata.comment.append("This ontology was made by Jaron Sprute, Bhuvenesh Verma and Szymon Czajkowski.")
schema_onto.metadata.versionInfo.append("Version: 2.0 - Schema separated from knowledge graph")

# Registry of knowledge graphs
knowledge_graphs = {}


def create_kg(source_name: str = "default", destroy_existing: bool = False):
    """
    Create a new knowledge graph ontology for a specific data source.
    
    All knowledge graphs import the schema ontology, allowing multiple
    independent datasets to share the same class/property definitions.
    
    Args:
        source_name: Identifier for this knowledge graph (e.g., "bbc", "allrecipes")
        destroy_existing: If True, destroy and recreate if KG already exists
    
    Returns:
        Knowledge graph ontology that imports schema_onto
    
    Example:
        kg_bbc = create_kg("bbc")
        load_recipes_from_json('bbc_recipes.json', target_kg=kg_bbc)
        kg_bbc.save('kg-bbc.rdf')
    """
    if source_name in knowledge_graphs and not destroy_existing:
        return knowledge_graphs[source_name]
    
    # Create knowledge graph with source-specific namespace
    kg = get_ontology(NAMESPACE + f"/kg/{source_name}/")
    
    if destroy_existing:
        kg.destroy(update_relation=True, update_is_a=True)
        kg = get_ontology(NAMESPACE + f"/kg/{source_name}/")
    
    # Add metadata
    kg.metadata.comment.append(f"Knowledge graph (ABox) for {source_name} recipes.")
    kg.metadata.comment.append("This ontology contains recipe instances and data.")
    kg.metadata.comment.append("This ontology was made by Jaron Sprute, Bhuvenesh Verma and Szymon Czajkowski.")
    kg.metadata.versionInfo.append("Version: 2.0 - Multi-source knowledge graph support")
    
    # Establish import relationship: knowledge graph imports schema
    if schema_onto not in kg.imported_ontologies:
        kg.imported_ontologies.append(schema_onto)
    
    # Register in global registry
    knowledge_graphs[source_name] = kg
    
    return kg


# Default knowledge graph (backward compatibility)
kg_onto = create_kg("default", destroy_existing=True)

# Backward compatibility alias (deprecated)
onto = kg_onto

