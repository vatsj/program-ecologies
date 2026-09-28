# Predictions: are islands "cool" (equal payoff among present programs)? 2026-09-28

Written and committed before the run. Motivation: the conversation of 2026-09-28. The claim is that in the
limit every program on an island earns the same against that island's population. THEORY §5 calls such
states cool. The island can then be aggregated into a mixed strategy over programs.

## Design

`src/islands.py` with per-island payoff-dispersion logging. Chicken without `ROLE` (L_6, 46 classes),
programs seeding, complete graph, w = 0.3, no mutation, replicate 0 only, 5·10⁴ generations, statistics
over the second half.
- N = 100, I = 64 at mN ∈ {0.01, 0.03, 0.1, 0.3, 1, 3} migrants per island per generation.
- N = 400, I = 16 at mN ∈ {0.01, 0.1, 1}. That keeps 6,400 slots.

Per island and sample:
- **spread**, the agent-weighted SD of payoff, √(Σ_k x_k (f_k − f̄)²). It is zero iff the island is cool.
- **resident range**, max − min payoff over classes holding at least 5% of the island.
- **mean payoff** f̄.

**Migration load** at mN is payoff(mN = 0.01) − payoff(mN), at the same N.

## Why I expect a floor, not zero, at fixed N

Near the mixed equilibrium, h* = 2/11 of the island plays Straight. The payoff gap between Straight and
Swerve players is 2 − 11h, so it moves 11 payoff units per unit of h. The restoring rate is
λ = w·h*(1 − h*)·11 ≈ 0.49 per generation. Moran drift adds variance of about 2h(1 − h)/N per generation.
The stationary SD of h is therefore about √(h(1 − h)/(Nλ)) ≈ 0.055 at N = 100. That gives a payoff-gap SD
of about 0.6 and a spread of about 0.39 × 0.6 ≈ 0.2 on islands holding Straight players. Islands that
have lost them are all-Swerve with spread 0, so the cell mean is lower. The floor should scale like
N^(−1/2). The claim "spread → 0 as m → 0" should then hold only in the joint limit, m → 0 and then N → ∞.

## Verdicts

1. **Spread rises with migration.** At N = 100 the cell-mean spread increases with mN across the six
   rates. At most one adjacent pair may invert, and only by less than 0.01.
2. **A drift floor.** At N = 100 and mN = 0.01 the mean spread lies in [0.05, 0.3], not near 0. At
   mN = 0.01 the ratio of the N = 400 spread to the N = 100 spread lies in [0.35, 0.7], against 0.5 for
   N^(−1/2).
3. **Spread tracks load.** At N = 100 the load is non-decreasing in mN, and the Spearman correlation between
   mean spread and load across the six rates is at least 0.9.
4. **Level.** At mN = 0.01 and N = 100 the mean payoff is within 0.05 of −2/11 = −0.182. The exception is
   the case where Straight players are lost globally and the run freezes at mutual Swerve (payoff 0,
   spread 0), which will be reported as such.

**Falsifier of the floor claim (2).** Mean spread ≤ 0.02 at N = 100 and mN = 0.01 with Straight players
still present. That would mean islands are cool at finite N, and the simple claim holds without N → ∞.
