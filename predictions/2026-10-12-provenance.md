# Predictions: provenance, who writes the first certificate and against whom (2026-10-12)

Spec `specs/2026-10-12-provenance.md` (reviewed by gpt-6.1-sol; the [after review] text is the resolution). Committed
after `notes/provenance.md` §1 (commit 0a3bdae) and before any code of this run, any measurement beyond the four
disclosed scratch counts of notes §1, and any counted cell. Numbers are hand calculations from the notes, scratch
counts on milestone 5's cached tables (labelled), or guesses (labelled). Lottery results will be ε = 0,
finite-(N, I, horizon) evidence; island-level efficiency and global universality are reported separately.

## Frozen design (notes §1)

1. Milestone 5's language, grammar (P, n = 7, prior L), post-play encounter (K = 10⁶, V = P = K/4), lack rule,
   would-be-self adoption check, kernel and endpoints; its cached tables reused.
2. Quote = code + certificate list; mode and provenance rule are metadata; "source" = spelling; same quote = same
   spelling and same list (notes §1.1).
3. Rules (notes §1.2): S-self; S-nonself; S-self-delayed (production at shadow-matched encounters against the actual
   partner); S-2 and S-3 (windows of k source-distinct partners, own-side validity, safeguard "score ≥ 2", fallback to
   the earliest candidate) and S-3 strict (no fallback; extra cell); S-gate+cache (gate rule with the cache contract;
   Lemma C: the cache changes costs only); CS-nonself; C-donor; H-only. D scripts produced identically by every
   producing rule.
4. Validity for S-k and for the self-play-only (SPO) definition = own-side validity (Lemma V: full validity cannot
   bootstrap a window from empty founders).
5. Cells (notes §1.7): 12 main cells at (100, 64), 40 runs, horizon 2,000; size panel (S-self, S-nonself, C-donor at
   (200, 64) and (100, 128), 20 runs, unresolved runs continued toward 10,000 as budget allows). Paired seeds and
   event-indexed streams. Primary contrasts (a) S-nonself vs S-self, (b) S-nonself vs S-self-delayed, (c) S-nonself vs
   C-donor, on universal-open and identity islands.
6. ≤ 3 worker processes. The gate cell's budget: closure ≤ 6 h, runs ≤ 12 h (notes §1.9).

## RE predictions (verbatim from the spec)

1. **S-nonself removes the minted cliques and recovers most of the donor cell's universality:** identity islands
   ≤ 0.08 (S-self 0.22) and universal-open ≥ 25/40 (S-self 13, C-donor 33, H-only 25); the self-play-only script
   fraction is 0. *Falsifier:* identity islands ≥ 0.15, or universal-open ≤ 18/40, or any self-play-only script
   under S-nonself.
2. **The residual gap to the donor cell is mostly the identity cliques the seed itself contains** [revised after
   review] (≈ 57 copies per run at this prior): the mass-matched ablation of S-nonself improves universal-open by
   ≥ 6 runs over S-nonself (my bet: to ≥ 28/40). *Falsifier:* an improvement ≤ 2 runs.
3. **The majority rule depends on coverage, not on an ordering** [revised after review]: S-3 retains a script that
   validates against two distinct sources and lands within 6 runs of S-nonself on universal-open; S-2 ties
   systematically (two candidates, each valid against one partner) and its tie-break makes it within 6 runs of
   S-self; no monotone ordering is predicted. *Falsifier:* S-3 differing from S-nonself by ≥ 12 runs, or S-2 ≥
   S-nonself.
4. **The nonself rule's median cost is low and its tail is heavy** [revised after review]: median per-acquisition
   cost within 1.5× of S-self's, but acquisition delays heavy-tailed, with ≥ 5% of producers in near-monoclonal
   islands waiting ≥ 20 encounters and ≥ 1% never acquiring by the horizon; the timing control S-self-delayed
   recovers ≤ half of S-nonself's gain over S-self in identity islands (the gain is generality, not timing).
   *Falsifier:* median cost ≥ 3×, or no producer waiting ≥ 20 encounters, or S-self-delayed recovering ≥ 0.8 of the
   gain.
5. **The mixed-provenance cell enriches faster-acquiring rules among cooperative holders** [revised after review]:
   S-self and S-2 are over-represented relative to ¼ at establishment (founder and linkage effects), the full-rule
   frequencies drift back toward the prior by the horizon, and the cell's universality sits between S-self's and
   S-nonself's. *Falsifier:* every rule within 0.05 of ¼ among cooperative holders at establishment, or a rule ≥ 0.7
   at the horizon.
6. **The gate rule with a negative cache is feasible and twins-biased:** the cell finishes within the budget, and
   its identity islands are ≥ S-self's. *Falsifier:* the cell not finishing within the budget, or identity islands
   ≤ S-nonself's.

**Scoring conventions fixed now.** RE 1's "self-play-only script fraction" is the SPO fraction of held C-script
instances (own-side validity, notes §1.3). RE 2's "≈ 57 copies per run" is the identity grammar's figure (`eq` has
mass 0.009 there); in this grammar the seed's own clique set Q is computed by the frozen rule of notes §1.6 (hand:
the TwinD family, ≈ 4.6 copies per run); the prediction is scored on its number (≥ 6 runs, falsifier ≤ 2). RE 3 is
scored on the primary (fallback) S-2 and S-3; S-3 strict is reported beside it. RE 4's "producers in near-monoclonal
islands" are producers whose spelling had frequency ≥ 0.9 on their island at their first encounter; "never acquiring
by the horizon" is reported for all producers and for capable producers (run trees with a non-self production);
"S-self-delayed recovering x of the gain" = (S-self − S-self-delayed) / (S-self − S-nonself) in mean identity islands.
RE 5's "at establishment" = the checkpoint of first establishment in each run (cooperative individuals on held islands
pooled over runs), "at the horizon" = generation 2,000. RE 6's budget is notes §1.9's.

## Hand numbers (notes §1.4–§1.6; scratch counts labelled)

- Founders meeting an exact copy as first partner: 0.0135 per island, **0.86 per run** (N Σ μ², scratch); 0.011 per run
  for the 97 only-self run trees (mass 0.018, 114 seeded copies per run); 0.059 per run for the 405 trees whose self
  script differs but which also produce at distinct roots. Islands seeded with ≥ 2 copies of one only-self spelling:
  0.55 per run.
- Milestone 5's minted cliques therefore come from lineages that grow while lacking a certificate (the only-self
  class, MM's), not from first encounters (hand mechanism, notes §1.5); a copy meets a co-resident copy with
  probability ≈ 1 − (98/99)^100 ≈ 0.63 per generation once two are present.
- The seed's own identity cliques: the TwinD family, mass 7.1·10⁻⁴, **≈ 4.6 seeded copies per run** (scratch); in
  milestone 5's H-only cell they made identity islands in 12/40 runs and were present in 11 of 14 non-universal runs.
- Receiving set of the ablation (prudent open core analogue): 11 run trees, mass 0.0024 (scratch).
- Modelled cost per acquisition (one successful attempt): S-self, S-nonself, S-self-delayed 13,743 (+ 9,058 for δ);
  S-2 ≈ 2 · 13,743 + 2 · 19,499 ≈ 66,000; S-3 ≈ 3 · 13,743 + 6 · 19,499 ≈ 158,000 (+ stored quotes); S-gate: as S-self
  at acquisition, then one gate check per encounter (15,815) unless cached.
- Which rules can keep an SPO script (notes §1.4): S-self, S-self-delayed, S-2, S-3 (fallback), S-gate; not
  S-nonself, not S-3 strict, not H; C and CS only by same-quote copying.

## The subagent's predictions (numbered, with falsifiers)

S1. **Claim N holds dynamically:** 0 SPO scripts written by any S-nonself production in any cell, and 0 SPO
    instances held in the S-nonself, ablation and S-3 strict cells. *Falsifier:* any. (A theorem for S-nonself; for
    S-3 strict it follows from the selection rule.)

S2. **S-nonself is close to H-only, not to C-donor:** identity islands 0.03–0.12 (the TwinD family survives the rule;
    point 0.07), universal-open 18–30 of 40 (point 24). *Falsifier:* identity islands < 0.01 or > 0.15, or
    universal-open outside 15–32.

S3. **Primary (a), S-nonself − S-self:** universal-open +6 to +16 runs (point +11), identity islands −0.08 to −0.20
    (point −0.14), paired. *Falsifier:* paired difference ≤ +2 runs, or identity difference > −0.04.

S4. **Primary (b), the gain is who, not when:** S-self-delayed recovers ≤ 0.25 of S-nonself's identity-island gain
    over S-self (point 0.1), and its universal-open is within 5 runs of S-self's. *Falsifier:* recovery ≥ 0.5.

S5. **Primary (c), S-nonself − C-donor:** C-donor is more universal by 4–14 runs (point −9), with identity islands
    ≤ 0.02 against S-nonself's 0.03–0.12. *Falsifier:* C-donor universal-open ≤ S-nonself's.

S6. **The coverage rule with a fallback does not remove the minted cliques:** S-2 and S-3 within 6 runs of S-self on
    universal-open and within 0.06 on identity islands, because the only-self class can only ever hold one candidate
    per window and the fallback keeps it. *Falsifier:* S-3 within 3 runs of S-nonself, or S-3's identity islands
    ≤ S-nonself's + 0.03.

S7. **The strict safeguard does:** S-3 strict within 5 runs of S-nonself on universal-open and within 0.04 on
    identity islands. *Falsifier:* S-3 strict within 3 runs of S-self, or its identity islands ≥ S-nonself's + 0.08.

S8. **Where S-k's SPO scripts come from:** ≥ 0.9 of the SPO acquisitions in S-2 and S-3 (fallback) are on run trees
    with no non-self production; the safeguard is met (kept score ≥ 2) in ≥ 0.8 of S-3's selections. *Falsifier:*
    < 0.7, or < 0.6.

S9. **Waiting is not heavy-tailed at this prior:** < 1% of S-nonself producers wait ≥ 20 encounters before their
    first attempt (islands are never near-monoclonal in a producer's own spelling while it lacks a certificate, except
    on defector islands), the median per-acquisition modelled cost of S-nonself within 1.2× of S-self's, and among
    capable producers < 1% never acquire by the horizon. *Falsifier:* ≥ 5% waiting ≥ 20 encounters, or median ≥ 1.5×.

S10. **The ablation:** Q is the TwinD family plus at most a few trees, μ(Q) ≤ 1.5·10⁻³; the ablated cell gains +4 to
    +12 runs of universal-open over S-nonself (point +8) and its identity islands are ≤ 0.01. *Falsifier:* a gain
    ≤ +1, or identity islands ≥ 0.03.

S11. **Mixed cell:** among cooperative individuals on held islands every rule is within 0.07 of ¼ at establishment
    (founders draw rules independently of spelling, and the open carriers that establish first are indifferent to the
    rule); by the horizon S-self + S-2 together hold ≥ 0.5 (the identity islands are theirs alone) and no rule holds
    ≥ 0.4; universal-open between S-self's and S-nonself's. *Falsifier:* a rule outside 0.18–0.32 at establishment, or
    a rule ≥ 0.4 at the horizon.

S12. **The gate cell:** the closure converges in budget with a gate universe ≤ 30,000 units; identity islands within
    ±0.05 of S-self's (the only-self class cannot be repaired; the CB1 class can, but is rarely minted); the cache cuts
    mean per-match production steps by ≥ 2×. *Falsifier:* identity islands ≤ S-nonself's + 0.03, or ≥ S-self's + 0.08,
    or a cut < 1.5×.

S13. **Island-level efficiency is never at risk:** E3 success ≥ 38/40 and mean island P(C,C) ≥ 0.95 in every main
    cell. *Falsifier:* E3 ≤ 35/40 or mean island P(C,C) < 0.9 in any main cell.

S14. **Size panel:** universal-open at 2,000 falls with N and with I in every swept cell, and the S-nonself − S-self
    gap is positive at both sizes. *Falsifier:* S-nonself ≤ S-self at either size.

S15. **Copied SPO scripts are rare:** in the mixed cell, SPO instances held by CS-nonself individuals are ≤ 0.1 of all
    SPO instances at the horizon. *Falsifier:* > 0.3.

*My expectation on the RE's six:* RE 1 about even (universal-open near 24, identity islands near 0.07); RE 2's number
plausible (my S10, point +8) on a premise that differs (≈ 4.6 copies, not 57); RE 3 fails (S-3 lands near S-self
because the fallback keeps the only-self class's candidate; S-2 does not tie on CB1's class since σCB1 is valid at the
self root); RE 4's 5% waiting clause fails, the rest holds; RE 5's falsifier fires (every rule within 0.05 of ¼ at
establishment is my point guess); RE 6 feasible, and identity islands near S-self's (could fall on either side).
