# Spec: the stable-set target in the Turing-complete arm, with islands → ∞ before time, 2026-10-29

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`,
folded [after second review]); to be run by a Sonnet subagent. Agreed by the RS (2026-10-29: "Ur experiment sgtm"),
after the target was restated (DEFERRED 15):

> RS (2026-10-29): "Sgtm - I see farsightedness as a band-aid antithetical to the rest of the program."

The restated target (DEFERRED 15): in majority-division games every island lands in the stable set V\* (the three fair
pairs), with each member equally likely across independent worlds; farsighted clauses are not part of the object.
Follows RESULTS "Islands to infinity before time" (the only cell meeting the target is the DSL readers arm R: V\*
≥ 0.999 from every tested start on the symmetric chain, 10/10 fair endpoints in finite pools from I = 1,024), "Churn
among the fair pairs in the primary object" (arm T, the Turing-complete readers used here), "Contracts that form in
encounters" (myopic contracting fails the target) and "Charging forfeits like failed reads" (the default compute
charge A_f). REJECTED.md checked: nothing re-opened. The long-term goal asks whether the readers result holds for
realizable source-reading programs; this is that test.

## The object

As in `specs/2026-10-25-many-islands.md` (same order of limits, same statistics), with arm T in place of the DSL arms:

- **Game.** `dollar3`, payoffs in sixths, V\* = the three fair pairs; N = 100 per slot, w = 0.3, ε = 0 after founding.
- **Programs.** Arm T of `src/churn_primary_t.py` (L_T^code, the cyclic frame, frozen KS = 400, KR = 1,200): 27 programs
  per slot, the 9 constants, 8 single-partner readers (T-S, four of them switchers), 8 two-partner readers (T-D), 2
  exploiting readers (T-X). A root that runs out of fuel or is stuck plays the timeout action (ALL, 2/3) (the stored
  convention), which is the forfeit.
- **Seed laws.** The churn experiment's library doses for T: **0** (constants only, the readers' mass moved to the
  constants proportionally: the control), **lo**, **main**, **hi** (readers about 9%, 9%, 16% of the seed).
- **Compute charge.** The default A_f (DEFERRED 16): P_fail per timed-out read in the root's own trace (nested timeouts
  charged to the root, as in the merged A) and the same P_fail per forfeit, one charge per failure event; the game's
  forfeit payoff (the disagreement the timeout action produces) is kept. P_fail is in dollars (the game's raw unit;
  0.1 dollars = 0.6 sixths). [After second review] The notes state the unit in which the stored kernel's w = 0.3 acts
  (sixths or dollars, from `many_islands.pfix` and the stored PAY), convert P_fail into it, and assert fitness ratios
  on hand-built triples. Levels: **0.1** (the default, primary), **0.03**, and **0** (matched to the DSL readers arm,
  which had no charge). Fitness exp(w·(payoff − charge)).
- **Order of limits.** Founding from the seed law; annealed arrivals A ∈ {0, 150} (Poisson total, the stored intensity);
  relaxation until every slot is monomorphic (20,000-generation cap, capped islands disclosed and continued); then the
  rare-migration jump chain (one migrant at a time, recipient, donor and slot uniform, the recipient relaxed before the
  next event; time = migrant events per island).

**What is new and exact here.** With 27 programs per slot the settled state space is 27³ = 19,683 triples, and a single
migrant into a settled island is a two-type constant-fitness Moran process with the closed-form fixation probability
(1 − 1/ρ)/(1 − ρ^−N), ρ = e^(wΔπ) (neutral: 1/N). So the one-migrant kernel K is known exactly from the 27³ payoff and
charge table, and the I → ∞ dynamics are an exact ODE on the triple simplex:
dx_c/dt = Σ_s (1/3) Σ_{a, y: a with slot s ← y = c, a ≠ c} x_a q_s(y) P_fix(a, s, y) − x_c Σ_s (1/3) Σ_y q_s(y) P_fix(c, s, y)·[y ≠ c_s],
with q_s(y) the slot-s marginal of the donors. [After review] The constant-fitness formula is exact because play is
across slots only (a slot-s individual's fitness is its payoff and charge against the other two slots, which are
monomorphic while a migrant is contested); the notes confirm this in the stored kernel before relying on it. Only the founding-plus-annealing phase is simulated (it gives the initial
law x(0)). This replaces the many-islands experiment's Monte Carlo pools with an exact computation and allows a linear
stability analysis of the symmetric state.

[After review] **Symmetrization and tilts.** The symmetric trajectory and the Jacobian use x(0) averaged over the three
cyclic rotations; the raw (unsymmetrized) pool laws are run separately and their sampling tilt reported, since a
knife-edge would amplify it. A tilted start rescales the outcome-class shares of the symmetrized x(0) to the stated
target (fair tilt: V\* ≥ 0.6; unequal tilt: unequal pairs ≥ 0.6; wasteful/disagreement tilt: W + D ≥ 0.6), keeping the
relative frequencies of triples within each class, so readers are neither added nor removed except through class
weights; the reader marginal Σ_{y ∈ readers} q_s(y) of each start is reported.

[After second review] **Three statistics, kept apart.** (a) The lim_t lim_I object: the ODE's V\* mass at convergence
(convergence: ‖dx/dt‖₁ < 10⁻⁹ per event and every class share changing by < 10⁻⁴ over the last decade of events;
otherwise extend the horizon tenfold up to 10⁷ events, then report "unresolved", not a limit). (b) The finite-time
proxy: V\* ≥ 0.99 at a stated horizon. (c) Finite-world consensus at finite I. Only (a) speaks to "every island lands
in V\*" in the RS's order; (c) speaks to which pair a world picks. The vector field is exact; the initial law is
estimated (three pools; where a verdict changes between pools, enlarge the pools near it) and the integration is
numerical (report the solver tolerance and a halved-step check).

## Questions

1. **Every island in V\*.** From the post-anneal law, does the exact ODE reach V\* share ≥ 0.99, and from every tested
   start (the natural law, a fair tilt, an unequal tilt with unequal pairs ≥ 0.6 of islands, a wasteful/disagreement
   tilt)? One basin or several?
2. **Crispness.** Does the ODE converge to a fixed point (report the residual ‖dx/dt‖ and the time), cycle, or drift?
3. **Knife-edge.** At the symmetric limit, the Jacobian on the simplex tangent space restricted to the
   rotation-non-invariant subspace, support-aware (directions into absent triples reported separately, since they are
   invasion rates, not perturbations): largest real part, and the leading eigenvector's outcome-class content.
   [After second review] Controlled symmetry-breaking perturbations of amplitude 10⁻⁶, 10⁻⁴ and 10⁻² along the leading
   eigenvector and along a random non-invariant direction, with their growth compared with the Jacobian. In finite worlds (event-driven archipelagos with the exact
   kernel, I ∈ {64, 256, 1,024, 4,096}, 20 worlds each, to 10⁵ events per island or the budget): the share of islands
   on a fair pair at the end, how many worlds end with ≥ 0.99 of islands on fair pairs, the time to the first loss of a
   fair pair against I, and which pair each world ends on.
4. **Equal likelihood across worlds.** The cyclic frame makes the seed law rotation-symmetric, so if the whole
   implementation is rotation-equivariant, each pair is equally likely across worlds conditional on a world reaching
   fair consensus. [After second review] Equivariance of the payoff, charge and kernel tables is tested exhaustively on
   all 27³ triples; worlds ending in non-consensus or on unequal pairs are reported separately; the end-pair count is a
   check, and a deviation at p < 0.01 is investigated and reported, not assumed to be a bug.
5. **The charge.** Does A_f at 0.1 change 1–3 against 0? Reader–reader encounters regress and time out; a reader paired
   with a constant finishes its read and pays nothing. Report charges per play by program class and the share of
   encounters with a timeout. [After review] Two ODE-only controls from the P_fail 0.1 and 0 founding laws: failed reads
   charged without the forfeit charge (A), and forfeits charged without failed reads, to separate the two charges.
   [After second review] At dose main, founding law × migration charge crossed (founding at 0 or 0.1, migration at 0
   or 0.1, ODE only), to separate the charge's effect at founding from its effect under migration.
6. **What carries it.** Per-event rates out of each dominated class into V\* by migrant program class, and the fair-to-
   fair rates κ (to the donor's pair) and α (to the third pair), as in the many-islands report; which reader families
   carry conversion (ablations of S, D, X at the main dose if the main cell meets question 1).

## Cells

Doses {0, lo, main, hi} × P_fail {0, 0.1} at A = 0; main × P_fail 0.03 at A = 0; main × {0, 0.1} at A = 150. Eleven
cells. Founding pools of at least 16,384 islands per cell (three independent pools, so x(0) has an interval; the ODE is
run from each pool's law). Finite worlds for main and 0 at P_fail 0.1 and 0, all four I.

## Validation (before any counted cell)

- The 27³ payoff table reproduces the stored arm-T encounter outcomes (`churn_primary_t`) on every triple.
- The charge counter reproduces the merged A_f counter's rules on hand-built reader–reader and reader–constant triples.
- The exact kernel against simulated relaxation: at least 2,000 single-migrant injections into settled islands drawn
  from the main post-anneal law, fixation frequencies within binomial intervals of P_fix. [After second review]
  Stratified by selection coefficient (neutral, |wΔπ| small, large) and by timeout pattern (none, reader–reader,
  root forfeit), with at least 200 injections per stratum, including triples drawn from the ODE trajectory at 10³
  events, not only post-anneal.
- The ODE conserves mass and nonnegativity; on a hand-built 3-state system it matches the known solution; its forward
  Euler / adaptive solution agrees with the event-driven archipelago at I = 4,096 to within 0.02 of V\* share at 10³
  events.
- Founding at dose main, P_fail 0, reproduces the churn experiment's T-main mN = 0 founding statistics within noise
  (report the comparison; geometry differs, so the comparison is of the per-island founding law).

## Outputs

- Founding and post-anneal outcome-class shares per cell, with intervals.
- The ODE trajectory of the outcome-class shares (V\*, each pair, unequal, grand, wasteful, disagreement) at events per
  island 10, 10², 10³, 10⁴, 10⁵ and at convergence; from each tested start.
- The Jacobian analysis at the symmetric limit (question 3).
- Finite-world tables (question 3), with Wilson intervals.
- Charges and timeouts (question 5); rates by migrant class (question 6).
- [After review] The reader marginal per slot along each ODE trajectory (at 0, 10, 10², …, 10⁵ events), so a loss of
  readers before conversion finishes is visible.
- [After review; amended after second review] In the notes, the arm-T table at P_fail 0 against the DSL readers arm's
  table on reader–reader and reader–constant triples, as a description of where they differ; it does not attribute a
  T-versus-R difference to the timeout action rather than fuel (fuel decides whether the fallback runs).
- For the RS, a plain statement: does arm T meet the target in this order of limits, at the default charge, and where
  does it fail.

## Predictions (the RE's; falsifiers in brackets)

1. *T meets the target's first clause at c = 0.* At dose main, P_fail 0, A = 0 the exact ODE reaches V\* ≥ 0.99 from the
   natural law, as the DSL readers did [V\* < 0.95 at convergence].
2. *One basin with readers.* At dose main, P_fail 0, the ODE reaches V\* ≥ 0.99 from the unequal and the
   wasteful/disagreement tilts [any tested start converging below 0.9].
3. *Constants alone are bistable.* At dose 0 the unequal tilt converges to unequal pairs (U ≥ 0.9) and the fair tilt to
   V\* ≥ 0.9, as the DSL L arm did [both tilts to the same class].
4. *The symmetric state is a knife-edge.* At the main dose the largest real part on the non-invariant subspace is
   positive, and finite worlds end on one pair: at I = 1,024 at most 2 of 20 worlds keep all three pairs at ≥ 0.05 of
   islands at their final time [a non-positive spectrum, or ≥ 10 of 20 worlds keeping all three pairs]. [After second
   review] The finite-world clause is scored only if the measured growth rate implies escape within the budget
   (λ·10⁵ events > ln √I); otherwise it is unscored. This makes the target's first clause the robust content: worlds
   end with ≥ 0.99 of islands on fair pairs in ≥ 18 of 20 worlds at I = 1,024 [fewer than 15].
5. *The default charge does not break it.* At P_fail 0.1, dose main, the ODE limit from the natural law has V\* ≥ 0.95,
   because the readers' useful encounters (reading a constant partner) finish [V\* < 0.9]. This is the RE's least
   certain prediction: reader–reader regress is charged on every such encounter and could select readers out before
   they re-pair islands.
6. *Switchers carry conversion.* Removing the switchers (T-S with fallback o) from the main dose lowers the ODE limit's
   V\* by more than removing the two-partner readers does [the reverse].

   *Counter-prediction (gpt-6.1-sol), registered:* under A_f the reader marginal is lower and conversion slower,
   possibly basin-dependent; V\* ≥ 0.95 is not confidently predicted.
   *Counter-prediction (gemini-4-argon), registered:* prediction 5 fails (V\* < 0.9 from the unequal tilt and possibly
   from the natural law), because a resident reader in one slot makes a migrant reader in another slot a reader–reader
   encounter that regresses, is charged, and can break the pair, so readers repel each other under the charge.

The RS is invited to add predictions; the RE's genuinely uncertain one is 5.

**Scope of any success** [after second review]: a positive result is a property of this 27-program library, these fuel
caps and this order of limits, reported with support and transition structure; it is evidence about realizable readers,
not a general theorem about them.

## Required outputs

- `src/many_islands_t.py` (+ runner, report), importing `many_islands`, `churn_primary_t` and the merged A_f counter as
  needed; no existing file edited.
- `tests/test_many_islands_t.py`: the validations above that can be unit-sized (table reproduction on a sample, the
  charge counter's hand cases, the 3-state ODE, P_fix against simulation on a few triples).
- `notes/many-islands-t.md` (§1 before code: hand predictions for the payoff table's key triples — a switcher with two
  constants, two readers with a constant, three readers — the expected charges, and the expected size of the occurring
  support; §2 deviations).
- `predictions/2026-10-29-many-islands-t.md` before any counted cell, with the RS's messages first.
- `runs/many-islands-t.md` and `.json`, `runs/many_islands_t/` (small files; no `.npy`, `.npz` or `.pkl`).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** Check `ps` and free memory before each batch; at most 3 workers. One job per process; no
`multiprocessing.Pool`; one background wait per batch that exits at completion and fires if the log stops changing for
2 hours; never poll periodically. Never read or source `.env`. Cut order (disclose): I = 4,096 finite worlds, the
A = 150 cells, dose lo, the ablations.
