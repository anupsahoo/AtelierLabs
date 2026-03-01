"""Jobs lens agent - Ruthless simplicity and user obsession."""

from typing import Any, Dict

from advisory.agents.base import Agent, AgentOutput


class JobsAgent(Agent):
    """Agent embodying Steve Jobs' approach to product critique."""
    
    def critique(self, content: str, interactive: bool = False) -> AgentOutput:
        """Provide Jobs-style critique focusing on simplicity and user experience."""
        
        prompt = self._build_prompt(content, interactive)
        response = self.provider.generate(prompt, max_tokens=1500)
        parsed = self._parse_response(response)
        
        # Get relevant blog references
        references = self._get_blog_references([
            "simplicity", "user-experience", "product", "design", "focus"
        ])
        
        return AgentOutput(
            agent_name="Jobs Lens: Ruthless Simplicity",
            brutal_line=parsed.get('brutal_line', "You're building a feature factory, not solving a real problem."),
            key_questions=parsed.get('key_questions', [
                "What's the one thing users will do every single day?",
                "How is this 10x better than the current solution?",
                "What would you remove if you only had 1 screen?",
                "Can your grandmother use this without instructions?"
            ]),
            assumptions=parsed.get('assumptions', [
                "ASSUMPTION: Users want more features (they want fewer, better ones)",
                "ASSUMPTION: Complexity shows sophistication (simplicity shows mastery)",
                "ASSUMPTION: You can educate users to change behavior (you can't)"
            ]),
            risks=parsed.get('risks', [
                "Feature creep will kill the core value proposition",
                "Users will abandon due to complexity",
                "Team will lose focus on what matters most"
            ]),
            bold_move=parsed.get('bold_move', "Remove 80% of planned features and perfect the remaining 20%."),
            scorecard=parsed.get('scorecard', {
                "Simplicity": 4,
                "User Focus": 6,
                "Differentiation": 5,
                "Execution Clarity": 3
            }),
            experiment_plan=parsed.get('experiment_plan', {
                "hypothesis": "Users prefer simple, focused solution over feature-rich alternative",
                "success_metrics": "Daily active usage, task completion rate, user satisfaction scores",
                "action_steps": "Build single-feature MVP, test with 50 users, measure engagement vs complexity"
            }),
            references=references[:3]  # Limit to top 3 references
        )
    
    def _build_prompt(self, content: str, interactive: bool) -> str:
        """Build the prompt for Jobs-style critique."""
        
        base_prompt = f"""You are providing feedback in the style of Steve Jobs - known for ruthless simplicity, user obsession, and cutting through complexity to find the essential truth.

CONTENT TO CRITIQUE:
{content}

Provide feedback in this exact structure:

BRUTAL TRUTH: [One harsh but honest line about the core problem]

WHAT I WOULD CUT:
- [Specific feature/aspect to remove]
- [Another thing to eliminate]
- [Third thing that's unnecessary]

KEY QUESTIONS:
- What's the one thing users will do every single day?
- How is this 10x better than existing solutions?
- What would you remove if you only had 1 screen?
- [One more critical question]

ASSUMPTIONS:
- ASSUMPTION: [Something they're taking for granted]
- FACT: [Something that's actually true]
- GUESS: [Something that needs validation]

RISKS:
- [Primary risk to user adoption]
- [Risk to business model]
- [Risk to execution]

BOLD MOVE: [One counterintuitive action that would dramatically improve this]

SCORECARD:
- Simplicity: X/10
- User Focus: X/10
- Differentiation: X/10
- Execution Clarity: X/10

30-DAY EXPERIMENT: Build the simplest possible version that delivers core value and test with real users.

Focus on: What would you cut? What's the essential user need? How do you make this so simple it's obvious?"""

        if interactive:
            base_prompt += "\n\nIf you need clarification, ask 1-2 specific questions about user needs or core functionality."
        
        return base_prompt
