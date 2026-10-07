# Contributing

## Branches

- `main`: released state. Every release is tagged `vX.Y.Z`.
- `develop`: integration branch. Branch from it, and merge back into it.
- Work branches are named after the kind of change:
  - `feat/<short-name>` for new behaviour in the skill or tooling
  - `fix/<short-name>` for bug fixes
  - `docs/<short-name>` for documentation only

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<optional scope>): <summary in the imperative>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `build`, `ci`, `chore`.
Scope is optional. Use `skill`, `cli`, `hooks`, `tests` or `tooling` when it helps.
Mark breaking changes with `!` after the type, or with a `BREAKING CHANGE:` footer.

## Before you push

```sh
make test
make validate
```

Both must pass. CI runs the same targets on Python 3.9 and 3.12.

## Rules

- **Behavioural changes to the skill need a matching test or eval.** If a
  change affects what the scripts do, add or update a unit test in
  `tests/test_memory.py`. If it affects what the agent is told to do (`SKILL.md`
  or `references/`), add or update an eval in `tests/evals.json`.
- **Keep `skill/memory-bank/` self-contained.** It must work when symlinked or
  unzipped into `~/.claude/skills/memory-bank`. Don't reference files outside
  it, and don't add third-party dependencies. The skill targets Python 3.8+,
  standard library only.
- **Keep the spec and the scripts in sync.** If you change a budget, an
  operation or the entry format, update `references/spec.md` and
  `scripts/schemas/ops.schema.json` in the same change.
- Record user-visible changes under `[Unreleased]` in `CHANGELOG.md`.
