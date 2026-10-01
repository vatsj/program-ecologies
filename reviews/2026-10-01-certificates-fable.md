# Review of `predictions/2026-10-01-certificates.md` by Fable (Claude subagent), before the run

Astra's points are not repeated. Where I disagree with astra I say so.

## 1. Design flaws and fixes

1. **The run is foreordained by the static estimate.** `--static` at n = 6, N = 100 gives tag 1.0000 / lfp 0.0171 / gfp 0.1285 / lob 0.1292, the declared smoke test to four digits. With `eager_poly=False` (verified exact for M0) and every exit in gfp/lob/lfp either pure dominance or neutral drift, the chain cells add no polymorphic states. Verdicts 1, 3, 5 (bullets 1, 3, 4), 6, 7's magnitudes and 9 are the static table restated; the tag arm is the priced arm's clique again (exits `other` only, 9·10⁻⁹ at N = 100, closed at N ≥ 10³). Fix: present the static table as *the* prediction and the cells as validation; put the content in the two ablations below, which the static machinery computes in seconds.
2. **Verdict 8's falsifier fires statically at n = 10.** Over all self-cooperating classes, 757 (a, faker) pairs exist, and 43 are loop-only in the brief's own sense (lfp says a defects on q): 323 at n = 11. Witness: `IMP(THEM(THEM))` ← `not(IMP(THEM(^IMP(THEM(ME)))))`, μ 9.6·10⁻⁶. It cooperates with itself *because* gfp FairBot's self-loop is C-seeded, defects on TT, and TT cooperates with it; a strict invader with N-independent ρ. The smoke test showed 0 only because the witness has 8 nodes. Astra's worry is realised. Fix: restrict 8 to FairBot (the mirror theorem) and state the compound part as a bound, loop-only flux ≤ 3% of total faker flux (π(TT)·9.6·10⁻⁶·ρ against π(TT)·4.2·10⁻⁴·ρ). Note that `faker_flux_loop_only` reads lfp at gfp class representatives; classes are gfp-behavioural, so members can differ in lfp.
3. **Tag equivalence lacks the equality axioms.** `and(EQ(ME),not(EQ(^C)))` is treated as inequivalent to `EQ(ME)` because EQ(ME) and EQ(^C) are independent atoms, though EQ(^A) ∧ EQ(^B) is unsatisfiable for A ≢ B. The extra cliques with μ ≈ 10⁻⁴ each (support at N ≥ 10³) are this artefact, and verdict 2's falsifier ("mutually cooperates with another conditional cooperator") can flip on a one-line change to the equivalence. Say which equivalence is meant and why.
4. **`static()` reports the wrong world for lfp.** `fb_name('lfp')` is `IMP(THEM(ME))`, which defects on itself, so the printed lfp "mutants in the all-main world" and ρ(main|D) = 0.01 describe a non-cooperator; the brief's `IMP(THEM(^C))` numbers (faker 6.4·10⁻⁴, neutral 4.9·10⁻³, led by `IMP(THEM(^D))`) are right, and I reproduce them. The cell's `FB` block has the same issue.
5. Fallback consistency (astra's worry), quantified: 8 settled entries at n = 10 (77 at n = 11) violate the fixed-point equation after the D fallback, μ×μ 1.6·10⁻¹⁰. Negligible; report it and move on.

## 2. Predictions likely to be wrong

- **Verdict 8 fails as written** (above).
- **Verdict 7's interpretation, "a stronger reader is more exploitable through its probe", is wrong.** The natural intermediate exists in `modal.py`: `kinds=((0,1),)`, PA + Con(PA). Its TT has fakers of total μ 1.2·10⁻⁶ (lob 3·10⁻⁷, gfp 4.5·10⁻⁴), `not(BOX1(THEM(^C)))` cooperates with itself but TT1 still defects on it, and the static chain gives 0.137 / 0.319 / 0.583 / 0.706, equal to lob. The contrast is truth versus provability: the faker's self-cooperation rests on a negative fact about ALLC, which no consistent reader proves and which C-seeded truth simply sees. Strength moves the faker mass by 4×, truth by 10³×.
- Verdict 7's magnitudes hold (static gap 0.13; ratio 0.13; slopes 0.34 / 0.48). Verdict 6's 21-of-24 holds; at n = 11 it is 46 of 51.

## 3. Missing controls

- **TT-faker suppression ablation** (astra asked; here is the number). Zeroing the faker edges out of `IMP(THEM(THEM))` in the gfp static chain gives 0.137 / 0.318 / 0.584 / 0.707, equal to lob's 0.138 / 0.319 / 0.584 / 0.706 at every N; π(TT) goes 0.06 → 0.35. I disagree with astra: the probe channel is the entire gap, exactly. Make this verdict 7's mechanism test, with falsifier "ablated gfp differs from lob by more than 0.02".
- **The BOX1-only arm** as the reader-strength control for 7's interpretation (one line of existing code).
- **Tag with equality axioms** in the equivalence, to see whether "parochial" survives.

## 4. Alternative explanations

- "Fakeable" in gfp is not dishonesty. `not(IMP(THEM(^C)))` honestly declares "I cooperate iff you defect on ALLC"; TT's probe is simply a bad test, as `THEM(^C)` was in the weak arm. The result says something about probes, not about certificates.
- gfp FairBot's universality is the mirror identity u(FB, y) = u(y, FB), so "cooperates with every cooperator that cooperates with it" is a tautology; the exceptions are programs that defect on it. The content is that the mirror is expressible at 3 nodes with neutral entry.
- The lob FairBot's non-mirror pairs (18 opponents, μ 1.9·10⁻³) are one-way exploitation *by* FairBot; they add nothing to the gap, which the ablation locates entirely in TT.

## 5. Beyond this experiment

- The gfp arm shows the modal result is not about provability: any semantics in which a short self-referential program is outcome-symmetric and defects on D meets both §9.2 conditions. State the characterization that way (outcome symmetry ⇒ no faker; defect on D ⇒ neutral entry), with Löb, coinduction and self-recognition as three ways of buying symmetry: unique fixed points, a selection rule, or parochialism.
- The three ways differ in runtime, which THEORY §9 item 11 named as the open selector and which this arm, free of compute, cannot rank. Certificate reading is the cheap route; the natural next cell is lazy pricing on the gfp arm, where cost incumbency against strangers (priced arm, n = 8) meets a universal mirror.
- The paper should say that the C-seeded loop is the "trust by default" that Löb's theorem licenses without a rule, and that the price of seeing truth is the probe. The witness in point 2 is the "forced-cooperate" objection in its smallest form.
