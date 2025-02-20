install: ## Install the poetry environment and install the pre-commit hooks.
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@poetry run pre-commit install
	@poetry shell

basic_example: ## Run the basic example
	@echo "🚀 Running basic ChirpStack operations example"
	@poetry run python examples/basic.py

integration_example: ## Run the integration example
	@echo "🚀 Running ChirpStack integration example"
	@poetry run python examples/integration.py

fuota_example: ## Run the FUOTA example
	@echo "🚀 Running ChirpStack FUOTA example"
	@poetry run python examples/fuota.py

run_all_examples: basic_example integration_example fuota_example ## Run all examples

check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a

clean: ## clean dev tools cache.
	@rm -rf .ruff_cache .pytest_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install basic_example integration_example fuota_example run_all_examples check clean help

.DEFAULT_GOAL := help

# Suppress Entering/Leaving print output from make.
MAKEFLAGS += --no-print-directory
