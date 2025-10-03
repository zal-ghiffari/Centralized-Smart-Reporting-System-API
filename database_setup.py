"""
Script untuk membuat tabel unit_kerja di database PostgreSQL
"""
import asyncio
import asyncpg
import json

DATABASE_URL = "postgresql://postgres:password@103.67.244.224:5432/smartreporting_db"

async def create_unit_kerja_table():
    """Create unit_kerja table"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Create table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS unit_kerja (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                keywords TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Table unit_kerja created successfully!")
        
        # Insert sample data
        sample_data = [
            {
                "name": "BSrE",
                "email": "aduanbsre@bssn.go.id",
                "description": "BSrE merupakan layanan di BSSN yang mengurus tentang sertifikat elektronik dan tanda tangan digital",
                "keywords": ["sertifikat elektronik", "tanda tangan digital", "digital signature", "certificate", "enkripsi", "kriptografi"]
            },
            {
                "name": "Dalinfo",
                "email": "laporkonten@bssn.go.id",
                "description": "Dalinfo merupakan unit kerja yang mengurus tentang berita hoax/disinformasi dan sejenisnya, beberapa pelaporan seputar pelanggaran dimedia sosial dapat dilaporkan",
                "keywords": ["hoax", "disinformasi", "misinformasi", "fake news", "media sosial", "pelanggaran", "konten", "berita palsu"]
            },
            {
                "name": "Direktorat Pemerintah Daerah",
                "email": "lapor.d32@bssn.go.id",
                "description": "Direktorat pada BSSN yang menangani perihal koordinasi terkait keamanan siber dengan Pemerintah Daerah di seluruh Indonesia",
                "keywords": [
                    "pemerintah daerah", "pemda", "koordinasi", "keamanan siber daerah", "bssn daerah"
                ],
            },
            {
                "name": "Gov-CSIRT",
                "email": "govcsirt@bssn.go.id",
                "description": "Sebuah layanan dari BSSN yang memangku kepentingan terkait pelaksanaan Computer Security Incident Response Team (CSIRT) di lingkungan Kementerian/Lembaga baik di Pusat maupun di derah",
                "keywords": [
                    "csirt", "insiden siber", "respons insiden", "kementerian", "lembaga", "gov csirt"
                ],
            },
            {
                "name": "Poltek SSN",
                "email": "humas@poltekssn.ac.id",
                "description": "Unit pelaksana Pendidikan dibawah BSSN (Perguruan Tinggi Kedinasan) yang menyelenggarakan Pendidikan Persandian dan Keamanan Siber di Indonesia. Poltek SSN menyelenggarakan pendidikan professional dalam bidang persandian dengan jenjang Diploma IV. Calon Mahasiswa berasal dari lulusan SMA/MA jurusan IPA dan atau Peserta Tugas Belajar atau SMK TI Bidang Keahlian Teknologi Informasi dan Komunikasi; Program Keahlian Teknik Komputer dan Informatika.",
                "keywords": [
                    "poltek ssn", "pendidikan", "persandian", "keamanan siber", "penerimaan mahasiswa"
                ],
            },
            {
                "name": "Pusatik BSSN",
                "email": "pusdatik@bssn.go.id",
                "description": "Unit kerja pada BSSN yang menangani tentang Infrastruktur Teknologi Informasi (TI) untuk semua layanan yang berada pada sistem BSSN.",
                "keywords": [
                    "infrastruktur ti", "pusdatik", "sistem bssn", "operasional ti", "jaringan"
                ],
            },
            {
                "name": "Humas BSSN",
                "email": "humas@bssn.go.id",
                "description": "Hubungan Masyarakat BSSN merupakan layanan publikasi dan dokumentasi seluruh kegiatan dari BSSN. Humas juga yang menjadi jembatan antara BSSN dan pihak luar seperti permintaan kunjungan, kuliah umum, kunjungan industri, kunjungan tour office, dan sejenisnya.",
                "keywords": [
                    "humas", "publikasi", "dokumentasi", "kunjungan", "kuliah umum", "media"
                ],
            },
            {
                "name": "Bantuan 70 BSSN",
                "email": "bantuan70@bssn.go.id",
                "description": "Merupakan Layanan Insiden Respon terhadap pemberitahuan atau pelaporan atas kejadian yang berkaitan dengan gangguan, serangan, pelanggaran, atau aktivitas mencurigakan di sistem informasi, jaringan, atau perangkat elektronik yang dapat berdampak terhadap keamanan siber.",
                "keywords": [
                    "bantuan 70", "insiden", "serangan", "pelanggaran", "respons cepat", "incident response"
                ],
            },
            {
                "name": "Sandi Data",
                "email": "sandi.data@bssn.go.id",
                "description": "Layanan dari Direktorat Keamanan Sandi yang dapat membantu membantu stakeholder (Pemerintah Pusat atau Daerah) dalam menangani proses persandian data pada system mereka, bagaimana mereka dibantu untuk mengamankan data mereka dengan module sandi data.",
                "keywords": [
                    "sandi data", "enkripsi", "keamanan data", "modul sandi", "proteksi data"
                ],
            },
            {
                "name": "Information Technology Security Assessment (ITSA)",
                "email": "layanan.itsa@bssn.go.id",
                "description": "Layanan oleh Direktorat Keamanan Siber yang dapat membantu stakeholder (Pemerintah Pusat atau Daerah) untuk melakukan pengujian pada system mereka, baik itu Web, Mobil app, maupun perangkat infrastruktur, pada pengujian tersebut apakah terdapat kerentanan atau celah.",
                "keywords": [
                    "itsa", "pengujian keamanan", "penetration test", "kerentanan", "pentest", "vulnerability", "assessment"
                ],
            },
            {
                "name": "Museum Sandi",
                "email": "museum.sandi@bssn.go.id",
                "description": "Unit Pelaksana Teknis di lingkungan Badan Siber dan Sandi Negara (BSSN). Museum Sandi mendukung pekerjaan dalam meningkatkan budaya keamanan informasi melalui edukasi kepada masyarakat sekaligus melestarikan nilai-nilai sejarah perjuangan insan persandian sebagai bagian integral perjuangan kemerdekaan Indonesia.",
                "keywords": [
                    "museum sandi", "edukasi", "sejarah persandian", "budaya keamanan informasi", "pameran"
                ],
            }
        ]
        
        for data in sample_data:
            await conn.execute("""
                INSERT INTO unit_kerja (name, email, description, keywords)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (name) DO UPDATE SET
                    email = EXCLUDED.email,
                    description = EXCLUDED.description,
                    keywords = EXCLUDED.keywords,
                    updated_at = CURRENT_TIMESTAMP
            """, data["name"], data["email"], data["description"], json.dumps(data["keywords"]))
        
        print("✅ Sample data inserted successfully!")
        
        # Verify data
        rows = await conn.fetch("SELECT * FROM unit_kerja")
        print(f"✅ Total records in unit_kerja table: {len(rows)}")
        for row in rows:
            print(f"  - {row['name']}: {row['email']}")
            
    except Exception as e:
        print(f"❌ Error creating table: {e}")
    finally:
        await conn.close()

async def create_raw_data_table():
    """Create raw_data table"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Create table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_data (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                language VARCHAR(10) NOT NULL,
                from_field VARCHAR(255) NOT NULL,
                type VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Table raw_data created successfully!")
    except Exception as e:
        print(f"❌ Error creating table: {e}")
    finally:
        await conn.close()

async def create_log_data_table():
    """Create log_data table"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Create table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS log_data (
                id SERIAL PRIMARY KEY,
                action TEXT NOT NULL,
                status VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Table log_data created successfully!")
    except Exception as e:
        print(f"❌ Error creating table: {e}")
    finally:
        await conn.close()

async def create_extraction_data_table():
    """Create extraction_data table"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Create table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS extraction_data (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                language VARCHAR(10) NOT NULL,
                from_field VARCHAR(255) NOT NULL,
                type VARCHAR(255) NOT NULL,
				topic TEXT[],
				sentiment VARCHAR(100),
				sentiment_score NUMERIC(5, 4),
				emotions TEXT[],
				entities TEXT[],
				locations TEXT[],
				hashtags TEXT[],
				summary TEXT,
				recommended_unit_name VARCHAR(255),
				recommended_unit_email VARCHAR(100),
				recommended_unit_desc TEXT,
				recommended_unit_confidence NUMERIC(5, 4),
				recommended_unit_match_key TEXT[],
				alternative_units TEXT[],
				classification_reason TEXT,
				processing_time NUMERIC,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Table extraction_data created successfully!")
    except Exception as e:
        print(f"❌ Error creating table: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_unit_kerja_table())
    asyncio.run(create_raw_data_table())
    asyncio.run(create_log_data_table())
    asyncio.run(create_extraction_data_table())