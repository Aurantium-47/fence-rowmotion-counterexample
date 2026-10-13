# Lean verification record

Date: 2026-10-13.

The publication copy was built successfully with `lean/build.ps1`: all four proof modules and the `W04.lean` library entry point were compiled from their copied source files. The command exited with code 0. The full actual output is in `lean_build.log`; printed axiom dependencies extracted from that output are in `lean_axioms.log`.

The build used Lean 4.19.0, release commit `6caaee842e94`, for `x86_64-w64-windows-gnu`. It read an explicitly supplied dependency packages directory without modifying it. The script verified the Git revision of every dependency against the fixed manifest. It wrote this project's compiled outputs under `lean/.lake/build/`; those files are excluded from the source distribution.

All four publication proof files were compared directly as byte arrays with the verified reference proof files and are identical. Per-file byte counts and both SHA-256 values are in `lean_evidence.json`. The publication manifest retains every original dependency revision and uses the project name `w04_fence`.

`W04.paper_fence_counterexample` and the final orbit theorems depend on `propext`, `Classical.choice`, `Lean.ofReduceBool`, and `Quot.sound`. The orbit certificates use `native_decide`, so the trusted computation includes Lean's native evaluator and compiler; this is not a pure kernel-reduction proof. The segment correspondence theorems do not use `Lean.ofReduceBool`. No completed proof source contains `sorry`, `admit`, `sorryAx`, or an unproved custom mathematical axiom.

The build has two `unnecessarySimpa` style warnings in `Poset.lean`, and no errors. The unchanged source is retained rather than editing it solely to suppress warnings.

The supplied Lake configuration and manifest are portable and fixed. This validation did **not** acquire dependencies from a fresh network environment and did **not** execute the conventional `lake build` command; it compiled the project using the provided build script with existing caches. A fresh-network Lake bootstrap is therefore not claimed as tested. No remote publication was performed by this verification.
