"""Munger lens agent - Mental models, inversion, and avoiding stupidity."""

from typing import Any, Dict

from board.agents.base import Agent, AgentOutput


class MungerAgent(Agent):
    """Agent embodying Charlie Munger's approach to mental models and inversion."""
    
    def critique(self, content: str, interactive: bool = False) -> AgentOutput:
        """Provide Munger-style critique focusing on mental models and inversion."""
        
        prompt = self._build_prompt(content, interactive)
        response = self.provider.generate(prompt, max_tokens=1500)
        parsed = self._parse_response(response)
        
        # Get relevant blog references
        references = self._get_blog_references([
            "mental-models", "inversion", "psychology", "biases", "systems-thinking", "failure"
        ])
        
        return AgentOutput(
            agent_name="Munger Lens: Mental Models & Inversion",
            brutal_line=parsed.get('brutal_line', "You're solving the wrong problem because you haven't inverted it."),
            key_questions=parsed.get('key_questions', [
                "What mental models are you missing here?",
                "If this fails spectacularly, what would be the cause?",
                "What biases are clouding your judgment?",
                "What would the opposite approach look like?"
            ]),
            assumptions=parsed.get('assumptions', [
                "ASSUMPTION: Customers will behave rationally (they won't)",
                "FACT: Incentives drive behavior more than intentions",
                "GUESS: Market conditions will remain stable (they change)"
            ]),
            risks=parsed.get('risks', [
                "Confirmation bias preventing you from seeing fatal flaws",
                "Overconfidence in your ability to predict outcomes",
                "Ignoring second and third-order consequences"
            ]),
            bold_move=parsed.get('bold_move', "Spend 30 days trying to prove why this idea will definitely fail."),
            scorecard=parsed.get('scorecard', {
                "Mental Model Usage": 4,
                "Inversion Thinking": 3,
                "Bias Awareness": 5,
                "Systems Perspective": 6
            }),
            experiment_plan=parsed.get('experiment_plan', {
                "hypothesis": "By inverting the problem, we'll discover the real constraints and failure modes",
                "success_metrics": "Number of failure modes identified, quality of mental models applied, bias mitigation strategies",
                "action_steps": "List all ways this could fail, apply 5 relevant mental models, identify cognitive biases in planning"
            }),
            references=references[:3]
        )
    
    def _build_prompt(self, content: str, interactive: bool) -> str:
        """Build the prompt for Munger-style critique."""
        
        base_prompt = f"""You are providing feedback in the style of Charlie Munger - focused on mental models, inversion thinking, avoiding stupidity, and understanding human psychology and incentives.

CONTENT TO CRITIQUE:
{content}

Provide feedback in this exact structure:

BRUTAL TRUTH: [One harsh line about flawed thinking or missing mental models]

INVERSION: HOW THIS FAILS
- [Primary failure mode when inverted]
- [Second-order failure consequence]
- [Third-order systemic failure]

MENTAL MODELS TO APPLY:
- [Relevant mental model #1 and how it applies]
- [Relevant mental model #2 and how it applies]
- [Relevant mental model #3 and how it applies]

KEY QUESTIONS:
- What mental models are you missing here?
- If this fails spectacularly, what would be the cause?
- What biases are clouding your judgment?
- [One more question about incentives or psychology]

ASSUMPTIONS:
- ASSUMPTION: [Something about human behavior they're assuming]
- FACT: [Something that's actually true about psychology/incentives]
- GUESS: [Something about market/timing that needs validation]

RISKS:
- [Cognitive bias risk]
- [Incentive misalignment risk]
- [Second-order consequence risk]

BOLD MOVE: [One action that inverts the conventional approach]

SCORECARD:
- Mental Model Usage: X/10
- Inversion Thinking: X/10
- Bias Awareness: X/10
- Systems Perspective: X/10

30-DAY EXPERIMENT: Spend time trying to prove why this will fail, then address those failure modes.

Focus on: What could go wrong? What mental models apply? What are you not seeing? How do incentives really work here?"""

        if interactive:
            base_prompt += "\n\nIf you need clarification, ask 1-2 specific questions about incentives, mental models, or potential failure modes."
        
        return base_prompt
