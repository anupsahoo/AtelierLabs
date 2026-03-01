"""
Cognitive Agent Framework (CAF)

A unified framework for building intelligent thinking agents
that apply mental models to solve real-world cognitive problems.

Framework Components:
- Base Agent Architecture
- Mental Models Library  
- Agent Memory System
- Multi-Modal Reasoning Engine
- Agent Communication Protocol
- Agent Orchestration

Author: Anup Sahoo
Purpose: Design intelligence systems beyond software engineering
"""

from .base_agent import CognitiveAgent
from .mental_models import MentalModelsLibrary
from .reasoning_engine import ReasoningEngine
from .agent_memory import AgentMemory
from .communication import AgentCommunication
from .orchestration import AgentOrchestrator

__version__ = "1.0.0"
__author__ = "Anup Sahoo"

__all__ = [
    "CognitiveAgent",
    "MentalModelsLibrary", 
    "ReasoningEngine",
    "AgentMemory",
    "AgentCommunication",
    "AgentOrchestrator"
]
