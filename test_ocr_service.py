#!/usr/bin/env python3
"""
Test script to verify Flask OCR service can extract from actual images
"""
import base64
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import time

def create_test_image():
    """Create a test image with OCR-readable text"""
    print("📸 Creating test image with medical document text...")
    
    # Create image with white background
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add test text (simulating a medical document)
    text_lines = [
        "RUMAH SAKIT SILOAM KEBON JERUK",
        "",
        "INVOICE / KWITANSI PEMBAYARAN",
        "",
        "Nomor Kwitansi: KW/2025/04/3143",
        "Tanggal: 14 April 2025",
        "Biaya Layanan: Rp 1.036.745",
        "Pasien: Budi Santoso",
        "",
        "SURAT KETERANGAN SAKIT",
        "",
        "Dokter: dr. Reza Wijaya, Sp.PD",
        "Diagnosa: Hipertensi Esensial Tahap 2",
        "Tanggal Mulai Sakit: 10 April 2025",
        "Tanggal Selesai: 14 April 2025",
    ]
    
    y = 30
    for line in text_lines:
        draw.text((30, y), line, fill='black')
        y += 40
    
    # Convert to base64
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    base64_str = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    
    print(f"✅ Test image created: {len(base64_str)} chars base64")
    return f"data:image/png;base64,{base64_str}"

def test_flask_service():
    """Test Flask OCR service endpoints"""
    
    print("\n" + "="*60)
    print("🧪 Testing Flask OCR Service")
    print("="*60)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n[1] Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   PaddleOCR: {'✅' if data.get('paddle_ocr') else '❌'}")
            print(f"   Tesseract: {'✅' if data.get('tesseract') else '❌'}")
            print(f"   Mode: {data.get('mode', 'unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Create test image and extract
    print("\n[2] Testing /ocr endpoint with test image...")
    try:
        base64_image = create_test_image()
        
        payload = {
            "image": base64_image
        }
        
        response = requests.post(
            f"{base_url}/ocr",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                extracted_text = data.get('text', '')
                print(f"✅ OCR extraction successful")
                print(f"   Text length: {len(extracted_text)} chars")
                if extracted_text:
                    print(f"   First 100 chars: {extracted_text[:100]}...")
                else:
                    print(f"   ⚠️  No text extracted")
            else:
                print(f"❌ Extraction failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Extract structured fields
    print("\n[3] Testing /ocr/extract endpoint...")
    try:
        base64_image = create_test_image()
        
        payload = {
            "image": base64_image,
            "type": "auto"
        }
        
        response = requests.post(
            f"{base_url}/ocr/extract",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                extracted = data.get('data', {})
                print(f"✅ Field extraction successful")
                print(f"   Confidence: {data.get('confidence')}%")
                print(f"   Source: {data.get('source', 'unknown')}")
                
                kwitansi = extracted.get('kwitansi', {})
                surat = extracted.get('surat', {})
                
                if kwitansi:
                    print(f"\n   🏥 Kwitansi Fields:")
                    for key, val in kwitansi.items():
                        if val:
                            print(f"      {key}: {val}")
                
                if surat:
                    print(f"\n   📄 Surat Fields:")
                    for key, val in surat.items():
                        if val:
                            print(f"      {key}: {val}")
            else:
                print(f"❌ Extraction failed: {data.get('error', 'Unknown error')}")
                if 'traceback' in data:
                    print(f"   Traceback: {data['traceback'][:200]}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("✅ Flask service test complete!")
    print("="*60)

if __name__ == "__main__":
    # Wait a moment for Flask to be ready
    print("⏳ Waiting for Flask service to be ready...")
    time.sleep(2)
    
    test_flask_service()
