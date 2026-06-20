#!/usr/bin/env python3
"""Validate current completion state for a lecture number.

Usage:
  python3 .claude/validators/validate_pipeline_state.py 11

This helper is for humans/CI. The Claude Code agents do not need to run it.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path.cwd()
MATH_SCHEMA = "math-gate-source-fidelity"
LIT_SCHEMA = "literature-gate-source-fidelity"


def sha(path: str) -> str:
    p = ROOT / path
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            raise SystemExit(f"{path}:{i}: invalid JSON: {e}")
        if not isinstance(obj, dict):
            raise SystemExit(f"{path}:{i}: JSONL entry is not object")
        rows.append(obj)
    return rows


def inputs_match(obj: Dict[str, Any]) -> bool:
    inputs = obj.get("inputs")
    if not isinstance(inputs, dict):
        return False
    for entry in inputs.values():
        if not isinstance(entry, dict):
            return False
        path = entry.get("path")
        digest = entry.get("sha256")
        if not isinstance(path, str) or not isinstance(digest, str):
            return False
        p = ROOT / path
        if not p.is_file():
            return False
        if sha(path) != digest.lower():
            return False
    return True


def latest_pass(rows: List[Dict[str, Any]], predicate) -> Optional[Dict[str, Any]]:
    for obj in reversed(rows):
        if obj.get("verdict") == "PASS" and predicate(obj) and inputs_match(obj):
            return obj
    return None


def report(name: str, ok: bool, detail: str) -> None:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}: {detail}")


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{2}", sys.argv[1]):
        print("Usage: validate_pipeline_state.py NN", file=sys.stderr)
        return 2
    nn = sys.argv[1]
    lit_rows = read_jsonl(ROOT / f"output/literature_gate_{nn}.jsonl")
    math_rows = read_jsonl(ROOT / f"output/gate_log_{nn}.jsonl")

    dossier = latest_pass(lit_rows, lambda o: o.get("schema_version") == LIT_SCHEMA and o.get("mode") == "dossier")
    lecture = latest_pass(lit_rows, lambda o: o.get("schema_version") == LIT_SCHEMA and o.get("mode") == "lecture")
    math = latest_pass(math_rows, lambda o: o.get("schema_version") == MATH_SCHEMA)

    checks = [
        ("literature dossier gate", dossier is not None, "current digest-bound PASS" if dossier else "missing/stale/FAIL"),
        ("mathematician gate", math is not None, "current digest-bound PASS" if math else "missing/stale/FAIL"),
        ("literature lecture gate", lecture is not None, "current digest-bound PASS" if lecture else "missing/stale/FAIL"),
    ]

    typeset = ROOT / f"output/typeset_check_{nn}.md"
    final = ROOT / f"output/final_pdftotext_check_{nn}.md"
    checks.append(("typeset report", typeset.exists() and "PASS" in typeset.read_text(encoding="utf-8"), str(typeset)))
    checks.append(("final pdftotext report", final.exists() and "PASS" in final.read_text(encoding="utf-8"), str(final)))

    all_ok = True
    for name, ok, detail in checks:
        report(name, ok, detail)
        all_ok = all_ok and ok
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
