# Predictions: the stable-set target in the Turing-complete arm under islands → ∞ before time (2026-10-29)

Committed before any code of this experiment runs and before any counted cell. Spec `specs/2026-10-29-many-islands-t.md`
(reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode amended`, both folded); notes `notes/many-islands-t.md` §1 (hand
analysis: units of w and P_fail, charges of key triples by the reading graph, expected support, exactness of the
kernel), written before this file.

## The RS's messages

> RS (2026-10-29): "Sgtm - I see farsightedness as a band-aid antithetical to the rest of the program."
> RS (2026-10-29), on this experiment: "Ur experiment sgtm."

The target (DEFERRED 15, restated 2026-10-29): in majority-division games every island lands in the stable set V\* (the
three fair pairs; the grand coalition is reported separately), with each member equally likely across independent
worlds; farsighted clauses are not part of the object; foresight must come from the programs' own play. The earlier
messages that fix the order of limits (2026-10-25): "send num islands to infinity first … shoot for (2) and tell me if and
where it fails"; "Anything needing several migrants is EVENTUALLY lost."

The question asked here: does the Turing-complete readers arm T meet the target, in this order of limits, at the default
compute charge A_f (P_fail = 0.1), and where does it fail.

## Frozen design choices (made before any run; the spec silent or open)

- Object, cells and charge as in the spec. P_fail in dollars; w = 0.3 acts on dollars (notes §1.1); fitness
  exp(w·(payoff − charge)); charge = P_fail × (failed reads in the root's own trace + forfeit), forfeit = root out of fuel,
  stuck or non-number. Failed reads are counted where an `enter_sim` frame closes on `TO` (a monkey-patched wrapper, no
  edit of `lt_code`); nested frames closed by an enclosing expiry are not counted (the stored accounting).
- Pools: 3 independent pools of 16,384 founders per cell (cut order and the cost of the founding phase may force 8,192; disclosed).
  A = 150 uses the stored intensity (t₁ = 200, t₀ = 500; 20,000-generation cap, capped islands run on 5,000 more, polymorphic
  states reported and excluded from the triple ODE as in the many-islands run).
- The ODE's time is migrant events per island. Symmetrization: x(0) averaged over the three cyclic rotations, and the
  vector field projected on the rotation-invariant subspace at every evaluation (the *symmetric* trajectory). The *raw*
  trajectory is the unsymmetrized pool law, integrated without projection. Verdicts are scored on the symmetric
  trajectories (the object for the symmetric limit) unless said otherwise; the raw ones are reported.
- Starts: **natural** (the symmetrized post-anneal law), **fair tilt** (V\* class share rescaled to 0.6), **unequal tilt**
  (U to 0.6), **wasteful/disagreement tilt** (W + D to 0.6); the other classes keep their ratios; the tilted class keeps
  its internal frequencies; a start whose tilted class has zero mass is reported as unavailable.
- Convergence (a): ‖dx/dt‖₁ < 10⁻⁹ per event and every class share changing by < 10⁻⁴ over the last decade of events,
  at some horizon ≤ 10⁷; else "unresolved". Finite-time proxy (b): V\* ≥ 0.99 at 10⁵ events. Finite-world consensus (c).
  A verdict on "V\* at convergence" uses (a); where (a) is unresolved the verdict is **unscored** and (b) is reported.
- Verdict classes: **held** iff the stated inequality holds in all three pools' symmetric trajectories; **failed** iff the
  falsifier holds in any pool; **partial** otherwise (labelled); **unscored** if unresolved or unavailable.

## The RE's predictions (from the spec, falsifiers in brackets)

1. *T meets the target's first clause at c = 0.* Dose main, P_fail 0, A = 0: V\* ≥ 0.99 at convergence from the natural
   law [V\* < 0.95 at convergence].
2. *One basin with readers.* Dose main, P_fail 0: V\* ≥ 0.99 from the unequal and the wasteful/disagreement tilts
   [any tested start converging below 0.9].
3. *Constants alone are bistable.* Dose 0: the unequal tilt converges to unequal pairs (U ≥ 0.9) and the fair tilt to
   V\* ≥ 0.9 [both tilts to the same class]. (Scored at P_fail 0 and at 0.1; constants never time out, so the two are the
   same table.)
4. *The symmetric state is a knife-edge.* At dose main (P_fail 0 and 0.1) the largest real part of the Jacobian on the
   rotation-non-invariant subspace is positive, and finite worlds end on one pair: at I = 1,024 at most 2 of 20 worlds
   keep all three pairs at ≥ 0.05 of islands at their final time [a non-positive spectrum, or ≥ 10 of 20 worlds keeping
   all three]. The finite-world clause is scored only if λ·10⁵ > ln √I (λ the measured growth rate); otherwise unscored.
   Robust content: worlds end with ≥ 0.99 of islands on fair pairs in ≥ 18 of 20 worlds at I = 1,024 [fewer than 15].
5. *The default charge does not break it.* P_fail 0.1, dose main: the ODE limit from the natural law has V\* ≥ 0.95
   [V\* < 0.9]. The least certain of the RE's predictions.
6. *Switchers carry conversion.* At dose main, removing the switchers (the four S…o… programs) lowers the ODE limit's V\*
   by more than removing the eight two-partner readers does [the reverse]. (Ablation cells at P_fail 0; also at 0.1 if
   the main cell meets question 1 and the budget allows.)

   *Counter-prediction (gpt-6.1-sol), registered:* under A_f the reader marginal is lower and conversion slower,
   possibly basin-dependent; V\* ≥ 0.95 is not confidently predicted.
   *Counter-prediction (gemini-4-argon), registered:* prediction 5 fails (V\* < 0.9 from the unequal tilt and possibly from
   the natural law), because a resident reader in one slot makes a migrant reader in another slot a reader–reader
   encounter that regresses, is charged, and can break the pair, so readers repel each other under the charge.

## The engineer's predictions (from notes §1; not the RE's; scored as stated)

E1. *No forfeits.* Zero forfeit events in all 3 × 19,683 root evaluations (the root fuel 1,200 is never reached; two expired
    reads cost ≈ 821 steps). Consequently the "forfeits without failed reads" control equals P_fail 0 exactly and A_f equals
    A on every triple [any forfeit event in the table].
E2. *Exact rotation equivariance.* Zero violations of payoff, charge and kernel tables on all 19,683 triples under (a₀,a₁,a₂) →
    (a₂,a₀,a₁) [any violation: implementation bug, the run stops].
E3. *Failed reads follow the reading graph.* Constants: 0 failed reads in every triple; S and X ≤ 1; D ≤ 2; a failed read occurs
    iff the read partner's computation re-enters the reader through a cycle of readers [any triple violating the bounds, or a
    failed read in a triple whose read graph from the root has no cycle].
E4. *Charge at founding is negligible.* Founding at P_fail 0.1 instead of 0 changes the post-anneal reader marginal by less
    than 10% (relative) and the post-anneal V\* share by less than 0.02, because only ≈ 7% of a reader's plays involve a charged
    read and selection acts through w·0.1 = 0.03 [relative change > 25% in either]. So any difference between the two ODE limits
    at the main dose is carried by the migration charge (crossed cells of question 5).
E5. *The occurring support* of a 16,384-island pool at main is between 1,000 and 5,000 triples (a quarter or less of 27³) [outside
    500-8,000]; the union of the three pools is at most twice a pool's.
E6. *The charge at P_fail 0.03 is between 0 and 0.1* for the V\* limit of the natural law at main: V\*(0.1) ≤ V\*(0.03) ≤ V\*(0) up to
    ±0.01 [non-monotone by more than 0.02].
E7. *A = 150 does not change the verdict of 1.* The V\* limit at A = 150, P_fail 0 is within 0.02 of the A = 0 value [difference > 0.05].
E8. *Dose.* The V\* limit of the natural law is non-decreasing in the dose (0 < lo ≈ main < hi) at P_fail 0, weakly (±0.01)
    [a decrease of more than 0.02 from main to hi].
E9. *Equal pairs across worlds.* Among finite worlds that end in fair consensus, the three pairs are each reached with frequency
    within a chi-square test p ≥ 0.01 of 1/3 (equivariance makes it exact in law) [p < 0.01, which is investigated, not assumed a bug].

## Scoring conventions fixed in advance

- Intervals: across the three pools (t, 2 degrees of freedom: 4.30); Wilson for world proportions; solver tolerances stated, with a
  halved-step / tightened-tolerance check for each reported limit; a verdict near its threshold (within the pool spread) is
  recomputed with a bigger pool before it is scored.
- Pool-wise ODE trajectories at events per island 10, 10², …, 10⁵ and at convergence; reader marginals at 0, 10, …, 10⁵.
- "Natural law" in predictions 1 and 5 means the symmetrized post-anneal law of each pool; the raw law is a robustness
  line and does not change a verdict unless it crosses the falsifier, in which case the verdict is **partial** and says so.
- Nothing here scores a general theorem about realizable readers: a positive result is a property of this 27-program
  library, these fuel caps and this order of limits (the spec's scope clause).
