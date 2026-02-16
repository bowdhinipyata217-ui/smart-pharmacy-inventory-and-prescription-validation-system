# Pharmacy AI - PowerShell Quick Start Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Pharmacy AI - Quick Start Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created!" -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Check if dependencies are installed
try {
    python -c "import django" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
        Write-Host "Dependencies installed!" -ForegroundColor Green
        Write-Host ""
    }
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "Dependencies installed!" -ForegroundColor Green
    Write-Host ""
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "IMPORTANT: Please edit .env file with your configuration!" -ForegroundColor Red
    Write-Host "Press any key to continue after editing .env..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    Write-Host ""
}

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py migrate
Write-Host ""

# Start Django server
Write-Host "Starting Django development server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver
