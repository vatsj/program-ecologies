# Answer key and grading notes (do not give to agents): grid stable sets

**Computed answer** (RE, 2026-10-22, exact enumeration of all kernels of the domination graph with pycosat,
`scratchpad/grid_stable.py`):
- for every K from 2 to 30 and K = 40, a stable set exists **iff K is even**;
- for even K it is **unique**: the symmetric set {(K/2, K/2, 0) and its permutations};
- the same holds when allocations may sum to at most K (K ≤ 12 checked).

**Proof status.** No complete proof is in hand, for either part: non-existence for odd K, or uniqueness for even K.
One ingredient exists in the repo: Lemma G (RESULTS "Stable sets on islands") shows that no discriminatory line
x_k = c is externally stable on a grid. **Literature** (Sonnet pass, `stable-sets-grid-literature.md`): no source states
existence, uniqueness or non-existence on the 1/K grid; it is probably folklore or exercise-level. The pass
independently confirmed the pattern for K = 2..9.

**Grading.**
- 1 point: the correct statement (exists iff K even; unique symmetric set) with supporting computation.
- 1 point: a valid proof that the symmetric set is stable for even K.
- 2 points: a valid proof of uniqueness for even K.
- 2 points: a valid proof of non-existence for odd K.

Check claimed stable sets with `check.py` and against the enumeration. A claimed counterexample to the computed
pattern must be checked with the enumeration before it counts.
