.PHONY: setup install dev lint test clean doctor run-example help

# Default target
help:
	@echo "Board of Directors Agents - AI Advisory System"
	@echo ""
	@echo "Available commands:"
	@echo "  setup       - Install package and dependencies"
	@echo "  dev         - Install with development dependencies"
	@echo "  lint        - Run code formatting and linting"
	@echo "  test        - Run test suite"
	@echo "  doctor      - Check Ollama connection and models"
	@echo "  run-example - Run example critique"
	@echo "  clean       - Clean build artifacts"

setup:
	pip install -e .
	@echo "✅ Setup complete! Try: board doctor"

dev:
	pip install -e ".[dev]"
	pre-commit install
	@echo "✅ Development setup complete!"

lint:
	black src/ tests/
	ruff check src/ tests/ --fix
	mypy src/

test:
	pytest tests/ -v --cov=board --cov-report=term-missing

doctor:
	board doctor

run-example:
	board critique --input examples/idea.md --output examples/output.md
	@echo "✅ Example complete! Check examples/output.md"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
