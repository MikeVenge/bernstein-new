#!/usr/bin/env python3
"""
CORS Fixed Backend Server

FastAPI backend with proper CORS configuration for local file access.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import uuid
import tempfile
import os
from pathlib import Path

app = FastAPI(title="Quarterly Earning Field Mapper API - CORS Fixed")

# Enable CORS for all origins (including file:// protocol)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins including file://
    allow_credentials=False,  # Set to False for file:// access
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Create temp directories
UPLOAD_DIR = Path("temp_uploads")
RESULTS_DIR = Path("temp_results")
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Simple job storage
jobs = {}

@app.get("/")
async def root():
    """Health check endpoint with CORS headers."""
    return {
        "message": "Quarterly Earning Field Mapper API is running with CORS enabled",
        "status": "ok",
        "cors_enabled": True
    }

@app.options("/api/upload-files")
async def upload_files_options():
    """Handle preflight requests."""
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.post("/api/upload-files")
async def upload_files(
    source_file: UploadFile = File(...),
    destination_file: UploadFile = File(...),
    mapping_file: UploadFile = File(...)
):
    """Upload files with CORS support."""
    
    try:
        job_id = str(uuid.uuid4())[:8]  # Short job ID for testing
        
        # Create job directory
        job_dir = UPLOAD_DIR / job_id
        job_dir.mkdir(exist_ok=True)
        
        # Save files
        files_info = {}
        for file_obj, file_type in [
            (source_file, "source"),
            (destination_file, "destination"),
            (mapping_file, "mapping")
        ]:
            file_path = job_dir / file_obj.filename
            content = await file_obj.read()
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            files_info[file_type] = {
                "filename": file_obj.filename,
                "path": str(file_path),
                "size": len(content)
            }
        
        # Store job info
        jobs[job_id] = {
            "status": "files_uploaded",
            "files": files_info,
            "created_at": "now"
        }
        
        response = JSONResponse(content={
            "status": "success",
            "job_id": job_id,
            "message": "Files uploaded successfully",
            "files": files_info
        })
        
        # Add CORS headers explicitly
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.options("/api/execute-mapping/{job_id}")
async def execute_mapping_options(job_id: str):
    """Handle preflight requests for execution."""
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.post("/api/execute-mapping/{job_id}")
async def execute_mapping(
    job_id: str,
    target_column: int = Form(...),
    data_column: str = Form("CO")
):
    """Execute mapping with CORS support."""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        # For testing, return simulated results
        # In production, this would run the actual field mapper
        
        result = {
            "mappings_processed": 134,
            "values_populated": 130,
            "success_rate": 97.0,
            "output_file": f"populated_{jobs[job_id]['files']['destination']['filename']}",
            "audit_file": f"audit_trail_{job_id}.csv",
            "sheet_stats": {
                "Key Metrics": 37,
                "Balance Sheet": 39,
                "Income Statement": 24,
                "Cash Flows": 30
            },
            "errors": ["Row 24: No source data available", "Row 25: No source data available"]
        }
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
        
        response = JSONResponse(content={
            "status": "success",
            "job_id": job_id,
            "result": result
        })
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")

@app.get("/api/download-result/{job_id}/{file_type}")
async def download_result(job_id: str, file_type: str):
    """Download endpoint with CORS support."""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # For testing, return download info
    response = JSONResponse(content={
        "message": f"Download {file_type} for job {job_id}",
        "filename": jobs[job_id]["result"]["output_file"] if file_type == "excel" else jobs[job_id]["result"]["audit_file"],
        "note": "This is test mode - in production this would download the actual file"
    })
    
    # Add CORS headers
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

if __name__ == "__main__":
    print("🚀 Starting Quarterly Earning Field Mapper Backend...")
    print("🌐 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("✅ CORS enabled for all origins (including file://)")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=False,
        access_log=True
    )
