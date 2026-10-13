# A finite counterexample to ideal-cardinality homomesy on fences

For the paper's fence `F̆(3^11)`, with 32 vertices and 11 segments, the lower ideal `{5,6,7,8,12}` has least rowmotion period **237** and orbit cardinality sum **3774**. Its mean is **1258/79**, not 16. This disproves Elizalde–Plante–Roby–Sagan, *Rowmotion on fences*, Conjecture 5.4(b). No claim is made against part (a) or about the smallest counterexample.

The parameter of each maximal-chain segment is its number of unshared vertices plus one. The explicit cover relations and the complete 237-state certificate appear in the manuscript.

## Contents

- `manuscript/main.pdf` and `manuscript/main.tex`: English short note, with the entire hexadecimal certificate in the appendix.
- `中文简述.md`: Chinese explanation of the result and verification limits.
- `data/orbit.csv`: all 237 ideals, cardinalities, maximal antichains, and masks.
- `checker/check.py`: standalone standard-library Python checker.
- `lean/`: the four unchanged proof modules, pinned versions, build script, and reproduction instructions.
- `verification/`: actual checking output, Lean build log and axiom audit, and PDF checks.
- `REFERENCES_AND_SCOPE.md` and `ATTRIBUTION.md`: sources, literature boundary, and attribution status.
- `PUBLIC_FILES.txt`, `SHA256SUMS`, and `make_release.py`: exact distribution allowlist, hashes, and a local packaging script.

## Verify the finite counterexample

From this directory, with Python 3:

```text
python checker/check.py
```

The checker reads the distributed certificate, constructs the fence order from the directed path, and checks all ideal and rowmotion conditions, distinctness, closure, least period, sum, and agreement with the Lean literals. It uses exact integers and rational arithmetic.

## Verify the Lean proof

See `lean/README.md`. Lean is fixed at 4.19.0 and mathlib at `c44e0c8ee63ca166450922a373c7409c5d26b00b`; all nine dependency revisions are locked. A conventional setup is:

```text
cd lean
lake exe cache get
lake build
```

The actual local validation rebuilt all four modules with existing caches at the pinned revisions. Network acquisition and a clean-machine bootstrap were not tested. The portable PowerShell script can check and reuse an explicitly supplied cache read-only.

**Trust boundary:** finite orbit certificates use `native_decide`. The final counterexample theorem depends on `propext`, `Classical.choice`, `Lean.ofReduceBool`, and `Quot.sound`. `Lean.ofReduceBool` adds trust in native evaluation and the Lean compiler. This is not a completed kernel-reduction-only proof. The final proof sources have no `sorry`, `admit`, or custom unproved mathematical axioms; the final axiom audit has no `sorryAx`.

## Rebuild the note and check the distribution

With a LaTeX installation containing the packages named in the preamble, run twice from `manuscript/`:

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

No external bibliography database is required. The saved PDF was exported using pdfTeX 1.40.25 (MiKTeX 24.1). The source also compiled with the editor compiler. On this machine `latexmk` could not run because Perl was absent, so the successful export used direct `pdflatex` passes. There are no unresolved references or overfull boxes in the final LaTeX log; environment-maintenance notices are recorded in the PDF verification report.

From the package root, check the exact released bytes against their hashes:

```text
python make_release.py --check
```

For a deliberate new local package after edits, run `python make_release.py`. It regenerates hashes and creates `_release/W04_fence.zip` from **only** the explicit allowlist. The hash file covers every distributed file except itself; it is an integrity record, not a digital signature. Local build products and any files absent from the allowlist are excluded.

## Scope and disclosure

This work was prepared with AI assistance. It has not been certified as externally human peer reviewed or as the first discovery. The 2025 Mertin dissertation's official record and abstract were checked, but its full-text download returned HTTP 403 and its contents remain unverified. See the source report for the narrower, completed literature checks. The manuscript is signed Aurantium (GitHub account Aurantium-47); no additional reuse license for the new work is provided at present. See `ATTRIBUTION.md`.
