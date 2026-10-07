PYTHON ?= python3
export PYTHON

.PHONY: help test smoke validate install uninstall package clean

help:
	@echo "make test       run the unit tests"
	@echo "make smoke      end-to-end CLI run in a temp dir"
	@echo "make validate   JSON/schema checks + smoke run"
	@echo "make install    symlink the skill into ~/.claude/skills (PROJECT=<path> for a project)"
	@echo "make uninstall  remove that symlink"
	@echo "make package    zip skill/memory-bank into dist/"
	@echo "make clean      remove dist/ and caches"

test:
	$(PYTHON) -m unittest discover -s tests -v

smoke:
	bash scripts/smoke.sh

validate:
	$(PYTHON) scripts/check_schema.py
	bash scripts/smoke.sh

install:
	bash scripts/install.sh $(if $(PROJECT),--project "$(PROJECT)")

uninstall:
	bash scripts/install.sh --uninstall $(if $(PROJECT),--project "$(PROJECT)")

package:
	$(PYTHON) scripts/package.py

clean:
	rm -rf dist
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
