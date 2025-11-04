# Architecture du Système Multi-Agent

## Vue d'ensemble

IntelligentTutorMultiAgent est un système de tutorat intelligent basé sur une architecture multi-agent utilisant des modèles de langage (LLM). Le système coordonne plusieurs agents spécialisés pour fournir une expérience d'apprentissage personnalisée et adaptative.

## Composants Principaux

### 1. Core Components (`src/core/`)

#### Agent Base (`agent.py`)
- `BaseAgent`: Classe abstraite de base pour tous les agents
- `AgentRole`: Énumération des rôles possibles (Tuteur, Évaluateur, etc.)
- `AgentCapability`: Capacités que peuvent posséder les agents
- `AgentConfig`: Configuration d'un agent

#### Message System (`message.py`)
- `Message`: Structure de message entre agents
- `MessageType`: Types de messages (Query, Response, Task, Feedback, etc.)
- Gestion de l'historique et du threading des conversations

#### Context Management (`context.py`)
- `ConversationContext`: Contexte d'une session de tutorat
- `StudentProfile`: Profil de l'étudiant
- Mémoire partagée entre agents

### 2. Orchestration Layer (`src/orchestrator/`)

#### Agent Orchestrator (`orchestrator.py`)
- Coordonne tous les agents du système
- Gère les sessions de tutorat
- Route les messages entre agents
- Maintient les contextes de conversation

#### Message Router (`routing.py`)
- `MessageRouter`: Routage intelligent des messages
- `RoutingStrategy`: Stratégies de routage
  - Direct: routage direct à un agent spécifique
  - Broadcast: diffusion à tous les agents
  - Capability-based: basé sur les capacités
  - Role-based: basé sur le rôle
  - Round-robin: distribution égale

### 3. Agent Implementations (`src/agents/`)

#### TutorAgent
**Rôle**: Agent tuteur principal
**Capacités**:
- Répondre aux questions
- Fournir des explications
- Adapter le contenu au niveau de l'étudiant

#### ExplanationAgent
**Rôle**: Spécialiste des explications détaillées
**Capacités**:
- Explications par concepts
- Explications étape par étape
- Explications par analogies

#### EvaluatorAgent
**Rôle**: Évaluation des réponses
**Capacités**:
- Évaluer les réponses des étudiants
- Fournir des feedbacks constructifs
- Calculer des scores de compréhension

#### ExerciseGeneratorAgent
**Rôle**: Génération d'exercices
**Capacités**:
- Générer des exercices adaptés
- Créer des quiz
- Ajuster la difficulté

### 4. LLM Integration (`src/agents/llm_client.py`)

Support pour plusieurs fournisseurs de LLM:
- **OpenAI**: GPT-4, GPT-3.5
- **Anthropic**: Claude 3

Interface abstraite permettant d'ajouter facilement d'autres fournisseurs.

### 5. Data Models (`src/models/`)

#### Student Model
- `Student`: Profil étudiant complet
- `LearningSession`: Session d'apprentissage
- `PerformanceMetrics`: Métriques de performance

### 6. Utilities (`src/utils/`)

- **Configuration**: Gestion de la configuration via `.env`
- **Logging**: Système de logging avec Loguru

## Flux de Données

```
┌─────────────┐
│   Student   │
│   Query     │
└──────┬──────┘
       │
       v
┌─────────────────────┐
│  Orchestrator       │
│  - Session Mgmt     │
│  - Message Routing  │
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│  Message Router     │
│  - Route Selection  │
│  - Agent Selection  │
└──────┬──────────────┘
       │
       v
┌─────────────────────────────────────┐
│         Active Agents               │
├────────────┬──────────┬─────────────┤
│   Tutor   │ Evaluator│  Exercise   │
│           │          │  Generator  │
└────────────┴──────────┴─────────────┘
       │
       v
┌─────────────────────┐
│   LLM Provider      │
│   (OpenAI/Claude)   │
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│   Response          │
│   Processing        │
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│   Student           │
│   Response          │
└─────────────────────┘
```

## Communication Inter-Agent

Les agents communiquent via un système de messages structurés:

1. **Message Structure**:
   - Type (Query, Response, Task, Feedback)
   - Sender (ID de l'agent émetteur)
   - Receiver (ID de l'agent destinataire)
   - Content (Contenu du message)
   - Metadata (Informations additionnelles)
   - Timestamp

2. **Message Flow**:
   - Étudiant → Orchestrateur
   - Orchestrateur → Router
   - Router → Agent(s) approprié(s)
   - Agent(s) → LLM
   - LLM → Agent(s)
   - Agent(s) → Orchestrateur
   - Orchestrateur → Étudiant

## Extensibilité

Le système est conçu pour être facilement extensible:

### Ajouter un Nouvel Agent

```python
from src.core.agent import BaseAgent, AgentConfig

class CustomAgent(BaseAgent):
    async def process_message(self, message, context):
        # Implémentation personnalisée
        pass

    async def execute_task(self, task, context, **kwargs):
        # Implémentation personnalisée
        pass
```

### Ajouter un Nouveau Fournisseur LLM

```python
from src.agents.llm_client import LLMClient

class CustomLLMClient(LLMClient):
    async def generate(self, prompt, system_prompt, **kwargs):
        # Implémentation personnalisée
        pass
```

### Ajouter une Nouvelle Stratégie de Routage

Ajouter dans `routing.py`:
```python
class RoutingStrategy(str, Enum):
    CUSTOM = "custom"

def _route_custom(self, message):
    # Implémentation personnalisée
    pass
```

## Configuration

Configuration via fichier `.env`:

```bash
# LLM API Keys
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Provider Selection
LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-4

# Agent Parameters
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=2000

# Logging
LOG_LEVEL=INFO
```

## Sécurité et Considérations

1. **API Keys**: Toujours utiliser des variables d'environnement
2. **Validation**: Valider toutes les entrées utilisateur
3. **Rate Limiting**: Implémenter des limites pour les appels LLM
4. **Privacy**: Anonymiser les données étudiants si nécessaire
5. **Error Handling**: Gestion robuste des erreurs

## Performance

- Communication asynchrone entre agents
- Traitement parallèle quand possible
- Cache des réponses fréquentes (à implémenter)
- Optimisation des prompts LLM

## Tests

Structure des tests:
- `tests/test_agents.py`: Tests des agents
- `tests/test_orchestrator.py`: Tests de l'orchestrateur
- `tests/test_routing.py`: Tests du routage

Utilisation de pytest avec support asyncio.

## Déploiement

Options de déploiement:
1. **API REST** (FastAPI): Voir `examples/rest_api.py`
2. **CLI**: Utilisation directe en ligne de commande
3. **WebSocket**: Pour interactions temps réel
4. **Containerization**: Docker (à venir)

## Évolutions Futures

- Support de davantage de LLM providers
- Système de mémoire à long terme
- Analytics et métriques avancées
- Interface web complète
- Support multilingue avancé
- Intégration de bases de connaissances externes
