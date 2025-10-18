#!/usr/bin/env python3
"""
Railway Configuration for Quarterly Earning Field Mapper Backend

Configuration settings for Railway deployment.
"""

import os
from pathlib import Path

# Railway Project Configuration
RAILWAY_PROJECT_ID = "a33c9b9d-889b-427d-aba8-6240ca22d770"

# Environment-based configuration
def get_cors_origins():
    """Get CORS origins based on environment."""
    if os.getenv("RAILWAY_ENVIRONMENT") == "production":
        return [
            "https://bernstein-mike-adgoios-projects.vercel.app",
            "https://quarterly-earning-field-mapper.vercel.app",
            "https://bernstein.vercel.app"
        ]
    else:
        return [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "*"  # Allow all for development
        ]

def get_upload_settings():
    """Get file upload settings."""
    return {
        "max_file_size": 50 * 1024 * 1024,  # 50MB
        "allowed_extensions": [".xlsx", ".xls", ".csv"],
        "upload_timeout": 300  # 5 minutes
    }

def get_app_config():
    """Get application configuration."""
    return {
        "title": "Quarterly Earning Field Mapper API",
        "version": "1.0.0",
        "description": "Parameterized Excel field mapping API for quarterly earnings data",
        "project_id": RAILWAY_PROJECT_ID
    }
