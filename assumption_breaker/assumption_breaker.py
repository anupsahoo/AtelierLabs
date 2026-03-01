"""
Assumption Breaker Agent

Identifies hidden assumptions in ideas and statements using first-principles thinking.
Challenges conventional wisdom and reveals the foundational beliefs that underlie arguments.

Mental Models Used:
- First Principles Thinking
- Inversion
"""


from .core.base_agent import CognitiveAgent, AgentResult
from .core.mental_models import MentalModelsLibrary


class AssumptionBreakerAgent(CognitiveAgent):
    """
    Agent that identifies hidden assumptions using first-principles thinking.
    
    Purpose: List hidden assumptions in any idea
    Input: Text/idea statement
    Output: Structured list of assumptions with confidence scores
    Mental Models: First-principles thinking, inversion
    """
    
    def __init__(self):
        super().__init__(
            name="Assumption Breaker",
            category="cognitive",
            mental_models=[MentalModelsLibrary.FIRST_PRINCIPLES, MentalModelsLibrary.INVERSION],
            description="Identifies hidden assumptions and challenges conventional wisdom",
            capabilities=[
                "Extract explicit and implicit assumptions",
                "Question fundamental beliefs",
                "Apply inversion to test assumptions",
                "Generate alternative perspectives"
            ]
        )
    
    async def process_input(self, input_data: str, context: dict = None) -> AgentResult:
        """Process input text to identify and break assumptions"""
        reasoning_trace = []
        
        # Step 1: Parse and structure the idea
        reasoning_trace.append("Parsing and structuring the input idea")
        structured_idea = self._parse_idea(input_data)
        reasoning_trace.append(f"Idea structured into {len(structured_idea)} components")
        
        # Step 2: Identify explicit assumptions
        reasoning_trace.append("Identifying explicit assumptions")
        explicit_assumptions = self._identify_explicit_assumptions(structured_idea)
        reasoning_trace.append(f"Found {len(explicit_assumptions)} explicit assumptions")
        
        # Step 3: Uncover implicit assumptions
        reasoning_trace.append("Uncovering implicit assumptions")
        implicit_assumptions = self._identify_implicit_assumptions(structured_idea, context)
        reasoning_trace.append(f"Found {len(implicit_assumptions)} implicit assumptions")
        
        # Step 4: Apply inversion to test assumptions
        reasoning_trace.append("Applying inversion to test assumptions")
        inverted_assumptions = self._apply_inversion(explicit_assumptions + implicit_assumptions)
        reasoning_trace.append(f"Generated {len(inverted_assumptions)} inverted perspectives")
        
        # Step 5: Question fundamental beliefs
        reasoning_trace.append("Questioning fundamental beliefs")
        fundamental_questions = self._question_fundamental_beliefs(explicit_assumptions + implicit_assumptions)
        reasoning_trace.append(f"Generated {len(fundamental_questions)} fundamental questions")
        
        # Step 6: Generate assumption breakdown
        reasoning_trace.append("Generating comprehensive assumption breakdown")
        breakdown = self._generate_breakdown(
            structured_idea, 
            explicit_assumptions, 
            implicit_assumptions, 
            inverted_assumptions, 
            fundamental_questions
        )
        
        return AgentResult(
            content=breakdown,
            confidence=0.85,
            reasoning_trace=reasoning_trace,
            mental_models_used=self.mental_models,
            processing_time=0.0,  # Would be calculated in actual implementation
            metadata={
                "total_assumptions": len(explicit_assumptions) + len(implicit_assumptions),
                "idea_complexity": self._assess_complexity(structured_idea)
            }
        )
    
    def _parse_idea(self, input_text: str) -> dict:
        """Parse and structure the input idea"""
        # Simple parsing - in practice would use NLP
        sentences = [s.strip() for s in input_text.split('.') if s.strip()]
        
        return {
            "original_text": input_text,
            "sentences": sentences,
            "key_concepts": self._extract_key_concepts(input_text),
            "claims": self._identify_claims(sentences),
            "certainty_level": self._assess_certainty(input_text)
        }
    
    def _extract_key_concepts(self, text: str) -> list:
        """Extract key concepts from text"""
        # Simplified concept extraction
        # In practice, would use more sophisticated NLP
        important_words = []
        
        # Look for capitalized words (potential concepts)
        import re
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
        important_words.extend(capitalized)
        
        # Look for technical/business terms
        business_terms = [
            "strategy", "process", "system", "model", "framework",
            "market", "customer", "product", "service", "solution",
            "growth", "revenue", "profit", "cost", "investment",
            "technology", "innovation", "digital", "transformation"
        ]
        
        text_lower = text.lower()
        for term in business_terms:
            if term in text_lower:
                important_words.append(term)
        
        return list(set(important_words))
    
    def _identify_claims(self, sentences: list) -> list:
        """Identify claims or assertions in sentences"""
        claims = []
        claim_indicators = [
            "is", "are", "will", "should", "must", "always", "never",
            "proves", "shows", "demonstrates", "ensures", "guarantees"
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(indicator in sentence_lower for indicator in claim_indicators):
                claims.append(sentence)
        
        return claims
    
    def _assess_certainty(self, text: str) -> str:
        """Assess the certainty level of the text"""
        high_certainty = ["definitely", "certainly", "absolutely", "always", "never", "proven"]
        medium_certainty = ["likely", "probably", "usually", "typically", "generally"]
        low_certainty = ["might", "could", "may", "possibly", "perhaps", "potentially"]
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in high_certainty):
            return "high"
        elif any(word in text_lower for word in medium_certainty):
            return "medium"
        elif any(word in text_lower for word in low_certainty):
            return "low"
        else:
            return "neutral"
    
    def _identify_explicit_assumptions(self, structured_idea: dict) -> list:
        """Identify explicit assumptions in the text"""
        assumptions = []
        
        # Look for assumption indicators
        assumption_phrases = [
            "assuming that", "based on the assumption", "under the assumption",
            "presuming that", "given that", "supposing that"
        ]
        
        text = structured_idea["original_text"].lower()
        
        for phrase in assumption_phrases:
            if phrase in text:
                # Extract the assumption (simplified)
                start_idx = text.find(phrase)
                end_idx = text.find(".", start_idx)
                if end_idx > start_idx:
                    assumption = text[start_idx:end_idx + 1]
                    assumptions.append({
                        "type": "explicit",
                        "text": assumption,
                        "confidence": 0.9,
                        "source": "explicit_statement"
                    })
        
        # Look for claims that imply assumptions
        for claim in structured_idea["claims"]:
            implied_assumptions = self._extract_implied_assumptions(claim)
            assumptions.extend(implied_assumptions)
        
        return assumptions
    
    def _identify_implicit_assumptions(self, structured_idea: dict, context: dict = None) -> list:
        """Identify implicit assumptions"""
        assumptions = []
        
        # Common implicit assumptions in business/tech contexts
        common_assumptions = [
            {
                "assumption": "Current market conditions will continue",
                "category": "market_stability",
                "confidence": 0.6
            },
            {
                "assumption": "Technology will continue to improve",
                "category": "technological_progress",
                "confidence": 0.7
            },
            {
                "assumption": "Customer behavior will remain predictable",
                "category": "customer_behavior",
                "confidence": 0.5
            },
            {
                "assumption": "Competitors will not change strategies",
                "category": "competitive_landscape",
                "confidence": 0.4
            },
            {
                "assumption": "Resources will be available as planned",
                "category": "resource_availability",
                "confidence": 0.5
            },
            {
                "assumption": "Regulatory environment will stay stable",
                "category": "regulatory_stability",
                "confidence": 0.6
            }
        ]
        
        # Filter assumptions based on context relevance
        text = structured_idea["original_text"].lower()
        
        for common_assumption in common_assumptions:
            relevance_score = self._calculate_assumption_relevance(
                common_assumption, text, context
            )
            
            if relevance_score > 0.3:
                assumptions.append({
                    "type": "implicit",
                    "text": common_assumption["assumption"],
                    "category": common_assumption["category"],
                    "confidence": common_assumption["confidence"] * relevance_score,
                    "source": "common_pattern",
                    "relevance_score": relevance_score
                })
        
        return assumptions
    
    def _extract_implied_assumptions(self, claim: str) -> list:
        """Extract assumptions implied by a claim"""
        assumptions = []
        
        claim_lower = claim.lower()
        
        # Growth claims imply market assumptions
        if any(word in claim_lower for word in ["grow", "growth", "increase", "expand"]):
            assumptions.append({
                "type": "implied",
                "text": "Market conditions support growth",
                "category": "market_growth",
                "confidence": 0.7,
                "source": "growth_claim"
            })
        
        # Technology claims imply technical feasibility
        if any(word in claim_lower for word in ["technology", "system", "platform", "tool"]):
            assumptions.append({
                "type": "implied",
                "text": "Technical implementation is feasible",
                "category": "technical_feasibility",
                "confidence": 0.6,
                "source": "technology_claim"
            })
        
        # Customer claims assume customer understanding
        if any(word in claim_lower for word in ["customer", "user", "client"]):
            assumptions.append({
                "type": "implied",
                "text": "Customer needs are understood correctly",
                "category": "customer_understanding",
                "confidence": 0.5,
                "source": "customer_claim"
            })
        
        return assumptions
    
    def _calculate_assumption_relevance(self, assumption: dict, text: str, context: dict = None) -> float:
        """Calculate relevance score for an assumption"""
        relevance = 0.0
        
        # Check keyword relevance
        assumption_text = assumption["assumption"].lower()
        keywords = assumption_text.split()
        
        keyword_matches = sum(1 for keyword in keywords if keyword in text)
        keyword_relevance = keyword_matches / len(keywords) if keywords else 0
        relevance += keyword_relevance * 0.5
        
        # Check category relevance
        category = assumption["category"]
        category_keywords = {
            "market_stability": ["market", "economy", "industry", "sector"],
            "technological_progress": ["technology", "innovation", "digital", "ai"],
            "customer_behavior": ["customer", "user", "client", "behavior"],
            "competitive_landscape": ["competitor", "competition", "market"],
            "resource_availability": ["resource", "budget", "team", "investment"],
            "regulatory_stability": ["regulation", "compliance", "legal", "policy"]
        }
        
        if category in category_keywords:
            cat_keywords = category_keywords[category]
            cat_matches = sum(1 for keyword in cat_keywords if keyword in text)
            cat_relevance = cat_matches / len(cat_keywords) if cat_keywords else 0
            relevance += cat_relevance * 0.3
        
        # Context relevance
        if context:
            context_relevance = 0.2  # Placeholder for context-based relevance
            relevance += context_relevance
        
        return min(relevance, 1.0)
    
    def _apply_inversion(self, assumptions: list) -> list:
        """Apply inversion to test assumptions"""
        inverted = []
        
        for assumption in assumptions:
            assumption_text = assumption["text"]
            
            # Generate inverted questions
            inverted_questions = [
                f"What if {assumption_text} is NOT true?",
                f"How would we proceed if {assumption_text} fails?",
                f"What evidence contradicts {assumption_text}?",
                f"Who benefits from {assumption_text} being false?"
            ]
            
            inverted.append({
                "original_assumption": assumption_text,
                "inverted_questions": inverted_questions,
                "testing_approach": self._suggest_testing_approach(assumption_text),
                "risk_if_false": self._assess_risk_if_false(assumption_text)
            })
        
        return inverted
    
    def _suggest_testing_approach(self, assumption: str) -> str:
        """Suggest approach to test an assumption"""
        assumption_lower = assumption.lower()
        
        if "market" in assumption_lower:
            return "Conduct market research and customer interviews"
        elif "technology" in assumption_lower:
            return "Build proof-of-concept and technical validation"
        elif "customer" in assumption_lower:
            return "Run customer surveys and usability tests"
        elif "competitor" in assumption_lower:
            return "Perform competitive analysis and intelligence gathering"
        elif "resource" in assumption_lower:
            return "Create resource allocation plan and secure commitments"
        else:
            return "Gather empirical evidence and expert opinions"
    
    def _assess_risk_if_false(self, assumption: str) -> str:
        """Assess risk level if assumption proves false"""
        assumption_lower = assumption.lower()
        
        if "always" in assumption_lower or "never" in assumption_lower:
            return "High risk - absolute claims are fragile"
        elif "growth" in assumption_lower or "increase" in assumption_lower:
            return "Medium risk - affects revenue projections"
        elif "feasible" in assumption_lower or "possible" in assumption_lower:
            return "High risk - technical feasibility is critical"
        elif "stable" in assumption_lower or "continue" in assumption_lower:
            return "Medium risk - stability assumptions often fail"
        else:
            return "Medium risk - most assumptions have some impact"
    
    def _question_fundamental_beliefs(self, assumptions: list) -> list:
        """Generate fundamental questions about assumptions"""
        questions = []
        
        # Group assumptions by category
        categories = {}
        for assumption in assumptions:
            category = assumption.get("category", "general")
            if category not in categories:
                categories[category] = []
            categories[category].append(assumption["text"])
        
        # Generate fundamental questions for each category
        for category, category_assumptions in categories.items():
            fundamental_questions = [
                f"What evidence supports our {category} assumptions?",
                f"How would we know if our {category} assumptions are wrong?",
                f"What would happen if all {category} assumptions failed simultaneously?",
                f"Who benefits from maintaining these {category} assumptions?",
                f"What historical precedents challenge these {category} assumptions?"
            ]
            
            questions.extend(fundamental_questions)
        
        # Add universal fundamental questions
        universal_questions = [
            "Which assumptions, if proven false, would invalidate the entire idea?",
            "What assumptions are we making without realizing it?",
            "How many layers of assumptions are we building upon?",
            "What would a complete beginner question about this idea?",
            "How would someone from a completely different field view these assumptions?"
        ]
        
        questions.extend(universal_questions)
        
        return questions
    
    def _generate_breakdown(
        self, 
        structured_idea: dict, 
        explicit_assumptions: list, 
        implicit_assumptions: list, 
        inverted_assumptions: list, 
        fundamental_questions: list
    ) -> dict:
        """Generate comprehensive assumption breakdown"""
        
        # Calculate assumption strength
        all_assumptions = explicit_assumptions + implicit_assumptions
        avg_confidence = sum(a.get("confidence", 0.5) for a in all_assumptions) / len(all_assumptions) if all_assumptions else 0
        
        # Identify riskiest assumptions
        riskiest_assumptions = sorted(
            all_assumptions, 
            key=lambda a: 1 - a.get("confidence", 0.5), 
            reverse=True
        )[:5]
        
        # Categorize assumptions
        assumption_categories = {}
        for assumption in all_assumptions:
            category = assumption.get("category", "general")
            if category not in assumption_categories:
                assumption_categories[category] = []
            assumption_categories[category].append(assumption)
        
        return {
            "idea_summary": {
                "original_text": structured_idea["original_text"],
                "key_concepts": structured_idea["key_concepts"],
                "certainty_level": structured_idea["certainty_level"],
                "complexity_score": self._assess_complexity(structured_idea)
            },
            "assumptions_analysis": {
                "total_assumptions": len(all_assumptions),
                "explicit_assumptions": len(explicit_assumptions),
                "implicit_assumptions": len(implicit_assumptions),
                "average_confidence": avg_confidence,
                "riskiest_assumptions": riskiest_assumptions,
                "categories": assumption_categories
            },
            "inversion_analysis": {
                "total_inverted": len(inverted_assumptions),
                "inverted_perspectives": inverted_assumptions
            },
            "fundamental_questions": {
                "total_questions": len(fundamental_questions),
                "critical_questions": fundamental_questions[:10],  # Top 10
                "all_questions": fundamental_questions
            },
            "recommendations": self._generate_recommendations(
                all_assumptions, 
                inverted_assumptions, 
                fundamental_questions
            ),
            "validation_plan": self._create_validation_plan(all_assumptions)
        }
    
    def _assess_complexity(self, structured_idea: dict) -> float:
        """Assess complexity of the idea"""
        complexity_score = 0.0
        
        # Base complexity from sentence count
        complexity_score += len(structured_idea["sentences"]) * 0.1
        
        # Complexity from key concepts
        complexity_score += len(structured_idea["key_concepts"]) * 0.15
        
        # Complexity from claims
        complexity_score += len(structured_idea["claims"]) * 0.2
        
        # Certainty affects complexity (lower certainty = higher complexity)
        certainty = structured_idea["certainty_level"]
        if certainty == "low":
            complexity_score += 0.3
        elif certainty == "medium":
            complexity_score += 0.15
        
        return min(complexity_score, 1.0)
    
    def _generate_recommendations(self, assumptions: list, inverted: list, questions: list) -> list:
        """Generate recommendations based on assumption analysis"""
        recommendations = []
        
        # High-level recommendations
        recommendations.append("Test riskiest assumptions first using empirical evidence")
        recommendations.append("Create contingency plans for high-impact assumptions")
        recommendations.append("Seek diverse perspectives to challenge blind spots")
        
        # Specific recommendations based on findings
        if len(assumptions) > 10:
            recommendations.append("Consider simplifying the idea to reduce assumption burden")
        
        avg_confidence = sum(a.get("confidence", 0.5) for a in assumptions) / len(assumptions) if assumptions else 0
        if avg_confidence < 0.6:
            recommendations.append("Gather more evidence before proceeding")
        
        # Category-specific recommendations
        categories = set(a.get("category", "general") for a in assumptions)
        if "market_stability" in categories:
            recommendations.append("Conduct thorough market analysis and scenario planning")
        if "technical_feasibility" in categories:
            recommendations.append("Build technical prototypes and conduct feasibility studies")
        if "customer_behavior" in categories:
            recommendations.append("Perform extensive customer research and validation")
        
        return recommendations
    
    def _create_validation_plan(self, assumptions: list) -> list:
        """Create a plan to validate key assumptions"""
        validation_plan = []
        
        # Prioritize assumptions by risk and confidence
        prioritized = sorted(
            assumptions,
            key=lambda a: (1 - a.get("confidence", 0.5)) * self._get_impact_weight(a),
            reverse=True
        )
        
        # Create validation steps for top assumptions
        for i, assumption in enumerate(prioritized[:5]):  # Top 5 assumptions
            validation_step = {
                "step": i + 1,
                "assumption": assumption["text"],
                "category": assumption.get("category", "general"),
                "validation_method": self._suggest_testing_approach(assumption["text"]),
                "success_criteria": f"Evidence that supports or refutes: {assumption['text']}",
                "timeline": f"Week {i + 1}",
                "responsible": "Product/Business team"
            }
            validation_plan.append(validation_step)
        
        return validation_plan
    
    def _get_impact_weight(self, assumption: dict) -> float:
        """Get impact weight for an assumption"""
        category = assumption.get("category", "general")
        
        impact_weights = {
            "market_stability": 0.9,
            "technical_feasibility": 0.8,
            "customer_behavior": 0.7,
            "resource_availability": 0.8,
            "competitive_landscape": 0.6,
            "regulatory_stability": 0.5
        }
        
        return impact_weights.get(category, 0.5)


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_assumption_breaker():
        agent = AssumptionBreakerAgent()
        
        test_idea = """
        Our AI-powered SaaS platform will definitely capture 50% of the market within 2 years 
        because customers always want automation and our technology is superior to competitors. 
        The market is growing at 20% annually and customers will pay premium prices for better solutions.
        """
        
        result = await agent.process(test_idea)
        
        print("=== Assumption Breaker Agent Test ===")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Processing Time: {result.processing_time:.2f}s")
        print("\nReasoning Trace:")
        for i, step in enumerate(result.reasoning_trace, 1):
            print(f"{i}. {step}")
        
        print("\nKey Results:")
        print(f"Total Assumptions: {result.content['assumptions_analysis']['total_assumptions']}")
        print(f"Average Confidence: {result.content['assumptions_analysis']['average_confidence']:.2f}")
        
        print("\nTop 3 Recommendations:")
        for i, rec in enumerate(result.content['recommendations'][:3], 1):
            print(f"{i}. {rec}")
    
    # Run test
    asyncio.run(test_assumption_breaker())