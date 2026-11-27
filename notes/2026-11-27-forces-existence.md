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
