# Environment variables
SHELL := /bin/bash
.DEFAULT_GOAL := help

define format_py_version
$(shell echo "py$(subst .,,$(1))")
endef

# PYTHON
PYTHON_VERSION := $(shell cat .python-version)

# PROJECT

# Define or receive the project root folder
PROJECT_ROOT= $(PWD)

# Define or receive folders and config files of the project
CONFIG_FILE 			= ${PROJECT_ROOT}/pyproject.toml
DOCS_DIR 				= ${PROJECT_ROOT}/docs
SCRIPTS_DIR 			= ${PROJECT_ROOT}/scripts
SOURCE_DIR_FOLDER_NAME	= commons
SOURCE_DIR 				= ${PROJECT_ROOT}/${SOURCE_DIR_FOLDER_NAME}
TEST_DIR 				= ${PROJECT_ROOT}/tests
VENV_DIR  				= ${PROJECT_ROOT}/.venv

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
	@make print-header
	@echo "Generating changelog..."
	uv tool run git-cliff -o -v  --github-repo TheAldersonProject/commons --github-token ${GITHUB_TOKEN_COMMONS}
	@echo ""
	@echo "... changelog generation finalized. check CHANGELOG.md!"
	make print-footer

check: clean format lint

.ONESHELL:
clean:
	@make print-header
	@echo "Cleaning project..."
	@cd ${PROJECT_ROOT}
	@echo "Working dir: $(PWD)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache build dist *.egg-info .coverage coverage.xml
	@make print-footer

.ONESHELL:
dev-config:
	@make print-header
	@echo "Configuring environment..."
	@echo "### Install UV"
	@echo "### Install UV tools"
	@make install-uv-tools
	@echo "### Install Python"
	@make install-python
	@echo "### Configure virtual environment"
	@uv venv .venv --allow-existing --trusted-host localhost --color auto --python python${PYTHON_VERSION}
	@source .venv/bin/activate
	@echo "Python version installed: $(python --version)"
	@echo "### Install project dependencies"
	@make install
	@echo ""
	@echo "...DEV environment configured!"
	@make print-footer

format:
	@make print-header
	@echo "Starting ruff check..."
	@echo ""
	${RUFF} format ${SOURCE_DIR} ${SCRIPTS_DIR} ${TEST_DIR} ${DOCS_DIR} ${RUFF_ARGS}
	@echo ""
	@echo "...ending ruff check!"
	@make print-footer

install: clean
	@make print-header
	@echo "Install dependencies using UV..."
	@echo ""
	@uv sync --link-mode=copy
	@echo ""
	@echo "...ending install dependencies!"
	@make print-footer

install-all: install-uv-tools install

install-python:
	@uv python install python${PYTHON_VERSION}

install-uv:
	@make print-header
	@echo "Installing UV..."
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "...UV installed."
	@make print-footer

install-uv-tools:
	@make print-header
	@echo "Install  UV tools..."
	@echo ""
	@uv tool install black
	@uv tool install git-cliff
	@uv tool install ruff
	@echo ""
	@echo "...ending install uv tools!"
	@make print-footer

lint:
	make print-header
	@echo "Starting ruff check..."
	@echo ""
	@echo "SRC :: ${SOURCE_DIR}"
	${RUFF} check ${SOURCE_DIR} ${SCRIPTS_DIR} ${TEST_DIR} ${DOCS_DIR}  ${RUFF_ARGS} -v --fix
	@echo ""
	@echo "...ending ruff check!"
	make print-footer

print-header:
	@echo ""
	@echo "Starting..."
	@echo "------------------------------------------------------------------"
	@echo ""

print-footer:
	@echo ""
	@echo "... and done!"
	@echo "=================================================================="
	@echo ""

test:
	@make print-header
	@echo "Running unit tests..."
	@echo ""
	@uv run pytest -v -s --log-level=DEBUG --color=auto --code-highlight=yes --cov --cov-report=xml
	@echo ""
	@echo "...ending unit tests!"
	@make print-footer
