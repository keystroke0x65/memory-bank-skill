# Tech Stack — memory-bank-skill-project

<!-- Entry file. Versions, tooling, environments, and the commands that actually work. -->

## Runtime and frameworks
<!-- empty: languages, frameworks, key libraries with versions -->
- [stack-0001] root h=0 x=0 d=2026-10-07 labels=python,ci src=".github/workflows/ci.yml" :: Python standard library only (argparse, json, pathlib, unittest, zipfile); CI tests on Python 3.9 and 3.12, local dev on 3.12

## Services and infrastructure
<!-- empty: hosting, databases, storage, CI/CD -->
- [stack-0002] root h=0 x=0 d=2026-10-07 labels=ci,github src=".github/workflows/ci.yml" :: GitHub Actions workflow CI runs make test then make validate on every push and pull request, matrix Python 3.9 and 3.12, fail-fast off

## Dev environment
<!-- empty: setup steps, env var NAMES (never values), local services -->
- [stack-0008] root h=0 x=0 d=2026-10-07 labels=env,bank,cli src="skill/memory-bank/scripts/lib/store.py" :: memory.py finds the bank via --bank PATH, else env var MEMORY_BANK_DIR, else the nearest memory-bank/ walking up from cwd; from this repo root that is the dogfood bank, so tests and smoke always pass --bank

## Commands
<!-- empty: build, test, lint, run, deploy commands verified to work -->
- [stack-0003] root h=0 x=0 d=2026-10-07 labels=commands,testing src="Makefile" :: make test runs python3 -m unittest discover -s tests -v from the repo root (12 tests in tests/test_memory.py); override the interpreter with PYTHON=...
- [stack-0004] root h=0 x=0 d=2026-10-07 labels=commands,testing,smoke src="scripts/smoke.sh" :: make smoke runs scripts/smoke.sh: init, apply --dry-run, apply, find, validate in a mktemp dir using tests/fixtures/smoke-ops.json, then asserts the IDs are on disk; prints FAIL and exits 1 on any error
- [stack-0005] root h=0 x=0 d=2026-10-07 labels=commands,schema,validate src="Makefile" :: make validate runs scripts/check_schema.py (parses all JSON, checks tests/fixtures/*-ops.json against ops.schema.json, confirms known-bad batches are rejected) and then the smoke run
- [stack-0006] root h=0 x=0 d=2026-10-07 labels=commands,install src="scripts/install.sh" :: make install symlinks skill/memory-bank to ~/.claude/skills/memory-bank; make install PROJECT=<path> targets <path>/.claude/skills; make uninstall removes only a symlink pointing at this repo; refuses real directories
- [stack-0007] root h=0 x=0 d=2026-10-07 labels=commands,package,release src="scripts/package.py" :: make package writes dist/memory-bank-<git describe>.zip with memory-bank/ as the top folder (caches excluded); make clean removes dist/ and __pycache__
