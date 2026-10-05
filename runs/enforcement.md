# Incentive-compatible enforcement in the union game, and the unfakeable-polarity pact (spec `specs/2026-10-05-enforcement.md`; predictions `predictions/2026-10-05-enforcement.md`, commit 38793e4, Part A addendum a4120fe)

Code: `src/union_enforcement.py` (override inside the per-world evaluator, boxes on implemented actions, replacement
pool, history-based independent evaluator for the box audit, Part A, reduced chain), `src/union_enforcement_run.py`
(runner, full-language audit, full-chain cells, report). Tests `tests/test_union_enforcement.py`, all pass: the CC
arm reproduces the union run's tensor and its static and reduced-chain tables exactly (c = 0, 0.1, 0.5; every
N); tie-breaking (indifference → recommendation); the boundary 1 − s = c both ways; pool payoffs; box audit over
156,864 encounters (every boss function × the four named workers in all 32 arm/pool/c/tie settings, plus 4,800
random full-language triples), 0 violations of: stable play = evaluator, box monotonicity, Lemma 0 at the stable
world, and a rational slot best-responding at the stable world. Raw output in `runs/enforcement/*.json`, collected
in `runs/enforcement.json`.

## What ran

- **Part A** (static, committed play): the six militant⁻/union⁻ variants (wage check BOX or BOX1, handshake BOX or
  BOX1) against every boss function at n = 6 with box levels {0, 1} (585 functions) and with level 0 only (297), all
  36 ordered pairs, world-by-world traces for nine named bosses. No chain run (the tables agree with the spec's
  derivation).
- **Part B** (reduced canonical chain, boss over the 9 constants, workers over scab/militant/union, exact dense
  log-GTH): 4 commitment arms × pool × c ∈ {0.1, 0.5} × N ∈ {10², 10³, 10⁴} × tie ∈ {whack, nowhack} × prior ∈
  {uniform, length}: 192 cells (N = 10⁴ added after the predictions as a scaling check). Masses frozen at the
  union run's class masses (boss constants 0.108 each; scab 0.480, militant 1.2·10⁻³, union 9.9·10⁻⁶).
- **Full-language tensors** in every (arm, pool, c, tie): 60,678,288 encounters each, all stabilize.
- **Part C** (full chain, length prior, c = 0.5, N = 10³): the specified RC-with-pool cell (θ = 10⁻¹¹; θ = 10⁻⁹
  and tie = nowhack as robustness), plus additions beyond the spec, each 15–60 s: CC with pool (matched control),
  CC without pool (reproduces the union run's cell to every printed digit), and RC, CR, RR without pool (RR also at
  N = 10² and 10⁴). Class counts change with the arm (the override merges programs); class masses are sums of the
  frozen function masses.
- Not run: the tie reading "boundary → recommendation" (needs a fourth whack policy for source targeting; the
  boundary is off-path in the reduced chain anyway, S5); Part A chain cells (not triggered).

## Part A: the unfakeable-polarity pact (reading)

- **union⁻₀** (`and(not(BOX(s = 1/2)), BOX(OTHER = strike))`) never strikes, against any of the 585 bosses, with
  either wage level: at world 0 every box is true, so ¬□fair is false, both work, and □(other strikes) is false
  from world 1 on.
- **union⁻₁** (level-1 handshake, PA wage check) strikes **iff the boss pays low at world 0** (390/390 such bosses
  struck, 0/195 world-0-fair bosses struck), whatever the boss pays later. So it is defeated by 72 faker classes
  (mass 0.003) that pay fair at world 0 and low at the stable world (`if(BOX(W1 = strike), (1/2,·), (0,·))`: fair
  while the workers are provably striking, which is vacuously true at world 0 only; the level-1 version
  `if(BOX1(W1 = strike), …)` is fair through world 1 and fakes it too), and it strikes 108 bosses that are fair at
  the stable world but paid low at world 0 (mass 0.0045): the pact's own self-harm.
- **The BOX1 wage-check twins never strike** (¬□₁fair is false at worlds 0 and 1, so the level-1 handshake fails
  at world 2): pushing the wage check up a level breaks activation exactly as the spec's regress says.
- **militant⁻** (`not(BOX(s = 1/2))`, a lone worker) is unfakeable: 0 bosses pay low at the stable world while it
  works; 0 Lemma 0 counterexamples in 21,060 + 10,692 encounters. Its error is self-harm only: 108 fair bosses struck
  (mass 0.0045; 0.006 in the level-0 boss language).
- The union run's wage faker (`if(BOX(W1 = work), (1/2,·), (0,·))`) pays fair forever to every militant⁻ and
  union⁻ pair. The faker of the unfakeable polarity's *handshake* is its mirror: "pay fair only while provably
  struck".
- Mixed pairs: union⁻₁ beside militant⁻ strikes only when militant⁻ struck from world 1 (boss low at world 0);
  otherwise a scab split. No pair strikes against every low-paying class.

## Part B and C: reading

**The four arms (reduced chain, uniform prior, c = 0.5, N = 10³; N = 10², 10⁴ within 0.03 everywhere):**

| arm | fair | intermediate | zero wage | boss | worker | efficiency |
|---|---|---|---|---|---|---|
| CC (union run) | 0.306 | 0.001 | 0.598 | 1.60 | 0.153 | 1.90 |
| RC (boss's whack ex-post rational) | **0.553** | 0.002 | 0.331 | 1.33 | 0.277 | 1.88 |
| CR (workers ex-post rational) | 7·10⁻⁵ | 0.001 | **0.998** | 2.00 | 4·10⁻⁴ | 2.00 |
| RR (both) | 0.001 | **0.668** | 0.327 | 1.66 | 0.168 | 2.00 |
| CC + pool | 0.031 | 3·10⁻⁴ | 0.963 | 1.96 | 0.015 | 1.99 |
| RC + pool | 10⁻¹³⁰ | 10⁻⁶⁶ | 1.000 | 2.00 | 0 | 2.00 |
| CR + pool | 6·10⁻⁵ | 0.001 | 0.998 | 2.00 | 4·10⁻⁴ | 2.00 |
| RR + pool | 10⁻¹³⁰ | 10⁻⁶⁶ | 1.000 | 2.00 | 0 | 2.00 |

1. **The workers' commitment is necessary for any positive wage** (CR: π on `(0, strike)` bosses 0.952; rational
   workers never strike into a committed strike-targeting boss, so the threat is never executed, realized
   repression 8·10⁻⁶, and it holds whether or not the threat would pay if called: value −0.50 without the pool,
   +0.50 with it, same π).
2. **The boss's commitment suppresses the fair share, and its threat is not credible.** In CC, 0.53 of π sits on
   committed strike-targeting bosses whose threat is never triggered and would cost −c if called. It works by
   making the militant's entry at zero wage deleterious (`(0,strike) scab scab`: militant −1), whereas in RC every
   zero-wage boss admits the militant neutrally. Removing it raises fair from 0.306 to 0.553 (limit fractions
   5/9 fair, 1/3 zero, 1/9 scab split at N = 10⁴). A non-credible threat deters in the ε→0 chain because the
   chain never tests it: entry is evaluated against the committed policy.
3. **With both sides rational the boss pays the smallest positive wage** (RR: intermediate 0.668 → 2/3 at
   N = 10⁴, fair 0.001): a rational strike is credible only where it is free (s = 0, a tie resolved by the
   recommendation), so against any refuser the boss's best wage is 1/4, where every rational worker works. The
   ultimatum game's subgame-perfect lesson, reproduced by stochastic stability.
4. **The pool makes repression credible and kills the wage** in every arm: CC fair 0.306 → 0.031 (c = 0.1:
   0.324 → 0.0005), RC 0.553 → 0, RR 0.668 intermediate → 0. Repression conditional on a strike rises (CC 6·10⁻⁷ →
   0.12; RC 0 → 1) while strike incidence falls (0.095 → 0.006; 0.114 → 10⁻¹³⁰). With rational whacking and the
   pool (c = 0.5) every boss whacks strikers at every wage (s = 1/2 at the declared tie), the militant's zero-wage
   entry is deleterious, and {(0, ·)} × {scab, union}² (minus the union pair) is a closed neutral network left only
   by deleterious steps (10⁻⁶⁷ per event at N = 10³).
5. **Under the length prior every reduced cell has zero wage ≥ 0.994** (the restricted prior gives the militant
   0.0025 of the worker mass and omits the constant striker).
6. **The full chain overturns (5) for RR** (additions beyond the spec, length prior, c = 0.5): RR gives
   intermediate 0.754 / 0.753 / 0.752 at N = 10² / 10³ / 10⁴, worker payoff 0.19 (union run: 0.005), boss 1.62
   (union run 1.36), efficiency 1.995 (1.37): **RR Pareto-dominates the union run's committed game under the length
   prior.** Mechanism: the constant striker (mass 0.48), which in CC strikes at every wage and wastes the product,
   becomes under ex-post rationality a free refuser at s = 0 and a worker at s ≥ 1/4; the boss raises to 1/4
   strictly whenever one worker slot holds it, and cuts back to 0 strictly only when both slots have drifted to
   work-at-zero programs (≈ 1/4 of the time: zero wage 0.24). The support is `(1/4, ·) | strike | strike` 0.233,
   `(1/4, ·) | work | strike` 0.230 ×2, `(0, ·) | work | work` 0.223; exits are neutral drift ∝ 1/N; the circulation
   is zero → scab split → intermediate → zero (net 8·10⁻⁵ per event). The other full cells: CR zero wage 0.998;
   RC (no pool) fair 0.005, zero 0.33, strike + split 0.65, efficiency 1.20 (the boss's deterrent gone, the heavy
   striker wastes more); CC + pool zero 0.986; RC + pool zero 0.9997.
7. **Part C** (RC + pool, the specified cell): zero wage 0.9997, fair 1.3·10⁻⁵, strike + scab split 0, repression
   conditional on a strike 1.000 (tie = whack; 0.58 with tie = nowhack, the boundary being on path through the
   constant striker at s = 1/2), worker payoff 9·10⁻⁵, efficiency 2.000; support `(0, strike) | work | work` 0.923
   plus worker conditionals that read the whack policy; exits neutral-keep only. Stable to θ (10⁻⁹: 610 states,
   cut 5%; 10⁻¹¹: 4,320 states, cut 0.5%; π equal to 10⁻⁵).
8. **No commitment structure gives equal division under either prior beyond CC/RC's uniform-prior values**; the
   best worker outcome is RC under the uniform prior (fair 0.553) and RR under the length prior (intermediate
   0.75). Efficiency and equal division come apart again: the most efficient cells (CR, any pool) pay the workers
   nothing.

## Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | no polarity carries a pact against every low-paying boss | **Held**: union⁻₀ never strikes; union⁻₁ strikes every constant low boss and works for the bottom-world faker (72 classes, μ 0.003); 0 Lemma 0 counterexamples; militant⁻ self-harm μ 0.0045 < 0.05; no variant strikes against every low-paying class |
| RE 2 | workers' commitment carries the fair share, the boss's does not; CR, RR fair ≤ 0.05 and zero ≥ 0.8; RC within 0.05 of CC | **Failed, falsifier fired**: RC − CC = +0.247 on fair (≥ 0.15). CR clause held (fair 7·10⁻⁵, zero 0.998); RR zero wage 0.327 < 0.8 (intermediate 0.668) |
| RE 3 | the pool lowers fair by ≥ 0.1 in CC and RC; RC + pool within 0.05 of CC + pool; repression \| strike up, incidence down | **Held** (c = 0.5: −0.275, −0.553, gap 0.031; c = 0.1: −0.323, −0.553, gap 0.0005) |
| RE 4 | length prior: every (Part B) cell zero wage ≥ 0.95 | **Held** in Part B (min 0.994); the full-chain RR cell (not a Part B cell) has zero wage 0.24 and intermediate 0.75 |
| RE 5 | Part C: repression \| strike ≥ 0.5, fair ≤ 0.01 | **Held** (1.000; 0.58 with tie = nowhack; fair 1.3·10⁻⁵) |
| S1 | rational strikes only at s = 0; CR, RR fair ≤ 0.01 | **Held** (0 strikes at s > 0 in every CR/RR full tensor; fair ≤ 0.0013) |
| S2 | RR no pool: intermediate ≥ 0.3, zero < 0.8 | **Held** (0.668, 0.327) |
| S3 | CR: (0, strike) states ≥ 0.5, realized repression ≤ 0.01 | **Held** (0.952, 8·10⁻⁶) |
| S4 | RC + pool fair ≤ 0.01 and CC + pool fair ≥ 0.05 | **Failed, falsifier fired**: CC + pool fair 0.031 (0.059 at N = 10², 0.027 at N = 10⁴); the RC clause held (10⁻¹³⁰) |
| S5 | tie rule off-path in the reduced chain | **Held** (max difference 0 in all 96 pairs) |
| S6 | length prior Part B: fair ≤ 0.01, intermediate ≤ 0.05 | **Held** (max 0.0011, 0.005) |
| S7 | Part C: zero ≥ 0.9, strike + split ≤ 0.05, rep \| strike = 1, worker ≤ 0.01, efficiency ≥ 1.85 | **Held** (0.9997, 0, 1.000, 9·10⁻⁵, 2.000) |
| S8 | only union⁻(PA wage, BOX1 handshake) self-pairs strike, iff s(world 0) low | **Held** (390/390, 0/195; all other union⁻ self-pairs 0) |

## Tables (generated by `python3 src/union_enforcement_run.py report`)

### Part A, boss language levels_01 (585 functions; constants 0.976 of μ)

Audit: 21060 encounters, 0 violations, 0 Lemma 0 counterexamples.

| self-pair | strikes, s(w0) low | works, s(w0) low | strikes, s(w0) fair | works, s(w0) fair |
|---|---|---|---|---|
| militant- | 390 | 0 | 72 | 123 |
| union-0 | 0 | 390 | 0 | 195 |
| union-1 | 390 | 0 | 0 | 195 |
| militant-[BOX1 wage] | 354 | 36 | 72 | 123 |
| union-0 [BOX1 wage] | 0 | 390 | 0 | 195 |
| union-1 [BOX1 wage] | 0 | 390 | 0 | 195 |

| pair (W1 \| W2) | low, struck | low, worked (of which fakers: fair at w0) | fair, worked | fair, struck (self-harm) |
|---|---|---|---|---|
| militant- \| militant- | 354 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 108 (0.0045) |
| militant- \| union-0 | 372 (0.6659) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 90 (0.0038) |
| militant- \| union-1 | 354 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 108 (0.0045) |
| militant- \| militant-[BOX1 wage] | 336 (0.6644) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 126 (0.0053) |
| militant- \| union-0 [BOX1 wage] | 372 (0.6659) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 90 (0.0038) |
| militant- \| union-1 [BOX1 wage] | 336 (0.6644) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 126 (0.0053) |
| union-0 \| militant- | 372 (0.6659) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 90 (0.0038) |
| union-0 \| union-0 | 0 (0.0000) | 390 (0.6667); fakers 72 (0.0030) | 195 (0.3333) | 0 (0.0000) |
| union-0 \| union-1 | 0 (0.0000) | 354 (0.6652); fakers 72 (0.0030) | 231 (0.3348) | 0 (0.0000) |
| union-0 \| militant-[BOX1 wage] | 354 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 159 (0.3318) | 72 (0.0030) |
| union-0 \| union-0 [BOX1 wage] | 0 (0.0000) | 390 (0.6667); fakers 72 (0.0030) | 195 (0.3333) | 0 (0.0000) |
| union-0 \| union-1 [BOX1 wage] | 0 (0.0000) | 390 (0.6667); fakers 72 (0.0030) | 195 (0.3333) | 0 (0.0000) |
| union-1 \| militant- | 354 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 108 (0.0045) |
| union-1 \| union-0 | 0 (0.0000) | 354 (0.6652); fakers 72 (0.0030) | 231 (0.3348) | 0 (0.0000) |
| union-1 \| union-1 | 282 (0.6622) | 72 (0.0030); fakers 72 (0.0030) | 123 (0.3303) | 108 (0.0045) |
| union-1 \| militant-[BOX1 wage] | 318 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 159 (0.3318) | 108 (0.0045) |
| union-1 \| union-0 [BOX1 wage] | 0 (0.0000) | 354 (0.6652); fakers 72 (0.0030) | 231 (0.3348) | 0 (0.0000) |
| union-1 \| union-1 [BOX1 wage] | 0 (0.0000) | 318 (0.6637); fakers 72 (0.0030) | 267 (0.3363) | 0 (0.0000) |
| militant-[BOX1 wage] \| militant- | 336 (0.6644) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 126 (0.0053) |
| militant-[BOX1 wage] \| union-0 | 354 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 159 (0.3318) | 72 (0.0030) |
| militant-[BOX1 wage] \| union-1 | 318 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 159 (0.3318) | 108 (0.0045) |
| militant-[BOX1 wage] \| militant-[BOX1 wage] | 318 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 159 (0.3318) | 108 (0.0045) |
| militant-[BOX1 wage] \| union-0 [BOX1 wage] | 354 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 159 (0.3318) | 72 (0.0030) |
| militant-[BOX1 wage] \| union-1 [BOX1 wage] | 354 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 159 (0.3318) | 72 (0.0030) |
| union-0 [BOX1 wage] \| militant- | 372 (0.6659) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 90 (0.0038) |
| union-0 [BOX1 wage] \| union-0 | 0 (0.0000) | 390 (0.6667); fakers 72 (0.0030) | 195 (0.3333) | 0 (0.0000) |
| union-0 [BOX1 wage] \| union-1 | 0 (0.0000) | 354 (0.6652); fakers 72 (0.0030) | 231 (0.3348) | 0 (0.0000) |
| union-0 [BOX1 wage] \| militant-[BOX1 wage] | 354 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 159 (0.3318) | 72 (0.0030) |
| union-0 [BOX1 wage] \| union-0 [BOX1 wage] | 0 (0.0000) | 390 (0.6667); fakers 72 (0.0030) | 195 (0.3333) | 0 (0.0000) |
| union-0 [BOX1 wage] \| union-1 [BOX1 wage] | 0 (0.0000) | 390 (0.6667); fakers 72 (0.0030) | 195 (0.3333) | 0 (0.0000) |
| union-1 [BOX1 wage] \| militant- | 336 (0.6644) | 0 (0.0000); fakers 0 (0.0000) | 123 (0.3303) | 126 (0.0053) |
| union-1 [BOX1 wage] \| union-0 | 0 (0.0000) | 390 (0.6667); fakers 72 (0.0030) | 195 (0.3333) | 0 (0.0000) |
| union-1 [BOX1 wage] \| union-1 | 0 (0.0000) | 318 (0.6637); fakers 72 (0.0030) | 267 (0.3363) | 0 (0.0000) |
| union-1 [BOX1 wage] \| militant-[BOX1 wage] | 354 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 159 (0.3318) | 72 (0.0030) |
| union-1 [BOX1 wage] \| union-0 [BOX1 wage] | 0 (0.0000) | 390 (0.6667); fakers 72 (0.0030) | 195 (0.3333) | 0 (0.0000) |
| union-1 [BOX1 wage] \| union-1 [BOX1 wage] | 0 (0.0000) | 390 (0.6667); fakers 72 (0.0030) | 195 (0.3333) | 0 (0.0000) |

### Part A, boss language levels_0 (297 functions; constants 0.976 of μ)

Audit: 10692 encounters, 0 violations, 0 Lemma 0 counterexamples.

| self-pair | strikes, s(w0) low | works, s(w0) low | strikes, s(w0) fair | works, s(w0) fair |
|---|---|---|---|---|
| militant- | 198 | 0 | 36 | 63 |
| union-0 | 0 | 198 | 0 | 99 |
| union-1 | 198 | 0 | 0 | 99 |
| militant-[BOX1 wage] | 162 | 36 | 36 | 63 |
| union-0 [BOX1 wage] | 0 | 198 | 0 | 99 |
| union-1 [BOX1 wage] | 0 | 198 | 0 | 99 |

| pair (W1 \| W2) | low, struck | low, worked (of which fakers: fair at w0) | fair, worked | fair, struck (self-harm) |
|---|---|---|---|---|
| militant- \| militant- | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 72 (0.0060) |
| militant- \| union-0 | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 54 (0.0045) |
| militant- \| union-1 | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 72 (0.0060) |
| militant- \| militant-[BOX1 wage] | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 72 (0.0060) |
| militant- \| union-0 [BOX1 wage] | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 54 (0.0045) |
| militant- \| union-1 [BOX1 wage] | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 72 (0.0060) |
| union-0 \| militant- | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 54 (0.0045) |
| union-0 \| union-0 | 0 (0.0000) | 198 (0.6667); fakers 36 (0.0030) | 99 (0.3333) | 0 (0.0000) |
| union-0 \| union-1 | 0 (0.0000) | 180 (0.6652); fakers 36 (0.0030) | 117 (0.3348) | 0 (0.0000) |
| union-0 \| militant-[BOX1 wage] | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 99 (0.3333) | 18 (0.0015) |
| union-0 \| union-0 [BOX1 wage] | 0 (0.0000) | 198 (0.6667); fakers 36 (0.0030) | 99 (0.3333) | 0 (0.0000) |
| union-0 \| union-1 [BOX1 wage] | 0 (0.0000) | 198 (0.6667); fakers 36 (0.0030) | 99 (0.3333) | 0 (0.0000) |
| union-1 \| militant- | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 72 (0.0060) |
| union-1 \| union-0 | 0 (0.0000) | 180 (0.6652); fakers 36 (0.0030) | 117 (0.3348) | 0 (0.0000) |
| union-1 \| union-1 | 126 (0.6607) | 36 (0.0030); fakers 36 (0.0030) | 63 (0.3303) | 72 (0.0060) |
| union-1 \| militant-[BOX1 wage] | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 99 (0.3333) | 36 (0.0030) |
| union-1 \| union-0 [BOX1 wage] | 0 (0.0000) | 180 (0.6652); fakers 36 (0.0030) | 117 (0.3348) | 0 (0.0000) |
| union-1 \| union-1 [BOX1 wage] | 0 (0.0000) | 162 (0.6637); fakers 36 (0.0030) | 135 (0.3363) | 0 (0.0000) |
| militant-[BOX1 wage] \| militant- | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 72 (0.0060) |
| militant-[BOX1 wage] \| union-0 | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 99 (0.3333) | 18 (0.0015) |
| militant-[BOX1 wage] \| union-1 | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 99 (0.3333) | 36 (0.0030) |
| militant-[BOX1 wage] \| militant-[BOX1 wage] | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 99 (0.3333) | 36 (0.0030) |
| militant-[BOX1 wage] \| union-0 [BOX1 wage] | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 99 (0.3333) | 18 (0.0015) |
| militant-[BOX1 wage] \| union-1 [BOX1 wage] | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 99 (0.3333) | 18 (0.0015) |
| union-0 [BOX1 wage] \| militant- | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 54 (0.0045) |
| union-0 [BOX1 wage] \| union-0 | 0 (0.0000) | 198 (0.6667); fakers 36 (0.0030) | 99 (0.3333) | 0 (0.0000) |
| union-0 [BOX1 wage] \| union-1 | 0 (0.0000) | 180 (0.6652); fakers 36 (0.0030) | 117 (0.3348) | 0 (0.0000) |
| union-0 [BOX1 wage] \| militant-[BOX1 wage] | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 99 (0.3333) | 18 (0.0015) |
| union-0 [BOX1 wage] \| union-0 [BOX1 wage] | 0 (0.0000) | 198 (0.6667); fakers 36 (0.0030) | 99 (0.3333) | 0 (0.0000) |
| union-0 [BOX1 wage] \| union-1 [BOX1 wage] | 0 (0.0000) | 198 (0.6667); fakers 36 (0.0030) | 99 (0.3333) | 0 (0.0000) |
| union-1 [BOX1 wage] \| militant- | 162 (0.6637) | 0 (0.0000); fakers 0 (0.0000) | 63 (0.3303) | 72 (0.0060) |
| union-1 [BOX1 wage] \| union-0 | 0 (0.0000) | 198 (0.6667); fakers 36 (0.0030) | 99 (0.3333) | 0 (0.0000) |
| union-1 [BOX1 wage] \| union-1 | 0 (0.0000) | 162 (0.6637); fakers 36 (0.0030) | 135 (0.3363) | 0 (0.0000) |
| union-1 [BOX1 wage] \| militant-[BOX1 wage] | 180 (0.6652) | 0 (0.0000); fakers 0 (0.0000) | 99 (0.3333) | 18 (0.0015) |
| union-1 [BOX1 wage] \| union-0 [BOX1 wage] | 0 (0.0000) | 198 (0.6667); fakers 36 (0.0030) | 99 (0.3333) | 0 (0.0000) |
| union-1 [BOX1 wage] \| union-1 [BOX1 wage] | 0 (0.0000) | 198 (0.6667); fakers 36 (0.0030) | 99 (0.3333) | 0 (0.0000) |

### Part A traces (levels {0,1}; committed play)

- `(0,none) || militant- | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=0 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=0 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
- `(0,none) || union-0 | union-0`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
- `(0,none) || union-1 | union-1`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
- `(0,none) || union-0 [BOX1 wage] | union-0 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(OTHER=strike)=T, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `(0,none) || union-1 [BOX1 wage] | union-1 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `(0,none) || militant-[BOX1 wage] | militant-[BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=0 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
- `(0,none) || union-1 | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w2: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w3: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
- `(0,none) || union-0 | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
- `(0,none) || union-1 | union-1 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `(0,none) || union-1 | union-0 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `(1/4,none) || militant- | militant-`
  - `w0: s=1/4 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/4 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=1/4 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=1/4 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
- `(1/4,none) || union-0 | union-0`
  - `w0: s=1/4 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=T]`
  - `w1: s=1/4 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w2: s=1/4 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w3: s=1/4 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
- `(1/4,none) || union-1 | union-1`
  - `w0: s=1/4 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/4 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/4 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=1/4 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
- `(1/4,none) || union-0 [BOX1 wage] | union-0 [BOX1 wage]`
  - `w0: s=1/4 WW  [W1:BOX(OTHER=strike)=T, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/4 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/4 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=1/4 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `(1/4,none) || union-1 [BOX1 wage] | union-1 [BOX1 wage]`
  - `w0: s=1/4 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/4 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/4 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=1/4 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `(1/4,none) || militant-[BOX1 wage] | militant-[BOX1 wage]`
  - `w0: s=1/4 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/4 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/4 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=1/4 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
- `(1/4,none) || union-1 | militant-`
  - `w0: s=1/4 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/4 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w2: s=1/4 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w3: s=1/4 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
- `(1/4,none) || union-0 | militant-`
  - `w0: s=1/4 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/4 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=1/4 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=1/4 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
- `(1/4,none) || union-1 | union-1 [BOX1 wage]`
  - `w0: s=1/4 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/4 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/4 WS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=1/4 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `(1/4,none) || union-1 | union-0 [BOX1 wage]`
  - `w0: s=1/4 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/4 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/4 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=1/4 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `(1/2,none) || militant- | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
- `(1/2,none) || union-0 | union-0`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=F]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=F]`
- `(1/2,none) || union-1 | union-1`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
- `(1/2,none) || union-0 [BOX1 wage] | union-0 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(OTHER=strike)=T, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
- `(1/2,none) || union-1 [BOX1 wage] | union-1 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
- `(1/2,none) || militant-[BOX1 wage] | militant-[BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
- `(1/2,none) || union-1 | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
- `(1/2,none) || union-0 | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
- `(1/2,none) || union-1 | union-1 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
- `(1/2,none) || union-1 | union-0 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || militant- | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || union-0 | union-0`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=F]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=F]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || union-1 | union-1`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || union-0 [BOX1 wage] | union-0 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(OTHER=strike)=T, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || union-1 [BOX1 wage] | union-1 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || militant-[BOX1 wage] | militant-[BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || union-1 | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || union-0 | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || union-1 | union-1 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
- `union-run faker if(BOX(W1=work),(1/2,none),(0,none)) || union-1 | union-0 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || militant- | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w2: s=0 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=0 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || union-0 | union-0`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=F]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || union-1 | union-1`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || union-0 [BOX1 wage] | union-0 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(OTHER=strike)=T, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || union-1 [BOX1 wage] | union-1 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || militant-[BOX1 wage] | militant-[BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=0 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || union-1 | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w2: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || union-0 | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w2: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || union-1 | union-1 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `bottom-world faker if(BOX(W1=strike),(1/2,none),(0,none)) || union-1 | union-0 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || militant- | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w3: s=0 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || union-0 | union-0`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=F]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || union-1 | union-1`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || union-0 [BOX1 wage] | union-0 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(OTHER=strike)=T, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w3: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || union-1 [BOX1 wage] | union-1 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || militant-[BOX1 wage] | militant-[BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w3: s=0 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || union-1 | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w3: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || union-0 | militant-`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=T]`
  - `w3: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || union-1 | union-1 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `level-1 faker if(BOX1(W1=strike),(1/2,none),(0,none)) || union-1 | union-0 [BOX1 wage]`
  - `w0: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || militant- | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=1/2 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=1/2 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || union-0 | union-0`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || union-1 | union-1`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || union-0 [BOX1 wage] | union-0 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(OTHER=strike)=T, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || union-1 [BOX1 wage] | union-1 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || militant-[BOX1 wage] | militant-[BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=1/2 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || union-1 | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w2: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w3: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || union-0 | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || union-1 | union-1 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `low-then-fair if(BOX(W1=work),(0,none),(1/2,none)) || union-1 | union-0 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || militant- | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=1/2 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=1/2 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || union-0 | union-0`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w2: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || union-1 | union-1`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || union-0 [BOX1 wage] | union-0 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(OTHER=strike)=T, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=0 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || union-1 [BOX1 wage] | union-1 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=0 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=0 WW  [W1:BOX1(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || militant-[BOX1 wage] | militant-[BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w2: s=0 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=1/2 SS  [W1:BOX1(s=1/2)=F, W2:BOX1(s=1/2)=F]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || union-1 | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w2: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w3: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || union-0 | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=0 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || union-1 | union-1 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=0 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=F, W2:BOX1(OTHER=strike)=F]`
- `low-then-fair-1 if(BOX1(W1=work),(0,none),(1/2,none)) || union-1 | union-0 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=0 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=F]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || militant- | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=1/2 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=1/2 SS  [W1:BOX(s=1/2)=F, W2:BOX(s=1/2)=F]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || union-0 | union-0`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F, W2:BOX(OTHER=strike)=F]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || union-1 | union-1`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F, W2:BOX1(OTHER=strike)=T]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || union-0 [BOX1 wage] | union-0 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(OTHER=strike)=T, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(OTHER=strike)=F, W1:BOX1(s=1/2)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || union-1 [BOX1 wage] | union-1 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
  - `w3: s=1/2 WW  [W1:BOX1(s=1/2)=T, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || militant-[BOX1 wage] | militant-[BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX1(s=1/2)=T, W2:BOX1(s=1/2)=T]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || union-1 | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w2: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
  - `w3: s=1/2 SS  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(s=1/2)=F]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || union-0 | militant-`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX(OTHER=strike)=T, W2:BOX(s=1/2)=T]`
  - `w1: s=1/2 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w2: s=1/2 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
  - `w3: s=1/2 WS  [W1:BOX(s=1/2)=F, W1:BOX(OTHER=strike)=F, W2:BOX(s=1/2)=F]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || union-1 | union-1 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w1: s=1/2 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX1(s=1/2)=T, W2:BOX1(OTHER=strike)=F]`
- `low-at-0-only if(BOX(W1=strike),(0,none),(1/2,none)) || union-1 | union-0 [BOX1 wage]`
  - `w0: s=0 WW  [W1:BOX(s=1/2)=T, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=T, W2:BOX1(s=1/2)=T]`
  - `w1: s=1/2 SW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=T, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w2: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`
  - `w3: s=1/2 WW  [W1:BOX(s=1/2)=F, W1:BOX1(OTHER=strike)=F, W2:BOX(OTHER=strike)=F, W2:BOX1(s=1/2)=T]`

### Reduced chain, uniform prior, c = 0.5, N = 1000 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 0.306 | 9.2e-04 | 0.598 | 0.001 | 0.093 | 7.2e-41 | 9.2e-05 | 0.095 | 5.8e-07 | 9.2e-05 | 1.597 | 0.153 | 1.904 | 1.904 | 0.420 |
| CC + pool | 0.031 | 2.7e-04 | 0.963 | 3.4e-04 | 0.005 | 6.2e-04 | 9.0e-05 | 0.006 | 0.119 | 7.1e-04 | 1.964 | 0.015 | 1.993 | 1.993 | 0.820 |
| RC | 0.553 | 0.002 | 0.331 | 0.003 | 0.111 | 0.000 | 0.000 | 0.114 | 0.000 | 0.000 | 1.330 | 0.277 | 1.884 | 1.884 | 0.148 |
| RC + pool | 1.2e-130 | 8.3e-66 | 1.000 | 0.000 | 0.000 | 1.0e-130 | 0.000 | 1.0e-130 | 1.000 | 1.0e-130 | 2.000 | 2.1e-66 | 2.000 | 2.000 | 0.333 |
| CR | 6.8e-05 | 0.001 | 0.998 | 6.5e-05 | 3.1e-04 | 0.000 | 8.1e-06 | 3.8e-04 | 1.5e-07 | 8.1e-06 | 1.999 | 4.0e-04 | 2.000 | 2.000 | 0.952 |
| CR + pool | 6.4e-05 | 0.001 | 0.998 | 6.0e-05 | 3.2e-04 | 0.000 | 1.4e-05 | 3.8e-04 | 0.012 | 1.4e-05 | 1.999 | 3.9e-04 | 2.000 | 2.000 | 0.952 |
| RR | 0.001 | 0.668 | 0.327 | 7.1e-04 | 0.003 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 1.660 | 0.168 | 1.996 | 1.996 | 0.110 |
| RR + pool | 6.9e-131 | 8.3e-66 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 2.1e-66 | 2.000 | 2.000 | 0.333 |

### Reduced chain, uniform prior, c = 0.5, N = 100 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 0.312 | 0.008 | 0.571 | 0.012 | 0.095 | 5.8e-09 | 9.0e-04 | 0.107 | 4.7e-05 | 9.0e-04 | 1.564 | 0.158 | 1.880 | 1.880 | 0.395 |
| CC + pool | 0.059 | 0.004 | 0.896 | 0.004 | 0.029 | 0.006 | 0.001 | 0.040 | 0.156 | 0.007 | 1.896 | 0.027 | 1.949 | 1.949 | 0.747 |
| RC | 0.536 | 0.015 | 0.315 | 0.023 | 0.111 | 0.000 | 0.000 | 0.133 | 0.000 | 0.000 | 1.301 | 0.272 | 1.844 | 1.844 | 0.149 |
| RC + pool | 2.2e-13 | 3.6e-07 | 1.000 | 0.000 | 0.000 | 1.9e-13 | 0.000 | 1.9e-13 | 1.000 | 1.9e-13 | 2.000 | 8.9e-08 | 2.000 | 2.000 | 0.333 |
| CR | 8.6e-04 | 0.014 | 0.982 | 7.3e-04 | 0.003 | 0.000 | 9.6e-05 | 0.004 | 1.3e-05 | 9.6e-05 | 1.988 | 0.004 | 1.995 | 1.995 | 0.932 |
| CR + pool | 8.2e-04 | 0.014 | 0.982 | 6.7e-04 | 0.003 | 0.000 | 1.6e-04 | 0.004 | 0.014 | 1.6e-04 | 1.988 | 0.004 | 1.995 | 1.995 | 0.932 |
| RR | 0.013 | 0.677 | 0.283 | 0.006 | 0.020 | 0.000 | 0.000 | 0.027 | 0.000 | 0.000 | 1.616 | 0.176 | 1.967 | 1.967 | 0.103 |
| RR + pool | 1.3e-13 | 3.6e-07 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 8.9e-08 | 2.000 | 2.000 | 0.333 |

### Reduced chain, uniform prior, c = 0.5, N = 10000 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 0.306 | 9.3e-05 | 0.601 | 1.3e-04 | 0.093 | 0.000 | 9.2e-06 | 0.093 | 6.0e-09 | 9.2e-06 | 1.601 | 0.153 | 1.907 | 1.907 | 0.423 |
| CC + pool | 0.027 | 2.4e-05 | 0.972 | 3.2e-05 | 5.0e-04 | 6.3e-05 | 8.8e-06 | 6.0e-04 | 0.114 | 7.2e-05 | 1.972 | 0.014 | 1.999 | 1.999 | 0.830 |
| RC | 0.555 | 1.7e-04 | 0.333 | 2.6e-04 | 0.111 | 0.000 | 0.000 | 0.111 | 0.000 | 0.000 | 1.333 | 0.278 | 1.888 | 1.888 | 0.148 |
| RC + pool | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 0.000 | 2.000 | 2.000 | 0.333 |
| CR | 6.6e-06 | 1.5e-04 | 1.000 | 6.4e-06 | 3.1e-05 | 0.000 | 7.9e-07 | 3.8e-05 | 9.8e-09 | 7.9e-07 | 2.000 | 4.0e-05 | 2.000 | 2.000 | 0.954 |
| CR + pool | 6.2e-06 | 1.5e-04 | 1.000 | 5.9e-06 | 3.2e-05 | 0.000 | 1.4e-06 | 3.8e-05 | 0.012 | 1.4e-06 | 2.000 | 3.9e-05 | 2.000 | 2.000 | 0.954 |
| RR | 1.3e-04 | 0.667 | 0.333 | 7.1e-05 | 3.2e-04 | 0.000 | 0.000 | 3.9e-04 | 0.000 | 0.000 | 1.666 | 0.167 | 2.000 | 2.000 | 0.111 |
| RR + pool | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 0.000 | 2.000 | 2.000 | 0.333 |

### Reduced chain, uniform prior, c = 0.1, N = 1000 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 0.324 | 7.4e-04 | 0.565 | 0.001 | 0.109 | 8.0e-07 | 2.4e-04 | 0.110 | 8.4e-06 | 2.4e-04 | 1.565 | 0.162 | 1.889 | 1.889 | 0.381 |
| CC + pool | 4.8e-04 | 9.4e-04 | 0.995 | 2.3e-04 | 0.002 | 7.9e-04 | 1.7e-04 | 0.003 | 0.250 | 9.6e-04 | 1.996 | -8.0e-05 | 1.996 | 1.996 | 0.832 |
| RC | 0.553 | 0.002 | 0.331 | 0.003 | 0.111 | 0.000 | 0.000 | 0.114 | 0.000 | 0.000 | 1.330 | 0.277 | 1.884 | 1.884 | 0.148 |
| RC + pool | 7.0e-131 | 8.3e-66 | 1.000 | 0.000 | 0.000 | 1.0e-130 | 0.000 | 1.0e-130 | 1.000 | 1.0e-130 | 2.000 | 2.1e-66 | 2.000 | 2.000 | 0.333 |
| CR | 5.8e-05 | 0.001 | 0.998 | 5.6e-05 | 3.2e-04 | 0.000 | 2.3e-05 | 3.7e-04 | 2.2e-06 | 2.3e-05 | 1.999 | 3.9e-04 | 2.000 | 2.000 | 0.951 |
| CR + pool | 4.9e-05 | 0.001 | 0.998 | 5.2e-05 | 3.4e-04 | 0.000 | 4.0e-05 | 4.0e-04 | 0.035 | 4.0e-05 | 1.999 | 3.7e-04 | 1.999 | 1.999 | 0.951 |
| RR | 0.001 | 0.668 | 0.327 | 7.1e-04 | 0.003 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 1.660 | 0.168 | 1.996 | 1.996 | 0.110 |
| RR + pool | 6.9e-131 | 8.3e-66 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 2.1e-66 | 2.000 | 2.000 | 0.333 |

### Reduced chain, uniform prior, c = 0.1, N = 100 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 0.325 | 0.007 | 0.543 | 0.010 | 0.112 | 2.2e-04 | 0.003 | 0.123 | 0.002 | 0.003 | 1.537 | 0.163 | 1.864 | 1.864 | 0.360 |
| CC + pool | 0.007 | 0.010 | 0.950 | 0.003 | 0.021 | 0.008 | 0.002 | 0.032 | 0.277 | 0.010 | 1.959 | -2.8e-04 | 1.958 | 1.959 | 0.783 |
| RC | 0.536 | 0.015 | 0.315 | 0.023 | 0.111 | 0.000 | 0.000 | 0.133 | 0.000 | 0.000 | 1.301 | 0.272 | 1.844 | 1.844 | 0.149 |
| RC + pool | 1.3e-13 | 3.6e-07 | 1.000 | 0.000 | 0.000 | 2.0e-13 | 0.000 | 2.0e-13 | 1.000 | 2.0e-13 | 2.000 | 8.9e-08 | 2.000 | 2.000 | 0.333 |
| CR | 7.7e-04 | 0.015 | 0.980 | 6.3e-04 | 0.003 | 0.000 | 4.9e-04 | 0.004 | 5.1e-04 | 4.9e-04 | 1.987 | 0.004 | 1.995 | 1.995 | 0.928 |
| CR + pool | 7.0e-04 | 0.015 | 0.980 | 5.9e-04 | 0.004 | 0.000 | 6.7e-04 | 0.004 | 0.035 | 6.7e-04 | 1.987 | 0.004 | 1.994 | 1.994 | 0.927 |
| RR | 0.013 | 0.677 | 0.283 | 0.006 | 0.020 | 0.000 | 0.000 | 0.027 | 0.000 | 0.000 | 1.616 | 0.176 | 1.967 | 1.967 | 0.103 |
| RR + pool | 1.3e-13 | 3.6e-07 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 8.9e-08 | 2.000 | 2.000 | 0.333 |

### Reduced chain, uniform prior, c = 0.1, N = 10000 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 0.324 | 7.4e-05 | 0.568 | 1.1e-04 | 0.109 | 7.9e-08 | 2.4e-05 | 0.109 | 7.4e-07 | 2.5e-05 | 1.568 | 0.162 | 1.891 | 1.891 | 0.383 |
| CC + pool | 4.5e-05 | 9.4e-05 | 1.000 | 2.2e-05 | 2.4e-04 | 7.9e-05 | 1.7e-05 | 3.5e-04 | 0.246 | 9.6e-05 | 2.000 | -9.2e-06 | 2.000 | 2.000 | 0.837 |
| RC | 0.555 | 1.7e-04 | 0.333 | 2.6e-04 | 0.111 | 0.000 | 0.000 | 0.111 | 0.000 | 0.000 | 1.333 | 0.278 | 1.888 | 1.888 | 0.148 |
| RC + pool | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 0.000 | 2.000 | 2.000 | 0.333 |
| CR | 5.6e-06 | 1.5e-04 | 1.000 | 5.5e-06 | 3.2e-05 | 0.000 | 2.2e-06 | 3.7e-05 | 1.0e-07 | 2.2e-06 | 2.000 | 4.0e-05 | 2.000 | 2.000 | 0.954 |
| CR + pool | 4.7e-06 | 1.5e-04 | 1.000 | 5.1e-06 | 3.4e-05 | 0.000 | 4.0e-06 | 4.0e-05 | 0.035 | 4.0e-06 | 2.000 | 3.7e-05 | 2.000 | 2.000 | 0.953 |
| RR | 1.3e-04 | 0.667 | 0.333 | 7.1e-05 | 3.2e-04 | 0.000 | 0.000 | 3.9e-04 | 0.000 | 0.000 | 1.666 | 0.167 | 2.000 | 2.000 | 0.111 |
| RR + pool | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 0.000 | 2.000 | 2.000 | 0.333 |

### Reduced chain, length prior, c = 0.5, N = 1000 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 7.3e-04 | 5.4e-06 | 0.997 | 7.4e-08 | 0.003 | 6.0e-45 | 6.3e-11 | 0.003 | 4.8e-14 | 6.3e-11 | 1.997 | 3.7e-04 | 1.997 | 1.997 | 0.333 |
| CC + pool | 4.1e-06 | 4.8e-07 | 1.000 | 3.9e-09 | 1.9e-04 | 1.2e-05 | 3.5e-11 | 2.1e-04 | 0.058 | 1.2e-05 | 2.000 | -3.8e-06 | 2.000 | 2.000 | 0.343 |
| RC | 0.001 | 7.5e-06 | 0.995 | 1.1e-07 | 0.004 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 1.995 | 5.1e-04 | 1.996 | 1.996 | 0.333 |
| RC + pool | 6.9e-131 | 8.3e-66 | 1.000 | 0.000 | 0.000 | 3.5e-133 | 0.000 | 3.5e-133 | 1.000 | 3.5e-133 | 2.000 | 2.1e-66 | 2.000 | 2.000 | 0.333 |
| CR | 1.9e-07 | 1.2e-04 | 1.000 | 5.6e-10 | 4.3e-05 | 0.000 | 1.9e-11 | 4.3e-05 | 1.1e-14 | 1.9e-11 | 2.000 | 3.1e-05 | 2.000 | 2.000 | 0.346 |
| CR + pool | 1.9e-07 | 1.2e-04 | 1.000 | 5.5e-10 | 4.3e-05 | 0.000 | 2.4e-11 | 4.3e-05 | 1.2e-07 | 2.4e-11 | 2.000 | 3.1e-05 | 2.000 | 2.000 | 0.346 |
| RR | 7.4e-07 | 0.005 | 0.995 | 1.7e-09 | 1.0e-04 | 0.000 | 0.000 | 1.0e-04 | 0.000 | 0.000 | 1.997 | 0.001 | 2.000 | 2.000 | 0.332 |
| RR + pool | 6.9e-131 | 8.3e-66 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 2.1e-66 | 2.000 | 2.000 | 0.333 |

### Reduced chain, length prior, c = 0.5, N = 100 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 7.7e-04 | 5.5e-05 | 0.997 | 6.1e-07 | 0.003 | 5.6e-11 | 5.3e-10 | 0.003 | 2.1e-08 | 5.9e-10 | 1.997 | 4.0e-04 | 1.997 | 1.997 | 0.333 |
| CC + pool | 1.4e-04 | 3.8e-05 | 0.999 | 1.9e-07 | 0.001 | 7.9e-05 | 4.1e-10 | 0.001 | 0.066 | 7.9e-05 | 1.999 | 4.1e-05 | 1.999 | 1.999 | 0.339 |
| RC | 0.001 | 7.7e-05 | 0.995 | 9.4e-07 | 0.004 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 1.995 | 5.6e-04 | 1.996 | 1.996 | 0.333 |
| RC + pool | 1.3e-13 | 3.6e-07 | 1.000 | 0.000 | 0.000 | 6.5e-16 | 0.000 | 6.5e-16 | 1.000 | 6.5e-16 | 2.000 | 8.9e-08 | 2.000 | 2.000 | 0.333 |
| CR | 1.5e-05 | 8.5e-04 | 0.999 | 3.5e-08 | 3.7e-04 | 0.000 | 2.2e-10 | 3.7e-04 | 3.1e-12 | 2.2e-10 | 1.999 | 2.2e-04 | 2.000 | 2.000 | 0.343 |
| CR + pool | 1.5e-05 | 8.5e-04 | 0.999 | 3.5e-08 | 3.7e-04 | 0.000 | 2.7e-10 | 3.7e-04 | 1.4e-07 | 2.7e-10 | 1.999 | 2.2e-04 | 2.000 | 2.000 | 0.343 |
| RR | 5.0e-05 | 0.005 | 0.994 | 9.7e-08 | 8.3e-04 | 0.000 | 0.000 | 8.3e-04 | 0.000 | 0.000 | 1.997 | 0.001 | 1.999 | 1.999 | 0.332 |
| RR + pool | 1.3e-13 | 3.6e-07 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 8.9e-08 | 2.000 | 2.000 | 0.333 |

### Reduced chain, length prior, c = 0.5, N = 10000 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 7.2e-04 | 5.4e-07 | 0.997 | 7.6e-09 | 0.003 | 0.000 | 6.5e-12 | 0.003 | 4.9e-16 | 6.5e-12 | 1.997 | 3.6e-04 | 1.997 | 1.997 | 0.333 |
| CC + pool | 6.9e-08 | 4.9e-09 | 1.000 | 6.5e-11 | 2.1e-05 | 1.3e-06 | 3.4e-12 | 2.2e-05 | 0.057 | 1.3e-06 | 2.000 | -6.0e-07 | 2.000 | 2.000 | 0.343 |
| RC | 0.001 | 7.5e-07 | 0.995 | 1.2e-08 | 0.004 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 1.995 | 5.1e-04 | 1.996 | 1.996 | 0.333 |
| RC + pool | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 0.000 | 2.000 | 2.000 | 0.333 |
| CR | 1.9e-09 | 1.3e-05 | 1.000 | 1.9e-11 | 4.3e-06 | 0.000 | 1.9e-12 | 4.3e-06 | 1.0e-16 | 1.9e-12 | 2.000 | 3.2e-06 | 2.000 | 2.000 | 0.346 |
| CR + pool | 1.9e-09 | 1.3e-05 | 1.000 | 1.8e-11 | 4.3e-06 | 0.000 | 2.3e-12 | 4.3e-06 | 1.2e-07 | 2.3e-12 | 2.000 | 3.2e-06 | 2.000 | 2.000 | 0.346 |
| RR | 7.8e-09 | 0.005 | 0.995 | 6.3e-11 | 1.1e-05 | 0.000 | 0.000 | 1.1e-05 | 0.000 | 0.000 | 1.997 | 0.001 | 2.000 | 2.000 | 0.332 |
| RR + pool | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 0.000 | 2.000 | 2.000 | 0.333 |

### Reduced chain, length prior, c = 0.1, N = 1000 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 7.3e-04 | 5.4e-06 | 0.997 | 7.4e-08 | 0.003 | 1.6e-12 | 1.2e-10 | 0.003 | 6.0e-10 | 1.2e-10 | 1.997 | 3.7e-04 | 1.997 | 1.997 | 0.333 |
| CC + pool | 6.9e-07 | 2.1e-05 | 1.000 | 1.4e-09 | 8.2e-05 | 1.2e-05 | 6.5e-11 | 9.4e-05 | 0.126 | 1.2e-05 | 2.000 | 1.9e-07 | 2.000 | 2.000 | 0.341 |
| RC | 0.001 | 7.5e-06 | 0.995 | 1.1e-07 | 0.004 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 1.995 | 5.1e-04 | 1.996 | 1.996 | 0.333 |
| RC + pool | 6.9e-131 | 8.3e-66 | 1.000 | 0.000 | 0.000 | 3.5e-133 | 0.000 | 3.5e-133 | 1.000 | 3.5e-133 | 2.000 | 2.1e-66 | 2.000 | 2.000 | 0.333 |
| CR | 1.9e-07 | 1.2e-04 | 1.000 | 5.5e-10 | 4.3e-05 | 0.000 | 3.7e-11 | 4.3e-05 | 3.3e-13 | 3.7e-11 | 2.000 | 3.1e-05 | 2.000 | 2.000 | 0.346 |
| CR + pool | 1.9e-07 | 1.2e-04 | 1.000 | 5.3e-10 | 4.3e-05 | 0.000 | 4.4e-11 | 4.3e-05 | 2.2e-07 | 4.4e-11 | 2.000 | 3.1e-05 | 2.000 | 2.000 | 0.346 |
| RR | 7.4e-07 | 0.005 | 0.995 | 1.7e-09 | 1.0e-04 | 0.000 | 0.000 | 1.0e-04 | 0.000 | 0.000 | 1.997 | 0.001 | 2.000 | 2.000 | 0.332 |
| RR + pool | 6.9e-131 | 8.3e-66 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 2.1e-66 | 2.000 | 2.000 | 0.333 |

### Reduced chain, length prior, c = 0.1, N = 100 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 7.5e-04 | 5.3e-05 | 0.997 | 6.0e-07 | 0.003 | 2.1e-06 | 1.9e-08 | 0.003 | 8.2e-04 | 2.1e-06 | 1.997 | 3.9e-04 | 1.997 | 1.997 | 0.333 |
| CC + pool | 4.5e-05 | 1.8e-04 | 0.999 | 8.5e-08 | 6.3e-04 | 9.6e-05 | 1.9e-08 | 7.3e-04 | 0.132 | 9.6e-05 | 1.999 | 2.2e-05 | 1.999 | 1.999 | 0.339 |
| RC | 0.001 | 7.7e-05 | 0.995 | 9.4e-07 | 0.004 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 1.995 | 5.6e-04 | 1.996 | 1.996 | 0.333 |
| RC + pool | 1.3e-13 | 3.6e-07 | 1.000 | 0.000 | 0.000 | 6.5e-16 | 0.000 | 6.5e-16 | 1.000 | 6.5e-16 | 2.000 | 8.9e-08 | 2.000 | 2.000 | 0.333 |
| CR | 1.5e-05 | 8.5e-04 | 0.999 | 3.5e-08 | 3.7e-04 | 0.000 | 1.9e-08 | 3.7e-04 | 3.5e-09 | 1.9e-08 | 1.999 | 2.2e-04 | 2.000 | 2.000 | 0.343 |
| CR + pool | 1.5e-05 | 8.5e-04 | 0.999 | 3.5e-08 | 3.7e-04 | 0.000 | 1.9e-08 | 3.7e-04 | 2.5e-07 | 1.9e-08 | 1.999 | 2.2e-04 | 2.000 | 2.000 | 0.343 |
| RR | 5.0e-05 | 0.005 | 0.994 | 9.7e-08 | 8.3e-04 | 0.000 | 0.000 | 8.3e-04 | 0.000 | 0.000 | 1.997 | 0.001 | 1.999 | 1.999 | 0.332 |
| RR + pool | 1.3e-13 | 3.6e-07 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 8.9e-08 | 2.000 | 2.000 | 0.333 |

### Reduced chain, length prior, c = 0.1, N = 10000 (tie = whack)

| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC | 7.2e-04 | 5.4e-07 | 0.997 | 7.6e-09 | 0.003 | 1.6e-14 | 1.2e-11 | 0.003 | 6.1e-12 | 1.2e-11 | 1.997 | 3.6e-04 | 1.997 | 1.997 | 0.333 |
| CC + pool | 7.3e-09 | 2.2e-06 | 1.000 | 2.9e-11 | 8.4e-06 | 1.2e-06 | 6.5e-12 | 9.7e-06 | 0.125 | 1.2e-06 | 2.000 | -1.3e-08 | 2.000 | 2.000 | 0.341 |
| RC | 0.001 | 7.5e-07 | 0.995 | 1.2e-08 | 0.004 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 1.995 | 5.1e-04 | 1.996 | 1.996 | 0.333 |
| RC + pool | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 0.000 | 2.000 | 2.000 | 0.333 |
| CR | 1.9e-09 | 1.3e-05 | 1.000 | 1.8e-11 | 4.3e-06 | 0.000 | 3.4e-12 | 4.3e-06 | 3.6e-15 | 3.4e-12 | 2.000 | 3.2e-06 | 2.000 | 2.000 | 0.346 |
| CR + pool | 1.9e-09 | 1.3e-05 | 1.000 | 1.6e-11 | 4.3e-06 | 0.000 | 4.1e-12 | 4.3e-06 | 2.1e-07 | 4.1e-12 | 2.000 | 3.2e-06 | 2.000 | 2.000 | 0.346 |
| RR | 7.8e-09 | 0.005 | 0.995 | 6.3e-11 | 1.1e-05 | 0.000 | 0.000 | 1.1e-05 | 0.000 | 0.000 | 1.997 | 0.001 | 2.000 | 2.000 | 0.332 |
| RR + pool | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | – | 0.000 | 2.000 | 0.000 | 2.000 | 2.000 | 0.333 |

Tie rule at 1 − s = c: max |Δ| over all summaries and cells between tie = whack and tie = nowhack: 0.

### Committed threats: payoff advantage over the feasible deviation (uniform prior, N = 10³)

| c | cell | boss threat untriggered: π mass, value if called | boss whack executed: π mass, advantage | worker strike executed: π mass (each slot), advantage |
|---|---|---|---|---|
| 0.5 | CC | 0.535, -0.50 | 9.2e-05, -0.50 | 0.048, -1.0e-05 |
| 0.5 | CC + pool | 0.834, 0.49 | 7.1e-04, 0.51 | 0.003, -0.12 |
| 0.5 | RC | – (not committed or never) | – (not committed or never) | 0.058, -3.0e-05 |
| 0.5 | RC + pool | – (not committed or never) | – (not committed or never) | 7.5e-131, -1.00 |
| 0.5 | CR | 0.952, -0.50 | 8.1e-06, -0.57 | – (not committed or never) |
| 0.5 | CR + pool | 0.952, 0.50 | 1.4e-05, -0.12 | – (not committed or never) |
| 0.5 | RR | – (not committed or never) | – (not committed or never) | – (not committed or never) |
| 0.5 | RR + pool | – (not committed or never) | – (not committed or never) | – (not committed or never) |
| 0.1 | CC | 0.493, -0.10 | 2.4e-04, -0.11 | 0.055, -8.2e-05 |
| 0.1 | CC + pool | 0.833, 0.90 | 9.6e-04, 0.92 | 0.002, -0.27 |
| 0.1 | RC | – (not committed or never) | – (not committed or never) | 0.058, -3.0e-05 |
| 0.1 | RC + pool | – (not committed or never) | – (not committed or never) | 7.6e-131, -1.00 |
| 0.1 | CR | 0.952, -0.10 | 2.3e-05, -0.12 | – (not committed or never) |
| 0.1 | CR + pool | 0.951, 0.90 | 4.0e-05, 0.39 | – (not committed or never) |
| 0.1 | RR | – (not committed or never) | – (not committed or never) | – (not committed or never) |
| 0.1 | RR + pool | – (not committed or never) | – (not committed or never) | – (not committed or never) |

#### Support and transitions: CC, uniform, c = 0.5, N = 10³ (99% of π on 26 of 81 states)

| π | state (boss, W1, W2) | implemented play | summary |
|---|---|---|---|
| 0.1436 | (0,strike) union scab | (0,strike) W W | zero wage |
| 0.1436 | (0,strike) scab union | (0,strike) W W | zero wage |
| 0.1327 | (0,strike) scab scab | (0,strike) W W | zero wage |
| 0.0592 | (0,source) scab scab | (0,source) W W | zero wage |
| 0.0450 | (0,none) scab scab | (0,none) W W | zero wage |
| 0.0369 | (1/2,source) militant militant | (1/2,source) W W | fair |

Largest currents between summaries (per mutation event): zero wage>scab split 3.1e-05; strike>fair 2.8e-05; fair>zero wage 2.0e-05; zero wage>strike 1.6e-05; scab split>zero wage 1.5e-05; scab split>strike 1.5e-05.
Exits from the top state `(0,strike) union scab`: total 1.5e-04 per event (strict 0.0e+00, neutral 1.5e-04, deleterious 1.3e-67); top moves: W1 → (0,strike) scab scab (neutral, 1.1e-04); B → (0,none) union scab (neutral, 3.7e-05); B → (0,source) union scab (deleterious, 4.3e-68).

#### Support and transitions: CC + pool, uniform, c = 0.5, N = 10³ (99% of π on 15 of 81 states)

| π | state (boss, W1, W2) | implemented play | summary |
|---|---|---|---|
| 0.2762 | (0,strike) union scab | (0,strike) W W | zero wage |
| 0.2762 | (0,strike) scab union | (0,strike) W W | zero wage |
| 0.2675 | (0,strike) scab scab | (0,strike) W W | zero wage |
| 0.0416 | (0,source) scab scab | (0,source) W W | zero wage |
| 0.0370 | (0,none) scab scab | (0,none) W W | zero wage |
| 0.0325 | (0,none) union scab | (0,none) W W | zero wage |

Largest currents between summaries (per mutation event): repression:strike>zero wage 3.2e-05; zero wage>scab split 2.5e-05; scab split>repression:strike 2.4e-05; zero wage>strike 1.4e-05; strike>fair 6.8e-06; strike>repression:strike 5.0e-06.
Exits from the top state `(0,strike) union scab`: total 1.5e-04 per event (strict 0.0e+00, neutral 1.5e-04, deleterious 1.3e-67); top moves: W1 → (0,strike) scab scab (neutral, 1.1e-04); B → (0,none) union scab (neutral, 3.7e-05); B → (0,source) union scab (deleterious, 4.3e-68).

#### Support and transitions: RC, uniform, c = 0.5, N = 10³ (99% of π on 33 of 81 states)

| π | state (boss, W1, W2) | implemented play | summary |
|---|---|---|---|
| 0.0370 | (0,source) scab scab | (0,none) W W | zero wage |
| 0.0370 | (0,none) scab scab | (0,none) W W | zero wage |
| 0.0370 | (0,strike) scab scab | (0,none) W W | zero wage |
| 0.0368 | (1/2,strike) militant militant | (1/2,none) W W | fair |
| 0.0368 | (1/2,none) militant militant | (1/2,none) W W | fair |
| 0.0368 | (1/2,source) militant militant | (1/2,none) W W | fair |

Largest currents between summaries (per mutation event): strike>fair 7.3e-05; zero wage>scab split 4.9e-05; zero wage>strike 4.9e-05; fair>zero wage 4.8e-05; intermediate>zero wage 2.6e-05; fair>intermediate 2.6e-05.
Exits from the top state `(0,source) scab scab`: total 5.2e-04 per event (strict 0.0e+00, neutral 5.2e-04, deleterious 1.3e-67); top moves: W2 → (0,source) scab militant (neutral, 1.1e-04); W2 → (0,source) scab union (neutral, 1.1e-04); W1 → (0,source) militant scab (neutral, 1.1e-04).

#### Support and transitions: RC + pool, uniform, c = 0.5, N = 10³ (99% of π on 9 of 81 states)

| π | state (boss, W1, W2) | implemented play | summary |
|---|---|---|---|
| 0.1111 | (0,strike) scab scab | (0,strike) W W | zero wage |
| 0.1111 | (0,strike) scab union | (0,strike) W W | zero wage |
| 0.1111 | (0,source) union scab | (0,strike) W W | zero wage |
| 0.1111 | (0,source) scab union | (0,strike) W W | zero wage |
| 0.1111 | (0,none) union scab | (0,strike) W W | zero wage |
| 0.1111 | (0,strike) union scab | (0,strike) W W | zero wage |

Largest currents between summaries (per mutation event): zero wage>intermediate 1.3e-67; intermediate>zero wage 1.3e-67; repression:strike>zero wage 5.4e-132; zero wage>repression:strike 5.3e-132; zero wage>fair 2.0e-132; fair>zero wage 2.0e-132.
Exits from the top state `(0,strike) scab scab`: total 3.0e-04 per event (strict 0.0e+00, neutral 3.0e-04, deleterious 1.3e-67); top moves: W2 → (0,strike) scab union (neutral, 1.1e-04); W1 → (0,strike) union scab (neutral, 1.1e-04); B → (0,none) scab scab (neutral, 3.7e-05).

#### Support and transitions: CR, uniform, c = 0.5, N = 10³ (99% of π on 13 of 81 states)

| π | state (boss, W1, W2) | implemented play | summary |
|---|---|---|---|
| 0.1116 | (0,strike) scab militant | (0,strike) W W | zero wage |
| 0.1116 | (0,strike) militant scab | (0,strike) W W | zero wage |
| 0.1115 | (0,strike) militant militant | (0,strike) W W | zero wage |
| 0.1099 | (0,strike) union militant | (0,strike) W W | zero wage |
| 0.1099 | (0,strike) militant union | (0,strike) W W | zero wage |
| 0.1088 | (0,strike) union union | (0,strike) W W | zero wage |

Largest currents between summaries (per mutation event): zero wage>scab split 8.0e-06; intermediate>zero wage 7.7e-06; scab split>intermediate 4.8e-06; zero wage>strike 4.7e-06; scab split>zero wage 3.0e-06; strike>intermediate 1.7e-06.
Exits from the top state `(0,strike) scab militant`: total 4.4e-04 per event (strict 0.0e+00, neutral 4.4e-04, deleterious 1.3e-67); top moves: W2 → (0,strike) scab scab (neutral, 1.1e-04); W2 → (0,strike) scab union (neutral, 1.1e-04); W1 → (0,strike) militant militant (neutral, 1.1e-04).

#### Support and transitions: CR + pool, uniform, c = 0.5, N = 10³ (99% of π on 13 of 81 states)

| π | state (boss, W1, W2) | implemented play | summary |
|---|---|---|---|
| 0.1118 | (0,strike) militant scab | (0,strike) W W | zero wage |
| 0.1118 | (0,strike) scab militant | (0,strike) W W | zero wage |
| 0.1117 | (0,strike) militant militant | (0,strike) W W | zero wage |
| 0.1098 | (0,strike) militant union | (0,strike) W W | zero wage |
| 0.1098 | (0,strike) union militant | (0,strike) W W | zero wage |
| 0.1083 | (0,strike) union union | (0,strike) W W | zero wage |

Largest currents between summaries (per mutation event): zero wage>scab split 8.0e-06; intermediate>zero wage 7.7e-06; scab split>intermediate 4.9e-06; zero wage>strike 4.7e-06; scab split>zero wage 3.1e-06; strike>intermediate 1.6e-06.
Exits from the top state `(0,strike) militant scab`: total 4.4e-04 per event (strict 0.0e+00, neutral 4.4e-04, deleterious 1.3e-67); top moves: W1 → (0,strike) scab scab (neutral, 1.1e-04); W2 → (0,strike) militant militant (neutral, 1.1e-04); W2 → (0,strike) militant union (neutral, 1.1e-04).

#### Support and transitions: RR, uniform, c = 0.5, N = 10³ (99% of π on 29 of 81 states)

| π | state (boss, W1, W2) | implemented play | summary |
|---|---|---|---|
| 0.0370 | (1/4,strike) militant militant | (1/4,none) W W | intermediate |
| 0.0370 | (1/4,source) militant militant | (1/4,none) W W | intermediate |
| 0.0370 | (1/4,none) militant militant | (1/4,none) W W | intermediate |
| 0.0369 | (1/4,none) militant union | (1/4,none) W W | intermediate |
| 0.0369 | (1/4,strike) militant union | (1/4,none) W W | intermediate |
| 0.0369 | (1/4,source) militant union | (1/4,none) W W | intermediate |

Largest currents between summaries (per mutation event): intermediate>zero wage 9.6e-05; zero wage>scab split 4.9e-05; zero wage>strike 4.8e-05; scab split>intermediate 4.7e-05; strike>intermediate 2.8e-05; fair>intermediate 2.1e-05.
Exits from the top state `(1/4,strike) militant militant`: total 5.2e-04 per event (strict 0.0e+00, neutral 5.2e-04, deleterious 1.3e-67); top moves: W1 → (1/4,strike) scab militant (neutral, 1.1e-04); W2 → (1/4,strike) militant scab (neutral, 1.1e-04); W2 → (1/4,strike) militant union (neutral, 1.1e-04).

#### Support and transitions: RR + pool, uniform, c = 0.5, N = 10³ (99% of π on 27 of 81 states)

| π | state (boss, W1, W2) | implemented play | summary |
|---|---|---|---|
| 0.0370 | (0,strike) scab scab | (0,strike) W W | zero wage |
| 0.0370 | (0,source) scab militant | (0,strike) W W | zero wage |
| 0.0370 | (0,source) scab scab | (0,strike) W W | zero wage |
| 0.0370 | (0,none) union union | (0,strike) W W | zero wage |
| 0.0370 | (0,none) union militant | (0,strike) W W | zero wage |
| 0.0370 | (0,none) union scab | (0,strike) W W | zero wage |

Largest currents between summaries (per mutation event): zero wage>intermediate 1.3e-67; intermediate>zero wage 1.3e-67; zero wage>fair 2.0e-132; fair>zero wage 2.0e-132; fair>intermediate 1.1e-132; intermediate>fair 1.1e-132.
Exits from the top state `(0,strike) scab scab`: total 5.2e-04 per event (strict 0.0e+00, neutral 5.2e-04, deleterious 1.3e-67); top moves: W2 → (0,strike) scab militant (neutral, 1.1e-04); W2 → (0,strike) scab union (neutral, 1.1e-04); W1 → (0,strike) militant scab (neutral, 1.1e-04).

### Full-language tensors (297 boss × 452 × 452 worker functions)

| arm \| pool \| c \| tie | unstable | strikes at s > 0 | strikes | implemented source targeting |
|---|---|---|---|---|
| CC \| pool0 \| c0.1 \| whack | 0 | 30597939 | 45715266 | 20226096 |
| CC \| pool0 \| c0.5 \| whack | 0 | 30597939 | 45715266 | 20226096 |
| CC \| pool1 \| c0.1 \| whack | 0 | 30597939 | 45715266 | 20226096 |
| CC \| pool1 \| c0.1 \| nowhack | 0 | 30597939 | 45715266 | 20226096 |
| CC \| pool1 \| c0.5 \| whack | 0 | 30597939 | 45715266 | 20226096 |
| CC \| pool1 \| c0.5 \| nowhack | 0 | 30597939 | 45715266 | 20226096 |
| RC \| pool0 \| c0.1 \| whack | 0 | 30576339 | 45682866 | 0 |
| RC \| pool0 \| c0.5 \| whack | 0 | 30576339 | 45682866 | 0 |
| RC \| pool1 \| c0.1 \| whack | 0 | 30576339 | 45682866 | 0 |
| RC \| pool1 \| c0.1 \| nowhack | 0 | 30576339 | 45682866 | 0 |
| RC \| pool1 \| c0.5 \| whack | 0 | 30576339 | 45682866 | 0 |
| RC \| pool1 \| c0.5 \| nowhack | 0 | 30592539 | 45699066 | 0 |
| CR \| pool0 \| c0.1 \| whack | 0 | 0 | 7796658 | 19555146 |
| CR \| pool0 \| c0.5 \| whack | 0 | 0 | 7796658 | 19555146 |
| CR \| pool1 \| c0.1 \| whack | 0 | 0 | 7796658 | 19555146 |
| CR \| pool1 \| c0.1 \| nowhack | 0 | 0 | 7796658 | 19555146 |
| CR \| pool1 \| c0.5 \| whack | 0 | 0 | 7796658 | 19555146 |
| CR \| pool1 \| c0.5 \| nowhack | 0 | 0 | 7796658 | 19555146 |
| RR \| pool0 \| c0.1 \| whack | 0 | 0 | 12199167 | 0 |
| RR \| pool0 \| c0.5 \| whack | 0 | 0 | 12199167 | 0 |
| RR \| pool1 \| c0.1 \| whack | 0 | 0 | 0 | 0 |
| RR \| pool1 \| c0.1 \| nowhack | 0 | 0 | 0 | 0 |
| RR \| pool1 \| c0.5 \| whack | 0 | 0 | 0 | 0 |
| RR \| pool1 \| c0.5 \| nowhack | 0 | 0 | 0 | 0 |

### Part C, full chain, length prior, N = 10³

| cell | θ | states | outcome cut | classes B/W | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \| strike | boss | worker | eff. | total surplus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC_pool0_c0.5_N1000_whack | 1e-09 | 5565 | 0.005 | 297/364 | 0.0032 | 0.0132 | 0.4758 | 0.1247 | 0.3831 | 1.7e-05 | 3.2e-08 | 0.5078 | 3.4e-05 | 1.357 | 0.0051 | 1.368 | 1.368 |
| CC_pool1_c0.5_N1000_whack | 1e-09 | 3083 | 0.005 | 297/364 | 2.8e-05 | 0.0021 | 0.9860 | 0.0001 | 0.0105 | 0.0012 | 6.7e-07 | 0.0119 | 0.105 | 1.987 | -7.8e-05 | 1.987 | 1.987 |
| CR_pool0_c0.5_N1000_whack | 1e-11 | 16751 | 2.8e-04 | 87/260 | 8.4e-06 | 0.0017 | 0.9978 | 2.5e-06 | 0.0005 | 0.0000 | 3.6e-08 | 0.0005 | 9.6e-07 | 1.999 | 0.0004 | 1.999 | 1.999 |
| RC_pool0_c0.5_N1000_whack | 1e-11 | 8514 | 9.3e-05 | 27/122 | 0.0048 | 0.0191 | 0.3254 | 0.1465 | 0.5042 | 0.0000 | 0.0000 | 0.6507 | 0.000 | 1.188 | 0.0075 | 1.203 | 1.203 |
| RC_pool1_c0.5_N1000_nowhack | 1e-11 | 4921 | 0.003 | 27/122 | 1.4e-05 | 0.0003 | 0.9996 | 1.1e-07 | 8.6e-06 | 1.2e-05 | 0.0000 | 2.1e-05 | 0.584 | 2.000 | 8.4e-05 | 2.000 | 2.000 |
| RC_pool1_c0.5_N1000_whack | 1e-11 | 4320 | 0.005 | 27/122 | 1.3e-05 | 0.0003 | 0.9997 | 0.0000 | 0.0000 | 3.0e-06 | 0.0000 | 3.0e-06 | 1.000 | 2.000 | 8.5e-05 | 2.000 | 2.000 |
| RC_pool1_c0.5_N1000_whack_theta1e-9 | 1e-09 | 610 | 0.052 | 27/122 | 1.3e-05 | 0.0003 | 0.9996 | 0.0000 | 0.0000 | 2.6e-06 | 0.0000 | 2.6e-06 | 1.000 | 2.000 | 8.9e-05 | 2.000 | 2.000 |
| RR_pool0_c0.5_N10000_whack | 1e-11 | 2099 | 6.2e-05 | 13/62 | 5.4e-06 | 0.7516 | 0.2479 | 1.0e-06 | 0.0005 | 0.0000 | 0.0000 | 0.0005 | 0.000 | 1.624 | 0.1879 | 1.999 | 1.999 |
| RR_pool0_c0.5_N1000_whack | 1e-11 | 3591 | 3.4e-05 | 13/62 | 0.0001 | 0.7534 | 0.2415 | 2.1e-05 | 0.0050 | 0.0000 | 0.0000 | 0.0050 | 0.000 | 1.618 | 0.1884 | 1.995 | 1.995 |
| RR_pool0_c0.5_N100_whack | 1e-11 | 8233 | 3.5e-06 | 13/62 | 0.0040 | 0.7545 | 0.2062 | 0.0009 | 0.0345 | 0.0000 | 0.0000 | 0.0353 | 0.000 | 1.583 | 0.1906 | 1.964 | 1.964 |

#### Support and transitions: CC_pool0_c0.5_N1000_whack

Whack policy held (implemented): strike 0.230, none 0.386, source 0.384; conditional programs hold 0.098 of π; 99% of π on 307 states.

| π | state | summary |
|---|---|---|
| 0.1973 | `(0,strike) | work | work` | zero wage |
| 0.1119 | `(0,source) | work | work` | zero wage |
| 0.1118 | `(0,none) | work | work` | zero wage |
| 0.0893 | `(0,source) | work | strike` | scab split |
| 0.0893 | `(0,source) | strike | work` | scab split |
| 0.0893 | `(0,none) | strike | work` | scab split |

Exits from `(0,strike) | work | work`: strict 0.0e+00, neutral-change 7.4e-05, neutral-keep 1.4e-05, deleterious 1.3e-67; top: B (0,none) (neutral-change, 3.6e-05) → zero wage; B (0,source) (neutral-change, 3.6e-05) → zero wage; W1 if(BOX(s in {0}),work,strike) (neutral-keep, 4.0e-07) → zero wage. Net currents: zero wage>scab split 1.8e-05; intermediate>zero wage 1.3e-05; intermediate>scab split -1.0e-05; fair>scab split -6.6e-06.

#### Support and transitions: CC_pool1_c0.5_N1000_whack

Whack policy held (implemented): strike 0.819, none 0.091, source 0.090; conditional programs hold 0.094 of π; 99% of π on 203 states.

| π | state | summary |
|---|---|---|
| 0.7416 | `(0,strike) | work | work` | zero wage |
| 0.0768 | `(0,source) | work | work` | zero wage |
| 0.0767 | `(0,none) | work | work` | zero wage |
| 0.0028 | `(0,strike) | work | if(BOX(h in {none,source}),strike,work)` | zero wage |
| 0.0028 | `(0,strike) | if(BOX(h in {none,source}),strike,work) | work` | zero wage |
| 0.0027 | `(0,strike) | work | if(BOX(h in {strike}),work,strike)` | zero wage |

Exits from `(0,strike) | work | work`: strict 0.0e+00, neutral-change 7.4e-05, neutral-keep 1.4e-05, deleterious 1.3e-67; top: B (0,none) (neutral-change, 3.6e-05) → zero wage; B (0,source) (neutral-change, 3.6e-05) → zero wage; W1 if(BOX(s in {0}),work,strike) (neutral-keep, 4.0e-07) → zero wage. Net currents: zero wage>scab split 5.4e-05; zero wage>repression:strike -5.2e-05; scab split>repression:strike 5.1e-05; intermediate>zero wage 2.0e-06.

#### Support and transitions: CR_pool0_c0.5_N1000_whack

Whack policy held (implemented): strike 0.956, none 0.022, source 0.022; conditional programs hold 0.079 of π; 99% of π on 156 states.

| π | state | summary |
|---|---|---|
| 0.2305 | `(0,strike) | strike | strike` | zero wage |
| 0.2295 | `(0,strike) | work | strike` | zero wage |
| 0.2295 | `(0,strike) | strike | work` | zero wage |
| 0.1914 | `(0,strike) | work | work` | zero wage |
| 0.0191 | `(0,source) | work | work` | zero wage |
| 0.0190 | `(0,none) | work | work` | zero wage |

Exits from `(0,strike) | strike | strike`: strict 0.0e+00, neutral-change 0.0e+00, neutral-keep 3.5e-04, deleterious 1.3e-67; top: W1 work (neutral-keep, 1.6e-04) → zero wage; W2 work (neutral-keep, 1.6e-04) → zero wage; W1 if(BOX(s in {1/2}),work,strike) (neutral-keep, 8.2e-07) → zero wage. Net currents: intermediate>zero wage 8.7e-06; zero wage>scab split 8.6e-06; intermediate>scab split -8.4e-06; fair>intermediate 1.3e-07.

#### Support and transitions: RC_pool0_c0.5_N1000_whack

Whack policy held (implemented): strike 0.000, none 1.000, source 0.000; conditional programs hold 0.082 of π; 99% of π on 92 states.

| π | state | summary |
|---|---|---|
| 0.3004 | `(0,strike) | work | work` | zero wage |
| 0.2368 | `(0,strike) | strike | work` | scab split |
| 0.2368 | `(0,strike) | work | strike` | scab split |
| 0.1404 | `(0,strike) | strike | strike` | strike |
| 0.0027 | `(1/4,strike) | if(BOX(s in {1/4,1/2}),work,strike) | work` | intermediate |
| 0.0027 | `(1/4,strike) | work | if(BOX(s in {1/4,1/2}),work,strike)` | intermediate |

Exits from `(0,strike) | work | work`: strict 0.0e+00, neutral-change 3.3e-04, neutral-keep 1.3e-05, deleterious 1.3e-67; top: W1 strike (neutral-change, 1.6e-04) → scab split; W2 strike (neutral-change, 1.6e-04) → scab split; W1 if(BOX(h in {strike}),strike,work) (neutral-keep, 1.3e-06) → zero wage. Net currents: zero wage>scab split 2.4e-05; intermediate>zero wage 1.9e-05; intermediate>scab split -1.5e-05; fair>scab split -9.5e-06.

#### Support and transitions: RC_pool1_c0.5_N1000_nowhack

Whack policy held (implemented): strike 1.000, none 2.2e-05, source 0.000; conditional programs hold 0.083 of π; 99% of π on 23 states.

| π | state | summary |
|---|---|---|
| 0.9166 | `(0,strike) | work | work` | zero wage |
| 0.0077 | `(0,strike) | if(BOX(s in {1/2}),strike,work) | work` | zero wage |
| 0.0077 | `(0,strike) | work | if(BOX(s in {1/2}),strike,work)` | zero wage |
| 0.0071 | `(0,strike) | work | if(BOX(s in {0,1/4}),work,strike)` | zero wage |
| 0.0071 | `(0,strike) | if(BOX(s in {0,1/4}),work,strike) | work` | zero wage |
| 0.0031 | `(0,strike) | if(BOX(h in {source}),strike,work) | work` | zero wage |

Exits from `(0,strike) | work | work`: strict 0.0e+00, neutral-change 0.0e+00, neutral-keep 1.4e-05, deleterious 1.3e-67; top: W1 if(BOX(s in {1/2}),strike,work) (neutral-keep, 1.2e-06) → zero wage; W2 if(BOX(s in {1/2}),strike,work) (neutral-keep, 1.2e-06) → zero wage; W1 if(BOX(s in {0,1/4}),work,strike) (neutral-keep, 1.2e-06) → zero wage. Net currents: zero wage>repression:strike -4.0e-07; zero wage>scab split 3.7e-07; scab split>repression:strike 3.7e-07; fair>zero wage -1.8e-07.

#### Support and transitions: RC_pool1_c0.5_N1000_whack

Whack policy held (implemented): strike 1.000, none 0.000, source 0.000; conditional programs hold 0.077 of π; 99% of π on 24 states.

| π | state | summary |
|---|---|---|
| 0.9233 | `(0,strike) | work | work` | zero wage |
| 0.0083 | `(0,strike) | work | if(BOX(h in {none}),strike,work)` | zero wage |
| 0.0083 | `(0,strike) | if(BOX(h in {none}),strike,work) | work` | zero wage |
| 0.0026 | `(0,strike) | work | if(BOX(s in {1/2}),strike,work)` | zero wage |
| 0.0026 | `(0,strike) | if(BOX(s in {1/2}),strike,work) | work` | zero wage |
| 0.0026 | `(0,strike) | if(BOX(s in {1/4}),strike,work) | work` | zero wage |

Exits from `(0,strike) | work | work`: strict 0.0e+00, neutral-change 0.0e+00, neutral-keep 1.3e-05, deleterious 1.3e-67; top: W1 if(BOX(h in {none}),strike,work) (neutral-keep, 1.3e-06) → zero wage; W2 if(BOX(h in {none}),strike,work) (neutral-keep, 1.3e-06) → zero wage; W1 if(BOX(s in {0}),work,strike) (neutral-keep, 4.2e-07) → zero wage. Net currents: fair>zero wage -1.7e-07; fair>intermediate 1.1e-07; zero wage>repression:strike -8.8e-08; intermediate>zero wage 8.5e-08.

#### Support and transitions: RC_pool1_c0.5_N1000_whack_theta1e-9

Whack policy held (implemented): strike 1.000, none 0.000, source 0.000; conditional programs hold 0.077 of π; 99% of π on 24 states.

| π | state | summary |
|---|---|---|
| 0.9233 | `(0,strike) | work | work` | zero wage |
| 0.0083 | `(0,strike) | if(BOX(h in {none}),strike,work) | work` | zero wage |
| 0.0083 | `(0,strike) | work | if(BOX(h in {none}),strike,work)` | zero wage |
| 0.0027 | `(0,strike) | work | if(BOX(s in {1/4}),strike,work)` | zero wage |
| 0.0027 | `(0,strike) | if(BOX(s in {1/4}),strike,work) | work` | zero wage |
| 0.0027 | `(0,strike) | work | if(BOX(s in {1/2}),strike,work)` | zero wage |

Exits from `(0,strike) | work | work`: strict 0.0e+00, neutral-change 0.0e+00, neutral-keep 1.3e-05, deleterious 1.3e-67; top: W1 if(BOX(h in {none}),strike,work) (neutral-keep, 1.3e-06) → zero wage; W2 if(BOX(h in {none}),strike,work) (neutral-keep, 1.3e-06) → zero wage; W1 if(BOX(s in {0}),work,strike) (neutral-keep, 4.2e-07) → zero wage. Net currents: fair>zero wage -1.7e-07; fair>intermediate 1.1e-07; zero wage>repression:strike -9.1e-08; intermediate>zero wage 7.8e-08.

#### Support and transitions: RR_pool0_c0.5_N10000_whack

Whack policy held (implemented): strike 0.000, none 1.000, source 0.000; conditional programs hold 0.074 of π; 99% of π on 74 states.

| π | state | summary |
|---|---|---|
| 0.2332 | `(1/4,strike) | strike | strike` | intermediate |
| 0.2323 | `(1/4,strike) | strike | work` | intermediate |
| 0.2323 | `(1/4,strike) | work | strike` | intermediate |
| 0.2269 | `(0,strike) | work | work` | zero wage |
| 0.0026 | `(1/4,strike) | strike | if(BOX(s in {1/4}),work,strike)` | intermediate |
| 0.0026 | `(1/4,strike) | if(BOX(s in {1/4}),work,strike) | strike` | intermediate |

Exits from `(1/4,strike) | strike | strike`: strict 0.0e+00, neutral-change 0.0e+00, neutral-keep 3.4e-05, deleterious 0.0e+00; top: W1 work (neutral-keep, 1.6e-05) → intermediate; W2 work (neutral-keep, 1.6e-05) → intermediate; W1 if(BOX(s in {1/4}),work,strike) (neutral-keep, 1.8e-07) → intermediate. Net currents: intermediate>zero wage 8.3e-06; zero wage>scab split 8.2e-06; intermediate>scab split -8.2e-06; fair>intermediate 8.3e-08.

#### Support and transitions: RR_pool0_c0.5_N1000_whack

Whack policy held (implemented): strike 0.000, none 1.000, source 0.000; conditional programs hold 0.073 of π; 99% of π on 77 states.

| π | state | summary |
|---|---|---|
| 0.2332 | `(1/4,strike) | strike | strike` | intermediate |
| 0.2302 | `(1/4,strike) | work | strike` | intermediate |
| 0.2302 | `(1/4,strike) | strike | work` | intermediate |
| 0.2233 | `(0,strike) | work | work` | zero wage |
| 0.0048 | `(1/4,strike) | work | work` | intermediate |
| 0.0026 | `(1/4,strike) | strike | if(BOX(s in {1/4}),work,strike)` | intermediate |

Exits from `(1/4,strike) | strike | strike`: strict 0.0e+00, neutral-change 0.0e+00, neutral-keep 3.4e-04, deleterious 1.3e-67; top: W1 work (neutral-keep, 1.6e-04) → intermediate; W2 work (neutral-keep, 1.6e-04) → intermediate; W1 if(BOX(s in {1/4}),work,strike) (neutral-keep, 1.8e-06) → intermediate. Net currents: intermediate>zero wage 8.0e-05; zero wage>scab split 7.9e-05; intermediate>scab split -7.8e-05; fair>intermediate 1.6e-06.

#### Support and transitions: RR_pool0_c0.5_N100_whack

Whack policy held (implemented): strike 0.000, none 1.000, source 0.000; conditional programs hold 0.072 of π; 99% of π on 89 states.

| π | state | summary |
|---|---|---|
| 0.2312 | `(1/4,strike) | strike | strike` | intermediate |
| 0.2154 | `(1/4,strike) | work | strike` | intermediate |
| 0.2154 | `(1/4,strike) | strike | work` | intermediate |
| 0.1910 | `(0,strike) | work | work` | zero wage |
| 0.0382 | `(1/4,strike) | work | work` | intermediate |
| 0.0161 | `(0,strike) | work | strike` | scab split |

Exits from `(1/4,strike) | strike | strike`: strict 0.0e+00, neutral-change 0.0e+00, neutral-keep 3.4e-03, deleterious 5.5e-09; top: W1 work (neutral-keep, 1.6e-03) → intermediate; W2 work (neutral-keep, 1.6e-03) → intermediate; W1 if(BOX(s in {1/4}),work,strike) (neutral-keep, 1.8e-05) → intermediate. Net currents: intermediate>zero wage 6.3e-04; zero wage>scab split 6.2e-04; intermediate>scab split -5.3e-04; fair>intermediate 6.2e-05.

