# Guide de Test Local - IntelligentTutorMultiAgent

## Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Clé API OpenAI ou Anthropic

## Étape 1: Vérifier Python

```bash
python --version
# ou
python3 --version
```

Si Python n'est pas installé, téléchargez-le depuis [python.org](https://www.python.org/downloads/)

## Étape 2: Créer un Environnement Virtuel (Recommandé)

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Linux/Mac:
source venv/bin/activate

# Sur Windows:
venv\Scripts\activate
```

Vous devriez voir `(venv)` au début de votre ligne de commande.

## Étape 3: Installer les Dépendances

```bash
pip install -r requirements.txt
```

Si vous rencontrez des erreurs, essayez:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Étape 4: Configuration des Clés API

### Option A: Fichier .env (Recommandé)

```bash
# Copier le fichier d'exemple
cp config/.env.example .env

# Éditer .env avec votre éditeur préféré
nano .env
# ou
vim .env
# ou ouvrez avec VSCode, etc.
```

Ajoutez votre clé API:
```bash
# Pour OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OU pour Anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxx

LLM_PROVIDER=openai  # ou anthropic
DEFAULT_MODEL=gpt-4
```

### Option B: Variables d'Environnement

```bash
# Sur Linux/Mac:
export OPENAI_API_KEY="sk-xxxxx"

# Sur Windows (CMD):
set OPENAI_API_KEY=sk-xxxxx

# Sur Windows (PowerShell):
$env:OPENAI_API_KEY="sk-xxxxx"
```

## Étape 5: Tests Rapides

### Test 1: Vérifier l'Installation

```bash
python -c "import sys; print(f'Python {sys.version}')"
python -c "import openai; print('OpenAI package OK')"
python -c "import pydantic; print('Pydantic package OK')"
```

### Test 2: Test Unitaire Simple

```bash
pytest tests/test_agents.py -v
```

### Test 3: Exemple de Base (Sans LLM)

Créez un fichier `test_quick.py`:
```python
from src.core.agent import AgentConfig, AgentRole, AgentCapability
from src.core.context import StudentProfile, ConversationContext
from src.core.message import Message, MessageType

print("✓ Imports OK")

# Test création de profil
student = StudentProfile(
    student_id="test_123",
    name="Alice Test",
    learning_style="visual"
)
print(f"✓ Student profile created: {student.name}")

# Test création de contexte
context = ConversationContext(
    session_id="test_session",
    student_profile=student
)
print(f"✓ Context created: {context.session_id}")

# Test création de message
message = Message(
    type=MessageType.QUERY,
    sender="student",
    content="Test question"
)
print(f"✓ Message created: {message.id}")

print("\n✅ All basic tests passed!")
```

Exécutez:
```bash
python test_quick.py
```

### Test 4: Test avec LLM (Nécessite API Key)

```bash
python examples/simple_test.py
```

### Test 5: API REST

```bash
# Terminal 1 - Démarrer le serveur
python examples/rest_api.py

# Terminal 2 - Tester l'API
curl http://localhost:8000/health
```

## Tests Avancés

### Test Complet avec LLM

```bash
python examples/basic_usage.py
```

### Test de l'API avec des Requêtes

```bash
# Créer une session
curl -X POST http://localhost:8000/sessions/create \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_001",
    "student_profile": {
      "student_id": "student_123",
      "name": "Alice"
    },
    "subject": "Mathematics"
  }'

# Poser une question
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_001",
    "query": "Qu'\''est-ce qu'\''une dérivée?"
  }'
```

## Résolution de Problèmes

### Erreur: Module not found

```bash
# Vérifier que vous êtes dans le bon répertoire
pwd

# Vérifier que l'environnement virtuel est activé
which python

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur: API Key

```bash
# Vérifier que la clé est définie
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY%  # Windows CMD

# Vérifier le fichier .env
cat .env
```

### Erreur: Port déjà utilisé (API REST)

```bash
# Changer le port dans rest_api.py
# Ligne: uvicorn.run(app, host="0.0.0.0", port=8001)

# Ou tuer le processus sur le port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Erreur: Import Error

```bash
# Ajouter le répertoire au PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%  # Windows CMD
```

## Vérification de l'Installation

Script de vérification complet:

```bash
python -c "
import sys
print('Python version:', sys.version)
print('Python path:', sys.executable)

try:
    import openai
    print('✓ OpenAI package installed')
except ImportError:
    print('✗ OpenAI package missing')

try:
    import anthropic
    print('✓ Anthropic package installed')
except ImportError:
    print('✗ Anthropic package missing')

try:
    import pydantic
    print('✓ Pydantic installed')
except ImportError:
    print('✗ Pydantic missing')

try:
    import loguru
    print('✓ Loguru installed')
except ImportError:
    print('✗ Loguru missing')

import os
if os.getenv('OPENAI_API_KEY'):
    print('✓ OPENAI_API_KEY is set')
elif os.getenv('ANTHROPIC_API_KEY'):
    print('✓ ANTHROPIC_API_KEY is set')
else:
    print('✗ No API key found')
"
```

## Logs et Débogage

Les logs sont sauvegardés dans `logs/tutor.log`

```bash
# Voir les logs en temps réel
tail -f logs/tutor.log

# Sur Windows:
Get-Content logs/tutor.log -Wait
```

## Prochaines Étapes

Une fois que tout fonctionne:
1. Explorez `examples/basic_usage.py` pour voir toutes les fonctionnalités
2. Testez l'API REST avec `examples/rest_api.py`
3. Créez vos propres agents personnalisés
4. Consultez `docs/ARCHITECTURE.md` pour comprendre le système

## Support

Si vous rencontrez des problèmes:
1. Vérifiez les logs dans `logs/tutor.log`
2. Assurez-vous que toutes les dépendances sont installées
3. Vérifiez que votre clé API est valide
4. Consultez la documentation dans `docs/`
