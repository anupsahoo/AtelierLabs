"""Tests for blog reference matching."""

import tempfile
from pathlib import Path

import pytest
import yaml

from board.retrieval.blog_refs import (
    load_blog_index,
    get_references_by_tags,
    get_all_tags
)


@pytest.fixture
def sample_blog_index():
    """Create a temporary blog index file for testing."""
    blog_data = [
        {
            "title": "First Principles Thinking",
            "url": "https://example.com/first-principles",
            "tags": ["first-principles", "thinking", "strategy"]
        },
        {
            "title": "Leverage and Wealth",
            "url": "https://example.com/leverage",
            "tags": ["leverage", "wealth", "scalability"]
        },
        {
            "title": "Mental Models Guide",
            "url": "https://example.com/mental-models",
            "tags": ["mental-models", "thinking", "decision-making"]
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(blog_data, f)
        f.flush()
        yield Path(f.name)
    
    # Cleanup
    Path(f.name).unlink()


def test_load_blog_index_success(sample_blog_index):
    """Test successful loading of blog index."""
    result = load_blog_index(str(sample_blog_index))
    
    assert len(result) == 3
    assert result[0]["title"] == "First Principles Thinking"
    assert "first-principles" in result[0]["tags"]


def test_load_blog_index_missing_file():
    """Test loading non-existent blog index file."""
    result = load_blog_index("nonexistent.yml")
    
    assert result == []


def test_get_references_by_tags(sample_blog_index):
    """Test getting references by tag matching."""
    # Mock the load function to use our test file
    import board.retrieval.blog_refs
    original_load = board.retrieval.blog_refs.load_blog_index
    board.retrieval.blog_refs.load_blog_index = lambda: load_blog_index(str(sample_blog_index))
    
    try:
        # Test single tag match
        results = get_references_by_tags(["thinking"])
        assert len(results) == 2
        assert any("First Principles" in r["title"] for r in results)
        assert any("Mental Models" in r["title"] for r in results)
        
        # Test multiple tag match
        results = get_references_by_tags(["leverage", "wealth"])
        assert len(results) == 1
        assert "Leverage and Wealth" in results[0]["title"]
        
        # Test no matches
        results = get_references_by_tags(["nonexistent"])
        assert len(results) == 0
        
    finally:
        # Restore original function
        board.retrieval.blog_refs.load_blog_index = original_load


def test_get_all_tags(sample_blog_index):
    """Test getting all unique tags."""
    # Mock the load function
    import board.retrieval.blog_refs
    original_load = board.retrieval.blog_refs.load_blog_index
    board.retrieval.blog_refs.load_blog_index = lambda: load_blog_index(str(sample_blog_index))
    
    try:
        tags = get_all_tags()
        
        expected_tags = [
            "decision-making", "first-principles", "leverage", 
            "mental-models", "scalability", "strategy", "thinking", "wealth"
        ]
        
        assert sorted(tags) == expected_tags
        
    finally:
        # Restore original function
        board.retrieval.blog_refs.load_blog_index = original_load


def test_get_references_case_insensitive(sample_blog_index):
    """Test that tag matching is case insensitive."""
    import board.retrieval.blog_refs
    original_load = board.retrieval.blog_refs.load_blog_index
    board.retrieval.blog_refs.load_blog_index = lambda: load_blog_index(str(sample_blog_index))
    
    try:
        # Test case insensitive matching
        results_lower = get_references_by_tags(["thinking"])
        results_upper = get_references_by_tags(["THINKING"])
        results_mixed = get_references_by_tags(["Thinking"])
        
        assert len(results_lower) == len(results_upper) == len(results_mixed)
        assert results_lower == results_upper == results_mixed
        
    finally:
        board.retrieval.blog_refs.load_blog_index = original_load
