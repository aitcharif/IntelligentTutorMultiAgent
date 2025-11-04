"""Student-related data models"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PerformanceMetrics(BaseModel):
    """Student performance metrics"""

    subject: str
    total_sessions: int = 0
    total_questions: int = 0
    correct_answers: int = 0
    average_score: float = 0.0
    topics_covered: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.now)

    @property
    def accuracy(self) -> float:
        """Calculate answer accuracy"""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100


class LearningSession(BaseModel):
    """Individual learning session record"""

    session_id: str
    student_id: str
    subject: Optional[str] = None
    topic: Optional[str] = None
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    questions_asked: int = 0
    exercises_completed: int = 0
    average_score: Optional[float] = None
    notes: List[str] = Field(default_factory=list)

    @property
    def duration_minutes(self) -> float:
        """Calculate session duration in minutes"""
        if not self.end_time:
            return 0.0
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60


class Student(BaseModel):
    """Student profile and data"""

    student_id: str
    name: str
    email: Optional[str] = None
    grade_level: Optional[str] = None
    learning_style: Optional[str] = None  # visual, auditory, kinesthetic, reading/writing
    interests: List[str] = Field(default_factory=list)
    learning_goals: List[str] = Field(default_factory=list)
    preferred_subjects: List[str] = Field(default_factory=list)

    # Performance tracking
    performance_metrics: Dict[str, PerformanceMetrics] = Field(default_factory=dict)
    sessions: List[LearningSession] = Field(default_factory=list)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    last_active: datetime = Field(default_factory=datetime.now)
    total_study_time: float = 0.0  # in minutes

    def add_session(self, session: LearningSession) -> None:
        """Add a learning session"""
        self.sessions.append(session)
        self.last_active = datetime.now()

        if session.end_time:
            self.total_study_time += session.duration_minutes

    def update_performance(self, subject: str, metrics: PerformanceMetrics) -> None:
        """Update performance metrics for a subject"""
        self.performance_metrics[subject] = metrics
        self.last_active = datetime.now()

    def get_performance(self, subject: str) -> Optional[PerformanceMetrics]:
        """Get performance metrics for a subject"""
        return self.performance_metrics.get(subject)

    @property
    def total_sessions(self) -> int:
        """Get total number of sessions"""
        return len(self.sessions)
