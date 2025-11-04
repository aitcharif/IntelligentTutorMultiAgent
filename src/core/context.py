"""Conversation context management"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from .message import Message


class StudentProfile(BaseModel):
    """Student profile information"""

    student_id: str
    name: Optional[str] = None
    learning_style: Optional[str] = None  # visual, auditory, kinesthetic, etc.
    knowledge_level: Dict[str, str] = Field(default_factory=dict)  # subject -> level
    interests: List[str] = Field(default_factory=list)
    learning_goals: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ConversationContext(BaseModel):
    """Context for a tutoring conversation"""

    session_id: str
    student_profile: StudentProfile
    subject: Optional[str] = None
    topic: Optional[str] = None
    messages: List[Message] = Field(default_factory=list)
    shared_memory: Dict[str, Any] = Field(default_factory=dict)  # Shared data between agents
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation history"""
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_recent_messages(self, limit: int = 10) -> List[Message]:
        """Get the most recent messages"""
        return self.messages[-limit:]

    def get_messages_by_type(self, message_type: str) -> List[Message]:
        """Get all messages of a specific type"""
        return [msg for msg in self.messages if msg.type == message_type]

    def update_memory(self, key: str, value: Any) -> None:
        """Update shared memory"""
        self.shared_memory[key] = value
        self.updated_at = datetime.now()

    def get_memory(self, key: str, default: Any = None) -> Any:
        """Retrieve from shared memory"""
        return self.shared_memory.get(key, default)
