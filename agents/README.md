# Agents

Every project in this folder is a self-contained AI agent — small, readable, and complete. Each agent lives in its own subfolder with independent dependencies, tests, configuration, and documentation. No agent depends on another. This isolation is intentional and allows the repository to scale to hundreds of agents without coupling or conflict.

## Convention

Every agent follows the same project structure:

```
<agent_name>/
  pyproject.toml          # Dependencies and CLI entrypoint
  .env.example            # Required environment variables
  Makefile                # setup, lint, typecheck, test, run, docker-build, docker-run
  Dockerfile              # Container-ready
  README.md               # Purpose, usage, configuration
  src/<agent_name>/       # Source code (src layout)
  tests/                  # Unit tests
```

To run any agent: enter its folder, copy `.env.example` to `.env`, set your keys, and run `make setup && make run`.

## Agent Index

| Agent | Description | Docs |
|-------|-------------|------|
| **[Autonomy Gatekeeper](autonomy_gatekeeper/)** | AI governance agent — decides whether to ACT, HOLD, or ESCALATE | [README](autonomy_gatekeeper/README.md) |
