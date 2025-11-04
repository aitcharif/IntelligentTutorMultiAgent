"""
Basic usage example of the IntelligentTutorMultiAgent system
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.agent import AgentConfig, AgentRole, AgentCapability
from src.core.context import StudentProfile
from src.agents import TutorAgent, EvaluatorAgent, ExerciseGeneratorAgent, ExplanationAgent
from src.orchestrator import AgentOrchestrator
from src.utils import load_config, setup_logger


async def main():
    """Main example function"""

    # Load configuration
    config = load_config()
    setup_logger(log_level=config.log_level)

    print("=== IntelligentTutorMultiAgent - Basic Usage ===\n")

    # Create orchestrator
    orchestrator = AgentOrchestrator()

    # Create and register agents
    print("Initializing agents...")

    # Tutor agent
    tutor_config = AgentConfig(
        agent_id="tutor_1",
        role=AgentRole.TUTOR,
        capabilities=[
            AgentCapability.ANSWER_QUESTIONS,
            AgentCapability.PROVIDE_FEEDBACK,
        ],
        llm_model=config.default_model,
    )
    tutor = TutorAgent(tutor_config)
    orchestrator.register_agent(tutor)

    # Explanation agent
    explanation_config = AgentConfig(
        agent_id="explainer_1",
        role=AgentRole.EXPLANATION_AGENT,
        capabilities=[AgentCapability.ANSWER_QUESTIONS],
        llm_model=config.default_model,
    )
    explainer = ExplanationAgent(explanation_config)
    orchestrator.register_agent(explainer)

    # Exercise generator
    exercise_config = AgentConfig(
        agent_id="exercise_gen_1",
        role=AgentRole.EXERCISE_GENERATOR,
        capabilities=[AgentCapability.GENERATE_CONTENT],
        llm_model=config.exercise_generator_model,
    )
    exercise_gen = ExerciseGeneratorAgent(exercise_config)
    orchestrator.register_agent(exercise_gen)

    # Evaluator agent
    evaluator_config = AgentConfig(
        agent_id="evaluator_1",
        role=AgentRole.EVALUATOR,
        capabilities=[
            AgentCapability.EVALUATE_RESPONSES,
            AgentCapability.PROVIDE_FEEDBACK,
        ],
        llm_model=config.evaluator_model,
    )
    evaluator = EvaluatorAgent(evaluator_config)
    orchestrator.register_agent(evaluator)

    print(f"✓ Registered {len(orchestrator.router.agents)} agents\n")

    # Create student profile
    student_profile = StudentProfile(
        student_id="student_123",
        name="Alice",
        learning_style="visual",
        interests=["mathematics", "physics", "programming"],
        learning_goals=["Master calculus", "Learn Python"],
    )

    # Create tutoring session
    session_id = "session_001"
    context = orchestrator.create_session(
        session_id=session_id,
        student_profile=student_profile,
        subject="Mathematics",
        topic="Calculus",
    )

    print(f"✓ Created session: {session_id}")
    print(f"  Student: {student_profile.name}")
    print(f"  Subject: {context.subject}")
    print(f"  Topic: {context.topic}\n")

    # Example 1: Ask a question
    print("=" * 50)
    print("Example 1: Student asks a question")
    print("=" * 50)

    question = "Qu'est-ce qu'une dérivée et pourquoi est-elle importante?"
    print(f"\nStudent: {question}\n")

    response = await orchestrator.process_student_query(session_id, question)
    print(f"Tutor: {response.content}\n")

    # Example 2: Request explanation with analogy
    print("=" * 50)
    print("Example 2: Request detailed explanation")
    print("=" * 50)

    from src.core.message import Message, MessageType

    explanation_request = Message(
        type=MessageType.QUERY,
        sender="student_123",
        content="Explique-moi les limites en mathématiques",
    )

    explanation_response = await explainer.process_message(explanation_request, context)
    if explanation_response:
        print(f"\nExplanation Agent: {explanation_response.content}\n")

    # Example 3: Generate exercises
    print("=" * 50)
    print("Example 3: Generate practice exercises")
    print("=" * 50)

    exercise_result = await exercise_gen.execute_task(
        task="Generate exercises on derivatives",
        context=context,
        topic="derivatives",
        difficulty="medium",
        count=3,
    )

    if exercise_result["success"]:
        print(f"\nExercises:\n{exercise_result['result']}\n")

    # Example 4: Evaluate student response
    print("=" * 50)
    print("Example 4: Evaluate student answer")
    print("=" * 50)

    question_text = "Quelle est la dérivée de x²?"
    student_answer = "La dérivée de x² est 2x"

    evaluation_result = await evaluator.execute_task(
        task="Evaluate student response",
        context=context,
        question=question_text,
        student_response=student_answer,
    )

    if evaluation_result["success"]:
        evaluation = evaluation_result["result"]
        print(f"\nQuestion: {question_text}")
        print(f"Student Answer: {student_answer}")
        print(f"\nEvaluation:\n{evaluation['feedback']}")
        print(f"\nScore: {evaluation['score']}/100\n")

    # Get session summary
    print("=" * 50)
    print("Session Summary")
    print("=" * 50)

    summary = orchestrator.get_session_summary(session_id)
    print(f"\nSession ID: {summary['session_id']}")
    print(f"Student: {summary['student_id']}")
    print(f"Subject: {summary['subject']}")
    print(f"Total Messages: {summary['message_count']}")
    print(f"Duration: {summary['created_at']} to {summary['updated_at']}\n")

    # Close session
    orchestrator.close_session(session_id)
    print("✓ Session closed\n")


if __name__ == "__main__":
    # Note: You need to set your API keys in .env file or environment variables
    print("Make sure you have set OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file!\n")

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease ensure:")
        print("1. You have created a .env file with your API keys")
        print("2. You have installed all dependencies: pip install -r requirements.txt")
