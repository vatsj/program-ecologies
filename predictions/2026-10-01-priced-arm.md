# Predictions: the priced arm (compute cost on checks), spatial structure, and cliques, 2026-10-01

Status: reviewed by astra (`reviews/2026-10-01-priced-arm-gpt-6-astra.md`) and fable
(`reviews/2026-10-01-priced-arm-fable.md`), then revised; changes are marked [after review]. Committed before any
run. Only static single-edge rates have been computed, and they are quoted.

## The arm (`src/modal.py: build_priced`)

**Pricing.** The modal arm, with a compute price on proof search.
- A program pays c per essential box atom per Kripke world that its atom values take to settle against the
  opponent: cost(x, y) = c · k(x) · (1 + last-change world). Constants pay nothing.
- FairBot pays 2c against D (one world to discover D's defection) and c against itself.
- PrudentBot pays 4c against D and 2c against itself.
- This is a stand-in for proof-search cost. It is the "price on one's own compute" left open in THEORY §9.11,
  not the timeout form REJECTED.md rules out.
- [after review] Strictly, this is *semantic-stabilization pricing*: the last-change world is known in hindsight,
  not a stopping time an evaluator could observe. It is a proxy for search work, not a measurement of it.
- [after review] A uniform per-match tax on every program is exactly invariant under f = exp(w·payoff), since the
  shift cancels. So every effect here comes from *differential* cost, and a tax control would be identical to
  c = 0 by construction.

**Cliques (Exp 3 only).** m spellings of `eq(THEM,ME)`. Each cooperates iff the opponent is an exact copy, pays
c_eq = c per match, and gets prior mass μ(FairBot), since `eq(THEM,ME)` has FairBot's size of 3 nodes.

## Two predicted mechanisms

**(a) An entry barrier.** A lone conditional cooperator in all-D trails D by about its check cost. The barrier in
the fixation product is roughly N·w·c²/(2b), so at fixed c > 0, well-mixed entry vanishes exponentially in N.
Static values for ρ(FairBot | all-D) at w = 0.3:

| c | N = 100 | 10³ | 10⁴ | 3·10⁴ |
|---|---|---|---|---|
| 10⁻² | 0.039 | 0.010 | 1.4·10⁻³ | 2.2·10⁻⁴ |
| 10⁻¹ | 0.015 | 3·10⁻⁵ | 5·10⁻²⁷ | — |

**(b) A price ladder.** Programs that behave identically on the path are ordered by cost, and each cheaper one
strictly invades the dearer: PrudentBot → FairBot → ALLC, which pays nothing, → D. So the shadow exit stops
vanishing. ρ(ALLC | all-FairBot) is about w·c, an N-independent 3·10⁻³ at c = 10⁻², against 1/N when c = 0.

Combined statically, the cooperative-to-D ratio peaks and falls:
- c = 10⁻³: 0.045 / 0.125 / 0.137 / 0.078 at N = 10² / 10³ / 10⁴ / 3·10⁴;
- c = 10⁻²: 0.036 / 0.035 / 0.005 / 0.001.

**Cliques escape the ladder.** No cheaper program cooperates with a clique, and a clique defects on its shadow.
A clique world has neither a strict nor a neutral exit, only deleterious fixation, which is exponentially small
with exponent about N·w·(1 − c). Its entry barrier, N·w·c²/(2b), is far smaller. So in the ε→0 chain at fixed
small c, cliques should take the cooperative mass as N grows. They should do so even at c = 0: a clique world
has no shadow to drift into, while a FairBot world drifts to ALLC at 1/N.

## Exp 1: priced chain, well-mixed

ε→0 chain, PD, w = 0.3, n ∈ {6, 8}, N ∈ {10², 10³, 10⁴, 3·10⁴}, `eager_poly=False`. c ∈ {10⁻³, 10⁻²}, plus c = 0
once, and c = 10⁻¹ at N = 10² only.

[after review] Three pricing modes:
- **atoms:** the formula above.
- **depth:** a control without the atom multiplier, c·(1 + settle world) for any program with boxes. Fable showed
  the PrudentBot → FairBot rung exists only because of the multiplier.
- **lazy:** a lazy prover. Programs read off a best reply to a constant opponent (C or D) and to an exact copy of
  themselves at zero cost, and pay the atoms price only against other non-trivial programs. This is fable's
  proposed escape from the ladder. The short-circuit is on cost, not on cooperation. It partly re-opens the
  REJECTED Levin-complexity entry's warning about CliqueBot-shaped short-circuits: here the short-circuit saves
  compute but does not change whom the program cooperates with.

Static facts at c = 10⁻², n = 8, for maximum regret against the resident:

| mode | against FairBot | against PrudentBot |
|---|---|---|
| atoms | 0.01 (ALLC) | 0.01 |
| depth | 0.01 (ALLC) | 0 |
| lazy | 0 | 0 |

Under lazy pricing both are no-regret, and ALLC is a neutral shadow again. One cell was observed during a smoke
test before this commit: lazy, n = 6, c = 10⁻², N = 10² gave P(C,C) = 0.169, against 0.169 for the free arm at
n = 6.

1. **c = 0 reproduces** the modal arm exactly, by construction (fable checked).
2. **atoms: the curve peaks and falls** [after review: numbers from fable's family-level three-state estimate].
   P(C,C) within ±50% of:
   - c = 10⁻³: 0.17 / 0.36 / 0.39 / 0.27, peaking near 10⁴;
   - c = 10⁻²: 0.14 / 0.14 / 0.02 / 0.004.

   At N = 3·10⁴, at least 2× below c = 0.
3. **atoms: the ladder sets the exit.** At c > 0, strict cheaper-equivalent invaders take at least 0.8 of
   all-FairBot's exits at N ≥ 10⁴. Fable expects ALLC to be the only one, at 0.97–1.00.
4. **atoms: PrudentBot is irrelevant.** n = 8 is within ±30% of n = 6 at every c > 0 and N. [after review]
   This holds by prior and entry, μ(PB) = 1.4·10⁻⁶, not only by the ladder.
5. **depth.** n = 6 matches atoms n = 6 to within ±10%, since FairBot has one atom. At n = 8, depth is at least
   atoms at every N, and π(PrudentBot) under depth rises with N, but stays small at these N because of its μ.
6. **lazy: the free arm returns.** At both c > 0 and both n, P(C,C) is within ±0.05 of the c = 0 value at every
   N, and it rises monotonically.

   *Falsifier of the lazy escape:* lazy P(C,C) at N = 3·10⁴ below 0.5 at n = 8, or a peak.

## Exp 2: does structure rescue entry? (`src/graph_rates.py`)

Per-mutant *hitting probabilities* on graphs (ε-free) [after review: labelled as such]. ρ is the probability
that one mutant reaches half the graph, which is not fixation. Update rule: death-birth; a random site dies and
its neighbours compete with weight exp(w · their mean payoff over their own neighbours). The mean is used rather
than the sum, so hypercube degree does not change selection strength. Costs are included in payoffs. The mutant
is placed uniformly. Priced n = 8 matrix, c ∈ {0, 10⁻², 10⁻¹}. Graphs: torus with side
16 / 32 / 64, and hypercube with d = 6 / 8 / 10 (N = 64 / 256 / 1,024). The well-mixed reference uses the
fixation formula to N/2.

[after review] Sampling is adaptive: batches of 1,000 trials until at least 20 successes or 20,000 trials, with
95% Wilson intervals. Comparisons whose intervals overlap are reported as inconclusive. Conclusions are
restricted to these transitions; four pairwise rates do not determine stationary mass on graphs.
- **Entry:** ρ(FairBot | all-D) and ρ(PrudentBot | all-D).
- **Ladder:** ρ(ALLC | all-FairBot) and ρ(FairBot | all-PrudentBot), measured up to N = 1,024.

5. **The torus rescues entry.** At every c, ρ(FairBot | all-D) on the torus varies by at most 2× across sides
   16–64. At c = 10⁻¹ it is at least 10× the well-mixed value at N = 1,024 and N = 4,096. Nucleation is local, so
   the barrier is set by the neighbourhood, not by N.
6. **The hypercube is in between.** Its degree grows like log N, and entry falls with d more slowly than in the
   well-mixed population.
7. **Structure does not stop the ladder** [after review: threshold depends on c]. ρ(ALLC | all-FairBot) on the
   torus and hypercube, against the measured neutral baseline on the same graph (a 2×2 zero-payoff run, 4,000
   trials), at N ≥ 256:
   - at c = 10⁻¹, at least 3×;
   - at c = 10⁻², above the baseline. The constant-advantage approximation x/(1 − e^(−x)), with x = w·c·N/2,
     gives only about 1.2× at N = 256.

   So spatial structure fixes entry but not the shadow, as far as these transitions show.

## Exp 3: cliques against provers [after review: reframed]

Fable showed the original verdicts were foreordained. A clique world has neither a strict nor a neutral exit
against any class: ρ(D | all-clique) ≈ 10⁻⁶⁷ and ρ(FairBot | all-clique) ≈ 10⁻³⁵ at N = 10³. So it is the unique
closed class, and π(cliques) ≈ 1 in every cell, at c = 0 as well. The clique also strictly invades
`BOX(THEM(THEM))`, at ρ = 0.26. The original verdicts 8–10 are withdrawn and recorded in REJECTED.md.

What remains informative is the expected number of mutation events from all-D until the chain first enters a
clique state, from the transient fundamental matrix; and, for m = 4, the number of terminal classes. With several
terminal classes the chain is an absorption lottery, not π, which rule 5 covers.

Cells: n = 8, c ∈ {0, 10⁻²}, N ∈ {10³, 10⁴}, and three clique treatments: m = 1; m = 4 with fixed mass per
spelling; m = 4 with fixed total mass.

8. **The check:** π(cliques) is at least 0.99 in every cell.
9. **Hitting times scale with clique supply.** With mass per spelling, the m = 4 hitting time is 1/4 of m = 1,
   ±30%. With fixed total mass it is within ±30% of m = 1.
10. **Pricing slows cliques only a little.** At N = 10⁴, c = 10⁻² raises the hitting time over c = 0 by less than
    2×. The clique's entry barrier is about N·w·c²/(2b) ≈ 0.15.

**Falsifiers.**
- *Of the ladder:* at c = 10⁻², ALLC is not the dominant exit from all-FairBot, or P(C,C) at N = 3·10⁴ is within
  2× of c = 0.
- *Of structural rescue:* torus entry at c = 10⁻¹ falls by more than 2× from side 16 to 64, beyond its confidence
  interval [after review: aligned with prediction 5].
- *Of the clique takeover:* π(cliques) below 0.99 in any cell.
- *Of the lazy escape:* see prediction 6.

**What this would mean.**
- Priced, universal conditional cooperation fails in the limit, well-mixed or not, because of the price ladder.
- Structure repairs entry, not the ladder.
- What survives pricing is parochial self-recognition. If so, realizable efficiency in the limit is clique-like,
  and universal cooperation needs either free reasoning or something that punishes cheaper on-path
  equivalents. That is the regress of THEORY §9.7, now with a price on every rung.
- Fable's E3 mechanism, a standing fringe of defectors pruning the shadow at finite ε, is not tested here. These
  runs are all ε→0 objects.
