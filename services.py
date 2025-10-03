import json
import re
from typing import Dict, Any, List
from datetime import datetime
from arkmodel_client import ArkModelClient
from models import ExtractionResult, ClassificationResult, UnitKerja, Emotion, Entity
from unit_kerja_service import unit_kerja_service

class DataExtractionService:
    def __init__(self):
        self.arkmodel_client = ArkModelClient()
    
    async def extract_from_content(self, content: str, language: str = "id", from_field: str = None, type: str = None) -> ExtractionResult:
        """Ekstraksi data dari konten menggunakan ArkModel"""
        try:
            # Panggil ArkModel untuk ekstraksi
            response = await self.arkmodel_client.extract_data(content, language)
            
            # Parse response dari ArkModel
            ai_response = response.get("choices", [{}])[0].get("message", {}).get("content", "{}")
            
            # Parse JSON response dari AI
            try:
                extracted_data = json.loads(ai_response)
            except json.JSONDecodeError as e:
                raise Exception(f"Failed to parse ArkModel response as JSON: {str(e)}")
            
            # Validasi dan format data
            return ExtractionResult(
                topic=extracted_data.get("topic", []),
                sentiment=extracted_data.get("sentiment", "neutral"),
                sentiment_score=float(extracted_data.get("sentiment_score", 0.5)),
                emotions=self._parse_emotions(extracted_data.get("emotions", [])),
                entities=self._parse_entities(extracted_data.get("entities", [])),
                locations=extracted_data.get("locations", []),
                hashtags=extracted_data.get("hashtags", []),
                summary=extracted_data.get("summary", "")
            )
            
        except Exception as e:
            # Jika ArkModel gagal, raise error
            raise Exception(f"ArkModel extraction failed: {str(e)}")
    
    
    def _parse_emotions(self, emotions_data: List[Dict]) -> List[Emotion]:
        """Parse emotions data"""
        emotions = []
        for emotion_data in emotions_data:
            if isinstance(emotion_data, dict):
                emotions.append(Emotion(
                    emotion=emotion_data.get("emotion", "neutral"),
                    confidence=float(emotion_data.get("confidence", 0.5))
                ))
        return emotions
    
    def _parse_entities(self, entities_data: List[Dict]) -> List[Entity]:
        """Parse entities data"""
        entities = []
        for entity_data in entities_data:
            if isinstance(entity_data, dict):
                entities.append(Entity(
                    name=entity_data.get("name", ""),
                    type=entity_data.get("type", "unknown"),
                    confidence=float(entity_data.get("confidence", 0.5))
                ))
        return entities

class ContentClassificationService:
    def __init__(self):
        self.arkmodel_client = ArkModelClient()
    
    async def classify_content(self, content: str, language: str = "id", from_field: str = None, type: str = None) -> ClassificationResult:
        """Klasifikasi konten untuk menentukan unit kerja"""
        try:
            # Panggil ArkModel untuk klasifikasi
            response = await self.arkmodel_client.classify_content(content, language)
            
            # Parse response dari ArkModel
            ai_response = response.get("choices", [{}])[0].get("message", {}).get("content", "{}")
            
            try:
                classification_data = json.loads(ai_response)
            except json.JSONDecodeError as e:
                raise Exception(f"Failed to parse ArkModel classification response as JSON: {str(e)}")
            
            # Format hasil klasifikasi
            recommended_unit_data = classification_data.get("recommended_unit", {})
            recommended_unit = UnitKerja(
                name=recommended_unit_data.get("name", "BSrE"),
                email=recommended_unit_data.get("email", "aduanbsre@bssn.go.id"),
                description=recommended_unit_data.get("description", "BSrE merupakan layanan di BSSN yang mengurus tentang sertifikat elektronik dan tanda tangan digital"),
                confidence=float(recommended_unit_data.get("confidence", 0.5)),
                matched_keywords=recommended_unit_data.get("matched_keywords", [])
            )
            
            alternative_units = []
            for alt_data in classification_data.get("alternative_units", []):
                alternative_units.append(UnitKerja(
                    name=alt_data.get("name", ""),
                    email=alt_data.get("email", ""),
                    description=alt_data.get("description", ""),
                    confidence=float(alt_data.get("confidence", 0.0)),
                    matched_keywords=alt_data.get("matched_keywords", [])
                ))
            
            return ClassificationResult(
                recommended_unit=recommended_unit,
                alternative_units=alternative_units,
                classification_reason=classification_data.get("classification_reason", "Berdasarkan analisis konten")
            )
            
        except Exception as e:
            # Jika ArkModel gagal, raise error
            raise Exception(f"ArkModel classification failed: {str(e)}")
    
