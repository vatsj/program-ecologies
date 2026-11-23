# Predictions: do the object's surviving programs best-respond in tiers? (queue 81)

Spec `specs/2026-11-23-tiered-best-response.md` (with both review amendments folded; the second overrides the first,
both override the original text). Mechanism under test: PROOFS P10 (the tiered fixation lemma). These are the RE's
predictions, copied verbatim in their amended form, committed before stage 0. All population numbers are
finite-schedule statistics, not π.

## Scoring conventions (spec, second amendment)

- Zero regret means at most 10⁻⁹.
- A case with an empty control set is dropped from that control's comparison and counted.
- Bootstrap resamples runs (percentile 95%).
- A prediction with fewer than 100 non-vacuous cases is scored "inconclusive".
- Verdict words: "holds", "falsified" (the falsifier fired), "fails, falsifier not fired", "inconclusive",
  "not tested".
- Primary statistic for RE 3–5 and RE 8: the T-weighted migrant regret (testers weighted by m_q·T_q, P10's σ);
  the arrival-weighted statistic is reported beside it.
- Regret shares use settled islands (majority share ≥ 0.8 in every slot); the excluded fraction is reported per
  cell; main statistics are also reported at ≥ 0.95. Migrant claims are scored on residents with zero native
  regret and reported for all.
- Prior regret (tier 3) is scored inside tier 2: within the members of E(p; k) that maximize the migrant payoff;
  the unconditional prior regret is reported beside it.
- Vacuous cases (E(p; k) = {p}; or migrant payoff equal for every member of E(p; k)) are counted and excluded from
  regret shares.

## Predictions

- **RE 1 (lemma under A), revised.** In stage 0a, each of the 18 points (9 values of σ × N ∈ {100, 400}) is compared
  with the exact finite-N fixation formula using a binomial 95% interval; at least 16 of the 18 points contain it.
  Falsifier: fewer than 14.
- **RE 2 (real testers keep the sign).** In 0b, N·ρ is above 1 whenever σ ≥ 0.5 and below 1 whenever σ ≤ −0.5, in
  all three tester cases; with an indifferent (neutral) tester it is within 25% of the formula. Falsifier: a wrong
  sign at |σ| ≥ 0.5, or an indifferent-tester point off by more than 40%. (Tester cases per the first amendment:
  testers selected against by the natives at relative fitness 0.7 and 0.9, and a neutral tester. Per the second
  amendment each replicate ends as variant fixes / variant lost / tester establishes; all three reported, none
  discarded; N·ρ is computed on all replicates with establishment counted as "variant not fixed".)
- **RE 3 (the pattern exists in diverse worlds).** In diverse worlds at mN = 1, pooled over arms that have at least
  100 non-vacuous (island, slot) cases, the residents' zero-migrant-regret share exceeds the prior-matched control's
  by at least 0.15. Falsifier: a difference below 0.05.
- **RE 4 (most of it is supply).** Against the supply control the excess is smaller: below half of the excess
  against the prior-matched control. Falsifier: at least as large.
- **RE 5 (dose), revised.** The T-weighted zero-regret share of residents on settled islands in diverse worlds is
  higher at mN = 1 than at 0.1 by at least 0.05 in each arm with diverse worlds at both; mN = 3 and 10 are reported
  without a prediction (record the settled fraction). Falsifier: lower at 1 than at 0.1 in every such arm.
- **RE 6 (consensus empties the tier).** In arm T at mN = 1 fewer than half of the worlds are diverse at the
  horizon, and fewer at mN = 10; arm P keeps a majority of worlds diverse at N = 200. Falsifier: arm T diverse in at
  least half of worlds at mN = 1.
- **RE 7 (the prior tier is negligible at our doses), revised.** Scored at Λ = 100 only: in consensus worlds the
  residents' zero-prior-regret share is within 0.05 of the prior-matched control's. Falsifier: an excess of 0.15 or
  more at Λ = 100. Λ = 1,000 is exploratory; report the share of tail arrivals that land in the second half of the
  horizon under the arm's annealing schedule.
- **RE 8 (time), revised.** Pooled over arms, the paired change in residents' mean T-weighted migrant regret on
  settled islands of diverse worlds between 25% and 100% of the horizon is not positive. Falsifier: positive with
  the bootstrap interval excluding zero.
- **RE 9 (routes).** Route (a), replacement of an on-path equivalent with positive regret on the same island after
  25% of the horizon, accounts for less than a quarter of zero-regret residents in every arm; the pattern, where it
  exists, is mostly islands with low-regret residents lasting longer or colonizing, not within-island replacement of
  threats. Falsifier: route (a) at or above one half in some arm. Routes are exclusive in the order (c) taken over
  by a migrant's profile, (a) replaced by an on-path equivalent, (b) held, (u) unresolved. If transitions cannot be
  logged, RE 9 is reported as a snapshot description and scored "not tested".

## Scope (to be stated in the report)

Finite horizon, catalogue-relative: low regret can come from founding abundance, the catalogue's geometry,
colonization or survival as well as from refinement of threats; nothing here establishes a large-N limit.
