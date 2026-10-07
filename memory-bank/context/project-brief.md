# Project Brief — memory-bank-skill-project

<!-- Entry file (declarative project knowledge). Changed only through memory.py apply.
     Foundation document: everything else should be consistent with it. -->

## Purpose
<!-- empty: what the project is and the problem it solves -->
- [brief-0001] root h=0 x=0 d=2026-10-07 labels=product,skill src="README.md" :: This repo develops and ships the memory-bank Claude Code skill, which gives an agent a persistent per-project memory in a memory-bank/ folder: project context plus lessons stored as root → delta chains with helpful/harmful counters

## Users
<!-- empty: who uses it and what they need -->
- [brief-0003] root h=0 x=0 d=2026-10-07 labels=github,workflow src="user" :: Private project maintained by Ash; GitHub repo memory-bank-skill (private), with main for releases and develop as the working branch

## Scope
<!-- empty: what is in scope -->
- [brief-0002] root h=0 x=0 d=2026-10-07 labels=scope,skill src="user" :: The skill content (SKILL.md, references/*.md, scripts/ Python, templates) is the product; the repo around it is the wrapper (tooling, tests, docs, CI). Skill content changes only on purpose or for a real bug, never as incidental rewording

## Non-goals
<!-- empty: what is deliberately out of scope -->

## Constraints
<!-- empty: deadlines, budget, compliance, platform limits -->
- [brief-0004] root h=0 x=0 d=2026-10-07 labels=python,dependencies src="skill/memory-bank/scripts/memory.py" :: Python 3.8+ standard library only, no third-party dependencies, for both the skill and the repo tooling; there is no requirements file or pyproject
- [brief-0005] root h=0 x=0 d=2026-10-07 labels=skill,install src="CONTRIBUTING.md" :: skill/memory-bank/ must stay self-contained: it has to work when symlinked or unzipped into ~/.claude/skills/memory-bank, so it may not reference files outside itself
