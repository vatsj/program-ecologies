# Rock-paper-scissors and mixed actions (notes, 2026-10-23)

Spec `specs/2026-10-23-rps-mixed.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both folded).
§1 is written by hand before any code of this run and before any counted cell. §2 (choices where the spec is silent,
and deviations) is appended with the code and before any counted cell. Everything numerical in §1 was derived on paper
from the semantics below; the code is checked against it afterwards (tests), never the other way round.

## 1. Hand derivations

### 1.0 Semantics used in the derivations

* Actions R, P, S, ordered cyclically by "beats": P beats R, S beats P, R beats S. Payoff +1 win, -1 loss, 0 tie.
  `next` maps R to P, P to S, S to R (the action that beats its argument).
* A program is its body (an A-sort expression). `THEM(ME)` run by program a against opponent b is: b's body run with
  b's opponent being a. One depth counter per root evaluation, D = 12 at the root; each application consumes one level;
  an application met at depth 0 yields **forfeit** (F). Evaluation of the opponent's body inside an application runs at
  the remaining depth, so a read of an opponent that itself reads recurses down to depth 0 and ends in F.
* `next(F) = F`. `cr` (the exact counter) of a distribution that puts mass p_f on F plays, with probability 1 - p_f, a
  best response to the *conditional* distribution (uniform tie-break) and forfeits with probability p_f.
* The two players' actual actions are independent given the programs. Payoff of an action against F: +1 (F loses to every
  action); F against F: 0. Hence an unconditionally uniform action earns 0 against any action distribution, and against
  an opponent who forfeits with probability f_o while the uniform player acts, it earns +f_o.

### 1.1 The ten named programs

R, P, S (1 node); X (1 node, uniform); TM = `THEM(ME)` (3 nodes, the mirror: copies what the opponent would do against
it); N = `next(THEM(ME))` (4, the simulating counter); C = `cr(THEM(ME))` (4, the exact counter); N2 =
`next(next(THEM(ME)))` (5, the counter's loser: counters the counter); GN = `coin X (next(THEM(ME)))` (6, grounded
simulating counter); GC = `coin X (cr(THEM(ME)))` (6, grounded exact counter). Call TM, N, N2, C the *pure readers*
and GN, GC the *guarded readers*. One extra mixer, M = `coin R P` (3 nodes), is added for the one place where the
simulating and the exact counter differ.

### 1.2 Derivations

(a) **Constants.** R, P, S play their own action whatever the opponent. Cyclic: P beats R, S beats P, R beats S.

(b) **X** plays a fresh uniform action. Against any opponent that acts, its expected payoff is exactly 0. Against an
opponent that forfeits with probability f it earns +f; an opponent that forfeits against X earns -1 there. No program
in the ten forfeits against X (a reader copies or counters a uniform sample, which is uniform), so X earns 0 against
all ten.

(c) **Pure reader against a constant c.** TM plays c's action against it, which is c: ties (0). N plays next(c) which
beats c: +1. N2 plays next(next(c)) which loses to c: -1. C plays the best response to c, which is next(c): +1.

(d) **Pure reader against X.** The sampled/read action is uniform, so TM, N, N2, C act uniformly; payoff 0.

(e) **Pure reader against a pure reader.** TM vs N: TM needs N's action against TM, which needs TM's action against N
one level lower, and so on to depth 0, where the application forfeits. `next`, `next next` and `cr` propagate F, so both
players forfeit with probability 1 and the payoff is 0 (the self-play of a pure reader forfeits with probability 1).

(f) **Guarded reader in self-play and against another guarded reader.** G_d(g1, g2) = 1/2 U + 1/2 phi(G_{d-1}(g2, g1))
with U the uniform distribution, phi in {next, cr}, and the application at depth 0 giving F: forfeit mass
f_0 = 1/2, f_d = f_{d-1}/2, so f_12 = 2^-13 = 1/8192 for both players. The acting part of each is uniform. Payoff 0
(equal forfeit masses, uniform acting parts). GN vs GC is the same: 0.

(g) **Pure reader r against guarded g.** Let a_d = G_d(g, r) and b_d = G_d(r, g). Then a_d = 1/2 U + 1/2 phi_g(b_{d-1})
(d >= 1; a_0 = 1/2 U + 1/2 F), b_d = phi_r(a_{d-1}) (d >= 1; b_0 = F). Acting parts stay uniform (next and cr of a
uniform are uniform). Forfeit masses: fa_d = fb_{d-1}/2, fb_d = fa_{d-1}, so fa_{2k} = fa_{2k+1} = 2^-(k+1) and
fa_12 = 2^-7 = 1/128, fb_12 = fa_11 = 2^-6 = 1/64. The pure reader earns fa - fb = 1/128 - 1/64 = **-1/128**; the
guarded reader earns **+1/128**. This is a depth-cap effect, one of the spec's declared concerns, and it depends on the
parity of D: for D = 2k the gap is fa_D - fb_D = 2^-(k+1) - 2^-k = -2^-(k+1), for D = 2k+1 it is fa_D - fb_D =
2^-(k+1) - fa_{2k} = 0. So D = 12: -1/128; D = 20: -1/2048; D = 11 and D = 13: exactly 0. The depth sweep must show
exactly this.

(h) **Guarded reader against a constant c.** GN plays 1/2 U + 1/2 next(c): payoff 1/2 * 0 + 1/2 * (+1) = **+1/2**. GC:
1/2 U + 1/2 BR(c) = same, +1/2. Against X: 0.

(i) **The mixer M = coin R P, played against the others.** M plays R or P with probability 1/2 each (no reading).
vs R: 1/2 * 0 + 1/2 * (+1) = +1/2. vs P: 1/2 * (-1) + 1/2 * 0 = -1/2. vs S: 1/2 * (+1) + 1/2 * (-1) = 0. vs X: 0. vs TM:
TM plays M's action, an independent (1/2 R, 1/2 P) draw; two iid draws from one distribution earn 0 against each other.
vs N: N plays next of an independent sample of M's action: for an opponent action distribution d = (r, p, s) the
simulating counter earns r(r-s) + p(p-r) + s(s-p) = 1/2[(r-s)^2 + (p-r)^2 + (s-p)^2] (a sum over its sampled
action, then the actual action), here d = (1/2, 1/2, 0): **1/4**. So u(M, N) = -1/4. vs C: C plays the best response
to d, here P, earning 1/2 * (+1) + 1/2 * 0 = **1/2**; u(M, C) = -1/2. vs N2: N2 plays next(next(sample)), the sampled
action is R or P so N2 plays S or R (S w.p. 1/2, R w.p. 1/2): vs M's actual (1/2 R, 1/2 P): S earns 1/2 * (-1) + 1/2 *
(+1) = 0, R earns 1/2 * 0 + 1/2 * (-1) = -1/2; N2 earns -1/4, u(M, N2) = +1/4. vs GN: GN = 1/2 U + 1/2 next(sample) =
1/2 (1/3, 1/3, 1/3) + 1/2 (0, 1/2, 1/2) = (1/6, 5/12, 5/12); M's payoff: R against d is s - p = 0, P against d is
r - s = -1/4; M earns -1/8, u(GN, M) = +1/8. vs GC: GC = 1/2 U + 1/2 P, d = (1/6, 2/3, 1/6): R earns s - p = -1/2, P earns
r - s = 0, M earns -1/4, u(GC, M) = +1/4. So N and C separate (1/4 against 1/2) and GN and GC separate (1/8 against
1/4) on M, though they coincide on the other nine programs.

### 1.3 The named-class payoff table

Row player's payoff, rows and columns in the order R, P, S, X, TM, N, N2, C, GN, GC (`e` = 1/128). Antisymmetric.

| row \ col | R | P | S | X | TM | N | N2 | C | GN | GC |
|---|---|---|---|---|---|---|---|---|---|---|
| R | 0 | -1 | +1 | 0 | 0 | -1 | +1 | -1 | -1/2 | -1/2 |
| P | +1 | 0 | -1 | 0 | 0 | -1 | +1 | -1 | -1/2 | -1/2 |
| S | -1 | +1 | 0 | 0 | 0 | -1 | +1 | -1 | -1/2 | -1/2 |
| X | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| TM | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -e | -e |
| N | +1 | +1 | +1 | 0 | 0 | 0 | 0 | 0 | -e | -e |
| N2 | -1 | -1 | -1 | 0 | 0 | 0 | 0 | 0 | -e | -e |
| C | +1 | +1 | +1 | 0 | 0 | 0 | 0 | 0 | -e | -e |
| GN | +1/2 | +1/2 | +1/2 | 0 | +e | +e | +e | +e | 0 | 0 |
| GC | +1/2 | +1/2 | +1/2 | 0 | +e | +e | +e | +e | 0 | 0 |

(The R, P, S rows against the constants: P beats R so u(P, R) = +1, u(R, P) = -1; S beats P; R beats S. Row R against S
is +1, row P against R is +1, row S against P is +1.)

Entries against M (the row's payoff against M = `coin R P`): u(R, M) = -1/2 (P beats R half the time), u(P, M) = +1/2,
u(S, M) = 0, u(X, M) = 0, u(TM, M) = 0, u(N, M) = +1/4, u(N2, M) = -1/4, u(C, M) = +1/2, u(GN, M) = +1/8, u(GC, M) = +1/4,
u(M, M) = 0.

Facts the table fixes:

* The ten programs fall into the classes {R}, {P}, {S}, {X}, {TM}, {N, C}, {N2}, {GN, GC}; with M added, N and C separate
  and GN and GC separate. X is behaviourally distinct from every guarded reader (they beat constants), and a payoff row
  of zeros is shared by no other program of the ten.
* Self-play forfeit probability at D = 12: TM, N, N2, C = 1; GN, GC = 2^-13 = 1.22e-4; R, P, S, X, M = 0.
* Against X every non-forfeiting program earns exactly 0 (statics, prediction 1).
* The simulating counter earns the *variance* 1/2 sum (d_i - d_j)^2 against a mixed opponent, the exact counter earns
  max_a (u(a, d)): they agree against the constants and against uniform, and differ against every other mixture.

### 1.4 Hand predictions for the ten-program toy ecology (the toy table is also the validation of the solver on a
two-type contest)

Toy chain: the 10 classes above plus M (11 classes), mutation prior uniform over the 11 classes, w = 0.3, the ε -> 0
chain by the published lumped-resident fixation (the same solver the counted cells use), D = 12.

* No monomorphic constant is stable (each is invaded by the next constant, by N, C, GN, GC, or by the program that
  beats it): the constants only appear transiently. The three-constant polymorphism is a replicator centre (conserved
  product) so it is reported as indeterminate, not forced.
* N (equivalently C) monomorphic is invaded only by the guarded readers, with advantage +e = 1/128 against it
  (selection w * e = 0.0023 per unit payoff gap); the other pure readers and X are neutral to it. N and C monomorphic
  are not stable; GN/GC monomorphic are neutral to each other and to X, and the pure readers invade them at fitness
  disadvantage -e only.
* Therefore at N = 10^4 (N * w * e = 23, selection strong) the support of the toy chain's pi lies on {GN, GC, X} (the
  neutral set of the three programs whose payoffs against each other are all 0 and which beat or tie everything else),
  with pi mass >= 0.8; at N = 100 (N * w * e = 0.23, near neutral) the pure readers are not removed and pi is spread
  over the guarded readers, X and the pure readers, with the {GN, GC, X} share below 0.8. The size of the effect
  (1/128) comes from the depth cap only: at D = 11 and D = 13 the pure and guarded readers tie exactly, at D = 20 the
  gap is 1/2048. The toy chain is therefore also rerun at D = 11, 13, 20: at D = 11, 13 the {GN, GC, X} neutral set loses
  its protection from the pure readers (the readers become exactly neutral to it), so the {GN, GC, X} share at
  N = 10^4 falls below its D = 12 value; this is a statement about the cap, not about the game.
