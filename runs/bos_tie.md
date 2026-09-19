# BoS tie-break (item 3)

games/bos.yaml is symmetric: player 2's table with A<->B relabelled equals player 1's, both constants earn 1.5 in self-play,
the classes all-A and all-B have 219 members each and identical mu (0.2490), and every exit from all-A has a mirror exit from all-B
with identical P (total 6.51e-4 at w=0.1, N=100).

What broke the tie (w=0.1, N=100, before the fix: all-A 0.713 / all-B 0.254): the only asymmetric edges were entries. All-A received
stationary flow 2.9e-4 from the polymorphic state {A 0.50, B 0.49, X 0.01} via the mutant `ROLE` (mu 0.19, rho 0.34), and all-B had no
mirror source. That state is the 50/50 A/B polymorphism after a coin mutant enters (49.5/49.5/1 agents): largest-remainder rounding to the
1/N grid broke the exact 49.5 vs 49.5 tie by type index, always giving A the extra agent, and from 50/49 the replicator + `ROLE` tips to all-A.
So the tie-breaker was the grid rounding, not the game, the language or mu.

Fix (src/chain.py `grid_options`): a rounding tie is split into every tie-break with equal weight, as a neutral rest set already was.
Both tie states now exist ({A 0.50, B 0.49, X 0.01} and {A 0.49, B 0.50, X 0.01}) and pi is exactly symmetric.

| w | N | all-A | all-B | mean payoff | loss |
|---|---|---|---|---|---|
| 0.01 | 10 | 0.2081 | 0.2081 | 0.9682 | 0.5318 |
| 0.01 | 100 | 0.2922 | 0.2922 | 1.1113 | 0.3887 |
| 0.1 | 10 | 0.2378 | 0.2378 | 1.0300 | 0.4700 |
| 0.1 | 100 | 0.4832 | 0.4832 | 1.4744 | 0.0256 |
| 1 | 10 | 0.3877 | 0.3877 | 1.3105 | 0.1895 |
| 1 | 100 | 0.4966 | 0.4966 | 1.4990 | 0.0010 |

PD cells are unaffected (no exact ties arise there; strong n=6 N=100 w=0.1 all-D = 0.991 before and after).
