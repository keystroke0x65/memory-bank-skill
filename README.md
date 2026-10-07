# memory-bank skill

A Claude Code skill that gives an agent a persistent, per-project memory in a
`memory-bank/` folder. The agent loads it at the start of a session and records
to it after meaningful work. The memory holds two kinds of knowledge:

- **Project context**: what is true about the project (purpose, architecture,
  tech stack, conventions, decisions, progress).
- **Experience**: what was learned doing work. Strategies that worked are
  stored as root entries with condition-specific deltas. Approaches that failed
  are stored as traps.

The agent never rewrites memory files directly. It writes a small JSON
*operations batch*, and a Python script validates it and merges it in.

Python 3.8+, standard library only. There are no dependencies to install.

## Repository layout

```
skill/memory-bank/   the skill itself; this folder is what gets installed
  SKILL.md           entry point the agent reads
  references/        per-mode instructions (init, load, reflect, curate, maintain), spec, safety
  scripts/           memory.py (CLI), hooks.py (agent hooks), lib/, schemas/ops.schema.json
  assets/templates/  files copied into a new memory-bank/
  hooks/             settings.example.json for SessionStart / Stop / PreCompact hooks
tests/               unit tests, evals.json (agent-level evals), fixtures
scripts/             repo tooling: install.sh, smoke.sh, check_schema.py, package.py
docs/                design notes
memory-bank/         this repo's own memory bank, maintained with the skill
```

## The `memory-bank/` folder the skill produces

```
<project>/memory-bank/
├── index.md              generated map of the bank; read at session start
├── active-context.md     current focus and next steps; the only file edited by hand (≤80 lines)
├── progress.md           Now / Next / Done / Known issues
├── context/
│   ├── project-brief.md  purpose, users, scope, non-goals
│   ├── architecture.md   components, data flow, invariants
│   ├── tech-stack.md     versions, services, env var names, commands
│   ├── conventions.md    code style, patterns, testing, workflow
│   └── decisions.md      decisions with rationale
├── experience/<topic>.md Lessons (root → delta chains) and Traps, one file per topic
├── history/archive.md    superseded, deleted and promoted entries with reasons
├── ops-log.jsonl         every applied batch
├── .state.json           ID counters and hook state
└── .snapshots/           pre-batch copies for rollback (gitignored)
```

Each entry is a single line with a stable ID and helpful/harmful counters:

```
- [auth-0001] root h=4 x=0 d=2026-09-16 labels=auth,clerk src="middleware.ts" :: Content sentence.
  - [auth-0001.1] delta h=1 x=0 d=2026-09-16 when="API route handlers" :: Only what differs under this condition.
- [auth-0002] trap h=0 x=0 d=2026-09-16 labels=auth :: FAILED: what was tried. INSTEAD: what works.
```

The full contract is in
[`skill/memory-bank/references/spec.md`](skill/memory-bank/references/spec.md).

## Install

The skill is installed as a symlink, so edits in this repo take effect immediately.

```sh
make install                      # ~/.claude/skills/memory-bank -> skill/memory-bank
make install PROJECT=~/code/app   # ~/code/app/.claude/skills/memory-bank instead
make uninstall                    # removes the symlink (same PROJECT= option)
```

You can also run `scripts/install.sh [--project <path>] [--uninstall]`
directly. The script is idempotent. It refuses to replace a real directory or
a symlink that points somewhere else.

To share the skill without the repo, run `make package`. It writes
`dist/memory-bank-<version>.zip`, with `memory-bank/` as the top-level folder.

### Hooks (optional)

`skill/memory-bank/hooks/settings.example.json` sets up three hooks:

- **SessionStart** prints `index.md` and `active-context.md`.
- **Stop** asks the agent once per session to record what it learned.
- **PreCompact** reminds the agent to record before context is compacted.

Merge its `hooks` block into `.claude/settings.json` or
`~/.claude/settings.json`, adjusting the path to wherever the skill is
installed. Each hook exits silently in projects that have no `memory-bank/`.

## CLI

Run these from the project, or pass `--bank PATH`. Without `--bank`, the CLI
uses `$MEMORY_BANK_DIR` if it is set, and otherwise the nearest `memory-bank/`
found by walking up from the current directory. Add `--json` to any command
for machine-readable output.

```
python3 scripts/memory.py init [PROJECT_DIR]       create memory-bank/ from templates (never overwrites)
python3 scripts/memory.py find <keywords...>       root → delta chains relevant to a task
python3 scripts/memory.py apply ops.json [--dry-run]   validate and apply a batch, atomically
python3 scripts/memory.py validate                 format, IDs, orphans, secrets, budgets
python3 scripts/memory.py consolidate              promote / prune / duplicate / stale report
python3 scripts/memory.py stats                    counts and counters
python3 scripts/memory.py index                    regenerate index.md
python3 scripts/memory.py rollback                 undo the most recent batch
```

`scripts/` here means `skill/memory-bank/scripts/`, or
`~/.claude/skills/memory-bank/scripts/` once installed.

## How the operations batch works

```json
{
  "note": "fixed preview deploy failures",
  "feedback": [{"id": "deploy-0001", "tag": "helpful"}],
  "operations": [
    {"op": "ADD_ROOT", "file": "experience/deploy.md", "section": "Lessons", "ref": "mig",
     "content": "Run database migrations before deploying the web app", "labels": ["deploy"]},
    {"op": "ADD_DELTA", "parent": "@mig", "when": "preview deployments",
     "content": "point migrations at the preview branch database, not main"}
  ]
}
```

- **Operations:** `ADD_ROOT` (a fact, lesson, or `kind: "trap"`), `ADD_DELTA`
  (a variation under a specific `when`), `UPDATE` (same fact, better wording),
  `SUPERSEDE` (the fact changed; the old entry is archived), `DELETE`, and
  `PROMOTE` (compile a proven delta chain into a new root).
- **IDs and refs:** the script assigns IDs. Later operations in the same batch
  can refer to earlier ones with `"@ref"`.
- **Feedback:** `feedback` tags update the helpful/harmful counters on entries
  the agent relied on. Entries with `x ≥ 2` and `x > h` are hidden from `find`
  and reported as prune candidates.
- **Atomic batches:** a batch is all-or-nothing. If anything fails, nothing is
  written. Failure reasons include a near-duplicate (similarity ≥ 0.82), a
  secret-looking string, a missing `when`, an unknown parent, content outside
  12–400 characters, or a delta deeper than 3. File-size budgets only produce
  warnings.
- **Rollback:** each applied batch is snapshotted, and `rollback` undoes the
  last one.

The batch shape is documented as a JSON Schema in
`skill/memory-bank/scripts/schemas/ops.schema.json`.

## Development

```sh
make test       # unit tests (python3 -m unittest discover -s tests)
make smoke      # end-to-end CLI run in a temp directory
make validate   # JSON/schema checks, then the smoke run
make package    # dist/memory-bank-<version>.zip
make clean      # remove dist/ and __pycache__
```

CI runs `make test` and `make validate` on Python 3.9 and 3.12. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the contribution rules.

## Why

Agents lose project knowledge between sessions. When an agent keeps notes by
rewriting a file, the notes tend to lose detail with each pass. The skill's
design adapts four research results to a file-based, prompt-only setting:

| Source | What the skill takes from it |
|---|---|
| **ReasoningBank** | What to store: generalizable lessons from both successes and failures, at most 3 per task. |
| **DeltaMem** | How memory is structured: a general root plus small condition-specific deltas and failure records. |
| **ACE** | How memory is written: small operations merged by a script, with helpful/harmful counters, and no whole-file rewrites (which cause "context collapse"). |
| **MemoryAgentBench** | Forgetting: contradicted and harmful entries are superseded or pruned. |

None of the papers' reported results were reproduced here. Sources, the
mapping from each rule to its source, and known gaps are in
[`skill/memory-bank/references/research-basis.md`](skill/memory-bank/references/research-basis.md).

## License

MIT. See [LICENSE](LICENSE).
