"""Evaluator Agent - Evaluates student solutions and provides feedback"""

from typing import Any, Dict, Optional
from ..core.base_agent import BaseAgent, AgentType, AgentCapability
from ..core.message import Message, MessageType
from ..core.context import ConversationContext


class EvaluatorAgent(BaseAgent):
    """Agent for evaluating student work"""

    def __init__(self, llm_client, agent_id: str = "evaluator", language: str = "fr"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.EVALUATOR,
            capabilities=[AgentCapability.EVALUATE, AgentCapability.PROVIDE_HINTS],
            language=language,
        )
        self.llm_client = llm_client

    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """Evaluate student solution"""
        try:
            system_prompt = self._get_evaluation_prompt(context.student_profile.language)
            user_prompt = f"Exercise: {context.get_memory('current_exercise')}\n\nStudent Solution: {message.content}"

            evaluation = await self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,
            )

            return self.create_message(
                content=evaluation,
                message_type=MessageType.FEEDBACK,
                parent_message_id=message.id,
                language=message.language,
            )
        except Exception as e:
            return await self.on_error(e, context, message)

    async def handle_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        try:
            system_prompt = self._get_evaluation_prompt(context.student_profile.language)
            response = await self.llm_client.generate(
                prompt=task, system_prompt=system_prompt, temperature=0.3
            )
            return {"success": True, "evaluation": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _get_evaluation_prompt(self, language: str) -> str:
        prompts = {
            "fr": "Tu es un évaluateur pédagogique. Évalue la solution et fournis un feedback constructif.",
            "ar": "أنت مقيّم تربوي. قيّم الحل وقدم تغذية راجعة بناءة.",
        }
        return prompts.get(language, prompts["fr"])
