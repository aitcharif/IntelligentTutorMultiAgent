"""Tutor Agent - Main teaching agent adapted for Moroccan students"""

from typing import Any, Dict, Optional
from loguru import logger

from ..core.base_agent import BaseAgent, AgentType, AgentCapability
from ..core.message import Message, MessageType
from ..core.context import ConversationContext


class TutorAgent(BaseAgent):
    """
    Tutor agent for personalized teaching
    Adapts to Moroccan education context and student level
    """

    def __init__(self, llm_client, agent_id: str = "tutor", language: str = "fr"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.TUTOR,
            capabilities=[
                AgentCapability.TEACH,
                AgentCapability.EXPLAIN,
                AgentCapability.PROVIDE_HINTS,
            ],
            language=language,
        )
        self.llm_client = llm_client

    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """Process student question and provide teaching response"""
        try:
            # Build context-aware prompt
            system_prompt = self._build_system_prompt(context)
            user_prompt = self._build_user_prompt(message, context)

            # Generate response
            response_text = await self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=2000,
            )

            return self.create_message(
                content=response_text,
                message_type=MessageType.RESPONSE,
                parent_message_id=message.id,
                language=message.language,
            )

        except Exception as e:
            return await self.on_error(e, context, message)

    async def handle_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        """Handle teaching task"""
        try:
            system_prompt = self._build_system_prompt(context)
            response = await self.llm_client.generate(
                prompt=task,
                system_prompt=system_prompt,
                temperature=0.7,
            )
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _build_system_prompt(self, context: ConversationContext) -> str:
        """Build system prompt with Moroccan context"""
        profile = context.student_profile
        lang = profile.language

        prompts = {
            "fr": f"""Tu es un professeur d'informatique expert spécialisé dans le système éducatif marocain.

Profil de l'élève:
- Niveau: {profile.curriculum_level}
- Style d'apprentissage: {profile.learning_style or 'Non spécifié'}
- Sujets d'intérêt: {', '.join(profile.subjects_of_interest) if profile.subjects_of_interest else 'Général'}

Contexte actuel:
- Sujet: {context.current_subject}
- Thème: {context.current_topic or 'Non spécifié'}

Tes responsabilités:
1. Adapter tes explications au curriculum marocain
2. Utiliser des exemples pertinents au contexte marocain
3. Être patient et encourageant
4. Fournir des explications claires et pédagogiques
5. Encourager la pensée critique

Ton ton doit être amical, professionnel et motivant.""",

            "ar": f"""أنت أستاذ خبير في علوم الحاسوب متخصص في النظام التعليمي المغربي.

ملف الطالب:
- المستوى: {profile.curriculum_level}
- أسلوب التعلم: {profile.learning_style or 'غير محدد'}
- المواضيع المفضلة: {', '.join(profile.subjects_of_interest) if profile.subjects_of_interest else 'عام'}

السياق الحالي:
- الموضوع: {context.current_subject}
- الدرس: {context.current_topic or 'غير محدد'}

مسؤولياتك:
1. تكييف شروحاتك مع المنهاج المغربي
2. استخدام أمثلة ملائمة للسياق المغربي
3. كن صبوراً ومشجعاً
4. قدم شروحات واضحة وتربوية
5. شجع التفكير النقدي

يجب أن تكون لهجتك ودية ومهنية ومحفزة."""
        }

        return prompts.get(lang, prompts["fr"])

    def _build_user_prompt(self, message: Message, context: ConversationContext) -> str:
        """Build user prompt with conversation history"""
        # Include recent context
        recent_messages = context.get_recent_messages(limit=5)
        history = ""

        if len(recent_messages) > 1:
            if message.language == "ar":
                history = "سياق المحادثة الأخير:\n"
            else:
                history = "Contexte de conversation récent:\n"

            for msg in recent_messages[:-1]:
                role = "Élève" if msg.sender_id != self.agent_id else "Professeur"
                history += f"{role}: {msg.content}\n"
            history += "\n"

        # Add RAG context if available
        rag_context = ""
        if context.retrieved_documents:
            if message.language == "ar":
                rag_context = "\nمعلومات مرجعية:\n"
            else:
                rag_context = "\nInformations de référence:\n"

            for doc in context.retrieved_documents[:3]:
                rag_context += f"- {doc.get('content', '')}\n"
            rag_context += "\n"

        if message.language == "ar":
            return f"{history}{rag_context}سؤال الطالب: {message.content}"
        else:
            return f"{history}{rag_context}Question de l'élève: {message.content}"
