# The stable-set target in the Turing-complete arm under islands → ∞ before time (notes, 2026-10-29)

Spec `specs/2026-10-29-many-islands-t.md` (the RS, 2026-10-29: "Ur experiment sgtm" after "Sgtm - I see farsightedness as
a band-aid antithetical to the rest of the program."; reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode amended`;
the folded text is the resolution). Follows `notes/many-islands.md` (the DSL readers arm R), `notes/churn-primary.md`
(arm T) and `notes/forfeit-pricing.md` (the A_f rule). §1 is written by hand before any code of this experiment and
before any counted cell; §2 (deviations, choices where the spec is silent, costs) is appended as they arise.

## 1. Hand analysis, before code

### 1.0 Disclosure about order

Nothing of this experiment had been run when §1 was written. I read the spec and both reviews, `src/churn_primary_t.py`
(the arm-T library and its tables), `src/many_islands.py` (the DSL arms' island kernel, `pfix`, the chain and the
class ODE), `src/lt_code.py` (`enter_sim`, `do_capk`, `evaluate`: where a read times out), `src/stable_sets.py`
(`Tables`: payoff units) and the A_f derivations in `notes/forfeit-pricing.md` §1.0. No scratch query was run and no
number below comes from a machine except two pocket-calculator evaluations of `pfix` that I redo by hand in §1.1.
Everything here is checked afterwards by `tests/test_many_islands_t.py` and the validations, never the other way round.

### 1.1 Units: what w = 0.3 acts on, and what P_fail is in that unit

`stable_sets.Tables` sets `PAY[code, s] = outcome[s] / g` with g = 6 (the realizable outcome list is in sixths), so the
stored `PAY` is in **dollars** (the pie is 1; a fair pair pays 0.5 each, an unequal pair 2/3 and 1/3). The kernels
(`island_run`, `kern_mw`) form fitness as exp(w · F) with F the expected payoff in those units, and `pfix(dpay, N, w)`
takes `dpay` in dollars (`PFT[d] = pfix(d/6.0, ...)`, d in sixths). So **w = 0.3 acts on dollars**. A sixth is 0.1667
dollars, so a payoff difference of one sixth is w·Δ = 0.05.

`P_fail` is in the game's raw unit, the dollar: P_fail = 0.1 dollars = 0.6 sixths, w·P_fail = 0.03, and the charge enters
as payoff − charge in dollars with no conversion factor. Hand fitness ratios (N = 100, ρ = e^(wΔ)):

| payoff change of the migrant (dollars) | wΔ | P_fix | in units of neutral (0.01) |
|---|---|---|---|
| +0.1 (one failed read saved) | +0.03 | (1 − e^−0.03)/(1 − e^−3) = 0.02955/0.9502 = 0.0311 | 3.1 |
| −0.1 (one failed read charged) | −0.03 | 0.02955·e^−2.97/(0.9502) = 0.02955·0.05130/0.9502 = 0.00160 | 0.16 |
| −0.2 (two failed reads) | −0.06 | 0.05824·e^−5.94/(1 − e^−6) = 0.05824·0.002619/0.9975 = 1.5·10⁻⁴ | 0.015 |
| one sixth (no charge) | +0.05 | 0.0491 | 4.9 |
| P_fail = 0.03 (one failed read) | −0.009 | 0.00895·e^−0.891/(1 − e^−0.9) = 0.00895·0.4102/0.5934 = 0.00619 | 0.62 |

So a single charged read at 0.1 costs a migrant its neutral chance five-sixths over (0.16 of neutral), i.e. the charge
is selectively as strong as 0.6 of a sixth, a gap the exact kernel will resolve. The tests assert these ratios on
hand-built triples to 1e-9 from the table.

### 1.2 What the 27³ table contains: the reading graph decides every timeout

Frame (arm T): slot s's program is run as p(<p>)(<next>)(<prev>); a value 0-8 is 3·partner + demand with partner 0 = next,
1 = prev, 2 = ALL, demand 0, 1, 2 = ⅓, ½, ⅔. Programs: 9 constants C0..C8 (value 0..8, a few steps); single readers
S{n,p}{o,z}{y,n} (read the next or the previous slot's program by simulation with cap k = 400, accept if the partner
names me at ½, [y: or if the read timed out]; else fallback o = name the other slot at ½, z = the null action 8); two-
partner readers D{n,p}{f,z}{y,n} (read the first partner, then the second; fallback f = name the first, z = null);
exploiting readers X{n,p}. The root has fuel K_R = 1,200 steps; a root that runs out of fuel, is stuck, or returns a
non-number plays the timeout action (ALL, ⅔), code 8, and that is the **forfeit**.

A read times out only in a *cycle*: a reader that reads partner b simulates b's program with b's own reads, and if b
(directly or through other readers) reads back to the reader, the simulation re-enters the reader's own computation and
runs until the outermost capk frame (400 steps) is exhausted. A reader reading a constant, or reading a chain of readers
that ends at a constant, finishes and pays nothing. All nested frames inside the timing-out outermost frame are closed
by it and are not counted separately (the existing accounting, `notes/forfeit-pricing.md` §1.0: a frame closed by an
enclosing timeout is not separately a failure event); the inner frames' deadlines are later than the outer frame's,
since they are entered later, so the outermost frame is always the one that expires first. Hence each *read* that
enters a cycle counts once, and the number of failed reads in a root is the number of its reads that enter a cycle:
0 or 1 for S and X, 0, 1 or 2 for D (the first read, then the second if the first is not accepted).

**Hand-built triples** (slot 0, slot 1, slot 2; payoffs in dollars; fair pair = 0.5 each; charges at P_fail = 0.1):

| triple | executions | joint outcome | failed reads (0, 1, 2) | payoffs gross → net |
|---|---|---|---|---|
| (Snoy, C4, C1): a switcher with two constants, partner offers ½ | slot 0 reads r = 4 → accepts → names 1 at ½; C4 names 0; C1 names 0 | fair pair {0,1}, slot 2 excluded | 0, 0, 0 | (½, ½, 0) → same; reader ≈ tens of steps |
| (Snoy, C1, C1): the partner does not offer to me | r = 1 ≠ 4 → no accept → fallback 4: names prev = slot 2; C1 slot 2 names slot 0 | fair pair {0,2}, slot 1 excluded | 0, 0, 0 | (½, 0, ½) → same |
| (Snoy, Spoy, C1): two readers with a constant, they read each other | slot 0 reads 1, slot 1 reads prev = 0: cycle, each outermost read expires at 400 steps, `y`: accept the timed-out read; slot 0 names 1, slot 1 names 0 | fair pair {0,1}, slot 2 excluded | 1, 1, 0 | (½, ½, 0) → (0.4, 0.4, 0); ≈ 410 steps each |
| (Snon, Spon, C1): the same with timeout not accepted | both reads time out, no accept, fallback o: slot 0 names 2, slot 1 names 2 (o for p = next), C1 names 0 | fair pair {0,2}, slot 1 excluded | 1, 1, 0 | (½, 0, ½) → (0.4, −0.1, 0.5) |
| (Snoy, Snoy, Snoy): three readers in one cyclic chain | every read enters the 3-cycle, expires, accepted; all name next | disagreement | 1, 1, 1 | (0, 0, 0) → (−0.1, −0.1, −0.1) |
| (Dnfy, Dpfy, Dpfy) (the churn notes' homogeneous cell) | each first read expires and is accepted | fair pair {0,1}, slot 2 excluded | 1, 1, 1 | (½, ½, 0) → (0.4, 0.4, −0.1) |
| (Dnfn, Dnfn, Dnfn) | both reads time out and neither is accepted, fallback f: name first | disagreement | 2, 2, 2 | (0, 0, 0) → (−0.2, −0.2, −0.2); ≈ 821 steps (the stored dearest finishing encounter) |
| (Snoy, Snoy, C4): a reader chain ending at a constant | slot 1 reads C4 (r = 4) → names 2; slot 0 reads slot 1 (r = 1 ≠ 4) → fallback names 2; C4 names 1 | fair pair {1,2}, slot 0 excluded | 0, 0, 0 | (0, ½, ½) → same |

**Expected charges by class.** Constants: exactly 0 failed reads in every triple. S and X: 0 or 1. D: 0, 1 or 2.
**Forfeits: none.** The dearest root is two expired reads (≈ 821 steps) plus the shell, below K_R = 1,200, and
a read that is cut at 400 steps cannot push the root past its fuel; no stuck term or non-number arises in the library.
So I predict **zero forfeit events in all 3 × 19,683 root evaluations**. Consequence: under this library the
"forfeits charged without failed reads" control of question 5 coincides with P_fail = 0 (it charges nothing), and
A_f coincides with A (the merged failed-read-only rule) in every triple. I record this as a prediction (the code
counts forfeits and reports the number) because it makes that control vacuous if it holds.

**Timeout share of encounters (order of magnitude).** At the founding law (main) each slot is a reader with probability
≈ 0.10, and a read enters a cycle only if the read partner reads back. For a next-reader the probability that its next
slot is a reader reading back (Sp, D, or a longer chain closing at itself) is ≈ 0.03 + 0.03 + O(10⁻³) ≈ 0.065. So about
0.07 of a single reader's plays involve a timeout, ≈ 0.007 of all encounters have a charged reader in some slot per slot
(counting the three slots, ≈ 2% of triples drawn from the founding law have a timeout somewhere). After settlement
the share can differ in either direction (the charged cycles are selected against at 0.1, and not at 0); the code
reports it for the founding law, the post-anneal law and the ODE limit.

### 1.3 The expected occurring support

The settled triple space is 27³ = 19,683. Constant-only triples are at most 9³ = 729 and carry about 0.73 of the founding
mass at main (0.9³); reader-containing triples number 27³ − 729 = 18,954, but a reader class has seed mass between
0.375% and 0.75%, so a slot population of 100 holds 0.4-0.8 copies of each reader class and reader copies rarely fix:
the survivors are mostly the families that win by selection (switchers paired into fair pairs, which earn the same as
constants, or readers meeting a constant they read finishing). My estimate of the *occurring* support (settled triples
with at least one island) is **1.5 × 10³ to 4 × 10³ per 16,384-island pool** at main, 1 × 10³ at dose 0, 3 × 10³ to 6 × 10³
at hi, and about twice the per-pool number in the union of three pools; so at most about a third of the 27³ space is occupied
at any dose, and the three-pool union at hi may exceed 8 × 10³. The ODE nevertheless runs on all 19,683 triples because a
single migrant can reach any triple whose slot programs are present in the donor marginals.

### 1.4 The exact kernel and why it is exact here

A migrant y into slot s of a settled triple a meets two monomorphic other slots, so the payoff of a slot-s individual
(its game payoff against one uniformly drawn member of each other slot, minus its charge, which depends only on the
three programs it meets) is the constant π_s(y | a). Play is across slots only: nothing a slot-s individual earns depends
on slot s's own composition. Therefore slot s is a two-type Moran process with constant fitness ratio e^(w(π_s(y|a) − π_s(a_s|a))),
fixation probability (1 − 1/ρ)/(1 − ρ^−N) (neutral: 1/N), exactly as in `notes/many-islands.md` §1.2. The charge changes
the table of π, not the form of the kernel. (Tests: the closed form against an exact absorption solve of the Moran
chain and against simulated relaxation of this experiment's own island simulator, which uses the stored
kernel's rules.) The mean-field ODE on the triple simplex is the I → ∞ limit of the jump chain in which an event
selects a recipient island uniformly and a donor island uniformly from the others, so the donor's slot-s marginal is
x's slot-s marginal; in time units of events per island.

### 1.5 Rotation symmetry, and what I expect of the Jacobian

The library is the same in every slot (cyclic frame), so the group C₃ acts on triples by (a₀, a₁, a₂) → (a₂, a₀, a₁).
If the whole table (joint outcome translation with the swap of the two partner codes in slot 1, payoffs, charges) is
equivariant the kernel is, and the symmetrized x(0) stays on the invariant subspace. I expect the exhaustive test on
all 19,683 triples to find 0 violations; a violation means a translation bug and stops the run. On the invariant
manifold the three fair pairs are exactly equal; whether the symmetric fixed point is a knife-edge is the spectrum on the
non-invariant subspace. Hand expectation (from the DSL arm R's knife-edge, `notes/many-islands.md`): a positive leading
real part of order 10⁻⁴-10⁻³ per event, with the leading eigenvector concentrated on the three fair-pair classes
with signs summing to zero (one pair up, another down), and nearly neutral directions on the rest. The quadratic
feedback comes through the donor marginals: a pair with more islands has more donors offering its slot-programs.
Integrating the symmetric trajectory in floating point amplifies round-off along such a direction unless the state
is projected back onto the invariant manifold; I project the vector field (the average over the three rotations of the
right-hand side) at every evaluation and report the unprojected runs separately.

### 1.6 Hand expectations beyond the spec's predictions

- At P_fail 0 the T and the DSL-R tables differ on reader–reader triples in a cycle: arm T plays the null action only if
  `n` (timeout not accepted, z fallback) and accepts under `y`; the DSL weak arm diverges to (ALL, ⅔) for every
  mutual-reading pair. So arm T keeps *more* readers' pairs (y variants) at P_fail 0 than the weak DSL arm would, and its
  readers are pairable with each other. What I cannot separate by hand is whether a T-versus-R difference of the ODE limit
  is due to the fallback convention or to fuel (the second reviewer's point): fuel decides whether the fallback runs.
- At P_fail 0.1 a timed-out `y` reader in a mutually-reading fair pair pays 0.1, a fitness penalty of 0.16 of neutral against a
  constant that takes its place. Readers therefore have an extra reason to leave read-cycles and an extra neutral cost to
  enter them (gemini-4-argon's mechanism). Whether the readers survive in the numbers that convert islands is what
  prediction 5 asks; I keep the spec's numbers (V\* ≥ 0.95 predicted, uncertain) and register the two counter-predictions.
- The ODE is expected to be cheap per right-hand side (3 × 27⁴ = 1.6 × 10⁶ multiply-adds per evaluation, a few milliseconds
  in numba) and the horizon of 10⁵ events per island needs about 10⁴ explicit steps (stability-limited by the fastest
  exit rate ≈ 0.17 per event); 10⁷ events needs an implicit or exponential scheme and will be done only for unresolved
  trajectories.

## 2. Deviations, choices where the spec is silent, costs (appended as they arose; entries before the counted cells were written before them)

### 2.1 Before any counted cell

- **Order of work and what was seen.** §1 and the predictions file were committed before any code. During the code I ran (all scratch, outside the
  repository, none a counted cell): the table build (5 s), which showed the forfeit count 0 and the failed-read histogram [11017, 7370, 1296] (the
  hand predictions of §1.2 were already written); a 4,000-island pilot pool at main, P_fail 0, with the exact ODE run from it to 10^6 events
  (V\* 0.28 -> 1.0000, grand coalition decaying roughly linearly in time, residual 10^-9) and its Jacobian (leading non-invariant real part 5.6e-4);
  and a backward-Euler test on the same pilot. Those numbers were seen before the counted cells; the predictions did not use them (they were written
  first) and they are not scored. The two main pools (P_fail 0 and 0.1) were built before the post-pool validations ran; no ODE, Jacobian or world
  result of a counted cell existed then.
- **Library.** The 27 programs of the prior (the four stub twins of `churn_primary_t` have weight zero and are excluded; all tables are 27^3). The seed
  law is the churn experiment's (`FAMILY_WEIGHT`), identical in the three slots.
- **Failed-read counter.** No edit of `lt_code`: a context manager wraps `lt_code.enter_sim` and counts a frame that returns `TO` (the compiled
  closures look the function up at call time). A forfeit is a root that runs out of fuel, gets stuck or returns a non-number (`BOT` or a value outside 0-8),
  all of which play the timeout action 8. The counter agrees with the merged A_f rules on hand programs (`V:charge`): one charge per failed read, a frame
  closed by an enclosing expiry not counted separately, a forfeit counted once, a read that expires and then loops two events. The stored accounting
  of `lt_tape` (the merged A_f counter's home) does not exist in `lt_code`, so the rule was reimplemented, not imported; this is a deviation from "importing the merged A_f counter".
- **Controls of question 5 are vacuous.** Since the table has no forfeit, "failed reads charged without the forfeit charge" is A_f itself and
  "forfeits charged without failed reads" is the P_fail 0 table (checked as equal payoff tables, max difference 0); no separate trajectories were run.
- **Pools.** 3 pools of 16,384 founders per cell, founders paired across P_fail (same generator for the founding draws and arrival times, per dose and A);
  A = 150 uses the stored intensity (t1 = 200, t0 = 500, 20,000-generation cap, 5,000 more for capped islands): no island was capped in any cell, so the
  amendment about mixed states was not exercised. Pools of 8,192 (the cut) were not needed: a 16,384-island pool costs 60 s here, against 0.1 s per island in the DSL arms.
- **Ablation law.** A family is removed from the main law and its mass goes to the constants in proportion to their weights (the other reader weights
  are unchanged); ablation cells run at P_fail 0 and 0.1, natural start only, 3 pools.
- **Starts.** The tilts are as pre-registered: the symmetrized post-anneal law, one class (F, U, or W + D with their ratio kept) rescaled to 0.6 and the
  other classes to 0.4 in proportion, within-class frequencies kept. Every tilt was available in every cell (no class had zero mass).

### 2.2 The ODE and its numerics

- Explicit adaptive integration (DOP853, rtol 1e-8, atol 1e-14) of the quadratic field on the 19,683 triples to 10^5 events per island with the field
  projected on the rotation-invariant subspace at every evaluation (symmetric trajectories), then, if criterion (a) is not met, backward Euler with
  Newton-GMRES (diagonal preconditioner, 8 geometric steps per decade, a step is halved when it lands on a negative or inaccurate root of the implicit
  quadratic) to 10^7 events (to 10^6 for the unprojected raw trajectories, which are not scored at convergence). All 162 symmetric trajectories (132 main-cell, 12 crossed-charge, 18 ablation)
  met criterion (a); the raw ones are horizon-limited at 10^6 by construction.
- Solver checks (natural start, pool 0, every cell): tightening rtol to 1e-10 changes no class share by more than 1e-12 at 10^4; halving the backward-Euler
  step (16 per decade) changes no class share by more than 3.2e-9 at the end; the explicit run to 10^6 on the 4,000-island pilot and backward Euler
  agreed to the printed digits (V\* 1.0000, G 0.0000).
- Mass is conserved to 2e-15 and the minimum entry never falls below -3e-13 (`V:ode`); the field equals the exact directional derivative's finite
  difference to 4e-13; forward Euler (dt 0.05) agrees with the adaptive solution of the logistic test to 2e-5; backward Euler to 4e-3.
- The "natural law" of the predictions is the symmetrized pool law; the raw laws were integrated separately (section 5 of the run) and show the sampling tilt amplified by the knife-edge.

### 2.3 Jacobian and perturbations

- J is computed exactly (directional derivative of the quadratic field) on the support S of x\* (threshold 1e-9, relaxed to 1e-8..1e-6 only if S exceeds
  6,000 triples; it never did), restricted to the non-invariant sector R = omega by the orbit basis (verified: the spectra of the two conjugate sectors and the
  invariant sector together are the spectrum of J on S, a test), plus matrix-free Arnoldi on the sector in the full 19,683-dimensional space (which also sees the
  absent-triple directions). The flux from S into absent triples is the "leak rate" (about 1e-14, zero within round-off at the converged limit).
- Controlled perturbations are relative (largest entry), mass-conserving by construction, integrated without projection; the growth rate is fitted where the
  non-invariant norm is between 3 N0 and 0.05.

### 2.4 Finite worlds

- 20 worlds per (cell, I) with I in {64, 256, 1024, 4096}, founded by sampling I islands iid from the pooled raw post-anneal law of the three pools, to
  10^5 events per island, with the exact kernel. Cells: main at P_fail 0.1 and 0, and dose 0 (P_fail does not matter for constants, so one dose-0 cell).
  Added beyond the spec: worlds from the unequal-tilted law at I = 1,024 and 4,096 (a check of the single-basin finding of the ODE by a method that does not
  use it), and long worlds (7b: I = 64 to 10^7, 256 to 3·10^6, 1,024 to 10^6 events per island) to see whether a fair consensus lasts. The cut order (I = 4,096
  worlds, the A = 150 cells, dose lo, the ablations) was not applied: nothing was cut.
- Event rate about 3·10^-8 s per event after compilation.

### 2.5 Costs

Table build 5 s. Pools: 60 s per 16,384 islands (A = 0), 118 s (A = 150). One symmetric ODE trajectory 50-100 s (the natural start of pool 0 also runs
the two solver checks), one raw 45-60 s. Jacobian job 100-120 s. Worlds: 65 s for 20 worlds at I = 1,024 (10^5 events per island). In all, about 3 hours of
three-worker time.
