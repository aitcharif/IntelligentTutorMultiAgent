# Guide d'Exécution sur VS Code (Windows)

Ce guide vous montre comment exécuter le système multi-agent localement sur VS Code Windows.

## Prérequis

1. **Python 3.10 ou 3.11** installé sur Windows
   - Télécharger depuis: https://www.python.org/downloads/
   - ⚠️ Cocher "Add Python to PATH" lors de l'installation

2. **VS Code** installé
   - Télécharger depuis: https://code.visualstudio.com/

3. **Ollama** installé sur Windows (pour le LLM local)
   - Télécharger depuis: https://ollama.ai/download
   - Après installation, télécharger le modèle: `ollama pull mistral`

4. **Git** installé (pour cloner le projet)

## Étape 1: Ouvrir le Projet dans VS Code

### Option A: Depuis VS Code
1. Ouvrir VS Code
2. `File` → `Open Folder`
3. Naviguer vers `E:\IntelligentTutorMultiAgent\IntelligentTutorMultiAgent`
4. Cliquer sur `Select Folder`

### Option B: Depuis PowerShell
```powershell
cd E:\IntelligentTutorMultiAgent\IntelligentTutorMultiAgent
code .
```

## Étape 2: Ouvrir le Terminal Intégré

Dans VS Code:
1. `Terminal` → `New Terminal` (ou `Ctrl + ù`)
2. Assurer que vous utilisez PowerShell (affiché en haut du terminal)

## Étape 3: Vérifier Python

```powershell
# Vérifier que Python est installé
python --version

# Devrait afficher: Python 3.10.x ou 3.11.x
```

Si Python n'est pas reconnu:
```powershell
# Essayer avec py
py --version

# Ou py -3.11 pour une version spécifique
py -3.11 --version
```

## Étape 4: Créer un Environnement Virtuel

```powershell
# Créer un environnement virtuel
python -m venv venv

# Ou si python ne fonctionne pas:
py -3.11 -m venv venv
```

## Étape 5: Activer l'Environnement Virtuel

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1
```

### ⚠️ Si vous avez une erreur de politique d'exécution:

```powershell
# Permettre l'exécution de scripts (une seule fois)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Puis réessayer
.\venv\Scripts\Activate.ps1
```

Vous devriez voir `(venv)` au début de votre ligne de commande.

## Étape 6: Installer les Dépendances

```powershell
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r backend/requirements.txt
```

Cette étape peut prendre 2-5 minutes. Vous verrez l'installation de:
- FastAPI, Uvicorn (API)
- OpenAI, Anthropic (LLM clients)
- Sentence-transformers (embeddings)
- Et autres dépendances...

## Étape 7: Configurer les Variables d'Environnement

Le fichier `.env` est déjà présent. Vérifier qu'il contient:

```powershell
# Voir le contenu du .env
Get-Content .env | Select-String "OLLAMA_HOST"
```

Devrait afficher: `OLLAMA_HOST=http://localhost:11434`

### Si vous utilisez Docker pour Ollama:
Modifier `.env` et changer:
```
OLLAMA_HOST=http://localhost:11434
```

### Si Ollama n'est pas installé:
Modifier `.env` et utiliser un LLM cloud:
```
USE_LOCAL_LLM=false
CLOUD_LLM_PROVIDER=openai
OPENAI_API_KEY=votre_clé_api
```

## Étape 8: Vérifier qu'Ollama Fonctionne (Optionnel)

Si vous utilisez Ollama local:

```powershell
# Vérifier qu'Ollama est démarré
ollama list

# Devrait afficher le modèle mistral

# Tester Ollama
curl http://localhost:11434/api/tags
```

Si Ollama n'est pas démarré:
1. Ouvrir le menu Démarrer
2. Chercher "Ollama"
3. Lancer l'application

## Étape 9: Démarrer le Serveur Backend

```powershell
# Définir la variable PYTHONPATH
$env:PYTHONPATH = "E:\IntelligentTutorMultiAgent\IntelligentTutorMultiAgent"

# Démarrer le serveur
python -m backend.api.main
```

Vous devriez voir:
```
✓ Multi-agent system initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Agent initialized: coordinator
INFO:     Registered agent: tutor
INFO:     Registered agent: evaluator
INFO:     Registered agent: generator
INFO:     Registered agent: rag
INFO:     Application startup complete.
```

## Étape 10: Tester l'API

### Ouvrir un Nouveau Terminal (Ctrl + Shift + ù)

```powershell
# Test 1: Vérifier le status
curl http://localhost:8000/api/status

# Test 2: Créer une session
curl -X POST http://localhost:8000/api/sessions `
  -H "Content-Type: application/json" `
  -d '{\"student_id\":\"test_001\",\"name\":\"Test\",\"curriculum_level\":\"tronc_commun\",\"language\":\"fr\"}'

# Test 3: Envoyer un message
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{\"session_id\":\"session_test_001_0\",\"message\":\"Explique-moi les variables en Python\",\"language\":\"fr\"}'
```

### Ou ouvrir dans le navigateur:
- Documentation API: http://localhost:8000/docs
- Interface Web: Ouvrir `frontend/index.html` dans le navigateur

## Étape 11: Configuration de VS Code (Optionnel mais Recommandé)

### Installer les Extensions VS Code

1. **Python** (Microsoft) - Support Python complet
2. **Pylance** (Microsoft) - IntelliSense amélioré
3. **REST Client** - Tester l'API directement dans VS Code
4. **Thunder Client** - Alternative à Postman intégré

### Créer une Configuration de Lancement

Créer `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI Backend",
            "type": "python",
            "request": "launch",
            "module": "backend.api.main",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

Puis appuyer sur `F5` pour démarrer le serveur en mode debug.

### Créer un fichier de requêtes REST

Créer `test_api.http` (avec l'extension REST Client):

```http
### Test Status
GET http://localhost:8000/api/status

### Create Session
POST http://localhost:8000/api/sessions
Content-Type: application/json

{
  "student_id": "vscode_test",
  "name": "VS Code Test",
  "curriculum_level": "tronc_commun",
  "language": "fr"
}

### Send Message
POST http://localhost:8000/api/chat
Content-Type: application/json

{
  "session_id": "session_vscode_test_0",
  "message": "Qu'est-ce qu'une variable en Python?",
  "language": "fr"
}
```

Cliquer sur "Send Request" au-dessus de chaque requête.

## Scripts PowerShell Utiles

### Créer `start_server.ps1`:

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Définir PYTHONPATH
$env:PYTHONPATH = $PWD.Path

# Démarrer le serveur
python -m backend.api.main
```

Utilisation:
```powershell
.\start_server.ps1
```

### Créer `install_deps.ps1`:

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r backend/requirements.txt

Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
```

Utilisation:
```powershell
.\install_deps.ps1
```

## Résolution de Problèmes

### Erreur: "python not found"

```powershell
# Utiliser py à la place
py -3.11 -m venv venv
py -3.11 -m backend.api.main
```

### Erreur: "Cannot be loaded because running scripts is disabled"

```powershell
# Changer la politique d'exécution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erreur: "ModuleNotFoundError"

```powershell
# Vérifier que l'environnement virtuel est activé
# Vous devriez voir (venv) au début de la ligne

# Réinstaller les dépendances
pip install -r backend/requirements.txt
```

### Erreur: "Address already in use" (Port 8000)

```powershell
# Trouver le processus qui utilise le port 8000
netstat -ano | findstr :8000

# Tuer le processus (remplacer PID par le numéro affiché)
Stop-Process -Id PID -Force

# Ou changer le port dans .env
# API_PORT=8001
```

### Erreur: "Cannot connect to Ollama"

```powershell
# Vérifier qu'Ollama est démarré
ollama list

# Si pas démarré, lancer Ollama depuis le menu Démarrer

# Ou utiliser un LLM cloud dans .env:
# USE_LOCAL_LLM=false
# CLOUD_LLM_PROVIDER=openai
# OPENAI_API_KEY=votre_clé
```

### Le serveur démarre mais les réponses sont vides

```powershell
# Vérifier les logs dans le terminal du serveur
# Vérifier que PYTHONPATH est défini:
echo $env:PYTHONPATH

# Devrait afficher le chemin du projet
```

## Développement

### Recharger automatiquement le serveur

Le serveur se recharge automatiquement quand vous modifiez le code (grâce à `API_RELOAD=true` dans `.env`)

### Voir les logs en temps réel

Les logs s'affichent directement dans le terminal VS Code où le serveur tourne.

### Déboguer le code

1. Mettre des points d'arrêt en cliquant à gauche des numéros de ligne
2. Appuyer sur `F5` pour démarrer en mode debug
3. Le serveur s'arrêtera aux points d'arrêt

## Performance

### Améliorer les performances sur Windows

```powershell
# Exclure le dossier venv de Windows Defender
Add-MpPreference -ExclusionPath "E:\IntelligentTutorMultiAgent\IntelligentTutorMultiAgent\venv"

# Exclure Python.exe
Add-MpPreference -ExclusionProcess "python.exe"
```

## Alternative: Utiliser WSL2

Si vous avez des problèmes avec Windows, vous pouvez utiliser WSL2:

```powershell
# Installer WSL2
wsl --install

# Ouvrir Ubuntu dans WSL2
wsl

# Puis suivre les instructions Linux du README.md
```

VS Code supporte WSL2 nativement avec l'extension "Remote - WSL".

## Commandes Rapides

```powershell
# Démarrer le serveur
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH = $PWD.Path
python -m backend.api.main

# Installer les dépendances
pip install -r backend/requirements.txt

# Mettre à jour les dépendances
pip install --upgrade -r backend/requirements.txt

# Voir les dépendances installées
pip list

# Désactiver l'environnement virtuel
deactivate
```

## Support

Pour plus d'informations:
- README.md - Documentation générale
- GUIDE_API_REST.md - Guide de l'API
- GUIDE_DOCKER.md - Guide Docker
- Documentation API: http://localhost:8000/docs
