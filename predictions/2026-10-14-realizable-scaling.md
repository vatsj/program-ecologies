# Predictions: the realizable lottery along paths in (N, I, mN), 2026-10-14

Spec `specs/2026-10-14-realizable-scaling.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the amendments supersede
the earlier text). Notes `notes/realizable-scaling.md` §1 (committed before any code). Written and committed before
any counted cell; the T_nuc calibration (independent replicates, m = 0) is not a counted cell and is reported in notes
§1.9 before any cell. ε = 0 lottery statistics at finite (N, I, horizon), never π.

**Scoring conventions (declared now).** Universality = universal-open (provenance's definition). Main cells (S-nonself
at calibrated mN on (100, 64), (200, 64), (400, 64), (100, 128), (200, 128), (100, 256), and the crossed panel) are
scored at their extended horizon T_ext = 10,000·(I·N^0.3)/(64·100^0.3), capped at 40,000 (amendment 5); every other
cell at 10,000 (runs universal-open at 2,000 with E3 decided are not extended and keep their 2,000 value, as in
provenance); the 2,000-generation value is reported beside every verdict, and where the verdict differs between 2,000
and the scoring horizon both are stated. "Universal" fractions are over runs; ties at a threshold count as meeting it.
Island efficiency: the fraction of islands with P(C,C) ≥ 0.95 at the scoring horizon. Where a prediction names "either
mN", it is scored at both arms.

## RE predictions (verbatim from the spec; revisions after review marked)

1. **Island efficiency rises with N** [revised after review by sol: P2 holds N fixed, so it cannot show a limit]:
   along P1 and P3 the sampled-island failure rate q falls with N and the efficient-island fraction is ≥ 0.95 at the
   largest cell; along P2 it plateaus, and all-island success may decline with I. *Falsifier:* q not decreasing in N
   along P1 for S-nonself, or below 0.9 efficient at its largest cell.
2. **Under S-nonself universality goes to 0 along P2 and P3 at either mN,** because seeded clique copies grow with
   N·I past the threshold: ≤ 0.2 of runs universal at (100, 256) and (200, 128). *Falsifier:* ≥ 0.5 at either.
3. **The ablation separates the causes:** with the TwinD mass moved, universality on the calibrated mN stays ≥ 0.7
   along P1, and its failures are non-identity patchworks. *Falsifier:* ablation ≤ 0.4 at (200, 64) calibrated.
4. **Calibrated migration rescues the bridged, migration-limited failures** [revised after review by sol: C-donor
   is near ceiling and bridge-less rivals cannot be rescued by migration]: for the ablation, the calibrated mN turns
   at least half of mN = 1's bridged unresolved failures at N ≥ 200 into universal runs, and rescues no bridge-less
   ones. *Falsifier:* fewer than a quarter of the bridged failures rescued.
5. **The threshold is an abundance on the calibrated path:** universality against seeded copies collapses onto one
   curve across cells on the calibrated mN (50% crossing within a factor 2 of 8 copies everywhere), and not at mN = 1
   (uncertain). *Falsifier:* crossings spread by more than 4× on the calibrated path.
6. **C-donor stays universal along P1** (≥ 0.85 at every N) and fails along P2 by the same identity mechanism as
   S-nonself. *Falsifier:* C-donor ≤ 0.6 at (400, 64), or ≥ 0.6 at (100, 256).

Scoring notes (mine, declared now, not changing the RE's wording): RE 4 is scored on paired replicates (the same
replicate at mN = 1 and calibrated), "bridged failure" being the static check's *bridged* or *reachable-bridge* label
at mN = 1 (notes §1.6); if mN = 1 has no bridged failure at N ≥ 200 the prediction is reported as untestable, not as
held. RE 5 is scored on the crossed panel (the four geometries at calibrated mN, crossings by interpolation in c,
"none" where the clique-free baseline is below 0.5) and, secondarily, on the natural cells' per-run counts; its mN = 1
clause on the natural cells only.

## Counter-predictions registered after review (verbatim intent from the spec)

- **G1 (gemini-4-argon):** at matched μ·N·I universality is higher along P1 than along P2 (per-island clustering of
  copies, not total copies, drives clique establishment). Scored at the matched total 18.25 copies: S-nonself
  calibrated (400, 64) vs (100, 256), with (200, 128) reported; and at 9.13 copies, (200, 64) vs (100, 128).
  *Falsifier (mine, for scoring):* (400, 64) not above (100, 256) at the scoring horizon and at 2,000.
- **G2 (gemini-4-argon):** C-donor at (400, 64) falls below 0.75. *Falsifier:* ≥ 0.75 at both mN arms.
- **S1 (gpt-6.1-sol):** RE 5 fails: there is no collapse on raw copies; establishment per copy varies with N and I.
  Scored as the negation of RE 5 plus the per-copy establishment statistic: holds if the panel crossings spread by
  more than 4× (or exist at some geometries and not others with f₀ ≥ 0.5 at both), or clique establishment per seeded
  copy varies by more than 2× across the four panel geometries.

## The run engineer's own predictions (numbered; with falsifiers)

From notes §1 (hand): f ≈ f₀·e^(−q_c·c) with q_c ≈ 0.05 per copy from the stored provenance cells; a TwinD island's
coordination time 1/(mN·ρ_N) ≈ 1.4·10³ / 5·10⁴ / 10⁸ / 10¹⁴ generations at N = 50 / 100 / 200 / 400; C-donor's copiers
cannot become the identity unit.

- **R1 (efficiency):** mean efficient-island fraction ≥ 0.97 in every S-nonself, ablation and proportional cell at
  N ≥ 100 at the scoring horizon, and all-island success ≥ 0.85 in each of them; q at N = 400 below q at N = 50 at
  both mN arms. *Falsifier:* any such cell below 0.95 mean efficient fraction, or q(400) ≥ q(50) at either arm.
- **R2 (universality on the 18-copy cells):** S-nonself calibrated is in [0.1, 0.45] at (400, 64) and (200, 128) at
  the scoring horizon; at (100, 256) it is ≤ 0.25 at 2,000 and rises by ≥ 0.15 between 2,000 and T_ext = 40,000
  (coordination absorption of TwinD islands at N = 100). *Falsifier:* (400, 64) or (200, 128) outside [0.05, 0.55];
  or (100, 256) rising by less than 0.05.
- **R3 (identity failures are absorbing above N = 100):** every S-nonself run at N ≥ 200 that fails with an identity
  island is classified absorbing by the static check (no living or reachable bridge; 1/h > 10⁶), and no identity
  failure anywhere has a bridge. At N = 50 identity failures are coordination-unresolved. *Falsifier:* any identity
  failure with a bridge, or any N ≥ 200 identity failure not absorbing.
- **R4 (C-donor removes the identity mechanism):** C-donor has no identity island (≤ 0.005 of islands, ≤ 1 run per
  cell with one) in every cell, and universal ≥ 0.85 in every cell including (100, 256) and (400, 64) at both arms;
  dense donors differ from one donor by ≤ 0.1. *Falsifier:* C-donor identity islands > 0.02 in any cell, or universal
  < 0.75 in any cell.
- **R5 (the ablation's gain is clique removal):** ablation − proportional ≤ 0.10 in every calibrated cell (paired), and
  proportional − S-nonself ≥ 0.15 at (200, 64), (400, 64), (200, 128) and (100, 256). *Falsifier:* ablation −
  proportional ≥ 0.20 at any calibrated cell, or proportional − S-nonself < 0.05 at two of those four.
- **R6 (the panel):** f(0) ≥ 0.75 at all four panel geometries; f(16) ≤ f(0) − 0.25 at each; the fitted q_c per
  geometry within a factor 2 of each other (in [0.025, 0.10]); crossings (where they exist) between 8 and 20 copies.
  *Falsifier:* q_c spread > 3×, or f(0) < 0.6 at any geometry, or a crossing below 5 copies.
- **R7 (clustering):** clique establishment per seeded copy is ≥ 2× higher for copies on islands seeded with ≥ 2
  copies than for singletons (pooled over S-nonself cells), but total copies predict "any identity island" at least
  as well as the multi-copy island count (log-likelihood within 2 or better). *Falsifier:* the multi-copy ratio < 1.3,
  or the multi-copy count beating total copies by > 4 in log-likelihood.
- **R8 (migration):** for S-nonself, calibrated − (mN = 1) is within [−0.1, +0.2] at N = 200 and 400 on P1 and P3, and
  within [−0.2, +0.1] at N = 50. *Falsifier:* outside [−0.2, +0.3] at any of these cells.
- **R9 (T_nuc and x):** per-island T_nuc at m = 0 is 20–70 generations at N = 100 under S-nonself and grows no faster
  than N^0.45 across N = 50–400; on the calibrated arm x = mN·T_nuc/N stays within a factor 1.5 across N; it lies in
  [0.15, 0.6] at every N. *Falsifier:* x > 0.6 or < 0.1 at some N on the calibrated arm (which would trigger the notes'
  decision rule), or the exponent > 0.6.
- **R10 (patchwork resolution):** among the ablation's and the proportional control's non-universal runs at N ≥ 200,
  at least half are bridged or reachable-bridge (unresolved), not bridge-less. *Falsifier:* fewer than a quarter.
