<#
.SYNOPSIS
    Launch script for Global AI & AGI News Intelligence Platform.
.DESCRIPTION
    Starts the FastAPI backend which serves both the REST API and the bundled React SPA on http://127.0.0.1:8000.
#>

$root = $PSScriptRoot
$pythonVenv = "$root\backend\.venv\Scripts\python.exe"

if (-not (Test-Path $pythonVenv)) {
    Write-Host "[!] Python venv not found at $pythonVenv. Please install Python dependencies." -ForegroundColor Red
    exit 1
}

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "       GLOBAL AI & AGI NEWS INTELLIGENCE PLATFORM                    " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "[+] Starting server at http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "[+] REST API & Swagger UI: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "[+] Background Scheduler: Active (6h ingestion & daily briefings)" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the platform." -ForegroundColor Gray
Write-Host ""

& $pythonVenv -m uvicorn app.main:app --app-dir "$root\backend" --host 127.0.0.1 --port 8000 --reload
