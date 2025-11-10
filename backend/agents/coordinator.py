"""
Central Coordinator Agent - Orchestrates all other agents
This is the brain of the system that routes requests and combines responses
"""

import asyncio
from typing import Any, Dict, List, Optional
from loguru import logger

from ..core.base_agent import BaseAgent, AgentType, AgentCapability
from ..core.message import Message, MessageType, Priority
from ..core.context import ConversationContext


class CoordinatorAgent(BaseAgent):
    """
    Central coordinator that orchestrates all agents

    Responsibilities:
    - Analyze student requests
    - Route to appropriate agents
    - Combine responses from multiple agents
    - Maintain conversation flow
    - Ensure response quality
    """

    def __init__(self, agent_id: str = "coordinator", language: str = "fr"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.COORDINATOR,
            capabilities=[
                AgentCapability.COORDINATE,
                AgentCapability.TEACH,
                AgentCapability.EXPLAIN,
            ],
            language=language,
        )
        self.registered_agents: Dict[str, BaseAgent] = {}
        logger.info("Central Coordinator initialized")

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the coordinator"""
        self.registered_agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.agent_id} ({agent.agent_type})")

    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent"""
        if agent_id in self.registered_agents:
            del self.registered_agents[agent_id]
            logger.info(f"Unregistered agent: {agent_id}")

    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """
        Process a message by routing to appropriate agents

        Flow:
        1. Analyze the request
        2. Determine which agents to involve
        3. Route to agents (parallel if possible)
        4. Combine and format responses
        5. Return final response
        """
        try:
            logger.info(f"Coordinator processing message: {message.id}")

            # Add message to context
            context.add_message(message)

            # Analyze request to determine intent
            intent = await self._analyze_intent(message, context)
            logger.debug(f"Detected intent: {intent}")

            # Route to appropriate agents
            if intent == "question":
                response = await self._handle_question(message, context)
            elif intent == "exercise_request":
                response = await self._handle_exercise_request(message, context)
            elif intent == "evaluation":
                response = await self._handle_evaluation(message, context)
            elif intent == "explanation":
                response = await self._handle_explanation(message, context)
            else:
                # Default: route to tutor
                response = await self._handle_question(message, context)

            if response:
                context.add_message(response)

            return response

        except Exception as e:
            logger.error(f"Error in coordinator: {str(e)}")
            return await self.on_error(e, context, message)

    async def handle_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        """Handle a specific coordination task"""
        try:
            task_type = kwargs.get("task_type", "general")

            if task_type == "multi_agent_query":
                # Query multiple agents and combine results
                results = await self._query_multiple_agents(task, context, **kwargs)
                return {"success": True, "results": results}

            elif task_type == "workflow":
                # Execute a multi-step workflow
                results = await self._execute_workflow(task, context, **kwargs)
                return {"success": True, "workflow_results": results}

            else:
                return {"success": False, "error": "Unknown task type"}

        except Exception as e:
            logger.error(f"Error in coordinator task: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _analyze_intent(
        self, message: Message, context: ConversationContext
    ) -> str:
        """
        Analyze message intent to route appropriately

        Intents:
        - question: General question needing answer
        - exercise_request: Student wants practice exercises
        - evaluation: Student submitting solution for evaluation
        - explanation: Needs detailed explanation
        - hint: Needs a hint for current problem
        """
        content_lower = message.content.lower()

        # Check for exercise request keywords
        exercise_keywords = {
            "fr": ["exercice", "pratique", "entraîne", "problème"],
            "ar": ["تمرين", "تطبيق", "مسألة"],
            "en": ["exercise", "practice", "problem"],
        }

        evaluation_keywords = {
            "fr": ["corriger", "évalue", "ma solution", "mon code"],
            "ar": ["صحح", "قيم", "حلي"],
            "en": ["correct", "evaluate", "my solution", "my code"],
        }

        explanation_keywords = {
            "fr": ["explique", "comment", "pourquoi", "qu'est-ce que"],
            "ar": ["اشرح", "كيف", "لماذا", "ما هو"],
            "en": ["explain", "how", "why", "what is"],
        }

        lang = message.language

        # Check for evaluation
        if any(keyword in content_lower for keyword in evaluation_keywords.get(lang, [])):
            return "evaluation"

        # Check for exercise request
        if any(keyword in content_lower for keyword in exercise_keywords.get(lang, [])):
            return "exercise_request"

        # Check for explanation
        if any(keyword in content_lower for keyword in explanation_keywords.get(lang, [])):
            return "explanation"

        # Check context for ongoing evaluation
        if context.get_memory("awaiting_solution"):
            return "evaluation"

        # Default to question
        return "question"

    async def _handle_question(
        self, message: Message, context: ConversationContext
    ) -> Message:
        """
        Handle a general question
        Uses: RAG Agent (for knowledge) + Tutor Agent (for response)
        """
        try:
            # Step 1: Retrieve relevant knowledge using RAG
            rag_agent = self._get_agent_by_type(AgentType.RAG)
            if rag_agent:
                logger.debug("Querying RAG agent for knowledge")
                rag_task_result = await rag_agent.handle_task(
                    task="retrieve",
                    context=context,
                    query=message.content,
                    top_k=5,
                )
                if rag_task_result.get("success"):
                    context.add_retrieved_docs(rag_task_result.get("documents", []))

            # Step 2: Generate response using Tutor
            tutor_agent = self._get_agent_by_type(AgentType.TUTOR)
            if tutor_agent:
                logger.debug("Routing to tutor agent")
                response = await tutor_agent.process_message(message, context)
                return response

            # Fallback if no tutor available
            return self.create_message(
                content=self._get_fallback_response(message.language),
                message_type=MessageType.RESPONSE,
                parent_message_id=message.id,
                language=message.language,
            )

        except Exception as e:
            logger.error(f"Error handling question: {str(e)}")
            return await self.on_error(e, context, message)

    async def _handle_exercise_request(
        self, message: Message, context: ConversationContext
    ) -> Message:
        """
        Handle exercise generation request
        Uses: Generator Agent
        """
        try:
            generator_agent = self._get_agent_by_type(AgentType.GENERATOR)
            if generator_agent:
                logger.debug("Routing to generator agent")
                response = await generator_agent.process_message(message, context)

                # Mark that we're awaiting a solution
                context.update_memory("awaiting_solution", True)
                context.update_memory("current_exercise", response.content)

                return response

            return self.create_message(
                content=self._get_no_generator_message(message.language),
                message_type=MessageType.RESPONSE,
                parent_message_id=message.id,
                language=message.language,
            )

        except Exception as e:
            logger.error(f"Error handling exercise request: {str(e)}")
            return await self.on_error(e, context, message)

    async def _handle_evaluation(
        self, message: Message, context: ConversationContext
    ) -> Message:
        """
        Handle solution evaluation
        Uses: Evaluator Agent + Tutor Agent (for feedback)
        """
        try:
            evaluator_agent = self._get_agent_by_type(AgentType.EVALUATOR)
            if evaluator_agent:
                logger.debug("Routing to evaluator agent")
                response = await evaluator_agent.process_message(message, context)

                # Clear awaiting solution flag
                context.update_memory("awaiting_solution", False)

                return response

            return self.create_message(
                content=self._get_no_evaluator_message(message.language),
                message_type=MessageType.RESPONSE,
                parent_message_id=message.id,
                language=message.language,
            )

        except Exception as e:
            logger.error(f"Error handling evaluation: {str(e)}")
            return await self.on_error(e, context, message)

    async def _handle_explanation(
        self, message: Message, context: ConversationContext
    ) -> Message:
        """
        Handle explanation request
        Uses: RAG Agent + Tutor Agent with detailed mode
        """
        # Similar to question but with more detail
        context.update_memory("explanation_mode", True)
        response = await self._handle_question(message, context)
        context.update_memory("explanation_mode", False)
        return response

    async def _query_multiple_agents(
        self, query: str, context: ConversationContext, **kwargs
    ) -> List[Dict[str, Any]]:
        """Query multiple agents in parallel"""
        agent_ids = kwargs.get("agent_ids", [])
        agents = [self.registered_agents[aid] for aid in agent_ids if aid in self.registered_agents]

        message = Message(
            sender_id=self.agent_id,
            type=MessageType.QUERY,
            content=query,
            language=context.student_profile.language,
        )

        tasks = [agent.process_message(message, context) for agent in agents]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        results = []
        for agent, response in zip(agents, responses):
            if isinstance(response, Exception):
                logger.error(f"Agent {agent.agent_id} error: {str(response)}")
            elif response:
                results.append({
                    "agent_id": agent.agent_id,
                    "response": response.content,
                    "metadata": response.metadata,
                })

        return results

    async def _execute_workflow(
        self, workflow_name: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        """Execute a multi-step workflow"""
        # Placeholder for workflow execution
        # Can implement specific workflows like:
        # - Complete lesson workflow
        # - Assessment workflow
        # - Remediation workflow
        return {"workflow": workflow_name, "status": "not_implemented"}

    def _get_agent_by_type(self, agent_type: AgentType) -> Optional[BaseAgent]:
        """Get first agent of specified type"""
        for agent in self.registered_agents.values():
            if agent.agent_type == agent_type and agent.is_active:
                return agent
        return None

    def _get_fallback_response(self, language: str) -> str:
        """Get fallback response when no agent available"""
        responses = {
            "fr": "Je suis désolé, je ne peux pas traiter votre demande pour le moment. "
                  "Pouvez-vous reformuler ou essayer plus tard?",
            "ar": "عذراً، لا أستطيع معالجة طلبك حالياً. "
                  "هل يمكنك إعادة الصياغة أو المحاولة لاحقاً؟",
            "en": "I'm sorry, I can't process your request at the moment. "
                  "Can you rephrase or try later?",
        }
        return responses.get(language, responses["fr"])

    def _get_no_generator_message(self, language: str) -> str:
        """Message when generator not available"""
        messages = {
            "fr": "Désolé, le générateur d'exercices n'est pas disponible actuellement.",
            "ar": "عذراً، مولد التمارين غير متاح حالياً.",
            "en": "Sorry, the exercise generator is not currently available.",
        }
        return messages.get(language, messages["fr"])

    def _get_no_evaluator_message(self, language: str) -> str:
        """Message when evaluator not available"""
        messages = {
            "fr": "Désolé, l'évaluateur n'est pas disponible actuellement.",
            "ar": "عذراً، المُقيّم غير متاح حالياً.",
            "en": "Sorry, the evaluator is not currently available.",
        }
        return messages.get(language, messages["fr"])

    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {
            "coordinator": {
                "id": self.agent_id,
                "active": self.is_active,
                "registered_agents": len(self.registered_agents),
            },
            "agents": []
        }

        for agent_id, agent in self.registered_agents.items():
            status["agents"].append({
                "id": agent_id,
                "type": agent.agent_type.value,
                "active": agent.is_active,
                "capabilities": [cap.value for cap in agent.capabilities],
            })

        return status
