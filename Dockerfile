# Use Python 3.8 slim image for Hugging Face Spaces
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p reports data

# Expose port (Hugging Face Spaces uses port 7860)
EXPOSE 7860

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run application with gunicorn for Hugging Face Spaces (port 7860)
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--timeout", "300", "--max-requests", "100", "--preload", "app:app"]
