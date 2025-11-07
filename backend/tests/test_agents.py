"""Tests for agents"""

import pytest
from backend.core.context import ConversationContext, StudentProfile
from backend.core.message import Message, MessageType


@pytest.fixture
def student_profile():
    """Create test student profile"""
    return StudentProfile(
        student_id="test_001",
        name="Ahmed Test",
        language="fr",
        curriculum_level="tronc_commun",
    )


@pytest.fixture
def conversation_context(student_profile):
    """Create test conversation context"""
    return ConversationContext(
        session_id="test_session",
        student_profile=student_profile,
    )


def test_message_creation():
    """Test message creation"""
    message = Message(
        sender_id="student",
        type=MessageType.QUERY,
        content="Test question",
        language="fr",
    )

    assert message.sender_id == "student"
    assert message.type == MessageType.QUERY
    assert message.content == "Test question"
    assert message.language == "fr"
    assert message.processed == False


def test_context_memory(conversation_context):
    """Test context shared memory"""
    conversation_context.update_memory("test_key", "test_value")
    assert conversation_context.get_memory("test_key") == "test_value"
    assert conversation_context.get_memory("nonexistent", "default") == "default"


def test_add_message_to_context(conversation_context):
    """Test adding message to context"""
    message = Message(
        sender_id="student",
        type=MessageType.QUERY,
        content="Test",
    )

    conversation_context.add_message(message)
    assert len(conversation_context.history.messages) == 1
    assert conversation_context.history.messages[0].content == "Test"


def test_student_profile_update():
    """Test student profile progress update"""
    profile = StudentProfile(
        student_id="test_002",
        name="Fatima",
    )

    initial_score = profile.average_score
    profile.update_progress(score=85.0, time_spent=30.0)

    assert profile.exercises_completed == 1
    assert profile.average_score == 85.0
    assert profile.total_study_time == 30.0
