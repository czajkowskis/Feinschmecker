# WebUI

The webui directory contains the Vue 3 frontend application for Feinschmecker.

## Purpose

This directory provides the user interface for the Feinschmecker recipe recommendation system. Built with Vue 3 and Vite, it offers an interactive web interface for searching and browsing recipes based on various filters.

## Structure

- **`public/`** - Static assets served directly
  - `images/` - Image files including hero images, icons, and recipe thumbnails
- **`src/`** - Vue source code
  - `assets/` - Vue-specific assets (SVG files, CSS)
  - `components/` - Reusable Vue components
    - `AboutUs.vue` - About section component
    - `HeroHeader.vue` - Hero section with title and tagline
    - `MacronutrientsSummary.vue` - Nutritional summary display
    - `Navbar.vue` - Navigation bar component
    - `RecipeCard.vue` - Recipe card display component
    - `RecipesSection.vue` - Container for recipe listings
    - `SearchForm.vue` - Recipe search form with filters
    - `SearchSection.vue` - Search section layout
  - `router/` - Vue Router configuration
    - `index.js` - Route definitions (HomeView, RecipeView)
  - `views/` - Page-level components
    - `HomeView.vue` - Main landing page
    - `RecipeView.vue` - Individual recipe detail page
  - `App.vue` - Root Vue component with routing
  - `main.js` - Application entry point
  - `style.css` - Global styles
- **`services/`** - Frontend service layer
  - `axios.js` - HTTP client configuration for API calls
- **`index.html`** - HTML template
- **`vite.config.js`** - Vite build configuration
- **`package.json`** - Node.js dependencies and scripts

## Key Features

### User Interface
- Responsive design with modern UI/UX
- Recipe search with multiple filter options
- Detailed recipe view with ingredients and instructions
- Nutritional information display
- Visual recipe cards with images

### Components
- **SearchForm**: Allows users to filter recipes by:
  - Ingredients
  - Macronutrients (protein, fat, carbohydrates, calories)
  - Cooking time
  - Difficulty level
  - Dietary preferences (vegan, vegetarian)
  - Meal type (breakfast, lunch, dinner)
- **RecipeCard**: Displays recipe preview with key information
- **RecipeView**: Shows full recipe details including:
  - Complete ingredient list
  - Step-by-step instructions
  - Nutritional breakdown
  - Author and source information

## Technology Stack

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next-generation frontend build tool
- **Vue Router** - Official router for Vue.js
- **Axios** - HTTP client for API requests
- **VueUse Motion** - Animation library for Vue

## Development

### Install dependencies
```bash
npm install
```

### Run development server
```bash
npm run dev
```

### Build for production
```bash
npm run build
```

### Preview production build
```bash
npm run preview
```

## API Integration

The frontend communicates with the backend Flask API (running on `backend/website.py`) through RESTful endpoints:
- `GET /recipes` - Fetch filtered recipes with query parameters

## Future Enhancements

Planned improvements include:
- Advanced search with query builder UI
- User account system (favorites, meal planning)
- Recipe recommendations
- Enhanced filtering UI
- Loading states and error handling
- Progressive Web App (PWA) capabilities
- Responsive image optimization
