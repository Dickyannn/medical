"""
OCR Engine - Simplified Version
Minimal dependencies - focuses on field extraction from uploaded images
Use this if full PaddleOCR installation is problematic
"""

from flask import Flask, request, jsonify
import sys
import os
import base64
import io
from PIL import Image

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from data_extraction import MedicalDataExtractor
    EXTRACTION_OK = True
except ImportError as e:
    print(f"❌ Cannot import data_extraction: {e}")
    EXTRACTION_OK = False

try:
    from normalization import DataNormalizer
    NORM_OK = True
except ImportError as e:
    print(f"❌ Cannot import normalization: {e}")
    NORM_OK = False

try:
    from classification import DiseaseClassifier
    CLASS_OK = True
except ImportError as e:
    print(f"❌ Cannot import classification: {e}")
    CLASS_OK = False

try:
    from duplicate_detection import DuplicateDetector
    DUP_OK = True
except ImportError as e:
    print(f"❌ Cannot import duplicate_detection: {e}")
    DUP_OK = False

# Try to import OCR engines
try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
    print("✅ PaddleOCR available")
except ImportError:
    PADDLE_AVAILABLE = False
    print("⚠ PaddleOCR not available - will try pytesseract")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    print("✅ Tesseract available")
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠ Tesseract not available - will use dummy data as fallback")

app = Flask(__name__)

# Initialize components that loaded successfully
try:
    data_extractor = MedicalDataExtractor() if EXTRACTION_OK else None
    normalizer = DataNormalizer() if NORM_OK else None
    classifier = DiseaseClassifier() if CLASS_OK else None
    duplicate_detector = DuplicateDetector() if DUP_OK else None
except Exception as e:
    print(f"⚠ Error initializing components: {e}")

# Initialize OCR engine
try:
    if PADDLE_AVAILABLE:
        # Use minimal PaddleOCR parameters (most compatible)
        paddle_ocr = PaddleOCR(lang='en')
        print("✅ PaddleOCR engine initialized")
    else:
        paddle_ocr = None
except Exception as e:
    print(f"⚠ PaddleOCR initialization error: {e}")
    paddle_ocr = None
    PADDLE_AVAILABLE = False


def decode_base64_image(base64_string):
    """Decode base64 string to PIL Image"""
    try:
        # Remove data:image/...;base64, prefix if exists
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_bytes))
        return image
    except Exception as e:
        print(f"Error decoding base64: {e}")
        return None


def extract_text_from_image(image):
    """Extract text from PIL Image using available OCR"""
    if image is None:
        return None
    
    try:
        # Try PaddleOCR first
        if PADDLE_AVAILABLE and paddle_ocr:
            print("📄 Using PaddleOCR to extract text...")
            import numpy as np
            result = paddle_ocr.ocr(np.array(image), cls=True)
            
            text = ""
            if result:
                for line in result:
                    if line:
                        for word_info in line:
                            text += word_info[1][0] + " "
                    text += "\n"
            
            if text.strip():
                return text.strip()
        
        # Fallback to tesseract
        if TESSERACT_AVAILABLE:
            print("📄 Using Tesseract to extract text...")
            text = pytesseract.image_to_string(image)
            if text.strip():
                return text.strip()
        
        return None
    
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'service': 'Medical Document OCR',
        'modules': {
            'data_extraction': EXTRACTION_OK,
            'normalization': NORM_OK,
            'classification': CLASS_OK,
            'duplicate_detection': DUP_OK,
        },
        'ocr_engines': {
            'paddle': PADDLE_AVAILABLE and paddle_ocr is not None,
            'tesseract': TESSERACT_AVAILABLE,
        },
        'mode': 'real_image_extraction'
    })


@app.route('/ocr', methods=['POST'])
def ocr_basic():
    """Basic OCR - extract text from uploaded image"""
    try:
        data = request.get_json() or {}
        
        if 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing image data'
            }), 400
        
        # Decode base64 image
        image = decode_base64_image(data['image'])
        if image is None:
            return jsonify({
                'success': False,
                'error': 'Failed to decode image'
            }), 400
        
        # Extract text
        text = extract_text_from_image(image)
        if text is None:
            return jsonify({
                'success': False,
                'error': 'No OCR engine available. Please install: pip install paddlepaddle paddleocr'
            }), 500
        
        return jsonify({
            'success': True,
            'text': text,
            'confidence': 75,
            'source': 'paddle_ocr' if PADDLE_AVAILABLE else 'tesseract'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/ocr/extract', methods=['POST'])
def ocr_extract():
    """Extract structured fields from uploaded image"""
    try:
        data = request.get_json() or {}
        
        if 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing image data'
            }), 400
        
        doc_type = data.get('type', 'auto')
        
        # Decode base64 image
        image = decode_base64_image(data['image'])
        if image is None:
            return jsonify({
                'success': False,
                'error': 'Failed to decode image'
            }), 400
        
        # Extract text from image
        raw_text = extract_text_from_image(image)
        
        if raw_text is None:
            return jsonify({
                'success': False,
                'error': 'No OCR engine available. Install: pip install paddlepaddle paddleocr'
            }), 500
        
        print(f"📝 Extracted text length: {len(raw_text)} chars")
        
        # Extract fields using regex patterns
        kwitansi_data = {}
        surat_data = {}
        
        if data_extractor:
            try:
                # Auto-detect document type and extract
                if doc_type == 'kwitansi' or 'kwitansi' in raw_text.lower():
                    print("📄 Extracting KWITANSI fields...")
                    kwitansi_data = data_extractor.extract_kwitansi_all(raw_text)
                
                if doc_type == 'surat' or 'surat' in raw_text.lower():
                    print("📄 Extracting SURAT fields...")
                    surat_data = data_extractor.extract_surat_all(raw_text)
            
            except Exception as e:
                print(f"Error in field extraction: {e}")
        
        extracted = {
            'type': doc_type,
            'kwitansi': kwitansi_data,
            'surat': surat_data,
            'raw_text': raw_text,
            'raw_confidence': 80
        }
        
        # Normalize if available
        if normalizer:
            try:
                normalized_kwitansi = normalizer.normalize_all(kwitansi_data)
                normalized_surat = normalizer.normalize_all(surat_data)
                extracted['normalized_kwitansi'] = normalized_kwitansi
                extracted['normalized_surat'] = normalized_surat
            except Exception as e:
                print(f"Normalization error: {e}")
        
        # Classify if available
        classification = {}
        if classifier and surat_data.get('diagnosis'):
            try:
                classification = classifier.classify(surat_data['diagnosis'])
            except Exception as e:
                print(f"Classification error: {e}")
        
        return jsonify({
            'success': True,
            'data': extracted,
            'classification': classification,
            'confidence': 80,
            'source': 'paddle_ocr' if PADDLE_AVAILABLE else 'tesseract' if TESSERACT_AVAILABLE else 'no_ocr'
        })
    
    except Exception as e:
        import traceback
        print(f"❌ Error in /ocr/extract: {e}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/ocr/check-duplicate', methods=['POST'])
def check_duplicate():
    """Check for duplicates"""
    try:
        if not duplicate_detector:
            return jsonify({
                'success': True,
                'is_duplicate': False,
                'score': 0,
                'warning': 'Duplicate detection not available'
            })
        
        data = request.get_json() or {}
        new_sub = data.get('new_submission')
        existing = data.get('existing_submissions', [])
        
        if not new_sub:
            return jsonify({
                'success': False,
                'error': 'Missing new_submission'
            }), 400
        
        is_dup, score, details = duplicate_detector.calculate_similarity(new_sub, existing)
        
        return jsonify({
            'success': True,
            'is_duplicate': is_dup,
            'score': score,
            'details': details
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🏥 Medical Document OCR Service (Simplified Mode)")
    print("=" * 60)
    print(f"Data Extraction: {'✅' if EXTRACTION_OK else '❌'}")
    print(f"Normalization:   {'✅' if NORM_OK else '❌'}")
    print(f"Classification:  {'✅' if CLASS_OK else '❌'}")
    print(f"Duplicate Det.:  {'✅' if DUP_OK else '❌'}")
    print("=" * 60)
    print("📡 Starting Flask server on http://0.0.0.0:5000")
    print("   Using DUMMY DATA for testing field extraction")
    print("   - POST /ocr → Basic extraction")
    print("   - POST /ocr/extract → Structured fields")
    print("   - POST /ocr/check-duplicate → Duplicate detection")
    print("   - GET /health → Health check")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
