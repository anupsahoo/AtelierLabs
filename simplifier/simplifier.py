"""
SimplifierAgent

Placeholder implementation. Replace `process_input` with real logic.
"""


from .core.base_agent import CognitiveAgent, AgentResult
from .core.mental_models import MentalModelsLibrary


class SimplifierAgent(CognitiveAgent):
    """Agent implementation coming soon."""

    def __init__(self):
        super().__init__(
            name="Simplifier",
            category="communication",
            mental_models=[],
            description="Implementation coming soon",
            capabilities=[]
        )

    async def process_input(self, input_data, context=None) -> AgentResult:
        raise NotImplementedError("SimplifierAgent is not implemented yet")