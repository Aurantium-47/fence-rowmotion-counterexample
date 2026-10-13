# Lean verification of the 32-vertex fence counterexample

This project verifies a counterexample to Elizalde–Plante–Roby–Sagan, *Rowmotion on fences*, Conjecture 5.4(b), for the paper's fence with segment parameter `(3,3,3,3,3,3,3,3,3,3,3)`. The exhibited rowmotion orbit has 237 distinct lower ideals and cardinality sum 3774, giving mean 1258/79 instead of 16.

The files `W04/Poset.lean`, `W04/Rowmotion.lean`, `W04/Orbit.lean`, and `W04/Main.lean` are unchanged copies of the verified proof sources. Their correspondence, current hashes, actual build output, and printed axiom dependencies are recorded in `../verification/lean_*`.

## Proof scope and trust

`Poset.lean` defines the actual 32-point partial order and proves that the eleven specified, distinct segments are exactly its maximal chains. Each segment has two unshared vertices, so its parameter in the paper's convention is three. `Rowmotion.lean` defines lower ideals and rowmotion as the downward closure of the minimal complement. `Orbit.lean` checks the finite orbit certificate. `Main.lean` identifies the complete set of iterates, proves period 237 with no earlier positive return, the sum and mean, and failure of half-cardinality homomesy.

The final theorem is `W04.paper_fence_counterexample`. The code does not formalize a general library of all fence parameters and makes no claim about the smallest possible counterexample.

The orbit certificates use `native_decide`. The final theorem's printed axiom dependencies are:

```text
[propext, Classical.choice, Lean.ofReduceBool, Quot.sound]
```

`Lean.ofReduceBool` records the additional trust in Lean's native computation and compiler. This is not a proof checked solely by kernel reduction. The segment correspondence uses `decide +kernel` and does not depend on `Lean.ofReduceBool`. The completed source contains no `sorry`, `admit`, or custom mathematical axioms.

## Fixed versions

- Lean 4.19.0, release commit `6caaee842e94`, selected by `lean-toolchain`.
- mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b` (v4.19.0).
- All nine dependency revisions are fixed in `lake-manifest.json`; the package is named `w04_fence`.

## Reproduction

With the pinned Lean toolchain available, run these commands from this directory for a conventional Lake setup:

```text
lake exe cache get
lake build
```

Keep the supplied manifest; do not run `lake update` to upgrade dependencies. Dependency acquisition and a fresh-network bootstrap were not executed for this publication copy. The actual validation used the build script below with existing dependency caches at the locked revisions, and compiled every project module anew.

On PowerShell, after dependency caches are available in `.lake/packages`:

```powershell
./build.ps1
```

To reuse an existing dependency cache read-only, explicitly provide its packages directory and the pinned Lean executable. Set the environment variables to the appropriate locations on your own machine:

```powershell
./build.ps1 -LeanExecutable $env:W04_LEAN_EXE -DependencyPackages $env:W04_DEPENDENCY_PACKAGES
```

The script checks the Lean version and every dependency Git revision. It reads those dependencies without changing them and writes project outputs only under this directory's `.lake/build/`. Build output uses relative project paths. `.lake/` and compiled binaries are excluded by `.gitignore` and are not part of the source distribution.

The two `unnecessarySimpa` style warnings in `Poset.lean` do not indicate proof failures; the source is retained unchanged. Necessary dependency licenses and source attribution remain with their upstream repositories.
