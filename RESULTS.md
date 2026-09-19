# Results — Moran-fixation chain (2026-09-19)

Second sweep.  The first sweep (deterministic-replicator transitions, neutral
sets as grid states) is kept as RESULTS-2026-09-18-replicator.md; its
"cooperative edge ≈ 0.30" was the artifact fixed here.

Every number comes from `runs/results.md` (one row per cell, 96 cells) and the
per-cell `runs/<hash>/report.md` (support, transitions, per-edge ρ and k*).
Node counts follow IMPLEMENTATION §2 (application is a node).  PD payoffs
C/C 0, C/D −2, D/C 1, D/D −1 (efficient 0).  Prior bits = log2 a(|p|) +
2 log2 |p| + 1.

## The chain

- **States**: monomorphic populations and polymorphic attractors (rest points
  of the replicator with a restoring force), on the 1/N grid.  Neutral sets
  are not states; a neutral rest set is collapsed to its vertices in
  proportion to the frequencies (neutral drift fixes type s with probability
  x_s).
- **Edge weights**: P(A→B) ∝ μ(q)·ρ(q | A→B).  ρ is the frequency-dependent
  Moran fixation probability of a single q-lineage against the lumped
  resident (fitness f = 1 + w·payoff, clamped at 1e-6):
  ρ = [1 + Σ_{k=1}^{k*−1} Π_{j=1}^{k} f_A(j)/f_q(j)]^{-1}, with k* = N for a
  monomorphic target (exactly 1/N for a neutral mutant; above 1/N for an
  advantaged one; below 1/N but positive for a disadvantaged one, so every
  mutant can now enter).  The deterministic target B is still found by the
  replicator from A + q (and from q at ½ when q dies at first order, to find
  targets behind a fitness valley).  1 − ρ stays at A.
- **Polymorphic targets** (approximation): k* is q's count at B, i.e. ρ is
  the probability of reaching B's composition before extinction, with the
  residents held at A's proportions along the way; when q invades, changes
  the residents and dies (e.g. `THEM(^D)` killing `THEM(^C)`), k* is q's
  peak count on the path.  The stationary flow into polymorphic targets is
  reported per cell as `poly_flow`; it is ≤ 6e-4 in every PD cell, ≤ 2e-2
  in Stag Hunt (N=10, where a Stag/coin polymorphism holds up to 0.33 of π)
  and ≤ 6e-2 in the ROLE games at N=10: those N=10 cells are where the
  approximation is load-bearing.
- **Selection intensity w** ∈ {0.01, 0.1, 1}; N ∈ {10, 100} (1000 for the
  strong arm).  Exploration, closed-class solve and reporting are unchanged.
  π sums to 1 in every cell; cut flow ≤ 1e-5.

## Moran check and calibration (`runs/moran_check.md`)

Chain π by majority type vs a Moran simulation with the same fitness map
(4·10⁶ events, PD, n=6, N=100):

| arm | w | ε (εN) | all-D chain / Moran | cooperator chain / Moran |
|---|---|---|---|---|
| strong | 0.01 | 0.001 (0.1) | 0.51 / 0.34 | — (X 0.29 / 0.43, C 0.18 / 0.23) |
| strong | 0.1 | 0.001 (0.1) | 0.991 / 0.998 | — |
| strong | 1 | 0.001 (0.1) | 0.999 / 1.000 | — |
| weak | 0.01 | 0.001 (0.1) | 0.50 / 0.34 | `THEM(^C)` 0.001 / 0.000 |
| weak | 0.1 | 0.001 (0.1) | 0.979 / 0.997 | `THEM(^C)` 0.006 / 0.000 |
| weak | 1 | 0.001 (0.1) | 0.882 / 0.992 | `THEM(^C)` 0.099 / 0.000 |
| weak | 1 | 0.01 (1) | 0.882 / 0.724 | `THEM(^C)` 0.099 / 0.215 |

Neutral-edge occupancy: the D–`THEM(ME)` edge that carried 45% of π in the
first sweep is gone; Moran has `THEM(ME)` present 0.1–2% of the time and the
chain now puts 0.1% on all-`THEM(ME)` (w = 0.1).  **w = 0.1 is the
calibration**: at εN = 0.1 (single-mutant regime) the mode and the
cooperator share agree to within 0.02 in both arms.  At w = 0.01 drift
dominates and the chain, which has no drift *within* a monomorphic state's
residence, overstates all-D relative to Moran's mutation–drift mixture; at
w = 1 the chain overstates `THEM(^C)` at εN = 0.1 and understates it at
εN = 1, i.e. the answer there depends on ε, outside the regime THEORY §5
assumes.

## PD

### Strong arm (n=6: N=10/100/1000; n=7: N=10/100)

| w | N | all-D | rest |
|---|---|---|---|
| 0.01 | 10 / 100 / 1000 | 0.35 / 0.51 / 0.99 | X 0.31 / 0.29 / 0.007, C 0.31 / 0.18 / 0 (mutation–drift) |
| 0.1 | 10 / 100 / 1000 | 0.53 / 0.991 / 0.999 | X 0.28 / 0.005 / 0 |
| 1 | 10 / 100 / 1000 | 0.997 / 0.999 / 0.999 | — |

n=7 is identical to n=6 to three decimals at every (w, N).  Mean payoff at
w ≥ 0.1, N ≥ 100: −0.996 … −1.000.  Prediction (a) stands; prediction (b)
(bistable switching to a FairBot–ALLC edge at the ¼-grounder's level) still
fails, now for a quantified reason: see (b) below.

### Weak arm (n=6 and n=7, N=10/100) — (a) time shares

| w | N | all-D | all-`THEM(^C)` | all-C | mean payoff |
|---|---|---|---|---|---|
| 0.01 | 10 | 0.347 | 0.0007 | 0.311 | −0.523 |
| 0.01 | 100 | 0.501 | 0.0012 | 0.184 | −0.663 |
| 0.1 | 10 | 0.528 | 0.0027 | 0.168 | −0.685 |
| 0.1 | 100 | 0.979 | 0.0059 | 0.0018 | −0.988 |
| 1 | 10 | 0.969 | 0.012 | 0.003 | −0.980 |
| 1 | 100 | 0.882 | 0.099 | 0.003 | −0.893 |

(n=7 differs from n=6 by ≤ 0.005 everywhere.)  The first sweep's "cooperative
edge ≈ 0.30" is gone: with fixation weights the cooperative state is
all-`THEM(^C)` at 0.6% (w = 0.1) to 10% (w = 1), and it is entered by
second-order selection (ρ = 0.026 at w = 0.1, 0.5 at w = 1, vs 1/N = 0.01
for a neutral mutant) and left mainly by ALLC drifting in (ρ = 1/N exactly)
and by `THEM(^D)`.

### (b) Do the FairBots enter all-D?

ρ(q | all-D) for a single mutant at N = 100 (N = 10 in brackets):

| q | nodes | u(q,D) | w = 0.01 | w = 0.1 | w = 1 |
|---|---|---|---|---|---|
| `or(X,THEM(ME))` (½-grounder) | 5 | −1.5 | 8.4e-3 (0.084) | 1.1e-3 (0.031) | 1e-191 (5e-12) |
| `or(and(X,X),THEM(ME))` (¼-grounder) | 7 | −1.25 | 1.0e-2 (0.100) | 8.6e-3 (0.096) | 2e-99 (5e-12) |
| `THEM(^C)` | 4 | −1 | 1.2e-2 (0.101) | 2.6e-2 (0.114) | 0.5 (0.5) |
| neutral reference | | | 1/N | 1/N | 1/N |

They enter now, but only at weak selection, where they enter as drift
(ρ ≈ 1/N) and leave the same way: π(all-`or(X,THEM(ME))`) = 7.6e-5 (w=0.01),
8.4e-6 (w=0.1), 5.6e-6 (w=1) at n=6, N=100; the ¼-grounder (7 nodes, n=7
cells) is below 1e-4 everywhere.  At w = 1 with these payoffs a single
C-against-D interaction (payoff −2, f clamped at 1e-6) makes the valley
uncrossable.  The stochastically-grounded FairBots are dominated by the
third-party probe `THEM(^C)`, which needs no grounding and pays no
exploitation cost against D.

### (c) The cooperation cycle (weak n=6, N=100; P = μ·ρ share of mutation events per step)

| step | mutant | μ | ρ (w=0.01 / 0.1 / 1) | P (w=0.01 / 0.1 / 1) |
|---|---|---|---|---|
| all-D → all-`THEM(^C)` | `THEM(^C)` | 6.8e-4 | 0.012 / 0.026 / 0.50 | 1.1e-5 / 2.4e-5 / 4.6e-4 |
| all-`THEM(^C)` → all-`THEM(^D)` | `THEM(^D)` | 6.8e-4 | 0.016 / 0.094 / 0.52 | 1.4e-5 / 8.6e-5 / 4.7e-4 |
| all-`THEM(^C)` → all-C (drift) | C | 0.245 | 0.010 / 0.010 / 0.010 | 3.3e-3 / 3.3e-3 / 3.3e-3 |
| all-`THEM(^D)` → all-C | C | 0.245 | 0.014 / 0.086 / 0.99 | 4.5e-3 / 2.8e-2 / 0.33 |
| all-`THEM(^D)` → all-D (neutral) | D | 0.245 | 0.010 / 0.010 / 0.010 | 3.3e-3 / 3.3e-3 / 3.3e-3 |
| all-C → all-D | D | 0.245 | 0.016 / 0.094 / 0.52 | 5.2e-3 / 3.1e-2 / 0.17 |

The dominant exit from all-`THEM(^C)` is not `THEM(^D)` but ALLC drift
(3.3e-3 vs ≤ 4.7e-4): ALLC is 1 node and enters neutrally at exactly 1/N,
after which D takes all-C at ρ = 0.09–0.5.  `THEM(^D)` matters at w = 1,
where it is a second-order-advantaged probe that goes to all-C with ρ = 0.99
(it cooperates with ALLC and starves against itself).  Every step of the
cycle is a monomorphic state; the neutral edges of the first sweep were the
walk between these vertices.

## Source arm (n=6, N=10/100)

| w | N=10 | N=100 |
|---|---|---|
| 0.01 | D 0.24, X 0.22, C 0.21, `not(C)` 0.06 (mutation–drift) | D 0.34, X 0.20, C 0.12 |
| 0.1 | D 0.36, X 0.20, C 0.11 | `eq(THEM,ME)` 0.33 + `eq(ME,THEM)` 0.33, D 0.15 |
| 1 | `eq(THEM,ME)` 0.50 + `eq(ME,THEM)` 0.50 | spread evenly over the 28 clique spellings (0.036 each) |

Prediction (d) holds at w ≥ 0.1, N = 100 (and at w = 1, N = 10); cliques are
left only by drift fixation of another clique spelling (ρ = 1/N, all cliques
being mutually neutral… no: `eq(THEM,ME)` vs `not(not(eq(THEM,ME)))` is
D/D, so the spellings are mutually *defecting* and a spelling switch is a
valley crossing; at N = 100, w = 1 those crossings are all equally unlikely,
which is why π is uniform over spellings).  At w = 0.01 the source arm is
mutation–drift like the others.

## Stag Hunt (Stag/Stag 4, Stag/Hare 0, Hare/Stag 3, Hare/Hare 3)

| arm | w | N=10 | N=100 | N=1000 |
|---|---|---|---|---|
| strong | 0.01 | Hare 0.36, {Stag ½, X ½} poly 0.33, Stag 0.13 | Hare 0.57, Stag 0.11 | Hare 0.99 |
| strong | 0.1 | Hare 0.54, poly 0.21 | Hare 0.991 | **Stag 0.90**, Hare 0.10 |
| strong | 1 | Hare 0.92 | Hare 0.98, Stag 0.02 | **Stag 1.00** |
| weak | 0.01 | Hare 0.35, poly 0.32, Stag 0.14 | Hare 0.57, Stag 0.13 | — |
| weak | 0.1 | Hare 0.53, poly 0.21 | Hare 0.97 | — |
| weak | 1 | Hare 0.91 | Hare 0.92, Stag 0.06 | — |

The basin selection is a valley-crossing competition: Stag invading all-Hare
needs to cross frequency ¾, Hare invading all-Stag needs frequency ¼, and
which crossing is rarer depends on N·w.  At N = 1000 the risk-dominated
Stag basin wins for w ≥ 0.1; at N ≤ 100 Hare wins.  The first sweep's
"all-Stag, loss 0" for the weak arm was the artifact (neutral drift along a
Stag–`THEM(^Stag)` edge never having to cross the valley).  The
{Stag ½, X ½} polymorphism at N = 10 is a genuine replicator attractor (X is a
fair coin; Stag and X earn equal fitness at that mix) and is where the
polymorphic-target approximation is load-bearing (`poly_flow` up to 1.8e-2).

## Test games (weak arm n=5; n=6 for exchange and dollar), N=10 / 100

| game | verdict written 2026-09-18 | w = 0.1, N = 100 | w = 1, N = 100 | w = 0.01 |
|---|---|---|---|---|
| Chicken + ROLE | all-`ROLE` / all-`not(ROLE)`, loss 0 | `ROLE` 0.80, `not(ROLE)` 0.20; payoff 0.499, loss 0.001 | `THEM(^not(ROLE))` 0.93 (a probe that realises the same correlated outcome), `ROLE` 0.06; loss 0.001 | mutation–drift mixture, loss 0.45 |
| Chicken, no ROLE | loss ≥ 0.5 | conditional polymorphism {Straight 0.19, `not(THEM(THEM))` 0.64, `not(THEM(^Straight))` 0.15, …}; loss 0.75 | same polymorphism at 1.00; loss 0.83 | loss 0.69 |
| Nash demand + ROLE | all-`ROLE`, loss 0 | `ROLE` 0.35, `not(ROLE)` 0.09, rest drift; loss 0.07 | `ROLE` 0.79, `not(ROLE)` 0.20; loss 0.001 | loss 0.11 |
| Nash demand, no ROLE | Hawk–Dove polymorphism, High at ⅓, payoff 0.4 | polymorphisms with payoff 0.399, loss 0.101 | payoff 0.400, loss 0.100 | loss 0.103 |
| Divide the dollar | all-Half, loss 0 | Half 0.78; loss 0.08 | Half 0.97; loss 0.000 | drift, loss 0.27 |
| Zero-sum + ROLE | drift or cycles, loss 0 | drift over monomorphic states (D 0.40, X 0.23, C 0.14), payoff 0 | D 0.44, X 0.23; payoff 0 | drift |
| Exchange game | cooperation via `or(X,THEM(ME))` | Keep 0.97, `THEM(^Give)` 0.009; loss 1.96 | Keep 0.97, `THEM(^Give)` 0.024; loss 1.94 | drift, loss 1.32 |
| Battle of the sexes + ROLE | all-A / all-B even, loss 0 | A 0.71, B 0.25; loss 0.03 | A 0.497, B 0.497; loss 0.001 | loss 0.39 |

At w = 0.01 every game is a mutation–drift mixture of the short constants
(C, D, X carry ≈ 80% of μ), so the verdicts are only testable at w ≥ 0.1.
There they hold as before, with two changes from the first sweep: the
zero-sum game no longer floods the state space (53 monomorphic states instead
of a 10⁶-point neutral simplex) and the exchange game's cooperator share
drops from ≈ 0.3 to ≈ 0.02, for the same reason as in the PD.  N = 10 cells
at any w are drift-dominated (polymorphic attractors of C with the coin
programs hold 0.1–0.4 of π); the polymorphic-target approximation carries up
to 6% of the flow there (`poly_flow`), the most anywhere in the sweep.

## Unfakeable enterers (`runs/enterers_n9.md`, `runs/enterers_n7.md`)

Weak arm, L_9 (228,794 programs).  Conditions: (i) u(p,D) ≥ u(D,D) = −1,
(ii) u(p,p) > −1, (iii) no q ∈ L_9 invades all-p from rare (u(q,p) < u(p,p),
or equal with u(q,q) ≤ u(p,q)).

- (i): 80,836 programs; (ii): 145,682; both: 2,516.  **None of the 2,516
  satisfies (iii)**: every one is invaded by a program of ≤ 6 nodes (the L_6
  prefilter rejected all of them, so no full L_9 test was needed).  Same at
  n=7 (98 candidates, none).
- Shortest satisfying (i)+(ii): `THEM(^C)` (4 nodes, 10.95 bits); invaded by
  `THEM(^D)` (u = 1 vs 0), `THEM(^X)` (0.5), and their spellings.
- Shortest satisfying (i)+(iii): `and(X,and(X,THEM(ME)))` (7 nodes) — a
  behavioural ALLD, uninvadable because it never cooperates.
- Shortest satisfying (ii)+(iii): `or(and(X,X),THEM(ME))` (7 nodes): the
  ¼-grounder is uninvadable by anything in L_9 but fails (i) (u(p,D) =
  −1.25 < −1).
- **`or(and(and(X,X),THEM(^C)),THEM(ME))` (12 nodes, 32.8 bits) satisfies all
  three against L_9**: u(p,D) = −1, u(p,p) = 0, u(D,p) = −1; no invader in
  L_9.  ρ(p | all-D) = 0.101 / 0.114 / 0.5 (N=10) and 0.0117 / 0.0258 / 0.5
  (N=100) at w = 0.01 / 0.1 / 1 — identical to `THEM(^C)`'s, since its payoffs
  against D and itself are the same.  Reference-evaluator spot check
  (budget 300): `THEM(^D)` plays D against it and it plays C w.p. ¼, so
  u(`THEM(^D)`, p) = −0.5 < 0: no invasion; `THEM(^C)`, `or(X,THEM(ME))` and C
  all cooperate mutually with it (u = 0 = u(p,p), u(q,q) = u(p,q) = 0):
  neutral, not invading.  So the shortest unfakeable enterer has between 10
  and 12 nodes; the L_9 search says no shorter one exists.  Caveat: (iii) was
  tested against L_9 only, and (iii) excludes invasion but not neutral drift
  (ALLC drifts in at 1/N and D then takes all-ALLC), so "unfakeable" here
  means "not invaded from rare", not "absorbing".

## Prior diagnostic (`runs/prior_uniform.md`)

Weak arm, PD, n=6, N=100, w=0.1, with μ uniform over the 1,852 programs of
L_6 instead of 2^−bits (class weights are then member counts, so the
behavioural classes C, D and X still carry 0.31, 0.31 and 0.18):

| state | π (bits) | π (uniform) | μ_class (bits) | μ_class (uniform) |
|---|---|---|---|---|
| all-D | 0.979 | 0.879 | 0.329 | 0.309 |
| all-`THEM(^C)` | 0.0059 | 0.0374 | 9.1e-4 | 7.6e-3 |
| all-X | 0.0073 | 0.0102 | 0.312 | 0.176 |
| all-C | 0.0018 | 0.0078 | 0.329 | 0.309 |
| mean payoff | −0.988 | −0.936 | | |

Removing the length prior raises the cooperative share 6× (its entry rate
from all-D rises 8×, μ(`THEM(^C)`) going from 9.1e-4 to 7.6e-3 with the same
ρ = 0.026), but all-D still holds 0.88.  The length prior is part of the
mechanism, not the whole of it: the exit from all-`THEM(^C)` is ALLC drifting
in (P = 3.3e-3 per event under bits, 3.1e-3 under uniform, μ(C)·1/N in
both), and μ(C) is large under either prior because the constant class is
huge.  Cooperation is limited by the ALLC leak, which the prior barely
changes.

## Not done

- Prediction (c) at n=9 through the chain (the enterer search covers what
  L_9 can do against all-D and all-p, but not the full n=9 chain).
- N = 1000 in the weak arm.
- Polymorphic-target ρ beyond the truncated-product approximation.
