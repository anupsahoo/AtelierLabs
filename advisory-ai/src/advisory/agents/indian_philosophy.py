"""Indian Philosophy lens agent - Dharma, long-term thinking, and ethical frameworks."""

from typing import Any, Dict

from advisory.agents.base import Agent, AgentOutput


class IndianPhilosophyAgent(Agent):
    """Agent embodying Indian philosophical approaches to dharma and ethical decision-making."""
    
    def critique(self, content: str, interactive: bool = False) -> AgentOutput:
        """Provide Indian philosophy-style critique focusing on dharma and long-term thinking."""
        
        prompt = self._build_prompt(content, interactive)
        response = self.provider.generate(prompt, max_tokens=1500)
        parsed = self._parse_response(response)
        
        # Get relevant blog references
        references = self._get_blog_references([
            "ethics", "dharma", "long-term", "sustainability", "purpose", "values", "philosophy"
        ])
        
        return AgentOutput(
            agent_name="Indian Philosophy Lens: Dharma & Long-term Thinking",
            brutal_line=parsed.get('brutal_line', "You're optimizing for short-term gains while ignoring your dharmic purpose."),
            key_questions=parsed.get('key_questions', [
                "What is the dharmic purpose of this endeavor?",
                "How does this serve the greater good beyond profit?",
                "What are the consequences seven generations from now?",
                "Are you acting from ego (ahamkara) or genuine service (seva)?"
            ]),
            assumptions=parsed.get('assumptions', [
                "ASSUMPTION: Success means financial returns (dharma includes broader impact)",
                "FACT: Sustainable businesses align with natural principles",
                "GUESS: Short-term metrics predict long-term value (often inverse)"
            ]),
            risks=parsed.get('risks', [
                "Misalignment with dharmic purpose leads to eventual failure",
                "Short-term thinking creates long-term negative karma",
                "Ignoring stakeholder harmony causes systemic problems"
            ]),
            bold_move=parsed.get('bold_move', "Redesign this entire approach around serving others rather than serving yourself."),
            scorecard=parsed.get('scorecard', {
                "Dharmic Alignment": 4,
                "Long-term Sustainability": 5,
                "Stakeholder Harmony": 6,
                "Ethical Foundation": 7
            }),
            experiment_plan=parsed.get('experiment_plan', {
                "hypothesis": "Aligning with dharmic principles will create more sustainable and fulfilling outcomes",
                "success_metrics": "Stakeholder satisfaction, long-term sustainability indicators, ethical impact measures",
                "action_steps": "Define dharmic purpose, assess all stakeholder impacts, redesign for service over profit"
            }),
            references=references[:3]
        )
    
    def _build_prompt(self, content: str, interactive: bool) -> str:
        """Build the prompt for Indian philosophy-style critique."""
        
        base_prompt = f"""You are providing feedback through the lens of Indian philosophy - focusing on dharma (righteous purpose), long-term thinking, ethical frameworks, and the interconnectedness of all actions.

CONTENT TO CRITIQUE:
{content}

Provide feedback in this exact structure:

BRUTAL TRUTH: [One harsh line about misaligned purpose or short-term thinking]

DHARMA CHECK:
- Purpose Alignment: [How well does this serve righteous purpose?]
- Stakeholder Impact: [Effect on all beings, not just customers/shareholders]
- Karmic Consequences: [Long-term effects of these actions]
- Ego vs Service: [Is this driven by ego or genuine service?]

KEY QUESTIONS:
- What is the dharmic purpose of this endeavor?
- How does this serve the greater good beyond profit?
- What are the consequences seven generations from now?
- [One more question about ethical foundations]

ASSUMPTIONS:
- ASSUMPTION: [Something about success/purpose they're assuming]
- FACT: [Something that's actually true about sustainability/ethics]
- GUESS: [Something about long-term impact that needs consideration]

RISKS:
- [Risk of dharmic misalignment]
- [Risk of short-term thinking]
- [Risk of stakeholder harm]

BOLD MOVE: [One action that would align this with higher purpose and long-term thinking]

SCORECARD:
- Dharmic Alignment: X/10
- Long-term Sustainability: X/10
- Stakeholder Harmony: X/10
- Ethical Foundation: X/10

30-DAY EXPERIMENT: Redesign the approach to prioritize service and long-term stakeholder benefit.

Focus on: What is the higher purpose? How does this serve all stakeholders? What are the long-term consequences? Is this dharmic?"""

        if interactive:
            base_prompt += "\n\nIf you need clarification, ask 1-2 specific questions about purpose, stakeholder impact, or long-term vision."
        
        return base_prompt
