"""Tests for graph routing decisions — ACT, HOLD, ESCALATE."""

from __future__ import annotations

import pytest

from autonomy_gatekeeper.graph import (
    GatekeeperState,
    evaluate_policies,
    load_policy_rules,
    route_after_policy,
    build_decision_card,
)
from autonomy_gatekeeper.schemas import Decision, RiskLevel


@pytest.fixture()
def policy_rules() -> list[dict]:
    """Load the default policy rules."""
    from pathlib import Path

    rules_path = (
        Path(__file__).parent.parent
        / "src"
        / "autonomy_gatekeeper"
        / "policy"
        / "rules.yaml"
    )
    return load_policy_rules(str(rules_path))


def _make_state(request: str) -> GatekeeperState:
    """Create a blank initial state for testing."""
    return GatekeeperState(
        request=request,
        matched_policies=[],
        policy_decision="HOLD",
        policy_risk="medium",
        llm_response={},
        decision_card={},
    )


class TestPolicyRouting:
    """Test that policy evaluation routes requests correctly."""

    def test_production_deploy_escalates(self, policy_rules: list[dict]) -> None:
        state = _make_state("Deploy model v2.3 to production")
        result = evaluate_policies(state, policy_rules)
        assert result["policy_decision"] == "ESCALATE"
        assert result["policy_risk"] == "critical"

    def test_data_deletion_escalates(self, policy_rules: list[dict]) -> None:
        state = _make_state("Delete all user records from staging")
        result = evaluate_policies(state, policy_rules)
        assert result["policy_decision"] == "ESCALATE"
        assert result["policy_risk"] == "critical"

    def test_access_change_holds(self, policy_rules: list[dict]) -> None:
        state = _make_state("Grant admin access to the new team member")
        result = evaluate_policies(state, policy_rules)
        assert result["policy_decision"] == "HOLD"
        assert result["policy_risk"] == "high"

    def test_config_change_holds(self, policy_rules: list[dict]) -> None:
        state = _make_state("Update the configuration for the cache layer")
        result = evaluate_policies(state, policy_rules)
        assert result["policy_decision"] == "HOLD"

    def test_read_only_acts(self, policy_rules: list[dict]) -> None:
        state = _make_state("List all running services and their status")
        result = evaluate_policies(state, policy_rules)
        assert result["policy_decision"] == "ACT"
        assert result["policy_risk"] == "low"

    def test_monitoring_acts(self, policy_rules: list[dict]) -> None:
        state = _make_state("Check health of the payment service")
        result = evaluate_policies(state, policy_rules)
        assert result["policy_decision"] == "ACT"
        assert result["policy_risk"] == "low"

    def test_unknown_request_defaults_to_act(self, policy_rules: list[dict]) -> None:
        state = _make_state("Summarize the quarterly report")
        result = evaluate_policies(state, policy_rules)
        # No keywords match, so defaults remain
        assert result["policy_decision"] == "ACT"
        assert len(result["matched_policies"]) == 0


class TestConditionalRouting:
    """Test the conditional edge routing logic."""

    def test_critical_escalation_skips_llm(self) -> None:
        state = _make_state("Deploy to production")
        state["policy_decision"] = "ESCALATE"
        state["policy_risk"] = "critical"
        assert route_after_policy(state) == "build_decision"

    def test_non_critical_goes_to_llm(self) -> None:
        state = _make_state("Update config")
        state["policy_decision"] = "HOLD"
        state["policy_risk"] = "medium"
        assert route_after_policy(state) == "llm_assess"

    def test_act_goes_to_llm(self) -> None:
        state = _make_state("List services")
        state["policy_decision"] = "ACT"
        state["policy_risk"] = "low"
        assert route_after_policy(state) == "llm_assess"


class TestDecisionCard:
    """Test decision card assembly."""

    def test_card_from_policy_only(self) -> None:
        state = _make_state("Delete production database")
        state["policy_decision"] = "ESCALATE"
        state["policy_risk"] = "critical"
        state["matched_policies"] = [
            {"rule_id": "DATA_DELETE", "description": "Data deletion", "matched": True}
        ]
        state["llm_response"] = {
            "decision": "ESCALATE",
            "risk_level": "critical",
            "reasoning": "Irreversible data operation.",
            "recommended_action": "Require explicit human approval.",
        }

        result = build_decision_card(state)
        card_data = result["decision_card"]
        assert card_data["decision"] == Decision.ESCALATE.value
        assert card_data["risk_level"] == RiskLevel.CRITICAL.value
        assert len(card_data["matched_policies"]) == 1

    def test_card_defaults_on_invalid_llm_response(self) -> None:
        state = _make_state("Do something ambiguous")
        state["policy_decision"] = "HOLD"
        state["policy_risk"] = "medium"
        state["matched_policies"] = []
        state["llm_response"] = {
            "decision": "INVALID",
            "risk_level": "unknown",
            "reasoning": "Test fallback.",
            "recommended_action": "",
        }

        result = build_decision_card(state)
        card_data = result["decision_card"]
        # Invalid values should fall back to HOLD / MEDIUM
        assert card_data["decision"] == Decision.HOLD.value
        assert card_data["risk_level"] == RiskLevel.MEDIUM.value
