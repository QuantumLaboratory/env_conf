PACKAGE_NAME := env_conf
CHECKER := mypy
LINTER := pylint
TESTER := pytest
TEST_ARGS ?=

.PHONY: clean lint check check-all test isort check-import

clean:
	@find $(CURDIR) -name '*.pyc' -delete
	@find $(CURDIR) -name '__pycache__' -delete
	@find $(CURDIR) -name '.coverage' -delete
	@rm -rf htmlcov
	@rm -rf dist
	@rm -rf build
	@rm -rf env.conf.egg-info

build:
	@python setup.py bdist_wheel

lint:
	@$(LINTER) $(PACKAGE_NAME)
	@$(LINTER) tests

check:
	@$(CHECKER) --ignore-missing-imports --strict-optional $(PACKAGE_NAME)

check-all: lint check check-import

test:
	@$(TESTER) tests $(TEST_ARGS)

isort:
	@isort -y -rc $(PACKAGE_NAME) tests

check-import:
	@isort -c -rc $(PACKAGE_NAME) tests
