"""Agent specialized in providing detailed explanations"""

from typing import Any, Dict, Optional
from loguru import logger

from ..core.agent import BaseAgent, AgentConfig, AgentRole, AgentCapability
from ..core.message import Message, MessageType
from ..core.context import ConversationContext
from .llm_client import create_llm_client, LLMClient


class ExplanationAgent(BaseAgent):
    """Agent that provides detailed, pedagogical explanations"""

    def __init__(self, config: AgentConfig, llm_client: Optional[LLMClient] = None):
        super().__init__(config)
        self.llm_client = llm_client or create_llm_client(
            provider="openai", model=config.llm_model
        )

    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """Process request for explanation"""
        if message.type != MessageType.QUERY:
            return None

        # Check if message requests explanation
        if not self._is_explanation_request(message.content):
            return None

        try:
            explanation = await self.explain_concept(
                concept=message.content, context=context, depth=message.metadata.get("depth", "medium")
            )

            return self.create_message(
                content=explanation,
                message_type=MessageType.RESPONSE,
                receiver=message.sender,
                parent_message_id=message.id,
                metadata={"explanation_type": "concept"},
            )

        except Exception as e:
            logger.error(f"Error in explanation agent: {str(e)}")
            return await self.on_error(e, context)

    async def execute_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        """Execute explanation task"""
        try:
            depth = kwargs.get("depth", "medium")
            explanation_type = kwargs.get("type", "concept")

            if explanation_type == "concept":
                result = await self.explain_concept(task, context, depth)
            elif explanation_type == "step_by_step":
                result = await self.explain_step_by_step(task, context)
            elif explanation_type == "analogy":
                result = await self.explain_with_analogy(task, context)
            else:
                result = await self.explain_concept(task, context, depth)

            return {"success": True, "result": result, "type": explanation_type}

        except Exception as e:
            logger.error(f"Error executing explanation: {str(e)}")
            return {"success": False, "error": str(e)}

    async def explain_concept(
        self, concept: str, context: ConversationContext, depth: str = "medium"
    ) -> str:
        """
        Provide detailed explanation of a concept

        Args:
            concept: The concept to explain
            context: Conversation context
            depth: Explanation depth (simple, medium, detailed)

        Returns:
            Detailed explanation
        """
        profile = context.student_profile

        depth_instructions = {
            "simple": "Utilise un langage simple et des exemples concrets. Évite les termes techniques complexes.",
            "medium": "Fournis une explication équilibrée avec des exemples et quelques détails techniques.",
            "detailed": "Fournis une explication approfondie avec des détails techniques, des exemples multiples et des références.",
        }

        system_prompt = f"""Tu es un expert pédagogue qui excelle dans l'explication de concepts complexes.

Profil de l'étudiant:
- Style d'apprentissage: {profile.learning_style or 'Non spécifié'}
- Intérêts: {', '.join(profile.interests) if profile.interests else 'Non spécifiés'}

{depth_instructions.get(depth, depth_instructions["medium"])}

Structure tes explications de manière claire:
1. Définition simple
2. Contexte et importance
3. Exemples concrets
4. Points clés à retenir
5. Liens avec d'autres concepts (si pertinent)
"""

        prompt = f"Explique le concept suivant: {concept}"

        explanation = await self.llm_client.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=self.config.max_tokens,
        )

        return explanation

    async def explain_step_by_step(
        self, process: str, context: ConversationContext
    ) -> str:
        """
        Provide step-by-step explanation of a process or problem

        Args:
            process: The process or problem to explain
            context: Conversation context

        Returns:
            Step-by-step explanation
        """
        system_prompt = """Tu es un expert dans les explications étape par étape.

Décompose les processus ou problèmes en étapes claires et logiques:
- Numéro chaque étape
- Explique pourquoi chaque étape est nécessaire
- Fournis des exemples ou visualisations quand c'est utile
- Assure la cohérence entre les étapes
- Inclus des vérifications ou points d'attention
"""

        prompt = f"""Explique étape par étape le processus ou problème suivant:

{process}

Format attendu:
**Étape 1: [Titre]**
[Explication détaillée]
Pourquoi cette étape: [Raison]

**Étape 2: [Titre]**
...
"""

        explanation = await self.llm_client.generate(
            prompt=prompt, system_prompt=system_prompt, temperature=0.6
        )

        return explanation

    async def explain_with_analogy(
        self, concept: str, context: ConversationContext
    ) -> str:
        """
        Explain using analogies and metaphors

        Args:
            concept: The concept to explain
            context: Conversation context

        Returns:
            Explanation using analogies
        """
        profile = context.student_profile
        interests = profile.interests

        system_prompt = f"""Tu es un maître des analogies pédagogiques.

Utilise des analogies créatives et pertinentes pour expliquer des concepts.
{f"Prends en compte les intérêts de l'étudiant: {', '.join(interests)}" if interests else ""}

Structure:
1. Présentation du concept
2. Analogie principale détaillée
3. Correspondances claires entre l'analogie et le concept
4. Limites de l'analogie
5. Conclusion avec le concept réel
"""

        prompt = f"Explique ce concept en utilisant une ou plusieurs analogies: {concept}"

        explanation = await self.llm_client.generate(
            prompt=prompt, system_prompt=system_prompt, temperature=0.8  # Higher for creativity
        )

        return explanation

    def _is_explanation_request(self, content: str) -> bool:
        """Check if message requests an explanation"""
        explanation_keywords = [
            "explique",
            "explain",
            "comment",
            "how",
            "pourquoi",
            "why",
            "qu'est-ce que",
            "what is",
            "c'est quoi",
            "définition",
            "definition",
        ]

        content_lower = content.lower()
        return any(keyword in content_lower for keyword in explanation_keywords)

    def can_handle(self, message: Message) -> bool:
        """Check if this agent can handle the message"""
        if message.type != MessageType.QUERY:
            return False
        return self._is_explanation_request(message.content)
