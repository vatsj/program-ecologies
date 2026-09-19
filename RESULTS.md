# Results — first sweep (2026-09-18)

All numbers come from `runs/results.md` (one row per cell) and the per-cell
`runs/<hash>/report.md`, which carry the full support and transition structure.
Node counts follow IMPLEMENTATION §2 (application is a node), so THEORY's
"n=5 / n=6" predictions correspond to n=6 / n=7 here.  PD payoffs: C/C 0,
C/D −2, D/C 1, D/D −1; efficient symmetric payoff 0.

## Predictions from THEORY §7

| | prediction | outcome |
|---|---|---|
| (a) | strong arm, PD, one level below the ¼-grounder: no stable cooperation | **Confirmed** at n=6: π is all-D plus the D–`THEM(ME)` neutral edge; mean payoff −1.0 at N=10, 100, 1000. 21 behavioural classes. |
| (b) | strong arm at the ¼-grounder's level: bistable switching FairBot–ALLC edge ↔ all-D | **Not observed** at n=7 (N=10, 100): π is still all-D + D-like neutral edge, deadweight loss 1.0. The 7-node `or(and(X,X),THEM(ME))` earns −1.25 against D versus D's −1, so under the deterministic replicator it dies on arrival; the only entry route is the neutral corner all-`THEM(ME)` (FairBot invades it at second order), which the μ-biased walk along the D–`THEM(ME)` edge essentially never reaches. Bistable switching does appear, but in the **weak** arm (below). |
| (c) | weak arm at n ≥ 9: PrudentBot collapses the FairBot–ALLC edge | n=9 not run yet (n=7 running; see below). |
| (d) | `eq(THEM,ME)` wins the source arm | **Confirmed** at n=6 (N=10, 100): the two spellings of the 3-node clique take 0.42 each; every other terminal class is another clique variant. Each clique is absorbing, so π is the seed-absorption mixture (28 closed classes). Mean payoff −0.022, deadweight loss 0.022. |

## Weak arm, PD, n=6 (N=10)

Bistable switching, one level earlier than THEORY expected and with a different
reciprocator: the 4-node third-party probe `THEM(^C)` ("cooperate iff you
cooperate with ALLC") needs no stochastic grounding, cooperates with itself and
with ALLC, defects against D, and is neutral against D at first order but
beats it at second order, so it invades all-D; ALLC then drifts in along the
neutral `THEM(^C)`–C edge until D re-invades (D's fitness on the edge is
2y − 1 at ALLC frequency y).  π at N=10: all-D 0.58, the C–`THEM(^C)` edge
≈ 0.30 (spread over grid positions), D–`THEM(ME)`/`THEM(THEM)` edges ≈ 0.06.
Mean payoff −0.68 (strong arm: −1.0).  48 behavioural classes.  74 transitions
indeterminate (replicator cycles among three conditional types; excluded and
flagged as THEORY §5 requires).

## Stag Hunt, weak arm n=6 (N=10)

All-Stag (0.98) with a small Stag–`THEM(^Stag)` neutral edge; payoff 4 =
efficient; deadweight loss 0.

## Moran check (strong arm, PD, n=6, N=100)

Mode agrees (all-D).  Neutral-edge occupancy does not: chain 45% on the
D–`THEM(ME)` edge, Moran < 1% at ε = 0.001, 0.01, 0.05, 0.2.  The mean-field
replicator has no genetic drift, so a neutral lineage persists until a
mutation displaces it; in the Moran process it is lost by drift within ~N
events unless εN ≫ 1, and then several lineages coexist.  This is a property
of the model as specified, not of the implementation.

## Divergence rates

strong n=6 0.04%, n=7 0.55%; weak n=6 0.19%; source n=6 0.14% of pairs.
