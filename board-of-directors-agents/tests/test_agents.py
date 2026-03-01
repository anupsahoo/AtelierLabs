"""Tests for agent functionality."""

from unittest.mock import Mock

import pytest

from board.agents.base import AgentOutput
from board.agents.jobs import JobsAgent
from board.agents.naval import NavalAgent
from board.agents.munger import MungerAgent
from board.agents.synthesis import SynthesisAgent


@pytest.fixture
def mock_provider():
    """Mock AI provider for testing."""
    provider = Mock()
    provider.generate.return_value = """
    BRUTAL TRUTH: This is a test critique
    
    KEY QUESTIONS:
    - What's the real problem?
    - How do you validate this?
    
    ASSUMPTIONS:
    - ASSUMPTION: Users want this feature
    - FACT: Market exists for this solution
    
    RISKS:
    - Market rejection risk
    - Technical implementation risk
    
    BOLD MOVE: Pivot to simpler solution
    
    SCORECARD:
    - Simplicity: 7/10
    - User Focus: 8/10
    """
    return provider


def test_jobs_agent_critique(mock_provider):
    """Test Jobs agent critique functionality."""
    agent = JobsAgent(mock_provider)
    
    result = agent.critique("Test business idea content")
    
    assert isinstance(result, AgentOutput)
    assert result.agent_name == "Jobs Lens: Ruthless Simplicity"
    assert result.brutal_line
    assert len(result.key_questions) > 0
    assert len(result.assumptions) > 0
    assert len(result.risks) > 0
    assert result.bold_move
    assert len(result.scorecard) > 0


def test_naval_agent_critique(mock_provider):
    """Test Naval agent critique functionality."""
    agent = NavalAgent(mock_provider)
    
    result = agent.critique("Test business idea content")
    
    assert isinstance(result, AgentOutput)
    assert result.agent_name == "Naval Lens: Leverage & Wealth Creation"
    assert result.brutal_line
    assert len(result.key_questions) > 0


def test_munger_agent_critique(mock_provider):
    """Test Munger agent critique functionality."""
    agent = MungerAgent(mock_provider)
    
    result = agent.critique("Test business idea content")
    
    assert isinstance(result, AgentOutput)
    assert result.agent_name == "Munger Lens: Mental Models & Inversion"
    assert result.brutal_line


def test_synthesis_agent_synthesize(mock_provider):
    """Test Synthesis agent functionality."""
    # Create mock critiques
    critique1 = AgentOutput(
        agent_name="Jobs Lens",
        brutal_line="Too complex",
        key_questions=["What to cut?"],
        assumptions=["Users want simplicity"],
        risks=["Feature creep"],
        bold_move="Remove 80% of features",
        scorecard={"Simplicity": 3},
        experiment_plan={"hypothesis": "Simple is better"},
        references=[]
    )
    
    critique2 = AgentOutput(
        agent_name="Naval Lens", 
        brutal_line="No leverage",
        key_questions=["Where's the scale?"],
        assumptions=["Manual work required"],
        risks=["No scalability"],
        bold_move="Find automation angle",
        scorecard={"Leverage": 2},
        experiment_plan={"hypothesis": "Need automation"},
        references=[]
    )
    
    agent = SynthesisAgent(mock_provider)
    
    result = agent.synthesize("Test content", [critique1, critique2])
    
    assert isinstance(result, AgentOutput)
    assert result.agent_name == "Board Synthesis: Unified Action Plan"
    assert result.brutal_line
    assert len(result.key_questions) > 0


def test_agent_output_validation():
    """Test AgentOutput model validation."""
    # Valid output
    output = AgentOutput(
        agent_name="Test Agent",
        brutal_line="Test critique",
        key_questions=["Question 1", "Question 2"],
        assumptions=["Assumption 1"],
        risks=["Risk 1"],
        bold_move="Bold action",
        scorecard={"Metric": 5},
        experiment_plan={"hypothesis": "Test hypothesis"},
        references=[{"title": "Test", "url": "http://test.com"}]
    )
    
    assert output.agent_name == "Test Agent"
    assert len(output.key_questions) == 2
    assert output.scorecard["Metric"] == 5


def test_agent_blog_references(mock_provider):
    """Test agent blog reference integration."""
    with pytest.mock.patch('board.agents.base.get_references_by_tags') as mock_refs:
        mock_refs.return_value = [
            {"title": "Test Article", "url": "http://test.com", "tags": ["test"]}
        ]
        
        agent = JobsAgent(mock_provider)
        result = agent.critique("Test content")
        
        assert len(result.references) > 0
        mock_refs.assert_called_once()
