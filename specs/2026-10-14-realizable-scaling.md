# Spec: the realizable lottery along paths in (N, I, mN): does island efficiency go to 1, and what does universality do?, 2026-10-14

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
Follow-up to RESULTS "Provenance", "Prudent openness against identity", "A path in (N, I, mN)" and DEFERRED 1 (the
defended claim: island-level efficiency along the seed path, plus universality relative to identity's seeded
abundance and the (N, I) geometry). REJECTED.md checked: "propagules are not a scaling fix" (2026-10-05) stands and
propagules are not used; nothing re-opened.

## Why

DEFERRED 1 makes the seed lottery the object: P(efficient) → 1 along a path in (N, I). Every realizable-language
result so far is at (100, 64), with a few 20-run size cells: under S-nonself universality falls from 22–28/40 at
(100, 64) to 11/20 at (200, 64) and 11/19 at (100, 128), while the single donor holds 20/20 and the mass-matched
ablation 17–18/20. Two mechanisms predict loss of universality along any growing path, and they must be separated:
(i) **identity abundance**: seeded clique copies scale as μ·N·I (TwinD family 4.6 per run at (100, 64); the measured
50% threshold is about 8), so at fixed μ they pass the threshold along any path growing N·I; (ii) **rival
patchworks**: with mN fixed, patchworks freeze at N ≥ 200 even without cliques (the clique-free baseline is 0.475 at
(100, 128)), while the calibrated rule x = mN·T_nuc/N ≲ 0.3, i.e. mN ∝ N^0.7, kept nucleation independent and let
bridged rivals resolve in the modal arm. The defended claim needs island efficiency to rise to 1 on these paths;
universality is the measured quantity.

## Design

**Machinery.** The provenance run's language, grammar, lack rule, adoption check, cached tables and kernel
(`src/provenance*.py`, `src/lt_genes*.py`; import only), `eq` admitted (DEFERRED 1), ε = 0, L seeds, w as in that
run, horizon 2,000 with 10,000 on every run of the main cells.

**Rules (three).** **S-nonself** (the operating hypothesis); the **mass-matched ablation** (S-nonself with the
seed's TwinD mass moved to the prudent open core; isolates identity abundance); **C-donor** (one donor per island;
the best design so far).

**Paths.**
- **P1, size at fixed I = 64:** N ∈ {50, 100, 200, 400}.
- **P2, islands at fixed N = 100:** I ∈ {32, 64, 128, 256}.
- **P3, diagonal:** (N, I) ∈ {(50, 32), (100, 64), (200, 128)}.
Each at **mN = 1** and at the **calibrated mN** = N^0.7 / 100^0.7 (= 1 at N = 100; T_nuc measured per N in §1 and
the calibration checked against x ≲ 0.3 before any cell). 20 runs per cell; 40 at (100, 64) (the reference).

**Statistics** (per cell, run-level uncertainty, ε = 0 at finite (N, I, horizon), never π):
- **Island efficiency:** the fraction of islands with P(C,C) ≥ 0.95, and P(every island efficient) per run.
- **Universality:** universal-open runs (as in provenance), and its decomposition by cause of failure: identity
  islands (TwinD family or minted cliques) vs non-identity rival patchworks (bridged or bridge-less) vs inefficient
  islands.
- Seeded clique copies per run (measured and μ·N·I), and universality against copies across all cells, fitted to the
  prudent-openness exponential, to test whether the threshold is an abundance at every (N, I) or moves with them.
- Patchwork resolution: fraction resolved by 2,000 and 10,000, time to resolution, the bridge's survival.
- Costs per cell; the projected cost of (400, 64) and (100, 256) before running them.

**Scale guard.** ≤ 3 workers; sibling runs (`founding_legibility`, `core_sweep`) may use up to 5 more: check `ps`
before any multi-worker step. Report projected costs first; drop order (disclosed): the 10,000 extensions outside the
main cells, then N = 400, then I = 256, then C-donor off P3.

## Required outputs

`src/realizable_scaling.py` (+ `_run.py`, `_report.py`), `tests/test_realizable_scaling.py` (reproduction of stored
provenance runs at (100, 64) and (200, 64) draw for draw; the mN calibration; the failure classifier on constructed
archipelagos), `notes/realizable-scaling.md` (§1 static: μ·N·I per cell, T_nuc per N, the calibrated mN, hand
predictions; §2 costs), `runs/realizable-scaling.md` and `.json`, predictions committed before any counted cell, and
the usual hand-back (draft RESULTS, REJECTED, THEORY §9 item 12 / DEFERRED 1, 11 edits, NOTATION, ≤ 5 lines,
branch, commits).

## RE predictions (with falsifiers)

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

7. **Counter-predictions registered after review.** *Gemini:* at matched μ·N·I universality is higher along P1
   than along P2 (per-island clustering of copies, not total copies, drives clique establishment), and C-donor at
   (400, 64) falls below 0.75. *Sol:* prediction 5 fails (no collapse on raw copies; establishment per copy varies
   with N and I).

The RS is invited to add his own; the uncertain ones are 4 and 5. If 1 and 2 hold, the defended claim becomes:
island efficiency → 1, universality → 0 under a fixed length prior, and the measured threshold is what a prior must
beat.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **Efficiency estimands.** Report mean island efficiency, the failure probability q of a randomly sampled island,
   and all-island success separately, with intervals. Claims are finite-(N, I, horizon) statements. The path claim
   is framed as sol's: all-island success needs I(N)·q(N) → 0 with joint failures controlled, so the admissible
   geometry is a measured target (recorded for DEFERRED 1).
2. **Crossed abundance panel (new, central).** At (100, 64), (200, 64), (100, 128) and (200, 128), calibrated mN,
   S-nonself, 20 runs: the seeded TwinD-family copy count is held at 0, 4, 8 and 16 per run (placed by the prior's
   own per-island law, conditioned on the total), with the displaced founders redrawn from the non-identity prior so
   the population is preserved. This estimates the clique-free baseline per geometry and whether a fixed count has
   a fixed effect across geometries. Cells with a clique-free baseline below 0.5 report no absolute crossing.
3. **The ablation is a joint intervention** (it removes cliques and strengthens the prudent core) and is described
   as such; a **proportional-replacement control** reallocates the removed mass across all non-identity types in
   proportion to their prior mass, on paired seeds.
4. **Per-island clustering.** Log seeded copies per island, the number of islands with ≥ 2 copies at t = 0,
   clique establishment per seeded copy, occupied islands, copies per occupied island, minted versus seeded identity
   lineages, and surviving bridges; test whether multi-copy islands predict identity takeover better than μ·N·I.
5. **Horizons and permanence.** Main cells, fixed before launch: S-nonself at calibrated mN on (100, 64), (200, 64),
   (400, 64), (100, 128), (200, 128), (100, 256), and the crossed panel. Every run ends with a static absorbing
   check on its final support: a non-universal run is *absorbing* if no living or prior-reachable bridge can resolve
   its rivals, and *unresolved* (right-censored) otherwise. Main-cell runs are extended to 10,000 ×
   (I·N^0.3)/(64·100^0.3) generations (capped at 40,000) if the projected cost allows; otherwise the static check is
   the classification. Time is in generations of N events per individual throughout.
6. **Donor density.** C-donor at one donor per island is kept and its dilution with N documented; a second C-donor
   arm on P1 with N/100 donors per island separates donor density from donor design.
7. **Calibration and pairing.** T_nuc is measured per N by a predefined rule on independent runs under this
   machinery (the time to the first island-level establishment from the seeded state, median over 20 runs), and
   x = mN·T_nuc/N is checked per rule. Seeds are paired across migration and rule arms; duplicate N = 100 cells are run
   once.
