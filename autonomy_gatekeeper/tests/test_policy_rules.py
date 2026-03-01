"""Tests for policy rule loading and evaluation."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from autonomy_gatekeeper.graph import evaluate_policies, load_policy_rules, GatekeeperState


RULES_PATH = str(
    Path(__file__).parent.parent
    / "src"
    / "autonomy_gatekeeper"
    / "policy"
    / "rules.yaml"
)


class TestPolicyLoading:
    """Test that policy rules load correctly from YAML."""

    def test_rules_file_exists(self) -> None:
        assert Path(RULES_PATH).exists()

    def test_rules_load_as_list(self) -> None:
        rules = load_policy_rules(RULES_PATH)
        assert isinstance(rules, list)
        assert len(rules) > 0

    def test_each_rule_has_required_fields(self) -> None:
        rules = load_policy_rules(RULES_PATH)
        required_fields = {"id", "description", "keywords", "decision", "risk_level"}
        for rule in rules:
            missing = required_fields - set(rule.keys())
            assert not missing, f"Rule {rule.get('id', '?')} missing fields: {missing}"

    def test_all_decisions_are_valid(self) -> None:
        rules = load_policy_rules(RULES_PATH)
        valid_decisions = {"ACT", "HOLD", "ESCALATE"}
        for rule in rules:
            assert rule["decision"] in valid_decisions, (
                f"Rule {rule['id']} has invalid decision: {rule['decision']}"
            )

    def test_all_risk_levels_are_valid(self) -> None:
        rules = load_policy_rules(RULES_PATH)
        valid_risks = {"low", "medium", "high", "critical"}
        for rule in rules:
            assert rule["risk_level"] in valid_risks, (
                f"Rule {rule['id']} has invalid risk_level: {rule['risk_level']}"
            )

    def test_missing_file_returns_empty(self, tmp_path: Path) -> None:
        rules = load_policy_rules(str(tmp_path / "nonexistent.yaml"))
        assert rules == []

    def test_empty_file_returns_empty(self, tmp_path: Path) -> None:
        empty_file = tmp_path / "empty.yaml"
        empty_file.write_text("")
        rules = load_policy_rules(str(empty_file))
        assert rules == []


class TestPolicyEvaluation:
    """Test keyword-based policy matching logic."""

    @pytest.fixture()
    def custom_rules(self) -> list[dict]:
        return [
            {
                "id": "TEST_ESCALATE",
                "description": "Test escalation rule",
                "keywords": ["danger", "critical-op"],
                "decision": "ESCALATE",
                "risk_level": "critical",
            },
            {
                "id": "TEST_HOLD",
                "description": "Test hold rule",
                "keywords": ["maybe", "unclear"],
                "decision": "HOLD",
                "risk_level": "medium",
            },
            {
                "id": "TEST_ACT",
                "description": "Test act rule",
                "keywords": ["safe", "harmless"],
                "decision": "ACT",
                "risk_level": "low",
            },
        ]

    def _make_state(self, request: str) -> GatekeeperState:
        return GatekeeperState(
            request=request,
            matched_policies=[],
            policy_decision="ACT",
            policy_risk="low",
            llm_response={},
            decision_card={},
        )

    def test_escalation_keyword_match(self, custom_rules: list[dict]) -> None:
        state = self._make_state("This is a danger zone operation")
        result = evaluate_policies(state, custom_rules)
        assert result["policy_decision"] == "ESCALATE"
        assert any(p["rule_id"] == "TEST_ESCALATE" for p in result["matched_policies"])

    def test_hold_keyword_match(self, custom_rules: list[dict]) -> None:
        state = self._make_state("This is maybe something we should do")
        result = evaluate_policies(state, custom_rules)
        assert result["policy_decision"] == "HOLD"

    def test_act_keyword_match(self, custom_rules: list[dict]) -> None:
        state = self._make_state("This is a safe read operation")
        result = evaluate_policies(state, custom_rules)
        assert result["policy_decision"] == "ACT"

    def test_strongest_decision_wins(self, custom_rules: list[dict]) -> None:
        state = self._make_state("This is a safe but danger operation")
        result = evaluate_policies(state, custom_rules)
        # ESCALATE should win over ACT
        assert result["policy_decision"] == "ESCALATE"

    def test_case_insensitive_matching(self, custom_rules: list[dict]) -> None:
        state = self._make_state("DANGER DANGER DANGER")
        result = evaluate_policies(state, custom_rules)
        assert result["policy_decision"] == "ESCALATE"

    def test_no_match_keeps_defaults(self, custom_rules: list[dict]) -> None:
        state = self._make_state("Something completely unrelated")
        result = evaluate_policies(state, custom_rules)
        assert result["policy_decision"] == "ACT"
        assert len(result["matched_policies"]) == 0
