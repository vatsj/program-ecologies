# Spec: a migration window for stable sets on islands, 2026-10-24

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. The RS (2026-10-24) proposed the target "all island outcomes are efficient and all stable sets
show up" and agreed with the RE's recommendation (the explainer "Stable Sets on Islands"): a migration sweep first, then
a derived immigrant-rejection guard (a later spec). Follows RESULTS "Stable sets on islands", "Dominance contracts and
refusal on islands", "Farsighted refusal". REJECTED.md checked: nothing re-opened.

## Why

In three-player majority divide-the-dollar (`dollar3`, outcomes in sixths) the unique stable set is V\* = the three
fair pairs. Without migration (mN = 0) islands freeze on dominated outcomes (0.28 on members, 0.23 wasteful); with
mN = 1 waste is cleared but one member spreads everywhere (coverage 0/40, consensus 0.95 by 10,000). Only mN ∈ {0, 1}
was run. The RE's reading: clearing waste is driven by strict invasion of wasteful islands by efficient immigrants,
while consensus is driven by neutral spread of one member across islands, so both slow down as mN falls but at
different rates, and the target may hold over a long window whose length grows as mN falls. The sweep measures
whether such a window exists, where, and how long it lasts.

## Design

Base: the stable-sets lottery (`src/stable_sets*.py`) and the farsighted-refusal guards (`src/farsighted_refusal*.py`),
reused by import; ε = 0, L seeds, w as in those runs, paired founders across cells.

- **Migration panel:** mN ∈ {0, 0.003, 0.01, 0.03, 0.1, 0.3, 1}.
- **Guards:** baseline (no contracts); U-gKR(0.99) (the derived farsighted guard, with contracts at ν = 0.1, β = 1);
  gV (the hand-written veto) as the reference that meets the target at mN = 1.
- **Sizes:** (N, I) = (100, 64), 40 runs; (200, 64), 20 runs.
- **Horizon:** 20,000 generations, with full snapshots at 1,000, 2,000, 5,000, 10,000 and 20,000, and [after review]
  every island's modal outcome logged every 50 generations and [after second review] the target indicators every
  generation, so target episodes are exact and other passage times are sampled-grid estimates.
- **Disconnected components** [added on the RS's messages of 2026-10-24: "I'd like our island models to be expressive
  enough for the entire stable set to coexist. Disconnected components reduces my goal to 'everything shows up w some
  probability' for ~free so I'll allow it for the time being", and "the disconnected components will still have to be
  large in general, else we won't have meaningful migrant effects"]: migration at mN within a component and none
  between. [Redesigned after the second review and the RS's second message: varying C at a fixed 64 islands would
  shrink the components and confound isolation with size.] *Main panel:* components of a fixed **16 islands**,
  C ∈ {1, 2, 4, 8} (16 to 128 islands); *size panel:* C = 4 components of 4, 16 or 64 islands. Baseline and U-gKR(0.99),
  mN ∈ {0.1, 1}, N ∈ {100, 200}. Per component: founding coverage, the probability of efficient absorption, the
  consensus outcome and its time. Reference: if each component's consensus were an independent uniform draw over the
  three fair pairs, P(all three present) = 1 − 3(2/3)^C + 3(1/3)^C = 0, 0, 0.444, 0.883 at C = 1, 2, 4, 8 (unit-tested).
  Components are a stand-in the RS allows for now: they reduce coexistence to "each member appears with some
  probability"; coexistence within one large connected component is the goal, for the immigrant-rejection spec.
- [After second review] *Controls:* a balanced start (each island seeded on one fair pair, the three in equal numbers,
  no waste) to measure coverage erosion alone, and a start with waste seeded among efficient islands to measure
  clearance alone.
- [After second review] *Frozen parameters:* L, w, the founding distribution, ν, β, the migration topology (complete
  within a component), the meaning of mN (expected migrants per island per generation, the stable-sets kernel's
  definition) and the code revision are recorded in the notes before any cell.

## Statistics

Per run and snapshot:
- [after review] **outcome breakdown:** islands on fair pairs (V\*), unequal pairs, the grand coalition, wasteful pairs
  and disagreement;
- **efficient islands:** share of islands whose modal outcome is a fair pair, an unequal pair or the grand coalition
  (no wasteful pair, no disagreement);
- **members present:** how many of the three fair pairs are the modal outcome of at least one island;
- **target met** [two versions after review]: *target (as stated)*: every island efficient and all three members
  present, the RS's wording, scored in every prediction; *target (V\*)*: every island on a fair pair and all three
  present, reported beside it, since unequal pairs are efficient but outside the set; for each, the share of runs
  meeting it at each snapshot and the total generations each run spends meeting it; [after second review] also an
  encounter-weighted inefficient mass per island and a high-purity version of each target (islands ≥ 0.95 on
  efficient outcomes), since modal efficiency allows inefficient minorities;
- **occupancy** (islands ≥ 0.95 on a member) and modal occupancy; consensus (one outcome on every island);
- **first-passage times:** to waste cleared (no wasteful island) and to coverage lost (fewer than three members), with
  Kaplan–Meier medians under right-censoring, and [corrected after second review] the last observed waste through
  the horizon (horizon-dependent, not "cleared for good"). **Target episodes** come from the target indicator itself:
  first entry, episode lengths, re-entries and cumulative occupancy; clearance time minus coverage-loss time is a
  diagnostic only;
- [after review] island transitions on colonization (which outcome replaces which), so that coverage lost by unequal
  pairs eating a fair pair is told apart from neutral coalescence among fair pairs;
- for components: per component, the consensus outcome and its time; across components, members present;
- the ensemble version of "all stable sets show up": the distribution of the consensus member across runs.

## Predictions (the RE's; falsifiers in brackets)

[After second review] Scoring: *held* at or past the stated threshold, *failed* at the falsifier, *partial* in between;
all contrasts paired on founders, with run-clustered intervals. The experiment is a finite-size transient-window
experiment, not evidence about asymptotic selection.

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

## Required outputs

- `src/migration_window.py` (+ runner, report) importing the existing modules; no existing file edited.
- `tests/test_migration_window.py`: mN = 0 and mN = 1 cells reproduce the stored stable-sets and farsighted-refusal runs
  draw for draw; the target statistic on hand-built archipelagos.
- `notes/migration-window.md` (§1 hand predictions; §2 deviations).
- `predictions/2026-10-24-migration-window.md`, before any counted cell, with the RS's target first.
- `runs/migration-window.md` and `.json`, `runs/migration_window/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** Each stable-sets run costs seconds; the guard runs cost more. Other subagents are running:
check `ps` before each batch and use at most 2 workers while any is alive; cap workers by memory. One job per process;
no `multiprocessing.Pool`; one background wait per batch that exits at completion and fires if the log stops changing
for 2 hours; never poll periodically. Cut order if needed (disclose): mN = 0.003, (200, 64) for the guard, the 20,000
snapshot, the 64-island size panel.
