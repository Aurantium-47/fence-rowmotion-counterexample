# Kernel verification of the fence counterexample

The counterexample is unchanged: the paper's 32-vertex fence with eleven segments of parameter 3 has a rowmotion orbit of least period 237, cardinality sum 3774, and mean 1258/79, unequal to 16. This disproves only Elizalde–Plante–Roby–Sagan, *Rowmotion on fences*, Conjecture 5.4(b). It makes no claim about part (a), minimality, or priority. The mathematical sources and attribution remain in [REFERENCES_AND_SCOPE.md](../REFERENCES_AND_SCOPE.md) and [ATTRIBUTION.md](../ATTRIBUTION.md).

## Fixed successful version

- Source commit: [`743fb848aa94c16b51dde32db51710a6f9aff598`](https://github.com/Aurantium-47/fence-rowmotion-counterexample/commit/743fb848aa94c16b51dde32db51710a6f9aff598).
- Original verification branch: `verification/fence-kernel-candidate-01`.
- Successful run: [38384896313](https://github.com/Aurantium-47/fence-rowmotion-counterexample/actions/runs/38384896313), attempt 1, [job 115254134890](https://github.com/Aurantium-47/fence-rowmotion-counterexample/actions/runs/38384896313/job/115254134890), completed on 2026-10-13.
- Lean 4.19.0, release commit `6caaee842e94`; mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`; all nine dependency revisions are fixed by `kernel-candidate/lake-manifest.json`.

This page reports that fixed run. A later documentation commit is not an additional proof run.

## Certificate and observed checks

`kernel-candidate/W04/KernelData.lean` contains the literal orbit states and their exact integer encodings. The thirty modules `W04/KernelCert/C00.lean` through `C29.lean` prove the 237 individual transition, encoding, cardinality, and inverse-index certificates with `decide +kernel`. `Orbit.lean` assembles these certificates, and `Main.lean` proves the same complete rowmotion-orbit, least-period, sum, mean, and counterexample statements. The order is the fence partial order, and rowmotion is the downward closure of the minimal complement.

The successful job's actual output establishes:

| Check | Observed result |
|---|---|
| Project compilation | All 39 own Lean source files compiled anew, including the two smoke modules and `Audit.lean`; every compilation exited 0. |
| Own imports | All 39 own imports resolved to the new output directory, with recorded output hashes matching this run. |
| Final audit probe | All 49 specified declarations had their complete types and transitive axiom lists printed; 19 definitions were also printed; the probe exited 0. |
| End assertions | The expected declaration sets, allowed axioms, and source-integrity checks completed, and the final PASS line was printed. |

The union of the 49 observed axiom lists is exactly:

```text
propext, Classical.choice, Quot.sound
```

In particular, the final theorem `W04.paper_fence_counterexample` has those three axioms. None of the 49 lists contains `Lean.ofReduceBool`, `Lean.ofReduceNat`, `sorryAx`, or a custom axiom. This conclusion uses the actual transitive axiom output, rather than a source-text search or the run's success icon alone.

Here, **kernel verification** means that the new finite certificates and final theorem avoid the native-evaluation axioms and passed the observed compilation and axiom audit. The Lean kernel and its standard foundational axioms remain trusted. External libraries were supplied as precompiled caches at fixed source revisions. This run did **not** rebuild all external dependencies from source, replay every dependency proof through the kernel, or check the result with an independent kernel implementation. It is also not external human peer review.

## Reproduction

Obtain the exact checked version, without replacing the pinned dependency manifest:

```sh
git clone https://github.com/Aurantium-47/fence-rowmotion-counterexample.git fence-verification
cd fence-verification
git checkout --detach 743fb848aa94c16b51dde32db51710a6f9aff598
```

The complete procedure actually executed is preserved in the [workflow at that commit](https://github.com/Aurantium-47/fence-rowmotion-counterexample/blob/743fb848aa94c16b51dde32db51710a6f9aff598/.github/workflows/fence-kernel-candidate.yml). It contains the exact dependency fetches, toolchain hashes, cache acquisition, serial compilation order, resource guard, generated 49-declaration probe, import checks, and final assertions. To reproduce the full check, execute its four verification `run` blocks in order on Ubuntu 24.04, respecting their working directories:

1. In an empty workspace, run **Fetch and identify the candidate alongside the unchanged release**, with `CANDIDATE_SHA=743fb848aa94c16b51dde32db51710a6f9aff598`. For execution outside Actions, set `GITHUB_PATH` and `GITHUB_ENV` to new text files in that workspace, then add the emitted toolchain directory to `PATH` and export the emitted `LEAN_SYSROOT` before the next block.
2. In the created `public-source/kernel-candidate` directory, run **Fetch exact dependency revisions without updating the manifest**. This includes the documented cache-helper adjustment and its exact hash check.
3. In that same directory, run **Obtain the fixed external caches**.
4. In that same directory, run **Compile the candidate serially, then audit all 49 original declarations**. Keep `LEAN_NUM_THREADS=1` and `MATHLIB_NO_CACHE_ON_UPDATE=1` throughout. Success requires all commands and assertions to exit 0, together with the final PASS line quoted below.

The workflow requires at least 14 GiB total memory, 12 GiB initially available memory, and 10 GiB free disk. Its project phase uses a 6 GiB process-group RSS limit, a 512 MiB swap limit, a 2 GiB system-available-memory floor, 180 seconds per command, and 1200 seconds for that phase. Use a fresh workspace for each complete replay; do not reuse an old `fresh-candidate` directory. The source comparison intentionally targets the exact successful commit, so use that commit even when reading a newer documentation version.

```text
PASS: candidate modules freshly compiled; all 49 original full types and their transitive axiom reports observed in the final probe.
```

The independent finite-certificate Python check is still available as `python checker/check.py` from the repository root. It checks the CSV and the historical `lean/` literals; it does not by itself reproduce the new Lean audit. This documentation update has not repeated the Lean compilation.

## Earlier run and released proof

The earlier [run 38383082046](https://github.com/Aurantium-47/fence-rowmotion-counterexample/actions/runs/38383082046) remains a failed run. Its 39 source compilations completed, but its additional audit probe exited 1 because Lean 4.19.0 rejected the display option `pp.width`; the final workflow assertions did not complete. The successful commit removes only that unsupported option from the workflow. It changes no mathematical source relative to the earlier candidate.

The original [`v0.1.0`](https://github.com/Aurantium-47/fence-rowmotion-counterexample/releases/tag/v0.1.0), fixed at [`516b2b4ab803b9dee2796c22edf9e2d33014b5d6`](https://github.com/Aurantium-47/fence-rowmotion-counterexample/commit/516b2b4ab803b9dee2796c22edf9e2d33014b5d6), retains its native-evaluation proof and original release assets. The `lean/` sources, manuscript, Chinese summary, and `verification/lean_*` files document that historical version, whose final theorem includes `Lean.ofReduceBool`. They have not been rewritten to appear native-free. The new `kernel-candidate/` sources and this page describe the later kernel-checked certificate.

This work was prepared with AI assistance. No additional reuse license is granted by this verification update; the existing attribution and upstream dependency licenses continue to apply.
