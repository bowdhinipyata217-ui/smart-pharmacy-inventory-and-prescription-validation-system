"""
AI utility functions for extracting medicine names from prescription text.
Uses OpenAI API for intelligent text parsing.
"""
import json
import re
from django.conf import settings


def extract_medicine_names_with_openai(prescription_text):
    """
    Extract medicine names from prescription text using OpenAI API.
    
    Args:
        prescription_text: Raw text extracted from prescription
        
    Returns:
        list: List of medicine names
    """
    try:
        from openai import OpenAI
        
        if not settings.OPENAI_API_KEY:
            raise Exception("OpenAI API key not configured.")
        
        # Initialize OpenAI client
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Create prompt for medicine extraction
        prompt = f"""Extract only the medicine names from the following prescription text. 
Return them as a clean JSON array of strings. Ignore doctor notes and dosage instructions.

Prescription text:
{prescription_text}

Return only a JSON array of medicine names, for example: ["Medicine1", "Medicine2", "Medicine3"]
"""
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a medical assistant that extracts medicine names from prescriptions. Return only valid JSON arrays."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # Extract response content
        content = response.choices[0].message.content.strip()
        
        # Try to parse JSON from response
        # Sometimes the response might have markdown code blocks
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*', '', content)
        content = content.strip()
        
        # Parse JSON
        try:
            medicines = json.loads(content)
            if isinstance(medicines, list):
                # Clean and normalize medicine names
                cleaned_medicines = [m.strip() for m in medicines if m.strip()]
                return cleaned_medicines
            else:
                return []
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract array manually
            # Look for array pattern in the response
            array_match = re.search(r'\[(.*?)\]', content)
            if array_match:
                # Try to extract strings from the array
                medicines = re.findall(r'"([^"]+)"', array_match.group(0))
                return [m.strip() for m in medicines if m.strip()]
            return []
            
    except ImportError:
        raise Exception("openai library is not installed. Install it using: pip install openai")
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")


def extract_medicine_names_fallback(prescription_text):
    """
    Fallback method to extract medicine names using regex patterns.
    Used when OpenAI API is not available.
    
    Args:
        prescription_text: Raw text extracted from prescription
        
    Returns:
        list: List of potential medicine names
    """
    medicines = []
    
    # Common patterns for medicine names in prescriptions
    # Look for lines that might contain medicine names
    lines = prescription_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip common prescription headers/footers
        skip_patterns = [
            'doctor', 'clinic', 'hospital', 'date', 'patient', 'age',
            'prescription', 'rx', 'diagnosis', 'advice', 'notes'
        ]
        
        if any(pattern in line.lower() for pattern in skip_patterns):
            continue
        
        # Look for capitalized words (medicine names are often capitalized)
        words = line.split()
        if len(words) >= 1:
            # Check if first word is capitalized (potential medicine name)
            if words[0] and words[0][0].isupper():
                # Remove common suffixes/prefixes
                medicine = words[0].strip('.,;:')
                if len(medicine) > 2 and medicine not in medicines:
                    medicines.append(medicine)
    
    return medicines[:10]  # Limit to 10 medicines


def extract_medicine_names(prescription_text):
    """
    Extract medicine names from prescription text.
    Tries OpenAI first, falls back to regex if unavailable.
    
    Args:
        prescription_text: Raw text extracted from prescription
        
    Returns:
        list: List of medicine names
    """
    if not prescription_text or not prescription_text.strip():
        return []
    
    # Try OpenAI first
    if settings.OPENAI_API_KEY:
        try:
            medicines = extract_medicine_names_with_openai(prescription_text)
            if medicines:
                return medicines
        except Exception:
            # Fallback to regex if OpenAI fails
            pass
    
    # Use fallback method
    return extract_medicine_names_fallback(prescription_text)
