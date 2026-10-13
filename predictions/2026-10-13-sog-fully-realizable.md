# Predictions: the social organization game, fully realizable (2026-10-13)

Spec `specs/2026-10-13-sog-fully-realizable.md` (reviewed by gpt-6.1-sol; the [after review] text is the resolution).
Committed after `notes/sog-fully-realizable.md` §1 (commit 3d0090c) and before any code of this run, any static
table, and any counted cell. Numbers are hand calculations from the notes, the six disclosed scratch measurements of
notes §1, or guesses (labelled). Lottery results will be ε = 0 evidence at finite (N, I, horizon); island-level
efficiency, productive efficiency and wage fairness are reported separately.

## Frozen design (notes §1)

1. Language K₃′ (notes §1.1): the realizable run's K₃ with four-abstraction carriers and the public slot label (sources
   are slot-independent), `EQS` source identity (`srcof` strips the certificate list), PROD3 (the tactic as code:
   path tactic on actual values, Hyp-first with backtracking), K = 10⁶, V = P = K/4.
2. Identity atoms: workers `EQ` = EQS(me, other); bosses `N1`, `N2` = EQS(w_j, ⌜T₁⌝) and `EQW` = EQS(w1, w2). Sham
   control: each identity atom replaced by a one-node always-false atom of equal cost (spelling bijection, identical
   prior masses). eq-without-⌜T₁⌝: `N1`, `N2` replaced by shams.
3. S-nonself₃ (notes §1.2): a worker produces only if the other worker's source differs from its own; bosses always
   may; post-play, per lacking set in family order, cap P, residual fuel; lack rule; inheritance; founders empty.
4. Executable semantics by composition of measured step counts (notes §1.7), validated on ≥ 200 encounters replayed
   whole before any counted cell; no support reduction.
5. Lottery (notes §1.11): (100, 64), mN = 1, w = 0.3, r = N/3 encounters per Moran event, horizon 2,000 (extension to
   10,000 a separate column), 40 runs per cell, paired founder streams; definitions fixed in notes §1.8.
6. ≤ 3 worker processes.

## The RS's prediction (verbatim, 2026-10-13; scored first)

> "It seems straightforward enough to probe for 'union-like contracts' - my guess is that identity-based contracts can
> at best fill more islands, not go from 0 to 1."

**Scoring (as the RE fixed it):** identity's effect on the fair share is incremental. Concretely, (i) establishment of
the fair wage does not depend on identity (H + no eq and H + eq both establish on ≥ 0.9 of runs, and the same under
S-nonself₃); (ii) the fair persistence under eq is never zero where it is positive without eq, and never positive where
it is zero without eq, in every paired arm; (iii) where identity changes persistence it does so by at most the gap
between the no-eq share and 1 (a fill) or by a bounded loss. **Falsifier:** a paired arm in which eq takes a fair share
≥ 0.2 to ≤ 0.05, or creates a fair share ≥ 0.2 from ≤ 0.05. Reported alongside the RE's prediction 3. Paired arms for
(ii) and the falsifier: (H + no eq, H + eq), (H + sham, H + eq), (H + eq without ⌜T₁⌝, H + eq), (S₃ + no eq, S₃ + eq),
and (S₃ + sham, S₃ + eq) if the extra cell runs; "fair share" = persistence (fraction of islands fair at 2,000), per
run paired, scored on the cell means and on the per-run pairs (the falsifier fires on cell means).

## RE predictions (verbatim from the spec)

1. **Feasibility:** under S-nonself the fair coalition still establishes on ≥ 0.8 of runs (H: 40/40), with
   establishment delayed by ≤ 2× and ≤ 10% of encounters timing out at K = 10⁶. *Falsifier:* establishment ≤ 0.5,
   or timeouts ≥ 25%.
2. **The greenbeard union cannot write its coalition certificate under S-nonself** (its strike beside a non-copy is
   "work", so the only certificate of a coordinated strike is self-play-only), hence it holds ≤ 0.05 of fair islands
   in the S-nonself + eq cell, while under H + eq (free certificates) it holds ≥ 0.2. *Falsifier:* ≥ 0.15 under
   S-nonself, or ≤ 0.05 under H.
3. **Identity's effect on persistence has an uncertain sign, and it does not act through B_eq's unread slot**
   [revised after review: B_eq reads w1, so substituting w2 leaves its wage unchanged]: against the matched-prior
   identity-disabled control, H + eq changes persistence by ≤ 0.1 in either direction; the local assays show the
   unread-slot substitution leaves the closed shop's wage unchanged and acts, if at all, through the open boss D\*
   (whose cut after a scab is neutral, as in the realizable run); any identity effect runs through worker-side
   coordination (greenbeard unions) or boss replacement. *Falsifier:* a persistence change ≥ 0.25 against the
   matched control, or the unread-slot assay showing a strict B_eq cut.
4. **The fully realizable cell is still fair on a plurality of islands:** S-nonself₃ + eq persistence ≥ 0.3
   (realizable run 0.53), with zero-wage plurality ≤ 0.2 and productive efficiency ≥ 0.9. *Falsifier:* persistence
   ≤ 0.15, or zero wage ≥ 0.5.
5. **The cost model: modest median overhead, failures in the tail** [revised after review]: production adds ≤ 2× to
   the L-weighted median per-encounter cost, while the failures (cap timeouts, failed attempts) concentrate in the
   top decile of required cost; the fraction of triples whose required cost exceeds K = 10⁶ is reported, with
   static evidence, and no fixed tail multiple is claimed. *Falsifier:* production ≥ 4× the median, or failures
   spread uniformly over the cost deciles.
6. **Closed shops are conditionally fit** [revised after review]: B_eq's invasion fitness on actual resident
   compositions is positive on islands held by exact-T₁ unions and negative elsewhere, so its share of the boss slot
   exceeds its prior share in cells where greenbeard unions hold ≥ 0.2 of fair islands and not otherwise.
   *Falsifier:* B_eq above 2× its prior share in a cell with greenbeard unions ≤ 0.05 of fair islands, or below
   its prior share where they hold ≥ 0.2.

**Scoring conventions fixed now.** "Encounters timing out" (RE 1) = encounters in which some check of a participant's
play or certification is executable-TO while its ideal value is T or F, or some participant's play times out
globally, pooled over the cell's realized encounters from generation 0 to 2,000 (reported also by period). "Fair
islands held by greenbeard unions" (RE 2) = the notes §1.8 holder classification (greenbeard union + half of
mixtures, both reported). "B_eq's share of the boss slot" (RE 6) = the closed-shop class share of notes §1.8 against
the prior share of the same classes; "invasion fitness on actual resident compositions" = the boss-replacement assay
on the lottery's horizon islands (B_eq as entrant). "Production adds ≤ 2× to the median" (RE 5) = median
per-encounter cost with production / without production (play steps only), over L-weighted static triples with the
inventories each reaches under S₃, and over realized encounters. RE 4's "productive efficiency" = notes §1.8, cell
mean over islands at 2,000.

## Subagent predictions (mine), with falsifiers

S1. **Scale guard does not fire:** worker classes (run trees with `EQ`) 602 per slot, row classes with S₃ inventories
    below 2,000 per slot. *Falsifier:* > 2,000 worker row classes reached in any S₃ cell. (Hand: scratch count (i).)
S2. **Founding-coalition masses** (notes §1.5): (c) no-eq within 10% of the realizable run's 0.0171 (the same grammar
    up to the slot label); (a) with identity in [0.004, 0.012] (dilution of both roles); the identity-only coalitions
    (rel = 1 part) ≤ 10⁻⁴ of mass; (d) S₃-producible ≥ 0.9 × (a). *Falsifier:* (c) outside [0.0154, 0.0188], or (a)
    outside [0.003, 0.014], or (d) < 0.8 × (a).
S3. **H + no eq on the ideal table reproduces the realizable L cell** (same game, same grammar, new seeds and slot
    label): established 40/40, persistence within 0.15 of 0.53, ¼ plurality the rest. *Falsifier:* persistence
    outside [0.38, 0.68] or establishment < 38/40.
S4. **Executable vs ideal under H + no eq:** persistence differs by ≤ 0.05 (timeouts act in the scramble only).
    *Falsifier:* |Δ| > 0.10.
S5. **Greenbeard unions are rare even with free certificates** (against RE 2's H clause): under H + eq greenbeard
    holders ≤ 0.10 of fair islands, because a union needs one spelling in both slot populations and acts as a scab
    elsewhere (U_eq's prior mass 8·10⁻⁴; ≈ 0.08 seeded copies per island per slot). *Falsifier:* ≥ 0.2.
S6. **Under S₃ + eq greenbeard holders ≤ 0.05** (agreeing with RE 2's S clause), and every greenbeard-held fair
    island there has a boss that reads no worker certificate (a constant ½ payer or an `EQW` reader). *Falsifier:*
    ≥ 0.15, or a greenbeard island under a probe-reading boss.
S7. **No selection for exclusivity:** the closed-shop share of the boss slot at 2,000 is within [0.3, 3]× its prior
    share in every eq cell. *Falsifier:* outside that band in some eq cell.
S8. **Identity's effect is small and of either sign** (with RE 3): |persistence(H + eq) − persistence(H + sham)| ≤ 0.10;
    |persistence(H + eq) − persistence(H + eq without ⌜T₁⌝)| ≤ 0.05. *Falsifier:* > 0.20, or > 0.10 respectively.
S9. **Endogenous production costs little at the coalition:** S₃ + eq vs H + eq: establishment 40/40 in both, median
    establishment generation S₃ ≤ 1.5× H; persistence lower by 0.00–0.15 (lack-rule path dependence and timeouts).
    *Falsifier:* establishment < 36/40 under S₃, or persistence lower by > 0.25, or higher by > 0.10.
S10. **Forced coalitions separate bootstrap from sustain:** the isolated pure coalition with empty inventories is never
    fair (0/40, the gate refuses every T₁ production), with preloaded inventories fair at 2,000 in ≥ 38/40; in the
    lottery the empty and preloaded forced cells differ in persistence by ≤ 0.05 (mixed islands bootstrap at once).
    *Falsifier:* any empty isolated replicate fair, or < 35/40 preloaded, or a lottery difference > 0.10.
S11. **The composition is exact:** composed required cost = the term's step count on ≥ 99% of sampled checks, plays
    and productions; the ≥ 200 whole replays agree on play and production results in ≥ 98%. *Falsifier:* < 95%.
S12. **Timeouts are a scramble effect:** at K = 10⁶ the fraction of realized encounters with an executable-TO check
    is ≤ 5% over generations 0–50 and ≤ 1% from 200 on, in every S₃ cell. *Falsifier:* > 10% early or > 3% late.
S13. **No self-play-only script is ever held under S₃** (Claim N₃; a theorem). *Falsifier:* any.
S14. **Zero wage stays rare:** zero-wage plurality ≤ 0.10 of islands in every (100, 64) natural cell; the non-fair
    islands are mostly ¼. *Falsifier:* ≥ 0.25 in some cell.
S15. **Larger islands keep more fair islands** (as the realizable run, L200 0.66 vs 0.53): S₃ + eq persistence at
    (200, 64) ≥ its (100, 64) value − 0.05. *Falsifier:* lower by > 0.15.
S16. **Exits are drift, not cost:** worker drift (unread-slot drift included) ≥ 0.6 of first exits of fair islands in
    every cell; timeout + production failure ≤ 0.05; false certificate and substitution 0. *Falsifier:* drift < 0.4, or
    timeout + production failure > 0.15, or any false certificate.
S17. **Productive efficiency ≥ 0.9** at 2,000 in every natural cell. *Falsifier:* < 0.8.

## Hand numbers (notes §1.3, §1.5)

- Spellings: workers 1,826 with `EQ` (1,282 without), 602 run trees (422); bosses 258,399 (137,385), 177,318 run trees
  (93,969). Normalizers Z_W = 19.5625 (14.281), Z_B = 2,252.9 (1,214.4).
- Spelling masses (eq grammar): constant boss 2.22·10⁻⁴; D\* 3.47·10⁻⁶; B_eq, B_id 2.77·10⁻⁵; scab, striker 0.0256;
  T₁ 3.19·10⁻³; U_eq, XM 7.99·10⁻⁴. Seeded copies per run at (100, 64) (6,400 per slot): T₁ ≈ 20 per slot, U_eq ≈ 5 per
  slot, B_eq ≈ 0.18, D\* ≈ 0.02.
- Greenbeard co-seeding: an island has a U_eq in both slots with probability ≈ (1 − e^{−0.08})² ≈ 0.006, ≈ 0.4 islands
  per run; a union needs growth in both slot populations.
- Coalition masses: (c) ≈ 0.0171 (realizable); (a) ≈ 0.006–0.010 (dilution); identity-only ≲ 10⁻⁵.
- Production: T₁'s [D] costs one boss =½ check (348 steps against a constant) plus PROD3's own steps (guess
  1–3·10⁴); D\*'s =½ production one probe check (≈ 14,000) plus own (guess 3–5·10⁴). The heavy cases are workers with
  two or three wage atoms producing against probe bosses (nested boss checks of 10⁵ each), which approach P = 2.5·10⁵.

## Addendum (2026-10-13, before any counted cell): the second review (gemini-4-argon)

Committed after the code's evaluation layer existed and before any lottery cell or static table was computed.
Design changes in notes §1.12: starved and capped production counted separately; a diagnostic arm **S-nonself-opp**
(no worker gate: non-self required only against the boss); a forced assay of one uncertified T₁ entering a fixed
(D\*, T₁, T₁) island under both gates.

**G (Gemini's counter-prediction, verbatim in substance):** "U_eq holds < 0.05 of fair islands even in H + eq, because
both worker slots must co-fix the same spelling." *Falsifier:* ≥ 0.05 in H + eq. Scored beside RE 2. If G holds, RE 6's
condition (greenbeard unions ≥ 0.2 of fair islands) is vacuous in every cell; B_eq's invasion fitness on resident
compositions is reported unconditionally.

S18 (mine). **The gate deadlock is a slot-1 loss, not an island failure:** in the forced assay, under S-nonself₃ the
uncertified slot-1 entrant's lineage is lost in ≥ 0.95 of replicates and never fixes; under S-nonself-opp it fixes at
about the neutral rate (1/N ± a factor 2). A slot-2 entrant is neutral under both gates. *Falsifier:* a slot-1 entrant
fixing under S-nonself₃, or the fair state lost in ≥ 0.05 of S-nonself₃ replicates.
S19 (mine). **S-nonself-opp vs S-nonself₃ in the lottery:** persistence within ±0.10 (open militants need no copy
production), greenbeard holders higher under S-nonself-opp (its strike certificate is producible). *Falsifier:*
|Δ persistence| > 0.2.
