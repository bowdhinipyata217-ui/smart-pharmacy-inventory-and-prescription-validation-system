"""
Views for Pharmacy AI application.
Includes both API endpoints and template-based views.
"""
import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Medicine, Alternative, Prescription
from .forms import PrescriptionUploadForm, MedicineForm, AlternativeForm
from .ocr_utils import perform_ocr
from .ai_utils import extract_medicine_names


# ==================== Authentication Views ====================

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view with role information."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            response.data['role'] = user.role
            response.data['user_id'] = user.id
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user (API endpoint)."""
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role', 'staff')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        role=role
    )
    
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'message': 'User created successfully',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'role': user.role,
        'user_id': user.id
    }, status=status.HTTP_201_CREATED)


# ==================== Template Views ====================

def register_view(request):
    """User registration page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role', 'staff')
        
        if not username or not password:
            return render(request, 'register.html', {
                'error': 'Username and password are required'
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            role=role
        )
        
        login(request, user)
        return redirect('dashboard')
    
    return render(request, 'register.html')


def login_view(request):
    """Login page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })
    
    return render(request, 'login.html')


@login_required
def dashboard_view(request):
    """Main dashboard."""
    user = request.user
    recent_prescriptions = Prescription.objects.filter(
        uploaded_by=user
    ).order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'recent_prescriptions': recent_prescriptions,
    }
    return render(request, 'dashboard.html', context)


@login_required
def upload_prescription_view(request):
    """Upload prescription page."""
    if request.method == 'POST':
        form = PrescriptionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.uploaded_by = request.user
            prescription.save()
            
            # Process prescription asynchronously (in production, use Celery)
            try:
                # Perform OCR
                file_path = prescription.file.path
                extracted_text = perform_ocr(file_path)
                prescription.extracted_text = extracted_text
                
                # Extract medicine names using AI
                medicine_names = extract_medicine_names(extracted_text)
                
                # Check inventory and prepare results
                results = []
                for med_name in medicine_names:
                    # Search for medicine (case-insensitive, partial match)
                    medicines = Medicine.objects.filter(
                        Q(name__icontains=med_name) | Q(name__iexact=med_name)
                    )
                    
                    if medicines.exists():
                        medicine = medicines.first()
                        if medicine.stock_quantity > 0:
                            # Available
                            alternative = None
                            # Check for alternatives if needed
                            alternatives = Alternative.objects.filter(
                                medicine=medicine
                            ).select_related('alternative_medicine')
                            
                            if alternatives.exists():
                                alt_med = alternatives.first().alternative_medicine
                                if alt_med.stock_quantity > 0:
                                    alternative = alt_med.name
                            
                            results.append({
                                'medicine_name': medicine.name,
                                'status': 'Available',
                                'stock': medicine.stock_quantity,
                                'alternative': alternative
                            })
                        else:
                            # Out of stock - suggest alternative
                            alternative = None
                            alternatives = Alternative.objects.filter(
                                medicine=medicine
                            ).select_related('alternative_medicine')
                            
                            if alternatives.exists():
                                alt_med = alternatives.first().alternative_medicine
                                if alt_med.stock_quantity > 0:
                                    alternative = alt_med.name
                            
                            results.append({
                                'medicine_name': medicine.name,
                                'status': 'Out of Stock',
                                'stock': 0,
                                'alternative': alternative
                            })
                    else:
                        # Medicine not found
                        results.append({
                            'medicine_name': med_name,
                            'status': 'Not Found',
                            'stock': None,
                            'alternative': None
                        })
                
                prescription.results_json = results
                prescription.save()
                
                return redirect('results', prescription_id=prescription.id)
            except Exception as e:
                return render(request, 'upload_prescription.html', {
                    'form': form,
                    'error': f'Error processing prescription: {str(e)}'
                })
    else:
        form = PrescriptionUploadForm()
    
    return render(request, 'upload_prescription.html', {'form': form})


@login_required
def results_view(request, prescription_id):
    """Display prescription processing results."""
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    # Ensure user can only view their own prescriptions (unless admin)
    if not request.user.is_admin() and prescription.uploaded_by != request.user:
        return HttpResponse('Unauthorized', status=403)
    
    results = prescription.results_json if prescription.results_json else []
    
    context = {
        'prescription': prescription,
        'results': results,
    }
    return render(request, 'results.html', context)


@login_required
def inventory_view(request):
    """Medicine inventory management page."""
    if not request.user.is_admin():
        return HttpResponse('Unauthorized - Admin access required', status=403)
    
    medicines = Medicine.objects.all().order_by('name')
    search_query = request.GET.get('search', '')
    
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(composition__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )
    
    
    low_stock_count = medicines.filter(stock_quantity__lt=10).count()

    context = {
        'medicines': medicines,
        'search_query': search_query,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'inventory.html', context)


@login_required
def admin_dashboard_view(request):
    """Admin dashboard."""
    if not request.user.is_admin():
        return HttpResponse('Unauthorized - Admin access required', status=403)
    
    total_medicines = Medicine.objects.count()
    low_stock_medicines = Medicine.objects.filter(stock_quantity__lt=10).count()
    total_prescriptions = Prescription.objects.count()
    recent_prescriptions = Prescription.objects.order_by('-created_at')[:10]
    
    context = {
        'total_medicines': total_medicines,
        'low_stock_medicines': low_stock_medicines,
        'total_prescriptions': total_prescriptions,
        'recent_prescriptions': recent_prescriptions,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def manage_alternatives_view(request):
    """Manage alternative medicines."""
    if not request.user.is_admin():
        return HttpResponse('Unauthorized - Admin access required', status=403)
    
    if request.method == 'POST':
        medicine_id = request.POST.get('medicine')
        alternative_id = request.POST.get('alternative_medicine')
        
        if medicine_id and alternative_id:
            if medicine_id == alternative_id:
                pass # Handle same medicine error if needed
            else:
                Alternative.objects.get_or_create(
                    medicine_id=medicine_id,
                    alternative_medicine_id=alternative_id
                )
        return redirect('manage_alternatives')
    
    alternatives = Alternative.objects.select_related('medicine', 'alternative_medicine').all()
    medicines = Medicine.objects.all().order_by('name')
    
    return render(request, 'manage_alternatives.html', {
        'alternatives': alternatives,
        'medicines': medicines
    })


@login_required
def delete_alternative_view(request, alternative_id):
    """Delete an alternative medicine suggestion."""
    if not request.user.is_admin():
         return HttpResponse('Unauthorized - Admin access required', status=403)
         
    alternative = get_object_or_404(Alternative, id=alternative_id)
    alternative.delete()
    return redirect('manage_alternatives')


# ==================== API Views ====================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_upload_prescription(request):
    """API endpoint for uploading prescription."""
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES['file']
    
    # Validate file
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.pdf']:
        return Response(
            {'error': 'Invalid file type. Allowed: jpg, jpeg, png, pdf'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create prescription record
    prescription = Prescription.objects.create(
        file=file,
        uploaded_by=request.user
    )
    
    try:
        # Perform OCR
        file_path = prescription.file.path
        extracted_text = perform_ocr(file_path)
        prescription.extracted_text = extracted_text
        
        # Extract medicine names using AI
        medicine_names = extract_medicine_names(extracted_text)
        
        # Check inventory and prepare results
        results = []
        for med_name in medicine_names:
            medicines = Medicine.objects.filter(
                Q(name__icontains=med_name) | Q(name__iexact=med_name)
            )
            
            if medicines.exists():
                medicine = medicines.first()
                if medicine.stock_quantity > 0:
                    alternative = None
                    alternatives = Alternative.objects.filter(
                        medicine=medicine
                    ).select_related('alternative_medicine')
                    
                    if alternatives.exists():
                        alt_med = alternatives.first().alternative_medicine
                        if alt_med.stock_quantity > 0:
                            alternative = {
                                'name': alt_med.name,
                                'stock': alt_med.stock_quantity
                            }
                    
                    results.append({
                        'medicine_name': medicine.name,
                        'status': 'Available',
                        'stock': medicine.stock_quantity,
                        'alternative': alternative
                    })
                else:
                    alternative = None
                    alternatives = Alternative.objects.filter(
                        medicine=medicine
                    ).select_related('alternative_medicine')
                    
                    if alternatives.exists():
                        alt_med = alternatives.first().alternative_medicine
                        if alt_med.stock_quantity > 0:
                            alternative = {
                                'name': alt_med.name,
                                'stock': alt_med.stock_quantity
                            }
                    
                    results.append({
                        'medicine_name': medicine.name,
                        'status': 'Out of Stock',
                        'stock': 0,
                        'alternative': alternative
                    })
            else:
                results.append({
                    'medicine_name': med_name,
                    'status': 'Not Found',
                    'stock': None,
                    'alternative': None
                })
        
        prescription.results_json = results
        prescription.save()
        
        return Response({
            'prescription_id': prescription.id,
            'extracted_text': extracted_text,
            'medicines_found': medicine_names,
            'results': results
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error processing prescription: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_prescription_history(request):
    """Get prescription history for authenticated user."""
    prescriptions = Prescription.objects.filter(
        uploaded_by=request.user
    ).order_by('-created_at')
    
    data = []
    for presc in prescriptions:
        data.append({
            'id': presc.id,
            'file_url': presc.file.url if presc.file else None,
            'created_at': presc.created_at.isoformat(),
            'results_count': len(presc.results_json) if presc.results_json else 0
        })
    
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_search_medicine(request):
    """Search for medicines."""
    query = request.GET.get('q', '')
    
    if not query:
        return Response(
            {'error': 'Query parameter "q" is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    medicines = Medicine.objects.filter(
        Q(name__icontains=query) |
        Q(composition__icontains=query) |
        Q(manufacturer__icontains=query)
    )[:20]
    
    data = []
    for med in medicines:
        data.append({
            'id': med.id,
            'name': med.name,
            'composition': med.composition,
            'stock_quantity': med.stock_quantity,
            'manufacturer': med.manufacturer,
            'is_available': med.is_available()
        })
    
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_medicines(request):
    """Get all medicines or create a new one."""
    if not request.user.is_admin():
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        medicines = Medicine.objects.all().order_by('name')
        data = []
        for med in medicines:
            data.append({
                'id': med.id,
                'name': med.name,
                'composition': med.composition,
                'stock_quantity': med.stock_quantity,
                'manufacturer': med.manufacturer,
                'created_at': med.created_at.isoformat(),
            })
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        name = request.data.get('name')
        composition = request.data.get('composition', '')
        stock_quantity = request.data.get('stock_quantity')
        if stock_quantity is None:
            stock_quantity = 0
        
        manufacturer = request.data.get('manufacturer', '')
        
        if not name:
            return Response(
                {'error': 'Medicine name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        medicine = Medicine.objects.create(
            name=name,
            composition=composition,
            stock_quantity=stock_quantity,
            manufacturer=manufacturer
        )
        
        return Response({
            'id': medicine.id,
            'name': medicine.name,
            'composition': medicine.composition,
            'stock_quantity': medicine.stock_quantity,
            'manufacturer': medicine.manufacturer,
        }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_medicine_detail(request, medicine_id):
    """Get, update, or delete a specific medicine."""
    if not request.user.is_admin():
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        medicine = Medicine.objects.get(id=medicine_id)
    except Medicine.DoesNotExist:
        return Response(
            {'error': 'Medicine not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        return Response({
            'id': medicine.id,
            'name': medicine.name,
            'composition': medicine.composition,
            'stock_quantity': medicine.stock_quantity,
            'manufacturer': medicine.manufacturer,
        }, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        medicine.name = request.data.get('name', medicine.name)
        medicine.composition = request.data.get('composition', medicine.composition)
        if 'stock_quantity' in request.data:
            val = request.data.get('stock_quantity')
            medicine.stock_quantity = val if val is not None else 0

        medicine.manufacturer = request.data.get('manufacturer', medicine.manufacturer)
        medicine.save()
        
        return Response({
            'id': medicine.id,
            'name': medicine.name,
            'composition': medicine.composition,
            'stock_quantity': medicine.stock_quantity,
            'manufacturer': medicine.manufacturer,
        }, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        medicine.delete()
        return Response(
            {'message': 'Medicine deleted successfully'},
            status=status.HTTP_200_OK
        )
