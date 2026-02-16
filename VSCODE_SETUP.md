# VS Code Setup Guide - Pharmacy AI Project

Complete step-by-step guide to run the Pharmacy AI project in Visual Studio Code.

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] VS Code installed
- [ ] Python 3.8+ installed
- [ ] MySQL server installed and running
- [ ] Git installed (optional)

---

## Step 1: Open Project in VS Code

1. **Open VS Code**
2. **File → Open Folder** (or `Ctrl+K Ctrl+O`)
3. Navigate to: `C:\Users\Rahul\Desktop\pharmacy_ai`
4. Click **Select Folder**

Your project should now be visible in the VS Code Explorer sidebar.

---

## Step 2: Install VS Code Extensions

Install these recommended extensions for Django development:

### Required Extensions:

1. **Python** (by Microsoft)
   - Press `Ctrl+Shift+X` to open Extensions
   - Search: `Python`
   - Click **Install**

2. **Django** (by Baptiste Darthenay)
   - Search: `Django`
   - Click **Install**

3. **Python Docstring Generator** (optional but recommended)
   - Search: `Python Docstring Generator`
   - Click **Install**

### Optional but Helpful:

- **MySQL** (by Jun Han)
- **GitLens** (for Git integration)
- **Prettier** (code formatting)
- **Error Lens** (inline error highlighting)

---

## Step 3: Configure Python Interpreter

1. **Open Command Palette**: `Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Select your Python 3.8+ interpreter
   - If not listed, click **Enter interpreter path...**
   - Browse to your Python installation (e.g., `C:\Python39\python.exe`)

**Verify Python:**
- Open VS Code terminal: `` Ctrl+` ``
- Run: `python --version`
- Should show: `Python 3.8.x` or higher

---

## Step 4: Create Virtual Environment

**In VS Code Terminal** (`` Ctrl+` ``):

```bash
# Navigate to project directory (if not already there)
cd C:\Users\Rahul\Desktop\pharmacy_ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Windows Command Prompt:
venv\Scripts\activate.bat

# Git Bash:
source venv/Scripts/activate
```

**You should see `(venv)` in your terminal prompt.**

---

## Step 5: Install Python Dependencies

**In the activated virtual environment terminal:**

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**This will install:**
- Django
- Django REST Framework
- MySQL client
- Tesseract OCR libraries
- OpenAI library
- And other dependencies

**Verify installation:**
```bash
pip list
```

You should see Django and other packages listed.

---

## Step 6: Configure Environment Variables

1. **In VS Code Explorer**, locate `.env.example`
2. **Right-click** → **Copy**
3. **Rename** the copy to `.env` (remove `.example`)
4. **Open `.env` file** and update these values:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (MySQL)
DB_NAME=pharmacy_ai
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Tesseract OCR (Windows default path)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Google Vision API (Optional)
GOOGLE_VISION_API_KEY=your-google-vision-key-here
```

**Important:** Replace placeholder values with your actual credentials!

---

## Step 7: Setup MySQL Database

### Option A: Using MySQL Command Line

1. **Open MySQL Command Line Client** or MySQL Workbench
2. **Login** with your MySQL root credentials
3. **Run these commands:**

```sql
-- Create database
CREATE DATABASE pharmacy_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify database created
SHOW DATABASES;
```

### Option B: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Click **Create Schema**
4. Name: `pharmacy_ai`
5. Collation: `utf8mb4_unicode_ci`
6. Click **Apply**

---

## Step 8: Run Database Migrations

**In VS Code Terminal** (with venv activated):

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, pharmacy_app, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying pharmacy_app.0001_initial... OK
```

---

## Step 9: Create Superuser (Admin Account)

**In VS Code Terminal:**

```bash
python manage.py createsuperuser
```

**Follow prompts:**
```
Username: admin
Email address: admin@pharmacy.com
Password: ********
Password (again): ********
Superuser created successfully.
```

---

## Step 10: (Optional) Load Sample Data

**In VS Code Terminal:**

```bash
python manage.py shell < setup_sample_data.py
```

Or manually in Django shell:
```bash
python manage.py shell
```

Then copy-paste code from `setup_sample_data.py`.

---

## Step 11: Configure VS Code Settings

Create `.vscode/settings.json` in your project root:

1. **Create folder**: `.vscode` (if it doesn't exist)
2. **Create file**: `settings.json`
3. **Add this content:**

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.analysis.autoImportCompletions": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "[python]": {
        "editor.defaultFormatter": "ms-python.python",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "files.associations": {
        "*.html": "html"
    }
}
```

---

## Step 12: Create Launch Configuration (Debugging)

Create `.vscode/launch.json`:

1. **Create file**: `.vscode/launch.json`
2. **Add this content:**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver",
                "--noreload"
            ],
            "django": true,
            "justMyCode": true,
            "env": {
                "DJANGO_SETTINGS_MODULE": "pharmacy_ai.settings"
            },
            "console": "integratedTerminal"
        }
    ]
}
```

---

## Step 13: Run the Development Server

### Method 1: Using VS Code Terminal

**In VS Code Terminal** (with venv activated):

```bash
python manage.py runserver
```

**Expected output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
February 16, 2026 - 03:00:00
Django version 4.2.x, using settings 'pharmacy_ai.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Method 2: Using VS Code Debugger

1. **Press `F5`** or click **Run → Start Debugging**
2. Select **"Python: Django"** configuration
3. Server will start automatically

---

## Step 14: Access the Application

1. **Open your web browser**
2. **Navigate to:**
   - Main Application: `http://localhost:8000`
   - Admin Panel: `http://localhost:8000/admin`
   - API Root: `http://localhost:8000/api/`

3. **Login** with your superuser credentials

---

## Step 15: Verify Everything Works

### Test Checklist:

- [ ] **Login Page** loads correctly
- [ ] **Can login** with superuser account
- [ ] **Dashboard** displays
- [ ] **Upload Prescription** page loads
- [ ] **Inventory** page accessible (admin only)
- [ ] **Admin Panel** works at `/admin`

### Test API (Optional):

**In VS Code Terminal**, open new terminal and test:

```bash
# Get JWT token
curl -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"your_password\"}"
```

---

## 🐛 Troubleshooting Common Issues

### Issue 1: Python Interpreter Not Found

**Solution:**
- `Ctrl+Shift+P` → `Python: Select Interpreter`
- Choose the correct Python version
- Or install Python from python.org

### Issue 2: Module Not Found Errors

**Solution:**
```bash
# Ensure venv is activated
# You should see (venv) in terminal

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: MySQL Connection Error

**Solution:**
1. Check MySQL is running:
   ```bash
   # Windows
   services.msc
   # Look for MySQL service
   ```

2. Verify `.env` database credentials
3. Test MySQL connection:
   ```bash
   mysql -u root -p
   ```

### Issue 4: Tesseract OCR Not Found

**Solution:**
1. Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Update `TESSERACT_CMD` in `.env`:
   ```env
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

### Issue 5: Port 8000 Already in Use

**Solution:**
```bash
# Use different port
python manage.py runserver 8001
```

### Issue 6: Static Files Not Loading

**Solution:**
```bash
python manage.py collectstatic
```

### Issue 7: Migration Errors

**Solution:**
```bash
# Delete migration files (except __init__.py)
# Then recreate:
python manage.py makemigrations
python manage.py migrate
```

---

## 🎯 VS Code Tips & Tricks

### 1. **Integrated Terminal**
- Open: `` Ctrl+` ``
- Split terminal: `` Ctrl+Shift+` ``
- New terminal: `Ctrl+Shift+5`

### 2. **Quick File Navigation**
- `Ctrl+P` - Quick open file
- `Ctrl+Shift+F` - Search in files
- `Ctrl+F` - Find in current file

### 3. **Django Template Support**
- Install "Django" extension for template syntax highlighting
- HTML files will have Django template support

### 4. **Debugging**
- Set breakpoints: Click left margin (red dot)
- `F5` - Start debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into

### 5. **Python IntelliSense**
- `Ctrl+Space` - Auto-complete
- `Ctrl+Click` - Go to definition
- `Alt+F12` - Peek definition

### 6. **Git Integration**
- `Ctrl+Shift+G` - Open Source Control
- Stage changes, commit, push directly from VS Code

---

## 📝 Recommended VS Code Workspace Settings

Create `.vscode/settings.json` with:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/venv": false
    },
    "editor.formatOnSave": true,
    "python.formatting.provider": "black"
}
```

---

## ✅ Success Checklist

You're ready when:
- [x] VS Code opens project without errors
- [x] Python interpreter selected
- [x] Virtual environment activated
- [x] Dependencies installed
- [x] `.env` file configured
- [x] MySQL database created
- [x] Migrations completed
- [x] Superuser created
- [x] Server runs without errors
- [x] Can access `http://localhost:8000`

---

## 🚀 Quick Start Commands Reference

```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

# Load sample data
python manage.py shell < setup_sample_data.py
```

---

## 📚 Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **VS Code Python Guide**: https://code.visualstudio.com/docs/python/python-tutorial
- **Django REST Framework**: https://www.django-rest-framework.org/

---

**Happy Coding! 🎉**

If you encounter any issues, check the troubleshooting section or refer to `README.md` for more details.
