# IntelligentTutorMultiAgent

IntelligentTutorMultiAgent est une plateforme de tutorat avancée qui utilise des technologies d'intelligence artificielle et une architecture multi-agent basée sur des LLM (Large Language Models) pour fournir des expériences d'apprentissage personnalisées et adaptatives.

## 🎯 Caractéristiques Principales

- **Architecture Multi-Agent**: Système coordonné d'agents spécialisés (Tuteur, Évaluateur, Générateur d'exercices, Explications)
- **Support Multi-LLM**: Compatible avec OpenAI (GPT-4) et Anthropic (Claude)
- **Personnalisation**: Adaptation au style d'apprentissage et niveau de chaque étudiant
- **Orchestration Intelligente**: Routage automatique des requêtes vers les agents appropriés
- **Extensible**: Architecture modulaire facile à étendre

## 🏗️ Architecture

Le système est composé de plusieurs couches:

### Agents Spécialisés

- **TutorAgent**: Agent tuteur principal pour interactions pédagogiques
- **ExplanationAgent**: Spécialiste des explications détaillées avec analogies
- **EvaluatorAgent**: Évaluation des réponses et feedback constructif
- **ExerciseGeneratorAgent**: Génération d'exercices adaptés au niveau

### Orchestration

- **AgentOrchestrator**: Coordonne les agents et gère les sessions
- **MessageRouter**: Route intelligemment les messages entre agents
- Support de multiples stratégies de routage

### Core Components

- **BaseAgent**: Classe de base pour tous les agents
- **Message System**: Communication structurée entre agents
- **Context Management**: Gestion du contexte de conversation

## 📦 Installation

### Prérequis

- Python 3.10 ou supérieur
- Clé API OpenAI ou Anthropic

### Installation des Dépendances

```bash
pip install -r requirements.txt
```

### Configuration

1. Copiez le fichier d'exemple:
```bash
cp config/.env.example .env
```

2. Éditez `.env` et ajoutez vos clés API:
```bash
OPENAI_API_KEY=your_openai_key_here
# ou
ANTHROPIC_API_KEY=your_anthropic_key_here

LLM_PROVIDER=openai  # ou anthropic
DEFAULT_MODEL=gpt-4
```

## 🚀 Utilisation

### Exemple Basique

```python
from src.core.agent import AgentConfig, AgentRole, AgentCapability
from src.core.context import StudentProfile
from src.agents import TutorAgent
from src.orchestrator import AgentOrchestrator

# Créer l'orchestrateur
orchestrator = AgentOrchestrator()

# Créer et enregistrer un agent tuteur
config = AgentConfig(
    agent_id="tutor_1",
    role=AgentRole.TUTOR,
    capabilities=[AgentCapability.ANSWER_QUESTIONS],
)
tutor = TutorAgent(config)
orchestrator.register_agent(tutor)

# Créer un profil étudiant
student = StudentProfile(
    student_id="student_123",
    name="Alice",
    learning_style="visual",
)

# Créer une session
context = orchestrator.create_session(
    session_id="session_001",
    student_profile=student,
    subject="Mathematics",
)

# Poser une question
response = await orchestrator.process_student_query(
    "session_001",
    "Qu'est-ce qu'une dérivée?"
)
print(response.content)
```

### Exemples Complets

#### 1. Utilisation Basique
```bash
python examples/basic_usage.py
```

#### 2. API REST
```bash
python examples/rest_api.py
```

Puis accédez à:
- API: http://localhost:8000
- Documentation interactive: http://localhost:8000/docs

### API REST Endpoints

```bash
# Créer une session
POST /sessions/create
{
  "session_id": "session_001",
  "student_profile": {
    "student_id": "student_123",
    "name": "Alice",
    "learning_style": "visual"
  }
}

# Poser une question
POST /query
{
  "session_id": "session_001",
  "query": "Qu'est-ce qu'une dérivée?"
}

# Générer des exercices
POST /exercises/generate
{
  "session_id": "session_001",
  "topic": "derivatives",
  "difficulty": "medium",
  "count": 3
}

# Évaluer une réponse
POST /evaluate
{
  "session_id": "session_001",
  "question": "Quelle est la dérivée de x²?",
  "student_response": "2x"
}
```

## 📚 Structure du Projet

```
IntelligentTutorMultiAgent/
├── src/
│   ├── core/              # Composants de base
│   │   ├── agent.py       # Classe BaseAgent
│   │   ├── message.py     # Système de messages
│   │   └── context.py     # Gestion du contexte
│   ├── agents/            # Implémentations d'agents
│   │   ├── tutor_agent.py
│   │   ├── evaluator_agent.py
│   │   ├── exercise_generator.py
│   │   ├── explanation_agent.py
│   │   └── llm_client.py  # Clients LLM
│   ├── orchestrator/      # Orchestration
│   │   ├── orchestrator.py
│   │   └── routing.py
│   ├── models/            # Modèles de données
│   └── utils/             # Utilitaires
├── examples/              # Exemples d'utilisation
├── tests/                 # Tests
├── config/                # Configuration
├── docs/                  # Documentation
└── requirements.txt       # Dépendances
```

## 🧪 Tests

```bash
pytest tests/
```

Avec couverture:
```bash
pytest --cov=src tests/
```

## 📖 Documentation

- [Architecture Détaillée](docs/ARCHITECTURE.md)
- [Guide des Agents](docs/AGENTS.md) (à venir)
- [API Reference](docs/API.md) (à venir)

## 🔧 Développement

### Ajouter un Nouvel Agent

1. Créer une nouvelle classe héritant de `BaseAgent`
2. Implémenter `process_message()` et `execute_task()`
3. Enregistrer l'agent avec l'orchestrateur

```python
from src.core.agent import BaseAgent

class MyCustomAgent(BaseAgent):
    async def process_message(self, message, context):
        # Votre logique ici
        pass

    async def execute_task(self, task, context, **kwargs):
        # Votre logique ici
        pass
```

### Ajouter un Nouveau Provider LLM

1. Créer une classe héritant de `LLMClient`
2. Implémenter la méthode `generate()`
3. L'ajouter à la factory `create_llm_client()`

## 🤝 Contribution

Les contributions sont les bienvenues! Consultez nos guidelines de contribution.

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- Votre Nom - Développeur Principal

## 🙏 Remerciements

- OpenAI pour l'API GPT
- Anthropic pour Claude
- La communauté open-source

## 📞 Support

Pour toute question ou problème:
- Ouvrir une issue sur GitHub
- Contact: your.email@example.com

## 🗺️ Roadmap

- [ ] Support de davantage de LLM providers (Cohere, Mistral)
- [ ] Interface web complète
- [ ] Système de mémoire à long terme
- [ ] Analytics et dashboards
- [ ] Support multilingue complet
- [ ] Intégration avec bases de connaissances externes
- [ ] Mode offline avec modèles locaux
- [ ] API webhooks pour intégrations 
