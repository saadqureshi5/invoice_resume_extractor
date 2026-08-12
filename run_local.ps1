# run_local.ps1
Write-Host "Setting up Python Virtual Environment..." -ForegroundColor Green
if (-Not (Test-Path "venv")) {
    python -m venv venv
}

Write-Host "Activating Virtual Environment and Installing Dependencies..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
pip install -r frontend\requirements.txt

Write-Host "Starting FastAPI Backend in a new window..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\Activate.ps1; uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

Write-Host "Starting Streamlit Frontend..." -ForegroundColor Green
$env:API_URL="http://localhost:8000"
streamlit run frontend\app.py
