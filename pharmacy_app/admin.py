"""
Admin configuration for Pharmacy AI application.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Medicine, Alternative, Prescription


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone')}),
    )


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """Admin interface for Medicine model."""
    list_display = ['name', 'manufacturer', 'stock_quantity', 'is_available', 'created_at']
    list_filter = ['manufacturer', 'created_at']
    search_fields = ['name', 'composition', 'manufacturer']
    readonly_fields = ['created_at', 'updated_at']
    
    def is_available(self, obj):
        return obj.is_available()
    is_available.boolean = True
    is_available.short_description = 'Available'


@admin.register(Alternative)
class AlternativeAdmin(admin.ModelAdmin):
    """Admin interface for Alternative model."""
    list_display = ['medicine', 'alternative_medicine', 'created_at']
    list_filter = ['created_at']
    search_fields = ['medicine__name', 'alternative_medicine__name']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    """Admin interface for Prescription model."""
    list_display = ['id', 'uploaded_by', 'created_at', 'has_results']
    list_filter = ['created_at', 'uploaded_by']
    search_fields = ['extracted_text', 'uploaded_by__username']
    readonly_fields = ['created_at', 'updated_at', 'extracted_text', 'results_json']
    
    def has_results(self, obj):
        return bool(obj.results_json)
    has_results.boolean = True
    has_results.short_description = 'Has Results'
