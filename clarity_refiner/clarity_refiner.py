"""
Clarity Refiner Agent

Makes vague ideas sharp and structured using first principles thinking and systems analysis.
Transforms ambiguous concepts into clear, actionable definitions with examples and boundaries.

Mental Models Used:
- First Principles Thinking
- Systems Thinking
- Concept Clarification
"""


from .core.base_agent import CognitiveAgent, AgentResult
from .core.mental_models import MentalModelsLibrary


class ClarityRefinerAgent(CognitiveAgent):
    """
    Agent that makes vague ideas sharp and structured.
    
    Purpose: Make vague ideas sharp and structured
    Input: Vague concept or idea description
    Output: Structured definition with examples and boundaries
    Mental Models: First Principles Thinking, Systems Thinking, Concept Clarification
    """
    
    def __init__(self):
        super().__init__(
            name="Clarity Refiner",
            category="cognitive",
            mental_models=[MentalModelsLibrary.FIRST_PRINCIPLES, MentalModelsLibrary.SYSTEMS_THINKING],
            description="Makes vague ideas sharp and structured using first principles and systems thinking",
            capabilities=[
                "Extract core concepts from vague ideas",
                "Define clear boundaries and scope",
                "Generate concrete examples",
                "Identify related concepts",
                "Create structured definitions"
            ]
        )
    
    async def process_input(self, input_data: str, context: dict = None) -> AgentResult:
        """Process vague idea to create structured definition"""
        reasoning_trace = []
        
        # Step 1: Parse and identify core concepts
        reasoning_trace.append("Parsing and identifying core concepts from vague idea")
        core_concepts = self._extract_core_concepts(input_data)
        reasoning_trace.append(f"Identified {len(core_concepts)} core concepts")
        
        # Step 2: Apply first principles thinking
        reasoning_trace.append("Applying first principles thinking to break down concepts")
        first_principles = self._apply_first_principles(core_concepts)
        reasoning_trace.append("First principles analysis completed")
        
        # Step 3: Define boundaries and scope
        reasoning_trace.append("Defining clear boundaries and scope")
        boundaries = self._define_boundaries(core_concepts, input_data)
        reasoning_trace.append("Boundaries and scope defined")
        
        # Step 4: Generate concrete examples
        reasoning_trace.append("Generating concrete examples and use cases")
        examples = self._generate_examples(core_concepts, boundaries)
        reasoning_trace.append(f"Generated {len(examples)} concrete examples")
        
        # Step 5: Identify related concepts
        reasoning_trace.append("Identifying related and adjacent concepts")
        related_concepts = self._identify_related_concepts(core_concepts)
        reasoning_trace.append(f"Identified {len(related_concepts)} related concepts")
        
        # Step 6: Create structured definition
        reasoning_trace.append("Creating structured definition with all components")
        structured_definition = self._create_structured_definition(
            core_concepts, first_principles, boundaries, examples, related_concepts
        )
        reasoning_trace.append("Structured definition completed")
        
        return AgentResult(
            content=structured_definition,
            confidence=0.85,
            reasoning_trace=reasoning_trace,
            mental_models_used=self.mental_models,
            processing_time=0.0,
            metadata={
                "core_concepts_count": len(core_concepts),
                "examples_count": len(examples),
                "related_concepts_count": len(related_concepts),
                "clarity_score": self._calculate_clarity_score(structured_definition)
            }
        )
    
    def _extract_core_concepts(self, text: str) -> list:
        """Extract core concepts from vague text"""
        # Identify key terms and phrases
        words = text.split()
        
        # Filter out common words
        common_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "can", "this", "that", "these", "those",
            "some", "many", "few", "all", "any", "every", "each", "much", "more",
            "less", "most", "least", "very", "quite", "rather", "pretty", "really",
            "actually", "basically", "essentially", "simply", "just", "only"
        }
        
        # Extract potential concepts
        potential_concepts = []
        for word in words:
            clean_word = word.lower().strip(".,!?;:()[]{}\"'").strip()
            if len(clean_word) > 3 and clean_word not in common_words:
                potential_concepts.append(clean_word)
        
        # Count frequency and get most common
        concept_counts = {}
        for concept in potential_concepts:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        # Get top concepts
        top_concepts = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Create concept objects
        core_concepts = []
        for concept, count in top_concepts:
            core_concepts.append({
                "name": concept,
                "frequency": count,
                "context": self._get_concept_context(concept, text),
                "vagueness_score": self._assess_vagueness(concept, text)
            })
        
        return core_concepts
    
    def _get_concept_context(self, concept: str, text: str) -> str:
        """Get the context around a concept in the text"""
        words = text.split()
        for i, word in enumerate(words):
            if concept.lower() in word.lower():
                context_start = max(0, i - 3)
                context_end = min(len(words), i + 4)
                return " ".join(words[context_start:context_end])
        return ""
    
    def _assess_vagueness(self, concept: str, text: str) -> float:
        """Assess how vague a concept is based on context"""
        vagueness_indicators = [
            "some", "kind", "type", "sort", "like", "similar", "about", "around",
            "approximately", "roughly", "basically", "essentially", "generally",
            "typically", "usually", "often", "sometimes", "occasionally"
        ]
        
        context = self._get_concept_context(concept, text).lower()
        vagueness_count = sum(1 for indicator in vagueness_indicators if indicator in context)
        
        return min(vagueness_count / 3, 1.0)
    
    def _apply_first_principles(self, core_concepts: list) -> dict:
        """Apply first principles thinking to break down concepts"""
        first_principles = {}
        
        for concept in core_concepts:
            principle_analysis = {
                "concept": concept["name"],
                "fundamental_truths": self._identify_fundamental_truths(concept),
                "assumptions": self._identify_assumptions(concept),
                "components": self._break_into_components(concept),
                "essential_properties": self._identify_essential_properties(concept)
            }
            first_principles[concept["name"]] = principle_analysis
        
        return first_principles
    
    def _identify_fundamental_truths(self, concept: dict) -> list:
        """Identify fundamental truths about a concept"""
        # This is a simplified implementation
        # In practice, would use more sophisticated analysis
        
        concept_name = concept["name"]
        fundamental_truths = []
        
        # Generic fundamental truths
        fundamental_truths.append(f"{concept_name.title()} exists as a distinct concept")
        fundamental_truths.append(f"{concept_name.title()} has identifiable characteristics")
        fundamental_truths.append(f"{concept_name.title()} can be distinguished from related concepts")
        
        # Concept-specific truths based on common patterns
        if "system" in concept_name:
            fundamental_truths.append("Systems have components that interact")
            fundamental_truths.append("Systems have boundaries and interfaces")
        elif "process" in concept_name:
            fundamental_truths.append("Processes have inputs and outputs")
            fundamental_truths.append("Processes transform inputs through steps")
        elif "model" in concept_name:
            fundamental_truths.append("Models represent aspects of reality")
            fundamental_truths.append("Models simplify complexity")
        elif "framework" in concept_name:
            fundamental_truths.append("Frameworks provide structure and guidance")
            fundamental_truths.append("Frameworks are composed of interconnected elements")
        
        return fundamental_truths
    
    def _identify_assumptions(self, concept: dict) -> list:
        """Identify assumptions about a concept"""
        concept_name = concept["name"]
        assumptions = []
        
        # Common assumptions to question
        assumptions.append(f"The definition of {concept_name} is universally understood")
        assumptions.append(f"The boundaries of {concept_name} are clear")
        assumptions.append(f"The context of {concept_name} is appropriate")
        assumptions.append(f"The importance of {concept_name} is established")
        
        return assumptions
    
    def _break_into_components(self, concept: dict) -> list:
        """Break a concept into its components"""
        concept_name = concept["name"]
        components = []
        
        # Generic component analysis
        components.append(f"Core essence of {concept_name}")
        components.append(f"Key attributes of {concept_name}")
        components.append(f"Typical context for {concept_name}")
        components.append(f"Relationships to other concepts")
        
        # Concept-specific components
        if "system" in concept_name:
            components.append("Elements or parts")
            components.append("Interactions and relationships")
            components.append("Boundaries and interfaces")
            components.append("Inputs and outputs")
        elif "process" in concept_name:
            components.append("Steps or stages")
            components.append("Resources required")
            components.append("Time and sequence")
            components.append("Outcomes and results")
        elif "model" in concept_name:
            components.append("Variables or parameters")
            components.append("Relationships or equations")
            components.append("Assumptions and constraints")
            components.append("Scope and limitations")
        elif "framework" in concept_name:
            components.append("Core principles")
            components.append("Structural elements")
            components.append("Guidelines and rules")
            components.append("Extension points")
        
        return components
    
    def _identify_essential_properties(self, concept: dict) -> list:
        """Identify essential properties of a concept"""
        concept_name = concept["name"]
        properties = []
        
        # Generic essential properties
        properties.append(f"Identifiable: {concept_name} can be recognized and distinguished")
        properties.append(f"Describable: {concept_name} can be explained in words")
        properties.append(f"Distinguishable: {concept_name} differs from related concepts")
        
        # Context-specific properties
        context = concept.get("context", "")
        if "business" in context or "market" in context:
            properties.append(f"Economic value: {concept_name} has business implications")
        if "technical" in context or "system" in context:
            properties.append(f"Technical feasibility: {concept_name} can be implemented")
        if "social" in context or "people" in context:
            properties.append(f"Social impact: {concept_name} affects people")
        
        return properties
    
    def _define_boundaries(self, core_concepts: list, original_text: str) -> dict:
        """Define clear boundaries and scope for concepts"""
        boundaries = {}
        
        for concept in core_concepts:
            concept_name = concept["name"]
            boundary_analysis = {
                "inclusion_criteria": self._define_inclusion_criteria(concept),
                "exclusion_criteria": self._define_exclusion_criteria(concept),
                "scope_limitations": self._identify_scope_limitations(concept),
                "adjacent_concepts": self._identify_adjacent_concepts(concept, core_concepts),
                "context_dependencies": self._identify_context_dependencies(concept, original_text)
            }
            boundaries[concept_name] = boundary_analysis
        
        return boundaries
    
    def _define_inclusion_criteria(self, concept: dict) -> list:
        """Define what is included in the concept"""
        concept_name = concept["name"]
        criteria = []
        
        # Generic inclusion criteria
        criteria.append(f"Must be recognized as {concept_name}")
        criteria.append(f"Must share core characteristics of {concept_name}")
        criteria.append(f"Must function within the typical context of {concept_name}")
        
        # Concept-specific criteria
        if "system" in concept_name:
            criteria.append("Must have multiple interacting components")
            criteria.append("Must have identifiable boundaries")
        elif "process" in concept_name:
            criteria.append("Must transform inputs through steps")
            criteria.append("Must have a clear purpose or goal")
        elif "model" in concept_name:
            criteria.append("Must represent something real or theoretical")
            criteria.append("Must simplify complexity")
        elif "framework" in concept_name:
            criteria.append("Must provide structure or guidance")
            criteria.append("Must be composed of related elements")
        
        return criteria
    
    def _define_exclusion_criteria(self, concept: dict) -> list:
        """Define what is excluded from the concept"""
        concept_name = concept["name"]
        criteria = []
        
        # Generic exclusion criteria
        criteria.append(f"Must not be fundamentally different from {concept_name}")
        criteria.append(f"Must not lack core characteristics of {concept_name}")
        criteria.append(f"Must not function in a completely different domain")
        
        # Concept-specific exclusions
        if "system" in concept_name:
            criteria.append("Must not be a single isolated element")
            criteria.append("Must not lack interactions between parts")
        elif "process" in concept_name:
            criteria.append("Must not be a static state")
            criteria.append("Must not lack transformation")
        elif "model" in concept_name:
            criteria.append("Must not be the actual reality")
            criteria.append("Must not be overly complex to understand")
        elif "framework" in concept_name:
            criteria.append("Must not be rigid and unchangeable")
            criteria.append("Must not lack practical application")
        
        return criteria
    
    def _identify_scope_limitations(self, concept: dict) -> list:
        """Identify limitations in scope"""
        concept_name = concept["name"]
        limitations = []
        
        # Generic limitations
        limitations.append(f"Definition may not cover all variations of {concept_name}")
        limitations.append(f"Context may affect the meaning of {concept_name}")
        limitations.append(f"Boundaries may blur with related concepts")
        
        # Context-specific limitations
        vagueness_score = concept.get("vagueness_score", 0)
        if vagueness_score > 0.7:
            limitations.append(f"High vagueness makes precise definition difficult")
        
        return limitations
    
    def _identify_adjacent_concepts(self, concept: dict, all_concepts: list) -> list:
        """Identify concepts that are adjacent or related"""
        concept_name = concept["name"]
        adjacent = []
        
        # Find concepts with similar names or contexts
        for other_concept in all_concepts:
            if other_concept["name"] != concept_name:
                other_name = other_concept["name"]
                
                # Check for name similarity
                if self._concepts_similar(concept_name, other_name):
                    adjacent.append(other_name)
                
                # Check for context similarity
                if self._contexts_similar(concept.get("context", ""), other_concept.get("context", "")):
                    adjacent.append(other_name)
        
        return list(set(adjacent))[:5]  # Limit to top 5
    
    def _concepts_similar(self, name1: str, name2: str) -> bool:
        """Check if two concept names are similar"""
        # Simple similarity check
        name1_words = set(name1.split())
        name2_words = set(name2.split())
        
        # Check for shared words
        shared_words = name1_words.intersection(name2_words)
        
        # Consider similar if they share at least one word and names are not too different
        return len(shared_words) > 0 and abs(len(name1) - len(name2)) <= 3
    
    def _contexts_similar(self, context1: str, context2: str) -> bool:
        """Check if two contexts are similar"""
        # Simple context similarity check
        context1_words = set(context1.lower().split())
        context2_words = set(context2.lower().split())
        
        # Consider similar if they share at least 2 words
        return len(context1_words.intersection(context2_words)) >= 2
    
    def _identify_context_dependencies(self, concept: dict, original_text: str) -> list:
        """Identify context dependencies"""
        dependencies = []
        
        context = concept.get("context", "").lower()
        
        # Common context dependencies
        if "business" in context:
            dependencies.append("Business environment and market conditions")
        if "technical" in context:
            dependencies.append("Technical infrastructure and capabilities")
        if "social" in context:
            dependencies.append("Social dynamics and human factors")
        if "legal" in context:
            dependencies.append("Legal framework and regulations")
        if "economic" in context:
            dependencies.append("Economic conditions and constraints")
        
        return dependencies
    
    def _generate_examples(self, core_concepts: list, boundaries: dict) -> list:
        """Generate concrete examples for concepts"""
        examples = []
        
        for concept in core_concepts:
            concept_name = concept["name"]
            concept_examples = []
            
            # Generate different types of examples
            concept_examples.extend(self._generate_positive_examples(concept))
            concept_examples.extend(self._generate_negative_examples(concept))
            concept_examples.extend(self._generate_boundary_examples(concept, boundaries[concept_name]))
            concept_examples.extend(self._generate_practical_examples(concept))
            
            examples.append({
                "concept": concept_name,
                "examples": concept_examples
            })
        
        return examples
    
    def _generate_positive_examples(self, concept: dict) -> list:
        """Generate positive examples of the concept"""
        concept_name = concept["name"]
        examples = []
        
        # Generic positive examples
        examples.append(f"Clear demonstration of {concept_name} in action")
        examples.append(f"Successful implementation of {concept_name}")
        examples.append(f"Effective use of {concept_name} principles")
        
        # Concept-specific examples
        if "system" in concept_name:
            examples.append("A well-functioning ecosystem where components interact effectively")
            examples.append("An organized structure with clear boundaries and interfaces")
        elif "process" in concept_name:
            examples.append("A step-by-step procedure that consistently produces desired results")
            examples.append("An efficient workflow that transforms inputs into outputs")
        elif "model" in concept_name:
            examples.append("An accurate representation that simplifies complex reality")
            examples.append("A useful abstraction that aids understanding and prediction")
        elif "framework" in concept_name:
            examples.append("A comprehensive structure that guides development and decisions")
            examples.append("A flexible system that adapts to changing requirements")
        
        return examples
    
    def _generate_negative_examples(self, concept: dict) -> list:
        """Generate negative examples (what the concept is NOT)"""
        concept_name = concept["name"]
        examples = []
        
        # Generic negative examples
        examples.append(f"Something completely different from {concept_name}")
        examples.append(f"A poor implementation of {concept_name} principles")
        examples.append(f"An example that lacks core characteristics of {concept_name}")
        
        # Concept-specific negative examples
        if "system" in concept_name:
            examples.append("A single isolated component without interactions")
            examples.append("A chaotic collection without organization")
        elif "process" in concept_name:
            examples.append("A random sequence of actions without purpose")
            examples.append("A static state that doesn't transform anything")
        elif "model" in concept_name:
            examples.append("An overly complex representation that confuses rather than clarifies")
            examples.append("An inaccurate representation that misleads understanding")
        elif "framework" in concept_name:
            examples.append("A rigid structure that cannot adapt")
            examples.append("A collection of unrelated rules without coherence")
        
        return examples
    
    def _generate_boundary_examples(self, concept: dict, boundaries: dict) -> list:
        """Generate examples that test the boundaries"""
        concept_name = concept["name"]
        examples = []
        
        # Examples near the boundary
        if boundaries["adjacent_concepts"]:
            for adjacent in boundaries["adjacent_concepts"][:3]:
                examples.append(f"Something that might be confused with {adjacent} but is actually {concept_name}")
                examples.append(f"An implementation that shares characteristics with {adjacent} but maintains {concept_name} identity")
        
        return examples
    
    def _generate_practical_examples(self, concept: dict) -> list:
        """Generate practical, real-world examples"""
        concept_name = concept["name"]
        examples = []
        
        # Industry-specific examples
        if "system" in concept_name:
            examples.append("Enterprise software architecture with microservices")
            examples.append("Ecosystem management in environmental science")
        elif "process" in concept_name:
            examples.append("Software development lifecycle with clear stages")
            examples.append("Manufacturing process with quality control checkpoints")
        elif "model" in concept_name:
            examples.append("Machine learning model for prediction")
            examples.append("Business model for revenue generation")
        elif "framework" in concept_name:
            examples.append("Agile framework for project management")
            examples.append("Regulatory compliance framework for healthcare")
        
        return examples
    
    def _identify_related_concepts(self, core_concepts: list) -> list:
        """Identify related concepts that might be confused"""
        related = []
        
        for concept in core_concepts:
            concept_name = concept["name"]
            related_concepts = []
            
            # Find related concepts based on patterns
            if "system" in concept_name:
                related_concepts.extend(["process", "framework", "model", "architecture", "structure"])
            elif "process" in concept_name:
                related_concepts.extend(["system", "workflow", "procedure", "method", "algorithm"])
            elif "model" in concept_name:
                related_concepts.extend(["system", "framework", "theory", "hypothesis", "simulation"])
            elif "framework" in concept_name:
                related_concepts.extend(["system", "structure", "methodology", "standard", "guideline"])
            
            # Add to related list
            for related in related_concepts:
                if related != concept_name and related not in [c["name"] for c in core_concepts]:
                    related.append({
                        "concept": concept_name,
                        "related_concept": related,
                        "relationship": self._describe_relationship(concept_name, related),
                        "clarification": self._generate_clarification(concept_name, related)
                    })
        
        return related
    
    def _describe_relationship(self, concept1: str, concept2: str) -> str:
        """Describe the relationship between two concepts"""
        relationships = {
            ("system", "process"): "A system contains processes, while processes are components of systems",
            ("process", "system"): "A process is a component of a system, while a system contains processes",
            ("model", "system"): "A model represents a system, while a system is modeled",
            ("system", "model"): "A system is modeled by models, while models represent systems",
            ("framework", "system"): "A framework provides structure for systems, while systems implement frameworks",
            ("system", "framework"): "A system follows a framework, while frameworks guide systems",
            ("process", "workflow"): "A process is a type of workflow with specific steps",
            ("model", "theory"): "A model is based on theory, while theory is represented by models"
        }
        
        return relationships.get((concept1, concept2), "Related concepts with overlapping characteristics")
    
    def _generate_clarification(self, concept1: str, concept2: str) -> str:
        """Generate clarification for distinguishing two concepts"""
        clarifications = {
            ("system", "process"): "Systems are broader than processes - systems contain processes, while processes are the specific steps within systems",
            ("model", "system"): "Models are representations of systems, while systems are the actual entities being modeled",
            ("framework", "system"): "Frameworks provide the structure for systems, while systems are the actual implementations"
        }
        
        return clarifications.get((concept1, concept2), f"Distinguish between {concept1} and {concept2} based on scope and purpose")
    
    def _create_structured_definition(
        self,
        core_concepts: list,
        first_principles: dict,
        boundaries: dict,
        examples: dict,
        related_concepts: list
    ) -> dict:
        """Create a structured definition for the vague idea"""
        structured_definition = {
            "executive_summary": self._create_executive_summary(core_concepts),
            "core_concepts": core_concepts,
            "first_principles_analysis": first_praritys,
            "boundaries_and_scope": boundaries,
            "examples": examples,
            "related_concepts": related_concepts,
            "clarification_checklist": self._create_clarification_checklist(),
            "next_steps": self._suggest_next_steps(core_concepts)
        }
        
        return structured_definition
    
    def _create_executive_summary(self, core_concepts: list) -> str:
        """Create an executive summary of the refined concept"""
        if len(core_concepts) == 1:
            concept = core_concepts[0]
            return f"The concept of {concept['name'].title()} has been clarified from vague to structured, with clear boundaries, essential properties, and practical examples."
        else:
            concept_names = [c["name"] for c in core_concepts]
            return f"The concepts of {', '.join(concept_names)} have been clarified from vague to structured, with clear boundaries, essential properties, and practical examples for each."
    
    def _create_clarification_checklist(self) -> list:
        """Create a checklist for further clarification"""
        return [
            "Are the boundaries clearly defined?",
            "Are the essential properties comprehensive?",
            "Are the examples representative and diverse?",
            "Are related concepts properly distinguished?",
            "Is the scope appropriate for the context?",
            "Are first principles assumptions valid?",
            "Is the definition actionable and useful?"
        ]
    
    def _suggest_next_steps(self, core_concepts: list) -> list:
        """Suggest next steps for refinement"""
        steps = []
        
        for concept in core_concepts:
            concept_name = concept["name"]
            steps.append(f"Test the definition of {concept_name} with real-world examples")
            steps.append(f"Get feedback from domain experts on {concept_name}")
            steps.append(f"Refine the boundaries of {concept_name} based on usage")
        
        steps.append("Document the refined definitions for consistent use")
        steps.append("Create visual diagrams to illustrate relationships")
        steps.append("Develop training materials for stakeholders")
        
        return steps
    
    def _calculate_clarity_score(self, structured_definition: dict) -> float:
        """Calculate an overall clarity score"""
        score = 0.0
        
        # Core concepts clarity
        core_concepts = structured_definition.get("core_concepts", [])
        if core_concepts:
            avg_vagueness = sum(c.get("vagueness_score", 0.5) for c in core_concepts) / len(core_concepts)
            score += (1 - avg_vagueness) * 0.3
        
        # First principles depth
        first_principles = structured_definition.get("first_principles_analysis", {})
        if first_principles:
            avg_depth = sum(len(fp.get("fundamental_truths", [])) for fp in first_principles.values()) / len(first_principles)
            score += min(avg_depth / 5, 1.0) * 0.2
        
        # Boundary clarity
        boundaries = structured_definition.get("boundaries_and_scope", {})
        if boundaries:
            avg_boundaries = sum(1 for b in boundaries.values() if b.get("inclusion_criteria")) / len(boundaries)
            score += avg_boundaries * 0.2
        
        # Example quality
        examples = structured_definition.get("examples", [])
        if examples:
            avg_examples = sum(len(e.get("examples", [])) for e in examples) / len(examples)
            score += min(avg_examples / 4, 1.0) * 0.2
        
        # Related concepts
        related = structured_definition.get("related_concepts", [])
        if related:
            score += 0.1  # Bonus for having related concepts
        
        return min(score, 1.0)


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_clarity_refiner():
        agent = ClarityRefinerAgent()
        
        vague_idea = """
        We need to build some kind of AI system that can help with business decisions. 
        It should be flexible and scalable, and work well with our existing processes.
        """
        
        result = await agent.process(vague_idea)
        
        print("=== Clarity Refiner Agent Test ===")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Clarity Score: {result.content['clarity_score']:.2f}")
        print(f"Core Concepts: {len(result.content['core_concepts'])}")
        print(f"Examples Generated: {result.content['examples'][0]['examples_count'] if result.content['examples'] else 0}")
        
        print("\nExecutive Summary:")
        print(result.content['executive_summary'])
        
        print("\nTop 3 Next Steps:")
        for i, step in enumerate(result.content['next_steps'][:3], 1):
            print(f"{i}. {step}")
    
    # Run test
    asyncio.run(test_clarity_refiner())