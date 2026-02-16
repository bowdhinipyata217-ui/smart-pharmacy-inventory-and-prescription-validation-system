"""
OCR utility functions for extracting text from prescription images.
Supports Tesseract OCR and Google Vision API.
"""
import os
import io
from PIL import Image
from django.conf import settings


def extract_text_with_tesseract(image_path):
    """
    Extract text from image using Tesseract OCR.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Extracted text
    """
    try:
        import pytesseract
        
        # Set Tesseract command path if configured
        if hasattr(settings, 'TESSERACT_CMD') and settings.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        
        # Open and process image
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='eng')
        
        return text.strip()
    except ImportError:
        raise Exception("pytesseract is not installed. Install it using: pip install pytesseract")
    except Exception as e:
        raise Exception(f"Tesseract OCR error: {str(e)}")


def extract_text_with_google_vision(image_path):
    """
    Extract text from image using Google Vision API.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Extracted text
    """
    try:
        from google.cloud import vision
        
        if not settings.GOOGLE_VISION_API_KEY:
            raise Exception("Google Vision API key not configured.")
        
        # Initialize client
        client = vision.ImageAnnotatorClient()
        
        # Read image file
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        
        # Perform text detection
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            return texts[0].description.strip()
        else:
            return ""
    except ImportError:
        raise Exception("google-cloud-vision is not installed. Install it using: pip install google-cloud-vision")
    except Exception as e:
        raise Exception(f"Google Vision API error: {str(e)}")


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        str: Extracted text
    """
    try:
        import PyPDF2
        
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        return text.strip()
    except ImportError:
        raise Exception("PyPDF2 is not installed. Install it using: pip install PyPDF2")
    except Exception as e:
        raise Exception(f"PDF extraction error: {str(e)}")


def perform_ocr(file_path):
    """
    Perform OCR on a file (image or PDF).
    Automatically detects file type and uses appropriate method.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: Extracted text
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Handle PDF files
    if file_ext == '.pdf':
        return extract_text_from_pdf(file_path)
    
    # Handle image files - try Google Vision first, fallback to Tesseract
    if file_ext in ['.jpg', '.jpeg', '.png']:
        # Try Google Vision if API key is configured
        if settings.GOOGLE_VISION_API_KEY:
            try:
                return extract_text_with_google_vision(file_path)
            except Exception:
                # Fallback to Tesseract
                pass
        
        # Use Tesseract OCR
        return extract_text_with_tesseract(file_path)
    
    raise Exception(f"Unsupported file type: {file_ext}")
