# Predictions: does the ε = 0 absorption lottery concentrate as the island count grows? 2026-09-30

Written and committed before the run.

## Design

PD, weak L_6 with `ROLE`, no mutation, complete graph, N = 100, w = 0.3, mN ∈ {0.1, 1}.
I ∈ {16, 64, 256, 1024} with {100, 100, 40, 10} replicates per mN. Horizon 2·10⁴ generations, stopping at
freeze.

**Seeding law, iid.** Each slot is drawn independently from the uniform law over programs, so class
weights are proportional to class sizes. The earlier "every program at least once" seeding needs
I·N ≥ 3,994 slots and cannot be used at I = 16. Under iid seeding, every program is present with high
probability once I·N ≫ 3,994 · ln 3,994. That holds for I ≥ 256 only.

End states are classified as:
- **cooperative:** frozen with P(C,C) = 1;
- **mutual defection:** frozen with every pair at (D,D);
- **other frozen:** exploitation probes and the like;
- **live:** not frozen at the horizon. Live runs are classified by their final global P(C,C) and payoff.

## Hypothesis

At I = 64 the process was extinction-driven. Classes went globally extinct within about 10³ generations,
before any mean-field time average formed, which is why the migration game mispredicted. As I grows, a
class's global copy number grows proportionally and extinction slows. The metapopulation should then
follow the migration game's replicator dynamics, the zero-sum game ρ − ρᵀ, for longer. That game's
equilibrium set is entirely mutual defection, and `THEM(^C)` lies outside it.

## Verdicts

1. **Cooperation vanishes as I grows.** The share of runs ending cooperative falls with I at both mN, and is
   below 0.05 at I = 1024.
2. **Exploitation probes vanish too.** The "other frozen" share falls with I. Mutual defection, frozen or
   live with P(C,C) < 0.1, rises and is at least 0.8 at I = 1024.
3. **Concentration.** At I = 1024 at least 90% of runs end in one family, namely mutual defection.
4. **Slower freezing.** The median freeze generation increases with I. Some I = 1024 runs may be live at
   2·10⁴; they are classified as above.
5. **The lottery at I = 64.** Cooperative share 0.1–0.3, consistent with the earlier 17.5% under different
   seeding.

**Falsifier of concentration.** No family holds at least 70% of runs at I = 1024.

**Falsifier of the direction.** The cooperative share at I = 1024 exceeds its value at I = 64. That would
mean seeding abundance favours `THEM(^C)`, by keeping enough copies alive to outlast the fakers.

**What each outcome would mean.**
- *If 1–3 hold:* the ε = 0 island model has a canonical I → ∞ answer. That answer is the migration game,
  and in the PD it is inefficient. Without mutation, more islands make the dilemma worse, not better.
- *If the lottery stays spread:* ε = 0 has no canonical answer, and the seeding law remains a free prior.
