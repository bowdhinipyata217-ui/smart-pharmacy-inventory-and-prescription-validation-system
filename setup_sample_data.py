"""
Script to create sample data for Pharmacy AI application.
Run this after migrations: python manage.py shell < setup_sample_data.py
Or run: python manage.py shell
Then copy-paste the code below.
"""

from pharmacy_app.models import Medicine, Alternative, User

# Create sample medicines
medicines_data = [
    {
        'name': 'Paracetamol 500mg',
        'composition': 'Paracetamol',
        'stock_quantity': 150,
        'manufacturer': 'ABC Pharmaceuticals'
    },
    {
        'name': 'Amoxicillin 250mg',
        'composition': 'Amoxicillin',
        'stock_quantity': 80,
        'manufacturer': 'XYZ Pharma Ltd'
    },
    {
        'name': 'Ibuprofen 400mg',
        'composition': 'Ibuprofen',
        'stock_quantity': 0,
        'manufacturer': 'ABC Pharmaceuticals'
    },
    {
        'name': 'Cetirizine 10mg',
        'composition': 'Cetirizine Hydrochloride',
        'stock_quantity': 120,
        'manufacturer': 'MedCorp Industries'
    },
    {
        'name': 'Azithromycin 500mg',
        'composition': 'Azithromycin',
        'stock_quantity': 60,
        'manufacturer': 'XYZ Pharma Ltd'
    },
    {
        'name': 'Omeprazole 20mg',
        'composition': 'Omeprazole',
        'stock_quantity': 90,
        'manufacturer': 'ABC Pharmaceuticals'
    },
    {
        'name': 'Metformin 500mg',
        'composition': 'Metformin Hydrochloride',
        'stock_quantity': 200,
        'manufacturer': 'MedCorp Industries'
    },
    {
        'name': 'Amlodipine 5mg',
        'composition': 'Amlodipine Besylate',
        'stock_quantity': 5,
        'manufacturer': 'XYZ Pharma Ltd'
    },
]

print("Creating sample medicines...")
for med_data in medicines_data:
    medicine, created = Medicine.objects.get_or_create(
        name=med_data['name'],
        defaults=med_data
    )
    if created:
        print(f"Created: {medicine.name}")
    else:
        print(f"Already exists: {medicine.name}")

# Create alternative medicines
print("\nCreating alternative medicine relationships...")
try:
    paracetamol = Medicine.objects.get(name='Paracetamol 500mg')
    ibuprofen = Medicine.objects.get(name='Ibuprofen 400mg')
    
    # Ibuprofen as alternative to Paracetamol (when Paracetamol is out of stock)
    Alternative.objects.get_or_create(
        medicine=paracetamol,
        alternative_medicine=ibuprofen
    )
    print(f"Created alternative: {paracetamol.name} -> {ibuprofen.name}")
except Medicine.DoesNotExist:
    print("Some medicines not found for alternatives")

# Create sample staff user (if doesn't exist)
print("\nCreating sample users...")
try:
    staff_user, created = User.objects.get_or_create(
        username='staff1',
        defaults={
            'email': 'staff1@pharmacy.com',
            'role': 'staff'
        }
    )
    if created:
        staff_user.set_password('staff123')
        staff_user.save()
        print(f"Created staff user: {staff_user.username}")
    else:
        print(f"Staff user already exists: {staff_user.username}")
except Exception as e:
    print(f"Error creating staff user: {e}")

print("\nSample data setup completed!")
print("\nDefault admin user should be created using: python manage.py createsuperuser")
