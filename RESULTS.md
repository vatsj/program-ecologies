# Results — Moran-fixation chain (2026-09-19)

Second sweep.  The first sweep (deterministic-replicator transitions, neutral
sets as grid states) is kept as RESULTS-2026-09-18-replicator.md; its
"cooperative edge ≈ 0.30" was the artifact fixed here.

Every number comes from `runs/results.md` (one row per cell, 96 cells) and the
per-cell `runs/<hash>/report.md` (support, transitions, per-edge ρ and k*).
Node counts follow IMPLEMENTATION §2 (application is a node).  PD payoffs
C/C 0, C/D −2, D/C 1, D/D −1 (efficient 0).  Prior bits = log2 a(|p|) +
2 log2 |p| + 1.

## Consistent sweep (exp fitness map, attracting-target check) — supersedes the per-game tables below

All 32 cells of the original grid re-run on 2026-09-19 with f = exp(w·payoff),
w ∈ {0.1, 0.3, 1}, N ∈ {10, 100} (1000 for strong PD/Stag), after the fix
that rejects non-attracting rest points found from the ½ probe (`runs/results.md`,
rows with `fmap=exp`).  The earlier sections are kept for the transition
narratives; where numbers differ, these are the ones to cite.

| game (arm, n) | w = 0.1, N = 100 | w = 0.3, N = 100 | w = 1, N = 100 | N = 10 (w = 0.1 / 1) |
|---|---|---|---|---|
| PD strong 6 (= strong 7 to 3 dp) | D 0.988 | D 0.998 | D 0.999 | D 0.52 / 0.99 (rest X, C: mutation–drift) |
| PD weak 6 (= weak 7) | D 0.977, `THEM(^C)` 0.006 | D 0.983, `THEM(^C)` 0.010 | D 0.980, `THEM(^C)` 0.016 | D 0.52 / 0.98 |
| PD weak 6, N = 1000 | D 0.981, `THEM(^C)` 0.015 | D 0.980, `THEM(^C)` 0.018 | D 0.980, `THEM(^C)` 0.017 | — |
| PD source 6 | `eq` cliques 0.32 + 0.32, D 0.18 | cliques 0.44 + 0.44 | cliques 0.45 + 0.45 | D 0.35 / D 0.32 + cliques 0.23 + 0.23 |
| Stag strong 6 | Hare 0.989 | Hare 0.944 | **Stag 0.992** | Hare 0.58 / 0.99 |
| Stag strong 6, N = 1000 | Stag 0.995 | Stag 1.000 | Stag 1.000 | — |
| Stag weak 6 | Hare 0.964 | Hare 0.832, Stag 0.155 | **Stag 0.992** | Hare 0.57 / 0.98 |
| Exchange weak 6 | Keep 0.974 | Keep 0.977, `THEM(^Give)` 0.014 | Keep 0.973, `THEM(^Give)` 0.021 | Keep 0.53 / 0.98 |
| Dollar weak 6 | Half 0.78 | Half 0.96 | Half 0.97 | Half 0.37 / 0.72 |
| Chicken + ROLE weak 5 | `ROLE` 0.80, `not(ROLE)` 0.20 (loss 0.001) | same (loss 0.002) | `THEM(^not(ROLE))` 0.997 (loss 0.000) | `ROLE` 0.41 / 0.80 |
| Chicken no ROLE | conditional polymorphism, loss 0.74 | loss 0.83 | loss 0.83 | loss 0.65 / 0.74 |
| Demand + ROLE | `ROLE` 0.36 (loss 0.07) | `ROLE` 0.65 (loss 0.02) | `ROLE` 0.80, `not(ROLE)` 0.20 (loss 0.000) | loss 0.12 / 0.08 |
| Demand no ROLE | polymorphisms, payoff 0.399 | 0.400 | 0.400 | 0.394 / 0.395 |
| Zero-sum + ROLE | drift over constants, payoff 0 | 0 | 0 | 0 |
| BoS + ROLE | A 0.491 = B 0.491 (loss 0.012) | 0.498 = 0.498 | 0.478 = 0.478 (loss 0.007) | 0.31 = 0.31 / 0.48 = 0.48 |
| Ultimatum ROLE weak 5 | M 0.372, L 0.349, H 0.092 (rejection 0.086) | — | — | — |

Changes from the clamped/first sweeps worth noting: (i) the Stag Hunt N = 10
"{Stag ½, X ½} polymorphism" (up to 0.33 of π) was a coordination
separatrix, not an attractor, and is gone; the N = 10 mass is now on the
constants.  (ii) Under the exponential map the Stag basin choice at N = 100
depends on w: Hare at w ≤ 0.3, Stag at w = 1 (both arms), and Stag at
N = 1000 for every w.  (iii) Chicken at w = 1 is taken over by
`THEM(^not(ROLE))` — a probe that plays what the opponent plays against the
role-mirror program, which realises the same correlated outcome as `ROLE`
with loss 0.  (iv) PD is unchanged in substance: all-D at 0.98–0.99, the
`THEM(^C)` cooperator at 0.6–1.8%.  (Rows in `runs/results.md` from the
earlier exp re-run at N = 1000 for the exchange game still carry the old
level names D/C for Keep/Give; the game's level order was fixed with the
k-ary refactor and the numbers are unchanged.)

## Void cells (fitness clamping)

The cells below were run with fitness f = 1 + w·payoff clamped at 1e-6.  In
games with negative payoffs (PD: C-vs-D pays −2; exchange: Give-vs-Keep
pays −1) the clamp binds at w = 1 (f = 1 − 2 < 0 → 1e-6), so a single
exploited interaction makes the fitness ratio ~10⁶ and every valley
crossing collapses to ~e^{−N·14}.  **All w = 1 PD and exchange cells in this
file and in `runs/results.md` (rows without `fmap=exp`) are void** for that
reason: the "2e-99 / 1e-191" FairBot entries, the 0.882 / 0.099 (N=100) and
0.695 / 0.288 (N=1000) weak-PD shares, the w = 1 Moran-check rows, and the
w = 1 exchange rows.  They are kept, not deleted; the replacement runs use
f = exp(w·payoff) and are in the "Exponential fitness map" section.  The
w = 0.01 and w = 0.1 rows are unaffected (1 + w·payoff ≥ 0.8 for all
payoffs in these games).  Stag Hunt, divide-the-dollar, Nash demand and BoS
have non-negative payoffs, so their w = 1 cells never hit the clamp and
stand; Chicken (−10, −1) and zero-sum (−1) do hit it at w = 1 and were not
re-run.

## The chain

- **States**: monomorphic populations and polymorphic attractors (rest points
  of the replicator with a restoring force), on the 1/N grid.  Neutral sets
  are not states; a neutral rest set is collapsed to its vertices in
  proportion to the frequencies (neutral drift fixes type s with probability
  x_s).
- **Edge weights**: P(A→B) ∝ μ(q)·ρ(q | A→B).  ρ is the frequency-dependent
  Moran fixation probability of a single q-lineage against the lumped
  resident (fitness f = 1 + w·payoff clamped at 1e-6 in the sweep; f =
  exp(w·payoff) from the "Exponential fitness map" section on):
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
| Battle of the sexes + ROLE | all-A / all-B even, loss 0 | A 0.483, B 0.483; loss 0.026 | A 0.497, B 0.497; loss 0.001 | loss 0.39 |

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

## lim_N: weak arm at N = 1000 (`runs/limN_weak.md`)

| game | w | N=10 | N=100 | N=1000 |
|---|---|---|---|---|
| PD: all-D / all-`THEM(^C)` | 0.1 | 0.528 / 0.001 | 0.979 / 0.006 | 0.980 / 0.016 |
| PD: all-D / all-`THEM(^C)` | 1 | 0.969 / 0.012 | 0.882 / 0.099 | **0.695 / 0.288** |
| PD mean payoff | 0.1 / 1 | −0.685 / −0.980 | −0.988 / −0.893 | −0.983 / −0.705 |
| Stag: all-Hare / all-Stag | 0.1 | 0.533 / 0.102 | 0.971 / 0.014 | 0.015 / 0.980 |
| Stag: all-Hare / all-Stag | 1 | 0.907 / 0.013 | 0.922 / 0.063 | 0.000 / 0.884 |

Entry and exit of all-`THEM(^C)` in the PD at N = 1000, per mutation event
(μ·ρ):

| edge | mutant | μ | ρ (w=0.1) | μρ (w=0.1) | ρ (w=1) | μρ (w=1) |
|---|---|---|---|---|---|---|
| all-D → all-`THEM(^C)` | `THEM(^C)` | 6.8e-4 | 8.3e-3 | 5.6e-6 | 0.500 | 3.4e-4 |
| all-`THEM(^C)` → all-C (drift) | C | 0.245 | 1/N = 1e-3 | 2.5e-4 | 1e-3 | 2.5e-4 |
| all-`THEM(^C)` → all-`THEM(^D)` | `THEM(^D)` | 6.8e-4 | 0.091 | 6.2e-5 | 0.502 | 3.4e-4 |
| all-`THEM(^C)` → all-`THEM(^X)` | `THEM(^X)` | 6.6e-4 | 0.048 | 3.1e-5 | 0.334 | 2.2e-4 |
| total exit | | | | 4.6e-4 | | 1.1e-3 |

The N-dependence is in two places.  The ALLC-drift exit is μ(C)/N and
vanishes as N → ∞; the second-order entry `THEM(^C)` has ρ → ½ at w = 1
(a mutant that is neutral at one copy and advantaged from two copies fixes
with probability → ½ under strong selection) but ρ → 0 like 1/N^{…} at
w = 0.1 (8.3e-3 at N=1000 vs 2.6e-2 at N=100: weak second-order selection
does not beat drift at large N).  So at w = 1 the cooperative share grows
with N (0.012 → 0.099 → 0.288) and the limit chain is the drift-free cycle
all-D → `THEM(^C)` → `THEM(^D)` → all-C → all-D with N-independent rates, in
which all-`THEM(^C)` holds a finite fraction; at w = 0.1 it stays at ~1–2%.
In the Stag Hunt N = 1000 flips the basin to all-Stag at both w (the Hare→Stag
valley at frequency ¾ is crossed more easily than the Stag→Hare valley at ¼
once N·w is large enough), with `THEM(^Stag)` a 0.3% transient.

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

## BoS tie-break (`runs/bos_tie.md`)

`games/bos.yaml` is symmetric (player 2's table with A↔B relabelled equals
player 1's; both constants earn 1.5 in self-play; the all-A and all-B classes
have 219 members and μ = 0.249 each; every exit from all-A had a mirror exit
from all-B with identical P).  The w = 0.1, N = 100 asymmetry (0.71 / 0.25)
came from a single unmirrored entry: the 50/50 A/B polymorphism plus one
coin mutant is 49.5/49.5/1 agents, and largest-remainder rounding to the 1/N
grid broke that tie by type index, always in A's favour, after which `ROLE`
(μ 0.19, ρ 0.34) tips 50/49 to all-A.  The tie-breaker was the grid
rounding, not the game, the language or μ.  Fixed: rounding ties now split
into every tie-break with equal weight; π is exactly symmetric (0.483 /
0.483 at w = 0.1, N = 100) and the PD cells are unchanged.

## Exponential fitness map: f = exp(w·payoff) (`runs/results.md` rows with `fmap=exp`, `runs/moran_check_exp.md`)

Weak arm, n=6, PD and exchange, re-run with f = exp(w·payoff) (no clamp; the
fitness ratio in the fixation product is exp(w·Δpayoff) at every frequency).

| game | w | N | all-D | all-`THEM(^C)` | ρ_enter(`THEM(^C)` \| all-D) | 1/N | mean payoff |
|---|---|---|---|---|---|---|---|
| PD | 0.1 | 100 | 0.977 | 0.0056 | 0.0248 | 0.010 | −0.987 |
| PD | 0.1 | 1000 | 0.981 | 0.0154 | 0.0079 | 0.001 | −0.984 |
| PD | 0.3 | 100 | 0.983 | 0.0103 | 0.0421 | 0.010 | −0.988 |
| PD | 0.3 | 1000 | 0.980 | 0.0175 | 0.0136 | 0.001 | −0.982 |
| PD | 1 | 100 | 0.980 | 0.0156 | 0.0742 | 0.010 | −0.983 |
| PD | 1 | 1000 | 0.980 | 0.0173 | 0.0246 | 0.001 | −0.982 |
| exchange | 0.1 | 100 | 0.974 | 0.0089 | 0.0346 | 0.010 | 0.034 |
| exchange | 0.1 | 1000 | 0.973 | 0.0215 | 0.0112 | 0.001 | 0.048 |
| exchange | 0.3 | 100 | 0.977 | 0.0143 | 0.0584 | 0.010 | 0.037 |
| exchange | 0.3 | 1000 | 0.972 | 0.0244 | 0.0192 | 0.001 | 0.052 |
| exchange | 1 | 100 | 0.973 | 0.0213 | 0.1016 | 0.010 | 0.048 |
| exchange | 1 | 1000 | 0.974 | 0.0240 | 0.0345 | 0.001 | 0.050 |

(ρ_enter is the fixation probability of a single `THEM(^C)` in all-D; it is
2.5–7× the neutral 1/N at N=100 and 8–25× at N=1000, because `THEM(^C)` is
neutral at one copy and advantaged from two.  Under the clamped map at w = 1
it was 0.5, an artifact.)

The cooperative time-share is 0.6–2.4% at every (w, N): the w = 1 numbers of
the clamped sweep (0.099 at N=100, 0.288 at N=1000) were the clamp, and the
lim_N growth reported above is gone — at N=1000 the share is 1.5–2.4% for
all w, in both games.  What limits cooperation is unchanged: all-`THEM(^C)`
is left by ALLC drift (μ(C)·1/N) and by `THEM(^D)`/`THEM(^X)`, and re-entered
from all-D at μ(`THEM(^C)`)·ρ_enter ≈ 6.8e-4 × 0.02–0.07; the ratio of exit
to entry rates is ~10–40 at every (w, N) tried.  Indeterminate transitions
(replicator cycles) appear in the exchange game at N=1000 and w ≥ 0.3 (63–92,
share < 1e-3), none in the PD.

Moran check (PD, n=6, N=100, 4·10⁶ events, same fitness map):

| arm | w | all-D chain / Moran (εN=0.1) | all-D chain / Moran (εN=1) | `THEM(^C)` chain / Moran (εN=0.1) / Moran (εN=1) |
|---|---|---|---|---|
| strong | 0.1 / 0.3 / 1 | 0.988/0.998, 0.998/1.000, 0.999/1.000 | 0.988/0.952, 0.998/0.999, 0.999/0.999 | — |
| weak | 0.1 | 0.977 / 0.997 | 0.977 / 0.951 | 0.006 / 0.000 / 0.000 |
| weak | 0.3 | 0.983 / 0.999 | 0.983 / 0.995 | 0.010 / 0.000 / 0.001 |
| weak | 1 | 0.980 / 0.998 | 0.980 / 0.969 | 0.016 / 0.000 / 0.022 |

**Calibration**: with the exponential map no w is singled out.  The mode
agrees to within 0.02 at every w at εN = 0.1 (the single-mutant regime),
and the cooperator share is below what 4·10⁶ events can resolve at
εN = 0.1 (≈ 4,000 mutation events × μ(`THEM(^C)`) × ρ ≈ 0.2 expected
entries); at εN = 1 and w = 1 the one observed visit gives 0.022 against the
chain's 0.016.  w is therefore a free intensity whose effect on the
cooperative share is a factor ≈ 3 between w = 0.1 and w = 1 at N = 100 and
≈ 1.1 at N = 1000.  Stag Hunt was not re-run: its payoffs are non-negative,
so 1 + w·payoff never clamped and its w = 1 cells are unaffected by the
change of map (they differ from exp(w·payoff) only by the curvature of the
map, not by a clamp).

## Reference-evaluator check: `and(THEM(^THEM(^C)),not(THEM(^D)))` vs `THEM(^C)`

Exact (floor probability 0, budget 200): `THEM(^C)` plays D against it (P(C) = 0.000, because against ALLC the 13-node program plays and(C, not(C)) = D) and it plays C against `THEM(^C)` (P(C) = 1.000); it cooperates with itself (P(C) = 1) and defects against D, so it is exploited by `THEM(^C)` (u = −2 vs 1) and does not invade all-`THEM(^C)`.

## Ultimatum game (k = 3), three arms (`runs/ult_*.md`, predictions in `predictions/2026-09-19-ultimatum.md`)

Levels L = 0.2 < M = 0.5 < H = 0.8, proposer plays the offer, responder the
threshold, accept iff offer ≥ threshold, payoffs (1−x, x), rejection (0, 0).
Weak arm n = 5 (902 programs without ROLE, 1,586 with), N = 100, w = 0.1,
exp fitness map.  Under the k-ary DSL the binary results are reproduced to
1e-15 (`runs/k2_identity_check.md`).

| arm | prediction | outcome | rejection | share P / R | conditional programs in support |
|---|---|---|---|---|---|
| (a) ROLE, one population | π spread over all-L / all-M / all-H, no concentration > 0.6, rejection 0 | all-M 0.372, all-L 0.349, all-H 0.093, all-X 0.065, all-`ROLE` 0.044 (offers L, demands H: pays 0 against itself), `{X 0.9, flip(ROLE) 0.1}` 0.029. **Not falsified** (max 0.37), but the spread is L/M-heavy: every constant earns 0.5 against itself under role averaging, and the tilt comes from asymmetric exit rates (an H-mutant in all-L loses 0.4, an L-mutant in all-H loses 0.1: all-H is the easiest to leave). | 0.086 | 0.523 / 0.391 | `THEM(ME)`, `THEM(THEM)` at 0.001 each |
| (b) fixed-mutual | (M, M) mode, rejection 0, proposer share 0.5 | **Falsified**: mode (L \| L) 0.387, then (M \| M) 0.191, (M \| L) 0.072, (L \| X) 0.047, (H \| H) 0.030.  (L \| L) is the subgame-perfect outcome: at (L \| L) a responder mutant M or H has its threshold unmet (ρ = 3.2e-3 < 1/N) and a proposer mutant M gives away 0.3 (ρ = 1.6e-3); (M \| M) is left by responder L (neutral, ρ = 1/N) and then (M \| L) → (L \| L) via proposer L (ρ = 0.031). | 0.109 | 0.540 / 0.351 | `(THEM(ME) \| H)`, `(THEM(THEM) \| H)`, `(L \| THEM(ME))` at 0.004 each |
| (c) fixed-one-sided (blind responders) | responders commit to H, proposers accommodate, responder share 0.8 | **Falsified**: identical to (b) to 3 decimals — (L \| L) 0.391, (M \| M) 0.193; responder share 0.352 < 0.7.  Blind responders are constants in effect, so seeing them changes nothing; a blind responder cannot commit, it can only reject, and rejection costs it 0.2 at (L \| L). | 0.110 | 0.538 / 0.352 | `(THEM(ME) \| H)` 0.011 |

What the conditional programs condition on: `THEM(ME)` as proposer ("offer
what you would demand of me") and `THEM(THEM)` ("offer what you demand of
yourself") mirror a constant responder's threshold, so they sit in the
support only paired with H (offer H to an H-responder, payoff 0.2) at
≤ 1%; no third-party probe (`THEM(^A_i)`) appears in any support.  The
Nash-bargaining prediction (M, M) is the second state in both fixed-role
arms at 0.19, not the mode; the mode is the proposer-favouring
subgame-perfect pair, held by the asymmetry that the responder's only
deviation (a higher threshold) is self-punishing while the proposer's
deviation (a higher offer) is merely generous.  Note the stated falsifier
for (a) was not met, but its verdict "no concentration" is at best half
true (0.72 on L+M).

## Ultimatum symmetry break: responder outside option (0, 0.3) on rejection, arm (b)

Predicted: mode shifts toward H (generalised Nash: maximise (1−x)(x−0.3),
x = 0.65, nearest level H).  Outcome (`runs/ult_ult_out_mutual_N100_w0.1.md`):
the mode **does move, upward, but to M**: (M \| M) 0.234 (was 0.191),
(L \| L) 0.102 (was 0.387), (H \| H) 0.073 (was 0.030), (M \| X) 0.083,
(M \| L) 0.077; rejection rate 0.216 (was 0.109), proposer share 0.371 (was
0.540), responder share 0.479 (was 0.351).  The mechanism: with the outside
option a responder mutant M at (L \| L) earns 0.3 > 0.2 by rejecting, so
(L \| L) is no longer stable and drains into (L \| M) → (M \| M); H stays a
minority because at (M \| M) a threshold-H responder still gets only 0.3
vs 0.5.  Direction as predicted; the nearest-level claim (H) is not borne
out — M, not H, is the mode, with H's share doubling.

## Standing variance: agent-based Moran at finite εN (`runs/abm_pd_N100_w0.3.md`, predictions in `predictions/2026-09-20-standing-variance.md`)

Agent-based Moran process (`src/abm.py`): N = 100, weak arm n = 6 **with
ROLE** (3,994 programs, 112 behavioural classes; μ(C) = μ(D) = 0.249,
μ(`THEM(^C)`) = 5.2e-4), PD, f = exp(w·payoff), w = 0.3, mutation per birth
at ε = εN/N with mutants drawn from μ over the classes; burn-in 10⁴
generations, 10⁵ sampled (N events each), 5 seeds.  Cooperative share is
(mean payoff − u(D,D)) / (efficient − u(D,D)) = mean payoff + 1.

| εN | cooperative share (mean ± sd) | `THEM(^C)` class share | ALLC class share | P(`THEM(^C)` and ALLC coexist) | P(C,C) | P(exploit) |
|---|---|---|---|---|---|---|
| 0.1 | 0.011 ± 0.009 | 0.007 ± 0.009 | 0.0015 ± 0.0004 | 0.0008 ± 0.0011 | 0.0075 ± 0.0087 | 0.0066 ± 0.0014 |
| 1 | 0.048 ± 0.004 | 0.016 ± 0.003 | 0.0117 ± 0.0003 | 0.013 ± 0.002 | 0.0202 ± 0.0032 | 0.0564 ± 0.0020 |
| 10 | 0.240 ± 0.001 | 0.0006 ± 0.0001 | 0.089 ± 0.000 | 0.014 ± 0.001 | 0.0610 ± 0.0003 | 0.3577 ± 0.0005 |

P(C,C) is the frequency of mutual-cooperation interactions and P(exploit)
the frequency of (C,D)+(D,C) interactions over all agent pairs (role draw
averaged; rerun 2026-09-20 with the same seeds, the other columns unchanged).
In this PD T + S = −1 > 2P = −2, so exploited pairs are more efficient than
mutual defection and the cooperative-share statistic counts mutation load as
efficiency; P(C,C) is the statistic for conditional cooperation from now on.

Verdict: **not falsified** — the share rises monotonically in εN and stays
below 0.10 at εN = 1 (0.048) and below 0.25 at εN = 10 (0.240, within
0.01 of the bound).  At εN = 0.1 the simulation reproduces the chain
(chain: `THEM(^C)` 0.010 at w = 0.3, N = 100 without ROLE; ABM 0.007 ± 0.009
with `THEM(^C)` present in 2 of 5 seeds' samples, i.e. the visits are rare
and long, as the chain's residence time predicts).  At εN = 1 the
conditional cooperator holds 1.6% and coexists with ALLC in 1.3% of
generations; the shadow mechanism still operates (ALLC is present 1.2% of
the time, entering at μ(C)·ε per birth).  At εN = 10 the cooperative share
is mutation load, not conditional cooperation: ALLC and the coin programs
are present as a standing 9%+ minority that all-D exploits, `THEM(^C)`
holds 0.06% (a tenth of its εN = 1 share), and the mean payoff of −0.76
reflects defectors being paid by a mutational stream of suckers.  Standing
variance therefore does not rescue the conditional cooperator: it raises
the payoff only by keeping unconditional cooperators alive as mutants, and
the conditional program's share peaks at εN ≈ 1 and falls beyond it.
Wall time 3–5 s per 1.1·10⁷-event run after a 545 s chunked evaluation of
the 3,994-program language.

## Spatial structure (`runs/lattice_pd_w0.3.md`, `runs/spatial/*.png`, predictions in `predictions/2026-09-20-spatial.md`)

Death-birth Moran on a 32×32 torus (N = 1024), von Neumann neighbourhood
(k = 4): a random site dies and its 4 neighbours compete to fill it with
probability ∝ exp(w·payoff), payoff being the mean over the neighbour's own
4 interactions; mutation per birth at ε = εN/N from μ over the 112
behavioural classes of L_6 with ROLE (cached evaluation); PD, w = 0.3;
burn-in 10⁴ generations (N deaths), 10⁵ sampled, 5 seeds.  Control: the same
rule on the complete graph at εN = 1.

| graph | εN | P(C,C) | P(exploit) | mean payoff | `THEM(^C)` | ALLC | D | `THEM(^D)` |
|---|---|---|---|---|---|---|---|---|
| lattice | 0.1 | 0.155 ± 0.190 | 0.006 ± 0.007 | −0.84 ± 0.19 | 0.142 ± 0.174 | 0.012 ± 0.016 | 0.837 ± 0.198 | 0.0006 ± 0.0008 |
| lattice | 1 | **0.544 ± 0.093** | 0.030 ± 0.006 | −0.44 ± 0.09 | **0.453 ± 0.077** | 0.084 ± 0.019 | 0.415 ± 0.095 | 0.0024 ± 0.0008 |
| complete | 1 | 0.022 ± 0.025 | 0.007 ± 0.002 | −0.97 ± 0.02 | 0.019 ± 0.023 | 0.003 ± 0.002 | 0.969 ± 0.025 | 0.0011 ± 0.0010 |

Verdicts: lattice εN = 1 P(C,C) > 0.3 **confirmed** (0.54, every seed
between 0.45 and 0.72); `THEM(^C)` share > 0.3 and above ALLC **confirmed**
(0.45 vs 0.08); `THEM(^D)` present at > 0.005 **not confirmed** (0.0024 ± 0.0008,
at its μ-weight); well-mixed control P(C,C) < 0.02 **marginally not
confirmed** (0.022 ± 0.025: three seeds at ≤ 0.007, one at 0.030, one at
0.066 — the well-mixed N = 1024 process at εN = 1 is the chain's PD regime,
`THEM(^C)` 0.019 vs the chain's 0.010–0.018).  The falsifier (lattice
P(C,C) < 0.1) is not triggered.  At εN = 0.1 the lattice is bimodal over
seeds: three seeds never leave all-D in 1.1·10⁵ generations, two spend
~40% of the window cooperative (P(C,C) 0.35, 0.42); the sweep is a rare
event at that mutation rate.

The lattice dynamics are intermittent, not a stable mixture: along seed 0 at
εN = 1 the `THEM(^C)` class is absent for the first ~25,000 generations
(all-D with mutational patches), then sweeps the torus in < 1,000
generations to 0.99, after which ALLC patches grow inside it (0.03 → 0.22
over 3,000 generations) — the shadow at work in space — and, as the
snapshots at the end of sampling show for seeds 0 and 4, the population is
back at all-D by the end of the 1.1·10⁵-generation window (the end-of-window
snapshots caught the defection phase; the time averages above are over the
whole window).  So spatial structure does what source observation could
not: a `THEM(^C)` cluster is on-path *distinguishable* from its shadow,
because a cluster of reciprocators facing D at its boundary keeps its
interior cooperating while a cluster of ALLC is eaten from the boundary in,
and `THEM(^C)` sweeps from a seed at rate ρ ≫ 1/N.  The shadow still
operates afterwards (ALLC drifts into the reciprocator sea, D re-invades),
so the ecology cycles all-D → `THEM(^C)` sweep → ALLC infiltration → D
re-invasion with ~45% of the time cooperative at εN = 1 and P(C,C) = 0.54,
against 0.02 in the well-mixed control of the same size.  `THEM(^D)` plays
no part: it stays at μ-weight on the lattice as it does when well mixed.

### Scaling and traces (`runs/lattice_pd_w0.3.md`, `runs/spatial/trace_*.png`, `runs/spatial/trace_*.npy`; predictions in `predictions/2026-09-20-spatial-scaling.md`)

Same process at sides {32, 64, 128} for εN = 1 and side 32 for εN ∈ {0.3, 3};
burn-in 10⁴ generations, 10⁵ sampled at every side (wall time did not
require scaling down: 8 s, 40 s and 140–480 s per seed), 5 seeds.  Traces
every 100 generations.  Collapse events are `THEM(^C)`-share crossings of
0.5 downward after having exceeded 0.8, with the ALLC share recorded 500
generations before; duty cycle is the fraction of sampled generations with
`THEM(^C)` share > 0.5.  Because at sides ≥ 64 other reciprocators carry
much of the cooperation (below), a payoff-based duty (fraction of trace
records with mean payoff > −0.5, i.e. more than halfway from mutual
defection to efficiency) and payoff-based collapses (payoff crossing −0.5
downward after exceeding −0.2) are given alongside.

| side | εN | P(C,C) | duty (`THEM(^C)` > ½) | collapses | pre-collapse ALLC | payoff-duty | payoff-collapses | pre-collapse ALLC (payoff) | trace |
|---|---|---|---|---|---|---|---|---|---|
| 32 | 0.3 | 0.075 ± 0.108 | 0.07 ± 0.11 | 3 | 0.21 ± 0.19 | 0.08 ± 0.11 | 10 | 0.08 ± 0.25 | [plot](runs/spatial/trace_32_epsN0.3.png) |
| 32 | 1 | 0.544 ± 0.093 | 0.51 ± 0.09 | 67 | 0.13 ± 0.12 | 0.57 ± 0.10 | 34 | 0.19 ± 0.20 | [plot](runs/spatial/trace_32_epsN1.png) |
| 32 | 3 | 0.356 ± 0.046 | 0.23 ± 0.06 | 48 | 0.14 ± 0.10 | 0.42 ± 0.05 | 35 | 0.17 ± 0.10 | [plot](runs/spatial/trace_32_epsN3.png) |
| 64 | 1 | 0.635 ± 0.185 | 0.37 ± 0.35 | 24 | 0.08 ± 0.08 | 0.70 ± 0.16 | 34 | 0.07 ± 0.13 | [plot](runs/spatial/trace_64_epsN1.png) |
| 128 | 1 | 0.615 ± 0.279 | 0.21 ± 0.29 | 13 | 0.06 ± 0.05 | 0.69 ± 0.27 | 14 | 0.04 ± 0.05 | [plot](runs/spatial/trace_128_epsN1.png) |
| complete, N = 1024 | 1 | 0.022 ± 0.025 | — | — | — | — | — | — | — |

Verdicts.  (1) *P(C,C) increases monotonically in side*: 0.54 → 0.63 →
0.61; 64² is above 32², so the falsifier is not triggered, but 128² is not
above 64² (within one sd; the seed spread at 128² is 0.25–0.96).  Rises
from 32² to 64², plateaus at 128².  (2) *Pre-collapse ALLC share > 0.15 and
within ×1.5 across sides*: **falsified** — 0.13, 0.08, 0.06 by the
`THEM(^C)` detector (0.19, 0.07, 0.04 by payoff), below 0.15 at every side
and falling by ×2.2 from 32² to 128².  A collapse needs less global ALLC on
a larger torus because the D front nucleates on a local ALLC cluster, not on
the global density.  (3) *Unimodal in εN with the peak in [0.3, 3]*:
confirmed, 0.075 / 0.544 / 0.356 at εN = 0.3 / 1 / 3.

What the traces show.  At 32² the ecology is the limit cycle already
described, ~15 cycles per 10⁵ generations per seed, `THEM(^C)` saturating
near 1 and ALLC reaching 0.2–0.5 inside it before each collapse.  At 64² and
128² the reciprocator is no longer always `THEM(^C)`: replaying seeds with a
full class histogram (deterministic seeds) gives, at 64², seed 0 =
`or(X,THEM(THEM))` 0.51 + `THEM(^ROLE)` 0.18 + D 0.15 + C 0.12 and seed 4 =
D 0.47 + `or(X,THEM(THEM))` 0.30 + `THEM(^ROLE)` 0.11; at 128², seed 4 =
**`or(X,THEM(ME))` 0.94** (the ½-grounded FairBot of THEORY §7(b), P(C,C) =
0.96, D and C at 0.025 each), seed 0 = D 0.40 + `THEM(^ROLE)` 0.33 + C 0.24
and seed 1 = `THEM(^X)` 0.36 + D 0.35 + C 0.25 — the last two a *standing*
three-way spatial coexistence of a reciprocator, its shadow and the
defector, with ALLC at 0.25–0.35 permanently (the traces' flat dashed
lines), P(C,C) 0.25–0.34.  So the `THEM(^C)`-based duty and collapse counts
undercount at large sides (seed 4 at 128²: duty 0.000, P(C,C) 0.96), which
is why the payoff-based columns are given; the two agree at 32².

Mechanism: entry versus exit.  Entry is pair nucleation.  A single
`THEM(^C)` in a D sea earns −1, the same as its D neighbours, so it is
neutral; two adjacent `THEM(^C)` each earn (0 − 3)/4 = −0.75 > −1 and the
pair grows, so the sweep starts once a mutant's copy lands next to it,
ρ ≈ ¼ per nucleation attempt against 1/N in the well-mixed process — which is
why the torus at εN = 1 sweeps ~15 times per 10⁵ generations while the
complete graph of the same size holds `THEM(^C)` 2% of the time.  Exit is
the ALLC-subsidized D front.  Inside a `THEM(^C)` sea ALLC drifts in
neutrally (the shadow); a D born next to ALLC and `THEM(^C)` with two of
each earns (1 + 1 − 1 − 1)/4 = 0, while the bordering `THEM(^C)` with
neighbours (D, `THEM(^C)`, `THEM(^C)`, C) earns (−1 + 0 + 0 + 0)/4 = −0.25,
so the front advances wherever ALLC is present and stalls where it is not;
the collapse is a local nucleation on an ALLC cluster, hence the falling
pre-collapse ALLC density with side.  FairBot (`or(X,THEM(ME))`) escapes the
exit because a D at its border earns 0 against it and 0 is also FairBot's
self-payoff: the front is neutral, and the seed at 128² that reached
FairBot held it for 94% of the window.  `THEM(^D)` (the faker) stays at
μ-weight in every cell (≤ 0.003).

### Per-mutant rates: the ε→0 object of the torus (`runs/lattice_rates.md`, predictions in `predictions/2026-09-21-lattice-rates.md`)

Death-birth on the torus with mutation off inside each trial (`src/lattice_rates.py`),
weak n=6 with ROLE, w = 0.3, sides 32 and 64.  (a) ρ_enter(R): one copy of R
in all-D, success = R share ≥ ½, 2000 trials.  (b) M_exit(R): from all-R,
mutants drawn one at a time from μ over the 112 classes, each followed to
extinction or fixation (per-mutant cap 1,000 generations, after which the
next mutant is drawn with the lineage still present), counted until the R
share falls below ½, 50 trials.  (c) all-R with one ALLC and one D injected;
lifetimes in generations, 500 trials.

| R | side | ρ_enter | generations to ½ | M_exit (mean ± sd, median) | generations to exit | last mutant at exit | ALLC lifetime mean / median | D lifetime mean / median |
|---|---|---|---|---|---|---|---|---|
| `THEM(^C)` | 32 | 0.109 | 89 | 1,514 ± 1,234 (1,080) | 7,600 | C 37/50, `THEM(^D)` 6, `THEM(^X)` 4 | 22.8 / 1.1 | 1.91 / 0.71 |
| `THEM(^C)` | 64 | 0.113 | 157 | 2,947 ± 2,776 (1,980) | 18,300 | C 20, `THEM(^D)` 14, `THEM(^ROLE)` 8 | 11.8 / 1.0 | 2.58 / 0.83 |
| `or(X,THEM(ME))` | 32 | 0.0065 (13/2000) | 381 | 2,584 ± 1,927 (1,898) | 19,200 | C 48/50 | 7.5 / 0.9 | 5.13 / 1.03 |
| `or(X,THEM(ME))` | 64 | 0.0035 (7/2000) | 829 | 7,486 ± 7,171 (5,649) | 62,400 | C 45/50 | 16.7 / 1.2 | 5.22 / 1.08 |
| `THEM(^ROLE)` | 32 | 0.055 | 151 | 37.8 ± 37.1 (22) | 400 | C 47/50 | — | — |
| `THEM(^ROLE)` | 64 | 0.070 | 261 | 47.7 ± 47.2 (32) | 480 | C 50/50 | — | — |

Verdicts.  (1) *ρ_enter side-independent within ×1.5*: **confirmed** for
`THEM(^C)` (×1.04) and `THEM(^ROLE)` (×1.28); for FairBot the ratio is ×1.9
on 13 vs 7 successes, inconclusive at these counts.  The value for
`THEM(^C)` is 0.11, not the ¼ estimated from the pair-nucleation argument
(a pair earns −0.75 against D's −1, but the first copy must still be placed
by a death-birth event that the lone mutant wins with probability ≈ ¼, and
the pair must then survive its own turnover).  (2) *M_exit side-independent
within ×2*: `THEM(^C)` ×1.95 (at the bound), `THEM(^ROLE)` ×1.26
(**confirmed**), FairBot ×2.9 (**falsified**); none grows ∝ N (×4), so the
lim_N falsifier does not fire either — M_exit grows like N^{0.5–0.8}.  The
exit in this ε→0 protocol is almost always the shadow: in 137 of 200
`THEM(^C)`/FairBot trials the mutant present when the R share crossed ½ was
ALLC, i.e. R was displaced by neutral drift of its own shadow accumulated
across mutants (ALLC lineages outlive the per-mutant cap), with the faker
`THEM(^D)` ending 20 of 100 `THEM(^C)` trials and D never ending one — under
serial single mutants a D never meets enough ALLC to build a front.
`THEM(^ROLE)` (self-payoff −0.5) is displaced by the first ALLC lineage that
takes hold, M_exit ≈ 40.  (3) *Lone-D lifetime in FairBot > 10× that in
`THEM(^C)`*: **falsified** — 5.1 vs 1.9 generations at 32² (5.2 vs 2.6 at
64²), a factor 2–2.7; a lone D in a FairBot sea is nearly neutral (its four
FairBot neighbours earn −0.375 against its 0, but the D site itself is
refilled by FairBot every time it dies), not long-lived.  (4) *ALLC lifetime
in FairBot < in `THEM(^C)`*: **not supported** — medians 0.9 vs 1.1 (32²)
and 1.2 vs 1.0 (64²), means 7.5 vs 22.8 and 16.7 vs 11.8, dominated by rare
long lineages and flipping sign between sides.  The FairBot-pruning
hypothesis (grounding noise makes roaming D neutral and D prunes ALLC) is
dropped (REJECTED.md).

What the ε→0 object says.  With entry rate μ(R)·ρ_enter per mutant and
residence M_exit mutants, the ε→0 time share of all-R from all-D is
M_exit / (M_exit + 1/(μ(R)ρ_enter)): for `THEM(^C)` 1/(μρ) ≈ 17,600 mutants
against M_exit 1,500–2,900, i.e. 8% at 32² and 14% at 64², rising with N only
through the sublinear growth of M_exit; for FairBot 1/(μρ) ≈ 4.8·10⁶ mutants
(μ = 4.2e-5, ρ = 0.005) against M_exit 2,600–7,500, i.e. < 0.2% — FairBot is
not reachable from all-D by single-copy nucleation, and the 128² FairBot sea
must have been reached by another route (neutral drift into a `THEM(^C)`
sea, where FairBot earns 0 against both).  The finite-εN duty cycles of
0.5–0.7 at εN = 1 are therefore not the ε→0 object: they come from
concurrent nucleation attempts during the slow collapse.

## Not done

- Prediction (c) at n=9 through the chain (the enterer search covers what
  L_9 can do against all-D and all-p, but not the full n=9 chain).
- N = 1000 in the weak arm.
- Polymorphic-target ρ beyond the truncated-product approximation.
