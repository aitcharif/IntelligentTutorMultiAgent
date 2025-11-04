"""Base agent class and interfaces"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from loguru import logger

from .message import Message, MessageType
from .context import ConversationContext


class AgentRole(str, Enum):
    """Roles that agents can play in the multi-agent system"""

    COORDINATOR = "coordinator"  # Coordinates other agents
    TUTOR = "tutor"  # Main tutoring agent
    KNOWLEDGE_BASE = "knowledge_base"  # Provides domain knowledge
    EVALUATOR = "evaluator"  # Evaluates student responses
    ADAPTER = "adapter"  # Adapts content to student level
    FEEDBACK_PROVIDER = "feedback_provider"  # Provides feedback
    EXERCISE_GENERATOR = "exercise_generator"  # Generates exercises
    EXPLANATION_AGENT = "explanation_agent"  # Provides explanations


class AgentCapability(str, Enum):
    """Capabilities that agents can have"""

    ANSWER_QUESTIONS = "answer_questions"
    GENERATE_CONTENT = "generate_content"
    EVALUATE_RESPONSES = "evaluate_responses"
    PROVIDE_FEEDBACK = "provide_feedback"
    ADAPT_DIFFICULTY = "adapt_difficulty"
    PLAN_CURRICULUM = "plan_curriculum"
    COORDINATE_AGENTS = "coordinate_agents"
    SEARCH_KNOWLEDGE = "search_knowledge"


class AgentConfig(BaseModel):
    """Configuration for an agent"""

    agent_id: str
    role: AgentRole
    capabilities: List[AgentCapability]
    llm_model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseAgent(ABC):
    """Base class for all agents in the system"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.agent_id = config.agent_id
        self.role = config.role
        self.capabilities = config.capabilities
        logger.info(f"Initializing agent: {self.agent_id} with role: {self.role}")

    @abstractmethod
    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """
        Process an incoming message and return a response

        Args:
            message: The incoming message
            context: The conversation context

        Returns:
            Optional response message
        """
        pass

    @abstractmethod
    async def execute_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a specific task

        Args:
            task: Task description
            context: Conversation context
            **kwargs: Additional parameters

        Returns:
            Task execution result
        """
        pass

    def can_handle(self, message: Message) -> bool:
        """
        Check if this agent can handle a given message

        Args:
            message: The message to check

        Returns:
            True if agent can handle the message
        """
        # Default implementation - can be overridden
        return True

    def create_message(
        self,
        content: str,
        message_type: MessageType,
        receiver: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        parent_message_id: Optional[str] = None,
    ) -> Message:
        """
        Create a message from this agent

        Args:
            content: Message content
            message_type: Type of message
            receiver: Optional receiver agent ID
            metadata: Optional metadata
            parent_message_id: Optional parent message ID for threading

        Returns:
            Created message
        """
        return Message(
            type=message_type,
            sender=self.agent_id,
            receiver=receiver,
            content=content,
            metadata=metadata or {},
            parent_message_id=parent_message_id,
        )

    async def on_error(self, error: Exception, context: ConversationContext) -> Message:
        """
        Handle errors that occur during processing

        Args:
            error: The error that occurred
            context: Conversation context

        Returns:
            Error message
        """
        logger.error(f"Error in agent {self.agent_id}: {str(error)}")
        return self.create_message(
            content=f"Une erreur s'est produite: {str(error)}",
            message_type=MessageType.ERROR,
            metadata={"error_type": type(error).__name__},
        )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.agent_id}, role={self.role})"

    def __repr__(self) -> str:
        return self.__str__()
