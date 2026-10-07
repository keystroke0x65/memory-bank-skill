#!/usr/bin/env bash
# End-to-end smoke run of the skill's CLI in a throwaway directory:
# init -> apply (dry-run, then real) -> find -> validate -> verify.
# Any non-zero exit or failed assertion stops the run with a FAIL line.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MEMORY="$ROOT/skill/memory-bank/scripts/memory.py"
OPS="$ROOT/tests/fixtures/smoke-ops.json"
PYTHON="${PYTHON:-python3}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
BANK="$TMP/memory-bank"
# Run from inside the temp dir so memory.py can never find this repo's own bank.
cd "$TMP"

fail() { echo "FAIL: $*" >&2; exit 1; }

run() {
  echo "+ memory.py $*"
  local out
  if ! out="$("$PYTHON" "$MEMORY" "$@" 2>&1)"; then
    echo "$out" >&2
    fail "memory.py $* exited non-zero"
  fi
  printf '%s\n' "$out" | sed 's/^/    /'
  LAST="$out"
}

run init "$TMP"
[ -f "$BANK/.state.json" ] || fail "init did not create $BANK/.state.json"
grep -qx '.snapshots/' "$BANK/.gitignore" || fail "init did not write .snapshots/ to memory-bank/.gitignore"

run --bank "$BANK" apply "$OPS" --dry-run
grep -q 'status: dry-run' <<<"$LAST" || fail "dry-run did not report status: dry-run"
[ ! -f "$BANK/experience/deploy.md" ] || fail "dry-run wrote experience/deploy.md"

run --bank "$BANK" apply "$OPS"
grep -q 'status: applied' <<<"$LAST" || fail "apply did not report status: applied"

run --bank "$BANK" find migrations preview deploy
grep -q 'deploy-0001\.1' <<<"$LAST" || fail "find did not return the deploy-0001 -> .1 chain"

run --bank "$BANK" validate
grep -q 'ok: memory bank is valid' <<<"$LAST" || fail "validate did not report ok"

# verify: the applied entries are on disk, indexed, and logged.
echo "+ verify"
grep -q '^- \[stack-0001\] root ' "$BANK/context/tech-stack.md" || fail "stack-0001 missing from context/tech-stack.md"
grep -q '^- \[deploy-0001\] root ' "$BANK/experience/deploy.md" || fail "deploy-0001 missing from experience/deploy.md"
grep -q '^  - \[deploy-0001\.1\] delta ' "$BANK/experience/deploy.md" || fail "deploy-0001.1 delta missing"
grep -q '^- \[deploy-0002\] trap ' "$BANK/experience/deploy.md" || fail "deploy-0002 trap missing"
grep -q 'deploy' "$BANK/index.md" || fail "index.md does not mention experience/deploy.md"
[ "$(wc -l < "$BANK/ops-log.jsonl")" -eq 1 ] || fail "ops-log.jsonl should hold exactly one batch"
[ -d "$BANK/.snapshots" ] || fail "apply did not write a rollback snapshot"

echo "smoke: ok"
