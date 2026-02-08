.PHONY: setup lint typecheck test run docker-build docker-run

setup:
	pip install -e ".[dev]"
	pre-commit install

lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

typecheck:
	mypy src/

test:
	pytest tests/ -v --tb=short

run:
	autonomy-gatekeeper evaluate --request "Deploy model v2.3 to production"

docker-build:
	docker build -t autonomy-gatekeeper:latest .

docker-run:
	docker run --rm --env-file .env autonomy-gatekeeper evaluate --request "Deploy model v2.3 to production"
