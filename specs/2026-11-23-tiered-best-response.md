# Spec: do the object's surviving programs best-respond in tiers? (queue 81)

## Context

The RS's statement of what the object produces after a long time (OH doc, main tab, 2026-11-23):

> Each program best-responds lexicographically. First, to the island's native population. Next, to the distribution
> of migrants. Finally, to the mutation prior.

It is his definition of a credible threat: credibility is not an axiom but a long-run property of the object.
PROOFS P10 (the tiered fixation lemma) gives the mechanism under an assumption: on an island fixed on a profile, a
variant that plays the same against the natives fixes with N·ρ → σ/(1 − e^(−σ)), where σ = (w/f)·Σ_q m_q T_q Δ_q sums
over testers q (migrants, then tail arrivals) their arrival rate m_q, lineage lifetime T_q and the variant's payoff
advantage Δ_q against them. Assumption A of the lemma (testers form a stationary field unaffected by the variant) is
not proved for the object.

The RE's caveats, to be tested: (1) the migrant tier is empty in a world at consensus, and worlds with migration tend
to consensus; (2) each tier is a bias of strength σ, not a filter, and at the usual doses (mN = 1, Λ = 100 per island
per run) the migrant tier is of order one and the prior tier negligible; (3) best response is among variants that
actually arrive.

This is a check of a claim about existing machinery. It re-opens nothing in REJECTED.md: the entries on credibility
(static clauses; the gene arm's per-point and whole-program filters) concern axioms, and this is a measurement.
All population numbers are finite-schedule statistics, not π, and must be reported as such.

## Object and arms

Two arms, both table-based and cheap. Use the existing code and stored tables; do not rebuild the languages.

- **Arm T (majority division, the current object).** `src/majority_tail.py`, `src/majority_tail_kern.py`,
  `src/majority_tail_run.py`, the 27-program library of `src/churn_primary_t.py`; arm M (the DSL length-prior arm of
  the same code) as the second catalogue. Queue 74's settings: I = 64, seed lottery plus the annealed tail, charge
  A_f at 0.1. RESULTS "Majority division in the current object".
- **Arm P (modal PD with rival networks).** `src/bridgeless_rivals.py` and the island code it uses (`src/islands.py`),
  the free-box modal language at n = 8, where permanent patchworks of rival cooperative networks exist at N ≥ 200
  (RESULTS "Bridge-less rivals"). This arm supplies worlds that stay diverse.

If one arm's code cannot save end states without more than a day's work, say so and run the other only.

## Definitions (fix these before any run; put them in NOTATION drafts)

- **World state at time t:** for each island and slot, the majority program (and its share).
- **On-path equivalent of p in slot j on island k:** a catalogue program p′ that plays the same action as p against
  the island's majority programs in the other slots and leaves every slot's payoff there unchanged. The set is
  E(p; k), and always contains p.
- **Migrant distribution seen by island k:** the majority programs of the other islands, slot by slot, weighted by
  island count (the migration kernel of the arm, if it is not uniform, replaces the count weights; say which).
- **Migrant payoff of p′ ∈ E(p; k):** the expected payoff to slot j when one other slot's resident is replaced by a
  draw from the migrant distribution for that slot (average over the other slots), the remaining slots resident.
  **Migrant regret of p:** the best migrant payoff in E(p; k) minus p's. Zero regret means p is a best reply to the
  migrants among its on-path equivalents.
- **Prior regret:** the same with the replacement drawn from the arm's tail law.
- **Controls.** For each (island, slot, resident p): (a) the *prior-matched control*, a draw from E(p; k) by the
  arm's seed law; (b) the *supply control*, a draw from E(p; k) restricted to programs present anywhere in that
  run's founders. Report the share of zero regret and the mean regret for residents and for both controls.
- **Diverse world:** at least two distinct island majority profiles, each on at least 5% of islands.
- **Vacuous cases** must be counted and excluded from regret shares, and reported: islands where E(p; k) = {p}, and
  slots whose migrant payoff is the same for every member of E(p; k).

## Stages

**Stage 0, the lemma against simulation (no population arm).** One slot, Moran, N ∈ {100, 400}, w = 0.3, a resident
and one on-path-equivalent variant, one tester type.
- 0a (assumption A by construction): testers met independently with probability ε = mT/N. Fixation from one copy,
  10⁵ replicates per point, σ ∈ {−3, −2, −1, −0.5, 0, 0.5, 1, 2, 3}. Compare N·ρ with σ/(1 − e^(−σ)).
- 0b (real testers): testers arrive as single individuals in the partner slot at rate m per generation and live or
  die under selection there; their own payoff may depend on whether they meet residents or variants (three cases:
  tester indifferent; tester does better against the variant; tester does worse against the variant). Measure T
  from the simulation with residents only, form σ, and compare. Same grid of σ by varying m.

**Stage 1, existing or regenerated worlds.** For arm T, arm M and arm P at their published main cells (arm T and M:
N ∈ {100, 200, 400}, mN = 1, Λ = 100; arm P: the dense and natural cells at N = 200 with migration), obtain end
states for 20 runs per cell (re-run with the published seeds and save states if they were not stored; confirm the
published headline statistic is reproduced before using any new state). Compute migrant regret, prior regret and
the controls at the horizon, split by diverse and consensus worlds.

**Stage 2, dose.** In each arm at one N (arm T and M: N = 200; arm P: N = 200), mN ∈ {0.1, 1, 10} and, at mN = 1,
tail dose Λ ∈ {0, 100, 1,000} where the arm has a tail. 20 runs per cell, same horizon as stage 1. Record regret
at 25%, 50% and 100% of the horizon, and the share of diverse worlds at each.

**Stage 3, variant supply (only if stages 1–2 leave budget).** At arm M, N = 200, mN = 1: add to the tail, at dose
Λ = 100, a law concentrated on the on-path equivalents of the programs that held islands in stage 1 (a supply of
exactly the variants the statement is about). Does migrant regret fall further?

## Required outputs

`runs/tiered-best-response.md` (report), `runs/tiered-best-response.json` (verdicts and tables), row files under
`runs/tbr_rows/`, notes with every deviation, drafts for RESULTS, REJECTED and NOTATION. For each cell: share of
diverse worlds; counts of vacuous cases; zero-regret share and mean regret for residents and both controls, with
bootstrap 95% intervals over runs; for stage 0 the table of N·ρ against the formula. Name three concrete islands
where a resident has positive migrant regret, with the better variant and the migrant that separates them, and three
where a costly threat is carried with zero regret (if any exist). State what the model cannot express.

## Predictions (the RE's; copy to `predictions/2026-11-23-tiered-best-response.md` before stage 0)

- **RE 1 (lemma under A).** In 0a, N·ρ is within 10% of σ/(1 − e^(−σ)) at every σ and both N. Falsifier: a point
  off by more than 20%.
- **RE 2 (real testers keep the sign).** In 0b, N·ρ is above 1 whenever σ ≥ 0.5 and below 1 whenever σ ≤ −0.5, in
  all three tester cases; with an indifferent tester it is within 25% of the formula. Falsifier: a wrong sign at
  |σ| ≥ 0.5, or an indifferent-tester point off by more than 40%.
- **RE 3 (the pattern exists in diverse worlds).** In diverse worlds at mN = 1, pooled over arms that have at
  least 100 non-vacuous (island, slot) cases, the residents' zero-migrant-regret share exceeds the prior-matched
  control's by at least 0.15. Falsifier: a difference below 0.05.
- **RE 4 (most of it is supply).** Against the supply control the excess is smaller: below half of the excess
  against the prior-matched control. Falsifier: at least as large.
- **RE 5 (dose).** The residents' zero-regret share in diverse worlds rises with mN from 0.1 to 10 in each arm that
  has diverse worlds at both ends, by at least 0.1. Falsifier: a fall, or a rise below 0.03, in every such arm.
- **RE 6 (consensus empties the tier).** In arm T at mN = 1 fewer than half of the worlds are diverse at the
  horizon, and fewer at mN = 10; arm P keeps a majority of worlds diverse at N = 200. Falsifier: arm T diverse in
  at least half of worlds at mN = 1.
- **RE 7 (the prior tier is negligible at our doses).** In consensus worlds the residents' zero-prior-regret share
  is within 0.05 of the prior-matched control's at Λ = 100, and rises by less than 0.1 at Λ = 1,000. Falsifier:
  an excess of 0.15 or more at Λ = 100.
- **RE 8 (time).** Mean migrant regret of residents in diverse worlds does not rise between 25% and 100% of the
  horizon in any arm. Falsifier: a rise beyond the bootstrap interval.

## Amendments after the first review [after review] (these override the text above where they differ)

- **Exact on-path equivalence.** p′ ∈ E(p; k) iff replacing p by p′ in slot j, with the other slots at their
  majority programs, leaves the whole payoff vector of the encounter unchanged (every slot's payoff, read from the
  full table, so that a native reader's reaction to p′'s source is included). **One-population arms (arm P):**
  p′ ∈ E(p; k) iff u(p′, p) = u(p, p′) = u(p′, p′) = u(p, p). Migrants join the same pool; the migrant payoff of
  p′ is its expected payoff against a migrant q drawn from the other islands' majorities, Δ_q = u(p′, q) − u(p, q).
- **Two weightings.** Report regret with testers weighted by arrival (the RS's words) and by arrival times
  lifetime, m_q·T_q (P10's σ), with T_q the mean copy-generations of a single q arriving on that island's native
  profile (from the exact single-mutant sojourn where the arm has it, else simulated). The primary statistic for
  RE 3–5 and RE 8 is the T-weighted one; the arrival-weighted one is reported beside it.
- **Settled islands only.** Regret shares use islands whose majority share is at least 0.8 in every slot; report the
  excluded fraction per cell. Report **native regret** too (the share of residents that are not a best reply to
  their own island's majority profile within the catalogue): tier 1 has to hold before tier 2 means anything.
- **Supply control weighted by founders.** Draw the supply control from E(p; k) ∩ founders with weights equal to
  founder counts in that run.
- **Stage 0b.** Use testers that are selected against by the natives (relative fitness 0.7 and 0.9) and a neutral
  tester; a tester lineage that reaches half of its slot ends the replicate, which is discarded and counted.
- **Doses.** mN ∈ {0.1, 1, 3, 10}. **RE 5 revised:** the T-weighted zero-regret share of residents on settled
  islands in diverse worlds is higher at mN = 1 than at 0.1 by at least 0.05 in each arm with diverse worlds at
  both; mN = 3 and 10 are reported without a prediction (the reviewer expects diversity to collapse or islands to
  stop being settled there; record the settled fraction). Falsifier: lower at 1 than at 0.1 in every such arm.
- **RE 7 revised.** Scored at Λ = 100 only; Λ = 1,000 is exploratory. Report the share of tail arrivals that land
  in the second half of the horizon under the arm's annealing schedule.
- **Survival against replacement.** Save the majority program of every island and slot at 25%, 50%, 75% and 100% of
  the horizon. For each resident with zero migrant regret at the horizon, classify how it got there: (a) it
  replaced an on-path equivalent with positive regret on the same island after 25%; (b) it held the island from
  25% on; (c) the island was taken over from another profile. **RE 9 (the RE's):** route (a) accounts for less
  than a quarter of zero-regret residents in every arm; the pattern, where it exists, is mostly islands with
  low-regret residents lasting longer or colonizing, not within-island replacement of threats. Falsifier: route
  (a) at or above one half in some arm.

## Amendments after the second review [after review] (these override everything above where they differ)

- **Tier 3 is scored inside tier 2.** Prior regret is computed within the members of E(p; k) that maximize the
  migrant payoff (a migrant-optimal resident may give up payoff against the prior); the unconditional prior regret
  is reported beside it. Migrant claims are scored on residents with zero native regret, and reported for all.
- **Tester lifetime.** T_q is the mean copy-generations of a single arrival until its lineage is extinct or reaches
  half of its slot (establishment); report the establishment probability with it. In stage 0b a replicate ends in
  one of three outcomes (variant fixes, variant lost, tester establishes); all three are reported and none is
  discarded; N·ρ is compared with the formula on all replicates, with establishment counted as "variant not fixed".
- **Native populations, not majority profiles.** Save the full composition of every island at the horizon. Native
  regret and on-path equivalence are also computed against the actual composition; report the main statistics at
  majority share ≥ 0.8 and ≥ 0.95.
- **Stage 1b, frozen natives (direct test of the statement on fixed profiles).** For the ten most common island
  profiles of each arm's stage-1 worlds: freeze the natives, take the world's migrant distribution as an exogenous
  tester field with the arm's mN, and compute for every member of E the exact or simulated N·ρ from one copy
  against the resident. Report it against P10's σ. This does not condition on which worlds or islands survive.
- **Doses are paired.** The same founder seeds at every mN and Λ. Report the unconditional joint table (share of
  worlds diverse, share of islands settled, share with nonempty E) beside every conditional statistic.
- **Routes.** Log every change of an island-slot majority (time, old program, new program, and whether the new
  program's first copy on that island was a founder, a migrant or a tail arrival) where the arm's code allows it at
  less than 20% overhead; routes are then exclusive in the order (c) taken over by a migrant's profile, (a) replaced
  by an on-path equivalent, (b) held, (u) unresolved. If transitions cannot be logged, RE 9 is reported as a
  snapshot description and scored "not tested".
- **Arrival opportunity.** Where arrivals can be logged, the supply control uses programs that arrived on the island
  while the horizon profile was resident; otherwise the founder-weighted control stands and is labelled an
  approximation.
- **RE 1 revised.** Each point is compared with the exact finite-N formula using a binomial 95% interval; the
  prediction is that at least 16 of the 18 points contain it. Falsifier: fewer than 14.
- **RE 8 revised.** Pooled over arms, the paired change in residents' mean T-weighted migrant regret on settled
  islands of diverse worlds between 25% and 100% of the horizon is not positive. Falsifier: positive with the
  bootstrap interval excluding zero.
- **Conventions.** Zero regret means at most 10⁻⁹; a case with an empty control set is dropped from that control's
  comparison and counted; bootstrap resamples runs; a prediction with fewer than 100 non-vacuous cases is scored
  "inconclusive".
- **Scope to state in the report.** Finite horizon, catalogue-relative: low regret can come from founding abundance,
  the catalogue's geometry, colonization or survival as well as from refinement of threats; nothing here
  establishes a large-N limit.

## Budget and operations

Local, at most 3 workers, target 40 CPU-hours; Daytona (`tools/daytona_run.py`) allowed up to 60 sandbox-CPU-hours
if stage 2 needs it, and `python3 tools/daytona_run.py list` must be empty at the end. Do not read `.env` or any
environment file; never print or commit keys. Do not commit `.npz`, `.pkl` or large `.npy` files; row files as
`.jsonl` or `.json.gz` under 5 MB each. Commit predictions before stage 0 and again (stage-2 scoring rules) before
stage 2 if anything in the definitions had to change. Work in your worktree; do not push. Cut order if short:
stage 3, then arm M in stage 2, then Λ = 1,000.
