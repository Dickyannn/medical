"""
OCR Engine - Enhanced for Medical Documents
Mengekstrak text dari gambar/PDF dengan preprocessing optimal
Adapted from: hr-medical-leave-system-OCR
"""
import io
import sys

# Try to import optional dependencies
try:
    from pdf2image import convert_from_bytes
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
    convert_from_bytes = None

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None
    np = None

try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
except ImportError:
    PADDLE_AVAILABLE = False
    PaddleOCR = None


class OCREngine:
    """OCR Engine using PaddleOCR"""
    
    def __init__(self, use_gpu=False):
        self.use_gpu = use_gpu
        if PADDLE_AVAILABLE:
            try:
                # Initialize PaddleOCR with angle classification and English language
                self.ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang='en',  # English for medical terms
                    use_gpu=use_gpu,
                    show_log=False
                )
                print("✓ PaddleOCR initialized successfully")
            except Exception as e:
                print(f"⚠ Warning: PaddleOCR initialization error: {e}")
                self.ocr = None
        else:
            print("⚠ PaddleOCR not available - install: pip install paddlepaddle paddleocr")
            self.ocr = None

    def pdf_to_images(self, pdf_bytes):
        """Convert PDF to list of PIL Image objects"""
        if not PDF2IMAGE_AVAILABLE or convert_from_bytes is None:
            print("⚠ pdf2image not available - cannot convert PDF")
            return []
        
        try:
            images = convert_from_bytes(pdf_bytes, fmt='ppm')
            return images
        except Exception as e:
            print(f"Error converting PDF: {e}")
            return []

    def preprocess_image(self, image):
        """
        Preprocess image untuk OCR optimal
        - Resize jika terlalu besar
        - Convert ke grayscale
        - Adaptive thresholding untuk kontras lebih baik
        - Denoise
        """
        # If cv2 not available, just return PIL image as is
        if not CV2_AVAILABLE or cv2 is None:
            return image
        
        # Convert PIL to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Resize jika terlalu besar
        height, width = cv_image.shape[:2]
        if width > 3000:
            scale = 3000 / width
            cv_image = cv2.resize(cv_image, (3000, int(height * scale)))
        
        # Convert to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Adaptive thresholding untuk kontras lebih baik
        gray = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Denoise
        gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        return gray

    def extract_text_from_image(self, image):
        """
        Extract text from image using PaddleOCR
        Returns raw text dengan confidence scores
        """
        if not PADDLE_AVAILABLE or self.ocr is None:
            return {
                'text': '',
                'confidence': 0,
                'error': 'PaddleOCR not available - ensure paddlepaddle & paddleocr installed'
            }
        
        try:
            # Preprocess
            processed = self.preprocess_image(image)
            
            # Convert back to PIL for PaddleOCR
            processed_pil = Image.fromarray(processed)
            
            # Run OCR
            result = self.ocr.ocr(np.array(processed_pil), cls=True)
            
            # Parse hasil OCR
            full_text = ""
            total_confidence = 0
            word_count = 0
            
            if result:
                for line in result:
                    if line:
                        for word_info in line:
                            text = word_info[1][0]
                            confidence = word_info[1][1]
                            
                            # Only take text with confidence > 0.3
                            if confidence > 0.3:
                                full_text += text + " "
                                total_confidence += confidence
                                word_count += 1
                    full_text += "\n"
            
            avg_confidence = (total_confidence / word_count * 100) if word_count > 0 else 0
            
            return {
                'text': full_text.strip(),
                'confidence': int(avg_confidence),
                'word_count': word_count
            }
        
        except Exception as e:
            return {
                'text': '',
                'confidence': 0,
                'error': f'OCR error: {str(e)}'
            }

    def process_file(self, file_bytes, file_type):
        """
        Process file (PDF or image) -> raw text
        
        Args:
            file_bytes: File content as bytes
            file_type: 'pdf', 'jpg', 'png', 'jpeg'
        
        Returns:
            {'text': '...', 'confidence': 85, 'pages': 1}
        """
        images = []
        
        if file_type.lower() == 'pdf':
            images = self.pdf_to_images(file_bytes)
        else:
            # Image format
            try:
                image = Image.open(io.BytesIO(file_bytes))
                images = [image]
            except Exception as e:
                return {
                    'text': '',
                    'confidence': 0,
                    'error': f'Can\'t open image: {str(e)}'
                }
        
        if not images:
            return {
                'text': '',
                'confidence': 0,
                'error': 'No images found in file'
            }
        
        # Process all pages/images
        all_texts = []
        confidences = []
        
        for image in images:
            result = self.extract_text_from_image(image)
            if 'error' not in result:
                all_texts.append(result['text'])
                confidences.append(result['confidence'])
        
        # Combine results
        combined_text = "\n---PAGE BREAK---\n".join(all_texts)
        avg_confidence = int(np.mean(confidences)) if confidences else 0
        
        return {
            'text': combined_text,
            'confidence': avg_confidence,
            'pages': len(images)
        }

    def process_base64_image(self, base64_string):
        """
        Process base64 encoded image
        
        Args:
            base64_string: Base64 image string (with or without 'data:image/...;base64,' prefix)
        
        Returns:
            {'text': '...', 'confidence': 85}
        """
        try:
            # Remove data:image/...;base64, prefix if exists
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64
            import base64
            image_bytes = base64.b64decode(base64_string)
            
            # Open image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Extract text
            result = self.extract_text_from_image(image)
            
            return result
        
        except Exception as e:
            return {
                'text': '',
                'confidence': 0,
                'error': f'Error processing base64 image: {str(e)}'
            }


# ============================================================
# Flask App Setup with Routes
# ============================================================

from flask import Flask, request, jsonify
from data_extraction import MedicalDataExtractor
from normalization import DataNormalizer
from classification import DiseaseClassifier
from duplicate_detection import DuplicateDetector

app = Flask(__name__)

# Initialize components
ocr_engine = OCREngine(use_gpu=False)
data_extractor = MedicalDataExtractor()
normalizer = DataNormalizer()
classifier = DiseaseClassifier()
duplicate_detector = DuplicateDetector()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'Medical Document OCR',
        'paddle_available': PADDLE_AVAILABLE,
        'ocr_ready': ocr_engine.ocr is not None,
    })


@app.route('/ocr', methods=['POST'])
def ocr_basic():
    """
    Basic OCR endpoint - returns raw extracted text only
    
    Request:
    {
        "image": "base64_string"
    }
    
    Response:
    {
        "success": true,
        "text": "raw OCR text...",
        "confidence": 85,
        "word_count": 1250
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing image data'
            }), 400
        
        base64_image = data['image']
        result = ocr_engine.process_base64_image(base64_image)
        
        if 'error' in result and result['error']:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
        return jsonify({
            'success': True,
            'text': result['text'],
            'confidence': result['confidence'],
            'word_count': result.get('word_count', 0)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/ocr/extract', methods=['POST'])
def ocr_extract():
    """
    Enhanced OCR endpoint - returns structured fields
    
    Request:
    {
        "image": "base64_string",
        "type": "kwitansi|surat|auto"
    }
    
    Response:
    {
        "success": true,
        "data": {
            "type": "kwitansi",
            "hospital_name": "...",
            "invoice_number": "...",
            "invoice_date": "2026-03-02",
            "total_cost": 350000,
            "patient_name": "...",
            "raw_confidence": 85
        },
        "normalized": {...},
        "classification": {...},
        "confidence": 87
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing image data'
            }), 400
        
        base64_image = data['image']
        doc_type = data.get('type', 'auto')
        
        # Step 1: Get raw text from OCR
        raw_result = ocr_engine.process_base64_image(base64_image)
        
        if 'error' in raw_result and raw_result['error']:
            return jsonify({
                'success': False,
                'error': raw_result['error']
            }), 500
        
        raw_text = raw_result['text']
        raw_confidence = raw_result['confidence']
        
        # Step 2: Extract fields
        extracted = data_extractor.extract_all(raw_text, doc_type)
        extracted['raw_confidence'] = raw_confidence
        
        # Step 3: Normalize data
        normalized = normalizer.normalize_all(extracted)
        
        # Step 4: Classification (for diagnosis)
        classification = {}
        if normalized.get('diagnosis'):
            classification = classifier.classify(normalized['diagnosis'])
        
        # Calculate confidence
        confidence = DiseaseClassifier._calculate_extraction_confidence(extracted)
        final_confidence = int((raw_confidence + confidence) / 2) if raw_confidence > 0 else confidence
        
        return jsonify({
            'success': True,
            'data': extracted,
            'normalized': normalized,
            'classification': classification,
            'raw_confidence': raw_confidence,
            'extraction_confidence': confidence,
            'confidence': final_confidence
        })
    
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/ocr/check-duplicate', methods=['POST'])
def check_duplicate():
    """
    Check for potential duplicate submission
    
    Request:
    {
        "new_submission": {...},
        "existing_submissions": [...]
    }
    
    Response:
    {
        "success": true,
        "is_duplicate": false,
        "score": 45,
        "warning": null
    }
    """
    try:
        data = request.get_json()
        
        new_sub = data.get('new_submission')
        existing_subs = data.get('existing_submissions', [])
        
        if not new_sub:
            return jsonify({
                'success': False,
                'error': 'Missing new_submission'
            }), 400
        
        is_dup, score, details = duplicate_detector.calculate_similarity(new_sub, existing_subs)
        
        return jsonify({
            'success': True,
            'is_duplicate': is_dup,
            'score': score,
            'matches': details.get('matches', []),
            'warning': details.get('warning'),
            'similar_submission_ids': details.get('similar_submission_ids', []),
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🏥 Medical Document OCR Service")
    print("=" * 60)
    print(f"PaddleOCR Available: {PADDLE_AVAILABLE}")
    print(f"OCR Engine Ready: {ocr_engine.ocr is not None}")
    print("=" * 60)
    print("📡 Starting Flask server on http://0.0.0.0:5000")
    print("   - POST /ocr → Basic OCR (raw text)")
    print("   - POST /ocr/extract → Structured extraction (fields)")
    print("   - POST /ocr/check-duplicate → Duplicate detection")
    print("   - GET /health → Health check")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
