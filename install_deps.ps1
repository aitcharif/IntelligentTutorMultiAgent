# Script d'installation des dépendances
# Usage: .\install_deps.ps1

Write-Host "=========================================" -ForegroundColor Blue
Write-Host "Installation des Dépendances" -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue

# Vérifier Python
Write-Host "`n1. Vérification de Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ✗ Python non trouvé" -ForegroundColor Red
    exit 1
}

# Créer l'environnement virtuel s'il n'existe pas
Write-Host "`n2. Configuration de l'environnement virtuel..." -ForegroundColor Yellow
if (Test-Path ".\venv") {
    Write-Host "   ✓ Environnement virtuel existe déjà" -ForegroundColor Green
} else {
    Write-Host "   Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "   ✓ Environnement virtuel créé" -ForegroundColor Green
}

# Activer l'environnement virtuel
Write-Host "`n3. Activation de l'environnement virtuel..." -ForegroundColor Yellow
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "   ✓ Activé" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Erreur. Exécutez:" -ForegroundColor Red
    Write-Host "   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# Mettre à jour pip
Write-Host "`n4. Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "   ✓ pip mis à jour" -ForegroundColor Green

# Installer les dépendances
Write-Host "`n5. Installation des dépendances..." -ForegroundColor Yellow
Write-Host "   (Cela peut prendre 2-5 minutes)" -ForegroundColor Cyan

$startTime = Get-Date
pip install -r backend/requirements.txt

if ($LASTEXITCODE -eq 0) {
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    Write-Host "   ✓ Dépendances installées en $([math]::Round($duration, 1)) secondes" -ForegroundColor Green
} else {
    Write-Host "   ✗ Erreur lors de l'installation" -ForegroundColor Red
    exit 1
}

# Vérifier les packages principaux
Write-Host "`n6. Vérification des packages..." -ForegroundColor Yellow
$packages = @("fastapi", "uvicorn", "openai", "anthropic", "loguru")
$allInstalled = $true

foreach ($package in $packages) {
    $check = pip show $package 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ $package" -ForegroundColor Green
    } else {
        Write-Host "   ✗ $package manquant" -ForegroundColor Red
        $allInstalled = $false
    }
}

Write-Host "`n=========================================" -ForegroundColor Blue
if ($allInstalled) {
    Write-Host "✓ Installation réussie!" -ForegroundColor Green
    Write-Host "`nPour démarrer le serveur, exécutez:" -ForegroundColor Cyan
    Write-Host "   .\start_server.ps1" -ForegroundColor White
} else {
    Write-Host "⚠ Installation incomplète" -ForegroundColor Yellow
    Write-Host "Réessayez ou installez manuellement les packages manquants" -ForegroundColor Yellow
}
Write-Host "=========================================" -ForegroundColor Blue
