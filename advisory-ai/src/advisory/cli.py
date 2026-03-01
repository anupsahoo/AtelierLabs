"""Command-line interface for Advisory AI."""

import json
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from advisory.agents.base import AgentOutput
from advisory.agents.jobs import JobsAgent
from advisory.agents.naval import NavalAgent
from advisory.agents.munger import MungerAgent
from advisory.agents.indian_philosophy import IndianPhilosophyAgent
from advisory.agents.ruthless_capitalist import RuthlessCapitalistAgent
from advisory.agents.synthesis import SynthesisAgent
from advisory.runtime.providers import get_provider

app = typer.Typer(
    name="board",
    help="AI Board of Directors - Get world-class feedback on your ideas",
    no_args_is_help=True,
)
console = Console()

AVAILABLE_LENSES = {
    "jobs": JobsAgent,
    "naval": NavalAgent,
    "munger": MungerAgent,
    "indian": IndianPhilosophyAgent,
    "capitalist": RuthlessCapitalistAgent,
}


@app.command()
def doctor() -> None:
    """Check system health and model availability."""
    console.print("[bold blue]Advisory AI - System Check[/bold blue]")
    console.print()
    
    try:
        provider = get_provider()
        console.print("✅ Provider initialized successfully")
        
        # Test model availability
        test_response = provider.generate("Test message", max_tokens=10)
        if test_response:
            console.print("✅ Model responding correctly")
        else:
            console.print("❌ Model not responding")
            return
            
    except Exception as e:
        console.print(f"❌ Provider error: {e}")
        console.print("\n[yellow]Troubleshooting:[/yellow]")
        console.print("1. Ensure Ollama is running: `ollama serve`")
        console.print("2. Pull required model: `ollama pull llama2`")
        console.print("3. Or set OPENAI_API_KEY environment variable")
        return
    
    console.print("\n[green]✅ All systems operational![/green]")
    console.print("Ready to provide world-class feedback on your ideas.")


@app.command()
def critique(
    input_file: Path = typer.Option(..., "--input", "-i", help="Input idea file (markdown)"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    lens: Optional[str] = typer.Option(None, "--lens", "-l", help="Single lens to use (jobs, naval, munger, indian, capitalist)"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    interactive: bool = typer.Option(False, "--interactive", help="Enable interactive mode with clarifying questions"),
) -> None:
    """Get critique from AI advisory of directors."""
    
    # Validate input file
    if not input_file.exists():
        console.print(f"❌ Input file not found: {input_file}")
        raise typer.Exit(1)
    
    # Read input content
    try:
        content = input_file.read_text(encoding="utf-8")
    except Exception as e:
        console.print(f"❌ Error reading input file: {e}")
        raise typer.Exit(1)
    
    # Initialize provider
    try:
        provider = get_provider()
    except Exception as e:
        console.print(f"❌ Provider initialization failed: {e}")
        console.print("Run `advisory doctor` to diagnose issues.")
        raise typer.Exit(1)
    
    console.print("[bold blue]Advisory AI[/bold blue]")
    console.print(f"Analyzing: {input_file.name}")
    console.print()
    
    results = []
    
    if lens:
        # Single lens mode
        if lens not in AVAILABLE_LENSES:
            console.print(f"❌ Unknown lens: {lens}")
            console.print(f"Available lenses: {', '.join(AVAILABLE_LENSES.keys())}")
            raise typer.Exit(1)
        
        agent_class = AVAILABLE_LENSES[lens]
        agent = agent_class(provider)
        
        with console.status(f"[bold green]Getting {lens} perspective..."):
            result = agent.critique(content, interactive=interactive)
            results.append(result)
    
    else:
        # Full advisory mode
        agents = [
            ("Jobs", JobsAgent(provider)),
            ("Naval", NavalAgent(provider)),
            ("Munger", MungerAgent(provider)),
            ("Indian Philosophy", IndianPhilosophyAgent(provider)),
            ("Ruthless Capitalist", RuthlessCapitalistAgent(provider)),
        ]
        
        # Get individual critiques
        for name, agent in agents:
            with console.status(f"[bold green]Getting {name} perspective..."):
                result = agent.critique(content, interactive=interactive)
                results.append(result)
        
        # Synthesis
        with console.status("[bold green]Synthesizing advisory feedback..."):
            synthesis_agent = SynthesisAgent(provider)
            synthesis_result = synthesis_agent.synthesize(content, results)
            results.append(synthesis_result)
    
    # Output results
    if json_output:
        output_data = {
            "input_file": str(input_file),
            "critiques": [result.model_dump() for result in results]
        }
        
        if output_file:
            output_file.write_text(json.dumps(output_data, indent=2))
            console.print(f"✅ JSON output saved to: {output_file}")
        else:
            console.print(json.dumps(output_data, indent=2))
    
    else:
        # Markdown output
        markdown_content = _format_markdown_output(results, input_file.name)
        
        if output_file:
            output_file.write_text(markdown_content)
            console.print(f"✅ Critique saved to: {output_file}")
        else:
            console.print(markdown_content)


def _format_markdown_output(results: list[AgentOutput], input_name: str) -> str:
    """Format results as markdown."""
    lines = [
        f"# Board Critique: {input_name}",
        "",
        f"*Generated by Advisory AI*",
        "",
    ]
    
    for result in results:
        lines.extend([
            f"## {result.agent_name}",
            "",
            f"**{result.brutal_line}**",
            "",
        ])
        
        if result.key_questions:
            lines.extend([
                "### Key Questions",
                "",
            ])
            for i, question in enumerate(result.key_questions, 1):
                lines.append(f"{i}. {question}")
            lines.append("")
        
        if result.assumptions:
            lines.extend([
                "### Assumptions Analysis",
                "",
            ])
            for assumption in result.assumptions:
                lines.append(f"- {assumption}")
            lines.append("")
        
        if result.risks:
            lines.extend([
                "### Risk Assessment",
                "",
            ])
            for risk in result.risks:
                lines.append(f"- {risk}")
            lines.append("")
        
        if result.bold_move:
            lines.extend([
                "### Bold Move",
                "",
                result.bold_move,
                "",
            ])
        
        if result.scorecard:
            lines.extend([
                "### Scorecard",
                "",
            ])
            for metric, score in result.scorecard.items():
                lines.append(f"- **{metric}**: {score}/10")
            lines.append("")
        
        if result.experiment_plan:
            lines.extend([
                "### 30-Day Experiment",
                "",
                f"**Hypothesis**: {result.experiment_plan.get('hypothesis', 'N/A')}",
                "",
                f"**Success Metrics**: {result.experiment_plan.get('success_metrics', 'N/A')}",
                "",
                f"**Action Steps**: {result.experiment_plan.get('action_steps', 'N/A')}",
                "",
            ])
        
        if result.references:
            lines.extend([
                "### References",
                "",
            ])
            for ref in result.references:
                lines.append(f"- [{ref['title']}]({ref['url']})")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


@app.command()
def version() -> None:
    """Show version information."""
    from advisory import __version__
    console.print(f"Advisory AI v{__version__}")


if __name__ == "__main__":
    app()
