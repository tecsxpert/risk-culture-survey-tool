FROM python:3.11-slim

# Set working directory 
WORKDIR /app

# Install system dependencies 
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker layer caching) 
COPY requirements.txt .

# Install Python dependencies 
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download sentence-transformer model 
# Done at build time so container starts instantly
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='/app/models'); \
print('Model downloaded successfully')"

# Copy application code 
COPY . .

# Set environment variables 
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TRANSFORMERS_OFFLINE=1
ENV HF_DATASETS_OFFLINE=1
ENV SENTENCE_TRANSFORMERS_HOME=/app/models
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Create directories 
RUN mkdir -p /app/chroma_data /app/models /app/logs

# Expose port 
EXPOSE 5000

# Health check 
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start application 
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:app"]