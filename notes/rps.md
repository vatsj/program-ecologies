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

## 2. Choices where the spec is silent, and deviations (written with the code, before any counted cell)

*Disclosure.* Development runs of the chain and of single lottery runs (exact arm, N = 100 and 10^3 .. 10^5; one lottery
run) were looked at while debugging the code; their output files were deleted or overwritten by the counted cells. They
showed the structure of the chain (below) but no prediction, scoring rule or cell was changed afterwards; the
predictions file was committed before any code existed.

1. **Prior.** mu(p) = 2^-bits with bits = log2 a(|p|) + 2 log2 |p| + 1 (the weak arm's length prior, uniform inside a length
   class), normalised over the n = 6 table. The spec says "2^-nodes over spellings"; IMPLEMENTATION 2 forbids 2^-nodes
   ("Bits, not nodes. For mu. Every time.") because it is improper for this grammar (the sum over spellings diverges). The
   spec's text is read as the repo's convention; 2^-nodes (normalised at n = 6) is run as a labelled chain sensitivity.
2. **Programs and stripping.** A program is its body, hash-consed (a syntactic spelling is one expression id; no behavioural
   dedup at enumeration). The weak arm's stripping: application is always `THEM(Q)`, Q in {ME, THEM, up(B)}; `ME(..)` and
   `(up A)(..)` are not enumerated. Size: `THEM(ME)` and `THEM(THEM)` are 3 nodes, `THEM(^B)` is 3 + |B| nodes (the `up` is a
   node), unary and `coin` one node plus children. The exact grammar has 4, 8, 34, 136, 616, 2,898 expressions at 1..6
   nodes (3,696), sample 1,258, pure 46, matched 3,696 (checked in tests).
3. **Evaluator.** G_d(a, b) is the (R, P, S, F) distribution of a's action against b with d application levels left; an
   application at d = 0 forfeits (uniform in exact-uniform). `coin` evaluates both branches exactly and mixes them 1/2;
   `cr` reads the conditional distribution given acting, ties within 1e-9 are broken uniformly, forfeit mass propagates
   (cr forfeits with the forfeit mass of its argument; surely if that is 1). exact-br: the genuine best response is the
   best response to the conditional distribution (forfeit adds the same +1 to every action, so it cannot change the argmax)
   and never forfeits; against certain forfeit every action ties and it plays uniform. D = 12 in the main cells; each other
   cap (11, 13, 20) is a separate evaluation of the full table.
4. **Classes.** Programs with identical rows and columns of the payoff table (rounded to 6 decimals; 5 decimals gives the same
   count in every arm) form a class; the class mass is the sum of the members' mu; the representative is the smallest
   (size, id). Statistics that use action distributions take the representative's. The audit (static.json) found one class
   whose members differ from the representative in action distribution: the class of `X` also contains the single program
   `THEM(^THEM(THEM))`, which forfeits against the pure readers (as the readers forfeit against it, payoff 0) and is
   payoff-identical to X on the 3,696-program table. Reported, not corrected (the spec asks for payoff classes).
5. **Chain.** `LogChain` with a class-level provider (`rps.ClassProvider`), exploration by `explore_log` seeded with
   every stable polymorphic candidate found by `solver_audit.enumerate_candidates_fast` and `invasion_closure`
   (max 6,000 nodes), theta_log = 1e-14 (1e-12 and 1e-16 sensitivities are exact copies when the explored set is the full
   monomorphic closure, reported as such), twin-expanded and lumped. States, statistics and transition structure follow
   `solver_audit`/`fixed_role_chicken.onepop_chain`. In this antisymmetric game a single mutant meets a monomorphic
   resident in a two-type contest, which has no interior attractor, so every state of the chain is monomorphic in the cells
   run; this is a result of the cells, not a design choice, and the indeterminate (three-type cycle) count is reported.
   N = 10^5 is added to the spec's N set to show the trend (spec: 10^2, 10^3, 10^4).
6. **Lottery.** `rps.lottery_kernel` is the kernel of `islands.py` (complete graph, replacement by the offspring of a parent
   drawn with probability proportional to count * exp(w * mean payoff against the other N - 1), from the same island or
   with probability m = mN/N from a uniformly chosen other island), without the freeze test (equal-payoff survivors still
   drift in composition, which the statistics read). A generation is I*N events. Founders: each slot draws a size (length
   prior) and a uniform position inside that size class in the canonical enumeration order; the same uniforms are used by
   every arm (common random numbers), and exact and sample-matched share their enumeration order spelling for spelling
   (`cr` <-> `next2`), so they are paired exactly; pure and sample are paired only through the sizes and quantiles. The
   dynamics seed is per arm. Runs 0-9 of the primary cell continue to 10,000 generations with the same random stream (the
   state at 2,000 is the primary run's); checkpoints at 100, 250, 500, 1,000, 1,500, 2,000 (5,000 and 10,000 for the
   continuation). Window statistics (classes alive, homozygosity) are sampled every 10 generations over 1,500-2,000.
7. **Statistics.** In-population program exploitability e(x) = max_k (U x)_k over the arm's classes; action exploitability
   with forfeit counted as a win for the constant, and the version conditional on non-forfeit plays; individual mixing =
   total variation distance to (1/3, 1/3, 1/3, 0) at most 0.05 of the (R, P, S, F) distribution, against a random
   population member (mix_pop) and against itself (mix_self); tv_marg = TV of the population's play marginal from uniform
   (reading (M)); self-play forfeit = sum x_a P(a forfeits against a); plays forfeit = forfeit share of the population's
   marginal. Run-clustered intervals: bootstrap over runs (4,000 resamples) of the run means; paired differences over runs.
8. **Toy chain.** The eleven programs R, P, S, X, THEM(ME), next(THEM(ME)), next(next(THEM(ME))), cr(THEM(ME)),
   coin(X, next(THEM(ME))), coin(X, cr(THEM(ME))), coin(R, P) as eleven classes with a uniform mutation prior, payoffs from
   the full-table evaluation at the stated D (an eleven-row sub-table of the exact arm), N = 100, 1,000, 10,000.
9. **Memory.** One arm build (full 3,696 x 3,696 x 4 float64 table, two buffers) peaks at 1.3 GB RSS; the static job with the
   three extra caps peaks at 2.3 GB; chain and lottery jobs load the cached class table and peak below 0.3 GB. At most 3
   processes at a time, one job per process, no pools.
10. **Not done at the time of writing:** n = 7 (the full table would be 17,888 programs, 10 GB per buffer; decided after the
    n = 6 cells, see below if added).
11. **Added after the first counted cells (disclosed; no prediction, convention or cell of the spec was changed).** (a) The
    first counted chains showed the exact arm more exploitable than the matched arm; since in-population program
    exploitability is a maximum over each arm's own grammar, a control with the exploiter set held fixed (the best any class
    of the exact grammar earns against the arm's population, representatives re-spelled with `next2` read as `next`) was added
    as `e_exset` (chain: recomputed for all chain cells; lottery: computed offline from the stored compositions at
    generation 2,000). The primary statistic (`e_prog`, own grammar) is the one the conventions score. (b) N = 10^5 and 10^6
    chains, to see the approach to the N -> infinity limit; the closed-form limit pi_inf(c) = mu(c)/mu(Z0) on the unexploitable
    classes Z0 follows from the neutral-entrant argument (pi(X) = mu(X) exactly) and is reported beside the finite-N cells.
    (c) A 200-run independent replicate of the primary lottery cell (pure, sample, matched, exact), because 40 runs cannot
    resolve the exact-minus-matched difference. (d) n = 7 (src/rps_n7.py, blocked evaluation; the class table is exact, 17,888
    programs in the exact grammar, K = 376 classes), chains at N = 10^2..10^5 and the primary lottery in the four arms. (e) The
    report script `src/rps_report.py` was written after the counted cells (the spec lists it with the code); it only reads
    the stored cells.
