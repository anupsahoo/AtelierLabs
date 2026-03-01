"""
Bias Detector Agent

Detects cognitive biases in text and decisions using critical thinking and probabilistic reasoning.
Helps identify patterns of irrational thinking and suggests more objective perspectives.

Mental Models Used:
- Critical Thinking
- Probabilistic Reasoning
- Cognitive Bias Framework
"""


from .core.base_agent import CognitiveAgent, AgentResult
from .core.mental_models import MentalModelsLibrary


class BiasDetectorAgent(CognitiveAgent):
    """
    Agent that detects cognitive biases in text and decisions.
    
    Purpose: Detect cognitive biases in text and decisions
    Input: Text content or decision description
    Output: Bias analysis with confidence scores and mitigation suggestions
    Mental Models: Critical Thinking, Probabilistic Reasoning, Cognitive Bias Framework
    """
    
    def __init__(self):
        super().__init__(
            name="Bias Detector",
            category="cognitive",
            mental_models=[MentalModelsLibrary.PROBABILISTIC_THINKING],
            description="Detects cognitive biases in text and decisions using critical thinking",
            capabilities=[
                "Identify common cognitive biases",
                "Assess bias probability and impact",
                "Provide debiasing strategies",
                "Explain bias mechanisms",
                "Suggest objective alternatives"
            ]
        )
        
        # Cognitive bias definitions
        self.biases = {
            "confirmation_bias": {
                "description": "Tendency to search for, interpret, and recall information that confirms one's preexisting beliefs",
                "indicators": ["only", "always", "never", "obviously", "clearly", "proves"],
                "debiasing_strategy": "Seek disconfirming evidence and consider alternative explanations"
            },
            "anchoring_bias": {
                "description": "Tendency to rely too heavily on the first piece of information encountered",
                "indicators": ["initial", "first", "starting point", "based on", "given"],
                "debiasing_strategy": "Generate multiple anchors and consider information independently"
            },
            "availability_heuristic": {
                "description": "Overestimating the likelihood of events that are more easily recalled",
                "indicators": ["recent", "vivid", "memorable", "dramatic", "shocking"],
                "debiasing_strategy": "Use base rates and statistical data rather than vivid examples"
            },
            "overconfidence_bias": {
                "description": "Excessive confidence in one's own answers, judgments, and abilities",
                "indicators": ["certain", "sure", "definitely", "guaranteed", "no doubt"],
                "debiasing_strategy": "Consider confidence intervals and probability distributions"
            },
            "sunk_cost_fallacy": {
                "description": "Continuing a behavior or endeavor as a result of previously invested resources",
                "indicators": ["already invested", "can't waste", "too much effort", "we've come this far"],
                "debiasing_strategy": "Evaluate decisions based on future costs and benefits, not past investments"
            },
            "bandwagon_effect": {
                "description": "Doing something primarily because other people are doing it",
                "indicators": ["everyone", "popular", "trending", "most people", "common"],
                "debiasing_strategy": "Evaluate based on independent analysis rather than popularity"
            },
            "dunning_kruger": {
                "description": "Low-ability individuals tend to overestimate their own ability",
                "indicators": ["easy", "simple", "obvious", "anyone can", "no problem"],
                "debiasing_strategy": "Seek expert feedback and consider the complexity of the domain"
            },
            "negativity_bias": {
                "description": "Tendency to pay more attention to negative information",
                "indicators": ["risk", "danger", "problem", "threat", "worst case"],
                "debiasing_strategy": "Balance negative information with positive outcomes and base rates"
            }
        }
    
    async def process_input(self, input_data: str, context: dict = None) -> AgentResult:
        """Process text to detect cognitive biases"""
        reasoning_trace = []
        
        # Step 1: Parse and analyze the input text
        reasoning_trace.append("Parsing and analyzing the input text for bias indicators")
        text_analysis = self._analyze_text(input_data)
        reasoning_trace.append(f"Text analysis completed: {len(text_analysis['sentences'])} sentences analyzed")
        
        # Step 2: Detect potential biases
        reasoning_trace.append("Scanning for cognitive bias indicators")
        detected_biases = self._detect_biases(text_analysis)
        reasoning_trace.append(f"Detected {len(detected_biases)} potential biases")
        
        # Step 3: Assess bias probability and impact
        reasoning_trace.append("Assessing bias probability and impact levels")
        bias_assessment = self._assess_biases(detected_biases, text_analysis)
        reasoning_trace.append("Bias assessment completed with confidence scores")
        
        # Step 4: Generate debiasing strategies
        reasoning_trace.append("Generating debiasing strategies and recommendations")
        debiasing_strategies = self._generate_debiasing_strategies(bias_assessment)
        reasoning_trace.append(f"Generated {len(debiasing_strategies)} debiasing strategies")
        
        # Step 5: Create objective alternative perspectives
        reasoning_trace.append("Creating objective alternative perspectives")
        objective_alternatives = self._generate_objective_alternatives(bias_assessment, input_data)
        reasoning_trace.append("Objective alternatives generated")
        
        # Step 6: Compile comprehensive bias analysis
        reasoning_trace.append("Compiling comprehensive bias analysis report")
        bias_report = self._compile_bias_report(
            text_analysis, detected_biases, bias_assessment, 
            debiasing_strategies, objective_alternatives
        )
        
        return AgentResult(
            content=bias_report,
            confidence=0.85,
            reasoning_trace=reasoning_trace,
            mental_models_used=self.mental_models,
            processing_time=0.0,
            metadata={
                "total_biases_detected": len(detected_biases),
                "high_risk_biases": len([b for b in bias_assessment if b.get("risk_level") == "high"]),
                "text_length": len(input_data),
                "bias_types": list(set(b.get("bias_type") for b in detected_biases))
            }
        )
    
    def _analyze_text(self, text: str) -> dict:
        """Analyze text structure and content"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        words = text.split()
        
        return {
            "original_text": text,
            "sentences": sentences,
            "word_count": len(words),
            "sentence_count": len(sentences),
            "certainty_words": self._extract_certainty_words(text),
            "absolute_terms": self._extract_absolute_terms(text),
            "emotional_words": self._extract_emotional_words(text),
            "statistical_terms": self._extract_statistical_terms(text)
        }
    
    def _extract_certainty_words(self, text: str) -> list:
        """Extract words that indicate certainty"""
        certainty_words = [
            "certain", "sure", "definitely", "absolutely", "guaranteed", "without doubt",
            "obviously", "clearly", "undoubtedly", "unquestionably", "no doubt"
        ]
        
        text_lower = text.lower()
        found_words = []
        
        for word in certainty_words:
            if word in text_lower:
                found_words.append(word)
        
        return found_words
    
    def _extract_absolute_terms(self, text: str) -> list:
        """Extract absolute terms that indicate bias"""
        absolute_terms = [
            "always", "never", "only", "every", "all", "none", "perfect", "impossible",
            "completely", "totally", "entirely", "absolutely", "exactly"
        ]
        
        text_lower = text.lower()
        found_terms = []
        
        for term in absolute_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms
    
    def _extract_emotional_words(self, text: str) -> list:
        """Extract emotionally charged words"""
        emotional_words = [
            "amazing", "terrible", "awful", "wonderful", "horrible", "fantastic",
            "disaster", "tragedy", "miracle", "nightmare", "dream", "nightmare",
            "love", "hate", "fear", "anger", "joy", "sad", "happy", "excited"
        ]
        
        text_lower = text.lower()
        found_words = []
        
        for word in emotional_words:
            if word in text_lower:
                found_words.append(word)
        
        return found_words
    
    def _extract_statistical_terms(self, text: str) -> list:
        """Extract statistical and probabilistic terms"""
        statistical_terms = [
            "probability", "likelihood", "chance", "risk", "odds", "percentage",
            "average", "mean", "median", "mode", "distribution", "sample",
            "confidence", "margin", "error", "significant", "correlation"
        ]
        
        text_lower = text.lower()
        found_terms = []
        
        for term in statistical_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms
    
    def _detect_biases(self, text_analysis: dict) -> list:
        """Detect potential biases in the text"""
        detected_biases = []
        text = text_analysis["original_text"].lower()
        
        for bias_type, bias_info in self.biases.items():
            bias_score = 0
            evidence = []
            
            # Check for bias indicators
            for indicator in bias_info["indicators"]:
                if indicator in text:
                    bias_score += 1
                    # Find context around the indicator
                    words = text.split()
                    for i, word in enumerate(words):
                        if indicator in word:
                            context_start = max(0, i - 5)
                            context_end = min(len(words), i + 6)
                            context = " ".join(words[context_start:context_end])
                            evidence.append(context)
            
            # Additional bias-specific detection logic
            if bias_type == "confirmation_bias":
                bias_score += self._detect_confirmation_bias(text_analysis)
            elif bias_type == "overconfidence_bias":
                bias_score += len(text_analysis["certainty_words"]) * 0.5
            elif bias_type == "negativity_bias":
                bias_score += len(text_analysis["emotional_words"]) * 0.3
            elif bias_type == "availability_heuristic":
                bias_score += self._detect_availability_heuristic(text_analysis)
            
            if bias_score > 0:
                detected_biases.append({
                    "bias_type": bias_type,
                    "description": bias_info["description"],
                    "score": min(bias_score / 5, 1.0),  # Normalize to 0-1
                    "evidence": evidence,
                    "debiasing_strategy": bias_info["debiasing_strategy"]
                })
        
        return detected_biases
    
    def _detect_confirmation_bias(self, text_analysis: dict) -> float:
        """Detect confirmation bias patterns"""
        score = 0.0
        
        # Check for selective evidence presentation
        if text_analysis["statistical_terms"] == []:
            score += 0.5  # No statistical evidence
        
        # Check for one-sided arguments
        if len(text_analysis["absolute_terms"]) > 2:
            score += 0.3
        
        # Check for lack of alternative perspectives
        alternative_words = ["however", "although", "despite", "conversely", "alternatively"]
        text_lower = text_analysis["original_text"].lower()
        
        if not any(word in text_lower for word in alternative_words):
            score += 0.2
        
        return score
    
    def _detect_availability_heuristic(self, text_analysis: dict) -> float:
        """Detect availability heuristic patterns"""
        score = 0.0
        
        # Check for vivid, memorable examples
        if len(text_analysis["emotional_words"]) > 3:
            score += 0.4
        
        # Check for recent time references
        recent_words = ["recently", "yesterday", "last week", "just", "today"]
        text_lower = text_analysis["original_text"].lower()
        
        for word in recent_words:
            if word in text_lower:
                score += 0.2
                break
        
        return score
    
    def _assess_biases(self, detected_biases: list, text_analysis: dict) -> list:
        """Assess the probability and impact of detected biases"""
        assessed_biases = []
        
        for bias in detected_biases:
            # Calculate probability based on score and text characteristics
            base_probability = bias["score"]
            
            # Adjust probability based on text characteristics
            if len(text_analysis["certainty_words"]) > 3:
                base_probability += 0.2
            
            if len(text_analysis["absolute_terms"]) > 2:
                base_probability += 0.1
            
            # Determine risk level
            if base_probability > 0.7:
                risk_level = "high"
            elif base_probability > 0.4:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            # Calculate impact score
            impact_score = self._calculate_impact_score(bias["bias_type"], base_probability)
            
            assessed_biases.append({
                **bias,
                "probability": min(base_probability, 1.0),
                "risk_level": risk_level,
                "impact_score": impact_score,
                "confidence": 0.8 - (0.2 * (1 - base_probability))  # Higher confidence for higher scores
            })
        
        return assessed_biases
    
    def _calculate_impact_score(self, bias_type: str, probability: float) -> float:
        """Calculate the potential impact of the bias"""
        impact_weights = {
            "confirmation_bias": 0.9,  # High impact - affects evidence evaluation
            "overconfidence_bias": 0.8,  # High impact - affects decision quality
            "anchoring_bias": 0.7,  # Medium-high impact - affects judgment
            "sunk_cost_fallacy": 0.8,  # High impact - affects resource allocation
            "negativity_bias": 0.6,  # Medium impact - affects risk assessment
            "bandwagon_effect": 0.5,  # Medium impact - affects independence
            "dunning_kruger": 0.7,  # Medium-high impact - affects self-assessment
            "availability_heuristic": 0.6  # Medium impact - affects probability judgment
        }
        
        weight = impact_weights.get(bias_type, 0.5)
        return weight * probability
    
    def _generate_debiasing_strategies(self, bias_assessment: list) -> list:
        """Generate debiasing strategies for detected biases"""
        strategies = []
        
        for bias in bias_assessment:
            strategy = {
                "bias_type": bias["bias_type"],
                "strategy": bias["debiasing_strategy"],
                "priority": "high" if bias["risk_level"] == "high" else "medium" if bias["risk_level"] == "medium" else "low",
                "specific_actions": self._generate_specific_actions(bias)
            }
            strategies.append(strategy)
        
        # Add general debiasing strategies
        general_strategies = [
            {
                "bias_type": "general",
                "strategy": "Consider multiple perspectives and seek disconfirming evidence",
                "priority": "high",
                "specific_actions": [
                    "Actively search for evidence that contradicts your initial position",
                    "Consult with people who have different viewpoints",
                    "Use structured decision-making frameworks"
                ]
            },
            {
                "bias_type": "general",
                "strategy": "Use probabilistic thinking and statistical reasoning",
                "priority": "medium",
                "specific_actions": [
                    "Replace absolute statements with probability estimates",
                    "Consider base rates and statistical data",
                    "Use confidence intervals instead of point estimates"
                ]
            }
        ]
        
        strategies.extend(general_strategies)
        
        return strategies
    
    def _generate_specific_actions(self, bias: dict) -> list:
        """Generate specific actions for a particular bias"""
        bias_type = bias["bias_type"]
        
        if bias_type == "confirmation_bias":
            return [
                "Create a list of arguments against your position",
                "Ask someone who disagrees with you to review your reasoning",
                "Look for evidence that would prove you wrong"
            ]
        elif bias_type == "overconfidence_bias":
            return [
                "Express confidence as a range (60-80% instead of 100%)",
                "Consider what could go wrong",
                "Seek expert validation of your assumptions"
            ]
        elif bias_type == "sunk_cost_fallacy":
            return [
                "Evaluate the decision based only on future costs and benefits",
                "Ask: 'Would I make this decision if I hadn't invested anything yet?'",
                "Consider the opportunity cost of continuing"
            ]
        elif bias_type == "negativity_bias":
            return [
                "Balance negative information with positive outcomes",
                "Use base rates and statistical data",
                "Consider the most likely outcome, not just the worst case"
            ]
        else:
            return [
                "Pause and reflect on your reasoning process",
                "Consider alternative explanations",
                "Seek diverse perspectives"
            ]
    
    def _generate_objective_alternatives(self, bias_assessment: list, original_text: str) -> list:
        """Generate objective alternative perspectives"""
        alternatives = []
        
        # Alternative 1: Remove biased language
        objective_text = self._remove_bias_language(original_text, bias_assessment)
        alternatives.append({
            "type": "objective_language",
            "description": "Rewritten text with bias indicators removed",
            "content": objective_text,
            "explanation": "This version removes absolute terms and emotional language"
        })
        
        # Alternative 2: Add probabilistic thinking
        probabilistic_text = self._add_probabilistic_thinking(original_text)
        alternatives.append({
            "type": "probabilistic",
            "description": "Text with probability estimates and uncertainty",
            "content": probabilistic_text,
            "explanation": "This version adds probability estimates and acknowledges uncertainty"
        })
        
        # Alternative 3: Consider alternative perspectives
        alternative_perspective = self._generate_alternative_perspective(original_text)
        alternatives.append({
            "type": "alternative_perspective",
            "description": "Alternative viewpoint on the same issue",
            "content": alternative_perspective,
            "explanation": "This version considers the opposite or alternative viewpoint"
        })
        
        return alternatives
    
    def _remove_bias_language(self, text: str, bias_assessment: list) -> str:
        """Remove biased language from text"""
        biased_terms = set()
        
        for bias in bias_assessment:
            bias_type = bias["bias_type"]
            if bias_type in self.biases:
                biased_terms.update(self.biases[bias_type]["indicators"])
        
        # Replace biased terms with more neutral language
        replacements = {
            "always": "often",
            "never": "rarely",
            "only": "primarily",
            "definitely": "likely",
            "obviously": "apparently",
            "clearly": "evidently",
            "proves": "suggests",
            "guaranteed": "expected"
        }
        
        text_lower = text.lower()
        for biased, neutral in replacements.items():
            text_lower = text_lower.replace(biased, neutral)
        
        return text_lower
    
    def _add_probabilistic_thinking(self, text: str) -> str:
        """Add probabilistic thinking to the text"""
        # This is a simplified implementation
        # In practice, would use more sophisticated NLP
        
        text_with_prob = text
        
        # Add uncertainty statements
        if "definitely" in text.lower() or "certainly" in text.lower():
            text_with_prob = text.replace("definitely", "likely (70-80% confidence)")
            text_with_prob = text_with_prob.replace("certainly", "probably (60-70% confidence)")
        
        # Add probability ranges
        if "always" in text.lower():
            text_with_prob = text_with_prob.replace("always", "in most cases (80-90% of instances)")
        
        if "never" in text.lower():
            text_with_prob = text_with_prob.replace("never", "rarely (5-10% of instances)")
        
        return text_with_prob
    
    def _generate_alternative_perspective(self, text: str) -> str:
        """Generate an alternative perspective on the text"""
        # This is a simplified implementation
        # In practice, would use more sophisticated reasoning
        
        # Find the main claim and create a counter-claim
        sentences = text.split('.')
        main_claim = sentences[0] if sentences else text
        
        # Simple alternative perspective generation
        if "good" in main_claim.lower():
            alternative = f"However, there are also potential downsides to consider: {main_claim}"
        elif "bad" in main_claim.lower():
            alternative = f"On the other hand, there might be some benefits to consider: {main_claim}"
        else:
            alternative = f"An alternative perspective might be: {main_claim}"
        
        return alternative
    
    def _compile_bias_report(
        self, 
        text_analysis: dict, 
        detected_biases: list, 
        bias_assessment: list,
        debiasing_strategies: list,
        objective_alternatives: list
    ) -> dict:
        """Compile comprehensive bias analysis report"""
        
        # Calculate overall bias risk
        high_risk_count = len([b for b in bias_assessment if b["risk_level"] == "high"])
        medium_risk_count = len([b for b in bias_assessment if b["risk_level"] == "medium"])
        
        overall_risk = "high" if high_risk_count >= 2 else "medium" if high_risk_count >= 1 or medium_risk_count >= 2 else "low"
        
        return {
            "text_analysis": {
                "word_count": text_analysis["word_count"],
                "sentence_count": text_analysis["sentence_count"],
                "certainty_words": text_analysis["certainty_words"],
                "absolute_terms": text_analysis["absolute_terms"],
                "emotional_words": text_analysis["emotional_words"],
                "statistical_terms": text_analysis["statistical_terms"]
            },
            "bias_detection": {
                "total_biases_detected": len(detected_biases),
                "bias_types": list(set(b["bias_type"] for b in detected_biases)),
                "high_risk_biases": high_risk_count,
                "medium_risk_biases": medium_risk_count,
                "overall_risk_level": overall_risk
            },
            "detailed_biases": bias_assessment,
            "debiasing_strategies": debiasing_strategies,
            "objective_alternatives": objective_alternatives,
            "recommendations": self._generate_recommendations(bias_assessment, overall_risk),
            "confidence_score": self._calculate_overall_confidence(bias_assessment)
        }
    
    def _generate_recommendations(self, bias_assessment: list, overall_risk: str) -> list:
        """Generate recommendations based on bias assessment"""
        recommendations = []
        
        if overall_risk == "high":
            recommendations.append("Review the text carefully before making decisions based on it")
            recommendations.append("Seek external validation from unbiased sources")
            recommendations.append("Consider using structured decision-making frameworks")
        elif overall_risk == "medium":
            recommendations.append("Be aware of potential biases in the reasoning")
            recommendations.append("Consider alternative perspectives")
        else:
            recommendations.append("The text appears relatively unbiased")
            recommendations.append("Continue to monitor for bias in future communications")
        
        # Add specific recommendations based on detected biases
        bias_types = set(b["bias_type"] for b in bias_assessment)
        
        if "confirmation_bias" in bias_types:
            recommendations.append("Actively seek disconfirming evidence")
        
        if "overconfidence_bias" in bias_types:
            recommendations.append("Use probability estimates instead of absolute statements")
        
        if "sunk_cost_fallacy" in bias_types:
            recommendations.append("Evaluate decisions based on future costs and benefits only")
        
        return recommendations
    
    def _calculate_overall_confidence(self, bias_assessment: list) -> float:
        """Calculate overall confidence in the bias assessment"""
        if not bias_assessment:
            return 0.5
        
        avg_confidence = sum(b["confidence"] for b in bias_assessment) / len(bias_assessment)
        
        # Adjust confidence based on the number of biases detected
        bias_count_factor = min(len(bias_assessment) / 5, 1.0)  # More biases = higher confidence
        
        return avg_confidence * bias_count_factor


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_bias_detector():
        agent = BiasDetectorAgent()
        
        test_text = """
        I definitely think that this new AI system will always work perfectly. 
        Everyone agrees that it's obviously the best solution. 
        We've already invested so much time and money that we can't possibly stop now. 
        The recent failures of other systems prove that our approach is superior.
        """
        
        result = await agent.process(test_text)
        
        print("=== Bias Detector Agent Test ===")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Overall Risk Level: {result.content['bias_detection']['overall_risk_level']}")
        print(f"Biases Detected: {result.content['bias_detection']['total_biases_detected']}")
        
        print("\nTop 3 Recommendations:")
        for i, rec in enumerate(result.content['recommendations'][:3], 1):
            print(f"{i}. {rec}")
    
    # Run test
    asyncio.run(test_bias_detector())