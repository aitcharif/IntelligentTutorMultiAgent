@echo off
REM Script de test rapide pour Windows
REM Usage: quick_test.bat

echo ======================================
echo Test Rapide - IntelligentTutorMultiAgent
echo ======================================
echo.

REM Vérifier Python
echo 1. Verification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH!
    exit /b 1
)
python --version
echo.

REM Vérifier pip
echo 2. Verification de pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip n'est pas installe!
    exit /b 1
)
echo pip trouve
echo.

REM Option: créer environnement virtuel
set /p VENV="Creer un environnement virtuel? (o/n) "
if /i "%VENV%"=="o" (
    echo 3. Creation de l'environnement virtuel...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo    Environnement virtuel active
) else (
    echo 3. Utilisation de l'environnement Python global
)
echo.

REM Installer les dépendances
set /p INSTALL="Installer les dependances? (o/n) "
if /i "%INSTALL%"=="o" (
    echo 4. Installation des dependances...
    pip install -r requirements.txt
    echo    Dependances installees
) else (
    echo 4. Installation des dependances ignoree
)
echo.

REM Vérifier la clé API
echo 5. Verification de la cle API...
if exist ".env" (
    echo    Fichier .env trouve
) else (
    echo    Fichier .env non trouve
    set /p CREATEENV="Creer .env depuis l'exemple? (o/n) "
    if /i "%CREATEENV%"=="o" (
        copy config\.env.example .env
        echo    .env cree - N'oubliez pas d'ajouter votre cle API!
        echo    Editez .env et ajoutez: OPENAI_API_KEY=sk-xxxxx
    )
)
echo.

REM Test d'installation
echo 6. Test d'installation...
python test_installation.py
echo.

REM Test simple
echo 7. Test simple (sans LLM)...
python examples\simple_test.py
echo.

REM Proposer le test complet
if exist ".env" (
    set /p FULLTEST="Executer le test avec LLM? (necessite cle API) (o/n) "
    if /i "%FULLTEST%"=="o" (
        echo 8. Test complet avec LLM...
        python examples\basic_usage.py
    )
)

echo.
echo ======================================
echo Tests termines!
echo ======================================
echo.
echo Prochaines etapes:
echo   - Voir docs\TESTING_LOCAL.md pour plus d'informations
echo   - Lancer l'API: python examples\rest_api.py
echo   - Consulter README.md pour l'utilisation

pause
