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

## Certificate pricing (decidability-based free set): one network, not faster (`runs/cert_pricing.md`; predictions in `predictions/2026-10-01-cert-pricing.md`)

Designed and run by a subagent, reviewed by astra and fable before the run, and re-run in full on the fixed chain
(a49a007). Old-chain cells differed by at most 6·10⁻⁵. Not to be confused with "Certificates-only arm" above.

**The arm** (`src/cert_priced.py`). Lazy's price function, c·k(x)·(1 + settle world), is unchanged; only the set of
free checks changes.
- **cert0** (primary). x's check of y is free iff PA decides y's action toward x, meaning y's value toward x is
  constant over all GL worlds. Constants are always decided, so entry into all-D stays neutral.
- **Variants:**
  - cert1: decided in PA + Con(PA);
  - certC: constants plus PA-certified cooperation only;
  - mono: a syntactic twin. Free iff y is constant, or y is monotone in its box atoms and either cooperates with x or
    plays D at world 0.
- **Controls:**
  - cert0flat: cert0's free set with a flat price c on every other check;
  - lazycert0: lazy's free set ∪ cert0's;
  - cert0diag: constants plus only those copies whose self-play PA decides.

Grid: ε→0, PD, w = 0.3, n ∈ {6, 8}, c ∈ {10⁻³, 10⁻²}, N ∈ {10², 10³, 10⁴, 3·10⁴}, plus N = 10⁵ for three cells.

**What cert0 is.** Every box is true at world 0, and box truth only falls with the world index. So a program monotone
in its atoms that ends up cooperating has cooperated at every world, and PA decides it.
- 330 of 610 canonical functions are monotone, carrying 98.7% of the prior mass.
- cert0 and mono differ on μ⊗μ weight 3.6·10⁻³ of 0.58, and their chains agree within 7.5·10⁻⁴.
- In effect, cert0 charges only for cooperation conditional on *non*-provability. That is the P* family's defining
  feature.
- It is not sameness: 9,267 of 20,353 mutually cooperating pairs are free both ways, against 0 under lazy, and 142 of
  287 self-cooperators pay to read their own copies.

**n = 8.**
- *X* is the π-weighted probability that two cooperative programs cooperate.
- *Rival share* is 1 minus the largest block's share of the mutual-cooperation graph over cooperative states with
  π ≥ 10⁻³, ALLC excluded.

| pricing | c | P(C,C) at N = 10² / 10³ / 10⁴ / 3·10⁴ / 10⁵ | rival share at N = 10³ / 10⁴ / 3·10⁴ / 10⁵ | X at the same N |
|---|---|---|---|---|
| free | 0 | 0.182 / 0.371 / 0.617 / 0.725 / 0.814 | 0.067 / 0.100 / 0.110 / 0.125 | 0.87 / 0.81 / 0.80 / 0.77 |
| lazy | 10⁻³ | 0.182 / 0.371 / 0.630 / 0.813 | 0.068 / 0.141 / 0.453 | 0.87 / 0.75 / 0.50 |
| lazy | 10⁻² | 0.182 / 0.379 / 0.998 / 1.000 / 1.000 | 0.096 / 0 / 0 / unresolved | 0.82 / 0.99 / 1.00 |
| cert0 = certC = mono | 10⁻³ | 0.182 / 0.368 / 0.597 / 0.702 | 0.035 / 0.018 / 0.007 | 0.92 / 0.96 / 0.98 |
| cert0 = certC = mono | 10⁻² | 0.181 / 0.357 / 0.592 / 0.700 / 0.792 | 0.012 / 0 / 0 / 0 | 0.97 / 0.99 / 0.99 / 0.99 |
| cert1 = cert0flat | both | free arm ± 0.0007 | as free | as free |
| lazycert0 | both | lazy ± 0.0013 | as lazy | as lazy |
| cert0diag | 10⁻² | 0.181 / 0.358 / 0.676 / 1.000 | 0.012 / 0 / 0 | 0.97 / 0.84 / 1.00 |

- **n = 6.** Every certificate variant is within 0.0008 of c = 0; there is no P* at that size.
- **Support and transitions under cert0.**
  - Support: all-D plus one FairBot-containing block (FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`,
    `BOX1(THEM(THEM))`, and PrudentBot at 0.4–2%).
  - Top state: FairBot. It has no strict exits, and its neutral exits equal the free arm's to three digits, 0.96 into
    ALLC.
  - One terminal class in every cell: no lottery, no near-closed classes, no indeterminate transitions. θ = 10⁻⁷ gives
    results identical to 10⁻⁶.
  - Polymorphic mass is 0.0078 in the c = 10⁻³, N = 10³ cells. That is the genuine ladder-rung state from the
    priced-arm addendum; it is zero elsewhere.
- **The P\* block under cert0.**
  - It pays 4c at home. Its cheaper equivalents `not(BOX(THEM(ME)))` and `not(BOX(THEM(THEM)))` pay 2c and invade it
    strictly, N-independent (1.85·10⁻⁵ at c = 10⁻²). Both cooperate with D, so D takes 0.93 of their exits.
  - π(P* block) at 3·10⁴ is 0.0005 (c = 10⁻²), against 0.079 in the free arm and 1.0 under lazy.
  - cert0 matches the renewal identity (P_free − p)/(1 − p), with p the block's free-arm mass, to within 0.0021. The
    whole drop from c = 0 is the P* block's excursions being deleted.
- **Controls: what does what.**
  1. *The copy subsidy is the lock-in.* lazycert0 equals lazy. cert0diag at c = 10⁻² locks in PrudentBot instead
     (0.9998 at N = 3·10⁴). PrudentBot cooperates with FairBot, so that lock-in is universal, not parochial.
  2. *The atom ladder, not the free set, removes the rival block.* Under cert0flat, P*'s exits are neutral and ∝ 1/N,
     and the block keeps its free-arm share (rival share 0.10–0.11).
  3. *Without the subsidy, cert0 gives one network at the free arm's rate.* The cooperative-to-D local slope is
     0.42–0.43, against 0.44–0.45 free; from 3·10⁴ to 10⁵ it is 0.406 against 0.420.
  4. *An exact zero is load-bearing* (static only). Charging c/10 on certified checks by programs with boxes rebuilds
     the ladder: ALLC strictly invades FairBot at 1.4·10⁻⁴ (c = 10⁻²), N-independent.
- **Lazy, c = 10⁻², N = 10⁵** (not scored). Four locked-in states have exits near 10⁻⁵⁰, so their split is not
  resolved in double precision, though P(C,C) = 1 is robust. The exits at 3·10⁴ suggest the resolved answer is the
  P* block.

**Verdicts.** 13 of 14 held. Verdict 3 held except at one cell, c = 10⁻³, N = 10³, which was +0.013 against a ±0.01
tolerance because the P* block's polymorphic rung is not counted in p. No falsifier fired. Two cells were reproduced
on main (cert0 and cert0flat at n = 8, c = 10⁻², N = 10⁴: 0.5919 and 0.6169).

**Reading.**
- On the GL chain, the certification criterion is, to 0.6% of pair weight, *syntactic monotonicity*: box-positive
  programs certify themselves.
- Certificate pricing yields one cooperative network containing FairBot, but no faster than the free arm.
- Every mechanism here that beats the shadow's 1/N exit is a *moat*: a copy subsidy (lazy, cert0diag) or a clique. A
  moat locks in whichever ALLC-punishing family it reaches first, chosen by prior and exit rate. That family can be
  parochial (P*) or universal (PrudentBot).
- "One network" and "faster than 1/N" have not been obtained together.

## Rival networks under lazy pricing on graphs (`runs/rival_networks.md`; predictions in `predictions/2026-10-01-rival-networks.md`)

Designed and run by a subagent, reviewed by astra and fable before the run.

**Set-up.**
- *Arm:* lazy-priced modal arm, n = 8, PD, w = 0.3, c ∈ {0, 10⁻², 10⁻¹}. P* = `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` and FB = `BOX(THEM(ME))`.
- *Labels*, assigned from actions:
  - D-type;
  - exploitable (cooperates with D);
  - FB-net: mutual cooperators with FB that defect on D, 72 classes, μ = 0.0237;
  - P\*-net: the same with P*, 4 classes, μ = 5.5·10⁻⁶;
  - other-coop.

  FB-net outweighs P*-net in prior mass by 4,300×. The "46 classes" P* cooperates with are mostly exploitable.
- *Update rule:* death-birth.
- *Kernel check:* exact against Monte Carlo on hypercube d = 3 and a 3 × 3 torus.

**Static blocks.**
- FB | D and P* | D are one block, so the two networks enter all-D identically on any graph.
- FB's only neutral mutant at c > 0 is ALLC. P* has no neutral and no strict mutant.
- P*'s nearest exit is its own shadow, `not(BOX(THEM(ME)))`, which pays half P*'s price on their shared edges.

**R1: per-mutant hitting probabilities to N/2 (ε-free).** Torus side 16 / 32 / 64; hypercube d = 6 / 8 / 10.
- *Entry:* FB | D = P* | D is 0.109 / 0.105 / 0.103 on the torus, N-flat at every c. On the hypercube it is 0.081 / 0.063 / 0.044. Well-mixed values are 0.027 / 0.013 / 0.007.
- *Shadows:*
  - ALLC | FB is neutral (2/N) on every graph.
  - ALLC | P* is 0 in 10⁵.
  - D | FB and D | P* are 0 in 10⁵, except hypercube 6 (1.4·10⁻⁴, never fixing).
  - D | ALLC is 0.15–0.21.
- *Lazy incumbency is a well-mixed effect on the torus.* A newcomer cluster's interior is all copies, so it pays only on its border, and there P* pays more.
  - P*'s shadow invades P* at 0.8–2.1 × 2/N at c = 10⁻², and at an N-independent 0.005–0.0075 at c = 10⁻¹. Well mixed, that rate is 4·10⁻²¹.
  - FB | P* at c = 10⁻¹ is 3·10⁻⁴ / 5·10⁻⁵ / 9·10⁻⁵.
  - On the hypercube the barrier returns as degree grows: at d = 10, c = 10⁻¹, P* has no exit in 10⁵ trials of any measured block.

**R2: partially lumped ε→0 chain on graphs (a representative model).**
- *States:* 16 residents, the heaviest members of each label.
- *Inputs:* 534 measured blocks per graph. At torus 64, 144 tier-2 blocks fall back to the primary representative and 1 is missing.
- *Validation:* well mixed, it matches the full chain within 0.003.

| graph | c | self-cooperating mass | π(D) | π(FB-net) | π(P*-net) |
|---|---|---|---|---|---|
| torus 16 / 32 / 64 | 10⁻² | 0.661 / 0.821 / 0.956 | 0.339 / 0.180 / 0.044 | 0.626 / 0.789 / 0.946 | 0.022 / 0.025 / 0.009 |
| torus 16 / 32 / 64 | 10⁻¹ | same within 0.003 | same | — | 0.010 / 0.008 / 0.001 |
| hypercube 6 / 8 / 10 | 10⁻² | 0.148 / 0.520 / 0.665 | — | — | — |

- *Rates of π(D):* on the torus it falls with log-slope −0.74 overall (−0.46, then −1.02 over the last doubling of side). Entry is N-independent and the shadow exit is 1/N, so π(D) heads toward N⁻¹, against N^(−1/2) well mixed.
- *Comparison:* well mixed at N = 4,096, c = 10⁻², P*-net holds 0.45 and FB-net 0.27.
- *Transitions, torus 64, c = 10⁻²* (per mutation event):

  | from | to | rate |
  |---|---|---|
  | D | FB-net | 2.4·10⁻³ |
  | D | P*-net | 5.6·10⁻⁷ |
  | FB-net | ALLC | 1.1·10⁻⁴ (0.47/N) |
  | P*-net | its shadow | 2.9·10⁻⁶ |
  | exploitable | D | 8.1·10⁻² |

- *Support:* monomorphic states only.
- *Hypercube d = 10, c = 10⁻¹:* P* is absorbing in sample, so its π is not trusted. The upper-bound variant gives self-cooperating mass 0.65.
- **Prior-swap control.** Give P*-net FB-net's prior mass and P*-net takes 0.95–0.98 of the torus mass (0.84 at side 64, c = 10⁻¹). FB-net's ε→0 dominance on graphs comes from prior mass, not universality.

**R3: domain competition without mutation (ε-free).**
- *c = 0:* symmetric, with P(FB first) between 0.517 and 0.54, every interval including ½.
- *Band start, c > 0:* FB wins.
  - c = 10⁻²: 0.56 / 0.71 / 0.93 on the torus, 0.54–0.62 on the hypercube.
  - c = 10⁻¹: 0.90 / 1.0 / 1.0 on the torus, 0.68 / 0.85 / 0.99 on the hypercube.
- *Front velocity:* matches first order (9.2·10⁻⁴ and 9.1·10⁻³ per cross edge per generation, at c = 10⁻² and 10⁻¹).
- *Droplets:* a P* disc in FB is lost in every run at c > 0.
- *Interface:* rival borders roughen to 3.3–4/side of edges.

**R3b: controlled fronts (no mutation; ALLC seeded at density x in the FB half).**
- *Torus:* P* eats the front's ALLC and nothing refills it. The crossing is 0.05–0.15 at c = 10⁻² and above 0.4 at c = 10⁻¹.
- *Hypercube:* there is no depletion, and the crossing is near the static threshold, x* = 0.118 at c = 10⁻¹.

**R4: agent-based runs at finite ε (approach rates, not π).** Torus 128² and hypercube d = 14, N = 16,384, ε = 10⁻³.
- *From all-D:*
  - FB-net is the majority by generation 2,000 in all 20 runs.
  - Second-half P(C,C) is 0.977–0.999.
  - The ALLC load x = ALLC/(ALLC + FB-net) is 0.20, and 0.10 at ε = 10⁻⁴.
  - P* never establishes on the hypercube.
  - One torus run went to a PrudentBot sea (0.988). PrudentBot punishes ALLC but sits inside FB-net.
- *From a half split:*
  - c ≤ 10⁻²: P* wins the torus (8 of 8, by generation 800–4,400).
  - c = 10⁻¹: FB wins.
  - Controls: with no ALLC in the mutation supply, FB wins; with only C and D in the supply, P* wins.
- *Welfare:* while both networks hold at least 10% (1,000–4,000 generations), rival-border mutual defection covers 0.032–0.040 of edges, 6× the D fringe. Second-half interaction welfare loss is 0.005–0.020, and compute cost per edge is ≤ 0.0014.

**Verdicts.** No falsifier fired. Of 23 verdicts:
- *Held:* most, including entry, shadows, the partial-chain validation, symmetry, FB winning the band, velocity, droplets, the finite-ε outcomes and the split runs.
- *Failed:*
  - 4: torus-16 rival nucleation, more suppressed than predicted;
  - 5: FB | P* at c = 10⁻¹, narrowly;
  - 6: hypercube 10 at c = 10⁻², 0.58 of 2/N;
  - 15: interface 3.3–4/side, not ≤ 3/side;
  - 17: the torus front crossing, because of depletion;
  - 19: torus ALLC load 0.20, not 0.01–0.10;
  - 23: border welfare loss 6× the fringe, not below it.
- *Narrow misses within 7:* the torus-16 mass (0.66) and the π(D) slope (−0.74).

**Reading.**
- *ε→0 on graphs:* structure makes both entry and P*'s shadow exit graph-local. That dissolves lazy pricing's cost incumbency on the torus, and which network holds the mass is then set by prior mass.
- *Finite ε:* the border goes to whichever ALLC-punisher is present, because it converts the mutation-supplied shadow into food. That punisher may be outside the universal network (P*) or inside it (PrudentBot).
- *The graph family matters:* as hypercube degree grows, the well-mixed lock-in returns.
- *Welfare:* rival borders are costly while they exist, but they last only thousands of generations.

## Ergodic islands: mutation re-injected (`runs/ergodic-islands.md`; predictions in `predictions/2026-10-02-ergodic-islands.md`)

Designed and run by a subagent, reviewed by astra and fable before the run. Fable computed some chain cells before the commit; they are disclosed in the brief, and those verdicts are marked *(seen)*.

**Setup.**
- PD, w = 0.3, no island-level selection (w_g = 0).
- Arms: the weak arm L_6 with `ROLE` (reciprocator R = `THEM(^C)`), and the modal arm at n = 6 (R = FairBot).
- mN, the migrants per island per generation, is held fixed as N varies.
- **A. The ε→0 two-level chain** (`src/ergodic_islands.py`).
  - It runs over monomorphic metapopulation states, with transitions μ(q)·Φ(q|a), where Φ is the chance that one mutant on a random island takes the whole metapopulation.
  - Φ₂ is the rare-migration value ρ_N(q|a)·(1 − 1/r)/(1 − r^−I), with r = ρ_N(q|a)/ρ_N(a|q). It is the same on every regular island graph.
  - At I = 1 the chain reproduces the existing lim_N and modal tables exactly.
- **B. Φ_MC:** Monte Carlo to global absorption at fixed mN, with Wilson intervals, on complete, hypercube and torus island graphs.
- **C. Finite-ε agent-based runs:** 2·10⁵ generations, 3 replicates. These are approach rates, not π.

**Three rates set the ε→0 object.**
- **Entry depends on island size.** At mN ≤ 1 it is independent of I and of the graph: 24 of 24 cells sit in their bands around ρ_N, and 12 of 12 graph ratios contain 1. It falls with migration: 0.043 / 0.042 / 0.033 / 0.021 at mN = 0.1 / 1 / 3 / 10 (I = 64, N = 100).
- **The shadow exit is exactly 1/(IN).**
- **The faker exit does not depend on structure.** In this PD the faker's selective edge is constant (T + S = R + P), so Φ = 1 − 1/r at any m, any I and on any regular graph. All 11 faker cells fit, at mN 0.1–10 on all three graphs: `THEM(^D)` 0.255–0.287 against 0.264.

**Weak arm, ε→0.**
- **The faker's share of exits depends only on total size M = IN**, to within 0.011 of f/(f + 0.2493/M).
  - It crosses ½ at M ≈ 860.
  - It is 0.88 for every split of M = 6,400, and 0.96 at M = 25,600.
- **π(all-`THEM(^C)`) follows the three-rate reduction** to within 4.4% for N ≥ 10. It rises with I to a plateau p*(N) = μ_R·ρ_N(R|D)/f: 0.125 at N = 10–16, 0.069 at N = 100, 0.024 at N = 1,000.
- **That plateau falls like N^−0.46.** P(C,C) never exceeds 0.127, which is 5–10× the well-mixed peak but not efficient along any island family.
- **Support and transitions.**
  - The support is all-D (0.85–0.99) and all-`THEM(^C)`.
  - A weak-faker sink, `and(X,THEM(^D))`, grows ∝ I to at most 0.011.
  - Entry is carried by `THEM(^C)` (0.99 of cooperative entry for N ≥ 25).
  - The roads out are faker → all-C → D and shadow → all-C → D.
  - There are no polymorphic states and no indeterminate transitions.
- **Patched chain** (exploratory; measured Φ_MC substituted). It stays within 0.86–1.18 of the plain chain's π_R at mN ≤ 1. At mN = 10 it gives 0.030, 3.5× well-mixed, so islands keep half their entry advantage even at 10 migrants per island per generation.

**Modal arm, ε→0: efficient faster on islands than well-mixed.**
- At N = 100, P(C,C) is 0.418 / 0.712 / 0.899 / 0.972 / 0.993 at I = 4 / 16 / 64 / 256 / 1024.
- Well-mixed at the same M it is 0.536 (M = 6,400) and 0.691 (M = 25,600).
- The log-odds slope in I is 0.97, so odds grow ∝ M at fixed island size, against M^½ well-mixed. Islands beat well-mixed in all 19 equal-M cells.
- The gain comes from the three unfakeable provers. The six fakeable provers' share falls like I^−0.92 (0.46 → 0.003), so islands purge fakeable provers from the cooperative family.

**Finite ε (approach rates; I grows at fixed per-island εN).** Adding islands *hurts* the weak arm. At εN = 0.1, mN = 1, N = 100:

| I | P(C,C) | R-dominant island-time |
|---|---|---|
| 16 | 0.154 (does not mix; indeterminate) | 0.051 |
| 64 | 0.144 | 0.029 |
| 256 | 0.040 (hypercube 0.024) | 0.008 |

- *Why:* global mutation supply I·εN grows with I, so fakers are always present somewhere and spread by migration.
- *Exits:* fakers carry 0.78–0.84 of exits from ≥ 90%-R islands. At N = 25 the shadow dominates instead.
- *What makes up P(C,C):* at I = 64, of the 0.144, R-dominant islands contribute only 0.028, below the chain's π_R of 0.062. The rest is probe self-play (0.049), ALLC islands (0.036) and others.
- *Modal arm:* 0.98 at εN = 0.1 and 0.997–0.999 at εN = 0.01, at every I.

**Verdicts.**
- *Held:* 1 (weak plateau), 4 *(seen)*, 5 (faker Φ invariant, 11/11), 6 (entry bands, 24/24), 7 (graph independence, 12/12), 11 and 13.
- *Held on the interval rule:* 8. The mN = 10 entry was 0.0209, above its band and 0.0002 short of the falsifier.
- *Partly held:*
  - 2: "weak + other exits < 0.01" failed at small M;
  - 3: support claims failed at N ≤ 16, I = 1;
  - 9: the mN = 10 part failed;
  - 12: failed at I = 256;
  - 14: weak I = 16 does not mix.
- *Failed:* 10, finite-ε flat in I.
- No falsifier fired.

**Reading.**
- On regular island graphs without group selection, structure acts only on entry (local relatedness) and on the shadow (total size). It never acts on the faker, whose fixation is a constant-selection invariant.
- So the weak arm stays at or below 0.13 along any island family. Its failure in the limit is fakeability.
- Structure and unfakeability are complements. Islands make the modal arm's odds grow ∝ M and purge its fakeable provers.
- The order of limits matters: many islands at fixed per-island ε are worse than the ε→0 chain (0.04 against 0.067 at I = 256), because faker supply grows with I.

## Universality against drift-closure: moats without copy subsidies (`runs/drift_closure.md`, `runs/drift_closure_static.md`; predictions in `predictions/2026-10-02-drift-closure.md`)

Designed and run by a subagent, reviewed by astra and fable before the run. ε→0 chain, PD, w = 0.3, `eager_poly=False`, 102 cells. Two cells were reproduced on main: D fringe n = 6, N = 10⁴ gives 0.9885, and the PrudentBot prior boost at n = 8 gives 0.9761.

**Part 1: proofs.** The setting is the PD with four distinct payoffs, deterministic programs (self-play is (C,C) or (D,D)), and the chain's fixation rule (mean field, no self-play, exp fitness).
- **Lemma 1.** From a world of self-cooperating x, a single mutant has one of three fates:
  - a *faker* (defects on x while x cooperates with it) fixes with N-independent probability;
  - a self-cooperator that plays (C,C) with x is exactly neutral and fixes with probability 1/N;
  - every other mutant fixes with probability e^(−Θ(N)).

  Polymorphic and valley routes add only e^(−Θ(N)).
- **Proposition 1.** x's neutral closure is its component K(x) in the graph of mutual cooperation among self-cooperators. x is *drift-closed* iff no member of K(x) can be suckered.
- **Corollary 1** (the §9.7 regress, exact). ALLC is in FairBot's component, and D suckers ALLC. So every drift-closed class has universality 0, meaning it mutually cooperates with nothing in FairBot's component. The content is the static fact that ALLC lies in that component.
- **Proposition 2** (rate law). Assumptions:
  - an unsuckerable core;
  - entry neutral at one copy;
  - fakers that leave the network;
  - all-D holding the non-cooperative mass.

  Then a non-closed network exits at Θ(1/N), and the cooperative odds are Θ(N^(1/2)). So β = 1/2, an empirical premise of the price-scaling proposition, is derived. Any class that cooperates with FairBot has a leak floor of about 0.9·μ(FB)/N.
- **Proposition 3** (prices). Let prices be non-negative, with constants free. Then in any world that tolerates ALLC, ALLC weakly dominates the resident. A family exits faster than 1/N only if every path into ALLC-tolerant worlds is blocked by local incumbency: a newcomer must pay more to read the incumbent than the incumbent pays to read itself. For a family that cooperates with FairBot, that is c(FB, y) > c(y, y), a moat.

**Static map.** The mutual-cooperation graph is one component at every n tested (6–11 with boxes up to PA + Con; 8–9 up to PA + Con²), with or without ALLC. No class is drift-closed. Along the rungs of prudence, universality and leak fall together (n = 10):

| class | order of prudence | cooperates with FairBot | universality | leak |
|---|---|---|---|---|
| FairBot | 0 | yes | 0.77 | 0.48 |
| PrudentBot | 1 (defects on D-cooperators) | yes | 0.33 | 5.2·10⁻³ |
| P* | 2 (defects on ALLC-cooperators) | no | 0.10 | 3.3·10⁻³ |
| P12b (size 14, needs PA + Con²) | 1 and 2 | no | ~10⁻⁴ | 2·10⁻⁶ |

- P* is behaviourally second-order prudence. The positive form `and(BOX(THEM(ME)),BOXD_L(THEM(^C)))` never self-cooperates at any level tested.
- Each added order of prudence costs one Con level.
- Per unit of prior, FairBot has the smallest leak of any unsuckerable class: leak/μ is 93–96 at n = 6–11, against about 3,700 for PrudentBot and 1,100 for P*.

**Chain verdicts.** 11 of 12 held.
1. The references reproduce. The free arm at n = 9, N = 10⁵ gives 0.814.
2. *PrudentBot at FairBot's prior mass.* The family and the constant change, not the exponent.
   - P(C,C) 0.752 / 0.924 / 0.976 / 0.986 / 0.992 at N = 10²–10⁵.
   - The prudent family holds 0.94–0.95 of cooperative mass.
   - Exit slope −0.99, odds slope 0.49.
3. *High-order prudence gains nothing once its siblings are in the language.* P12b added alone takes everything, but that is a language-coverage artifact. With its five same-size siblings, odds are only 4–7× the boosted PrudentBot's, with exit slope −0.84.
4. *D fringe at n = 6* (a fixed background of D that charges cooperation with D). The network stays universal: P(C,C) 0.9885 / 0.9933 / 0.9963 at 10⁴ / 3·10⁴ / 10⁵, with exit slope −1.00.
5. *D fringe at n = 8.* The network goes to the parochial P* family (rival share 0.92–0.95), still at exit slope −1.
6. *CD fringe at n = 8* (also rewards exploiting ALLC). Two rival blocks; prudent/rival goes 0.46/0.51 → 0.86/0.14 by 3·10⁵.
7. *CD fringe at n = 6.* FairBot's entry barrier shows as an odds slope of 0.14.
8. *μ fringe at n = 8* (the prior as a background population). Families close as a crossover in N: exit slopes −3.2 and then about −22, ending on P* at 1.000 by 3·10⁵, where exits are 3·10⁻¹⁸.
9. *μ fringe at n = 6* (no parochial family exists at this size). One universal network with an exit faster than 1/N: exit slopes −2.45 and −5.72, and 1 − P = 3.4·10⁻⁵ at 10⁶.
10. *D fringe along δ_N = 10/N.* P(C,C) 0.890 / 0.933 / 0.962, odds slope 0.50.
11. *The open problem.* No cell at n ≥ 8 has one FairBot-cooperating network (rival < 0.05) together with an exit slope ≤ −1.3.
12. *Numerics: failed in part.*
    - Indeterminate transitions in four μ cells, with π-weighted mass ≤ 2.4·10⁻⁹.
    - Cut flow up to 2.7·10⁻⁵ in four small-N cells, against a limit of 10⁻⁵.
    - Kept exit share below 0.99 in the CD and μ cells at n = 8, the dropped exits going to one-copy polymorphic twins.
    - A θ = 10⁻⁹ re-run leaves the family shares and P(C,C) unchanged.

**Support and transitions.** Every cell has one terminal class and no near-closed classes. Polymorphic flow is below 2·10⁻⁴. Top states: FairBot (free), PrudentBot (boost, CD), P* (D and μ fringes at n = 8), `BOX(THEM(THEM))` (μ fringe at n = 6).

**Reading.**
- In the pure game, one universal network and an exit faster than 1/N are incompatible: Corollary 1 with Proposition 2. The exponent 1/2 is derived.
- Prices with free constants beat 1/N only through incumbency (Proposition 3).
- The one mechanism outside both results is a fringe, which acts like an opponent-independent price on constants. It can close families, but at n ≥ 8 it hands the mass to the parochial P*, because it selects for exploiting the background.

## Conjecture 4: the sibling theorem, and the leak at n ≤ 13 (`runs/conjecture4.md`, `notes/conjecture4.md`; spec `specs/2026-10-04-conjecture4.md`, predictions in `predictions/2026-10-04-conjecture4.md`)

Designed by the RE under the spec workflow, reviewed by gpt-6.1-sol, run by an Opus subagent. The RE re-checked the construction on FairBot, PrudentBot and P* with the independent evaluator `src/conj4.py` after the merge.

**Theorem (no drift-closed class, levels unbounded).** In the modal language with boxes at every PA + Con^k level, every self-cooperating class has a suckerable neighbour in the mutual-cooperation graph, one step away. So no class is drift-closed.

*Construction.* Take a self-cooperating x that defects on D (otherwise x is suckerable at distance 0). Let F(x) be x together with all its fixed arguments ^A, recursively, and let K be the largest world by which any P ∈ F(x) has settled against D.
- ψ_K = `and(not(BOX_K(THEM(^D))),not(BOXD_K(THEM(^D))))`: "your play against D is undecided in PA + Con^K".
- Sibling y = `or(x, ψ_K)`, of size |x| + 12.
- Faker z = `BOX_K(THEM(^D))`, of size 4.

*Lemmas.*
- A (finite settling): each box atom flips at most once after its level, so every play sequence settles.
- B: ψ_K is false at every world against any opponent whose play against D has settled by world K.
- C (mimicry): by induction on worlds, y and x play identically against every P ∈ F(x) ∪ {D}; every such P plays y as it plays x; and y against y matches x against x. x sees an opponent only through finitely many probes (its play against x, against itself, against x's fixed arguments), and ψ_K is silent on all of them.
- D: settle(P, D) ≤ maxlevel(P) + 1, so K ≤ maxlevel(x) + 1. The sibling needs exactly one more Con level than x uses.

*Proof.* By C, y and x cooperate with each other and y cooperates with itself, so y is adjacent to x. z defects on y because y defects on D. z's own play against D is C up to world K and D after, so it is undecided at level K: ψ_K(z) holds and y cooperates with z. So y is suckerable. ∎

*Dependency ledger.* Lemmas A, B, D use the linear chain and the level structure. Lemma C and the theorem use only extensional observation through finitely many probes. No step uses Löb; Löb supplies only x's self-cooperation, which y inherits. The arithmetic lift uses de Jongh–Sambin uniqueness, the letterless reduction, arithmetic soundness of GL, and the consistency of every PA + Con^k. The theorem is about monomorphic residents only.

*Evaluator check.* `src/conj4.py` is an independent trace evaluator; it agrees with `modal_lv` on 3,000 random pairs per language. It checked every self-cooperating canonical function at n = 6–11 with one level and n = 6–9 with two levels, up to 3,481 self-cooperators per language, with y and z added: 0 failures. The full prudence ladder passes (FairBot, PrudentBot, P*, P2, P12b, P*1b, PB2); P* needs K = 2.

**Fixed level cap: open.** A level-preserving sibling (K ≤ lmax) works for every class at 9/1, 10/1, 8/2 and 9/2 and first fails at 11/1, for 4 classes such as `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(ME))))))`. They are not truncation-closed candidates: the graph is one component at n = 11, so they reach suckerable classes by other paths.

**Static map, extended.** The new code reproduces the committed n ≤ 11 numbers exactly.
- n = 12: 13,514 classes, 6,286 self-cooperating, one component, 0 closed, maximum drift distance 1.
- n = 13: 27,189 classes, 12,310 self-cooperating, one component, 0 closed, maximum drift distance 1 (388 s on 3 threads, 2.7 GB).

**Leak ratio.** FairBot's leak/μ is the minimum at both sizes: 92.45 at n = 12 and 92.22 at n = 13, with `BOX1(THEM(ME))` 2·10⁻⁴ above it. Of every length shell from s = 5 to 13, 0.41–0.42 is a suckerable FairBot mate and 0.007–0.009 is FairBot's own class. Under the length prior each shell has mass 1/(2s²), so shell contributions fall like 1/s², with successive ratios 0.75 rising to 0.856, not geometrically. The extrapolated limit of leak/μ is about 89–90. A uniform bound is trivial under the length prior (leak/μ ≤ 27π² ≈ 266); the content is the limit value.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | Conjecture 4 holds, by a sibling with a provable-cooperation disjunct | **Conclusion held; mechanism failed.** The disjunct is an *undecidedness* test, and membership in the graph comes from mimicry, not from a cooperation test. |
| 2a | Lemma 1 and Corollary 1 transfer to bounded proof search | **Held** |
| 2b | the sibling transfers only under budget assumptions | **Held** (see transfer) |
| 3 | FairBot leak/μ-optimal in [85, 105]; shells decay geometrically (ratio < 0.7) | **Partly.** Optimal and in range; shell ratios 0.83–0.86, a 1/s² tail. |
| 4 | no drift-closed class at n = 12, 13 | **Held** |

**Transfer to bounded proof search over source** (`notes/conjecture4.md` §6). Drift-closure needs a reader that can tell a sibling from a copy. The theorem's mechanism is extensional: a reader that sees opponents only through finitely many behavioural probes always has a sibling it cannot distinguish, and that sibling can be exploited through the probe the reader never runs. So the transfer condition is: the sibling construction goes through for a bounded reader whose budget k exceeds its own self-check by poly(b_x) + O(|x| + log k), with the faker's budget B ≥ poly(b) by Pudlák's bounds. With tight budgets, a proof-length fingerprint (a soft clique) may allow closure. Both routes to closure, syntax (cliques) and proof length, are self-recognition or incumbency. With syntactic equality the conjecture is false: CliqueBot is drift-closed.

**Reading.**
- Exact closure is impossible in the free modal arm, so every cooperative network exits at Θ(1/N) at least and odds are capped near N^(1/2) unless a fringe or incumbency is added.
- The obstruction is extensionality, not GL.
- The guaranteed leak from the theorem is tiny (μ(x)·5^(−12)); the real leak is far larger (leak/μ ≥ 92). The quantitative theorem linking witness size and escape rate is the next object.
- Each order of prudence has a sibling one Con level up, so more prudence never escapes the regress.

## Almost all seeds? Persistence without mutation along N ≫ I and I ≫ N (`runs/almost-all-seeds.md`; spec `specs/2026-10-04-almost-all-seeds.md`, predictions in `predictions/2026-10-04-almost-all-seeds.md`)

Designed by the RE under the spec workflow, reviewed by gpt-6.1-sol, run by an Opus subagent. The RE reproduced three cells with fresh seeds after the merge: modal (100, 64) 6 of 6 efficient; modal (400, 4) 5 of 12; W0 (100, 256) 3 of 6. This re-opens the REJECTED entry "Seeding randomness as a substitute for mutation" (2026-09-30), whose evidence was the L6R arm, uniform-over-programs seeding, and I ≫ N at N = 100.

**Setup.** PD, w = 0.3. Arms: the modal arm (all box kinds), W0 (the weak arm without X and `ROLE`, matching the modal grammar and prior), and L6R (L_6 with X and `ROLE`), all at n = 6 for the islands.
- **Object 1:** the replicator from x₀ = prior on the full class matrix, under eight priors (length; per-program bases 2, 4, 8; tempered β = 0.5 and 2; uniform over programs; uniform over classes). Endpoints are *closed*: any class with positive growth rate at the pruned endpoint is re-injected at 10⁻⁶ and the run re-integrated until none grows; a fixed-step integration without pruning cross-checks.
- **Object 2:** ε = 0 islands, each slot seeded iid from μ (a new seeding; the existing 'prior' seeding puts every program in once and is not iid), complete island graph, mN = 1, horizon 10⁵ generations, 20 runs per cell and 40 at the end cells, Wilson intervals. Certification: all 897 runs with migration were outcome-frozen (every surviving class pairwise payoff-identical) by generation 20–490; none were metastable or unresolved. W0 at n = 8 could not be built (memory).

**Object 1: static.**
- *Modal arm.* The closed endpoint has P(C,C) = 1.000 at n = 6–9 under all eight priors: a prover family (FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`) at 0.2–0.28 each, with no class in the language growing. Every perturbation recovers (ALLC first, then all neutral classes, then random mixtures), and the result holds at tolerances ×10 and ÷10. ALLC goes extinct at t ≈ 15, D at t ≈ 56. The whole segment from μ to either uniform is efficient. Two caveats: at n = 8, 9 under three priors the *pruned* endpoint left `or(BOXD(THEM(ME)),BOX(THEM(^D)))` growing at 0.03–0.11 (it exploits probe-reading provers), and one closure round removed it; under tempered-2 at n = 8 the unpruned flow is still at all-D at t = 3,000 with the provers at 0.003 growing at 3.6·10⁻³.
- *Weak arms.* The closed endpoints are P(C,C) = 0.000 in W0 (n = 6, 7) and L6R (n = 6) under every prior: D plus `THEM(^D)` plus traces, persistent. W0 at n = 7 passes through P(C,C) 0.85–0.91 at t = 100 under two priors before collapsing.

**Object 2: modal arm.** Efficient fraction with 95% intervals:

| path | cells |
|---|---|
| N ≫ I (I = 4) | N = 100: 0.25 [0.14, 0.40]; 400: 0.45 [0.26, 0.66]; 1,600: 0.80 [0.58, 0.92]; 6,400: **1.00 [0.91, 1.00]** |
| I ≫ N (N = 100) | I = 4: 0.25; 16: 0.75 [0.53, 0.89]; 64: 1.00 [0.84, 1.00]; 256: **1.00 [0.91, 1.00]** |
| diagonal (N = 25·I) | (200, 8): 0.70; (400, 16): 1.00; (800, 32): 1.00 |

- Every non-efficient run froze in all-D. Median freeze time rises with I: 40 → 280 generations.
- *No-migration control:* islands alone end efficient 0.14 of the time at N = 400 and 0.07 at N = 100. Migration lifts (100, 64) from 0.07 per island to 1.00 per run.
- *The per-island chance scales like √N,* and the run-level outcome is 1 − (1 − p)^I: 0.07·√(N/100) gives 0.14 / 0.28 / 0.56 at N = 400 / 1,600 / 6,400, against measured per-island 0.14 / 0.33 / ≥ 0.6, and 1 − 0.93^4 = 0.25, 1 − 0.93^64 = 0.99 at I = 4, 64.
- *Spread is one-way.* One FairBot migrant fixes on an all-D island with probability 0.042 / 0.021 / 0.011 at N = 100 / 400 / 1,600 (exact slope −0.49, Monte Carlo −0.52). One D migrant fixes on an all-FairBot island at 1.7·10⁻⁸ (N = 100) and 2.5·10⁻²⁸ (N = 400). So the bad event is losing every prover everywhere, with probability about (per-island loss)^I, not a bad seed somewhere: I·P(no unfakeable cooperator in the seed) is 57 at I = 256, yet every run there ended efficient.
- *Mechanism.* ALLC is globally extinct by generation 40–60 (maximum 260) and never returns. 69 cooperative islands were lost after that, all to the probe-fakers `BOX(THEM(^D))` and `BOX1(THEM(^D))`, which exploit only the fakeable probe-reading provers; every such run still froze efficient.

**Object 2: weak arms.**

| arm | N ≫ I (N = 100 / 400 / 1,600 / 6,400) | I ≫ N (I = 4 / 16 / 64 / 256) | diagonal |
|---|---|---|---|
| W0 | 0.03 / 0.00 / 0.15 / 0.25 [0.14, 0.40] | 0.03 / 0.20 / 0.40 [0.22, 0.61] / 0.55 [0.40, 0.69] | 0.15 / 0.15 / 0.20 |
| L6R | 0.00 / 0.00 / 0.05 / 0.10 | 0.00 / 0.05 / 0.10 / 0.15 | 0.00 / 0.05 / 0.05 |

- Efficient frozen states are all-`THEM(^C)`; defecting ones are D, sometimes with `THEM(^D)`; L6R also freezes in `THEM(^ROLE)`/`THEM(^X)` mixtures (14 of 40 at I = 256). No-migration islands end efficient 0.00–0.01 of the time.
- *The faker race.* `THEM(^D)` takes an all-`THEM(^C)` island at 0.26 per migrant at every N and is neutral on D islands. `THEM(^C)` enters D islands at exactly FairBot's rate (identical 2×2 payoffs against D). At ε = 0 the fakers are a *finite stock* drifting on D islands; if every faker lineage is lost before it reaches a `THEM(^C)` island, the run freezes efficient. In W0 the fakers have R's prior mass (0.002); in L6R they have 3× it over 13 classes.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | modal static efficient and persistent at every n and prior; ALLC dies before D | **Holds** on closed endpoints; the falsifier fired on the pruned endpoint at n = 8, 9 under three priors and one closure round removed it; the thin-margin prior was tempered-2, not uniform |
| 2 | weak static goes to defection everywhere | **Holds** |
| 3 | modal basin efficient to t ≤ 0.75 | **Holds** (to t = 1) |
| 4 | modal N ≫ I: ≥ 0.5 at 400, ≥ 0.9 at 6,400; assay slope −½ | **Partly:** 0.45 at 400 fails, 1.00 at 6,400 holds, slope −0.49 holds; the RE addendum's 0.5–0.8 at (6,400, 4) was also low |
| 5 | modal I ≫ N rises, ≥ 0.6 at 256; freeze time grows | **Holds** (1.00; 40 → 280) |
| 6 | weak ≤ 0.15 everywhere, falling along I ≫ N, ≤ 0.05 at 6,400 | **Failed, falsifier fired:** W0 rises to 0.55 at I = 256 and is 0.25 at N = 6,400; L6R rises to 0.15 |
| 7 | modal rises on the diagonal; weak falls or stays ≤ 0.15 | modal and L6R **hold**; W0 **fails** (0.15 → 0.20) |
| RS | cooperation appears as islands grow along N ≫ I; no claim for few islands | **Holds** |
| S1–S3 | subagent's own | S1, S2 hold; S3 (no island lost after ALLC) fails: 69 lost, all fakeable classes |

**Reading.**
- In the faker-free modal language, iid seeding from μ at ε = 0 ends efficient with probability → 1 along both paths and the diagonal. The RS's N ≫ I condition is sufficient, not necessary: spread is one-way, so one surviving prover island suffices and more islands help.
- Fakeable languages are not doomed at ε = 0 either: without mutation the faker is a finite stock, and the race is often won before a faker reaches a reciprocator island. Unfakeability matters for the version with mutation (lim_N), where the faker exit is constant, not for the seed lottery.
- The static replicator from μ predicts the modal arm but not the weak arms (all-D statically against up to 0.55 efficient on islands). lim_t lim_N and lim_N lim_t differ, as sol warned; the proof object for the seed claim has to go through spread and extinction rates, not basin membership alone.
- The 2026-09-30 conclusion that the ε = 0 lottery concentrates on defection depended on the seeding law (uniform over programs, heavy in fakers) in L6R.

## The closed club: semantic self-recognition as an oracle benchmark (`runs/club.md`; spec `specs/2026-10-04-club.md`; predictions in `predictions/2026-10-04-club.md`)

Designed by the RE, reviewed by gpt-6.1-sol, run by an Opus subagent. The RS had objected to the club on normative grounds before the run; the result supports the objection on structural grounds too.

**The arm.** `CLUB(THEM)` (3 nodes) is a global semantic oracle over L_n: true iff the opponent is in K, where K is a fixed point of F(K) = {x : x self-cooperates under K and cooperates with nothing outside K}. This is an upper bound on semantic self-recognition, not a realizability result. Membership is solved over canonical functions of atoms; behavioural classes are formed afterwards.

**Fixed-point structure.**
- F is deflationary (F(K) ⊆ K), so iteration always descends to a fixed point and there are no cycles.
- **Every subset of the full-set limit is a fixed point**: 2, 32 and 512 of them at n = 6, 7, 8. Membership of a guarded program `and(CLUB(THEM), ψ)` is self-fulfilling: inside K it cooperates with itself, outside K it defects on itself. So "the club" is one choice out of 2^|K*|.
- F is not monotone at n = 8 (50 of 200 random nested pairs violate it, in both grammars), so the full-set start misses the maximal fixed point from n = 8 on; a guarded-set start with greedy ascent finds one maximal fixed point at each n (|K_max| = 1 / 5 / 13 / 17 canons at n = 6–9), with no incomparable fixed point found. Every member at every n is guarded.
- K is empty in the base language at n = 6–9.

**Composition at K_max.** 1 / 1 / 7 / 10 behavioural classes at n = 6 / 7 / 8 / 9, with μ(K) = 0.0047–0.0049, of which about 99% is `CLUB(THEM)`, "cooperate iff you are a member", the semantic CliqueBot, whose prior matches the m = 1 clique's within 1%. At n ≤ 7 K is one behavioural class. At n = 8 the within-K graph has three complete components, one of them {`CLUB(THEM)`, club-FairBot, `and(BOX1(THEM(THEM)),CLUB(THEM))`}; at n = 9 one component of 10 classes. For comparison the P* block has 46 classes (μ 0.0030) and FairBot's component 292 (μ 0.031).

**Drift-closure.** No program outside K is a neutral entrant into any club state. But from n = 8 on the members are suckerable by other members: 5 of 7 at n = 8, 7 of 10 at n = 9 (`CLUB(THEM)` is suckered by `and(CLUB(THEM),not(BOX(THEM(ME))))`). **K is closed as a set, not state by state: Corollary 1's leak returns inside the club as a ladder of member-fakers.**

**Collateral.** Unsuckerable self-cooperators excluded from K (FairBot, `BOX1(THEM(ME))`, PrudentBot, …) carry 2.0× K's mass at every n; suckerable excluded mass is 0.486; old-sense universality is exactly 0. No member drops out across cutoffs 6→9.

**ε→0 chain** (PD, w = 0.3, club at K_max, against the m = 1 clique and the free arm):

| n | N | club P(C,C) | clique P(C,C) | free | log(1 − π(K)) club / clique | hitting time all-D → K, club / clique |
|---|---|---|---|---|---|---|
| 6 | 10² | 0.9989 | 0.9990 | 0.169 | −6.6 / −6.7 | 4.1·10³ / 3.9·10³ |
| 6 | 10⁵ | 1.0000 | 1.0000 | 0.814 | −7498.3 / −7498.3 | 2.1·10⁵ / 2.1·10⁵ |
| 8 | 10² | 0.9988 | 0.9990 | 0.182 | −6.5 / −6.7 | 4.0·10³ / 3.8·10³ |
| 8 | 10⁵ | 1.0000 | 1.0000 | 0.814 | −7498.2 / −7498.1 | 2.3·10⁵ / 2.3·10⁵ |

- **The club is numerically a clique.** Exits out of K fall as e^(−wN/4) (d log rate/dN = −0.0750), a symmetric coordination against FairBot or `BOX1(THEM(ME))`; entry is identical to FairBot's to all digits (same 2×2 against D); hitting times match the clique's within 5%.
- **Where π sits is chosen by the fixed point.** At n = 8 on K_max, π lands on `and(CLUB(THEM),not(BOX1(THEM(THEM))))` (0.995 at N = 10³, 0.999 above), the unsuckerable end of the internal faker ladder, with prior mass 1.3·10⁻⁶; its only non-exponential exit is neutral, inside K, at μ/N. On the smaller fixed point K′ (the four `BOX`-guarded variants) all of K′ is one class and `CLUB(THEM)` holds π = 1. One terminal class and no polymorphic mass in every cell; residuals ≤ 3·10⁻¹⁵; the log-domain chain agrees on π(K) to 10⁻⁸; the free-arm control reproduces 0.8135 at n = 8, N = 10⁵.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | K empty in base language; club-FairBot in K; 3–30 classes, μ < 0.01 | **Held** (7 classes, μ 0.0048, 99% `CLUB(THEM)`) |
| 2 | drift-closed: no outside neutral entrant, no suckerable member | **Failed:** members are suckerable by members from n = 8 |
| 2b | unique maximal fixed point; empty set the only other; no cycles | **Failed in part:** unique maximum and no cycles held; 32 fixed points at n = 7; the full-set start misses the maximum at n ≥ 8 |
| 3 | exits deleterious below e^(−0.2N); slope steeper than −3; π(K) ≥ 0.99 | **Failed in part:** a neutral exit inside K; the exit out of K is e^(−0.075N); slope −29.8 and π(K) ≥ 0.998 held |
| 4 | entry equals FairBot's; hitting time within 2× of the clique's | **Held** (Δ = 0; ratio 0.98–1.05) |
| 5 | excluded unsuckerable mass ≥ 10× K's; universality 0 | **Failed on magnitude** (2.0×); universality 0 held |
| 6 | not a clique in disguise; K < 10% of classes | **Held statically** (a 3-member complete component; 2.3%), but K is one class at n ≤ 7 and π sits on a single-class block at n = 8 |
| 7 | ≤ 20% of members drop out per cutoff step | **Held** (none) |

**Reading.** Semantic membership closes the network as a set at exactly the clique's rate, and the club is about 99% the semantic CliqueBot. Membership is a free bit per guarded program, so the imposed fixed point is chosen, not derived, and the choice does hidden work twice: it picks one of 2^|K*| clubs, and it decides which member holds π. Corollary 1 is not evaded: universality is 0, and the leak reappears inside the club as member-fakers. Closure by declaration is a third route to self-recognition beside syntax and proof length, and it carries no more information than a tag. The open lever remains realizability: bounded, sound membership certificates with explicit proof costs.

## Bounded provers: a semantic legibility gate (`runs/bounded-provers.md`; spec `specs/2026-10-04-bounded-provers.md`, predictions in `predictions/2026-10-04-bounded-provers.md`)

Designed by the RE, reviewed by gpt-6.1-sol, run by an Opus subagent. Everything here is specific to this gate and to L_6 and L_8. The cost proxy is semantic stabilization (essential atoms × settle world), not measured proof length; this is not a bounded-Löb implementation. The RE re-checked FairBot's threshold and the b = ∞ reproduction at n = 6 after the merge.

**The gate.** x reading y pays v(x, y) = k(y)·(1 + settle(y, x)); constants cost 0; a box is true only if true in the free sense and v ≤ b. ε→0 chain, PD, w = 0.3, n = 6 and 8.

**Semantics: a design deviation.** The spec's synchronous joint fixed point never converges: it falls into a period-2 cycle at every finite b (mutual readers whose gates close and reopen together; at n = 8, b = 4 the two phases differ in 32,063 of 372,100 plays). The subagent redefined the gate on the bounded trace, world by world: at world n, x's boxes reading y are open iff k(y)·(1 + the last world before n at which y's atoms toward x changed) ≤ b. Cost only grows with n, so each gate closes at most once, box truth is monotone, the trace settles by world 7–11, and no fixed point has to be selected. Soundness holds on every pair (0 violations in 70,862 true open atoms at n = 8, b = 4); b = ∞ reproduces the free arm exactly. Masking is not monotone in b (share of box-reading pairs masked at n = 8: 0.75 / 0.86 / 0.67 / 0.52 / 0.22 / 0.05 at b = 1–8).

**Thresholds b\*.** FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))` and `BOX1(THEM(THEM))` all have b* = 1: FairBot's atom against a copy never changes, so its self-cost is 1·(1 + 0). PrudentBot has b* = 2, P* b* = 4. 99.45% of prover mass at n = 8 has b* = 1. Below threshold, FairBot-like provers still cooperate with ALLC (0.94 of that mass at b = 1); PrudentBot and P* below threshold defect on ALLC and on every named prover.

**Static map.** One component at every b (except n = 6, b = 3: two, neither closed). **0 drift-closed classes at every b**, at n = 6 and 8. Old-sense universality: FairBot 0.77–0.80 at every b.

**Siblings.** y = or(x, ψ_K) was built for every D-defecting self-cooperator whatever its size (16 at n = 6, 104–122 at n = 8). At every finite b ≤ 8, 0 siblings are legible to their original: sibling cost is 9–15 for FairBot (self-cost 1), 9–15 for PrudentBot (2), 16–24 for P* (4), ratio ≥ 2. At b = ∞ every sibling is legible, adjacent and suckered, reproducing the sibling theorem.

**Why nothing closes.** The leaks run through neighbours *cheaper* than the resident, which the gate never cuts: FairBot leaks through ALLC (cost 0); PrudentBot through `BOX(THEM(THEM))` (cost 1), suckered by `BOX1(THEM(^not(BOX(THEM(ME)))))`; P* through 33 suckerable mates (μ 3.1·10⁻³) led by `not(BOX(THEM(ME)))` (cost ≤ 2), suckered by D. So a reader whose legibility is monotone in opponent cost cannot be drift-closed in these languages.

**Chain, n = 8, N = 10⁵.** P(C,C) = 0.847 / 0.848 / 0.822 / 0.823 / 0.8135 at b = 1 / 2 / 3 / 4 / {6, 8, ∞}. Everywhere the top exit is neutral into ALLC with fitted exit slope −1.00 over N = 10³–10⁵ and odds slope 0.43–0.48; rival share 0 at b ≤ 3 (P* does not self-cooperate) and 0.122 at b = 4 against 0.125 free; one terminal class, no indeterminate transitions, cut flow ≤ 10⁻⁶. The arm under mutation is the free arm with the P* block thinned.

**Controls.** The atom-count gate is trivial (k ≤ 2) except at n = 8, b = 1 (0.802, slope −1). The **random gate** at matched masking count locks in P* at n = 8, b ∈ {1, 3, 4} (P(C,C) 0.9998 / 0.994 / 0.984) with exits of 6–8·10⁻¹¹ but still slope −1.00: a leak cut by about 10⁵ in mass, not a closure, achieved by randomly cutting P*'s cheap mates, which is a tag. At n = 6, b = 1 the random gate creates strict fakers (0.36). The clique arm is 1.000 from N = 10³.

**Per-program budgets.** Fixed support: prover π by b = 1–4 is 0.235 / 0.223 / 0.189 / 0.184 at n = 8, N = 10⁵, a weak tilt to small budgets. Length-penalized: b = 1 holds the mass by prior and P(C,C) falls to 0.613 because the penalty shrinks the provers' prior; the penalty removes PrudentBot and P* at n = 8 at every b.

**ε = 0 lottery** (n = 6, iid from μ, paired seeds, 20–40 runs). Free arm under this seeding: 0.20 / 0.55 / 0.82 at I = 4, N = 100 / 400 / 1,600; 1.00 at I ≥ 64. Paired differences against b = ∞: **0.00 at every cell for b ≥ 4**; within ±0.07 at b = 1–3 (two cells unresolved at 40 runs); every I ≥ 64 cell is 1.00 at every b. The random gate at b = 1 lowers it by 0.20–0.40 at I = 4. Runs that end defecting are, almost exactly, the runs whose cooperative core is gone when ALLC goes extinct at generation 40–60; loss happens in the scramble at the same rate at every b. Caveat: n = 6 has no prudent provers and b = 4 changes only 21 canonical plays.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | FairBot b* = 2, PrudentBot 4, P* 4; selective cooperation below threshold | **Failed, falsifier fired:** 1, 2, 4. Selective cooperation holds for FairBot-like mass only |
| 2 | first drift-closed classes at b = 4 | **Failed, falsifier fired:** none at any b; the sibling-exclusion clause held |
| 3 | FairBot leaks neutrally at 1/N, odds ∝ N^½ | **Held** (−1.00; 0.43–0.48) |
| 4 | π at b = 4 goes to a closed prudent family, slope < −1.5 | **Failed, falsifier fired:** slope −1.00, rival 0.10; "b ≥ 8 within 0.05 of free" held; no control beat slope −1 |
| 5 | fixed support puts π on the smallest closed b | **Mechanism failed** (nothing closed); the tilt to small b is weak |
| 6 | lottery unaffected at b ≥ 4, weakened at b = 2, zero at b = 1 | **Partly:** b ≥ 4 held exactly; b = 2 not lower; b = 1 not zero |
| 7 | budget decides closure under mutation, not seeding | **First half failed;** second half held (no core fragmentation) |
| S1–S3 | subagent's own | S1 held; S2 failed (the joint iteration cycles); S3 second clause failed |

**Reading.**
- Budget-limited legibility is *harmless* in this proxy: the free modal results (1/N leak, odds ∝ N^½, the seeding lottery) survive at every b at n ≤ 8, and the gate creates no fakers. The operating hypothesis "sound bounded prover" is not undermined at this level.
- Proof length is not a moat here. The gate prices out every sibling (ratio ≥ 2) and still closes nothing, because every unsuckerable class leaks through a neighbour cheaper than itself.
- What does close, the random gate, works as a tag: closure keeps coming from self-recognition.
- The cost proxy does not charge the Löb step (a stable self-proof has settle world 0), so budgets 1–4 barely bind on occupied states. The next instrument needs an explicit proof system with measured length, to see whether `not(BOX(THEM(ME)))`-type neighbours are cheap to prove about there as well.

## Almost all seeds: cutoff sensitivity in n (`runs/seeds-in-n.md`; spec `specs/2026-10-05-seeds-in-n.md`, predictions in `predictions/2026-10-05-seeds-in-n.md`)

Designed by the RE, reviewed by gpt-6.1-sol, run by an Opus subagent. A local test at n = 6–9; it does not establish uniformity in n. 1,920 runs, no administrative censoring, one dynamically unresolved run. The RE spot-checked with fresh seeds after the merge: per-island 13/120 at n = 9 and 16/120 at n = 6 (no migration, N = 100), 8/8 efficient at (100, 64), n = 9.

**Setup.** Modal arm, PD, w = 0.3, ε = 0, iid seeding from the length prior at cutoff n ∈ {6, 7, 8, 9}; complete island graph, mN = 1; budget 10⁵ generations; unpaired Wilson 95% intervals.

**Static masses** (μ): ALLC 0.466–0.469; D the same; self-cooperators 0.0284 → 0.0313; unfakeable core 0.0149 → 0.0102 (flat from n = 7); FairBot 0.0051 at every n; fakeable self-cooperators 0.0135 → 0.0210; **D-entering self-cooperators 0.0229 → 0.0246**. The core's one-step drop at n = 7 is `BOX(THEM(THEM))` becoming fakeable by fakers of mass ~10⁻⁵, which an island almost never seeds. Every self-cooperator that defects on D enters an all-D island of 100 at the same ρ = 0.0421.

**Per-island chance p(N, n)** (no migration, 400 islands per cell):

| N | n = 6 | 7 | 8 | 9 |
|---|---|---|---|---|
| 100 | 0.083 [0.059, 0.114] | 0.090 | 0.092 | 0.090 [0.066, 0.122] |
| 400 | 0.158 | 0.198 | 0.195 | 0.185 |
| 1,600 | 0.383 | 0.427 | 0.427 | 0.412 [0.365, 0.461] |

- p is flat in n; the slope of log p on log N is 0.55 at every n.
- The predictor a·μ_core·√N (fitted at n = 6) misses by +57% to +89% at n = 7–9, in all 9 cells. The predictor a·μ_est·√N, with μ_est the mass of D-entering self-cooperators, fits within −9% to +12% at n = 7–9 when fitted on n = 6's three N. **p tracks the D-entering self-cooperators, fakeable or not, not the unfakeable core.**

**Run-level efficient fraction** (mN = 1): (100, 4): 0.35 / 0.25 / 0.25 / 0.20 at n = 6–9; (400, 4): 0.35 / 0.40 / 0.55 / 0.40; (1,600, 4): 0.78 / 0.85 / 0.85 / 0.80; (400, 16): 0.90 / 0.90 / 1.00 / 0.95; (100, 64): 20/20 at every n; (100, 256): 40/40 at every n. Every non-efficient run froze in all-D; every run with migration was certified. 1 − (1 − p)^I fits at I ≥ 16 but overpredicts at (400, 4) (0.56 against 0.42 [0.32, 0.53]): at I = 4 with mN = 1, migration partly merges the islands during nucleation.

**Seed conditioning.** At (100, 4) the efficient fraction rises with the number of islands seeded with a core program: 0/1, 3/13, 4/20, 14/46 for 0 / 1 / 2 / 3–4 islands. At N = 100, 54 of 59 defecting I = 4 runs had no self-cooperator left when the last ALLC died (loss in the scramble). At N = 1,600, none of the 29 defecting runs had lost them all: they still held a median of 26 core programs at ALLC extinction (efficient runs: 77). At large N the failure is a failure to nucleate from a minority after ALLC is gone.

**Nucleation-then-spread control** ((100, 64), migration off until generation 2,000): at the switch 5.4 (n = 6) and 5.7 (n = 9) of 64 islands were certified cooperative, a per-island rate of 0.084 / 0.089 equal to the no-migration p, with at least 2 in every run; after the switch 80 of 80 runs froze efficient. Establishment is independent per island at rate p, and one established island suffices at I = 64.

**Losses** (island ≥ 90% → < 50% self-cooperators; 160 runs per n). Before / after global ALLC extinction: 2/25, 5/173, 4/113, 4/75 at n = 6–9, all at I ≥ 16, heavy-tailed. After ALLC, 0.88 (n = 6) and 0.97–0.99 (n = 7–9) of losses are fakeable-held islands taken by probe-fakers (`BOX(THEM(^D))`, `BOX1(THEM(^D))`, and at larger n new ones such as `BOX1(THEM(^BOXD1(THEM(^C))))`, 20 islands at n = 9). Mechanisms reconstructed from the payoff table: 33 strict invasions of monomorphic islands across n, **all of fakeable-held islands**; 1 neutral replacement; the rest displacements from mixed islands. **Core-held losses: 13, none a strict invasion**, 11 by a probe-faker that grew on a fakeable co-resident, 1 by ALLC before its global extinction, 1 by D against selection (17 D migrants in 20 generations into a still mostly-D archipelago, verified by birth-level replay). Every run with losses froze efficient.

**Frozen efficient states.** FairBot + `BOX1(THEM(ME))` hold 0.41–0.49 of islands; fakeable self-cooperators 0.33 / 0.54 / 0.59 / 0.51; `BOX(THEM(THEM))` + `BOX1(THEM(THEM))` 0.39–0.48. The four D-entering provers split the islands about evenly, each near its predicted μ·ρ share of ≈ 0.21; total-variation distance to normalized μ·ρ(D) is 0.03–0.08 at every n. **Composition is prior mass × establishment; fakeability plays no part.**

**ALLC extinction** (island level): medians 13–14 at N = 100, 19–20 at 400, 24–25 at 1,600, with n = 9 / n = 6 ratios 1.00–1.03 in every cell; the global time grows with I as an extreme statistic (20 / 35–41 / 48–63 at I = 4 / 64 / 256).

**Unresolved:** 1 of 1,920 (n = 9, (400, 4), no migration): an island at a stable anti-coordination rest point between `not(BOXD(THEM(THEM)))` and `BOX1(THEM(^BOX1(THEM(^D))))`, each defecting on its own class and cooperating with the other, P(C,C) ≈ 0.5. Not a cycle.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | one step down at n = 7, then flat | **The step failed** (no step; μ_core misses everywhere at n ≥ 7); "no further fall" held; falsifier not fired |
| 2 | fractions ≈ 1 − (1 − p)^I | **Inconclusive at I = 4**, held at I ≥ 64; fails as a law at (400, 4) |
| 3 | post-ALLC losses are fakeable provers; no strict invasion of the core | **Held** (0 strict invasions of core in 13 core losses; ≥ 0.9 share at n ≥ 7) |
| 4 | FairBot + `BOX1(THEM(ME))` hold ≥ 0.6; fakeable share falls with n | **Failed, falsifier fired** (0.41–0.49; fakeable share 0.51 at n = 9 and rising); μ × establishment holds (TV ≤ 0.08) |
| 5 | island-level extinction n-independent, median 15–60 | n-independence **held**; the range failed at N = 100 (13–14) |
| S1–S4 | subagent's own | S1, S2 held; S3 failed narrowly; S4 failed (losses vary 3× across n) |

**Reading.**
- Over n = 6–9 the per-island chance is flat in the cutoff (0.083–0.092 at N = 100, ∝ N^0.55), so the extra fakeable provers at larger n cost nothing.
- The lottery runs on the mass of *D-entering self-cooperators*, not on unfakeability: a fakeable prover counts fully unless its faker is seeded nearby. Unfakeability belongs to the mutation object (where fakers are re-supplied), not to the seeding object.
- Establishment and spread decompose cleanly: islands establish independently at p, one established island spreads to all, and the bad event is that no island establishes.
- The sound core was never strictly invaded in 1,920 runs; its only loss route is displacement from a mixed island where a probe-faker feeds on a fakeable neighbour.
- Uniformity beyond n = 9 needs a tail bound on μ_est(n), which should be monotone if D-entering self-cooperators only accumulate, plus a bound on probe-faker mass (0.0030 → 0.0036 here).

## Almost all seeds: the tail in n (static, n ≤ 12) and island merging at I = 4 (`runs/seeds-tail.md`; spec `specs/2026-10-05-seeds-tail.md`, predictions in `predictions/2026-10-05-seeds-tail.md`)

Designed by the RE, reviewed by gpt-6.1-sol, run by an Opus subagent. Nothing censored, nothing unresolved. One correction fixed in the predictions before computing: the infinite length prior totals Σ 1/(2s²) = π²/12 ≈ 0.822, not 1, so masses are given raw (unnormalized), in *inf* units (raw/(π²/12)) and in *cut* units (raw/retained(n)); the published μ_est values are cut units.

**Part A: the tail.** The modal language evaluated once at n = 12 (22,690 canonical functions, 51 s); smaller cutoffs are sub-blocks (canonical ids form a prefix; the n = 9 sub-block reproduces `modal.build(9)` to 10⁻¹⁵). *Establisher:* self-cooperates and defects on D. *Probe-faker:* strictly invades some establisher's monomorphic world.

| n | classes | establishers / fakers / core | μ_est cut | μ_core cut | μ_pf cut (union) | r = μ_pf/μ_est | P(K_pf > 0 \| A) |
|---|---|---|---|---|---|---|---|
| 6 | 51 | 9 / 37 / 3 | 0.0229 | 0.0149 | 0.053 | 2.30 | 0.189 |
| 8 | 471 | 96 / 381 / 9 | 0.0242 | 0.0102 | 0.060 | 2.46 | 0.233 |
| 10 | 1,752 | 319 / 1,524 / 15 | 0.0249 | 0.0104 | 0.062 | 2.49 | 0.260 |
| 12 | 13,514 | 2,505 / 12,245 / 85 | 0.0253 | 0.0104 | 0.064 | 2.53 | 0.274 |

- **A rigorous lower bound, uniform in n.** Establisher status switched 0 times at every step (it depends only on self-play and play against D), so raw μ_est only accumulates, and **μ_est(cut) ≥ raw(6)/(π²/12) = 0.0207 at every cutoff**. The omitted mass ω(n) is 0.077 at n = 6 and 0.040 at n = 12, giving 0.0240 ≤ μ_est(∞) ≤ 0.0726 in inf units rigorously; the 1/s²-tail extrapolation gives μ_est(∞) ≈ 0.027.
- **Shells.** The shell fraction f_est(s) is 0.061–0.091 at s = 6–12 (odd shells heavier, from the grammar's parity); two-step ratios 0.58 / 0.65 / 0.69 against (s/(s+2))² = 0.56 / 0.64 / 0.69: a 1/s² tail, not geometric.
- **Global faker mass is the wrong spoiler measure.** The union is 2.5× μ_est and is dominated by the fakers of two near-universal suckers, `not(BOXD(THEM(^C)))` and `not(BOXD1(THEM(^C)))` (μ 0.0003 each), which count FairBot among their fakers. The resident-conditioned exposure, from 10⁵ seeds of N = 100 conditioned on containing an establisher (P(A) ≈ 0.91): P(K_pf > 0 | A) = 0.19 → 0.27 at n = 6–12 with shrinking increments (0.022 → 0.007); E[K_pf | A] = 0.32 → 0.61, a quarter of it establishers faking the two suckers, which leaves a cooperative island. The μ-weighted exposure is 0.0015 → 0.0026.
- The 8 establishers with raw mass ≥ 10⁻⁴ carry 97% of μ_est; all have the same ρ(x | all-D) (0.0421 / 0.0214 / 0.0108 at N = 100 / 400 / 1,600), so Σ μρ = ρ·μ_est exactly. **FairBot and `BOX1(THEM(ME))` have no strict invader at any n ≤ 12.** The core lost `BOX(THEM(THEM))` to reclassification at n = 7 (0.0037 raw) and ≤ 2.5·10⁻⁵ per step after.

**Part B: merging at I = 4** (n = 6, four islands of N = 400, horizon 10⁵, 60 runs per mN, all certified). References rerun: no-migration per-island p(400) = 0.190 [0.155, 0.231]; one island of 1,600: 0.371 [0.312, 0.434] (240 runs). Run-level efficient fraction: **0.617 [0.49, 0.73] at mN = 0.1; 0.517 at mN = 1; 0.433 at mN = 10**, every run ending all-efficient or all-D. Predeclared contrast (mN = 0.1 − mN = 10): 0.183, 95% interval [0.005, 0.346]. Monotone, no intermediate maximum. Event logs: before the first certified island, D migrants per run are 24 / 280 / 2,206 at mN = 0.1 / 1 / 10 and establisher migrants 3 / 58 / 668; islands ≥ 90% cooperative by generation 200 in efficient runs are mostly one (mN = 0.1, matching independent trials) or all four (mN = 10); spread time from first to last cooperative island 940 / 120 / 20 generations. **0 cooperative islands lost in 180 migration runs; no probe-faker ever migrated into a cooperative island.** Migration hurts only by diluting the nucleating minority with D migrants, which merges the islands during nucleation and moves the run-level chance toward p(IN).

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | μ_est(12) ∈ [0.024, 0.028], 1/s² tail, shell fraction within ±50% of f(6) | **Held in substance** (0.0253; 1/s²; within ±50% at s = 6–12); the 0.03–0.06 band failed narrowly (0.061–0.091); "limit below 0.03" consistent but not rigorous |
| 2 | μ_pf(12) ≤ 0.006, r ≤ 0.25, E[K_pf \| A] < 0.5, P(K_pf > 0 \| A) < 0.35 | **Failed, falsifier fired** on the global union (0.064; r = 2.5) and E[K] from n = 9; P(K > 0 \| A) < 0.35 **held** |
| 3 | FairBot and `BOX1(THEM(ME))` unfakeable to n = 12 | **Held** |
| 4 | merging: 0.50 / 0.42 / 0.38 ± bands, contrast > 0 | **Contrast held** (0.18 [0.005, 0.35]); bands inconclusive (point estimates inside, intervals straddling) |
| S1–S5 | subagent's own | S1 failed (global union), S2, S3, S5 held, S4 mixed |

**Reading.**
- The establishment term of the seed lottery is rigorously positive uniformly in the cutoff, by construction rather than extrapolation: establisher status cannot be lost by adding opponents.
- The spoiler term must be resident-conditioned. The global faker union is meaningless here; the conditioned chance that an establishing seed also carries one of its own fakers is 0.27 at n = 12 and flattening. This is now the sole open ingredient for "almost all seeds" in this language family.
- Migration between islands costs only through merging during nucleation, never through spoilers. The I ≫ N path keeps islands as independent trials only when migrants per island during nucleation are small relative to N (mN·T_nuc ≈ 6 / 60 / 600 against N = 400 gave independent / partly merged / merged).

## Spoiler-conditioned establishment: does a co-seeded faker stop establishment? (`runs/spoiler-conditioned.md`; spec `specs/2026-10-05-spoiler-conditioned.md`, predictions in `predictions/2026-10-05-spoiler-conditioned.md`)

Designed by the RE, reviewed by gpt-6.1-sol, run by an Opus subagent. Finite-cell evidence at n ∈ {6, 9, 12}, N ∈ {100, 400}: single islands, no migration, horizon 10⁵, modal arm, w = 0.3, iid seeds from μ. 24,000 natural islands and 42,000 forced backgrounds; 0 natural and 7 forced islands unresolved; nothing administratively censored. Declared deviations: a replacement-by-D control (cD) added beside the spec's (c), which changes target dosage; thresholds judged on relative reductions; one supplementary pair with an establisher-faker; §6 of the run file is post hoc.

**Payoff tables.** A faker's play against D is one of three types: *disadvantaged* (it cooperates with D), *neutral* (it defects on D and on itself), *advantaged* (it is itself an establisher). Faker mass of the 8 heavy targets: disadvantaged 0.025–0.028, neutral 0.003–0.005, advantaged 0.023–0.025 at n = 6–12. The six heaviest (target, faker) pairs are the same at every n: `BOX1(THEM(THEM))` ← `not(BOX(THEM(ME)))` / `not(BOX(THEM(THEM)))` (disadvantaged) and the probe-readers `BOX(THEM(^C))` / `BOX1(THEM(^C))` ← `BOX(THEM(^D))` / `BOX1(THEM(^D))` (neutral). **No faker of any main prover ties D on both D and ALLC** to n = 12: every faker of FairBot's family or of the probe-readers either cooperates with D or cooperates with ALLC, so it is strictly worse than D while ALLC is present. For the probe-readers this is structural: passing the probe `THEM(^C)` means cooperating with ALLC. Fakers that tie D on {D, ALLC} exist only for the two near-universal suckers, at mass 0 / 3.5·10⁻⁴ / 5.2·10⁻⁴ at n = 6 / 9 / 12.

**Natural seeds, four disjoint cells** (given an establisher present: (i) no faker of it, (ii) non-establisher fakers only, (iii) establisher-fakers only, (iv) both; cooperative fixation, which coincides with efficiency; bootstrap ratio intervals):

| n, N | islands (i / ii / iii / iv) | coop (i) | coop (ii) | d = (ii)/(i) |
|---|---|---|---|---|
| 6, 100 | 2,933 / 590 / 16 / 83 | 0.093 | 0.115 | 1.24 [0.96, 1.57] |
| 9, 100 | 2,755 / 704 / 27 / 183 | 0.099 | 0.108 | 1.09 [0.84, 1.37] |
| 12, 100 | 2,604 / 831 / 26 / 220 | 0.095 | 0.108 | 1.14 [0.90, 1.41] |
| 6, 400 | 840 / 2,685 / 0 / 475 | 0.173 | 0.190 | 1.10 [0.94, 1.31] |
| 9, 400 | 574 / 2,559 / 1 / 866 | 0.166 | 0.196 | 1.18 [0.98, 1.47] |
| 12, 400 | 421 / 2,573 / 1 / 1,005 | 0.164 | 0.183 | 1.12 [0.90, 1.42] |

The raw target-survival ratio across cells (0.33–0.56) is confounded by target identity (cell (i) holds FairBot, cell (ii) the weaker faked provers); matched on target it is 0.7–1.6. In cell (ii) the faker is extinct by the island's ALLC extinction in 0.88–0.99 of islands, and cooperative islands there are mostly won by unfaked establishers.

**Forced seeds** (1,000 paired backgrounds per pair, N and dose k; relative reduction of target survival from inserting the faker beside its target). k = 1: disadvantaged −0.13 to 0.21, neutral −0.32 to 0.35, every interval including 0 except one cell; k = 10 at N = 400: neutral 0.25–0.41, flat in n, disadvantaged −0.01 to 0.15. Replacement by D alone, (a) − (cD), is within ±0.004. A faker alone (d) at N = 400 is in the terminal support in 3.3–4.9% of islands (neutral, frozen with D) and 0% (disadvantaged); no disadvantaged faker won any (b) island. Supplement: FairBot inserted as the faker of a sucker *raises* cooperative fixation by 4–52%.

**Frequency logs.** Given the target is alive at the island's ALLC extinction, it survives with probability 0.42–0.58 if the faker is already dead and 0.07–0.29 if it is still alive. The faker rarely gets that far: per co-seeded copy, its chance of surviving the scramble is 0.014–0.06 (disadvantaged), 0.05–0.09 (neutral), 0.06–0.12 (advantaged). The two-factor prediction (fraction alive at ALLC extinction × post-scramble harm) gives 0.28 against 0.34 measured at k = 10 (neutral) and 0.38 against 0.40 (advantaged).

**Held-out decomposition** (fit on islands 0–1,999, test on 2,000–3,999): errors −11.6% / +2.1% / +2.7% at N = 100 and −0.5% / −0.5% / −2.4% at N = 400. Close to an identity in expectation, as sol said.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | co-seeded non-establisher fakers rarely stop establishment; pooled d ≥ 0.7 | **Held** (d 1.09–1.24, lower bounds 0.84–0.98); "neutral fakers worse" seen only at k = 10 |
| 2 | pair-level effect flat in n | **Inconclusive** at k = 1 (intervals ±0.4–0.6); flat within 0.1 at k = 10 |
| 3 | establisher-fakers leave a cooperative island | **Inconclusive** (cell (iii) has ≤ 27 islands); every cooperative (iii) island was won by an establisher; cell (iv) and the supplement support it |
| 4 | forced-seed mechanism | **Held except the log clause:** the faker's share does not "fall after ALLC extinction" because it is already dead then (90–99%); as "dead or falling while the target rises" it holds in 74–89% |
| 5 | held-out decomposition within 15% | **Held** |
| S1–S6 | subagent's own | S1 failed (single-dose neutral fakers are not strongly harmful); S4 neutral part failed; S2 narrowly; S3 partly; S5, S6 held |

**Reading.**
- **Co-seeded fakers of the main provers do not stop establishment.** They are strictly worse than D while ALLC is present, because they either feed D by cooperating with it or fail to eat ALLC. So they die in the scramble, before their post-scramble advantage over the target can act.
- **The harm is a product of two factors:** the faker's chance of surviving the scramble (0.01–0.1 per copy) and its post-scramble harm (about half the target's survival). With exposure E[K_pf | A] ≈ 0.3–0.6, that is a bounded discount, and in natural seeds it is hidden by rescue from other establishers.
- **The spoiler that would matter is a faker payoff-identical to D on {D, ALLC}.** None exists for any main prover to n = 12, and for the probe-readers none can by construction. The open part of "almost all seeds" narrows to bounding the mass of such fakers in n (≤ 5·10⁻⁴ here, for the suckers only).
- **The lemma, in the form the logs support:** P(target survives | faker co-seeded) ≈ P(target survives)·[1 − q·h], with h ≤ 0.9 measured, and q bounded by the faker's integrated payoff deficit against D over the scramble, which ∫x_ALLC dt makes strictly positive for any faker that does not tie D on {D, ALLC}. That is a bound on integrated selection, not on instantaneous advantage, as sol framed it.

## The scramble lemma and Claim A (`runs/scramble-lemma.md`, `notes/scramble-lemma.md`; spec `specs/2026-10-05-scramble-lemma.md`, predictions in `predictions/2026-10-05-scramble-lemma.md`)

Designed by the RE, reviewed by gpt-6.1-sol, run by an Opus subagent. Claim A is proved and exhaustively checked; Claim B is proved in its stated form but turns out to carry little content, and the result *corrects* the reading of RESULTS "Spoiler-conditioned establishment": fakers die in the scramble mostly by demographic extinction, not by selection.

**Lemma 0 (box soundness at the stable world).** `_evaluate` runs one chain of worlds shared by every ordered pair and stops at a global fixed point (the first n* ≥ 2 at which no entry changes), so values at n* repeat at every later world, and any box atom true at n* at any level L ≤ n* covers world n*: the boxed pair really plays the boxed action. The nested call `THEM(THEM)` reads the pair (q, q) at the same world, so there is no level/world mismatch. *Ledger:* shared chain, box quantifies over L ≤ m < n, global fixed-point stop. No Löb, no fixed-point uniqueness, every level.

**Claim A, proved member by member** (every level and cutoff, no Löb): FairBot and `BOX1(THEM(ME))` have no fakers at all (if x cooperates with q, Lemma 0 gives that q cooperates with x; Löb is needed only for x to self-cooperate, not for unfakeability); every faker of `BOX(THEM(^C))` / `BOX1(THEM(^C))` cooperates with ALLC (the probe is the population's ALLC class); every faker of `BOX(THEM(THEM))` / `BOX1(THEM(THEM))` self-cooperates, so it is an establisher or cooperates with D. The case is not vacuous: `not(BOX(THEM(ME)))` is a D-cooperating faker of `BOX1(THEM(THEM))`. Exhaustive at n = 6, 9, 12: 0 counterexamples (at n = 12: 374 / 643 / 1,846 / 1,712 non-establisher fakers of the four fakeable members, every one cooperating with D or ALLC or both; 92–118 establisher-fakers each, mass ≈ 2·10⁻⁵); the independent evaluator agrees on all 24,981 (x, q) pairs. The spec's example establisher-faker `and(BOX(THEM(THEM)),not(BOX(THEM(^C))))` was wrong: it defects on itself (its self-play fixed point is ⊥). Working examples: `BOX1(THEM(^not(BOX(THEM(ME)))))` fakes `BOX(THEM(THEM))`.

**The kernel** is a birth–death Moran process (parent by fitness, victim uniform), not death–birth as the spec said; for a class with k copies the expected change per event is exactly (k/N)(f_q/F̄ − 1), with no rarity assumption.

**Claim B.** (B1, exact) k_t·e^{Λ_t} is a martingale with Λ_t = −Σ log(1 + r/N), r = f_q/F̄ − 1; optional stopping at τ = ALLC extinction ∧ freeze ∧ 2,000 generations gives P(q alive at τ | E) ≤ P(Λ_τ < Λ | E) + E[k₀ | E]·e^{−Λ} for any Λ, handling the stopping-time correlation exactly. (B2) Λ_τ ≥ w∫[0.659·(π̄ − π_q)⁺ − 1.615·(π_q − π̄)⁺] dt at w = 0.3. (B3, exact in {D, ALLC, q} with q rare) π̄ − π_q is x_A·x_q for a probe-faker (**mean-neutral to first order**), x_D² − x_A² for a D-cooperator (above the mean while ALLC outnumbers D), x_D(x_D + x_A) for one that cooperates with both. (B4) The seed event E = {x_A(0), x_D(0) ≥ 0.3} fails with probability ≤ 2e^{−0.042N} uniformly in n; the distribution of Λ_τ is measured, not proved. The instrumented kernel reproduces the spoiler run draw for draw (124/124), and the martingale identity holds (E[k_τe^Λ]/E[k₀] = 0.96–1.07 in 14 of 15 cells).

**Neutral-lineage ("ghost") control.** The inserted faker is replaced by a ghost that plays as the faker but has its fitness pinned to the population mean, on the same seeds and stopping rule (3,000 backgrounds per pair), at k = 1 in E:

| N | faker type | faker alive at τ | ghost alive at τ | ghost/faker | selection share of log deficit | B1 bound (× measured) | median τ |
|---|---|---|---|---|---|---|---|
| 100 | D-cooperator | 0.038 | 0.082 | 2.1 | 0.23 | 10.7× | 13.4 |
| 100 | probe-faker | 0.071 | 0.072 | 1.02 | 0.01 | vacuous | 13.6 |
| 400 | D-cooperator | 0.0077 | 0.052 | 6.8 | 0.39 | 20× | 19.0 |
| 400 | probe-faker | 0.046 | 0.048 | 1.05 | 0.02 | vacuous | 19.1 |

The ghost survives like a critical lineage, P(alive) ≈ E[1/(1 + τ)]; establisher-fakers behave like ghosts; everything is flat in n. Along the scrambles at N = 400, D holds about 86% of the time and the probe-faker's loss to D (+1.7) and gain over ALLC (−1.6) cancel, as B3 says.

**Combined per-island bound.** The exact identity P(target survives) = ρ̃ − P(A∩F)·h (A: target alive at τ; F: some co-seeded faker alive at τ; h the conditional harm) with the union step P(A∩F) ≤ Σ_q E[K_q | E]·q̄_q gives P ≥ ρ̃ − Σ_q E[K_q|E]·q̄_q·h_q⁺, which is **non-positive in 16 of 18 cells with B1's q̄**: the union step loses a factor 1/P(A) ≈ 7–20 because the target itself survives the scramble in only 5–14% of islands. Proved: the identity, the union bound, B1–B3, Claim A, P(Eᶜ). Measured: Λ's distribution, h, P(A). Assumed: ρ̃ ≈ the faker-free establishment chance.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | Claim A for all six members | **Held** |
| 2 | first-moment bound within 10×; selection ≥ half the deficit | **Failed, falsifier fired:** vacuous for probe-fakers (ghost/faker 1.02–1.05); 10.7× / 20× loose for D-cooperators; selection share 0.23 / 0.39 |
| 3 | combined bound positive and uniform in n | **Failed on positivity, held on uniformity** |

**Reading.**
- **Unfakeability needs only soundness, not Löb.** Löb buys self-cooperation; soundness buys unfakeability; the two are independent. Lemma 0 is the one fact behind the whole FairBot family's unfakeability at every level.
- **A co-seeded faker of a probe-reader is a neutral lineage, not a disadvantaged one.** The scramble kills it by demography, with per-copy survival ≈ 1/(1 + τ_A), and τ_A grows like log N (13 → 19 over N = 100–400); selection adds a factor of 2–7 only for D-cooperating fakers.
- So for fakeable establishers the expected spoiler term N·μ_q·q̄_q·h_q grows like N/log N unless the post-scramble harm h falls (it fell from 0.44 to ≈ 0.2 between N = 100 and 400). **"Almost all seeds" is clean only for the fakerless establishers, FairBot and `BOX1(THEM(ME))`** (μ_core ≈ 0.0102), whose per-island chance needs no spoiler term at all; the fakeable provers are a bonus measured to n = 12 and N = 400.

## Proof-carrying contracts v1 (`runs/proof-carrying-contracts.md`; spec `specs/2026-10-04-proof-carrying-contracts.md`, predictions in `predictions/2026-10-04-proof-carrying-contracts.md`)

Designed by the RE from the RS's pitch, reviewed by gpt-6.1-sol, run by an Opus subagent. Finite-size mechanism results; swapping is a second operator outside the ε→0 chain. The all-D-start cells (144 runs) were not run, by the RE's decision after the gate proved inert at b = 2; they are recorded as not run, not censored. A b = 0 supplement was preregistered in a predictions addendum before any b = 0 run.

**Semantics.** Reading contracts as bare truth tables is paradoxical: iterating the all-carrier table from the GL play cycles with period 4 and 58,996 of 372,100 entries never settle (negated mutual reference: FairBot's entry against `BOXD(THEM(ME))` must equal its own negation). So contracts are read through provability: the alphabet C is the 471 behavioural classes of the free n = 8 game (19,544 programs, 610 canonical sources), each represented by its shortest source, and a contract read is the ungated free-GL stable box over the representatives; a 'none' entry is read from source through the gate. 14 policy-duplicate groups (42 classes) share a row but not a column.

**Compatibility.** 1,022 valid (source, contract) pairs over 1,632 types; every source is valid for its own signature; 427 of 610 sources are valid for exactly one contract, 48 for 2, 83 for 3, 10 for 4, 42 for 5. Validity breadth is largest for the D contract and its policy duplicates (35–37 sources) and, among self-cooperating contracts, for ALLC-like ones (17–19). FairBot's contract is the broadest conditional one, valid for 7 sources (μ 0.0051); P*'s for 2, PrudentBot's for 1. There are no tags.

**Certified-implication audit.** Exhaustive over every (type, type, atom) at b ∈ {∞, 4, 2, 0}: 2,452,800 contract reads, 566,032 with a true box, **0 violations**; 0 source-box violations; 0 of 1,044,484 carrier pairs off-table; at b = ∞ the non-carrier block equals `modal.evaluate` exactly.

**Gate** (v = k(y)·(1 + settle(y, x)), the semantic-stabilization proxy). The joint fixed point cycles with period 2 at b = 4 and b = 2 (the intersection of the cycling masks was used; the sibling gate run used a world-indexed trace instead). Masked μ×μ share 0.0005 / 0.018 / 0.067 at b = 4 / 2 / 0. FairBot's self-cost is 1, so the prover network stays mutually legible for every b ≥ 1 and the gate binds only at b = 0, where only constants are legible from source.

**Finite-ε runs** (well-mixed, N = 6,400, ε = 10⁻³, w = 0.3, 10⁵ generations, second half, μ seed, 3 seeds; b ∈ {2, 4, ∞} × s ∈ {0, 1} × f₀ ∈ {0, 0.01, 1} × σ ∈ {0, 0.1, 1}). Every cell lies between 0.93 and 0.99: source oracle 0.991; b = 2 with no contracts 0.991; contract baseline (b = ∞, f₀ = 1, s = 1) 0.980; b = 2, f₀ = 1: 0.970 (s = 0) and 0.975 (s = 1). Where contracts are carried, **contract composition equals source composition** (e.g. FairBot 0.50 / C 0.22 / `BOX(THEM(THEM))` 0.19 as contracts and as sources). Swaps at σ = 1, s = 1 over 3 seeds: about 1.1·10⁹ copied the recipient's own contract, about 7.5·10⁸ were rejected as invalid, and 1–4·10⁴ were accepted changes, mostly none → `<D>` on D-source newborns. With s = 0, carriers die out (second-half fraction 0.000 at f₀ = 0.01, 0.00–0.04 at f₀ = 1). Source-ALLC load 0.155–0.283; contract-ALLC load equals it when s = 1 and is 0 when s = 0. The anti-prover ("exploit if provable") share is 0.000 in every cell.

**Uniform-donor control** (σ = 1): FairBot's contract share 0.14–0.57 with uniform donors against 0.01–0.50 payoff-weighted; at b = ∞, s = 1, f₀ = 1 `<BOX1(THEM(ME))>` (0.45) beat FairBot's contract (0.009). Composition tracks the sources, not breadth or donor fitness. **Neutral-label control:** a behaviourally neutral label copied the same way fixes at 1.00 in nearly every σ = 1 cell, while the largest contract share is ≈ 0.70: copying alone concentrates more than contracts do, because validity pins contracts to sources.

**N path** (b = 2, s = 0, f₀ = 0.01): σ = 1 gives 0.854 / 0.977 / 0.992 and σ = 0 gives 0.987 / 0.979 / 0.984 at N = 1,600 / 6,400 / 25,600; carriers 0 throughout.

**Lottery** (ε = 0, iid μ seeding, mN = 1, 40 runs per cell). Efficient fraction at (100, 4) / (400, 4) / (100, 64) / (100, 256): free arm (b = ∞) 0.33 / 0.55 / 0.97 / 1.00; b = 2 with no contracts 0.30 / 0.55 / 1.00 / 1.00; every b = 2 and b = ∞ contract configuration within Wilson noise of these (the one marginal cell is b = 2, f₀ = 1, σ = 1 at (400, 4): 0.40 against 0.55). Every run froze. **The n = 8 free-arm lottery reproduces the n = 6 pattern** (0.25 / 0.45 / 1.00 / 1.00) within its intervals.

**b = 0 supplement** (the gate binds; N = 6,400, μ seed):

| s | f₀ | σ | P(C,C) | carriers | top contract |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0.001 | 0 | — |
| 0 | 0.01 | 0 / 1 | 0.002 / 0.003 | 0 / 0.17 (all `<D>`) | — |
| 0 | 1 | 0 | **0.989** | 0.72 | `<BOX(THEM(THEM))>` 0.33, FairBot's 0.33 |
| 0 | 1 | 1 | 0.659 (one seed collapsed to D) | 0.80 | FairBot's 0.33 |
| 1 | any | any | 0.95–0.99 | 1.00 | FairBot's 0.15–0.67 |

b = 0 lottery: with f₀ = 1 the efficient fractions are 0.25 / 0.42 / 0.97 / 1.00 (σ = 0) and 0.35 / 0.57 / 0.97 / 1.00 (σ = 1), the free arm's levels; with f₀ = 0.01 they are 0.00–0.17 at every (N, I) and σ, and with f₀ = 0 they are 0.00–0.05.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| P1 | contracts restore legibility at b = 2 | **Failed on its premise:** b = 2 without contracts is 0.991 (the gate is inert); the other clauses hold |
| P2 | under swapping the FairBot-contract wins on validity breadth | **Failed:** ≤ 0.50; composition tracks sources; P* is 0 and there are no tags, so the falsifier did not fire |
| P3 | swapping spreads a contract from a 1% seed | **Failed:** σ = 0 and σ = 1 agree (0.98) with carriers 0; the seed dies at every σ and N |
| P4 | source-ALLC load 0.2–0.35, unchanged by σ | **Partly:** 0.155–0.283; loads coincide when s = 1, not when f₀ = 1 |
| P5 | lottery: f₀ = 1 within 0.15 of free at b = 2; f₀ = 0.01, σ = 0 at least 0.3 lower | **Mixed:** first clause holds (one cell at the margin); second fails because nothing was lost at b = 2 |
| P6 | neutral label concentrates less than the FairBot-contract | **Failed, falsifier fired:** the label fixes at 1.00 |
| RS-a | with rich contracts, limits to the free-proof case | **Mostly holds:** f₀ = 1 cells 0.933–0.988 against 0.991; two cells 0.057–0.058 below |
| RS-b | "defect if their cooperation is provable" does poorly | **Holds:** share 0.000 everywhere |
| S1–S4 | b = 0 supplement: collapse without contracts; restoration with | **Hold:** 0.001–0.003 without; 0.95–0.99 with f₀ = 1 or s = 1 |

**Reading.**
- **Proof-carrying contracts need Löb.** Read as truth tables they are paradoxical; read through provability they are certified-sound (0 violations in 2.45 million reads) and, among carriers, exactly the ungated free box, the α = 1 amortized path. They add nothing to a reader that can already read source.
- **Where legibility is lost, carried contracts restore it.** At b = 0 cooperation collapses to 0.001 without contracts and returns to 0.95–0.99 when contracts are produced at birth (s = 1) or inherited from an established carrier population (f₀ = 1), with FairBot's contract and its family carrying it. This is the RS's pitch confirmed for the case it was made for.
- **Swapping is inert, and a 1% seed dies.** Validity binds each contract to about one source, so transmission reduces to source selection; the few prover carriers in a μ-drawn 1% seed die by drift before any advantage acts, at every budget, including b = 0. The RS's intuition that a small seed spreads to every program that can carry it fails for a seed drawn from μ; a seed of prover carriers was not tested.
- The anti-prover program's share is 0 everywhere, as the RS predicted.

## Three-player majority divide-the-dollar with separate slot populations (`runs/three-player-dollar.md`, `runs/dollar3/`; spec `specs/2026-10-04-three-player-dollar.md`, predictions in `predictions/2026-10-04-three-player-dollar.md`)

Designed by the RE, reviewed by gpt-6.1-sol, run by an Opus subagent over two days under heavy machine load. The modal (PA + Con) full chain at every N and modalPA at N = 10⁴ did not finish (projected beyond 2 hours at load averages near 260); modalPA at N ≤ 10³, one-ring runs of both modal arms at N = 100 (agreeing within 0.01), and static exit and bridge analyses that match between the arms stand in for them.

**Game and language.** Three slots, each submitting (partner, demand) with partner ∈ {other two, ALL} and demand ∈ {1/3, 1/2, 2/3}; pairs form on mutual naming with demands summing ≤ 1, the excluded slot gets 0; the grand coalition needs all three at ALL with thirds; else zeros. Three separate populations, fixed roles. Grammar `A ::= a | if(B, A, A)`, `B ::= BOX_L(THEM_j = a) | not | and | or`, with 3-node atoms about the current encounter. n ≤ 5 is the 9 constants (a conditional needs an `if`); n = 6–9 give identical canonical sets (one-atom conditionals); n = 10 (23k–93k functions per slot) is out of reach for a K³ chain, so n = 6. Arms: modal (PA and PA + Con, 2,475 payoff classes per slot), modalPA (PA only, 1,179; the weak arm's grammar), weak (simulation, 903; it has no probes and hence no fakers), and the constants baseline. Relabeling invariance: 0 mismatches over 20,000 triples × 6 permutations; π invariant to 10⁻¹³.

**Solver.** Rates reach e^(−1000) at N = 10⁴; sparse LU on the generator fails at N = 10³ (it assigned the grand coalition π = 1.0 against 0.003 from GTH). The 729 constant triples plus promoted states are solved by log-scaled GTH, and explored non-core states are eliminated exactly as a stochastic complement. Exploration admits states whose π-weighted inflow exceeds θ with θN = 10⁻⁷; outcome-changing flow leaving the explored set is 0.3–1.1% of all outcome-changing flow.

**π by outcome** (grand / fair pair / unfair pair / wasteful pair / disagreement):

| arm | N = 10² | N = 10³ | N = 10⁴ |
|---|---|---|---|
| constants | .0025 / .376 / .596 / .026 / 1e-4 | .0029 / .371 / .624 / .002 / 0 | .0029 / .368 / .629 / .0002 / 0 |
| weak | .0101 / .373 / .591 / .026 / 4e-4 | .0161 / .366 / .615 / .002 / 1e-4 | .0167 / .364 / .620 / .0002 / 0 |
| modalPA | .0099 / .373 / .591 / .026 / 4e-4 | .0161 / .366 / .615 / .002 / 1e-4 | not finished |

Encounter-level: E[max share] 0.596 at N = 100 and 0.600–0.604 at N ≥ 10³; P(some slot gets 0) 0.983–0.998; efficiency ≥ 0.995.

**Support.** About 0.94 of π sits on constant triples; the rest is one-conditional "shadow" states (a constant pair plus a reader in one slot, each ≈ 10⁻⁵). States with two or three conditionals have zero mass: hand-built Löbian handshakes leak at least as fast as their constant counterparts (pair handshake neutral exit 3.7·10⁻⁴ against 3.0·10⁻⁴ for the constant pair at N = 10³; grand handshakes 0.7–1.1·10⁻⁴ against 2.7·10⁻⁶ for the constant grand coalition).

**Transitions.** The pair mechanism is identical in every arm: (1) the excluded slot drifts neutrally to an offer that pays one member more (0.299/N per mutation event); (2) that member, the pivot, takes it by a strict move (ρ = 0.049 or 0.095); (3) pivots only move up, 1/3 → 1/2 → 2/3. **No program in a pair can stop its partner's own slot from defecting, so reading source does not plug this exit.** Currents: the net circulation P12 → P13 → P23 is 0 (10⁻²⁰), forced by relabeling symmetry; between outcome types there is a consistent net current fair → unfair → wasteful → fair of 1.9·10⁻⁵ / 3.6·10⁻⁶ / 3.9·10⁻⁷ per event at N = 10² / 10³ / 10⁴, ∝ 1/N.

**Grand coalition.** With constants only it is drift-closed (every exit and the entry cost a member 1/3), with a flat share 0.003. At n = 6 it is not: 54 bridges (108 in modal) such as `if(BOX(2 = (1, 1/2)), (2, 1/3), (ALL, 1/3))`, which plays (ALL, 1/3) on path and accepts a pair offer, with mass 3.3·10⁻⁴ per event against 0.149 for a constant pair; neutral exits 2.67·10⁻³/N, then strict or neutral pair formation. Entry runs through "join iff slot j joins" readers plus a strict last step, flat in N. Net: 3–6× the constants' grand coalition, at an N-independent ≈ 0.016.

**Dwell and mixing** (weak arm, mutation events): grand 2.1·10⁵ / 3.7·10⁶ / 3.7·10⁷; pair 2.2·10³ / 1.35·10⁴ / 1.2·10⁵; disagreement ≈ 80. Lumped relaxation time 2.1·10⁵ / 3.7·10⁶ / 3.6·10⁷.

**Agent-based check** (εN = 0.1 per slot per generation; approach rates). Uniform starts reach pairs within 10–900 generations; mean interior pair dwell 790–2,130 generations with 5–37 pair-to-pair switches per 10⁵ generations; the grand-coalition start holds for 26,440 and 67,100 generations, and for all 10⁵ in one seed.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | no efficient triple is drift-closed at the n run | **Held** at n = 6 (none of 150 efficient states per cell); the constant grand coalition is drift-closed at n = 1, sol's trapped state one language down |
| 2 | pairs ≥ 0.6, grand ≤ 0.2; a net current around the three pairs | mass **held** (pairs 0.99); the circulation clause **failed as stated**: it is 0 by symmetry; the real current is among outcome types |
| 3 | unfair pairs below fair pairs (bidding war capped) | **Failed, falsifier fired:** unfair 0.59–0.63 against fair 0.36–0.38 everywhere |
| 4 | E[max share] ∈ [0.45, 0.60], exclusion ≥ 0.6 | **Held** (0.596–0.604; at the upper edge by 2:1 arithmetic; the > 0.62 falsifier never met) |
| 5 | grand coalition leaks like the shadow; share < 0.2 | share and exit mechanism **held**; the "three neutral steps" entry clause **failed** (reader plus strict step) |
| 6 | weak arm has ≥ 2× the modal arm's disagreement | **Failed:** identical |
| 7 | finite ε: pair turnover; grand start decays within 10⁴ generations | turnover **held**; decay clause **failed** (26k, 67k, > 100k) |
| 8 | constants baseline: fair pairs ≥ 0.5, grand < 0.1 | **Failed** on fair (0.37); grand clause held; the stated reason was wrong too |

**Reading.**
- **Source reading adds nothing to coalition stability here.** Modal equals weak to three decimals, and both equal the constants apart from a 3–6× bump in the grand coalition.
- **The binding exit is new to k ≥ 3:** a pair member defecting to the excluded slot's better offer. That is a strict move in the defector's own slot, which no program reading its partner can prevent. Unfakeability, the PD lesson, does not cover it.
- **Stochastic stability selects rotating, mostly unfair pairs:** a dictatorship of the pivot, rotated by symmetry. Unfair pairs win because each pair has two unfair orientations and pivots only ratchet up: the excluded slot buys a member with 2/3 at its own cost of 1/3.
- **The grand coalition is drift-closed only in the constants language** and loses closure at n = 6 to one-atom "accept a pair offer" bridges, a k = 3 instance of the sibling theorem's lesson that larger languages open leaks.
- As with the fixed-role ultimatum game, the selected outcome is the one whose deviations are generous rather than self-punishing.

## Almost all seeds: compatibility among co-seeded establishers (`runs/compatibility.md`; spec `specs/2026-10-05-compatibility.md`, predictions in `predictions/2026-10-05-compatibility.md`)

Designed by the RE, reviewed by gpt-6.1-sol, run by an Opus subagent (about 35 minutes on 3 workers; nothing censored). Modal arm, PD, w = 0.3, ε = 0; classes are the behavioural classes at the cutoff.

**Compatibility index** κ = P(mutual cooperation | both μ-draws are establishers), denominator μ_est², same-class draws counting as cooperation (18% of the denominator at n = 12): κ = 0.977 / 0.958 / 0.951 at n = 6 / 9 / 12 (0.971 / 0.949 / 0.941 excluding same-class draws); mutual-defection rate 0 / 0.0010 / 0.0017; exploitation rate 0.023 / 0.041 / 0.047. All establishers form one mutual-cooperation component at every n, so components carry no information (as sol said); the missing-edge mass inside it is 2.3% / 4.2% / 4.9%, rising with n. In the heavy set at n = 12, FairBot's pair, the THEM(THEM) pair and the probe-readers are a pairwise clique; every other heavy incompatibility involves the two near-universal suckers `not(BOXD(THEM(^C)))` / `not(BOXD1(THEM(^C)))` (establishers that every prover exploits) or PrudentBot (μ ≈ 3·10⁻⁶), which mutually defects with `BOX1(THEM(ME))` and both probe-readers.

**Co-seeding.** Incompatible pairs number 11 / 4,360 / 1,401,462 at n = 6 / 9 / 12 (mutual defection 0 / 770 / 283,091; the rest exploitation). The 10 consequential pairs at every n are all a prover exploiting a sucker (co-seeding 0.053–0.095 each at N = 400). P(an island co-seeds some incompatible establisher pair), simulated: 0.026 / 0.053 / 0.063 at N = 100 and 0.119 / 0.219 / 0.260 at N = 400 (n = 6 / 9 / 12); at n = 12, 0.696 at N = 1,600 and 0.992 at N = 6,400. **Co-seeding tends to 1 in N**, as sol predicted. **Anti-coordinators** (x(y) = y(x) = C, x(x) = y(y) = D; never establishers) carry 2–3% of μ; some pair is co-seeded on 0.89–0.93 of islands at N = 400, 0.024–0.073 for pairs that both defect on D; the observed unresolved pair co-seeds at 0.001.

**Re-analysis by the certification rule alone** (1,920 seeds-in-n runs, 520 seeds-tail runs, 24,000 natural and 525,000 forced spoiler islands). In the PD, a certified island has every present class pairwise payoff-identical, and since T ≠ S that forces all-CC or all-DD: P(C,C) is 0 or 1 on every certified island and P(C,C) < 0.95 coincides with Pareto inefficiency. 0 frozen cooperative islands are below 0.95; 1,920 certified islands hold two or more establisher classes, all mutually cooperating. The only uncertified islands in the programme are 9 anti-coordinator polymorphisms at P(C,C) ≈ 0.5 with no establisher (1 of 4,800 seeds-in-n islands, 8 of 525,000 forced, 0 of 24,000 natural). Two runs at n = 9, (100, 256) are certified-*separated*: `BOX1(THEM(ME))` on 255 islands and a P*-family program on one, mutually defecting across islands yet every island efficient: a rival network between islands. Natural-island efficiency is not lower when an incompatible pair is co-seeded (0.269 with a mutually-defecting pair, 0.204 exploitation-only, 0.180 compatible, at n = 12, N = 400).

**Conditioned lottery** (n = 12, N = 400, 400 islands each): conditioned on a consequential pair (acceptance 0.199), 84 efficient and 0 with an incompatible pair in the terminal support (exploiter survives 82, exploited 18, both 0); conditioned on a mutually-defecting establisher pair (acceptance 0.017), 89 efficient and 0 polymorphic; unconditioned, 68 efficient. All certified.

**Pair competitions** (N = 400, 100 runs per start): exploitation pairs, the exploiter wins 100% pair-only and dies alongside in up to 15% of runs in a full-μ background; mutually-defecting pairs are bistable (coin flip at 1:1, the larger class wins 100% at 3:1, never polymorphic), shifted in the background toward the ALLC-exploiting member (TV 0.19–0.34 at 1:1); anti-coordinators are 100% polymorphic pair-only and collapse in the background unless both defect on D (then polymorphic in 29–41%).

**The two-class argument.** Two self-cooperating classes both earn R = 0 against themselves; a stable mixed state would need each to earn more than 0 against the other, so each would have to exploit the other, which is impossible. Establisher pairs are neutral, bistable or dominated, and only self-defecting classes can hold a stable two-class polymorphism. With three or more classes a cycle is not excluded analytically; none was observed.

**Unresolved incompatibility risk** = P(co-seed) × P(resolution fails): the first factor rises to 1 in N; the second is 0 of 3,814 co-seeded islands (rule-of-three bound 7.9·10⁻⁴). Per-island risk ≤ 7.9·10⁻⁴ at N ≤ 400, n ≤ 12, with uniformity in N resting on the two-class argument.

**Verdicts.**
| # | prediction | outcome |
|---|---|---|
| 1 | κ ≥ 0.9; heavy set one network except PrudentBot | **Held** on the falsifier; "one component" vacuous; PrudentBot also mutually defects with `BOX1(THEM(ME))` |
| 2 | pair mass < 0.05 of μ_est²; co-seeding 0.1–0.4 at N = 400, rising | **Held** (0.0017; 0.26) |
| 3 | certified cooperative islands efficient | **Held structurally** |
| 4 | resolution by pattern; anti-coordinator co-seeding < 0.02; background changes < 20% | **Failed** on the last two clauses (0.024–0.073; TV 0.19–1.0); pattern clauses held; falsifier not fired |

**Reading.**
- Compatibility is not where the seed lottery fails at n ≤ 12: incompatible establishers meet on most large islands and selection settles every pair, because two self-cooperators cannot hold a stable mixture.
- The only unresolved islands in the programme are anti-coordinator polymorphisms with no establisher, ≈ 3·10⁻⁵ per natural island.
- The real compatibility risk is *between* islands: mutually-defecting establishers held on separate islands, each efficient, a rival network at the metapopulation level, which is DEFERRED 1's I ≫ N migration question.
- κ < 1 comes from the provers' exploitation of the near-universal suckers, the faker structure of the mutation object seen from the other side; it is a property of the prior and language-relative.

## Not done

- Prediction (c) at n=9 through the chain (the enterer search covers what
  L_9 can do against all-D and all-p, but not the full n=9 chain).
- N = 1000 in the weak arm.
- Polymorphic-target ρ beyond the truncated-product approximation.
