"""Board of Directors Agents package."""

from .base import Agent, AgentOutput
from .jobs import JobsAgent
from .naval import NavalAgent
from .munger import MungerAgent
from .indian_philosophy import IndianPhilosophyAgent
from .ruthless_capitalist import RuthlessCapitalistAgent
from .synthesis import SynthesisAgent

__all__ = [
    "Agent",
    "AgentOutput", 
    "JobsAgent",
    "NavalAgent",
    "MungerAgent",
    "IndianPhilosophyAgent",
    "RuthlessCapitalistAgent",
    "SynthesisAgent",
]
