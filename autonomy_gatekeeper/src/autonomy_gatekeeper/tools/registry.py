"""Tool registry — manages available tools for the governance agent.

In this governance agent, tools are intentionally minimal. The agent's
primary function is evaluation, not execution. This registry exists as
a pattern for extending the agent with action capabilities when needed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class Tool(Protocol):
    """Protocol for a callable tool."""

    name: str
    description: str

    def __call__(self, **kwargs: Any) -> Any: ...


@dataclass
class ToolRegistry:
    """Registry of tools available to the agent."""

    _tools: dict[str, Tool] = field(default_factory=dict)

    def register(self, tool: Tool) -> None:
        """Register a tool by name."""
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        """Retrieve a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
