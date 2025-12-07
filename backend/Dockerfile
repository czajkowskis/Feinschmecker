FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for Python packages
# - gcc: Required for compiling Python extensions
# - python3-dev: Python development headers for building extensions
# - libxml2-dev: Required for owlready2 XML parsing
# - libxslt1-dev: Required for owlready2 XSLT transformations
# - zlib1g-dev: Compression library
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to ensure latest version
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Verify critical packages are installed and can be imported
RUN python -c "import rdflib; print(f'✓ rdflib {rdflib.__version__} installed successfully')" && \
    python -c "import owlready2; print('✓ owlready2 installed successfully')" && \
    python -c "from rdflib import Graph; print('✓ rdflib.Graph import successful')"

# Copy application code (maintain directory structure for imports)
COPY backend/ /app/backend/
COPY ontology/ /app/ontology/
COPY data/ /app/data/

# Expose port
EXPOSE 5000

# Create a non-root user for running the application
# Using UID 1000 (common non-root user ID) for compatibility with volume mounts
RUN groupadd -r -g 1000 appuser && useradd -r -u 1000 -g appuser appuser

# Set ownership of app directory
RUN chown -R appuser:appuser /app

# Set environment variables
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Switch to non-root user
USER appuser

# Run gunicorn (config file is in backend directory)
CMD ["gunicorn", "-c", "backend/gunicorn.conf.py", "backend.website:app"]

