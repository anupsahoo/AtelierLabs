# AtelierLabs

A growing collection of production-ready AI agents, each built as an independent, deployable project. Every agent in this repository is small by design — focused on a single responsibility, structured for clarity, and ready to run. This is not a framework or a library. It is a workshop where each agent demonstrates how autonomous systems can reason, decide, and act in real-world contexts.

Learning happens by reading the code. There are no tutorials.

---

## Philosophy

- **Intent before implementation.** Understand the problem deeply before writing a single line.
- **Simplicity as a discipline.** Small systems that do one thing well are more valuable than large systems that do many things poorly.
- **Responsibility in autonomy.** Agents that act on behalf of people must be transparent, predictable, and correctable.
- **Craftsmanship over scale.** A well-structured fifty-line agent teaches more than a sprawling framework.
- **Human judgment where it matters.** Full autonomy is not always the goal. Knowing when to defer to a person is a design decision.

---

## Repository Structure

```
AtelierLabs/
  agents/
    autonomy_gatekeeper/       # AI governance agent (ACT / HOLD / ESCALATE)
    <next_agent>/              # Each new agent follows the same pattern
    ...
```

The repository is flat and intentional. Every agent lives under `agents/` in its own self-contained subfolder. Each agent has its own `pyproject.toml`, `src/` layout, tests, Dockerfile, Makefile, and README. No shared dependencies. No coupling between agents. This structure is designed to scale to hundreds of agents without friction.

---

## Agents

| Agent | Description | Docs |
|-------|-------------|------|
| **[Autonomy Gatekeeper](agents/autonomy_gatekeeper/)** | AI governance agent that decides whether to ACT, HOLD, or ESCALATE a request based on policy rules and LLM assessment | [README](agents/autonomy_gatekeeper/README.md) |

New agents will be added to this table as they are built.

---

## Getting Started with Any Agent

Each agent is independent. To work with one:

1. Navigate into the agent's folder
2. Copy `.env.example` to `.env` and add your configuration (see the agent's README for details)
3. Run `make setup` to install dependencies
4. Run `make run` to execute, or `make test` to verify

Every agent README contains specific instructions, environment variables, and usage examples.

---

## Common Configuration

Most agents in this repository use LLM providers. The typical environment variables are:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | API key for OpenAI | `sk-...` |
| `OPENAI_MODEL` | Model to use | `gpt-4o` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

Each agent may have additional configuration. Refer to the `.env.example` file inside each agent's folder for the complete list.

---

## How to Navigate

Pick any agent that interests you. Open its README for context, then read the code starting from the entry point. Each agent is self-explanatory. There is no required order and no prerequisites. The repository rewards curiosity and careful reading.

---

## Author

Built by a technical leader working at the intersection of software architecture and intelligent systems. This repository is a way of sharing practical thinking about agent design through code rather than commentary.

---

## License

This repository is licensed under the MIT License.
