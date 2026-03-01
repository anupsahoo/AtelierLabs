"""Base agent interface and output contracts."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentOutput(BaseModel):
    """Structured output from an agent critique."""
    
    agent_name: str = Field(..., description="Name of the agent providing critique")
    brutal_line: str = Field(..., description="One brutal, honest line summarizing the core issue")
    key_questions: List[str] = Field(default_factory=list, description="Critical questions that need answers")
    assumptions: List[str] = Field(default_factory=list, description="Assumptions being made (labeled as fact/assumption/guess)")
    risks: List[str] = Field(default_factory=list, description="Key risks and failure modes")
    bold_move: Optional[str] = Field(None, description="One counterintuitive action to consider")
    scorecard: Dict[str, int] = Field(default_factory=dict, description="Numerical scores on key dimensions (1-10)")
    experiment_plan: Dict[str, Any] = Field(default_factory=dict, description="30-day experiment structure")
    references: List[Dict[str, str]] = Field(default_factory=list, description="Relevant blog references")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            # Add custom encoders if needed
        }


class Agent(ABC):
    """Base class for all advisory member agents."""
    
    def __init__(self, provider: Any) -> None:
        """Initialize agent with AI provider."""
        self.provider = provider
        self.name = self.__class__.__name__.replace("Agent", "")
    
    @abstractmethod
    def critique(self, content: str, interactive: bool = False) -> AgentOutput:
        """
        Provide critique of the given content.
        
        Args:
            content: The idea/content to critique
            interactive: Whether to ask clarifying questions
            
        Returns:
            Structured critique output
        """
        pass
    
    def _get_blog_references(self, tags: List[str]) -> List[Dict[str, str]]:
        """Get relevant blog references based on tags."""
        from advisory.retrieval.blog_refs import get_references_by_tags
        return get_references_by_tags(tags)
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured format."""
        # This is a simplified parser - in production you'd want more robust parsing
        lines = response.strip().split('\n')
        parsed = {
            'brutal_line': '',
            'key_questions': [],
            'assumptions': [],
            'risks': [],
            'bold_move': '',
            'scorecard': {},
            'experiment_plan': {},
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections
            if line.lower().startswith('brutal truth:') or line.lower().startswith('brutal line:'):
                parsed['brutal_line'] = line.split(':', 1)[1].strip().strip('"')
            elif line.lower().startswith('key questions:'):
                current_section = 'key_questions'
            elif line.lower().startswith('assumptions:'):
                current_section = 'assumptions'
            elif line.lower().startswith('risks:'):
                current_section = 'risks'
            elif line.lower().startswith('bold move:'):
                parsed['bold_move'] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('scorecard:'):
                current_section = 'scorecard'
            elif line.lower().startswith('experiment:') or line.lower().startswith('30-day'):
                current_section = 'experiment'
            elif current_section and line.startswith(('- ', '* ', '1. ', '2. ', '3. ')):
                # Handle list items
                item = line.lstrip('- *123456789. ').strip()
                if current_section in ['key_questions', 'assumptions', 'risks']:
                    parsed[current_section].append(item)
                elif current_section == 'scorecard':
                    # Parse scorecard items like "Simplicity: 7/10"
                    if ':' in item:
                        metric, score = item.split(':', 1)
                        try:
                            score_num = int(score.strip().split('/')[0])
                            parsed['scorecard'][metric.strip()] = score_num
                        except (ValueError, IndexError):
                            pass
        
        return parsed
