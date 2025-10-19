#!/usr/bin/env python3
"""
Quarterly Earning Field Mapper Backend API

FastAPI backend for the parameterized field mapping tool.
Railway deployment ready.

Author: AI Assistant
Date: October 2025
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import openpyxl
import pandas as pd
import csv
import os
import shutil
import uuid
from pathlib import Path
from typing import Dict, List, Optional
import tempfile
import zipfile
from datetime import datetime

# Railway-specific imports
try:
    from railway_config import get_cors_origins, get_app_config, get_upload_settings
    # Get configuration
    app_config = get_app_config()
    cors_origins = get_cors_origins()
    upload_settings = get_upload_settings()
except ImportError:
    # Fallback configuration for Railway
    app_config = {
        "title": "Quarterly Earning Field Mapper API",
        "version": "1.0.0",
        "description": "Parameterized Excel field mapping API for quarterly earnings data",
        "project_id": os.getenv("RAILWAY_PROJECT_ID", "a33c9b9d-889b-427d-aba8-6240ca22d770")
    }
    cors_origins = [
        "https://bernstein-eight.vercel.app",
        "https://bernstein-mike-adgoios-projects.vercel.app",
        "*"
    ]
    upload_settings = {"max_file_size": 50 * 1024 * 1024}

# Import field mapping logic with fallback
try:
    import sys
    sys.path.append('..')
    from parameterized_field_mapper import ParameterizedFieldMapper
except ImportError:
    # Create a minimal version for Railway
    class ParameterizedFieldMapper:
        def __init__(self, *args, **kwargs):
            self.stats = {'mappings_processed': 0, 'values_populated': 0, 'errors': []}
        
        def load_mapping_file(self):
            return []
        
        def validate_files(self):
            return True, []
        
        def populate_fields(self, mappings):
            return []
        
        def generate_audit_trail(self, results):
            pass

app = FastAPI(
    title=app_config["title"],
    version=app_config["version"],
    description=app_config.get("description", "Field mapping API")
)

# Enable CORS - Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Set to False when using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories for file storage
UPLOAD_DIR = Path("uploads")
RESULTS_DIR = Path("results")
MAPPINGS_DIR = Path("mappings")
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)
MAPPINGS_DIR.mkdir(exist_ok=True)

# Predefined mapping configurations
PREDEFINED_MAPPINGS = {
    "ipg_photonics": {
        "label": "IPG Photonics",
        "filename": "GENERIC_FIELD_MAPPINGS.csv",
        "description": "Standard field mapping for IPG Photonics quarterly earnings"
    }
}


class MappingJob:
    """Represents a field mapping job."""
    
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.status = "created"
        self.progress = 0
        self.result = None
        self.error = None
        self.files = {}
        self.parameters = {}
        self.created_at = datetime.now()


# Store active jobs
active_jobs: Dict[str, MappingJob] = {}


@app.get("/")
async def root():
    """API health check."""
    return {
        "message": f"{app_config['title']} is running on Railway",
        "version": app_config["version"],
        "railway_project_id": app_config["project_id"],
        "cors_origins": cors_origins,
        "status": "healthy",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for frontend."""
    return {
        "status": "ok",
        "message": "Quarterly Earning Field Mapper API is healthy",
        "timestamp": datetime.now().isoformat(),
        "railway_project": app_config["project_id"]
    }


@app.get("/api/available-mappings")
async def get_available_mappings():
    """Get list of available predefined mapping files."""
    mappings = []
    for key, config in PREDEFINED_MAPPINGS.items():
        mappings.append({
            "key": key,
            "label": config["label"],
            "description": config["description"]
        })
    return {
        "status": "ok",
        "mappings": mappings
    }


@app.post("/api/upload-files")
async def upload_files(
    source_file: UploadFile = File(...),
    destination_file: UploadFile = File(...),
    mapping_key: str = Form(...)
):
    """Upload source and destination files, use predefined mapping."""
    
    try:
        # Validate mapping key
        if mapping_key not in PREDEFINED_MAPPINGS:
            raise HTTPException(status_code=400, detail=f"Invalid mapping key: {mapping_key}")
        
        # Create new job
        job_id = str(uuid.uuid4())
        job = MappingJob(job_id)
        
        # Create job directory
        job_dir = UPLOAD_DIR / job_id
        job_dir.mkdir(exist_ok=True)
        
        # Save uploaded files
        files_saved = {}
        
        for file_obj, file_type in [
            (source_file, "source"),
            (destination_file, "destination")
        ]:
            if not file_obj.filename:
                raise HTTPException(status_code=400, detail=f"No {file_type} file provided")
            
            file_path = job_dir / file_obj.filename
            content = await file_obj.read()
            
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
            files_saved[file_type] = {
                "filename": file_obj.filename,
                "path": str(file_path),
                "size": len(content)
            }
        
        # Use predefined mapping file
        mapping_config = PREDEFINED_MAPPINGS[mapping_key]
        mapping_file_path = Path(__file__).parent / mapping_config["filename"]
        
        if not mapping_file_path.exists():
            raise HTTPException(status_code=500, detail=f"Mapping file not found: {mapping_config['filename']}")
        
        files_saved["mapping"] = {
            "filename": mapping_config["filename"],
            "path": str(mapping_file_path),
            "label": mapping_config["label"],
            "key": mapping_key
        }
        
        job.files = files_saved
        job.status = "files_uploaded"
        active_jobs[job_id] = job
        
        return {
            "job_id": job_id,
            "status": "success",
            "message": "Files uploaded successfully",
            "files": files_saved,
            "mapping": {
                "key": mapping_key,
                "label": mapping_config["label"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@app.post("/api/execute-mapping/{job_id}")
async def execute_mapping(
    job_id: str,
    target_column: int = Form(...),
    data_column: str = Form("CO")
):
    """Execute field mapping for uploaded files."""
    
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = active_jobs[job_id]
    
    try:
        job.status = "processing"
        job.progress = 10
        job.parameters = {
            "target_column": target_column,
            "data_column": data_column
        }
        
        # Create results directory for this job
        job_results_dir = RESULTS_DIR / job_id
        job_results_dir.mkdir(exist_ok=True)
        
        # Get file paths
        source_path = job.files['source']['path']
        destination_path = job.files['destination']['path']
        mapping_path = job.files['mapping']['path']
        
        # Set output paths
        output_filename = f"populated_{job.files['destination']['filename']}"
        output_path = job_results_dir / output_filename
        audit_filename = f"audit_trail_{job_id}.csv"
        audit_path = job_results_dir / audit_filename
        
        # Initialize field mapper
        mapper = ParameterizedFieldMapper(
            source_file=source_path,
            destination_file=destination_path,
            mapping_file=mapping_path,
            target_column=target_column,
            data_column=data_column,
            output_file=str(output_path),
            audit_file=str(audit_path)
        )
        
        job.progress = 30
        
        # Validate files
        is_valid, errors = mapper.validate_files()
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Validation failed: {', '.join(errors)}")
        
        # Load mappings
        mappings = mapper.load_mapping_file()
        job.progress = 50
        
        # Execute mapping
        results = mapper.populate_fields(mappings)
        job.progress = 80
        
        # Generate audit trail
        mapper.generate_audit_trail(results)
        job.progress = 100
        
        # Calculate success rate
        success_rate = (mapper.stats['values_populated'] / mapper.stats['mappings_processed'] * 100) if mapper.stats['mappings_processed'] > 0 else 0
        
        job.status = "completed"
        job.result = {
            "mappings_processed": mapper.stats['mappings_processed'],
            "values_populated": mapper.stats['values_populated'],
            "success_rate": round(success_rate, 1),
            "output_file": output_filename,
            "audit_file": audit_filename,
            "output_path": str(output_path),
            "audit_path": str(audit_path),
            "sheet_stats": mapper.stats.get('sheet_stats', {}),
            "errors": mapper.stats.get('errors', [])
        }
        
        return {
            "status": "success",
            "job_id": job_id,
            "result": job.result
        }
        
    except Exception as e:
        job.status = "error"
        job.error = str(e)
        raise HTTPException(status_code=500, detail=f"Mapping execution failed: {str(e)}")


@app.get("/api/job-status/{job_id}")
async def get_job_status(job_id: str):
    """Get status of a mapping job."""
    
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = active_jobs[job_id]
    
    return {
        "job_id": job_id,
        "status": job.status,
        "progress": job.progress,
        "result": job.result,
        "error": job.error,
        "created_at": job.created_at.isoformat(),
        "parameters": job.parameters
    }


@app.get("/api/download-result/{job_id}/{file_type}")
async def download_result(job_id: str, file_type: str):
    """Download result files."""
    
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = active_jobs[job_id]
    
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    # Determine file path based on type
    if file_type == "excel":
        file_path = job.result.get("output_path")
        filename = job.result.get("output_file")
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif file_type == "audit":
        file_path = job.result.get("audit_path")
        filename = job.result.get("audit_file")
        media_type = "text/csv"
    elif file_type == "all":
        # Create a zip file with both files
        import zipfile
        zip_path = RESULTS_DIR / job_id / f"results_{job_id}.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            if job.result.get("output_path"):
                zipf.write(job.result["output_path"], job.result["output_file"])
            if job.result.get("audit_path"):
                zipf.write(job.result["audit_path"], job.result["audit_file"])
        file_path = str(zip_path)
        filename = f"results_{job_id}.zip"
        media_type = "application/zip"
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if not file_path or not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting {app_config['title']} on Railway...")
    print(f"🌐 Port: {port}")
    print(f"📋 Project ID: {app_config['project_id']}")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)