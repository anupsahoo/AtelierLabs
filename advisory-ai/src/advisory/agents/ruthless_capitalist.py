"""Ruthless Capitalist lens agent - Moats, pricing power, and competitive dynamics."""

from typing import Any, Dict

from advisory.agents.base import Agent, AgentOutput


class RuthlessCapitalistAgent(Agent):
    """Agent embodying ruthless capitalist approach to moats and competitive advantage."""
    
    def critique(self, content: str, interactive: bool = False) -> AgentOutput:
        """Provide ruthless capitalist critique focusing on moats and pricing power."""
        
        prompt = self._build_prompt(content, interactive)
        response = self.provider.generate(prompt, max_tokens=1500)
        parsed = self._parse_response(response)
        
        # Get relevant blog references
        references = self._get_blog_references([
            "moats", "competition", "pricing", "market-power", "capitalism", "strategy", "monopoly"
        ])
        
        return AgentOutput(
            agent_name="Ruthless Capitalist Lens: Moats & Pricing Power",
            brutal_line=parsed.get('brutal_line', "You have no moat and competitors will crush you on price."),
            key_questions=parsed.get('key_questions', [
                "What prevents competitors from copying this in 6 months?",
                "Where's your pricing power? Can you raise prices 2x?",
                "How do you plan to kill the competition?",
                "What's your path to market dominance?"
            ]),
            assumptions=parsed.get('assumptions', [
                "ASSUMPTION: Being first gives lasting advantage (it doesn't)",
                "FACT: Markets reward monopolistic advantages, not fair competition",
                "GUESS: Customers will pay premium for quality (they usually won't)"
            ]),
            risks=parsed.get('risks', [
                "Commoditization - competitors copy and undercut on price",
                "No switching costs - customers leave for cheaper alternatives",
                "Venture-funded competitor burns cash to steal market share"
            ]),
            bold_move=parsed.get('bold_move', "Find a way to make this winner-take-all instead of winner-take-some."),
            scorecard=parsed.get('scorecard', {
                "Moat Strength": 3,
                "Pricing Power": 4,
                "Competitive Advantage": 5,
                "Market Dominance Potential": 4
            }),
            experiment_plan=parsed.get('experiment_plan', {
                "hypothesis": "We can build sustainable competitive advantages that create pricing power",
                "success_metrics": "Customer acquisition cost vs lifetime value, price elasticity, competitor response time",
                "action_steps": "Identify strongest moat opportunity, test pricing power, analyze competitive threats"
            }),
            references=references[:3]
        )
    
    def _build_prompt(self, content: str, interactive: bool) -> str:
        """Build the prompt for ruthless capitalist critique."""
        
        base_prompt = f"""You are providing feedback as a ruthless capitalist - focused on moats, pricing power, competitive dynamics, and building unassailable market positions. No mercy for weak business models.

CONTENT TO CRITIQUE:
{content}

Provide feedback in this exact structure:

BRUTAL TRUTH: [One harsh line about lack of competitive advantage or pricing power]

MOAT + PRICING POWER ANALYSIS:
- Network Effects: [How does this get stronger with more users?]
- Switching Costs: [What makes customers sticky?]
- Economies of Scale: [How do you get cheaper as you grow?]
- Brand/Regulatory Moats: [What legal or brand advantages exist?]

KEY QUESTIONS:
- What prevents competitors from copying this in 6 months?
- Where's your pricing power? Can you raise prices 2x?
- How do you plan to kill the competition?
- [One more question about market dominance]

ASSUMPTIONS:
- ASSUMPTION: [Something about competition they're assuming]
- FACT: [Something that's actually true about markets/competition]
- GUESS: [Something about customer behavior/pricing that needs testing]

RISKS:
- [Risk of commoditization]
- [Risk of price competition]
- [Risk of well-funded competitors]

BOLD MOVE: [One action that would create winner-take-all dynamics]

SCORECARD:
- Moat Strength: X/10
- Pricing Power: X/10
- Competitive Advantage: X/10
- Market Dominance Potential: X/10

30-DAY EXPERIMENT: Test your pricing power and identify the strongest moat-building opportunity.

Focus on: What's your unfair advantage? How do you dominate this market? Where's your pricing power? How do you crush competition?"""

        if interactive:
            base_prompt += "\n\nIf you need clarification, ask 1-2 specific questions about competitive dynamics or business model defensibility."
        
        return base_prompt
