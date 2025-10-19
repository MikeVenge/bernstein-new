FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads results

# Expose port (Railway will override this with PORT env var)
EXPOSE 8000

# Start the FastAPI application (Railway will set PORT env var)
CMD python -c "import os; import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=int(os.getenv('PORT', 8000)))"