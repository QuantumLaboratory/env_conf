PACKAGE_NAME := env_conf
CHECKER := mypy
LINTER := pylint
TESTER := pytest
TEST_ARGS ?= --cov $(PACKAGE_NAME)

.PHONY: clean lint check check-all

clean:
	@find $(CURDIR) -name '*.pyc' -delete
	@find $(CURDIR) -name '__pycache__' -delete
	@find $(CURDIR) -name '.coverage' -delete

lint:
	@$(LINTER) $(PACKAGE_NAME)
	@$(LINTER) tests

check:
	@$(CHECKER) $(PACKAGE_NAME)

check-all: lint check

test:
	@$(TESTER) tests $(TEST_ARGS)
