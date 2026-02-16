"""
URL configuration for pharmacy_app.
"""
from django.urls import path
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    login_view,
    register_view,
    dashboard_view,
    upload_prescription_view,
    results_view,
    inventory_view,
    admin_dashboard_view,
    manage_alternatives_view,
    delete_alternative_view,
    CustomTokenObtainPairView,
    register_user,
    api_upload_prescription,
    api_prescription_history,
    api_search_medicine,
    api_medicines,
    api_medicine_detail,
)

urlpatterns = [
    # Template-based views
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register_page'),
    path('logout/', LogoutView.as_view(next_page='register_page'), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('upload/', upload_prescription_view, name='upload_prescription'),
    path('results/<int:prescription_id>/', results_view, name='results'),
    path('inventory/', inventory_view, name='inventory'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('alternatives/', manage_alternatives_view, name='manage_alternatives'),
    path('alternatives/delete/<int:alternative_id>/', delete_alternative_view, name='delete_alternative'),
    
    # API endpoints - Authentication
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', register_user, name='register'),
    
    # API endpoints - Prescriptions
    path('api/prescriptions/upload/', api_upload_prescription, name='api_upload_prescription'),
    path('api/prescriptions/history/', api_prescription_history, name='api_prescription_history'),
    
    # API endpoints - Medicines
    path('api/medicines/', api_medicines, name='api_medicines'),
    path('api/medicines/<int:medicine_id>/', api_medicine_detail, name='api_medicine_detail'),
    path('api/medicines/search/', api_search_medicine, name='api_search_medicine'),
]
