# Rock-paper-scissors with a compute price (notes, 2026-10-23)

Spec `specs/2026-10-23-rps-priced.md` (reviewed by gpt-6.1-sol, then gemini-4-argon in amended mode; both folded). Builds on
`specs/2026-10-23-rps-mixed.md`, `notes/rps.md` and `runs/rps.md`. §1 is written by hand before any code of this run and
before any counted cell. §2 (choices where the spec is silent, and deviations) is appended with the code, before any
counted cell. Everything numerical in §1 was derived on paper from the semantics below; the code is checked against it
afterwards (tests), never the other way round.

## 1. Hand derivations

### 1.0 The charge, as a recurrence

Notation as in `notes/rps.md` §1: D = 12, one depth counter per root evaluation, an application consumes one level, an
application met at remaining depth 0 yields a forfeit and executes nothing. For a body `e` of program a facing opponent
program b with d levels left, let

* `E_d(e; a, b)` be the application depth reached when `e` is evaluated the way a program plays (its own coins are
  sampled; the expected value over them is taken), and
* `M_d(e; a, b)` the application depth reached when `e` is evaluated exactly, i.e. inside a `cr` (every coin branch is
  explored; the deepest branch counts).

Recurrences (the opponent's body is run on one level less, with the roles swapped):

| node | `E_d` (play) | `M_d` (exact reading) |
|---|---|---|
| R, P, S, X | 0 | 0 |
| `next e` | E(e) | M(e) |
| `coin e1 e2` | 1/2 E(e1) + 1/2 E(e2) | max(M(e1), M(e2)) |
| `cr e` | M(e) | M(e) |
| `THEM(arg)`, d >= 1 | 1 + E_{d-1}(body of b; b, arg) | 1 + M_{d-1}(body of b; b, arg) |
| `THEM(arg)`, d = 0 | 0 (forfeit) | 0 (forfeit) |

where `arg` is a (ME: a, THEM: b, `^B`: B). The depth cost of a against b is `H(a, b) = E_D(body a; a, b)`. A forfeit
along a linear chain pays exactly D = 12 (the chain of nested applications executed before the cap), and nothing pays
more; X, constants and `coin` of constants pay 0. The priced payoff is `U_c(a, b) = U(a, b) - c H(a, b)` with U the
unpriced payoff of `notes/rps.md` §1.3. The *work* price replaces the max in `M(coin)` by a sum (all branches of a `cr`
computation are executed); the *forfeit-only* control charges `c D P(a forfeits against b)` and nothing else.

### 1.1 Depth and work coincide at n = 6 (and in play at every n)

A body has no sequential composition: its constructors are unary (`next`, `cr`) and `coin`, and an application's argument
is a lifted program that is not executed. Along any one evaluation path a body therefore executes at most one application
per level, so the expected number of applications equals the expected depth in play mode, for every n. The max and the sum
in `M(coin)` differ only if both branches of a coin contain an application, which needs `coin(THEM(.), THEM(.))`, 7 nodes.
At n = 6 no body has two applications, so **work = depth on the whole n = 6 table in every arm**, and the spec's
work-price sensitivity is vacuous at n = 6. It becomes informative only for an exact reader of a two-application coin at
n >= 7: for `K2 = coin(THEM(ME), THEM(THEM))` read by `C = cr(THEM(ME))`, the depth is the deepest of the two branches
(a single chain, at most D) while the work is the sum of both branches' executions, which branch again at every level of
the mutual reading and grows like 2^(D/2); the number is computed in §2. The code will check "work = depth at n = 6" as a test, and the sensitivity will be made informative at n = 7 on
the unpriced class representatives (§2 says what was done).

### 1.2 The cost table of the eleven named programs (depth = work), D = 12

Row = the program that pays, column = the opponent. R, P, S, X and M = `coin R P` pay 0 against everyone. TM = `THEM(ME)`,
N = `next(THEM(ME))`, N2 = `next(next(THEM(ME)))` have identical cost rows (a unary wrapper adds nothing); C =
`cr(THEM(ME))`, GN = `coin X (next(THEM(ME)))`, GC = `coin X (cr(THEM(ME)))`.

(a) Pure reader r in {TM, N, N2} against a constant or X or M: one application, then the opponent's body is a leaf:
H = 1. Against another linear reader (TM, N, N2, C): each reads the other, the chain runs to the cap: H = D = 12.

(b) C against a constant, X or M: 1. Against any reader, guarded or not: exact reading explores every branch of the
guard's coin, so the deepest branch is the full chain: H = 12 (also against GN and GC).

(c) Pure reader r against GN. Write a_d = H_d(GN; r), b_d = H_d(r; GN). Then a_0 = b_0 = 0, a_d = 1/2 (1 + b_{d-1}),
b_d = 1 + a_{d-1}. Iterating: (a_1, b_1) = (1/2, 1), (a_2, b_2) = (1, 3/2), (a_3, b_3) = (5/4, 2), (a_4, b_4) = (3/2, 9/4),
(a_5, b_5) = (13/8, 5/2), (a_6, b_6) = (7/4, 21/8), (a_7, b_7) = (29/16, 11/4), (a_8, b_8) = (15/8, 45/16),
(a_9, b_9) = (61/32, 23/8), (a_10, b_10) = (31/16, 93/32), (a_11, b_11) = (125/64, 47/16), then
a_12 = 1/2 (1 + 47/16) = **63/32 = 1.96875** (GN pays this against a pure reader) and b_12 = 1 + 125/64 = **189/64 =
2.953125** (the pure reader pays this against GN). Fixed point (2, 3) as D -> infinity.

(d) GN against itself: e_d = 1/2 (1 + e_{d-1}), e_0 = 0, so e_12 = 1 - 2^-12 = **4095/4096**. GN against a constant, X
or M: 1/2 (1 + 0) = 1/2.

(e) GC pays half of an exact reading: against any reader, linear or guarded, and against C: 1/2 * 12 = **6**; against a
constant, X or M: 1/2. GN against C: 1/2 (1 + E_11(C; GN)) where E(C) = M = 11 at d = 11: 1/2 * 12 = **6**. GN against GC:
1/2 (1 + E_11(GC; GN)) with E_11(GC; GN) = 1/2 * 11 = 11/2: 1/2 * 13/2 = **13/4 = 3.25**. A pure reader against GC:
1 + E_11(GC; r) = 1 + 11/2 = **13/2 = 6.5**.

Summary, H(row, column):

| row \ col | R P S X M | TM N N2 | C | GN | GC |
|---|---|---|---|---|---|
| R P S X M | 0 | 0 | 0 | 0 | 0 |
| TM N N2 | 1 | 12 | 12 | 189/64 | 13/2 |
| C | 1 | 12 | 12 | 12 | 12 |
| GN | 1/2 | 63/32 | 6 | 4095/4096 | 13/4 |
| GC | 1/2 | 6 | 6 | 6 | 6 |

Forfeit-only control (charge `c D P(forfeit)`, D = 12): self-play forfeit probabilities from `notes/rps.md` §1.3: TM, N, N2,
C forfeit against every reader with probability 1 (so pay 12 c) and against constants, X, M never (pay 0); GN and GC
forfeit against everything with probability 2^-13 (pay 12 c 2^-13 = 1.46e-3 c); a pure reader against a guarded reader
forfeits with probability 2^-6 (b-side) and the guarded reader with 2^-7; constants, X, M never. The forfeit-only price of
N against a constant is 0, whereas the depth price is c.

### 1.3 Priced payoffs, c = 0.01 (depth price = work price), D = 12

`U_c = U - c H`, U from `notes/rps.md` §1.3 (e = 1/128). Row against column; constants R, P, S keep their unpriced rows
among themselves. Selected entries:

* R, P, S, X, M against anything: unchanged (they pay nothing).
* N and C against a constant: **0.99**; N2 against a constant: **-1.01**; TM against a constant, X or M: **-0.01**.
* any pure reader against X: **-0.01** (it earns 0 in the game and pays 1 level); C, N, N2 against X: -0.01.
* TM, N, N2, C against each other: **-0.12** (a mutual forfeit, game payoff 0).
* N against GN: **-1/128 - 0.01 * 189/64 = -0.037344**; GN against N: **+1/128 - 0.01 * 63/32 = -0.011875**.
  The guarded reader's gap over the pure reader against the same opponent grows from 2e (1/64) to 0.0156 + 0.0098 = 0.0254.
* GN against a constant: **0.5 - 0.005 = 0.495**; GN against X: **-0.005**; GN against GN: **-0.009998**
  (cost 0.01 * 4095/4096, game payoff 0).
* GC against a pure reader (TM, N, N2, C): **+1/128 - 0.06 = -0.052188**; against GN or GC: **-0.06**; against a constant:
  **0.495**. A pure reader against GC: **-1/128 - 0.01 * 13/2 = -0.072813**.
* X against everything: **0** (no program that does not forfeit earns anything against X; X pays nothing).

### 1.4 Hand statics

(i) *Prediction 1.* Let r be a program whose self-play forfeits with probability p_f > 0. Its game payoff against itself is
0 (symmetric), its cost H(r, r) >= p_f * D > 0, so U_c(r, r) <= -c p_f D < 0. X earns U_c(X, r) = -U(r, X) >= 0 (the game
is zero-sum, X is uniform, so the only game payoff against X is a forfeit penalty -p_f(r, X) <= 0 for r), and r earns
U_c(r, X) = U(r, X) - c H(r, X) <= 0. In the two-type contest at frequency x of X, the fitness difference X - r is
linear in x: at x = 0 it is U_c(X, r) - U_c(r, r) > 0 (X invades) and at x = 1 it is -U_c(r, X) >= 0. So X invades r and
weakly dominates it at every frequency, strictly for x < 1. The checks over the whole n = 6 table: X's payoff against every
program is >= 0 (X earns exactly 0 against everything that does not forfeit and +p_f against a program that forfeits
against it; no program forfeits against X in the present grammar), X pays 0, and the dominance inequality above holds for
every program with p_f > 0, for each c > 0 (and fails for c = 0, where U_c(r, r) = 0 for a self-forfeiting program only
ties: X does not invade it).

(ii) *Consequence for the chain (not a scored prediction).* In the unpriced chain pi(X) = mu(X) held exactly because X
entered and left every state at the neutral rate. Priced, a mutant meeting X pays a non-negative cost and earns at most 0, so
leaving X is never faster than neutral while entering a costly resident is faster than neutral: pi(X) >= mu(X), strictly
for c > 0 whenever any costly program is a resident anywhere in the chain. The constants R, P, S and M stay exactly
neutral to X (zero cost, zero payoff in both directions), so the X sea remains neutrally invaded by them, and the chain's
net-unexploitable set Z0 still contains X's cost-free twins and nothing that reads.

(iii) *Toy chain.* The eleven classes of `notes/rps.md` §1.4 with a uniform prior, priced at c = 0.01 (D = 12): X is
invaded by nothing except the cost-free constants and M (neutral); every reader sea (N, C, TM, N2) is invaded by X (X earns
0 against a sea whose members earn -0.12) and by GN/GC with a large advantage; GN and GC seas are invaded by X
(advantage 0.01 against a GN sea, 0.06 against a GC sea). Hence pi concentrates on X (plus neutral constants and M, which are
re-invaded by readers and by the guards). At N = 10^4 the pi mass on X is >= 0.8 and the mass on the guarded readers is
below 0.1; at N = 100 selection is weak (N w * 0.06 = 1.8 at the largest payoff gap) and pi is more spread. This is the
validation cell for the chain machinery (it also reproduces `chain.Chain` on the same table).

## 2. Choices where the spec is silent, and deviations (written with the code, before any counted cell)

*Disclosure.* Before this section was committed I ran, while debugging, the following; none changed a prediction, a scoring
convention or a cell of the spec. (i) The static table (classes, splits, Prediction 1 statics, work-minus-depth) over all
arm and price combinations, `runs/rps_priced/static.json`. (ii) The sample arm at c = 0.01: discovery, the chain at N = 100
(exploration thresholds 1e-6, 1e-8, 1e-10) and N = 10^4 (1e-10), which showed pi(X) = 0.84 at N = 10^4 and a polymorphic mass of
a few 1e-4; N = 100 at 1e-10 was killed after 20 minutes. (iii) Lottery pipeline tests: sample arm at c = 0 runs 0-2 (they
reproduce the stored unpriced run bitwise) and exact arm at c = 0.01 runs 0-1 (deleted before the counted cells). (iv) The
eleven-program toy chain (§1.4(iii)), `runs/rps_priced/toy.json`. The predictions file was committed before any code existed.

1. **Price implemented as §1.** One numba kernel computes `E_d` and `M_d` for every ordered pair of programs
   (`rps_priced._cost_depth`), the work price replaces the max in `M(coin)` by a sum, the forfeit-only price is
   `c D P(forfeit)` from the stored forfeit mass. The kernel is checked against a recursive reference on random pairs in every
   arm and against the hand table of §1.2 on the eleven programs. Payoffs `U - c * cost` are formed on the full program table
   and only then collapsed to classes.
2. **Work = depth at n = 6; the work-price sensitivity of the spec is vacuous there.** The check is `HW == H` on the whole
   table (maximum absolute difference 0.0 in all four arms), so a work-price cell would reproduce the depth-price cell bit for
   bit and is not rerun; the maximum node count over the n = 6 table is 12, equal to the depth maximum. The sensitivity is
   made informative at n = 7 on the unpriced exact class representatives (`n7work`, §3 of the run report; the classes are not
   recomputed under the price there). The spec's remark that the notes' hand table contains cases where depth and work differ
   is corrected by §1.1: it needs a two-application coin, 7 nodes.
3. **Classes.** Programs with equal priced payoff rows and columns, rounded to 9 decimals (the chain's own twin tolerance is
   1e-9) and then merged where the representatives agree within 1e-11 on every entry (rounding-boundary splits); at c = 0 the
   unpriced 6-decimal rule is used so the unpriced tables are reproduced exactly. Pricing splits only the class of `X`: its
   unpriced class contains the costly impostor `THEM(^THEM(THEM))`. K goes 87 -> 88 (sample, matched), 125 -> 126 (exact),
   123 -> 124 (exact-br) and the pure arm is unchanged at 18. Class masses and source multiplicities are the sums of member
   priors.
4. **Chain solver.** `LogChain`, twin-expanded, closure-seeded as in the unpriced run, with these choices. (a) The exploration
   threshold is 1e-8 (log10 theta = -8, not the unpriced 1e-14): once polymorphic states exist, the expansion of every state with
   inflow above 1e-14 is not affordable (each polymorphic expansion costs 1-3 s, thousands of states); the cut mass is reported
   per cell as `log10_cut` and the sensitivity cells at N = 10^4 re-run at 1e-6 and 1e-10 and lumped. (b) The invasion
   closure follows only the 8 strongest invaders at each node (the unrestricted closure explodes: over 100 s at 600 nodes
   at K = 88), and a multi-start replicator search (1,000 random starts, supports of 2-6 classes, `solver_audit.attractor_search`)
   supplies further stable polymorphic seeds. Both are N-independent and computed once per cell. (c) Any three-type cycle met
   by a mutant is recorded as an indeterminate event and receives no stationary weight (`indeterminate_*` fields).
5. **Lottery.** `rps.lottery_kernel` unchanged; founders drawn at the program level with the unpriced run's founder seeds
   (`founders|primary` run r), mapped to the priced classes after seeding (tested: summing the priced counts over the members of
   an unpriced class returns the unpriced founder counts exactly); dynamics seed identical to the unpriced run's, so that the
   c = 0 pipeline is bitwise the stored run (tested on the stored statistics). Every run is carried to 10,000 generations (the
   cost is a few seconds per run, so the extension rule "unresolved islands continue to 10,000" is applied to all runs; the
   generation-2,000 reading stays the primary one, and the 10,000 reading is reported for the runs with an unresolved island and
   for all). Supports are sampled every 10 generations over [1500, 2000] and [9500, 10000]; the share cut-off is
   count >= 5% of N. A class change, a return to an earlier support, and no change give unresolved, cycling, resolved.
6. **Statistics.** Net exploitability `e_prog` = max over the arm's own classes of the priced payoff against the population;
   gross = same with game payoffs (`e_gross`); individual exploitability `e_indiv` = sum over residents of x_p max_k U_c[k, p];
   `cost_paid` = x' C x with C the class-level cost matrix (c included), `net_payoff` = x' U_c x. The exploiter-set control uses
   the priced exact arm at the same price (`rps_priced.get_aex`). The pure arm has no X, so its net exploitability can be
   negative.
7. **Work/forfeit/depth-panel controls.** Forfeit-only at c = 0.01 in all four arms; the depth panel holds c D = 0.12 at D = 8
   (c = 0.015) and D = 16 (c = 0.0075) in the sample and exact arms, with the base tables rebuilt at those caps; exact-br at
   c = 0.01.
8. **Memory.** One exact-arm job (priced classes, table memory-mapped, 3,696 programs) peaks at 0.71 GB RSS, so three workers
   fit comfortably.
9. **Not done / deviations of scope.** n = 7 priced for the main arms (the priced spec does not ask for it); a 200-run
   replicate is run only if the budget allows (flagged in the run report).

## 3. Deviations and facts recorded while running (after the counted cells began)

1. **Batch.** 26 jobs of `rps_priced_run.py job` (one process each, three at a time, peak 0.7 GB) plus the 200-run replicates of the four arms at
   c = 0.01 (`--lottery primary200`, same founder seeds as the unpriced replicate). Per job: discovery once (about 100-150 s: pairs,
   triples, the 8-strongest-invader closure, 1,000-start replicator search), then the four chains, then the lottery cells. Exploration threshold
   1e-8 (primary); the N = 10^4 sensitivity cells re-ran at 1e-6, 1e-10 and lumped for the four arms at c = 0.01 only.
2. **c = 0 reference.** Run through this pipeline (chains N = 10^3, 10^4; lottery primary) so that the reference has the extra statistics (readers,
   guarded, cost); the lottery rows are bitwise the stored unpriced run (tested) and the chain rows agree with the stored chains to 1e-6.
3. **The 200-run replicate** was not in the spec's cut order; it was run because 40 runs cannot resolve Prediction 7 (disclosed; it is a
   supplementary cell and is reported beside the 40-run paired difference, which is the scored one).
4. **Resolution rule.** Applied at the primary generation-2,000 reading and, for every run, at generation 10,000; the "cycling" label is
   frequent because a class hovering around the 5% cut-off revisits an earlier support, so it measures drift among neutral classes, not
   a limit cycle of the replicator. Cycling and unresolved islands are reported, not extended.
5. **Work price at n = 6** was not run as separate cells (identical tables, §2.2). The n = 7 work-versus-depth supplement is described in the run
   report; if its chain did not finish, the report says so.
6. **Correction to §1.1.** The hand estimate "grows like 2^(D/2)" for the work of an exact reader of a two-application coin was wrong. Both branches
   of `coin(THEM(ME), THEM(THEM))` execute an application and recurse into the same reader at every level, so the exact computation
   executes 1 + 2 + ... + 2^(D-1) = 2^D - 1 = 4095 applications at D = 12 (the computed maximum over the n = 7 closed set is 4095, for
   `cr(...)` readers of that coin; the depth cost of the same pair is 12). 244 of the 141,376 class pairs have work above depth. At c = 0.01 that
   is a branching tax of 41 per play, so a work price would end exact reading of branching programs outright; none of them is in the chain's
   support, which is why the n = 7 chains under the two prices coincide to six decimals.
7. **n = 7 chains.** The first full-discovery launch used the unpriced exploration threshold 1e-14 by mistake (a missing argument in the
   `n7work` driver) and was killed after about 2 hours of CPU; the reported n = 7 cells are the restricted-discovery run (`--quick`: pairs and
   triples among the 120 highest-prior classes, the 8-strongest-invader closure, no attractor search, threshold 1e-8), with the classes of the
   unpriced n = 7 table (not recomputed under the price).
