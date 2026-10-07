#!/usr/bin/env python3
"""Static checks for the skill's JSON files. Python 3.8+, standard library only.

  1. Every *.json in the skill and tests/ parses.
  2. Example batches (tests/fixtures/*-ops.json) validate against
     skill/memory-bank/scripts/schemas/ops.schema.json.
  3. Known-bad batches are rejected, so the checker itself is exercised.

The skill's scripts do not load ops.schema.json; it documents the batch format.
This checker implements only the JSON Schema keywords that schema uses:
type, properties, required, enum, const, minLength, maxLength, maxItems,
items, allOf with if/then, and additionalProperties: false.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "memory-bank"
SCHEMA = SKILL / "scripts" / "schemas" / "ops.schema.json"

TYPES = {"object": dict, "array": list, "string": str, "boolean": bool}
SUPPORTED = {"$schema", "title", "description", "type", "properties", "required", "enum", "const",
             "minLength", "maxLength", "maxItems", "items", "allOf", "if", "then", "additionalProperties"}


def unsupported(schema, path="#"):
    """Keywords this checker would silently ignore — fail instead of passing wrongly."""
    if not isinstance(schema, dict):
        return []
    bad = [f"{path}/{k}" for k in schema if k not in SUPPORTED]
    for k, v in schema.get("properties", {}).items():
        bad += unsupported(v, f"{path}/properties/{k}")
    if "items" in schema:
        bad += unsupported(schema["items"], f"{path}/items")
    for i, sub in enumerate(schema.get("allOf", [])):
        bad += unsupported(sub.get("if"), f"{path}/allOf/{i}/if")
        bad += unsupported(sub.get("then"), f"{path}/allOf/{i}/then")
    return bad


def validate(value, schema, path="$"):
    errors = []
    t = schema.get("type")
    if t and not (isinstance(value, TYPES[t]) and not (t != "boolean" and isinstance(value, bool))):
        return [f"{path}: expected {t}, got {type(value).__name__}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must be {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not one of {schema['enum']}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: longer than {schema['maxLength']}")
    if isinstance(value, list):
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: more than {schema['maxItems']} items")
        for i, item in enumerate(value):
            errors += validate(item, schema.get("items", {}), f"{path}[{i}]")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required '{key}'")
        for key, sub in value.items():
            if key in props:
                errors += validate(sub, props[key], f"{path}.{key}")
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property '{key}'")
    for cond in schema.get("allOf", []):
        if not validate(value, cond.get("if", {}), path):
            errors += validate(value, cond.get("then", {}), path)
    return errors


BAD_BATCHES = {
    "unknown op": {"operations": [{"op": "REPLACE", "id": "x-0001"}]},
    "ADD_ROOT without section": {"operations": [{"op": "ADD_ROOT", "file": "context/tech-stack.md",
                                                 "content": "a perfectly fine sentence"}]},
    "ADD_DELTA without when": {"operations": [{"op": "ADD_DELTA", "parent": "x-0001",
                                               "content": "a perfectly fine sentence"}]},
    "content too short": {"operations": [{"op": "ADD_ROOT", "file": "progress.md", "section": "Now", "content": "tiny"}]},
    "bad feedback tag": {"feedback": [{"id": "x-0001", "tag": "great"}], "operations": []},
    "top-level typo": {"operation": []},
}


def main() -> int:
    failures = []
    files = sorted(p for d in (SKILL, ROOT / "tests") for p in d.rglob("*.json") if "node_modules" not in p.parts)
    for p in files:
        try:
            json.loads(p.read_text())
        except json.JSONDecodeError as exc:
            failures.append(f"{p.relative_to(ROOT)}: invalid JSON: {exc}")
    print(f"parsed {len(files)} JSON files")

    schema = json.loads(SCHEMA.read_text())
    for kw in unsupported(schema):
        failures.append(f"ops.schema.json uses {kw}, which scripts/check_schema.py does not implement")

    examples = sorted((ROOT / "tests" / "fixtures").glob("*-ops.json"))
    if not examples:
        failures.append("no example batches found in tests/fixtures/*-ops.json")
    for p in examples:
        for err in validate(json.loads(p.read_text()), schema):
            failures.append(f"{p.relative_to(ROOT)}: {err}")
    print(f"validated {len(examples)} example batch(es) against ops.schema.json")

    accepted = [name for name, batch in BAD_BATCHES.items() if not validate(batch, schema)]
    failures += [f"schema accepted a known-bad batch: {name}" for name in accepted]
    print(f"rejected {len(BAD_BATCHES) - len(accepted)}/{len(BAD_BATCHES)} known-bad batches")

    for f in failures:
        print(f"FAIL: {f}", file=sys.stderr)
    print("schema check: " + ("FAILED" if failures else "ok"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
