# AI Fraud Detection System Startup Script
# Requires PowerShell 5.1 or higher

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Fraud Detection System Startup" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created successfully!" -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "[1/4] Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "[SUCCESS] Virtual environment activated!" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to activate virtual environment!" -ForegroundColor Red
    Write-Host "Make sure PowerShell execution policy allows running scripts." -ForegroundColor Yellow
    Write-Host "Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Check dependencies
Write-Host "[2/4] Checking dependencies..." -ForegroundColor Yellow
try {
    $flask = pip show flask 2>$null
    if (-not $flask) {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
    Write-Host "[SUCCESS] Dependencies ready!" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Start MLflow in new window
Write-Host "[3/4] Starting MLflow server..." -ForegroundColor Yellow
$mlflowScript = {
    param($Path)
    Set-Location $Path
    & .\venv\Scripts\Activate.ps1
    mlflow server --host 127.0.0.1 --port 5001
}

Start-Job -ScriptBlock $mlflowScript -ArgumentList (Get-Location) -Name "MLflowServer"
Start-Sleep -Seconds 3
Write-Host "[SUCCESS] MLflow server started!" -ForegroundColor Green
Write-Host ""

# Start Flask application
Write-Host "[4/4] Starting Flask application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting AI Fraud Detection System" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "MLflow Dashboard: http://127.0.0.1:5001" -ForegroundColor Green
Write-Host "Main Application: http://127.0.0.1:5000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    python app.py
} catch {
    Write-Host "[ERROR] Failed to start Flask application!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
} finally {
    # Cleanup
    Stop-Job -Name "MLflowServer" -ErrorAction SilentlyContinue
    Remove-Job -Name "MLflowServer" -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Application stopped. Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
