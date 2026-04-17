# OCR Service - PaddleOCR

Microservice untuk ekstraksi teks dari gambar menggunakan PaddleOCR.

## Requirements

- Python 3.8+
- pip (Python package manager)

## Installation & Setup

### Windows

1. **Install Python** (jika belum ada):
   - Download dari https://www.python.org/downloads/
   - Pastikan centang "Add Python to PATH" saat instalasi

2. **Start OCR Service**:
   ```bash
   cd ocr_service
   start_ocr_service.bat
   ```

   Script akan otomatis:
   - Membuat virtual environment
   - Install dependencies (PaddleOCR, Flask, OpenCV, dll)
   - Start Flask server di port 5000

### Linux/Mac

1. **Create virtual environment**:
   ```bash
   cd ocr_service
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start service**:
   ```bash
   python ocr_engine.py
   ```

## API Endpoints

### Health Check
```
GET http://localhost:5000/health
```

Response:
```json
{
  "status": "ok",
  "paddle_available": true,
  "ocr_ready": true
}
```

### OCR Processing
```
POST http://localhost:5000/ocr
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

Response:
```json
{
  "success": true,
  "text": "Extracted text from image...",
  "confidence": 85,
  "word_count": 42
}
```

## Integration with Laravel

The Laravel backend (`SubmissionController.php`) calls this service via HTTP:

```php
$response = Http::timeout(30)->post('http://localhost:5000/ocr', [
    'image' => $base64Image
]);
```

## Troubleshooting

### Port 5000 already in use
```bash
# Windows: Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### PaddleOCR installation fails
Try installing with specific versions:
```bash
pip install paddlepaddle==3.0.0b1 --no-cache-dir
pip install paddleocr==2.7.0.3 --no-cache-dir
```

### Low OCR accuracy
- Ensure images are high resolution (min 300 DPI)
- Images should have good contrast
- Text should be horizontal (not rotated)
- Use preprocessing (already implemented in `preprocess_image()`)

## Performance

- First request: ~3-5 seconds (model loading)
- Subsequent requests: ~1-2 seconds per image
- Memory usage: ~500MB-1GB

## Features

- ✅ Adaptive thresholding for better contrast
- ✅ Denoising for cleaner text extraction
- ✅ Auto-resize for large images
- ✅ Confidence scoring per word
- ✅ Support for Indonesian medical documents
- ✅ Base64 image input/output
