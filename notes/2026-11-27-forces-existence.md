# Existence of the leader-value core in terms of "forces" (2026-11-27)

Influence function (the RE's proposal): after a commitment a_S the followers' profiles are linked by strictly
improving moves of follower coalitions; a *sink* is a minimal nonempty set closed under those moves; S forces
a_S × K for each sink K (and supersets). A strong Nash profile of the followers' game is a one-point sink.
Core: x is dominated if some S forces a set every outcome of which every member of S strictly prefers to x.

Claims to check on random games (`src/lvc_forces.py`), written before the run:
- C1 (two players): the core is nonempty iff some outcome gives each player at least the best payoff it can force.
  Falsifier: one game where the two disagree.
- C2 (Scarf): if the forcing powers are balanced, the core is nonempty. Falsifier: one balanced game with an empty
  core.
- C3: the converse of C2 fails for three players (some nonempty cores are unbalanced). Falsifier: none in 20,000.
- C4: with three players, a commitment that leaves the followers without a strong Nash profile is common (more than
  5% of games have one). Falsifier: under 5%.

## Results (`runs/lvc-forces.json`; payoffs uniform at random, seed 20261127)

| players × actions | games | core nonempty | balanced | balanced, core empty | nonempty, unbalanced | games with a commitment leaving no follower strong Nash profile |
|---|---|---|---|---|---|---|
| 2 × 3 | 20,000 | 16,376 | 16,376 | 0 | 0 | 0 |
| 3 × 2 | 20,000 | 16,067 | 5,006 | 0 | 11,061 | 13,320 |
| 3 × 3 | 2,000 | 1,522 | 370 | 0 | 1,152 | 1,908 |

C1 holds (the two conditions agree in all 20,000 two-player games). C2 holds (no balanced game with an empty core).
C3 holds: balancedness catches 31% (3 × 2) and 24% (3 × 3) of the nonempty cores. C4 holds: 67% and 95% of
three-player games have a commitment after which the followers have no strong Nash profile (5.8% and 7.3% of all
commitments).
