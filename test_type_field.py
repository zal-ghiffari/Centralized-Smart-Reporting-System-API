"""
Script untuk testing field 'type' pada API Smart Reporting
"""
import requests
import json

# Konfigurasi
BASE_URL = "http://localhost:8000"

def test_type_field():
    """Test field type pada semua endpoint"""
    print("Testing field 'type' pada API endpoints...")
    
    test_data = {
        "content": "Saya ingin melaporkan masalah dengan sertifikat digital saya yang tidak bisa digunakan untuk tanda tangan elektronik.",
        "language": "id",
        "from_field": "xyz@gmail.com",
        "type": "Email"
    }
    
    print(f"Test data: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    print("-" * 50)
    
    # Test /extract endpoint
    print("1. Testing /extract endpoint:")
    try:
        response = requests.post(f"{BASE_URL}/extract", json=test_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Extract endpoint berhasil dengan field 'type'")
        else:
            print(f"   ❌ Extract endpoint gagal: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("-" * 30)
    
    # Test /classify endpoint
    print("2. Testing /classify endpoint:")
    try:
        response = requests.post(f"{BASE_URL}/classify", json=test_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Classify endpoint berhasil dengan field 'type'")
        else:
            print(f"   ❌ Classify endpoint gagal: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("-" * 30)
    
    # Test /process endpoint
    print("3. Testing /process endpoint:")
    try:
        response = requests.post(f"{BASE_URL}/process", json=test_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Process endpoint berhasil dengan field 'type'")
        else:
            print(f"   ❌ Process endpoint gagal: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("-" * 50)
    print("Testing selesai!")

if __name__ == "__main__":
    test_type_field()
