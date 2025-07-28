# Environment variables
SHELL := /bin/bash
.DEFAULT_GOAL := help

define format_py_version
$(shell echo "py$(subst .,,$(1))")
endef

# PYTHON
PYTHON_VERSION := $(shell cat .python-version)

# PROJECT
CONFIG_FILE = ./pyproject.toml
SOURCE_DIR 	= ./commons
SCRIPTS_DIR = ./scripts
TEST_DIR 	= ./tests
DOCS_DIR 	= ./docs

# TOOLS
RUFF = uv tool run ruff --config $(CONFIG_FILE)
RUFF_ARGS = --target-version $(call format_py_version,$(PYTHON_VERSION)) -n

.PHONY: help check clean format install

help:
	@echo ""
	@echo "Commons module commands"
	@echo "Using python: $(call format_py_version,$(PYTHON_VERSION))"
	@echo ""
	@echo "Development:"
	@echo "  make install      : Clean install of dependencies"
	@echo "  make format       : Format code using Ruff"
	@echo "  make lint         : Run linters"
	@echo "  make test         : Run tests with coverage"
	@echo "  make check        : Run format, lint, and test"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs         : Generate documentation"
	@echo ""
	@echo "Deployment:"
	@echo "  make clean        : Remove build artifacts"
	@echo "  make version      : Update version and changelog"
	@echo "  make build        : Build package"
	@echo ""

changelog-generate:
	@echo ""
	@echo "Generating changelog..."
	uv tool run git-cliff -o -v  --github-repo TheAldersonProject/commons --github-token ${GITHUB-TOKEN-COMMONS}
	@echo ""
	@echo "... changelog generation finalized. check CHANGELOG.md!"

check: clean format check-lint

check-lint:
	@echo ""
	@echo "Starting ruff check..."
	@echo ""
	${RUFF}  check ${SOURCE_DIR} ${SCRIPTS_DIR} ${TEST_DIR} ${DOCS_DIR}  ${RUFF_ARGS} --fix
	@echo ""
	@echo "...ending ruff check!"
	@echo ""

clean:
	@echo ""
	@echo "Cleaning project..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache build dist *.egg-info .coverage coverage.xml
	@echo ""

format:
	@echo ""
	@echo "Starting ruff check..."
	@echo ""
	${RUFF} format ${SOURCE_DIR} ${SCRIPTS_DIR} ${TEST_DIR} ${DOCS_DIR} ${RUFF_ARGS}
	@echo ""
	@echo "...ending ruff check!"
	@echo ""

install: clean
	@echo ""
	@echo "Install dependencies using UV..."
	@echo ""
	uv sync --link-mode=copy
	@echo ""
	@echo "...ending install dependencies!"
	@echo ""

install-uv-tools:
	@echo ""
	@echo "Install  UV tools..."
	@echo ""
	uv tool install black
	uv tool install git-cliff
	uv tool install ruff
	@echo ""
	@echo "...ending install uv tools!"
	@echo ""

install-all: install-uv-tools install

test:
	@echo ""
	@echo "Running unit tests..."
	@echo ""
	uv run pytest -v -s --log-level=DEBUG --color=auto --code-highlight=yes --cov
	@echo ""
	@echo "...ending unit tests!"
	@echo ""
