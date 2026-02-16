"""
Test script to verify Pharmacy AI setup.
Run this after setup to check if everything is configured correctly.
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ai.settings')
django.setup()

from django.conf import settings
from django.db import connection
from pharmacy_app.models import User, Medicine, Alternative, Prescription

def test_database_connection():
    """Test database connection."""
    print("Testing database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_models():
    """Test if models can be accessed."""
    print("\nTesting models...")
    try:
        user_count = User.objects.count()
        medicine_count = Medicine.objects.count()
        prescription_count = Prescription.objects.count()
        alternative_count = Alternative.objects.count()
        
        print(f"✅ Models accessible:")
        print(f"   - Users: {user_count}")
        print(f"   - Medicines: {medicine_count}")
        print(f"   - Prescriptions: {prescription_count}")
        print(f"   - Alternatives: {alternative_count}")
        return True
    except Exception as e:
        print(f"❌ Model access failed: {e}")
        return False

def test_settings():
    """Test Django settings."""
    print("\nTesting settings...")
    issues = []
    
    if not settings.SECRET_KEY or settings.SECRET_KEY == 'django-insecure-change-this-in-production-12345':
        issues.append("⚠️  SECRET_KEY should be changed in production")
    else:
        print("✅ SECRET_KEY configured")
    
    if settings.DEBUG:
        print("⚠️  DEBUG is True (should be False in production)")
    else:
        print("✅ DEBUG is False")
    
    if settings.OPENAI_API_KEY:
        print("✅ OpenAI API key configured")
    else:
        issues.append("⚠️  OpenAI API key not configured")
    
    if settings.TESSERACT_CMD:
        print(f"✅ Tesseract path configured: {settings.TESSERACT_CMD}")
    else:
        issues.append("⚠️  Tesseract path not configured")
    
    if settings.MEDIA_ROOT:
        media_path = Path(settings.MEDIA_ROOT)
        if media_path.exists():
            print(f"✅ Media directory exists: {media_path}")
        else:
            issues.append(f"⚠️  Media directory does not exist: {media_path}")
    
    return len(issues) == 0

def test_imports():
    """Test if all required modules can be imported."""
    print("\nTesting imports...")
    modules = [
        'rest_framework',
        'rest_framework_simplejwt',
        'corsheaders',
        'pharmacy_app',
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed.append(module)
    
    # Test optional modules
    optional_modules = {
        'pytesseract': 'Tesseract OCR',
        'openai': 'OpenAI API',
        'PIL': 'Pillow (Image processing)',
        'PyPDF2': 'PDF processing',
    }
    
    print("\nOptional modules:")
    for module, name in optional_modules.items():
        try:
            __import__(module)
            print(f"✅ {name} ({module})")
        except ImportError:
            print(f"⚠️  {name} ({module}) not installed")
    
    return len(failed) == 0

def test_urls():
    """Test if URLs are configured."""
    print("\nTesting URL configuration...")
    try:
        from django.urls import reverse, NoReverseMatch
        
        urls_to_test = [
            'login',
            'dashboard',
            'upload_prescription',
        ]
        
        for url_name in urls_to_test:
            try:
                reverse(url_name)
                print(f"✅ URL '{url_name}' configured")
            except NoReverseMatch:
                print(f"⚠️  URL '{url_name}' not found (may be normal)")
            except Exception as e:
                print(f"❌ URL '{url_name}' failed: {e}")
        
        return True
    except Exception as e:
        print(f"❌ URL testing failed: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("Pharmacy AI - Setup Verification")
    print("="*60)
    
    results = []
    
    results.append(("Database Connection", test_database_connection()))
    results.append(("Models", test_models()))
    results.append(("Settings", test_settings()))
    results.append(("Imports", test_imports()))
    results.append(("URLs", test_urls()))
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Setup is complete.")
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")
    
    print("="*60)

if __name__ == '__main__':
    main()
