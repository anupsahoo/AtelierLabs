"""Tests for CLI functionality."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from board.cli import app


@pytest.fixture
def runner():
    """CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_idea_file():
    """Create a temporary idea file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Test Idea
        
This is a test business idea for the board to critique.
It involves building a revolutionary new product that will change the world.
        """)
        f.flush()
        yield Path(f.name)
    
    # Cleanup
    Path(f.name).unlink()


def test_doctor_command_success(runner):
    """Test doctor command with successful provider."""
    with patch('board.cli.get_provider') as mock_provider:
        mock_provider.return_value.generate.return_value = "Test response"
        
        result = runner.invoke(app, ["doctor"])
        
        assert result.exit_code == 0
        assert "All systems operational" in result.stdout


def test_doctor_command_failure(runner):
    """Test doctor command with failed provider."""
    with patch('board.cli.get_provider') as mock_provider:
        mock_provider.side_effect = Exception("Connection failed")
        
        result = runner.invoke(app, ["doctor"])
        
        assert result.exit_code == 0
        assert "Provider error" in result.stdout


def test_critique_single_lens(runner, sample_idea_file):
    """Test critique command with single lens."""
    with patch('board.cli.get_provider') as mock_provider:
        mock_provider.return_value.generate.return_value = """
        BRUTAL TRUTH: This is a test critique
        KEY QUESTIONS:
        - What's the real problem?
        - How do you validate this?
        ASSUMPTIONS:
        - ASSUMPTION: Users want this
        RISKS:
        - Market rejection
        BOLD MOVE: Pivot immediately
        SCORECARD:
        - Simplicity: 5/10
        """
        
        result = runner.invoke(app, [
            "critique", 
            "--input", str(sample_idea_file),
            "--lens", "jobs"
        ])
        
        assert result.exit_code == 0
        assert "Jobs Lens" in result.stdout


def test_critique_json_output(runner, sample_idea_file):
    """Test critique command with JSON output."""
    with patch('board.cli.get_provider') as mock_provider:
        mock_provider.return_value.generate.return_value = """
        BRUTAL TRUTH: This is a test critique
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as output_file:
            result = runner.invoke(app, [
                "critique",
                "--input", str(sample_idea_file),
                "--lens", "jobs", 
                "--json",
                "--output", output_file.name
            ])
            
            assert result.exit_code == 0
            
            # Check JSON output was created
            output_path = Path(output_file.name)
            assert output_path.exists()
            
            # Validate JSON structure
            with open(output_path) as f:
                data = json.load(f)
                assert "input_file" in data
                assert "critiques" in data
            
            # Cleanup
            output_path.unlink()


def test_critique_invalid_lens(runner, sample_idea_file):
    """Test critique command with invalid lens."""
    result = runner.invoke(app, [
        "critique",
        "--input", str(sample_idea_file),
        "--lens", "invalid"
    ])
    
    assert result.exit_code == 1
    assert "Unknown lens" in result.stdout


def test_critique_missing_input_file(runner):
    """Test critique command with missing input file."""
    result = runner.invoke(app, [
        "critique",
        "--input", "nonexistent.md"
    ])
    
    assert result.exit_code == 1
    assert "Input file not found" in result.stdout


def test_version_command(runner):
    """Test version command."""
    result = runner.invoke(app, ["version"])
    
    assert result.exit_code == 0
    assert "Board of Directors Agents" in result.stdout
