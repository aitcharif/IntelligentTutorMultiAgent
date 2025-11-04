"""
Script de test rapide pour vérifier l'installation
Ce script ne nécessite PAS de clé API - il teste seulement les composants de base
"""

import sys
import os

print("=" * 60)
print("Test d'Installation - IntelligentTutorMultiAgent")
print("=" * 60)
print()

# Test 1: Version Python
print("1. Vérification de Python...")
print(f"   Version: {sys.version}")
print(f"   Chemin: {sys.executable}")
if sys.version_info >= (3, 10):
    print("   ✓ Version Python OK (>= 3.10)")
else:
    print("   ✗ ERREUR: Python 3.10+ requis")
    sys.exit(1)
print()

# Test 2: Imports des packages externes
print("2. Vérification des packages...")
required_packages = [
    "pydantic",
    "pydantic_settings",
    "loguru",
    "dotenv",
]

optional_packages = [
    "openai",
    "anthropic",
    "fastapi",
    "uvicorn",
    "pytest",
]

missing_required = []
missing_optional = []

for package in required_packages:
    try:
        if package == "dotenv":
            __import__("dotenv")
        elif package == "pydantic_settings":
            __import__("pydantic_settings")
        else:
            __import__(package)
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ✗ {package} (REQUIS)")
        missing_required.append(package)

for package in optional_packages:
    try:
        __import__(package)
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ⚠ {package} (optionnel)")
        missing_optional.append(package)

if missing_required:
    print(f"\n   ✗ ERREUR: Packages requis manquants: {', '.join(missing_required)}")
    print("   Installez avec: pip install -r requirements.txt")
    sys.exit(1)
print()

# Test 3: Import des modules du projet
print("3. Vérification des modules du projet...")
try:
    from src.core.agent import BaseAgent, AgentConfig, AgentRole, AgentCapability
    print("   ✓ src.core.agent")

    from src.core.message import Message, MessageType
    print("   ✓ src.core.message")

    from src.core.context import ConversationContext, StudentProfile
    print("   ✓ src.core.context")

    from src.orchestrator import AgentOrchestrator, MessageRouter
    print("   ✓ src.orchestrator")

    print("   ✓ Tous les modules principaux sont accessibles")
except ImportError as e:
    print(f"   ✗ ERREUR d'import: {e}")
    print("   Assurez-vous d'être dans le répertoire racine du projet")
    sys.exit(1)
print()

# Test 4: Création d'objets de base
print("4. Test de création d'objets...")
try:
    # Créer un profil étudiant
    student = StudentProfile(
        student_id="test_123",
        name="Alice Test",
        learning_style="visual",
        interests=["math", "science"],
    )
    print(f"   ✓ StudentProfile créé: {student.name}")

    # Créer un contexte
    context = ConversationContext(
        session_id="test_session_001",
        student_profile=student,
        subject="Mathematics",
    )
    print(f"   ✓ ConversationContext créé: {context.session_id}")

    # Créer un message
    message = Message(
        type=MessageType.QUERY,
        sender="student",
        content="Question de test",
    )
    print(f"   ✓ Message créé: {message.id}")

    # Ajouter message au contexte
    context.add_message(message)
    print(f"   ✓ Message ajouté au contexte ({len(context.messages)} messages)")

    # Test de la mémoire partagée
    context.update_memory("test_key", "test_value")
    retrieved = context.get_memory("test_key")
    assert retrieved == "test_value"
    print(f"   ✓ Mémoire partagée fonctionne")

    # Créer une configuration d'agent
    config = AgentConfig(
        agent_id="test_agent",
        role=AgentRole.TUTOR,
        capabilities=[AgentCapability.ANSWER_QUESTIONS],
    )
    print(f"   ✓ AgentConfig créé: {config.agent_id}")

    # Créer un orchestrateur
    orchestrator = AgentOrchestrator()
    print(f"   ✓ AgentOrchestrator créé")

except Exception as e:
    print(f"   ✗ ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# Test 5: Vérification des clés API
print("5. Vérification des clés API...")
has_openai = os.getenv("OPENAI_API_KEY")
has_anthropic = os.getenv("ANTHROPIC_API_KEY")

if has_openai:
    print(f"   ✓ OPENAI_API_KEY trouvée (longueur: {len(has_openai)})")
elif has_anthropic:
    print(f"   ✓ ANTHROPIC_API_KEY trouvée (longueur: {len(has_anthropic)})")
else:
    print("   ⚠ Aucune clé API trouvée")
    print("   Pour utiliser les LLM, configurez:")
    print("   - OPENAI_API_KEY pour OpenAI (GPT-4)")
    print("   - ANTHROPIC_API_KEY pour Anthropic (Claude)")
    print("   Dans un fichier .env ou comme variable d'environnement")
print()

# Test 6: Vérification de la structure du projet
print("6. Vérification de la structure du projet...")
required_dirs = ["src", "examples", "tests", "config", "docs"]
for dir_name in required_dirs:
    if os.path.isdir(dir_name):
        print(f"   ✓ {dir_name}/")
    else:
        print(f"   ✗ {dir_name}/ manquant")

required_files = [
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "src/core/agent.py",
    "src/orchestrator/orchestrator.py",
]
for file_name in required_files:
    if os.path.isfile(file_name):
        print(f"   ✓ {file_name}")
    else:
        print(f"   ✗ {file_name} manquant")
print()

# Résumé
print("=" * 60)
print("RÉSUMÉ")
print("=" * 60)
print()
print("✓ Installation de base: OK")
print("✓ Modules du projet: OK")
print("✓ Création d'objets: OK")
print()

if has_openai or has_anthropic:
    print("✓ Clé API configurée: OK")
    print()
    print("Vous pouvez maintenant:")
    print("  1. Exécuter les exemples: python examples/basic_usage.py")
    print("  2. Lancer l'API REST: python examples/rest_api.py")
    print("  3. Exécuter les tests: pytest tests/")
else:
    print("⚠ Clé API non configurée")
    print()
    print("Pour une utilisation complète:")
    print("  1. Copiez config/.env.example vers .env")
    print("  2. Ajoutez votre clé API dans .env")
    print("  3. Relancez ce script")
print()

if missing_optional:
    print("⚠ Packages optionnels manquants:")
    for pkg in missing_optional:
        print(f"    - {pkg}")
    print("  Pour une installation complète: pip install -r requirements.txt")
    print()

print("Pour plus d'informations: docs/TESTING_LOCAL.md")
print("=" * 60)
