"""Message routing strategies for multi-agent communication"""

from enum import Enum
from typing import List, Optional
from loguru import logger

from ..core.agent import BaseAgent, AgentCapability
from ..core.message import Message, MessageType


class RoutingStrategy(str, Enum):
    """Strategies for routing messages to agents"""

    BROADCAST = "broadcast"  # Send to all agents
    CAPABILITY_BASED = "capability_based"  # Route based on agent capabilities
    ROLE_BASED = "role_based"  # Route based on agent role
    DIRECT = "direct"  # Direct routing to specific agent
    ROUND_ROBIN = "round_robin"  # Distribute equally
    PRIORITY_BASED = "priority_based"  # Based on priority rules


class MessageRouter:
    """Routes messages to appropriate agents"""

    def __init__(self):
        self.agents: List[BaseAgent] = []
        self.round_robin_index = 0
        logger.info("MessageRouter initialized")

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the router"""
        self.agents.append(agent)
        logger.info(f"Agent registered: {agent.agent_id} (role: {agent.role})")

    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent"""
        self.agents = [a for a in self.agents if a.agent_id != agent_id]
        logger.info(f"Agent unregistered: {agent_id}")

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID"""
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent
        return None

    def route_message(
        self, message: Message, strategy: RoutingStrategy = RoutingStrategy.DIRECT
    ) -> List[BaseAgent]:
        """
        Route a message to appropriate agent(s)

        Args:
            message: The message to route
            strategy: Routing strategy to use

        Returns:
            List of agents that should receive the message
        """
        if strategy == RoutingStrategy.DIRECT:
            return self._route_direct(message)
        elif strategy == RoutingStrategy.BROADCAST:
            return self._route_broadcast()
        elif strategy == RoutingStrategy.CAPABILITY_BASED:
            return self._route_by_capability(message)
        elif strategy == RoutingStrategy.ROLE_BASED:
            return self._route_by_role(message)
        elif strategy == RoutingStrategy.ROUND_ROBIN:
            return self._route_round_robin()
        else:
            logger.warning(f"Unknown routing strategy: {strategy}, using direct")
            return self._route_direct(message)

    def _route_direct(self, message: Message) -> List[BaseAgent]:
        """Route directly to specified receiver"""
        if message.receiver:
            agent = self.get_agent(message.receiver)
            return [agent] if agent else []
        return []

    def _route_broadcast(self) -> List[BaseAgent]:
        """Route to all agents"""
        return self.agents.copy()

    def _route_by_capability(self, message: Message) -> List[BaseAgent]:
        """Route based on agent capabilities"""
        # Extract required capability from message metadata
        required_capability = message.metadata.get("required_capability")
        if not required_capability:
            return []

        return [
            agent
            for agent in self.agents
            if required_capability in agent.capabilities and agent.can_handle(message)
        ]

    def _route_by_role(self, message: Message) -> List[BaseAgent]:
        """Route based on agent role"""
        required_role = message.metadata.get("required_role")
        if not required_role:
            return []

        return [agent for agent in self.agents if agent.role == required_role]

    def _route_round_robin(self) -> List[BaseAgent]:
        """Route using round-robin strategy"""
        if not self.agents:
            return []

        agent = self.agents[self.round_robin_index]
        self.round_robin_index = (self.round_robin_index + 1) % len(self.agents)
        return [agent]

    def get_agents_by_role(self, role: str) -> List[BaseAgent]:
        """Get all agents with a specific role"""
        return [agent for agent in self.agents if agent.role == role]

    def get_agents_by_capability(self, capability: AgentCapability) -> List[BaseAgent]:
        """Get all agents with a specific capability"""
        return [agent for agent in self.agents if capability in agent.capabilities]
