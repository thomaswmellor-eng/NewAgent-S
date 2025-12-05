# Script de lancement d'Agent S3 avec Claude Sonnet 4.5 + Fara-7B
# Pour Windows PowerShell

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  AGENT S3 - LAUNCHER" -ForegroundColor Cyan
Write-Host "  Claude Sonnet 4.5 + Fara-7B" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Charger les variables d'environnement depuis .env
Write-Host "Chargement de la configuration..." -ForegroundColor Yellow

# Lire le fichier .env
if (Test-Path ".env") {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    Write-Host "Configuration chargee depuis .env`n" -ForegroundColor Green
} else {
    Write-Host "Fichier .env introuvable!`n" -ForegroundColor Red
    exit 1
}

# Verifier les variables requises
$required_vars = @(
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_NAME",
    "AZURE_FARA_API_KEY",
    "AZURE_FARA_ENDPOINT",
    "AZURE_FARA_NAME"
)

$missing = @()
foreach ($var in $required_vars) {
    if (-not [Environment]::GetEnvironmentVariable($var, "Process")) {
        $missing += $var
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Variables d'environnement manquantes:" -ForegroundColor Red
    foreach ($var in $missing) {
        Write-Host "   - $var" -ForegroundColor Red
    }
    Write-Host "`nVerifiez votre fichier .env`n" -ForegroundColor Yellow
    exit 1
}

# Definir les valeurs par defaut
if (-not $env:GROUNDING_WIDTH) { $env:GROUNDING_WIDTH = '1920' }
if (-not $env:GROUNDING_HEIGHT) { $env:GROUNDING_HEIGHT = '1080' }

# Afficher la configuration
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "   Claude deployment: $env:AZURE_OPENAI_NAME" -ForegroundColor White
Write-Host "   Fara deployment: $env:AZURE_FARA_NAME" -ForegroundColor White
Write-Host "   Resolution: $($env:GROUNDING_WIDTH)x$($env:GROUNDING_HEIGHT)`n" -ForegroundColor White

# Lancer Agent S3
Write-Host "Lancement d'Agent S3...`n" -ForegroundColor Green

agent_s --provider azure --model $env:AZURE_OPENAI_NAME --model_url $env:AZURE_OPENAI_ENDPOINT --model_api_key $env:AZURE_OPENAI_API_KEY --ground_provider vllm --ground_url $env:AZURE_FARA_ENDPOINT --ground_api_key $env:AZURE_FARA_API_KEY --ground_model $env:AZURE_FARA_NAME --grounding_width $env:GROUNDING_WIDTH --grounding_height $env:GROUNDING_HEIGHT --enable_reflection
