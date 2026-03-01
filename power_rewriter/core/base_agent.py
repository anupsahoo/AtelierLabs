"""
Base Agent Architecture

Core foundation for all cognitive agents in the framework.
Provides unified processing pipeline, memory integration, and reasoning capabilities.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

from .mental_models import MentalModelsLibrary
from .agent_memory import AgentMemory
from .reasoning_engine import ReasoningEngine


@dataclass
class AgentResult:
    """Standardized result structure for all agent outputs"""
    content: Any
    confidence: float
    reasoning_trace: List[str]
    mental_models_used: List[str]
    processing_time: float
    metadata: Dict[str, Any]


class CognitiveAgent(ABC):
    """
    Base class for all thinking agents with unified agentic patterns.
    
    Each agent inherits this base to ensure consistent:
    - Processing pipeline
    - Memory integration
    - Mental model application
    - Reasoning capabilities
    - Result formatting
    """
    
    def __init__(
        self, 
        name: str, 
        category: str, 
        mental_models: List[str],
        description: str = "",
        capabilities: List[str] = None
    ):
        self.name = name
        self.category = category
        self.mental_models = mental_models
        self.description = description
        self.capabilities = capabilities or []
        
        # Core framework components
        self.memory = AgentMemory()
        self.reasoning_engine = ReasoningEngine()
        self.mental_models_lib = MentalModelsLibrary()
        
        # Agent state
        self.created_at = datetime.now()
        self.total_interactions = 0
        self.last_interaction = None
        
    @abstractmethod
    async def process_input(self, input_data: Any, context: Optional[Dict] = None) -> AgentResult:
        """
        Process input data using agent-specific logic.
        Must be implemented by each concrete agent.
        """
        pass
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> AgentResult:
        """
        Unified processing pipeline for all agents.
        
        Pipeline Steps:
        1. Input validation & preprocessing
        2. Context enrichment
        3. Mental model application
        4. Reasoning & inference
        5. Output structuring
        6. Confidence scoring
        7. Memory storage
        """
        start_time = datetime.now()
        reasoning_trace = []
        
        try:
            # Step 1: Input validation & preprocessing
            validated_input = self._validate_input(input_data)
            reasoning_trace.append(f"Input validated: {type(validated_input)}")
            
            # Step 2: Context enrichment
            enriched_context = self._enrich_context(validated_input, context)
            reasoning_trace.append("Context enriched with agent memory and mental models")
            
            # Step 3: Mental model application
            mental_model_results = await self._apply_mental_models(validated_input, enriched_context)
            reasoning_trace.append(f"Applied mental models: {self.mental_models}")
            
            # Step 4: Agent-specific processing
            result = await self.process_input(validated_input, enriched_context)
            reasoning_trace.extend(result.reasoning_trace)
            
            # Step 5: Confidence scoring
            confidence = self._calculate_confidence(result, mental_model_results)
            reasoning_trace.append(f"Confidence calculated: {confidence:.2f}")
            
            # Step 6: Memory storage
            await self._store_interaction(validated_input, result, context)
            reasoning_trace.append("Interaction stored in agent memory")
            
            # Step 7: Create final result
            processing_time = (datetime.now() - start_time).total_seconds()
            
            final_result = AgentResult(
                content=result.content,
                confidence=confidence,
                reasoning_trace=reasoning_trace,
                mental_models_used=self.mental_models,
                processing_time=processing_time,
                metadata={
                    "agent_name": self.name,
                    "category": self.category,
                    "interaction_id": self.total_interactions,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            self.total_interactions += 1
            self.last_interaction = datetime.now()
            
            return final_result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            reasoning_trace.append(f"Error occurred: {str(e)}")
            
            return AgentResult(
                content={"error": str(e), "error_type": type(e).__name__},
                confidence=0.0,
                reasoning_trace=reasoning_trace,
                mental_models_used=[],
                processing_time=processing_time,
                metadata={"error": True}
            )
    
    def _validate_input(self, input_data: Any) -> Any:
        """Validate and preprocess input data"""
        if input_data is None:
            raise ValueError("Input data cannot be None")
        return input_data
    
    def _enrich_context(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        """Enrich context with agent memory and mental model information"""
        enriched_context = context or {}
        
        # Add relevant memory patterns
        relevant_patterns = self.memory.retrieve_patterns(str(input_data)[:100])
        enriched_context["memory_patterns"] = relevant_patterns
        
        # Add mental model information
        enriched_context["available_mental_models"] = self.mental_models
        enriched_context["agent_capabilities"] = self.capabilities
        
        return enriched_context
    
    async def _apply_mental_models(self, input_data: Any, context: Dict) -> Dict[str, Any]:
        """Apply configured mental models to the input"""
        results = {}
        
        for model_name in self.mental_models:
            try:
                model_result = self.mental_models_lib.apply_model(model_name, input_data, context)
                results[model_name] = model_result
            except Exception as e:
                results[model_name] = {"error": str(e)}
        
        return results
    
    def _calculate_confidence(self, result: AgentResult, mental_model_results: Dict) -> float:
        """Calculate confidence score based on result quality and mental model consistency"""
        base_confidence = 0.7  # Base confidence for any result
        
        # Factor in mental model success
        successful_models = sum(1 for r in mental_model_results.values() if "error" not in r)
        model_factor = successful_models / len(self.mental_models) if self.mental_models else 1.0
        
        # Factor in result completeness
        completeness_factor = 1.0 if hasattr(result, 'content') and result.content else 0.5
        
        # Calculate final confidence
        confidence = base_confidence * model_factor * completeness_factor
        return min(confidence, 1.0)
    
    async def _store_interaction(self, input_data: Any, result: AgentResult, context: Optional[Dict]):
        """Store interaction in agent memory for learning"""
        interaction_data = {
            "input": str(input_data)[:200],  # Truncate for storage
            "output": str(result.content)[:200],
            "confidence": result.confidence,
            "mental_models": result.mental_models_used,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        
        self.memory.store_interaction(interaction_data)
    
    def explain_reasoning(self, result: AgentResult) -> str:
        """Generate human-readable explanation of the agent's reasoning process"""
        explanation = f"""
## {self.name} Reasoning Process

**Agent Category:** {self.category}
**Mental Models Used:** {', '.join(result.mental_models_used)}
**Confidence:** {result.confidence:.2f}
**Processing Time:** {result.processing_time:.2f}s

### Reasoning Steps:
"""
        
        for i, step in enumerate(result.reasoning_trace, 1):
            explanation += f"{i}. {step}\n"
        
        explanation += f"\n### Result:\n{json.dumps(result.content, indent=2)}"
        
        return explanation
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get comprehensive agent information"""
        return {
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "mental_models": self.mental_models,
            "capabilities": self.capabilities,
            "created_at": self.created_at.isoformat(),
            "total_interactions": self.total_interactions,
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None
        }
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category}) - {len(self.mental_models)} mental models"
    
    def __repr__(self) -> str:
        return f"CognitiveAgent(name='{self.name}', category='{self.category}', models={self.mental_models})"
