"""
Database models for Pharmacy AI application.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """Custom User model with role-based access."""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_staff_member(self):
        return self.role == 'staff'


class Medicine(models.Model):
    """Medicine inventory model."""
    name = models.CharField(max_length=200, unique=True, db_index=True)
    composition = models.TextField(blank=True, null=True)
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medicines'
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicines'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (Stock: {self.stock_quantity})"
    
    def is_available(self):
        return self.stock_quantity > 0


class Alternative(models.Model):
    """Alternative medicine suggestions."""
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='alternatives',
        db_index=True
    )
    alternative_medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='alternative_for',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'alternatives'
        verbose_name = 'Alternative Medicine'
        verbose_name_plural = 'Alternative Medicines'
        unique_together = ['medicine', 'alternative_medicine']
    
    def __str__(self):
        return f"{self.medicine.name} -> {self.alternative_medicine.name}"


class Prescription(models.Model):
    """Prescription upload and processing model."""
    file = models.FileField(upload_to='prescriptions/%Y/%m/%d/')
    extracted_text = models.TextField(blank=True, null=True)
    results_json = models.JSONField(default=dict, blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescriptions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'prescriptions'
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prescription {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
