# Predictions: a path in (N, I, mN) on which islands nucleate independently and rival networks still resolve (2026-10-05)

Spec `specs/2026-10-05-island-path.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-island-path-gpt-6.1-sol.md`).
Code: `src/island_path.py`, propagule option in `src/rival_islands.py` (`_kern(..., kprop)`). Committed after cell 0
(calibration and statics, allowed by the brief because the boundary depends on the calibrated T_nuc) and before any
counted run of cells 1–4.

## What ran before this commit (cell 0, recorded here as the addendum the brief allows)

**Kernel identity.** The k = 1 path of the modified kernel is draw-for-draw identical to the kernel at ca3cc7f on 48
runs across four presets and three (N, I, mN) cells (`tests/check_rival_kernel_identity.py`). The propagule
validation against an unskipped reference and the default-kernel regression against `seeds_in_n._run` were started
at the same time and are reported in the run file.

**Calibration** (m = 0, iid, I = 16, 120 runs per N; the spec's 40 runs are the first 40 of these; the extra runs are
the paired m = 0 reference for q at I = 16; 40 runs at I = 64 for the I = 64 reference). Nucleation event = first
check (every 5 generations) at which the island is certified with a cooperative holder.

| N | nucleating islands | p (per island) | T_nuc (median) [run-bootstrap 95%] | 5 / 25 / 75 / 95% | boundary mN = 0.3·N/T_nuc |
|---|---|---|---|---|---|
| 100 | 166 / 1,920 | 0.086 | 45 [40, 45] | 25 / 35 / 50 / 70 | 0.667 |
| 200 | 251 / 1,920 | 0.131 | 55 [50, 55] | 35 / 45 / 65 / 85 | 1.091 |
| 400 | 344 / 1,920 | 0.179 | 70 [65, 75] | 45 / 60 / 90 / 125 | 1.714 |

T_nuc ∝ N^0.32 over 100–400 (the rival run's extrapolated exponent is confirmed; N = 200 is now measured).

**Statics** (`runs/island-path-static.json`; exact two-type formula and 10⁴ simulated runs per cell, same law as the
kernel; 116 of 120 cells inside the 95% Wilson interval, the four outside at |z| ≈ 2.0–2.3, as expected from
sampling). Classes: A = `BOX1(THEM(ME))`, B₁ = `BOX1(THEM(^not(BOX(THEM(ME)))))` (pair 1), B₃ = P\* =
`and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (pair 3), bridge = `BOX1(THEM(THEM))`.
- A ↔ B₁ and A ↔ B₃ are the symmetric coordination game: P(fix) from k at once = 1.85·10⁻⁵ / 8.7·10⁻⁴ / 0.060 / 0.78
  (N = 100, k = 1 / 10 / 30 / 60); 7.2·10⁻⁹ / 3.7·10⁻⁷ / 6.1·10⁻⁵ / 0.014 (N = 200); 1.6·10⁻¹⁵ / 8.2·10⁻¹⁴ /
  2.2·10⁻¹¹ / 2.8·10⁻⁸ (N = 400). **At fixed k/N = 0.15 the probability falls from 6.1·10⁻⁵ (N = 200) to 2.8·10⁻⁸
  (N = 400):** the barrier is ≈ N·w·(1/2 − k/N)², so k/N is not a sufficient scaling variable unless k/N → 1/2.
- Bridge ↔ A and bridge ↔ B₁ are exactly neutral (k/N).
- **P\* exploits the bridge** (U(P\*, bridge) = 1, U(bridge, P\*) = −2): P\* invades a bridge island with probability
  0.26 from one migrant; the bridge never invades P\*. So pair 3 has no bridge (tag 3 empty), as the rival run said,
  and the bridge is P\*'s prey.

## Design as implemented

Kernel `rival_islands._kern` (exact skipping, lumping, ancestry labels; ε = 0; modal arm n = 9; PD; w = 0.3; iid
seeds from the length prior; complete island graph; generation = I·N births; horizon 10⁵). Initial states depend only
on (N, I, rep, pair, preset), so the m = 0 reference, the path and every propagule k share them (common random
numbers for the seed draw; the dynamics' streams differ).

**Definitions** (spec, applied exactly):
- *Nucleation event, T_nuc:* above. *Boundary path:* mN = 0.667 / 1.091 / 1.714 at N = 100 / 200 / 400.
- *q (holder form, the spec's):* Σ over runs of background islands whose horizon (or stop) holder has local ancestry
  — the island was established with ≥ 0.5 of its holder class local-labelled, and the horizon holder is that class up
  to exact lumping — divided by the same count in the m = 0 reference with the same initial seeds. Interval: run-pair
  bootstrap (islands within a run are not independent). *q_est* (the rival run's form: local establishments) reported
  alongside.
- *Both-present:* tags 1 and 2 each hold ≥ 1 island (plurality holder) at the horizon or stop. *Separation loss:* first
  check at which tag 1 or 2 holds no island. *Hazard:* losses / Σ_runs ∫ min(held_A, held_B) dt up to the loss or
  stop (per minority-island-generation), exact Poisson interval; references mN·ρ_DD(N) (single migrant) and
  (mN/k)·P_k(N) (propagule), both per recipient island-generation. KM survival of the loss time at 10², 10³, 10⁴, 10⁵.
- *Invasion:* a change of strong holder (a class reaching ≥ 0.9 of an island) between different tags, by direction;
  per-migrant invasion probability = invasions / migrant individuals of the invading tag into islands strongly held by
  the resident tag. Tag 0 ("other": not cooperating with A or B, e.g. a faker of B) is reported as its own direction,
  so B-island losses split into replacement by A (2>1), absorption by the bridge (2>3) and capture by other classes
  (2>0).
- *Global resolution:* every island held by one tag at the horizon or stop.
- *Propagule:* k offspring drawn without replacement, fitness-weighted per individual (exactly the single-migrant
  parent law at k = 1), from one uniformly chosen other island replace k uniformly chosen residents of the recipient
  simultaneously; donors keep theirs; a migration event has probability m/k per birth, i.e. mN/k events per
  island-generation (flux matched). Ancestry: children immigrant-labelled; victims' labels drawn without replacement
  within their class.
- *Natural separation (cell 3):* separated at the horizon = two certified islands whose cooperative holders mutually
  defect; ever separated = at any check. Bridge share = share of islands at the end held by classes mutually
  cooperating with both members of the first separated pair (ever-separated runs). Colonization time = first
  immigrant-founded establishment − first establishment; rival interval = first establishment of an island whose
  holder mutually defects with an earlier-established holder − first establishment (censored if none).
- *Island-level P(C,C)* (mean over islands of within-island P(C,C)) and the *counterfactual cross-island P(C,C)*
  under uniform mixing are reported separately in every cell.

**Cells** (fixed priority 0 → 1 → 3 → 2 → 4; ≤ 3 workers):
1. Path: N ∈ {100, 200, 400} × I ∈ {16, 64} × pair ∈ {3, 1}, preset A on island 0 and B on island 1, rest iid, mN on
   the boundary, 40 runs; iid ancestry-tagged runs at the same (N, I, mN), 120 runs at I = 16 and 40 at I = 64.
2. Natural: iid, (N, I) ∈ {100, 200} × {64, 256}, boundary mN, 300 runs (100 at (200, 256)).
3. Propagules: pre-seeded pairs 3 and 1 at I = 16, k ∈ {10, 30} at N = 200 and {10, 30, 60} at N = 400, boundary
   flux, 40 runs; the k = 1 cells are the path cells at I = 16 (same seeds), not rerun; iid q runs 120 per cell.
4. Bridge test (pair 1 tags): N = 100, I = 16, mN ∈ {0.1, 1}, 40 runs each: A, B, bridge pre-seeded on islands
   0–2; control "bridge alone" (bridge on island 0); **added control "A, A, bridge"** (same number of pre-seeded
   competitor islands as the conflict cell, no B), declared here because the bridge-alone control differs from the
   conflict cell in prior abundance as well as in conflict. Merge test on N = 200 runs of cells 1–2 ending with both
   present, reported as conditional on survival.

## RE predictions (from the spec, verbatim)

1. **On the boundary path, rivals resolve only at N = 100.** At N = 100: both-present at the horizon ≤ 0.2 for
   pair 1 and ≤ 0.5 for pair 3. At N = 200 and 400 on the boundary: both-present ≥ 0.8 for pair 3 and the hazard
   ≤ 10⁻⁵ per minority-island-generation, with q ≥ 0.75 everywhere on the path. *Falsifier:* both-present ≤ 0.5 for
   pair 3 at N = 400 on the boundary, or q < 0.6 on the boundary. Gap (0.5–0.8): inconclusive, predeclared.
2. **Propagules resolve rivals when k/N ≥ 0.15** (both-present ≤ 0.3 at k = 30, N = 200 and at k = 60, N = 400),
   **and not at k/N = 0.075** (k = 30, N = 400: both-present ≥ 0.6) [after review: k/N is the variable]; the effect
   on q is uncertain in sign and the RE predicts |Δq| ≤ 0.3 at matched flux. *Falsifier:* k/N = 0.15 leaves
   both-present ≥ 0.7 at N = 400, or |Δq| ≥ 0.4.
3. **Natural horizon separation stays below 0.05 at N = 100 on the boundary and grows with I at N = 200** (sol's
   point: more islands, more chances for a second rival to nucleate before colonization reaches it), reaching
   ≥ 0.05 at (200, 256); the colonization time is shorter than the first-to-second-rival interval at N = 100 and
   not at N = 200. *Falsifier:* horizon separation ≥ 0.1 at (100, 256), or separation at (200, 256) below (200, 64).
4. **The bridge grows during conflict** (its island share at the horizon exceeds its no-conflict control share by
   ≥ 0.1 at mN = 1) **but majority is not assured** (the RE predicts majority in 0.3–0.6 of runs at mN = 1 and
   ≤ 0.3 at mN = 0.1). *Falsifier:* the bridge's share not above its control at mN = 1, or majority ≥ 0.8.

The RE's "control" in 4 is the spec's bridge-alone control; the added A, A, bridge control is reported beside it and
does not change the RE's verdict.

## Subagent predictions (S1–S7), written after cell 0 and before any counted run

The statics change the picture for pairs 1 and 3 differently: pair 1's B₁ is neutral with the bridge (absorption is
polynomial, rate ≈ mN·s_bridge/N per B-island-generation) and has fakers of mass 0.018 (the rival run's static),
while pair 3's P\* has neither and eats the bridge.

- **S1 (pair 1 resolves at every N, not by replacement).** On the boundary path, pair-1 both-present ≤ 0.2 in every
  (N, I) cell, and at N ≥ 200 fewer than 0.2 of B-held-island losses are replacement by A (2>1); the rest are
  absorption by the bridge (2>3) or capture by other classes (2>0). *Falsifier:* pair-1 both-present ≥ 0.5 in any
  N ≥ 200 cell.
- **S2 (the boundary holds q constant: the x-collapse).** q (holder form) at N = 100, 200, 400 lies in
  [0.65, 0.95] in every path cell and the three N agree within 0.15 at each I. *Falsifier:* any q < 0.55, or
  q(400) − q(100) > 0.25 at either I.
- **S3 (pair 3 does not resolve at N ≥ 200; minority islands are many).** Pair-3 both-present ≥ 0.9 in every N ≥ 200
  path cell, with B holding ≥ 3 islands on average at the horizon (B colonizes the iid background before
  separation); pair-3 hazard per minority-island-generation ≤ 10⁻⁶ at N ≥ 200. *Falsifier:* both-present < 0.7 in
  any N ≥ 200 pair-3 cell.
- **S4 (k/N-matched propagules do not resolve rivals).** Because the barrier is ≈ N·w·(1/2 − k/N)², pair-3
  both-present ≥ 0.85 at every N = 400 propagule cell including k = 60, and ≥ 0.6 at (200, 30); the pair-3 hazard is
  within ×10 of (mN/k)·P_k(N)·(A's share of sources) where it is measurable. *Falsifier:* pair-3 both-present ≤ 0.5
  at (400, 60).
- **S5 (propagules barely move q at matched flux).** |q(k) − q(1)| ≤ 0.15 in every propagule q cell. *Falsifier:*
  |Δq| ≥ 0.3 in any cell.
- **S6 (natural separation at N = 200 is limited by rival nucleation, not by resolution).** Horizon separation at
  (200, 256) ≤ 0.05 (point estimate), ever-separated there in [0.01, 0.12], and the fraction of ever-separated runs
  still separated at the horizon is larger at N = 200 than at N = 100 (pooled over I). In runs where a rival
  establishes, it does so before the first immigrant-founded island in ≥ 0.5 of them at each N (rivals nucleate in
  parallel, not after colonization). *Falsifier:* horizon separation ≥ 0.10 at (200, 256), or the survival fraction
  of separations lower at N = 200 than at N = 100.
- **S7 (bridge: prior abundance, not conflict, sets its share).** At mN = 1, the bridge's mean horizon island share
  in the conflict cell (A, B, bridge) is below the bridge-alone control (RE 4's falsifier fires) and within ±0.15 of
  the A, A, bridge control; bridge majority in 0.2–0.5 of conflict runs at both mN. *Falsifier:* conflict share
  exceeds the A, A, bridge control by ≥ 0.2, or exceeds the bridge-alone control.

## Verdict rules

- A prediction **holds** if every clause holds at its point estimate; **fails** if any clause misses. A failed
  prediction is reported as **falsifier fired** only if its falsifier's condition is met; otherwise "failed, falsifier
  not fired".
- **Gap verdicts (predeclared):** RE 1, pair 3 at N = 400 both-present in (0.5, 0.8): inconclusive (spec). RE 2,
  both-present at (400, 60) in (0.3, 0.7): failed, falsifier not fired; |Δq| in (0.3, 0.4): failed, falsifier not
  fired. RE 3, horizon separation at (100, 256) in [0.05, 0.1): failed, falsifier not fired. RE 4, conflict share
  above control by less than 0.1: failed, falsifier not fired; majority in (0.6, 0.8): failed, falsifier not fired.
  S-predictions: a point estimate between the prediction and the falsifier threshold is "failed, falsifier not
  fired".
- Every fraction carries a Wilson 95% interval (run-level, since islands within a run are not independent); where an
  interval straddles a threshold the verdict says "within sampling error". Hazards carry exact Poisson intervals; q
  carries a run-pair bootstrap interval.
- Every run is in every denominator; administratively censored runs (if any) are reported separately and counted as
  both-present at their last state.
- "Colonization time shorter than the rival interval" (RE 3) is read on medians, conditional on runs in which a rival
  establishes (the interval is censored otherwise); with fewer than 5 such runs in a cell the clause is
  inconclusive.
