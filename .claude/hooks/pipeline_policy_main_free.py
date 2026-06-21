#!/usr/bin/env python3
"""
PreToolUse wrapper for the source-fidelity lecture pipeline.

Intent:
  - Main orchestrator events are allowed to mutate workspace files.
  - Custom subagent events remain governed by the original pipeline_policy.py.

Assumption used by this pipeline:
  - No agent_type/subagent_type field means main orchestrator.
  - Any explicit agent_type/subagent_type means subagent and is delegated.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

# Audit trace: every PreToolUse decision (agent identity, tool, target, verdict)
# is appended here so subagent behaviour can be reconstructed after the fact.
# Failures to write the trace must never break the policy decision itself.
AUDIT_PATH = Path("logs/agent_trace.jsonl")


def audit(record: Dict[str, Any], decision: Optional[str], reason: Optional[str], decided_by: str) -> None:
    try:
        AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
            "agent": (record.get("agent") or "main-orchestrator"),
            "tool": record.get("tool"),
            "target": record.get("target"),
            "decision": decision or "unknown",
            "decided_by": decided_by,
        }
        if reason:
            entry["reason"] = reason
        with AUDIT_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
    except Exception:
        pass

FILE_MUTATION_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
MAIN_FS_BASH_COMMANDS = {"mkdir", "touch", "cp", "mv"}
SHELL_METACHARS = ("|", ";", "&&", "||", "`", "$(", ">", "<", "\n")
# Carve-outs from the "main orchestrator is free to mutate files" rule.
#
# Gate logs are audit artifacts: the orchestrator must NOT be able to append an
# unvalidated (possibly forged-PASS) line. spec/ and template/ are authoritative
# source documents (CLAUDE.md §12) the original policy protects even from the
# orchestrator. Both classes are delegated to the original policy, which denies
# orchestrator writes (and, for gate logs, schema/digest-validates subagent
# writes). Everything else stays freely mutable so the pipeline can be iterated
# on conversationally.
GATE_LOG_RE = re.compile(r"(?:^|/)(?:gate_log|literature_gate)_\d{2}\.jsonl$")
PROTECTED_PREFIXES = ("spec/", "template/")


def emit(decision: str, reason: Optional[str] = None) -> None:
    payload: Dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
        }
    }
    if reason:
        payload["hookSpecificOutput"]["permissionDecisionReason"] = reason
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    raise SystemExit(0)


def allow(reason: str) -> None:
    emit("allow", reason)


def deny(reason: str) -> None:
    emit("deny", reason)


def nested_get(obj: Any, path: Iterable[str]) -> Any:
    cur = obj
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def first_present(values: Iterable[Any]) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def acting_agent_type(event: Dict[str, Any]) -> Any:
    # Be deliberately tolerant of small hook-input schema variations.
    paths = [
        ("agent_type",),
        ("agentType",),
        ("subagent_type",),
        ("subagentType",),
        ("agent", "type"),
        ("agent", "name"),
        ("context", "agent_type"),
        ("context", "agentType"),
        ("context", "subagent_type"),
        ("hook_context", "agent_type"),
        ("hookContext", "agentType"),
        ("metadata", "agent_type"),
        ("tool_input", "agent_type"),
        ("toolInput", "agentType"),
    ]
    return first_present(nested_get(event, path) for path in paths)


def tool_name(event: Dict[str, Any]) -> Optional[str]:
    value = event.get("tool_name") or event.get("toolName")
    return value if isinstance(value, str) else None


def tool_input(event: Dict[str, Any]) -> Dict[str, Any]:
    value = event.get("tool_input") or event.get("toolInput") or {}
    return value if isinstance(value, dict) else {}


def bash_command(event: Dict[str, Any]) -> str:
    value = tool_input(event).get("command", "")
    return value if isinstance(value, str) else ""


def mutation_target(event: Dict[str, Any]) -> str:
    value = tool_input(event).get("file_path", "")
    return str(value or "").replace("\\", "/")


def project_relative(target: str, cwd: str) -> str:
    if target.startswith("/"):
        try:
            rel = Path(target).resolve().relative_to(Path(cwd).resolve())
            return "/".join(rel.parts)
        except Exception:
            return target  # escapes project root; original policy will reject it
    return target[2:] if target.startswith("./") else target


def is_protected_mutation(event: Dict[str, Any]) -> bool:
    cwd = event.get("cwd") or os.getcwd()
    rel = project_relative(mutation_target(event), cwd if isinstance(cwd, str) else os.getcwd())
    if GATE_LOG_RE.search(rel):
        return True
    return rel.startswith(PROTECTED_PREFIXES)


def is_simple_main_fs_bash(command: str) -> bool:
    if not command.strip():
        return False
    if any(mark in command for mark in SHELL_METACHARS):
        return False
    try:
        argv = shlex.split(command)
    except ValueError:
        return False
    if not argv:
        return False
    return Path(argv[0]).name in MAIN_FS_BASH_COMMANDS


def delegate_to_original(raw: bytes, record: Optional[Dict[str, Any]] = None) -> int:
    original = Path(__file__).resolve().with_name("pipeline_policy.py")
    if not original.exists():
        if record is not None:
            audit(record, "deny", "original pipeline policy hook not found", "wrapper")
        deny(f"Original pipeline policy hook not found: {original}")
    proc = subprocess.run(
        [sys.executable, str(original)],
        input=raw,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd(),
    )
    if proc.stdout:
        sys.stdout.buffer.write(proc.stdout)
    if proc.stderr:
        sys.stderr.buffer.write(proc.stderr)
    if record is not None:
        decision, reason = None, None
        try:
            last = proc.stdout.decode("utf-8").strip().splitlines()[-1]
            hso = json.loads(last).get("hookSpecificOutput", {})
            decision = hso.get("permissionDecision")
            reason = hso.get("permissionDecisionReason")
        except Exception:
            pass
        audit(record, decision, reason, "original")
    return proc.returncode


def main() -> int:
    raw = sys.stdin.buffer.read()
    try:
        event = json.loads(raw.decode("utf-8"))
    except Exception:
        return delegate_to_original(raw, {"agent": None, "tool": None, "target": "<unparseable hook input>"})
    if not isinstance(event, dict):
        return delegate_to_original(raw, {"agent": None, "tool": None, "target": "<non-dict hook input>"})

    agent_type = acting_agent_type(event)
    name = tool_name(event)
    is_main_orchestrator = agent_type in (None, "")

    ti = tool_input(event)
    record = {
        "agent": agent_type,
        "tool": name,
        "target": (ti.get("file_path") or ti.get("command") or ti.get("query") or ti.get("url") or ti.get("pattern") or ""),
    }

    if is_main_orchestrator:
        if name in FILE_MUTATION_TOOLS and not is_protected_mutation(event):
            audit(record, "allow", "main orchestrator file mutation allowed (non-protected)", "wrapper")
            allow("main orchestrator file mutation allowed (non-protected)")
        if name == "Bash" and is_simple_main_fs_bash(bash_command(event)):
            audit(record, "allow", "main orchestrator simple filesystem Bash command allowed", "wrapper")
            allow("main orchestrator simple filesystem Bash command allowed")

    # Protected mutations (gate logs, spec/, template/) by the orchestrator — and
    # everything else — fall through to the original policy for validation /
    # fail-closed handling.
    return delegate_to_original(raw, record)


if __name__ == "__main__":
    raise SystemExit(main())
