# Review of `predictions/2026-10-01-cert-pricing.md` (fable, second pass)

Static checks run with `src/cert_priced.py` at n = 8 (single `Chain.expand` calls, no exploration). Agree with astra on the component/threshold statistic and on "cannot hold mass" needing full-chain evidence; not repeated.

## 1. Design flaws and fixes

**(a) cert0 is a monotonicity criterion, and the brief should say so.** On the GL chain every box is true at world 0, so a program's world-0 action is its "default" (truth table at all-atoms-true), and atom truth is monotone non-increasing in the world index. Hence for any program that is *monotone in its atoms* (no effective negation), stable cooperation ⇒ cooperation at every world ⇒ PA-decided. Checked: 330 of 610 canonical functions are monotone, carrying 98.7% of prior mass; for monotone y, "y cooperates with x" and `hc[0,y,x]` agree on all pairs (0 mismatches); 99.99% of cert0's free cooperative mass (μ⊗μ-weighted) comes from monotone y. Equivalently: cert0 taxes exactly cooperation that is *conditional on non-provability* (negated boxes), which is P*'s defining feature. That is the honest Löbian reading (Σ1-completeness), and it is fine, but the brief's framing "legibility, not sameness" hides that the criterion coincides with a one-line syntactic rule. Fix: state it; add the syntactic control in §3(a).

**(b) The incumbency removal is a price ladder, not the free set.** P*'s strict exit exists only because `cost = c·k(x)·(1+last)` gives P* 4c at home and `not(BOX(THEM(ME)))` 2c. With a flat non-free price (c per unpriced check, no atom or depth multiplier) P* and all its non-monotone neighbours pay c alike, P* is untouched by monotone mutants (they defect on it) and by D, and its exits are neutral and ∝ 1/N exactly as at c = 0. So verdict 5 is a consequence of "cert0 free set + atom/depth ladder confined to the illegible", not of certification alone. The brief half-says this ("the new rung runs from illegible to legible") but then attributes the result to legibility. Fix: run the flat control (§3(b)) and word verdict 5 and the "What each outcome would mean" paragraph conditionally on it.

**(c) The retrospective price now applies almost only to reading non-monotone programs** (by (a)), so the "inherited" caveat is narrower than stated; worth one sentence.

**(d) `networks()` counts ALLC in the cooperative mass and in the FairBot block.** Harmless at π(C) ≈ 1e-4, but it should be excluded or reported, since the shadow is the exit being measured.

## 2. Predictions likely to be off

**Verdict 3's point values are ~0.015 too high and the band's lower edge is thin.** The two-level estimate gives the P* block 4% of block mass at c = 0; the c = 0 chain gives 13–15% (`runs/priced_limN.json`, n = 8: P* 0.041 + P*M 0.020 + P*T ≈ 0.020 at N = 1e4; 0.053 + 0.026 + ≈0.026 at 3e4). Under cert0 the P* exit rises from 3.1e-7 / 1.0e-7 to 1.8e-5 (58× / 180×), so the block's residence collapses and its time goes to all-D (via nB → D). Renewal identity: P_cert0 ≈ (P_c0 − p)/(1 − p) with p the c = 0 P*-block mass, giving 0.583 at N = 1e4 and 0.693–0.700 at 3e4 (c = 1e-2), i.e. c = 0 minus 0.03, against the brief's 0.60 / 0.71 and a band floor of c = 0 − 0.04. Recommend replacing the band with this identity (±0.01) as the verdict: it ties the whole P(C,C) change to the P* block, which is the mechanism claim.

**Verdict 6 is safe** (checked at N = 1e4, c = 1e-2): FairBot and FB1 worlds under cert0 have no strict exits, neutral 4.85e-5 with ALLC 4.7e-5, "other" ≤ 1e-19; identical to c = 0. Note BTT (`BOX(THEM(THEM))`, π = 0.17 at c = 0) has a strict exit 5.2e-6 and BTT1 7.4e-4 to `not(BOX(THEM(ME)))` at c = 0 already; the driver's "top state" logic will pick FB/FB1, fine, but report BTT's exits too since it holds a quarter of the block.

**Verdict 4, c = 0 rival share [0.08, 0.20]**: chain data imply 0.13–0.15; fine.

**Class counts**: c = 0 471, lazy 610, cert0 585, certC 586; runtime comparable to lazy's (~85 s per 3e4 cell), 72 cells is ~40 min at 3 workers.

## 3. Missing controls

(a) **`mono`**: free iff y is constant, or y monotone in its atoms and cooperates with x (plus, for the cert0 version, y default-D and defecting on x). Prediction: equals cert0 cell-for-cell within 1e-3; if so, say "certificate = monotone box-positive program" in the paper.

(b) **`cert0-flat`**: cert0 free set, flat price c for every non-free check. Prediction: P* block survives at its c = 0 mass (rival share 0.13–0.15, P(C,C) ≈ c = 0, P* exits neutral ∝ 1/N). This is the decisive control for whether legibility or the ladder removes incumbency. Four cells (n = 8, c ∈ {1e-3, 1e-2}, N ∈ {1e4, 3e4}) suffice.

(c) **PrudentBot under cert0**: PB is monotone, ALLC-punishing, self-certifying, and in the FB block; its neutral exit is 1.0e-6 at N = 1e4 (50× stickier than FairBot, as the ratchet result found). Report π(PB) per cell: it is the universal ALLC-punisher that cert0 leaves free, and the natural comparison to P*.

## 4. Alternative explanations

- The "universal network" under cert0 is just the c = 0 chain restricted to the monotone sub-language (99% of prior mass): cert0 changes nothing among monotone pairs. A reader could say the experiment shows "deleting 1.3% of the prior" rather than a pricing effect. The flat control separates these.
- P*'s c = 0 mass comes from being 160× stickier than FairBot (no shadow, rare neutral neighbours), not from being a rival *network*; "rival networks" at c = 0 is a stickiness artefact of a three-member family.

## 5. For the program

Every mechanism that has beaten the shadow's 1/N exit so far is a moat (lazy incumbency, cliques) or a ratchet with rare neighbours (PB, P*), and cert0 deliberately removes the moat for the monotone block, so it cannot beat 1/N by construction; the brief says this. The useful general statement cert0 supports is narrower than "legibility": within the GL semantics, *monotone* programs' cooperation is self-certifying and only non-monotone cooperation can be priced without pricing entry. THEORY §9.2's realizable condition should be phrased in those terms.
