# Completion checklist

A lecture is complete only if all items below are true for the current files.

1. `work/lectureNN_research.md` exists.
2. `work/lectureNN_theory.md` exists.
3. `output/lectureNN.tex` exists.
4. Latest applicable `literature-gate` dossier PASS has input hashes matching current research/theory files.
5. Latest applicable typeset report is PASS and its lecture tex hash matches current lecture tex.
6. Latest applicable `math-gate` PASS has input hashes matching current lecture tex, theory file, and typeset report.
7. Latest applicable `literature-gate` lecture PASS has input hashes matching current lecture tex, theory file, and research file.
8. `output/final_pdftotext_check_NN.md` is PASS and its hashes match current `output/lectureNN.pdf` and `output/lectureNN.tex`.

If any hash does not match, do not reuse the PASS. Resume at the invalidation graph in `CLAUDE.md`.
