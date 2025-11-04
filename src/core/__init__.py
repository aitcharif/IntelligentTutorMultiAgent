"""Core components for the multi-agent system"""

from .agent import BaseAgent, AgentRole, AgentCapability
from .message import Message, MessageType
from .context import ConversationContext

__all__ = [
    "BaseAgent",
    "AgentRole",
    "AgentCapability",
    "Message",
    "MessageType",
    "ConversationContext",
]
