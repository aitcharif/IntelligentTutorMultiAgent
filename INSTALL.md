# 📦 Guide d'Installation Complet

## 🎯 Trois Méthodes d'Installation

### Méthode 1: Script Automatique (RECOMMANDÉ)

#### Linux/Mac:
```bash
git clone <votre-repo>
cd IntelligentTutorMultiAgent
./start.sh
```

#### Windows:
```bash
git clone <votre-repo>
cd IntelligentTutorMultiAgent
start.bat
```

Le script fait automatiquement:
- ✅ Vérification de Python
- ✅ Vérification d'Ollama
- ✅ Création de l'environnement virtuel
- ✅ Installation des dépendances
- ✅ Démarrage du serveur

---

### Méthode 2: Docker (PRODUCTION)

#### Prérequis:
- Docker et Docker Compose installés

#### Installation:
```bash
# Cloner le repo
git clone <votre-repo>
cd IntelligentTutorMultiAgent

# Copier la configuration
cp config/.env.example .env

# Démarrer avec Docker Compose
docker-compose up -d

# Télécharger le modèle Ollama
docker exec -it moroccan-cs-ollama ollama pull mistral
```

#### Services disponibles:
- Backend API: http://localhost:8000
- Frontend: http://localhost:8080
- Ollama: http://localhost:11434

#### Commandes utiles:
```bash
# Voir les logs
docker-compose logs -f backend

# Arrêter
docker-compose down

# Redémarrer
docker-compose restart
```

---

### Méthode 3: Installation Manuelle

#### Étape 1: Prérequis

**Python 3.10+**
```bash
# Vérifier
python3 --version
```

**Ollama (optionnel mais recommandé)**
```bash
# Linux/Mac
curl https://ollama.ai/install.sh | sh

# Windows: télécharger depuis https://ollama.ai/download
```

#### Étape 2: Cloner et Configurer

```bash
# Cloner
git clone <votre-repo>
cd IntelligentTutorMultiAgent

# Environnement virtuel
python3 -m venv venv

# Activer
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installer dépendances
pip install -r backend/requirements.txt
```

#### Étape 3: Configuration

```bash
# Copier la config
cp config/.env.example .env

# Éditer .env (optionnel)
nano .env
```

**Configuration minimale (.env):**
```bash
USE_LOCAL_LLM=true
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral
```

#### Étape 4: Télécharger un Modèle LLM

```bash
# Modèle général (recommandé)
ollama pull mistral

# Modèle pour l'arabe (meilleur pour العربية)
ollama pull aya

# Modèle pour le code
ollama pull codellama
```

#### Étape 5: Démarrer

```bash
# Démarrer Ollama (si pas déjà lancé)
ollama serve

# Dans un autre terminal, démarrer le backend
cd backend
python -m api.main
```

#### Étape 6: Ouvrir l'Interface

Ouvrez `frontend/index.html` dans votre navigateur

---

## 🔧 Configuration Avancée

### Utiliser OpenAI/Claude (Cloud)

Dans `.env`:
```bash
USE_LOCAL_LLM=false
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
CLOUD_LLM_PROVIDER=openai
CLOUD_LLM_MODEL=gpt-4
```

### Configurer le RAG

```bash
# Dans .env
CHROMA_DB_PATH=./data/chroma_db
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
```

### Audio (STT/TTS)

```bash
# Dans .env
STT_SERVICE=whisper
WHISPER_MODEL=base
TTS_SERVICE=gtts
TTS_LANGUAGE=fr
```

---

## 🧪 Tester l'Installation

### Test 1: API Status
```bash
curl http://localhost:8000/api/status
```

### Test 2: Créer une Session
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "test_001",
    "name": "Test",
    "language": "fr"
  }'
```

### Test 3: Envoyer un Message
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_test_001_0",
    "message": "Bonjour!"
  }'
```

---

## 📊 Vérification du Système

### Checklist Post-Installation

- [ ] Python 3.10+ installé
- [ ] Ollama installé et en cours d'exécution
- [ ] Modèle LLM téléchargé (mistral/aya)
- [ ] Dépendances Python installées
- [ ] Fichier .env créé
- [ ] Backend démarré sur port 8000
- [ ] API répond aux requêtes
- [ ] Frontend accessible

### Commandes de Vérification

```bash
# Version Python
python3 --version

# Ollama
ollama list

# Processus backend
ps aux | grep "api.main"

# Ports ouverts
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows
```

---

## 🚨 Résolution de Problèmes

### Erreur: "Ollama not found"

```bash
# Vérifier installation
which ollama

# Si non installé
curl https://ollama.ai/install.sh | sh

# Démarrer manuellement
ollama serve
```

### Erreur: "Port 8000 already in use"

```bash
# Trouver le processus
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Tuer le processus
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Ou changer le port dans .env
API_PORT=8001
```

### Erreur: "Module not found"

```bash
# Réinstaller les dépendances
pip install --upgrade -r backend/requirements.txt
```

### Erreur: "Connection refused to Ollama"

```bash
# Vérifier qu'Ollama tourne
ollama list

# Redémarrer Ollama
pkill ollama
ollama serve
```

### Performance Lente

```bash
# Utiliser un modèle plus petit
ollama pull mistral:7b-instruct

# Ou en .env
OLLAMA_MODEL=mistral:7b-instruct
```

---

## 🔄 Mise à Jour

```bash
# Récupérer les dernières modifications
git pull origin main

# Mettre à jour les dépendances
pip install --upgrade -r backend/requirements.txt

# Redémarrer le serveur
# (Ctrl+C puis relancer)
```

---

## 📚 Ressources Supplémentaires

- **Documentation Ollama**: https://ollama.ai/docs
- **API Reference**: http://localhost:8000/docs (après démarrage)
- **Guide Architecture**: docs/ARCHITECTURE.md
- **Quick Start**: QUICKSTART.md

---

## 💡 Conseils

1. **Première utilisation**: Commencez avec Ollama (gratuit, local)
2. **Production**: Utilisez Docker pour faciliter le déploiement
3. **Développement**: Utilisez l'installation manuelle pour plus de contrôle
4. **Performance**: Le modèle `mistral` est un bon compromis qualité/vitesse

---

## ✅ Installation Réussie?

Vous devriez voir:
```
✓ Backend démarré sur http://localhost:8000
✓ Documentation API: http://localhost:8000/docs
✓ Frontend accessible via index.html
✓ Système multi-agent initialisé
```

Vous êtes prêt! 🎉

Consultez [QUICKSTART.md](QUICKSTART.md) pour commencer à utiliser le système.
