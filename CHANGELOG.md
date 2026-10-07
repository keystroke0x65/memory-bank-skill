# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-07

### Added
- `memory-bank` skill: `SKILL.md`, mode references (init, load, reflect, curate,
  maintain), spec, safety rules, and research basis.
- `memory.py` CLI: `init`, `find`, `apply` (atomic operations batches with
  ADD_ROOT, ADD_DELTA, UPDATE, SUPERSEDE, DELETE, PROMOTE and feedback counters),
  `validate`, `consolidate`, `stats`, `index`, `rollback`.
- `hooks.py` with SessionStart, Stop and PreCompact hooks, plus
  `hooks/settings.example.json`.
- Templates for `memory-bank/` context, progress, active-context and experience files.
- `ops.schema.json` describing the operations batch.
- Unit tests and agent-level evals with a sample-project fixture.
- Repo tooling: Makefile, `scripts/install.sh` (symlink install), `scripts/smoke.sh`,
  `scripts/check_schema.py`, `scripts/package.py`.
- GitHub Actions CI on Python 3.9 and 3.12.
- This repo's own `memory-bank/`, created with the skill.

[Unreleased]: https://github.com/keystroke0x65/memory-bank-skill/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/keystroke0x65/memory-bank-skill/releases/tag/v0.1.0
