PYTHON=python3.8

ENV_DIR=.env_$(PYTHON)
IN_ENV=. $(ENV_DIR)/bin/activate &&
TEST_CONTEXT=export TEST_ENV=True &&

env: $(ENV_DIR)

assert_clean:
	@status=$$(git status --porcelain); \
	if test "x$${status}" != x; then \
			echo "Working directory is dirty" >&2; \
			exit 1; \
	fi

upload_pip: assert_clean test build_dist 
	twine upload --repository pypi dist/*

build:
	$(IN_ENV) $(PYTHON) -m pip install --editable .
	rm -fr dist/
	$(IN_ENV) $(PYTHON) setup.py sdist bdist_wheel

build_dist:
	rm -fr dist/
	$(IN_ENV) python setup.py sdist

setup:
	$(PYTHON) -m pip install --upgrade virtualenv
	$(PYTHON) -m virtualenv -p $(PYTHON) $(ENV_DIR)
	$(IN_ENV) $(PYTHON) -m pip install --upgrade -r requirements.txt
	$(IN_ENV) $(PYTHON) -m pip install --editable .

test_requirements:
	$(IN_ENV) python -m pip install --upgrade -r test_requirements.txt

requirements:
	$(IN_ENV) $(PYTHON) -m pip install --upgrade -r requirements.txt

test: setup build test_requirements quick_test
	@echo "Make some tests!"

quick_test:
	@echo "Make some tests!"
	# $(IN_ENV) $(TEST_CONTEXT) python `which nosetests` -q -s tests/ --with-coverage --cover-erase --cover-package=src
	# $(IN_ENV) coverage report -m
