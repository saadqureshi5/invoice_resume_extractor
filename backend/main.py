from fastapi import FastAPI, UploadFile, File, HTTPException, status
from pydantic import BaseModel
from typing import Any, Dict
import io

from backend.extractor import extract_data

app = FastAPI(
    title="Automated Invoice & Resume Extractor API",
    description="API for extracting structured data from Invoices and Resumes using LLMs.",
    version="1.0.0"
)

ALLOWED_MIME_TYPES = ["application/pdf", "text/plain"]

class ExtractionResponse(BaseModel):
    data: Dict[str, Any]
    metadata: Dict[str, Any]

@app.post("/extract/invoice", response_model=ExtractionResponse, tags=["Extraction"])
async def extract_invoice(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Only PDF and Text files are allowed."
        )
    
    try:
        content = await file.read()
        extracted_data, metadata = extract_data(
            file_content=content,
            schema_type="invoice",
            mime_type=file.content_type
        )
        return ExtractionResponse(
            data=extracted_data.model_dump(),
            metadata=metadata
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}"
        )

@app.post("/extract/resume", response_model=ExtractionResponse, tags=["Extraction"])
async def extract_resume(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Only PDF and Text files are allowed."
        )
    
    try:
        content = await file.read()
        extracted_data, metadata = extract_data(
            file_content=content,
            schema_type="resume",
            mime_type=file.content_type
        )
        return ExtractionResponse(
            data=extracted_data.model_dump(),
            metadata=metadata
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}"
        )

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API is running."}
