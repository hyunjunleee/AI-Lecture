#!/usr/bin/env python3
from __future__ import annotations
import fnmatch, hashlib, json, os, re, shlex, sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
VERDICTS = {"PASS", "FAIL"}
REPAIR_CHANNELS = {"tex-writer", "researcher", "theory-curator", "literature-gate", "manual_decision"}
WEB_AGENTS = {"researcher", "theory-curator", "literature-gate"}
BLOCKED_SHELL_FRAGMENTS = [";", "&&", "||", "|", "`", "$(", ">", "<", "\n", "\r"]

# The three blank-slate gates (read/claim/model) each may Read ONLY the lecture .tex
# (audit target) and their OWN gate log. theory.md, typeset report, spec/, research.md,
# OTHER gates' logs, logs/**, .claude/** are all blocked: each auditor reconstructs
# meaning purely from the .tex with no source/theory/peer context. (Digests of
# lecture_tex / typeset_report are computed via `sha256sum`, which hashes without reading.)
GATE_LOGS = {
    "read-gate": "read_gate",
    "claim-gate": "claim_gate",
    "model-gate": "model_gate",
}

WRITE_OWNERS: List[Tuple[str, str]] = [
    ("work/lecture[0-9][0-9]_research.md", "researcher"),
    ("work/lecture[0-9][0-9]_research_supplement_[0-9][0-9].md", "researcher"),
    ("work/lecture[0-9][0-9]_theory.md", "theory-curator"),
    ("work/lecture[0-9][0-9]_theory_supplement_[0-9][0-9].md", "theory-curator"),
    ("output/lecture[0-9][0-9].tex", "tex-writer"),
    ("output/typeset_check_[0-9][0-9]_round[0-9][0-9].md", "typeset-checker"),
    ("output/typeset_check_[0-9][0-9].md", "typeset-checker"),
    ("output/final_pdftotext_check_[0-9][0-9].md", "typeset-checker"),
    ("output/read_gate_[0-9][0-9]*.jsonl", "read-gate"),
    ("output/claim_gate_[0-9][0-9]*.jsonl", "claim-gate"),
    ("output/model_gate_[0-9][0-9]*.jsonl", "model-gate"),
    ("output/literature_gate_[0-9][0-9]*.jsonl", "literature-gate"),
]

def out(decision: str, reason: str) -> None:
    print(json.dumps({"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":decision,"permissionDecisionReason":reason}}, ensure_ascii=False))
    raise SystemExit(0)

def allow(reason: str) -> None: out("allow", reason)
def deny(reason: str) -> None: out("deny", reason)

def norm(p: Any) -> str:
    s = str(p or "").strip().replace("\\", "/")
    if s.startswith("./"):
        s = s[2:]
    if len(s) > 1:
        s = s.rstrip("/")  # tolerate a trailing slash (e.g. "output/") without flagging it unsafe
    return s

def safe(p: str) -> bool:
    p = norm(p)
    return bool(p) and not p.startswith(("/", "~")) and all(x not in {"", ".", ".."} for x in p.split("/"))

def file_sha(cwd: str, rel: str) -> str:
    if not safe(rel): deny(f"unsafe digest path: {rel}")
    full = (Path(cwd) / norm(rel)).resolve()
    root = Path(cwd).resolve()
    try:
        full.relative_to(root)
    except Exception:
        deny(f"digest path escapes project root: {rel}")
    if not full.is_file():
        deny(f"digest target does not exist: {rel}")
    import hashlib
    h = hashlib.sha256()
    with full.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def m(pat: str, p: str) -> bool: return fnmatch.fnmatchcase(norm(p), pat)

def require_agent(agent: str, expected: str, target: str) -> None:
    if agent == expected: return
    if not agent or agent == "unknown": deny(f"Cannot verify owner for {target}: agent_type missing. Expected {expected}. Fail-closed.")
    deny(f"Only {expected} may operate on {target}; got {agent}.")

def read_old(path: str, cwd: str) -> str:
    full = Path(cwd) / path
    if not full.exists(): return ""
    try: return full.read_text(encoding="utf-8")
    except UnicodeDecodeError: deny(f"Existing JSONL is not UTF-8: {path}")

def appended_obj(old: str, new: str, path: str) -> Dict[str, Any]:
    if not new.startswith(old): deny(f"{path} must preserve existing content as an exact prefix.")
    added = new[len(old):]
    lines = [x for x in added.splitlines() if x.strip()]
    if len(lines) != 1: deny(f"{path} must append exactly one non-empty compact JSON line; got {len(lines)}.")
    try: obj = json.loads(lines[0])
    except Exception as e: deny(f"{path} appended line is not valid JSON: {e}")
    if not isinstance(obj, dict): deny(f"{path} appended JSON item must be an object.")
    return obj

def actual_sha256(cwd: str, path: str) -> str:
    if not safe(path):
        deny(f"unsafe input path for sha256 validation: {path}")
    full = (Path(cwd) / norm(path)).resolve()
    root = Path(cwd).resolve()
    try:
        full.relative_to(root)
    except Exception:
        deny(f"input path escapes project root: {path}")
    if not full.is_file():
        deny(f"input file does not exist for digest validation: {path}")
    h = hashlib.sha256()
    with full.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def check_inputs(obj: Dict[str, Any], keys: Any, cwd: str) -> None:
    inp = obj.get("inputs")
    if not isinstance(inp, dict): deny("gate JSON requires inputs object.")
    expected = keys if isinstance(keys, dict) else {k: None for k in keys}
    for k, expected_path in expected.items():
        item = inp.get(k)
        if not isinstance(item, dict): deny(f"missing inputs.{k} object.")
        p, h = item.get("path"), item.get("sha256")
        if not isinstance(p, str) or not safe(p): deny(f"inputs.{k}.path must be a safe relative path.")
        if expected_path is not None and norm(p) != expected_path:
            deny(f"inputs.{k}.path must be {expected_path}, got {p}")
        if not isinstance(h, str) or not HEX64.match(h): deny(f"inputs.{k}.sha256 must be a 64-hex digest.")
        actual = actual_sha256(cwd, p)
        if actual.lower() != h.lower():
            deny(f"inputs.{k}.sha256 mismatch for {p}: declared {h}, actual {actual}")

def check_dirs(obj: Dict[str, Any], stall_ids: set[str]) -> None:
    dirs = obj.get("revision_directives", [])
    if not isinstance(dirs, list): deny("revision_directives must be a list.")
    if obj.get("verdict") == "FAIL" and not dirs: deny("FAIL requires at least one revision directive.")
    for d in dirs:
        if not isinstance(d, dict): deny("revision_directives items must be objects.")
        if not isinstance(d.get("directive_id"), str) or not d.get("directive_id"): deny("directive_id required.")
        refs = d.get("refs", [])
        if not isinstance(refs, list) or not all(isinstance(x, str) for x in refs): deny("refs must be a list of strings.")
        miss = set(refs) - stall_ids
        if miss: deny(f"revision directive references unknown stalls: {sorted(miss)}")

def check_stall(st: Dict[str, Any]) -> None:
    for f in ["stall_id", "loc", "why", "fix", "repair_channel"]:
        if not isinstance(st.get(f), str) or not st.get(f): deny(f"stall missing non-empty string field {f}.")
    if st["repair_channel"] not in REPAIR_CHANNELS: deny(f"invalid repair_channel: {st['repair_channel']}")
    ck = st.get("canonical_key")
    if not isinstance(ck, dict): deny("stall requires canonical_key object.")
    if ck.get("repair_channel") is not None and ck.get("repair_channel") != st["repair_channel"]: deny("canonical_key.repair_channel mismatch.")
    if st["repair_channel"] in {"researcher", "theory-curator"} and (not st.get("research_question") or not st.get("minimum_acceptance")):
        deny(f"{st['repair_channel']} stall requires research_question and minimum_acceptance.")

def math_stalls(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    sections = obj.get("sections", [])
    if not isinstance(sections, list): deny("math gate sections must be a list.")
    out: List[Dict[str, Any]] = []
    for sec in sections:
        if not isinstance(sec, dict): deny("sections items must be objects.")
        stalls = sec.get("stalls", [])
        if not isinstance(stalls, list): deny("sections[].stalls must be a list.")
        for st in stalls:
            if not isinstance(st, dict): deny("stall must be object.")
            out.append(st)
    return out

def validate_gate(obj: Dict[str, Any], path: str, cwd: str) -> None:
    mm = re.match(r"^output/(read_gate|claim_gate|model_gate)_(\d{2})(?:_r\d+)?\.jsonl$", norm(path))
    if not mm: deny("gate log path must be output/{read_gate|claim_gate|model_gate}_NN(.jsonl or _rRR.jsonl)")
    prefix, nn = mm.group(1), mm.group(2)
    expected_schema = {"read_gate": "read-gate-v1", "claim_gate": "claim-gate-v1", "model_gate": "model-gate-v1"}[prefix]
    if obj.get("schema_version") != expected_schema: deny(f"{prefix} log requires schema_version == '{expected_schema}'.")
    if obj.get("lecture") != nn: deny(f"gate log lecture must be {nn}")
    if not isinstance(obj.get("iter"), int) or obj.get("iter") < 1: deny("iter must be a positive integer.")
    check_inputs(obj, {
        "lecture_tex": f"output/lecture{nn}.tex",
        "typeset_report": f"output/typeset_check_{nn}.md",
    }, cwd)
    if obj.get("verdict") not in VERDICTS: deny("verdict must be PASS or FAIL.")
    stalls = math_stalls(obj)
    if obj.get("stall_count") != len(stalls): deny("stall_count does not match actual stalls.")
    seen=set()
    for st in stalls:
        check_stall(st)
        if st["stall_id"] in seen: deny(f"duplicate stall_id: {st['stall_id']}")
        seen.add(st["stall_id"])
        if st.get("repair_channel") != "tex-writer": deny("gate stalls must route to tex-writer (repair_channel='tex-writer'); deciding whether further research/theory work is needed is tex-writer's call, not the gate's.")
        if prefix in ("read_gate", "model_gate") and st.get("principle") not in {"A", "B", "C"}: deny(f"{prefix} stall principle must be A, B, or C.")
        if prefix == "model_gate" and (not isinstance(st.get("object_or_block"), str) or not st.get("object_or_block")): deny("model gate stall requires object_or_block.")
        if prefix == "claim_gate":
            for fld in ("claim_text", "trigger_type", "failed_test"):
                if not isinstance(st.get(fld), str) or not st.get(fld): deny(f"claim gate stall requires {fld}.")
    if obj["verdict"] == "PASS" and obj.get("stall_count") != 0: deny("PASS requires stall_count == 0.")
    gc = obj.get("global_checks")
    if not isinstance(gc, dict): deny("global_checks object required.")
    if obj["verdict"] == "PASS" and any(v is False for v in gc.values()): deny("PASS cannot have false global_checks.")
    check_dirs(obj, {st["stall_id"] for st in stalls})
    ev=obj.get("evidence")
    if not isinstance(ev, dict): deny("evidence object required.")
    if obj["verdict"] == "PASS":
        key = "audited_claims" if prefix == "claim_gate" else "audited_sections"
        if not isinstance(ev.get(key), list) or not ev.get(key): deny(f"PASS requires evidence.{key} non-empty.")

def lit_stalls(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    sections = obj.get("sections", [])
    if not isinstance(sections, list): deny("literature sections must be a list.")
    out: List[Dict[str, Any]] = []
    for sec in sections:
        if not isinstance(sec, dict): deny("sections items must be objects.")
        stalls = sec.get("stalls", [])
        if not isinstance(stalls, list): deny("sections[].stalls must be a list.")
        for st in stalls:
            if not isinstance(st, dict): deny("literature stall must be object.")
            out.append(st)
    return out

def validate_lit(obj: Dict[str, Any], path: str, cwd: str) -> None:
    if obj.get("schema_version") != "literature-gate-source-fidelity": deny("literature gate JSON requires schema_version == 'literature-gate-source-fidelity'.")
    mm = re.match(r"^output/literature_gate_(\d{2})(?:_r\d+)?\.jsonl$", norm(path))
    if not mm: deny("literature gate log path must be output/literature_gate_NN(.jsonl or _rRR.jsonl)")
    nn = mm.group(1)
    if obj.get("lecture") != nn: deny(f"literature gate lecture must be {nn}")
    if not isinstance(obj.get("iter"), int) or obj.get("iter") < 1: deny("iter must be a positive integer.")
    mode = obj.get("mode")
    if mode == "dossier":
        check_inputs(obj, {"research_md": f"work/lecture{nn}_research.md", "theory_md": f"work/lecture{nn}_theory.md"}, cwd)
    elif mode == "lecture":
        check_inputs(obj, {"research_md": f"work/lecture{nn}_research.md", "theory_md": f"work/lecture{nn}_theory.md", "lecture_tex": f"output/lecture{nn}.tex"}, cwd)
    else: deny("literature mode must be dossier or lecture.")
    if obj.get("verdict") not in VERDICTS: deny("literature verdict must be PASS or FAIL.")
    stalls = lit_stalls(obj)
    if obj.get("stall_count") != len(stalls): deny("literature stall_count does not match actual stalls.")
    seen=set()
    for st in stalls:
        check_stall(st)
        if st["stall_id"] in seen: deny(f"duplicate stall_id: {st['stall_id']}")
        seen.add(st["stall_id"])
        if not isinstance(st.get("fidelity_axis"), str) or not st.get("fidelity_axis"):
            deny("literature stall requires fidelity_axis.")
        if mode == "lecture" and not st.get("claim_id") and not st.get("document_level"): deny("lecture-mode stall requires claim_id or document_level:true.")
    if obj["verdict"] == "PASS" and obj.get("stall_count") != 0: deny("PASS requires stall_count == 0.")
    gc = obj.get("global_checks")
    if not isinstance(gc, dict): deny("global_checks object required.")
    if obj["verdict"] == "PASS" and any(v is False for v in gc.values()): deny("PASS cannot have false global_checks.")
    check_dirs(obj, {st["stall_id"] for st in stalls})
    ev=obj.get("evidence")
    if not isinstance(ev, dict): deny("evidence object required.")
    if obj["verdict"] == "PASS" and not isinstance(ev.get("checked_claim_ids"), list):
        deny("PASS requires evidence.checked_claim_ids list.")

def gate_append_content(tool: str, ti: Dict[str, Any], old: str) -> str:
    # A gate log is updated either by Write (content = full new file) or by Edit
    # (old_string/new_string applied to the current file). For Edit we reconstruct
    # the resulting file so the SAME exact-prefix + single-new-line validation runs:
    # this lets a gate append by reproducing only the last line (not the whole log,
    # which becomes infeasible to hand-transcribe as iterations accumulate), while
    # append-only is still enforced downstream by appended_obj (the reconstructed
    # result must keep the old content as an exact prefix and add exactly one line).
    if tool == "Write":
        content = ti.get("content")
        if not isinstance(content, str): deny("gate log Write requires string content.")
        return content
    os_, ns_ = ti.get("old_string"), ti.get("new_string")
    if not isinstance(os_, str) or not isinstance(ns_, str): deny("gate log Edit requires string old_string and new_string.")
    if not os_: deny("gate log Edit old_string must be non-empty.")
    if old.count(os_) != 1: deny("gate log Edit old_string must match the current file exactly once.")
    return old.replace(os_, ns_)

def handle_write(tool: str, ti: Dict[str, Any], agent: str, cwd: str) -> None:
    raw = str(ti.get("file_path", "") or "").strip().replace("\\", "/")
    if not agent or agent == "unknown":
        try:
            abs_root = Path(cwd).resolve()
            rel = Path(raw).resolve().relative_to(abs_root)
            if not rel.parts: deny(f"orchestrator {tool} path resolves to project root: {raw!r}")
            opath = "/".join(rel.parts)
        except Exception:
            deny(f"orchestrator path invalid or escapes project root: {raw!r}")
        if m("spec/**", opath) or m("template/**", opath):
            deny(f"{tool} to spec/ or template/ is forbidden: {opath}")
        if is_gate(opath):
            deny(f"gate logs are append-only audit artifacts; only the owning gate subagent may write them, not the orchestrator: {opath}")
        if m("work/**", opath) or m("output/**", opath):
            deny(f"orchestrator may not directly write agent artifacts: {opath}. All work/** and output/** content is authored by the owning subagent (researcher/theory-curator/tex-writer/typeset-checker/gates) — orchestrate, don't author.")
        allow(f"orchestrator {tool} accepted: {opath}")
    # Subagent tools pass an absolute file_path; normalize it to a project-relative
    # path so ownership/safety checks operate uniformly (the orchestrator branch
    # above already does this for itself). An absolute path outside the project
    # root is rejected.
    if raw.startswith("/"):
        try:
            rel = Path(raw).resolve().relative_to(Path(cwd).resolve())
            if not rel.parts: deny(f"{tool} path resolves to project root: {raw!r}")
            raw = "/".join(rel.parts)
        except Exception:
            deny(f"{tool} path is absolute and escapes project root: {raw!r}")
    path = norm(raw)
    if not safe(path): deny(f"unsafe or missing file_path: {path!r}")
    if m("spec/**", path) or m("template/**", path): deny(f"{tool} to spec/ or template/ is forbidden: {path}")
    # Blank-slate gates carry Write+Edit, but their mutation scope is confined to their
    # OWN gate log (base or per-round file) — never another gate's log, the .tex, or any
    # other file. Ownership below already enforces this, but make it explicit and tool-
    # agnostic (covers both Write and Edit) so the blank-slate boundary is unambiguous.
    if agent in GATE_LOGS:
        own = GATE_LOGS[agent]
        if not re.match(rf"^output/{own}_\d{{2}}(?:_r\d+)?\.jsonl$", path):
            deny(f"{agent} is a blank-slate gate; {tool} is allowed only on its own output/{own}_NN(.jsonl or _rRR.jsonl), not {path}.")
    owner = None
    for pat, ag in WRITE_OWNERS:
        if m(pat, path): owner = ag; break
    if owner is None: deny(f"No pipeline role owns {tool} target path: {path}")
    require_agent(agent, owner, path)
    if re.match(r"^output/(?:read_gate|claim_gate|model_gate)_\d{2}(?:_r\d+)?\.jsonl$", path):
        old = read_old(path, cwd)
        validate_gate(appended_obj(old, gate_append_content(tool, ti, old), path), path, cwd); allow("gate JSONL append accepted")
    if m("output/literature_gate_[0-9][0-9]*.jsonl", path):
        old = read_old(path, cwd)
        validate_lit(appended_obj(old, gate_append_content(tool, ti, old), path), path, cwd); allow("literature gate JSONL append accepted")
    allow(f"{tool} path ownership accepted")

def parse(command: str) -> List[str]:
    if not isinstance(command, str) or not command.strip(): deny("empty Bash command.")
    for frag in BLOCKED_SHELL_FRAGMENTS:
        if frag in command: deny(f"Bash command contains blocked shell fragment {frag!r}.")
    try: return shlex.split(command)
    except ValueError as e: deny(f"Bash command cannot be parsed safely: {e}")

def req_paths(paths: List[str]) -> None:
    for p in paths:
        if not safe(p): deny(f"unsafe Bash path: {p}")

def lecno(s: str) -> str:
    mm = re.search(r"lecture(\d{2})", s)
    return mm.group(1) if mm else ""

def is_research(p): return bool(re.match(r"^work/lecture\d{2}_research(?:_supplement_\d{2})?\.md$", norm(p)))
def is_theory(p): return bool(re.match(r"^work/lecture\d{2}_theory(?:_supplement_\d{2})?\.md$", norm(p)))
def is_tex(p): return bool(re.match(r"^output/lecture\d{2}\.tex$", norm(p)))
def is_pdf(p): return bool(re.match(r"^output/lecture\d{2}\.pdf$", norm(p)))
def is_txt(p): return bool(re.match(r"^output/lecture\d{2}(?:_final)?\.txt$", norm(p)))
def is_log(p): return bool(re.match(r"^output/lecture\d{2}\.log$", norm(p)))
def is_build_log(p): return bool(re.match(r"^output/build/lecture\d{2}_round\d{2}/lecture\d{2}\.log$", norm(p)))
def is_build_pdf(p): return bool(re.match(r"^output/build/lecture\d{2}_round\d{2}/lecture\d{2}\.pdf$", norm(p)))
def is_report(p): return bool(re.match(r"^output/typeset_check_\d{2}(?:_round\d{2})?\.md$", norm(p))) or bool(re.match(r"^output/final_pdftotext_check_\d{2}\.md$", norm(p)))
def is_gate(p): return bool(re.match(r"^output/(?:gate_log|literature_gate|read_gate|claim_gate|model_gate)_\d{2}(?:_r\d+)?\.jsonl$", norm(p)))

def check_sha(argv: List[str]) -> None:
    if argv[0] != "sha256sum" or len(argv) < 2: deny("sha256sum requires paths.")
    paths = [norm(x) for x in argv[1:]]; req_paths(paths)
    for p in paths:
        if not (is_research(p) or is_theory(p) or is_tex(p) or is_pdf(p) or is_txt(p) or is_log(p) or is_report(p) or is_gate(p)):
            deny(f"sha256sum path not allowed: {p}")

def check_typeset(argv: List[str]) -> None:
    cmd = argv[0]
    if cmd == "sha256sum": check_sha(argv); return
    if cmd == "mkdir":
        if len(argv) != 3 or argv[1] != "-p": deny("mkdir allowed only as mkdir -p output/build|preview/lectureNN_roundRR")
        p = norm(argv[2]); req_paths([p])
        if not re.match(r"^output/(?:build|preview)/lecture\d{2}_round\d{2}$", p): deny(f"mkdir path not allowed: {p}")
        return
    if cmd == "xelatex":
        if len(argv) != 6: deny("xelatex must use exact safe form.")
        if set(argv[1:4]) != {"-interaction=nonstopmode", "-halt-on-error", "-file-line-error"}: deny("xelatex options not allowed.")
        if not argv[4].startswith("-output-directory="): deny("xelatex requires -output-directory=...")
        outdir, tex = norm(argv[4].split("=",1)[1]), norm(argv[5]); req_paths([outdir, tex])
        if not re.match(r"^output/build/lecture\d{2}_round\d{2}$", outdir): deny(f"xelatex output dir not allowed: {outdir}")
        if not is_tex(tex) or lecno(outdir) != lecno(tex): deny("xelatex lecture mismatch or invalid tex path.")
        return
    if cmd == "tail":
        if len(argv) != 3 or argv[1] not in {"-20", "-40", "-80"}: deny("tail allowed only with -20|-40|-80 and build log.")
        p = norm(argv[2]); req_paths([p])
        if not is_build_log(p): deny(f"tail path not allowed: {p}")
        return
    if cmd == "grep":
        if len(argv) < 3: deny("grep requires pattern and path.")
        p = norm(argv[-1]); req_paths([p])
        if not (is_tex(p) or is_build_log(p) or is_txt(p)): deny(f"grep path not allowed: {p}")
        opts = [x for x in argv[1:-2] if x.startswith("-")]
        if any(o not in {"-n", "-c", "-cF", "-nE", "-nF"} for o in opts): deny(f"grep option not allowed: {opts}")
        return
    if cmd == "cp":
        if len(argv) != 3: deny("cp allowed only with one source and one destination.")
        src, dst = norm(argv[1]), norm(argv[2]); req_paths([src, dst])
        if is_build_pdf(src) and is_pdf(dst) and lecno(src) == lecno(dst): return
        if is_build_log(src) and is_log(dst) and lecno(src) == lecno(dst): return
        deny(f"cp form not allowed: {src} -> {dst}")
    if cmd == "pdftotext":
        if len(argv) != 4 or argv[1] != "-layout": deny("pdftotext allowed only as pdftotext -layout output/lectureNN.pdf output/lectureNN(.|_final).txt")
        pdf, txt = norm(argv[2]), norm(argv[3]); req_paths([pdf, txt])
        if not (is_pdf(pdf) and is_txt(txt) and lecno(pdf) == lecno(txt)): deny(f"pdftotext paths not allowed: {pdf} -> {txt}")
        return
    if cmd == "pdftoppm":
        if len(argv) != 5 or argv[1] != "-r" or argv[2] != "120": deny("pdftoppm allowed only as pdftoppm -r 120 output/lectureNN.pdf output/preview/lectureNN_roundRR/p")
        pdf, prefix = norm(argv[3]), norm(argv[4]); req_paths([pdf, prefix])
        if not is_pdf(pdf) or not re.match(r"^output/preview/lecture\d{2}_round\d{2}/p$", prefix) or lecno(pdf) != lecno(prefix): deny("pdftoppm paths not allowed.")
        return
    if cmd == "ls":
        if len(argv) != 2: deny("ls allowed only with one preview directory.")
        p = norm(argv[1]); req_paths([p])
        if not re.match(r"^output/preview/lecture\d{2}_round\d{2}$", p): deny(f"ls path not allowed: {p}")
        return
    if cmd == "wc":
        if len(argv) != 3 or argv[1] != "-l": deny("wc allowed only as wc -l output/lectureNN(.|_final).txt")
        p = norm(argv[2]); req_paths([p])
        if not is_txt(p): deny(f"wc path not allowed: {p}")
        return
    deny(f"Bash command not allowed for typeset-checker: {cmd}")

def handle_read(ti: Dict[str, Any], agent: str, cwd: str) -> None:
    # Only the three blank-slate gates are restricted; every other agent's Read falls through.
    if agent not in GATE_LOGS:
        return
    own = GATE_LOGS[agent]  # e.g. "read_gate"
    raw = str(ti.get("file_path", "") or "").strip().replace("\\", "/")
    if raw.startswith("/"):
        try:
            rel = Path(raw).resolve().relative_to(Path(cwd).resolve())
            raw = "/".join(rel.parts)
        except Exception:
            deny(f"{agent} Read path is absolute and escapes project root: {raw!r}")
    path = norm(raw)
    if not safe(path):
        deny(f"{agent} unsafe Read path: {path!r}")
    if re.match(r"^output/lecture\d{2}\.tex$", path) or re.match(rf"^output/{own}_\d{{2}}(?:_r\d+)?\.jsonl$", path):
        allow(f"{agent} Read whitelisted: {path}")
    deny(f"{agent} may Read only output/lecture<NN>.tex and its own output/{own}_<NN>.jsonl. (theory.md, typeset report, spec/, research.md, other gates' logs, .claude/ all blocked — blank-slate auditor. Use sha256sum, not Read, for digests.)")


def handle_bash(ti: Dict[str, Any], agent: str) -> None:
    if not agent or agent == "unknown":
        argv = parse(ti.get("command", ""))
        cmd = argv[0] if argv else ""
        if cmd == "sha256sum":
            req_paths([norm(x) for x in argv[1:]]); allow("orchestrator sha256sum accepted")
        if cmd == "mkdir" and len(argv) >= 2 and argv[1] == "-p":
            req_paths([norm(x) for x in argv[2:]]); allow("orchestrator mkdir accepted")
        if cmd == "ls":
            req_paths([norm(x) for x in argv[1:]]); allow("orchestrator ls accepted")
        if cmd in {"python3", "python"} and len(argv) >= 3 and argv[1] == "-m" and argv[2] == "py_compile":
            allow("orchestrator py_compile accepted")
        deny(f"orchestrator Bash restricted to sha256sum/mkdir/ls/py_compile; got {cmd!r}.")
    argv = parse(ti.get("command", ""))
    if agent == "typeset-checker": check_typeset(argv); allow("typeset-checker Bash command accepted")
    if agent in {"read-gate", "claim-gate", "model-gate", "literature-gate"}:
        if argv[0] != "sha256sum": deny(f"{agent} may use Bash only for sha256sum.")
        check_sha(argv); allow(f"{agent} sha256sum accepted")
    deny(f"Bash is not allowed for agent {agent}.")

def main() -> None:
    try: data = json.load(sys.stdin)
    except Exception as e: deny(f"hook input is not valid JSON: {e}")
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    agent = data.get("agent_type") or data.get("agent_name") or data.get("subagent_type") or "unknown"
    cwd = data.get("cwd") or os.getcwd()
    if tool in {"Write", "Edit"}: handle_write(tool, ti, str(agent), cwd)
    if tool == "Read": handle_read(ti, str(agent), cwd)
    if tool == "Bash": handle_bash(ti, str(agent))
    if tool in {"WebSearch", "WebFetch"}:
        if agent in WEB_AGENTS: allow(f"{tool} accepted for {agent}")
        if not agent or agent == "unknown": deny(f"{tool} denied: agent_type missing. Fail-closed.")
        deny(f"{tool} is allowed only for {sorted(WEB_AGENTS)}; got {agent}.")
    allow(f"No pipeline policy for tool {tool}; accepted")

if __name__ == "__main__":
    main()
