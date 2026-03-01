"""Naval lens agent - Leverage, wealth creation, and first principles."""

from typing import Any, Dict

from board.agents.base import Agent, AgentOutput


class NavalAgent(Agent):
    """Agent embodying Naval Ravikant's approach to leverage and wealth creation."""
    
    def critique(self, content: str, interactive: bool = False) -> AgentOutput:
        """Provide Naval-style critique focusing on leverage and first principles."""
        
        prompt = self._build_prompt(content, interactive)
        response = self.provider.generate(prompt, max_tokens=1500)
        parsed = self._parse_response(response)
        
        # Get relevant blog references
        references = self._get_blog_references([
            "leverage", "wealth", "first-principles", "automation", "scalability", "network-effects"
        ])
        
        return AgentOutput(
            agent_name="Naval Lens: Leverage & Wealth Creation",
            brutal_line=parsed.get('brutal_line', "You're trading time for money instead of building leverage."),
            key_questions=parsed.get('key_questions', [
                "Where's your leverage? (Code, media, capital, or people?)",
                "How does this scale without your direct involvement?",
                "What network effects make this more valuable over time?",
                "Are you solving a problem or creating a vitamin?"
            ]),
            assumptions=parsed.get('assumptions', [
                "ASSUMPTION: Hard work equals success (leverage multiplies work)",
                "FACT: Scalable businesses create more wealth than service businesses",
                "GUESS: This market timing is optimal (needs validation)"
            ]),
            risks=parsed.get('risks', [
                "No clear path to leverage - remains a time-for-money business",
                "Competitors with better leverage will outcompete you",
                "Market may not value this solution at scale"
            ]),
            bold_move=parsed.get('bold_move', "Find the leverage angle that makes this 100x more valuable with same effort."),
            scorecard=parsed.get('scorecard', {
                "Leverage Potential": 4,
                "Scalability": 5,
                "Network Effects": 3,
                "Market Timing": 6
            }),
            experiment_plan=parsed.get('experiment_plan', {
                "hypothesis": "This solution can achieve leverage through [code/media/capital/network]",
                "success_metrics": "Revenue per employee, viral coefficient, marginal cost of serving new users",
                "action_steps": "Identify highest leverage component, build MVP focused on that lever, measure scaling metrics"
            }),
            references=references[:3]
        )
    
    def _build_prompt(self, content: str, interactive: bool) -> str:
        """Build the prompt for Naval-style critique."""
        
        base_prompt = f"""You are providing feedback in the style of Naval Ravikant - focused on leverage, wealth creation, first principles thinking, and building scalable systems.

CONTENT TO CRITIQUE:
{content}

Provide feedback in this exact structure:

BRUTAL TRUTH: [One harsh line about lack of leverage or scalability]

LEVERAGE MAP:
- Code Leverage: [How software/automation multiplies effort]
- Media Leverage: [How content/audience creates compounding returns]
- Capital Leverage: [How money works for you]
- People Leverage: [How others multiply your output]

KEY QUESTIONS:
- Where's your leverage? (Code, media, capital, or people?)
- How does this scale without your direct involvement?
- What network effects make this more valuable over time?
- [One more critical question about wealth creation]

ASSUMPTIONS:
- ASSUMPTION: [Something about business model they're taking for granted]
- FACT: [Something that's actually true about markets/leverage]
- GUESS: [Something about timing/adoption that needs validation]

RISKS:
- [Risk of remaining a time-for-money business]
- [Risk of competitors with better leverage]
- [Risk of market not valuing at scale]

BOLD MOVE: [One action that would create 10x more leverage]

SCORECARD:
- Leverage Potential: X/10
- Scalability: X/10
- Network Effects: X/10
- Market Timing: X/10

30-DAY EXPERIMENT: Identify and test the highest leverage component of this idea.

Focus on: What's the leverage? How does this compound? What makes this more valuable over time without linear effort?"""

        if interactive:
            base_prompt += "\n\nIf you need clarification, ask 1-2 specific questions about the business model or leverage mechanisms."
        
        return base_prompt
