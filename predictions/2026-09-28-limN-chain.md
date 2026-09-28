# Predictions: lim_N of the attractor chain in the PD, 2026-09-28

Written and committed before any chain cell in this file was run. Executions so far are static only:
the cached class payoff matrix and the Moran fixation formula (`chain.fixation`) evaluated for single
edges, as below.

## Cells

Weak arm, L_6 with `ROLE` (3,994 programs, 112 classes), PD, f = exp(w · payoff), the ε→0 attractor
chain (`src/run.py`, Moran fixation transitions). w ∈ {0.1, 0.3, 1}; N ∈ {100, 300, 1,000, 3,000, 10,000,
30,000}. The earlier lim_N rows (RESULTS.md, "Exponential fitness map") are without `ROLE` and stop at
N = 1,000.

Reported per cell: π and the support with transition structure (rule 4). Also:
- π(all-`THEM(^C)`) and π-weighted P(C,C);
- ρ_enter, the fixation probability of one `THEM(^C)` on an all-D population;
- the exits from all-`THEM(^C)` as shares of mutation events, split three ways:
  - **shadow**: a mutant on-path identical to `THEM(^C)`, meaning u(q,R) = u(R,q) = u(q,q) = u(R,R). These are
    C and eight grounded or `ROLE`-guarded variants;
  - **faker**: u(q,R) > u(R,R), 13 classes;
  - **other**.

## The claim under test

Stated in conversation on 2026-09-28. In lim_N, the shadow is a finite-N obstruction and the faker is the
binding one:
- **Entry** into all-`THEM(^C)` from all-D falls like N^(−1/2). `THEM(^C)` is neutral at one copy and its
  advantage grows with its frequency.
- **Shadow exit** falls like 1/N, since it is neutral drift.
- **Faker exit** is N-independent: the faker strictly invades, with ρ(`THEM(^D)` | all-`THEM(^C)`) ≈ 0.26 at
  w = 0.3 for every N.

Hence π(all-`THEM(^C)`) rises, peaks, and then falls like N^(−1/2), and the well-mixed PD is not efficient
in lim_N. THEORY §9.1 calls the PD limit "answered" from N = 1,000; this tests whether it was.

Static single-edge rates per mutation event, from the fixation formula and the μ of each class:

| w | N | entry | shadow exit | faker exit | faker share | entry / exit |
|---|---|---|---|---|---|---|
| 0.1 | 100 | 1.3e-5 | 2.5e-3 | 1.1e-4 | 0.03 | 0.0037 |
| 0.1 | 1,000 | 4.1e-6 | 2.5e-4 | 1.0e-4 | 0.29 | 0.0116 |
| 0.1 | 3,000 | 2.4e-6 | 8.3e-5 | 1.0e-4 | 0.55 | 0.0128 |
| 0.1 | 30,000 | 7.5e-7 | 8.3e-6 | 1.0e-4 | 0.92 | 0.0068 |
| 0.3 | 100 | 2.2e-5 | 2.5e-3 | 2.9e-4 | 0.10 | 0.0077 |
| 0.3 | 1,000 | 7.0e-6 | 2.5e-4 | 2.9e-4 | 0.53 | 0.0131 |
| 0.3 | 10,000 | 2.2e-6 | 2.5e-5 | 2.9e-4 | 0.92 | 0.0072 |
| 0.3 | 30,000 | 1.3e-6 | 8.3e-6 | 2.9e-4 | 0.97 | 0.0044 |
| 1 | 100 | 3.8e-5 | 2.5e-3 | 7.6e-4 | 0.23 | 0.0117 |
| 1 | 300 | 2.3e-5 | 8.3e-4 | 7.6e-4 | 0.48 | 0.0143 |
| 1 | 30,000 | 2.4e-6 | 8.3e-6 | 7.5e-4 | 0.99 | 0.0031 |

## Verdicts

1. **Rise, peak, fall.** For each w, π(all-`THEM(^C)`) peaks at an interior N of the grid, and its value
   at N = 30,000 is at most 1/1.5 of the peak. The peak sits near N ≈ 3,000 at w = 0.1, N ≈ 1,000 at
   w = 0.3 and N ≈ 300 at w = 1; each must fall within one grid step of that.
2. **Exit composition.** At every cell, the chain's faker share of exits from all-`THEM(^C)` is within 0.1
   of the static column above, or of the static value at that N for rows not shown. It crosses 0.5
   between the grid points bracketing the static crossing, and exceeds 0.9 at N = 30,000 for every w.
3. **Entry scaling.** Fitting log ρ_enter against log N over N ∈ [1,000, 30,000] gives a slope in
   [−0.55, −0.45] at every w.
4. **Level.** π-weighted P(C,C) is below 0.05 in every cell, and all-D holds π ≥ 0.9 in every cell.
5. **Support.** No state other than the monomorphic ones reaches π ≥ 10⁻³ in any cell. The states
   expected in support are all-D, all-`THEM(^C)` and the on-path-D faker states. Flow into polymorphic
   targets stays below 10⁻⁴.

**Falsifier of the claim.** Either of the following refutes it:
- at w = 0.3, π(all-`THEM(^C)`) at N = 30,000 is at least its value at N = 1,000;
- the shadow share of exits from all-`THEM(^C)` exceeds 0.5 at N = 10,000 for any w.

**What each outcome would mean.**
- *If 1–3 hold:* the unconditional shadow is demoted to a finite-N effect in THEORY. The lim_N
  obstruction in well-mixed populations becomes fakeability, and that motivates the characterization
  sketched on 2026-09-28: Σ is efficient iff some reciprocator has no grounding cost and no strict
  invader. It also motivates the modal (Löbian) arm.
- *If the falsifier fires:* some exit or entry channel is missing from the single-edge picture, and the
  full chain's transition structure should name it.
