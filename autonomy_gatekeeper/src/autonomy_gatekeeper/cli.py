"""CLI entrypoint for the Autonomy Gatekeeper."""

from __future__ import annotations

import click
from rich.console import Console

from autonomy_gatekeeper.app import evaluate_request, format_output
from autonomy_gatekeeper.config import load_settings

console = Console()


@click.group()
@click.version_option(package_name="autonomy-gatekeeper")
def main() -> None:
    """Autonomy Gatekeeper — AI governance agent for decision control."""


@main.command()
@click.option(
    "--request",
    "-r",
    required=True,
    help="The request text to evaluate.",
)
@click.option(
    "--json-output",
    is_flag=True,
    default=False,
    help="Output the Decision Card as JSON.",
)
@click.option(
    "--policy",
    "-p",
    default=None,
    help="Path to a custom policy rules YAML file.",
)
def evaluate(request: str, json_output: bool, policy: str | None) -> None:
    """Evaluate a request and produce a Decision Card."""
    settings = load_settings()
    if policy:
        settings.policy_path = policy

    try:
        card = evaluate_request(request, settings=settings)
        output = format_output(card, output_json=json_output)
        console.print(output)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
