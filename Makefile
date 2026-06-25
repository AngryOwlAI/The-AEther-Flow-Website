SHELL := /bin/bash

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: install dev build preview test lint validate quality clean docker-build docker-dev docker-preview

install:
	npm install
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements-dev.txt

dev:
	npm run dev

build:
	npm run build

preview:
	npm run preview

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy scripts tests

validate:
	$(PYTHON) scripts/validate_assets.py
	$(PYTHON) scripts/validate_content_sources.py
	$(PYTHON) scripts/validate_cloudflare_pages_config.py
	npm run build

quality: validate test lint
	$(PYTHON) scripts/quality_gate.py

clean:
	rm -rf dist .astro .pytest_cache .mypy_cache .ruff_cache htmlcov

docker-build:
	docker build -t aether-flow-website:local .

docker-dev:
	docker compose up --build

docker-preview:
	docker run --rm -p 8080:80 aether-flow-website:local
