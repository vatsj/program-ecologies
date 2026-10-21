# Predictions: hooks follow-ups in the weak wing (open vs parochial contracts in the PD; union contracts in the union game), 2026-10-21

Spec `specs/2026-10-21-hooks-followups-weak.md` (reviewed by gemini-4-argon then gpt-6.1-sol; the two amendment sections
supersede the earlier text, the later one winning). Notes `notes/hooks-w2.md` §1 (committed before any code, f2da457).
Written and committed before the code and before any counted cell. Every ε = 0 number is a lottery statistic at finite
(N, I, horizon), never π. Statistics, cells and the hand tabulation are in notes §1.1–§1.8.

*Static numbers used below (computed before this file; no dynamics run).* PD (from Part W's language builder): the hooked
n = 6 grammar has 490 base types, hook carriers hold 0.651 of the prior, each of the two bare `HOOK(t, D)` leaves 0.123;
by the hand equivalences of notes §1.1 a bare `HOOK(t, D)` plus the open promise is FairBot. Union game (`SogLang`):
boss prior: unhooked constants 0.325, hooked constants 0.649, responsive (atom-reading) programs 0.026 (0.003 unhooked,
0.023 hooked); hook-carrying bosses 0.673 (two tags 0.006). Worker prior: unhooked constants 0.311, hooked constants
0.623, responsive 0.066; hook-carrying workers 0.684 (two tags 0.018); union-tag (QUORUM) workers 0.0049. So a boss that
can adopt a response fill is the common case (0.67), a responsive boss program is rare (0.026), and workers able to hold
a demand fill are the common case (0.68).

## The RE's predictions (verbatim from the spec; scoring notes appended)

1. **Parochial keys cause the PD collapse:** open maximal has universal-open ≥ 0.65 (at least the inert level), against
   lineage maximal's ≈ 0. *Falsifier:* open maximal ≤ 0.2.
   *Scoring:* amended by gemini's amendment 1 (the open key is the predicate "the partner provably cooperates with me",
   judged jointly by the prover, not a static box class); scored on the amended technology; "inert level" is Part W's
   inert universal-open (0.65).
2. **Contracts are the decisive part:** open contracts only recovers most of the gain (≥ 0.5); open history only does not
   (≤ 0.3). *Falsifier:* the reverse ordering.
   *Scoring:* "gain" is universal-open above `lineage-max`; "reverse ordering" = open-history ≥ open-contract.
3. **Open maximal survives fission–fusion** (≥ 0.7 universal-open). *Falsifier:* ≤ 0.4.
4. **Myopic union contracts change nothing:** under (M) the fair share stays ≤ 0.05 (a joint strike demand is never a
   myopic Pareto improvement). *Falsifier:* ≥ 0.15.
   *Scoring and restatement (second review, amendment 4):* "never" is restated as "against non-conceding constant
   bosses"; notes §1.5 tabulates that (M) accepts no wage-raising demand against a constant boss but does accept
   *taming* contracts at the current wage (s ≤ w_cur, some worker currently striking), and accepts demands against
   responsive boss programs (R1). The fair-share clause is scored as stated, on `union-M`; the "never" clause is scored
   by the acceptance log (wage-raising accepted demands against constant bosses; see B2 below).
5. **Credible-response union contracts reach the fair wage on some islands:** under (C) the fair share is ≥ 0.2, with
   union strikes rarely executed (≤ 10⁻²). *Falsifier:* fair share ≤ 0.05.
   *Scoring:* on `union-C` (the main, lineage-keyed (C) cell); `union-C-role` is reported beside it; execution is
   executed / challenged per s.
6. **The role-keyed union contract does at least as well as the lineage-keyed one** under (C). *Falsifier:* lower by ≥ 0.2.
7. **Counter-predictions registered (gemini-4-argon).** If β is a static box class, open contracts make defectors
   suckers to their own class or an unbridgeable β-clique, so predictions 1 and 2 fail; lineage-keyed (C) union contracts
   fail (≤ 0.10) while role-keyed (C) succeed (≥ 0.30).
   *Scoring:* the first clause is about a technology the amendment replaced (static class keys); it is recorded as
   **superseded** and not scored, but the sucker rate of open-contract holders (a logged statistic) is the check on its
   mechanism. The second clause is scored on the fair share of `union-C` (≤ 0.10) and `union-C-role` (≥ 0.30).

**Amended and superseded items, listed so they are scored separately.** *Amended:* RE 1, 2 (amendment 1: the open key),
RE 4 (amendment 4: "never" against constant bosses), RE 5 (implemented response, matched cells: amendments 2, 3).
*Superseded:* RE 7's first clause (static class keys). *Unchanged:* RE 3, RE 6, RE 7's second clause.

## My predictions (run engineer), with falsifiers and outcome regions

Outcome regions for a paired difference Δ (cell − reference, run-level share of runs, or mean over runs of a share of
islands): **down** Δ ≤ −0.2, **flat** |Δ| ≤ 0.1, **up** Δ ≥ 0.2, otherwise **grey** (Part W's regions). Run-level
statistics use 40 runs per island cell and 20 per fission–fusion cell; the reference is `lineage-max`.

### PD

- **A1. The paired reference reproduces Part W.** With the open flags off my module reproduces Part W's stored maximal
  rows on checked runs (final class counts and statistics identical, validation §2) and `lineage-max` has run-level
  universal-open ≤ 0.10 (Part W: 0.00), mean island efficiency ≤ 0.35 (0.22) and lineage-closed islands ≥ 0.10 (0.18).
  *Falsifier:* universal-open ≥ 0.25, or non-identical rows on a validated run.
- **A2. Open maximal escapes the collapse** (RE 1, amended): universal-open 0.85 (region [0.6, 1.0]), up ≥ 0.2 against
  `lineage-max`, mean island efficiency ≥ 0.9. *Mechanism:* an open promise turns a default-defecting hook carrier into
  FairBot (notes §1.1); hook carriers hold 0.65 of the prior and 98.7% of Part W's maximal island majorities, so the
  converted mass is large; converted programs cooperate with strangers. *Falsifier:* universal-open ≤ 0.4 (RE 1's own
  falsifier, ≤ 0.2, is weaker).
- **A3. No lineage-closed islands under open maximal:** lineage-closed ≤ 0.02 of islands (no lineage key is written; the
  seeded history fills are dead letters). *Falsifier:* ≥ 0.10.
- **A4. Contracts are the decisive part** (RE 2, amended): `open-contract` universal-open ≥ 0.5 (my estimate 0.7) and
  `open-history` ≤ 0.3 (estimate 0.15), with `open-contract` − `open-history` ≥ 0.2. *Mechanism:* the harm in Part W
  comes from the lineage contracts (strict no-contract 0.675); open writes follow the cooperation they thank. *Falsifier:*
  `open-history` ≥ `open-contract` (RE 2's reverse ordering).
- **A5. Held contracts are promises that work:** the *sucker rate* of open-contract holders (play C against D per
  sampled encounter in which they hold one) ≤ 0.02 in `open-max`; on winning (efficient) islands ≥ 0.5 of island
  majorities at the horizon hold an open contract-origin fill or are plain provers (contract survival). *Falsifier:*
  sucker rate ≥ 0.10, or survival ≤ 0.25.
- **A6. Activation:** under `open-max` the open contract fills are selected on a carried tag and executed (outcome
  differs from the fill-inert match) at a rate per held contract-fill-encounter at least 5× the lineage contracts' rate
  under `lineage-max` (a lineage contract applies only when its partner's lineage recurs). *Falsifier:* ≤ 2×.
- **A7. Fission–fusion** (RE 3): `ff-open-max` universal-open ≥ 0.6 (estimate 0.8) against `ff-lineage-max` ≤ 0.15 (Part W
  0.05). *Falsifier:* `ff-open-max` ≤ 0.3.
- **A8. Contract timing:** acceptance per proposal is higher under the open technology than the lineage technology in
  the same early islands (both accept (D, D) → (C, C); open accepts across lineages). Descriptive; no falsifier beyond
  "open ≥ lineage".

### Union game

- **B1. The myopic reference reproduces Part W's maximal:** `myopic-ref` has ¼-wage share in [0.75, 0.95] (0.85), fair
  ≤ 0.02, and rows equal to the stored maximal on checked runs. *Falsifier:* ¼ share outside [0.6, 0.98].
- **B2. (M) moves no wage against constant bosses** (RE 4, amended): in `union-M`, accepted union contracts have the
  pre-contract wage of a *constant* boss at or above their demand (tamings) in all but ≤ 5% of acceptances, and the
  fair share ≤ 0.05; ¼ stays the modal island (0.65–0.9). *Falsifier:* wage-raising acceptances against constant
  bosses > 5% of acceptances (the code check of §1.5), or fair ≥ 0.15.
- **B3. (C), lineage key** (RE 7's counter-prediction, with a mechanism): fair share ≤ 0.15 (estimate 0.05–0.10), ½
  demands are adopted but the response is keyed on the contracting workers' lineages while the demand fills spread to
  other workers by copies and inheritance, so the realized wage falls short of the predicted wage in ≥ 0.3 of challenged
  encounters and the strike is executed in ≥ 0.1 of challenges (RE 5's "≤ 10⁻²" fails here). *Falsifier:* fair ≥ 0.3,
  or execution ≤ 10⁻².
- **B4. (C), role key:** fair share 0.30 (region [0.2, 0.6]); execution ≤ 0.05 of challenges (the boss's response is
  role-wide); `union-C-role` − `union-C` ≥ 0.2. *Mechanism:* the demand binds every boss, so a boss that cannot respond
  (unhooked constant, 0.325 of the boss prior) earns 0 and is outcompeted by payers, which needs a critical mass of
  demanding workers. *Falsifier:* `union-C-role` fair ≤ 0.10 (RE 6's falsifier is "lower than lineage-keyed by ≥ 0.2").
- **B5. The control** `bw-only-C` is flat against `myopic-ref` on the ¼ share and fair share (|Δ| ≤ 0.1): protecting a
  boss's wage fills does not change Part W's outcome. *Falsifier:* |Δ| ≥ 0.2.
- **B6. Hand-tabulation code check** (deterministic, tests): the acceptance rules reproduce §1.5's table on the
  constant-boss grid (every cell of the (M) and (C) tables), the boss's best reply and tie-break on the enumerated
  cases, and R1's and R2's stable plays on the evaluator. *Falsifier:* any mismatch (reported as a bug or a hand error).
- **B7. Union adoption is sparse under (M)** (≤ 0.01 accepted contracts per sampled encounter) and much more frequent
  under (C) with hooked bosses (≥ 3× `union-M`'s rate in `union-C-role`). *Falsifier:* ratio ≤ 1.5.

### What would change my reading

If A2 holds and A6 holds, the PD collapse is a property of parochial keys, not of contracts as such, for this
predicate; if A2 fails while A5's sucker rate is high, the counter-prediction's mechanism (open promises exploited)
applies to this technology too. In the union game, a fair share under (C) that comes with executed strikes would show
the credible-response rule is not self-enforcing in the lottery.
