# 🎓 Plateforme Multi-Agent d'Enseignement Informatique pour le Maroc

Système intelligent multi-agent basé sur LLM pour l'enseignement de l'informatique adapté au contexte éducatif marocain.

## ✨ Fonctionnalités Principales

### 🤖 Architecture Multi-Agent avec Coordinateur Central
- **Coordinateur Central**: Orchestre tous les agents et gère le flux de travail
- **Agent Tuteur**: Enseignement personnalisé en français et arabe
- **Agent Évaluateur**: Évaluation automatique des exercices
- **Agent Générateur**: Création d'exercices adaptés au curriculum marocain
- **Agent RAG**: Récupération intelligente de connaissances

### 🧠 Systèmes d'IA Avancés
- **Support LLM Cloud**: OpenAI GPT-4, Anthropic Claude
- **Support LLM Local**: Ollama, LlamaCpp pour utilisation hors ligne
- **RAG (Retrieval Augmented Generation)**: Base de connaissances contextuelle
- **Embeddings**: ChromaDB pour recherche sémantique

### 🎨 Interface Utilisateur Moderne
- Interface web responsive et attrayante
- Chat en temps réel avec les agents
- Tableaux de bord de progression
- Mode sombre/clair
- Design adapté au contexte marocain

### 🎤 Fonctionnalités Audio
- **Speech-to-Text**: Convertir la voix en texte (arabe/français)
- **Text-to-Speech**: Réponses vocales naturelles
- Chat vocal interactif

### 🌍 Contexte Marocain
- Curriculum officiel marocain en informatique
- Support français et arabe
- Exemples culturellement pertinents
- Exercices adaptés au système éducatif local

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           Interface Utilisateur (Frontend)       │
│          React + Tailwind + WebRTC              │
└────────────────┬────────────────────────────────┘
                 │ REST API / WebSocket
┌────────────────┴────────────────────────────────┐
│          API Gateway (FastAPI)                   │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────┐
│      🎯 COORDINATEUR CENTRAL                     │
│  - Gestion des sessions                          │
│  - Routage intelligent                           │
│  - Orchestration des agents                      │
└─┬──────┬──────┬──────┬──────┬────────────────┬─┘
  │      │      │      │      │                │
  ┌──┴──┐ ┌─┴──┐ ┌─┴──┐ ┌─┴──┐ ┌──┴───┐     ┌─┴──┐
  │Agent│ │Agent│ │Agent│ │Agent│ │Agent │     │Audio│
  │Tuteur│ │Eval│ │Gen │ │RAG │ │Lang  │     │Proc │
  └──┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └──┬───┘     └─┬──┘
     │      │      │      │       │            │
  ┌──┴──────┴──────┴──────┴───────┴────────────┴─┐
  │          Couche LLM                            │
  │  - OpenAI / Claude (Cloud)                    │
  │  - Ollama / LlamaCpp (Local)                  │
  └────────────────────────────────────────────────┘
                     │
  ┌──────────────────┴─────────────────────────────┐
  │     Base de Connaissances (RAG)                │
  │  - ChromaDB (Embeddings)                       │
  │  - Cours informatique                          │
  │  - Exercices et solutions                      │
  │  - Documentation                                │
  └────────────────────────────────────────────────┘
```

## 📦 Structure du Projet

```
IntelligentTutorMultiAgent/
├── backend/                    # Backend Python
│   ├── agents/                # Agents spécialisés
│   │   ├── coordinator.py     # Coordinateur central
│   │   ├── tutor_agent.py     # Agent tuteur
│   │   ├── evaluator_agent.py # Agent évaluateur
│   │   ├── generator_agent.py # Générateur d'exercices
│   │   └── rag_agent.py       # Agent RAG
│   ├── core/                  # Composants de base
│   │   ├── base_agent.py      # Classe de base
│   │   ├── message.py         # Système de messages
│   │   └── context.py         # Gestion du contexte
│   ├── rag/                   # Système RAG
│   │   ├── embeddings.py      # Génération embeddings
│   │   ├── vector_store.py    # ChromaDB
│   │   └── retriever.py       # Récupération docs
│   ├── llm/                   # Intégration LLM
│   │   ├── cloud_llm.py       # OpenAI/Claude
│   │   ├── local_llm.py       # Ollama/LlamaCpp
│   │   └── llm_factory.py     # Factory pattern
│   ├── audio/                 # Traitement audio
│   │   ├── speech_to_text.py  # STT
│   │   └── text_to_speech.py  # TTS
│   └── api/                   # API REST
│       ├── main.py            # FastAPI app
│       ├── routes/            # Routes API
│       └── websocket.py       # WebSocket
├── frontend/                  # Frontend React
│   ├── src/
│   │   ├── components/        # Composants React
│   │   │   ├── Chat.jsx       # Interface chat
│   │   │   ├── AudioChat.jsx  # Chat vocal
│   │   │   └── Dashboard.jsx  # Tableau de bord
│   │   ├── pages/             # Pages
│   │   ├── services/          # Services API
│   │   └── assets/            # Assets statiques
│   ├── package.json
│   └── vite.config.js
├── data/                      # Données pédagogiques
│   ├── courses/               # Cours informatique
│   ├── exercises/             # Exercices
│   └── knowledge_base/        # Base de connaissances
├── docs/                      # Documentation
└── config/                    # Configuration
```

## 🚀 Installation

### Prérequis

- Python 3.10+
- Node.js 18+
- (Optionnel) Ollama pour LLM local

### Backend

```bash
# Installer les dépendances Python
cd backend
pip install -r requirements.txt

# Configuration
cp ../config/.env.example ../.env
# Éditer .env avec vos clés API

# Initialiser la base de données RAG
python -m rag.setup_database

# Lancer le serveur
python -m api.main
```

### Frontend

```bash
# Installer les dépendances Node
cd frontend
npm install

# Configuration
cp .env.example .env

# Lancer le dev server
npm run dev
```

### LLM Local (Optionnel)

```bash
# Installer Ollama
curl https://ollama.ai/install.sh | sh

# Télécharger un modèle français
ollama pull mistral
ollama pull aya  # Meilleur pour l'arabe
```

## 📖 Utilisation

### 1. Interface Web

Accédez à `http://localhost:5173` pour l'interface utilisateur

### 2. Chat Textuel

- Posez des questions en français ou arabe
- Recevez des explications personnalisées
- Demandez des exercices
- Obtenez de l'aide sur le code

### 3. Chat Vocal

- Cliquez sur le microphone
- Parlez en français ou arabe
- Recevez des réponses vocales

### 4. API REST

```bash
# Créer une session
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "student_123",
    "language": "fr"
  }'

# Envoyer un message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_001",
    "message": "Explique-moi les boucles en Python"
  }'
```

## 🎯 Fonctionnalités Détaillées

### Coordinateur Central

Le coordinateur orchestre tous les agents:
- Analyse les requêtes des étudiants
- Route vers les agents appropriés
- Combine les réponses de plusieurs agents
- Gère la cohérence de la conversation
- Adapte les réponses au niveau de l'étudiant

### Système RAG

Base de connaissances enrichie:
- Curriculum marocain en informatique
- Cours de programmation (Python, Java, C++)
- Algorithmes et structures de données
- Réseaux et sécurité
- Bases de données
- Développement web

### Agents Spécialisés

**Agent Tuteur**: Enseignement interactif personnalisé
**Agent Évaluateur**: Correction automatique et feedback
**Agent Générateur**: Création d'exercices variés
**Agent RAG**: Recherche intelligente dans la base de connaissances
**Agent Langue**: Traduction et adaptation culturelle

## 🌐 Support Multilingue

### Français
- Interface complète en français
- Explications pédagogiques
- Terminologie technique

### Arabe
- Interface en arabe
- Support RTL (right-to-left)
- Exemples culturellement adaptés

## 🔧 Configuration

### Variables d'Environnement

```bash
# LLM Cloud (optionnel)
OPENAI_API_KEY=sk-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx

# LLM Local (par défaut)
USE_LOCAL_LLM=true
OLLAMA_HOST=http://localhost:11434
LOCAL_MODEL=mistral

# RAG
CHROMA_DB_PATH=./data/chroma
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2

# Audio
STT_SERVICE=whisper  # ou google
TTS_SERVICE=gtts     # ou elevenlabs
AUDIO_LANGUAGE=fr

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## 📊 Curriculum Marocain

Le système couvre les programmes officiels:

### Tronc Commun
- Introduction à l'informatique
- Algorithmique de base
- Initiation à la programmation

### 1ère Année Bac
- Structures de données
- Programmation orientée objet
- Bases de données

### 2ème Année Bac
- Algorithmes avancés
- Développement web
- Projet final

## 🧪 Tests

```bash
# Tests backend
cd backend
pytest tests/ -v

# Tests frontend
cd frontend
npm test
```

## 📚 Documentation

- [Architecture Détaillée](docs/ARCHITECTURE.md)
- [Guide des Agents](docs/AGENTS.md)
- [Configuration RAG](docs/RAG.md)
- [Audio Setup](docs/AUDIO.md)
- [API Reference](docs/API.md)

## 🤝 Contribution

Les contributions sont les bienvenues! Surtout pour:
- Ajout de contenu pédagogique marocain
- Amélioration du support arabe
- Nouveaux exercices
- Tests et documentation

## 📄 Licence

MIT License

## 🙏 Remerciements

- Ministère de l'Éducation Nationale du Maroc
- Communauté open source
- Contributeurs de contenu pédagogique

## 📞 Support

- Issues GitHub
- Email: support@example.com
- Documentation: docs/
