"""Conversation context and student profile management"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from .message import MessageHistory, Message


class StudentProfile(BaseModel):
    """Student profile with Moroccan education context"""

    student_id: str
    name: Optional[str] = None
    language: str = "fr"  # fr, ar, en
    curriculum_level: str = "tronc_commun"  # tronc_commun, premiere_bac, deuxieme_bac

    # Learning preferences
    learning_style: Optional[str] = None  # visual, auditory, kinesthetic, reading
    preferred_difficulty: str = "medium"  # easy, medium, hard

    # Academic info
    subjects_of_interest: List[str] = Field(default_factory=list)
    strong_topics: List[str] = Field(default_factory=list)
    weak_topics: List[str] = Field(default_factory=list)
    learning_goals: List[str] = Field(default_factory=list)

    # Progress tracking
    exercises_completed: int = 0
    average_score: float = 0.0
    total_study_time: float = 0.0  # in minutes
    last_active: datetime = Field(default_factory=datetime.now)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def update_progress(self, score: float, time_spent: float) -> None:
        """Update student progress"""
        self.exercises_completed += 1
        # Calculate rolling average
        total_score = self.average_score * (self.exercises_completed - 1) + score
        self.average_score = total_score / self.exercises_completed
        self.total_study_time += time_spent
        self.last_active = datetime.now()


class ConversationContext(BaseModel):
    """Context for a teaching session"""

    session_id: str
    student_profile: StudentProfile

    # Current session info
    current_topic: Optional[str] = None
    current_subject: str = "informatique"
    difficulty_level: str = "medium"

    # Message history
    history: MessageHistory = Field(default_factory=MessageHistory)

    # Shared memory between agents
    shared_memory: Dict[str, Any] = Field(default_factory=dict)

    # RAG context
    retrieved_documents: List[Dict[str, Any]] = Field(default_factory=list)

    # Session state
    session_start: datetime = Field(default_factory=datetime.now)
    last_interaction: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

    # Moroccan context
    use_moroccan_examples: bool = True
    cultural_context: str = "moroccan"

    def add_message(self, message: Message) -> None:
        """Add message to conversation"""
        self.history.add(message)
        self.last_interaction = datetime.now()

    def get_recent_messages(self, limit: int = 10) -> List[Message]:
        """Get recent messages"""
        return self.history.get_recent(limit)

    def update_memory(self, key: str, value: Any) -> None:
        """Update shared memory"""
        self.shared_memory[key] = value
        self.last_interaction = datetime.now()

    def get_memory(self, key: str, default: Any = None) -> Any:
        """Get from shared memory"""
        return self.shared_memory.get(key, default)

    def add_retrieved_docs(self, docs: List[Dict[str, Any]]) -> None:
        """Add retrieved documents from RAG"""
        self.retrieved_documents = docs
        self.update_memory("last_rag_retrieval", datetime.now().isoformat())

    def get_context_summary(self) -> str:
        """Get a text summary of the context"""
        return f"""
Session: {self.session_id}
Étudiant: {self.student_profile.name or self.student_profile.student_id}
Niveau: {self.student_profile.curriculum_level}
Langue: {self.student_profile.language}
Sujet actuel: {self.current_subject} - {self.current_topic or 'Non spécifié'}
Difficulté: {self.difficulty_level}
Messages: {len(self.history.messages)}
Durée de session: {(self.last_interaction - self.session_start).total_seconds() / 60:.1f} minutes
        """.strip()

    def end_session(self) -> None:
        """End the current session"""
        self.is_active = False
        duration = (datetime.now() - self.session_start).total_seconds() / 60
        self.student_profile.update_progress(
            score=self.get_memory("session_average_score", 0.0),
            time_spent=duration
        )
