import asyncio
import asyncpg
from typing import List, Dict, Any
import json

# Database configuration
DATABASE_URL = "postgresql://postgres:password@103.67.244.224:5432/smartreporting_db"

async def get_db_connection():
    """Get database connection"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

async def get_all_unit_kerja() -> List[Dict[str, Any]]:
    """Get all active unit kerja from database"""
    conn = await get_db_connection()
    if not conn:
        return get_fallback_data()
    
    try:
        query = """
        SELECT id, name, email, description, keywords, is_active 
        FROM unit_kerja 
        WHERE is_active = true
        """
        rows = await conn.fetch(query)
        
        unit_kerja_list = []
        for row in rows:
            unit_kerja_list.append({
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "description": row["description"],
                "keywords": json.loads(row["keywords"]) if row["keywords"] else [],
                "is_active": row["is_active"]
            })
        
        return unit_kerja_list
        
    except Exception as e:
        print(f"Error getting unit kerja from database: {e}")
        return get_fallback_data()
    finally:
        await conn.close()

def get_fallback_data() -> List[Dict[str, Any]]:
    """Fallback data if database is unavailable"""
    return [
        {
            "id": 1,
            "name": "BSrE",
            "email": "aduanbsre@bssn.go.id",
            "description": "BSrE merupakan layanan di BSSN yang mengurus tentang sertifikat elektronik dan tanda tangan digital",
            "keywords": ["sertifikat elektronik", "tanda tangan digital", "digital signature", "certificate", "enkripsi", "kriptografi"],
            "is_active": True
        },
        {
            "id": 2,
            "name": "Dalinfo",
            "email": "laporkonten@bssn.go.id",
            "description": "Dalinfo merupakan unit kerja yang mengurus tentang berita hoax/disinformasi dan sejenisnya, beberapa pelaporan seputar pelanggaran dimedia sosial dapat dilaporkan",
            "keywords": ["hoax", "disinformasi", "misinformasi", "fake news", "media sosial", "pelanggaran", "konten", "berita palsu"],
            "is_active": True
        }
    ]

async def test_database_connection():
    """Test database connection"""
    conn = await get_db_connection()
    if conn:
        try:
            result = await conn.fetchval("SELECT 1")
            print("✅ Database connection successful!")
            return True
        except Exception as e:
            print(f"❌ Database query failed: {e}")
            return False
        finally:
            await conn.close()
    else:
        print("❌ Database connection failed!")
        return False

if __name__ == "__main__":
    # Test database connection
    asyncio.run(test_database_connection())
