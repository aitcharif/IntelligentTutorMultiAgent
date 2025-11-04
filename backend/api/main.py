"""FastAPI Application - Main entry point"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

from ..core.config import get_settings
from ..core.context import ConversationContext, StudentProfile
from ..core.message import Message, MessageType
from ..agents import CoordinatorAgent, TutorAgent, EvaluatorAgent, GeneratorAgent, RAGAgent
from ..llm import create_llm_client

settings = get_settings()

app = FastAPI(
    title="Moroccan CS Education Multi-Agent API",
    description="Multi-agent system for teaching computer science to Moroccan students",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
coordinator: Optional[CoordinatorAgent] = None
active_sessions: dict = {}


@app.on_event("startup")
async def startup():
    """Initialize the multi-agent system"""
    global coordinator

    # Create LLM client
    llm_client = create_llm_client()

    # Create coordinator
    coordinator = CoordinatorAgent()

    # Register agents
    coordinator.register_agent(TutorAgent(llm_client))
    coordinator.register_agent(EvaluatorAgent(llm_client))
    coordinator.register_agent(GeneratorAgent(llm_client))
    coordinator.register_agent(RAGAgent())

    print("✓ Multi-agent system initialized")


class CreateSessionRequest(BaseModel):
    student_id: str
    name: Optional[str] = None
    language: str = "fr"
    curriculum_level: str = "tronc_commun"


class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: Optional[str] = "fr"


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "running",
        "system": "Moroccan CS Education Multi-Agent",
        "version": "1.0.0",
    }


@app.post("/api/sessions")
async def create_session(request: CreateSessionRequest):
    """Create a new learning session"""
    try:
        student_profile = StudentProfile(
            student_id=request.student_id,
            name=request.name,
            language=request.language,
            curriculum_level=request.curriculum_level,
        )

        context = ConversationContext(
            session_id=f"session_{request.student_id}_{len(active_sessions)}",
            student_profile=student_profile,
        )

        active_sessions[context.session_id] = context

        return {
            "success": True,
            "session_id": context.session_id,
            "message": "Session created successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Send a message and get response"""
    try:
        if request.session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        context = active_sessions[request.session_id]

        message = Message(
            sender_id="student",
            type=MessageType.QUERY,
            content=request.message,
            language=request.language or context.student_profile.language,
        )

        response = await coordinator.process_message(message, context)

        if response:
            return {
                "success": True,
                "response": response.content,
                "message_id": response.id,
            }
        else:
            return {"success": False, "error": "No response generated"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    context = active_sessions[session_id]
    return {
        "session_id": session_id,
        "student": context.student_profile.dict(),
        "message_count": len(context.history.messages),
        "is_active": context.is_active,
    }


@app.get("/api/status")
async def system_status():
    """Get system status"""
    if coordinator:
        return coordinator.get_system_status()
    return {"error": "System not initialized"}


if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
