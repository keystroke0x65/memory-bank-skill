# Architecture — memory-bank-skill-project

<!-- Entry file. How the system is put together. Prefer facts verifiable in the code; set src= to the file. -->

## Components
<!-- empty: major modules/services and their responsibility -->
- [arch-0001] root h=0 x=0 d=2026-10-07 labels=layout,repo src="README.md" :: Repo layout: skill/memory-bank/ (the skill), tests/ (test_memory.py, evals.json, fixtures/), scripts/ (repo tooling, not the skill's scripts), docs/ (design notes), memory-bank/ (this repo's own bank), .github/workflows/ci.yml
- [arch-0002] root h=0 x=0 d=2026-10-07 labels=skill,modes,hooks src="skill/memory-bank/SKILL.md" :: Skill: SKILL.md picks a mode (init, load, record, maintain) and points to references/<mode>.md; scripts/memory.py is the CLI; scripts/hooks.py serves SessionStart/Stop/PreCompact hooks; assets/templates seed a new bank
- [arch-0003] root h=0 x=0 d=2026-10-07 labels=lib,cli src="skill/memory-bank/scripts/lib/ops.py" :: scripts/lib: ops.py runs batches, store.py does file IO, IDs, snapshots and rollback, entry.py parses entry lines, search.py does keyword find and duplicate similarity, budget.py holds limits, safety.py scans for secrets

## Data flow
<!-- empty: how data and requests move through the system -->
- [arch-0004] root h=0 x=0 d=2026-10-07 labels=ops,apply,batch src="skill/memory-bank/scripts/memory.py" :: Writes go agent → JSON operations batch → memory.py apply: the whole batch is validated (atomic, nothing written on any error), snapshotted to .snapshots/, merged into entry files, logged to ops-log.jsonl, and index.md is regenerated

## Integrations
<!-- empty: external services, APIs, auth providers, queues -->

## Invariants
<!-- empty: rules that must stay true (e.g. "all DB access goes through lib/db") -->
- [arch-0005] root h=0 x=0 d=2026-10-07 labels=install,paths,symlink src="skill/memory-bank/scripts/memory.py" :: memory.py and hooks.py resolve every path from Path(__file__), so the skill runs unchanged through a symlink or from a zip extract; keep new skill code on that pattern
- [arch-0006] root h=0 x=0 d=2026-10-07 labels=schema,validate src="scripts/check_schema.py" :: ops.schema.json is documentation only and no skill script loads it; scripts/check_schema.py implements just the keywords it uses and fails if the schema adopts an unsupported keyword
