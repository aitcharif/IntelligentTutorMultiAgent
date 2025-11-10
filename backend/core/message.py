"""Message system for inter-agent communication"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field
import uuid


class MessageType(str, Enum):
    """Types of messages"""
    QUERY = "query"  # Student question
    RESPONSE = "response"  # Agent response
    TASK = "task"  # Task assignment
    FEEDBACK = "feedback"  # Evaluation feedback
    EXERCISE = "exercise"  # Exercise generation
    EXPLANATION = "explanation"  # Detailed explanation
    HINT = "hint"  # Hint for exercise
    EVALUATION = "evaluation"  # Evaluation request
    SYSTEM = "system"  # System message
    ERROR = "error"  # Error message


class Priority(str, Enum):
    """Message priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class Message(BaseModel):
    """Message exchanged between agents"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType
    sender_id: str  # Agent or user ID
    receiver_id: Optional[str] = None  # Specific agent or None for broadcast
    content: str
    language: str = "fr"  # fr, ar, en
    metadata: Dict[str, Any] = Field(default_factory=dict)
    priority: Priority = Priority.NORMAL
    timestamp: datetime = Field(default_factory=datetime.now)
    parent_message_id: Optional[str] = None  # For threading
    requires_response: bool = True
    processed: bool = False

    class Config:
        use_enum_values = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "language": self.language,
            "metadata": self.metadata,
            "priority": self.priority,
            "timestamp": self.timestamp.isoformat(),
            "parent_message_id": self.parent_message_id,
            "requires_response": self.requires_response,
            "processed": self.processed,
        }

    def mark_processed(self) -> None:
        """Mark message as processed"""
        self.processed = True


class MessageHistory(BaseModel):
    """History of messages in a conversation"""

    messages: List[Message] = Field(default_factory=list)
    max_size: int = 50

    def add(self, message: Message) -> None:
        """Add message to history"""
        self.messages.append(message)
        # Keep only recent messages
        if len(self.messages) > self.max_size:
            self.messages = self.messages[-self.max_size :]

    def get_recent(self, limit: int = 10) -> List[Message]:
        """Get recent messages"""
        return self.messages[-limit:]

    def get_by_type(self, message_type: MessageType) -> List[Message]:
        """Get messages by type"""
        return [msg for msg in self.messages if msg.type == message_type]

    def get_thread(self, parent_id: str) -> List[Message]:
        """Get message thread"""
        thread = []
        for msg in self.messages:
            if msg.parent_message_id == parent_id or msg.id == parent_id:
                thread.append(msg)
        return thread

    def clear(self) -> None:
        """Clear history"""
        self.messages.clear()
