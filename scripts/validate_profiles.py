#!/usr/bin/env python3
"""Validate team-profiles/*.json against team-profiles/profile.schema.json.

Stdlib only. Implements just enough of JSON Schema draft-07 to hand-validate
the profile schema in this repo: type, enum, required, properties,
additionalProperties (bool or subschema), and items. No third-party dep.

Usage:
  python scripts/validate_profiles.py [--format {human,github}]

Exit 0 if all profiles validate, 1 otherwise.
"""
import argparse
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILES_DIR = os.path.join(REPO_ROOT, "team-profiles")
SCHEMA_PATH = os.path.join(PROFILES_DIR, "profile.schema.json")
PROFILE_FILES = ["greenfield.json", "active.json", "legacy.json"]

# JSON Schema "type" -> Python type(s). bool checked before int (bool is int subclass).
_TYPE_CHECKS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "null": lambda v: v is None,
}


def _validate(instance, schema, path, errors):
    """Append human-readable error strings to `errors` for any violations."""
    if "type" in schema:
        t = schema["type"]
        types = t if isinstance(t, list) else [t]
        if not any(_TYPE_CHECKS[tt](instance) for tt in types):
            errors.append("%s: expected type %s, got %s"
                          % (path or "<root>", "|".join(types), type(instance).__name__))
            # Type mismatch invalidates deeper keyword checks for this node.
            return

    if "enum" in schema:
        if instance not in schema["enum"]:
            errors.append("%s: value %r not in enum %s" % (path, instance, schema["enum"]))

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append("%s: missing required key %r" % (path or "<root>", req))

        props = schema.get("properties", {})
        for key, subval in instance.items():
            child_path = "%s.%s" % (path, key) if path else key
            if key in props:
                _validate(subval, props[key], child_path, errors)
            else:
                addl = schema.get("additionalProperties", True)
                if addl is False:
                    errors.append("%s: additional property %r not allowed" % (path or "<root>", key))
                elif isinstance(addl, dict):
                    _validate(subval, addl, child_path, errors)
                # addl is True (or absent): anything goes.

    if isinstance(instance, list) and "items" in schema:
        item_schema = schema["items"]
        # Only list-of-one-schema form is used in this repo's schema.
        if isinstance(item_schema, dict):
            for i, item in enumerate(instance):
                _validate(item, item_schema, "%s[%d]" % (path, i), errors)


def validate(instance, schema):
    """Return a list of error strings (empty == valid)."""
    errors = []
    _validate(instance, schema, "", errors)
    return errors


def _load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate team profiles against the draft-07 schema.")
    ap.add_argument("--format", choices=["human", "github"], default="human")
    args = ap.parse_args(argv)

    try:
        schema = _load_json(SCHEMA_PATH)
    except (OSError, ValueError) as e:
        print("error: cannot load schema %s: %s" % (SCHEMA_PATH, e), file=sys.stderr)
        return 1

    if schema.get("$schema") != "http://json-schema.org/draft-07/schema#":
        print("error: profile.schema.json is not declared as draft-07", file=sys.stderr)
        return 1

    ok = True
    for fname in PROFILE_FILES:
        fpath = os.path.join(PROFILES_DIR, fname)
        rel = os.path.relpath(fpath, REPO_ROOT)
        try:
            inst = _load_json(fpath)
        except (OSError, ValueError) as e:
            ok = False
            if args.format == "github":
                print("::error file=%s::cannot parse: %s" % (rel, e))
            else:
                print("FAIL %s: cannot parse: %s" % (rel, e))
            continue

        errs = validate(inst, schema)
        if errs:
            ok = False
            for e in errs:
                if args.format == "github":
                    print("::error file=%s::%s" % (rel, e))
                else:
                    print("FAIL %s: %s" % (rel, e))
        else:
            if args.format != "github":
                print("OK   %s" % rel)

    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print("internal error: %s" % e, file=sys.stderr)
        sys.exit(2)
