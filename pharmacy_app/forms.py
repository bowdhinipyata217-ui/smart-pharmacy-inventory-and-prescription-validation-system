"""
Forms for Pharmacy AI application.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Medicine, Alternative, Prescription
import os


class PrescriptionUploadForm(forms.ModelForm):
    """Form for uploading prescription files."""
    
    class Meta:
        model = Prescription
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise ValidationError("Please select a file to upload.")
        
        # Check file extension
        ext = os.path.splitext(file.name)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
        if ext not in allowed_extensions:
            raise ValidationError(
                f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Check file size (10MB max)
        if file.size > 10 * 1024 * 1024:
            raise ValidationError("File size exceeds 10MB limit.")
        
        return file


class MedicineForm(forms.ModelForm):
    """Form for adding/editing medicines."""
    
    class Meta:
        model = Medicine
        fields = ['name', 'composition', 'stock_quantity', 'manufacturer']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Medicine Name'
            }),
            'composition': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Active ingredients and composition'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'manufacturer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Manufacturer Name'
            }),
        }


class AlternativeForm(forms.ModelForm):
    """Form for adding alternative medicines."""
    
    class Meta:
        model = Alternative
        fields = ['medicine', 'alternative_medicine']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'alternative_medicine': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        medicine = cleaned_data.get('medicine')
        alternative_medicine = cleaned_data.get('alternative_medicine')
        
        if medicine and alternative_medicine:
            if medicine == alternative_medicine:
                raise ValidationError("A medicine cannot be an alternative to itself.")
        
        return cleaned_data
