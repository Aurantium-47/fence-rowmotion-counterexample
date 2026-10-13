# References and scope

## Bibliography

1. Sergi Elizalde, Matthew Plante, Tom Roby, and Bruce E. Sagan. “Rowmotion on fences.” *Algebraic Combinatorics* **6**(1) (2023), 17–36. [doi:10.5802/alco.256](https://doi.org/10.5802/alco.256). See also [arXiv:2108.12443v2](https://arxiv.org/abs/2108.12443v2), dated 26 April 2025.

2. Alec Mertin and Svetlana Poznanović. “Toggleability Spaces of Fences.” *The Electronic Journal of Combinatorics* **31**(4) (2024), #P4.46, 36 pages. Published 29 November 2024. [doi:10.37236/13085](https://doi.org/10.37236/13085). Preprint: [arXiv:2406.02493v1](https://arxiv.org/abs/2406.02493v1), dated 4 June 2024.

3. Alec Mertin. *Homomesies and Toggleability Spaces*. Ph.D. dissertation, Clemson University, August 2025. *All Dissertations*, 4090. [Official repository record](https://open.clemson.edu/all_dissertations/4090/).

## Target statement and convention

The target is Conjecture 5.4(b) of [1], printed page 35: for the fence \(F=\breve F(a^t)\) with \(a\ge2\) and odd \(t\), the cardinality of a lower ideal is \(|F|/2\)-mesic under rowmotion. Here

\[
\rho(I)=\mathord\downarrow\min(F\setminus I).
\]

A segment is a maximal chain. The paper defines \(\alpha_i\) as one plus the number of unshared vertices on segment \(i\); a shared vertex belongs to two adjacent segments. Thus \(\alpha_i\) is not uniformly the number of edges. For \(\breve F(3^{11})\), the two end segments have three vertices each, the nine interior segments have four each, and every segment has two unshared vertices. The fence has \(11\cdot3-1=32\) vertices.

The exhibited orbit has 237 distinct lower ideals and cardinality sum 3774, so its mean is \(1258/79=16-6/79\), disproving this conjecture. This conclusion concerns part (b); it makes no claim about part (a), which concerns antichain-cardinality homometry.

## Relationship to the 2024 paper

Numbering in [2] differs between the journal article and its arXiv version:

| Journal | arXiv v1 | Scope |
|---|---|---|
| Conjecture 12, p.18 | Conjecture 5.1 | Restates [1, Conjecture 5.4(b)]. |
| Theorem 14, p.19 | Theorem 5.3 | Relates the ideal-cardinality deviation to the peak-minus-valley antichain statistic, modulo toggleability statistics. |
| Conjecture 15, p.20 | Conjecture 5.4 | Equivalent to Conjecture 12 by Theorem 14. |
| Conjecture 16, p.20 | Conjecture 5.5 | Stronger symmetry claim for pairs of shared vertices. |
| Theorem 19, p.21 | Theorem 5.8 | Proves the relevant statistic identity for three segments. |
| Corollary 25 / Theorem 26, p.27 | Corollary 5.14 / Theorem 5.15 | Gives conditional orbit symmetry and a homomesy on dihedral-group orbits. |

The established results in the last two rows do not imply the conjecture for each rowmotion orbit of an eleven-segment fence.

## Literature and priority limitations

The original article, its second arXiv version, and Section 5 of both versions of [2] were checked. They do not supply an earlier resolution of the target. The literature check was not exhaustive, and no priority or first-discovery claim is made.

For [3], the official metadata and abstract were accessible. Its official full-text download returned HTTP 403 during the check on 13 October 2026. The dissertation's full contents remain unverified; its abstract cannot establish whether it contains this counterexample or another resolution. This access limitation affects the literature and priority assessment, not the mathematical validity of the exhibited finite certificate.
