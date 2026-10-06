# Predictions: the guard margin as a heritable trait, 2026-10-06

Spec: `specs/2026-10-06-guard-trait.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-06-guard-trait-gpt-6.1-sol.md`,
and revised; where they differ the spec is the resolution). Code: `src/guard_trait.py`. Committed before any chain,
sham, intervention, lottery or price run. ε → 0 chain numbers are lim-object quantities at the stated N (π of the
attractor chain; per-mutant entry and exit rates and their N-slopes reported separately); lottery numbers are ε = 0 at
(N, I) = (100, 64), mN = 1, Wilson 95% and paired differences.

**What was seen before this file was written** (honesty note).
(i) The mixed-guard calculus and the high-budget certificate rule (module docstring of `src/guard_trait.py`; proof in
`runs/guard-trait.md` §1) were written and validated at **n = 6, b = 16**: K's mixed closure (132 catalogue genotypes,
106 K genotypes, 8,406 contents; g = 0 block identical to the published K table), 664 K misses, 332 certified, 332
uncertified (all involving a long guard); K_c4 search on the 332: 168 newly derived within b, 0 soundness violations,
168 checked by the independent checker (225 Dist nodes, 25 Lemma C witnesses replayed, 0 failures); 329 plays change
vs K. **The full K_c4 closure over the n = 6 mixed catalogue equals the targeted table (0 differing plays).**
(ii) n = 8: the mixed catalogue has 1,220 genotypes (610 sources × 2), 1,066 K genotypes (154 sources have no level ≥ 1
atom anywhere, so their two genotypes are one program), 803,016 atom contents. Nothing else at n = 8 was seen.

## Design choices fixed before the run

1. **Semantics.** Genotype (s, g), g ∈ {0, L}; a g = L reader's level-k atoms read ¬□_{2b+8}^k⊥ (offset b + 8). A
   quoted argument ^A of x is A at x's budget **and x's guard** (it is part of x's source). The opponent's definition
   carries the opponent's guard, so cross-guard blocks are built from one mixed closure, never from homogeneous
   tables. A source with no level ≥ 1 atom anywhere (quotes included; FairBot, `BOX(THEM(THEM))`, C, D, the Gödel
   sentence `not(BOX(THEM(ME)))`, …) has a guard-free definition: (s, 0) and (s, L) are the same program and twins by
   construction. Its g bit is a sham bit carried by the real catalogue.
2. **Calculus and method.** K_c4 (K + Cut + UnfId + Dist⁺), b = 16, search cap 40, GL-erasure prune, K's JLöb
   candidate rule. Targeted table: K's mixed closure; the extension-model certificate on every GL-true K miss, extended
   by the high-budget rule (a box query above b + 1 is false in I_E when its content is Std-false and GL+Def does not
   prove erase(⊡E → Y), ⊡E = ∧_{X∈E}(X ∧ □X)); the K_c4 search on the uncertified misses only (in ≤ 3 chunks, each
   its own closure). Exactness: K ⊆ K_c4 and the certificate covers every size; validated against the full closure at
   n = 6. Every newly derived content is extracted and checked by the independent checker (Lemma C witnesses replayed
   with the reader's budget and the opponent's genotype, guard included). Soundness checked in every closure.
3. **Prior.** μ(s, g) = μ_canon(s) · π_g(g), π_g uniform or (0.9, 0.1) on (0, L).
4. **Kernels.** *Joint:* a mutant genotype is drawn from μ. *Separate:* a mutant of resident (s, g) is (s′, g) with
   probability ½ μ_canon(s′) or (s, g′) with probability ½ π_g(g′) (a draw equal to the resident is a no-op); in a
   polymorphic state the parent is drawn by frequency. Under the joint kernel the chain is lumped by identical rows and
   columns (joint lumpability across both guard populations: the lump is computed on the full 1,220 table); within a
   lump π splits ∝ μ (exact for a resident-independent kernel). Under the separate kernel the kernel is
   resident-dependent and behavioural lumping is not valid, so the chain runs on genotypes (lumping only genotypes
   with identical rows, columns and identical kernel rows over the lumps, by partition refinement).
5. **Neutral vs active.** (s, L) is a guard twin of (s, 0) iff their rows and columns in the full mixed table are
   identical (payoffs, and costs in the price sweep); neutral guard mass = π on twin (s, L) genotypes; active guard
   mass = π on non-twin (s, L). *Allocation* of a label = the share of the label-1 member in the π of twin pairs
   (neutral guard mass / mass of twin pairs), compared with the sham's.
6. **Sham bit.** The g = 0 K_c4 block duplicated with a label h ∈ {0, 1} that changes no proof and no cost, under the
   same priors and kernels.
7. **Action-change table.** For every ordered pair of catalogue genotypes (x, y) with at least one g = L, compare
   x's play against y with the play of x̄ against ȳ (bars: g set to 0). Each changed cell is classified by the new
   outcome of the pair: new mutual C (enabled cooperation); x newly C while y D on x (x newly suckered: enabled
   exploitation by y); x newly D while y C on x (enabled exploitation by x); new mutual D (protection). Weighted by
   μ(x)μ(y) under the uniform prior.
8. **Attribution (N = 10⁴, uniform, joint).** *Newly enabled fakers:* genotypes z that strictly invade some x
   (U[z, x] > U[x, x]) in the mixed table and z̄ does not strictly invade x̄ in the guard-erased table. *Newly enabled
   cooperative partners:* g = L genotypes with a newly enabled mutual-cooperation cell (self-play included) that are
   not fakers. Deletion = prior weight 0; other weights retained. A "delete both" cell is added.
9. **Price.** Amortized c·(2b + 8)/N per match for every g = L genotype whose source reads a guard (twins included);
   guard-free sources read no guard and pay nothing. c ∈ {0, 0.01, 0.1, 1}, N = 10⁴. The schedule is imposed.
10. **Chains.** Seeded log-domain solver of `src/k_cut.py` (every monomorphic state and every 2-type deep state
    seeded; expansion by relative inflow to 10⁻¹²; log-domain GTH), generalized to a resident-dependent kernel; audit:
    residual ‖πQ‖/‖π·out‖, the lazy linear-domain chain as independent state discovery (joint kernel), dominant
    entry/exit rates recomputed by an mpmath Moran sum, N-slopes of the top exits and entries from N ∈ {10³, 10⁴,
    3·10⁴}. References: K (published b = 16 numbers), the g = 0-only K_c4 chain, and the g = L-only chain (L–L block
    with the guard-free sources).
11. **Cores.** Supported self-cooperators (π ≥ 10⁻³ at N = 10⁴) of the g = 0-only and g = L-only chains.
    Establisher: self-cooperates, defects on D. Incompatible pair: two establishers that mutually defect or one
    strictly invades the other. Rival of a core: an establisher outside the core that mutually defects with a core
    member. Bridge of (core, R): a self-cooperating non-ALLC class that mutually cooperates with every core member and R.

## RE predictions (copied verbatim from the spec)

1. **Neutral guard mass is prior- and kernel-sensitive and uninformative; the active g = long mass is small:**
   π on active g = long genotypes ≤ 0.2 at N = 10⁴ under the uniform prior and both kernels, and the sham bit's
   allocation matches the neutral guard twins' within 0.05 under each kernel. *Falsifier:* active g = long π ≥ 0.4,
   or the sham allocation differing from the neutral twins' by ≥ 0.15. Grey zone 0.2–0.4.
2. **Displacement is explained by transition structure, not interpolation** (sol's reading adopted): the mixed
   chain's P(C,C) at N = 10⁴ need not lie between the homogeneous references, and the RE predicts it within 0.03 of
   K, with the attribution interventions showing the newly enabled fakers lowering P(C,C) by more than the newly
   enabled partners raise it. *Falsifier:* P(C,C) above K by ≥ 0.05 (the margin is worth buying), or the partner
   intervention's gain exceeding the faker intervention's loss by a factor ≥ 2. Grey zone between.
3. **A g = long FairBot mutant is exactly neutral in a g = 0 FairBot resident** (all four encounter payoffs
   identical, N·ρ = 1 to numerical error) **and g = long P\* strictly invades no g = 0 core program.** *Falsifier:*
   a payoff difference among the four, or P\*_long strictly invading a core program.
4. **The lottery's efficient fraction is unchanged within pairing** (paired difference's interval includes 0) and
   g = 0 holders are ≥ 0.5 of islands under the uniform prior. *Falsifier:* paired difference ≤ −0.15, or g = long
   holders ≥ 0.7.
5. **Under the amortized price the active g = long mass decreases monotonically in c and is ≤ 0.05 at c = 0.1.**
   *Falsifier:* non-monotone in c, or ≥ 0.2 at c = 0.1.

*Operationalization (fixed now).* RE 1: "sham allocation" vs "neutral twins' allocation" as in design choice 5,
uniform prior, N = 10⁴, each kernel. RE 2: "the newly enabled fakers lowering P(C,C)" = P(C,C)(delete fakers) −
P(C,C)(mixed) (the loss they cause); "the partners raise it" = P(C,C)(mixed) − P(C,C)(delete partners); held if the
first exceeds the second and |P(C,C) − 0.670960| < 0.03; falsified if P(C,C) ≥ 0.720960 or the partner gain ≥ 2 × the
faker loss. "K" = the published K b = 16 value 0.670960 (the g = 0-only K_c4 chain is reported beside it). RE 3:
FairBot is guard-free in this semantics, so its half is true by construction; the four payoffs are computed for every
core program with a guard (`BOX1(THEM(ME))`, `BOX1(THEM(THEM))`, PrudentBot) as well and reported, but the verdict
is on the spec's literal statement. "Core program" = the g = 0 core of design choice 11. RE 4: lottery paired against
the g = 0-only K_c4 catalogue with the same seeds; "g = long holder" = an efficient island whose majority cooperative
genotype has g = L and is not a guard twin; twin holders (g = L members of a twin pair) are reported separately and
counted as neither, and the share is also reported with twins counted by their g bit. RE 5: "monotonically" = non-increasing across c ∈ {0, 0.01, 0.1, 1}
up to 10⁻⁴.

## Subagent predictions

S1. **Catalogue.** In the n = 8 mixed table at b = 16, P\* and P2 self-cooperate at g = L (as in the long-guard family
    sweep), and ≥ 10 of the 37 Gödel/Con-set classes strictly invade some g = L reader they do not invade at g = 0.
    The g = 0 block differs from K_c's published b = 16 table only by Dist⁺ acceleration: ≤ 500 plays, μ² ≤ 10⁻⁶.
    *Falsifier:* P\*_L self-defects, or ≤ 3 such Gödel/Con classes, or the g = 0 block differs from K_c's by μ² > 10⁻⁵.
S2. **Action changes.** μ-weighted, enabled exploitation (x newly suckered + x newly exploiting) exceeds enabled
    mutual cooperation. *Falsifier:* enabled cooperation ≥ 2 × enabled exploitation. Grey: between 1× and 2×.
S3. **Twins.** Under the joint kernel the neutral twin allocation equals the prior share of g = L (0.5 / 0.1) to
    10⁻⁶ and the sham's equals it too (a theorem of the lumped chain; a check of the code). Under the separate kernel
    the guard twins' allocation is within 0.05 of the sham's. *Falsifier:* joint-kernel deviation > 10⁻⁴, or a
    separate-kernel gap ≥ 0.15. Grey: 0.05–0.15.
S4. **Composition.** At N = 10⁴, uniform prior, joint kernel, the P\*-type genotypes at g = L (P\*, P2 and the
    `and(BOX1(THEM(x)),not(BOX(THEM(y))))` family) carry ≤ 0.05 of π, and the guard-free core (FairBot,
    `BOX(THEM(THEM))`) carries ≥ 0.25. *Falsifier:* P\*-type at g = L ≥ 0.15, or guard-free core ≤ 0.15.
S5. **Price.** Active long mass at c = 1 is at most half its c = 0 value. *Falsifier:* at c = 1 it is ≥ its c = 0
    value.
S6. **Lottery.** Every lottery cell (both priors, mixed and g = 0-only) is ≥ 0.85 efficient (K_c was 20/20).
    *Falsifier:* any mixed cell ≤ 0.6.
S7. **N-scaling.** The active long mass changes by less than a factor 3 between N = 10³ and 3·10⁴ (its exits are
    neutral drift like the core's, ∝ 1/N). *Falsifier:* a factor ≥ 5. Grey: 3–5.

## Verdict rules

Held / failed / grey exactly as each prediction states; grey is reported as inconclusive. A prediction whose
computation did not run is "not run", never held. A design degeneracy (e.g. an empty faker or partner set) is
reported as such and the dependent prediction is "degenerate", not held. Failures, including mine, go to REJECTED
drafts.
