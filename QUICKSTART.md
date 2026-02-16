# Quick Start Guide

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL server installed and running
- [ ] Tesseract OCR installed
- [ ] OpenAI API key obtained

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- MySQL database credentials
- OpenAI API key
- Tesseract path (if needed)

### 3. Create MySQL Database

```sql
CREATE DATABASE pharmacy_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

### 6. (Optional) Load Sample Data

```bash
python manage.py shell < setup_sample_data.py
```

Or manually in Django shell:
```python
python manage.py shell
# Then copy-paste code from setup_sample_data.py
```

### 7. Run Development Server

```bash
python manage.py runserver
```

### 8. Access Application

- Web Interface: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API Root: http://localhost:8000/api/

## First Steps

1. **Login**: Use the admin credentials you created
2. **Add Medicines**: Go to Inventory → Add Medicine
3. **Upload Prescription**: Go to Upload Prescription and test with a sample image
4. **View Results**: Check the Results page after processing

## Testing API

### Get JWT Token

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

### Use Token in Requests

```bash
curl -X GET http://localhost:8000/api/medicines/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Troubleshooting

### MySQL Connection Error
- Check MySQL is running: `mysql -u root -p`
- Verify database exists: `SHOW DATABASES;`
- Check `.env` credentials

### Tesseract Not Found
- Windows: Install from https://github.com/UB-Mannheim/tesseract/wiki
- Set `TESSERACT_CMD` in `.env` to full path
- Linux: `sudo apt-get install tesseract-ocr`

### OpenAI API Error
- Verify API key in `.env`
- Check account has credits
- Ensure internet connection

### Static Files Not Loading
```bash
python manage.py collectstatic
```

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- Explore API endpoints at `/api/`
- Customize settings in `pharmacy_ai/settings.py`
- Add more medicines through admin panel or API
