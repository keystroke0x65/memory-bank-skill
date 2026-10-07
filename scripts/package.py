#!/usr/bin/env python3
"""Zip skill/memory-bank into dist/memory-bank-<version>.zip. Standard library only.

The archive's top-level folder is memory-bank/, so it can be unzipped straight
into ~/.claude/skills/ or <project>/.claude/skills/. Caches are left out.
"""
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "memory-bank"
SKIP_DIRS = {"__pycache__", ".pytest_cache"}
SKIP_FILES = {".DS_Store"}


def version() -> str:
    try:
        out = subprocess.run(["git", "describe", "--tags", "--always", "--dirty"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        return out.lstrip("v") or "dev"
    except (OSError, subprocess.CalledProcessError):
        return "dev"


def main() -> int:
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / f"memory-bank-{version()}.zip"
    files = sorted(p for p in SKILL.rglob("*")
                   if p.is_file() and not SKIP_DIRS.intersection(p.parts) and p.name not in SKIP_FILES
                   and p.suffix != ".pyc")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            zf.write(p, Path("memory-bank") / p.relative_to(SKILL))
    print(f"wrote {out.relative_to(ROOT)} ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
