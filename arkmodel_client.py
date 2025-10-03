import httpx
import json
from typing import Dict, Any, List
from config import settings
from unit_kerja_service import unit_kerja_service

class ArkModelClient:
    def __init__(self):
        self.api_key = settings.arkmodel_api_key
        self.base_url = settings.arkmodel_base_url
        self.model_name = settings.arkmodel_model_name
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Membuat request ke ArkModel API"""
        # Pastikan tidak ada double slash
        if self.base_url.endswith('/'):
            url = f"{self.base_url}{endpoint}"
        else:
            url = f"{self.base_url}/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"HTTP error: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                raise Exception(f"Request error: {str(e)}")
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")
    
    async def extract_data(self, content: str, language: str = "id", from_field: str = None, type: str = None) -> Dict[str, Any]:
        """Ekstraksi data dari konten aduan"""
        prompt = f"""
        Sebagai AI agent untuk ekstraksi data aduan/laporan, analisis konten berikut dan ekstrak informasi berikut dalam format JSON:

        Konten: {content}

        Ekstrak informasi berikut:
        1. Topik utama aduan (bukan kalimat ringkasan, namun kata kunci/keyword dari inti aduan/laporan)
        2. Sentimen (positive, negative, neutral) dengan skor 0-1
        3. Emosi yang terdeteksi (anger, fear, joy, sadness, surprise, disgust, anticipation, trust) dengan skor confidence
        4. Entity (nama orang, perusahaan, organisasi) dengan tipe dan confidence
        5. Lokasi yang disebutkan (hanya ambil lokasi setingkat provinsi)
        6. Hashtag yang disebutkan
        7. Ringkasan singkat yang memuat inti aduan/laporan (5-10 kalimat)

        Format output JSON:
        {{
            "topic": ["string"],
            "sentiment": "string",
            "sentiment_score": float,
            "emotions": [{{"emotion": "string", "confidence": float}}],
            "entities": [{{"name": "string", "type": "string", "confidence": float}}],
            "locations": ["string"],
            "hashtags": ["string"],
            "summary": "string"
        }}
        """
        
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "Anda adalah AI agent yang ahli dalam menganalisis dan mengekstrak informasi dari teks aduan/laporan dalam bahasa Indonesia."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        return await self._make_request("v3/chat/completions", payload)
    
    async def classify_content(self, content: str, language: str = "id", from_field: str = None, type: str = None) -> Dict[str, Any]:
        """Klasifikasi konten untuk menentukan unit kerja yang tepat"""
        
        # Get unit kerja data from database
        try:
            unit_kerja_data = await unit_kerja_service.get_unit_kerja_data()
        except Exception as e:
            print(f"Error getting unit kerja data: {e}")
            # Use fallback data
            from config import FALLBACK_UNIT_KERJA_DATA
            unit_kerja_data = FALLBACK_UNIT_KERJA_DATA
        
        # Build unit kerja info string
        unit_kerja_info = "Unit Kerja yang tersedia:\n"
        for i, (name, data) in enumerate(unit_kerja_data.items(), 1):
            keywords_str = ", ".join(data["keywords"])
            unit_kerja_info += f"{i}. {name} ({data['email']}) - {data['description']}\n"
            unit_kerja_info += f"   Keywords: {keywords_str}\n"
        
        prompt = f"""
        Sebagai AI agent untuk klasifikasi aduan, analisis konten berikut untuk menentukan unit kerja yang paling tepat:

        Konten: {content}
        
        {unit_kerja_info}
        
        Berdasarkan analisis konten, tentukan:
        1. Unit kerja yang paling sesuai (BSrE atau Dalinfo)
        2. Confidence score (0-1)
        3. Kata kunci yang cocok dari konten
        4. Alasan klasifikasi
        5. Unit kerja alternatif jika ada
        
        Format output JSON:
        {{
            "recommended_unit": {{
                "name": "string",
                "email": "string", 
                "description": "string",
                "confidence": float,
                "matched_keywords": ["string"]
            }},
            "alternative_units": [
                {{
                    "name": "string",
                    "email": "string",
                    "description": "string", 
                    "confidence": float,
                    "matched_keywords": ["string"]
                }}
            ],
            "classification_reason": "string"
        }}
        """
        
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "Anda adalah AI agent yang ahli dalam mengklasifikasi aduan/laporan ke unit kerja yang tepat berdasarkan konten dan konteks."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 800
        }
        
        return await self._make_request("v3/chat/completions", payload)
