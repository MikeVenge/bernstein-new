FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY parameterized_field_mapper.py .
COPY railway_config.py .

# Create necessary directories
RUN mkdir -p uploads results

# Expose port (Railway will override this with PORT env var)
EXPOSE 8000

# Start the FastAPI application (Railway will use PORT env var)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
