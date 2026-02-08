"""LangGraph state machine — routes requests through policy evaluation and LLM assessment."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, TypedDict

import yaml
from langgraph.graph import END, StateGraph

from autonomy_gatekeeper.config import Settings
from autonomy_gatekeeper.llm.factory import create_llm
from autonomy_gatekeeper.llm.prompts import build_governance_prompt
from autonomy_gatekeeper.schemas import (
    Decision,
    DecisionCard,
    PolicyMatch,
    RiskLevel,
)

logger = logging.getLogger("autonomy_gatekeeper")


class GatekeeperState(TypedDict):
    """State passed through the governance graph."""

    request: str
    matched_policies: list[dict[str, Any]]
    policy_decision: str
    policy_risk: str
    llm_response: dict[str, Any]
    decision_card: dict[str, Any]


def load_policy_rules(policy_path: str) -> list[dict[str, Any]]:
    """Load policy rules from a YAML file."""
    path = Path(policy_path)
    if not path.exists():
        logger.warning("Policy file not found at %s, using empty rules", policy_path)
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("rules", []) if data else []


def evaluate_policies(state: GatekeeperState, rules: list[dict[str, Any]]) -> GatekeeperState:
    """Match request text against policy rules using keyword matching."""
    request_lower = state["request"].lower()
    matched: list[dict[str, Any]] = []
    strongest_decision = "ACT"
    strongest_risk = "low"

    decision_priority = {"ACT": 0, "HOLD": 1, "ESCALATE": 2}
    risk_priority = {"low": 0, "medium": 1, "high": 2, "critical": 3}

    for rule in rules:
        keywords = [kw.lower() for kw in rule.get("keywords", [])]
        if any(kw in request_lower for kw in keywords):
            matched.append(
                {
                    "rule_id": rule["id"],
                    "description": rule["description"],
                    "matched": True,
                }
            )
            rule_decision = rule.get("decision", "HOLD")
            rule_risk = rule.get("risk_level", "medium")

            if decision_priority.get(rule_decision, 0) > decision_priority.get(
                strongest_decision, 0
            ):
                strongest_decision = rule_decision

            if risk_priority.get(rule_risk, 0) > risk_priority.get(
                strongest_risk, 0
            ):
                strongest_risk = rule_risk

    state["matched_policies"] = matched
    state["policy_decision"] = strongest_decision
    state["policy_risk"] = strongest_risk
    logger.info(
        "Policy evaluation: decision=%s risk=%s matched=%d rules",
        strongest_decision,
        strongest_risk,
        len(matched),
    )
    return state


def assess_with_llm(state: GatekeeperState, settings: Settings) -> GatekeeperState:
    """Use the LLM to produce a governance assessment informed by policy matches."""
    llm = create_llm(settings)
    prompt = build_governance_prompt()

    policies_text = "\n".join(
        f"- [{p['rule_id']}] {p['description']}" for p in state["matched_policies"]
    )
    if not policies_text:
        policies_text = "(no policy rules matched)"

    chain = prompt | llm
    response = chain.invoke(
        {"request": state["request"], "matched_policies": policies_text}
    )

    try:
        content = response.content if hasattr(response, "content") else str(response)
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
            cleaned = cleaned.rsplit("```", 1)[0]
        parsed = json.loads(cleaned)
    except (json.JSONDecodeError, IndexError):
        logger.warning("LLM returned non-JSON response, falling back to policy decision")
        parsed = {
            "decision": state["policy_decision"],
            "risk_level": state["policy_risk"],
            "reasoning": "LLM response could not be parsed. Falling back to policy-based decision.",
            "recommended_action": "Review the request manually.",
        }

    state["llm_response"] = parsed
    return state


def build_decision_card(state: GatekeeperState) -> GatekeeperState:
    """Assemble the final Decision Card from policy and LLM outputs."""
    llm_resp = state.get("llm_response", {})

    decision_str = llm_resp.get("decision", state["policy_decision"])
    risk_str = llm_resp.get("risk_level", state["policy_risk"])

    try:
        decision = Decision(decision_str.upper())
    except ValueError:
        decision = Decision.HOLD

    try:
        risk_level = RiskLevel(risk_str.lower())
    except ValueError:
        risk_level = RiskLevel.MEDIUM

    card = DecisionCard(
        request=state["request"],
        decision=decision,
        risk_level=risk_level,
        reasoning=llm_resp.get("reasoning", "No reasoning provided."),
        matched_policies=[
            PolicyMatch(**p) for p in state.get("matched_policies", [])
        ],
        recommended_action=llm_resp.get("recommended_action", ""),
    )

    state["decision_card"] = card.model_dump(mode="json")
    return state


def route_after_policy(state: GatekeeperState) -> str:
    """Determine the next node based on policy evaluation.

    If policy alone produces ESCALATE with critical risk, skip the LLM
    to avoid unnecessary cost. Otherwise, proceed to LLM assessment.
    """
    if (
        state["policy_decision"] == "ESCALATE"
        and state["policy_risk"] == "critical"
    ):
        logger.info("Critical escalation — skipping LLM, routing to decision card")
        return "build_decision"
    return "llm_assess"


def build_graph(settings: Settings) -> StateGraph:
    """Construct the LangGraph governance state machine."""
    rules = load_policy_rules(settings.policy_path)

    def policy_node(state: GatekeeperState) -> GatekeeperState:
        return evaluate_policies(state, rules)

    def llm_node(state: GatekeeperState) -> GatekeeperState:
        return assess_with_llm(state, settings)

    def decision_node(state: GatekeeperState) -> GatekeeperState:
        return build_decision_card(state)

    graph = StateGraph(GatekeeperState)

    graph.add_node("evaluate_policy", policy_node)
    graph.add_node("llm_assess", llm_node)
    graph.add_node("build_decision", decision_node)

    graph.set_entry_point("evaluate_policy")
    graph.add_conditional_edges(
        "evaluate_policy",
        route_after_policy,
        {"llm_assess": "llm_assess", "build_decision": "build_decision"},
    )
    graph.add_edge("llm_assess", "build_decision")
    graph.add_edge("build_decision", END)

    return graph
