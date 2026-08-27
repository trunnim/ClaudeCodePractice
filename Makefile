# Run `make` with no arguments to see what is available.
.DEFAULT_GOAL := help
.PHONY: help check docs test progress

help: ## Show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

check: docs test ## Run every check. Run this before you commit.

docs: ## Validate documentation, memory files, skills and lesson ordering
	@python3 tools/check_docs.py

test: ## Run the validator's own unit tests
	@python3 -m unittest discover -s tools/tests -q

progress: ## Show which lesson exercises you have completed
	@python3 tools/progress.py
