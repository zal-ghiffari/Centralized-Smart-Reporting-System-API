"""
Script untuk testing API Smart Reporting
"""
import requests
import json
import time

# Konfigurasi
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_extract():
    """Test extraction endpoint"""
    print("Testing extraction endpoint...")
    
    test_data = {
        "content": "Saya ingin melaporkan masalah dengan sertifikat digital saya yang tidak bisa digunakan untuk tanda tangan elektronik. Ini sangat menyusahkan karena saya perlu menyelesaikan dokumen penting.",
        "language": "id",
        "from_field": "website",
        "type": "Email"
    }
    
    response = requests.post(f"{BASE_URL}/extract", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print("-" * 50)

def test_classify():
    """Test classification endpoint"""
    print("Testing classification endpoint...")
    
    test_data = {
        "content": "Ada berita hoax tentang pemerintah yang beredar di media sosial dan sangat menyesatkan masyarakat",
        "language": "id",
        "from_field": "mobile_app",
        "type": "SMS"
    }
    
    response = requests.post(f"{BASE_URL}/classify", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print("-" * 50)

def test_process():
    """Test complete processing endpoint"""
    print("Testing complete processing endpoint...")
    
    test_cases = [
        {
            "name": "BSrE Case",
            "content": "Saya mengalami masalah dengan sertifikat digital saya yang tidak bisa digunakan untuk tanda tangan elektronik pada dokumen penting. Mohon bantuan untuk mengatasi masalah ini.",
            "language": "id",
            "from_field": "website",
            "type": "Email"
        },
        {
            "name": "Dalinfo Case", 
            "content": "Saya menemukan konten hoax tentang COVID-19 di Facebook yang sangat menyesatkan masyarakat. Konten ini sudah viral dan banyak yang percaya.",
            "language": "id",
            "from_field": "social_media",
            "type": "Social Media"
        },
        {
            "name": "Mixed Case",
            "content": "Ada masalah dengan sertifikat digital yang digunakan untuk memverifikasi berita hoax di media sosial. Ini sangat membingungkan.",
            "language": "id",
            "from_field": "mobile_app",
            "type": "Mobile App"
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting {test_case['name']}:")
        print(f"Content: {test_case['content']}")
        
        response = requests.post(f"{BASE_URL}/process", json=test_case)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Extraction Topic: {', '.join(result['extraction']['topic'])}")
            print(f"Sentiment: {result['extraction']['sentiment']} ({result['extraction']['sentiment_score']})")
            print(f"Recommended Unit: {result['classification']['recommended_unit']['name']}")
            print(f"Confidence: {result['classification']['recommended_unit']['confidence']}")
            print(f"Email: {result['classification']['recommended_unit']['email']}")
            print(f"Processing Time: {result['processing_time']:.2f}s")
        else:
            print(f"Error: {response.text}")
        
        print("-" * 50)

def test_units():
    """Test units endpoint"""
    print("Testing units endpoint...")
    response = requests.get(f"{BASE_URL}/units")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print("-" * 50)

def main():
    """Run all tests"""
    print("Smart Reporting API Test Suite")
    print("=" * 50)
    
    try:
        # Test health check
        test_health()
        
        # Test extraction
        test_extract()
        
        # Test classification
        test_classify()
        
        # Test complete processing
        test_process()
        
        # Test units
        test_units()
        
        print("\nAll tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
