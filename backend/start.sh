#!/bin/bash
echo "🚀 Starting Quarterly Earning Field Mapper Backend on Railway..."
echo "Project ID: a33c9b9d-889b-427d-aba8-6240ca22d770"

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI application
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
