FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (maintain directory structure for imports)
COPY backend/ /app/backend/
COPY ontology/ /app/ontology/
COPY data/ /app/data/

# Expose port
EXPOSE 8000

# Set environment variables
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run gunicorn (config file is in backend directory)
CMD ["gunicorn", "-c", "backend/gunicorn.conf.py", "backend.website:app"]

