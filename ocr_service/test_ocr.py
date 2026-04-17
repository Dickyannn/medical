"""
Test script for OCR service
"""
import requests
import base64
import sys

def test_health():
    """Test health endpoint"""
    print("=" * 50)
    print("Testing Health Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok' and data.get('ocr_ready'):
                print("✓ OCR Service is ready!")
                return True
            else:
                print("✗ OCR Service is not ready")
                return False
        else:
            print("✗ Health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to OCR service")
        print("  Please start the service: start_ocr_service.bat")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_ocr_with_sample():
    """Test OCR with a sample base64 image"""
    print("\n" + "=" * 50)
    print("Testing OCR Endpoint with Sample Image")
    print("=" * 50)
    
    # Create a simple test image (1x1 white pixel)
    # In production, use a real medical document image
    sample_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    try:
        response = requests.post(
            'http://localhost:5000/ocr',
            json={'image': sample_base64},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✓ OCR successful!")
                print(f"  Text length: {len(data.get('text', ''))}")
                print(f"  Confidence: {data.get('confidence', 0)}%")
                print(f"  Word count: {data.get('word_count', 0)}")
                return True
            else:
                print(f"✗ OCR failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print("✗ OCR request failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("\n🔍 OCR Service Test Suite\n")
    
    # Test 1: Health check
    health_ok = test_health()
    
    if not health_ok:
        print("\n❌ OCR service is not running or not ready")
        print("\nTo start the service:")
        print("  1. Open terminal in ocr_service folder")
        print("  2. Run: start_ocr_service.bat")
        sys.exit(1)
    
    # Test 2: OCR processing
    ocr_ok = test_ocr_with_sample()
    
    if ocr_ok:
        print("\n✅ All tests passed!")
        print("\nOCR service is ready for integration with Laravel")
    else:
        print("\n⚠️ OCR processing test failed")
        print("Check the service logs for details")
        sys.exit(1)

if __name__ == '__main__':
    main()
