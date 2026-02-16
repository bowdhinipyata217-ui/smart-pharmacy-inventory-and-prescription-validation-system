#!/usr/bin/env python
"""
Setup script for Pharmacy AI application.
This script helps automate the initial setup process.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(step_num, message):
    """Print a formatted step message."""
    print(f"\n{'='*60}")
    print(f"Step {step_num}: {message}")
    print('='*60)

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_mysql():
    """Check if MySQL is available."""
    try:
        result = subprocess.run(['mysql', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✅ MySQL detected: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("⚠️  MySQL not found in PATH. Please ensure MySQL is installed.")
        return False
    except Exception as e:
        print(f"⚠️  Could not check MySQL: {e}")
        return False

def check_tesseract():
    """Check if Tesseract OCR is installed."""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ Tesseract OCR detected: {version_line}")
            return True
    except FileNotFoundError:
        print("⚠️  Tesseract OCR not found in PATH.")
        print("   Please install Tesseract OCR:")
        print("   Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   Linux: sudo apt-get install tesseract-ocr")
        print("   macOS: brew install tesseract")
        return False
    except Exception as e:
        print(f"⚠️  Could not check Tesseract: {e}")
        return False

def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from .env.example")
        print("⚠️  Please edit .env file with your configuration!")
        return True
    else:
        print("❌ .env.example not found!")
        return False

def create_directories():
    """Create necessary directories."""
    directories = ['media', 'media/prescriptions', 'staticfiles']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Created necessary directories")

def install_dependencies():
    """Install Python dependencies."""
    print("\nInstalling Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_migrations():
    """Run Django migrations."""
    print("\nRunning migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Migrations completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        print("   Make sure MySQL database is created and configured in .env")
        return False

def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("Pharmacy AI - Setup Script")
    print("="*60)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Step 1: Check Python version
    print_step(1, "Checking Python Version")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check MySQL
    print_step(2, "Checking MySQL")
    mysql_available = check_mysql()
    if not mysql_available:
        print("⚠️  Continue anyway? MySQL is required for the application to work.")
    
    # Step 3: Check Tesseract OCR
    print_step(3, "Checking Tesseract OCR")
    tesseract_available = check_tesseract()
    if not tesseract_available:
        print("⚠️  Continue anyway? Tesseract is required for OCR functionality.")
    
    # Step 4: Create .env file
    print_step(4, "Setting up Environment File")
    create_env_file()
    
    # Step 5: Create directories
    print_step(5, "Creating Directories")
    create_directories()
    
    # Step 6: Install dependencies
    print_step(6, "Installing Dependencies")
    install_choice = input("Install Python dependencies? (y/n): ").lower()
    if install_choice == 'y':
        if not install_dependencies():
            print("⚠️  Dependencies installation failed. Please install manually:")
            print("   pip install -r requirements.txt")
    
    # Step 7: Run migrations
    print_step(7, "Running Database Migrations")
    migrate_choice = input("Run database migrations? (y/n): ").lower()
    if migrate_choice == 'y':
        if not run_migrations():
            print("⚠️  Migrations failed. Please ensure:")
            print("   1. MySQL database is created")
            print("   2. Database credentials are correct in .env")
            print("   3. Run manually: python manage.py migrate")
    
    # Final instructions
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit .env file with your configuration:")
    print("   - MySQL database credentials")
    print("   - OpenAI API key")
    print("   - Tesseract path (if needed)")
    print("\n2. Create MySQL database:")
    print("   CREATE DATABASE pharmacy_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("\n3. Run migrations (if not done):")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    print("\n4. Create superuser:")
    print("   python manage.py createsuperuser")
    print("\n5. (Optional) Load sample data:")
    print("   python manage.py shell < setup_sample_data.py")
    print("\n6. Run development server:")
    print("   python manage.py runserver")
    print("\n7. Access application:")
    print("   http://localhost:8000")
    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
