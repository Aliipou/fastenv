.PHONY: dev test lint typecheck install build clean

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=fastenv --cov-report=term-missing

lint:
	ruff check . --fix && ruff format .

typecheck:
	mypy fastenv/ --ignore-missing-imports

build:
	python -m build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf dist/ build/ .pytest_cache/ coverage.xml
