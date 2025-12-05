# Script pour lancer le serveur API Agent S3

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  AGENT S3 API SERVER" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Vérifier que nous sommes dans le bon environnement
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
    & "..\.venv312\Scripts\Activate.ps1"
}

# Vérifier le fichier .env
if (-not (Test-Path "../.env")) {
    Write-Host "Erreur: Fichier .env introuvable!" -ForegroundColor Red
    Write-Host "Assurez-vous que le fichier .env existe dans le dossier parent" -ForegroundColor Yellow
    exit 1
}

Write-Host "Configuration chargee depuis .env" -ForegroundColor Green
Write-Host "`nDemarrage du serveur API sur http://localhost:8000..." -ForegroundColor Yellow
Write-Host "WebSocket disponible sur ws://localhost:8000/ws/agent`n" -ForegroundColor Cyan

# Lancer le serveur avec uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info
