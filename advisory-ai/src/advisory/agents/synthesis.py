"""Synthesis agent - Reconciles disagreements and creates final actionable plan."""

from typing import Any, Dict, List

from advisory.agents.base import Agent, AgentOutput


class SynthesisAgent(Agent):
    """Agent that synthesizes feedback from all advisory members into actionable plan."""
    
    def synthesize(self, content: str, critiques: List[AgentOutput]) -> AgentOutput:
        """Synthesize multiple critiques into unified actionable plan."""
        
        prompt = self._build_synthesis_prompt(content, critiques)
        response = self.provider.generate(prompt, max_tokens=2000)
        parsed = self._parse_response(response)
        
        # Aggregate references from all critiques
        all_references = []
        for critique in critiques:
            all_references.extend(critique.references)
        
        # Remove duplicates and limit
        unique_refs = []
        seen_urls = set()
        for ref in all_references:
            if ref.get('url') not in seen_urls:
                unique_refs.append(ref)
                seen_urls.add(ref.get('url'))
        
        return AgentOutput(
            agent_name="Board Synthesis: Unified Action Plan",
            brutal_line=parsed.get('brutal_line', "The advisory agrees: you need to focus, find leverage, avoid stupidity, serve others, and build moats."),
            key_questions=parsed.get('key_questions', [
                "What's the single most important thing to validate first?",
                "Which advisory member's advice should you prioritize and why?",
                "What would success look like in 90 days?",
                "What's the biggest risk that all advisory members agree on?"
            ]),
            assumptions=parsed.get('assumptions', [
                "SYNTHESIS: Multiple advisory members identified similar assumptions",
                "CONSENSUS: All agree on the core market/user validation needs",
                "DISAGREEMENT: Tension between short-term execution and long-term vision"
            ]),
            risks=parsed.get('risks', [
                "Trying to address all feedback simultaneously (analysis paralysis)",
                "Ignoring the consensus warnings about market/competition",
                "Choosing the wrong lens to prioritize for next phase"
            ]),
            bold_move=parsed.get('bold_move', "Pick one advisory member's lens as your primary filter for the next 90 days."),
            scorecard=parsed.get('scorecard', {
                "Board Consensus": 7,
                "Action Clarity": 6,
                "Risk Mitigation": 8,
                "Strategic Focus": 5
            }),
            experiment_plan=parsed.get('experiment_plan', {
                "hypothesis": "Focusing on the highest-consensus recommendations will yield fastest validation",
                "success_metrics": "Progress on top 3 advisory recommendations, risk mitigation, strategic clarity",
                "action_steps": "Choose primary lens, address top consensus risks, validate core assumptions"
            }),
            references=unique_refs[:5]  # Top 5 unique references
        )
    
    def critique(self, content: str, interactive: bool = False) -> AgentOutput:
        """Not used - synthesis agent only synthesizes other critiques."""
        raise NotImplementedError("Synthesis agent only synthesizes other critiques")
    
    def _build_synthesis_prompt(self, content: str, critiques: List[AgentOutput]) -> str:
        """Build prompt for synthesizing multiple critiques."""
        
        critique_summaries = []
        for critique in critiques:
            summary = f"""
{critique.agent_name}:
- Brutal Truth: {critique.brutal_line}
- Key Risks: {', '.join(critique.risks[:2])}
- Bold Move: {critique.bold_move}
- Top Scores: {self._format_top_scores(critique.scorecard)}
"""
            critique_summaries.append(summary.strip())
        
        critiques_text = "\n\n".join(critique_summaries)
        
        return f"""You are synthesizing feedback from a advisory of AI advisors. Your job is to reconcile disagreements, identify consensus, and create one unified action plan.

ORIGINAL CONTENT:
{content}

BOARD FEEDBACK RECEIVED:
{critiques_text}

Provide synthesis in this exact structure:

BRUTAL TRUTH: [One line that captures the board's consensus on the biggest issue]

BOARD CONSENSUS:
- [What all/most advisory members agree on]
- [Second area of strong agreement]
- [Third consensus point]

KEY DISAGREEMENTS:
- [Where advisory members conflict and why]
- [How to resolve the tension]

UNIFIED RECOMMENDATIONS:
1. [Top priority action based on consensus]
2. [Second priority that addresses multiple concerns]
3. [Third action that mitigates biggest risks]

KEY QUESTIONS:
- What's the single most important thing to validate first?
- Which advisory member's advice should you prioritize and why?
- What would success look like in 90 days?
- [One more strategic question]

ASSUMPTIONS:
- SYNTHESIS: [What multiple advisory members identified]
- CONSENSUS: [What all agree needs validation]
- DISAGREEMENT: [Where there's productive tension]

RISKS:
- [Risk of trying to do everything at once]
- [Consensus risk all advisory members identified]
- [Risk of ignoring important minority opinion]

BOLD MOVE: [One action that addresses multiple advisory concerns simultaneously]

SCORECARD:
- Board Consensus: X/10
- Action Clarity: X/10
- Risk Mitigation: X/10
- Strategic Focus: X/10

90-DAY UNIFIED PLAN: [Concrete plan that synthesizes the best advice from all advisory members]

Focus on: What does the advisory agree on? Where do they disagree and why? What's the unified path forward?"""
    
    def _format_top_scores(self, scorecard: Dict[str, int]) -> str:
        """Format top 2 scores from scorecard."""
        if not scorecard:
            return "No scores"
        
        sorted_scores = sorted(scorecard.items(), key=lambda x: x[1], reverse=True)
        top_2 = sorted_scores[:2]
        return ", ".join([f"{metric}: {score}/10" for metric, score in top_2])
