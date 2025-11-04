"""Agent for evaluating student responses and understanding"""

from typing import Any, Dict, Optional
from loguru import logger

from ..core.agent import BaseAgent, AgentConfig, AgentRole, AgentCapability
from ..core.message import Message, MessageType
from ..core.context import ConversationContext
from .llm_client import create_llm_client, LLMClient


class EvaluatorAgent(BaseAgent):
    """Agent that evaluates student responses and provides feedback"""

    def __init__(self, config: AgentConfig, llm_client: Optional[LLMClient] = None):
        super().__init__(config)
        self.llm_client = llm_client or create_llm_client(
            provider="openai", model=config.llm_model
        )

    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """Process and evaluate student response"""
        if message.type != MessageType.RESPONSE:
            return None

        try:
            evaluation = await self.evaluate_response(
                student_response=message.content,
                context=context,
                question=message.metadata.get("question", ""),
            )

            return self.create_message(
                content=evaluation["feedback"],
                message_type=MessageType.FEEDBACK,
                receiver=message.sender,
                parent_message_id=message.id,
                metadata=evaluation,
            )

        except Exception as e:
            logger.error(f"Error in evaluator agent: {str(e)}")
            return await self.on_error(e, context)

    async def execute_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        """Execute evaluation task"""
        try:
            student_response = kwargs.get("student_response", "")
            question = kwargs.get("question", "")

            evaluation = await self.evaluate_response(student_response, context, question)
            return {"success": True, "result": evaluation}

        except Exception as e:
            logger.error(f"Error executing evaluation: {str(e)}")
            return {"success": False, "error": str(e)}

    async def evaluate_response(
        self, student_response: str, context: ConversationContext, question: str = ""
    ) -> Dict[str, Any]:
        """
        Evaluate a student's response

        Args:
            student_response: The student's answer
            context: Conversation context
            question: The original question

        Returns:
            Evaluation results with feedback and scoring
        """
        system_prompt = """Tu es un évaluateur pédagogique expert.
Ton rôle est d'évaluer les réponses des étudiants de manière constructive et encourageante.

Pour chaque réponse, tu dois:
1. Identifier les points forts
2. Identifier les points à améliorer
3. Donner un score de compréhension (0-100)
4. Fournir des suggestions constructives

Ton feedback doit être:
- Constructif et encourageant
- Spécifique et actionnable
- Adapté au niveau de l'étudiant
"""

        prompt = f"""
Question: {question}

Réponse de l'étudiant: {student_response}

Fournis une évaluation détaillée au format suivant:

**Points forts:**
[Liste les points forts]

**Points à améliorer:**
[Liste les points à améliorer]

**Score de compréhension:** [0-100]

**Suggestions:**
[Suggestions constructives]
"""

        feedback = await self.llm_client.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for more consistent evaluation
        )

        # Extract score (simple parsing - can be enhanced)
        score = self._extract_score(feedback)

        return {
            "feedback": feedback,
            "score": score,
            "question": question,
            "student_response": student_response,
        }

    def _extract_score(self, feedback: str) -> int:
        """Extract numerical score from feedback text"""
        import re

        # Look for patterns like "Score: 75" or "Score de compréhension: 75"
        patterns = [
            r"score[:\s]+(\d+)",
            r"(\d+)\s*/\s*100",
            r"(\d+)%",
        ]

        for pattern in patterns:
            match = re.search(pattern, feedback.lower())
            if match:
                try:
                    score = int(match.group(1))
                    return min(100, max(0, score))  # Clamp between 0-100
                except ValueError:
                    continue

        # Default score if not found
        return 50

    def can_handle(self, message: Message) -> bool:
        """Check if this agent can handle the message"""
        return message.type in [MessageType.RESPONSE, MessageType.TASK]
