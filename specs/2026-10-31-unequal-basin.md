# Spec: where the unequal basin of the length-prior arms comes from, with islands → ∞ before time, 2026-10-31

Status: draft by the RE; to be reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`,
folded [after second review]); to be run by a Sonnet subagent. Queue 70. Agreed by the RS:

> RS (2026-10-31), on the RE's list of next experiments ("1. Where the unequal basin comes from …"): "1 sgtm btw"

Context. The target (DEFERRED 15, restated 2026-10-29 and 2026-10-31): in majority division every island lands in the
stable set V\* (the three fair pairs), each member equally likely across independent worlds (a lottery across worlds
suffices); farsighted clauses are out of the object. RESULTS "Islands to infinity before time" (2026-10-25) found the
DSL arms L (weak evaluator) and M (modalPA), founded from the n ≤ 6 length prior, **bistable** on the symmetric
mean-field chain: L A = 0 goes to V\* 0.999 from a fair tilt and to U 0.995 from an unequal tilt; M A = 0 does the same,
and its natural start collapses onto unequal pairs (V\* 0.100 at 3·10⁴ events). The readers arm R had one basin.
RESULTS "Arm T under islands to infinity before time" (2026-10-29) then showed, with the exact mean-field ODE, that the
nine constants alone reach V\* = 1 from every tested start, unequal tilt included (the RE's prediction that constants
are bistable failed; REJECTED). So the unequal basin of L and M is not a property of constants. The RE's hypothesis:
it is carried by the length prior's conditional programs. This experiment finds which programs carry it and how.
REJECTED.md checked: nothing re-opened (the entry on prediction 3 of the arm-T run is the motivation, not an overlap).

Why it matters for the long-term goal: a realizable library with a length-like prior would inherit whatever carries
this basin. Arm T met the target with a hand-built library; if the unequal basin is carried by a specific family of
cheap conditional programs, any realizable prior that weights them heavily will fail the target in the same way.

## The object

As in `specs/2026-10-25-many-islands.md` and `specs/2026-10-29-many-islands-t.md` (same order of limits: founding,
annealing, relaxation to monomorphic slots, then rare migration with I → ∞ before time; same statistics):

- **Game.** `dollar3`, N = 100 per slot, w = 0.3, payoffs in dollars (the stored PAY), V\* = the three fair pairs.
- **Arms.** L and M exactly as in `src/many_islands.py` (`Arm('L')`, `Arm('M')`): the 1,305 canonical functions of the
  `dollar3` grammar at n ≤ 6, weak (L) or modalPA (M) evaluator, seed law `stable_sets.seed_law('L', s)` (the length
  prior) for every slot.
- **Founding.** 3 fresh pools of 16,384 islands per arm and cell, built by `many_islands_run.build_pool` (the stored
  pools' `.npz` files were not committed). A = 0 primary; A = 150 secondary (first to cut).
- **Mean-field object.** The exact ODE of the arm-T run (`src/many_islands_t_ode.py`: dx/dt over triples, time in
  migrant events per island, donors from the slot marginals q_s, closed-form Moran fixation PF), carried over to L and
  M. At ε = 0 the slot supports never grow: a migrant is drawn from an existing marginal. So the reachable state space
  is the product of the post-anneal slot supports (about 700 programs per slot in the stored pools), too large for a
  dense field. **The object computed is the empirical-start ODE** [after second review]: the I → ∞ dynamics started
  from the post-anneal law of a finite founding sample (the union of a cell's 3 pools, 49,152 islands). A program with
  positive founding probability that no sampled island settled on is absent from it. Report the seed-law mass of the
  programs absent from the union's supports, compare the endpoint and u\* from one pool against the 3-pool union
  (support sensitivity), and restrict every conclusion to the empirical start. Two reductions, in this order:
  1. **Exact behavioural lumping.** Two programs y, y′ of slot s are merged iff, for every pair of programs of the
     other two slots in the supports, the triple with y and the triple with y′ give the same joint code (all three
     actions) **and the same divergence vector** (which slots diverge; at P_fail > 0 a divergent (ALL, 2/3) is charged
     and a returned one is not) [after review]. The supports are the **S₃-union** of the three slots' post-anneal
     supports (each slot's support mapped through `permute_support` and united), **plus all nine constants** (the
     ablations' replacement targets) [after second review], computed before lumping, so the quotient is the same in
     every slot and S₃-equivariance survives [after review]. Lumping is for integration only: the start law, every
     ablation and every attribution act on program-level masses (each program keeps its syntactic family and its own
     mass inside its behavioural class) and are lumped afterwards [after second review]. Because the supports cannot
     grow, this lumping is exact for all time. Report the class counts per slot.
  2. **No pruning of the state** [after review: θ-pruning would reintroduce the support truncation that question 1
     is about]. The state x keeps every reachable lumped triple at all times. If the class count C per slot makes a
     dense field too slow (the field costs about 3·C⁴ fixation lookups per evaluation), the only permitted
     economy is on the donor side: skip migrants y with q_s(y) < 10⁻¹⁵ in an evaluation, accumulate the skipped
     inflow, report the total omitted donor rate over the trajectory, rerun every cell whose verdict is decisive
     without skipping, and never set any x to zero [after second review]. If even that is infeasible, stop and report the class
     counts before running anything counted.
  Either way the result is validated against the stored pool Monte Carlo (V below).
- **Symmetry.** The `dollar3` grammar is S₃-symmetric (`many_islands.permute_support`); symmetric trajectories start from
  the S₃-average of the pool law and project the field on the invariant subspace, as in the arm-T run. Raw pool laws
  are run unprojected and reported separately.
- **Starts.** Natural (symmetrized post-anneal law), fair tilt, unequal tilt, wasteful-plus-disagreement tilt: the
  class share rescaled to 0.6, within-class frequencies kept (the arm-T construction). In addition, a **tilt scan** on U:
  the unequal class rescaled to u ∈ {0.3, 0.4, …, 0.9}. The endpoint class (U-dominated: U ≥ 0.5 at convergence;
  V\*-dominated; other) is reported at every scanned u, with every transition between neighbouring scanned values
  refined by bisection to ±0.02 [after second review: the classification need not be monotone in u]. The **basin
  boundary** u\* is the first U-dominated crossing within the scanned range, reported with the range; u\* = "none" if no
  u ≤ 0.9 is U-dominated. u\* is the scalar every ablation is compared on.
- **Convergence.** As in the arm-T run: ‖dx/dt‖₁ < 10⁻⁹ per event and every class share moving < 10⁻⁴ over the last
  decade of events, at some horizon ≤ 10⁷; else "unresolved", and verdicts that need the limit are unscored. Because
  rare donors can rescue late [after second review], a U-dominated endpoint is certified only if, in addition, no
  class with mass below 10⁻³ has a positive relative growth rate at the horizon, and the residual stays below
  10⁻⁹ when the solver tolerance is tightened tenfold; report each rare class's growth rate and, where positive, the
  implied time to reach 10⁻² mass. Otherwise the endpoint is reported as **metastable**, not as a basin.
- **Compute charge.** The default A_f at P_fail = 0.1 dollars (DEFERRED 16), with P_fail = 0 as the control. Mapping to
  the DSL: in the weak evaluator any atom that reads a bottom value leaves its slot bottom, so a failed read and a
  forfeit are the same event, a divergent root playing (ALL, 2/3); A_f charges P_fail once per divergent slot per
  encounter. The modalPA evaluator always returns (the engineer checks this on the whole support, counting any
  `eval_modal` non-convergence), so in M the charge is vacuous and M is run once, the P_fail = 0.1 cell being identical
  by construction (verified on the table, not assumed). Founding and migration both use the cell's charge (L at 0.1
  needs its own pools); a crossed cell (founding at 0, migration at 0.1) for L only, as in the arm-T run.

Cells: L × {0, 0.1}, M × {0}, at A = 0; then L × 0 and M × 0 at A = 150. Five cells, 3 pools each.

## Questions

1. **Does the unequal basin exist in the exact ODE?** For L and M at A = 0: the endpoint from each start, and u\*. The
   stored bistability came from a Monte Carlo of resampled pools whose slot supports collapsed to about 10 programs per
   slot by 3·10⁴ events; the exact ODE keeps every program at positive mass. If the exact ODE has no unequal basin, the
   stored bistability was a finite-pool effect, and that is the answer.
2. **Which family carries it?** Matched ablations of the seed law, each compared on u\* and on the natural-start
   endpoint:
   - *Families by syntax* (from the canonical function's essential atoms): **C** constants; **A1** one essential atom;
     **A2s** two essential atoms reading the same other slot; **A2x** two atoms reading both other slots.
   - *Ablation rule, primary: on the start law, no refounding* [after review]. Remove the family's programs from the
     symmetrized post-anneal triple law: a triple containing a removed program in slot s is reassigned to the triples
     with that slot replaced by each constant, in proportion to the constants' own slot-s marginal (the arm-T rule
     applied at the triple level); then run the ODE and the tilt scan. This costs no founding time and separates the
     migration basin from founding effects. Each family is removed alone; "all conditionals" (constants only) is the
     control that must agree with arm T's dose-0 behaviour (one basin). A second rule, dropping the family's triples
     and renormalizing, is run for the family that moves u\* most (a check that the effect is not the constants'
     extra mass).
   - *Ablation rule, secondary: on the seed law, refounded.* The same families removed from `seed_law('L', s)` (mass to
     the constants proportionally), 3 pools refounded, the ODE rerun: what the family does through founding. First to
     cut after A = 150.
   - *Data-driven attribution.* At the unequal endpoint of the U-tilted trajectory, list the behaviour classes with
     mass ≥ 10⁻³ per slot. For each of the top 20 by mass, remove it from the start law (its mass to the constants as
     above, no refounding) and recompute u\*. Rank classes by the shift in u\*. Because a basin held by complementary
     programs can survive any single removal [after review], also remove the top k classes jointly, k ∈ {1, 2, 5, 10,
     20}, to find the smallest knockout set, and remove jointly all top-20 classes that sit in pair slots against all
     that sit in the excluded slot of the dominant unequal triples. Report the full program-by-role association at
     the unequal endpoint (each program's mass in the high, low and excluded roles), not only marginal masses
     [after second review].
   - *Controls for abundance and sufficiency* [after second review]. For every knockout that moves u\*, a matched-mass
     random knockout (conditional classes drawn at random until the removed mass matches, 10 draws) gives the shift
     expected from removing that much conditional mass. For the smallest knockout set, a **restoration test**: put the
     removed classes back at 0.25, 0.5 and 1 times their mass and report u\* at each dose. Necessity plus a
     dose-dependent rescue is the claim; a single failed knockout cannot distinguish redundancy from irrelevance and is
     reported as such.
3. **How do the carriers hold an unequal island?** Static analysis at the unequal endpoint: for the dominant unequal
   triple(s), every single-migrant move that would take the island to a fair pair when all residents are constants
   (the rescue moves: the underpaid member switching to an excluded slot that offers it ½, or the excluded slot
   offering ½ to the underpaid member), its payoff change Δ and P_fix in the endpoint's actual composition, and which
   resident's program blocks it (the excluded slot not offering, the high demander retaliating against a switch, or
   something else). Decompose the U → V\* flux per event at the endpoint by migrant class and recipient slot role
   (high demander, low demander, excluded). Show source and action table of each decisive program.
   *Tilt check* [after review]: the U tilt keeps within-class frequencies, so if conditional programs are
   over-represented among unequal islands at founding, the tilt also inflates their donor share. Report each slot's
   conditional marginal share at t = 0 for every start, and test the U endpoint for self-consistency: mix 1% and 10%
   of the natural law into it and check whether it returns to U.
4. **Is the unequal endpoint stable, and how?** Jacobian at the U endpoint (support-aware, as in
   `many_islands_t_jac.py`), with three spectra kept apart [after second review]: the invariant subspace (S₃-symmetric
   perturbations), the transverse (symmetry-breaking) sectors, and the full simplex including invasion by triples
   absent from the endpoint's support (reported as leak rates). The leading eigenvalue on class-changing directions
   in each; perturbations of 10⁻⁶, 10⁻⁴, 10⁻² toward V\*, and small asymmetric ones, with their fate. State which
   programs are excluded by the empirical-support approximation. Compare with arm T's
   single-pair fair endpoint of constants (all eigenvalues zero within 10⁻⁶ on the support).
5. **Does the default charge change it?** u\* and the natural endpoint in L at P_fail 0.1 against 0, with the crossed cell.

## Validations (before any counted cell)

- **V1. Arm independence of constants.** With only constants, the L ODE's table and PF must equal arm T's dose-0 table
  and PF after mapping actions and slot conventions (arm T uses the cyclic frame); started from arm T's dose-0 law, the
  L constants-only ODE must reproduce arm T's dose-0 V\* at 10², 10³, 10⁴ events to 10⁻⁶.
- **V2. Lumping is exact.** On 10⁴ random reachable triples, the lumped field equals the unlumped field (computed
  sparsely) to 10⁻¹²; class counts per slot reported.
- **V3. ODE against a matched Monte Carlo** [after second review]. The correctness gate: a fresh pool Monte Carlo
  (`many_islands_run.run_chain`, 262,144 islands resampled from exactly the same symmetrized empirical law, 3
  replicates) agrees with the ODE at 10², 10³ and 3·10³ events within its replicate band (or 0.01, whichever is
  larger). Replication, not a gate: the rebuilt pools against the stored post-anneal V\* 0.280 (L) and 0.277 (M) at
  A = 0, and the ODE against the stored symmetric chain (`runs/many_islands/sym_*_A0_sym.json`), whose later
  checkpoints are where the pool's support collapse may matter.
- **V4. Kernel.** The exact kernel matches simulated relaxation (`many_islands.island_run`) in ≥ 6 strata (selection
  sign × slot role), 200 injections each, |z| < 3 throughout.
- **V5. Charge.** The divergence count per triple and slot in L, and zero non-convergence in M on the full support.
- **V6. Symmetry.** The table and PF are exactly S₃-equivariant on the support (0 violations).

## Required outputs

`runs/unequal-basin.md` and `.json`, rows in `runs/unequal_basin/`; notes `notes/unequal-basin.md` (§1 hand analysis
before code: what a constants-only rescue move needs, which program shapes could block it, and a hand prediction of
the carrier; §2 deviations). Tables: per cell and start, V\*, U, G, W + D at 0, 10², 10³, 10⁴, 10⁵ events and the limit;
u\* per cell and per ablation (with the endpoint class at each scanned u); the attribution ranking (top 20 classes:
source, slot role at the endpoint, mass, Δu\*); the rescue-move table and the flux decomposition; the Jacobian table;
the lumping and threshold diagnostics. Always report support and transition structure alongside shares (CLAUDE.md
discipline 4). Drafts for RESULTS, REJECTED, THEORY, NOTATION in `notes/unequal-basin-drafts.md`.

## Predictions (RE, registered before the run)

1. **The basin exists.** In the exact ODE at A = 0, P_fail 0, both L and M end U-dominated (U ≥ 0.9 at convergence) from
   the 0.6 unequal tilt. *Falsifier:* either arm ends with V\* ≥ 0.9 from that start. (Confidence about 0.65; the
   alternative is that the stored bistability was the Monte Carlo's support collapse.)
2. **Natural starts.** L ends with V\* ≥ 0.99 from its natural start; M ends U-dominated (U ≥ 0.5) from its natural start,
   as in the stored chain. *Falsifier:* L below 0.99, or M with V\* ≥ 0.5. (Confidence 0.8 for L, 0.5 for M.)
3. **Conditionals carry it.** Removing all conditional programs (constants only) removes the basin in both arms
   (u\* = none). *Falsifier:* the constants-only cell has u\* ≤ 0.9. (Confidence 0.85; V1 checks one constants-only
   start, not the correlated laws that replacement and tilting produce.)
4. **Which family.** Removing A1 alone removes the basin (u\* = none) in both arms, while removing A2s and A2x (together
   or alone) leaves u\* within 0.1 of the full arm. *Falsifier:* A1 removal leaves u\* ≤ 0.9, or removing A2s or A2x moves
   u\* by more than 0.1. (Confidence 0.4: I do not know whether one atom suffices.)
5. **Mechanism: the excluded slot.** The decisive classes (largest Δu\* in the attribution) sit in the excluded slot of
   the dominant unequal triples, and they block the constants' rescue move by not offering ½ to a switching low
   demander (they condition on what the pair plays). *Falsifier:* the top-ranked class sits in a pair slot, or the
   blocked rescue is blocked by retaliation from the high demander. (Confidence 0.5.)
   *Counter-prediction (gemini-4-argon):* the obstruction sits in the pair slots, a conditional low demander that
   accepts 1/3 against a 2/3 demander and does not switch to the excluded slot unless the excluded slot already offers
   it ½, or a high demander that punishes defection; an excluded slot offering ½ invades neutrally, so it cannot be the
   block.
6. **Stability.** The unequal endpoint is linearly stable on its support, with a strictly negative leading eigenvalue on
   class-changing directions (≤ −10⁻⁵ per event), unlike the neutral single-pair endpoint of constants. *Falsifier:* a
   leading eigenvalue ≥ −10⁻⁶ (neutral or unstable) on those directions. (Confidence 0.6.)
   *Counter-prediction (gpt-6.1-sol):* at least one arm has a near-zero mode at the unequal endpoint, or its stability
   on the support does not extend to the transverse directions; at ε = 0 the faces with missing donors are invariant,
   so neutral directions and non-hyperbolic attraction are plausible.
7. **The charge.** In L, A_f at P_fail 0.1 moves u\* by less than 0.05 against P_fail 0. *Falsifier:* |Δu\*| ≥ 0.05.
   (Confidence 0.7; divergent programs are a small part of the founding law, but a divergence-prone carrier would
   change this.)

The RS is invited to add predictions; the most uncertain are 1 and 4.

## Scale and cuts

At most 3 workers (2 while another subagent is alive). Pools: 5 cells × 3 (about 15 pools of 16,384 islands at about 30 minutes each, so about 2.5 hours on 3 workers), plus
the secondary refounded ablations (4 families × 2 arms × 3 pools, about 4 hours). The primary ablations and the
attribution need no pools. Cut order if needed: A = 150 cells; the refounded ablations; the crossed charge cell; the
renormalized check. Do not cut V1–V6, the tilt scans at A = 0 or the attribution.

## Scope

A statement about the n ≤ 6 `dollar3` grammar under the length prior, in this order of limits. The families are
syntactic classes of a small DSL; the answer says which kind of cheap conditional program a length-like prior must not
weight heavily for the stable-set target to hold, and it is a prediction for realizable libraries, not a result about
them. Efficiency and fairness here are evaluations of the outcome, never selectors.
