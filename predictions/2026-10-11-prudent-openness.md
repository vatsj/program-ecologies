# Predictions: prudent openness against identity (2026-10-11)

Spec `specs/2026-10-11-prudent-openness.md` (reviewed by gpt-6.1-sol; [after review] text is the resolution). Committed
after `notes/prudent-openness.md` §1 (commit 8d19050) and before any project code of this experiment and any counted
cell. Static numbers below come from notes §1 (hand derivations, checked against the cached class table by a disclosed
scratch query); everything else is a guess labelled as such.

## Frozen design (notes §1)

1. **Language, law, classes:** the identity-and-tags run's grammar, production, checker, K = 10⁶, V = K/4, 3,974
   identity-aware classes, L prior, ε = 0 island kernel (N = 100, I = 64, mN = 1, w = 0.3), holder-based outcomes,
   the identity run's seed streams (paired seeds), 40 runs per cell; the cached class table reused.
2. **Horizon:** every run to 10,000 generations (or frozen); common checkpoints 500, 1,000, 2,000, 5,000, 10,000; no
   outcome-conditioned extension.
3. **Families (frozen rule, notes §1.4):** F_P = the heaviest maximal clique containing CBP (147 classes, L mass
   0.01551, contains CB); prudent core F_P^pr (38, 0.00218); nice part F_P^n (109, 0.01333); F_X = XC's family (9,
   5.81·10⁻⁴, = the exclusive label).
4. **Part 1 cells** (notes §1.6): L, P1, P2 (= T1c), P3, P4, P4′, P5 as the spec writes them, plus the matched cells
   P1p, P2n, P3p, P4p, P4n, P5p added before any cell because F_P is mostly nice (notes §1.3).
5. **Part 2:** the scan in identity mass m ∈ {0, 2·10⁻⁴, 5·10⁻⁴, 10⁻³, 2·10⁻³, 5·10⁻³, m_L = 0.008979, 2·10⁻²}, with
   and without F_P at M; threshold = 50% crossing of the universal-open fraction at 10,000, paired bootstrap; refinement
   rule; scaling panel at the bracketing points, (N, I) ∈ {(50, 64), (100, 32), (100, 128)}.
6. **Part 3:** reduced-support no-clique chain with F_P added, N = 10³, 10⁴, twin drift on and off, closure check.
7. **Workers ≤ 3** (10 minus the sibling count, capped at 3).

## Hand numbers (notes §1)

- CBP and CB are **compatible** (CB certifies defection against the certificate-less ⌜C⌝); CBP and XC mutually defect;
  CBP refuses every unconditional cooperator but one (9.7·10⁻⁵).
- F_P ⊂ N(CB) ∪ {CB}; overlaps: F_CB 105 classes, P_open (open ∩ refuses Cc) 38 of 39, S-guarded-refusing-Cc 16 of 28,
  F_X 0; CBP's bridge-connected component 568 classes, contains XC.
- CBP–XC paths: one pairwise bridge XB = `if(CHK(me,⌜CB⌝,C),D,if(CHK(them,me,C),C,D))` (1.45·10⁻⁴, ∈ F_X, no strict
  invader); 72 direct F_P–F_X edges, all through XB; 150 length-2 intermediates (0.0144).
- Seed payoffs (L): CBP −0.043, EQ +0.001, CB −0.441, XC −0.025, core −0.089, nice −0.442. Under P1: CBP −0.042, EQ
  −0.015. Core − nice: 0.347 with cooperators (P1p/P2n), 0.106 without (P4p/P4n).
- Copies per run at (100, 64): F_P 99 (L), 201 under every tilt at M; identity 57 (L), 88 with cooperators removed,
  153 under P5/P5p.
- **A cap the spec did not anticipate:** at M a tilted block has about 201 seeded copies per run for 64 islands, so its
  islands per seeded copy cannot exceed 64/201 = 0.32. RE prediction 1's "≥ 0.35" is unreachable for F_P under P1; its
  falsifier (≤ 0.2) is the operative clause.
- Scan: copies per run 0, 1.3, 3.2, 6.4, 12.8, 32, 57.5, 128.

## The RE's predictions (verbatim from the spec)

1. **Prudent openness establishes like a clique:** under P1 CBP's islands per seeded copy are ≥ 0.35 (identity
   run: EQ 0.47, CB 0.14), its seed payoff is within 0.05 of EQ's, and the prudent open family holds every island
   on ≥ 0.5 of runs at 10,000 (against 0/40 for CB's family under T1c at 2,000 and 7/40 at 10,000). *Falsifier:*
   islands per copy ≤ 0.2, or universal-prudent ≤ 0.2 of runs.
2. **Most of the advantage is made of refusing the seed's cooperators** [revised after review: a residual is
   expected, since CBP and CB also differ in compatibility and in exploitation by other readers]: on matched
   backgrounds the CBP − CB difference in established islands per occupied seed island is at least halved when the
   unconditional cooperators are removed (P4 against P4′, compared with P1 against P2); the sign of the residual is
   not predicted. *Falsifier:* the difference without cooperators ≥ 0.8 of the difference with them.
3. **Head to head, prudent openness beats identity by pooling once it establishes like it:** under P5 the frozen
   prudent family holds more islands than the ten EQ spellings at 10,000 (≥ 0.6 against ≤ 0.3), because its
   spellings absorb each other's islands and EQ's do not. *Falsifier:* EQ ≥ the prudent family at 10,000.
4. **CBP is not compatible with CB; CBP's standing against XC is open** [revised after review]: (i) CBP–CB
   incompatible (CB lacks the certified defection against C); (ii) my bet is that the tactic does produce CBP's D
   script against ⌜CB⌝ and XC accepts it, so XC cooperates with CBP while CBP cooperates with XC iff XC certifies
   cooperation with CBP, making the pair compatible one way or both; the report settles it. Universality is then
   claimed only within the frozen prudent family: its cross-island P(C,C) within the family ≥ 0.9 under P1, with
   no claim on reader-wide P(C,C). *Falsifier:* CBP–CB compatible, or within-family cross-island P(C,C) ≤ 0.7.
5. **The abundance threshold is exponential in copies at low m and saturates** [revised after review]: the
   universal-open fraction follows exp(−6,400·m·q) with one fitted q for m ≤ 10⁻³, deviates upward (saturation of
   establishment) above, and the 50% crossing lies in [3·10⁻⁴, 3·10⁻³]; the scaling panel at the bracketing points
   moves the crossing by ≤ 2× in m. *Falsifier:* a residual ≥ 0.3 at two points with m ≤ 10⁻³, or the crossing
   outside [10⁻⁴, 10⁻²], or the panel moving it by ≥ 4×.
6. **With CBP at M the crossing shifts right modestly, and XC persists in the chain** [revised after review]: the
   50% crossing moves right by a factor in [1.5, 5] (better establishment does not remove established identity
   islands), and in the no-clique chain the top cooperative state is prudent-open at 10³ but XC holds ≥ 0.2 of π
   at 10⁴. *Falsifier:* a shift ≤ 1.2× or ≥ 10×, or XC ≤ 0.05 of π at 10⁴.

**How the RE's predictions are scored (fixed now):** "CBP's family" and "the frozen prudent family" are F_P (the
frozen rule); "CB's set" is P2's block (the CB run tree's classes). RE 1: islands per seeded copy of F_P at 10,000
under P1, seed payoff of the CBP class under P1 against EQ's, F_P-universal at 10,000. RE 2: established islands per
occupied seed island at 10,000 (F_P in P1/P4 against the CB set in P2/P4′); the matched version (core in P1p/P4p
against nice in P2n/P4n) is reported beside it and scored as S3. RE 3: islands held by F_P against the ten EQ spellings
at 10,000 under P5. RE 4: (i) and (ii) are static and already decided (notes §1.2, §1.5): **CBP–CB compatible, so the
falsifier of RE 4 has fired before any cell**; the within-family statistic is cross-island P(C,C) over island pairs both
held by F_P members, at 10,000 under P1, reported anyway. RE 5 and RE 6 as written, at 10,000; "XC" in the chain = F_X.

## My predictions (subagent), with falsifiers

**Part 1**

- **S1 (P1 is a family tilt, not a clique).** Under P1 at 10,000: F_P islands per seeded copy in [0.12, 0.30];
  F_P-universal ≤ 0.15 of runs; universal-open in [0.03, 0.30]; identity islands in [0.08, 0.30]. *Falsifier:*
  F_P-universal ≥ 0.3, or universal-open ≥ 0.4.
- **S2 (prudence pays at establishment, matched).** P1p against P2n at 10,000: the core's established islands per
  occupied seed island exceed the nice part's by ≥ 0.05 and by a factor ≥ 1.2; islands held by the block higher for
  the core; identity islands lower under P1p by ≥ 0.03. *Falsifier:* core ≤ nice on established islands per occupied
  seed island.
- **S3 (the prudence advantage is mostly the cooperators, matched version of RE 2).** The core − nice difference in
  established islands per occupied seed island under P4p/P4n is ≤ 0.5 of its value under P1p/P2n (the seed-payoff gap
  falls to 0.31 of itself). *Falsifier:* ratio ≥ 0.8.
- **S4 (RE 2 literal is ill-conditioned).** |F_P(P1) − CB set(P2)| in established islands per occupied seed island ≤
  0.10 (F_P is mostly nice and 63% of its mass is exploitable, while the CB set is S-guarded). *Falsifier:* > 0.2.
- **S5 (identity removed).** P3 and P3p: universal-open at 10,000 ≥ 0.7; F_P-universal (P3) ≤ 0.4; core-universal (P3p)
  ≤ 0.3. *Falsifier:* universal-open < 0.5 in either.
- **S6 (head to head).** P5: the ten EQ spellings hold ≥ F_P's islands at 10,000 (RE 3's falsifier fires). P5p (coin
  flip, 55%): the core holds more islands than the ten EQ spellings at 10,000. *Falsifier:* P5 F_P ≥ EQ ten + 0.1; P5p
  EQ ten ≥ core + 0.1.
- **S7 (XC stays marginal at natural mass).** XC islands ≤ 0.05 at 10,000 in every Part 1 cell; XB seeded in 0.45–0.75
  of runs (0.93 copies per run). *Falsifier:* XC islands > 0.1 in any Part 1 cell.
- **S8 (established mass predicts).** Where a set wins, the largest-established set wins ≥ 0.9 of decided runs (pooled
  over Part 1 at 10,000). *Falsifier:* < 0.8.

**Part 2**

- **S9 (the threshold is a count of clique copies).** f(m) (universal-open at 10,000) is non-increasing in m within
  sampling error; f(0) ∈ [0.65, 0.85]; f(m_L) ≤ 0.15; f(2·10⁻²) ≤ 0.05; the two-parameter fit gives f₀ ∈ [0.6, 0.9],
  q ∈ [0.02, 0.08]; **m* ∈ [8·10⁻⁴, 3·10⁻³]**, i.e. 5–20 seeded clique copies per run; the RE's one-parameter form
  misfits mainly at m = 0 (residual ≈ f₀ − 1). *Falsifier:* m* outside [3·10⁻⁴, 6·10⁻³], or f(0) < 0.5.
- **S10 (scaling panel).** The crossing measured in seeded copies per run (N·I·m*) stays within a factor 2.5 across
  (100, 64), (100, 32), (100, 128); in m it moves up at (100, 32) and down at (100, 128). *Falsifier:* N·I·m* moving by
  ≥ 4× within the panel.
- **S11 (F_P at M).** f with F_P at M ≥ f without at every m ≥ 2·10⁻⁴ within sampling error (paired); shift factor in
  [1.1, 2.5]. *Falsifier:* shift < 1.0 or > 4.

**Part 3**

- **S12 (the chain is the identity run's).** The top cooperative state at both N is XC or XC′; π(F_X) ∈ [0.2, 0.5] at
  10⁴; π(F_P^pr) ≤ 0.15; P(C,C) within 0.05 of the identity run's topLnoclosed (0.560 / 0.781); twin drift off changes
  P(C,C) by ≤ 0.05. *Falsifier:* a core member as the top cooperative state at 10⁴, or π(F_X) < 0.1.

**Static (decided before any cell, recorded):** CBP–CB compatible (RE 4 (i) fails); no D script of CBP against ⌜CB⌝
(RE 4 (ii) fails); CBP's seed payoff within 0.05 of EQ's under L (0.044) and P1 (0.027), the one clause of RE 1 that
can be scored statically.
