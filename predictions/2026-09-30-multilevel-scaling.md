# Predictions: does the multilevel threshold grow with island size or island count? 2026-09-30

Written and committed before the run.

## Design

Same model as `predictions/2026-09-30-multilevel.md`: PD, weak L_6 with `ROLE`, complete graph, w = 0.3,
every island starting all-D. Per-island rates are held fixed as size changes: εN = 0.1 mutants and mN = 1
migrant per island per generation. The horizon is 2·10⁵ generations, statistics over the second half,
3 replicates per cell. w_g ∈ {3, 6, 10, 15, 25}.

- **Size series:** N ∈ {50, 100, 200} at I = 64.
- **Count series:** I ∈ {16, 64, 256} at N = 100.

The threshold w_g* is where mean second-half P(C,C) crosses 0.5, interpolated linearly in log w_g. It is
reported as "> 25" if never crossed. This is a finite-εN run, so it measures approach rates and a mechanism,
not the ε→0 object.

## Why a growing threshold is expected

Island selection only changes how much each island exports. It can suppress faker and D islands, by
e^(−w_g) per unit of payoff deficit, but it cannot raise a cooperative island's export share above 1.

Two rates matter per island and generation:
- **Recolonization.** A D island is retaken at about mN × (share of `THEM(^C)` migrants) × ρ(`THEM(^C)` | D).
  That ρ falls like N^(−1/2), as the lim_N chain showed.
- **Mutation-borne faker entry** into a `THEM(^C)` island, at εN · μ(faker) · ρ(faker | `THEM(^C)`). This is
  N-independent, and w_g does not touch it.

So at fixed w_g, cooperation should fall with N, and w_g* should rise with N or leave the grid. Across
island counts on a complete graph, the per-island mean-field dynamics are unchanged. More islands only
reduce finite-I noise, so w_g* should be about flat in I.

## Verdicts

1. **Cooperation falls with island size.** At w_g = 10 and w_g = 15, mean P(C,C) satisfies N = 50 > N = 100
   > N = 200.
2. **The threshold rises with island size.** w_g*(N = 200) exceeds w_g*(N = 100) by at least one grid step,
   or is > 25. w_g*(N = 50) is below w_g*(N = 100).
3. **The threshold is flat in island count.** w_g* at I = 16, 64 and 256 agree to within one grid step.
4. **Mixing.** First- and second-half P(C,C) agree within 0.1 in every cell at N ≤ 100. At N = 200 this may
   fail, and that will be reported.
5. **Consistency.** At I = 64, N = 100, w_g = 10, the result reproduces the earlier 5·10⁵-generation value,
   0.75, to within 0.1.

**Falsifier of "the rescue does not survive the limit".** w_g* does not increase from N = 100 to N = 200, or
P(C,C) at w_g = 15 is at least as high at N = 200 as at N = 100.

**What each outcome would mean.**
- *If 1 and 2 hold:* multilevel selection is a finite-island-size rescue. In the limit it needs w_g → ∞ or
  migration that scales with N, which moves it from mechanism toward assumption.
- *If w_g* is flat in N:* island selection is a limit-robust route, and the next question is w_g's
  interpretation.
