"""Main orchestrator for coordinating multiple agents"""

import asyncio
from typing import Any, Dict, List, Optional
from loguru import logger

from ..core.agent import BaseAgent, AgentRole
from ..core.message import Message, MessageType
from ..core.context import ConversationContext, StudentProfile
from .routing import MessageRouter, RoutingStrategy


class AgentOrchestrator:
    """Orchestrates multiple agents to provide intelligent tutoring"""

    def __init__(self):
        self.router = MessageRouter()
        self.active_contexts: Dict[str, ConversationContext] = {}
        logger.info("AgentOrchestrator initialized")

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the orchestrator"""
        self.router.register_agent(agent)

    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent"""
        self.router.unregister_agent(agent_id)

    def create_session(
        self,
        session_id: str,
        student_profile: StudentProfile,
        subject: Optional[str] = None,
        topic: Optional[str] = None,
    ) -> ConversationContext:
        """
        Create a new tutoring session

        Args:
            session_id: Unique session identifier
            student_profile: Student profile information
            subject: Optional subject being studied
            topic: Optional specific topic

        Returns:
            Created conversation context
        """
        context = ConversationContext(
            session_id=session_id,
            student_profile=student_profile,
            subject=subject,
            topic=topic,
        )
        self.active_contexts[session_id] = context
        logger.info(f"Created session: {session_id} for student: {student_profile.student_id}")
        return context

    def get_context(self, session_id: str) -> Optional[ConversationContext]:
        """Get an active conversation context"""
        return self.active_contexts.get(session_id)

    async def process_student_query(
        self, session_id: str, query: str, sender_id: str = "student"
    ) -> Message:
        """
        Process a query from a student

        Args:
            session_id: Session identifier
            query: Student's query
            sender_id: Sender identifier

        Returns:
            Response message
        """
        context = self.get_context(session_id)
        if not context:
            logger.error(f"Session not found: {session_id}")
            return Message(
                type=MessageType.ERROR,
                sender="orchestrator",
                content="Session non trouvée",
            )

        # Create student message
        student_message = Message(
            type=MessageType.QUERY,
            sender=sender_id,
            content=query,
        )
        context.add_message(student_message)

        # Route to coordinator agent first if available
        coordinator_agents = self.router.get_agents_by_role(AgentRole.COORDINATOR)
        if coordinator_agents:
            response = await self._process_with_coordinator(
                student_message, context, coordinator_agents[0]
            )
        else:
            # Fallback to capability-based routing
            response = await self._process_with_agents(student_message, context)

        if response:
            context.add_message(response)

        return response

    async def _process_with_coordinator(
        self, message: Message, context: ConversationContext, coordinator: BaseAgent
    ) -> Message:
        """Process message through coordinator agent"""
        try:
            logger.info(f"Processing message through coordinator: {coordinator.agent_id}")
            response = await coordinator.process_message(message, context)
            if response:
                return response
        except Exception as e:
            logger.error(f"Error in coordinator processing: {str(e)}")
            return await coordinator.on_error(e, context)

        # Return default response if coordinator doesn't provide one
        return Message(
            type=MessageType.RESPONSE,
            sender=coordinator.agent_id,
            content="Je n'ai pas pu traiter votre demande. Pouvez-vous reformuler?",
        )

    async def _process_with_agents(
        self, message: Message, context: ConversationContext
    ) -> Message:
        """Process message with multiple agents in parallel"""
        # Get relevant agents based on message type and context
        relevant_agents = self._select_relevant_agents(message, context)

        if not relevant_agents:
            logger.warning("No relevant agents found for message")
            return Message(
                type=MessageType.RESPONSE,
                sender="orchestrator",
                content="Aucun agent disponible pour traiter cette demande.",
            )

        # Process with all relevant agents
        tasks = [agent.process_message(message, context) for agent in relevant_agents]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter valid responses
        valid_responses = [r for r in responses if isinstance(r, Message) and r is not None]

        if not valid_responses:
            return Message(
                type=MessageType.RESPONSE,
                sender="orchestrator",
                content="Je n'ai pas pu générer une réponse appropriée.",
            )

        # Return the first valid response (can be enhanced with response ranking)
        return valid_responses[0]

    def _select_relevant_agents(
        self, message: Message, context: ConversationContext
    ) -> List[BaseAgent]:
        """Select agents relevant for processing the message"""
        # Simple selection logic - can be enhanced
        if message.type == MessageType.QUERY:
            # For queries, prefer tutor agents
            tutor_agents = self.router.get_agents_by_role(AgentRole.TUTOR)
            if tutor_agents:
                return tutor_agents

        # Default to all agents that can handle the message
        return [agent for agent in self.router.agents if agent.can_handle(message)]

    async def execute_task(
        self, session_id: str, task: str, agent_id: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a specific task

        Args:
            session_id: Session identifier
            task: Task description
            agent_id: Optional specific agent to use
            **kwargs: Additional parameters

        Returns:
            Task result
        """
        context = self.get_context(session_id)
        if not context:
            return {"error": "Session not found"}

        if agent_id:
            agent = self.router.get_agent(agent_id)
            if agent:
                return await agent.execute_task(task, context, **kwargs)
            return {"error": f"Agent not found: {agent_id}"}

        # Execute with first available agent
        if self.router.agents:
            return await self.router.agents[0].execute_task(task, context, **kwargs)

        return {"error": "No agents available"}

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of a tutoring session"""
        context = self.get_context(session_id)
        if not context:
            return {"error": "Session not found"}

        return {
            "session_id": session_id,
            "student_id": context.student_profile.student_id,
            "subject": context.subject,
            "topic": context.topic,
            "message_count": len(context.messages),
            "created_at": context.created_at.isoformat(),
            "updated_at": context.updated_at.isoformat(),
        }

    def close_session(self, session_id: str) -> bool:
        """Close a tutoring session"""
        if session_id in self.active_contexts:
            del self.active_contexts[session_id]
            logger.info(f"Session closed: {session_id}")
            return True
        return False
