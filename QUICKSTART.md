# 🚀 Guide de Démarrage Rapide

## Installation Rapide

### 1. Backend (Python)

```bash
# Installer les dépendances
cd backend
pip install -r requirements.txt

# Configuration
cp ../config/.env.example ../.env

# Pour utiliser LLM local (RECOMMANDÉ - pas besoin de clé API)
# Installer Ollama
curl https://ollama.ai/install.sh | sh

# Télécharger un modèle
ollama pull mistral
```

### 2. Lancer le Système

```bash
# Démarrer le backend
cd backend
python -m api.main

# Le serveur démarre sur http://localhost:8000
```

### 3. Tester l'API

```bash
# Créer une session
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "student_001",
    "name": "Ahmed",
    "language": "fr",
    "curriculum_level": "tronc_commun"
  }'

# Envoyer un message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_student_001_0",
    "message": "Explique-moi les boucles en Python",
    "language": "fr"
  }'
```

## Configuration LLM

### Option 1: LLM Local (Ollama) - RECOMMANDÉ

```bash
# Dans .env
USE_LOCAL_LLM=true
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral
```

**Avantages:**
- ✅ Gratuit
- ✅ Fonctionne hors ligne
- ✅ Pas besoin de clé API
- ✅ Données privées

### Option 2: LLM Cloud (OpenAI/Claude)

```bash
# Dans .env
USE_LOCAL_LLM=false
OPENAI_API_KEY=sk-xxxxx
CLOUD_LLM_PROVIDER=openai
CLOUD_LLM_MODEL=gpt-4
```

## Fonctionnalités Disponibles

### 1. Chat Éducatif

```python
# L'élève pose une question
"Qu'est-ce qu'une variable en Python?"

# Le système:
# 1. Analyse la question (Coordinateur)
# 2. Récupère les connaissances (RAG Agent)
# 3. Génère une réponse pédagogique (Tutor Agent)
```

### 2. Génération d'Exercices

```python
"Donne-moi des exercices sur les listes Python"

# Le système:
# 1. Détecte la demande d'exercices (Coordinateur)
# 2. Génère des exercices adaptés (Generator Agent)
```

### 3. Évaluation

```python
"Voici ma solution: [code]"

# Le système:
# 1. Évalue le code (Evaluator Agent)
# 2. Donne un feedback constructif
```

## Architecture

```
Student Message
      ↓
Coordinateur Central (analyse et route)
      ↓
   ┌──┴──┬───────┬──────────┐
   ↓     ↓       ↓          ↓
 Tutor  RAG  Evaluator  Generator
   ↓     ↓       ↓          ↓
      Ollama/OpenAI
```

## Langues Supportées

- 🇫🇷 Français
- 🇲🇦 العربية (Arabe)
- 🇬🇧 English

## Curriculum Marocain

- **Tronc Commun**: Introduction à l'informatique
- **1ère Bac**: Programmation, Algorithmique
- **2ème Bac**: Structures de données, POO

## Troubleshooting

### Erreur: "Connection refused" avec Ollama

```bash
# Vérifier qu'Ollama tourne
ollama list

# Démarrer Ollama si nécessaire
ollama serve
```

### Erreur: "Module not found"

```bash
pip install -r backend/requirements.txt
```

## Documentation Complète

- [README.md](README.md) - Vue d'ensemble
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Architecture détaillée
- [API Documentation](http://localhost:8000/docs) - Swagger UI

## Support

- GitHub Issues
- Email: support@example.com
