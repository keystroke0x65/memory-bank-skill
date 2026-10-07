# Progress — memory-bank-skill-project

<!-- Entry file. Changed only through memory.py apply. Move items between sections with UPDATE + section. -->

## Now
<!-- empty: work in progress -->

## Next
<!-- empty: planned work, highest priority first -->
- [prog-0002] root h=0 x=0 d=2026-10-07 labels=dogfood,skill src="user" :: Review the dogfooding rough-edge list from the 0.1.0 setup session and decide which skill changes to make; each needs a test or eval per CONTRIBUTING.md
- [prog-0003] root h=0 x=0 d=2026-10-07 labels=install,workspace src="ls -la ../../.claude/skills/memory-bank" :: The workspace's .claude/skills/memory-bank is a separate real-directory copy of the skill; replace it with make install PROJECT=<workspace root> once it has been removed, so there is one source
- [prog-0004] root h=0 x=0 d=2026-10-07 labels=evals,testing src="tests/evals.json" :: tests/evals.json holds 3 agent-level evals with no runner in this repo; decide how to run them (skill-creator eval flow or a script) and wire them into a make target

## Done
<!-- empty: completed milestones (keep the latest 15; consolidate archives older ones) -->
- [prog-0001] root h=0 x=0 d=2026-10-07 labels=release src="CHANGELOG.md" :: 0.1.0: skill moved to skill/memory-bank, evals to tests/, Makefile and repo scripts, README/CHANGELOG/CONTRIBUTING/LICENSE, CI, and this dogfood bank

## Known issues
<!-- empty: bugs, tech debt, limitations still open -->
- [prog-0005] root h=0 x=0 d=2026-10-07 labels=python,ci src=".github/workflows/ci.yml" :: The skill claims Python 3.8+ but nothing tests 3.8: CI covers only 3.9 and 3.12, and setup-python on ubuntu-latest may no longer ship 3.8
