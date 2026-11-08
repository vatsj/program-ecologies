# Predictions: EV-monotonicity and weight responsiveness in arm T under islands → ∞ before time (2026-11-08)

Committed before any computation of this experiment. Object: queue 69 (RESULTS "Arm T under islands to infinity before
time"; `src/many_islands_t*.py`), main dose, A_f charge P_fail = 0.1, natural start = the rotation-averaged post-anneal
law. The only change: outcome payoffs in dollars, before the A_f charge, and hence the exact Moran fixation kernel.

## The question

Does arm T's island equilibrium respect monotonicity in expected value (a technology axiom), and do its weights respond to
incentives? Two probes:

1. **EV-monotone test.** Lower the payoff of every outcome that is not a fair pair by c ∈ {0.05, 0.1}, for every player who
   receives a positive amount there (unequal pairs, grand splits, wasteful outcomes); fair pairs and disagreement
   unchanged.
2. **Weight responsiveness.** Add a bonus b ∈ {1/12, 1/6} dollars to the fair pair (½, ½, 0) (slots 0 and 1 named each
   other at ½), for both members. Report the mean-field shares of the three fair pairs at 10³, 10⁴, 10⁵ events per island
   and at convergence; finite worlds (I = 1,024, 20 worlds each, seeded, run to 10⁵ events per island): the number of
   worlds in consensus on each pair and the mean share per pair; the same for b = 0 as the control (queue 69: roughly
   uniform, 44 / 54 / 57 over 155 single-pair worlds pooled).

V\* (share on any fair pair) is reported in every case.

## Predictions (verbatim from the RE's brief)

- **RE 1 (EV-monotone test passes).** With the penalty, V\* at convergence is ≥ 0.999 and the three pairs keep their
  symmetric-path shares within 0.01 of the unpenalized run. *Falsifier:* V\* < 0.99, or a pair's share moves by > 0.05.
- **RE 2 (weights follow incentives).** With the bonus, the bonused pair's mean-field share at convergence is ≥ 0.9 at
  b = 1/12, and in finite worlds it wins consensus in ≥ 16 of 20 at b = 1/6. *Falsifier:* mean-field share < 0.5, or ≤ 8
  of 20 worlds.

## Additional predictions (the subagent's, made before any run)

- **RE 3 (the penalty is exactly symmetric, so pair equality is trivial at the limit).** The penalty is
  rotation-equivariant and the start is symmetrized, so the symmetric ODE gives each pair 1/3 at every time by
  construction; RE 1's "within 0.01" is therefore a statement about the symmetric path only. The informative quantity is
  speed: the penalty raises V\* at 10³ events above the unpenalized 0.874 (c = 0.1 to ≥ 0.92, c = 0.05 in between).
  *Falsifier:* V\* at 10³ events with c = 0.1 below 0.874.
- **RE 4 (the penalty in finite worlds does not make the lottery biased).** Single-pair worlds under the penalty at
  I = 1,024 split across the three pairs without a significant departure from uniform (pooled over c, χ² p > 0.05),
  and consensus on unequal pairs is not more frequent than in the control (queue 69: 2 of 20 at main, P_fail 0.1).
  *Falsifier:* χ² p < 0.05 on the pooled single-pair worlds, or ≥ 4 of 20 unequal-consensus worlds at either c.
- **RE 5 (the bonus is selected quickly, not just eventually).** At b = 1/6 the bonused pair holds ≥ 0.5 of the mean-field
  shares of fair-pair islands by 10⁴ events per island, and ≥ 0.99 at convergence; at b = 1/12 ≥ 0.5 by 10⁵ events.
  *Falsifier:* the bonused pair below 0.5 at 10⁴ events at b = 1/6.
- **RE 6 (monotone in b).** The bonused pair's share at 10³, 10⁴ and 10⁵ events is increasing in b over {0, 1/12, 1/6};
  at b = 0 with the symmetric start it is 1/3 on the symmetric path. In finite worlds at b = 1/12 the bonused pair wins in
  ≥ 12 of 20 worlds. *Falsifier:* any of these orderings reversed at the mean-field checkpoints, or ≤ 8 of 20 worlds at
  b = 1/12.
- **RE 7 (V\* does not drop under the bonus).** V\* at convergence ≥ 0.999 at both b, and in finite worlds ≥ 0.99 of
  islands on fair pairs in ≥ 16 of 20 worlds. *Falsifier:* V\* < 0.99 at convergence.
- **Caveat on the mean-field bonus runs.** The bonus breaks rotation symmetry, so the ODE is integrated unsymmetrized
  from the symmetric natural start; convergence is scored by the queue-69 criterion on the raw field, and a trajectory
  not converged by 10⁷ events is reported at its last checkpoint with that label.

## Disclosures

- No pilot of any counted quantity has been run. Before this file was written the subagent only built the tables (to read
  the class composition of outcomes and the index of the fair pair (½, ½, 0), index 0) and read the stored run's V\*
  trajectory (needed for the validation).
- The stored founding pools are not in the repository (scratch only, not committed); the main-dose pools (3 × 16,384
  islands, seeds as in `run_pool`) are recomputed and the validation compares the recomputed natural-start trajectory with
  the stored pool-mean trajectory in `runs/many_islands_t/ode.json`.
- Finite-world schedule labels: worlds run at I = 1,024 to 10⁵ events per island are a finite-schedule property
  ("finite-I, finite-time"), not the ε-free or I → ∞ object.
