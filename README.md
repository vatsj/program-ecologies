# Program ecologies

Implementation of THEORY.md / IMPLEMENTATION.md: stochastic stability of program
strategies in open-source games.  Python + NumPy (+ numba for the replicator loop).

```
src/dsl.py        grammar, enumerator, hash-consing, program bodies, bits prior
src/evaluate.py   batched value iteration over a flat (pair, subterm) tape
src/reference.py  slow recursive oracle + Monte-Carlo sampler
src/chain.py      replicator, payoff providers (square / incremental), attractor chain
src/moran.py      finite-N Moran check
src/report.py     support + transition rendering, results table
src/run.py        sweep runner; runs/<hash>/report.md, runs/results.md
games/*.yaml      game configs;  predictions/  dated verdicts written before first run
tests/            oracle agreement + hand cases (pytest)
```

Run one cell:

```bash
python3 src/run.py --arm weak --n 6 --game pd --N 10 100 1000
```

`n <= 6` uses the square program×program matrix; `n >= 7` uses the incremental
program×attractor path (`--mode` overrides).

## Conventions and deviations from the spec

- **Node counting.**  Every constructor is a node, application included
  (IMPLEMENTATION §2).  So `THEM(ME)` is 3 nodes, `or(X,THEM(ME))` 5, and
  `or(and(X,X),THEM(ME))` **7**, one more than THEORY §7 counts it.  Predictions
  (a)/(b) therefore refer to n=6 / n=7 here.  Language sizes (cumulative): weak
  n=6 1852, n=7 9426, n=9 228,794; strong n=6 1726; growth ≈ 5.75×/level.
- **Prior.**  bits(p) = log2 a(|p|) + 2 log2 |p| + 1 (uniform inside a length
  class, Elias-gamma length prefix), normalised over the truncated language.
- **Divergence.**  Each pair carries (c, f): P(action 0) and P(hit the budget
  floor).  Floor hits abort the path.  V = c + f·[minimax = action 0]; a pair is
  divergent when f > 1e-6 at convergence.  This is exact for `THEM(ME)` vs
  itself (f = 1 from budget 0) and for match-vs-swap, and it catches programs
  whose output happens not to depend on the floor value but which never
  terminate.
- **Applications strip `ME(...)`** in applied position by default (`me_app=True`
  re-enables it; the evaluator supports it and is tested with it).  This is what
  keeps the dependency closure of a program×attractor rectangle small.
- **Chain states.**  Monomorphic populations and polymorphic attractors
  (replicator rest points with a restoring force), stored on the 1/N grid
  (largest-remainder rounding; types below 1/(2N) are dropped).  Neutral sets
  are not states: a neutral rest set is collapsed to its vertices in
  proportion to the frequencies.
- **Transition weights.**  P(A→B) ∝ μ(q)·ρ(q | A→B), ρ the frequency-dependent
  Moran fixation probability of a single q-lineage against the lumped resident,
  fitness f = exp(w·payoff) (`chain.fixation`; the first Moran-fixation sweep
  used 1 + w·payoff clamped at 1e-6, whose w = 1 cells are void in games with
  negative payoffs — see RESULTS.md).  The target B is
  found by the replicator from A + q at 1/N (and from ½ if q dies at first
  order).  For a monomorphic B the product runs to N (exact for the 2-type
  chain); for a polymorphic B it is truncated at q's count in B, and at q's
  peak count when q invades and then dies — an approximation whose weight is
  reported per cell as `poly_flow`.  `w` (selection intensity) is a sweep
  parameter: `--w 0.01 0.1 1.0`.
- **Flow-pruned exploration.**  Exact enumeration of neutral grids is
  infeasible (a 5-type neutral set has C(N+4,4) points).  States are expanded
  only when the stationary flow into them exceeds `theta` (1e-6), the dominant
  out-edge is followed eagerly, edges into unexpanded states are dropped with the
  source row renormalised, and the dropped flow is reported (`cut_flow`).
- **Closed classes.**  The condensation DAG is processed sink-first; a class
  whose absorption solve fails the row-sum identity is numerically closed and
  becomes a closed class of its own (`near_closed_classes` in the row).  π is
  the absorption-weighted mixture over closed classes from the seed
  distribution (monomorphic states weighted by μ); absorption probabilities are
  reported and π sums to 1 by construction.
- **Performance.**  BLAS is pinned to one thread in `dsl.py` (multi-threaded
  OpenBLAS on small solves was 600× slower under load).  The replicator loop is
  numba-compiled.  Square cells at n=6 take seconds to a minute at N ≤ 100;
  N = 1000 takes about a minute for the strong arm.
- **Incremental path.**  Behavioural classes need a signature that separates
  programs neutral against the current support but different elsewhere, so
  every program is evaluated once against a probe set (all programs of size ≤ 4)
  and per support; the class representative is the shortest member.  Agreement
  with the square path at strong n=6: max |Δπ| ≈ 1e-3 (N=10), 1e-2 (N=100).

## Model issue surfaced by the Moran check, and its fix

The first sweep used deterministic-replicator transitions with neutral sets as
grid states.  Having no genetic drift, it let a neutral mutant persist at 1/N
until a mutation displaced it, and put ~N× too much occupancy on neutral edges
(strong arm, PD, N=100: 45% on the D–`THEM(ME)` edge vs < 1% in Moran).  The
second sweep replaces the edge weights with Moran fixation probabilities and
removes neutral sets from the state space.  The neutral-edge artifact is gone,
and at w = 0.1, εN = 0.1 the chain and the Moran simulation agree on the mode
and the cooperator share to within 0.02 in both arms (`runs/moran_check.md`).

What remains: (1) at w = 0.01 the chain has no drift *inside* a state's
residence, so it overstates the mode relative to Moran's mutation–drift
mixture; (2) at w = 1 the Moran answer depends on ε (εN = 0.1 vs 1 differ by
0.2 in the cooperator share), outside the single-mutant regime THEORY §5
assumes; (3) ρ into polymorphic attractors is the truncated-product
approximation, load-bearing only in N = 10 cells; (4) the resident is lumped
at the state's proportions along the mutant's path.  Findings: RESULTS.md
(second sweep) and RESULTS-2026-09-18-replicator.md (first sweep).
