# Review of `predictions/2026-10-01-price-scaling-path.md` by fable

(Saved from the fable subagent's report. Lightly condensed. All numbers and claims are as reported.)

Checked by reading `chain.py` (`fixation`, `replicator`, `_polish`, `Chain.fates`), `modal.build_priced`,
`priced_limN.cell` and `scaling_path.py`, and by short static computations against the real n = 6 provider.

*Disclosure:* to diagnose the numerics item, fable ran seven n = 6 grid cells of this experiment through
`priced_limN.cell`, with and without a one-line diagnostic patch:
- α = 1 at N = 3·10⁴, 10⁵ and 3·10⁵;
- α = 0.75 at 10⁵;
- c0 = 10⁻³ at 10³, 10⁴ and 10⁵.

## 1. Design flaws and fixes

1. **The chain is wrong at small c, and the 1% polymorphic flag cannot see it.**
   - *The bug.* `replicator` returns status 2 ("near rest") at the *initial* point whenever the mutant's payoff gap
     is below `polish_thresh = 1e-3`. `_polish` then projects onto any equal-fitness point within 1e-2, with no
     stability check. For a FairBot mutant in all-D, that point is the *unstable* separatrix x* = 2c/(1+c).
     `Chain.fates` accepts it and emits a polymorphic target {D: N−2cN, FB: 2cN} with kstar = 2cN.
   - *Where it fires.*
     - α = 1 for N ≥ 3·10⁴ (kstar = 20);
     - α = 0.75 for N ≥ 10⁵;
     - the whole c0 = 10⁻³ path for N ≥ 10³;
     - it reproduces the existing suspect cell exactly (c = 10⁻³, N = 10³: poly {D 0.998, FB 0.002}, kstar = 2).
   - *Why it matters.* The polymorphic state is a stepping stone over the barrier: its inflow is about 1/(2cN), far
     above θ, so it is expanded, and from there the cooperative family is reached at O(1).
   - *Full-chain values, unpatched:*
     - α = 1: 0.920 / 0.975 / 0.992 at N = 3·10⁴ / 10⁵ / 3·10⁵, with polymorphic π 9.5e-3 / 3.0e-3 / 1.0e-3;
     - c0 = 10⁻³: 0.926 at 10⁴, with polymorphic π 2.3e-2;
     - α = 0.75: 0.742 at 10⁵, with polymorphic π 1.1e-2.

     Three of these pass the 1% flag and sit above the free arm at the same N.
   - *With `_polish` disabled:*
     - α = 1: 0.426 / 0.577 / 0.704;
     - c0 = 10⁻³: 0.476 at 10⁴;
     - α = 0.75: 0.302 at 10⁵;
     - suspect cell: 0.3095.

     All have zero polymorphic mass. The brief's two-edge predictions for those cells are 0.42 / 0.56 / 0.68, 0.47,
     0.28 and 0.31. So the predictor is right and the chain is not.
   - *Fix.* In `Chain.fates`, if the first replicator call ends at an interior point that is not attracting, take
     the "q died at first order" branch. After the fix:
     - require polymorphic π < 1e-4;
     - report `cut_flow` and `near_closed`;
     - check the hard bound P_c(N) ≤ P_0(N) cell by cell.
   - *Tolerances that are fine.*
     - `fit_tol` is dead.
     - `rest_tol = 1e-8` is on the payoff gap, and the minimum gap on this grid is 3.3e-5.
     - `is_neutral` at 1e-7, the provider merge at 9 decimals and the strict/neutral split at 1e-12 are safe.
     - Only `polish_thresh = 1e-3` is unsafe; it is above c on 19 of the 44 cells.
2. **Verdict 1's mechanism bullet is wrong by the brief's own predictor.**
   - Along α = 0.25 the barrier exponent 2wc²N is 0.19 / 0.33 / 0.60 / 1.04 at N = 10⁴ / 3·10⁴ / 10⁵ / 3·10⁵, not
     "below 0.3".
   - The predicted log-odds slope over [10⁴, 3·10⁵] is −0.61: ladder −0.75, free arm +0.45, entry −0.32.
   - Replace the bullet with per-path slope predictions that include entry.
3. **The mechanism falsifier is unfalsifiable.** The strict/neutral exit ratio is w·c_N·N = 17–216 along α = 0.25,
   so it holds by construction.
4. **Family entry is not FairBot's.** The three `BOX1` variants pay 3c against D, so their barrier exponent is 2.25×
   FairBot's.
   - Along α = 0.25 at N = 10⁵ / 3·10⁵, family weighting gives 0.0099 / 0.0038, against 0.0137 / 0.0060 FairBot-only.
   - Along α = 0.5 the correction is a constant −7%; at α ≥ 0.75 it is negligible.
   - State both numbers.
5. **Odds against P(C,C).** 0.80 and 0.87 are P(C,C), so only the wording needs fixing. The free arm's local
   exponent is rising (0.43 → 0.48), and extrapolating with the last segment gives 0.81 / 0.88.

## 2. Predictions likely wrong

- **If run unpatched,** verdicts 3–5 fail upward, as in item 1 above.
- **Verdict 1** may come in at about 0.039 / 0.022 / 0.010 / 0.004, with a slope of −0.61 to −0.70.
- **Verdict 2's −0.06 slope** becomes −0.02 with the local β = 0.48.
- **α = 1's constant factor holds.**
  - The exit ratio is exactly (1−e⁻³)/3 = 0.317.
  - The entry ratio is 0.915–0.984 at 10⁴–3·10⁵.
  - Their product is 0.29–0.31.
  - Astra is right that P(C,C) → 1 along α = 1 regardless.
- **Self-play claim correct.** The constant at c = 0.1 is exp(w·2c). Self-play flips FairBot's sign only when
  c < 1/(2N).

## 3. Missing controls or cheap additions

1. Per-path slope falsifiers over [10⁴, 3·10⁵]: about −0.61 / −0.05 / +0.24 / +0.47 for α = 0.25 / 0.5 / 0.75 / 1.
   d(slope)/dα ≈ 1 is a one-parameter test of the ladder exponent.
2. A barrier path, c0 = 0.03 and α = 0.25 at N ≤ 10⁵, where the exponent goes 0.54 / 1.7 / 5.4.
3. Report the two edges per cell (family Σμρ entry, ALLC exit).
4. Re-run the suspect cell with the fixed chain as the acceptance test (expected 0.31), and add a RESULTS addendum.
5. Run the free-arm extension first and re-issue the predictor, keeping the original for scoring.

## 4. Alternative explanations

- **Hard bound as an artifact detector.** Pricing can only lower entry and raise the ALLC exit, so P_c(N) ≤ P_0(N)
  holds within the two-edge model.
- **The +4–7% residual** of the patched chain over the FairBot-only predictor at α ≥ 0.75, N ≥ 10⁵, comes from the
  free arm's rising local exponent.
- **Two family members have fakers at c = 0.** They are entered only by neutral drift, at about +1% on the ALLC exit,
  so they are not a confound at n = 6.
- **Continuity at c = 0.** Both edges are continuous in c and the recurrent structure does not change. The only
  discontinuity is the polish bug.

## 5. Beyond this experiment

Conjecture D's "iff" is a proposition about the two-edge reduction with explicit fixation integrals:
- the barrier boundary, α = 1/2, comes from c²N;
- the ladder boundary, α = 1 − β, comes from entry N^(−1/2) against exit max(wc, 1/N).

The two 1/2's coincide for different reasons. The empirical content is (i) β → 1/2 and (ii) the reduction holding at
larger n. Carry it in THEORY as a proposition with this experiment as its check.
