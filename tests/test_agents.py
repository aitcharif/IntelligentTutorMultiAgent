"""Tests for agent implementations"""

import pytest
from src.core.agent import AgentConfig, AgentRole, AgentCapability
from src.core.context import ConversationContext, StudentProfile
from src.core.message import Message, MessageType


@pytest.fixture
def student_profile():
    """Create a test student profile"""
    return StudentProfile(
        student_id="test_student",
        name="Test Student",
        learning_style="visual",
        interests=["math", "science"],
    )


@pytest.fixture
def conversation_context(student_profile):
    """Create a test conversation context"""
    return ConversationContext(
        session_id="test_session", student_profile=student_profile, subject="Mathematics"
    )


def test_agent_config():
    """Test agent configuration"""
    config = AgentConfig(
        agent_id="test_agent",
        role=AgentRole.TUTOR,
        capabilities=[AgentCapability.ANSWER_QUESTIONS],
        llm_model="gpt-4",
    )

    assert config.agent_id == "test_agent"
    assert config.role == AgentRole.TUTOR
    assert AgentCapability.ANSWER_QUESTIONS in config.capabilities


def test_message_creation():
    """Test message creation"""
    message = Message(
        type=MessageType.QUERY,
        sender="student_1",
        receiver="tutor_1",
        content="What is calculus?",
    )

    assert message.type == MessageType.QUERY
    assert message.sender == "student_1"
    assert message.receiver == "tutor_1"
    assert message.content == "What is calculus?"


def test_conversation_context(conversation_context):
    """Test conversation context"""
    assert conversation_context.session_id == "test_session"
    assert conversation_context.subject == "Mathematics"

    # Add message
    message = Message(type=MessageType.QUERY, sender="student", content="Test question")
    conversation_context.add_message(message)

    assert len(conversation_context.messages) == 1
    assert conversation_context.messages[0].content == "Test question"


def test_shared_memory(conversation_context):
    """Test shared memory functionality"""
    conversation_context.update_memory("test_key", "test_value")
    assert conversation_context.get_memory("test_key") == "test_value"
    assert conversation_context.get_memory("nonexistent", "default") == "default"


# Note: Tests requiring LLM API calls would need mocking
# Here's an example structure:

"""
@pytest.mark.asyncio
async def test_tutor_agent(conversation_context):
    # Test would require mocking LLM client
    from src.agents import TutorAgent

    config = AgentConfig(
        agent_id="tutor_test",
        role=AgentRole.TUTOR,
        capabilities=[AgentCapability.ANSWER_QUESTIONS],
    )

    # Would need to inject mock LLM client
    agent = TutorAgent(config)

    # Test agent methods with mocked responses
    pass
"""
