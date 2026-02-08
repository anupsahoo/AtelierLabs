"""Application entrypoint — orchestrates the governance evaluation pipeline."""

from __future__ import annotations

import json

from autonomy_gatekeeper.config import Settings, load_settings
from autonomy_gatekeeper.graph import GatekeeperState, build_graph
from autonomy_gatekeeper.schemas import DecisionCard
from autonomy_gatekeeper.utils.logging import setup_logging


def evaluate_request(
    request: str,
    settings: Settings | None = None,
) -> DecisionCard:
    """Run a request through the governance graph and return a DecisionCard."""
    if settings is None:
        settings = load_settings()

    logger = setup_logging(settings.log_level)
    logger.info("Evaluating request: %s", request[:120])

    graph = build_graph(settings)
    compiled = graph.compile()

    initial_state: GatekeeperState = {
        "request": request,
        "matched_policies": [],
        "policy_decision": "HOLD",
        "policy_risk": "medium",
        "llm_response": {},
        "decision_card": {},
    }

    final_state = compiled.invoke(initial_state)
    card = DecisionCard(**final_state["decision_card"])

    logger.info("Decision: %s | Risk: %s", card.decision.value, card.risk_level.value)
    return card


def format_output(card: DecisionCard, output_json: bool = False) -> str:
    """Format a DecisionCard for display."""
    if output_json:
        return json.dumps(card.model_dump(mode="json"), indent=2)
    return card.to_human_readable()
