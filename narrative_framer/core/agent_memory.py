"""
Agent Memory System

Persistent memory for agents to learn from interactions.
Provides short-term, long-term, and episodic memory capabilities.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import hashlib


@dataclass
class MemoryPattern:
    """A pattern learned from past interactions"""
    pattern_id: str
    context_signature: str
    frequency: int
    success_rate: float
    last_seen: datetime
    associated_outcomes: List[str]


@dataclass
class EpisodicMemory:
    """Single interaction episode"""
    episode_id: str
    timestamp: datetime
    input_hash: str
    context: Dict[str, Any]
    output: Dict[str, Any]
    confidence: float
    mental_models_used: List[str]
    feedback: Optional[Dict[str, Any]] = None


class AgentMemory:
    """
    Persistent memory system for cognitive agents.
    
    Memory Types:
    - Short-term: Current session context and working memory
    - Long-term: Learned patterns and generalizations
    - Episodic: Complete interaction history
    """
    
    def __init__(self, max_episodic_memories: int = 1000):
        self.max_episodic_memories = max_episodic_memories
        
        # Memory stores
        self.short_term_memory: Dict[str, Any] = {}
        self.long_term_patterns: Dict[str, MemoryPattern] = {}
        self.episodic_memories: List[EpisodicMemory] = []
        
        # Memory statistics
        self.total_interactions = 0
        self.last_interaction = None
        
    def store_interaction(self, interaction_data: Dict[str, Any]):
        """Store a new interaction in memory"""
        timestamp = datetime.now()
        
        # Generate episode ID
        episode_id = self._generate_episode_id(interaction_data, timestamp)
        
        # Create episodic memory
        episodic_memory = EpisodicMemory(
            episode_id=episode_id,
            timestamp=timestamp,
            input_hash=self._hash_input(interaction_data.get("input", "")),
            context=interaction_data.get("context", {}),
            output={"content": interaction_data.get("output", ""), 
                   "confidence": interaction_data.get("confidence", 0.0)},
            confidence=interaction_data.get("confidence", 0.0),
            mental_models_used=interaction_data.get("mental_models", []),
            feedback=interaction_data.get("feedback")
        )
        
        # Store episodic memory
        self.episodic_memories.append(episodic_memory)
        
        # Limit episodic memory size
        if len(self.episodic_memories) > self.max_episodic_memories:
            self.episodic_memories.pop(0)
        
        # Update short-term memory
        self.short_term_memory.update({
            "last_input": interaction_data.get("input", ""),
            "last_output": interaction_data.get("output", ""),
            "last_confidence": interaction_data.get("confidence", 0.0),
            "session_context": interaction_data.get("context", {})
        })
        
        # Update long-term patterns
        self._update_patterns(episodic_memory)
        
        # Update statistics
        self.total_interactions += 1
        self.last_interaction = timestamp
    
    def retrieve_patterns(self, context_signature: str, limit: int = 5) -> List[MemoryPattern]:
        """Retrieve relevant patterns based on context"""
        relevant_patterns = []
        
        for pattern in self.long_term_patterns.values():
            # Simple relevance check based on context similarity
            if self._calculate_context_similarity(context_signature, pattern.context_signature) > 0.3:
                relevant_patterns.append(pattern)
        
        # Sort by relevance and frequency
        relevant_patterns.sort(
            key=lambda p: (p.frequency * p.success_rate, p.last_seen),
            reverse=True
        )
        
        return relevant_patterns[:limit]
    
    def get_recent_episodes(self, limit: int = 10) -> List[EpisodicMemory]:
        """Get most recent episodic memories"""
        return sorted(self.episodic_memories, key=lambda e: e.timestamp, reverse=True)[:limit]
    
    def get_successful_patterns(self, min_success_rate: float = 0.7, min_frequency: int = 3) -> List[MemoryPattern]:
        """Get patterns that have proven successful"""
        successful_patterns = []
        
        for pattern in self.long_term_patterns.values():
            if (pattern.success_rate >= min_success_rate and 
                pattern.frequency >= min_frequency):
                successful_patterns.append(pattern)
        
        return sorted(successful_patterns, key=lambda p: p.success_rate, reverse=True)
    
    def update_feedback(self, episode_id: str, feedback: Dict[str, Any]):
        """Update an episode with feedback for learning"""
        for episode in self.episodic_memories:
            if episode.episode_id == episode_id:
                episode.feedback = feedback
                
                # Update associated patterns based on feedback
                if feedback.get("success", False):
                    self._reinforce_patterns(episode)
                else:
                    self._weaken_patterns(episode)
                
                break
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about the agent's memory"""
        return {
            "total_interactions": self.total_interactions,
            "episodic_memories": len(self.episodic_memories),
            "long_term_patterns": len(self.long_term_patterns),
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None,
            "average_confidence": self._calculate_average_confidence(),
            "most_common_mental_models": self._get_most_common_mental_models()
        }
    
    def clear_short_term_memory(self):
        """Clear short-term memory (useful for new sessions)"""
        self.short_term_memory.clear()
    
    def export_memory(self) -> Dict[str, Any]:
        """Export memory data for persistence"""
        return {
            "short_term_memory": self.short_term_memory,
            "long_term_patterns": {
                pid: {
                    "pattern_id": p.pattern_id,
                    "context_signature": p.context_signature,
                    "frequency": p.frequency,
                    "success_rate": p.success_rate,
                    "last_seen": p.last_seen.isoformat(),
                    "associated_outcomes": p.associated_outcomes
                }
                for pid, p in self.long_term_patterns.items()
            },
            "episodic_memories": [
                {
                    "episode_id": e.episode_id,
                    "timestamp": e.timestamp.isoformat(),
                    "input_hash": e.input_hash,
                    "context": e.context,
                    "output": e.output,
                    "confidence": e.confidence,
                    "mental_models_used": e.mental_models_used,
                    "feedback": e.feedback
                }
                for e in self.episodic_memories
            ],
            "total_interactions": self.total_interactions,
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None
        }
    
    def import_memory(self, memory_data: Dict[str, Any]):
        """Import memory data from persistence"""
        self.short_term_memory = memory_data.get("short_term_memory", {})
        
        # Import long-term patterns
        pattern_data = memory_data.get("long_term_patterns", {})
        self.long_term_patterns = {}
        for pid, p_data in pattern_data.items():
            self.long_term_patterns[pid] = MemoryPattern(
                pattern_id=p_data["pattern_id"],
                context_signature=p_data["context_signature"],
                frequency=p_data["frequency"],
                success_rate=p_data["success_rate"],
                last_seen=datetime.fromisoformat(p_data["last_seen"]),
                associated_outcomes=p_data["associated_outcomes"]
            )
        
        # Import episodic memories
        episodic_data = memory_data.get("episodic_memories", [])
        self.episodic_memories = []
        for e_data in episodic_data:
            self.episodic_memories.append(EpisodicMemory(
                episode_id=e_data["episode_id"],
                timestamp=datetime.fromisoformat(e_data["timestamp"]),
                input_hash=e_data["input_hash"],
                context=e_data["context"],
                output=e_data["output"],
                confidence=e_data["confidence"],
                mental_models_used=e_data["mental_models_used"],
                feedback=e_data.get("feedback")
            ))
        
        self.total_interactions = memory_data.get("total_interactions", 0)
        last_interaction = memory_data.get("last_interaction")
        self.last_interaction = datetime.fromisoformat(last_interaction) if last_interaction else None
    
    # Private methods
    
    def _generate_episode_id(self, interaction_data: Dict[str, Any], timestamp: datetime) -> str:
        """Generate unique episode ID"""
        content = f"{timestamp.isoformat()}-{interaction_data.get('input', '')}-{interaction_data.get('mental_models', [])}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _hash_input(self, input_text: str) -> str:
        """Generate hash for input text"""
        return hashlib.md5(input_text.encode()).hexdigest()[:16]
    
    def _update_patterns(self, episode: EpisodicMemory):
        """Update long-term patterns based on new episode"""
        context_signature = self._extract_context_signature(episode.context)
        
        if context_signature not in self.long_term_patterns:
            self.long_term_patterns[context_signature] = MemoryPattern(
                pattern_id=f"pattern_{len(self.long_term_patterns)}",
                context_signature=context_signature,
                frequency=0,
                success_rate=0.0,
                last_seen=episode.timestamp,
                associated_outcomes=[]
            )
        
        pattern = self.long_term_patterns[context_signature]
        pattern.frequency += 1
        pattern.last_seen = episode.timestamp
        
        # Update success rate
        if episode.feedback:
            success = episode.feedback.get("success", False)
            pattern.success_rate = ((pattern.success_rate * (pattern.frequency - 1)) + (1.0 if success else 0.0)) / pattern.frequency
        
        # Add to associated outcomes
        outcome_summary = str(episode.output)[:100]
        if outcome_summary not in pattern.associated_outcomes:
            pattern.associated_outcomes.append(outcome_summary)
    
    def _extract_context_signature(self, context: Dict[str, Any]) -> str:
        """Extract a signature from context for pattern matching"""
        # Simple signature based on context keys and first values
        signature_parts = []
        for key in sorted(context.keys()):
            value = str(context.get(key, ""))[:50]
            signature_parts.append(f"{key}:{value}")
        
        return "|".join(signature_parts)
    
    def _calculate_context_similarity(self, sig1: str, sig2: str) -> float:
        """Calculate similarity between two context signatures"""
        # Simple similarity based on common parts
        parts1 = set(sig1.split("|"))
        parts2 = set(sig2.split("|"))
        
        if not parts1 or not parts2:
            return 0.0
        
        intersection = parts1.intersection(parts2)
        union = parts1.union(parts2)
        
        return len(intersection) / len(union)
    
    def _reinforce_patterns(self, episode: EpisodicMemory):
        """Reinforce patterns based on positive feedback"""
        context_signature = self._extract_context_signature(episode.context)
        
        if context_signature in self.long_term_patterns:
            pattern = self.long_term_patterns[context_signature]
            # Boost success rate for successful episodes
            pattern.success_rate = min(1.0, pattern.success_rate + 0.1)
    
    def _weaken_patterns(self, episode: EpisodicMemory):
        """Weaken patterns based on negative feedback"""
        context_signature = self._extract_context_signature(episode.context)
        
        if context_signature in self.long_term_patterns:
            pattern = self.long_term_patterns[context_signature]
            # Reduce success rate for unsuccessful episodes
            pattern.success_rate = max(0.0, pattern.success_rate - 0.05)
    
    def _calculate_average_confidence(self) -> float:
        """Calculate average confidence across all episodes"""
        if not self.episodic_memories:
            return 0.0
        
        total_confidence = sum(episode.confidence for episode in self.episodic_memories)
        return total_confidence / len(self.episodic_memories)
    
    def _get_most_common_mental_models(self) -> List[str]:
        """Get most commonly used mental models"""
        model_counts = {}
        
        for episode in self.episodic_memories:
            for model in episode.mental_models_used:
                model_counts[model] = model_counts.get(model, 0) + 1
        
        # Sort by frequency and return top 5
        sorted_models = sorted(model_counts.items(), key=lambda x: x[1], reverse=True)
        return [model for model, count in sorted_models[:5]]
