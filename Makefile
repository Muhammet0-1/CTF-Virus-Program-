PYTHON ?= python3

.PHONY: bootstrap format format-check lint typecheck test compile clean-build build package-check smoke verify clean

bootstrap:
	$(PYTHON) -m pip install -e '.[dev]'

format:
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix .

format-check:
	$(PYTHON) -m ruff format --check .

lint:
	$(PYTHON) -m ruff check .

typecheck:
	$(PYTHON) -m mypy

test:
	$(PYTHON) -m pytest

compile:
	$(PYTHON) -m compileall -q src tests tools agent.py

clean-build:
	rm -rf build dist
	find . -type d -name '*.egg-info' -prune -exec rm -rf {} +

build:
	PIP_NO_INDEX=1 $(PYTHON) -m build --no-isolation

package-check:
	$(PYTHON) tools/verify_artifacts.py

smoke:
	PYTHONPATH=src $(PYTHON) -m ctf_malware_lab --version
	PYTHONPATH=src $(PYTHON) -m ctf_malware_lab self-test
	PYTHONPATH=src $(PYTHON) -m ctf_malware_lab catalog >/dev/null

verify: format-check lint typecheck test compile clean-build build package-check smoke

clean: clean-build
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

