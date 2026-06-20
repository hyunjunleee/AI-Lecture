# Hook policy details

`pipeline_policy.py` is intentionally written as one reference implementation.
The policy itself is match-style: tool name, agent identity, target path, and Bash argv determine allow/deny.

## Fail-closed rule

For `Write`, `Edit`, `Bash`, `WebSearch`, and `WebFetch`, missing `agent_type` means deny. A pipeline that cannot identify the acting subagent should stop rather than guess.

## Bash rule

The hook parses Bash commands with `shlex` and rejects shell metacharacters such as `|`, `;`, `&&`, `||`, backticks, command substitution, and redirection.
Only the command forms listed in `typeset-checker.md` are accepted for `typeset-checker`. `mathematician-gate` and `literature-gate` may use only `sha256sum`.

## JSONL append rule

`output/gate_log_NN.jsonl` and `output/literature_gate_NN.jsonl` are append-only through `Write`:

1. Existing content must be an exact prefix.
2. Exactly one non-empty compact JSON object line may be added.
3. The JSON schema is checked before the write is allowed.
4. The sha256 digests in `inputs` must match the current files.
