"""
Second-Order Thinking Agent

Predicts downstream consequences of decisions and actions.
Helps think beyond immediate effects to consider second and third-order impacts.

Mental Models Used:
- Second-Order Thinking
- Systems Thinking
- Probabilistic Thinking
"""


from .core.base_agent import CognitiveAgent, AgentResult
from .core.mental_models import MentalModelsLibrary


class SecondOrderThinkingAgent(CognitiveAgent):
    """
    Agent that predicts downstream consequences using second-order thinking.
    
    Purpose: Predict downstream consequences of decisions
    Input: Decision/action description
    Output: Consequence tree with probability weights
    Mental Models: Second-order thinking, systems thinking, probabilistic thinking
    """
    
    def __init__(self):
        super().__init__(
            name="Second Order Thinking",
            category="cognitive",
            mental_models=[
                MentalModelsLibrary.SECOND_ORDER_THINKING,
                MentalModelsLibrary.SYSTEMS_THINKING,
                MentalModelsLibrary.PROBABILISTIC_THINKING
            ],
            description="Predicts downstream consequences and ripple effects of decisions",
            capabilities=[
                "Generate first-order consequences",
                "Predict second-order effects",
                "Forecast third-order impacts",
                "Assess probability and timing",
                "Identify feedback loops"
            ]
        )
    
    async def process_input(self, input_data: str, context: dict = None) -> AgentResult:
        """Process decision to predict consequences"""
        reasoning_trace = []
        
        # Step 1: Parse and identify the primary decision
        reasoning_trace.append("Parsing and identifying the primary decision/action")
        primary_action = self._extract_primary_action(input_data)
        reasoning_trace.append(f"Primary action identified: {primary_action['description']}")
        
        # Step 2: Generate first-order consequences
        reasoning_trace.append("Generating first-order consequences")
        first_order = self._generate_first_order_consequences(primary_action, context)
        reasoning_trace.append(f"Generated {len(first_order)} first-order consequences")
        
        # Step 3: Predict second-order consequences
        reasoning_trace.append("Predicting second-order consequences")
        second_order = self._generate_second_order_consequences(first_order, context)
        reasoning_trace.append(f"Generated {len(second_order)} second-order consequences")
        
        # Step 4: Forecast third-order consequences
        reasoning_trace.append("Forecasting third-order consequences")
        third_order = self._generate_third_order_consequences(second_order, context)
        reasoning_trace.append(f"Generated {len(third_order)} third-order consequences")
        
        # Step 5: Identify feedback loops and cascading effects
        reasoning_trace.append("Identifying feedback loops and cascading effects")
        feedback_loops = self._identify_feedback_loops(first_order, second_order, third_order)
        reasoning_trace.append(f"Identified {len(feedback_loops)} feedback loops")
        
        # Step 6: Assess probabilities and timelines
        reasoning_trace.append("Assessing probabilities and timelines")
        probability_analysis = self._assess_probabilities(first_order, second_order, third_order)
        reasoning_trace.append("Completed probability and timeline assessment")
        
        # Step 7: Generate consequence tree
        reasoning_trace.append("Building comprehensive consequence tree")
        consequence_tree = self._build_consequence_tree(
            primary_action, first_order, second_order, third_order, 
            feedback_loops, probability_analysis
        )
        
        return AgentResult(
            content=consequence_tree,
            confidence=0.80,
            reasoning_trace=reasoning_trace,
            mental_models_used=self.mental_models,
            processing_time=0.0,
            metadata={
                "total_consequences": len(first_order) + len(second_order) + len(third_order),
                "complexity_score": self._calculate_complexity_score(consequence_tree),
                "risk_level": self._assess_overall_risk(consequence_tree)
            }
        )
    
    def _extract_primary_action(self, input_text: str) -> dict:
        """Extract the primary action or decision from text"""
        # Identify action keywords
        action_patterns = [
            r"we will (.+)",
            r"we should (.+)",
            r"let's (.+)",
            r"I will (.+)",
            r"the plan is to (.+)",
            r"decided to (.+)",
            r"going to (.+)",
            r"implement (.+)",
            r"launch (.+)",
            r"build (.+)",
            r"create (.+)",
            r"start (.+)",
            r"stop (.+)",
            r"change (.+)"
        ]
        
        import re
        primary_action = {
            "description": input_text.strip(),
            "action_type": "general",
            "scope": "unknown",
            "stakeholders": [],
            "resources": []
        }
        
        for pattern in action_patterns:
            match = re.search(pattern, input_text, re.IGNORECASE)
            if match:
                action_text = match.group(1).strip()
                primary_action["description"] = action_text
                primary_action["action_type"] = self._classify_action_type(action_text)
                break
        
        # Extract additional information
        primary_action["stakeholders"] = self._identify_stakeholders(input_text)
        primary_action["resources"] = self._identify_resources(input_text)
        primary_action["scope"] = self._determine_scope(input_text)
        
        return primary_action
    
    def _classify_action_type(self, action_text: str) -> str:
        """Classify the type of action"""
        action_lower = action_text.lower()
        
        if any(word in action_lower for word in ["launch", "release", "deploy", "roll out"]):
            return "launch"
        elif any(word in action_lower for word in ["build", "create", "develop", "implement"]):
            return "development"
        elif any(word in action_lower for word in ["change", "modify", "update", "transform"]):
            return "change"
        elif any(word in action_lower for word in ["stop", "end", "terminate", "cancel"]):
            return "termination"
        elif any(word in action_lower for word in ["start", "begin", "initiate", "commence"]):
            return "initiation"
        elif any(word in action_lower for word in ["hire", "recruit", "expand", "grow"]):
            return "expansion"
        elif any(word in action_lower for word in ["cut", "reduce", "downsize", "optimize"]):
            return "reduction"
        else:
            return "general"
    
    def _identify_stakeholders(self, text: str) -> list:
        """Identify stakeholders affected by the action"""
        stakeholder_groups = [
            "customers", "users", "clients", "employees", "team", "staff",
            "management", "leadership", "investors", "shareholders", "board",
            "partners", "suppliers", "vendors", "competitors", "regulators",
            "community", "public", "government", "media"
        ]
        
        text_lower = text.lower()
        identified_stakeholders = []
        
        for stakeholder in stakeholder_groups:
            if stakeholder in text_lower:
                identified_stakeholders.append(stakeholder)
        
        return identified_stakeholders
    
    def _identify_resources(self, text: str) -> list:
        """Identify resources involved in the action"""
        resource_types = [
            "money", "budget", "funding", "investment", "capital",
            "time", "schedule", "timeline", "deadline",
            "people", "team", "staff", "personnel", "headcount",
            "technology", "software", "hardware", "infrastructure",
            "data", "information", "knowledge", "expertise",
            "office", "space", "facilities", "equipment"
        ]
        
        text_lower = text.lower()
        identified_resources = []
        
        for resource in resource_types:
            if resource in text_lower:
                identified_resources.append(resource)
        
        return identified_resources
    
    def _determine_scope(self, text: str) -> str:
        """Determine the scope of the action"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["company", "organization", "entire", "all"]):
            return "organizational"
        elif any(word in text_lower for word in ["team", "department", "division"]):
            return "team"
        elif any(word in text_lower for word in ["project", "initiative", "program"]):
            return "project"
        elif any(word in text_lower for word in ["product", "service", "feature"]):
            return "product"
        elif any(word in text_lower for word in ["market", "industry", "sector"]):
            return "market"
        else:
            return "unknown"
    
    def _generate_first_order_consequences(self, primary_action: dict, context: dict = None) -> list:
        """Generate immediate consequences"""
        consequences = []
        action_type = primary_action["action_type"]
        scope = primary_action["scope"]
        
        # Resource consequences
        if "money" in primary_action["resources"] or "budget" in primary_action["resources"]:
            consequences.append({
                "order": 1,
                "type": "resource",
                "description": "Immediate financial resource allocation",
                "impact": "budget_impact",
                "probability": 0.9,
                "timeline": "immediate",
                "stakeholders_affected": ["management", "finance"]
            })
        
        if "people" in primary_action["resources"] or "team" in primary_action["resources"]:
            consequences.append({
                "order": 1,
                "type": "resource",
                "description": "Human resource reallocation or hiring",
                "impact": "team_impact",
                "probability": 0.8,
                "timeline": "short_term",
                "stakeholders_affected": ["employees", "hr"]
            })
        
        # Action-specific consequences
        if action_type == "launch":
            consequences.extend([
                {
                    "order": 1,
                    "type": "market",
                    "description": "Initial market reaction and adoption",
                    "impact": "market_response",
                    "probability": 0.7,
                    "timeline": "immediate",
                    "stakeholders_affected": ["customers", "sales"]
                },
                {
                    "order": 1,
                    "type": "operational",
                    "description": "Increased operational workload",
                    "impact": "operational_strain",
                    "probability": 0.8,
                    "timeline": "immediate",
                    "stakeholders_affected": ["operations", "support"]
                }
            ])
        
        elif action_type == "change":
            consequences.extend([
                {
                    "order": 1,
                    "type": "organizational",
                    "description": "Resistance to change from affected parties",
                    "impact": "change_resistance",
                    "probability": 0.6,
                    "timeline": "immediate",
                    "stakeholders_affected": ["employees", "management"]
                },
                {
                    "order": 1,
                    "type": "process",
                    "description": "Temporary disruption of existing processes",
                    "impact": "process_disruption",
                    "probability": 0.7,
                    "timeline": "short_term",
                    "stakeholders_affected": ["all_staff"]
                }
            ])
        
        elif action_type == "expansion":
            consequences.extend([
                {
                    "order": 1,
                    "type": "resource",
                    "description": "Increased resource requirements",
                    "impact": "resource_pressure",
                    "probability": 0.8,
                    "timeline": "immediate",
                    "stakeholders_affected": ["finance", "operations"]
                },
                {
                    "order": 1,
                    "type": "coordination",
                    "description": "Increased coordination complexity",
                    "impact": "coordination_challenges",
                    "probability": 0.7,
                    "timeline": "immediate",
                    "stakeholders_affected": ["management", "team"]
                }
            ])
        
        # Stakeholder-specific consequences
        for stakeholder in primary_action["stakeholders"]:
            if stakeholder == "customers":
                consequences.append({
                    "order": 1,
                    "type": "customer",
                    "description": "Customer experience changes",
                    "impact": "customer_impact",
                    "probability": 0.6,
                    "timeline": "immediate",
                    "stakeholders_affected": ["customers"]
                })
            elif stakeholder == "employees":
                consequences.append({
                    "order": 1,
                    "type": "employee",
                    "description": "Employee morale and motivation changes",
                    "impact": "employee_sentiment",
                    "probability": 0.5,
                    "timeline": "immediate",
                    "stakeholders_affected": ["employees"]
                })
        
        return consequences
    
    def _generate_second_order_consequences(self, first_order: list, context: dict = None) -> list:
        """Generate consequences of consequences"""
        consequences = []
        
        for first in first_order:
            first_impact = first["impact"]
            first_type = first["type"]
            
            # Market consequences of market impacts
            if first_type == "market" and first_impact == "market_response":
                consequences.extend([
                    {
                        "order": 2,
                        "type": "competitive",
                        "description": "Competitor reactions to market entry",
                        "impact": "competitive_response",
                        "probability": 0.7,
                        "timeline": "medium_term",
                        "stakeholders_affected": ["competitors", "sales"],
                        "parent_consequence": first["description"]
                    },
                    {
                        "order": 2,
                        "type": "market",
                        "description": "Market positioning shifts",
                        "impact": "positioning_change",
                        "probability": 0.6,
                        "timeline": "medium_term",
                        "stakeholders_affected": ["marketing", "strategy"],
                        "parent_consequence": first["description"]
                    }
                ])
            
            # Operational consequences of operational strain
            elif first_type == "operational" and first_impact == "operational_strain":
                consequences.extend([
                    {
                        "order": 2,
                        "type": "quality",
                        "description": "Quality standards may be compromised",
                        "impact": "quality_risk",
                        "probability": 0.4,
                        "timeline": "medium_term",
                        "stakeholders_affected": ["customers", "quality"],
                        "parent_consequence": first["description"]
                    },
                    {
                        "order": 2,
                        "type": "employee",
                        "description": "Employee burnout and turnover risk",
                        "impact": "turnover_risk",
                        "probability": 0.5,
                        "timeline": "medium_term",
                        "stakeholders_affected": ["employees", "hr"],
                        "parent_consequence": first["description"]
                    }
                ])
            
            # Financial consequences of budget impacts
            elif first_type == "resource" and first_impact == "budget_impact":
                consequences.extend([
                    {
                        "order": 2,
                        "type": "financial",
                        "description": "Cash flow pressure on other projects",
                        "impact": "resource_competition",
                        "probability": 0.6,
                        "timeline": "medium_term",
                        "stakeholders_affected": ["finance", "other_projects"],
                        "parent_consequence": first["description"]
                    },
                    {
                        "order": 2,
                        "type": "strategic",
                        "description": "Strategic priorities may need adjustment",
                        "impact": "strategic_shift",
                        "probability": 0.5,
                        "timeline": "medium_term",
                        "stakeholders_affected": ["leadership", "strategy"],
                        "parent_consequence": first["description"]
                    }
                ])
            
            # Organizational consequences of change resistance
            elif first_type == "organizational" and first_impact == "change_resistance":
                consequences.extend([
                    {
                        "order": 2,
                        "type": "productivity",
                        "description": "Productivity decline during adaptation",
                        "impact": "productivity_loss",
                        "probability": 0.6,
                        "timeline": "medium_term",
                        "stakeholders_affected": ["management", "employees"],
                        "parent_consequence": first["description"]
                    },
                    {
                        "order": 2,
                        "type": "cultural",
                        "description": "Organizational culture shifts",
                        "impact": "cultural_change",
                        "probability": 0.5,
                        "timeline": "long_term",
                        "stakeholders_affected": ["all_employees"],
                        "parent_consequence": first["description"]
                    }
                ])
        
        # Add general second-order consequences
        consequences.extend([
            {
                "order": 2,
                "type": "learning",
                "description": "Organizational learning and capability building",
                "impact": "capability_growth",
                "probability": 0.7,
                "timeline": "medium_term",
                "stakeholders_affected": ["organization"]
            },
            {
                "order": 2,
                "type": "reputation",
                "description": "Brand and reputation impacts",
                "impact": "reputation_change",
                "probability": 0.5,
                "timeline": "medium_term",
                "stakeholders_affected": ["marketing", "customers"]
            }
        ])
        
        return consequences
    
    def _generate_third_order_consequences(self, second_order: list, context: dict = None) -> list:
        """Generate consequences of second-order consequences"""
        consequences = []
        
        for second in second_order:
            second_impact = second["impact"]
            second_type = second["type"]
            
            # Industry-level consequences
            if second_type == "competitive" and second_impact == "competitive_response":
                consequences.extend([
                    {
                        "order": 3,
                        "type": "industry",
                        "description": "Industry competitive dynamics shift",
                        "impact": "industry_transformation",
                        "probability": 0.5,
                        "timeline": "long_term",
                        "stakeholders_affected": ["industry", "regulators"],
                        "parent_consequence": second["description"]
                    },
                    {
                        "order": 3,
                        "type": "innovation",
                        "description": "Innovation race acceleration",
                        "impact": "innovation_pressure",
                        "probability": 0.6,
                        "timeline": "long_term",
                        "stakeholders_affected": ["rd", "product"],
                        "parent_consequence": second["description"]
                    }
                ])
            
            # Market evolution consequences
            elif second_type == "market" and second_impact == "positioning_change":
                consequences.append({
                    "order": 3,
                    "type": "market",
                    "description": "Market structure evolution",
                    "impact": "market_evolution",
                    "probability": 0.4,
                    "timeline": "long_term",
                    "stakeholders_affected": ["industry", "customers"],
                    "parent_consequence": second["description"]
                })
            
            # Talent ecosystem consequences
            elif second_type == "employee" and second_impact == "turnover_risk":
                consequences.extend([
                    {
                        "order": 3,
                        "type": "talent",
                        "description": "Talent ecosystem reputation impact",
                        "impact": "talent_brand",
                        "probability": 0.5,
                        "timeline": "long_term",
                        "stakeholders_affected": ["hr", "recruiting"],
                        "parent_consequence": second["description"]
                    },
                    {
                        "order": 3,
                        "type": "knowledge",
                        "description": "Institutional knowledge loss",
                        "impact": "knowledge_drain",
                        "probability": 0.4,
                        "timeline": "long_term",
                        "stakeholders_affected": ["organization", "operations"],
                        "parent_consequence": second["description"]
                    }
                ])
            
            # Strategic positioning consequences
            elif second_type == "strategic" and second_impact == "strategic_shift":
                consequences.append({
                    "order": 3,
                    "type": "strategic",
                    "description": "Long-term strategic positioning change",
                    "impact": "strategic_repositioning",
                    "probability": 0.6,
                    "timeline": "long_term",
                    "stakeholders_affected": ["leadership", "board"],
                    "parent_consequence": second["description"]
                })
        
        # Add general third-order consequences
        consequences.extend([
            {
                "order": 3,
                "type": "systemic",
                "description": "Systemic changes in business model",
                "impact": "business_model_evolution",
                "probability": 0.3,
                "timeline": "long_term",
                "stakeholders_affected": ["entire_organization"]
            },
            {
                "order": 3,
                "type": "societal",
                "description": "Broader industry or societal impact",
                "impact": "societal_impact",
                "probability": 0.2,
                "timeline": "very_long_term",
                "stakeholders_affected": ["society", "industry"]
            }
        ])
        
        return consequences
    
    def _identify_feedback_loops(self, first_order: list, second_order: list, third_order: list) -> list:
        """Identify feedback loops in the consequence chain"""
        feedback_loops = []
        
        # Look for reinforcing loops
        reinforcing_patterns = [
            ("growth", "growth"),
            ("success", "success"),
            ("adoption", "adoption"),
            ("innovation", "innovation"),
            ("learning", "capability")
        ]
        
        for pattern in reinforcing_patterns:
            loop = self._find_reinforcing_loop(pattern, first_order, second_order, third_order)
            if loop:
                feedback_loops.append(loop)
        
        # Look for balancing loops
        balancing_patterns = [
            ("strain", "burnout"),
            ("resistance", "productivity"),
            ("competition", "pressure"),
            ("cost", "budget")
        ]
        
        for pattern in balancing_patterns:
            loop = self._find_balancing_loop(pattern, first_order, second_order, third_order)
            if loop:
                feedback_loops.append(loop)
        
        return feedback_loops
    
    def _find_reinforcing_loop(self, pattern: tuple, consequences: list) -> dict:
        """Find reinforcing feedback loops"""
        # Simplified loop detection
        loop_consequences = []
        
        for consequence_set in consequences:
            for consequence in consequence_set:
                desc = consequence["description"].lower()
                if pattern[0] in desc and pattern[1] in desc:
                    loop_consequences.append(consequence)
        
        if len(loop_consequences) >= 2:
            return {
                "type": "reinforcing",
                "pattern": pattern,
                "consequences": loop_consequences,
                "description": f"Reinforcing loop: {pattern[0]} leads to more {pattern[1]}"
            }
        
        return None
    
    def _find_balancing_loop(self, pattern: tuple, consequences: list) -> dict:
        """Find balancing feedback loops"""
        loop_consequences = []
        
        for consequence_set in consequences:
            for consequence in consequence_set:
                desc = consequence["description"].lower()
                if pattern[0] in desc:
                    loop_consequences.append(consequence)
                elif pattern[1] in desc:
                    loop_consequences.append(consequence)
        
        if len(loop_consequences) >= 2:
            return {
                "type": "balancing",
                "pattern": pattern,
                "consequences": loop_consequences,
                "description": f"Balancing loop: {pattern[0]} triggers {pattern[1]} which regulates the system"
            }
        
        return None
    
    def _assess_probabilities(self, first_order: list, second_order: list, third_order: list) -> dict:
        """Assess probabilities and create probability distribution"""
        all_consequences = first_order + second_order + third_order
        
        probability_analysis = {
            "high_probability": [],  # > 0.7
            "medium_probability": [],  # 0.4 - 0.7
            "low_probability": [],  # < 0.4
            "average_probability": 0.0,
            "confidence_distribution": {}
        }
        
        total_probability = 0
        for consequence in all_consequences:
            prob = consequence["probability"]
            total_probability += prob
            
            if prob > 0.7:
                probability_analysis["high_probability"].append(consequence["description"])
            elif prob >= 0.4:
                probability_analysis["medium_probability"].append(consequence["description"])
            else:
                probability_analysis["low_probability"].append(consequence["description"])
        
        probability_analysis["average_probability"] = total_probability / len(all_consequences) if all_consequences else 0
        
        # Create confidence distribution by order
        for order, consequences in [("first", first_order), ("second", second_order), ("third", third_order)]:
            if consequences:
                avg_prob = sum(c["probability"] for c in consequences) / len(consequences)
                probability_analysis["confidence_distribution"][order] = avg_prob
        
        return probability_analysis
    
    def _build_consequence_tree(
        self, 
        primary_action: dict, 
        first_order: list, 
        second_order: list, 
        third_order: list,
        feedback_loops: list,
        probability_analysis: dict
    ) -> dict:
        """Build comprehensive consequence tree"""
        
        return {
            "primary_action": primary_action,
            "consequence_analysis": {
                "first_order": {
                    "consequences": first_order,
                    "count": len(first_order),
                    "average_probability": sum(c["probability"] for c in first_order) / len(first_order) if first_order else 0,
                    "timeline_distribution": self._analyze_timeline_distribution(first_order)
                },
                "second_order": {
                    "consequences": second_order,
                    "count": len(second_order),
                    "average_probability": sum(c["probability"] for c in second_order) / len(second_order) if second_order else 0,
                    "timeline_distribution": self._analyze_timeline_distribution(second_order)
                },
                "third_order": {
                    "consequences": third_order,
                    "count": len(third_order),
                    "average_probability": sum(c["probability"] for c in third_order) / len(third_order) if third_order else 0,
                    "timeline_distribution": self._analyze_timeline_distribution(third_order)
                }
            },
            "feedback_loops": feedback_loops,
            "probability_analysis": probability_analysis,
            "risk_assessment": self._assess_risks(first_order, second_order, third_order),
            "strategic_implications": self._generate_strategic_implications(first_order, second_order, third_order),
            "monitoring_recommendations": self._generate_monitoring_recommendations(first_order, second_order, third_order),
            "mitigation_strategies": self._generate_mitigation_strategies(first_order, second_order, third_order)
        }
    
    def _analyze_timeline_distribution(self, consequences: list) -> dict:
        """Analyze timeline distribution of consequences"""
        timelines = {"immediate": 0, "short_term": 0, "medium_term": 0, "long_term": 0, "very_long_term": 0}
        
        for consequence in consequences:
            timeline = consequence.get("timeline", "unknown")
            if timeline in timelines:
                timelines[timeline] += 1
        
        return timelines
    
    def _assess_risks(self, first_order: list, second_order: list, third_order: list) -> dict:
        """Assess risks across all consequence orders"""
        all_consequences = first_order + second_order + third_order
        
        risk_categories = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": []
        }
        
        for consequence in all_consequences:
            risk_score = self._calculate_risk_score(consequence)
            
            consequence["risk_score"] = risk_score
            
            if risk_score > 0.7:
                risk_categories["high_risk"].append(consequence)
            elif risk_score > 0.4:
                risk_categories["medium_risk"].append(consequence)
            else:
                risk_categories["low_risk"].append(consequence)
        
        return {
            "risk_distribution": risk_categories,
            "overall_risk_level": self._calculate_overall_risk(all_consequences),
            "critical_risks": [c for c in all_consequences if c.get("risk_score", 0) > 0.8]
        }
    
    def _calculate_risk_score(self, consequence: dict) -> float:
        """Calculate risk score for a consequence"""
        probability = consequence["probability"]
        impact = self._assess_impact_severity(consequence)
        
        # Risk = Probability × Impact
        return probability * impact
    
    def _assess_impact_severity(self, consequence: dict) -> float:
        """Assess the severity of consequence impact"""
        impact_type = consequence["impact"]
        
        high_impact_types = [
            "budget_impact", "quality_risk", "turnover_risk", 
            "competitive_response", "industry_transformation"
        ]
        
        medium_impact_types = [
            "market_response", "operational_strain", "change_resistance",
            "resource_pressure", "positioning_change"
        ]
        
        if impact_type in high_impact_types:
            return 0.8
        elif impact_type in medium_impact_types:
            return 0.5
        else:
            return 0.3
    
    def _calculate_overall_risk(self, consequences: list) -> str:
        """Calculate overall risk level"""
        if not consequences:
            return "low"
        
        avg_risk_score = sum(self._calculate_risk_score(c) for c in consequences) / len(consequences)
        
        if avg_risk_score > 0.6:
            return "high"
        elif avg_risk_score > 0.3:
            return "medium"
        else:
            return "low"
    
    def _generate_strategic_implications(self, first_order: list, second_order: list, third_order: list) -> list:
        """Generate strategic implications"""
        implications = []
        
        # Analyze patterns across consequences
        all_consequences = first_order + second_order + third_order
        
        # Resource implications
        resource_consequences = [c for c in all_consequences if c["type"] == "resource"]
        if resource_consequences:
            implications.append("Resource allocation will be significantly impacted across multiple areas")
        
        # Stakeholder implications
        stakeholder_types = set()
        for c in all_consequences:
            stakeholder_types.update(c.get("stakeholders_affected", []))
        
        if len(stakeholder_types) > 5:
            implications.append("Wide stakeholder impact requires comprehensive communication strategy")
        
        # Timeline implications
        long_term_consequences = [c for c in all_consequences if c["timeline"] in ["long_term", "very_long_term"]]
        if len(long_term_consequences) > len(all_consequences) * 0.3:
            implications.append("Long-term consequences suggest need for sustained commitment")
        
        # Competitive implications
        competitive_consequences = [c for c in all_consequences if c["type"] == "competitive"]
        if competitive_consequences:
            implications.append("Competitive landscape will be affected - need proactive positioning")
        
        return implications
    
    def _generate_monitoring_recommendations(self, first_order: list, second_order: list, third_order: list) -> list:
        """Generate monitoring recommendations"""
        recommendations = []
        
        # Early warning indicators
        high_probability_first = [c for c in first_order if c["probability"] > 0.7]
        for consequence in high_probability_first:
            recommendations.append(f"Monitor: {consequence['description']}")
        
        # Leading indicators
        recommendations.extend([
            "Track stakeholder sentiment and feedback",
            "Monitor resource utilization and burn rates",
            "Watch for competitor reactions and market changes",
            "Measure operational capacity and quality metrics"
        ])
        
        return recommendations
    
    def _generate_mitigation_strategies(self, first_order: list, second_order: list, third_order: list) -> list:
        """Generate mitigation strategies"""
        strategies = []
        
        # Risk-based strategies
        all_consequences = first_order + second_order + third_order
        high_risk = [c for c in all_consequences if self._calculate_risk_score(c) > 0.7]
        
        if high_risk:
            strategies.append("Develop contingency plans for high-risk consequences")
            strategies.append("Create early warning systems for critical risks")
        
        # General strategies
        strategies.extend([
            "Build flexibility and adaptability into plans",
            "Maintain resource buffers for unexpected impacts",
            "Establish clear communication channels with stakeholders",
            "Create feedback loops for course correction"
        ])
        
        return strategies
    
    def _calculate_complexity_score(self, consequence_tree: dict) -> float:
        """Calculate complexity score of the consequence tree"""
        first_count = len(consequence_tree["consequence_analysis"]["first_order"]["consequences"])
        second_count = len(consequence_tree["consequence_analysis"]["second_order"]["consequences"])
        third_count = len(consequence_tree["consequence_analysis"]["third_order"]["consequences"])
        
        # Weight higher orders more heavily
        complexity = (first_count * 1.0 + second_count * 1.5 + third_count * 2.0) / 10
        return min(complexity, 1.0)
    
    def _assess_overall_risk(self, consequence_tree: dict) -> str:
        """Assess overall risk level"""
        return consequence_tree["risk_assessment"]["overall_risk_level"]


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_second_order_thinking():
        agent = SecondOrderThinkingAgent()
        
        test_decision = """
        We will launch a new AI-powered SaaS product in the healthcare market next quarter. 
        This will require significant investment in development and marketing, 
        and we'll need to hire additional engineers and sales staff.
        """
        
        result = await agent.process(test_decision)
        
        print("=== Second Order Thinking Agent Test ===")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Processing Time: {result.processing_time:.2f}s")
        print(f"Overall Risk: {result.content['risk_assessment']['overall_risk_level']}")
        
        print("\nConsequence Summary:")
        first = result.content['consequence_analysis']['first_order']['count']
        second = result.content['consequence_analysis']['second_order']['count']
        third = result.content['consequence_analysis']['third_order']['count']
        print(f"First-order: {first}, Second-order: {second}, Third-order: {third}")
        
        print("\nTop 3 Strategic Implications:")
        for i, implication in enumerate(result.content['strategic_implications'][:3], 1):
            print(f"{i}. {implication}")
    
    # Run test
    asyncio.run(test_second_order_thinking())