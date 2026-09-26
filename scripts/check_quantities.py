#!/usr/bin/env python3
"""Verify the canonical quantity register against the code that implements it.

A register nobody checks is decoration. This reads each registered `code_anchor` out of the
source by parsing it, and fails when the code and the register disagree. That is the one thing
a register must guarantee: a quantity used in more than one place has one value.

It checks provenance discipline too, because the categories only mean something if they are
used consistently:

  - every quantity declares a provenance from the allowed set and an evidence status;
  - anything marked `provisional_estimate` states what would resolve it;
  - a `sourced_assumption` names its source, and if it states an applicability condition it must
    also say whether that condition was checked;
  - nothing claims to be physically tested, because no measurement exists in this project yet.
"""
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/canonical-quantities.json"


def literal_constants(path):
    """Module-level `NAME = <number>` assignments, read from the source rather than imported."""
    out = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, (int, float)):
            out[node.targets[0].id] = node.value.value
    return out


def keyword_defaults(path):
    """Defaulted numeric keyword arguments, e.g. `min_improvement=0.20`."""
    out = {}
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        args = node.args
        pairs = list(zip(args.args[len(args.args) - len(args.defaults):], args.defaults))
        pairs += list(zip(args.kwonlyargs, args.kw_defaults))
        for arg, default in pairs:
            if isinstance(default, ast.Constant) and isinstance(default.value, (int, float)):
                out.setdefault(arg.arg, set()).add(default.value)
    return out


def check():
    doc = json.loads(REGISTER.read_text())
    categories = set(doc["provenance_categories"])
    statuses = set(doc["evidence_status"])
    problems = []

    for name, q in doc["quantities"].items():
        prov = q.get("provenance")
        if prov not in categories:
            problems.append("%s: provenance %r is not one of the declared categories" % (name, prov))
        if q.get("evidence_status") not in statuses:
            problems.append("%s: evidence_status %r is not declared" % (name, q.get("evidence_status")))
        if prov == "provisional_estimate" and not q.get("open_question"):
            problems.append("%s: a provisional estimate must say what would resolve it" % name)
        if prov == "sourced_assumption":
            if not q.get("source"):
                problems.append("%s: a sourced assumption must name its source" % name)
            if q.get("applicability_condition") and not q.get("condition_status"):
                problems.append("%s: states an applicability condition but not whether it holds" % name)
        if q.get("evidence_status") == "physically_tested":
            problems.append("%s: claims physical testing, but this project has no measurement" % name)
        if "value" not in q or not q.get("unit") or not q.get("definition"):
            problems.append("%s: needs a value, a unit and a definition" % name)

        anchor = q.get("code_anchor")
        if not anchor:
            continue
        path = ROOT / anchor["file"]
        if not path.exists():
            problems.append("%s: code anchor %s does not exist" % (name, anchor["file"]))
            continue
        symbol, want = anchor["symbol"], q["value"]
        consts = literal_constants(path)
        if symbol in consts:
            if consts[symbol] != want:
                problems.append("%s: register says %s = %r, %s says %r"
                                % (name, symbol, want, anchor["file"], consts[symbol]))
            continue
        defaults = keyword_defaults(path).get(symbol)
        if defaults is None:
            problems.append("%s: %s defines no constant or defaulted argument %s"
                            % (name, anchor["file"], symbol))
        elif defaults != {want}:
            problems.append("%s: register says %s = %r, %s defaults to %s"
                            % (name, symbol, want, anchor["file"], sorted(defaults)))

    if problems:
        print("Canonical quantity register: FAIL")
        for p in problems:
            print("  -", p)
        return 1
    anchored = sum(1 for q in doc["quantities"].values() if q.get("code_anchor"))
    print("Canonical quantity register: PASS (%d quantities, %d checked against code)"
          % (len(doc["quantities"]), anchored))
    return 0


if __name__ == "__main__":
    sys.exit(check())
