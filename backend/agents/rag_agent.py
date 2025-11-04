"""RAG Agent - Retrieves relevant knowledge from database"""

from typing import Any, Dict, Optional, List
from ..core.base_agent import BaseAgent, AgentType, AgentCapability
from ..core.message import Message, MessageType
from ..core.context import ConversationContext


class RAGAgent(BaseAgent):
    """Agent for knowledge retrieval using RAG"""

    def __init__(self, retriever=None, agent_id: str = "rag", language: str = "fr"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.RAG,
            capabilities=[AgentCapability.RETRIEVE_KNOWLEDGE],
            language=language,
        )
        self.retriever = retriever

    async def process_message(
        self, message: Message, context: ConversationContext
    ) -> Optional[Message]:
        """Retrieve relevant documents"""
        try:
            if not self.retriever:
                return None

            results = await self.retriever.search(message.content, top_k=5)
            context.add_retrieved_docs(results)

            return self.create_message(
                content=f"Retrieved {len(results)} relevant documents",
                message_type=MessageType.SYSTEM,
                parent_message_id=message.id,
                language=message.language,
                metadata={"document_count": len(results)},
            )
        except Exception as e:
            return await self.on_error(e, context, message)

    async def handle_task(
        self, task: str, context: ConversationContext, **kwargs
    ) -> Dict[str, Any]:
        try:
            query = kwargs.get("query", task)
            top_k = kwargs.get("top_k", 5)

            if not self.retriever:
                return {"success": False, "error": "No retriever configured"}

            documents = await self.retriever.search(query, top_k=top_k)

            return {
                "success": True,
                "documents": documents,
                "count": len(documents),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
