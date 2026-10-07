# Active Context — memory-bank-skill-project

<!-- Freeform, short-lived state. The agent MAY rewrite this file directly (the only exception
     to operations-only writes). Keep it under 80 lines. Durable facts belong in context/ or experience/. -->

## Current focus
0.1.0 project wrapper is done: layout, tooling, docs and CI, tagged v0.1.0 on main and pushed
with develop to the private GitHub repo memory-bank-skill. Day-to-day work happens on develop.

## Open questions / blockers
- Which dogfooding rough edges (reported to the user at the end of the 0.1.0 session) become
  skill changes? The user decides; don't edit skill/memory-bank/ for them unprompted.
- How should the 3 agent-level evals in tests/evals.json be run? There is no runner yet (prog-0004).

## Recent changes
- 2026-10-07: init batch b-20261007-203703-09z2 seeded context/ and progress.md (30 roots).
- 2026-10-07: moved the skill to skill/memory-bank and evals to tests/; added Makefile,
  scripts/{install,smoke}.sh, check_schema.py, package.py, docs and CI.
- The only skill edit so far: one line in references/research-basis.md now points at
  tests/evals.json instead of evals/ (approved by the user).

## Next steps
- Branch feat/* or fix/* off develop for any skill change, with a test or eval (conv-0002).
- Remove the workspace's real-directory copy of the skill and replace it with a symlink (prog-0003).
- Add Python 3.8 coverage, or change the 3.8+ claim (prog-0005).
