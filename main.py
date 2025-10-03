from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import time
from typing import Dict, Any

from models import (
    ProcessingRequest, 
    ProcessingResponse, 
    ExtractionRequest, 
    ClassificationRequest,
    ErrorResponse
)
from services import DataExtractionService, ContentClassificationService
from config import settings
from unit_kerja_service import unit_kerja_service

# Inisialisasi FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API untuk ekstraksi dan klasifikasi data aduan/laporan menggunakan ArkModel BytePlus"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi services
extraction_service = DataExtractionService()
classification_service = ContentClassificationService()

@app.get("/")
async def root():
    """Endpoint root untuk health check"""
    return {
        "message": "Smart Reporting API is running",
        "version": settings.app_version,
        "timestamp": datetime.now()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "extraction": "ready",
            "classification": "ready"
        }
    }

@app.post("/extract", response_model=Dict[str, Any])
async def extract_data(request: ExtractionRequest):
    """
    Endpoint untuk ekstraksi data dari konten aduan/laporan
    """
    try:
        start_time = time.time()
        
        # Ekstraksi data
        extraction_result = await extraction_service.extract_from_content(
            content=request.content,
            language=request.language,
            from_field=request.from_field,
            type=request.type
        )
        
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "data": extraction_result.dict(),
            "processing_time": processing_time,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during extraction: {str(e)}"
        )

@app.post("/classify", response_model=Dict[str, Any])
async def classify_content(request: ClassificationRequest):
    """
    Endpoint untuk klasifikasi konten berdasarkan hasil ekstraksi
    """
    try:
        start_time = time.time()
        
        # Klasifikasi konten
        classification_result = await classification_service.classify_content(
            content=request.content,
            language=request.language,
            from_field=request.from_field,
            type=request.type
        )
        
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "data": classification_result.dict(),
            "processing_time": processing_time,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during classification: {str(e)}"
        )

@app.post("/process", response_model=ProcessingResponse)
async def process_complaint(request: ProcessingRequest):
    """
    Endpoint utama untuk memproses aduan/laporan secara lengkap
    Melakukan ekstraksi dan klasifikasi dalam satu request
    """
    try:
        start_time = time.time()
        
        # Step 1: Ekstraksi data
        extraction_result = await extraction_service.extract_from_content(
            content=request.content,
            language=request.language,
            from_field=request.from_field,
            type=request.type
        )
        
        # Step 2: Klasifikasi konten
        classification_result = await classification_service.classify_content(
            content=request.content,
            language=request.language,
            from_field=request.from_field,
            type=request.type
        )
        
        processing_time = time.time() - start_time
        
        return ProcessingResponse(
            extraction=extraction_result,
            classification=classification_result,
            processing_time=processing_time,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during processing: {str(e)}"
        )

@app.get("/units")
async def get_available_units():
    """
    Endpoint untuk mendapatkan daftar unit kerja yang tersedia dari database
    """
    try:
        units = await unit_kerja_service.get_unit_kerja_list()
        
        return {
            "success": True,
            "data": units,
            "timestamp": datetime.now(),
            "source": "database"
        }
        
    except Exception as e:
        # Fallback to static data
        from config import FALLBACK_UNIT_KERJA_DATA
        
        units = []
        for name, data in FALLBACK_UNIT_KERJA_DATA.items():
            units.append({
                "name": name,
                "email": data["email"],
                "description": data["description"],
                "keywords": data["keywords"]
            })
        
        return {
            "success": True,
            "data": units,
            "timestamp": datetime.now(),
            "source": "fallback",
            "warning": f"Database unavailable, using fallback data: {str(e)}"
        }

@app.post("/units/refresh")
async def refresh_unit_kerja_cache():
    """
    Endpoint untuk refresh cache unit kerja dari database
    """
    try:
        await unit_kerja_service.refresh_cache()
        
        return {
            "success": True,
            "message": "Unit kerja cache refreshed successfully",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error refreshing cache: {str(e)}"
        )

@app.get("/database/status")
async def get_database_status():
    """
    Endpoint untuk mengecek status koneksi database
    """
    try:
        is_connected = await unit_kerja_service.test_connection()
        
        return {
            "success": True,
            "database_connected": is_connected,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        return {
            "success": False,
            "database_connected": False,
            "error": str(e),
            "timestamp": datetime.now()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug
    )
