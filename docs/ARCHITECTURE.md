# Architecture du Système Multi-Agent pour l'Enseignement Informatique

## Vue d'ensemble

Ce système utilise une architecture multi-agent orchestrée par un coordinateur central pour fournir un enseignement personnalisé d'informatique aux élèves marocains.

## Composants Principaux

### 1. Coordinateur Central (CoordinatorAgent)

**Rôle:** Cerveau du système qui orchestre tous les autres agents

**Responsabilités:**
- Analyser les requêtes des étudiants
- Déterminer l'intention (question, exercice, évaluation)
- Router vers les agents appropriés
- Combiner les réponses de plusieurs agents
- Maintenir la cohérence de la conversation

**Flow de traitement:**
```
Message Étudiant
    ↓
Analyse d'intention
    ↓
Routage intelligent
    ↓
┌───┴───┬────────┬─────────┐
↓       ↓        ↓         ↓
Agents spécialisés
```

### 2. Agent Tuteur (TutorAgent)

**Rôle:** Enseignement personnalisé

**Capacités:**
- Répondre aux questions techniques
- Adapter les explications au niveau de l'élève
- Utiliser des exemples du contexte marocain
- Support multilingue (français/arabe)

**Prompt System:**
- Intègre le profil de l'étudiant
- Adapte au curriculum marocain
- Utilise le contexte RAG si disponible

### 3. Agent Évaluateur (EvaluatorAgent)

**Rôle:** Évaluation et feedback

**Capacités:**
- Corriger les solutions des élèves
- Fournir un feedback constructif
- Identifier les points forts et faibles
- Suggérer des améliorations

**Température LLM:** 0.3 (précision maximale)

### 4. Agent Générateur (GeneratorAgent)

**Rôle:** Création de contenu pédagogique

**Capacités:**
- Générer des exercices adaptés
- Créer des quiz
- Adapter la difficulté au niveau
- Respecter le curriculum marocain

**Température LLM:** 0.9 (créativité)

### 5. Agent RAG (RAGAgent)

**Rôle:** Récupération de connaissances

**Capacités:**
- Rechercher dans la base de connaissances
- Embeddings multilingues
- Recherche sémantique
- Contexte pertinent pour les autres agents

## Architecture Technique

### Stack Backend

```
Python 3.10+
├── FastAPI (API REST)
├── Pydantic (Validation)
├── ChromaDB (Vector Store)
├── Ollama/OpenAI (LLM)
└── Loguru (Logging)
```

### Stack Frontend

```
HTML5 + CSS3 + Vanilla JS
├── Interface responsive
├── Chat en temps réel
└── Support RTL (arabe)
```

## Flux de Données

### 1. Question Simple

```
Étudiant: "Qu'est-ce qu'une variable?"
    ↓
Coordinateur (analyse: question)
    ↓
RAG Agent (récupère docs pertinents)
    ↓
Tutor Agent (génère réponse pédagogique)
    ↓
Réponse à l'étudiant
```

### 2. Demande d'Exercices

```
Étudiant: "Donne-moi des exercices sur les listes"
    ↓
Coordinateur (analyse: exercise_request)
    ↓
Generator Agent (crée exercices adaptés)
    ↓
Contexte: marque "awaiting_solution"
    ↓
Exercices envoyés à l'étudiant
```

### 3. Soumission de Solution

```
Étudiant: "Voici ma solution: [code]"
    ↓
Coordinateur (détecte: évaluation)
    ↓
Evaluator Agent (évalue le code)
    ↓
Contexte: efface "awaiting_solution"
    ↓
Feedback constructif à l'étudiant
```

## Gestion du Contexte

### ConversationContext

```python
{
    session_id: str
    student_profile: StudentProfile
    history: MessageHistory
    shared_memory: Dict
    retrieved_documents: List
    current_topic: str
    difficulty_level: str
}
```

### StudentProfile

```python
{
    student_id: str
    language: "fr" | "ar" | "en"
    curriculum_level: "tronc_commun" | "premiere_bac" | "deuxieme_bac"
    learning_style: str
    exercises_completed: int
    average_score: float
}
```

## Intégration LLM

### LLM Local (Ollama)

**Avantages:**
- Gratuit
- Privé
- Fonctionne hors ligne

**Modèles recommandés:**
- Mistral (général)
- Aya (meilleur pour l'arabe)
- CodeLlama (programmation)

### LLM Cloud (OpenAI)

**Avantages:**
- Qualité supérieure
- Pas de setup local

**Coût:** Variable selon utilisation

## Système RAG

### Pipeline

```
Question
    ↓
Embedding (multilingual-mpnet)
    ↓
Recherche ChromaDB (top_k=5)
    ↓
Documents pertinents
    ↓
Contexte enrichi pour LLM
```

### Base de Connaissances

```
data/knowledge_base/
├── cours/
│   ├── python_basics.md
│   ├── algorithms.md
│   └── data_structures.md
├── exercises/
│   ├── beginner/
│   ├── intermediate/
│   └── advanced/
└── curriculum/
    └── morocco_program.md
```

## Sécurité et Privacy

1. **Sessions isolées:** Chaque étudiant a sa propre session
2. **Données locales:** Option LLM local pour privacy totale
3. **Validation:** Toutes les entrées sont validées (Pydantic)
4. **Rate limiting:** À implémenter en production

## Scalabilité

### Actuel

- Sessions en mémoire
- SQLite pour persistance
- Agents synchrones

### Production

- Redis pour sessions
- PostgreSQL
- Agents asynchrones
- Load balancing
- Kubernetes

## Extensibilité

### Ajouter un Nouvel Agent

```python
class MyCustomAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__(
            agent_id="custom",
            agent_type=AgentType.CUSTOM,
            capabilities=[AgentCapability.CUSTOM]
        )

    async def process_message(self, message, context):
        # Implémentation

# Enregistrer
coordinator.register_agent(MyCustomAgent(llm_client))
```

### Ajouter une Langue

1. Ajouter la langue dans `supported_languages`
2. Ajouter les prompts dans chaque agent
3. Configurer TTS/STT
4. Mettre à jour le frontend

## Monitoring

### Métriques à Tracker

- Latence des réponses
- Qualité des réponses (feedback utilisateur)
- Utilisation par agent
- Sessions actives
- Taux d'erreur

### Logs

```python
# Loguru configuration
logger.info("Agent processing message")
logger.error("Error in coordinator")
```

## Roadmap

### Phase 1 (Actuelle)
- ✅ Architecture multi-agent
- ✅ Coordinateur central
- ✅ Support LLM local/cloud
- ✅ Interface web basique

### Phase 2
- [ ] RAG complet avec ChromaDB
- [ ] Audio (STT/TTS)
- [ ] Frontend React avancé
- [ ] Dashboard de progression

### Phase 3
- [ ] Mobile app
- [ ] Gamification
- [ ] Analytics avancés
- [ ] Certificats

## Performance

### Temps de Réponse Typiques

- Question simple: 2-5s (local), 1-3s (cloud)
- Génération exercices: 5-10s
- Évaluation: 3-7s

### Optimisations

1. Cache des prompts courants
2. Streaming des réponses
3. Batch processing
4. Connection pooling

## Déploiement

### Development

```bash
python -m api.main
```

### Production

```bash
uvicorn backend.api.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4
```

### Docker

```dockerfile
FROM python:3.10
COPY backend /app/backend
RUN pip install -r requirements.txt
CMD ["uvicorn", "backend.api.main:app"]
```

## Tests

```bash
# Unit tests
pytest backend/tests/

# Integration tests
pytest backend/tests/integration/

# Load tests
locust -f load_test.py
```

## Contribution

Voir CONTRIBUTING.md pour:
- Standards de code
- Process de review
- Guidelines de documentation
