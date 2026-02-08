"""Prompt templates for governance evaluation."""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

GOVERNANCE_SYSTEM_PROMPT = """\
You are an AI governance evaluator. Your role is to assess incoming requests
and determine the appropriate level of autonomy.

You must return a JSON object with these fields:
- decision: one of "ACT", "HOLD", or "ESCALATE"
- risk_level: one of "low", "medium", "high", or "critical"
- reasoning: a concise explanation of your assessment
- recommended_action: a short suggested next step

Decision guidelines:
- ACT: The request is safe, low-risk, and can proceed without human intervention.
- HOLD: The request is ambiguous or medium-risk. Ask for clarification before proceeding.
- ESCALATE: The request is high-risk or irreversible. Require explicit human approval.

Policy rules that matched this request:
{matched_policies}

Evaluate the following request strictly. When in doubt, choose the more
cautious option. Never default to ACT for ambiguous requests."""

GOVERNANCE_USER_PROMPT = """\
Request: {request}

Provide your governance evaluation as JSON."""


def build_governance_prompt() -> ChatPromptTemplate:
    """Build the governance evaluation prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            ("system", GOVERNANCE_SYSTEM_PROMPT),
            ("human", GOVERNANCE_USER_PROMPT),
        ]
    )
