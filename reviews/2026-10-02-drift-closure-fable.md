# Review of `predictions/2026-10-02-drift-closure.md` (fable, 2026-10-02)

Numbers below come from read-only scripts over `fringe.build_variant`, `moat_static.closure` and the local-estimate matrices (scratch under `scratchpad/fable/`). Astra's points are not repeated; where I build on one I say so.

## 1. Design flaws and fixes

**1.1 The "local estimate" is the full monomorphic chain, so a disagreement with the driver points at the driver, not at missed routes.** At depth 3 from all-D the estimate holds 471 of 471 classes (n = 8; 472 for addP12b) and is solved by GTH with no pruning. The driver differs from it only by polymorphic states, θ-pruning and `eager_top`. The brief's reading of a verdict-5 failure ("the deep chain finds routes the local estimate misses") is backwards: the likelier cause is a dropped exit edge. Say so, and on disagreement trust the unpruned GTH solve unless poly flow is non-zero. Call the estimate what it is: the unpruned monomorphic chain.

**1.2 The exits being measured sit 5–7 orders below θ, and cut_flow cannot see them (sharpening astra §1.1).** Top-state exits per mutation event at N = 10⁵ from the unpruned matrices: P\* under μ 3.3·10⁻¹³, P\* under D 2.7·10⁻¹¹, PB under CD 1.4·10⁻¹¹, P12b 5.4·10⁻¹¹. Stationary flow into their targets is ≈ 10⁻¹¹ ≪ θ = 10⁻⁶, so no target is expanded by the lazy rounds; the chain stays connected to all-D only through `eager_top` (one successor per state). If a chain of top successors cycles without reaching D, the state becomes a terminal class and `stationary()` returns an absorption lottery from the μ-seeds, with cut_flow still < 10⁻⁵ and absorb_error 0: verdict 12 passes while π is not π. The smoke cell at 10⁴ matching shows the top-successor chains reached D there, not that they will at 10⁵. Fix: for every state with π > 10⁻³ report the share of its exit flow whose targets are expanded ("kept exit share"), and expand any target carrying ≥ 1% of a top state's exit flow regardless of θ. The LU solve itself is fine: LU and GTH agree to ≤ 3·10⁻⁶ absolute and to four digits in π(D) on all five matrices checked (addP12b, μ, CD, D at 10⁵; μ at 3·10⁴).

**1.3 "Closure" under μ is a crossover at N\* ≈ 1/(wδΔf), not a property of the N-range run.** Under D and CD, mate gaps are exactly 0 or ≥ δ/2 (no pair in (0, 3·10⁻⁴)), so static closure and the chain agree. Under μ at n = 8 there are 26,806 mate pairs: 108 with 0 < |gap| < 10⁻⁷ (the chain calls these exactly neutral, ρ = 1/N), 2,652 with |gap| < 3.3·10⁻⁵ (wgN < 1 at 10⁵; suppression factor x/(eˣ−1) ≥ 0.58), 11,330 with |gap| < 3.3·10⁻⁴. `closure` at the chain's tolerance and at the dynamical ones:

| n | tol 10⁻¹² | 10⁻⁷ | 3.3·10⁻⁵ | 3.3·10⁻⁴ |
|---|---|---|---|---|
| 6 | FB, BTT, FB1 | same | none | none |
| 8 | PB, P\* | same | P\* | none |
| 9 | PB, P\* | PB | none | none |

PB's closure at n = 8 rests on one edge, to `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` (μ 1.4·10⁻⁶), gap −1.6·10⁻⁵: at 10⁵ it leaks at 0.78 of the neutral rate. At n = 9, P\* has a mate `and(BOX1(THEM(THEM)),not(BOX(THEM(^C))))` at gap −3.2·10⁻⁸ (μ 2.3·10⁻⁷) that leads out; the chain treats it as exactly neutral, so P\* is not closed at n = 9 in the object the driver computes. Only P\* at n = 8 (all mate gaps ≤ −5·10⁻³, wgN ≈ 150) is closed inside the grid. The gaps are set by the prior mass of the opponents on which siblings differ, which shrinks with n, so μ-closure is not uniform in n (the fringe version of Conjecture 4). State verdicts 8–9 as crossover statements and add control 3.1.

**1.4 Proposition 3 and the fringe are the same object; the brief should say so.** U′ = U + δf(x) is a row constant: an opponent-independent price c(x) = −δf(x) that charges constants (c(ALLC) = 2δ, c(D) = δ under D). It is neither a copy subsidy nor self-recognition; it is a fixed, world-independent fitness ordering. That is why it is not a moat in the brief's sense (a moat locks in whichever family arrives first; the fringe always favours the f-maximal closed class), and why it gives PB universality 0.33 with closure: it beats Corollary 1 by leaving the pure game. In "If 8 and 9 hold", replace "behavioural moat" with "exogenous fitness ordering", and file the fringe next to Proposition 3 as the price class its hypothesis excludes.

## 2. Predictions likely to be wrong

- **Verdict 3 (addP12b) measures language coverage, not grammar.** The static map's own regularity (max drift distance 1 at every n) says every unsuckerable class has a suckerable sibling of its own size in L_n. P12b's leak 2·10⁻⁶ is computed in L_8, where its size-14 THEM(THEM) siblings do not exist; in L_14 they would carry about its own mass and leak/μ would be O(1) as for every other class (FB 95, PB 3,700, P\* 1,100; P12b as run 4·10⁻⁴). The ≥ 300× claim will hold as run and mean nothing about prudence. Add the siblings at the same mass (astra) and predict the ratio collapses, or drop the cell.
- **Verdict 8 at n = 9:** P\* is not closed at the chain's tolerance (1.3); its exit is 2.3·10⁻⁷/N neutral plus a −5.3·10⁻⁵ edge. The prudent/rival split at 10⁵ rests on 10⁻¹²-level flows and on 1.2. Do not score it.
- **Verdict 9's slope** −1.37 reproduces by hand as the onset of suppression of FB's two suckerable mates at gaps −3.8·10⁻⁵ and −4.3·10⁻⁵ (factors 0.54 and 0.49 at 10⁵, 0.84 and 0.82 at 3·10⁴). Right number, wrong description: at δ = 10⁻³ the same window gives ≈ −1.0.
- **Verdict 7:** the CD entry barrier is exp(−wδ²N/8) = exp(−0.375) at 10⁵ and exp(−0.11) at 3·10⁴, which alone moves the odds slope from 0.5 to ≈ 0.28; 0.14 needs something more. Widen to ≤ 0.35.
- **Verdict 5's magnitude:** P\*'s residual leak under D is 1.36·10⁻⁶ against family prior 4.1·10⁻⁶ (odds 3.0); the unsuckerable FB-family entrants carry ≈ 0.0102 against leak 0.0134 (odds 0.76). Two-state balance gives rival ≈ 0.80, not 0.95; the rest is inflow structure. The 0.5 falsifier is safe, but report which two mates carry the 1.36·10⁻⁶ and whether they feed back into P\*.
- Verdict 10's constant checks: the shadow edge's factor at x = 3 is 0.157, giving odds × 5.2 with ALLC at 0.96 of FB's exits.

## 3. Missing controls

1. **μ at δ = 10⁻³ (n = 6, 8).** If the exit slope over [3·10⁴, 10⁵] returns to ≈ −1 while δ = 10⁻² gives −1.4 to −3, the variable is wδΔf·N and "closure" is a crossover. One row.
2. **μ, n = 6 at N = 3·10⁵ and 10⁶** (51 classes, seconds). FB is closed at tol 10⁻⁷ with all leaking edges at |gap| ≥ 1.4·10⁻⁵, so x ≥ 4 at 10⁶: the slope must steepen past −2. If not, the closure test is wrong, not the chain.
3. **Kept-exit-share diagnostic** (1.2) in every cell.
4. **A static one-liner:** min over unsuckerable x of leak(x)/μ(x) at n = 8–11 (see §5).

## 4. Alternative explanations

- Where two classes are both closed inside the grid (P\* 3·10⁻¹³ against PB 8·10⁻¹² at n = 8 under μ), their split is set by entry and by the ratio of two suppressed leaks, so 0.82/0.18 is not a rate statement about either family; label it as the brief does for lotteries even when the chain finds one terminal class.
- The D-fringe handover to P\* is a leak-ratio effect with a 10⁻⁶ denominator, not "the trade-off acting": a single extra sibling of P\* at n = 9 (`and(BOX1(THEM(ME)),not(BOX(THEM(^D))))`, leak 8·10⁻³) already changes the family's leak by 10³.

## 5. Beyond this experiment

- **The pure-game trade-off has a sharper dynamical form than the corner.** Lemma 1 plus the drift-distance-1 regularity give, for every unsuckerable x, leak(x) ≥ μ(x̃) for a sibling of x's own size, hence leak(x)/μ(x) ≥ c > 0 uniformly over classes. That bounds cooperative odds by c′·N^{1/2} with a constant no order of prudence improves, which is what Conjecture 4 needs and what replaces "the trade-off is a corner" (true, but definitional) with a rate theorem. It is checkable statically today.
- **The finite-ε counterpart of the fringe is resident-dependent.** Standing variance is μ weighted by mutant lifetimes against the current resident (fakers live long, deleterious mutants one generation), so a frozen μ fringe is the leading order only, and resident-dependence is where a genuine incumbency effect could enter. Re-read E3's 0.99 with that in mind before the fringe is used beyond an instrument.

## Specific checks

**(a) Proofs.** *Lemma 1:* correct; the gap formula matches `fixation` (k−1 self-count, N−1 denominator). One extra assumption: the four PD payoffs are distinct, so u(y,x) = R identifies (C,C). No polymorphic route: a single mutant in a cooperative PD world has no interior attractor (it would need S > u(y,y)); the chain's valley-crossing retry from 1/2 gives e^{−wN/4} for self-cooperating rivals, 5·10⁻⁴ at N = 100, so "e^{−Θ(N)}" is honest from N ≈ 10³. Case 2 carries over to fringes with a constant gap δΔf; case 3 is unchanged. *Proposition 1 / Corollary 1:* correct; the corollary is immediate and its content is the static fact ALLC ∈ K(FB). *Proposition 2:* the rate law and β = ½ hold under astra's assumptions plus one more: a suckerable member's faker must lead out of the network (BTT's faker is itself self-cooperating, so ℓ over-counts; the measured network exit is the right quantity). *Proposition 3:* correct as an edge statement (astra); the "equality with adverse slope" branch gives exponential suppression, not a 1/N correction, and the text should say so. Its hypothesis c(constant,·) = 0 is exactly what the fringe violates (1.4).

**(b) Tolerances.** Below 10⁻⁷ the chain is exactly neutral; `_polish` cannot misclassify a two-type row-constant gap above ≈ 10⁻¹⁰ (lstsq residual check at 10⁻¹⁰), and between 10⁻⁷ and 10⁻³ the replicator runs to rest with the true gap. The only mismatch is `closure`'s 10⁻¹² against the dynamics, quantified in 1.3.

**(c) Local estimate.** It is the unpruned chain (1.1); near-closed classes will not appear as lotteries by themselves, but θ-pruning can manufacture them (1.2).

**(d) Scope.** The arms are a labelled modified game and the re-opening of "Standing variance" is justified by E3, but the fringe should be filed as an opponent-independent price that charges constants, not as a background device distinct from Proposition 3.
