"""Decision output schemas — structured models for governance decisions."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class Decision(str, Enum):
    """Possible governance decisions."""

    ACT = "ACT"
    HOLD = "HOLD"
    ESCALATE = "ESCALATE"


class RiskLevel(str, Enum):
    """Risk classification for incoming requests."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PolicyMatch(BaseModel):
    """A policy rule that matched the request."""

    rule_id: str
    description: str
    matched: bool = True


class DecisionCard(BaseModel):
    """The structured output of a governance evaluation — the Decision Card."""

    request: str = Field(description="Original request text")
    decision: Decision = Field(description="Governance decision: ACT, HOLD, or ESCALATE")
    risk_level: RiskLevel = Field(description="Assessed risk level")
    reasoning: str = Field(description="Explanation of why this decision was made")
    matched_policies: list[PolicyMatch] = Field(
        default_factory=list,
        description="Policy rules that influenced the decision",
    )
    recommended_action: str = Field(
        default="",
        description="Suggested next step for the operator",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of the evaluation",
    )

    def to_human_readable(self) -> str:
        """Render the decision card as human-readable text."""
        policies = "\n".join(
            f"    - [{p.rule_id}] {p.description}" for p in self.matched_policies
        )
        if not policies:
            policies = "    (none)"

        return (
            f"{'=' * 60}\n"
            f"  DECISION CARD\n"
            f"{'=' * 60}\n"
            f"  Request:      {self.request}\n"
            f"  Decision:     {self.decision.value}\n"
            f"  Risk Level:   {self.risk_level.value}\n"
            f"  Reasoning:    {self.reasoning}\n"
            f"  Policies:\n{policies}\n"
            f"  Action:       {self.recommended_action}\n"
            f"  Timestamp:    {self.timestamp.isoformat()}\n"
            f"{'=' * 60}"
        )
