"""
Mental Models Library

Curated collection of mental models that agents can apply to solve problems.
Each mental model provides a different lens for analyzing and understanding situations.

Available Mental Models:
- First Principles Thinking
- Second-Order Thinking  
- Systems Thinking
- Inversion
- Pareto Principle
- Opportunity Cost
- Probabilistic Thinking
- Network Effects
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import re
import json


@dataclass
class MentalModelResult:
    """Result of applying a mental model to a problem"""
    insights: List[str]
    analysis: Dict[str, Any]
    confidence: float
    recommendations: List[str]


class MentalModel(ABC):
    """Base class for all mental models"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def apply(self, problem_context: str, additional_context: Dict[str, Any]) -> MentalModelResult:
        """Apply the mental model to a problem context"""
        pass


class FirstPrinciplesModel(MentalModel):
    """Break down complex problems into their fundamental truths"""
    
    def __init__(self):
        super().__init__(
            "first_principles",
            "Deconstruct problems into their most basic, undeniable truths"
        )
    
    async def apply(self, problem_context: str, additional_context: Dict[str, Any]) -> MentalModelResult:
        insights = []
        analysis = {}
        recommendations = []
        
        # Identify assumptions
        assumptions = self._extract_assumptions(problem_context)
        insights.append(f"Identified {len(assumptions)} assumptions")
        
        # Question each assumption
        questioned_assumptions = []
        for assumption in assumptions:
            question = f"What if {assumption} is not true?"
            questioned_assumptions.append(question)
            insights.append(f"Questioned: {assumption}")
        
        # Identify fundamental truths
        fundamental_truths = self._identify_fundamental_truths(problem_context, assumptions)
        insights.append(f"Found {len(fundamental_truths)} fundamental truths")
        
        analysis = {
            "assumptions": assumptions,
            "questioned_assumptions": questioned_assumptions,
            "fundamental_truths": fundamental_truths
        }
        
        recommendations = [
            "Build solutions based on fundamental truths rather than assumptions",
            "Continuously question and validate assumptions",
            "Simplify by removing unnecessary complexity"
        ]
        
        return MentalModelResult(
            insights=insights,
            analysis=analysis,
            confidence=0.8,
            recommendations=recommendations
        )
    
    def _extract_assumptions(self, text: str) -> List[str]:
        """Extract assumptions from text using pattern matching"""
        assumption_patterns = [
            r"everyone knows that",
            r"obviously",
            r"clearly",
            r"of course",
            r"we all know",
            r"it goes without saying"
        ]
        
        assumptions = []
        for pattern in assumption_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            assumptions.extend(matches)
        
        # Add common implicit assumptions
        implicit_assumptions = [
            "current conditions will continue",
            "past trends will continue",
            "others think the same way",
            "technology will keep improving"
        ]
        
        return assumptions + implicit_assumptions
    
    def _identify_fundamental_truths(self, text: str, assumptions: List[str]) -> List[str]:
        """Identify fundamental truths that can't be broken down further"""
        # This is a simplified implementation
        # In practice, this would involve more sophisticated NLP
        fundamental_truths = [
            "Resources are limited",
            "People act in their perceived self-interest",
            "Systems tend toward entropy without energy input",
            "Information asymmetry creates power imbalances"
        ]
        
        return [truth for truth in fundamental_truths if truth.lower() in text.lower()]


class SecondOrderThinkingModel(MentalModel):
    """Think through consequences of consequences"""
    
    def __init__(self):
        super().__init__(
            "second_order_thinking",
            "Consider the downstream effects of decisions and actions"
        )
    
    async def apply(self, problem_context: str, additional_context: Dict[str, Any]) -> MentalModelResult:
        insights = []
        analysis = {}
        recommendations = []
        
        # Identify primary action/decision
        primary_action = self._extract_primary_action(problem_context)
        insights.append(f"Primary action: {primary_action}")
        
        # Generate first-order consequences
        first_order = self._generate_first_order_consequences(primary_action)
        insights.append(f"Generated {len(first_order)} first-order consequences")
        
        # Generate second-order consequences
        second_order = self._generate_second_order_consequences(first_order)
        insights.append(f"Generated {len(second_order)} second-order consequences")
        
        # Generate third-order consequences
        third_order = self._generate_third_order_consequences(second_order)
        insights.append(f"Generated {len(third_order)} third-order consequences")
        
        analysis = {
            "primary_action": primary_action,
            "first_order_consequences": first_order,
            "second_order_consequences": second_order,
            "third_order_consequences": third_order
        }
        
        recommendations = [
            "Consider effects up to third order",
            "Look for unintended consequences",
            "Plan for ripple effects in complex systems",
            "Test decisions against long-term outcomes"
        ]
        
        return MentalModelResult(
            insights=insights,
            analysis=analysis,
            confidence=0.75,
            recommendations=recommendations
        )
    
    def _extract_primary_action(self, text: str) -> str:
        """Extract the primary action or decision from text"""
        # Simplified extraction - in practice would use NLP
        action_keywords = ["will", "should", "decide", "implement", "launch", "build"]
        
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in action_keywords):
                return sentence.strip()
        
        return "Action not clearly identified"
    
    def _generate_first_order_consequences(self, action: str) -> List[str]:
        """Generate immediate consequences"""
        consequences = [
            f"Immediate resource allocation for: {action}",
            f"Direct impact on stakeholders from: {action}",
            f"Required changes to processes for: {action}",
            f"Short-term results from: {action}"
        ]
        return consequences
    
    def _generate_second_order_consequences(self, first_order: List[str]) -> List[str]:
        """Generate consequences of consequences"""
        consequences = [
            "System-wide adjustments to first-order effects",
            "Competitor responses to initial changes",
            "Market adaptation to new conditions",
            "Cultural shifts from process changes"
        ]
        return consequences
    
    def _generate_third_order_consequences(self, second_order: List[str]) -> List[str]:
        """Generate consequences of second-order consequences"""
        consequences = [
            "Industry-level transformation",
            "Regulatory changes in response",
            "Long-term societal impact",
            "Fundamental paradigm shifts"
        ]
        return consequences


class SystemsThinkingModel(MentalModel):
    """View problems as interconnected systems rather than isolated events"""
    
    def __init__(self):
        super().__init__(
            "systems_thinking",
            "Understand the interconnected components and feedback loops in systems"
        )
    
    async def apply(self, problem_context: str, additional_context: Dict[str, Any]) -> MentalModelResult:
        insights = []
        analysis = {}
        recommendations = []
        
        # Identify system components
        components = self._identify_system_components(problem_context)
        insights.append(f"Identified {len(components)} system components")
        
        # Map relationships
        relationships = self._map_relationships(components)
        insights.append(f"Mapped {len(relationships)} relationships")
        
        # Identify feedback loops
        feedback_loops = self._identify_feedback_loops(relationships)
        insights.append(f"Found {len(feedback_loops)} feedback loops")
        
        # Find leverage points
        leverage_points = self._find_leverage_points(components, relationships)
        insights.append(f"Identified {len(leverage_points)} leverage points")
        
        analysis = {
            "components": components,
            "relationships": relationships,
            "feedback_loops": feedback_loops,
            "leverage_points": leverage_points
        }
        
        recommendations = [
            "Focus on leverage points for maximum impact",
            "Consider feedback loops when making changes",
            "Understand system boundaries and interactions",
            "Look for patterns rather than isolated events"
        ]
        
        return MentalModelResult(
            insights=insights,
            analysis=analysis,
            confidence=0.85,
            recommendations=recommendations
        )
    
    def _identify_system_components(self, text: str) -> List[str]:
        """Identify key components of the system"""
        # Simplified component identification
        component_keywords = ["people", "process", "technology", "data", "resources", "environment"]
        
        components = []
        for keyword in component_keywords:
            if keyword in text.lower():
                components.append(keyword)
        
        return components or ["system", "environment", "actors"]
    
    def _map_relationships(self, components: List[str]) -> List[Dict[str, str]]:
        """Map relationships between components"""
        relationships = []
        
        for i, comp1 in enumerate(components):
            for comp2 in components[i+1:]:
                relationships.append({
                    "from": comp1,
                    "to": comp2,
                    "type": "influence"
                })
        
        return relationships
    
    def _identify_feedback_loops(self, relationships: List[Dict]) -> List[str]:
        """Identify feedback loops in the system"""
        # Simplified feedback loop identification
        loops = [
            "Reinforcing loop: success breeds more success",
            "Balancing loop: problems trigger corrections",
            "Delay loop: effects lag behind causes"
        ]
        return loops
    
    def _find_leverage_points(self, components: List[str], relationships: List[Dict]) -> List[str]:
        """Find high-leverage intervention points"""
        leverage_points = [
            "Change underlying rules and constraints",
            "Modify information flows",
            "Shift incentive structures",
            "Redesign system boundaries"
        ]
        return leverage_points


class MentalModelsLibrary:
    """Curated collection of mental models for agents"""
    
    # Constants for mental model names
    FIRST_PRINCIPLES = "first_principles"
    SECOND_ORDER_THINKING = "second_order_thinking"
    SYSTEMS_THINKING = "systems_thinking"
    INVERSION = "inversion"
    PARETO_PRINCIPLE = "pareto"
    OPPORTUNITY_COST = "opportunity_cost"
    PROBABILISTIC_THINKING = "probabilistic"
    NETWORK_EFFECTS = "network_effects"
    
    def __init__(self):
        self.models = {
            self.FIRST_PRINCIPLES: FirstPrinciplesModel(),
            self.SECOND_ORDER_THINKING: SecondOrderThinkingModel(),
            self.SYSTEMS_THINKING: SystemsThinkingModel(),
            # Additional models would be implemented here
        }
    
    def apply_model(self, model_name: str, problem_context: str, additional_context: Dict[str, Any] = None) -> MentalModelResult:
        """Apply specific mental model to problem"""
        if model_name not in self.models:
            raise ValueError(f"Mental model '{model_name}' not found. Available models: {list(self.models.keys())}")
        
        model = self.models[model_name]
        return model.apply(problem_context, additional_context or {})
    
    def get_available_models(self) -> List[str]:
        """Get list of available mental models"""
        return list(self.models.keys())
    
    def get_model_description(self, model_name: str) -> str:
        """Get description of a specific mental model"""
        if model_name not in self.models:
            raise ValueError(f"Mental model '{model_name}' not found")
        
        return self.models[model_name].description
    
    def apply_multiple_models(self, model_names: List[str], problem_context: str, additional_context: Dict[str, Any] = None) -> Dict[str, MentalModelResult]:
        """Apply multiple mental models to the same problem"""
        results = {}
        
        for model_name in model_names:
            try:
                result = self.apply_model(model_name, problem_context, additional_context)
                results[model_name] = result
            except Exception as e:
                results[model_name] = MentalModelResult(
                    insights=[f"Error applying model: {str(e)}"],
                    analysis={"error": str(e)},
                    confidence=0.0,
                    recommendations=[]
                )
        
        return results
