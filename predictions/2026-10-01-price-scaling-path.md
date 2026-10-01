# Predictions: price scaling paths c_N = c0·(N/10³)^(−α), 2026-10-01

Status: reviewed by astra (`reviews/2026-10-01-price-scaling-path-gpt-6-astra.md`) and fable
(`reviews/2026-10-01-price-scaling-path-fable.md`), then revised; changes are marked [after review]. Committed before
the sweep.

**Executions before this commit.**
- The static single-edge rates quoted below.
- [after review] Fable's diagnosis. Fable ran seven n = 6 grid cells through `priced_limN.cell`, with and without a
  diagnostic patch, and found a chain bug:
  - `replicator` polishes onto an *unstable* equal-fitness point when the mutant's payoff gap is below 10⁻³;
  - `Chain.fates` accepted that separatrix as a target, which made a polymorphic stepping stone over the cost
    barrier.

  The fix is commit a49a007. A polished interior point reached from 1/N that is not attracting is now a barrier.
  Acceptance: the old suspect cell goes from 0.83 to 0.3095, which matches this predictor's 0.31, and c = 0 and
  c = 10⁻² cells reproduce exactly. All runs here use the fixed chain. Fable's patched-chain values for the seven
  cells are quoted where they apply. They were seen before this commit, so those verdicts are checks, not blind
  predictions.

## Motivation

At fixed c > 0, atom pricing kills well-mixed cooperation in the limit (RESULTS "Priced arm"). There are two
mechanisms:
- an entry barrier, with exponent about 2·w·c²·N for FairBot, which pays 2c against D;
- the price ladder: ALLC strictly invades FairBot with ρ ≈ w·c.

The RS proposed taking the price to zero before the size goes to infinity, as lim_N lim_c, with programs also
playing themselves.

**The iterated limit is the free arm.** At fixed N every fixation probability is continuous in c. All are positive,
so the explored chain is irreducible and π is continuous in c. [after review] Fable checked that the recurrent
structure does not change at c = 0, so the inner limit returns the c = 0 chain at every N.

**Self-play is not the lever.** It gives a lone reciprocator (R − P)/N, which is Hamilton's rule with r = 1/N. Static
check: ρ(FairBot | all-D) changes by
- +4% / +1.3% / +0.4% at c = 0 and N = 10² / 10³ / 10⁴;
- +4% / +1.6% / +0.7% at c = 10⁻²;
- +6.5% / +5.6% / +5.6% at c = 10⁻¹.

[after review] The constant at c = 10⁻¹ is exp(w·2c), a one-copy shift. Self-play flips FairBot's sign against all-D
only when (R − P)/N > 2c, which is beyond α = 1, where the barrier is already gone. It is not run.

**The informative object is a joint limit along a path.** Take c_N = c0·(N/10³)^(−α).
- Entry: ρ(FB | D) ≈ N^(−1/2) · exp(−O(c²N)).
- Exit: ρ(C | FB) ≈ max(w·c_N, 1/N).

**Proposition D** [after review: restated]. In the two-edge reduction, cooperation tends to 1 along the path iff
α > 1/2. The proposition rests on two boundaries:
- *Barrier boundary.* α = 1/2, from c²N, the Gaussian width of the neutral fixation sum. The barrier kills entry when
  c²N → ∞.
- *Ladder boundary.* α = 1 − β, where β is the free arm's odds exponent: entry ~N^(−β) against exit ~w·c_N.

Both equal 1/2 when β = 1/2, but for different reasons. Since the reduction is explicit fixation integrals, the
empirical content is two-fold:
- (i) β → 1/2 in the free arm;
- (ii) the full chain follows the reduction along shrinking-price paths.

This experiment checks (ii) and extends (i).

[after review] I previously said "a neutral lineage reaches about √N copies". That is wrong as a statement about
typical lineages: neutral gambler's ruin gives reach-k probability 1/k (astra). √N is where the accumulated
selection in the fixation integral becomes order one.

Odds below mean P(C,C)/(1 − P(C,C)). [after review: the earlier wording mixed odds and probabilities.] The free arm's
measured odds exponent over N ∈ [10³, 3·10⁴] is 0.44, rising locally from 0.43 to 0.48.

## Predictor (calibrated)

odds_c(N) = odds_free(N) × [ρ(FB | D)_c / ρ(FB | D)_0] × [ρ(C | FB)_0 / ρ(C | FB)_c], using exact single-edge fixation
from `chain.fixation`.

Check against the four existing atoms cells at n = 6, c = 10⁻²:

| N | predicted | measured |
|---|---|---|
| 10² | 0.140 | 0.137 |
| 10³ | 0.111 | 0.116 |
| 10⁴ | 0.0150 | 0.0150 |
| 3·10⁴ | 0.0023 | 0.0019 |

The fixed chain gives 0.3095 at the old suspect cell, against a predicted 0.31.

For N > 3·10⁴, the free arm's P(C,C) is extrapolated from a power-law fit of its odds over 10³–3·10⁴: 0.80 at
N = 10⁵ and 0.87 at 3·10⁵. [after review] The free-arm extension cells run first. An *updated* predictor using
their measured values is reported separately; the verdicts are scored against the values below.

[after review] FairBot-only against family-weighted entry. The n = 6 cooperative family has six members. The three
`BOX1` variants pay 3c against D, so their barrier exponent is 2.25× FairBot's. Family-weighted entry lowers the
prediction where the barrier is non-negligible, mainly along α = 0.25 and c0 = 0.03. Both numbers are given there.

## Design

- **Chain:** ε→0, PD, w = 0.3, atoms pricing, `eager_poly=False`, fixed chain (a49a007). At n = 6, atoms pricing is
  identical to depth pricing.
- **Driver:** `src/scaling_path.py`.
- **Grid:** N ∈ {10², 10³, 10⁴, 3·10⁴, 10⁵, 3·10⁵}.
- **Paths at n = 6:**
  - c0 = 10⁻², α ∈ {0.25, 0.5, 0.6, 0.75, 1, 1.5} [after review: 0.6 and 1.5 added, astra];
  - α = 0.5, c0 ∈ {10⁻³, 10⁻¹};
  - [after review] a barrier path, c0 = 3·10⁻², α = 0.25, at N ≤ 10⁵ (fable). It is the only path where c²N grows
    past order one, so it tests the barrier half of the boundary directly.
- **Checks:**
  - c0 = 10⁻², α = 0.5 at n = 8;
  - c = 0 at n = 6 for N ∈ {10⁵, 3·10⁵}.
- **Reported per cell:**
  - P(C,C), π(all-D), π(all-FairBot), π(all-ALLC);
  - polymorphic π, cut flow, near-closed classes;
  - FairBot exits, split into strict and neutral;
  - terminal classes and support;
  - [after review] the two edges themselves: family entry Σ μ_q ρ(q | D) over self-cooperating classes, FairBot-only
    entry, and the ALLC exit μ(C)·ρ(C | FB). This checks the reduction on rates, not only through P(C,C).
- **Artifact detectors** [after review: these replace the 1% polymorphic flag]:
  - polymorphic π must be below 10⁻⁴;
  - P_c(N) ≤ P_0(N) at the same N and n, cell by cell. Pricing here can only lower entry and raise the ALLC exit,
    and the family's internal neutrality is unchanged, so a priced cell above the free arm is a numerics signature.

  A cell that violates either is reported and makes its path's verdict indeterminate. It is not silently excluded
  (astra).

## Verdicts

Predicted P(C,C) values are listed at N = 10² / 10³ / 10⁴ / 3·10⁴ / 10⁵ / 3·10⁵.

1. **α = 0.25 declines** (c0 = 10⁻²).
   - FairBot-only prediction 0.12 / 0.11 / 0.046 / 0.028 / 0.014 / 0.006; family-weighted about
     0.039 / 0.022 / 0.010 / 0.004 from N = 10⁴. Each cell lies within ±30% of the interval between the two.
   - It is monotone decreasing from N = 10³.
   - [after review] The decline is ladder plus barrier: 2wc²N rises 0.19 / 0.33 / 0.60 / 1.04 over 10⁴–3·10⁵. The
     earlier "barrier below 0.3" bullet was wrong, and the "strict share of exits" falsifier is dropped because it
     holds by construction (fable).
2. **α = 0.5 is nearly flat** (c0 = 10⁻²). Predicted 0.091 / 0.111 / 0.100 / 0.098 / 0.091 / 0.086.
   - Every cell at N ≥ 10³ lies in [0.06, 0.15].
   - Flatness here is the β ≈ 0.45–0.48 window, not a boundary shift.
3. **At α = 0.5 the plateau is set by c0.**
   - c0 = 10⁻³: 0.16 / 0.31 / 0.47 / 0.54 / 0.55 / 0.55, each within ±25%. Fable's patched cells, seen before this
     commit, gave 0.31 / 0.48 / 0.58 at 10³ / 10⁴ / 10⁵.
   - c0 = 10⁻¹: below 0.005 at every N ≥ 10³, with a constant barrier exponent of about 6.
4. **α = 0.75 rises** (c0 = 10⁻²). Predicted 0.056 / 0.111 / 0.18 / 0.23 / 0.28 / 0.33, each within ±30%, monotone
   from 10³. Fable's patched cell at 10⁵ gave 0.30.
5. **α = 1 approaches 1, with a constant odds penalty** (c0 = 10⁻²).
   - Predicted 0.023 / 0.111 / 0.29 / 0.42 / 0.56 / 0.67, each within ±30%, monotone. Fable's patched cells gave
     0.43 / 0.58 / 0.70 at 3·10⁴ / 10⁵ / 3·10⁵.
   - Its odds are 0.31 ± 0.1 of the free arm's at N ≥ 10⁴. Along α = 1, w·c_N·N = 3, so the exit ratio is
     (1 − e⁻³)/3 = 0.317 at every N.
   - [after review] This does not stop P(C,C) → 1, it lags (astra). Only α > 1 converges to the free arm in odds.
6. **α = 1.5 converges to the free arm** [after review]. Predicted 0.000 / 0.111 / 0.47 / 0.65 / 0.78 / 0.86. At
   N ≥ 10⁵ it is within 0.03 of the free arm, and its odds ratio to the free arm rises toward 1.
7. **α = 0.6 rises slowly** [after review]. Predicted 0.077 / 0.111 / 0.13 / 0.14 / 0.15 / 0.16, each within ±30%.
   This is the finite-window crossover side, α > 1 − β.
8. **The barrier path collapses** [after review] (c0 = 3·10⁻², α = 0.25). FairBot-only prediction
   0.059 / 0.021 / 0.0027 / 0.0006 / <10⁻⁴. The entry ratio ρ_c/ρ_0 falls 0.61 / 0.36 / 0.097 / 0.027 / 0.0024 as
   2wc²N goes 0.17 / 0.54 / 1.7 / 3.0 / 5.4. Measured P(C,C) at 10⁵ is below 10⁻³.
9. **The free arm extends** (n = 6, c = 0). P(C,C) is 0.80 ± 0.05 at N = 10⁵ and 0.87 ± 0.05 at 3·10⁵.
10. **n = 8 matches n = 6** at α = 0.5, c0 = 10⁻², within ±30% at every N.
11. **The slopes come out as the reduction says** [after review, fable].
    - Fitted log-odds slopes over [10⁴, 3·10⁵], within ±0.15:
      - −0.61 for α = 0.25 (−0.70 family-weighted);
      - −0.05 for α = 0.5;
      - +0.24 for α = 0.75;
      - +0.47 for α = 1.
    - Across the c0 = 10⁻² paths with 0.5 ≤ α ≤ 1, d(slope)/dα is in [0.8, 1.2]. This is a one-parameter test of
      the ladder exponent.

## Falsifiers

- *Of the reduction holding along shrinking-price paths:*
  - any path's slope outside its ±0.15 window in verdict 11;
  - d(slope)/dα outside [0.8, 1.2];
  - the measured edge rates deviating from the static ones by more than 2× at any cell.
- *Of the barrier half:* the barrier path above 10⁻³ at N = 10⁵.
- *Of the boundary's location:* the α = 0.75 or α = 1 path not increasing over [10⁴, 3·10⁵], or the α = 0.25 path not
  decreasing over that range.
- *Artifact detectors:* any cell above the free arm at the same N, or polymorphic π ≥ 10⁻⁴, is reported and makes
  that path indeterminate.

## What it would mean

- **If the reduction holds,** efficiency in the limit is compatible with a positive compute price that vanishes
  faster than N^(−1/2) of the stakes. lim_N lim_c is the trivially safe end of this, and α = 1/2 is the knife edge.
  At these N the ladder half binds first, and the barrier half kills cooperation exponentially below 1/2.
- **Self-play** adds one copy's worth of advantage and does not move the boundary.
- **Pricing's reach is limited.** A price large enough to matter in the limit (α ≤ 1/2) destroys universal provers
  unless an exemption removes the ladder. Experiments A and B test those exemptions.
