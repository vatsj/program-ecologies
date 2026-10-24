# Predictions: a migration window for stable sets on islands (2026-10-24)

Spec `specs/2026-10-24-migration-window.md` (reviewed by gemini-4-argon, then gpt-6.1-sol; both folded); design,
definitions, frozen parameters and the engineer's hand numbers in `notes/migration-window.md` §1 (committed before
this file). Committed before any code of this experiment and before any counted cell. The experiment is a finite-size
transient-window experiment at ε = 0 (N = 100 and 200, I = 64, horizon 20,000); nothing here is about π or
asymptotic selection.

## The RS's target and his messages

**Target (RS, 2026-10-24):** "all island outcomes are efficient and all stable sets show up." The spec scores it in two
versions, **target (as stated)** (every island's modal outcome efficient, i.e. a fair pair, an unequal pair or the grand
coalition, and all three fair pairs the modal outcome of at least one island) and **target (V\*)** (every island on a
fair pair and all three present); the first is scored in every prediction.

**RS message 1 (2026-10-24), on components:** "I'd like our island models to be expressive enough for the entire stable
set to coexist. Disconnected components reduces my goal to 'everything shows up w some probability' for ~free so I'll
allow it for the time being."

**RS message 2 (2026-10-24), on component size:** "the disconnected components will still have to be large in
general, else we won't have meaningful migrant effects."

The RS registered no numeric prediction for this experiment. Components are a stand-in he allows for now; coexistence
inside one large connected component is the goal, for the later immigrant-rejection spec.

## The RE's predictions (verbatim from the spec, falsifiers in brackets)

Scoring: *held* at or past the stated threshold, *failed* at the falsifier, *partial* in between; all contrasts paired
on founders, with run-clustered intervals. The experiment is a finite-size transient-window experiment, not evidence
about asymptotic selection.

1. *A window exists.* For the baseline at (100, 64) there is an mN in the panel at which at least 0.5 of runs meet the
   target at generation 10,000 [no mN reaches 0.25].
2. *Lifetime scales with 1/mN.* Over the mN values with uncensored Kaplan–Meier medians (at least 0.03, 0.1, 0.3),
   the median time to waste cleared and the median time to coverage lost both scale roughly as 1/mN (log-log slopes
   in [−1.3, −0.7]), with coverage lost later than waste cleared by a factor of at least 5 [slopes outside the range,
   or coverage lost before waste cleared]. *Counter-prediction (gemini-4-argon), registered:* coverage is lost by
   unequal pairs invading fair pairs (selection), not neutral coalescence, which compresses the factor below 5.
   *Counter-prediction (gpt-6.1-sol), registered:* if both times scale as 1/mN, lowering migration only stretches one
   trajectory; time rescaling holds after establishment, with deviations at low migration.
3. *The window narrows with N.* At (200, 64) the best mN meets the target in fewer runs than at (100, 64), because
   unequal pairs take over under migration from N = 200 [as many or more].
4. *The derived guard widens the window.* U-gKR(0.99) meets the target in at least as many runs as the baseline at
   every mN, and in at least 0.2 more at its best mN [fewer at the best mN]. *Counter-prediction (gemini-4-argon),
   registered:* the guard locks its member in on colonizing and spreads, so it beats the baseline at low mN and in
   lifetime but ties or loses at mN ∈ {0.1, 0.3} at generation 10,000.
5. *The veto is the ceiling.* gV meets the target in at least 0.9 of runs at every mN ≥ 0.01 [below 0.7 at any].
   [Checked after second review: the stored R2 cell at mN = 1 has consensus in 0/40 runs and all three members in
   every run, modal occupancy 0.996; the subagent re-verifies this from the stored trajectories before using gV as
   the reference.] *Counter-prediction (gpt-6.1-sol), registered:* high member occupancy with declining three-member
   coverage at high migration.
6. *Components deliver the RS's reduced goal.* With 16-island components at N = 100, mN = 1, baseline, the share of
   runs meeting the target rises with C and is within 0.15 of the independent-uniform reference at C ≥ 4 [below it by
   more than 0.15 at C = 8]. At N = 200 it stays below the reference, since components settle on unequal pairs [at or
   above it]. In the size panel, 4-island components meet the target more often than 64-island ones by preserving
   founding diversity rather than by migration [the reverse].

Reference for 6 (unit-tested): if each component's consensus were an independent uniform draw over the three fair
pairs, P(all three present) = 1 − 3(2/3)^C + 3(1/3)^C = 0, 0, 0.444, 0.883 at C = 1, 2, 4, 8.

## Scoring rules fixed before the cells (the engineer's reading where the spec is silent)

- Scored on target (as stated) at generation 10,000; target (V\*), the high-purity versions and generation 20,000
  reported beside. Run-clustered percentile bootstrap, 4,000 resamples.
- **1:** held if the maximum over the mN panel of the baseline share is ≥ 0.5, failed if < 0.25, partial between.
- **2:** the slope fit uses every mN with an uncensored KM median for the measure (restricted fit on {0.03, 0.1, 0.3}
  reported beside); held if both slopes are in [−1.3, −0.7] and the ratio of the medians (coverage lost over waste
  cleared) is ≥ 5 at every mN where both are uncensored; failed if a slope is outside [−1.3, −0.7] by more than 0.3 or
  coverage is lost before waste is cleared at any such mN; partial otherwise. "Coverage lost" and "waste cleared" are
  the debounced first-passage times of notes §1.2. The two registered counter-predictions are scored separately
  (gemini: ratio < 5 with a majority of coverage losses coming from unequal pairs eating a fair pair; gpt: slopes
  steepen or flatten at the lowest mN and the rescaled trajectories coincide after establishment).
- **3:** compare the best mN at (200, 64) with the best mN at (100, 64): held if the share is lower, with the paired
  difference reported; failed if it is as many or more; partial if lower by point estimate but the interval contains 0.
- **4:** held if the baseline-minus-guard difference is ≤ 0 (guard ≥ baseline) at every mN on the point estimate and
  the gain is ≥ 0.2 at the guard's best mN; failed if the guard has fewer at its best mN; partial otherwise. The gain at
  the best mN > 0 is reported beside it, since at mN = 0 the baseline cannot meet the target (frozen waste) and the
  second clause is nearly free there. Gemini's counter-prediction is scored as: guard share ≤ baseline share at
  mN ∈ {0.1, 0.3}, guard above the baseline at mN ≤ 0.03.
- **5:** held if gV's share is ≥ 0.9 at every mN ≥ 0.01, failed if < 0.7 at any, partial between; the stored R2 mN = 1
  cell is re-verified from a rerun of its 40 founders before gV is used as a reference. gpt's counter-prediction is
  scored as: gV's share of runs with three members present falls with mN while modal occupancy stays ≥ 0.9.
- **6:** "rises with C" on the point estimates at C = 1, 2, 4, 8; "within 0.15" on the point estimate of the baseline
  share against the reference at C = 4 and 8; at N = 200 "below the reference" on the point estimate at C = 4 and 8;
  the size-panel clause is scored on the direction (4 × 4 above 4 × 64, N = 100, mN = 1, generation 10,000); its
  mechanism clause has no direct statistic and is reported (component outcome distributions), not scored.
- The engineer's own predictions (E1–E8) are in `notes/migration-window.md` §1.5.
- Cut order if time requires (disclosed): mN = 0.003, (200, 64) for the guards, the 20,000 snapshot, the 64-island
  size panel.

## What would count as the RS's target being met

A configuration (guard, N, mN, component structure) meets the RS's target if target (as stated) holds in at least
0.9 of runs at generation 10,000 and 20,000, with target (V\*) and the high-purity version reported beside it; the
report names the (N, mN, component size) where this happens and says whether it is a plateau or a transient.
