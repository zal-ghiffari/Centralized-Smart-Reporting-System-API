import os
from typing import List, Dict
from pydantic import BaseSettings

class Settings(BaseSettings):
    # ArkModel BytePlus Configuration
    arkmodel_api_key: str = os.getenv("ARKMODEL_API_KEY", "8bd81401-e8d6-4309-b4d2-ae84b56b5f93")
    arkmodel_base_url: str = os.getenv("ARKMODEL_BASE_URL", "https://ark.ap-southeast.bytepluses.com/api")
    arkmodel_model_name: str = os.getenv("ARKMODEL_MODEL_NAME", "seed-1-6-250915")
    
    # Database Configuration
    db_host: str = os.getenv("DB_HOST", "103.67.244.224")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "smartreporting_db")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "password")
    
    # Application Configuration
    app_name: str = "Centralized Smart Reporting System API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    port: int = int(os.getenv("PORT", "8000"))
    
    class Config:
        env_file = ".env"

# Static data untuk unit kerja (fallback jika database tidak tersedia)
FALLBACK_UNIT_KERJA_DATA = {
    "BSrE": {
        "email": "aduanbsre@bssn.go.id",
        "description": "BSrE merupakan layanan di BSSN yang mengurus tentang sertifikat elektronik dan tanda tangan digital",
        "keywords": ["sertifikat elektronik", "tanda tangan digital", "digital signature", "certificate", "enkripsi", "kriptografi"]
    },
    "Dalinfo": {
        "email": "laporkonten@bssn.go.id",
        "description": "Dalinfo merupakan unit kerja yang mengurus tentang berita hoax/disinformasi dan sejenisnya, beberapa pelaporan seputar pelanggaran dimedia sosial dapat dilaporkan",
        "keywords": ["hoax", "disinformasi", "misinformasi", "fake news", "media sosial", "pelanggaran", "konten", "berita palsu"]
    },
    "Direktorat Pemerintah Daerah": {
        "email": "lapor.d32@bssn.go.id",
        "description": "Direktorat pada BSSN yang menangani perihal koordinasi terkait keamanan siber dengan Pemerintah Daerah di seluruh Indonesia",
        "keywords": ["pemerintah daerah", "pemda", "koordinasi", "keamanan siber daerah", "bssn daerah"]
    },
    "Gov-CSIRT": {
        "email": "govcsirt@bssn.go.id",
        "description": "Sebuah layanan dari BSSN yang memangku kepentingan terkait pelaksanaan Computer Security Incident Response Team (CSIRT) di lingkungan Kementerian/Lembaga baik di Pusat maupun di derah",
        "keywords": ["csirt", "insiden siber", "respons insiden", "kementerian", "lembaga", "gov csirt"]
    },
    "Poltek SSN": {
        "email": "humas@poltekssn.ac.id",
        "description": "Unit pelaksana Pendidikan dibawah BSSN (Perguruan Tinggi Kedinasan) yang menyelenggarakan Pendidikan Persandian dan Keamanan Siber di Indonesia. Poltek SSN menyelenggarakan pendidikan professional dalam bidang persandian dengan jenjang Diploma IV. Calon Mahasiswa berasal dari lulusan SMA/MA jurusan IPA dan atau Peserta Tugas Belajar atau SMK TI Bidang Keahlian Teknologi Informasi dan Komunikasi; Program Keahlian Teknik Komputer dan Informatika.",
        "keywords": ["poltek ssn", "pendidikan", "persandian", "keamanan siber", "penerimaan mahasiswa"]
    },
    "Pusatik BSSN": {
        "email": "pusdatik@bssn.go.id",
        "description": "Unit kerja pada BSSN yang menangani tentang Infrastruktur Teknologi Informasi (TI) untuk semua layanan yang berada pada sistem BSSN.",
        "keywords": ["infrastruktur ti", "pusdatik", "sistem bssn", "operasional ti", "jaringan"]
    },
    "Humas BSSN": {
        "email": "humas@bssn.go.id",
        "description": "Hubungan Masyarakat BSSN merupakan layanan publikasi dan dokumentasi seluruh kegiatan dari BSSN. Humas juga yang menjadi jembatan antara BSSN dan pihak luar seperti permintaan kunjungan, kuliah umum, kunjungan industri, kunjungan tour office, dan sejenisnya.",
        "keywords": ["humas", "publikasi", "dokumentasi", "kunjungan", "kuliah umum", "media"]
    },
    "Bantuan 70 BSSN": {
        "email": "bantuan70@bssn.go.id",
        "description": "Merupakan Layanan Insiden Respon terhadap pemberitahuan atau pelaporan atas kejadian yang berkaitan dengan gangguan, serangan, pelanggaran, atau aktivitas mencurigakan di sistem informasi, jaringan, atau perangkat elektronik yang dapat berdampak terhadap keamanan siber.",
        "keywords": ["bantuan 70", "insiden", "serangan", "pelanggaran", "respons cepat", "incident response"]
    },
    "Sandi Data": {
        "email": "sandi.data@bssn.go.id",
        "description": "Layanan dari Direktorat Keamanan Sandi yang dapat membantu membantu stakeholder (Pemerintah Pusat atau Daerah) dalam menangani proses persandian data pada system mereka, bagaimana mereka dibantu untuk mengamankan data mereka dengan module sandi data.",
        "keywords": ["sandi data", "enkripsi", "keamanan data", "modul sandi", "proteksi data"]
    },
    "Information Technology Security Assessment (ITSA)": {
        "email": "layanan.itsa@bssn.go.id",
        "description": "Layanan oleh Direktorat Keamanan Siber yang dapat membantu stakeholder (Pemerintah Pusat atau Daerah) untuk melakukan pengujian pada system mereka, baik itu Web, Mobil app, maupun perangkat infrastruktur, pada pengujian tersebut apakah terdapat kerentanan atau celah.",
        "keywords": ["itsa", "pengujian keamanan", "penetration test", "kerentanan", "pentest", "vulnerability", "assessment"]
    },
    "Museum Sandi": {
        "email": "museum.sandi@bssn.go.id",
        "description": "Unit Pelaksana Teknis di lingkungan Badan Siber dan Sandi Negara (BSSN). Museum Sandi mendukung pekerjaan dalam meningkatkan budaya keamanan informasi melalui edukasi kepada masyarakat sekaligus melestarikan nilai-nilai sejarah perjuangan insan persandian sebagai bagian integral perjuangan kemerdekaan Indonesia.",
        "keywords": ["museum sandi", "edukasi", "sejarah persandian", "budaya keamanan informasi", "pameran"]
    }
}

settings = Settings()
