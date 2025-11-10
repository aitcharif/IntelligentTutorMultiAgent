"""Generator Agent - Generates exercises and problems"""

from typing import Any, Dict, Optional
from ..core.base_agent import BaseAgent, AgentType, AgentCapability
from ..core.message import Message, MessageType
from ..core.context import ConversationContext


class GeneratorAgent(BaseAgent):
    """Agent for generating exercises"""

    def __init__(self, llm_client, agent_id: str = "generator", language: str = "fr"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.GENERATOR,
            capabilities=[AgentCapability.GENERATE_EXERCISES],
            language=language,
        )
        self.llm_client = llm_client

    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """Generate exercises based on request"""
        try:
            system_prompt = self._get_generation_prompt(context)
            user_prompt = f"Generate exercises for: {message.content}"

            exercises = await self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.9,
            )

            return self.create_message(
                content=exercises,
                message_type=MessageType.EXERCISE,
                parent_message_id=message.id,
                language=message.language,
            )
        except Exception as e:
            return await self.on_error(e, context, message)

    async def handle_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        try:
            system_prompt = self._get_generation_prompt(context)
            response = await self.llm_client.generate(
                prompt=task, system_prompt=system_prompt, temperature=0.9
            )
            return {"success": True, "exercises": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _get_generation_prompt(self, context: ConversationContext) -> str:
        lang = context.student_profile.language
        level = context.student_profile.curriculum_level

        prompts = {
            "fr": f"Tu es un générateur d'exercices pour le niveau {level} marocain. Crée des exercices adaptés.",
            "ar": f"أنت مولد تمارين للمستوى {level} المغربي. أنشئ تمارين مناسبة.",
        }
        return prompts.get(lang, prompts["fr"])
