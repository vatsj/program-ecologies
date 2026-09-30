# Predictions: island-level selection on emigration (multilevel), 2026-09-30

Written and committed before any cell was run. The only executions so far are a smoke test and timing at
200–2,000 generations, whose outcomes were not inspected.

## Model

`src/islands.py` with two additions:
- **Mutation**, at ε per birth, drawing the offspring from μ over classes. εN = 0.1 mutants per island
  per generation.
- **Island-level selection.** A migrant's source island is drawn among the neighbours with probability
  proportional to exp(w_g · island mean payoff). w_g = 0 is the plain island model.

The rest: PD, weak L_6 with `ROLE`; 64 islands of N = 100 on a complete graph; w = 0.3 within islands;
mN = 1 migrant per island per generation. Every island starts all-D. The horizon is 5·10⁵ generations,
with statistics over the second half. w_g ∈ {0, 1, 3, 10}, 5 replicates each.

## Status of this run

- **Finite εN.** This is a finite-εN run: an approach rate and a mechanism test, not π of an ε→0 object
  (rule 5). First-half and second-half P(C,C) are both reported as a mixing check.
- **Why this approximates policy regret.** It is the island-level approximation to policy regret: islands
  whose programs do well in the long run export more.
- **Rule 3.** Islands are weighted by their own mean payoff, a group-level fitness. No deadweight-loss or
  efficiency criterion is applied. In the PD, island mean payoff and P(C,C) move together, so this sits
  close to rule 3. That is stated here, not hidden.

## Rough rates behind the verdicts

Per island per generation at εN = 0.1, using ρ at N = 100 and w = 0.3 from earlier results:
- **`THEM(^C)` island to faker by mutation:** 0.1 · 5·10⁻⁴ · 0.26 ≈ 1.3·10⁻⁵.
- **`THEM(^C)` island to shadow by drift:** 0.1 · 0.25 · 0.01 ≈ 2.5·10⁻⁴.
- **Shadow island to D by mutation:** about 6.5·10⁻³.
- **D island back to `THEM(^C)`:** about 0.04 per `THEM(^C)` migrant.

With w_g = 0, faker and D islands export as much as any other island. Fakers then spread by migration, at
ρ = 0.26 per faker migrant on a `THEM(^C)` island. With w_g ≥ 3, islands at payoff −1 export
e^(−3) ≈ 5% as much as cooperative islands. The mutation-borne exits remain, and the fast
D → `THEM(^C)` recolonization dominates the cycle.

## Verdicts

1. **w_g = 0 stays defective.** Second-half P(C,C) < 0.1 in every replicate.
2. **Monotone in w_g.** Mean P(C,C) increases with w_g. It is at least 0.5 at w_g = 3 and at least 0.7
   at w_g = 10.
3. **The exit mix flips.** At w_g = 0, faker exits from `THEM(^C)` islands outnumber shadow exits, since
   fakers arrive by migration. At w_g ≥ 3, shadow exits outnumber faker exits, since fakers arrive only by
   mutation. The rates above put this near 20:1.
4. **Mixed.** In every cell at w_g ≥ 3, first-half and second-half mean P(C,C) differ by less than 0.1.

**Falsifier.** Mean second-half P(C,C) < 0.2 at w_g = 3, meaning island-level selection does not rescue
the dilemma at this intensity.

**What each outcome would mean.** If 2 holds, selection between islands on long-run payoff overcomes both
obstructions:
- *the faker*, because exploited islands stop exporting;
- *the shadow*, because shadow islands are recolonized after D takes them.

The open question is then whether the needed w_g must grow with N or with the number of islands, which
decides whether this survives the limit. If the falsifier fires, within-island exits outrun
between-island selection at this w_g.
