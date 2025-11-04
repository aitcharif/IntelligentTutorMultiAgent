"""Agent for generating educational exercises and problems"""

from typing import Any, Dict, List, Optional
from loguru import logger

from ..core.agent import BaseAgent, AgentConfig, AgentRole, AgentCapability
from ..core.message import Message, MessageType
from ..core.context import ConversationContext
from .llm_client import create_llm_client, LLMClient


class ExerciseGeneratorAgent(BaseAgent):
    """Agent that generates educational exercises tailored to student level"""

    def __init__(self, config: AgentConfig, llm_client: Optional[LLMClient] = None):
        super().__init__(config)
        self.llm_client = llm_client or create_llm_client(
            provider="openai", model=config.llm_model
        )

    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """Process request for exercise generation"""
        if message.type != MessageType.TASK:
            return None

        if "exercise" not in message.content.lower() and "exercice" not in message.content.lower():
            return None

        try:
            exercises = await self.generate_exercises(
                topic=message.metadata.get("topic", context.topic or ""),
                difficulty=message.metadata.get("difficulty", "medium"),
                count=message.metadata.get("count", 3),
                context=context,
            )

            return self.create_message(
                content=exercises,
                message_type=MessageType.RESPONSE,
                receiver=message.sender,
                parent_message_id=message.id,
                metadata={"exercise_type": "generated"},
            )

        except Exception as e:
            logger.error(f"Error in exercise generator: {str(e)}")
            return await self.on_error(e, context)

    async def execute_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        """Execute exercise generation task"""
        try:
            topic = kwargs.get("topic", context.topic or "")
            difficulty = kwargs.get("difficulty", "medium")
            count = kwargs.get("count", 3)

            exercises = await self.generate_exercises(
                topic=topic, difficulty=difficulty, count=count, context=context
            )

            return {"success": True, "result": exercises, "count": count}

        except Exception as e:
            logger.error(f"Error executing exercise generation: {str(e)}")
            return {"success": False, "error": str(e)}

    async def generate_exercises(
        self,
        topic: str,
        difficulty: str = "medium",
        count: int = 3,
        context: Optional[ConversationContext] = None,
    ) -> str:
        """
        Generate educational exercises

        Args:
            topic: The topic for exercises
            difficulty: Difficulty level (easy, medium, hard)
            count: Number of exercises to generate
            context: Optional conversation context

        Returns:
            Generated exercises as formatted text
        """
        system_prompt = """Tu es un expert en pédagogie et création d'exercices éducatifs.
Tu crées des exercices adaptés au niveau de l'étudiant qui sont:
- Progressifs et bien structurés
- Engageants et pertinents
- Avec des objectifs d'apprentissage clairs
- Variés (QCM, problèmes, analyses, etc.)
"""

        # Build student context if available
        student_context = ""
        if context:
            profile = context.student_profile
            student_context = f"""
Profil de l'étudiant:
- Style d'apprentissage: {profile.learning_style or 'Non spécifié'}
- Niveau: {profile.knowledge_level.get(topic, 'Intermédiaire')}
- Intérêts: {', '.join(profile.interests) if profile.interests else 'Non spécifiés'}
"""

        difficulty_map = {
            "easy": "facile (débutant)",
            "medium": "moyen (intermédiaire)",
            "hard": "difficile (avancé)",
        }

        prompt = f"""
{student_context}

Génère {count} exercices sur le sujet suivant: {topic}
Niveau de difficulté: {difficulty_map.get(difficulty, difficulty)}

Format souhaité pour chaque exercice:

**Exercice N:**
[Type d'exercice]

**Énoncé:**
[Description claire de l'exercice]

**Objectif d'apprentissage:**
[Ce que l'étudiant doit apprendre]

**Indice (optionnel):**
[Un indice pour aider]

---

Assure-toi que les exercices sont:
1. Progressifs en difficulté
2. Variés dans leur format
3. Stimulants intellectuellement
4. Adaptés au niveau spécifié
"""

        exercises = await self.llm_client.generate(
            prompt=prompt, system_prompt=system_prompt, temperature=0.8  # Higher for creativity
        )

        return exercises

    async def generate_quiz(
        self,
        topic: str,
        num_questions: int = 5,
        question_type: str = "multiple_choice",
        context: Optional[ConversationContext] = None,
    ) -> Dict[str, Any]:
        """
        Generate a quiz on a specific topic

        Args:
            topic: The topic for the quiz
            num_questions: Number of questions
            question_type: Type of questions (multiple_choice, true_false, open_ended)
            context: Optional conversation context

        Returns:
            Generated quiz with questions and answers
        """
        system_prompt = """Tu es un expert en création de quiz éducatifs.
Génère des questions de quiz bien formulées avec des réponses claires."""

        prompt = f"""
Crée un quiz de {num_questions} questions sur le sujet: {topic}
Type de questions: {question_type}

Format pour chaque question:

Q1: [Question]
a) [Option 1]
b) [Option 2]
c) [Option 3]
d) [Option 4]

Réponse correcte: [lettre]
Explication: [Courte explication]

---
"""

        quiz_content = await self.llm_client.generate(
            prompt=prompt, system_prompt=system_prompt, temperature=0.7
        )

        return {
            "topic": topic,
            "num_questions": num_questions,
            "question_type": question_type,
            "content": quiz_content,
        }

    def can_handle(self, message: Message) -> bool:
        """Check if this agent can handle the message"""
        if message.type != MessageType.TASK:
            return False

        content_lower = message.content.lower()
        keywords = ["exercise", "exercice", "quiz", "problème", "problem", "practice"]
        return any(keyword in content_lower for keyword in keywords)
