FROM python:3.11-slim

LABEL maintainer="Moroccan CS Education Platform"
LABEL description="Multi-agent intelligent tutoring system for Moroccan students"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements-docker.txt /app/backend/requirements-docker.txt

# Install Python dependencies (using Docker-optimized requirements)
RUN pip install --no-cache-dir -r backend/requirements-docker.txt

# Copy application code
COPY backend/ /app/backend/
COPY config/ /app/config/
COPY data/ /app/data/
COPY .env.example /app/.env

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8000

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["python", "-m", "backend.api.main"]
