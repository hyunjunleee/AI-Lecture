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
GATE_LOG_RE = re.compile(r"(?:^|/)(?:gate_log|literature_gate|read_gate|claim_gate|model_gate)_\d{2}(?:_r\d+)?\.jsonl$")
PROTECTED_PREFIXES = ("spec/", "template/")

# Blank-slate gates: spawn prompt must match the canonical template exactly (whitelist).
BLANK_SLATE_GATE_TYPES = {"read-gate", "claim-gate", "model-gate"}

# Canonical prompt templates for each gate.
# Variables: (\d+) group 1 = NN (lecture number), group 2 = K (iter), group 3 = KK (round).
# \1 backreference ensures NN is consistent throughout the prompt.
_GATE_TEMPLATE_RES: Dict[str, re.Pattern] = {
    "read-gate": re.compile(
        r"(\d+)강 read-gate, iter=(\d+)\.\n"
        r"- output/lecture\1\.tex 읽기\n"
        r"- output/read_gate_\1\.jsonl 읽기 \(자기 이전 로그\)\n"
        r"- output/typeset_check_\1\.md sha256sum만\n"
        r"처음부터 끝까지 순차 독해\. 이름 바인딩·표현식 적형·논리 흐름·누출 전수 감사\.\n"
        r"판정: output/read_gate_\1_r(\d+)\.jsonl에 Write\."
    ),
    "claim-gate": re.compile(
        r"(\d+)강 claim-gate, iter=(\d+)\.\n"
        r"- output/lecture\1\.tex 읽기\n"
        r"- output/claim_gate_\1\.jsonl 읽기 \(자기 이전 로그\)\n"
        r"- output/typeset_check_\1\.md sha256sum만\n"
        r"처음부터 끝까지 순차 독해\. load-bearing 주장 전수 열거·5테스트 감사\.\n"
        r"판정: output/claim_gate_\1_r(\d+)\.jsonl에 Write\."
    ),
    "model-gate": re.compile(
        r"(\d+)강 model-gate, iter=(\d+)\.\n"
        r"- output/lecture\1\.tex 읽기\n"
        r"- output/model_gate_\1\.jsonl 읽기 \(자기 이전 로그\)\n"
        r"- output/typeset_check_\1\.md sha256sum만\n"
        r"처음부터 끝까지 순차 독해\. 모델·객체·계산 블록 완결성 전수 감사\.\n"
        r"판정: output/model_gate_\1_r(\d+)\.jsonl에 Write\."
    ),
}

# Description blacklist: description is UI-only (not agent-facing) but still enforce hygiene.
_DESC_HINT_RE = re.compile(r"이전\s*[Ss]tall|해소\s*여부|\b(?:RG|CG|MG)-\d{2}-\d{3,}\b")


def _check_gate_spawn_contamination(prompt: str, description: str, subagent: str) -> None:
    """Whitelist the prompt against the canonical template; blacklist the description.

    Exits the process via deny() on violation; returns normally when clean.
    """
    # Prompt whitelist: must be exactly the canonical template (NN, K, KK as only variables).
    template_re = _GATE_TEMPLATE_RES.get(subagent)
    if template_re is not None and not template_re.fullmatch(prompt.strip()):
        deny(
            f"blank-slate enforcement: '{subagent}' spawn prompt does not match the canonical "
            f"template. The only accepted form is:\n"
            f"  NN강 {subagent}, iter=K.\\n"
            f"  - output/lectureNN.tex 읽기\\n"
            f"  - output/<log>_NN.jsonl 읽기 (자기 이전 로그)\\n"
            f"  - output/typeset_check_NN.md sha256sum만\\n"
            f"  처음부터 끝까지 순차 독해. <dimension> 전수 감사.\\n"
            f"  판정: output/<log>_NN_rKK.jsonl에 Write.\n"
            f"Any extra content, prior stall context, or deviation is rejected."
        )
    # Description blacklist (UI metadata — not agent-facing, but enforce hygiene).
    m = _DESC_HINT_RE.search(description)
    if m:
        deny(
            f"blank-slate violation: description to {subagent!r} contains contaminating phrase "
            f"({m.group()!r}). Keep description clean."
        )


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


# The orchestrator tunes the PIPELINE (its own machinery) but must NOT author or alter
# ARTIFACTS: every work/** and output/** file is produced solely by its owning subagent
# (researcher / theory-curator / tex-writer / typeset-checker / gates). The orchestrator's
# directly-writable domain is therefore limited to .claude/** (agents, settings, hooks,
# policy), logs/** (its own run narrative), and top-level repo meta (CLAUDE.md, .gitignore,
# README, ...). Anything else falls through to the original policy, which denies orchestrator
# artifact writes and validates subagent writes by ownership.
def is_orchestrator_writable(event: Dict[str, Any]) -> bool:
    cwd = event.get("cwd") or os.getcwd()
    rel = project_relative(mutation_target(event), cwd if isinstance(cwd, str) else os.getcwd())
    if not rel:
        return False
    if rel.startswith(("spec/", "template/", "work/", "output/")):
        return False
    if GATE_LOG_RE.search(rel):
        return False
    if rel.startswith((".claude/", "logs/")):
        return True
    if "/" not in rel:  # top-level repo-meta file
        return True
    return False


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
        # Free mutation only within the orchestrator's own domain (.claude/, logs/, repo
        # meta). Artifact writes (work/**, output/**), spec/template, and gate logs fall
        # through to the original policy. Bash also falls through to the original policy
        # (sha256sum/mkdir/ls/py_compile only) — cp/mv/touch into work/** or output/**
        # would forge artifacts, so the wrapper no longer grants simple-FS Bash here.
        if name in FILE_MUTATION_TOOLS and is_orchestrator_writable(event):
            audit(record, "allow", "main orchestrator domain mutation (.claude/, logs/, repo meta)", "wrapper")
            allow("main orchestrator may mutate only its own domain (.claude/, logs/, top-level repo meta); work/** and output/** artifacts are authored by subagents")

    # Blank-slate gate spawn enforcement: deny Agent calls that inject prior stall context.
    # This runs for both orchestrator and subagent callers; only orchestrator spawns matter
    # in practice but checking both is harmless.
    if name == "Agent":
        subagent = str(ti.get("subagent_type") or "")
        if subagent in BLANK_SLATE_GATE_TYPES:
            prompt = str(ti.get("prompt") or "")
            description = str(ti.get("description") or "")
            _check_gate_spawn_contamination(prompt, description, subagent)
            audit(record, "allow", f"blank-slate gate spawn OK: {subagent}", "wrapper")
            allow(f"blank-slate gate spawn OK — no prior stall context detected: {subagent}")

    # Protected mutations (gate logs, spec/, template/) by the orchestrator — and
    # everything else — fall through to the original policy for validation /
    # fail-closed handling.
    return delegate_to_original(raw, record)


if __name__ == "__main__":
    raise SystemExit(main())
