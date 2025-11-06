.PHONY: help install install-dev test lint format clean data notebooks run-pipeline

# Default target
help:
	@echo "Available targets:"
	@echo "  install       - Install project dependencies"
	@echo "  install-dev   - Install development dependencies"
	@echo "  test          - Run test suite"
	@echo "  test-cov      - Run tests with coverage report"
	@echo "  lint          - Run code linters (flake8, pylint)"
	@echo "  format        - Format code with black"
	@echo "  type-check    - Run mypy type checker"
	@echo "  clean         - Remove build artifacts and cache"
	@echo "  clean-data    - Remove processed data files"
	@echo "  notebooks     - Start Jupyter notebook server"
	@echo "  run-pipeline  - Execute full data pipeline"

# Installation
install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

# Code Quality
lint:
	flake8 src/ tests/
	pylint src/ tests/

format:
	black src/ tests/ notebooks/

type-check:
	mypy src/

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -f .coverage

clean-data:
	rm -rf data/processed/*
	rm -rf data/integrated/*
	@echo "Raw data preserved. Processed and integrated data removed."

# Development
notebooks:
	jupyter notebook notebooks/

# Pipeline Execution
run-pipeline:
	python -m src.main
