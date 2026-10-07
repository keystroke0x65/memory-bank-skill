#!/usr/bin/env bash
# Symlink skill/memory-bank into a Claude Code skills directory.
#
#   scripts/install.sh                      -> ~/.claude/skills/memory-bank
#   scripts/install.sh --project <path>     -> <path>/.claude/skills/memory-bank
#   scripts/install.sh --uninstall [--project <path>]
#
# Idempotent: re-installing an existing link to this repo is a no-op.
# Never replaces a real directory or a symlink that points somewhere else,
# and --uninstall only removes a symlink that points at this repo.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/skill/memory-bank"
SKILLS_DIR="$HOME/.claude/skills"
MODE=install

usage() { sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --project)
      [ $# -ge 2 ] || { echo "error: --project needs a path" >&2; exit 2; }
      [ -d "$2" ] || { echo "error: project directory not found: $2" >&2; exit 2; }
      SKILLS_DIR="$(cd "$2" && pwd)/.claude/skills"
      shift 2 ;;
    --uninstall) MODE=uninstall; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

DEST="$SKILLS_DIR/memory-bank"

points_here() { [ -L "$DEST" ] && [ "$(readlink "$DEST")" = "$SRC" ]; }

if [ "$MODE" = install ]; then
  if points_here; then
    echo "already installed: $DEST -> $SRC"
    exit 0
  fi
  if [ -L "$DEST" ]; then
    echo "error: $DEST is a symlink to $(readlink "$DEST"), not this repo; remove it first" >&2
    exit 1
  fi
  if [ -e "$DEST" ]; then
    echo "error: $DEST already exists and is not a symlink; refusing to replace it" >&2
    exit 1
  fi
  mkdir -p "$SKILLS_DIR"
  ln -s "$SRC" "$DEST"
  echo "installed: $DEST -> $SRC"
else
  if points_here; then
    rm "$DEST"
    echo "uninstalled: removed symlink $DEST"
  elif [ -L "$DEST" ]; then
    echo "error: $DEST points to $(readlink "$DEST"), not this repo; leaving it alone" >&2
    exit 1
  elif [ -e "$DEST" ]; then
    echo "error: $DEST is a real directory, not an install from this repo; leaving it alone" >&2
    exit 1
  else
    echo "not installed: nothing at $DEST"
  fi
fi
