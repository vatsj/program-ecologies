# Predictions: dominance contracts and refusal on islands (2026-10-14)

Spec `specs/2026-10-14-dominance-contracts.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict); design, definitions and hand numbers in
`notes/dominance-contracts.md` §1 (committed before this file). Committed before any code of this experiment and
before any counted cell. Every cell is the ε = 0 island lottery at finite (N, I, horizon); nothing here is about π.

## The RS's prediction (verbatim, first)

> My more pointed prediction is that contracts deviating to dominating actions will recover the vNM stable set.

**Operationalization (the RE's, stated before the run; the RS may amend):** "recover" = member occupancy (fraction
of islands whose modal play is one of the three 50–50 pairs V\*) ≥ 0.8 at the horizon *and* island support ⊆ V\* in
≥ 0.5 of runs, in the main contract cell (D1 below) at mN = 0 or mN = 1. The baseline without contracts is 0.28
(mN = 0) and 0.74 (mN = 1, N = 100), with support ⊆ V\* in 0/40 and 0.82 of runs.

*Scoring notes (fixed now).* Occupancy = islands classified (≥ 0.95 of encounters) on a member, the definition of
the baseline's 0.281 / 0.739. Support ⊆ V\* = every island on a member or member-mixed (amendment 4: other-mixed
islands count against); the stable-sets definition (classified islands only, which gave the baseline's 0.82) is
reported beside it. Horizon 2,000 is primary; 10,000 is reported for D1. Recovery at either mN counts. The same two
thresholds are also reported for every other cell as a secondary reading, never as the verdict on the RS's
prediction, which is about D1.

## The RE's predictions (verbatim from the spec, with the revisions after review)

1. **The RS's prediction fails in D1:** with every dominating move available and no refusal, islands cycle, and
   member occupancy at the horizon is within 0.1 of the time-weighted walk of §1 (my bet 0.2–0.4 at mN = 0); support
   ⊆ V\* in ≤ 0.2 of runs. *Falsifier:* occupancy ≥ 0.6 in D1 at either mN.
2. **Contracts make things worse for the set at mN = 1:** D1's occupancy at mN = 1 is below the baseline's 0.74,
   because contracts break the fair-pair consensus that drift and migration built. *Falsifier:* D1 at mN = 1 ≥ 0.74.
3. **The rate does not save it:** D2 (ν = 0.01) lies between the baseline and D1. *Falsifier:* D2 outside that
   interval by more than run-level uncertainty.
4. **Refusal is lost where it is private and drifts where it is public** [revised after review: under slot-wide
   consent the refuser's cost falls on its whole slot]: in R1-private the refusal frequency falls (mean below 0.5 by
   the horizon in ≥ 0.8 of runs at mN = 0); in R1-public its frequency is a neutral martingale within islands (mean
   change within run-level uncertainty of 0), and island occupancy of V\* rises with the island's refusal frequency.
   *Falsifier:* refusal rising in ≥ 0.5 of R1-private runs, or a systematic trend in R1-public.
5. **Universal refusal makes V\* reachable and nearly absorbing** [revised after review: the guard blocks M exits,
   not drift or migration]: the contracts-only R2 chain hits V\* from every outcome; the full-kernel R2 reaches
   occupancy ≥ 0.9 and support ⊆ V\* in ≥ 0.8 of runs. *Falsifier:* occupancy ≤ 0.7, read through the measured
   escape hazards (drift and migration leakage), not as unreachability.
6. **Seeded contracts at ε = 0 are close to the baseline:** D4's occupancy within 0.1 of the baseline at mN = 0,
   because menus are sparse and the needed dominating contract is rarely present. *Falsifier:* a difference ≥ 0.2.
7. ~~Joint entry mostly fixes at β = 0.25~~ [withdrawn after review by gemini-4-argon before any run: an installed
   slot-1 demand meets an installed partner only a quarter of the time and otherwise disagrees, so it earns ≈ 1/6
   against the residents' 3/6]. **Revised:** joint entry has a coordination threshold β\* > 0.5 for every dominating
   contract out of a member (computed in §1), fixation at β = 0.25 is ≤ 0.05, and D3 is within run-level uncertainty
   of the baseline. *Falsifier:* fixation ≥ 0.2 at β = 0.25. **Gemini's counter-prediction (registered):** fixation
   < 0.05 and D3 identical to the baseline; it and the revised RE 7 now agree, so the informative cell is D3′ at
   β just above β\*.
8. **Gemini's alternative, registered as a test:** if D1 at mN = 1 beats D1 at mN = 0, it is because contracts break
   wasteful and disagreement traps into unequal pairs that drift and migration then carry into V\*, not because
   contracts select V\*. Decided by the trigger decomposition of entries into V\* (contract vs drift vs migration).

Uncertain (the RE's list): 2 (contracts may also accelerate consensus), 4 (the cost is paid only at contract events,
so drift may dominate at ν = 0.1), 6.

*Scoring notes for the RE's predictions (fixed now, from notes §1).* RE 1's "time-weighted walk of §1" is the exact
generator's 1/3 (notes §1.2); the uniform-successor 0.235 is reported beside it. RE 2 and RE 3 are scored at 2,000
(RE 3 at both mN; "run-level uncertainty" = 95% bootstrap intervals over runs; at mN = 0 the baseline-to-D1 interval
is narrow, 0.28–0.33 by hand, so RE 3 is scored on the paired difference). RE 4's R1-private clause at mN = 0 and at
mN = 1 reported; "mean below 0.5" = the run's mean bit frequency over all island-slots. RE 7's "β\* > 0.5" is scored
on both thresholds of notes §1.6: it holds for β\*_static (0.76) and fails for β\*_flow (0.40), which by hand is the
operative one; its fixation clause is scored on the forced-island assays at β = 0.25 for exits from members, its D3
clause on D3 against the paired baseline at mN = 0 and 1. RE 8 is scored on D1 at mN = 1: it holds if D1(mN = 1) >
D1(mN = 0) and at least half of the entries into V\* at mN = 1 are not contract-triggered.

## The run engineer's predictions (numbered, with falsifiers)

S1. **D1 at mN = 0 is the generator walk.** Occupancy within 0.05 of 1/3 at 2,000 and at 10,000; unequal within
    0.07 of 1/2; wasteful within 0.07 of 1/6; disagreement and (2, 2, 2) ≤ 0.02. *Falsifier:* occupancy outside
    [0.28, 0.39] at either horizon.
S2. **The RS's prediction fails in D1 at both mN.** mN = 1 occupancy in [0.45, 0.62] at 2,000; support ⊆ V\* in
    ≤ 0.1 of runs at either mN. *Falsifier:* D1 occupancy ≥ 0.7 at mN = 1, or support ⊆ V\* in ≥ 0.3 of runs.
S3. **Contract jumps follow the generator.** At mN = 0, every contract-triggered member exit lands on an unequal pair
    and the empirical contract-jump matrix among the five classes matches the generator's jump chain within 0.05 per
    entry. *Falsifier:* ≥ 0.05 of contract-triggered member exits landing elsewhere, or an entry off by > 0.1.
S4. **Turnover among members is near-independent, not a directed rotation.** After a member exit at mN = 0, the next
    member reached is the same member with probability 0.32 ± 0.06 (generator: 0.319); at mN = 1 above that
    (migration pulls islands back toward the locally common member). *Falsifier:* same-member returns outside
    [0.2, 0.45] at mN = 0.
S5. **RE 8's mechanism holds at mN = 1.** In D1 at mN = 1 at least 0.4 of entries into V\* are not contract-triggered
    (hand ≈ 0.6); at mN = 0 at least 0.9 are contract-triggered. *Falsifier:* < 0.25 non-contract at mN = 1.
S6. **Joint entry at β = 0.25 favours the set.** Forced assays: per-attempt joint fixation of a member exit ≤ 0.05 at
    β = 0.25 and ≥ 0.5 at β = 0.5; entries into members at β = 0.25 fix at ≥ 3 times the member-exit rate. D3
    (β = 0.25) occupancy exceeds the paired baseline by ≥ 0.1 at mN = 0. *Falsifier:* member-exit fixation ≥ 0.1 at
    β = 0.25, or D3 − baseline < 0.05 at mN = 0.
S7. **R1-public is a neutral bit that protects islands.** At mN = 0: occupancy in [0.75, 0.92] at 2,000 and ≥ 0.85
    at 10,000; support ⊆ V\* in ≤ 0.1 of runs; the run-mean bit frequency changes by ≤ 0.05 in absolute value on
    average; islands whose member is protected by their fixed bits (r_k = 1 or r_i = r_j = 1) hold ≥ 0.9 member
    time-share at 10,000 and the unprotected configuration (0, 0, 0) ≈ 1/3. *Falsifier:* occupancy < 0.65 at 2,000,
    or a mean change of the bit > 0.1.
S8. **R1-private: the cost is real but rarely paid at mN = 0.** Occupancy in [0.55, 0.78] at 2,000 at mN = 0; the bit's
    run-mean falls by ≤ 0.05 at mN = 0 and by ≥ 0.05 at mN = 1 (at 2,000). *Falsifier:* a fall ≥ 0.1 at mN = 0, or no
    fall (≤ 0.01) at mN = 1.
S9. **R2.** Occupancy ≥ 0.95 at 2,000 at mN = 0 and in [0.8, 0.95] at mN = 1; the escape hazard from V\* at mN = 1
    ≤ 1/500 per member-island-generation and carried by drift-prepared ratchets (excluded slot drifts to an offer,
    then a strict single-slot move), not by contracts (0 by construction). *Falsifier:* mN = 1 occupancy ≤ 0.7.
S10. **D4 freezes early.** At mN = 0: occupancy in [0.18, 0.34] at 2,000, the mean menu size ≤ 1 contract per island
    by 2,000. *Falsifier:* mean menu size > 3 at 2,000 at mN = 0, or occupancy outside [0.15, 0.40].
S11. **Contracts buy efficiency, not the set.** At mN = 0, D1's efficiency exceeds the paired baseline's by ≥ 0.05
    (the wasteful and disagreement traps are broken) while its occupancy rises by ≤ 0.08. *Falsifier:* efficiency gain
    < 0.02, or occupancy gain > 0.12.
S12. **The contract walk is N-free.** D1 at mN = 0 within 0.05 of 1/3 at N = 50 and N = 200. *Falsifier:* either
    outside [0.28, 0.39].
S13. **Recovery needs refusal.** No D cell meets the RS's two thresholds at either mN; among the refusal cells R2 at
    mN = 0 meets both by 10,000 (support ⊆ V\* in ≥ 0.5 of runs), while R1-public meets the occupancy threshold and
    fails the support threshold. *Falsifier:* a D cell meeting both, or R2 at mN = 0 failing the support threshold.
