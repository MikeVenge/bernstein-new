#!/usr/bin/env python3
"""
Simple Backend Server

A minimal FastAPI backend for testing the frontend connection.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Simple Field Mapper API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Simple Field Mapper API is running", "status": "ok"}

@app.post("/api/upload-files")
async def upload_files(
    source_file: UploadFile = File(...),
    destination_file: UploadFile = File(...),
    mapping_file: UploadFile = File(...)
):
    """Simple file upload endpoint for testing."""
    
    try:
        job_id = "test-job-123"
        
        return {
            "status": "success",
            "job_id": job_id,
            "message": "Files uploaded successfully (test mode)",
            "files": {
                "source": {"filename": source_file.filename, "size": 1024},
                "destination": {"filename": destination_file.filename, "size": 2048},
                "mapping": {"filename": mapping_file.filename, "size": 512}
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/execute-mapping/{job_id}")
async def execute_mapping(job_id: str, target_column: int = Form(...), data_column: str = Form("CO")):
    """Simple execution endpoint for testing."""
    
    return {
        "status": "success",
        "job_id": job_id,
        "result": {
            "mappings_processed": 134,
            "values_populated": 134,
            "success_rate": 100.0,
            "output_file": "test_populated_file.xlsx",
            "audit_file": "test_audit_trail.csv",
            "sheet_stats": {
                "Key Metrics": 37,
                "Balance Sheet": 39,
                "Income Statement": 24,
                "Cash Flows": 34
            },
            "errors": []
        }
    }

@app.get("/api/download-result/{job_id}/{file_type}")
async def download_result(job_id: str, file_type: str):
    """Simple download endpoint for testing."""
    
    return {
        "message": f"Download {file_type} for job {job_id} (test mode)",
        "note": "In production, this would return the actual file"
    }

if __name__ == "__main__":
    print("🚀 Starting Simple Backend Server...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API docs will be at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
