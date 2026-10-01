# Predictions: rival cooperative networks under spatial structure (lazy pricing), 2026-10-01

Status: reviewed by astra (`reviews/2026-10-01-rival-networks-gpt-6-astra.md`) and fable
(`reviews/2026-10-01-rival-networks-fable.md`), then revised; changes are marked [after review]. Committed before any
run. Only static computations (`src/rival_static.py`, quoted below) and declared smoke tests have been run:
- graphs outside the measured grid (torus side 8, hypercube d = 4, neutral blocks only);
- a 200-generation agent-based run on a side-8 torus;
- ε = 0 all-D timing runs at full agent-based size, in which nothing can change;
- a timing run of one near-neutral block on torus side 24 and hypercube d = 7.

[after review] An exact check of the kernel (`src/rival_exact.py`, `runs/rival_exact.txt`):
- it solves the absorbing chain over all 2^N configurations on hypercube d = 3 and torus 3 × 3, for five
  non-neutral blocks;
- all 10 exact values lie inside the 95% intervals of 10⁶ Monte Carlo trials of `_invade_fix`;
- the convention, stated here and shared with `src/graph_rates.py` and `src/lattice.py`: neighbours' payoffs are
  evaluated before the dying site is replaced.

## Question

In the well-mixed ε→0 chain, lazy pricing at n = 8 and c = 10⁻² goes to P(C,C) = 1.0. It gets there through cost
incumbency of P* = `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (RESULTS.md, "Priced arm"). P* exploits ALLC, and
P* and FairBot (FB, `BOX(THEM(ME))`) defect on each other. So the language holds two rival cooperative networks.
Under spatial structure, do they coexist with defection along their borders, which one spreads, and how much
welfare is lost at the borders?

## The arm and the networks

Lazy-priced modal arm (`build_priced(8, c, pricing='lazy')`), PD with T, R, P, S = 1, 0, −1, −2, so R − P = 1;
w = 0.3; c ∈ {0, 10⁻², 10⁻¹}. Lazy pricing charges nothing against C, D or an exact copy, and charges the atoms
price against every other non-trivial program. c = 0 is the free modal arm at n = 8.

Each class gets one label from its actions (`rival_static.networks`):
- **D-type:** defects against a copy of itself.
- **exploitable:** cooperates with itself and with D. This is ALLC and its kin, the shadows.
- **FB-net:** cooperates with itself, defects on D, and cooperates mutually with FB.
- **P\*-net:** the same, but mutually with P*.
- **other-coop:** the remaining self-cooperators that defect on D.

No class is in both networks.

| label (c = 10⁻²) | classes | prior mass μ |
|---|---|---|
| D-type | 323 | 0.503 |
| exploitable | 169 | 0.473 |
| FB-net | 72 | 0.0237 |
| P*-net | 4 | 5.5·10⁻⁶ |
| other-coop | 42 | 5.3·10⁻⁴ |

The "46 classes" P* cooperates with (RESULTS.md) are mostly exploitable programs such as `not(BOX(THEM(ME)))`.
Only 4 classes are P*-net proper: P* and three spellings of the same pattern. FB-net outweighs P*-net in prior
mass by 4,300×.

**Payoff blocks (static).** A block is (u_qq, u_qr, u_rq, u_rr) for mutant q against resident r.

| pair q \| r | c = 0 | c = 10⁻² | c = 10⁻¹ |
|---|---|---|---|
| P* \| FB | (0, −1, −1, 0) | (0, −1.06, −1.02, 0) | (0, −1.6, −1.2, 0) |
| FB \| P* | (0, −1, −1, 0) | (0, −1.02, −1.06, 0) | (0, −1.2, −1.6, 0) |
| ALLC \| FB | neutral | neutral | neutral |
| ALLC \| P* | (0, −2, 1, 0) | same | same |
| D \| FB = D \| P* | (−1, −1, −1, 0) | same | same |
| FB \| D = P* \| D | (0, −1, −1, −1) | same | same |
| D \| ALLC | (−1, 1, −2, 0) | same | same |
| P*-shadow `not(BOX(THEM(ME)))` \| P* | neutral | (0, −0.02, −0.04, 0) | (0, −0.2, −0.4, 0) |

Lazy pricing is free against constants and copies, so seven of these pairs do not depend on c at all. Entry
from all-D is the same block for FB and P*, so on any graph the two networks enter all-D at the same
per-mutant rate. They differ in μ, by 4,300×, and in what can leave them:
- **FB:** its only neutral mutant at c > 0 is ALLC (μ 0.47). It has no strict invader.
- **P\*:** it has no neutral and no strict mutant at c > 0. Its nearest exit is its own shadow,
  `not(BOX(THEM(ME)))` (exploitable, μ 1.3·10⁻³). That shadow pays half what P* pays on their shared edges.
- **The two networks against each other:** FB pays 2c per cross edge and P* pays 6c, so FB wins a border
  between them.

**Static well-mixed rates, w = 0.3** (`chain.fixation`). Hitting N/2 at N = 64 / 256 / 1,024 / 4,096:

| pair | c | hitting N/2 |
|---|---|---|
| FB \| D | all | 0.054 / 0.027 / 0.013 / 0.0068 (fixation equal) |
| ALLC \| FB | all | 2/N exactly; fixation 1/N |
| D \| ALLC | all | 0.27 / 0.26 / 0.26 / 0.26 |
| D \| FB | all | 1.6·10⁻⁴ / 6·10⁻¹⁴ / 2·10⁻⁵¹ / ~0 |
| ALLC \| P* | all | 2.5·10⁻⁸ / 3·10⁻³⁰ / ~0 / ~0 |
| P* \| FB | 0 | 6.9·10⁻⁴ / 1.9·10⁻¹⁰ / 9·10⁻³⁶ / ~0 |
| P* \| FB | 10⁻² | 5.1·10⁻⁴ / 4.6·10⁻¹¹ / 2·10⁻³⁸ / ~0 |
| P* \| FB | 10⁻¹ | 2.6·10⁻⁵ / 1·10⁻¹⁶ / ~0 / ~0 |
| FB \| P* | 10⁻² | 6.7·10⁻⁴ / 1.8·10⁻¹⁰ / 8·10⁻³⁶ / ~0 |
| FB \| P* | 10⁻¹ | 5.2·10⁻⁴ / 7.9·10⁻¹¹ / 6·10⁻³⁷ / ~0 |
| P*-shadow \| P* | 10⁻² | 0.030 / 6.5·10⁻³ / 8.8·10⁻⁴ / 1.5·10⁻⁵ |
| P*-shadow \| P* | 10⁻¹ | 0.020 / 9.7·10⁻⁴ / 2·10⁻⁷ / 4·10⁻²¹ |

Well mixed, P*'s exits are all exponentially small at c > 0. That is the lock-in.

## Design

Four parts. The first three are ε-free; the fourth is not.

**Update rule.** Death-birth on vertex-transitive graphs, the rule of `src/graph_rates.py`:
- a uniformly random site dies;
- its neighbours compete for the site with weight exp(w · their mean payoff over their own neighbours);
- costs are included in payoffs;
- graphs are the torus at side 16 / 32 / 64 (N = 256 / 1,024 / 4,096, degree 4) and the hypercube at
  d = 6 / 8 / 10 (N = 64 / 256 / 1,024, degree d).

Kernels are in `src/rival_kernels.py` and the driver in `src/rival_run.py`.

**R1, per-mutant rates (ε-free).** These are hitting probabilities of N/2 for a single uniformly placed
mutant. Each success is continued to fixation or loss, capped at 4N generations, for at most 20 successes per
cell, which gives P(fix | half). That is the quantity a transition network needs, because reaching half is not
fixation.
- Sampling is adaptive: batches of 2,000 trials, until 20 successes, 10⁵ trials, or a time cap (400 s, or
  1,200 s at N = 4,096). Intervals are 95% Wilson; undecided trials are excluded from the denominator.
- Exactly neutral blocks are not simulated (2/N, and P(fix | half) = ½ by the martingale), except as a check
  at N ≤ 256.
- The requested pairs are all included: P* | FB, FB | P*, ALLC | each, D | each, each | D, and D | ALLC.
- Identical blocks are simulated once and reported at every c they occur.

**R2, a reduced spatial transition network (ε→0, approximate).** Pairwise rates do not determine stationary
mass, so I build a lumped chain over the five labels:
- *Representatives:* each label is represented by one resident: D, FB, P*, ALLC, and the heaviest other-coop
  class `not(BOXD(THEM(^C)))`.
- *Rates:* the rate from label A to label B is Σ μ(q) · ρ_fix(q | rep(A)) over every class q labelled B.
  Here ρ_fix = P(hit N/2) · P(fix | N/2) on the graph.
- *Coverage:* every distinct block between a representative and any class is measured on every graph and
  every c, 258 blocks per graph.
- *Validation (static, done).* The same construction with well-mixed fixation probabilities reproduces the
  published full chain:

| c | N | lumped, self-cooperating mass | full chain P(C,C) |
|---|---|---|---|
| 10⁻² | 10³ | 0.42 | 0.379 |
| 10⁻² | 10⁴ | 0.997 | 0.9985 |
| 10⁻² | 3·10⁴ | 1.000 | 1.000 |
| 0 | 10³ | 0.42 | 0.371 |
| 0 | 10⁴ | 0.70 | 0.617 |
| 0 | 3·10⁴ | 0.80 | 0.725 |

  At c = 10⁻² it also reproduces the support: P*-net at N ≥ 10⁴. It over-predicts by at most 0.08 at c = 0,
  where fakeable FB-net members such as `BOX(THEM(THEM))` have strict exits their representative lacks.
- [after review] *Partially lumped chain (the primary R2 object).* Astra points out that labels are not
  lumpable: an invasion changes the resident program, not only its label. So the chain's states are 16
  residents, the heaviest members of each label by μ:
  - D;
  - 6 FB-net: FB, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`, `BOX(THEM(^C))`, `BOX1(THEM(^C))`;
  - all 4 P*-net;
  - 3 exploitable: C, `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))`;
  - 2 other-coop.

  A mutant that is a resident goes to that resident. Any other mutant goes to its label's primary
  representative, so lumping happens only outside the resident set.
  - *Static validation (well mixed):* self-cooperating mass against the full chain.

    | c | N = 10³ | 10⁴ | 3·10⁴ |
    |---|---|---|---|
    | 0 | 0.370 (0.3707) | 0.617 (0.6172) | 0.725 (0.7246) |
    | 10⁻² | 0.378 (0.379) | 0.998 (0.9985) | 1.000 (1.000) |

    So with these 16 residents the well-mixed chain is reproduced to 0.002. On graphs the claim is still a
    representative-model result. Graphs can open exits from programs outside the resident set that are
    negligible well mixed, and I report how many blocks are missing.
  - *Cost:* the resident set needs 546 distinct blocks per graph (258 for the five primary representatives).
    The extra residents (tier 2) are not run at torus side 64. [after review: fable found that the draft code
    made those residents absorbing.] There a missing block for a non-primary resident is replaced by the same
    mutant's block against its label's primary representative. The report counts missing and fallback blocks,
    and flags any state with zero measured out-rate as "absorbing in sample" instead of trusting its π.
  - *Uncertainty* [after review]:
    - Blocks with 0 successes enter at rate 0. In a sensitivity variant they enter at half their Wilson upper
      bound, but only if they have at least 10⁴ trials [after review], so that under-sampled blocks cannot set
      the band.
    - Undecided trials are counted and reported.
    - Stopping at a fixed number of successes (inverse sampling) biases h/n upward by about 1/h. That is 5% at
      h = 20, and 10% at h = 10 for tier ≥ 1 blocks, which get 10 successes and a 200–300 s cap.
- *Run check:* the full well-mixed chain at N = 256 / 1,024 / 4,096 (`wmchain`), against the lumped
  well-mixed values. At c = 10⁻² those are 0.27 / 0.43 / 0.70 self-cooperating, with P*-net at
  0.010 / 0.022 / 0.27.
- *Limits:* the lumping assumes that every member of a label leaves like its representative. Graph claims
  are made at that level, and I report the transition structure, not only π.
- [after review] *Prior swap control* (no extra simulation). Recompute the chain with P*-net's prior mass scaled
  up to FB-net's. If P* then takes the graph, the result is about the 4,300× prior, not about universality.
- [after review] *What R2 adds.* Fable expects R2 on the torus to be decided by two blocks:
  - shadow | P*, which his 1,000–12,000-trial checks put at (1.0–1.3) × 2/N;
  - FB | P*.

  The π table is then bookkeeping. I keep it, because the chain is the only place where all exits are
  weighed against each other, and I present the two blocks as the content.

**R3, domain competition (ε-free, no mutation).** FB on one half and P* on the other:
- on the torus, a straight split with two borders; on the hypercube, the subcube split on the top bit, so
  every site starts with one cross neighbour;
- replicates: 400 / 200 / 60 on the torus and 400 / 200 / 100 on the hypercube, at each c;
- reported: P(FB reaches 3N/4 before N/4), P(fix | first passage), first-passage time, border velocity, and
  the fraction of edges joining FB and P* (all of them mutual defection) before first passage.
- [after review] *Velocity* is the Wald ratio Σ ΔFB / Σ(generations × recorded cross-edge count), over
  records before first passage. That is FB's gain per cross edge per generation, and it is comparable with the
  first-order p_FB − p_P* despite roughening. P(FB first) does not depend on roughening (fable), so verdict 11
  is the robust one.
- [after review] *Droplet starts* on the torus at side 32 and 64, 100 / 40 replicates per c: a disc of radius
  side/4 of one network in a sea of the other, P*-in-FB and FB-in-P*. Reported: P(disc reaches N/2 before it
  is lost). At finite ε domains nucleate as droplets, and the band start removes curvature.

**R3b, controlled fronts (ε-free, no mutation)** [after review: astra's and fable's control of the threshold
argument].
- *Start:* P* on one half. The FB half has each site replaced by ALLC independently with probability
  x ∈ {0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4}.
- *Graphs and c:* torus 64 (4,000 generations) and hypercube 10 (2,000 generations), 20 replicates, every c.
- *Measured:* P*'s velocity (gain per generation per unit border, over the first 500 generations and over the
  whole run), and the ALLC share of the FB-side front. Front sites are non-P* sites with a P* neighbour.
  Seeded ALLC is eaten at the front and refilled only by neutral drift.
- The hypercube rows at x = 0.05 are fable's "pre-seeded hypercube split" control for verdict 18.

**R4, agent-based runs at finite ε (approach rates only, not π).**
- *Graphs:* torus side 128 and hypercube d = 14, both N = 16,384.
- *Settings:* ε = 10⁻³ (εN = 16); mutants drawn from μ over all classes.
- *Cells:* c ∈ {0, 10⁻², 10⁻¹} × {all-D start, half-split FB/P* start}, plus ε = 10⁻⁴ at c = 10⁻¹ for both
  starts. Seeds [after review]: 4 per cell on the torus, 2 on the hypercube.
- [after review] *Controls* (split start, c = 10⁻²):
  - `split-noALLC`, on both graphs: the ALLC class is never supplied by mutation;
  - `split-CDonly`, on the torus: only ALLC and D are supplied, which separates the ALLC/D fringe from the
    priced FB-net load;
  - torus side 64 with 3 seeds and 5·10⁴ generations, as a small-system check.
- *Length:* 2·10⁵ generations on the torus and 10⁵ on the hypercube, recorded every 100.
- *Recorded:*
  - P(C,C) over edges, label shares and the ALLC share;
  - mutual-defection (MD) edges, split into FB-net–P*-net borders, edges with a D-type end, and other;
  - [after review] the composition of the front (ALLC and FB-net among non-P* sites with a P*-net
    neighbour);
  - [after review] the interaction welfare loss f_DD + ½(f_CD + f_DC), which is astra's measure. It is
    reported beside the MD fraction × (R − P), with R − P = 1, and beside the compute cost per edge;
  - rival-border MD is also averaged only over records where both networks hold at least 10% (fable).

## Mechanism I expect at finite ε (static argument)

Mutation keeps an ALLC load x inside FB domains. ALLC is neutral there, and D mutants prune it, as in E3,
where x = 0.26 at ε = 10⁻³ well mixed. P* eats ALLC (+1 per edge, ALLC −2). At a border:
- the payoff of a P* site per cross edge is x + (1 − x)(−1 − 6c);
- the average for the FB side is (1 − x)(−1 − 2c) − 2x.

P* advances iff 3x > 4c(1 − x), that is, iff x > x\*(c) = 4c / (3 + 4c). This gives 0, 0.013 and 0.118 at
c = 0, 10⁻² and 10⁻¹. The same threshold holds in the mean field at a 50/50 split. So the shadow that mutation
supplies inside FB domains should reverse the border that FB wins without mutation.

[after review] Two qualifications:
- *Astra:* this compares cross-edge payoffs, not whole neighbourhoods, and bulk x need not equal x at the
  front. R3b and the front records test the threshold directly.
- *Fable:* ALLC pruning on the torus is local. A D mutant landing in an ALLC pocket is favoured there, whatever
  the global x. So the torus x should be far below the well-mixed 0.26.

## Verdicts

### R1: per-mutant rates (ε-free)

1. **Entry is identical and N-independent on the torus.**
   - FB | D = P* | D, which is a single block at every c.
   - [after review] The criterion is interval overlap with the priced arm's c = 0 values, measured with 1,000
     trials each: torus 0.108 [0.090, 0.129] / 0.108 [0.090, 0.129] / 0.104 [0.087, 0.125]; hypercube
     0.084 [0.068, 0.103] / 0.057 [0.044, 0.073] / 0.044 [0.033, 0.059]. Fable measured 0.077 [0.062, 0.095] at
     torus side 32, so the torus values may sit near 0.08–0.09.
   - Torus values vary by less than 1.5× across sides.
   - P(fix | half) ≥ 0.9.
2. **Shadows.**
   - ALLC | FB matches 2/N within its interval at N ≤ 256.
   - ALLC | P* < 10⁻⁴ on every graph (0 successes in ≥ 5·10⁴ trials allowed).
3. **No direct D invasion.**
   - D | FB = D | P* < 10⁻⁴ everywhere.
   - D | ALLC lies in [0.12, 0.30] [after review: lower bound from 0.15; fable measured 0.16–0.20], below the
     well-mixed 0.26 on the torus.
4. **Rival nucleation is suppressed at c ≤ 10⁻²** [after review: numbers from fable's checks and
   critical-nucleus estimate].
   - P* | FB and FB | P* lie below 2/N on every graph.
   - Torus side 16: ratio to 2/N in [0.01, 0.15].
   - Torus side 64: 0 successes in the trials run for both pairs.
   - Hypercube d = 10: ratio < 0.1.
   - At c > 0, FB | P* ≥ P* | FB wherever both are resolved.
5. **c = 10⁻¹ opens nucleation of FB inside P*.** The cost asymmetry, FB paying 1.2 and P* 1.6 per cross edge,
   gives a critical nucleus of 3×3–4×4 sites (fable). So ρ(FB | P*) on the torus is 3·10⁻⁴–2·10⁻³ and roughly
   N-independent: the side-64 value is at least 0.3× the side-16 value.
6. **Structure frees P\*'s shadow.** For `not(BOX(THEM(ME)))` | P*, both cluster interiors are free, and P* pays
   twice the shadow's price on the border.
   - At c = 10⁻², its graph value is at least 0.7 × 2/N at every size, against 1.5·10⁻⁵ well mixed at
     N = 4,096. Fable measured 1.0–1.3 × 2/N.
   - At c = 10⁻¹, at least 2/N on the torus at side ≥ 32, against 2·10⁻⁷ and 4·10⁻²¹ well mixed.

### R2: partially lumped spatial chain (ε→0, representative model)

7. **Torus: cooperation tends to 1 and FB-net holds it.** Given verdicts 1, 2 and 6 this is close to
   foreordained, as fable notes, and the content is the transition structure.
   - *The estimate:* entry is about 0.09 · μ(FB-net) = 2.1·10⁻³ per mutation event. FB-net leaves through
     ALLC at 0.47/N, after which D takes ALLC. So π(D-type)/π(FB-net) ≈ 220/N.
   - *Self-cooperating mass:* 0.54 / 0.82 / 0.95 (±0.1) at N = 256 / 1,024 / 4,096, at every c.
   - *π(D-type):* falls with slope in [−1.2, −0.8] in log N.
   - *Structure:* π(FB-net) ≥ 5 π(P*-net) at every side and c > 0. At c = 10⁻¹, π(P*-net) < 0.01 at side 64,
     because P*'s main exit there is FB nucleation (verdict 5).
   - *Prior swap control:* with P*-net given FB-net's prior mass, P*-net holds at least as much as FB-net at
     c = 10⁻². The P*–FB cost asymmetry favours FB, so I expect a split near even, not a P* takeover. If so, the
     torus result is carried by the 4,300× prior.
   - *Contrast:* well mixed at N = 4,096 and c = 10⁻², the lumped chain has P*-net 0.27 against FB-net 0.43,
     and the full chain gives P* all the mass from N = 10⁴. Structure should reverse that: P*'s exits become
     O(1/N) through its shadow, while FB keeps its prior advantage.
8. **The hypercube is in between.** Self-cooperating mass is 0.21 / 0.43 / 0.69 (±0.12) at d = 6 / 8 / 10.
9. **c drops out of the torus D-share.** π(D-type) at c = 10⁻² and 10⁻¹ is within 0.05 of c = 0 at each side.
   [after review] This holds by construction (fable): every c-dependent transition is ≤ 10⁻⁶ per mutation
   event. It is a consistency check, not evidence that lazy pricing is harmless.
10. **The well-mixed reference.** The partially lumped well-mixed chain is within 0.02 of the full chain at
    N = 256 / 1,024 / 4,096 for every c. R2 is reported as unvalidated if the gap exceeds 0.05.

### R3: domain competition (ε-free)

11. **c = 0 is a symmetry check.** P(FB first) = 0.5 within its interval on every graph.
12. **Without mutation, FB wins a band border at c > 0.**
    - Torus, c = 10⁻²: P(FB first) = 0.56 / 0.72 / 0.98 (±0.15) at side 16 / 32 / 64, the biased-walk
      estimate.
    - Torus, c = 10⁻¹: ≥ 0.85 at side 16, and ≥ 0.97 at 32 and 64.
    - Hypercube: at least the well-mixed birth-death value minus 0.1. That is 0.52 / 0.55 / 0.60 at c = 10⁻²
      and 0.68 / 0.85 / 0.98 at 10⁻¹. The well-mixed death-birth values agree with these within 7%.
13. **Border velocity on the torus** [after review: per cross edge, Wald ratio]. FB gains
    9.2·10⁻⁴ ± 50% per cross edge per generation at c = 10⁻², 9.1·10⁻³ ± 50% at 10⁻¹, and 0 within 2 s.e. at
    c = 0.
14. **Droplets.**
    - A P* disc in FB is lost with probability ≥ 0.9 at every c > 0 and both sides.
    - At c = 0, curvature alone gives P(disc reaches N/2) < 0.3 for both disc types.
    - An FB disc in P* at c = 10⁻¹ reaches N/2 with probability ≥ 0.8.
15. **Welfare at the interface.**
    - Torus: the FB–P* edge fraction starts at 1/side, and its mean before first passage lies in
      [1/side, 3/side].
    - Hypercube: it starts at 1/d, and its mean before first passage exceeds 1/d.
16. **Resolution.** P(fix agrees with first passage) ≥ 0.95.

### R3b: controlled fronts (ε-free) [after review: new]

17. **P\*'s velocity rises with x and changes sign at x₀(c).**
    - At c = 0, P* advances for every x > 0 and stalls at x = 0, within 2 s.e.
    - The crossing is above the flat-border x* because front ALLC is depleted (fable):
      x₀(10⁻²) ∈ [0.015, 0.06] and x₀(10⁻¹) ∈ [0.12, 0.35], on the torus, using the first-500-generation
      velocity.
    - On the hypercube, the c = 10⁻² crossing lies within the same band.

### R4: finite ε (approach rates only, not π)

18. **From all-D, FB-net arrives first.**
    - FB-net is the majority label by generation 2,000 in every run.
    - Second-half P(C,C) is ≥ 0.85 on the torus and ≥ 0.80 on the hypercube, at every c.
19. **The shadow load** [after review: torus band moved down, following fable's local-pruning argument].
    x = ALLC / (ALLC + FB-net) in the second half of all-D runs at ε = 10⁻³ is 0.01–0.10 on the torus and
    0.10–0.35 on the hypercube. It is lower at ε = 10⁻⁴.
20. **On the torus, mutation can reverse the border; it does so slowly** [after review: weakened].
    - From the split start at c = 0, P*-net exceeds 0.9 by generation 10⁵ in every replicate.
    - At c = 10⁻², P* gains on average, with P*-net above 0.5 at the end of the run in at least 2 of 4
      replicates. The rate is set by the measured front x against x₀(10⁻²) from R3b.
    - At c = 10⁻¹, FB wins (P*-net below 0.1 at the end) unless the measured front x exceeds x₀(10⁻¹).
    - Controls at c = 10⁻²:
      - `split-noALLC`: FB gains, the sign of verdict 12.
      - `split-CDonly`: P* gains at least as fast as in the full-prior run.
21. **The hypercube split start.**
    - At c = 0, P* exceeds 0.9 by generation 2·10⁴.
    - At c ∈ {10⁻², 10⁻¹}, FB wins (P*-net < 0.1 by generation 2·10⁴) in at least 1 of 2 seeds at 10⁻², and in
      both at 10⁻¹. The coordination escape, about 25 generations, outruns the build-up of x (fable).
22. **P\* from all-D.**
    - Hypercube: P*-net stays below 0.01 throughout.
    - Torus: no unconditional prediction. Conditional: if a P*-net domain reaches 1% of the torus at c = 0, it
      exceeds 50% within 5·10⁴ generations.
23. **Welfare lost at borders is small.**
    - On the torus, while both networks hold at least 10%, the FB-net–P*-net MD-edge fraction averages
      ≤ 2/side = 0.016, and its peak is ≤ 4/side.
    - In every split run, that average is below the MD fraction with a D-type end over the same records.
    - The interaction welfare loss in the second half is ≤ 0.08 in all-D runs.

## Falsifiers

- *Of the spatial result (R2):* π(P*-net) ≥ π(FB-net) on the torus at side 64, c = 10⁻², with no state absorbing
  in sample; or a π(D-type) slope shallower than −0.6.
- *Of the chain:* the partially lumped well-mixed chain differs from the full well-mixed chain by more than 0.05
  in self-cooperating mass at any of N = 256 / 1,024 / 4,096. If so, R2 is reported as unvalidated, and only R1
  is used.
- *Of the shadow-as-food mechanism (R3b and R4):* in R3b, P*'s velocity does not increase with x at c = 10⁻²; or
  in R4, `split-noALLC` shows P* gaining as fast as the full run.
- *Of the border cost (R3):* P(FB first) at c = 10⁻¹ on torus side 64 below 0.8.

## What each outcome would mean

- **If 6 and 7 hold, cost incumbency is a well-mixed artifact.**
  - Under lazy pricing a newcomer escapes the price only on copies. On a graph, a cluster's interior is all
    copies, so the newcomer pays only on its border, and the incumbent pays there too.
  - The exit returns to O(1/N), and lazy pricing on graphs behaves like the free arm.
  - Which network holds the ε→0 mass is then set by prior mass, and the prior swap control says how much.
- **If 17 and 20 hold, finite ε has its own answer: P\* converts the shadow into food.**
  - Mutation keeps ALLC inside FB domains, and P* eats it at the border. So at finite ε a border can move
    toward the ALLC-punishing network even where it wins nothing without mutation.
  - [after review] This is a contrast between rare-mutation occupancy (ε→0) and mutation-dependent invasion
    (finite ε). It is not an order-of-limits theorem, since no joint scaling of N, ε and t is claimed.
- **If 7 fails because P\* takes the torus,** the well-mixed lock-in is robust to structure, and parochial
  cooperation is the lazy arm's answer on graphs too.
- **On welfare:** if 23 holds, borders between rival networks cost about 1/side of edges. The D fringe costs
  more.
- **If 12 holds and 20 fails,** compute cost decides borders even at finite ε, and FB is favoured in both
  regimes.
