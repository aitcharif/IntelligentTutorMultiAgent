"""Base agent class for all specialized agents"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from loguru import logger

from .message import Message, MessageType, Priority
from .context import ConversationContext


class AgentType(str, Enum):
    """Types of agents in the system"""
    COORDINATOR = "coordinator"
    TUTOR = "tutor"
    EVALUATOR = "evaluator"
    GENERATOR = "generator"
    RAG = "rag"
    LANGUAGE = "language"
    AUDIO = "audio"


class AgentCapability(str, Enum):
    """Capabilities that agents can have"""
    TEACH = "teach"
    EVALUATE = "evaluate"
    GENERATE_EXERCISES = "generate_exercises"
    RETRIEVE_KNOWLEDGE = "retrieve_knowledge"
    TRANSLATE = "translate"
    PROCESS_AUDIO = "process_audio"
    COORDINATE = "coordinate"
    PROVIDE_HINTS = "provide_hints"
    EXPLAIN = "explain"


class BaseAgent(ABC):
    """Base class for all agents"""

    def __init__(
        self,
        agent_id: str,
        agent_type: AgentType,
        capabilities: List[AgentCapability],
        language: str = "fr",
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.language = language
        self.is_active = True

        logger.info(
            f"Agent initialized: {agent_id} (type: {agent_type}, "
            f"capabilities: {len(capabilities)})"
        )

    @abstractmethod
    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """
        Process an incoming message

        Args:
            message: The message to process
            context: Conversation context

        Returns:
            Response message or None
        """
        pass

    @abstractmethod
    async def handle_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        """
        Handle a specific task

        Args:
            task: Task description
            context: Conversation context
            **kwargs: Additional parameters

        Returns:
            Task result
        """
        pass

    def can_handle(self, message: Message, required_capability: AgentCapability) -> bool:
        """
        Check if agent can handle a message

        Args:
            message: Message to check
            required_capability: Required capability

        Returns:
            True if agent can handle the message
        """
        return (
            self.is_active
            and required_capability in self.capabilities
            and (message.language == self.language or AgentCapability.TRANSLATE in self.capabilities)
        )

    def create_message(
        self,
        content: str,
        message_type: MessageType,
        receiver_id: Optional[str] = None,
        parent_message_id: Optional[str] = None,
        language: str = None,
        priority: Priority = Priority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """
        Create a message from this agent

        Args:
            content: Message content
            message_type: Type of message
            receiver_id: Receiver agent ID
            parent_message_id: Parent message ID for threading
            language: Message language
            priority: Message priority
            metadata: Additional metadata

        Returns:
            Created message
        """
        return Message(
            sender_id=self.agent_id,
            type=message_type,
            content=content,
            receiver_id=receiver_id,
            parent_message_id=parent_message_id,
            language=language or self.language,
            priority=priority,
            metadata=metadata or {},
        )

    async def on_error(
        self, error: Exception, context: ConversationContext, message: Optional[Message] = None
    ) -> Message:
        """
        Handle errors

        Args:
            error: The error that occurred
            context: Conversation context
            message: Original message if available

        Returns:
            Error message
        """
        logger.error(f"Error in agent {self.agent_id}: {str(error)}")

        error_content = self._get_localized_error(error, context.student_profile.language)

        return self.create_message(
            content=error_content,
            message_type=MessageType.ERROR,
            parent_message_id=message.id if message else None,
            language=context.student_profile.language,
            metadata={"error_type": type(error).__name__, "error_message": str(error)},
        )

    def _get_localized_error(self, error: Exception, language: str) -> str:
        """Get localized error message"""
        error_messages = {
            "fr": "Désolé, une erreur s'est produite. Pouvez-vous reformuler votre question?",
            "ar": "عذراً، حدث خطأ. هل يمكنك إعادة صياغة سؤالك؟",
            "en": "Sorry, an error occurred. Can you rephrase your question?",
        }
        return error_messages.get(language, error_messages["fr"])

    def activate(self) -> None:
        """Activate the agent"""
        self.is_active = True
        logger.info(f"Agent {self.agent_id} activated")

    def deactivate(self) -> None:
        """Deactivate the agent"""
        self.is_active = False
        logger.info(f"Agent {self.agent_id} deactivated")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.agent_id}, type={self.agent_type})"

    def __repr__(self) -> str:
        return self.__str__()
