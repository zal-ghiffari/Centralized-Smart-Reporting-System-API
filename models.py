from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ExtractionRequest(BaseModel):
    content: str
    language: Optional[str] = "id"
    from_field: Optional[str] = None  # Field untuk mengetahui sumber aduan
    type: Optional[str] = None  # Field untuk mengetahui tipe aduan

class Entity(BaseModel):
    name: str
    type: str  # person, organization, company, location
    confidence: float

class Emotion(BaseModel):
    emotion: str
    confidence: float

class ExtractionResult(BaseModel):
    topic: List[str]
    sentiment: str
    sentiment_score: float
    emotions: List[Emotion]
    entities: List[Entity]
    locations: List[str]
    hashtags: List[str]
    summary: str

class ClassificationRequest(BaseModel):
    content: str
    language: Optional[str] = "id"
    from_field: Optional[str] = None  # Field untuk mengetahui sumber aduan
    type: Optional[str] = None  # Field untuk mengetahui tipe aduan

class UnitKerja(BaseModel):
    name: str
    email: str
    description: str
    confidence: float
    matched_keywords: List[str]

class ClassificationResult(BaseModel):
    recommended_unit: UnitKerja
    alternative_units: List[UnitKerja]
    classification_reason: str

class ProcessingRequest(BaseModel):
    content: str
    language: Optional[str] = "id"
    from_field: Optional[str] = None  # Field untuk mengetahui sumber aduan
    type: Optional[str] = None  # Field untuk mengetahui tipe aduan

class ProcessingResponse(BaseModel):
    extraction: ExtractionResult
    classification: ClassificationResult
    processing_time: float
    timestamp: datetime

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime
