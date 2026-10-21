# Predictions: every behavioural predicate as a hook key, and the mechanism of open writes, 2026-10-21

Spec `specs/2026-10-21-behavioural-hooks.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode amended`, both folded).
Written and committed before any code and before any counted cell. Every ε = 0 number in this run is a lottery statistic at
finite (N, I, horizon), never π. The numbered predictions below are the RE's, verbatim from the spec; the scoring notes and
the engineer's hand check of the statics are appended and are mine.

## The RE's predictions (verbatim from the spec)

1. *Statics:*
   - FairBot against TrustingBot: FairBot defects and TrustingBot cooperates.
   - The Gödel predator cooperates with itself and is suckered by FairBot.
   - PrudentBot exploits TrustingBot and CooperateBot, and cooperates with FairBot.

   [any of these different in the solver's table]. *Disputed (gemini-4-argon):* the review computed that FairBot exploits
   the Gödel predator, taking □ as false at world 0. In GL's Kripke semantics □ is vacuously true at world 0, which gives
   the RE's reading. The solver decides, and the convention it uses is reported.
2. *Maximal family:* `beh-max` is universal-open on at least 0.75 of runs [below 0.5].
3. *The friendly guard wins on merit:* on winning islands at the end, at least 50% of individuals are FairBot- or
   PrudentBot-equivalent in play through a fill [below 30%].
4. *Hostile keys are founded and selected out:* hostile named keys are present at founding on ≥ 90% of islands and
   held by < 5% of individuals at the end, under both priors [≥ 20% at the end under `beh-max-hostile`].
5. *Prudence:* in `beh-max`, PrudentBot-equivalents outnumber FairBot-equivalents on winning islands at generation 200,
   while TrustingBots and CooperateBots are still present [fewer]. This is the RS's prudence premium. *Counter-
   prediction (gemini-4-argon), registered:* FairBot-equivalents outnumber PrudentBot-equivalents, because FairBot's key
   (□a, 2 nodes) outweighs PrudentBot's (6 nodes) under the length prior and written keys are drawn from it.
   gpt-6.1-sol registers the same counter. Production rates and conditional reproductive success of the two classes
   are reported separately.
6. *The diagnostic:* `beh-max-noA` falls to ≤ 0.70 universal-open, near Part W's inert hooks (0.65). So the recovery
   needs the prover's guard to be expressible, which is the prover arm's lesson and not an imported answer [≥ 0.85].
7. *Fission–fusion:* `ff-beh-max` ≥ 0.9 [< 0.7].
8. *Contagion (H1):* in `open-thanks-only`, at least 50% of FairBot-equivalents at generation 200 carry a thanks fill
   whose ancestry includes a copy event. Copying off (M3b) and both off (M3c) fall to ≤ 0.70 universal-open, while
   inheritance off alone (M3a) stays ≥ 0.85, so inheritance is dispensable and copying is the carrier. Inheritance's
   contribution is measured, not assumed [the copy share below 25%, or M3b ≥ 0.9]. No eviction (M3d) and single-hook programs (M3e) stay within 0.1 of `open-thanks-only` (H3 and
   H4 are not the mechanism) [a fall of more than 0.2].
9. *Why thanks beat grudges:* in `open-grudge-only` the converted carriers are CooperateBot-like (suckers, not
   defectors), and DefectBot-like carriers hold the islands that fail [failed islands have no DefectBot-like majority].
10. *Timing (M4):* writes in generations 0–50 alone recover at least 80% of `open-max`'s universal-open, so conversion
    acts in the founding scramble [below 50%].
11. *Sham (M5):* unconditioned keys fall to ≤ 0.70 universal-open, so conditioning the key on the partner matters
    [≥ 0.85].

## Registered counter-predictions and disputes (from the spec)

- Prediction 5's counter (gemini-4-argon, gpt-6.1-sol): FairBot-equivalents outnumber PrudentBot-equivalents at generation
  200 in `beh-max`, because FairBot's key (□a, two nodes) outweighs PrudentBot's key (six nodes) under the length prior
  and written keys are drawn from the same prior.
- Prediction 1's disputed static (gemini-4-argon against the RE): the Gödel predator against FairBot. The RE's reading
  (□ vacuously true at world 0) gives: FairBot defects, the predator cooperates. The review's reading (□ false at world
  0) gives the opposite orientation for the first worlds. The solver's convention decides and is reported.

## Scoring notes (engineer)

- "Universal-open", "efficient island", "FairBot-/PrudentBot-/CooperateBot-/DefectBot-equivalent" and "winning island" are
  Part W's and the spec's definitions. Equivalence is scored in play, against the fixed diagnostic panel (spec M1), as
  "plays like the named program on every panel member"; ambiguous holders are reported as their own class and are not
  counted for or against any prediction.
- Prediction 3's denominator is individuals on efficient islands at the end (generation 1,000), numerator the individuals
  that are FairBot- or PrudentBot-equivalent in play *through a fill* (the equivalence fails when the same holder's fills are
  made inert).
- Prediction 4's "founded" is: at least one seeded fill whose (default, key, action) triple is a hostile construction is held
  by some founder of the island at generation 0 ("hostile construction" as defined in the spec, cell 4).
- Predictions 8–11 compare cells paired by run index; "stays within 0.1" and "a fall of more than 0.2" are differences of
  run-level shares of universal-open runs.
- All verdicts are reported with the number; "partial" means one clause of a conjunctive prediction held and another failed.

## Engineer's hand check of the statics (written before the solver is run)

I derived each static by hand from the Kripke semantics (□φ at world n iff φ at every m < n, so vacuously true at world 0;
play at world n is the program's value there; the outcome is the stabilized value), with every box at the level the stored
solver gives the behaviour atoms, level PA (`hooks_w.py`: bits of β are `hc[0, …]`).

- FairBot against TrustingBot: FairBot (T, F, F, …), TrustingBot (F, T, T, …): FairBot defects, TrustingBot cooperates. *As the RE.*
- Gödel predator against itself: (F, T, T, …) both: mutual cooperation. *As the RE.*
- Gödel predator against FairBot: FairBot (T, F, F, …), predator (F, F, T, T, …): FairBot defects and the predator cooperates.
  *As the RE; the vacuous-□ convention is the solver's* (`hc` starts true).
- PrudentBot against CooperateBot: D against C (exploits). *As the RE.*
- PrudentBot against TrustingBot: D against C (exploits). *As the RE.*
- **PrudentBot against FairBot: I expect mutual defection, not mutual cooperation.** Reason: the key □a ∧ □¬d is read at level
  PA. FairBot cooperates with DefectBot at world 0 (□ of a false clause is vacuously true there), so d = (C, D, D, …) for
  FairBot and □¬d is false from world 1 on; the prudent program then defects from world 1, FairBot follows from world 2, and
  the stabilized outcome is (D, D). The same holds for PrudentBot against itself. The standard PrudentBot reads the d-clause
  one level up (BOX1, which ignores world 0). If the solver agrees with this hand check the launch gate fails on this
  entry, the run stops there and the disagreement is handed back without counted cells.
