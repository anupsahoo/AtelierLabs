"""Scoring rubrics and validation logic for agent outputs."""

from typing import Dict, List, Any
from pydantic import BaseModel, Field, validator


class ScoringRubric(BaseModel):
    """Base scoring rubric for agent evaluations."""
    
    name: str
    description: str
    min_score: int = 1
    max_score: int = 10
    criteria: Dict[str, str] = Field(default_factory=dict)


class JobsRubric(ScoringRubric):
    """Scoring rubric for Jobs lens evaluation."""
    
    def __init__(self):
        super().__init__(
            name="Jobs Lens Rubric",
            description="Evaluates simplicity, user focus, and execution clarity",
            criteria={
                "Simplicity": "How focused and simple is the core value proposition?",
                "User Focus": "How well does this solve a real user problem?",
                "Differentiation": "How unique and compelling is this vs alternatives?",
                "Execution Clarity": "How clear and achievable is the implementation plan?"
            }
        )


class NavalRubric(ScoringRubric):
    """Scoring rubric for Naval lens evaluation."""
    
    def __init__(self):
        super().__init__(
            name="Naval Lens Rubric", 
            description="Evaluates leverage potential and wealth creation",
            criteria={
                "Leverage Potential": "How well does this scale without linear effort?",
                "Scalability": "Can this grow exponentially with same resources?",
                "Network Effects": "Does this get more valuable with more users?",
                "Market Timing": "Is this the right time for this solution?"
            }
        )


class MungerRubric(ScoringRubric):
    """Scoring rubric for Munger lens evaluation."""
    
    def __init__(self):
        super().__init__(
            name="Munger Lens Rubric",
            description="Evaluates mental model usage and inversion thinking",
            criteria={
                "Mental Model Usage": "How well are relevant mental models applied?",
                "Inversion Thinking": "How thoroughly are failure modes considered?", 
                "Bias Awareness": "How well are cognitive biases identified and mitigated?",
                "Systems Perspective": "How well are second/third-order effects considered?"
            }
        )


class IndianPhilosophyRubric(ScoringRubric):
    """Scoring rubric for Indian Philosophy lens evaluation."""
    
    def __init__(self):
        super().__init__(
            name="Indian Philosophy Lens Rubric",
            description="Evaluates dharmic alignment and long-term thinking",
            criteria={
                "Dharmic Alignment": "How well does this serve righteous purpose?",
                "Long-term Sustainability": "How sustainable is this approach over decades?",
                "Stakeholder Harmony": "How well does this serve all stakeholders?",
                "Ethical Foundation": "How strong are the ethical foundations?"
            }
        )


class RuthlessCapitalistRubric(ScoringRubric):
    """Scoring rubric for Ruthless Capitalist lens evaluation."""
    
    def __init__(self):
        super().__init__(
            name="Ruthless Capitalist Lens Rubric",
            description="Evaluates competitive advantage and market dominance",
            criteria={
                "Moat Strength": "How defensible is this competitive position?",
                "Pricing Power": "How much pricing flexibility does this create?",
                "Competitive Advantage": "How sustainable are the competitive advantages?",
                "Market Dominance Potential": "How likely is this to dominate its market?"
            }
        )


# Registry of all rubrics
RUBRICS = {
    "jobs": JobsRubric(),
    "naval": NavalRubric(),
    "munger": MungerRubric(),
    "indian": IndianPhilosophyRubric(),
    "capitalist": RuthlessCapitalistRubric(),
}


def get_rubric(agent_type: str) -> ScoringRubric:
    """Get scoring rubric for specific agent type."""
    return RUBRICS.get(agent_type.lower())


def validate_scores(scores: Dict[str, int], agent_type: str) -> Dict[str, Any]:
    """Validate scores against rubric criteria."""
    rubric = get_rubric(agent_type)
    if not rubric:
        return {"valid": False, "error": f"No rubric found for agent type: {agent_type}"}
    
    validation_results = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Check if all required criteria are scored
    for criterion in rubric.criteria.keys():
        if criterion not in scores:
            validation_results["warnings"].append(f"Missing score for: {criterion}")
    
    # Check score ranges
    for criterion, score in scores.items():
        if not isinstance(score, int):
            validation_results["errors"].append(f"Score for {criterion} must be integer, got {type(score)}")
            validation_results["valid"] = False
        elif score < rubric.min_score or score > rubric.max_score:
            validation_results["errors"].append(
                f"Score for {criterion} ({score}) outside valid range {rubric.min_score}-{rubric.max_score}"
            )
            validation_results["valid"] = False
    
    return validation_results


def calculate_aggregate_score(scores: Dict[str, int]) -> float:
    """Calculate aggregate score from individual criterion scores."""
    if not scores:
        return 0.0
    
    return sum(scores.values()) / len(scores)
