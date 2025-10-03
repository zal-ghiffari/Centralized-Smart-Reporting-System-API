from typing import List, Dict, Any
import asyncio
from database import get_all_unit_kerja, test_database_connection

class UnitKerjaService:
    def __init__(self):
        self._unit_kerja_cache = None
        self._cache_timestamp = None
        self._cache_duration = 300  # 5 minutes cache
    
    async def get_unit_kerja_data(self, force_refresh: bool = False) -> Dict[str, Dict[str, Any]]:
        """Get unit kerja data with caching"""
        import time
        
        current_time = time.time()
        
        # Check if cache is valid
        if (not force_refresh and 
            self._unit_kerja_cache is not None and 
            self._cache_timestamp is not None and 
            (current_time - self._cache_timestamp) < self._cache_duration):
            return self._unit_kerja_cache
        
        try:
            # Get data from database
            unit_kerja_list = await get_all_unit_kerja()
            
            # Convert to dictionary format
            unit_kerja_dict = {}
            for unit in unit_kerja_list:
                unit_kerja_dict[unit["name"]] = {
                    "email": unit["email"],
                    "description": unit["description"],
                    "keywords": unit["keywords"]
                }
            
            # Update cache
            self._unit_kerja_cache = unit_kerja_dict
            self._cache_timestamp = current_time
            
            return unit_kerja_dict
            
        except Exception as e:
            print(f"Error getting unit kerja data: {e}")
            # Return fallback data
            return {
                "BSrE": {
                    "email": "aduanbsre@bssn.go.id",
                    "description": "BSrE merupakan layanan di BSSN yang mengurus tentang sertifikat elektronik dan tanda tangan digital",
                    "keywords": ["sertifikat elektronik", "tanda tangan digital", "digital signature", "certificate", "enkripsi", "kriptografi"]
                },
                "Dalinfo": {
                    "email": "laporkonten@bssn.go.id",
                    "description": "Dalinfo merupakan unit kerja yang mengurus tentang berita hoax/disinformasi dan sejenisnya, beberapa pelaporan seputar pelanggaran dimedia sosial dapat dilaporkan",
                    "keywords": ["hoax", "disinformasi", "misinformasi", "fake news", "media sosial", "pelanggaran", "konten", "berita palsu"]
                }
            }
    
    async def get_unit_kerja_list(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """Get unit kerja as list"""
        unit_kerja_dict = await self.get_unit_kerja_data(force_refresh)
        
        unit_kerja_list = []
        for name, data in unit_kerja_dict.items():
            unit_kerja_list.append({
                "name": name,
                "email": data["email"],
                "description": data["description"],
                "keywords": data["keywords"]
            })
        
        return unit_kerja_list
    
    async def refresh_cache(self):
        """Force refresh cache"""
        await self.get_unit_kerja_data(force_refresh=True)
    
    async def test_connection(self) -> bool:
        """Test database connection"""
        return await test_database_connection()

# Global instance
unit_kerja_service = UnitKerjaService()
