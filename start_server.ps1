# Script de démarrage du serveur backend
# Usage: .\start_server.ps1

Write-Host "=========================================" -ForegroundColor Blue
Write-Host "Système Multi-Agent - Démarrage" -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue

# Vérifier que Python est installé
Write-Host "`n1. Vérification de Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Python installé: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ✗ Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host "   Téléchargez Python depuis: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Vérifier que l'environnement virtuel existe
Write-Host "`n2. Vérification de l'environnement virtuel..." -ForegroundColor Yellow
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "   ✓ Environnement virtuel trouvé" -ForegroundColor Green
} else {
    Write-Host "   ✗ Environnement virtuel non trouvé" -ForegroundColor Red
    Write-Host "   Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Environnement virtuel créé" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Erreur lors de la création de l'environnement virtuel" -ForegroundColor Red
        exit 1
    }
}

# Activer l'environnement virtuel
Write-Host "`n3. Activation de l'environnement virtuel..." -ForegroundColor Yellow
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "   ✓ Environnement virtuel activé" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Erreur d'activation. Essayez:" -ForegroundColor Red
    Write-Host "   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# Vérifier les dépendances
Write-Host "`n4. Vérification des dépendances..." -ForegroundColor Yellow
$fastapi = pip show fastapi 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Dépendances installées" -ForegroundColor Green
} else {
    Write-Host "   ✗ Dépendances manquantes" -ForegroundColor Red
    Write-Host "   Installation des dépendances..." -ForegroundColor Yellow
    pip install -r backend/requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Dépendances installées avec succès" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Erreur lors de l'installation des dépendances" -ForegroundColor Red
        exit 1
    }
}

# Vérifier Ollama (optionnel)
Write-Host "`n5. Vérification d'Ollama..." -ForegroundColor Yellow
try {
    $ollamaTest = curl -s http://localhost:11434/api/tags 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Ollama est accessible sur le port 11434" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Ollama n'est pas accessible" -ForegroundColor Yellow
        Write-Host "   Le système fonctionnera en mode dégradé" -ForegroundColor Yellow
        Write-Host "   Pour installer Ollama: https://ollama.ai/download" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ⚠ Impossible de vérifier Ollama" -ForegroundColor Yellow
}

# Définir PYTHONPATH
Write-Host "`n6. Configuration de PYTHONPATH..." -ForegroundColor Yellow
$env:PYTHONPATH = $PWD.Path
Write-Host "   ✓ PYTHONPATH = $env:PYTHONPATH" -ForegroundColor Green

# Démarrer le serveur
Write-Host "`n7. Démarrage du serveur..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Blue
Write-Host "Le serveur va démarrer sur http://localhost:8000" -ForegroundColor Cyan
Write-Host "Documentation API: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Blue
Write-Host ""

python -m backend.api.main
