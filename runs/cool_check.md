# Cool check: payoff dispersion per island vs migration rate (chicken_norole without ROLE, complete graph, programs seeding, rep 0, 50000 generations, second half)

spread = agent-weighted SD of payoff on an island (0 iff cool); resident range = max - min payoff over classes with >= 5% of the island; load = payoff(smallest mN) - payoff(mN) at the same N; cool = share of island-samples with spread 0.

| N | I | mN | spread | resident range | cool | mean payoff | load | P(Swerve,Swerve) | frozen at | within-run corr(spread, payoff) |
|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 64 | 0.01 | 0.000 | 0.000 | 1.00 | 0.000 | 0.000 | 1.000 | 11380 | nan |
| 100 | 64 | 0.03 | 0.059 | 0.158 | 0.68 | -0.062 | 0.062 | 0.897 | - | -0.68 |
| 100 | 64 | 0.1 | 0.161 | 0.343 | 0.00 | -0.414 | 0.414 | 0.399 | - | -0.19 |
| 100 | 64 | 0.3 | 0.236 | 0.670 | 0.02 | -0.289 | 0.289 | 0.550 | - | -0.46 |
| 100 | 64 | 1 | 0.267 | 0.771 | 0.00 | -0.342 | 0.342 | 0.478 | - | -0.40 |
| 100 | 64 | 3 | 0.182 | 0.492 | 0.00 | -0.194 | 0.194 | 0.676 | - | -0.37 |

N = 100: Spearman(spread, load) across mN = 0.66

| 400 | 16 | 0.01 | 0.142 | 0.418 | 0.00 | -0.348 | 0.000 | 0.436 | - | -0.19 |
| 400 | 16 | 0.1 | 0.142 | 0.417 | 0.00 | -0.348 | -0.000 | 0.436 | - | -0.21 |
| 400 | 16 | 1 | 0.142 | 0.416 | 0.00 | -0.350 | 0.002 | 0.435 | - | -0.26 |

N = 400: Spearman(spread, load) across mN = -0.50

