# 📥 Guide de Clonage et Configuration

## 🎯 Méthode Rapide (3 minutes)

### 1️⃣ Cloner le Repository

```bash
# Remplacez <URL_GITHUB> par l'URL de votre repository
git clone https://github.com/aitcharif/IntelligentTutorMultiAgent.git

# Entrer dans le dossier
cd IntelligentTutorMultiAgent
```

### 2️⃣ Installer Ollama (LLM Local Gratuit)

#### **Linux:**
```bash
curl https://ollama.ai/install.sh | sh
ollama pull mistral
```

#### **Mac:**
```bash
# Télécharger depuis https://ollama.ai/download
# ou avec Homebrew:
brew install ollama
ollama pull mistral
```

#### **Windows:**
```powershell
# Télécharger et installer depuis: https://ollama.ai/download
# Puis dans PowerShell:
ollama pull mistral
```

### 3️⃣ Lancer le Système

#### **Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

#### **Windows:**
```cmd
start.bat
```

### 4️⃣ Ouvrir l'Interface

Ouvrez `frontend/index.html` dans votre navigateur 🎉

---

## 🐳 Méthode Docker (Alternative)

```bash
# 1. Cloner
git clone https://github.com/aitcharif/IntelligentTutorMultiAgent.git
cd IntelligentTutorMultiAgent

# 2. Copier la configuration
cp config/.env.example .env

# 3. Démarrer tout avec Docker
docker-compose up -d

# 4. Télécharger le modèle LLM
docker exec -it moroccan-cs-ollama ollama pull mistral

# 5. Accéder
# Frontend: http://localhost:8080
# API: http://localhost:8000
```

---

## 📋 Guide Détaillé Étape par Étape

### Étape 1: Prérequis

**Vérifier Git:**
```bash
git --version
```
Si pas installé: https://git-scm.com/downloads

**Vérifier Python:**
```bash
python --version  # ou python3 --version
```
Nécessite Python 3.10+. Si pas installé: https://www.python.org/downloads/

### Étape 2: Cloner le Repository

```bash
# SSH (recommandé si vous avez des clés SSH configurées)
git clone git@github.com:aitcharif/IntelligentTutorMultiAgent.git

# HTTPS (plus simple)
git clone https://github.com/aitcharif/IntelligentTutorMultiAgent.git

# Entrer dans le dossier
cd IntelligentTutorMultiAgent
```

### Étape 3: Vérifier le Contenu

```bash
# Lister les fichiers
ls -la

# Devrait afficher:
# backend/
# frontend/
# data/
# config/
# docs/
# start.sh
# start.bat
# README.md
# etc.
```

### Étape 4: Configuration

#### **Option A: Utiliser le Script Automatique**

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

Le script fait automatiquement:
- ✅ Vérifie Python
- ✅ Vérifie Ollama
- ✅ Crée l'environnement virtuel
- ✅ Installe les dépendances
- ✅ Lance le serveur

**Windows:**
```cmd
start.bat
```

#### **Option B: Configuration Manuelle**

```bash
# 1. Créer environnement virtuel
python -m venv venv

# 2. Activer l'environnement
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Installer les dépendances
pip install -r backend/requirements.txt

# 4. Copier la configuration
cp config/.env.example .env

# 5. (Optionnel) Éditer .env
nano .env
```

### Étape 5: Installer et Configurer Ollama

#### **Installation:**

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Mac:**
```bash
# Télécharger depuis https://ollama.ai/download
# Ou avec Homebrew:
brew install ollama
```

**Windows:**
```powershell
# Télécharger et installer: https://ollama.ai/download
```

#### **Télécharger un Modèle:**

```bash
# Modèle général (recommandé)
ollama pull mistral

# Modèle pour l'arabe (meilleur pour العربية)
ollama pull aya

# Modèle pour le code
ollama pull codellama
```

#### **Vérifier l'Installation:**
```bash
ollama list
# Devrait afficher les modèles téléchargés
```

### Étape 6: Démarrer le Serveur

#### **Méthode 1: Avec le Script**
```bash
./start.sh        # Linux/Mac
start.bat         # Windows
```

#### **Méthode 2: Manuellement**
```bash
# Activer l'environnement virtuel si pas déjà fait
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Démarrer le serveur
cd backend
python -m api.main
```

### Étape 7: Vérifier que Tout Fonctionne

#### **Test 1: API**
```bash
curl http://localhost:8000/

# Devrait retourner:
# {"status":"running","system":"Moroccan CS Education Multi-Agent","version":"1.0.0"}
```

#### **Test 2: Documentation API**
Ouvrez dans le navigateur:
```
http://localhost:8000/docs
```

#### **Test 3: Interface Web**
Ouvrez le fichier:
```
frontend/index.html
```

### Étape 8: Tester le Système

1. **Ouvrir l'interface** (`frontend/index.html`)
2. **Sélectionner la langue** (Français/Arabe/Anglais)
3. **Poser une question:** "Explique-moi les variables en Python"
4. **Attendre la réponse** (2-5 secondes)

---

## 🔧 Configuration Avancée

### Utiliser OpenAI/Claude (Cloud LLM)

Si vous préférez utiliser un LLM cloud plutôt qu'Ollama:

1. **Éditer `.env`:**
```bash
nano .env
```

2. **Modifier ces lignes:**
```bash
USE_LOCAL_LLM=false
OPENAI_API_KEY=sk-votre-clé-api-ici
CLOUD_LLM_PROVIDER=openai
CLOUD_LLM_MODEL=gpt-4
```

3. **Redémarrer le serveur**

### Configurer le RAG (Base de Connaissances)

```bash
# Dans .env
CHROMA_DB_PATH=./data/chroma_db
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
RAG_TOP_K=5
```

### Activer l'Audio

```bash
# Dans .env
STT_SERVICE=whisper
WHISPER_MODEL=base
TTS_SERVICE=gtts
TTS_LANGUAGE=fr
```

---

## 🚨 Résolution de Problèmes

### Problème 1: "git: command not found"
```bash
# Installer Git
# Ubuntu/Debian:
sudo apt-get install git

# CentOS/RHEL:
sudo yum install git

# Mac:
brew install git

# Windows: télécharger depuis https://git-scm.com/
```

### Problème 2: "python: command not found"
```bash
# Essayer:
python3 --version

# Si ça ne marche pas, installer Python:
# https://www.python.org/downloads/
```

### Problème 3: "Permission denied: ./start.sh"
```bash
# Rendre le script exécutable
chmod +x start.sh
```

### Problème 4: "Port 8000 already in use"
```bash
# Trouver et tuer le processus
# Linux/Mac:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Ou changer le port dans .env:
API_PORT=8001
```

### Problème 5: "Ollama connection refused"
```bash
# Démarrer Ollama manuellement
ollama serve

# Vérifier qu'il tourne
ollama list
```

### Problème 6: "Module not found"
```bash
# Réinstaller les dépendances
pip install --upgrade -r backend/requirements.txt
```

### Problème 7: Réponses Lentes
```bash
# Utiliser un modèle plus petit
ollama pull mistral:7b-instruct

# Mettre à jour .env:
OLLAMA_MODEL=mistral:7b-instruct
```

---

## 📊 Vérification Post-Installation

### Checklist:
- [ ] Git installé
- [ ] Python 3.10+ installé
- [ ] Repository cloné
- [ ] Ollama installé
- [ ] Modèle LLM téléchargé (mistral)
- [ ] Dépendances Python installées
- [ ] Fichier .env créé
- [ ] Serveur démarre sans erreur
- [ ] API répond sur http://localhost:8000
- [ ] Interface web s'ouvre
- [ ] Questions reçoivent des réponses

### Commandes de Vérification:
```bash
# 1. Versions
git --version
python --version
ollama --version

# 2. Modèles
ollama list

# 3. Processus
ps aux | grep "api.main"

# 4. Ports
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# 5. Test API
curl http://localhost:8000/
```

---

## 🎯 Prochaines Étapes

Après installation réussie:

1. **Lire la documentation:**
   - [README.md](README.md) - Vue d'ensemble
   - [QUICKSTART.md](QUICKSTART.md) - Guide rapide
   - [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Architecture

2. **Explorer l'API:**
   - http://localhost:8000/docs (Swagger)
   - http://localhost:8000/redoc (ReDoc)

3. **Tester les fonctionnalités:**
   - Poser des questions
   - Générer des exercices
   - Évaluer du code
   - Essayer différentes langues

4. **Personnaliser:**
   - Ajouter du contenu dans `data/courses/`
   - Créer des exercices dans `data/exercises/`
   - Modifier l'interface dans `frontend/`

---

## 💡 Conseils

1. **Première fois:** Utilisez le script automatique (`./start.sh` ou `start.bat`)
2. **Développement:** Installation manuelle pour plus de contrôle
3. **Production:** Utilisez Docker avec `docker-compose`
4. **Performance:** `mistral` est un bon compromis qualité/vitesse
5. **Offline:** Tout fonctionne sans internet avec Ollama

---

## 📚 Ressources

- **Documentation Ollama:** https://ollama.ai/docs
- **Repository GitHub:** https://github.com/aitcharif/IntelligentTutorMultiAgent
- **API Docs:** http://localhost:8000/docs
- **Support:** GitHub Issues

---

## ✅ Installation Réussie!

Si vous voyez:
```
✓ Backend démarré sur http://localhost:8000
✓ Documentation API: http://localhost:8000/docs
✓ Système multi-agent initialisé
```

**Félicitations! Vous êtes prêt! 🎉**

Ouvrez `frontend/index.html` et commencez à apprendre! 🎓
