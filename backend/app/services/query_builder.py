"""
SPARQL query builder for recipe filtering.

This module constructs SPARQL queries dynamically based on filter parameters,
supporting nutritional values, dietary restrictions, ingredients, and more.
"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class RecipeQueryBuilder:
    """Builder class for constructing SPARQL queries for recipe filtering."""
    
    def __init__(self):
        """Initialize the query builder."""
        self.header = ""
        self.body = ""
        self.filters = {}
    
    def build_query(self, filters: Dict[str, Any], limit: Optional[int] = None, offset: Optional[int] = None) -> str:
        """
        Build a complete SPARQL query from filter parameters.
        
        Args:
            filters: Dictionary of filter parameters
            limit: Maximum number of results to return
            offset: Number of results to skip (for pagination)
        
        Returns:
            Complete SPARQL query string
        """
        self.filters = filters
        self._build_header()
        self._build_body()
        
        query = self.header + " " + self.body
        
        # Add LIMIT and OFFSET for pagination
        if limit is not None:
            query += f" LIMIT {limit}"
        if offset is not None:
            query += f" OFFSET {offset}"
        
        logger.debug(f"Built SPARQL query: {query}")
        return query
    
    def _build_header(self):
        """Build the SELECT clause of the query."""
        self.header = (
            "SELECT ?name ?link ?image_link ?instructions "
            "(GROUP_CONCAT(?ing_name ; separator = \"#\" ) AS ?ingredients) "
            "?vegan ?vegetarian ?type_name ?time_amount ?difficulty_amount "
        )
    
    def _build_body(self):
        """Build the WHERE clause and filters of the query."""
        self.body = "{?res rdf:type feinschmecker:Recipe . \n"
        
        # Add ingredient filters
        if "ingredients" in self.filters:
            self._add_ingredient_filters(self.filters["ingredients"])
        
        # Add vegan/vegetarian filters
        self._add_dietary_filters()
        
        # Add meal type filter
        self._add_meal_type_filter()
        
        # Add time and difficulty filters
        self._add_time_difficulty_filters()
        
        # Add nutrient filters
        self._add_nutrient_filters()
        
        # Add required fields
        self._add_required_fields()
        
        self.body += "}"
        self.body += self._build_group_by()
    
    def _add_ingredient_filters(self, ingredients: list):
        """
        Add ingredient filtering to the query.
        
        Args:
            ingredients: List of ingredient names to filter by
        """
        appendum = "a"
        for i, ingredient in enumerate(ingredients):
            self.body += f"?res feinschmecker:has_ingredient ?ext_ing{appendum} . \n"
            self.body += f"?ext_ing{appendum} feinschmecker:type_of_ingredient ?ing{appendum} . \n"
            self.body += f"?ing{appendum} feinschmecker:has_ingredient_name ?ing_name{appendum} . \n"
            self.body += f"FILTER regex(?ing_name{appendum}, \"{ingredient}\", \"i\") . \n"
            appendum += "a"
    
    def _add_dietary_filters(self):
        """Add vegan and vegetarian filtering to the query."""
        if "vegan" in self.filters:
            vegan_value = "true" if self.filters["vegan"] else "false"
            self.body += f"?res feinschmecker:is_vegan {vegan_value} . \n"
        self.body += "?res feinschmecker:is_vegan ?vegan . \n"
        
        if "vegetarian" in self.filters:
            vegetarian_value = "true" if self.filters["vegetarian"] else "false"
            self.body += f"?res feinschmecker:is_vegetarian {vegetarian_value} . \n"
        self.body += "?res feinschmecker:is_vegetarian ?vegetarian . \n"
    
    def _add_meal_type_filter(self):
        """Add meal type filtering to the query."""
        if "meal_type" in self.filters:
            self.body += "?res feinschmecker:is_meal_type ?type . \n"
            self.body += f"?type feinschmecker:has_meal_type_name \"{self.filters['meal_type']}\" . \n"
            self.body += "?type feinschmecker:has_meal_type_name ?type_name . \n"
        else:
            self.body += "OPTIONAL {?res feinschmecker:is_meal_type ?type . \n"
            self.body += "   ?type feinschmecker:has_meal_type_name ?type_name}. \n"
    
    def _add_time_difficulty_filters(self):
        """Add time and difficulty filtering to the query."""
        # Time filter
        self.body += "?res feinschmecker:requires_time ?time . \n"
        self.body += "?time feinschmecker:amount_of_time ?time_amount . \n"
        if "time" in self.filters:
            self.body += f"FILTER (?time_amount < {self.filters['time']}) . \n"
        
        # Difficulty filter
        self.body += "?res feinschmecker:has_difficulty ?difficulty . \n"
        self.body += "?difficulty feinschmecker:has_numeric_difficulty ?difficulty_amount . \n"
        if "difficulty" in self.filters:
            self.body += f"FILTER (?difficulty_amount = {self.filters['difficulty']}) . \n"
    
    def _add_nutrient_filters(self):
        """Add nutrient filtering to the query."""
        nutrients = ['calories', 'protein', 'fat', 'carbohydrates']
        
        for nutrient in nutrients:
            self._add_nutrient_filter(nutrient)
    
    def _add_nutrient_filter(self, nutrient: str):
        """
        Add a single nutrient filter to the query.
        
        Args:
            nutrient: Name of the nutrient (e.g., 'calories', 'protein')
        """
        self.header += f"?{nutrient}_amount "
        self.body += f"?res feinschmecker:has_{nutrient} ?{nutrient} . \n"
        self.body += f"?{nutrient} feinschmecker:amount_of_{nutrient} ?{nutrient}_amount . \n"
        
        # Support both old naming (bigger/smaller) and new naming (min/max)
        bigger_key = f"{nutrient}_bigger"
        min_key = f"{nutrient}_min"
        smaller_key = f"{nutrient}_smaller"
        max_key = f"{nutrient}_max"
        
        # Min/bigger filter
        if bigger_key in self.filters:
            self.body += f"FILTER (?{nutrient}_amount > {self.filters[bigger_key]}) . \n"
        elif min_key in self.filters:
            self.body += f"FILTER (?{nutrient}_amount > {self.filters[min_key]}) . \n"
        
        # Max/smaller filter
        if smaller_key in self.filters:
            self.body += f"FILTER (?{nutrient}_amount < {self.filters[smaller_key]}) . \n"
        elif max_key in self.filters:
            self.body += f"FILTER (?{nutrient}_amount < {self.filters[max_key]}) . \n"
    
    def _add_required_fields(self):
        """Add required recipe fields to the query."""
        self.body += "?res feinschmecker:has_link ?link . \n"
        self.body += "?res feinschmecker:has_image_link ?image_link . \n"
        self.body += "?res feinschmecker:has_recipe_name ?name . \n"
        self.body += "?res feinschmecker:has_instructions ?instructions . \n"
        self.body += "?res feinschmecker:has_ingredient ?ing . \n"
        self.body += "?ing feinschmecker:has_ingredient_with_amount_name ?ing_name . \n"
        
        # Author and source information
        self.header += " ?author_name ?source_name ?source_link"
        self.body += "?res feinschmecker:authored_by ?author . \n"
        self.body += "?author feinschmecker:has_author_name ?author_name . \n"
        self.body += "?author feinschmecker:is_author_of ?source . \n"
        self.body += "?source feinschmecker:has_source_name ?source_name . \n"
        self.body += "?source feinschmecker:is_website ?source_link . \n"
    
    def _build_group_by(self) -> str:
        """Build the GROUP BY clause."""
        return (
            "GROUP BY ?name ?link ?image_link ?instructions ?vegan ?vegetarian "
            "?type_name ?time_amount ?difficulty_amount ?calories_amount "
            "?protein_amount ?fat_amount ?carbohydrates_amount "
            "?author_name ?source_name ?source_link"
        )


def build_count_query(filters: Dict[str, Any]) -> str:
    """
    Build a SPARQL query to count total matching recipes (for pagination).
    
    Args:
        filters: Dictionary of filter parameters
    
    Returns:
        SPARQL COUNT query string
    """
    # Build a query similar to the main query but only count results
    builder = RecipeQueryBuilder()
    builder.filters = filters
    
    # Use COUNT with DISTINCT
    count_header = "SELECT (COUNT(DISTINCT ?res) AS ?count) "
    
    # Build body without grouping
    builder._build_body()
    
    # Remove the GROUP BY clause from the body
    body = builder.body.split("GROUP BY")[0]
    
    query = count_header + body
    logger.debug(f"Built count query: {query}")
    return query

