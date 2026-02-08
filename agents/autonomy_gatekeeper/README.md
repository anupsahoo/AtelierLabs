# Autonomy Gatekeeper

> Part of [AtelierLabs](../../README.md) — a collection of production-ready AI agents.

An AI governance agent that evaluates incoming requests and decides whether the system should **ACT**, **HOLD**, or **ESCALATE** — enforcing restraint, safety, and human oversight at the point of decision.

---

## Why This Exists

Autonomous systems that act without boundaries are liabilities. The Autonomy Gatekeeper introduces a deliberate checkpoint between intent and execution. Every request passes through policy evaluation and, when warranted, LLM-based assessment before any action is taken.

The goal is not to slow systems down. It is to ensure that the right level of scrutiny is applied to the right kind of request.

---

## Decision Flow

```
                ┌─────────────────┐
                │  Incoming       │
                │  Request        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Policy         │
                │  Evaluation     │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
     Critical Escalation?     All other cases
              │                     │
              ▼                     ▼
    ┌─────────────────┐   ┌─────────────────┐
    │  Build Decision  │   │  LLM            │
    │  Card (skip LLM) │   │  Assessment     │
    └─────────────────┘   └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Build Decision  │
                          │  Card            │
                          └─────────────────┘
```

**Policy Evaluation** matches the request against keyword-based rules defined in YAML. If the policy produces a critical escalation, the LLM is skipped entirely to avoid unnecessary cost. Otherwise, the LLM provides a nuanced assessment informed by the matched policies.

---

## Decisions

| Decision     | Meaning                                                    |
|--------------|------------------------------------------------------------|
| **ACT**      | Safe to proceed. Low risk, no ambiguity.                   |
| **HOLD**     | Ambiguous or medium risk. Clarification needed.            |
| **ESCALATE** | High risk or irreversible. Requires human approval.        |

---

## Example Usage

### CLI

```bash
# Evaluate a request
autonomy-gatekeeper evaluate --request "Deploy model v2.3 to production"

# Output as JSON
autonomy-gatekeeper evaluate --request "List all running services" --json-output

# Use a custom policy file
autonomy-gatekeeper evaluate --request "Delete staging data" --policy ./custom-rules.yaml
```

### Example Decision Card

**Human-readable output:**

```
============================================================
  DECISION CARD
============================================================
  Request:      Deploy model v2.3 to production
  Decision:     ESCALATE
  Risk Level:   critical
  Reasoning:    Production deployments are irreversible operations
                that require explicit human approval.
  Policies:
    - [PROD_DEPLOY] Production deployments require human approval
  Action:       Obtain written approval from the deployment owner.
  Timestamp:    2026-02-08T11:15:00+00:00
============================================================
```

**JSON output:**

```json
{
  "request": "Deploy model v2.3 to production",
  "decision": "ESCALATE",
  "risk_level": "critical",
  "reasoning": "Production deployments are irreversible operations that require explicit human approval.",
  "matched_policies": [
    {
      "rule_id": "PROD_DEPLOY",
      "description": "Production deployments require human approval",
      "matched": true
    }
  ],
  "recommended_action": "Obtain written approval from the deployment owner.",
  "timestamp": "2026-02-08T11:15:00+00:00"
}
```

---

## Project Structure

```
agents/autonomy_gatekeeper/
  src/autonomy_gatekeeper/
    cli.py              # CLI entrypoint (Click)
    app.py              # Application orchestrator
    graph.py            # LangGraph state machine
    schemas.py          # Pydantic models (DecisionCard, etc.)
    config.py           # Settings loader (.env + env vars)
    policy/
      rules.yaml        # Governance policy rules
    llm/
      factory.py        # LLM instance creation
      prompts.py        # Prompt templates
    tools/
      registry.py       # Tool registry pattern
    utils/
      logging.py        # Structured logging
  tests/
    test_graph_routing.py
    test_policy_rules.py
```

---

## Configuration

Before running the agent, create a `.env` file from the provided template:

```bash
cp .env.example .env
```

Then set your values:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | Your OpenAI API key. Obtain one from your OpenAI account dashboard. |
| `OPENAI_MODEL` | No | `gpt-4o` | The model used for LLM-based assessment. Any OpenAI chat model works (`gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, etc.). |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`. |
| `POLICY_PATH` | No | `src/autonomy_gatekeeper/policy/rules.yaml` | Path to the YAML policy rules file. Override to use a custom policy. |

The agent will not start without a valid `OPENAI_API_KEY`. All other variables have sensible defaults.

---

## Running Locally

```bash
# Install with dev dependencies
make setup

# Configure environment (see Configuration above)
cp .env.example .env
# Edit .env — at minimum, set OPENAI_API_KEY

# Run an evaluation
make run

# Run tests (does not require an API key)
make test

# Lint and type check
make lint
make typecheck
```

---

## Running with Docker

```bash
# Build the image
make docker-build

# Run with environment file (ensure .env exists with your OPENAI_API_KEY)
make docker-run
```

You can also pass the API key directly:

```bash
docker run --rm -e OPENAI_API_KEY=sk-your-key-here autonomy-gatekeeper evaluate --request "Deploy to production"
```

---

## Policy Configuration

Governance rules are defined in `src/autonomy_gatekeeper/policy/rules.yaml`. Each rule specifies:

- **id** — Unique identifier
- **description** — Human-readable explanation
- **keywords** — Terms that trigger this rule
- **decision** — ACT, HOLD, or ESCALATE
- **risk_level** — low, medium, high, or critical

Rules are evaluated in order. The strongest matching decision and risk level take precedence.

---

## Technology

- **LangChain** — LLM abstraction and prompt management
- **LangGraph** — State machine for decision routing
- **Pydantic** — Structured output schemas and validation
- **Click** — CLI framework
- **Rich** — Terminal output formatting

---

## License

MIT
