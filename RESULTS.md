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

### Mixing check at 128² (`runs/lattice_pd_w0.3_mix128.md`, traces `runs/spatial/trace_128_epsN1_mix128.png`)

128², εN = 1, five new seeds (5–9), burn-in 10⁴ and a sampled window of
3·10⁵ generations (three times the earlier one); per-seed P(C,C) over the
window and the dominant class (share of the sampled records) and P(C,C) in
each third of it:

| seed | P(C,C) | third 1 | third 2 | third 3 |
|---|---|---|---|---|
| 5 | 0.679 | `THEM(^X)` (0.38), 0.36 | `THEM(^C)` (0.54), 0.78 | `THEM(^C)` (0.69), 0.90 |
| 6 | 0.690 | D (0.31), 0.50 | C (0.32), 0.70 | `THEM(^C)` (0.64), 0.86 |
| 7 | 0.955 | `THEM(^C)` (0.77), 0.93 | `THEM(^C)` (0.77), 0.97 | `THEM(^C)` (0.79), 0.96 |
| 8 | 0.826 | `THEM(^C)` (0.57), 0.69 | `THEM(^C)` (0.69), 0.81 | `THEM(^C)` (0.79), 0.98 |
| 9 | 0.634 | `THEM(^ROLE)` (0.27), 0.48 | `or(X,THEM(THEM))` (0.50), 0.63 | `THEM(^C)` (0.38), 0.79 |

The seeds converge.  Whatever the first third holds — a `THEM(^X)` or
`THEM(^ROLE)` coexistence, a D/C phase, an `or(X,THEM(THEM))` sea — by the
last third every seed is a `THEM(^C)` sea with P(C,C) between 0.79 and 0.98
(spread 0.19 against 0.71 across the five earlier seeds at 1.1·10⁵
generations), and P(C,C) rises monotonically through the thirds in four of
five seeds.  The 1.1·10⁵-generation window of the scaling table was shorter
than the mixing time at 128²; its seed spread was a spread over transient
basins, not over π, as REJECTED.md already records.  The converged 128²
state is the `THEM(^C)` limit cycle with a high duty (collapses still occur —
5 to 33 per seed — but recover within the third), P(C,C) ≈ 0.8–1.0 at
εN = 1.  This is a finite-εN approach rate, not the ε→0 object of the
previous subsection, where the same regime holds 14% of the time at 64²: at
εN = 1 on 16,384 sites, nucleation attempts are concurrent with the slow
ALLC-subsidized collapse, and the sea is re-seeded before it is lost.

## Island model: migration replaces mutation (`runs/islands_*.md`, `runs/islands_*.json`; predictions in `predictions/2026-09-23-islands.md`)

`src/islands.py`: 64 islands of N = 100 on a complete graph or a ring. A
random agent dies and is replaced by a local birth, or with probability m by
the offspring of a parent drawn by fitness on a random neighbouring island.
Fitness is exp(0.3 · mean payoff) against the parent's own island; mN is 0.1
or 1 migrants per island per generation. **There is no mutation.** Each of
four seedings places every program of L_6 at least once (6,400 slots):
programs (the rest uniform over programs), prior (the rest from μ), hostile
(the rest A_0) and clustered (dealt in class order, so each class occupies as
few islands as possible). The horizon is 2·10⁵ generations and statistics
come from the second half. A run stops when it is frozen, meaning every
surviving pair of classes has the same payoff; the frozen state then stands
for the remainder. There are 20 replicates per cell.

### PD

| graph | mN | seeding | P(C,C) mean ± sd | payoff | island-time DWL > 0.1 | frozen (median gen) | frozen: all-`THEM(^C)` / mutual D / other | `THEM(^C)` extinct |
|---|---|---|---|---|---|---|---|---|
| complete | 0.1 | programs | 0.315 ± 0.415 | -0.487 | 0.75 | 2580 | 5 / 5 / 10 | 15 |
| complete | 0.1 | prior | 0.388 ± 0.429 | -0.450 | 0.70 | 2650 | 6 / 5 / 9 | 14 |
| complete | 0.1 | hostile | 0.200 ± 0.348 | -0.581 | 0.85 | 2680 | 3 / 5 / 12 | 17 |
| complete | 0.1 | clustered | 0.188 ± 0.315 | -0.650 | 0.90 | 2250 | 2 / 9 / 9 | 18 |
| complete | 1 | programs | 0.228 ± 0.351 | -0.650 | 0.85 | 370 | 3 / 9 / 8 | 17 |
| complete | 1 | prior | 0.244 ± 0.396 | -0.637 | 0.80 | 380 | 4 / 9 / 7 | 16 |
| complete | 1 | hostile | 0.215 ± 0.354 | -0.600 | 0.85 | 380 | 3 / 6 / 11 | 17 |
| complete | 1 | clustered | 0.062 ± 0.092 | -0.762 | 1.00 | 470 | 0 / 8 / 12 | 20 |
| ring | 0.1 | programs | 0.294 ± 0.377 | -0.475 | 0.80 | 14250 | 4 / 3 / 13 | 16 |
| ring | 0.1 | prior | 0.403 ± 0.419 | -0.438 | 0.70 | 13060 | 6 / 4 / 10 | 14 |
| ring | 0.1 | hostile | 0.234 ± 0.337 | -0.500 | 0.85 | 16630 | 3 / 2 / 15 | 17 |
| ring | 0.1 | clustered | 0.204 ± 0.320 | -0.613 | 0.90 | 19060 | 2 / 6 / 12 | 18 |
| ring | 1 | programs | 0.285 ± 0.340 | -0.450 | 0.85 | 1860 | 3 / 1 / 16 | 17 |
| ring | 1 | prior | 0.171 ± 0.353 | -0.738 | 0.85 | 1370 | 3 / 12 / 5 | 17 |
| ring | 1 | hostile | 0.432 ± 0.435 | -0.412 | 0.65 | 2030 | 7 / 4 / 9 | 13 |
| ring | 1 | clustered | 0.166 ± 0.318 | -0.694 | 0.90 | 2090 | 2 / 9 / 9 | 18 |

**Every PD run freezes**, at a median of 2,170 generations (max 40,280).
Without mutation the island model is not ergodic, and a replicate is one
draw from an absorption lottery over three families:

- **All-`THEM(^C)`**: P(C,C) = 1, in 56 of 320 runs.
- **Mutual defection**: D, `THEM(^D)`, `and(X,THEM(^D))` and the `THEM(ME)`-and-D
  family, all mutually neutral at −1, in 97 runs.
- **Exploitation probes**: `THEM(^ROLE)`, `THEM(^X)`, `THEM(^or(X,ROLE))`,
  `THEM(^and(X,ROLE))` and the like, in 167 runs. Each copies a non-constant
  third party (`THEM(^ROLE)` plays against you what you play against
  `ROLE`), so against itself it reproduces `ROLE` against `ROLE`, an (C,D) pair
  every match. Payoff is −0.25 to −0.875, and P(C,C) is 0 to 0.56.

The persistent island-states are the absorbing ones. B′ is falsified in
every cell: 0.65–1.00 of second-half island-time has DWL > 0.1.

**The spoiler is the faker.** Island dominant-class changes out of
`THEM(^C)` were sampled every 20 generations and pooled over all runs, 2,358
in total:

| destination | exits |
|---|---|
| strict faker (earns more against `THEM(^C)` than `THEM(^C)` earns against itself): `THEM(^ROLE)`, `THEM(^X)`, `THEM(^D)`, `THEM(^or(X,ROLE))`, … | 1,901 |
| weak faker (earns 0 against it while `THEM(^C)` is exploited): `and(X,THEM(^D))`, `and(ROLE,THEM(^D))`, … | 437 |
| D | 18 |
| an on-path-identical shadow (ALLC-like) | 0 |
| other | 2 |

The shadow is consumed before it can matter. ALLC is extinct in all 320
runs, at a median of generation 40 and by generation 1,320 at the latest.
Shadow islands were taken by a class exploiting the shadow 945 times, the
subsidized-front route. Transitions are pooled over time, so these cannot be
dated. They do not end `THEM(^C)` islands, because no `THEM(^C)` island ever
became a shadow island. `THEM(^C)`
itself is lost early: 264 runs lose it, 168 of them within 100 generations,
during the first within-island scramble. Where it survives it nucleates
readily. Of 5,817 island entries into `THEM(^C)`, 5,404 are from D. It holds
only when every faker has gone extinct first.

**Conjecture A.**
- *Set level: holds.* All three absorbing families occur under every seeding.
- *Distribution level: fails for placement, not for composition.* Pooled over
  graphs and migration rates, cooperative absorption comes out as follows:

  | seeding | cooperative absorption | Fisher p against the rest |
  |---|---|---|
  | programs | 15 / 80 | |
  | prior | 19 / 80 | |
  | hostile | 16 / 80 | |
  | clustered | 6 / 80 | 0.006 |

  Filling every spare slot with D does not hurt cooperation. Concentrating
  each class on a few islands does.
- *Cell spread.* Within each graph × mN, the seeding means of P(C,C) spread
  by 0.18–0.27, against a standard error of about 0.08 per mean. A single
  cell can therefore not resolve seeding effects smaller than about 0.2.

**The migration game mispredicts.** Its equilibrium set, the replicator
time-average of ρ − ρᵀ over monomorphic island-states, is entirely
mutual-defection classes. The runs absorb into all-`THEM(^C)` in 17.5% of
cases and into exploitation-probe states in 52%. Neither is in the set. With
64 islands, classes go globally extinct within about 10³ generations, and at
ε = 0 each extinction is permanent. The dynamics reach the boundary long
before a time average could form.

### Chicken with `ROLE`

| graph | mN | seeding | payoff mean ± sd | P(Swerve,Swerve) | island-time DWL > 0.1 | island-time DWL ≥ 0.45 | frozen (payoff at freeze) |
|---|---|---|---|---|---|---|---|
| complete | 0.1 | programs | 0.480 ± 0.025 | 0.029 | 0.07 | 0.029 | 1 (0.5) |
| complete | 0.1 | hostile | 0.421 ± 0.161 | 0.150 | 0.18 | 0.150 | 4 (all at 0.5) |
| complete | 0.1 | clustered | 0.473 ± 0.028 | 0.040 | 0.09 | 0.040 | 0 |
| complete | 1 | programs | 0.409 ± 0.141 | 0.104 | 0.33 | 0.109 | 7 (at 0 and 0.5) |
| complete | 1 | hostile | 0.411 ± 0.117 | 0.053 | 0.33 | 0.071 | 5 (all at 0.5) |
| complete | 1 | clustered | 0.380 ± 0.129 | 0.127 | 0.41 | 0.131 | 2 (0.5, 0.5) |
| ring | 0.1 | programs | 0.487 ± 0.011 | 0.021 | 0.05 | 0.011 | 0 |
| ring | 0.1 | hostile | 0.485 ± 0.016 | 0.027 | 0.06 | 0.015 | 0 |
| ring | 0.1 | clustered | 0.418 ± 0.083 | 0.162 | 0.24 | 0.090 | 1 (0.5) |
| ring | 1 | programs | 0.432 ± 0.102 | 0.070 | 0.22 | 0.075 | 1 (0.5) |
| ring | 1 | hostile | 0.453 ± 0.073 | 0.056 | 0.15 | 0.057 | 1 (0.5) |
| ring | 1 | clustered | 0.394 ± 0.124 | 0.166 | 0.30 | 0.118 | 0 |

In the table, payoff is 0.5 at the correlated optimum. A run is frozen when a
single convention has taken every island.

`ROLE` conventions dominate: `ROLE` holds 0.22–0.54 of dominant-island-time
and `not(ROLE)` up to 0.38. In the ring at mN = 0.1 under the shuffled
seedings they keep payoff within 0.02 of 0.5. Of the 22 frozen runs, 21 froze
into a single convention. Mutual-Swerve islands also
persist, in the self-referential `THEM(ME)` family:

| class | cell | share of dominant-island-time |
|---|---|---|
| `not(or(THEM(THEM),X))` | complete, mN = 0.1, hostile | 0.14 |
| `not(or(THEM(THEM),X))` | complete, mN = 1, programs | 0.10 |
| `not(or(THEM(THEM),X))` | ring, mN = 1, clustered | 0.08 |
| `not(or(THEM(ME),X))` | complete, mN = 1, clustered | 0.05 |

These islands sit at payoff 0, because their self-play diverges to the minimax
action Swerve. One run of 240 froze globally in that state (complete,
mN = 1). B′ is therefore falsified in Chicken with `ROLE`, but narrowly. The
remaining deadweight loss at mN = 1 is mostly migration load: a `not(ROLE)`
migrant on a `ROLE` island crashes half its matches. Conjecture A holds at
the outcome level. Within each graph × mN, the seeding means of payoff differ
by 0.03–0.07.

### Chicken without `ROLE`

| graph | mN | seeding | payoff mean ± sd | P(Swerve,Swerve) | island-time DWL > 0.1 | island-time DWL ≥ 0.45 | frozen (payoff at freeze) |
|---|---|---|---|---|---|---|---|
| complete | 0.1 | programs | -0.216 ± 0.135 | 0.670 | 1.00 | 1.000 | 0 |
| complete | 0.1 | hostile | -0.184 ± 0.077 | 0.702 | 1.00 | 1.000 | 0 |
| complete | 0.1 | clustered | -0.127 ± 0.133 | 0.806 | 1.00 | 1.000 | 5 (all at 0) |
| complete | 1 | programs | -0.343 ± 0.093 | 0.486 | 1.00 | 0.999 | 1 (0) |
| complete | 1 | hostile | -0.271 ± 0.081 | 0.575 | 1.00 | 1.000 | 0 |
| complete | 1 | clustered | -0.142 ± 0.115 | 0.784 | 1.00 | 1.000 | 4 (all at 0) |
| ring | 0.1 | programs | -0.202 ± 0.121 | 0.686 | 1.00 | 1.000 | 0 |
| ring | 0.1 | hostile | -0.173 ± 0.080 | 0.720 | 1.00 | 1.000 | 0 |
| ring | 0.1 | clustered | -0.159 ± 0.119 | 0.751 | 1.00 | 1.000 | 2 (0, 0) |
| ring | 1 | programs | -0.353 ± 0.065 | 0.470 | 1.00 | 1.000 | 0 |
| ring | 1 | hostile | -0.292 ± 0.098 | 0.551 | 1.00 | 1.000 | 1 (0) |
| ring | 1 | clustered | -0.159 ± 0.103 | 0.747 | 1.00 | 1.000 | 4 (all at 0) |

Every island-sample has DWL above 0.45, against the correlated optimum of 0.5.
At mN = 0.1 under the shuffled seedings, the islands sit at the mixed
equilibrium:

| | observed | mixed equilibrium |
|---|---|---|
| payoff | −0.17 to −0.22 | −2/11 = −0.18 |
| P(Swerve,Swerve) | 0.67–0.72 | (9/11)² = 0.67 |

The route is a polymorphism, not mixing programs. The dominant classes are
self-referential best-responders: `not(THEM(ME))`, `not(THEM(THEM))` and
`THEM(^Swerve)`. They swerve against a Straight player and against each
other, the latter by divergence to the minimax action. A Straight minority
lives among them, with the constant Straight at a global share of 0.10 ± 0.06
at the end of the live mN = 0.1 runs, and it earns 2 against each of them.
The minority grows until the two earn the same, which is the mixed
equilibrium in population form. At mN = 1, migration adds Straight load, and
payoff falls to −0.27 to −0.35. Under the clustered seeding the Straight
players are sometimes lost globally: 15 of 17 frozen runs are clustered, and
all freeze at mutual Swerve, payoff 0. That raises the clustered means to
−0.13 to −0.16. None of these states approaches 0.5, so the falsifier THEORY
§9.5 names (Chicken without `ROLE` persisting at the mixed equilibrium) fires,
as THEORY predicted.

### Verdicts against `predictions/2026-09-23-islands.md`

| # | prediction | outcome |
|---|---|---|
| 1 | B′ falsified in the PD; every cell P(C,C) < 0.2; island-time at P(C,C) < 0.1 ≥ 0.8 | **B′ falsified: holds.** The level **failed**: P(C,C) is 0.06–0.43, below 0.2 in 4 of 16 cells, and island-time at P(C,C) < 0.1 is 0.37–0.78. The level falsifier (any cell ≥ 0.5) did not fire. |
| 2 | faker exits outnumber shadow exits at least 2:1 | **Holds.** Strict fakers 1,901, weak fakers 437, shadow 0. |
| 3 | ALLC below 0.01 by generation 1,000 and extinct in ≥ 90% of runs | **Holds.** Maximum share at generation 1,000 is 0.007, and ALLC is extinct in 320 of 320 runs. |
| 4 | `THEM(^C)` extinct in ≥ half of complete mN = 0.1 runs, then a freeze into on-path defection | **Extinction holds** (64 of 80). **The freeze into defection failed**: of those 64, 40 froze into exploitation-probe states at payoff −0.25 to −0.875 and 24 into mutual defection. |
| 5 | A in the PD holds at the outcome level, with seedings within 0.1; fails at the class level, with hostile D-share more than 0.2 above programs | **Failed on both counts.** Seeding spreads are 0.18–0.27. The falsifier (more than 0.2 apart) fired in ring mN = 1 (0.43 against 0.17) and sits at the boundary in complete mN = 0.1 (0.200). The clustered seeding is the one that differs, at p = 0.006. The hostile D-share is not above the programs D-share (0.11 against 0.12 in complete mN = 0.1). |
| 6 | B′ falsified in Chicken with `ROLE`: ≥ 0.1 island-time at DWL ≥ 0.45 in some cell | **Holds** in 3 of 12 cells (0.15, 0.13, 0.11), with one global freeze at mutual Swerve. |
| 7 | A fails at the outcome level in Chicken with `ROLE` | **Failed.** Seeding spreads are 0.03–0.07. |
| 8 | Chicken without `ROLE` at mutual Swerve, payoff in [−0.1, 0.1] | **Failed.** Islands sit at the mixed equilibrium, as THEORY §9.5 predicted. My prediction took the migration game's monomorphic equilibria for the persistent states and missed the polymorphism. |
| 9 | ring and mN = 1 do not change verdicts 1, 6 and 8 | **Holds** for 1 and 8. For 6 it holds in three of four graph × mN (ring mN = 0.1 peaks at 0.090). |

The migration game, meaning the equilibrium set of ρ − ρᵀ over monomorphic
island-states, was the basis of verdicts 1, 4, 6 and 8. It is not the ε-free
object of this model. At ε = 0 with 64 islands, the PD reaches absorbing
states within about 10³ generations, so the dynamics are extinction-driven,
not time-averaged. In Chicken, island-states are polymorphic.

## lim_N of the chain with `ROLE`: the shadow is finite-N, the faker is the limit (`runs/limN_pd.md`, predictions in `predictions/2026-09-28-limN-chain.md`)

`src/limN.py` runs the ε→0 chain for the weak PD (L_6 with `ROLE`, exp fitness map). It splits the exits
from all-`THEM(^C)` by mutant type:
- **shadow:** on-path identical to `THEM(^C)`, meaning C and eight grounded or `ROLE`-guarded variants;
- **faker:** earns more against `THEM(^C)` than `THEM(^C)` earns against itself, 13 classes;
- **other.**

| w | N | π(all-D) | π(all-`THEM(^C)`) | P(C,C) | ρ_enter | shadow share of exits | faker share of exits |
|---|---|---|---|---|---|---|---|
| 0.1 | 100 | 0.9709 | 0.0037 | 0.0069 | 2.48e-02 | 0.72 | 0.03 |
| 0.1 | 300 | 0.9866 | 0.0078 | 0.0087 | 1.44e-02 | 0.88 | 0.11 |
| 0.1 | 1,000 | 0.9847 | 0.0115 | 0.0119 | 7.92e-03 | 0.71 | 0.29 |
| 0.1 | 3,000 | 0.9849 | 0.0126 | 0.0129 | 4.59e-03 | 0.45 | 0.55 |
| 0.1 | 10,000 | 0.9882 | 0.0101 | 0.0103 | 2.52e-03 | 0.20 | 0.80 |
| 0.1 | 30,000 | 0.9920 | 0.0068 | 0.0068 | 1.45e-03 | 0.08 | 0.92 |
| 0.3 | 100 | 0.9865 | 0.0077 | 0.0086 | 4.21e-02 | 0.89 | 0.10 |
| 0.3 | 300 | 0.9847 | 0.0112 | 0.0117 | 2.46e-02 | 0.74 | 0.26 |
| 0.3 | 1,000 | 0.9845 | 0.0130 | 0.0132 | 1.36e-02 | 0.47 | 0.53 |
| 0.3 | 3,000 | 0.9872 | 0.0110 | 0.0111 | 7.92e-03 | 0.23 | 0.77 |
| 0.3 | 10,000 | 0.9915 | 0.0072 | 0.0073 | 4.35e-03 | 0.08 | 0.92 |
| 0.3 | 30,000 | 0.9945 | 0.0044 | 0.0045 | 2.52e-03 | 0.03 | 0.97 |
| 1 | 100 | 0.9841 | 0.0116 | 0.0121 | 7.42e-02 | 0.77 | 0.23 |
| 1 | 300 | 0.9831 | 0.0141 | 0.0144 | 4.41e-02 | 0.52 | 0.48 |
| 1 | 1,000 | 0.9856 | 0.0125 | 0.0127 | 2.46e-02 | 0.25 | 0.75 |
| 1 | 3,000 | 0.9898 | 0.0088 | 0.0089 | 1.44e-02 | 0.10 | 0.90 |
| 1 | 10,000 | 0.9937 | 0.0052 | 0.0053 | 7.92e-03 | 0.03 | 0.97 |
| 1 | 30,000 | 0.9959 | 0.0031 | 0.0031 | 4.59e-03 | 0.01 | 0.99 |

**Support and transitions.** The support is all-D and all-`THEM(^C)` in every cell. At w = 0.1 and
N = 100 it also includes all-X (0.008) and all-`ROLE` (0.006). Polymorphic mass is at most 6·10⁻⁸ and
no transition is indeterminate. Cooperation has one road in and two roads out:
- **In:** all-D goes to all-`THEM(^C)` via the `THEM(^C)` mutant, at ρ_enter.
- **Out, shadow:** all-`THEM(^C)` goes to all-C by ALLC drift, μ(C)/N, and all-C then falls to D.
- **Out, faker:** all-`THEM(^C)` goes to the faker states `THEM(^D)`, `THEM(^X)` and `THEM(^ROLE)`. Their
  shares are about 0.47, 0.24 and 0.23 of the faker flow. These states are on-path D and return to all-D
  by drift.

**The two-state reduction is exact.** π(all-`THEM(^C)`) equals π(all-D) × entry / exit to within 2% in
every cell, so all the N-dependence sits in three rates:
- **Entry** ρ_enter falls like N^(−1/2). The fitted slope over N ∈ [1,000, 30,000] is −0.498, −0.497 and
  −0.494 at w = 0.1, 0.3 and 1.
- **Shadow exit** falls like 1/N: μ(C)/N = 2.49·10⁻³ at N = 100 and 8.3·10⁻⁶ at N = 30,000.
- **Faker exit** is flat: 1.0·10⁻⁴, 2.9·10⁻⁴ and 7.6·10⁻⁴ per mutation event at w = 0.1, 0.3 and 1,
  from N = 100 to 30,000.

The faker share of exits crosses ½ at N ≈ 3,000, 1,000 and 300 for w = 0.1, 0.3 and 1. It reaches
0.92–0.99 at N = 30,000. π(all-`THEM(^C)`) peaks at the crossing, at 0.013–0.014 for every w, and then
falls. From the peak to N = 30,000 it drops by a factor of 1.9, 3.0 and 4.6. Its log-slope over
N ∈ [3,000, 30,000] is −0.27, −0.40 and −0.45, approaching the asymptotic −½.

The earlier reading that the PD limit was answered at N = 1,000 with 1.5–2.4% cooperation (RESULTS,
"Exponential fitness map", without `ROLE`) sampled the peak. The limit is 0, like N^(−1/2), and the
binding exit is the faker, not the shadow. The shadow dominates exits only for N below the crossing.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 1 | Rise, peak and fall; peak within one grid step of 3,000 / 1,000 / 300; the N = 30,000 value at most 1/1.5 of the peak | **Holds.** The peaks are exactly at 3,000 / 1,000 / 300, with factors 1.9 / 3.0 / 4.6. |
| 2 | Faker share within 0.1 of the static single-edge rates; above 0.9 at N = 30,000 | **Holds** to within 0.01. This is close to tautological: the chain's exits from a monomorphic state are exactly its single-edge μ·ρ. The substantive part is that no other route carries weight, which the two-state reduction confirms. |
| 3 | ρ_enter slope in [−0.55, −0.45] | **Holds:** −0.494 to −0.498. |
| 4 | P(C,C) < 0.05 and all-D ≥ 0.9 everywhere | **Holds:** P(C,C) ≤ 0.015, all-D ≥ 0.971. |
| 5 | No polymorphic state at π ≥ 10⁻³; polymorphic flow < 10⁻⁴ | **Holds.** Faker states, expected in the support, stay below 10⁻³. They drain to all-D faster than they are entered. |

The falsifier did not fire. At w = 0.3, N = 30,000 gives 0.0044 against 0.0130 at N = 1,000, and the
shadow share at N = 10,000 is at most 0.20.

## Cool check: payoff dispersion per island vs migration rate (`runs/cool_check.md`, predictions in `predictions/2026-09-28-cool-check.md`)

`src/cool_check.py` runs Chicken without `ROLE` with the programs seeding on a complete graph, replicate 0,
for 5·10⁴ generations. At every sample in the second half it logs each island's **spread**, the
agent-weighted SD of payoff, which is 0 iff the island is cool. It also logs the **resident range**,
max − min payoff over classes holding at least 5% of the island.

| N | I | mN | spread | resident range | cool island-samples | mean payoff | P(Swerve,Swerve) | frozen at |
|---|---|---|---|---|---|---|---|---|
| 100 | 64 | 0.01 | 0.000 | 0.000 | 1.00 | 0.000 | 1.000 | 11,380 |
| 100 | 64 | 0.03 | 0.059 | 0.158 | 0.68 | −0.062 | 0.897 | – |
| 100 | 64 | 0.1 | 0.161 | 0.343 | 0.00 | −0.414 | 0.399 | – |
| 100 | 64 | 0.3 | 0.236 | 0.670 | 0.02 | −0.289 | 0.550 | – |
| 100 | 64 | 1 | 0.267 | 0.771 | 0.00 | −0.342 | 0.478 | – |
| 100 | 64 | 3 | 0.182 | 0.492 | 0.00 | −0.194 | 0.676 | – |
| 400 | 16 | 0.01 | 0.142 | 0.418 | 0.00 | −0.348 | 0.436 | – |
| 400 | 16 | 0.1 | 0.142 | 0.417 | 0.00 | −0.348 | 0.436 | – |
| 400 | 16 | 1 | 0.142 | 0.416 | 0.00 | −0.350 | 0.435 | – |

The replicate is dominated by which state each run fell into, not by migration.

- **N = 100, mN = 0.01.** Straight players were lost globally and the run froze at mutual Swerve, so every
  island is trivially cool.
- **N = 100, mN = 0.03.** Two thirds of island-samples are all-Swerve.
- **N = 100, mN = 0.1.** The islands hold `not(THEM(ME))` (0.63) with `not(or(X,THEM(ME)))` (0.37).
- **N = 400 at every mN, and N = 100 at mN = 1.** The islands hold a three-class mixture: the
  best-responder `not(THEM(THEM))`, the constant Straight, and the conditional Straight
  `not(THEM(^Straight))`. The two Straight players split the role between them: when they meet, the
  constant goes straight and the conditional one swerves.

**The three-class mixture is a cool state.** Its interior rest point is (0.659, 0.195, 0.146), with a common
payoff of −0.341. The global composition of the N = 400 runs is (0.664, 0.194, 0.143) at a mean payoff of
−0.348. The islands therefore sit on a cool rest point on average, and aggregating each island into the
mixed strategy of its rest point reproduces the payoff to within 0.01.

**The rest point is worse than the mixed equilibrium.** It pays −0.341, against −2/11 = −0.182 at the
mixed equilibrium. Coolness is an equilibrium property, not an efficiency property.

**The instantaneous spread around the rest point is drift, not migration.**
- At N = 400 it is 0.142 at mN = 0.01, 0.1 and 1, flat over a 100-fold range.
- At the same rest point, it is 0.267 at N = 100 and mN = 1, against 0.142 at N = 400. The ratio is 0.53,
  against N^(−1/2) = 0.5. This comparison is post hoc: the cell designated for the floor test,
  N = 100 at mN = 0.01, froze.
- Within runs, islands with a larger spread earn less. The correlation between spread and payoff is −0.2 to
  −0.7.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 1 | Spread rises with mN at N = 100 | **Failed.** The spread is 0 (frozen), then 0.06, 0.16, 0.24, 0.27, then falls to 0.18 at mN = 3. Across mN the runs sit in different states, so the curve compares attractors, not migration rates. |
| 2 | Drift floor 0.05–0.3 at N = 100 and mN = 0.01; N = 400 / N = 100 ratio of 0.35–0.7 there | **Not testable** at the designated cell, which froze. The post-hoc same-state comparison gives a ratio of 0.53, inside the band. The falsifier, spread ≤ 0.02 with Straight players present, did not fire. |
| 3 | Load non-decreasing in mN; Spearman(spread, load) ≥ 0.9 | **Failed:** Spearman 0.66, and the load is non-monotone. The load baseline is the frozen all-Swerve run, so "load" here measures attractor switching. At N = 400 the load is 0 to within 0.002 across mN. |
| 4 | Payoff within 0.05 of −0.182 at mN = 0.01 and N = 100, unless frozen | **The exception applies:** frozen at mutual Swerve, payoff 0. |

**Conclusion for the conversation's claim.** "Each program earns the same against its island in the limit" holds
in two senses:
- time-averaged composition sits on a cool rest point;
- the instantaneous spread shrinks like N^(−1/2).

It does not hold as "the spread shrinks as migration → 0" at fixed N. At N = 400 migration moves neither the
spread nor the payoff. Migration's effect is on which cool state, or which absorbing state, the islands occupy.

## Regret witnesses of persistent states (`runs/regret_witnesses.md`, predictions in `predictions/2026-09-30-regret-witnesses.md`)

`src/regret.py` computes r(q) = u(q, σ) − u(σ, σ) over every class q, for states taken from earlier runs.
This is a post-hoc analysis with no new simulation. A state is no-regret iff max r ≤ 10⁻⁹, which for a
symmetric population is a symmetric Nash equilibrium of the program game.

| game | state | payoff | max regret | witness |
|---|---|---|---|---|
| PD | all-D | −1 | 0 | — |
| PD | all-`THEM(^C)` | 0 | 1 = T − R | `THEM(^D)` (the shadow C has 0) |
| PD | all-X, all-`ROLE` | −0.5 | 0.5 | D |
| PD islands | frozen all-`THEM(^C)` (56) | 0 | 1 in every run | `THEM(^D)`, extinct |
| PD islands | frozen mutual defection (97) | −1 | 0 in 38 runs; median 0.013, max 1.99 | `not(THEM(ME))` ×23, `THEM(^C)` ×12, `not(THEM(^C))` ×11 |
| PD islands | frozen exploitation probes (167) | −0.25 to −0.875 | > 0 in every run; median 0.75 | `not(and(THEM(ME),ROLE))` ×55, `C` ×44, `or(ROLE,THEM(^D))` ×37 |
| Chicken + `ROLE` | all-`ROLE`, all-`not(ROLE)` | 0.5 | 0 | — |
| Chicken + `ROLE` | all-`THEM(ME)`, all-`not(or(THEM(THEM),X))`, all-`not(or(THEM(ME),X))` | 0 | **0** | — |
| Chicken, no `ROLE` | mixed equilibrium: `not(THEM(ME))` 9/11 + Straight 2/11 | −0.182 | 1.636 | `not(THEM(^Straight))` |
| Chicken, no `ROLE` | three-class state (27/41, 8/41, 6/41) | −14/41 = −0.341 | **0** (exact rest point) | — |
| Chicken, no `ROLE` | `not(THEM(ME))` 0.627 + `not(or(X,THEM(ME)))` 0.372 | −0.352 | 0.164 | `not(THEM(^Straight))` |

**The Chicken mutual-Swerve states are no-regret.** `THEM(ME)` and its relatives are mirrors: they go
straight against a Straight player, so Straight earns −10 against them. The islands that persisted at
payoff 0 in Chicken with `ROLE` are symmetric Nash equilibria of the program game, not artifacts of ε = 0.
In the ε→0 chain their only exits are neutral drift, which vanishes like 1/N. So in lim_N they compete with
the `ROLE` conventions on drift rates alone. That is untested: the Chicken chain results are at N ≤ 1,000.

**Chicken without `ROLE`: a no-regret state below the mixed equilibrium.**
- The mixed-equilibrium state is strongly invaded by `not(THEM(^Straight))`. That program goes straight
  against the swerver and swerves against Straight. Its regret is 1.64.
- It invades until the three-class state `not(THEM(THEM))` 27/41, Straight 8/41, `not(THEM(^Straight))` 6/41,
  which is an exact no-regret rest point.
- That state pays −14/41 = −0.341. This is the state the N = 400 islands held in the cool check.

Selection over programs moved this game from its base-game mixed equilibrium to a program-game Nash
equilibrium that is worse for everyone.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 1 | PD all-D no-regret | **Holds** |
| 2 | all-`THEM(^C)` regret 1 by a faker; shadow 0 | **Holds** |
| 3 | all-X and all-`ROLE` positive, D a witness | **Holds** (0.5, D) |
| 4 | frozen PD island states | Cooperative and exploitation-probe runs **hold**. For mutual defection: every no-regret run has a sucker-cooperating share ≤ 1/3 (max 0.33), but "regret > 0 iff that share > 1/3" **fails**. 59 positive-regret runs have other witnesses, such as `not(THEM(ME))` and `THEM(^C)`, at shares down to 0. |
| 5 | Chicken + `ROLE`: conventions no-regret; mutual-Swerve islands positive regret | Conventions **hold**. The mutual-Swerve part **fails**: regret 0, protected by mirrors. |
| 6 | Chicken no `ROLE`: mixed-eq regret ≈ 1.6 by `not(THEM(^Straight))`; three-class state positive | Mixed-equilibrium part **holds** (1.636, that witness). The three-class part **fails**: it is exactly no-regret. |

The falsifier (all-D positive, a non-faker top witness of all-`THEM(^C)`, a positive-regret convention,
or a wrong mixed-eq witness) did not fire.

## Island-level selection on emigration (`runs/multilevel_pd.md`, predictions in `predictions/2026-09-30-multilevel.md`)

`src/islands.py` gains mutation and payoff-weighted emigration. The mutation rate is εN = 0.1 per island
per generation. A migrant's source island is drawn among the neighbours with probability proportional to
exp(w_g · island mean payoff).

Setup: PD, weak L_6 with `ROLE`; 64 islands of N = 100 on a complete graph; mN = 1 migrant per island per
generation; w = 0.3 within islands. Every island starts all-D. Each run is 5·10⁵ generations, with 5
replicates per w_g. This is a finite-εN run, so it measures an approach rate and tests a mechanism; it is not
the ε→0 object. Island weighting by mean payoff approximates policy regret at the island level. Because it
weights islands by payoff, it sits close to rule 3.

| w_g | P(C,C), 2nd half | P(C,C), 1st half | payoff | exits from `THEM(^C)` islands: faker / shadow / other | dominant classes, replicate 0 |
|---|---|---|---|---|---|
| 0 | 0.129 ± 0.023 | 0.140 | −0.786 | 6,582 / 4,286 / 341 | D 0.71, `THEM(^ROLE)` 0.13, `THEM(^X)` 0.04, `THEM(^C)` 0.03 |
| 1 | 0.148 ± 0.023 | 0.141 | −0.763 | 6,188 / 3,375 / 357 | D 0.63, `THEM(^ROLE)` 0.13, `THEM(^X)` 0.11, C 0.06 |
| 3 | 0.233 ± 0.016 | 0.226 | −0.669 | 2,225 / 1,159 / 370 | D 0.43, `THEM(^X)` 0.26, C 0.12, `and(X,THEM(ME))` 0.11 |
| 10 | 0.748 ± 0.065 | 0.730 | −0.217 | 61,382 / 188,546 / 6,948 | `THEM(^C)` 0.61, D 0.16, C 0.12, X 0.02 |

**It rescues cooperation, but only at a high intensity.** P(C,C) rises monotonically, but it stays below
0.25 until w_g = 10. At w_g = 10 an island at payoff −1 exports e^(−10) as much as a cooperative island,
and the between-island selection intensity is about 30× the within-island intensity w = 0.3. The
multilevel threshold is steep.

**Suppressing the faker brings back the shadow.** Island selection stops faker and D islands from
exporting. It cannot see the shadow, because ALLC islands pay 0, the same as `THEM(^C)` islands. So the
exit mix flips from faker-dominated at w_g ≤ 3 to shadow-dominated at w_g = 10, by 3 : 1. The shadow
islands are then taken by D mutants and recolonized, and at w_g = 10 that churn accounts for about 190,000
island transitions.

**Plain islands with mutation (w_g = 0) reach P(C,C) = 0.13**, about ten times the well-mixed chain at
N = 100. The ergodic island model is not the same object as the well-mixed one. That is queue item (i) of
§9.5, answered only at this single setting.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 1 | w_g = 0 below 0.1 in every replicate | **Failed.** Replicates are 0.10–0.17. |
| 2 | monotone; w_g = 3 at least 0.5; w_g = 10 at least 0.7 | **Monotone holds**; w_g = 3 **failed** (0.233); w_g = 10 **holds** (0.748) |
| 3 | faker exits dominate at w_g = 0; shadow exits dominate at w_g ≥ 3 | **Partly.** Faker exits dominate at w_g = 0 (holds) and still at w_g = 3 (fails). Shadow exits dominate at w_g = 10 by 3 : 1, not the estimated 20 : 1. |
| 4 | halves within 0.1 at w_g ≥ 3 | **Holds** (0.226 vs 0.233; 0.730 vs 0.748) |

The falsifier, mean P(C,C) < 0.2 at w_g = 3, did not fire, but only barely, at 0.233.

## Multilevel threshold vs island size and count (`runs/multilevel_scaling.md`, predictions in `predictions/2026-09-30-multilevel-scaling.md`)

Same model as the previous section. Per-island rates are fixed at εN = 0.1 mutants and mN = 1 migrant per
island per generation. Each run is 2·10⁵ generations, with 3 replicates per cell. Cells are mean
second-half P(C,C), with the first-half mean in parentheses. w_g* is where the mean crosses ½. This is a
finite-εN run, so it measures approach rates.

| I | N | w_g=3 | w_g=6 | w_g=10 | w_g=15 | w_g=25 | w_g* |
|---|---|---|---|---|---|---|---|
| 64 | 50 | 0.241 (0.238) | 0.780 (0.708) | 0.818 (0.685) | 0.586 (0.574) | 0.561 (0.627) | 4.2 |
| 64 | 100 | 0.227 (0.215) | 0.637 (0.441) | 0.817 (0.589) | 0.791 (0.625) | 0.883 (0.635) | 4.8 |
| 64 | 200 | 0.216 (0.192) | 0.203 (0.187) | 0.577 (0.613) | 0.747 (0.697) | 0.651 (0.756) | 9.0 |
| 16 | 100 | 0.184 (0.163) | 0.224 (0.296) | 0.482 (0.641) | 0.631 (0.777) | 0.674 (0.781) | 10.5 |
| 256 | 100 | 0.246 (0.248) | 0.620 (0.598) | 0.735 (0.689) | 0.641 (0.595) | 0.512 (0.475) | 4.8 |

**The threshold rises with island size.** w_g* goes from 4.2 at N = 50 to 4.8 at N = 100 to 9.0 at
N = 200. At w_g = 6 the N = 200 islands stay at 0.20, against 0.64–0.78 for the smaller ones. This matches
the rate argument:
- recolonizing a D island needs a `THEM(^C)` migrant to fix, with ρ ~ N^(−1/2);
- mutation-borne fakers take cooperative islands at an N-independent rate that island selection cannot
  touch.

At fixed w_g the rescue weakens as islands grow.

**Small metapopulations do worse.** w_g* is 4.8 at both I = 64 and I = 256, but 10.5 at I = 16, with
replicate spread 0.04–0.80. With 16 islands, one mutation-borne exit is a large share of the cooperative
islands.

**Too much island selection hurts.** At N = 50 and at I = 256, P(C,C) peaks at w_g = 6–10 and then falls:
- N = 50: 0.82 at w_g = 10, then 0.56 at w_g = 25;
- I = 256: 0.74 at w_g = 10, then 0.51 at w_g = 25.

The fall appears in all three replicates. A post-hoc, untested hypothesis: at extreme w_g, migrants come
almost only from payoff-0 islands. Those include ALLC shadow islands, which island selection cannot tell
apart from `THEM(^C)` islands. So the shadow is exported as readily as the reciprocator.

**Caveats.** Replicate spread is 0.1–0.3, and at N = 100 first and second halves differ by up to 0.25.
The first half includes the approach from all-D, but several cells are not mixed within 2·10⁵ generations.
The thresholds carry about one grid step of uncertainty.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 1 | P(C,C) decreasing in N at w_g = 10 and w_g = 15 | **Partly.** w_g = 10: 0.818 ≈ 0.817 > 0.577. w_g = 15: fails, with N = 50 at 0.586 below N = 100 at 0.791. |
| 2 | w_g* rises with N by at least one grid step from 100 to 200; N = 50 lower | **Holds:** 4.2 < 4.8 < 9.0 |
| 3 | w_g* flat in I within one grid step | **Fails at I = 16** (10.5); holds from 64 to 256 (4.8, 4.8) |
| 4 | halves within 0.1 at N ≤ 100 | **Fails** in 7 cells, with gaps up to 0.25 |
| 5 | I = 64, N = 100, w_g = 10 reproduces 0.75 within 0.1 | **Holds** (0.817) |

The falsifier did not fire: w_g* rises from N = 100 to N = 200, and w_g = 15 gives 0.747 at N = 200
against 0.791 at N = 100.

**Reading.** Payoff-weighted emigration is a finite-island-size rescue. The required intensity roughly
doubles from N = 100 to N = 200. It needs enough islands, and it has an interior optimum. The evidence is
consistent with it failing in lim_N at any fixed w_g, but not conclusive: this is three sizes, three
replicates, and imperfect mixing.

## ε = 0 islands vs island count (`runs/islands_count.md`, predictions in `predictions/2026-09-30-islands-count.md`)

`src/islands_count.py` runs the PD with no mutation on a complete graph, N = 100, w = 0.3. Seeding is iid:
each slot is drawn from the uniform law over programs. Horizon 2·10⁴ generations. Every run froze well
before the horizon.

| I | mN | runs | coop | defect | other | live-coop | live-defect | live-other | median freeze gen | mean final P(C,C) |
|---|---|---|---|---|---|---|---|---|---|---|
| 16 | 0.1 | 100 | 0.09 | 0.58 | 0.33 | 0.00 | 0.00 | 0.00 | 430 | 0.125 |
| 16 | 1 | 100 | 0.09 | 0.64 | 0.27 | 0.00 | 0.00 | 0.00 | 140 | 0.126 |
| 64 | 0.1 | 100 | 0.14 | 0.23 | 0.63 | 0.00 | 0.00 | 0.00 | 2620 | 0.199 |
| 64 | 1 | 100 | 0.10 | 0.36 | 0.54 | 0.00 | 0.00 | 0.00 | 360 | 0.161 |
| 256 | 0.1 | 40 | 0.00 | 0.62 | 0.38 | 0.00 | 0.00 | 0.00 | 2580 | 0.028 |
| 256 | 1 | 40 | 0.00 | 0.65 | 0.35 | 0.00 | 0.00 | 0.00 | 420 | 0.043 |
| 1024 | 0.1 | 10 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2370 | 0.000 |
| 1024 | 1 | 10 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 470 | 0.000 |

**The lottery concentrates, on mutual defection.** At I = 1024 all 20 runs end in mutual defection, and at
I = 256 no run ends cooperative. The frozen defecting states at I = 1024 hold `THEM(^D)` 0.64, D 0.30 and
`and(X,THEM(^D))` 0.06, so the fakers that beat `THEM(^C)` are still there when the run freezes.

**The migration game gets the outcome right but not the composition.** Its prediction, on-path mutual
defection, is the I → ∞ outcome. The composition is outside its equilibrium set, which allows `THEM(^D)`
at most 0.06. The frozen mixtures are mutually neutral at −1, so their composition is whatever the race
left behind.

**The trend is not monotone at small I.** I = 16 ends mostly in defection: 0.58–0.64 of runs, with
cooperation at 0.09. With 1,600 iid slots, many programs are never seeded; `THEM(^C)` has about 6 copies
expected. Cooperation peaks at I = 64, at 0.10–0.14, and then vanishes.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 1 | cooperative share falls with I; below 0.05 at I = 1024 | **Partly.** Zero at 256 and 1024, holding. It is not monotone: 0.09 → 0.14 from I = 16 to 64 at mN = 0.1. |
| 2 | "other frozen" falls with I; defection at least 0.8 at I = 1024 | **Partly.** Defection is 1.00 at 1024, holding. "Other frozen" is non-monotone: 0.33 → 0.63 → 0.38 → 0 at mN = 0.1. |
| 3 | at least 90% of runs in one family at I = 1024 | **Holds:** 100% mutual defection |
| 4 | median freeze generation increases with I | **Fails** at mN = 0.1 (430, 2,620, 2,580, 2,370). Holds roughly at mN = 1 (140, 360, 420, 470). |
| 5 | cooperative share 0.1–0.3 at I = 64 | **Holds** (0.10–0.14) |

Neither falsifier fired.

**Reading.** The ε = 0 island model has a canonical I → ∞ answer in the PD, and it is inefficient.
Seeding randomness does not substitute for mutation as a route to cooperation. More islands make the
dilemma worse: the faker has more chances to reach every cooperative island before the fakers go extinct.

## Modal (Löbian) arm: lim_N in the PD (`runs/modal_limN.md`, predictions in `predictions/2026-09-30-modal-arm.md`)

**The arm.** `src/modal.py` builds pure modal agents of rank 0:
- **Operators.** Four provability boxes: `BOX`/`BOXD`, provable in PA that the opponent plays C/D against
  P; and `BOX1`/`BOXD1`, the same in PA + Con(PA).
- **Semantics.** Evaluated on the linear Kripke chain of provability logic GL.
- **Excluded.** No X, no `ROLE`, no unboxed simulation.
- **Prior.** Same length prior as the weak arm. The box is the application node, so FairBot costs 3 nodes.
- **Sizes.** 1,020 / 19,544 / 89,842 programs at n = 6 / 8 / 9, which are 51 / 471 / 863 behavioural classes.
- **Checks.** The evaluator agrees with direct recursion on syntax trees for all 1,040,400 pairs at n = 6,
  and reproduces the known agent outcomes, with PrudentBot needing PA + 1.

The runs are the ε→0 chain. Three cells were unfinished at write-up: n = 8 at N = 3,000 and 10⁴, and n = 9
at w = 0.1, N = 10⁴. They will be appended.

| n | w | N | P(C,C) | π(all-D) | π(all-FairBot) | π(all-PrudentBot) | ρ(FairBot \| all-D) | exit rate from all-FairBot | ALLC share of exits |
|---|---|---|---|---|---|---|---|---|---|
| 9 | 0.1 | 100 | 0.124 | 0.873 | 0.024 | 0.0002 | 0.0248 | 4.95e-03 | 0.94 |
| 9 | 0.1 | 300 | 0.188 | 0.810 | 0.039 | 0.0007 | 0.0144 | 1.62e-03 | 0.96 |
| 9 | 0.1 | 1,000 | 0.278 | 0.721 | 0.064 | 0.0016 | 0.0079 | 4.85e-04 | 0.96 |
| 9 | 0.1 | 3,000 | 0.377 | 0.623 | 0.095 | 0.0030 | 0.0046 | 1.62e-04 | 0.96 |
| 9 | 0.1 | 30,000 | 0.622 | 0.378 | 0.182 | 0.0077 | 0.0015 | 1.62e-05 | 0.96 |
| 9 | 0.3 | 100 | 0.186 | 0.813 | 0.038 | 0.0007 | 0.0421 | 4.85e-03 | 0.96 |
| 9 | 0.3 | 300 | 0.268 | 0.731 | 0.060 | 0.0014 | 0.0246 | 1.62e-03 | 0.96 |
| 9 | 0.3 | 1,000 | 0.377 | 0.623 | 0.094 | 0.0029 | 0.0136 | 4.85e-04 | 0.96 |
| 9 | 0.3 | 3,000 | 0.491 | 0.508 | 0.134 | 0.0050 | 0.0079 | 1.62e-04 | 0.96 |
| 9 | 0.3 | 10,000 | 0.622 | 0.377 | 0.181 | 0.0076 | 0.0044 | 4.85e-05 | 0.96 |
| 9 | 0.3 | 30,000 | 0.727 | 0.273 | 0.227 | 0.0101 | 0.0025 | 1.62e-05 | 0.96 |
| 9 | 1 | 100 | 0.272 | 0.727 | 0.060 | 0.0013 | 0.0742 | 4.85e-03 | 0.96 |
| 9 | 1 | 300 | 0.376 | 0.623 | 0.092 | 0.0027 | 0.0441 | 1.62e-03 | 0.96 |
| 9 | 1 | 1,000 | 0.504 | 0.496 | 0.135 | 0.0050 | 0.0246 | 4.85e-04 | 0.96 |
| 9 | 1 | 3,000 | 0.624 | 0.376 | 0.179 | 0.0074 | 0.0144 | 1.62e-04 | 0.96 |
| 9 | 1 | 10,000 | 0.739 | 0.261 | 0.227 | 0.0100 | 0.0079 | 4.85e-05 | 0.96 |
| 9 | 1 | 30,000 | 0.818 | 0.182 | 0.275 | 0.0127 | 0.0046 | 1.62e-05 | 0.96 |
| 6 | 0.3 | 100 | 0.169 | 0.830 | 0.037 | — | 0.0421 | 4.87e-03 | 0.96 |
| 6 | 0.3 | 300 | 0.246 | 0.754 | 0.059 | — | 0.0246 | 1.62e-03 | 0.96 |
| 6 | 0.3 | 1,000 | 0.345 | 0.655 | 0.094 | — | 0.0136 | 4.87e-04 | 0.96 |
| 6 | 0.3 | 3,000 | 0.452 | 0.548 | 0.137 | — | 0.0079 | 1.62e-04 | 0.96 |
| 6 | 0.3 | 10,000 | 0.587 | 0.413 | 0.189 | — | 0.0044 | 4.87e-05 | 0.96 |
| 6 | 0.3 | 30,000 | 0.707 | 0.293 | 0.233 | — | 0.0025 | 1.62e-05 | 0.96 |
| 8 | 0.3 | 100 | 0.182 | 0.817 | 0.038 | 0.0006 | 0.0421 | 4.85e-03 | 0.96 |
| 8 | 0.3 | 300 | 0.263 | 0.736 | 0.060 | 0.0012 | 0.0246 | 1.62e-03 | 0.96 |
| 8 | 0.3 | 1,000 | 0.371 | 0.629 | 0.094 | 0.0026 | 0.0136 | 4.85e-04 | 0.96 |
| 8 | 0.3 | 30,000 | 0.725 | 0.275 | 0.226 | 0.0084 | 0.0025 | 1.62e-05 | 0.96 |

**Cooperation rises with N, with no peak.**
- *Magnitude.* At n = 9 and w = 0.3, P(C,C) is 0.19 at N = 100, 0.38 at 10³, 0.62 at 10⁴ and 0.73 at
  3·10⁴. At w = 1 it reaches 0.82.
- *Rate.* The ratio of cooperative mass to all-D mass grows like N^0.43–0.45 over N ∈ [10³, 3·10⁴], at
  every n and w. This approaches the predicted N^(1/2) from below.
- *Mechanism.* Entry ρ(FairBot | all-D) falls like N^(−0.50). The exit rate from all-FairBot falls like
  N^(−1.00): all of it is neutral drift, 94–96% of it into ALLC, which D then takes.
- *Contrast with the weak arm.* The weak arm peaked at 0.013 and fell to 0.004 at N = 3·10⁴. The modal arm is
  the first instrument whose cooperation rises toward 1 in lim_N.
- *Extrapolation.* 90% cooperation would take roughly N ≈ 5·10⁵ at w = 0.3 and about 1.4·10⁵ at w = 1.

**Support and transitions.** The support is all-D plus a family of mutually cooperating provers at roughly
equal weight: `BOX(THEM(ME))` (FairBot), `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, and from N ≈ 3,000 also
`and(BOX1(THEM(ME)),not(BOX(THEM(ME))))`. PrudentBot sits at 0.0002–0.013, rising with N. Polymorphic mass
is at most 3·10⁻⁷, and no transition is indeterminate.

`BOX(THEM(THEM))`, "cooperate iff you provably cooperate with yourself", is a third-party probe, with
yourself as the third party. At n ≥ 8 it has strict invaders, and at n = 9 it falls behind FairBot: 0.156
against 0.227 at N = 3·10⁴. The faker law of the weak arm operates inside the modal arm too.

**What this does and does not show** (from the reviews below).
- A free, sound, self-referential oracle removes both obstacles by construction:
  - grounding cost, because FairBot enters all-D neutrally;
  - fakeability, because soundness forbids exploiting FairBot.
- So "efficient in the limit" is built in once the primitive is granted. The empirical content is the rate,
  a cooperative-to-defect ratio ∝ N^0.44, and the constant, set by the shadow's μ-weight, μ(C) ≈ 0.47.
- "No strict exits" is a theorem of soundness, so it tests the evaluator, not the dynamics.
- The comparison with the weak arm is confounded. The modal arm also drops X and `ROLE`, so fewer exploiting
  classes exist. The effect cannot yet be attributed to provability alone.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 1 | no peak; P(C,C) within 1.5× of 0.04 / 0.12 / 0.3 / 0.45 | **No peak holds.** The **magnitudes failed** (0.19 / 0.38 / 0.62 / 0.73). I counted FairBot's entry alone, but three or four unfakeable provers enter at equal μ. |
| 2 | no strict exits from all-FairBot; exit slope in [−1.1, −0.9] | **Holds** (0; −1.00). The first part holds by construction. |
| 3 | ρ(FairBot \| all-D) slope in [−0.55, −0.45] | **Holds** (−0.49 to −0.50) |
| 4 | ALLC at least 0.9 of FairBot's exits | **Holds** (0.94–0.96) |
| 5 | π(all-PrudentBot) < 0.01 at n = 8, 9; n = 9 within ±20% of n = 6 | PrudentBot **narrowly failed** (0.0101 at w = 0.3, N = 3·10⁴; 0.0127 at w = 1). The n-comparison **holds** (0.727 vs 0.707). |
| 6 | P(C,C) at N = 3·10⁴ at least 10× the weak arm's 0.0044 | **Holds** (0.73, 165×) |

Neither falsifier fired: there is no peak and no strict exit.

**Reviews.** Posted after the run as a pilot of the review workflow: `reviews/2026-09-30-modal-arm-gpt-6-astra.md`
and `reviews/2026-09-30-modal-arm-fable.md`. Points adopted:
- Efficiency is built in, so the claim is the exponent.
- Verdict 2 cannot fire.
- The weak-vs-modal comparison is confounded by X and `ROLE`, and needs a control arm stripped of them.
- "Upper bound" is the wrong word for a free box. The arm removes capabilities as well as adding one, so it
  is a distinct idealization.
- My 90% extrapolation, near 10⁶ from the static estimate, was arithmetically off. It is superseded by the
  measured ratio above.

## E1 matched control: simulation vs provability (`runs/matched_control.md`, predictions in `predictions/2026-10-01-modal-followups.md`)

The two arms have identical grammars and identical priors: the program counts by size match exactly, and
μ(C) = μ(D) = 0.488 in both. They differ only in what an application means.
- **W0** is the weak arm without X and `ROLE`: applications are simulated, and self-reference that never
  terminates gets D.
- **M0** is the modal arm with the PA box only: applications are provability statements.

ε→0 chain, PD, w = 0.3, with `eager_poly=False`, which was verified exact.

| arm | n | N | programs | classes | P(C,C) | π(all-D) | top cooperative state | its π | ρ_enter | exits from it: strict / neutral / other | cut flow |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W0 | 6 | 100 | 666 | 12 | 0.0171 | 0.9803 | `THEM(^C)` | 0.0152 | 0.0421 | 5.22e-04 / 4.88e-03 / 1.45e-08 | 1.7e-07 |
| W0 | 6 | 1000 | 666 | 12 | 0.0266 | 0.9719 | `THEM(^C)` | 0.0263 | 0.0136 | 5.14e-04 / 4.88e-04 / 6.65e-39 | 8.5e-08 |
| W0 | 6 | 10000 | 666 | 12 | 0.0152 | 0.9835 | `THEM(^C)` | 0.0151 | 0.0044 | 5.13e-04 / 4.88e-05 / 0.00e+00 | 4.3e-08 |
| W0 | 6 | 30000 | 666 | 12 | 0.0094 | 0.9893 | `THEM(^C)` | 0.0093 | 0.0025 | 5.13e-04 / 1.63e-05 / 0.00e+00 | 2.6e-08 |
| W0 | 7 | 100 | 2796 | 19 | 0.0180 | 0.9789 | `THEM(^C)` | 0.0160 | 0.0421 | 5.55e-04 / 4.87e-03 / 1.61e-08 | 2.1e-07 |
| W0 | 7 | 1000 | 2796 | 19 | 0.0273 | 0.9707 | `THEM(^C)` | 0.0269 | 0.0136 | 5.46e-04 / 4.87e-04 / 9.07e-39 | 1.1e-07 |
| W0 | 7 | 10000 | 2796 | 19 | 0.0152 | 0.9830 | `THEM(^C)` | 0.0151 | 0.0044 | 5.45e-04 / 4.87e-05 / 0.00e+00 | 5.1e-08 |
| W0 | 7 | 30000 | 2796 | 19 | 0.0094 | 0.9888 | `THEM(^C)` | 0.0093 | 0.0025 | 5.45e-04 / 1.62e-05 / 0.00e+00 | 3.1e-08 |
| M0 | 6 | 100 | 666 | 8 | 0.1292 | 0.8706 | `BOX(THEM(ME))` | 0.1109 | 0.0421 | 0.00e+00 / 4.91e-03 / 4.52e-08 | 0.0e+00 |
| M0 | 6 | 1000 | 666 | 8 | 0.3059 | 0.6940 | `BOX(THEM(ME))` | 0.2857 | 0.0136 | 0.00e+00 / 4.91e-04 / 5.59e-38 | 0.0e+00 |
| M0 | 6 | 10000 | 666 | 8 | 0.5703 | 0.4297 | `BOX(THEM(ME))` | 0.5633 | 0.0044 | 0.00e+00 / 4.91e-05 / 0.00e+00 | 0.0e+00 |
| M0 | 6 | 30000 | 666 | 8 | 0.6955 | 0.3045 | `BOX(THEM(ME))` | 0.6925 | 0.0025 | 0.00e+00 / 1.64e-05 / 0.00e+00 | 0.0e+00 |
| M0 | 7 | 100 | 2796 | 10 | 0.1332 | 0.8666 | `BOX(THEM(ME))` | 0.1140 | 0.0421 | 0.00e+00 / 4.90e-03 / 4.75e-08 | 0.0e+00 |
| M0 | 7 | 1000 | 2796 | 10 | 0.3128 | 0.6871 | `BOX(THEM(ME))` | 0.2921 | 0.0136 | 0.00e+00 / 4.90e-04 / 5.94e-38 | 0.0e+00 |
| M0 | 7 | 10000 | 2796 | 10 | 0.5782 | 0.4218 | `BOX(THEM(ME))` | 0.5711 | 0.0044 | 0.00e+00 / 4.90e-05 / 0.00e+00 | 0.0e+00 |
| M0 | 7 | 30000 | 2796 | 10 | 0.7023 | 0.2976 | `BOX(THEM(ME))` | 0.6991 | 0.0025 | 0.00e+00 / 1.63e-05 / 0.00e+00 | 0.0e+00 |

**Provability alone reproduces the gap.**
- *W0 behaves like the weak arm.* P(C,C) is 0.017 → 0.027 → 0.015 → 0.009, peaking at N = 10³. Its best
  reciprocator `THEM(^C)` leaves through a constant faker exit, 5.1·10⁻⁴ per mutation event at every N, which
  overtakes the shadow's 1/N drift by N = 10³.
- *M0 behaves like the full modal arm.* P(C,C) is 0.13 → 0.31 → 0.57 → 0.70, rising monotonically. FairBot has no
  strict exits, and the cooperative-to-D ratio grows like N^0.48.
- *The gap.* At N = 3·10⁴, M0 is 74× W0. X and `ROLE` were not what separated the weak and modal arms.
- *M0 is cleaner than the full arm.* The full modal arm's exponent was 0.44. Its extra box kinds add fakeable
  provers, such as `BOX(THEM(THEM))` at n ≥ 8.

**What it cannot separate** (from the fable review). Provability does two things here:
- it makes FairBot unfakeable;
- it makes entry 7× cheaper. M0's FairBot class has μ = 0.0148, against W0's `THEM(^C)` at 0.002, because W0's
  size-3 self-referential forms defect on themselves.

The exponent comes from unfakeability: there is no constant exit. The constant comes from both. A sound,
free prover is also more computational power than simulation, so this measures what a free prover buys, not
what a realizable source-reading program buys.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 1 | W0 peaks within one grid step of 10³, is 0.005–0.02 at 3·10⁴, and its exits are faker-dominated at N ≥ 10⁴ | **Holds:** peak at 10³, 0.009, strict 5.1·10⁻⁴ against neutral 4.9·10⁻⁵ |
| 2 | M0 monotone; 0.70 ± 0.1 at 3·10⁴; exponent 0.50 ± 0.05; no strict invaders | **Holds:** 0.70, exponent 0.48, strict exits 0 |
| 3 | M0 at least 10× W0 at 3·10⁴ | **Holds:** 74× |

The falsifier, M0 below 2× W0, did not fire. Fable's static two-state prediction, 0.70 for M0 and 0.009 for
W0, was exact.

## E2 ratchet: does the support migrate from FairBot to PrudentBot? (`runs/modal_ratchet.md`)

Full modal arm, n = 8, w = 0.3, ε→0 chain. New cells at N = 10⁵ and 3·10⁵ use `eager_poly=False`, verified to
reproduce all four earlier n = 8 cells exactly. The new cells are repeated at θ = 10⁻⁷, with identical results.

| N | theta | P(C,C) | π(all-D) | π(FairBot) | π(PrudentBot) | π(PB)/π(FB) | cut flow | time (s) |
|---|---|---|---|---|---|---|---|---|
| 100 | 1e-06 (earlier run) | 0.1821 | 0.8166 | 0.0379 | 0.00062 | 0.0163 | 1.3e-06 | 16 |
| 300 | 1e-06 (earlier run) | 0.2635 | 0.7358 | 0.0599 | 0.00123 | 0.0205 | 5.2e-07 | 17 |
| 1000 | 1e-06 (earlier run) | 0.3707 | 0.6288 | 0.0940 | 0.00256 | 0.0272 | 2.0e-07 | 20 |
| 3000 | 1e-06 (earlier run) | 0.4845 | 0.5152 | 0.1338 | 0.00432 | 0.0323 | 8.3e-08 | 7606 |
| 10000 | 1e-06 (earlier run) | 0.6172 | 0.3826 | 0.1816 | 0.00643 | 0.0354 | 3.1e-08 | 15217 |
| 30000 | 1e-06 (earlier run) | 0.7246 | 0.2753 | 0.2262 | 0.00837 | 0.0370 | 1.2e-08 | 260 |
| 100000 | 1e-06 | 0.8135 | 0.1864 | 0.2791 | 0.01075 | 0.0385 | 1.5e-08 | 132 |
| 100000 | 1e-07 | 0.8135 | 0.1864 | 0.2791 | 0.01075 | 0.0385 | 1.5e-08 | 132 |
| 300000 | 1e-06 | 0.8733 | 0.1266 | 0.3277 | 0.01298 | 0.0396 | 8.4e-09 | 336 |
| 300000 | 1e-07 | 0.8733 | 0.1266 | 0.3277 | 0.01298 | 0.0396 | 8.4e-09 | 336 |

**A plateau, not a ratchet.** π(PrudentBot)/π(FairBot) is 0.016 → 0.027 → 0.032 → 0.035 → 0.037 → 0.0385 →
0.0396 from N = 100 to 3·10⁵, flattening toward about 0.04. Total cooperation keeps rising: P(C,C) is 0.81 at
10⁵ and 0.87 at 3·10⁵.

**The prover family is shifting toward unfakeable members.** The fakeable `BOX(THEM(THEM))` holds 0.25 of the
family at N = 10³, 0.24 at 3·10⁴, 0.17 at 10⁵ and 0.09 at 3·10⁵. Its strict invaders exit at an N-independent
rate, as fable predicted. FairBot and `BOX1(THEM(ME))` each grow to 0.33.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 4 | π(PB)/π(FB) < 0.06 at 3·10⁵, with the increase shrinking | **Holds:** 0.0396; +0.0047 from 3·10³ to 3·10⁴, then +0.0026 from 3·10⁴ to 3·10⁵ |
| 5 | P(C,C) 0.80 ± 0.05 at 10⁵ and 0.86 ± 0.05 at 3·10⁵ | **Holds** (0.81, 0.87) |
| — | the ratio is insensitive to θ | **Holds:** identical at 10⁻⁷ |

The plateau falsifier, a ratio of at least 0.08, did not fire.

## E3 finite-εN agent-based runs: modal vs weak arm, with and without structure (`runs/modal_abm.md`)

Agent-based Moran, PD, w = 0.3, 2·10⁵ generations (a generation is I·N births), second half, 3 replicates per
cell. Finite εN, so these are approach rates. The cooperative and all-D starts agree, so the second halves
are mixed.

| arm | configuration | P(C,C) per replicate | mean | R share | ALLC share of population | ALLC share of population during cooperative phases |
|---|---|---|---|---|---|---|
| modal n=6 | big island, eps 1e-3 | 0.99, 0.99, 0.99 | 0.989 | 0.090 | 0.258 | 0.261 |
| modal n=6 | big island, eps 1e-3, cooperative start | 0.99, 0.99, 0.99 | 0.989 | 0.130 | 0.261 | 0.269 |
| modal n=6 | big island, eps 1e-4 | 0.97, 1.00, 0.96 | 0.978 | 0.287 | 0.127 | 0.130 |
| modal n=6 | 64 islands, w_g 0 | 0.98, 0.98, 0.98 | 0.980 | 0.125 | 0.105 | 0.105 |
| modal n=6 | 64 islands, w_g 10 | 0.98, 0.98, 0.98 | 0.982 | 0.251 | 0.115 | 0.115 |
| weak L_6 | big island, eps 1e-3 | 0.06, 0.06, 0.08 | 0.064 | 0.025 | 0.023 | 0.232 |
| weak L_6 | big island, eps 1e-3, cooperative start | 0.06, 0.06, 0.08 | 0.064 | 0.025 | 0.023 | 0.232 |
| weak L_6 | big island, eps 1e-4 | 0.00, 0.05, 0.00 | 0.018 | 0.012 | 0.004 | 0.065 |
| weak L_6 | 64 islands, w_g 0 | 0.13, 0.17, 0.13 | 0.144 | 0.028 | 0.063 | 0.054 |
| weak L_6 | 64 islands, w_g 10 | 0.88, 0.94, 0.63 | 0.817 | 0.662 | 0.123 | 0.132 |

**The modal arm cooperates without any spatial structure.** On one well-mixed island of 6,400, P(C,C) is 0.989
in every replicate, from an all-D start and from a cooperative start. It is 0.978 at the lower mutation rate.
The weak arm on the same island is at 0.06; its cooperative start collapses within about 3,000 generations and
then merges exactly with the all-D trajectory, since both runs draw the same random numbers per event. The
64-island configurations add nothing for the modal arm: 0.98 at w_g = 0 and at w_g = 10. The weak arm needs
w_g = 10 to reach 0.82.

**The mechanism: mutation supplies its own pruner** (fable's review). At finite ε a standing fringe of
defectors exploits ALLC. That keeps the shadow in check, so the shadow never reaches the (R − P)/(T − P) = ½
needed for D to invade. ALLC sits at 0.26 of the population at ε = 10⁻³ and 0.13 at ε = 10⁻⁴. No collapses
occur: every replicate stays at 0.96–1.00.

This finite-εN result is stronger than the ε→0 chain at the same N, which gives about 0.5 at N ≈ 6,400. In the
chain the population is monomorphic between mutations, so nothing prunes the shadow while it drifts in. This is
a third regime, distinct from the ε→0 chain (shadow exit ∝ 1/N) and from the lattice.

**Verdicts.**

| # | prediction | outcome |
|---|---|---|
| 6 | modal big island 0.6–0.95 at ε = 10⁻³ and lower at 10⁻⁴; weak below 0.1 | **Band failed (too high):** 0.989. The ordering holds (0.978 < 0.989), and weak is 0.064. Predicted collapse excursions did not occur. |
| 7 | modal 64 islands, w_g = 0, at least 0.7 | **Holds** (0.98) |
| 8 | modal 64 islands, w_g = 10, at least 0.75 | **Holds** (0.98) |
| 9 | ALLC share 0.32 ± 0.1 at both ε | **Holds** at 10⁻³ (0.26). **Fails** at 10⁻⁴ (0.13): the pinning depends on ε, contrary to the mean-field x* = μ_C/(1 + μ_D). |
| 10 | cooperative and all-D starts within 0.15 | **Holds** (0.989 both) |

The falsifier, big-island modal below 0.1, did not fire. My original E3 mechanism (ALLC flooding,
P(C,C) 0.2–0.6) was replaced after review and is recorded in REJECTED.md.

## Priced arm: compute cost on proofs, spatial structure, and cliques (`runs/priced_limN.md`, `runs/graph_rates.md`; predictions in `predictions/2026-10-01-priced-arm.md`)

`build_priced` charges c per essential box atom per Kripke world the program's atom values take to settle
against the opponent. This is semantic-stabilization pricing: a proxy for proof-search work, not a measurement of
it. A uniform tax would cancel exactly under exp fitness, so only *differential* cost matters. Three modes:
- **atoms:** the formula above.
- **depth:** no atom multiplier.
- **lazy:** free against constant opponents and exact copies; pays the atoms price only against other
  non-trivial programs.

### Exp 1: priced ε→0 chain, well-mixed, w = 0.3

| pricing | n | c | N | P(C,C) | π(all-D) | π(all-FairBot) | polymorphic π |
|---|---|---|---|---|---|---|---|
| atoms | 6 | 0 | 100 | 0.1693 | 0.8299 | 0.0372 | 0.0e+00 |
| atoms | 6 | 0 | 1,000 | 0.3453 | 0.6545 | 0.0945 | 0.0e+00 |
| atoms | 6 | 0 | 10,000 | 0.5869 | 0.4130 | 0.1893 | 0.0e+00 |
| atoms | 6 | 0 | 30,000 | 0.7068 | 0.2932 | 0.2331 | 0.0e+00 |
| atoms | 6 | 0.001 | 100 | 0.1660 | 0.8332 | 0.0365 | 0.0e+00 |
| atoms | 6 | 0.001 | 1,000 | 0.8315 | 0.0925 | 0.3896 | 7.6e-02 |
| atoms | 6 | 0.001 | 10,000 | 0.3004 | 0.6978 | 0.0929 | 1.8e-03 |
| atoms | 6 | 0.001 | 30,000 | 0.1936 | 0.8057 | 0.0611 | 6.6e-04 |
| atoms | 6 | 0.01 | 100 | 0.1366 | 0.8510 | 0.0302 | 1.2e-02 |
| atoms | 6 | 0.01 | 1,000 | 0.1163 | 0.8836 | 0.0303 | 0.0e+00 |
| atoms | 6 | 0.01 | 10,000 | 0.0150 | 0.9850 | 0.0049 | 0.0e+00 |
| atoms | 6 | 0.01 | 30,000 | 0.0019 | 0.9981 | 0.0008 | 0.0e+00 |
| atoms | 6 | 0.1 | 100 | 0.0196 | 0.9803 | 0.0050 | 0.0e+00 |
| depth | 6 | 0.001 | 100 | 0.1660 | 0.8332 | 0.0365 | 0.0e+00 |
| depth | 6 | 0.001 | 1,000 | 0.8315 | 0.0925 | 0.3896 | 7.6e-02 |
| depth | 6 | 0.001 | 10,000 | 0.3004 | 0.6978 | 0.0929 | 1.8e-03 |
| depth | 6 | 0.001 | 30,000 | 0.1936 | 0.8057 | 0.0611 | 6.6e-04 |
| depth | 6 | 0.01 | 100 | 0.1366 | 0.8510 | 0.0302 | 1.2e-02 |
| depth | 6 | 0.01 | 1,000 | 0.1163 | 0.8836 | 0.0303 | 0.0e+00 |
| depth | 6 | 0.01 | 10,000 | 0.0150 | 0.9850 | 0.0049 | 0.0e+00 |
| depth | 6 | 0.01 | 30,000 | 0.0019 | 0.9981 | 0.0008 | 0.0e+00 |
| lazy | 6 | 0.001 | 100 | 0.1693 | 0.8299 | 0.0368 | 0.0e+00 |
| lazy | 6 | 0.001 | 1,000 | 0.3453 | 0.6544 | 0.0936 | 0.0e+00 |
| lazy | 6 | 0.001 | 10,000 | 0.5883 | 0.4117 | 0.1880 | 0.0e+00 |
| lazy | 6 | 0.001 | 30,000 | 0.7094 | 0.2906 | 0.2317 | 0.0e+00 |
| lazy | 6 | 0.01 | 100 | 0.1694 | 0.8298 | 0.0368 | 0.0e+00 |
| lazy | 6 | 0.01 | 1,000 | 0.3461 | 0.6537 | 0.0938 | 0.0e+00 |
| lazy | 6 | 0.01 | 10,000 | 0.5903 | 0.4096 | 0.1887 | 0.0e+00 |
| lazy | 6 | 0.01 | 30,000 | 0.7100 | 0.2900 | 0.2319 | 0.0e+00 |
| atoms | 8 | 0 | 100 | 0.1821 | 0.8166 | 0.0379 | 0.0e+00 |
| atoms | 8 | 0 | 1,000 | 0.3707 | 0.6288 | 0.0940 | 0.0e+00 |
| atoms | 8 | 0 | 10,000 | 0.6172 | 0.3826 | 0.1816 | 0.0e+00 |
| atoms | 8 | 0 | 30,000 | 0.7246 | 0.2753 | 0.2262 | 0.0e+00 |
| atoms | 8 | 0.001 | 100 | 0.1784 | 0.8204 | 0.0372 | 0.0e+00 |
| atoms | 8 | 0.001 | 1,000 | 0.8403 | 0.0906 | 0.3901 | 7.1e-02 |
| atoms | 8 | 0.001 | 10,000 | 0.3175 | 0.6800 | 0.0934 | 2.3e-03 |
| atoms | 8 | 0.001 | 30,000 | 0.2051 | 0.7940 | 0.0621 | 8.8e-04 |
| atoms | 8 | 0.01 | 100 | 0.1453 | 0.8366 | 0.0307 | 1.7e-02 |
| atoms | 8 | 0.01 | 1,000 | 0.1227 | 0.8772 | 0.0311 | 0.0e+00 |
| atoms | 8 | 0.01 | 10,000 | 0.0158 | 0.9842 | 0.0051 | 0.0e+00 |
| atoms | 8 | 0.01 | 30,000 | 0.0021 | 0.9979 | 0.0008 | 0.0e+00 |
| atoms | 8 | 0.1 | 100 | 0.0206 | 0.9792 | 0.0052 | 0.0e+00 |
| depth | 8 | 0.001 | 100 | 0.1786 | 0.8201 | 0.0372 | 0.0e+00 |
| depth | 8 | 0.001 | 1,000 | 0.8415 | 0.0903 | 0.3893 | 7.0e-02 |
| depth | 8 | 0.001 | 10,000 | 0.3760 | 0.6218 | 0.0854 | 2.6e-02 |
| depth | 8 | 0.001 | 30,000 | 0.3278 | 0.6714 | 0.0525 | 4.0e-02 |
| depth | 8 | 0.01 | 100 | 0.1477 | 0.8341 | 0.0306 | 1.9e-02 |
| depth | 8 | 0.01 | 1,000 | 0.1368 | 0.8630 | 0.0306 | 0.0e+00 |
| depth | 8 | 0.01 | 10,000 | 0.0313 | 0.9687 | 0.0050 | 0.0e+00 |
| depth | 8 | 0.01 | 30,000 | 0.0050 | 0.9950 | 0.0008 | 0.0e+00 |
| lazy | 8 | 0.001 | 100 | 0.1821 | 0.8166 | 0.0377 | 0.0e+00 |
| lazy | 8 | 0.001 | 1,000 | 0.3710 | 0.6285 | 0.0933 | 0.0e+00 |
| lazy | 8 | 0.001 | 10,000 | 0.6296 | 0.3702 | 0.1757 | 0.0e+00 |
| lazy | 8 | 0.001 | 30,000 | 0.8132 | 0.1867 | 0.1548 | 0.0e+00 |
| lazy | 8 | 0.01 | 100 | 0.1822 | 0.8165 | 0.0377 | 0.0e+00 |
| lazy | 8 | 0.01 | 1,000 | 0.3790 | 0.6205 | 0.0925 | 0.0e+00 |
| lazy | 8 | 0.01 | 10,000 | 0.9985 | 0.0015 | 0.0007 | 0.0e+00 |
| lazy | 8 | 0.01 | 30,000 | 1.0000 | 0.0000 | 0.0000 | 0.0e+00 |

**Atom pricing kills the well-mixed limit.**
- *c = 10⁻²:* P(C,C) is 0.14 → 0.12 → 0.015 → 0.002 at n = 6.
- *c = 10⁻³:* 0.17 → [0.83] → 0.30 → 0.19. The bracketed value is suspect, see below.
- *Exit mix:* at c > 0, exits from all-FairBot are 99% *strict*: ALLC, which pays nothing, invades the priced
  prover. This is the price ladder.
- *PrudentBot:* changes nothing (n = 8 is within 10% of n = 6), because its prior mass is 1.4·10⁻⁶.
- *Depth pricing:* removes only the PrudentBot → FairBot rung, so n = 8 does a little better than under atoms
  (0.33 against 0.21 at c = 10⁻³, N = 3·10⁴).

**Suspect cell.** atoms and depth at c = 10⁻³, N = 10³ give P(C,C) ≈ 0.83, above the free arm's 0.35, with 7%
polymorphic mass at {D 0.998, FairBot 0.001, `BOX(THEM(THEM))` 0.001}. That state sits at the cost barrier, where
fitness differences are about 10⁻⁶. The likeliest cause is the chain's slow-rest fallback treating an unstable
barrier point as an attractor, which lets the chain step over the barrier. This is a hypothesis, not checked, and
the cell is not used.

**Lazy pricing escapes the ladder.**
- *n = 6:* it reproduces the free arm to within 0.003 at every N and both c.
- *n = 8, c = 10⁻²:* cooperation goes to 1 (0.9985 at N = 10⁴, 1.0000 at 3·10⁴). The support is a family led by
  `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))`. It exploits ALLC, mutually defects with FairBot, and cooperates with
  46 classes.
- *Mechanism: incumbency.* Under lazy pricing a copy is free, while a behaviourally neutral newcomer pays c
  against the residents. A world whose members also punish ALLC therefore has no neutral exit and absorbs. This
  is a cost-based version of the clique effect that the REJECTED Levin entry warned about: the short-circuit on
  self-recognition saves compute without changing whom the program cooperates with, and it still locks in the
  incumbent.

### Exp 2: hitting probabilities on graphs (priced n = 8; probability a single mutant reaches half the graph)

| pair | c | torus 16 | torus 32 | torus 64 | hypercube d = 6 | d = 8 | d = 10 |
|---|---|---|---|---|---|---|---|
| entry FB|D | 0 | 0.1080 | 0.1080 | 0.1040 | 0.0840 | 0.0570 | 0.0440 |
| entry FB|D | 0.01 | 0.0930 | 0.0970 | 0.1090 | 0.0720 | 0.0450 | 0.0360 |
| entry FB|D | 0.1 | 0.0640 | 0.0620 | 0.0680 | 0.0550 | 0.0250 | 0.0040 |
| entry PB|D | 0 | 0.1080 | 0.1080 | 0.1040 | 0.0840 | 0.0570 | 0.0440 |
| entry PB|D | 0.01 | 0.0740 | 0.1030 | 0.0910 | 0.0700 | 0.0480 | 0.0400 |
| entry PB|D | 0.1 | 0.0390 | 0.0460 | 0.0350 | 0.0270 | 0.0034 | 0.0000 |
| ladder C|FB | 0 | 0.0083 | 0.0015 | — | 0.0300 | 0.0057 | 0.0017 |
| ladder C|FB | 0.01 | 0.0080 | 0.0037 | — | 0.0360 | 0.0100 | 0.0033 |
| ladder C|FB | 0.1 | 0.0410 | 0.0290 | — | 0.0540 | 0.0270 | 0.0380 |
| neutral baseline | — | 0.0065 | 0.0027 | — | 0.0265 | 0.0075 | 0.0013 |

Well-mixed reference for FairBot entry: c = 0: N=256 2.7e-02, N=1024 1.3e-02, N=4096 6.8e-03; c = 0.01: N=256 2.3e-02, N=1024 1.0e-02, N=4096 3.5e-03; c = 0.1: N=256 3.6e-03, N=1024 2.6e-05, N=4096 6.9e-13.

**Structure rescues entry.** On the torus, FairBot's entry into all-D is independent of N at every price: 0.064,
0.062 and 0.068 at c = 0.1 for N = 256, 1,024 and 4,096. The well-mixed values are 3.6·10⁻³, 2.6·10⁻⁵ and
7·10⁻¹³. Nucleation is local, so the barrier is set by the neighbourhood. The hypercube, whose degree grows like
log N, falls in between: 0.055, 0.025 and 0.004 at c = 0.1.

**Structure does not stop the ladder.** ALLC invades FairBot on graphs at about its well-mixed rate. At c = 0.1 that
is 3.6–29× the measured neutral baseline at N ≥ 256. At c = 10⁻² it is above the baseline but within overlapping
intervals, so inconclusive. FairBot invading PrudentBot gives identical numbers. Its payoff block is a constant
shift of ALLC-vs-FairBot, and a constant shift cancels under exp fitness.

### Exp 3: cliques (foreordained by fable's review; hitting times are the content)

| m (mass) | c | N | π(cliques) | hitting time from all-D (mutation events) | terminal classes |
|---|---|---|---|---|---|
| 1 (per) | 0 | 1,000 | 1.0000 | 8.94e+03 | 1 |
| 1 (per) | 0 | 10,000 | 1.0000 | 3.58e+04 | 1 |
| 1 (per) | 0.01 | 1,000 | 1.0000 | 1.09e+04 | 1 |
| 1 (per) | 0.01 | 10,000 | 1.0000 | 5.58e+04 | 1 |
| 4 (per) | 0 | 1,000 | 1.0000 | 3.45e+03 | 1 |
| 4 (per) | 0 | 10,000 | 1.0000 | 1.57e+04 | 1 |
| 4 (per) | 0.01 | 1,000 | 1.0000 | 3.52e+03 | 1 |
| 4 (per) | 0.01 | 10,000 | 1.0000 | 1.66e+04 | 1 |
| 4 (total) | 0 | 1,000 | 1.0000 | 8.94e+03 | 1 |
| 4 (total) | 0 | 10,000 | 1.0000 | 3.58e+04 | 1 |
| 4 (total) | 0.01 | 1,000 | 1.0000 | 1.09e+04 | 1 |
| 4 (total) | 0.01 | 10,000 | 1.0000 | 5.58e+04 | 1 |

π(cliques) = 1 in every cell. With fixed total clique mass the hitting time is identical for 1 and 4 spellings. With
mass per spelling, 4 spellings take 0.39–0.44× as long, not the predicted 0.25×. A price of c = 10⁻² slows cliques
by 1.2–1.6×.

### Verdicts

| # | prediction | outcome |
|---|---|---|
| 1 | c = 0 reproduces the free arm | **Holds** (by construction) |
| 2 | atoms: peak and fall, within ±50% of the family estimate; at least 2× below c = 0 at 3·10⁴ | **Mostly holds.** c = 10⁻² holds except 0.0019 at 3·10⁴, just under the band. c = 10⁻³ holds except the suspect cell. At least 3.6× below c = 0. |
| 3 | strict cheaper equivalents take at least 0.8 of FairBot's exits at N ≥ 10⁴ | **Holds** (0.99) |
| 4 | atoms n = 8 within ±30% of n = 6 | **Holds** (within 10%) |
| 5 | depth n = 6 = atoms; n = 8 depth at least atoms | **Holds** |
| 6 | lazy within ±0.05 of c = 0 | **Holds at n = 6.** **Fails upward at n = 8**: 0.81 against 0.72 at c = 10⁻³, and 1.00 against 0.72 at c = 10⁻², from incumbency. The falsifier, below 0.5 or a peak, did not fire. |
| 7 | ladder on graphs: at least 3× neutral at c = 0.1; above at 0.01 | **Holds** at c = 0.1. Above but inconclusive at 0.01. |
| 5′ (Exp 2) | torus entry flat; at least 10× well-mixed at c = 0.1 | **Holds** (flat; 2,400× at N = 1,024) |
| 6′ (Exp 2) | hypercube in between | **Holds** |
| 8 | π(cliques) at least 0.99 | **Holds** |
| 9 | hitting time: 1/4 with mass per spelling; m-independent with fixed total | Mass per spelling **fails** (0.39–0.44). Fixed total **holds** (identical). |
| 10 | price slows cliques less than 2× | **Holds** (1.2–1.6) |

**Reading.**
- Pricing proofs restores both obstacles in a well-mixed population. Entry pays a barrier exponential in N, and the
  shadow becomes a strict, cheaper invader.
- Spatial structure removes the barrier but not the ladder.
- Lazy pricing removes the ladder. At n = 8 it produces full cooperation through a cost-based incumbency that
  favours a cooperative family which punishes ALLC. That family is broad, 46 classes, but rivals FairBot's
  network rather than including it.
- Cliques are absorbing whatever the price.

## Certificates-only arm: tags, D-seeded and C-seeded certificates (`runs/certificates.md`; predictions in `predictions/2026-10-01-certificates.md`)

Designed and run by a subagent; reviewed by astra and fable before the run.

**The arm.** Programs see only the opponent's certificate. Certificates are honest by construction: the certificate *is* the rule, so holding K and behaving as K are the same thing, and label fakers are impossible by definition. The grammar matches the matched control (W0 / M0) node for node, so the length prior is identical. Atoms cost 3 nodes, or 3 + |A| for a literal. Only the meaning of an atom changes:
- **tag**: `EQ(ME)` / `EQ(^A)`, equivalence of certificates, propositional over independent atoms.
- **tageq**: the same with the equality axioms; for example `and(EQ(ME),not(EQ(^D)))` ≡ `EQ(ME)`.
- **lfp** (D-seeded): `IMP(THEM(·))`, "your certificate implies you play C against ·", by synchronous Kleene iteration from all-D.
- **gfp** (C-seeded): the same iteration from all-C. This re-opens "Black-magic fixed points", with the rule stated.
- **lob** / **lob1**: provability in PA (= M0) and in PA + Con(PA).

Divergent pairs (negated self-reference) get D; the fallback breaks the fixed-point equations of 8 pairs at n = 10, with μ×μ weight 1.6·10⁻¹⁰. The evaluator agrees with a tree-level reference on every pair at n = 5 for all variants, and at n = 6 for the D-seeded, C-seeded and tag variants (`tests/test_certificates.py`).

ε→0 chain, PD, w = 0.3, `eager_poly=False`, n = 10 (43 / 33 / 82 / 82 / 25 / 25 classes) and n = 11. Transitions below 10⁻¹³ were dropped, since clique exits are e^(−Θ(N)) and cannot be resolved next to a self-loop of 1; P(C,C) is unchanged at a 10⁻¹¹ cutoff. There were no indeterminate transitions and no polymorphic mass, and cut flow stayed at or below 5.5·10⁻⁷.

| variant (n = 10) | N = 10² | 10³ | 10⁴ | 3·10⁴ | main cooperator | exits from it at 3·10⁴: faker / neutral |
|---|---|---|---|---|---|---|
| tag | 1.000 | 1.000 | 1.000 | 1.000 | `EQ(ME)`, π 0.9999 | none (deleterious only) |
| tageq | 1.000 | 1.000 | 1.000 | 1.000 | `EQ(ME)`, π 1.0000 | none |
| lfp | 0.020 | 0.029 | 0.015 | 0.009 | `IMP(THEM(^C))` | 6.3·10⁻⁴ / 1.6·10⁻⁵ |
| gfp | 0.136 | 0.299 | 0.478 | 0.575 | `IMP(THEM(ME))`, π 0.50 | 0 / 1.7·10⁻⁵ (shadow 0.98) |
| gfp, probe-faker edges suppressed | 0.137 | 0.319 | 0.584 | 0.707 | | |
| lob | 0.138 | 0.319 | 0.584 | 0.706 | `BOX(THEM(ME))`, π 0.36 | 0 / 1.7·10⁻⁵ |
| lob1 | identical to lob | | | | | |

n = 11 is within 0.002 of n = 10 in every variant. Entry ρ(main | all-D) is 0.042 / 0.0136 / 0.0044 / 0.0025 in every arm, a slope of −0.50.

**Tags are efficient, through one parochial clique.**
- `EQ(ME)` has no faker, strict or neutral exit, so it absorbs.
- It mutually cooperates with none of the language's other conditional cooperators: 0 of 7 (tag) and 0 of 4 (tageq) at n = 10; 0 of 11 and 0 of 7 at n = 11.
- The π-support holds 3 mutually defecting clique blocks under tag. The length prior puts 0.9999 on the shortest.
- At N ≥ 10³ the split among cliques is an absorption lottery, not π (rule 5). The log-space escape-rate correction also gives 1.000 to `EQ(ME)`.
- Hitting time from all-D is 2.9·10³ / 9.0·10³ / 2.8·10⁴ / 4.9·10⁴ mutation events.

**D-seeded certificates have no working self-reference.**
- The inductive FairBot defects on itself.
- The only cooperators are third-party probes, faked at an N-independent 6.3·10⁻⁴ by `IMP(THEM(^D))`.
- The curve peaks at 10³ with W0's shape and values, although the semantics differ from W0 on 0.26% of pairs.
- Stratified certificates have only such probes, so they land here too.

**The C-seeded FairBot is a mirror.** It plays against y what y plays against it, so every pair is (C,C) or (D,D).
- Hence it has no faker (π-weighted faker flux exactly 0), and it enters all-D neutrally.
- Cooperation rises with no peak; the cooperative-to-D ratio grows like N^0.34.
- The cooperative support is one network: 0.9999 of cooperative mass, pairwise coverage 0.999. Coverage is tautological for a mirror, so this is compatibility, not a separate finding.
- The C-seeded rule does create loop-only fakers of other residents, for example `not(IMP(THEM(^IMP(THEM(ME)))))` against `IMP(THEM(THEM))`. They carry at most 1.1% of those residents' faker flux.

**The gap between C-seeded certificates and Löb is entirely a fakeable probe.**
- In gfp, `IMP(THEM(THEM))` ("cooperate iff you cooperate with yourself") is faked by `not(IMP(THEM(^C)))` at 1.1·10⁻⁴, independent of N. That faker's self-cooperation rests on a true negative fact, which C-seeded truth sees and no consistent prover proves.
- So π(probe)/π(FairBot) is 0.13 in gfp against 0.97 in lob.
- Suppressing those faker edges closes the gap to within 0.0013 at every N.
- lob1 equals lob, so the gap is truth against provability, not logical strength.

**Against the free modal arm's 0.73 at 3·10⁴:** gfp 0.575, Löb at this grammar 0.706, tags 1.000, lfp 0.009.

**Verdicts.** All 9 held:
1. Tags: P(C,C) ≥ 0.99, `EQ(ME)` ≥ 0.99 of cooperative mass, no non-deleterious exit, entry equal to FairBot's.
2. Tags are parochial under both equivalences.
3. Hitting time is within 1% of 1/(Σμρ); the effective split is ≥ 0.99 on `EQ(ME)`.
4. lfp peaks then falls, as predicted; faker share 0.93 and 0.97 at N ≥ 10⁴.
5. gfp matches the static estimate within ±0.03, with no peak; FairBot faker and strict exits are 0; exit slope −1, entry slope −0.5.
6. gfp has one component with ≥ 0.99 of mass; coverage 0.999.
7. gfp is 0.130 below lob; the probe ratio is 0.127 against 0.969; ablated gfp is within 0.0013 of lob; lob1 is identical to lob.
8. There is no faker flux out of FairBot; the loop-only share is ≤ 1.1%.
9. gfp 0.575, lob 0.706, tags 1.000 and lfp 0.009, all inside the predicted bands.

**Reading.**
- What the modal arm buys is *outcome symmetry*, not provability. A short program whose action against y equals y's action against it, and which defects on D, meets both conditions of the §9.2 conjecture. Löb, coinduction and self-recognition are three ways to get it, and only Löb needs no selection rule.
- Seeing more truth is not free: a reader of truth can be faked through its self-cooperation probe, which costs 0.13 of P(C,C) at N = 3·10⁴.
- Without self-reference, certificates fall back to the weak arm's faker limit.
- Efficiency is built in here as in the modal arm: the mirror, like soundness, excludes FairBot's fakers. The static single-edge estimate was the whole answer, so the content is the comparison across semantics at a fixed grammar and prior, not any one curve.

## Addendum to "Priced arm": chain polish fix and the c = 10⁻³ cells (`runs/priced_recheck.md`, commit a49a007)

**The bug.** Fable found it while reviewing the price-scaling-path brief.
- When a mutant's payoff gap at 1/N is below the polish threshold of 10⁻³, `replicator` projects onto any
  equal-fitness point within 10⁻² and does not check stability.
- For a priced prover entering all-D, that point is the *unstable* separatrix x* = 2c/(1+c). `Chain.fates` accepted
  it as a target.
- This created a polymorphic stepping stone over the cost barrier.

**The fix.** A polished interior point reached from 1/N that is not attracting is now treated as a barrier: the
mutant dies at first order and the valley search runs.

**Who was affected.** Only cells where a payoff gap falls below 10⁻³:
- *Affected:* every c = 10⁻³ cell.
- *Unaffected:* costs at c ≥ 10⁻² are multiples of c, and c = 0 has exact ties. Those cells reproduce exactly
  (0.3453, 0.7068, 0.0150; lazy n = 8 at 1.0000 and 0.8132). The weak, modal, matched-control and certificate arms
  have no small payoff gaps.

**Re-run of all 24 c = 10⁻³ cells.**

| pricing | n | P(C,C) at N = 10² / 10³ / 10⁴ / 3·10⁴, after the fix | before |
|---|---|---|---|
| atoms = depth | 6 | 0.166 / **0.310** / 0.302 / 0.195 | 0.166 / 0.832 / 0.300 / 0.194 |
| atoms | 8 | 0.178 / **0.332** / 0.319 / 0.207 | 0.178 / 0.840 / 0.318 / 0.205 |
| depth | 8 | 0.179 / **0.335** / 0.360 / 0.295 | 0.179 / 0.842 / 0.376 / 0.328 |
| lazy | 6 and 8 | unchanged | — |

- The suspect cell (atoms/depth, c = 10⁻³, N = 10³) was 0.83 and is now 0.31, matching the two-edge prediction. The
  attribution in "Suspect cell" above is confirmed.
- **Prediction 2 now covers that cell.** The c = 10⁻³ curve peaks and falls (0.17 / 0.31 / 0.30 / 0.19 at n = 6),
  inside the ±50% band around 0.17 / 0.36 / 0.39 / 0.27. Every fixed priced cell is at or below the free arm at the
  same N.
- **Remaining polymorphic mass at n = 8** (0.7–1.2% under atoms and depth) is genuine, not an artifact.
  - `BOXD(THEM(^C))` cooperates with the incumbent `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` and pays less.
  - It defects on its own kind.
  - So it is a price-ladder rung with a stable interior rest point, at x* = c (depth) or 3c (atoms); the
    2×2 game has a positive gap when rare and a negative gap when common.
  - Its cost to P(C,C) is about 0.1%.
- Lazy n = 8 at c = 10⁻³ remains above the free arm (0.813 against 0.725 at N = 3·10⁴). That is incumbency, not
  numerics: the cell has zero polymorphic mass and is unchanged by the fix.

## Price scaling paths: c_N = c0·(N/10³)^(−α) (`runs/scaling_path.md`; predictions in `predictions/2026-10-01-price-scaling-path.md`)

**Setup.** ε→0 chain, PD, w = 0.3, atoms pricing, fixed chain (a49a007), `eager_poly=False`. n = 6, with one n = 8
path. Every cell has zero polymorphic mass, and every n = 6 priced cell is at or below the free arm at the same N, so
no artifact flags fired.

**P(C,C)** at N = 10² / 10³ / 10⁴ / 3·10⁴ / 10⁵ / 3·10⁵, with the fitted log-odds slope over [10⁴, 3·10⁵]:

| path | P(C,C) | slope (predicted) |
|---|---|---|
| free arm, c = 0 | 0.169 / 0.345 / 0.587 / 0.707 / **0.814** / **0.883** | local β 0.49 (3·10⁴–10⁵), 0.50 (10⁵–3·10⁵) |
| c0 = 10⁻², α = 0.25 | 0.118 / 0.116 / 0.050 / 0.029 / 0.014 / 0.0056 | −0.65 (−0.61 to −0.70) |
| c0 = 10⁻², α = 0.5 | 0.088 / 0.116 / 0.110 / 0.105 / 0.101 / 0.098 | −0.04 (−0.05) |
| c0 = 10⁻², α = 0.6 | 0.074 / 0.116 / 0.141 / 0.152 / 0.166 / 0.182 | +0.09 |
| c0 = 10⁻², α = 0.75 | 0.052 / 0.116 / 0.196 / 0.242 / 0.302 / 0.365 | +0.25 (+0.24) |
| c0 = 10⁻², α = 1 | 0.020 / 0.116 / 0.302 / 0.426 / 0.577 / 0.704 | +0.50 (+0.47) |
| c0 = 10⁻², α = 1.5 | 0.0001 / 0.116 / 0.476 / 0.649 / 0.790 / 0.874 | +0.60 |
| c0 = 10⁻³, α = 0.5 | 0.159 / 0.310 / 0.476 / 0.539 / 0.577 / 0.588 | +0.13 |
| c0 = 10⁻¹, α = 0.5 | 10⁻⁴ / <10⁻⁴ at every N ≥ 10³ | — |
| c0 = 3·10⁻², α = 0.25 (barrier path) | 0.055 / 0.019 / 0.0023 / 0.0005 / <10⁻⁴ (N ≤ 10⁵) | −1.7 |
| n = 8, c0 = 10⁻², α = 0.5 | 0.094 / 0.123 / 0.116 / 0.111 / 0.107 / 0.104 | −0.04 |

**All 11 verdicts held.**
1. α = 0.25 declines monotonically from N = 10³, inside the FairBot-only/family band at every N. It sits nearer the
   FairBot-only end.
2. α = 0.5 stays in [0.06, 0.15] at every N ≥ 10³.
3. The α = 0.5 plateau is set by c0: 0.59 at c0 = 10⁻³, 0.10 at 10⁻², below 10⁻⁴ at 10⁻¹. Fable's patched cells had
   been seen before the commit.
4. α = 0.75 rises within ±30% of prediction at every N.
5. α = 1 rises; its odds are 0.304 / 0.308 / 0.312 / 0.315 of the free arm's at N ≥ 10⁴, against (1 − e⁻³)/3 = 0.317.
6. α = 1.5 converges: it is within 0.023 and 0.009 of the free arm at 10⁵ and 3·10⁵, with an odds ratio of
   0.64 → 0.77 → 0.86 → 0.92.
7. α = 0.6 rises slowly, as predicted.
8. The barrier path collapses: below 10⁻⁴ at N = 10⁵ as 2wc²N passes 5.
9. The free arm extends to 0.814 and 0.883, inside 0.80 ± 0.05 and 0.87 ± 0.05.
10. n = 8 is within 8% of n = 6.
11. Every slope is inside its ±0.15 window. d(slope)/dα over the four c0 = 10⁻² paths with 0.5 ≤ α ≤ 1 is 1.08,
    inside [0.8, 1.2].

One falsifier was vacuous as implemented: "measured edge rates deviating > 2× from static". The diagnostic columns
are themselves static fixation computations, so that check is not independent.

**Reading.**
- The full chain follows the two-edge reduction along shrinking-price paths, at n = 6 and n = 8. With the free arm's
  local exponent now measured at 0.49–0.50, both empirical premises of the proposition hold over this range:
  - (i) β → 1/2;
  - (ii) the reduction holds.
- So a compute price is compatible with efficiency in the limit iff it vanishes faster than N^(−1/2) of the stakes:
  - α > 1/2 gives cooperation → 1;
  - α = 1/2 is a knife edge, with a plateau set by c0;
  - below 1/2 the ladder takes cooperation to 0, and then the barrier takes it down exponentially.
- α = 1 still goes to 1, but with a constant odds penalty. Only α > 1 recovers the free arm's odds.
- The RS's iterated limit lim_N lim_c is the safe end of this family and coincides with the free arm.
- Self-play changes FairBot's entry by 0.4–6.5% (static) and does not move the boundary.

## Not done

- Prediction (c) at n=9 through the chain (the enterer search covers what
  L_9 can do against all-D and all-p, but not the full n=9 chain).
- N = 1000 in the weak arm.
- Polymorphic-target ρ beyond the truncated-product approximation.
