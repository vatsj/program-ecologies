# Spec: every behavioural predicate as a hook key, and the mechanism of open writes, 2026-10-21

Status: draft by the RE; reviewed by gemini-4-argon, then gpt-6.1-sol (`--mode amended`), both folded [after review]; to be run by
a Sonnet subagent. The RS (2026-10-21): leaning toward admitting behaviour-keyed fills; the hard-coded predicate must
sit inside a family that also admits its competitors (TrustingBot, "cooperate unless you provably defect"; the
predator "defect if they provably cooperate"); "why not admit every behavioral predicate?"; agrees to the cheap
follow-up; "also let's understand the mechanism". **Decided (RS, 2026-10-21):** behaviour-keyed fills are admitted;
if this experiment's results spook the RS or the RE, the decision is deferred to Fable 5.5 through DEFERRED 12. Follows RESULTS "Hooks follow-ups in the weak wing" (open writes
recover the PD lottery, 0.875–1.00; thanks-only 1.00 beats grudges-only 0.50, unexplained) and DEFERRED 12. REJECTED.md
checked: nothing re-opened.

## Why

The follow-up admitted one behavioural predicate, p = □(partner plays C against me), FairBot's own guard. The worry
is that this imports the answer. The test is the maximal behavioural family: every modalized formula over the
partner's play, under a length prior. That family contains FairBot and PrudentBot and their competitors, but no
identity (no quote-equality atom), so cliques of the TwinD kind are inexpressible by construction. Separately, the
mechanism of the recovery is unknown. [Rewritten after review.] Thanks is written only after *mutual* cooperation
(`notes/hooks-w2.md` §1.1), so a carrier whose hooks all default to D cannot write thanks itself. The first draft's
self-conversion story is impossible as stated. The candidates, which Part M discriminates, are:
- *(H1) contagion:* thanks fills, (t, open, p = 1, C), written by cooperating carriers, are copied verbatim (0.1 per
  encounter) to D-default carriers with the same tag, which become FairBot in play;
- *(H2) inheritance:* written fills pass to offspring, so converted carriers breed true;
- *(H3) eviction:* writes fill the four-slot FIFO list and push out seeded fills, some of which made carriers
  exploitable or hostile;
- *(H4) multi-hook programs:* a fill written while cooperating through a C-default hook applies at a D-default hook
  with the same tag elsewhere in the same program.

The RE's leading guess is H1 + H2 (contagion, then breeding true). Grudges convert C-default carriers, which were only
suckers.

## Part K: the maximal behavioural key

**Keys.** A key is a *modalized* formula φ in which every atom is under a box, so GL fixed points exist and are unique
(de Jongh–Sambin), evaluated jointly with both parties' fills in force by the stored modal solver. Its atoms are the
partner's play against me (a), against ⌜C⌝ (c) and against ⌜D⌝ (d). Connectives are ¬, ∧, ∨ and □, with modal depth
≤ 2 and size ≤ 7 nodes. [After review:] keys are deduplicated by GL-equivalence **before** the prior is assigned. Each
equivalence class gets the weight of its shortest member, and constant-true and constant-false keys are excluded, so
tautologies cannot turn thanks into unconditional cooperation. Prior: a length prior over the classes (geometric in
nodes, the repo's ratio). Evaluation tables over key classes and program classes are precomputed once. Part W's three
behaviour boxes and the open p = □a are members.

**Named members (statics, by the solver, committed before the dynamics).** Each is a base hook with one fill:
- FairBot: `HOOK(t, D)` + (□a → C);
- TrustingBot: `HOOK(t, C)` + (□¬a → D);
- PrudentBot: `HOOK(t, D)` + (□a ∧ □¬d → C);
- Gödel predator: `HOOK(t, C)` + (□a → D), the RS's "defect if they provably cooperate";
- CooperateBot and DefectBot.

Output: the full pairwise outcome table.

**Sources.**
- *Seeded fills:* keys drawn from the prior.
- *Written fills:* on a trigger (thanks after **mutual** cooperation only; grudge after being defected against while
  cooperating, as in the follow-up's kernel) [after second review: consistent with the code], the writer draws a key from the prior conditioned on being true of the triggering
  partner, with the trigger's action.
- *Contracts:* a pair of fills with keys from the prior, judged jointly by the prover as in the follow-up.

Everything else (conflict rule, capacity, copies, inheritance) is the follow-up's open-max configuration.

**Cells** (PD islands (100, 64), mN = 1, 40 runs, generation 1,000; reuse `src/hooks_w2*` by import, new modules only):
1. `open-max` rerun (reproduction check against the stored row);
2. `beh-max`, the maximal behavioural family;
3. `beh-max-noA`: the a-free grammar enumerated separately, quotiented by GL-equivalence on its own, and weighted by
   its own shortest members [after second review: removal after quotienting depends on the representative], so FairBot and PrudentBot are inexpressible as
   fills (the "imports the answer" diagnostic);
4. `beh-max-hostile`: `beh-max` with the prior mass of the hostile named **constructions** multiplied by 10. These are
   (C-default, □¬a, D) for TrustingBot and (C-default, □a, D) for the Gödel predator, as whole (default, key, action)
   triples, so FairBot's (D-default, □a, C) is not boosted with them [after second review];
4b. `beh-written-only`: founders' seeded keys and contract technology as in `open-max`; only written fills draw from
   the behavioural family. This separates sources [after second review];
5. `ff-beh-max`: fission–fusion 32 × 100, merged at 200, horizon 600, 20 runs.
6. Secondary: `beh-max` at N = 200 per island and horizon 2,000, 20 runs. These are finite-lottery statistics, not a
   large-population limit.

**Launch gate** [after second review]: the solver's table for the named members must match the RE's hand derivation
below, by stabilized evaluation on GL's finite linear frames (□φ at world n iff φ at every m < n, so vacuously true at
world 0; the outcome is the stabilized value). Any disagreement stops the run and is reported.
- FairBot vs TrustingBot: FairBot is (T, F, F, …) and TrustingBot (F, T, T, …). FairBot defects and TrustingBot
  cooperates.
- Gödel predator vs itself: (F, T, T, …). It cooperates.
- FairBot vs Gödel predator: FairBot (T, F, F, …), predator (F, F, T, T, …). FairBot defects and the predator
  cooperates.
- PrudentBot vs CooperateBot: CooperateBot cooperates with DefectBot, so PrudentBot's □¬d clause fails and it
  defects. It exploits CooperateBot.
- PrudentBot vs TrustingBot: TrustingBot provably defects against DefectBot, so the □¬d clause holds. PrudentBot then
  reduces to FairBot against TrustingBot: it defects, and TrustingBot cooperates. It exploits TrustingBot through the
  first clause, not the DefectBot test.
- PrudentBot vs FairBot: mutual cooperation.

## Part M: the mechanism of open writes

On `open-max`, `open-thanks-only` and `open-grudge-only` (stored configurations), and on `beh-max`:
- **M1, trajectories.** The share of individuals in each *response signature*, classified against a **fixed diagnostic
  panel** [after second review: classification against the current population cannot tell guards apart on path]. The
  panel is CooperateBot, DefectBot, FairBot, TrustingBot, PrudentBot, the Gödel predator and a stranger copy of the
  individual. The classes are FairBot-equivalent, PrudentBot-equivalent, CooperateBot-like, DefectBot-like, other and
  an explicit ambiguous class. Split by the origin of the deciding fill (none, seeded, written-thanks, written-grudge,
  inherited-written, contract), sampled every 10 generations for the first 200 and at the end [after review: cost].
- **M2, conversions.** Count the events in which a write, a copy or an eviction changes a carrier's effective class,
  by from-class, to-class and event type (write, copy, eviction, inheritance), and whether the program has several hook
  nodes with one tag (H4).
- **M3, transmission ablations** [extended after review]. Primary on `open-thanks-only` (no contracts); repeated on
  `open-max` as secondary. Each fill keeps its ancestry (original writer and trigger) separately from its latest
  transmission event, and before/after states are logged [after second review]:
  - (a) written fills not inherited (offspring receive the base program and its seeded fills only);
  - (b) copying off, inheritance on;
  - (c) both off;
  - (d) no eviction: writes fill only empty slots, with a matched-insertion counterfactual (the same write rejected when
    the list is full) logged for comparison;
  - (e) single-hook programs only (the prior restricted to programs with one hook node per tag).
- **M4, timing ablation.** Writes are allowed only in generations 0–50, or only after generation 50. Run on
  `open-max`.
- **M5, sham writes.** Writes happen at the same triggers, but the key is drawn unconditionally, matched in key length
  and in its pre-write applicability frequency across the panel [after second review]. Run on `beh-max`.
- **M6, stranger compatibility.** On winning islands at the end, each holder's outcome against the panel's FairBot
  stranger and its own stranger copy. This checks for behavioural assortativity or modal rival networks, which
  removing quote equality does not exclude by itself [after second review].

## Predictions (the RE's; falsifiers in brackets)

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

## Required outputs

- *Code:* `src/hooks_beh.py` (+ `_kern.py`, `_run.py`, `_report.py`), with `src/hooks_w2*` reused by import and no
  existing file edited.
- *Tests:* `tests/test_hooks_beh.py`, covering:
  - the named members' table by hand;
  - key enumeration and the guardedness check;
  - with the new flags off and the keys restricted to p, `open-max` reproduces its stored row.
- *Notes:* `notes/hooks-beh.md` (§1 hand predictions, §2 deviations).
- *Predictions:* `predictions/2026-10-21-behavioural-hooks.md`, committed before any counted cell.
- *Runs:* `runs/hooks_beh/` (gzipped rows over 5 MB), and verdicts in `runs/hooks-beh.md`.
- *Hand back* RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Scale guard.** 1 worker until the prudence run's batch finishes (`runs/prudence/batch.done` in its worktree), then at
most 3. One job per process. **Waiting:** watch short commands; for long batches wait on one background command that
exits at completion, or end the turn with outputs on disk; never poll periodically.
