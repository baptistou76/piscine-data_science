.PHONY: install clean re

VENV = .venv
PYTHON = python3
PIP = $(VENV)/bin/pip

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install pandas
	$(PIP) install matplotlib
	$(PIP) install psycopg2-binary
	$(PIP) install scikit-learn

clean:
	@rm -rf $(VENV)
	@rm -rf __pycache__
	@rm -rf *.pyc
	@rm -rf .pytest_cache
	@rm -rf build dist *.egg-info

re: clean install