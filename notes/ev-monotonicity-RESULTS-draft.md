## EV-monotonicity and weight responsiveness in arm T: a penalty on every non-fair outcome speeds the stable set and changes no weights, a bonus on one fair pair selects it, and a small bonus opens a transient route to the unequal state that b = 1/6 closes (2026-11-08)

Predictions `predictions/2026-11-08-ev-monotonicity.md` (committed before any run), code `src/ev_monotonicity.py` (5 tests,
`tests/test_ev_monotonicity.py`, passing), report `runs/ev-monotonicity.md` and `.json`. Run by a Sonnet subagent on the
queue-69 machinery (RESULTS "Arm T under islands to infinity before time": 27 L_T programs per slot, `dollar3`, settled
islands = program triples, exact ODE on the triple simplex for I → ∞, jump chain for finite I, A_f charge P_fail = 0.1, main
dose, natural start = the rotation-averaged post-anneal law). The question: does arm T's island equilibrium respect
monotonicity in expected value (a technology axiom), and do its weights respond to incentives? Payoff modifications are
applied to the outcome payoffs in dollars before the A_f charge, and the exact Moran fixation kernel is rebuilt from the
modified table.

**Design.** *Penalty c* ∈ {0.05, 0.1}: every outcome of class unequal pair, grand split or wasteful loses c for each player
whose amount there is positive; fair pairs and disagreement unchanged. This is rotation-equivariant, so the symmetric ODE
applies. *Bonus b* ∈ {1/12, 1/6}: the fair pair F0 = (½, ½, 0) pays b more to slots 0 and 1. This breaks rotation symmetry,
so the ODE is integrated unsymmetrized from the symmetric natural start. Mean field: three pools of 16,384 founders (main
dose, P_fail 0.1; recomputed, 2 minutes each, since the stored pools are scratch-only), pool means reported. Finite worlds:
I = 1,024, 20 worlds, 10⁵ events per island, the queue-69 seeds (common random numbers across conditions); this is a
finite-I, finite-time schedule, not the I → ∞ object. Total compute about 40 CPU-minutes locally (4 CPUs, 3 workers; founding 2 minutes per pool, one ODE about 1–1.5 minutes, 20 worlds about 1 minute); no Daytona.

**Validation.** With c = 0, b = 0 the recomputed natural-start trajectory reproduces the stored pool-mean class-share
trajectory (max abs difference 0 at t = 0, ≤ 7·10⁻¹⁶ at 10³, 10⁴, 10⁵ and 1.2·10⁻¹² at convergence) and the stored
per-pool end shares (≤ 2.6·10⁻¹²); the control worlds' final pair counts are identical to the stored `worlds.json` at
I = 1,024. The stored and recomputed founding pools therefore agree exactly.

**Mean field (pool mean of 3; pairs F0 / F1 / F2).** V\* by events per island:

| condition | 10³ | 10⁴ | 10⁵ | convergence |
|---|---|---|---|---|
| control | 0.8738 | 0.99887 | 0.99927 | 1 (pairs ⅓ each) |
| penalty 0.05 | 0.9080 | 0.99902 | 0.99981 | 1 (⅓ each) |
| penalty 0.1 | 0.9355 | 0.99940 | 0.99999 | 1 (⅓ each) |
| bonus 1/12 | 0.8914 | **0.0041** | 0.99925 | 1, all on F0 |
| bonus 1/6 | 0.9190 | 0.99825 | 0.99921 | 1, all on F0 |

Bonused pair F0 share of all islands: b = 1/12: 0.733, 0.0036, 0.99925, 1; b = 1/6: 0.859, 0.99825, 0.99921, 1 (the
unbonused symmetric path: 0.291, 0.333, 0.333, ⅓). All 15 registered trajectories (and the 6 exploratory ones) meet the queue-69 convergence criterion (to 10⁷
events at most for the bonus runs, 1.8·10⁶ for c = 0.05, 4.2·10⁵ for c = 0.1). The penalty runs keep the three pairs equal
by symmetry at every time; what moves is speed (V\* at 10³ events 0.874 → 0.908 → 0.936). The b = 1/12 path is not
monotone: F0 holds 0.97 of islands by 5·10³ events, then V\* falls to 0.0005–0.0042 (the excursion minimum, at 10⁴–2·10⁴
events per island in the three pools; 0.99 of islands on unequal pairs) before F0 returns by ~5·10⁴. At 10⁴ events the
top triples of the unequal state (pool 0) are a bully in slot 0 against an accommodating constant in slot 2, (⅔, 0, ⅓).

**Finite worlds (I = 1,024, 20 worlds, 10⁵ events per island).**

| condition | ≥ 0.99 on fair pairs | consensus F0 / F1 / F2 | unequal consensus | all three pairs ≥ 0.05 | mean share F0 / F1 / F2 | mean V\* |
|---|---|---|---|---|---|---|
| control (b = 0) | 18 | 4 / 8 / 1 | 2 | 1 | 0.233 / 0.486 / 0.180 | 0.899 |
| penalty 0.05 | 20 | 5 / 5 / 5 | 0 | 2 | 0.333 / 0.348 / 0.319 | 0.9998 |
| penalty 0.1 | 20 | 3 / 6 / 7 | 0 | 0 | 0.239 / 0.371 / 0.391 | 1.0000 |
| bonus 1/12 | 10 | 6 / 2 / 2 | 10 | 0 | 0.300 / 0.100 / 0.100 | 0.499 |
| bonus 1/6 | 20 | 20 / 0 / 0 | 0 | 0 | 0.999 / 0.000 / 0.000 | 0.999 |

The control reproduces queue 69's pooled single-pair lottery in kind (13 single-pair worlds, 4 / 8 / 1; with the 155 worlds
of queue 69 the pooled count is uniform). Penalty single-pair worlds pooled over c: 8 / 11 / 12 (χ² p = 0.66). The
unbonused symmetric laws and the worlds start from the same raw pooled histogram, so the penalty's finite-world gains are
the speed effect: unequal consensus 2 of 20 in the control against 0 and 0. Under b = 1/12 the mean V\* across worlds
falls to 0.31 at 10⁴ events per island and sits at 0.50 at 10⁵, with 10 of 20 worlds on an unequal consensus, 6 on F0 and
4 on F1 or F2 (the bonused pair does not keep priority after the excursion).

**Exploratory (post hoc, not registered).** Two more bonuses, three pools and 20 worlds each. b = 1/8: no mean-field
excursion (V\* ≥ 0.64 after 100 events per island, end F0 = 1); finite worlds 19 of 20 on F0, one on unequal (mean V\* 0.949). b = 1/24: the
mean-field limit depends on the founding pool, one pool ends on a fair pair (F1, not F0) and two on unequal pairs (pool-mean
V\* ⅓ at convergence); finite worlds 14 of 20 on fair pairs, 6 unequal (consensus 6 / 3 / 5 on F0 / F1 / F2). The size of the
excursion falls as b rises toward 1/6, where F0 pays ½ + b = ⅔, the unequal pair's top payoff. The reading (inference, not
isolated by a control) is that a bonused fair pair makes the two named slots monomorphic for a long time and leaves the
excluded slot's program neutral, so it drifts toward accommodating constants (the ⅓-accepting programs of the unequal
pairs), after which a bully gains ⅔ − (½ + b) over the pair; b ≥ 1/6 removes that gain.

**Verdicts (as registered).** *RE 1 held:* V\* at convergence 1.000000 for both c and the pairs ⅓ each (a symmetric-path
identity: the penalty is rotation-equivariant), within 3·10⁻⁴ of the unpenalized run in each pair's share at 10⁵ events (V\* 0.99927 control, 0.99981 and 0.99999 penalized); falsifier (V\* < 0.99 or a
pair moves by > 0.05) not met. *RE 2 held:* the bonused pair's share at convergence 1.000 at b = 1/12 (≥ 0.9) and 20 of 20
worlds at b = 1/6 (≥ 16); falsifier (< 0.5 or ≤ 8 of 20) not met. *RE 3 held:* V\* at 10³ events with c = 0.1 is 0.9355
(≥ 0.92). *RE 4 held:* penalty worlds χ² p = 0.66 (> 0.05) and 0 unequal-consensus worlds at each c (< 4). *RE 5 held as
written* (b = 1/6: F0 0.998 of islands at 10⁴; b = 1/12: ≥ 0.5 by 10⁵), though b = 1/12 is far below 0.5 at 10⁴ events.
*RE 6 failed:* the ordering in b is reversed at 10⁴ events per island (b = 1/12 below b = 0) and at 10⁵ (0.99925 against
0.99921, a rounding-sized reversal), and b = 1/12 wins consensus in only 6 of 20 worlds (falsifier ≤ 8 of 20; prediction ≥ 12). *RE 7 half held:* V\* at convergence ≥ 0.999 at both b (held), but the finite-world clause fails at b = 1/12 (10 of
20 worlds on fair pairs against ≥ 16; held at b = 1/6, 20 of 20).

**Reading.**
- *EV-monotonicity holds for the stable-set target:* lowering the payoff of every non-fair outcome never moves V\* away
  from 1, leaves the three pairs symmetric on the symmetric path, speeds the limit, and removes the finite-world unequal
  consensus seen in the control (2 of 20 to 0 of 40). It does not distinguish pairs, so it is silent on the lottery's
  weights beyond the symmetric identity.
- *Weights respond to incentives, with a stability condition:* a bonus on one pair selects it in the mean field at every
  b tested down to 1/12 and in every finite world at b ≥ 1/6, so the lottery across pairs is no longer uniform once the
  payoffs are asymmetric. But the unequal state is not a monotone function of b: below the gap between the unequal pair's
  top payoff and the bonused pair (b < 1/6), the bonused monoculture is a source of a transient (b = 1/12) or a permanent
  (b = 1/24) route to unequal consensus. Responsiveness is therefore conditional on the bonus clearing the unequal
  pair's payoff, not just on being positive.
- *Caveats:* a hand-built 27-program library with fixed fuel caps; three pools; 20 worlds per cell (the single-pair
  counts are small); the b = 1/12 excursion mechanism is the RE's inference from the top triples at one checkpoint and one
  pool, not a controlled test; the exploratory b = 1/8 and 1/24 cells are post hoc; the bonus is on slots 0 and 1 only and
  the penalty on all non-fair classes at once (no class-by-class split); the finite-world horizon (10⁵ events per island) is
  short of the mean-field convergence times (up to 10⁷) for the bonus runs.
