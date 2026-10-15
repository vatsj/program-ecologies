# Predictions: farsighted refusal (2026-10-14)

Spec `specs/2026-10-14-farsighted-refusal.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict); design, definitions and hand numbers in
`notes/farsighted-refusal.md` §1 (committed before this file). Committed before any code of this experiment, before
any fixed point is computed and before any counted cell. Every cell is the ε = 0 island lottery at finite
(N, I, horizon); nothing here is about π. The RS registered no prediction for this experiment.

## The RE's predictions (verbatim from the spec, with the revisions after review)

1. **The one-step derived guard singles out nothing:** U-g1 freezes islands at their first pair outcome; occupancy at
   mN = 0 within 0.05 of the no-contract baseline's (0.28) plus the share of disagreement islands converted, and far
   below gV. *Falsifier:* U-g1 occupancy ≥ 0.6.
2. **Some KR fixed point has absorbing set exactly V\* at δ ≥ 0.9**, and others absorb on held-player unequal pairs
   [after review by sol: Anesi's protocol is not ours, so this is a bet, not an inference]. *Falsifier:* *certified*
   nonexistence of a V\*-absorbing fixed point at every δ ≤ 0.99 ("not found" by search is reported as such, not as a
   falsification).
3. **The default (myopic-start) fixed point is not the V\* one at δ = 0.9** (uncertain): at moderate patience
   members still accept unequal offers, so U-gKR(0.9) sits between D1 and gV. *Falsifier:* its absorbing set is
   exactly V\*.
4. **Where the static fixed point absorbs on V\*, the universal guard recovers the set on islands** (occupancy ≥ 0.9
   at mN = 0, modal ≥ 0.9 at mN = 1). *Falsifier:* occupancy ≤ 0.7 with the static absorbing set equal to V\*.
5. **gKR spreads like the hand-written veto:** in M-gKR its frequency is neutral at mN = 0 and rises in ≥ 0.8 of
   runs at mN = 1. *Falsifier:* it falls in ≥ 0.5 of runs at mN = 1.
6. **In C3 the hand-written veto and gKR coexist; g0 is lost** (both refusers rise; neither wins outright by 2,000).
   *Falsifier:* g0 above ⅓ at the horizon in ≥ 0.5 of runs.
7. ~~Reading pays in M-read~~ [withdrawn after review by gemini-4-argon: on an island of gKR and gKR-read only,
   both make identical decisions, so M-read is neutral by construction]. **Revised, on C3-read:** with g0 present,
   gKR-read rises against gKR at mN = 1 (uncertain). *Falsifier:* it falls in ≥ 0.5 of runs. **Gemini's
   counter-prediction (registered):** in M-read the two drift neutrally (kept as a sanity cell).
8. **The guard is cheap:** gKR-read costs ≤ 10⁵ evaluator steps per decision, so realizability is not the bind here.
   *Falsifier:* > 10⁶.

Uncertain (the RE's list): 3 and 7.

### Scoring notes (fixed now)

- Occupancy = islands classified (≥ 0.95 of encounters) on a V\* member at generation 2,000 (10,000 reported beside
  it for the main cells); "modal" = islands whose modal realized outcome is a member. "Far below gV" (RE 1) = at least
  0.3 below U-gV's (R2's) occupancy at the same mN.
- RE 1's "share of disagreement islands converted" = the baseline's disagreement share (0.070) times the fraction of
  U-g1's contract installations out of disagreement that land on a member, i.e. a reference value of
  0.281 + 0.070 × (installed into V\* / installed, from (0, 0, 0)); "within 0.05" is scored on that number.
- RE 2: "absorbing set exactly V\*" = the union of the recurrent classes of the fixed point's event chain equals
  V\*; "held-player unequal pairs" = some fixed point whose absorbing set contains an unequal pair. Certified
  nonexistence = the exhaustive search terminates with no V\*-absorbing fixed point at every δ ∈ {0.9, 0.95, 0.99}.
- RE 3 is scored on the static default at δ = 0.9; its second clause ("U-gKR(0.9) sits between D1 and gV") on the
  cell at mN = 0, against D1 = 0.338 and R2 = 1.000.
- RE 4 is scored on every δ whose default absorbs exactly on V\* and was run (0.99, and 0.9 if so); "modal" as above.
- RE 5: "neutral" = mean change of the gKR frequency over runs with a 95% bootstrap interval containing 0 or within
  ±0.02; "rises" = run-mean frequency at 2,000 above 0.5.
- RE 6: "neither wins outright" = neither refuser above 0.9 at 2,000 in more than half the runs.
- RE 7 (revised) is scored on C3-read: the reader's frequency at 2,000 against gKR's in the same run; "falls" = below
  gKR's. Gemini's counter on M-read: mean change of the reader's frequency within run-level uncertainty of 0.
- RE 8 is scored on the executable benchmark (notes §1.8) only, at δ = 0.99 and the composition of a polymorphic
  island (three guards present), median over the benchmark's compositions.

## The subagent's predictions (from notes §1.5–1.6, before any computation)

S1. **g1's static freezing set** is every outcome except (0, 0, 0), where all 18 proposals pass; **g1-x freezes all
    20.** *Falsifier:* any other set from the code.
S2. **U-g1 at mN = 0 lies below the baseline:** 0.22 (0.15–0.29), because scramble islands with a disagreement modal
    jump once to a uniform feasible pair outcome (fair 1/6) and freeze. *Falsifier:* ≥ 0.30 or ≤ 0.12.
S3. **U-g1 at mN = 1 is near the baseline's drift-and-migration consensus:** 0.55–0.80 on the classifier.
    *Falsifier:* outside [0.45, 0.85].
S4. **U-g1-x at mN = 0 equals the baseline in distribution:** within 0.03 of 0.281. *Falsifier:* a difference > 0.05.
S5. **Existence:** a V\*-absorbing fixed point exists at δ ∈ {0.9, 0.95, 0.99} and none at δ ∈ {0.5, 0.8}.
    *Falsifier:* certified absence at any of the first three, or presence at either of the last two.
S6. **δ = 0.5:** the unique fixed point is the myopic policy (all 90 proposed contracts accepted). *Falsifier:* any
    other or an additional fixed point.
S7. **The default at δ = 0.99 absorbs exactly on V\*** (60%). *Falsifier:* it does not.
S8. **Multiplicity at δ ≥ 0.9:** at least two S₃-orbits of fixed points at each of 0.9, 0.95, 0.99. *Falsifier:* a
    unique orbit at any of them.
S9. **No exact ties; minimum consent margin at δ = 0.99 ≥ 10⁻⁴ sixths** at the default. *Falsifier:* a tie or a
    smaller margin.
S10. **U-gKR(0.99) ≈ R2** (if S7 holds): occupancy ≥ 0.95 at mN = 0; modal ≥ 0.95 at mN = 1. *Falsifier:* occupancy
    < 0.9 at mN = 0 or modal < 0.9 at mN = 1.
S11. **U-gKR-read(0.99) reproduces U-gKR(0.99) draw for draw** in every run. *Falsifier:* any run differs.
S12. **M-gKR mirrors R1-public:** mean change at mN = 0 within ±0.02; rises in ≥ 0.8 of runs at mN = 1 (if S7 holds).
    *Falsifier:* a mean change outside ±0.05 at mN = 0, or rises in < 0.6 of runs at mN = 1.
S13. **M-g1 (generic caution) spreads less than gKR:** g1 rises in ≤ 0.6 of runs at mN = 1, and its mean gain is
    below gKR's in M-gKR. *Falsifier:* rises in ≥ 0.8 of runs with a mean gain at least gKR's.
S14. **C3:** g0 below ⅓ at 2,000 in ≥ 0.8 of runs; |gV − gKR| run-mean difference below 0.1. *Falsifier:* g0 below ⅓
    in < 0.5 of runs, or one refuser ahead of the other by ≥ 0.2 on average.
S15. **C3-read:** the reader ends below gKR in more than half the runs (55%). *Falsifier:* it ends above gKR in
    ≥ 0.6 of runs.
S16. **Rare invasion:** gKR at 0.05 rises in ≥ 0.7 of runs by 2,000. *Falsifier:* rises in < 0.5.
S17. **Forced starts (U-gKR(0.99), mN = 0):** persistence 1.0 from every member; recovery ≥ 0.95 from every outsider
    by 2,000 generations (if S7 holds). *Falsifier:* persistence < 0.95 or recovery < 0.8 from some outsider class.
S18. **N panel:** U-gKR(0.99) occupancy at mN = 0 is ≥ 0.95 at N = 50 and N = 200. *Falsifier:* < 0.9 at either.
S19. **Cost:** one executable 20-state solve costs 0.5–3·10⁵ evaluator steps; a reader's decision ≤ 3·10⁵; deriving
    the default table by best-response iteration ≥ 10⁶. *Falsifier:* a solve outside [3·10⁴, 10⁶] or a derivation
    below 3·10⁵.

Every prediction above is scored on the cells as amended in the spec; any deviation is disclosed in the run report
before the cells it affects.
