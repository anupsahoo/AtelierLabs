"""
LongHorizonAgent

Placeholder implementation. Replace `process_input` with real logic.
"""


from .core.base_agent import CognitiveAgent, AgentResult
from .core.mental_models import MentalModelsLibrary


class LongHorizonAgent(CognitiveAgent):
    """Agent implementation coming soon."""

    def __init__(self):
        super().__init__(
            name="LongHorizon",
            category="beyond_software",
            mental_models=[],
            description="Implementation coming soon",
            capabilities=[]
        )

    async def process_input(self, input_data, context=None) -> AgentResult:
        raise NotImplementedError("LongHorizonAgent is not implemented yet")