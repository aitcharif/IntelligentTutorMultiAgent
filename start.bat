@echo off
REM Script de démarrage pour Windows

echo ╔═══════════════════════════════════════════════════╗
echo ║   Plateforme Multi-Agent - Education Marocaine   ║
echo ╚═══════════════════════════════════════════════════╝
echo.

REM Verification Python
echo Verification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe!
    pause
    exit /b 1
)
echo [OK] Python trouve
echo.

REM Verification Ollama
echo Verification d'Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVERTISSEMENT] Ollama n'est pas installe
    echo.
    echo Pour installer Ollama: https://ollama.ai/download
    echo Puis telecharger un modele: ollama pull mistral
    echo.
    set /p CONTINUE="Continuer sans Ollama? (o/N) "
    if /i not "%CONTINUE%"=="o" exit /b 1
) else (
    echo [OK] Ollama installe
    echo.
    echo Modeles disponibles:
    ollama list
)
echo.

REM Creer environnement virtuel
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
    echo [OK] Environnement virtuel cree
)

REM Activer environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer dependances
echo Installation des dependances...
pip install -q -r backend\requirements.txt
echo [OK] Dependances installees
echo.

REM Verifier configuration
if not exist ".env" (
    echo [AVERTISSEMENT] Fichier .env non trouve
    echo Creation du fichier .env...
    copy config\.env.example .env
    echo [OK] Fichier .env cree
    echo.
    echo Note: Editez .env pour utiliser un LLM cloud (OpenAI/Claude)
)
echo.

REM Creer dossier logs
if not exist "logs" mkdir logs

REM Demarrer backend
echo Demarrage du serveur backend...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

cd backend
python -m api.main

REM Le script s'arrete ici car le serveur tourne
REM Pour arreter: Ctrl+C
