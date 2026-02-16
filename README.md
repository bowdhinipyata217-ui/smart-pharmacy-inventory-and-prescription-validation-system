# 💊 Pharmacy AI Management System

A full-stack AI-powered pharmacy management web application built with Django (Python) backend and HTML/CSS/JavaScript frontend. This system uses OCR and AI to extract medicine names from prescription images and automatically check inventory availability.

## 🎯 Features

- **Prescription Processing**: Upload prescription images/PDFs and extract medicine names using OCR and AI
- **AI-Powered Medicine Extraction**: Uses OpenAI API to intelligently extract medicine names from prescription text
- **Inventory Management**: Complete medicine inventory system with stock tracking
- **Alternative Medicine Suggestions**: Automatically suggests alternatives when medicines are out of stock
- **Role-Based Access Control**: Admin and Staff roles with JWT authentication
- **RESTful API**: Complete REST API for all operations
- **Modern UI**: Professional green & white themed interface
- **Prescription History**: Track all processed prescriptions
- **Manual Medicine Search**: Search medicines by name, composition, or manufacturer

## 🛠️ Tech Stack

### Backend
- **Django 4.2+**: Web framework
- **Django REST Framework**: REST API
- **MySQL**: Database
- **JWT Authentication**: Secure token-based authentication
- **Tesseract OCR**: Text extraction from images
- **OpenAI API**: AI-powered medicine name extraction
- **Google Vision API** (Optional): Alternative OCR solution

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling (Green & White theme)
- **JavaScript**: Client-side interactions
- **Responsive Design**: Mobile-friendly interface

## 📋 Prerequisites

- Python 3.8+
- MySQL 5.7+ or MySQL 8.0+
- Tesseract OCR installed on your system
- OpenAI API key (for AI features)
- Google Vision API key (optional, for enhanced OCR)

### Installing Tesseract OCR

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location: `C:\Program Files\Tesseract-OCR\`
3. Add to PATH or configure `TESSERACT_CMD` in `.env`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pharmacy_ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update with your configuration:

```bash
cp .env.example .env
```

Edit `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=pharmacy_ai
DB_USER=root
DB_PASSWORD=your-mysql-password
OPENAI_API_KEY=your-openai-api-key
```

### 5. Setup MySQL Database

```sql
CREATE DATABASE pharmacy_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow prompts to create admin account.

### 8. Load Sample Data (Optional)

You can create sample medicines through the admin panel or use Django shell:

```bash
python manage.py shell
```

```python
from pharmacy_app.models import Medicine, User

# Create sample medicines
Medicine.objects.create(name="Paracetamol 500mg", composition="Paracetamol", stock_quantity=100, manufacturer="ABC Pharma")
Medicine.objects.create(name="Amoxicillin 250mg", composition="Amoxicillin", stock_quantity=50, manufacturer="XYZ Pharma")
Medicine.objects.create(name="Ibuprofen 400mg", composition="Ibuprofen", stock_quantity=0, manufacturer="ABC Pharma")

# Create staff user
User.objects.create_user(username="staff1", password="staff123", role="staff")
```

## 🏃 Running the Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000`

## 📚 API Endpoints

### Authentication

- `POST /api/token/` - Obtain JWT access token
  ```json
  {
    "username": "admin",
    "password": "password"
  }
  ```

- `POST /api/token/refresh/` - Refresh access token
  ```json
  {
    "refresh": "refresh_token_here"
  }
  ```

- `POST /api/register/` - Register new user (Admin only)
  ```json
  {
    "username": "newuser",
    "password": "password123",
    "email": "user@example.com",
    "role": "staff"
  }
  ```

### Prescriptions

- `POST /api/prescriptions/upload/` - Upload prescription
  - Content-Type: `multipart/form-data`
  - Body: `file` (image/PDF)
  - Returns: Prescription ID and processing results

- `GET /api/prescriptions/history/` - Get prescription history
  - Requires: JWT Authentication
  - Returns: List of user's prescriptions

### Medicines

- `GET /api/medicines/` - List all medicines
  - Requires: Admin role
  - Query params: None

- `POST /api/medicines/` - Create new medicine
  - Requires: Admin role
  ```json
  {
    "name": "Medicine Name",
    "composition": "Active ingredients",
    "stock_quantity": 100,
    "manufacturer": "Manufacturer Name"
  }
  ```

- `GET /api/medicines/{id}/` - Get medicine details
  - Requires: Admin role

- `PUT /api/medicines/{id}/` - Update medicine
  - Requires: Admin role
  ```json
  {
    "name": "Updated Name",
    "stock_quantity": 150
  }
  ```

- `DELETE /api/medicines/{id}/` - Delete medicine
  - Requires: Admin role

- `GET /api/medicines/search/?q=query` - Search medicines
  - Requires: Authentication
  - Query params: `q` (search term)

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in requests:

```http
Authorization: Bearer <access_token>
```

### Example API Request

```bash
# Login and get token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Use token for authenticated requests
curl -X GET http://localhost:8000/api/medicines/ \
  -H "Authorization: Bearer <access_token>"
```

## 📁 Project Structure

```
pharmacy_ai/
│
├── pharmacy_ai/              # Django project settings
│   ├── settings.py           # Main settings file
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── pharmacy_app/             # Main application
│   ├── models.py             # Database models
│   ├── views.py              # Views and API endpoints
│   ├── urls.py               # App URL configuration
│   ├── forms.py              # Django forms
│   ├── admin.py              # Admin configuration
│   ├── ai_utils.py           # AI integration functions
│   ├── ocr_utils.py          # OCR functions
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── upload_prescription.html
│   │   ├── results.html
│   │   ├── inventory.html
│   │   └── admin_dashboard.html
│   └── static/               # Static files
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
│
├── media/                    # Uploaded files
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🗄️ Database Models

### User
- Custom user model with role-based access (Admin/Staff)
- Fields: username, email, password, role, phone

### Medicine
- Medicine inventory
- Fields: name, composition, stock_quantity, manufacturer

### Alternative
- Alternative medicine suggestions
- Fields: medicine, alternative_medicine

### Prescription
- Prescription uploads and processing results
- Fields: file, extracted_text, results_json, uploaded_by

## 🔄 Workflow

1. **Upload Prescription**: User uploads prescription image/PDF
2. **OCR Processing**: System extracts text using Tesseract OCR or Google Vision
3. **AI Extraction**: OpenAI API extracts medicine names from text
4. **Inventory Check**: System checks each medicine against database
5. **Results Display**: Shows availability status and suggests alternatives if needed

## 🎨 UI Pages

- **Login**: Admin/Staff authentication
- **Dashboard**: Main dashboard with recent prescriptions
- **Upload Prescription**: Upload and process prescriptions
- **Results**: Display processing results with medicine availability
- **Inventory**: Manage medicine inventory (Admin only)
- **Admin Dashboard**: Overview of pharmacy operations (Admin only)

## 🧪 Testing

```bash
# Run Django tests
python manage.py test

# Run specific app tests
python manage.py test pharmacy_app
```

## 🔒 Security Features

- JWT token-based authentication
- Role-based access control
- CSRF protection
- File upload validation
- SQL injection protection (Django ORM)
- XSS protection (Django templates)

## 🐛 Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Check database credentials in `.env`
- Verify database exists: `CREATE DATABASE pharmacy_ai;`

### Tesseract OCR Error
- Verify Tesseract is installed: `tesseract --version`
- Check `TESSERACT_CMD` path in `.env`
- On Windows, ensure path uses backslashes: `C:\Program Files\Tesseract-OCR\tesseract.exe`

### OpenAI API Error
- Verify API key is correct in `.env`
- Check API quota/credits
- Ensure internet connection is available

### File Upload Issues
- Check file size (max 10MB)
- Verify file format (jpg, jpeg, png, pdf)
- Ensure `media/` directory has write permissions

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions, please open an issue on the repository.

## 🎯 Future Enhancements

- [ ] Real-time prescription processing with WebSockets
- [ ] Email notifications for low stock
- [ ] Barcode scanning for medicines
- [ ] Prescription PDF generation
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Batch prescription processing
- [ ] Integration with pharmacy suppliers

## 📸 Screenshots

*Screenshots will be added here*

- Login Page
- Dashboard
- Upload Prescription
- Results Page
- Inventory Management
- Admin Dashboard

---

**Built with ❤️ using Django and AI**
