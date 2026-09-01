.PHONY: help install dev test lint format clean

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make install-dev   - Install dev dependencies"
	@echo "  make dev          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Remove cache files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

dev:
	python -m uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

test-cov:
	pytest --cov=src --cov-report=html

lint:
	flake8 src tests
	mypy src
	pylint src

format:
	black src tests
	isort src tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov
