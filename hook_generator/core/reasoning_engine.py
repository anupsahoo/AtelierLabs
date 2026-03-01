"""
Multi-Modal Reasoning Engine

Provides different reasoning capabilities for cognitive agents.
Supports logical, analogical, causal, and probabilistic reasoning.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re
import json


@dataclass
class ReasoningResult:
    """Result of reasoning process"""
    conclusion: Any
    confidence: float
    reasoning_steps: List[str]
    evidence: List[str]
    assumptions: List[str]


class ReasoningMethod(ABC):
    """Base class for reasoning methods"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def reason(self, problem: Any, context: Dict[str, Any]) -> ReasoningResult:
        """Apply reasoning method to solve a problem"""
        pass


class LogicalReasoning(ReasoningMethod):
    """Deductive and inductive logical reasoning"""
    
    def __init__(self):
        super().__init__(
            "logical_reasoning",
            "Apply deductive and inductive logic to reach conclusions"
        )
    
    async def reason(self, problem: Any, context: Dict[str, Any]) -> ReasoningResult:
        reasoning_steps = []
        evidence = []
        assumptions = []
        
        # Convert problem to string for analysis
        problem_text = str(problem)
        
        # Identify logical structure
        reasoning_steps.append("Analyzing logical structure of the problem")
        
        # Look for conditional statements (if-then)
        conditionals = self._extract_conditionals(problem_text)
        if conditionals:
            reasoning_steps.append(f"Found {len(conditionals)} conditional statements")
            evidence.extend(conditionals)
        
        # Look for causal relationships
        causal_relations = self._extract_causal_relations(problem_text)
        if causal_relations:
            reasoning_steps.append(f"Found {len(causal_relations)} causal relationships")
            evidence.extend(causal_relations)
        
        # Apply deductive reasoning
        deductive_conclusions = self._deductive_reasoning(conditionals, causal_relations)
        reasoning_steps.append("Applied deductive reasoning")
        
        # Apply inductive reasoning
        inductive_conclusions = self._inductive_reasoning(problem_text, context)
        reasoning_steps.append("Applied inductive reasoning")
        
        # Combine conclusions
        conclusion = {
            "deductive": deductive_conclusions,
            "inductive": inductive_conclusions,
            "combined": self._combine_conclusions(deductive_conclusions, inductive_conclusions)
        }
        
        confidence = self._calculate_logical_confidence(conditionals, causal_relations, context)
        
        return ReasoningResult(
            conclusion=conclusion,
            confidence=confidence,
            reasoning_steps=reasoning_steps,
            evidence=evidence,
            assumptions=["Logical structure is consistent", "Statements are truthful"]
        )
    
    def _extract_conditionals(self, text: str) -> List[str]:
        """Extract if-then statements from text"""
        conditional_patterns = [
            r"if\s+.*\s+then\s+.*",
            r"when\s+.*\s+.*\s+occurs",
            r"should\s+.*\s+then\s+.*",
            r"provided\s+.*\s+.*\s+will"
        ]
        
        conditionals = []
        for pattern in conditional_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            conditionals.extend(matches)
        
        return conditionals
    
    def _extract_causal_relations(self, text: str) -> List[str]:
        """Extract causal relationships from text"""
        causal_patterns = [
            r"because\s+.*",
            r"since\s+.*",
            r"due to\s+.*",
            r"as a result of\s+.*",
            r"leads to\s+.*",
            r"causes\s+.*"
        ]
        
        causal_relations = []
        for pattern in causal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            causal_relations.extend(matches)
        
        return causal_relations
    
    def _deductive_reasoning(self, conditionals: List[str], causal_relations: List[str]) -> List[str]:
        """Apply deductive reasoning to reach certain conclusions"""
        conclusions = []
        
        # Simple deductive patterns
        for conditional in conditionals:
            if "if" in conditional.lower() and "then" in conditional.lower():
                # Extract the conclusion part
                parts = conditional.lower().split("then")
                if len(parts) > 1:
                    conclusions.append(f"Deductive conclusion: {parts[1].strip()}")
        
        for causal in causal_relations:
            if "because" in causal.lower():
                # Extract the effect part
                parts = causal.lower().split("because")
                if len(parts) > 1:
                    conclusions.append(f"Causal conclusion: {parts[0].strip()}")
        
        return conclusions
    
    def _inductive_reasoning(self, text: str, context: Dict[str, Any]) -> List[str]:
        """Apply inductive reasoning to generalize from specific cases"""
        conclusions = []
        
        # Look for patterns and generalizations
        if "always" in text.lower() or "never" in text.lower():
            conclusions.append("Inductive generalization detected")
        
        # Look for statistical indicators
        if any(word in text.lower() for word in ["usually", "often", "typically", "generally"]):
            conclusions.append("Probabilistic generalization detected")
        
        # Use context to strengthen inductive reasoning
        if context.get("memory_patterns"):
            conclusions.append("Generalization based on past patterns")
        
        return conclusions
    
    def _combine_conclusions(self, deductive: List[str], inductive: List[str]) -> List[str]:
        """Combine deductive and inductive conclusions"""
        combined = []
        
        # Prioritize deductive conclusions (more certain)
        combined.extend(deductive)
        
        # Add inductive conclusions with uncertainty noted
        for conclusion in inductive:
            combined.append(f"{conclusion} (probabilistic)")
        
        return combined
    
    def _calculate_logical_confidence(self, conditionals: List[str], causal_relations: List[str], context: Dict[str, Any]) -> float:
        """Calculate confidence in logical reasoning"""
        base_confidence = 0.7
        
        # More logical structure increases confidence
        structure_bonus = min(0.2, (len(conditionals) + len(causal_relations)) * 0.05)
        
        # Context evidence increases confidence
        context_bonus = 0.1 if context.get("evidence") else 0.0
        
        confidence = base_confidence + structure_bonus + context_bonus
        return min(confidence, 1.0)


class AnalogicalReasoning(ReasoningMethod):
    """Reasoning by analogy and pattern matching"""
    
    def __init__(self):
        super().__init__(
            "analogical_reasoning",
            "Apply analogical reasoning by finding similar patterns and relationships"
        )
    
    async def reason(self, problem: Any, context: Dict[str, Any]) -> ReasoningResult:
        reasoning_steps = []
        evidence = []
        assumptions = []
        
        problem_text = str(problem)
        
        reasoning_steps.append("Searching for analogous patterns")
        
        # Find analogies based on structure
        structural_analogies = self._find_structural_analogies(problem_text)
        reasoning_steps.append(f"Found {len(structural_analogies)} structural analogies")
        evidence.extend(structural_analogies)
        
        # Find functional analogies
        functional_analogies = self._find_functional_analogies(problem_text, context)
        reasoning_steps.append(f"Found {len(functional_analogies)} functional analogies")
        evidence.extend(functional_analogies)
        
        # Apply analogical transfer
        transferred_insights = self._transfer_insights(structural_analogies, functional_analogies)
        reasoning_steps.append("Applied analogical transfer of insights")
        
        conclusion = {
            "analogies": {
                "structural": structural_analogies,
                "functional": functional_analogies
            },
            "transferred_insights": transferred_insights,
            "confidence_factors": self._evaluate_analogy_strength(structural_analogies, functional_analogies)
        }
        
        confidence = self._calculate_analogy_confidence(structural_analogies, functional_analogies)
        
        return ReasoningResult(
            conclusion=conclusion,
            confidence=confidence,
            reasoning_steps=reasoning_steps,
            evidence=evidence,
            assumptions=["Analogous situations share relevant properties", "Transfer is valid across domains"]
        )
    
    def _find_structural_analogies(self, text: str) -> List[str]:
        """Find analogies based on structural patterns"""
        # Simplified structural pattern matching
        structural_patterns = [
            "hierarchy", "network", "cycle", "linear_progression", 
            "feedback_loop", "cascade", "emergence"
        ]
        
        analogies = []
        for pattern in structural_patterns:
            if self._matches_structural_pattern(text, pattern):
                analogies.append(f"Structural analogy: {pattern}")
        
        return analogies
    
    def _find_functional_analogies(self, text: str, context: Dict[str, Any]) -> List[str]:
        """Find analogies based on functional relationships"""
        functional_patterns = [
            "resource_allocation", "information_processing", "decision_making",
            "adaptation", "optimization", "coordination"
        ]
        
        analogies = []
        for pattern in functional_patterns:
            if self._matches_functional_pattern(text, pattern):
                analogies.append(f"Functional analogy: {pattern}")
        
        return analogies
    
    def _matches_structural_pattern(self, text: str, pattern: str) -> bool:
        """Check if text matches a structural pattern"""
        pattern_indicators = {
            "hierarchy": ["levels", "ranks", "top", "bottom", "chain"],
            "network": ["nodes", "connections", "links", "distributed"],
            "cycle": ["repeat", "cycle", "loop", "circular"],
            "linear_progression": ["step", "phase", "sequence", "progress"],
            "feedback_loop": ["feedback", "adjust", "regulate", "balance"],
            "cascade": ["cascade", "chain_reaction", "ripple", "spread"],
            "emergence": ["emerge", "appear", "arise", "spontaneous"]
        }
        
        indicators = pattern_indicators.get(pattern, [])
        return any(indicator in text.lower() for indicator in indicators)
    
    def _matches_functional_pattern(self, text: str, pattern: str) -> bool:
        """Check if text matches a functional pattern"""
        pattern_indicators = {
            "resource_allocation": ["allocate", "distribute", "assign", "budget"],
            "information_processing": ["process", "analyze", "compute", "transform"],
            "decision_making": ["decide", "choose", "select", "determine"],
            "adaptation": ["adapt", "adjust", "modify", "evolve"],
            "optimization": ["optimize", "improve", "enhance", "maximize"],
            "coordination": ["coordinate", "synchronize", "align", "integrate"]
        }
        
        indicators = pattern_indicators.get(pattern, [])
        return any(indicator in text.lower() for indicator in indicators)
    
    def _transfer_insights(self, structural: List[str], functional: List[str]) -> List[str]:
        """Transfer insights from analogies to current problem"""
        insights = []
        
        for analogy in structural + functional:
            if "hierarchy" in analogy:
                insights.append("Consider power dynamics and reporting structures")
            elif "network" in analogy:
                insights.append("Look for distributed effects and network externalities")
            elif "cycle" in analogy:
                insights.append("Identify cyclical patterns and intervention points")
            elif "resource_allocation" in analogy:
                insights.append("Examine how resources are distributed and constrained")
            elif "decision_making" in analogy:
                insights.append("Analyze decision criteria and information flows")
        
        return insights
    
    def _evaluate_analogy_strength(self, structural: List[str], functional: List[str]) -> Dict[str, float]:
        """Evaluate the strength of analogies"""
        return {
            "structural_match": min(1.0, len(structural) * 0.2),
            "functional_match": min(1.0, len(functional) * 0.2),
            "cross_domain_validation": 0.6  # Placeholder for cross-domain validation
        }
    
    def _calculate_analogy_confidence(self, structural: List[str], functional: List[str]) -> float:
        """Calculate confidence in analogical reasoning"""
        base_confidence = 0.6  # Lower base confidence for analogical reasoning
        
        # More analogies increase confidence
        analogy_bonus = min(0.3, (len(structural) + len(functional)) * 0.05)
        
        confidence = base_confidence + analogy_bonus
        return min(confidence, 1.0)


class CausalReasoning(ReasoningMethod):
    """Reasoning about cause and effect relationships"""
    
    def __init__(self):
        super().__init__(
            "causal_reasoning",
            "Analyze cause-effect relationships and predict outcomes"
        )
    
    async def reason(self, problem: Any, context: Dict[str, Any]) -> ReasoningResult:
        reasoning_steps = []
        evidence = []
        assumptions = []
        
        problem_text = str(problem)
        
        reasoning_steps.append("Analyzing causal relationships")
        
        # Identify causes and effects
        causes, effects = self._identify_causes_and_effects(problem_text)
        reasoning_steps.append(f"Identified {len(causes)} causes and {len(effects)} effects")
        evidence.extend(causes + effects)
        
        # Build causal chains
        causal_chains = self._build_causal_chains(causes, effects)
        reasoning_steps.append(f"Built {len(causal_chains)} causal chains")
        
        # Identify confounding variables
        confounding_variables = self._identify_confounding_variables(problem_text, context)
        if confounding_variables:
            reasoning_steps.append(f"Identified {len(confounding_variables)} potential confounding variables")
        
        # Predict outcomes
        predictions = self._predict_outcomes(causal_chains, context)
        reasoning_steps.append("Generated causal predictions")
        
        conclusion = {
            "causes": causes,
            "effects": effects,
            "causal_chains": causal_chains,
            "confounding_variables": confounding_variables,
            "predictions": predictions
        }
        
        confidence = self._calculate_causal_confidence(causal_chains, confounding_variables)
        
        return ReasoningResult(
            conclusion=conclusion,
            confidence=confidence,
            reasoning_steps=reasoning_steps,
            evidence=evidence,
            assumptions=["Causal relationships are identifiable", "No unmeasured confounders"]
        )
    
    def _identify_causes_and_effects(self, text: str) -> Tuple[List[str], List[str]]:
        """Identify causes and effects in text"""
        causes = []
        effects = []
        
        # Causal indicators
        cause_indicators = ["because", "due to", "since", "as a result of", "caused by"]
        effect_indicators = ["leads to", "results in", "causes", "produces", "creates"]
        
        sentences = text.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check for causes
            if any(indicator in sentence_lower for indicator in cause_indicators):
                causes.append(sentence.strip())
            
            # Check for effects
            if any(indicator in sentence_lower for indicator in effect_indicators):
                effects.append(sentence.strip())
        
        return causes, effects
    
    def _build_causal_chains(self, causes: List[str], effects: List[str]) -> List[Dict[str, Any]]:
        """Build causal chains from identified causes and effects"""
        chains = []
        
        for i, cause in enumerate(causes):
            for j, effect in enumerate(effects):
                # Simple chain: cause -> effect
                chain = {
                    "chain_id": f"chain_{i}_{j}",
                    "cause": cause,
                    "effect": effect,
                    "strength": self._estimate_causal_strength(cause, effect),
                    "mechanism": self._infer_mechanism(cause, effect)
                }
                chains.append(chain)
        
        return chains
    
    def _identify_confounding_variables(self, text: str, context: Dict[str, Any]) -> List[str]:
        """Identify potential confounding variables"""
        confounders = []
        
        # Common confounding patterns
        confounding_patterns = [
            "correlation does not imply causation",
            "other factors",
            "external influences",
            "environmental factors",
            "third variable"
        ]
        
        for pattern in confounding_patterns:
            if pattern in text.lower():
                confounders.append(pattern)
        
        # Add context-based confounders
        if context.get("environment"):
            confounders.append("environmental factors")
        
        return confounders
    
    def _predict_outcomes(self, causal_chains: List[Dict], context: Dict[str, Any]) -> List[str]:
        """Predict outcomes based on causal chains"""
        predictions = []
        
        for chain in causal_chains:
            strength = chain["strength"]
            if strength > 0.7:
                predictions.append(f"High confidence: {chain['effect']} is likely to occur")
            elif strength > 0.4:
                predictions.append(f"Medium confidence: {chain['effect']} may occur")
            else:
                predictions.append(f"Low confidence: {chain['effect']} might occur")
        
        return predictions
    
    def _estimate_causal_strength(self, cause: str, effect: str) -> float:
        """Estimate the strength of causal relationship"""
        # Simplified strength estimation
        strong_indicators = ["directly", "immediately", "significantly", "strongly"]
        weak_indicators = ["might", "could", "possibly", "potentially"]
        
        cause_effect_text = f"{cause} {effect}".lower()
        
        if any(indicator in cause_effect_text for indicator in strong_indicators):
            return 0.8
        elif any(indicator in cause_effect_text for indicator in weak_indicators):
            return 0.4
        else:
            return 0.6
    
    def _infer_mechanism(self, cause: str, effect: str) -> str:
        """Infer the mechanism linking cause and effect"""
        # Simplified mechanism inference
        if "information" in cause.lower() and "decision" in effect.lower():
            return "information processing"
        elif "resource" in cause.lower() and "outcome" in effect.lower():
            return "resource allocation"
        elif "behavior" in cause.lower() and "result" in effect.lower():
            return "behavioral mechanism"
        else:
            return "unknown mechanism"
    
    def _calculate_causal_confidence(self, causal_chains: List[Dict], confounding_variables: List[str]) -> float:
        """Calculate confidence in causal reasoning"""
        base_confidence = 0.65
        
        # More chains increase confidence
        chain_bonus = min(0.2, len(causal_chains) * 0.05)
        
        # Confounding variables decrease confidence
        confounding_penalty = min(0.2, len(confounding_variables) * 0.05)
        
        confidence = base_confidence + chain_bonus - confounding_penalty
        return max(0.3, min(confidence, 1.0))


class ProbabilisticReasoning(ReasoningMethod):
    """Reasoning with probabilities and uncertainty"""
    
    def __init__(self):
        super().__init__(
            "probabilistic_reasoning",
            "Apply probabilistic reasoning to handle uncertainty and likelihoods"
        )
    
    async def reason(self, problem: Any, context: Dict[str, Any]) -> ReasoningResult:
        reasoning_steps = []
        evidence = []
        assumptions = []
        
        problem_text = str(problem)
        
        reasoning_steps.append("Analyzing probabilistic information")
        
        # Extract probability statements
        probabilities = self._extract_probabilities(problem_text)
        reasoning_steps.append(f"Extracted {len(probabilities)} probability statements")
        evidence.extend(probabilities)
        
        # Identify uncertainty indicators
        uncertainty_indicators = self._identify_uncertainty_indicators(problem_text)
        reasoning_steps.append(f"Found {len(uncertainty_indicators)} uncertainty indicators")
        
        # Calculate expected values
        expected_values = self._calculate_expected_values(probabilities, context)
        reasoning_steps.append("Calculated expected values")
        
        # Assess risk
        risk_assessment = self._assess_risk(probabilities, uncertainty_indicators)
        reasoning_steps.append("Assessed risk levels")
        
        conclusion = {
            "probabilities": probabilities,
            "uncertainty_indicators": uncertainty_indicators,
            "expected_values": expected_values,
            "risk_assessment": risk_assessment
        }
        
        confidence = self._calculate_probabilistic_confidence(probabilities, uncertainty_indicators)
        
        return ReasoningResult(
            conclusion=conclusion,
            confidence=confidence,
            reasoning_steps=reasoning_steps,
            evidence=evidence,
            assumptions=["Probability estimates are accurate", "Events are independent unless specified"]
        )
    
    def _extract_probabilities(self, text: str) -> List[Dict[str, Any]]:
        """Extract probability statements from text"""
        probabilities = []
        
        # Probability patterns
        prob_patterns = [
            r"(\d+\.?\d*)\s*%.*",
            r"probability of (\d+\.?\d*)",
            r"chance of (\d+\.?\d*)",
            r"likelihood (\d+\.?\d*)"
        ]
        
        for pattern in prob_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    prob_value = float(match)
                    if prob_value <= 1.0 and prob_value >= 0.0:
                        probabilities.append({
                            "value": prob_value,
                            "percentage": prob_value * 100,
                            "source": text[:100]  # First 100 chars as source
                        })
                except ValueError:
                    continue
        
        return probabilities
    
    def _identify_uncertainty_indicators(self, text: str) -> List[str]:
        """Identify words and phrases indicating uncertainty"""
        uncertainty_words = [
            "might", "could", "may", "possibly", "potentially", "likely", "unlikely",
            "uncertain", "unclear", "ambiguous", "unknown", "variable", "fluctuating"
        ]
        
        indicators = []
        text_lower = text.lower()
        
        for word in uncertainty_words:
            if word in text_lower:
                indicators.append(word)
        
        return list(set(indicators))  # Remove duplicates
    
    def _calculate_expected_values(self, probabilities: List[Dict], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate expected values for probabilistic outcomes"""
        expected_values = []
        
        for prob in probabilities:
            # Simplified expected value calculation
            # In practice, would need outcome values
            ev = {
                "probability": prob["value"],
                "expected_outcome": f"Outcome with {prob['percentage']:.1f}% probability",
                "risk_level": self._categorize_risk(prob["value"])
            }
            expected_values.append(ev)
        
        return expected_values
    
    def _assess_risk(self, probabilities: List[Dict], uncertainty_indicators: List[str]) -> Dict[str, Any]:
        """Assess overall risk level"""
        if not probabilities:
            return {"risk_level": "unknown", "confidence": "low"}
        
        avg_probability = sum(p["value"] for p in probabilities) / len(probabilities)
        uncertainty_level = len(uncertainty_indicators) / 10.0  # Normalize to 0-1
        
        risk_level = "low"
        if avg_probability > 0.7:
            risk_level = "high"
        elif avg_probability > 0.4:
            risk_level = "medium"
        
        return {
            "risk_level": risk_level,
            "average_probability": avg_probability,
            "uncertainty_level": uncertainty_level,
            "confidence": "high" if uncertainty_level < 0.3 else "medium" if uncertainty_level < 0.6 else "low"
        }
    
    def _categorize_risk(self, probability: float) -> str:
        """Categorize risk level based on probability"""
        if probability > 0.7:
            return "high"
        elif probability > 0.4:
            return "medium"
        else:
            return "low"
    
    def _calculate_probabilistic_confidence(self, probabilities: List[Dict], uncertainty_indicators: List[str]) -> float:
        """Calculate confidence in probabilistic reasoning"""
        base_confidence = 0.7
        
        # More probability statements increase confidence
        prob_bonus = min(0.2, len(probabilities) * 0.05)
        
        # More uncertainty decreases confidence
        uncertainty_penalty = min(0.3, len(uncertainty_indicators) * 0.05)
        
        confidence = base_confidence + prob_bonus - uncertainty_penalty
        return max(0.4, min(confidence, 1.0))


class ReasoningEngine:
    """
    Multi-modal reasoning engine that combines different reasoning methods.
    """
    
    def __init__(self):
        self.methods = {
            "logical": LogicalReasoning(),
            "analogical": AnalogicalReasoning(),
            "causal": CausalReasoning(),
            "probabilistic": ProbabilisticReasoning()
        }
    
    async def reason(self, problem: Any, mental_models: List[str], context: Dict[str, Any]) -> Dict[str, ReasoningResult]:
        """Apply appropriate reasoning methods based on problem type and mental models"""
        results = {}
        
        # Select reasoning methods based on mental models
        selected_methods = self._select_reasoning_methods(mental_models)
        
        # Apply each selected method
        for method_name in selected_methods:
            if method_name in self.methods:
                method = self.methods[method_name]
                result = await method.reason(problem, context)
                results[method_name] = result
        
        return results
    
    def _select_reasoning_methods(self, mental_models: List[str]) -> List[str]:
        """Select appropriate reasoning methods based on mental models"""
        method_mapping = {
            "first_principles": ["logical", "causal"],
            "second_order_thinking": ["causal", "probabilistic"],
            "systems_thinking": ["causal", "logical"],
            "inversion": ["logical"],
            "pareto": ["probabilistic"],
            "opportunity_cost": ["probabilistic", "causal"],
            "probabilistic_thinking": ["probabilistic"],
            "network_effects": ["causal", "analogical"]
        }
        
        selected_methods = set()
        for model in mental_models:
            if model in method_mapping:
                selected_methods.update(method_mapping[model])
        
        # Default to logical reasoning if no specific mapping
        if not selected_methods:
            selected_methods.add("logical")
        
        return list(selected_methods)
    
    def get_available_methods(self) -> List[str]:
        """Get list of available reasoning methods"""
        return list(self.methods.keys())
    
    def get_method_description(self, method_name: str) -> str:
        """Get description of a reasoning method"""
        if method_name in self.methods:
            return self.methods[method_name].description
        return "Unknown reasoning method"
