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
