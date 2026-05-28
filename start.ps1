# AQM — Start all services
# Run from project root: .\start.ps1

$root = $PSScriptRoot
$venv = "$root\.venv\Scripts\python.exe"

Write-Host "[1/4] Starting MQTT broker (Docker)..." -ForegroundColor Cyan
docker compose up -d broker

Start-Sleep -Seconds 2

Write-Host "[2/4] Starting backend (port 8000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; & '$venv' run_backend.py"

Start-Sleep -Seconds 1

Write-Host "[3/4] Starting dashboard (port 8001)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; .\.venv\Scripts\uvicorn dashboard.app:app --port 8001 --reload"

Start-Sleep -Seconds 1

Write-Host "[4/4] Starting simulator..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; & '$venv' -m simulator.sensors"

Write-Host ""
Write-Host "AQM running:" -ForegroundColor Green
Write-Host "  Dashboard  -> http://localhost:8001" -ForegroundColor Green
Write-Host "  Backend API -> http://localhost:8000/sensors" -ForegroundColor Green
Write-Host "  MQTT Broker -> localhost:1883" -ForegroundColor Green
