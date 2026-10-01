# Review of `predictions/2026-10-01-rival-networks.md` (fable, second pass)

Read: the revised brief (partial chain, exact check), astra's review, RESULTS "Priced arm"/"E3"/"Modal", THEORY §9, REJECTED, the kernels and driver. Short read-only checks run: `rival_static.py validate`, GTH with an absorbing label, neutral hitting at the brief's caps, a DB flat-border computation with an ALLC load, and 1,000–12,000-trial estimates of five blocks on torus 16/32 and hypercube 8. I don't repeat astra; where I checked a point numerically I say so.

## 1. Design flaws and code bugs

1. **Partial chain at torus side 64 is broken, in the direction of the prediction.** Tier-2 blocks are skipped at N > 1024, and `lumped_graph(partial=True)` returns 0 for a missing block. The tier-2 residents are still *entered* (their entry blocks are tier 1) but have no measured exits, so they are absorbing. `gth` then puts π = 1 on them (checked: an absorbing P*-net gets 1.0, the rest 10⁻²⁹⁴). At side 64 the mass collapses onto whichever FB-net tier-2 member is entered first, which "confirms" verdict 7 at the falsifier size by artifact. The brief says the chain "falls back to the lumped rates" there; the code does not. Fix: in `fn`, when the resident is tier 2 and the row is missing, use the block against its label's primary representative; and flag any state with zero out-rate as "absorbing in sample" instead of reporting π for it.
2. **Zero-success blocks and the 300 s cap.** A near-neutral block at N = 4,096 costs ~5–10 ms per trial, so tier-1 jobs get ~30–60k trials: fine. But a job that stops after one batch (0/2000) enters the "upper" variant at ½·1.8·10⁻³ ≈ 2× neutral; the upper band will be set by under-sampled blocks, not physics. Print trials per zero block and exclude blocks with < 10⁴ trials from the upper variant.
3. **R3 velocity estimator.** `mean(Δcnt/t)` over runs is dominated by fast runs; for a biased walk E[Δ/t] ≠ v, and the "factor 3" tolerance will absorb the estimator's bias rather than roughening. Use the Wald ratio ΣΔ/Σt and normalize by the *recorded* cross-edge count, not 2·side: the first-order prediction then becomes p_fb − p_ps ≈ 8·10⁻⁴ per cross edge per generation at c = 10⁻², testable despite roughening. Note that P(FB first) is invariant to roughening (drift and variance both ∝ cross edges), so verdict 11 is robust while verdict 12 and t_first are not. `stop = max(2, …)` uses a post-passage record for fast runs.
4. **The front control (`_front`, `FRONT_X`, `run_front`) has no verdict in the brief.** Add one (see §2). Also record x in the two FB-side rows adjacent to P*, since the seeded ALLC is eaten at the front and refilled only by neutral drift.
5. **Verdict 1's criterion.** "0.108 must fall within the interval" ignores the reference's own error: my 1,000-trial FB|D at side 32 gave 0.077 [0.062, 0.095], excluding 0.108. Use interval overlap, or re-measure with ≥ 200 successes (one batch).
6. **R4 is thin and under-instrumented.** Runs are cheap (minutes on the torus); use ≥ 4 seeds. Record the ALLC fraction among FB-side sites adjacent to P*-net, and the number of P*-net clusters, or "mutation reverses the border" cannot be attributed. x uses only the ALLC class (col 10); also report the exploitable label. Average border MD only while both networks hold ≥ 10%, or verdict 20 is vacuous once P* fixes.
7. Minor, for the record: censoring is negligible (neutral at cap 2N: 21 undecided in 180k trials; ρ = 0.00795 ± 0.0002 vs 2/N = 0.00781), so astra's point is answered numerically. Batch seeds are shared across blocks on a graph (common random numbers), so ratios between blocks are not independent.

## 2. Predictions likely wrong

- **Verdict 4, torus side 16 ratio in [0.1, 0.9].** Checks: FB|P* at c = 10⁻², side 16: 1/4000 (ratio ≈ 0.03, CI < 0.18); at c = 10⁻¹: 3/4000. Curvature costs ~0.25 per extra cross edge against a cost asymmetry of 0.04, so the critical nucleus is ~100 sites ≈ N/2 at side 16. I predict ratio 0.02–0.1 at side 16 and 0 successes in 10⁵ at side 64 for c ≤ 10⁻².
- **Verdict 5.** Critical nucleus at c = 10⁻¹ is 3×3–4×4 (a 4×4 FB block in P* is about neutral: loss 0.239 vs gain 0.248 per border site), so ρ(FB|P*) ≈ 3·10⁻⁴–10⁻³, flat in N. Then P*'s torus exit at c = 10⁻¹ is FB nucleation (0.0237 × 5·10⁻⁴ ≈ 10⁻⁵), 20× the shadow exit (1.3·10⁻³ × 2/N ≈ 6·10⁻⁷ at 4,096): π(P*-net) ≪ 0.01, stronger than "≥ 5×".
- **Verdict 7 is foreordained.** shadow|P* at c = 10⁻² measured (1.0–1.3)×2/N (0.0084 vs 0.0078 at side 16; 0.0023 vs 0.0020 at 32), as its structure requires (both interiors free, the shadow pays less at the border). With that, the torus chain is D ⇄ FB ⇄ ALLC with π(D)/π(FB) = 188/N and π(P*) ≈ 0.03–0.08 at side 64. Present R2's torus result as two blocks (shadow|P*, FB|P*); the π table adds nothing.
- **Verdict 16, torus x.** Pruning is local: a D landing in an ALLC pocket is favoured there (local x = 1), unlike well mixed, where D is favoured only at global x > ½. An ALLC lineage lives until hit, ~50–200 generations, so x ≈ ε·μ_C·T ≈ 0.02–0.08 on the torus; hypercube ≈ 0.2–0.3. Prediction: torus below or at the band's floor.
- **Verdict 17, c = 10⁻².** The DB flat-border computation reproduces the brief's thresholds (x* = 0.013, 0.115), but at x = 0.03 the drift is +0.0012 per border site per generation → 0.3 sites/gen → ~27,000 generations for 8,000 sites, with border depletion on top. Predict: P* wins slowly in some replicates, not all by 4·10⁴; at c = 0 it wins; at c = 10⁻¹ FB wins on the torus.
- **Verdict 18, hypercube c = 10⁻².** The split erodes near-neutrally (a flipped site wins 5.6% vs 7.1% neutral), then the coordination game escapes 50/50 in ~25 generations with cost drift 0.0015/gen against noise 0.004/gen, while x reaches only ~0.012 < x*_hyp ≈ 0.02. Predict FB wins with P ≈ 0.8 per seed. At c = 0, P*.
- **Front control (unregistered).** Predict the measured crossing above the flat-border x*: 0.03–0.05 at c = 10⁻², 0.2–0.3 at c = 10⁻¹.
- Verdict 3 holds (D|ALLC 0.163 / 0.168 / 0.198 on torus 16 / 32 / hypercube 8, fixation 20/20) but note a large D domain loses a flat border to ALLC (0.24 vs 0.26 per site); the torus value is well below 0.26.
- Verdict 20's "≤ 2/side at every record" is at risk from fingering through ALLC pockets; allow 4/side at the peak.

## 3. Missing controls

- **Prior swap** (no simulation): recompute the partial chain with μ(P*-net) := μ(FB-net). If P* then takes the torus, the headline is the 4,300× prior, not universality.
- **Droplet start for R3** (P* disc of radius side/4, and the reverse): at finite ε domains nucleate as droplets; the band start removes curvature, which the ε-free FB-wins verdict then overstates.
- **ABM with mutation restricted to {C, D}**: isolates the ALLC/D fringe from shadows and the priced FB-net load.
- **Hypercube split with ALLC pre-seeded at x = 0.05**: tests the race argument of verdict 18 directly.

## 4. Alternative explanations

- Torus FB dominance in R2 = prior mass × a near-neutral shadow block; the prior-swap control decides.
- The finite-ε P* advance may be carried by the priced FB-net load (μ 0.024 of near-neutral costlier members inside FB domains, which pay c against P* too) rather than by ALLC; the pure-ALLC front separates them.
- "c drops out" (verdict 9) is true by construction at these N: every c-dependent transition is ≤ 10⁻⁶ per mutation event, below what 10⁵ trials resolve. It is not evidence that lazy pricing is harmless on graphs.

## 5. For the program

The ε-free half of this experiment is mostly settled by one argument: incumbency under lazy pricing needs the newcomer to pay on every edge, and on any graph with cluster interiors a copy-free newcomer's interior is free, so the exit returns to O(1/N). Cost incumbency is a well-mixed artifact, and lazy pricing on graphs is the free arm. State that in THEORY §9.2 (the "whether any pricing yields one network" sentence) once the shadow block is measured. The new content is at finite ε: the torus shadow load x, set by *local* pruning, is the finite-ε analogue of the shadow exit and decides which network wins a border. It deserves measurement as a function of ε and graph in its own right, with the mechanism stated as "P* converts the shadow into food", which is what survives either outcome of 17.
