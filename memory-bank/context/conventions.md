# Conventions — memory-bank-skill-project

<!-- Entry file. How code is written here. Only record conventions observed in the code or stated by the user. -->

## Code style
<!-- empty: formatting, naming, file layout -->

## Patterns
<!-- empty: preferred patterns and ones to avoid -->

## Testing
<!-- empty: what to test, where tests live, how to run a single test -->
- [conv-0001] root h=0 x=0 d=2026-10-07 labels=testing,unittest src="tests/test_memory.py" :: Unit tests import the CLI by putting skill/memory-bank/scripts on sys.path (never by editing the skill) and drive memory.main() against a temp bank via --bank
- [conv-0002] root h=0 x=0 d=2026-10-07 labels=testing,evals,contributing src="CONTRIBUTING.md" :: Behavioural changes to the skill need a matching check: script behaviour → unit test in tests/test_memory.py; agent instructions in SKILL.md or references/ → eval in tests/evals.json

## Workflow
<!-- empty: branching, commits, reviews, release steps -->
- [conv-0003] root h=0 x=0 d=2026-10-07 labels=git,branches,commits src="CONTRIBUTING.md" :: Branches feat/*, fix/*, docs/* off develop; main holds tagged releases vX.Y.Z; Conventional Commits (feat, fix, docs, test, refactor, build, ci, chore); run make test and make validate before pushing
- [conv-0004] root h=0 x=0 d=2026-10-07 labels=spec,schema,changelog src="CONTRIBUTING.md" :: When a budget, operation or entry format changes, update references/spec.md and scripts/schemas/ops.schema.json in the same change; the scripts are authoritative, and user-visible changes go under Unreleased in CHANGELOG.md
