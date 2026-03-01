"""Blog reference matching system."""

import os
from pathlib import Path
from typing import Dict, List

import yaml


def load_blog_index(file_path: str = None) -> List[Dict[str, any]]:
    """Load blog index from YAML file."""
    if file_path is None:
        # Default path
        file_path = os.getenv("BLOG_INDEX_PATH", "resources/blog_index.yml")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or []
    except FileNotFoundError:
        # Return empty list if file doesn't exist
        return []
    except Exception as e:
        print(f"Warning: Could not load blog index: {e}")
        return []


def get_references_by_tags(tags: List[str], max_results: int = 5) -> List[Dict[str, str]]:
    """Get blog references that match the given tags."""
    blog_index = load_blog_index()
    
    if not blog_index:
        return []
    
    # Score each article by tag matches
    scored_articles = []
    
    for article in blog_index:
        article_tags = article.get('tags', [])
        if not article_tags:
            continue
        
        # Calculate match score
        matches = sum(1 for tag in tags if tag.lower() in [t.lower() for t in article_tags])
        
        if matches > 0:
            scored_articles.append({
                'score': matches,
                'article': {
                    'title': article.get('title', 'Untitled'),
                    'url': article.get('url', ''),
                    'tags': article_tags
                }
            })
    
    # Sort by score (descending) and return top results
    scored_articles.sort(key=lambda x: x['score'], reverse=True)
    
    return [item['article'] for item in scored_articles[:max_results]]


def get_all_tags() -> List[str]:
    """Get all unique tags from the blog index."""
    blog_index = load_blog_index()
    
    all_tags = set()
    for article in blog_index:
        tags = article.get('tags', [])
        all_tags.update(tag.lower() for tag in tags)
    
    return sorted(list(all_tags))
