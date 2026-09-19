# Results — first sweep (2026-09-18)

Every number below comes from `runs/results.md` (one row per cell) and the per-cell
`runs/<hash>/report.md`, which carry the full support and transition structure.
Node counts follow IMPLEMENTATION §2 (application is a node), so THEORY's
"n=5 / n=6" predictions correspond to n=6 / n=7 here.  PD payoffs C/C 0,
C/D −2, D/C 1, D/D −1 (efficient 0).  Prior: bits = log2 a(|p|) + 2 log2|p| + 1.
Chain: deterministic replicator, single-mutant transitions, flow-pruned
exploration (theta 1e-6, cut flow ≤ 6e-4 in every cell), π = absorption-weighted
mixture over closed classes from the μ-weighted monomorphic seeds; π sums to 1
in every cell.

## THEORY §7 predictions

| | prediction | outcome |
|---|---|---|
| (a) | strong arm, PD, one level below the ¼-grounder: no stable cooperation | **Confirmed** (n=6, N=10/100/1000; n=7 N=10/100): π is all-D plus the D–`THEM(ME)` neutral edge, mean payoff −1.000. 21 classes at n=6, 44 at n=7. |
| (b) | strong arm at the ¼-grounder's level: bistable switching FairBot–ALLC ↔ all-D | **Not observed** at n=7 (N=10, 100): still all-D, deadweight loss 1.0. `or(and(X,X),THEM(ME))` earns −1.25 against D vs D's −1, so under the deterministic replicator it dies on arrival. Its only entry is the neutral corner all-`THEM(ME)` (which it invades at second order); the μ-biased walk along the D–`THEM(ME)` edge (μ(D) ≈ 90× μ(`THEM(ME)`)) never gets there (flow < 1e-6). |
| (c) | weak arm at n ≥ 9: PrudentBot collapses the FairBot–ALLC edge | Not run (n=9 needs ~40× the n=7 evaluation; see "not done"). At n=7 the edge is *already* collapsed, but by a different mechanism (below). |
| (d) | `eq(THEM,ME)` wins the source arm | **Confirmed** (n=6, N=10/100): the two spellings of the 3-node clique take 0.423 each; all 28 closed classes are clique variants (`not(not(eq(..)))`, `and(eq(..),C)`, …). Mean payoff −0.022. |

## Weak arm, PD (n=6: N=10/100; n=7: N=10) — bistable switching via a third-party probe

The reciprocator that appears is not FairBot but the **4-node `THEM(^C)`**:
"cooperate iff the opponent cooperates with ALLC".  It needs no stochastic
grounding (the probe bottoms out in the constant), cooperates with itself and
with ALLC, defects against D, and is neutral against D at first order but beats
it at second order (0 vs −1 in self-play), so it invades all-D.

Transition structure (from the n=7, N=10 report):

- all-D → `THEM(^C)` takes over (share of mutation events 9.5e-4; the D–`THEM(ME)` edge takes 7.5e-3 but is a dead end).
- all-`THEM(^C)` → ALLC drifts in (neutral edge; ALLC is 1 node, so the walk is biased toward ALLC).
- edge at ALLC frequency y → all-D via a D mutant once y > ½ (D earns 2y − 1 on the edge), **or** → all-ALLC via `THEM(^D)` ("cooperate iff you cooperate with ALLD"), which exploits `THEM(^C)` (1 vs −2), kills it, then starves against itself and leaves ALLC; D then takes all-ALLC.

So the FairBot–ALLC edge THEORY expected at n ≥ 9 to be collapsed by PrudentBot
is at n=6–7 a `THEM(^C)`–ALLC edge collapsed by D and by `THEM(^D)`.

| cell | all-D | cooperative edge | mean payoff |
|---|---|---|---|
| n=6 N=10 | 0.58 | ≈0.30 | −0.684 |
| n=6 N=100 | 0.23 | ≈0.35 (concentrated near 45/55) | −0.725 |
| n=7 N=10 | 0.58 | ≈0.30 | −0.687 |

48 classes at n=6, 105 at n=7.  Indeterminate transitions: 136 / 435 / 458 —
genuine replicator cycles among three conditional types (e.g. `THEM(THEM)`,
`and(X,THEM(^C))`, `not(THEM(^C))`; trajectory spread 0.4), excluded and flagged
as THEORY §5 requires.  Their total mutation share is < 1e-3.

## Stag Hunt (Stag/Stag 4, Stag/Hare 0, Hare/Stag 3, Hare/Hare 3)

Strong arm n=6: N=10 all-Stag (0.998); N=100/1000 bistable, all-Stag 0.33 /
0.28 vs all-Hare + its `THEM(ME)` edge ≈ 0.67 / 0.72 (mean payoff 3.33).
Weak arm n=6: all-Stag 0.98 (N=10), 0.83 + Stag–`THEM(^Stag)` edge (N=100);
payoff 4.000, loss 0.  Weak extensionality removes the Hare basin here.

## Exchange game (Give/Give 2, Give/Keep −1, Keep/Give 3, Keep/Keep 0), weak n=6

Same structure as the PD: all-Keep 0.57 (N=10) / 0.22 (N=100) and the
`THEM(^Give)`–Give edge; mean payoff 0.64 / 0.60 (efficient 2).  The
prediction that `or(X,THEM(ME))` would already sustain cooperation here (it is
strictly stable against Keep: 3·½ < 2) is **not** borne out: FairBot does not
enter the support at all; the probe reciprocator dominates it.

## Divide the dollar (Half/Half 0.5, else 0), weak n=6

All-Half and its neutral equivalents; payoff 0.500 = efficient.  As predicted.

## Moran check (strong arm, PD, n=6, N=100)

Mode agrees (all-D).  Neutral-edge occupancy does not: chain 45% on the
D–`THEM(ME)` edge, Moran < 1% at ε ∈ {0.001, 0.01, 0.05, 0.2}.  The mean-field
replicator has no genetic drift, so a neutral lineage persists until a mutation
displaces it; in the Moran process it is lost by drift within ~N events unless
εN ≫ 1, and then several lineages coexist.  A property of the model as
specified, not of the implementation.

## Divergence rates (pairs with floor probability > 1e-6)

strong n=6 0.04%, n=7 0.58%; weak n=6 0.19%, n=7 1.24%; source n=6 0.14%.

## Not done

- n=8, 9 (prediction (c)).  The incremental path works (n=7 weak: 9.4K programs,
  105 classes, 20K states, 100 s at N=10); n=9 is 228K programs and the
  per-support signature pass scales linearly, so ~1 h per N is expected.
- N = 1000 for the weak arm (state counts ~10⁵); N ≤ 100 only.
