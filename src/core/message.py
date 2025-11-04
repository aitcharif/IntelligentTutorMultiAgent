"""Message handling for inter-agent communication"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    """Types of messages that can be exchanged between agents"""

    QUERY = "query"  # Question or request
    RESPONSE = "response"  # Answer or result
    TASK = "task"  # Task assignment
    STATUS = "status"  # Status update
    ERROR = "error"  # Error notification
    FEEDBACK = "feedback"  # Feedback or evaluation
    COLLABORATION = "collaboration"  # Request for collaboration


class Message(BaseModel):
    """Message exchanged between agents"""

    id: str = Field(default_factory=lambda: f"msg_{datetime.now().timestamp()}")
    type: MessageType
    sender: str  # Agent ID who sent the message
    receiver: Optional[str] = None  # Agent ID who should receive (None = broadcast)
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    parent_message_id: Optional[str] = None  # For threading conversations

    class Config:
        use_enum_values = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "parent_message_id": self.parent_message_id,
        }
