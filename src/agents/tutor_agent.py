"""Main tutor agent for educational interactions"""

from typing import Any, Dict, Optional
from loguru import logger

from ..core.agent import BaseAgent, AgentConfig, AgentRole, AgentCapability
from ..core.message import Message, MessageType
from ..core.context import ConversationContext
from .llm_client import create_llm_client, LLMClient


class TutorAgent(BaseAgent):
    """Main tutoring agent that interacts with students"""

    def __init__(self, config: AgentConfig, llm_client: Optional[LLMClient] = None):
        super().__init__(config)
        self.llm_client = llm_client or create_llm_client(
            provider="openai", model=config.llm_model
        )

    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """Process student message and provide tutoring response"""
        if message.type != MessageType.QUERY:
            return None

        try:
            # Build context-aware prompt
            system_prompt = self._build_system_prompt(context)
            user_prompt = self._build_user_prompt(message, context)

            # Generate response using LLM
            response_content = await self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )

            # Create response message
            return self.create_message(
                content=response_content,
                message_type=MessageType.RESPONSE,
                receiver=message.sender,
                parent_message_id=message.id,
            )

        except Exception as e:
            logger.error(f"Error in tutor agent: {str(e)}")
            return await self.on_error(e, context)

    async def execute_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        """Execute a tutoring task"""
        try:
            system_prompt = self._build_system_prompt(context)
            response = await self.llm_client.generate(
                prompt=task, system_prompt=system_prompt, **kwargs
            )
            return {"success": True, "result": response}
        except Exception as e:
            logger.error(f"Error executing task: {str(e)}")
            return {"success": False, "error": str(e)}

    def _build_system_prompt(self, context: ConversationContext) -> str:
        """Build system prompt based on context"""
        profile = context.student_profile
        prompt = f"""Tu es un tuteur pédagogique intelligent et bienveillant.

Profil de l'étudiant:
- Nom: {profile.name or 'Non spécifié'}
- Style d'apprentissage: {profile.learning_style or 'Non spécifié'}
- Intérêts: {', '.join(profile.interests) if profile.interests else 'Non spécifiés'}

"""
        if context.subject:
            prompt += f"Sujet actuel: {context.subject}\n"
        if context.topic:
            prompt += f"Thème actuel: {context.topic}\n"

        prompt += """
Tes responsabilités:
1. Répondre aux questions de manière claire et pédagogique
2. Adapter tes explications au niveau de l'étudiant
3. Encourager la réflexion critique et l'apprentissage actif
4. Fournir des exemples concrets et pertinents
5. Être patient et encourageant

Adopte un ton amical, professionnel et pédagogique.
"""
        return prompt

    def _build_user_prompt(self, message: Message, context: ConversationContext) -> str:
        """Build user prompt with conversation history"""
        # Include recent conversation history for context
        recent_messages = context.get_recent_messages(limit=5)
        history = ""

        if len(recent_messages) > 1:
            history = "Historique récent de la conversation:\n"
            for msg in recent_messages[:-1]:  # Exclude current message
                role = "Étudiant" if msg.sender == "student" else "Tuteur"
                history += f"{role}: {msg.content}\n"
            history += "\n"

        return f"{history}Question de l'étudiant: {message.content}"

    def can_handle(self, message: Message) -> bool:
        """Check if this agent can handle the message"""
        return message.type in [MessageType.QUERY, MessageType.TASK]
