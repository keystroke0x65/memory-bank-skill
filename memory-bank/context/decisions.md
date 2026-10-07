# Decisions — memory-bank-skill-project

<!-- Entry file (ADR-style). One decision per root: "Chose X over Y because Z". When a decision
     changes, SUPERSEDE it — the old one moves to history/archive.md with the reason. -->

## Decisions
<!-- empty: architectural and product decisions with their rationale -->
- [dec-0001] root h=0 x=0 d=2026-10-07 labels=install,symlink src="README.md" :: Chose symlink install over copying so edits in skill/memory-bank take effect immediately; make package covers sharing without the repo
- [dec-0002] root h=0 x=0 d=2026-10-07 labels=docs,research src="docs/README.md" :: Kept references/research-basis.md inside the skill rather than moving it to docs/, because SKILL.md links to it; docs/README.md points to it instead
