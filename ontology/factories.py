"""
Factory functions for creating OWL classes, properties, and relationships.
"""

from owlready2 import Thing, ThingClass, ObjectProperty, DataProperty
from .setup import onto


def ThingFactory(name, BaseClass=Thing) -> type[Thing]:
    """
    Create a new OWL class (Thing).
    
    Args:
        name: Name of the class to create
        BaseClass: Base class to inherit from (default: Thing)
    
    Returns:
        New OWL class type
    """
    with onto:
        return type[Thing](name, (BaseClass,), {})


def RelationFactory(name, domain: list[ThingClass] = None, range=None) -> type[ObjectProperty]:
    """
    Create a new OWL object property (relation between Things).
    
    Args:
        name: Name of the property
        domain: List of classes this property can be applied to (default: [Thing])
        range: List of classes this property can point to (default: [Thing])
    
    Returns:
        New ObjectProperty type
    """
    if domain is None:
        domain = [Thing]
    if range is None:
        range = [Thing]
    with onto:
        return type[ObjectProperty](name, (ObjectProperty,), {
            "domain": domain,
            "range": range,
        })


def DataFactory(name, domain: list[ThingClass] = None, range=None, BaseClass=DataProperty) -> type[DataProperty]:
    """
    Create a new OWL data property (property with primitive values).
    
    Args:
        name: Name of the property
        domain: List of classes this property can be applied to (default: [Thing])
        range: List of data types this property can have (default: [str])
        BaseClass: Base data property class (default: DataProperty)
    
    Returns:
        New DataProperty type
    """
    if domain is None:
        domain = [Thing]
    if range is None:
        range = [str]
    with onto:
        return type[BaseClass](name, (BaseClass,), {
            "domain": domain,
            "range": range,
        })


def makeInverse(first: ObjectProperty, second: ObjectProperty) -> None:
    """
    Define two object properties as inverses of each other.
    
    Args:
        first: First object property
        second: Second object property (inverse of first)
    
    Raises:
        TypeError: If either property is None
    """
    if first is None or second is None:
        raise TypeError("There is no inverse of no element: first:", str(first), "second:", str(second))
    with onto:
        first.inverse_property = second
        second.inverse_property = first

