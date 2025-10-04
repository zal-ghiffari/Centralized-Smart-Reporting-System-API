# Centralized Smart Reporting System API

API untuk ekstraksi dan klasifikasi data aduan/laporan menggunakan ArkModel BytePlus sebagai AI agent.

## Fitur

- **Ekstraksi Data**: Mengekstrak topik, sentimen, emosi, entity, lokasi, dan hashtag dari konten aduan
- **Klasifikasi Konten**: Mengklasifikasi aduan ke unit kerja yang tepat secara independen
- **Database Dinamis**: Unit kerja data diambil dari PostgreSQL database secara real-time
- **Caching System**: Sistem cache untuk performa optimal dengan auto-refresh
- **Error Handling**: Error handling yang jelas jika ArkModel atau database tidak tersedia
- **RESTful API**: Endpoint yang mudah digunakan dengan dokumentasi otomatis

## Instalasi

1. Clone repository ini
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Buat file `.env` berdasarkan `.env.example`:
```bash
cp .env.example .env
```

4. Edit file `.env` dan isi konfigurasi:
```
# ArkModel BytePlus Configuration
ARKMODEL_API_KEY=your_api_key_here
ARKMODEL_BASE_URL=https://api.byteplus.com
ARKMODEL_MODEL_NAME=your_model_name

# Database Configuration
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_user_pass
```

## Database Setup

API menggunakan PostgreSQL database untuk menyimpan data unit kerja secara dinamis. Pastikan database sudah dikonfigurasi dengan benar.

```bash
python database_setup.py
```

### Struktur Tabel

```sql
CREATE TABLE IF NOT EXISTS raw_data (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    language VARCHAR(10) NOT NULL,
    from_field VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

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

CREATE TABLE IF NOT EXISTS log_data (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    status VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE IF NOT EXISTS unit_kerja (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    keywords TEXT NOT NULL,  -- JSON string
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sample Data

```sql
INSERT INTO unit_kerja (name, email, description, keywords) VALUES
('BSrE', 'aduanbsre@bssn.go.id', 
 'BSrE merupakan layanan di BSSN yang mengurus tentang sertifikat elektronik dan tanda tangan digital',
 '["sertifikat elektronik", "tanda tangan digital", "digital signature", "certificate", "enkripsi", "kriptografi"]'),
('Dalinfo', 'laporkonten@bssn.go.id',
 'Dalinfo merupakan unit kerja yang mengurus tentang berita hoax/disinformasi dan sejenisnya',
 '["hoax", "disinformasi", "misinformasi", "fake news", "media sosial", "pelanggaran", "konten", "berita palsu"]');
```

## Menjalankan Aplikasi

```bash
python main.py
```

Atau menggunakan uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API akan berjalan di `http://localhost:8000`

## Dokumentasi API

Setelah aplikasi berjalan, buka `http://localhost:8000/docs` untuk melihat dokumentasi interaktif Swagger UI.

## Endpoints

### 1. Health Check
```
GET /
GET /health
```

### 2. Ekstraksi Data
```
POST /extract
```

**Request Body:**
```json
{
  "content": "Saya ingin melaporkan masalah dengan sertifikat digital saya yang tidak bisa digunakan untuk tanda tangan elektronik",
  "language": "id",
  "from_field": "website",
  "type": "Email"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "topic": ["sertifikat digital", "tanda tangan elektronik", "masalah teknis"],
    "sentiment": "negative",
    "sentiment_score": 0.3,
    "emotions": [
      {"emotion": "frustration", "confidence": 0.8}
    ],
    "entities": [
      {"name": "sertifikat digital", "type": "technology", "confidence": 0.9}
    ],
    "locations": [],
    "hashtags": [],
    "summary": "Laporan masalah dengan sertifikat digital yang tidak berfungsi untuk tanda tangan elektronik. Pengguna mengalami kesulitan dalam menggunakan fitur tanda tangan digital pada dokumen penting. Masalah ini terjadi secara konsisten dan mempengaruhi produktivitas kerja."
  },
  "processing_time": 1.2,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 3. Klasifikasi Konten
```
POST /classify
```

**Request Body:**
```json
{
  "content": "Ada berita hoax tentang pemerintah yang beredar di media sosial",
  "language": "id",
  "from_field": "mobile_app",
  "type": "SMS"
}
```

**Catatan:** Agent klasifikasi bekerja secara independen dari agent ekstraksi dan menganalisis konten langsung untuk menentukan unit kerja yang tepat.

**Response:**
```json
{
  "success": true,
  "data": {
    "recommended_unit": {
      "name": "Dalinfo",
      "email": "laporkonten@bssn.go.id",
      "description": "Dalinfo merupakan unit kerja yang mengurus tentang berita hoax/disinformasi dan sejenisnya",
      "confidence": 0.9,
      "matched_keywords": ["hoax", "media sosial"]
    },
    "alternative_units": [
      {
        "name": "BSrE",
        "email": "aduanbsre@bssn.go.id",
        "description": "BSrE merupakan layanan di BSSN yang mengurus tentang sertifikat elektronik dan tanda tangan digital",
        "confidence": 0.1,
        "matched_keywords": []
      }
    ],
    "classification_reason": "Konten mengandung kata kunci hoax dan media sosial yang sesuai dengan domain Dalinfo"
  },
  "processing_time": 0.8,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 4. Proses Lengkap
```
POST /process
```

**Request Body:**
```json
{
  "content": "Saya menemukan konten hoax tentang COVID-19 di Facebook yang sangat menyesatkan masyarakat",
  "language": "id",
  "from_field": "social_media",
  "type": "Social Media"
}
```

**Response:**
```json
{
  "extraction": {
    "topic": ["hoax", "COVID-19", "Facebook", "disinformasi"],
    "sentiment": "negative",
    "sentiment_score": 0.2,
    "emotions": [{"emotion": "concern", "confidence": 0.8}],
    "entities": [
      {"name": "COVID-19", "type": "medical", "confidence": 0.9},
      {"name": "Facebook", "type": "platform", "confidence": 0.9}
    ],
    "locations": [],
    "hashtags": [],
    "summary": "Laporan konten hoax tentang COVID-19 yang menyesatkan di platform Facebook. Konten ini telah viral dan banyak masyarakat yang terpengaruh oleh informasi palsu tersebut. Dampaknya sangat merugikan karena menyebarkan ketakutan dan kebingungan di tengah pandemi."
  },
  "classification": {
    "recommended_unit": {
      "name": "Dalinfo",
      "email": "laporkonten@bssn.go.id",
      "description": "Dalinfo merupakan unit kerja yang mengurus tentang berita hoax/disinformasi dan sejenisnya",
      "confidence": 0.95,
      "matched_keywords": ["hoax", "menyesatkan"]
    },
    "alternative_units": [
      {
        "name": "BSrE",
        "email": "aduanbsre@bssn.go.id",
        "description": "BSrE merupakan layanan di BSSN yang mengurus tentang sertifikat elektronik dan tanda tangan digital",
        "confidence": 0.05,
        "matched_keywords": []
      }
    ],
    "classification_reason": "Konten jelas mengandung hoax dan disinformasi yang merupakan domain Dalinfo"
  },
  "processing_time": 2.1,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 5. Daftar Unit Kerja (Dinamis dari Database)
```
GET /units
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "BSrE",
      "email": "aduanbsre@bssn.go.id",
      "description": "BSrE merupakan layanan di BSSN yang mengurus tentang sertifikat elektronik dan tanda tangan digital",
      "keywords": ["sertifikat elektronik", "tanda tangan digital", "digital signature", "certificate", "enkripsi", "kriptografi"]
    },
    {
      "name": "Dalinfo",
      "email": "laporkonten@bssn.go.id",
      "description": "Dalinfo merupakan unit kerja yang mengurus tentang berita hoax/disinformasi dan sejenisnya",
      "keywords": ["hoax", "disinformasi", "misinformasi", "fake news", "media sosial", "pelanggaran", "konten", "berita palsu"]
    },
    {
      "name": "Direktorat Pemerintah Daerah",
      "email": "lapor.d32@bssn.go.id",
      "description": "Direktorat pada BSSN yang menangani perihal koordinasi terkait keamanan siber dengan Pemerintah Daerah di seluruh Indonesia",
      "keywords": ["pemerintah daerah", "pemda", "koordinasi", "keamanan siber daerah", "bssn daerah"]
    },
    {
      "name": "Gov-CSIRT",
      "email": "govcsirt@bssn.go.id",
      "description": "Sebuah layanan dari BSSN yang memangku kepentingan terkait pelaksanaan CSIRT di lingkungan K/L",
      "keywords": ["csirt", "insiden siber", "respons insiden", "kementerian", "lembaga"]
    }
  ],
  "timestamp": "2024-01-15T10:30:00",
  "source": "database"
}
```

### 6. Refresh Cache Unit Kerja
```
POST /units/refresh
```

**Response:**
```json
{
  "success": true,
  "message": "Unit kerja cache refreshed successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 7. Status Database
```
GET /database/status
```

**Response:**
```json
{
  "success": true,
  "database_connected": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

## Contoh Penggunaan dengan cURL

### Ekstraksi Data
```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Saya ingin melaporkan masalah dengan sertifikat digital saya",
    "language": "id",
    "from_field": "website",
  "type": "Email"
  }'
```

### Proses Lengkap
```bash
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Ada berita hoax tentang pemerintah yang beredar di media sosial",
    "language": "id",
    "from_field": "mobile_app",
  "type": "SMS"
  }'
```

## Contoh Penggunaan dengan Python

### Menggunakan Endpoint Terpisah (Ekstraksi dan Klasifikasi Independen)

```python
import requests
import json

# Test ekstraksi data
extract_url = "http://localhost:8000/extract"
extract_data = {
    "content": "Saya menemukan konten hoax tentang COVID-19 di Facebook yang sangat menyesatkan masyarakat",
    "language": "id",
    "from_field": "website",
  "type": "Email"
}

extract_response = requests.post(extract_url, json=extract_data)
extract_result = extract_response.json()

print("Hasil Ekstraksi:")
print(f"Topik: {', '.join(extract_result['data']['topic'])}")
print(f"Sentimen: {extract_result['data']['sentiment']}")
print(f"Skor Sentimen: {extract_result['data']['sentiment_score']}")

# Test klasifikasi (bekerja independen dari ekstraksi)
classify_url = "http://localhost:8000/classify"
classify_data = {
    "content": "Saya menemukan konten hoax tentang COVID-19 di Facebook yang sangat menyesatkan masyarakat",
    "language": "id",
    "from_field": "mobile_app",
  "type": "SMS"
}

classify_response = requests.post(classify_url, json=classify_data)
classify_result = classify_response.json()

print("\nHasil Klasifikasi:")
print(f"Unit Kerja: {classify_result['data']['recommended_unit']['name']}")
print(f"Email: {classify_result['data']['recommended_unit']['email']}")
print(f"Confidence: {classify_result['data']['recommended_unit']['confidence']}")
```

### Menggunakan Endpoint Lengkap (Ekstraksi + Klasifikasi)

```python
# URL API
url = "http://localhost:8000/process"

# Data request
data = {
    "content": "Saya menemukan konten hoax tentang COVID-19 di Facebook yang sangat menyesatkan masyarakat",
    "language": "id",
    "from_field": "social_media",
  "type": "Social Media"
}

# Kirim request
response = requests.post(url, json=data)

# Parse response
result = response.json()

print("Hasil Ekstraksi:")
print(f"Topik: {', '.join(result['extraction']['topic'])}")
print(f"Sentimen: {result['extraction']['sentiment']}")
print(f"Skor Sentimen: {result['extraction']['sentiment_score']}")

print("\nHasil Klasifikasi:")
print(f"Unit Kerja: {result['classification']['recommended_unit']['name']}")
print(f"Email: {result['classification']['recommended_unit']['email']}")
print(f"Confidence: {result['classification']['recommended_unit']['confidence']}")
```

## Struktur Project

```
smart-reporting/
├── main.py                 # FastAPI application
├── models.py              # Pydantic models
├── services.py            # Business logic services
├── arkmodel_client.py     # ArkModel BytePlus client
├── config.py              # Configuration settings
├── database.py            # Database connection and queries
├── unit_kerja_service.py  # Unit kerja service with caching
├── requirements.txt       # Python dependencies
├── run.py                 # Application runner
├── test_api.py           # API test suite
└── README.md             # Documentation
```

## Unit Kerja (Dinamis dari Database)

Data unit kerja sekarang diambil secara dinamis dari PostgreSQL database. Berikut adalah contoh unit kerja yang tersedia:

### BSrE (Badan Sertifikasi Elektronik)
- **Email**: aduanbsre@bssn.go.id
- **Domain**: Sertifikat elektronik dan tanda tangan digital
- **Keywords**: sertifikat elektronik, tanda tangan digital, digital signature, certificate, enkripsi, kriptografi

### Dalinfo (Direktorat Analisis Informasi)
- **Email**: laporkonten@bssn.go.id
- **Domain**: Berita hoax/disinformasi dan pelanggaran media sosial
- **Keywords**: hoax, disinformasi, misinformasi, fake news, media sosial, pelanggaran, konten, berita palsu

### Direktorat Pemerintah Daerah
- **Email**: lapor.d32@bssn.go.id
- **Domain**: Koordinasi keamanan siber dengan Pemerintah Daerah
- **Keywords**: pemerintah daerah, pemda, koordinasi, keamanan siber daerah

### Gov-CSIRT
- **Email**: govcsirt@bssn.go.id
- **Domain**: CSIRT untuk Kementerian/Lembaga (pusat dan daerah)
- **Keywords**: csirt, insiden siber, respons insiden, kementerian, lembaga

### Poltek SSN
- **Email**: humas@poltekssn.ac.id
- **Domain**: Pendidikan persandian dan keamanan siber (PTK BSSN)
- **Keywords**: poltek ssn, pendidikan, persandian, keamanan siber

### Pusatik BSSN
- **Email**: pusdatik@bssn.go.id
- **Domain**: Infrastruktur TI untuk layanan di sistem BSSN
- **Keywords**: infrastruktur ti, pusdatik, jaringan, operasional ti

### Humas BSSN
- **Email**: humas@bssn.go.id
- **Domain**: Publikasi, dokumentasi, dan fasilitasi kunjungan
- **Keywords**: humas, publikasi, dokumentasi, kunjungan, media

### Bantuan 70 BSSN
- **Email**: bantuan70@bssn.go.id
- **Domain**: Layanan respons insiden terhadap gangguan/serangan siber
- **Keywords**: bantuan 70, insiden, serangan, pelanggaran, incident response

### Sandi Data
- **Email**: sandi.data@bssn.go.id
- **Domain**: Persandian data dan proteksi data
- **Keywords**: sandi data, enkripsi, keamanan data, modul sandi

### Information Technology Security Assessment (ITSA)
- **Email**: layanan.itsa@bssn.go.id
- **Domain**: Pengujian keamanan (web, mobile app, infrastruktur)
- **Keywords**: itsa, pengujian keamanan, pentest, vulnerability, assessment

### Museum Sandi
- **Email**: museum.sandi@bssn.go.id
- **Domain**: Edukasi dan pelestarian sejarah persandian
- **Keywords**: museum sandi, edukasi, sejarah persandian, budaya keamanan informasi

**Catatan**: Data unit kerja dapat ditambah, diubah, atau dinonaktifkan melalui database tanpa perlu mengubah kode aplikasi.

## Error Handling

API menggunakan sistem error handling yang komprehensif:
- HTTP status codes yang sesuai
- Error messages yang informatif
- Tidak ada fallback system - jika ArkModel gagal, akan mengembalikan error yang jelas
- Global exception handler

### Contoh Error Response

```json
{
  "error": "ArkModel extraction failed: HTTP error: 401 - Unauthorized",
  "detail": "Invalid API key or authentication failed",
  "timestamp": "2024-01-15T10:30:00"
}
```

## Development

Untuk development, gunakan:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Ini akan menjalankan server dengan auto-reload untuk development.
