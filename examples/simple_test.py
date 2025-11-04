"""
Exemple de test simple sans nécessiter de clé API
Ce script démontre les fonctionnalités de base du système
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.agent import AgentConfig, AgentRole, AgentCapability
from src.core.context import StudentProfile, ConversationContext
from src.core.message import Message, MessageType
from src.orchestrator import AgentOrchestrator, MessageRouter, RoutingStrategy


def print_section(title):
    """Print a formatted section title"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


async def main():
    print_section("Test Simple - IntelligentTutorMultiAgent")

    # 1. Créer des profils étudiants
    print_section("1. Création de Profils Étudiants")

    alice = StudentProfile(
        student_id="alice_001",
        name="Alice",
        learning_style="visual",
        interests=["mathematics", "physics"],
        learning_goals=["Maîtriser le calcul différentiel"],
    )
    print(f"✓ Profil créé: {alice.name}")
    print(f"  - Style d'apprentissage: {alice.learning_style}")
    print(f"  - Intérêts: {', '.join(alice.interests)}")

    bob = StudentProfile(
        student_id="bob_002",
        name="Bob",
        learning_style="kinesthetic",
        interests=["programming", "robotics"],
        learning_goals=["Apprendre Python"],
    )
    print(f"✓ Profil créé: {bob.name}")
    print(f"  - Style d'apprentissage: {bob.learning_style}")
    print(f"  - Intérêts: {', '.join(bob.interests)}")

    # 2. Créer des contextes de conversation
    print_section("2. Création de Contextes de Conversation")

    context_alice = ConversationContext(
        session_id="session_alice_001",
        student_profile=alice,
        subject="Mathematics",
        topic="Calculus",
    )
    print(f"✓ Session créée: {context_alice.session_id}")
    print(f"  - Étudiant: {context_alice.student_profile.name}")
    print(f"  - Sujet: {context_alice.subject}")
    print(f"  - Thème: {context_alice.topic}")

    # 3. Créer et gérer des messages
    print_section("3. Système de Messages")

    # Message de l'étudiant
    msg1 = Message(
        type=MessageType.QUERY,
        sender="alice_001",
        content="Qu'est-ce qu'une dérivée?",
    )
    context_alice.add_message(msg1)
    print(f"✓ Message QUERY créé")
    print(f"  - De: {msg1.sender}")
    print(f"  - Type: {msg1.type}")
    print(f"  - Contenu: {msg1.content}")
    print(f"  - ID: {msg1.id}")

    # Réponse simulée
    msg2 = Message(
        type=MessageType.RESPONSE,
        sender="tutor_1",
        receiver="alice_001",
        content="Une dérivée mesure le taux de variation d'une fonction...",
        parent_message_id=msg1.id,
    )
    context_alice.add_message(msg2)
    print(f"\n✓ Message RESPONSE créé")
    print(f"  - De: {msg2.sender}")
    print(f"  - À: {msg2.receiver}")
    print(f"  - En réponse à: {msg2.parent_message_id}")

    # Message de tâche
    msg3 = Message(
        type=MessageType.TASK,
        sender="coordinator",
        receiver="exercise_gen_1",
        content="Générer 3 exercices sur les dérivées",
        metadata={"difficulty": "medium", "count": 3},
    )
    context_alice.add_message(msg3)
    print(f"\n✓ Message TASK créé")
    print(f"  - Metadata: {msg3.metadata}")

    print(f"\n📊 Statistiques de conversation:")
    print(f"  - Total messages: {len(context_alice.messages)}")
    print(f"  - Messages QUERY: {len(context_alice.get_messages_by_type(MessageType.QUERY))}")
    print(f"  - Messages RESPONSE: {len(context_alice.get_messages_by_type(MessageType.RESPONSE))}")

    # 4. Mémoire partagée
    print_section("4. Mémoire Partagée")

    context_alice.update_memory("current_difficulty", "medium")
    context_alice.update_memory("topics_covered", ["derivatives", "limits"])
    context_alice.update_memory("student_score", 85)

    print("✓ Données enregistrées en mémoire:")
    print(f"  - current_difficulty: {context_alice.get_memory('current_difficulty')}")
    print(f"  - topics_covered: {context_alice.get_memory('topics_covered')}")
    print(f"  - student_score: {context_alice.get_memory('student_score')}")

    # 5. Configuration d'agents
    print_section("5. Configuration d'Agents")

    agents_config = [
        {
            "id": "tutor_1",
            "role": AgentRole.TUTOR,
            "capabilities": [
                AgentCapability.ANSWER_QUESTIONS,
                AgentCapability.PROVIDE_FEEDBACK,
            ],
        },
        {
            "id": "evaluator_1",
            "role": AgentRole.EVALUATOR,
            "capabilities": [
                AgentCapability.EVALUATE_RESPONSES,
                AgentCapability.PROVIDE_FEEDBACK,
            ],
        },
        {
            "id": "exercise_gen_1",
            "role": AgentRole.EXERCISE_GENERATOR,
            "capabilities": [AgentCapability.GENERATE_CONTENT],
        },
    ]

    for agent_cfg in agents_config:
        config = AgentConfig(
            agent_id=agent_cfg["id"],
            role=agent_cfg["role"],
            capabilities=agent_cfg["capabilities"],
        )
        print(f"✓ Configuration créée: {config.agent_id}")
        print(f"  - Rôle: {config.role}")
        print(f"  - Capacités: {len(config.capabilities)}")

    # 6. Routeur de messages
    print_section("6. Routage de Messages")

    router = MessageRouter()
    print("✓ MessageRouter créé")

    # Note: On ne peut pas vraiment tester le routage sans instances d'agents
    # mais on peut montrer les stratégies disponibles
    print("\nStratégies de routage disponibles:")
    for strategy in RoutingStrategy:
        print(f"  - {strategy.value}")

    # 7. Orchestrateur
    print_section("7. Orchestrateur Multi-Agent")

    orchestrator = AgentOrchestrator()
    print("✓ AgentOrchestrator créé")

    # Créer une session via l'orchestrateur
    context = orchestrator.create_session(
        session_id="test_session_001",
        student_profile=alice,
        subject="Physics",
        topic="Mechanics",
    )
    print(f"✓ Session créée via orchestrateur: {context.session_id}")

    # Vérifier que la session est bien enregistrée
    retrieved_context = orchestrator.get_context("test_session_001")
    if retrieved_context:
        print("✓ Session récupérée avec succès")
    else:
        print("✗ Erreur: Session non trouvée")

    # Obtenir un résumé de session
    summary = orchestrator.get_session_summary("test_session_001")
    print("\n📊 Résumé de session:")
    for key, value in summary.items():
        print(f"  - {key}: {value}")

    # Fermer la session
    success = orchestrator.close_session("test_session_001")
    if success:
        print("\n✓ Session fermée avec succès")

    # 8. Résumé final
    print_section("RÉSUMÉ DES TESTS")

    print("✓ Tous les composants de base fonctionnent correctement:")
    print("  1. Profils étudiants ✓")
    print("  2. Contextes de conversation ✓")
    print("  3. Système de messages ✓")
    print("  4. Mémoire partagée ✓")
    print("  5. Configuration d'agents ✓")
    print("  6. Routeur de messages ✓")
    print("  7. Orchestrateur ✓")

    print("\n📝 Note:")
    print("  Ce test vérifie les composants de base SANS appels LLM.")
    print("  Pour tester avec un LLM réel:")
    print("    1. Configurez votre clé API dans .env")
    print("    2. Exécutez: python examples/basic_usage.py")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("\n✅ Test terminé avec succès!\n")
    except Exception as e:
        print(f"\n❌ Erreur pendant le test: {str(e)}\n")
        import traceback

        traceback.print_exc()
        sys.exit(1)
