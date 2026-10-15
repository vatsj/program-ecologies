# Predictions: legibility at founding in the fully realizable social organization game (2026-10-14)

Spec `specs/2026-10-14-founding-legibility.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the "Amendments after
review" supersede the earlier text where they conflict). Committed after `notes/founding-legibility.md` §1 (commit
a1e6850) and before any code of this run, any static number and any counted cell. Numbers are hand calculations from
the notes, readings of the parent's stored baseline (disclosed in notes §1), or guesses (labelled). Lottery results are
ε = 0 evidence at finite (N, I, horizon); efficiency and fairness are reported separately; outcomes are all-or-nothing
by run, so contrasts rest on a few runs and are scored with run-level intervals.

## Frozen design (notes §1.0)

1. Base: the parent's S-nonself₃ + eq cell (K₃′, `eq` in both roles, PROD3 after the play in the residual fuel, cap
   P = K/4, lack rule, inheritance, the worker gate), (100, 64), mN = 1, w = 0.3, horizon 2,000, every run extended to
   10,000, replicate r paired with the parent's founder stream r.
2. L1: one frozen empty-list snapshot; each founder runs S-nonself₃ production (alone) on M = 10 random non-self
   cross-role triples of its island's founders, under the ordinary cap and fuel, lack rule; partners frozen.
3. L1-withheld: L1's lists delivered at generation 10 (the first check), pooled by spelling, lack rule; deviation from
   "after the first selection event" stated in notes §1.0 item 3.
4. L2: a NONE-only negative cache keyed on everything production reads (own type, set, the encounter values PROD3
   reads), held per type; the spec's bare-source key is tested and replayed, not run (notes §1.0 item 4, Lemma M).
5. Cells: natural at 10⁶ (stored; 5 rerun), 3·10⁶ and ideal; L1 at 10⁶, 3·10⁶ (L3) and ideal; L1-withheld at 3·10⁶;
   L1-sham at 3·10⁶; the N panel (L1 at (200, 64), 3·10⁶); L2 pilot (5 runs); L1 + L2; the isolated assay; an added,
   labelled diagnostic H + eq on the ideal table. Run counts and drops fixed in notes §2 before any counted cell, in
   the spec's drop order (L1 + L2, then the N panel, then the sham cell).
6. ≤ 3 worker processes.

## RE predictions (verbatim from the spec; revisions as the spec marks them)

1. **Legibility at founding is the mechanism where fuel does not bind** [revised after review by gemini-4-argon: with
   free full lists H gave 0.03 at K = 10⁶, so founding lists cannot beat fuel there]: L1 at 10⁶ ≤ 0.1; L1 on the
   ideal table ≥ 0.3 (against S₃ + eq ideal 0/20) and L1 at 3·10⁶ ≥ 0.3, each with the unconditional workers' share
   at generation 50 at least 0.1 below the matched natural-founding cell's. *Falsifier:* L1 ideal ≤ 0.1 (then the
   bind is not founding legibility; the candidates left are the coalition's demographic mass and the scramble).
2. **The mark is a cost fix, not a dynamic one:** L2 within 0.05 of S₃ + eq in persistence, with the median
   per-encounter cost falling to ≤ 1.5× play. *Falsifier:* a persistence change ≥ 0.15, or cost still ≥ 2×.
   *(Scored on the safe key of notes §1.0 item 4; the bare-source key's safety is scored separately as S7.)*
3. **Fuel and legibility compound:** L3 ≥ natural founding at 3·10⁶ + 0.2 [revised after review: the natural cell at
   3·10⁶ is the matched control]. *Falsifier:* L3 within run-level uncertainty of it.
4. **Identity still decides nothing:** the sham cell within 0.1 of L1. *Falsifier:* a difference ≥ 0.2.
5. **Size still hurts:** L1 at (200, 64) below L1 at (100, 64) (uncertain). *Falsifier:* at least as high.
   *(If both are 0 the falsifier fires trivially; that case will be reported as uninformative.)*
6. ~~The isolated coalition becomes fair with founding lists~~ [withdrawn after review by sol: in (D\*, T₁, T₁) the two
   workers are copies, so the S-nonself₃ gate refuses T₁'s production at founding as later]. **Revised:** a
   deterministic gate-and-production trace shows the gate binds, and the assay stays 0/40 with L1 lists.
   *Falsifier:* any fair run.

## Gemini's counter-prediction (registered in the spec)

**G.** L1 at 10⁶ ≤ 0.1 and L3 (3·10⁶) ≥ 0.3; if L1 fails even at 3·10⁶ the bind is the coalition's initial demographic
mass. *Scored:* holds iff L1₆ ≤ 0.1 and L3 ≥ 0.3; the conditional reading is reported, not scored.

## gpt-6.1-sol's predictions from the review (registered here, scored as stated)

**Sol-a.** "L1 improves early militant survival but need not reach 0.3 persistence." *Scored on* manipulation check
(c): the open-militant share of worker slots at generation 10 higher under L1 than natural by ≥ 0.05 in at least one
K, with L1 persistence < 0.3.
**Sol-b.** "Neutrality only for an invariant-failure cache; the proposed unrestricted mark may change persistence in
either direction." *Scored on* S7 and S8 (the invariant cache is neutral up to Lemma M; the bare-source mark is unsafe).

## Subagent predictions (mine), with falsifiers

**S1. L1 changes nothing measurable.** Paired L1 − natural persistence |Δ| ≤ 0.05 at 10⁶, at 3·10⁶ and on the ideal
table; L1₆ ≤ 0.1, L1ᵢ ≤ 0.1, L3 ≤ 0.15. *Falsifier:* |Δ| ≥ 0.15 in any K, or L1ᵢ ≥ 0.3.

**S2. Fuel is not S₃'s bind.** Natural at 3·10⁶ ≤ 0.15 (S₃ + eq ideal was 0/20). *Falsifier:* ≥ 0.3.

**S3. The scramble is unchanged.** The unconditional workers' share of worker slots at generation 50, L1 minus natural,
within ±0.05 in every K. *Falsifier:* L1 lower by ≥ 0.1 in any K (RE 1's mechanism clause).

**S4. Timing is not the lever.** L1-withheld within 0.05 of L3 in persistence. *Falsifier:* |Δ| ≥ 0.15.

**S5. Generation-0 yield.** Of naturally founded coalitions (notes §1.3), the fraction fair at generation 0 is 0 under
natural founding and in [0.2, 0.5] under L1 (guess); no D\*-type probe concession is certified at generation 0 under L1.
*Falsifier:* natural > 0; L1 < 0.1 or > 0.7; or a D\*-type coalition fair at generation 0 under L1.

**S6. The isolated assay.** 0/40 fair with L1 lists, every replicate at (0; S, S) from generation 0. *Falsifier:* any
fair check.

**S7. The bare-source mark is unsafe.** The test "production reads sources only" fails, and replaying sampled cached
failures against later encounters with the same bare partner sources and the same own list finds suppressed
successes. *Falsifier:* 0 suppressed successes in ≥ 1,000 replayed cached failures.

**S8. The safe mark is neutral.** Mark-sensitive encounters (Lemma M) ≤ 10⁻³ of executed encounters at 10⁶; every L2
pilot run's persistence within 0.02 of its paired S₃ + eq run, and at least 3 of 5 bit-identical. *Falsifier:* any pilot
run differs by ≥ 0.1, or mark-sensitive encounters > 10⁻² of executed encounters.

**S9. The safe mark removes the futile retries.** On the kernel's sample of executed encounters the median per-encounter
cost with the mark is ≤ 1.5× play, and ≥ 2× without it on the same encounters. *Falsifier:* ≥ 2× with the mark.

**S10. Full founding lists do rescue: the gap is coverage, not timing.** H + eq on the ideal table (the maximal founding
list, no production) ≥ 0.3 on the 20 seeds where Nᵢ is 0/20. *Falsifier:* ≤ 0.15 (then neither founding lists nor
identity explain the H/S₃ gap, and the free-list dynamics differ in some other way).

**S11. Militants do not survive better early.** The open-militant share of worker slots at generations 10 and 50, L1
minus natural, within ±0.05 at every K. *Falsifier:* L1 higher by ≥ 0.1 at generation 10 in any K.

**S12. First-encounter decisions.** At generation 0, an open-militant founder strikes in a uniformly drawn encounter on
its island with probability ≥ 0.95 under natural founding and in [0.5, 0.9] under L1 (guess: the ½-certified bosses of
the founding pass are W-probe readers, ½-constants and identity readers). *Falsifier:* L1 ≥ 0.95 or ≤ 0.3.

**S13. The founding pass is cheap.** Median production steps per founder in the pass ≤ K = 10⁶ (one encounter's fuel),
and every founder's later 9 triples are NONE retries for workers. *Falsifier:* median > 10⁶, or a worker founder
acquiring a script after its first triple.

**S14. Size and identity (if the cells run).** L1 at (200, 64) and L1-sham at 3·10⁶ both ≤ 0.1. *Falsifier:* either
≥ 0.3.
