# Policy matrix

| Agent | May read | May write | May edit | May web | May bash |
|---|---|---|---|---|---|
| researcher | spec, work, output logs | `work/lecture*_research*.md` | no | yes | no |
| theory-curator | spec, work, output logs | `work/lecture*_theory*.md` | no | yes | no |
| literature-gate | spec, work, lecture tex, literature logs | `output/literature_gate_*.jsonl` | no | yes | `sha256sum` only |
| tex-writer | spec, template, research, theory, gate reports | `output/lecture*.tex` | `output/lecture*.tex` | no | no |
| typeset-checker | `output/lecture*.tex` | typeset/final reports | no | no | restricted compile/PDF/hash commands |
| mathematician-gate | spec, theory, lecture tex, typeset report | `output/gate_log_*.jsonl` | no | no | `sha256sum` only |

Invariant:

```text
A PASS verdict is valid only for the exact input file hashes recorded in the gate log.
```
