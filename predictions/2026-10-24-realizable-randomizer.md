# Predictions: a private random tape in the realizable language, 2026-10-24

Spec `specs/2026-10-24-realizable-randomizer.md` (reviewed by gpt-6.1-sol, then gemini-4-argon in amended mode; both
folded). Hand derivations: `notes/lt-tape.md` §1 (committed before any code, `6304e48`). Written and committed before any
code of this run exists and before any counted cell. Chain numbers (if the diagnostic runs) are ε→0 chain quantities,
lottery numbers are ε = 0 seed-lottery statistics at finite (N, I, horizon), never π. Scoring: held / failed / partial /
not scored, each with the number, in `runs/lt-tape.md` and `.json`.

## The RS's statement (2026-10-24; quoted in the spec)

* "1 sgtm as an experiment! A private random tape is an acceptable primitive." (queue item 59; the standing question is
  DEFERRED 16: can a realizable language offer a randomizer that opponents can see and simulate but not predict, at no
  cost to its user.)

The RE's reading: this is a transfer test of two DSL findings (RESULTS "Rock–paper–scissors with a compute price": once
non-play costs, the coin takes the islands; "Mixed actions in two-role games": a responsive inspector makes the
efficient outcome the modal island, commitment appears when only the inspectee reads) into L_T, where the coin is a
private tape, reading is a sound bounded prover or a checked certificate, and every step is charged. N = 100 is a transfer
test, not a limit claim.

## Scoring conventions fixed here (engineer, before any code), so no threshold can move afterwards

* **Cells.** RPS: one population, (r, m) = (3, 3), N = 100, I = 64 islands, mN = 1 (migration probability 1/N per
  event), w = 0.3, 40 runs, founders drawn per slot from the length prior over template spellings with common random
  numbers across arms (every arm keeps the full grammar's templates and prior mass: a disabled template plays the
  stated default, see below). Arms: full, no-prover (constants, mixers and simulators kept, provers, counted-probability
  readers and carriers disabled), no-tape (templates that read the tape disabled), pseudo-random-only (tape mixers and
  fallbacks replaced by quote hashes). Prices c ∈ {0, c₀}. Inspection: fixed roles, (r, m) = (2, 3), N = 100 per role,
  I = 64, mN = 1, 40 runs. Arms: full, no-prover, no-tape, inspector-only reading, inspectee-only reading. c ∈ {0, c₀}.
  Chain diagnostic, m = 4 checks and the pseudo-random-only arm in inspection are the spec's cut order and are
  disclosed if cut. **K₀ is fixed in `notes/lt-tape.md` §2 from the measured step counts of the named programs before any
  lottery cell, and c₀ = 0.12/K₀.**
* **Disabled-template defaults** (stated per class before any cell). RPS: a disabled template cycles R, P, S in index
  order of the disabled set, so no action gains founder mass. Inspection: disabled inspectors play N, disabled
  inspectees play C. For each arm the shift in founder share of the default class (against the full arm) is reported; where it
  exceeds 0.05 the renormalized arm (disabled templates removed, prior renormalized) is run beside it and reported as co-primary.
* **Horizon and intervals.** Verdicts are read at generation 2,000 (the standing convention of the DSL runs), island
  means then run means; all runs also continue to 4,000 generations (checkpoints 500, 1,000, 1,500, 2,000, 4,000). An
  island is *resolved* if its support (classes with share ≥ 0.05) is the same at 1,500 and 2,000. The unresolved
  fraction is reported and the 4,000-generation statistics are reported beside every verdict statistic; unresolved
  islands are never counted as absorbed. 95% intervals are run-clustered bootstrap (4,000 resamples of the 40 runs).
* **Statistics.** *Share* of a family = population fraction of the family's templates (island mean). *Forfeited plays* =
  expected fraction of encounters in which the program forfeits (fuel exhausted, stuck, or a non-action value),
  population-weighted. *Individual mixing* (RPS) = population fraction whose action distribution against the island's
  population is within total variation 0.05 of uniform on (R, P, S, forfeit mass counted against); (inspection) the
  fraction whose probability of inspecting (resp. cheating) against the other role's population lies in (0.02, 0.98).
  *Net exploitability* e_prog = max over the arm's templates k of the net payoff of k against the island's population;
  *individual statewise exploitability* e_indiv = Σ_x share_x max_k U_net(k, x) (the best response to each resident
  taken separately, as in the DSL's per-class e). The two are reported together everywhere. *Efficient island* (inspection) =
  both roles' mean game payoff ≥ −0.05 (the (N, C) outcome (0, 0)); *committed-and-compliant* = mean P(inspect) over the island's
  inspectors > 1/4 + 5·10⁻³ and mean P(cheat) < 0.1. *Tape mixers* = {U, B, CB} (RPS), {M, CARR} for the inspector and {Mc} for the inspectee (inspection).
  *Reader routes*: search = RI/RIM/PB/PE/PEC; enumeration = PR/PRR; check = CR/CRR; PCR counts as check. Payoffs in
  verdicts are **game payoffs**; net payoffs (gross minus c × expected steps) are reported beside them.
* **Statics.** Over the named programs and the whole catalogue: exact rational payoffs and steps (tape expectations by
  exact enumeration of the decision tree); the hand table of `notes/lt-tape.md` §1.2–1.5 is checked entry by entry.
* **Conjunctive rules.** A prediction with sub-claims is *held* if all sub-claims hold, *failed* if the stated falsifier
  trips, *partial* otherwise ("not scored" only when a required cell did not complete). A named counter-prediction gets its
  own held/failed line by the rule stated with it.

## Predictions (the RE's, verbatim from the spec; falsifiers in brackets), with scoring rules added by the engineer

1. *Statics.* 0 false atoms over all named pairs and adversarial cases; on explicitly terminating hash fixtures under
   matched execution semantics the pseudo-random control is predicted exactly by a simulator and exploited by it (+1
   in RPS), while the uniform tape mixer is not (expected 0); a biased tape mixer is exploited only to the extent of
   its bias [a false atom, an accepted bad certificate, or a simulator that predicts a uniform tape mixer].
   *Scoring:* held iff (a) the soundness test finds 0 false atoms among the derived atoms of every named pair and of the
   adaptive/nested cases (branch-dependent simulation, repeated tape reads), and 0 of the adversarial certificates (malformed,
   duplicate or omitted assignments, overlapping prefixes, over- or under-long prefixes, wrong weights, a certificate for another
   fuel stamp, a replay that reads the opponent) is accepted; (b) `SIM{100}` earns exactly +1 (to 10⁻⁹) against each `H{j}` and
   `U` earns exactly 0 against `SIM{100}`; (c) `SIM{100}` earns exactly 1/3 against `B(a₁,a₂)` (the bias, half the best response
   2/3). Failed iff the falsifier trips (a false atom, an accepted bad certificate, a simulator earning ≠ 0 against `U` beyond
   10⁻⁹). Partial otherwise.
2. *RPS, c₀.* The uniform tape mixer holds at least 0.6 of the lottery population and forfeits are below 0.1 of plays
   (the DSL priced run: `X` 0.84–0.87) [tape mixers below 0.3]. In the pseudo-random-only arm individual
   programs are predictable (statewise exploitability ≥ 0.3) [≤ 0.1]. *Counter-prediction (gpt-6.1-sol), registered:*
   deterministic individuals can form a balanced aggregate, so population exploitability may be low
   even when individuals are predictable; both are reported.
   *Scoring (full arm c₀, generation 2,000; pseudo-random-only arm c₀):* part (a): held iff the share of `U` ≥ 0.6 and forfeited
   plays < 0.1; failed iff the share of {U, B, CB} < 0.3. Part (b) in the pseudo-random-only arm: held iff e_indiv ≥ 0.3, failed iff
   e_indiv ≤ 0.1. The prediction is held iff (a) and (b) held, failed iff either failed, partial otherwise.
   *gpt-6.1-sol:* held iff in the pseudo-random-only arm e_indiv ≥ 0.3 while e_prog ≤ 0.1 (aggregate balanced, individuals predictable).
3. *Inspection, full arm, c = 0.* Efficient islands are at least 0.3 (DSL free oracle 0.65), held by the responsive
   inspector over compliant constants [below 0.1]. [After review] At c = 0 steps matter only through the fuel cap, so
   any gap to the DSL is budget-dependent; the fuel-varying cell measures it.
   *Scoring (generation 2,000):* part (a): held iff efficient islands ≥ 0.3, failed iff < 0.1; part (b) (descriptive, decides held vs partial only):
   on the efficient islands, the responsive inspectors {RI, RIM} hold more than half of the inspector population on at least half of them and
   the compliant constants {C0} hold more than half of the inspectees on at least half of them. Held iff (a) and (b), partial if (a) only, failed iff (a) failed.
4. *Inspection, inspectee-only reading, c = 0.* Committed-and-compliant islands are at least 0.5, carried by tape
   mixers with count certificates at probabilities above 1/4 (the DSL ablation: 0.91) [below 0.2].
   *Scoring (generation 2,000):* part (a): held iff committed-and-compliant islands ≥ 0.5, failed iff < 0.2. Part (b) (descriptive): on those islands carriers
   {CARR} hold more than the plain mixers among the committed inspector mass (P(inspect) > 1/4), reported as the carrier share of committed
   mass and the check-route share among inspectee readers. Held iff (a) and (b), partial if (a) only, failed iff (a) failed.
5. *Cost of the two routes* [revised after review: the ratio is fixed from the hand table, not from enumeration size].
   The notes' hand table gives the per-encounter steps of the responsive inspector's proof and of the committed
   inspector's count-certificate check; the measured ratio is within a factor 2 of the hand table's [outside].
   *Scoring:* the hand ratio is check/proof = 27/12 = 2.25 (`CR{3}` on `CARR{3}` = 27 steps against `RI` on `C0` = 12 steps, notes §1.4). Held iff the
   measured steps of the same two encounters in the static tables lie within a factor 2 of the hand values (ratio in [1.125, 4.5]) **and** the lottery-weighted
   mean steps per encounter on the check route over the search route (primary inspection cell, c = 0, generation 2,000, encounters where each route is used)
   lies in [1.125, 4.5]; partial if only the static one does; failed iff the static one is outside.
6. *Price.* At c₀ the route that the hand table makes cheaper survives the price better [the dearer route survives
   better]. [After second review] The hand table prices the responsive inspector's bounded search against a depth-1
   constant explicitly, beside a one-digit mixer's two-assignment check, since search may be the dearer route.
   *Scoring:* survival of a route = (share of its reader classes in the primary inspection cell at c₀) / (the same at c = 0), full arm, generation 2,000, run-paired.
   The hand table's cheaper route is the one with fewer total steps on the encounters it actually has in the primary cell (computed from the static tables, not
   from the lottery): the comparison is among the three inspectee routes {search (PE, PEC), enumeration (PR), check (CR, PCR)} and the inspector's search (RI, RIM).
   Held iff the survival of the cheapest of them exceeds the survival of the dearest by more than the run-clustered interval of their difference (excludes 0);
   failed iff the dearest route's survival exceeds the cheapest's with an interval excluding 0; partial otherwise (including: no resolvable difference).
   The fixed-c fuel panel (K₀/2, K₀, 2K₀ at c₀) is reported beside it.

## The engineer's own predictions (S), with falsifiers

* **S1 (the hand table is the semantics).** Every entry of `notes/lt-tape.md` §1.2–§1.5 (leaf lists, steps, cert sizes, route totals 11 / 14 / 16 / 18 / 21 / 27 / 28 / 31 / 43 / 47 / 4, W = 8 and 12 steps for `RI` against `C0`, payoff
  tables) matches the code. [any entry beyond 10⁻⁹ for values or exactly for integers; a mismatch is reported as an erratum, not fixed in the notes]
* **S2 (check beats enumeration on the same carrier).** In the static tables the certificate check is cheaper than the enumeration of the same carrier for every carrier
  CARR{1,2,3,4,6}, and `CR` on a plain mixer costs 4 steps and plays K. [any carrier where check ≥ enumeration]
* **S3 (refutation is the dear part of search).** The responsive inspector's refutation against `K0` and against every inspectee mixer costs W > 8 (more than its success against `C0`).
  [W ≤ 8 for any refuted inspectee]
* **S4 (the price is small at K₀).** At c₀ the primary inspection lottery (full arm) shows no change in efficient islands beyond the run-clustered interval
  of the c = 0 value (|Δ| < 0.1); the fuel panel at fixed c (K₀/2) is where a difference can appear. [|Δ| ≥ 0.1 at c₀ in the primary cell]
* **S5 (the tape is unpredictable and the hash is not).** In the pseudo-random-only RPS arm the share of {SIM100, PB} (the exploiters of hashes) is larger than in the full arm
  at c = 0. [not larger]
* **S6 (the carrier lowers the cost of commitment).** In the inspectee-only arm at c = 0 the committed inspector mass sits more on carriers than their founder share (prior 
  mass of carriers among committed inspector templates). [not more]
