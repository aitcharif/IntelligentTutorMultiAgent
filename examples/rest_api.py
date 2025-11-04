"""
REST API example for the IntelligentTutorMultiAgent system
This example shows how to expose the multi-agent system as a REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.agent import AgentConfig, AgentRole, AgentCapability
from src.core.context import StudentProfile
from src.agents import TutorAgent, EvaluatorAgent, ExerciseGeneratorAgent, ExplanationAgent
from src.orchestrator import AgentOrchestrator
from src.utils import load_config, setup_logger

# Initialize FastAPI app
app = FastAPI(
    title="IntelligentTutorMultiAgent API",
    description="REST API for multi-agent intelligent tutoring system",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator: Optional[AgentOrchestrator] = None


# Request/Response models
class StudentProfileRequest(BaseModel):
    student_id: str
    name: Optional[str] = None
    learning_style: Optional[str] = None
    interests: List[str] = []
    learning_goals: List[str] = []


class CreateSessionRequest(BaseModel):
    session_id: str
    student_profile: StudentProfileRequest
    subject: Optional[str] = None
    topic: Optional[str] = None


class QueryRequest(BaseModel):
    session_id: str
    query: str


class ExerciseRequest(BaseModel):
    session_id: str
    topic: str
    difficulty: str = "medium"
    count: int = 3


class EvaluationRequest(BaseModel):
    session_id: str
    question: str
    student_response: str


class ExplanationRequest(BaseModel):
    session_id: str
    concept: str
    depth: str = "medium"


@app.on_event("startup")
async def startup_event():
    """Initialize the multi-agent system on startup"""
    global orchestrator

    # Load configuration
    config = load_config()
    setup_logger(log_level=config.log_level)

    # Create orchestrator
    orchestrator = AgentOrchestrator()

    # Create and register agents
    # Tutor agent
    tutor_config = AgentConfig(
        agent_id="tutor_1",
        role=AgentRole.TUTOR,
        capabilities=[AgentCapability.ANSWER_QUESTIONS, AgentCapability.PROVIDE_FEEDBACK],
        llm_model=config.default_model,
    )
    orchestrator.register_agent(TutorAgent(tutor_config))

    # Explanation agent
    explanation_config = AgentConfig(
        agent_id="explainer_1",
        role=AgentRole.EXPLANATION_AGENT,
        capabilities=[AgentCapability.ANSWER_QUESTIONS],
        llm_model=config.default_model,
    )
    orchestrator.register_agent(ExplanationAgent(explanation_config))

    # Exercise generator
    exercise_config = AgentConfig(
        agent_id="exercise_gen_1",
        role=AgentRole.EXERCISE_GENERATOR,
        capabilities=[AgentCapability.GENERATE_CONTENT],
        llm_model=config.exercise_generator_model,
    )
    orchestrator.register_agent(ExerciseGeneratorAgent(exercise_config))

    # Evaluator agent
    evaluator_config = AgentConfig(
        agent_id="evaluator_1",
        role=AgentRole.EVALUATOR,
        capabilities=[
            AgentCapability.EVALUATE_RESPONSES,
            AgentCapability.PROVIDE_FEEDBACK,
        ],
        llm_model=config.evaluator_model,
    )
    orchestrator.register_agent(EvaluatorAgent(evaluator_config))

    print(f"✓ Initialized multi-agent system with {len(orchestrator.router.agents)} agents")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "IntelligentTutorMultiAgent API",
        "version": "0.1.0",
        "status": "running",
        "agents": len(orchestrator.router.agents) if orchestrator else 0,
    }


@app.post("/sessions/create")
async def create_session(request: CreateSessionRequest):
    """Create a new tutoring session"""
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    try:
        student_profile = StudentProfile(
            student_id=request.student_profile.student_id,
            name=request.student_profile.name,
            learning_style=request.student_profile.learning_style,
            interests=request.student_profile.interests,
            learning_goals=request.student_profile.learning_goals,
        )

        context = orchestrator.create_session(
            session_id=request.session_id,
            student_profile=student_profile,
            subject=request.subject,
            topic=request.topic,
        )

        return {
            "success": True,
            "session_id": request.session_id,
            "message": "Session created successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def process_query(request: QueryRequest):
    """Process a student query"""
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    try:
        response = await orchestrator.process_student_query(
            session_id=request.session_id, query=request.query
        )

        return {
            "success": True,
            "response": response.content,
            "message_id": response.id,
            "sender": response.sender,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/exercises/generate")
async def generate_exercises(request: ExerciseRequest):
    """Generate practice exercises"""
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    try:
        result = await orchestrator.execute_task(
            session_id=request.session_id,
            task="Generate exercises",
            agent_id="exercise_gen_1",
            topic=request.topic,
            difficulty=request.difficulty,
            count=request.count,
        )

        return {"success": result.get("success", False), "exercises": result.get("result", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate")
async def evaluate_response(request: EvaluationRequest):
    """Evaluate a student response"""
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    try:
        result = await orchestrator.execute_task(
            session_id=request.session_id,
            task="Evaluate response",
            agent_id="evaluator_1",
            question=request.question,
            student_response=request.student_response,
        )

        if result.get("success"):
            evaluation = result["result"]
            return {
                "success": True,
                "feedback": evaluation["feedback"],
                "score": evaluation["score"],
            }
        else:
            return {"success": False, "error": result.get("error", "Unknown error")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain")
async def explain_concept(request: ExplanationRequest):
    """Get detailed explanation of a concept"""
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    try:
        result = await orchestrator.execute_task(
            session_id=request.session_id,
            task=request.concept,
            agent_id="explainer_1",
            depth=request.depth,
        )

        return {"success": result.get("success", False), "explanation": result.get("result", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions/{session_id}/summary")
async def get_session_summary(session_id: str):
    """Get session summary"""
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    try:
        summary = orchestrator.get_session_summary(session_id)
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/sessions/{session_id}")
async def close_session(session_id: str):
    """Close a tutoring session"""
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    try:
        success = orchestrator.close_session(session_id)
        if success:
            return {"success": True, "message": "Session closed successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agents": len(orchestrator.router.agents) if orchestrator else 0}


if __name__ == "__main__":
    print("Starting IntelligentTutorMultiAgent REST API...")
    print("Make sure you have set your API keys in .env file!")
    print("\nAPI will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs\n")

    # Note: Install FastAPI and Uvicorn first:
    # pip install fastapi uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
