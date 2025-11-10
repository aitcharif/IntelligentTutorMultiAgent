# Guide de Test de l'API REST

Ce guide vous montre comment tester l'API REST du système multi-agent.

## URL de Base

- **Local**: http://localhost:8000
- **Docker**: http://localhost:8000

## Endpoints Disponibles

### 1. Status du Système

Vérifier que tous les agents sont actifs.

**Endpoint**: `GET /api/status`

```bash
curl http://localhost:8000/api/status
```

**Réponse**:
```json
{
  "coordinator": {
    "id": "coordinator",
    "active": true,
    "registered_agents": 4
  },
  "agents": [
    {
      "id": "tutor",
      "type": "tutor",
      "active": true,
      "capabilities": ["teach", "explain", "provide_hints"]
    },
    {
      "id": "evaluator",
      "type": "evaluator",
      "active": true,
      "capabilities": ["evaluate", "provide_hints"]
    },
    {
      "id": "generator",
      "type": "generator",
      "active": true,
      "capabilities": ["generate_exercises"]
    },
    {
      "id": "rag",
      "type": "rag",
      "active": true,
      "capabilities": ["retrieve_knowledge"]
    }
  ]
}
```

### 2. Créer une Session

Créer une nouvelle session d'apprentissage.

**Endpoint**: `POST /api/sessions`

```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "ahmed_001",
    "name": "Ahmed",
    "curriculum_level": "tronc_commun",
    "language": "fr"
  }'
```

**Paramètres**:
- `student_id`: Identifiant unique de l'étudiant (requis)
- `name`: Nom de l'étudiant (optionnel)
- `curriculum_level`:
  - `tronc_commun` (Tronc Commun)
  - `premiere_bac` (1ère Bac)
  - `deuxieme_bac` (2ème Bac)
- `language`:
  - `fr` (Français)
  - `ar` (Arabe)
  - `en` (Anglais)

**Réponse**:
```json
{
  "success": true,
  "session_id": "session_ahmed_001_0",
  "message": "Session created successfully"
}
```

**Sauvegarder le session_id** pour les requêtes suivantes!

### 3. Envoyer un Message (Chat)

Poser une question ou demander de l'aide.

**Endpoint**: `POST /api/chat`

#### Exemple 1: Question sur les variables Python

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Explique-moi ce qu'est une variable en Python",
    "language": "fr"
  }'
```

#### Exemple 2: Demander un exercice

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Donne-moi un exercice sur les variables Python",
    "language": "fr"
  }'
```

#### Exemple 3: Soumettre une solution

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Voici ma solution:\n\nage = 17\nprint(age)",
    "language": "fr"
  }'
```

#### Exemple 4: Question en Arabe

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "ما هي المتغيرات في بايثون؟",
    "language": "ar"
  }'
```

**Réponse Typique**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "En Python, une variable est un espace mémoire...",
  "agent_used": "tutor",
  "intent": "question",
  "timestamp": "2025-11-08T17:48:29.790Z"
}
```

## Exemples Complets de Scénarios

### Scénario 1: Apprendre les Variables Python

```bash
# 1. Créer une session
SESSION_ID=$(curl -s -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "Fatima",
    "curriculum_level": "tronc_commun",
    "language": "fr"
  }' | jq -r '.session_id')

echo "Session créée: $SESSION_ID"

# 2. Poser une question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"Explique-moi ce qu'est une variable en Python avec un exemple simple\",
    \"language\": \"fr\"
  }" | jq .

# 3. Demander un exercice
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"Donne-moi un exercice facile sur les variables\",
    \"language\": \"fr\"
  }" | jq .

# 4. Soumettre une solution
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"Voici ma solution:\n\nnom = 'Fatima'\nage = 16\nprint('Je m\\'appelle', nom, 'et j\\'ai', age, 'ans')\",
    \"language\": \"fr\"
  }" | jq .
```

### Scénario 2: Cours en Arabe

```bash
# Créer une session en arabe
SESSION_ID=$(curl -s -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "محمد",
    "curriculum_level": "premiere_bac",
    "language": "ar"
  }' | jq -r '.session_id')

# Poser une question en arabe
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"ما هي الدوال في بايثون؟\",
    \"language\": \"ar\"
  }" | jq .
```

### Scénario 3: Niveau Avancé (2ème Bac)

```bash
# Session pour 2ème Bac
SESSION_ID=$(curl -s -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "Youssef",
    "curriculum_level": "deuxieme_bac",
    "language": "fr"
  }' | jq -r '.session_id')

# Question avancée sur les algorithmes
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"Explique-moi l'algorithme de tri par insertion avec un exemple\",
    \"language\": \"fr\"
  }" | jq .
```

## Test avec Python

Si vous préférez utiliser Python pour tester:

```python
import requests
import json

# URL de base
BASE_URL = "http://localhost:8000"

# 1. Créer une session
session_response = requests.post(
    f"{BASE_URL}/api/sessions",
    json={
        "student_id": "Amina",
        "curriculum_level": "tronc_commun",
        "language": "fr"
    }
)
session_data = session_response.json()
session_id = session_data["session_id"]
print(f"Session créée: {session_id}")

# 2. Envoyer un message
chat_response = requests.post(
    f"{BASE_URL}/api/chat",
    json={
        "session_id": session_id,
        "message": "Qu'est-ce qu'une boucle for en Python?",
        "language": "fr"
    }
)
chat_data = chat_response.json()
print(f"\nRéponse: {chat_data['response']}")
print(f"Agent utilisé: {chat_data['agent_used']}")
```

## Test avec Postman

1. **Importer la collection** (fichier à créer):
   - Créer une nouvelle collection "Moroccan CS Tutor"
   - Ajouter les requêtes ci-dessus

2. **Variables d'environnement**:
   - `base_url`: http://localhost:8000
   - `session_id`: (sera rempli automatiquement)

3. **Scripts de test**:
```javascript
// Dans la requête POST /api/sessions
pm.test("Session créée", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.environment.set("session_id", jsonData.session_id);
});
```

## Test avec cURL - Scripts Complets

### Script de Test Complet (Bash)

Créez un fichier `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "========================================="
echo "Test de l'API Multi-Agent"
echo "========================================="

# Couleurs pour le terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Test du status
echo -e "\n${BLUE}1. Test du status${NC}"
curl -s $BASE_URL/api/status | jq .

# 2. Créer une session
echo -e "\n${BLUE}2. Création d'une session${NC}"
SESSION_RESPONSE=$(curl -s -X POST $BASE_URL/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "Test Student",
    "curriculum_level": "tronc_commun",
    "language": "fr"
  }')

SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')
echo -e "${GREEN}Session ID: $SESSION_ID${NC}"

# 3. Test question
echo -e "\n${BLUE}3. Test question${NC}"
curl -s -X POST $BASE_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"Qu'est-ce qu'une variable?\",
    \"language\": \"fr\"
  }" | jq .

# 4. Test demande exercice
echo -e "\n${BLUE}4. Test demande exercice${NC}"
curl -s -X POST $BASE_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"Donne-moi un exercice\",
    \"language\": \"fr\"
  }" | jq .

echo -e "\n${GREEN}Tests terminés!${NC}"
```

Rendre le script exécutable:
```bash
chmod +x test_api.sh
./test_api.sh
```

## Documentation Interactive

L'API FastAPI génère automatiquement une documentation interactive:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Vous pouvez tester toutes les endpoints directement depuis votre navigateur!

## Codes de Réponse HTTP

- `200`: Succès
- `400`: Requête invalide
- `404`: Session non trouvée
- `500`: Erreur serveur

## Résolution de Problèmes

### Erreur "Connection refused"

Le serveur n'est pas démarré:
```bash
# Local
source venv/bin/activate
PYTHONPATH=/home/user/IntelligentTutorMultiAgent python -m backend.api.main

# Docker
docker compose up -d
```

### Erreur "Session not found"

Le session_id est invalide ou expiré. Créez une nouvelle session.

### Réponse vide ou erreur

Vérifiez les logs du serveur:
```bash
# Local: voir le terminal où le serveur tourne

# Docker
docker compose logs backend
```

## Performance

- **Temps de réponse moyen**: 1-3 secondes
- **Latence LLM local (Ollama)**: 2-5 secondes
- **Latence LLM cloud (OpenAI/Claude)**: 1-2 secondes

## Limites

- **Taille maximale du message**: 10,000 caractères
- **Durée de vie de la session**: 24 heures
- **Nombre de messages par session**: Illimité

## Support

Pour plus d'informations:
- Documentation API: http://localhost:8000/docs
- README: ../README.md
- Guide Docker: GUIDE_DOCKER.md
