# Project Overview

## General Information
Feinschmecker is designed as a companion for everybody interested in cooking their own meals. It provides tools to retrieve culinary recipes with specified properties (e.g., amount of macronutrients, amount of calories, presence of meat, etc.) based on individual needs. Due to its focus on meal nutrition values, it is especially suitable for people during their weight loss or strength training journey. The possibility of filtering recipes based on the list of available ingredients helps to prevent waste of food.

## Key Questions
Feinschmecker uses a knowledge graph created using OWL to answer the following key questions:
- What ingredients are required for a given recipe?
- Which recipes contain at least the specified amount of protein / fats / carbohydrates?
- Which recipes contain at most the specified amount of calories?
- Which recipes are vegetarian / vegan?
- Which recipes are good for breakfast / lunch / dinner 
- Which recipes can be made using the list of specified ingredients?
- Which recipes are easy / moderately hard / hard to make?
- Which recipes can be prepared within a specific amount of time?

# How to use the application?

## Option 1: Using Docker (Recommended)

The easiest way to run the application is using Docker Compose, which sets up all services including the backend, frontend, Redis, and Celery workers.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed

### Quick Start

1. **Build the local ontology file:**
   Before starting the services, you need to build the knowledge graph. This script fetches the base ontology, merges it with local data, and saves it as `data/feinschmecker.nt`.
   ```console
   python scripts/build_ontology.py
   ```
   This file is used by the application by default.

1. **Start all services:**
   ```console
   docker compose up
   ```

2. **Or run in detached mode (background):**
   ```console
   docker compose up -d
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - API Documentation: http://localhost:5000/apidocs/

### Services

The Docker setup includes:
- **Backend** - Flask API server (port 5000)
- **Frontend** - Vue.js development server (port 3000)
- **Redis** - Cache and message broker (port 6379)
- **Celery Worker** - Background task processing
- **Celery Beat** - Scheduled task scheduler

### Useful Commands

```console
# View logs
docker compose logs -f

# View logs for a specific service
docker compose logs -f backend
docker compose logs -f celery-worker

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# Rebuild containers after code changes
docker compose up --build

# Restart a specific service
docker compose restart backend
```

### Environment Variables

You can customize the configuration using environment variables. Create a `.env` file in the root directory:

```env
FLASK_ENV=development
REDIS_URL=redis://redis:6379/0
# ONTOLOGY_URL=https://example.com/your-custom-ontology.nt  # Optional: Defaults to the local data/feinschmecker.nt
CORS_ORIGINS=*
```

See `.env.example` for all available options.

## Option 2: Local Development

### Backend Setup

1. **Install dependencies:**
   ```console
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the backend server:**
   ```console
   python3 website.py
   ```
   
   Or using gunicorn:
   ```console
   gunicorn -c gunicorn.conf.py backend.website:app
   ```

### Frontend Setup

1. **Install dependencies:**
   ```console
   cd webui
   npm install
   ```

2. **Run the development server:**
   ```console
   npm run dev
   ```

3. **Or build for production:**
   ```console
   npm run build
   npm run preview
   ```

### Access the Application

Open a browser and go to the address specified in the terminal (typically http://localhost:3000 for the frontend).
