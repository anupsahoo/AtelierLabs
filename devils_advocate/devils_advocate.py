"""
Devil's Advocate Agent

Provides logical opposition to test arguments and strengthen reasoning through critical analysis.
Uses logical reasoning and inversion to challenge assumptions and identify weaknesses.

Mental Models Used:
- Logical Reasoning
- Inversion
- Critical Thinking
"""


from .core.base_agent import CognitiveAgent, AgentResult
from .core.mental_models import MentalModelsLibrary


class DevilsAdvocateAgent(CognitiveAgent):
    """
    Agent that provides logical opposition to test arguments.
    
    Purpose: Provide logical opposition to test arguments
    Input: Argument, claim, or position statement
    Output: Structured counter-arguments with evidence and reasoning
    Mental Models: Logical Reasoning, Inversion, Critical Thinking
    """
    
    def __init__(self):
        super().__init__(
            name="Devil's Advocate",
            category="cognitive",
            mental_models=[MentalModelsLibrary.FIRST_PRINCIPLES, MentalModelsLibrary.INVERSION],
            description="Provides logical opposition to test arguments and strengthen reasoning",
            capabilities=[
                "Generate counter-arguments",
                "Identify logical fallacies",
                "Test argument strength",
                "Provide evidence-based opposition",
                "Suggest argument improvements"
            ]
        )
        
        # Logical fallacy definitions
        self.fallacies = {
            "straw_man": {
                "description": "Misrepresenting someone's argument to make it easier to attack",
                "indicators": ["so you're saying", "you believe", "that means"],
                "counter_strategy": "Address the actual argument, not the misrepresentation"
            },
            "ad_hominem": {
                "description": "Attacking the person instead of the argument",
                "indicators": ["you're", "your", "because you"],
                "counter_strategy": "Focus on the argument's merits, not the person"
            },
            "false_dilemma": {
                "description": "Presenting only two options when more exist",
                "indicators": ["either/or", "only choice", "no alternative"],
                "counter_strategy": "Identify and explore alternative options"
            },
            "slippery_slope": {
                "description": "Arguing that a small step will lead to extreme consequences",
                "indicators": ["will lead to", "eventually", "inevitably"],
                "counter_strategy": "Evaluate each step independently"
            },
            "appeal_to_authority": {
                "description": "Using authority as evidence instead of logical reasoning",
                "indicators": ["experts say", "studies show", "authority"],
                "counter_strategy": "Examine the actual evidence and reasoning"
            },
            "circular_reasoning": {
                "description": "The conclusion is included in the premise",
                "indicators": ["because", "therefore", "obviously"],
                "counter_strategy": "Ensure premises support conclusion independently"
            }
        }
    
    async def process_input(self, input_data: str, context: dict = None) -> AgentResult:
        """Process argument to provide logical opposition"""
        reasoning_trace = []
        
        # Step 1: Parse and analyze the argument
        reasoning_trace.append("Parsing and analyzing the argument structure")
        argument_analysis = self._analyze_argument(input_data)
        reasoning_trace.append(f"Argument analysis completed: {len(argument_analysis['claims'])} claims identified")
        
        # Step 2: Identify logical fallacies
        reasoning_trace.append("Scanning for logical fallacies")
        detected_fallacies = self._detect_fallacies(argument_analysis)
        reasoning_trace.append(f"Detected {len(detected_fallacies)} potential logical fallacies")
        
        # Step 3: Generate counter-arguments
        reasoning_trace.append("Generating logical counter-arguments")
        counter_arguments = self._generate_counter_arguments(argument_analysis)
        reasoning_trace.append(f"Generated {len(counter_arguments)} counter-arguments")
        
        # Step 4: Apply inversion to test assumptions
        reasoning_trace.append("Applying inversion to test underlying assumptions")
        inversion_analysis = self._apply_inversion(argument_analysis)
        reasoning_trace.append("Inversion analysis completed")
        
        # Step 5: Identify evidence gaps
        reasoning_trace.append("Identifying evidence gaps and weaknesses")
        evidence_gaps = self._identify_evidence_gaps(argument_analysis)
        reasoning_trace.append(f"Identified {len(evidence_gaps)} evidence gaps")
        
        # Step 6: Generate strengthening recommendations
        reasoning_trace.append("Generating recommendations to strengthen the argument")
        strengthening_recommendations = self._generate_strengthening_recommendations(
            argument_analysis, detected_fallacies, counter_arguments, evidence_gaps
        )
        reasoning_trace.append("Strengthening recommendations generated")
        
        # Step 7: Compile devil's advocate report
        reasoning_trace.append("Compiling comprehensive devil's advocate analysis")
        devil_report = self._compile_devils_advocate_report(
            argument_analysis, detected_fallacies, counter_arguments,
            inversion_analysis, evidence_gaps, strengthening_recommendations
        )
        
        return AgentResult(
            content=devil_report,
            confidence=0.85,
            reasoning_trace=reasoning_trace,
            mental_models_used=self.mental_models,
            processing_time=0.0,
            metadata={
                "total_claims": len(argument_analysis['claims']),
                "fallacies_detected": len(detected_fallacies),
                "counter_arguments": len(counter_arguments),
                "argument_strength": self._assess_argument_strength(argument_analysis)
            }
        )
    
    def _analyze_argument(self, text: str) -> dict:
        """Analyze the structure and content of the argument"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # Identify claims and supporting statements
        claims = []
        supporting_statements = []
        conclusions = []
        
        claim_indicators = ["should", "must", "will", "is", "are", "proves", "shows", "demonstrates"]
        conclusion_indicators = ["therefore", "thus", "consequently", "as a result", "hence"]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check if it's a conclusion
            if any(indicator in sentence_lower for indicator in conclusion_indicators):
                conclusions.append(sentence)
            # Check if it's a claim
            elif any(indicator in sentence_lower for indicator in claim_indicators):
                claims.append(sentence)
            else:
                supporting_statements.append(sentence)
        
        # Extract key terms and concepts
        key_terms = self._extract_key_terms(text)
        
        # Identify evidence types
        evidence_types = self._identify_evidence_types(text)
        
        return {
            "original_text": text,
            "sentences": sentences,
            "claims": claims,
            "supporting_statements": supporting_statements,
            "conclusions": conclusions,
            "key_terms": key_terms,
            "evidence_types": evidence_types,
            "argument_structure": self._analyze_structure(claims, supporting_statements, conclusions)
        }
    
    def _extract_key_terms(self, text: str) -> list:
        """Extract key terms and concepts from the argument"""
        # Simple key term extraction
        words = text.split()
        
        # Filter out common words
        common_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "can", "this", "that", "these", "those"
        }
        
        key_terms = []
        for word in words:
            clean_word = word.lower().strip(".,!?;:")
            if len(clean_word) > 3 and clean_word not in common_words:
                key_terms.append(clean_word)
        
        # Remove duplicates and return most frequent
        term_counts = {}
        for term in key_terms:
            term_counts[term] = term_counts.get(term, 0) + 1
        
        return sorted(term_counts.keys(), key=lambda x: term_counts[x], reverse=True)[:10]
    
    def _identify_evidence_types(self, text: str) -> list:
        """Identify types of evidence used in the argument"""
        evidence_types = []
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["study", "research", "data", "statistics"]):
            evidence_types.append("statistical")
        
        if any(word in text_lower for word in ["expert", "authority", "professional", "specialist"]):
            evidence_types.append("authority")
        
        if any(word in text_lower for word in ["example", "case", "instance", "story"]):
            evidence_types.append("anecdotal")
        
        if any(word in text_lower for word in ["logic", "reason", "because", "therefore"]):
            evidence_types.append("logical")
        
        if any(word in text_lower for word in ["experience", "felt", "saw", "observed"]):
            evidence_types.append("experiential")
        
        return evidence_types
    
    def _analyze_structure(self, claims: list, supporting: list, conclusions: list) -> dict:
        """Analyze the logical structure of the argument"""
        return {
            "claim_count": len(claims),
            "supporting_count": len(supporting),
            "conclusion_count": len(conclusions),
            "support_ratio": len(supporting) / len(claims) if claims else 0,
            "has_conclusion": len(conclusions) > 0,
            "structure_type": self._classify_structure(claims, supporting, conclusions)
        }
    
    def _classify_structure(self, claims: list, supporting: list, conclusions: list) -> str:
        """Classify the argument structure"""
        if not claims:
            return "no_claims"
        elif not supporting:
            return "unsupported_claims"
        elif not conclusions:
            return "no_conclusion"
        elif len(supporting) >= len(claims):
            return "well_supported"
        else:
            return "poorly_supported"
    
    def _detect_fallacies(self, argument_analysis: dict) -> list:
        """Detect logical fallacies in the argument"""
        detected_fallacies = []
        text = argument_analysis["original_text"].lower()
        
        for fallacy_type, fallacy_info in self.fallacies.items():
            fallacy_score = 0
            evidence = []
            
            # Check for fallacy indicators
            for indicator in fallacy_info["indicators"]:
                if indicator in text:
                    fallacy_score += 1
                    # Find context around the indicator
                    words = text.split()
                    for i, word in enumerate(words):
                        if indicator in word:
                            context_start = max(0, i - 3)
                            context_end = min(len(words), i + 4)
                            context = " ".join(words[context_start:context_end])
                            evidence.append(context)
            
            # Additional fallacy-specific detection
            if fallacy_type == "false_dilemma":
                fallacy_score += self._detect_false_dilemma(argument_analysis)
            elif fallacy_type == "slippery_slope":
                fallacy_score += self._detect_slippery_slope(argument_analysis)
            elif fallacy_type == "circular_reasoning":
                fallacy_score += self._detect_circular_reasoning(argument_analysis)
            
            if fallacy_score > 0:
                detected_fallacies.append({
                    "fallacy_type": fallacy_type,
                    "description": fallacy_info["description"],
                    "score": min(fallacy_score / 3, 1.0),  # Normalize to 0-1
                    "evidence": evidence,
                    "counter_strategy": fallacy_info["counter_strategy"]
                })
        
        return detected_fallacies
    
    def _detect_false_dilemma(self, argument_analysis: dict) -> float:
        """Detect false dilemma fallacy"""
        score = 0.0
        text = argument_analysis["original_text"].lower()
        
        # Look for either/or language
        either_or_patterns = ["either/or", "either or", "only choice", "no alternative", "must choose"]
        
        for pattern in either_or_patterns:
            if pattern in text:
                score += 0.5
                break
        
        # Check if only two options are presented
        if len(argument_analysis["key_terms"]) < 3:
            score += 0.3
        
        return score
    
    def _detect_slippery_slope(self, argument_analysis: dict) -> float:
        """Detect slippery slope fallacy"""
        score = 0.0
        text = argument_analysis["original_text"].lower()
        
        # Look for chain reaction language
        chain_patterns = ["will lead to", "will cause", "eventually", "inevitably", "domino effect"]
        
        for pattern in chain_patterns:
            if pattern in text:
                score += 0.5
                break
        
        # Check for extreme consequences
        extreme_words = ["disaster", "catastrophe", "collapse", "destroy", "ruin"]
        
        for word in extreme_words:
            if word in text:
                score += 0.3
                break
        
        return score
    
    def _detect_circular_reasoning(self, argument_analysis: dict) -> float:
        """Detect circular reasoning fallacy"""
        score = 0.0
        text = argument_analysis["original_text"].lower()
        
        # Check if conclusion is repeated in premises
        if argument_analysis["conclusions"]:
            for conclusion in argument_analysis["conclusions"]:
                conclusion_lower = conclusion.lower()
                # Simple check: if conclusion words appear in supporting statements
                for supporting in argument_analysis["supporting_statements"]:
                    if conclusion_lower in supporting.lower():
                        score += 0.4
                        break
        
        return score
    
    def _generate_counter_arguments(self, argument_analysis: dict) -> list:
        """Generate logical counter-arguments"""
        counter_arguments = []
        
        # Counter each claim
        for claim in argument_analysis["claims"]:
            counter_arg = self._counter_claim(claim, argument_analysis)
            counter_arguments.append(counter_arg)
        
        # Question evidence
        for evidence_type in argument_analysis["evidence_types"]:
            counter_arg = self._question_evidence(evidence_type, argument_analysis)
            counter_arguments.append(counter_arg)
        
        # Challenge conclusions
        for conclusion in argument_analysis["conclusions"]:
            counter_arg = self._challenge_conclusion(conclusion, argument_analysis)
            counter_arguments.append(counter_arg)
        
        return counter_arguments
    
    def _counter_claim(self, claim: str, argument_analysis: dict) -> dict:
        """Generate counter-argument for a specific claim"""
        # Simple counter-argument generation
        claim_lower = claim.lower()
        
        if "always" in claim_lower or "never" in claim_lower:
            return {
                "type": "absolute_counter",
                "target": claim,
                "counter": f"The claim uses absolute language ('always'/'never'), which is rarely accurate in complex situations. Consider exceptions and edge cases.",
                "strength": "strong"
            }
        elif "should" in claim_lower or "must" in claim_lower:
            return {
                "type": "normative_counter",
                "target": claim,
                "counter": f"The claim uses normative language ('should'/'must') which presumes a specific value system. Different stakeholders may have different priorities.",
                "strength": "medium"
            }
        else:
            return {
                "type": "evidence_counter",
                "target": claim,
                "counter": f"The claim lacks sufficient supporting evidence. What specific data or examples validate this assertion?",
                "strength": "medium"
            }
    
    def _question_evidence(self, evidence_type: str, argument_analysis: dict) -> dict:
        """Generate counter-argument questioning the evidence type"""
        evidence_questions = {
            "statistical": {
                "counter": "Statistical evidence requires proper methodology, sample size, and statistical significance. Are these details provided?",
                "strength": "strong"
            },
            "authority": {
                "counter": "Appeals to authority should be supported by the authority's actual expertise and evidence. Is this authority truly qualified in this domain?",
                "strength": "medium"
            },
            "anecdotal": {
                "counter": "Anecdotal evidence is not statistically significant and may not be representative. What broader data supports this claim?",
                "strength": "strong"
            },
            "logical": {
                "counter": "Logical reasoning must be sound and free from fallacies. Are there hidden assumptions or logical gaps?",
                "strength": "medium"
            },
            "experiential": {
                "counter": "Personal experience may not be generalizable. Is this experience representative of broader patterns?",
                "strength": "medium"
            }
        }
        
        return {
            "type": "evidence_question",
            "target": evidence_type,
            **evidence_questions.get(evidence_type, {"counter": "Question the validity of this evidence type.", "strength": "medium"})
        }
    
    def _challenge_conclusion(self, conclusion: str, argument_analysis: dict) -> dict:
        """Generate counter-argument challenging the conclusion"""
        return {
            "type": "conclusion_challenge",
            "target": conclusion,
            "counter": f"The conclusion may not logically follow from the premises. Are there alternative conclusions that better fit the evidence?",
            "strength": "strong"
        }
    
    def _apply_inversion(self, argument_analysis: dict) -> dict:
        """Apply inversion to test underlying assumptions"""
        inversion_analysis = {
            "inverted_claims": [],
            "inverted_conclusions": [],
            "assumption_challenges": []
        }
        
        # Invert claims
        for claim in argument_analysis["claims"]:
            inverted = self._invert_statement(claim)
            inversion_analysis["inverted_claims"].append(inverted)
        
        # Invert conclusions
        for conclusion in argument_analysis["conclusions"]:
            inverted = self._invert_statement(conclusion)
            inversion_analysis["inverted_conclusions"].append(inverted)
        
        # Challenge assumptions
        for key_term in argument_analysis["key_terms"][:5]:  # Top 5 terms
            assumption = f"The argument assumes {key_term} is universally true/valuable."
            challenge = f"What if {key_term} is not true or has different implications?"
            inversion_analysis["assumption_challenges"].append({
                "assumption": assumption,
                "challenge": challenge
            })
        
        return inversion_analysis
    
    def _invert_statement(self, statement: str) -> str:
        """Invert a statement to test assumptions"""
        # Simple inversion patterns
        inversions = {
            "is": "is not",
            "are": "are not",
            "will": "will not",
            "should": "should not",
            "can": "cannot",
            "good": "bad",
            "bad": "good",
            "effective": "ineffective",
            "ineffective": "effective",
            "important": "unimportant",
            "unimportant": "important",
            "necessary": "unnecessary",
            "unnecessary": "necessary"
        }
        
        inverted = statement
        for original, inverted_word in inversions.items():
            inverted = inverted.replace(original, inverted_word)
        
        return inverted
    
    def _identify_evidence_gaps(self, argument_analysis: dict) -> list:
        """Identify gaps in evidence and reasoning"""
        gaps = []
        
        # Check for lack of supporting evidence
        if argument_analysis["structure"]["support_ratio"] < 0.5:
            gaps.append({
                "type": "insufficient_support",
                "description": "Claims lack sufficient supporting evidence",
                "severity": "high"
            })
        
        # Check for lack of specific evidence
        if "statistical" not in argument_analysis["evidence_types"]:
            gaps.append({
                "type": "no_statistical_evidence",
                "description": "No statistical evidence provided to support claims",
                "severity": "medium"
            })
        
        # Check for lack of expert validation
        if "authority" not in argument_analysis["evidence_types"]:
            gaps.append({
                "type": "no_expert_validation",
                "description": "No expert or authority validation provided",
                "severity": "medium"
            })
        
        # Check for logical structure issues
        if argument_analysis["structure"]["structure_type"] == "poorly_supported":
            gaps.append({
                "type": "poor_logical_structure",
                "description": "Argument lacks proper logical structure",
                "severity": "high"
            })
        
        return gaps
    
    def _generate_strengthening_recommendations(
        self, 
        argument_analysis: dict, 
        fallacies: list, 
        counter_arguments: list, 
        evidence_gaps: list
    ) -> list:
        """Generate recommendations to strengthen the argument"""
        recommendations = []
        
        # Address fallacies
        for fallacy in fallacies:
            recommendations.append({
                "category": "fallacy_correction",
                "recommendation": f"Address {fallacy['fallacy_type']}: {fallacy['counter_strategy']}",
                "priority": "high" if fallacy["score"] > 0.7 else "medium"
            })
        
        # Address evidence gaps
        for gap in evidence_gaps:
            if gap["severity"] == "high":
                recommendations.append({
                    "category": "evidence_improvement",
                    "recommendation": f"Strengthen evidence: {gap['description']}",
                    "priority": "high"
                })
        
        # General strengthening recommendations
        if argument_analysis["structure"]["support_ratio"] < 1.0:
            recommendations.append({
                "category": "structure_improvement",
                "recommendation": "Add more supporting statements for each claim",
                "priority": "medium"
            })
        
        if len(argument_analysis["evidence_types"]) < 3:
            recommendations.append({
                "category": "evidence_diversity",
                "recommendation": "Include multiple types of evidence (statistical, expert, anecdotal)",
                "priority": "medium"
            })
        
        return recommendations
    
    def _assess_argument_strength(self, argument_analysis: dict) -> str:
        """Assess the overall strength of the argument"""
        structure_score = 0
        
        # Structure assessment
        if argument_analysis["structure"]["structure_type"] == "well_supported":
            structure_score += 3
        elif argument_analysis["structure"]["structure_type"] == "poorly_supported":
            structure_score -= 2
        elif argument_analysis["structure"]["structure_type"] == "unsupported_claims":
            structure_score -= 3
        
        # Evidence assessment
        evidence_score = len(argument_analysis["evidence_types"])
        
        # Overall assessment
        total_score = structure_score + evidence_score
        
        if total_score >= 4:
            return "strong"
        elif total_score >= 2:
            return "moderate"
        elif total_score >= 0:
            return "weak"
        else:
            return "very_weak"
    
    def _compile_devils_advocate_report(
        self,
        argument_analysis: dict,
        detected_fallacies: list,
        counter_arguments: list,
        inversion_analysis: dict,
        evidence_gaps: list,
        strengthening_recommendations: list
    ) -> dict:
        """Compile comprehensive devil's advocate report"""
        
        return {
            "argument_analysis": {
                "original_text": argument_analysis["original_text"],
                "structure": argument_analysis["argument_structure"],
                "key_terms": argument_analysis["key_terms"],
                "evidence_types": argument_analysis["evidence_types"],
                "strength_assessment": self._assess_argument_strength(argument_analysis)
            },
            "fallacy_analysis": {
                "total_fallacies": len(detected_fallacies),
                "fallacies": detected_fallacies,
                "critical_fallacies": [f for f in detected_fallacies if f["score"] > 0.6]
            },
            "counter_arguments": {
                "total_count": len(counter_arguments),
                "arguments": counter_arguments,
                "strongest_counter": max(counter_arguments, key=lambda x: self._get_counter_strength(x["strength"])) if counter_arguments else None
            },
            "inversion_analysis": {
                "inverted_claims": inversion_analysis["inverted_claims"],
                "inverted_conclusions": inversion_analysis["inverted_conclusions"],
                "assumption_challenges": inversion_analysis["assumption_challenges"]
            },
            "evidence_gaps": {
                "total_gaps": len(evidence_gaps),
                "gaps": evidence_gaps,
                "critical_gaps": [g for g in evidence_gaps if g["severity"] == "high"]
            },
            "strengthening_recommendations": {
                "total_recommendations": len(strengthening_recommendations),
                "recommendations": strengthening_recommendations,
                "priority_actions": [r for r in strengthening_recommendations if r["priority"] == "high"]
            },
            "overall_assessment": self._generate_overall_assessment(
                argument_analysis, detected_fallacies, evidence_gaps
            )
        }
    
    def _get_counter_strength(self, strength: str) -> int:
        """Get numeric strength for counter-argument"""
        strength_map = {"strong": 3, "medium": 2, "weak": 1}
        return strength_map.get(strength, 1)
    
    def _generate_overall_assessment(self, argument_analysis: dict, fallacies: list, gaps: list) -> dict:
        """Generate overall assessment of the argument"""
        critical_fallacies = len([f for f in fallacies if f["score"] > 0.6])
        critical_gaps = len([g for g in gaps if g["severity"] == "high"])
        
        if critical_fallacies >= 2 or critical_gaps >= 2:
            assessment = "very_weak"
            confidence = 0.9
        elif critical_fallacies >= 1 or critical_gaps >= 1:
            assessment = "weak"
            confidence = 0.8
        elif len(fallacies) >= 2 or len(gaps) >= 3:
            assessment = "moderate"
            confidence = 0.7
        else:
            assessment = "strong"
            confidence = 0.6
        
        return {
            "assessment": assessment,
            "confidence": confidence,
            "key_issues": {
                "critical_fallacies": critical_fallacies,
                "critical_gaps": critical_gaps,
                "total_issues": len(fallacies) + len(gaps)
            }
        }


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_devils_advocate():
        agent = DevilsAdvocateAgent()
        
        test_argument = """
        This AI system will definitely revolutionize our industry. 
        Everyone agrees that it's obviously the best solution available. 
        We must implement it immediately because all our competitors are already using similar systems.
        Either we adopt this technology or we'll be left behind.
        """
        
        result = await agent.process(test_argument)
        
        print("=== Devil's Advocate Agent Test ===")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Argument Strength: {result.content['argument_analysis']['strength_assessment']}")
        print(f"Fallacies Detected: {result.content['fallacy_analysis']['total_fallacies']}")
        print(f"Overall Assessment: {result.content['overall_assessment']['assessment']}")
        
        print("\nTop 3 Recommendations:")
        for i, rec in enumerate(result.content['strengthening_recommendations']['priority_actions'][:3], 1):
            print(f"{i}. {rec['recommendation']}")
    
    # Run test
    asyncio.run(test_devils_advocate())