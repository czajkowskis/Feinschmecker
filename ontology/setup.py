"""
Ontology initialization and namespace setup for the Feinschmecker recipe ontology.
"""

from owlready2 import get_ontology

# Namespace and ontology initialization
NAMESPACE = "https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker"

# Destroy influence from last python runtime
onto = get_ontology(NAMESPACE + "/")
onto.destroy(update_relation=True, update_is_a=True)
onto = get_ontology(NAMESPACE + "/")

# Add metadata
onto.metadata.comment.append("This project is about recipes that are used for meal preparations found in the web.")
onto.metadata.comment.append("This ontology was made by Jaron Sprute, Bhuvenesh Verma and Szymon Czajkowski.")
onto.metadata.versionInfo.append("Version: 1.1 - Existing and working ontology with sparse individuals, initial feedback included")

