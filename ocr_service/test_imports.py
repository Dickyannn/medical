"""
Test script to verify all imports work correctly
"""
import sys
import importlib

packages_to_test = [
    ('flask', 'Flask'),
    ('pdf2image', 'convert_from_bytes'),
    ('PIL', 'Image'),
    ('cv2', 'cv2'),
    ('np', 'numpy'),
    ('paddleocr', 'PaddleOCR'),
]

print("=" * 60)
print("🔍 Testing Python Package Imports")
print("=" * 60)

all_ok = True

for module_name, item in packages_to_test:
    try:
        module = importlib.import_module(module_name)
        print(f"✅ {module_name:20} - OK")
    except ImportError as e:
        print(f"❌ {module_name:20} - MISSING: {e}")
        all_ok = False

print("=" * 60)

if all_ok:
    print("✅ All imports successful! Ready to run ocr_engine.py")
    sys.exit(0)
else:
    print("❌ Some packages are missing. Install with:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
