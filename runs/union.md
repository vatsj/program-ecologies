# The union game (spec `specs/2026-10-05-union.md`; predictions `predictions/2026-10-05-union.md`, commit 977a6e8)

Code: `src/union.py` (game, grammar, GL evaluator, classes), `src/union_chain.py` (ε→0 chain, reduced dense chain),
`src/union_run.py` (cells, static tables), `src/union_post.py` (fair-state exits, wage fakers), `src/union_abm.py` +
`src/union_abm_run.py` (agent-based and island runs), `src/union_report.py` (tables); tests `tests/test_union.py`
(QUORUM resolves by Löb, union ≡ union′ over the whole tensor, W1/W2 symmetry, and a slot mutant's payoff equals the
pairwise payoff at every intermediate mutant count k = 1..N−1, for every named triple and c). Raw output in
`runs/union/*.json`, chains in `runs/union/*_chain.npz`, everything collected in `runs/union.json`.

## Setup as run

Boss slot n_B = 6 (constants and one-atom conditionals on the workers' play: 297 functions = 297 classes). Worker slots
n_W = 10, the smallest cutoff with the union (452 functions, 364 classes; 54 tagged). PA boxes only. Atoms are boxes
of propositions about the current encounter; workers read the wage through `BOX(s ∈ S)`, the whack policy through
`BOX(h ∈ H)`, the other worker through `BOX(OTHER = a)` and `QUORUM = BOX(s<1/2 → OTHER = strike)`. Masses: scab
0.480, always strike 0.480, militant 1.2·10⁻³, union 9.9·10⁻⁶, union′ 9.9·10⁻⁶, each boss constant 0.108. Arms:
QUORUM, matched no-QUORUM (QUORUM spellings removed, same weights), blind (no reading of the other worker). w = 0.3,
L = 1, c ∈ {0, 0.1, 0.5}, N ∈ {10², 10³, 10⁴}. All 27 chain cells finished (4–13k explored states; outcome-changing
cut 0.1–1.4%). Runs were interrupted once by machine sleep; cells were re-run where outputs were incomplete (4 cells
re-run to fix a reporting bug in the tagged-presence field; π unchanged to all printed digits).

## Static tables (c = 0.5; full tables for every c in `runs/union/static.json`)

Named triples, play and payoffs (boss, W1, W2), and every non-deleterious move that changes play (from the full
static table; neutral moves that keep play omitted):

| triple | play | payoffs | strict (+) and neutral (0) moves out |
|---|---|---|---|
| (0,none) scab scab | W W, zero wage | 2, 0, 0 | B → (0,strike)/(0,source) 0; W → militant 0 (scab split) |
| (0,none) militant scab | S W, scab split | 1, 0, 0 | B → (1/2,·) 0 (fair); W → militant/union 0 (strike); militant → scab 0 |
| (0,none) union scab | W W, zero wage | 2, 0, 0 | W → militant/union 0 (strike); B → (0,strike) 0 |
| (0,none) union union | S S, strike | 0, 0, 0 | B → (1/2,none/strike) +1 (fair); B → (1/2,source) 0 (repression:source); W → scab 0 |
| (0,strike) militant scab | S W, repression:strike | 0.5, 0, −1 | B → (1/2,·) +0.5; W → scab/union +1 |
| (1/4,none) scab scab | W W, intermediate | 1.5, ¼, ¼ | B → (0,·) +0.5 |
| (1/4,none) scab union | W W, intermediate | 1.5, ¼, ¼ | B → (0,·) +0.5; second union −¼ (strikes, deleterious) |
| (1/2,none) scab scab | W W, fair | 1, ½, ½ | B → (0,·) +1, (1/4,·) +0.5 |
| (1/2,none) scab militant | W W, fair | 1, ½, ½ | B → (0,none/source) 0 (scab split) |
| (1/2,none) union scab | W W, fair | 1, ½, ½ | B → (0,·) +1, (1/4,·) +0.5 (the union works beside a scab) |
| (1/2,none) union union | W W, fair | 1, ½, ½ | none against constants (scab 0, keeps play) |
| (1/2,source) union union | W W, repression:source | 0, −½, −½ | B → (1/2,none/strike) +1; W → scab/militant +1 |

The algebra the predictions missed: at s = 1/4 a *second* union strikes and earns 0 against ¼, so it is deleterious;
refusal is neutral only at s = 0, where every worker earns 0 unless whacked, so the constant striker (mass 0.48) and
the militant enter there as freely as the union.

**Reduced canonical-strategy chain** (boss over the 9 constants, workers over {scab, militant, union}): with a
uniform prior, fair 0.31 at every c and N (intermediate ≤ 0.008); with the length prior restricted to these programs,
zero wage 0.997 and fair 0.001. Worker-set ablations (uniform, N = 10³): scab + militant gives fair 0.30 (c = 0) /
0.39 (c = 0.5); scab + union 0.03 / 0.07; scab + union′ 0.14 / 0.14; adding the union to scab + militant gives 0.31 /
0.31. So in the interpretable reference the lone militant carries the fair share, the quorum adds nothing, and the
tagged union does 2–4× worse than its untagged twin because source targeting can see it.

## The ε→0 chain: reading

**π sits at zero wage.** In every arm and cell the wage is 0 in 0.96–0.99 of π; fair (s = 1/2, both work, no whack)
holds 0.001–0.005, intermediate 0.007–0.022, strike 0.07–0.13, scab split 0.28–0.39, realized repression ≤ 0.005
(strike targeting) and ≤ 2·10⁻⁵ (source targeting). Worker mean payoff 0.0025–0.010; boss 1.34–1.57. Efficiency
(total payoff, maximum 2) is 1.36–1.57: the waste is strikes, not whacking. **The three arms agree to three decimals**
(fair at c = 0.5, N = 10⁴: QUORUM 0.0025, no-QUORUM 0.0023, blind 0.0023).

**Support** (c = 0.5, N = 10⁴; 288 states hold 0.99): `(0,strike) | work | work` 0.197, `(0,source) | work | work`
0.112, `(0,none) | work | work` 0.112, the four `(0, none/source)` scab/striker splits 0.090 each, `(0, none/source) |
strike | strike` 0.061 each; then worker conditionals that read the whack policy (`if(BOX(h ∈ {none,source}), strike,
work)` beside a scab under strike targeting, 0.002 each). Conditional programs hold 0.10 of π (worker 0.08, boss 0.02).
The militant is present in 0.002 of π, the union in 1.7·10⁻⁵, union′ in 2.7·10⁻⁵, any tagged worker in 0.003.

**Transitions.** At s = 0 every worker program earns 0 unless whacked, so the worker slots drift neutrally among scab
and striker (0.48 each) at 1.6·10⁻⁵ per event per slot at N = 10⁴, and the boss drifts among (0, strike/none/source)
while nobody strikes. Strike targeting freezes the workers (a striker is whacked, so strikers are deleterious) and is
left only by the boss's own neutral drift. When both workers strike, every boss move is neutral (all earn 0), and once
the boss drifts to s > 0 a scab enters strictly; a boss facing working scabs at s > 0 cuts to 0 strictly
(ρ = 0.26 for 1/2 → 0). Net currents at N = 10⁴, c = 0.5 (per event): zero wage → scab split 1.8·10⁻⁶, scab split →
fair 6.4·10⁻⁷, fair → zero wage 4.0·10⁻⁷ and fair → intermediate 2.6·10⁻⁷, intermediate → zero wage 1.3·10⁻⁶: a net
circulation zero → split → (fair or intermediate) → zero, carried by neutral drift up and a strict cut down, ∝ 1/N.
This is a current in an ergodic chain, not a limit cycle.

**Dwell per visit** (mutation events, c = 0.5): fair 73 / 445 / 3,380, intermediate 177 / 964 / 6,600, zero wage 568 /
5,720 / 56,900 at N = 10² / 10³ / 10⁴; repression states 10–25 events at every N (strict exits). Lumped relaxation
time 331 / 3,320 / 33,500 events, ∝ N.

**The fair states.** At N = 10⁴ the fair mass sits mostly on a scab beside `if(BOX(s ∈ {1/2}), work, strike)` ("work
only if provably fair", mass 1.2·10⁻³), 0.15 of fair each of six orientations; its exits are neutral (the boss's cut
to 0 leaves the boss at 1 either way). The union pair F = `(1/2,none) | union | union` has π 1.4·10⁻¹⁰. Exit rate out
of the fair summary: 1.36·10⁻² / 2.25·10⁻³ / 2.96·10⁻⁴ per unit mass (c = 0.5), slope −0.83 (c = 0: −0.78; c = 0.1:
−0.83; blind arm −0.83).

**A wage faker.** The union's and the militant's wage check `BOX(s ∈ {0,1/4})` is fakeable. 72 boss classes (mass
0.006), all of the form `if(BOX(W_j = work), (1/2, ·), (s<1/2, ·))`, pay below 1/2 to a working union pair (and to a
militant pair and a union′ pair): at the bottom world every box holds, the boss pays 1/2, so "the wage is provably low"
fails at every later world and the workers work, while the boss's own condition (W_j provably works) fails at world 1
and it pays the low wage from then on. At F this is a strict, N-independent exit (2.7·10⁻⁴ per event at c = 0.5; F′
4.0·10⁻⁴), which overtakes the scab's neutral exit (3.3·10⁻⁵ at N = 10⁴) between N = 10³ and 10⁴. The positive
polarity `work iff BOX(s = 1/2)` is not fakeable this way, and it is what holds the fair mass. But a strike pact
needs the positive box of the *low* wage: with ¬□(fair) in its place the pair never resolves its Löb loop (the bottom
world makes every negated box false). In PA alone a union cannot be both Löb-resolvable and unfakeable on the wage.

**The drift race** (per mutation event): union or union′ into a worker slot 1.1·10⁻⁷ / 1.1·10⁻⁸ / 1.1·10⁻⁹ at
N = 10² / 10³ / 10⁴; source targeting into the boss slot 3.4·10⁻⁴ / 3.4·10⁻⁵ / 3.4·10⁻⁶, of which from states with a
tagged worker 1.1·10⁻⁷ / 3·10⁻⁹ / 3·10⁻¹¹ (c = 0.5); strike targeting into the boss slot 1.7·10⁻⁴ / 1.8·10⁻⁵ / 1.8·10⁻⁶
(c = 0.5) and 3.4·10⁻⁴ … at c = 0. Per mutant (ε-free): at `(0,none) scab scab` a union enters at μ/3 · 1/N =
3.3·10⁻⁶/N and needs a second neutral fixation at the same rate; source targeting enters at 0.036/N and needs one.
Repression wins the race by four orders of magnitude per step, but it rarely matters: it is drift with no target,
since the union is almost never there, and the untagged union′ and militant are invisible to it. Source targeting
does suppress the tagged union relative to its twin (union present 1.7·10⁻⁵ against union′ 2.7·10⁻⁵ at c = 0.5,
N = 10⁴; 0.6×), at every c.

**c.** Higher c lowers zero wage (0.64 at c = 0 → 0.48 at c = 0.5) and raises strikes and scab splits, because strike
targeting is neutral against strikers only at c = 0 and so disciplines them there. Efficiency is highest at c = 0
(1.57 against 1.37): cheap repression suppresses strikes. The fair share rises slightly with c (0.0014 → 0.0025 at
N = 10⁴).

## Agent-based runs (finite εN = 0.1 per slot per generation; approach rates, not π)

N = 100 per slot, 10⁵ generations, 3 seeds per (c, start); the same seed numbers are used at every c (common random
numbers, so seeds are correlated across c). Encounter-level time shares: fair 0.001–0.047, intermediate 0.002–0.095,
zero wage 0.23–0.65, strike 0.05–0.24, scab split 0.24–0.50, realized repression ≤ 0.016. From the low-wage start the
first fair majority phase appears at generation 5,540 / 9,530 / 77,580 (c = 0.5), 9,530 / 77,580 / never (c = 0.1),
9,530 / 55,240 / never (c = 0). From the fair start ((1/2,none), union, union) the fair phase holds 580 / 1,130 /
1,350 generations (identical at every c: nothing costs c until someone is whacked). Fair phases last 30–2,300
generations (means 330–2,330); 236–418 phase switches per run. Finite εN shows more fair (up to 0.05) than π
(≤ 0.005), as expected from standing variation.

## Spatial selection on bosses (approach rates)

I = 16 islands, N = 100 per slot, mN = 1, εN = 0.1, 10⁵ generations, low-wage start, 3 seeds (mean ± sd over seeds).
Fair stays at 0.001 in every condition. Boss-slot selection (w_g^B = 10) raises zero wage (c = 0.5: 0.485 → 0.677;
c = 0: 0.905 → 0.972) and lowers strikes and scab splits; it raises the share of the strike-targeting *policy*
(c = 0.5: 0.07 → 0.26) while realized repression stays at 0.002–0.004. Selection on all slots raises zero wage
further (0.789 at c = 0.5), not less. Boss payoff rises (1.39 → 1.61 → 1.77), worker payoff stays ≈ 0. Islands
without selection already sit lower in fair than the single island (0.001 vs 0.01–0.05).

## Verdicts

| # | prediction | outcome |
|---|---|---|
| 1 | fair not drift-closed; leaks through the scab (1/N) then a strict cut; falsifier: no neutral exit or slope steeper than −1.3 | **Held.** Every fair state has a neutral exit; fair exit slope −0.78 to −0.83. Mechanism amended: the fair mass sits on "work iff provably fair" beside a scab (neutral boss cut), and for the union pair a strict N-independent *wage faker* overtakes the scab between N = 10³ and 10⁴ |
| 2 | alternation fair/intermediate/zero ∝ 1/N; fair N-independent within 2×, in [0.2, 0.6]; intermediate ≥ 0.2 | **Failed; falsifier fired** (fair 0.0025 at N = 10⁴, c = 0.5; intermediate 0.009). Fair falls 2.0× from N = 10² to 10⁴. The [0.2, 0.6] range holds only in the reduced chain with a uniform prior (0.31), where intermediate is ≤ 0.008. The stated mechanism also fails: a second union is deleterious at s = 1/4 |
| 3 | fair monotone in c; c = 0 below 0.15; c = 0.1 below c = 0.5 by ≥ 0.1; repression the mirror image | **Failed** on magnitude (c = 0.1 and 0.5 equal to 10⁻³); direction holds (c = 0 lowest at every N, 0.0014 vs 0.0025 at N = 10⁴); falsifier not fired. Realized repression falls with c but is ≤ 0.005 |
| 4 | w_g^B = 10 lowers fair by ≥ 0.15 at c = 0.5; all-slot effect smaller | **Failed** (fair 0.001 in every condition: nothing to lower); falsifier not fired. Sol's alternative holds: boss selection spreads cheap exploitation (zero wage 0.49 → 0.68) and the deterrent strike-targeting policy, not realized repression; the all-slot effect is larger |
| 5 | low start: first fair phase within 10⁴ generations in all seeds (c = 0.5); dwell 10²–10⁴ | **Failed** on first passage (5,540 / 9,530 / 77,580); dwell clause held (330–1,800); falsifier (no fair in 2 of 3 seeds) not fired |
| 6 | no-QUORUM: intermediate ≥ 0.5, fair ≤ 0.15; QUORUM fair higher by ≥ 0.2 | **Failed; falsifier fired** (no-QUORUM equals QUORUM to three decimals; intermediate ≤ 0.022). union′ is the union without the atom; the blind arm (no union at all) is also identical |
| RS | public membership: source targeting strangles the union | **Held in direction, not decisive**: the tagged union is 0.6× as present as its untagged twin in the chain and 2–4× less fair-supporting in the reduced chain; but the union is equally absent without repression (scab drift, rarity, wage faker), and an untagged equivalent exists at the same size |
| A1 | intermediate < 0.05 everywhere (chain) | **Held** (≤ 0.022) |
| A2 | fair < 0.1 everywhere (QUORUM arm) | **Held** (≤ 0.005) |
| A3 | three arms within 0.02 | **Held** (identical to 10⁻³) |
| A4 | realized source repression < 0.01 | **Held** (≤ 2·10⁻⁵) |
## Chain: joint (wage s, work pattern) distribution, quorum arm (whack-policy split in runs/union.json)

| c | N | s=0 both work | s=0 one strikes | s=0 both strike | s=1/4 both work | s=1/4 one strikes | s=1/4 both strike | s=1/2 both work | s=1/2 one strikes | s=1/2 both strike |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 0.617 | 0.277 | 0.074 | 0.018 | 0.004 | 0.002 | 0.004 | 0.002 | 0.001 |
| 0 | 1000 | 0.636 | 0.277 | 0.073 | 0.010 | 6e-04 | 3e-04 | 0.002 | 2e-04 | 1e-04 |
| 0 | 10000 | 0.637 | 0.279 | 0.075 | 0.007 | 1e-04 | 3e-05 | 0.001 | 2e-05 | 1e-05 |
| 0.1 | 100 | 0.491 | 0.353 | 0.116 | 0.021 | 0.006 | 0.003 | 0.005 | 0.002 | 0.002 |
| 0.1 | 1000 | 0.488 | 0.373 | 0.121 | 0.013 | 8e-04 | 4e-04 | 0.003 | 3e-04 | 2e-04 |
| 0.1 | 10000 | 0.491 | 0.375 | 0.122 | 0.009 | 2e-04 | 4e-05 | 0.002 | 9e-05 | 2e-05 |
| 0.5 | 100 | 0.458 | 0.375 | 0.124 | 0.022 | 0.007 | 0.004 | 0.005 | 0.003 | 0.002 |
| 0.5 | 1000 | 0.476 | 0.382 | 0.124 | 0.013 | 9e-04 | 4e-04 | 0.003 | 4e-04 | 2e-04 |
| 0.5 | 10000 | 0.478 | 0.384 | 0.125 | 0.009 | 2e-04 | 4e-05 | 0.002 | 1e-04 | 2e-05 |

Full joint at c = 0.5, N = 10^4 (quorum): s=0, both work, strike 0.2272, s=0, one strikes, none 0.1925, s=0, one strikes, source 0.1917, s=0, both work, none 0.1258, s=0, both work, source 0.1253, s=0, both strike, none 0.0629, s=0, both strike, source 0.0625, s=1/4, both work, source 0.0034, s=1/4, both work, none 0.0033, s=1/4, both work, strike 0.0025, s=1/2, both work, none 0.0011, s=1/2, both work, source 0.0010, s=1/2, both work, strike 0.0004

## Reduced canonical-strategy chain (boss: 9 constants; workers: scab, militant, union)

| c | prior | N | fair | intermediate | zero wage | strike | scab split | repression:strike | repression:source | top states |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | uniform | 100 | 0.308 | 0.006 | 0.545 | 0.009 | 0.125 | 0.002 | 0.005 | (0,strike) scab scab 0.130; (0,strike) scab union 0.110; (0,strike) union scab 0.110 |
| 0 | uniform | 1000 | 0.312 | 0.001 | 0.560 | 0.001 | 0.126 | 0.000 | 0.000 | (0,strike) scab scab 0.134; (0,strike) union scab 0.114; (0,strike) scab union 0.114 |
| 0 | uniform | 10000 | 0.312 | 0.000 | 0.562 | 0.000 | 0.126 | 0.000 | 0.000 | (0,strike) scab scab 0.135; (0,strike) scab union 0.114; (0,strike) union scab 0.114 |
| 0 | mu | 100 | 0.001 | 0.000 | 0.997 | 0.000 | 0.002 | 0.000 | 0.000 | (0,strike) scab scab 0.334; (0,source) scab scab 0.332; (0,none) scab scab 0.331 |
| 0 | mu | 1000 | 0.001 | 0.000 | 0.997 | 0.000 | 0.002 | 0.000 | 0.000 | (0,strike) scab scab 0.334; (0,source) scab scab 0.332; (0,none) scab scab 0.332 |
| 0 | mu | 10000 | 0.001 | 0.000 | 0.997 | 0.000 | 0.002 | 0.000 | 0.000 | (0,strike) scab scab 0.334; (0,source) scab scab 0.332; (0,none) scab scab 0.332 |
| 0.1 | uniform | 100 | 0.325 | 0.007 | 0.543 | 0.010 | 0.112 | 0.000 | 0.003 | (0,strike) scab scab 0.121; (0,strike) union scab 0.119; (0,strike) scab union 0.119 |
| 0.1 | uniform | 1000 | 0.324 | 0.001 | 0.565 | 0.001 | 0.109 | 0.000 | 0.000 | (0,strike) union scab 0.128; (0,strike) scab union 0.128; (0,strike) scab scab 0.126 |
| 0.1 | uniform | 10000 | 0.324 | 0.000 | 0.568 | 0.000 | 0.109 | 0.000 | 0.000 | (0,strike) union scab 0.128; (0,strike) scab union 0.128; (0,strike) scab scab 0.127 |
| 0.1 | mu | 100 | 0.001 | 0.000 | 0.997 | 0.000 | 0.003 | 0.000 | 0.000 | (0,strike) scab scab 0.333; (0,source) scab scab 0.332; (0,none) scab scab 0.332 |
| 0.1 | mu | 1000 | 0.001 | 0.000 | 0.997 | 0.000 | 0.003 | 0.000 | 0.000 | (0,strike) scab scab 0.333; (0,source) scab scab 0.332; (0,none) scab scab 0.332 |
| 0.1 | mu | 10000 | 0.001 | 0.000 | 0.997 | 0.000 | 0.003 | 0.000 | 0.000 | (0,strike) scab scab 0.333; (0,source) scab scab 0.332; (0,none) scab scab 0.332 |
| 0.5 | uniform | 100 | 0.312 | 0.008 | 0.571 | 0.012 | 0.095 | 0.000 | 0.001 | (0,strike) scab union 0.134; (0,strike) union scab 0.134; (0,strike) scab scab 0.126 |
| 0.5 | uniform | 1000 | 0.306 | 0.001 | 0.598 | 0.001 | 0.093 | 0.000 | 0.000 | (0,strike) union scab 0.144; (0,strike) scab union 0.144; (0,strike) scab scab 0.133 |
| 0.5 | uniform | 10000 | 0.306 | 0.000 | 0.601 | 0.000 | 0.093 | 0.000 | 0.000 | (0,strike) scab union 0.145; (0,strike) union scab 0.145; (0,strike) scab scab 0.133 |
| 0.5 | mu | 100 | 0.001 | 0.000 | 0.997 | 0.000 | 0.003 | 0.000 | 0.000 | (0,strike) scab scab 0.333; (0,source) scab scab 0.332; (0,none) scab scab 0.332 |
| 0.5 | mu | 1000 | 0.001 | 0.000 | 0.997 | 0.000 | 0.003 | 0.000 | 0.000 | (0,strike) scab scab 0.333; (0,source) scab scab 0.332; (0,none) scab scab 0.332 |
| 0.5 | mu | 10000 | 0.001 | 0.000 | 0.997 | 0.000 | 0.003 | 0.000 | 0.000 | (0,strike) scab scab 0.333; (0,source) scab scab 0.332; (0,none) scab scab 0.332 |
## Chain: π by disjoint summary (fair / intermediate / zero wage / strike / scab split / repression:strike / repression:source)

| arm | c | N | fair | intermediate | zero wage | strike | scab split | repression:strike | repression:source | efficiency | boss | worker | states | outcome cut |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| quorum | 0 | 100 | 0.004 | 0.018 | 0.617 | 0.077 | 0.279 | 0.005 | 2e-05 | 1.556 | 1.547 | 0.0044 | 13266 | 1.9e-03 |
| quorum | 0 | 1000 | 0.002 | 0.010 | 0.636 | 0.074 | 0.277 | 5e-04 | 2e-06 | 1.575 | 1.568 | 0.0035 | 5256 | 4.8e-03 |
| quorum | 0 | 10000 | 0.001 | 0.007 | 0.637 | 0.075 | 0.279 | 5e-05 | 1e-07 | 1.571 | 1.566 | 0.0025 | 5299 | 1.4e-02 |
| quorum | 0.1 | 100 | 0.005 | 0.021 | 0.491 | 0.121 | 0.361 | 0.001 | 6e-06 | 1.395 | 1.378 | 0.0084 | 13378 | 1.8e-03 |
| quorum | 0.1 | 1000 | 0.003 | 0.013 | 0.488 | 0.122 | 0.374 | 7e-05 | 2e-07 | 1.383 | 1.373 | 0.0049 | 5847 | 4.9e-03 |
| quorum | 0.1 | 10000 | 0.002 | 0.009 | 0.491 | 0.123 | 0.375 | 7e-06 | 1e-09 | 1.380 | 1.373 | 0.0035 | 5731 | 1.4e-02 |
| quorum | 0.5 | 100 | 0.005 | 0.022 | 0.458 | 0.129 | 0.385 | 2e-04 | 1e-06 | 1.356 | 1.337 | 0.0096 | 13259 | 1.7e-03 |
| quorum | 0.5 | 1000 | 0.003 | 0.013 | 0.476 | 0.125 | 0.383 | 2e-05 | 3e-08 | 1.368 | 1.357 | 0.0051 | 5565 | 4.7e-03 |
| quorum | 0.5 | 10000 | 0.002 | 0.009 | 0.478 | 0.125 | 0.384 | 2e-06 | 3e-10 | 1.365 | 1.357 | 0.0036 | 5407 | 1.4e-02 |
| noquorum | 0 | 100 | 0.004 | 0.018 | 0.617 | 0.077 | 0.279 | 0.005 | 0 | 1.556 | 1.547 | 0.0044 | 12297 | 1.7e-03 |
| noquorum | 0 | 1000 | 0.002 | 0.011 | 0.636 | 0.074 | 0.277 | 5e-04 | 0 | 1.575 | 1.568 | 0.0035 | 4851 | 4.4e-03 |
| noquorum | 0 | 10000 | 0.001 | 0.007 | 0.638 | 0.075 | 0.279 | 5e-05 | 0 | 1.572 | 1.567 | 0.0025 | 4936 | 1.3e-02 |
| noquorum | 0.1 | 100 | 0.005 | 0.021 | 0.491 | 0.121 | 0.361 | 0.001 | 0 | 1.395 | 1.378 | 0.0083 | 12432 | 1.6e-03 |
| noquorum | 0.1 | 1000 | 0.003 | 0.013 | 0.488 | 0.122 | 0.374 | 7e-05 | 0 | 1.383 | 1.373 | 0.0049 | 5508 | 4.6e-03 |
| noquorum | 0.1 | 10000 | 0.002 | 0.009 | 0.491 | 0.122 | 0.375 | 7e-06 | 0 | 1.380 | 1.373 | 0.0034 | 5370 | 1.3e-02 |
| noquorum | 0.5 | 100 | 0.005 | 0.022 | 0.458 | 0.129 | 0.385 | 2e-04 | 0 | 1.355 | 1.336 | 0.0095 | 12430 | 1.6e-03 |
| noquorum | 0.5 | 1000 | 0.003 | 0.013 | 0.476 | 0.125 | 0.383 | 2e-05 | 0 | 1.367 | 1.357 | 0.0050 | 5242 | 4.4e-03 |
| noquorum | 0.5 | 10000 | 0.002 | 0.009 | 0.478 | 0.125 | 0.385 | 2e-06 | 0 | 1.365 | 1.358 | 0.0035 | 5040 | 1.3e-02 |
| blind | 0 | 100 | 0.004 | 0.018 | 0.617 | 0.077 | 0.279 | 0.005 | 0 | 1.556 | 1.547 | 0.0044 | 9574 | 1.3e-03 |
| blind | 0 | 1000 | 0.002 | 0.011 | 0.636 | 0.073 | 0.277 | 5e-04 | 0 | 1.575 | 1.568 | 0.0035 | 4121 | 3.3e-03 |
| blind | 0 | 10000 | 0.001 | 0.007 | 0.638 | 0.074 | 0.279 | 5e-05 | 0 | 1.572 | 1.567 | 0.0025 | 4269 | 1.1e-02 |
| blind | 0.1 | 100 | 0.005 | 0.021 | 0.491 | 0.121 | 0.361 | 0.001 | 0 | 1.394 | 1.378 | 0.0083 | 9582 | 1.3e-03 |
| blind | 0.1 | 1000 | 0.003 | 0.013 | 0.489 | 0.121 | 0.374 | 7e-05 | 0 | 1.383 | 1.373 | 0.0049 | 4723 | 3.5e-03 |
| blind | 0.1 | 10000 | 0.002 | 0.009 | 0.491 | 0.122 | 0.375 | 7e-06 | 0 | 1.380 | 1.374 | 0.0035 | 4727 | 1.0e-02 |
| blind | 0.5 | 100 | 0.005 | 0.022 | 0.458 | 0.129 | 0.385 | 2e-04 | 0 | 1.355 | 1.336 | 0.0095 | 9582 | 1.2e-03 |
| blind | 0.5 | 1000 | 0.003 | 0.013 | 0.476 | 0.124 | 0.383 | 2e-05 | 0 | 1.368 | 1.358 | 0.0051 | 4477 | 3.3e-03 |
| blind | 0.5 | 10000 | 0.002 | 0.009 | 0.479 | 0.125 | 0.384 | 2e-06 | 0 | 1.365 | 1.358 | 0.0035 | 4393 | 1.1e-02 |

## Chain: wage and whack-policy distributions, conditional-program mass

| arm | c | N | s = 0 / 1/4 / 1/2 | policy strike / none / source | mass with a conditional (boss / worker) | militant present | union or union′ present | tagged worker present |
|---|---|---|---|---|---|---|---|---|
| quorum | 0 | 100 | 0.968 / 0.025 / 0.007 | 0.404 / 0.298 / 0.298 | 0.104 (0.017 / 0.088) | 0.002 | 5e-05 | 0.004 |
| quorum | 0 | 1000 | 0.986 / 0.011 / 0.002 | 0.409 / 0.295 / 0.295 | 0.099 (0.017 / 0.085) | 0.002 | 5e-05 | 0.003 |
| quorum | 0 | 10000 | 0.991 / 0.007 / 0.001 | 0.407 / 0.297 / 0.296 | 0.094 (0.019 / 0.080) | 0.001 | 5e-05 | 0.003 |
| quorum | 0.1 | 100 | 0.960 / 0.031 / 0.009 | 0.263 / 0.369 / 0.368 | 0.105 (0.017 / 0.089) | 0.003 | 4e-05 | 0.004 |
| quorum | 0.1 | 1000 | 0.982 / 0.014 / 0.004 | 0.247 / 0.377 / 0.376 | 0.098 (0.018 / 0.083) | 0.002 | 4e-05 | 0.003 |
| quorum | 0.1 | 10000 | 0.988 / 0.009 / 0.002 | 0.247 / 0.378 / 0.376 | 0.097 (0.022 / 0.080) | 0.002 | 4e-05 | 0.003 |
| quorum | 0.5 | 100 | 0.957 / 0.033 / 0.010 | 0.222 / 0.390 / 0.388 | 0.105 (0.017 / 0.089) | 0.003 | 4e-05 | 0.004 |
| quorum | 0.5 | 1000 | 0.982 / 0.015 / 0.004 | 0.230 / 0.386 / 0.384 | 0.098 (0.018 / 0.084) | 0.002 | 4e-05 | 0.003 |
| quorum | 0.5 | 10000 | 0.988 / 0.009 / 0.003 | 0.230 / 0.386 / 0.384 | 0.097 (0.022 / 0.080) | 0.002 | 4e-05 | 0.003 |
| noquorum | 0 | 100 | 0.968 / 0.025 / 0.007 | 0.404 / 0.298 / 0.298 | 0.102 (0.017 / 0.085) | 0.002 | 3e-05 | 0 |
| noquorum | 0 | 1000 | 0.986 / 0.011 / 0.002 | 0.409 / 0.295 / 0.295 | 0.097 (0.017 / 0.082) | 0.002 | 3e-05 | 0 |
| noquorum | 0 | 10000 | 0.991 / 0.007 / 0.001 | 0.407 / 0.296 / 0.296 | 0.092 (0.019 / 0.078) | 0.001 | 3e-05 | 0 |
| noquorum | 0.1 | 100 | 0.961 / 0.031 / 0.009 | 0.263 / 0.369 / 0.369 | 0.102 (0.017 / 0.086) | 0.003 | 3e-05 | 0 |
| noquorum | 0.1 | 1000 | 0.982 / 0.014 / 0.003 | 0.247 / 0.376 / 0.376 | 0.096 (0.018 / 0.081) | 0.002 | 3e-05 | 0 |
| noquorum | 0.1 | 10000 | 0.988 / 0.009 / 0.002 | 0.247 / 0.377 / 0.377 | 0.094 (0.022 / 0.078) | 0.002 | 3e-05 | 0 |
| noquorum | 0.5 | 100 | 0.957 / 0.033 / 0.010 | 0.222 / 0.389 / 0.389 | 0.102 (0.017 / 0.086) | 0.003 | 3e-05 | 0 |
| noquorum | 0.5 | 1000 | 0.982 / 0.015 / 0.004 | 0.230 / 0.385 / 0.385 | 0.096 (0.018 / 0.081) | 0.002 | 3e-05 | 0 |
| noquorum | 0.5 | 10000 | 0.988 / 0.010 / 0.002 | 0.230 / 0.385 / 0.385 | 0.095 (0.023 / 0.078) | 0.002 | 3e-05 | 0 |
| blind | 0 | 100 | 0.968 / 0.025 / 0.007 | 0.403 / 0.298 / 0.298 | 0.092 (0.018 / 0.075) | 0.002 | 0 | 0 |
| blind | 0 | 1000 | 0.986 / 0.011 / 0.002 | 0.409 / 0.296 / 0.296 | 0.088 (0.017 / 0.073) | 0.002 | 0 | 0 |
| blind | 0 | 10000 | 0.991 / 0.007 / 0.001 | 0.407 / 0.296 / 0.296 | 0.084 (0.019 / 0.070) | 0.001 | 0 | 0 |
| blind | 0.1 | 100 | 0.961 / 0.031 / 0.009 | 0.262 / 0.369 / 0.369 | 0.092 (0.017 / 0.076) | 0.003 | 0 | 0 |
| blind | 0.1 | 1000 | 0.982 / 0.014 / 0.004 | 0.247 / 0.376 / 0.376 | 0.087 (0.018 / 0.073) | 0.002 | 0 | 0 |
| blind | 0.1 | 10000 | 0.988 / 0.009 / 0.002 | 0.247 / 0.376 / 0.376 | 0.086 (0.022 / 0.069) | 0.002 | 0 | 0 |
| blind | 0.5 | 100 | 0.957 / 0.033 / 0.010 | 0.221 / 0.389 / 0.389 | 0.092 (0.018 / 0.076) | 0.003 | 0 | 0 |
| blind | 0.5 | 1000 | 0.982 / 0.015 / 0.004 | 0.230 / 0.385 / 0.385 | 0.088 (0.018 / 0.073) | 0.002 | 0 | 0 |
| blind | 0.5 | 10000 | 0.988 / 0.010 / 0.002 | 0.230 / 0.385 / 0.385 | 0.087 (0.023 / 0.069) | 0.002 | 0 | 0 |

## Chain: dwell per visit (mutation events) and lumped relaxation time

| arm | c | N | fair | intermediate | zero wage | strike | scab split | repression:strike | repression:source | relaxation |
|---|---|---|---|---|---|---|---|---|---|---|
| quorum | 0 | 100 | 62.5 | 168 | 816 | 169 | 249 | 24.2 | 11.7 | 301 |
| quorum | 0 | 1000 | 338 | 888 | 8.22e+03 | 1.61e+03 | 2.44e+03 | 24.7 | 11.9 | 3.06e+03 |
| quorum | 0 | 10000 | 2.31e+03 | 6.07e+03 | 8.15e+04 | 1.63e+04 | 2.44e+04 | 25.1 | 11.7 | 3.1e+04 |
| quorum | 0.1 | 100 | 79 | 184 | 624 | 207 | 267 | 21 | 11.7 | 338 |
| quorum | 0.1 | 1000 | 482 | 1.01e+03 | 5.96e+03 | 1.98e+03 | 2.65e+03 | 20.8 | 11.4 | 3.36e+03 |
| quorum | 0.1 | 10000 | 3.54e+03 | 6.9e+03 | 5.93e+04 | 1.99e+04 | 2.65e+04 | 20.9 | 12.6 | 3.39e+04 |
| quorum | 0.5 | 100 | 73.4 | 177 | 568 | 209 | 272 | 17.9 | 11.4 | 331 |
| quorum | 0.5 | 1000 | 445 | 964 | 5.72e+03 | 1.98e+03 | 2.66e+03 | 18.9 | 10.4 | 3.32e+03 |
| quorum | 0.5 | 10000 | 3.38e+03 | 6.6e+03 | 5.69e+04 | 1.99e+04 | 2.66e+04 | 20.4 | 10.4 | 3.35e+04 |
| noquorum | 0 | 100 | 60.6 | 168 | 816 | 169 | 248 | 24.1 | – | 301 |
| noquorum | 0 | 1000 | 322 | 892 | 8.21e+03 | 1.61e+03 | 2.44e+03 | 24.7 | – | 3.06e+03 |
| noquorum | 0 | 10000 | 2.3e+03 | 6.07e+03 | 8.15e+04 | 1.62e+04 | 2.44e+04 | 25.1 | – | 3.09e+04 |
| noquorum | 0.1 | 100 | 75.9 | 184 | 622 | 207 | 266 | 21 | – | 338 |
| noquorum | 0.1 | 1000 | 452 | 1.01e+03 | 5.94e+03 | 1.98e+03 | 2.64e+03 | 20.7 | – | 3.36e+03 |
| noquorum | 0.1 | 10000 | 3.38e+03 | 6.9e+03 | 5.92e+04 | 1.98e+04 | 2.64e+04 | 20.8 | – | 3.38e+04 |
| noquorum | 0.5 | 100 | 69.9 | 177 | 567 | 208 | 272 | 17.9 | – | 330 |
| noquorum | 0.5 | 1000 | 415 | 968 | 5.71e+03 | 1.98e+03 | 2.65e+03 | 18.9 | – | 3.32e+03 |
| noquorum | 0.5 | 10000 | 3.14e+03 | 6.6e+03 | 5.68e+04 | 1.98e+04 | 2.65e+04 | 20.3 | – | 3.34e+04 |
| blind | 0 | 100 | 60.8 | 168 | 815 | 169 | 247 | 24.1 | – | 302 |
| blind | 0 | 1000 | 327 | 902 | 8.19e+03 | 1.61e+03 | 2.42e+03 | 24.6 | – | 3.06e+03 |
| blind | 0 | 10000 | 2.31e+03 | 6.09e+03 | 8.14e+04 | 1.62e+04 | 2.43e+04 | 25 | – | 3.09e+04 |
| blind | 0.1 | 100 | 76.1 | 184 | 622 | 207 | 265 | 20.9 | – | 340 |
| blind | 0.1 | 1000 | 457 | 1.02e+03 | 5.94e+03 | 1.97e+03 | 2.63e+03 | 20.6 | – | 3.36e+03 |
| blind | 0.1 | 10000 | 3.42e+03 | 6.95e+03 | 5.91e+04 | 1.98e+04 | 2.63e+04 | 20.7 | – | 3.39e+04 |
| blind | 0.5 | 100 | 70.1 | 177 | 566 | 208 | 270 | 17.7 | – | 332 |
| blind | 0.5 | 1000 | 419 | 977 | 5.7e+03 | 1.98e+03 | 2.64e+03 | 18.7 | – | 3.32e+03 |
| blind | 0.5 | 10000 | 3.17e+03 | 6.64e+03 | 5.68e+04 | 1.98e+04 | 2.64e+04 | 20.1 | – | 3.35e+04 |

## Chain: the drift race (π-weighted flow per mutation event)

| arm | c | N | union or union′ into a worker slot | tagged class into a worker slot | source targeting into the boss slot | of which from states with a tagged worker | strike targeting into the boss slot |
|---|---|---|---|---|---|---|---|
| quorum | 0 | 100 | 1.16e-07 | 1.04e-05 | 3.41e-04 | 1.73e-06 | 3.44e-04 |
| quorum | 0 | 1000 | 1.18e-08 | 9.45e-07 | 3.42e-05 | 1.55e-07 | 3.45e-05 |
| quorum | 0 | 10000 | 1.18e-09 | 8.31e-08 | 3.42e-06 | 8.73e-09 | 3.43e-06 |
| quorum | 0.1 | 100 | 1.07e-07 | 9.84e-06 | 3.30e-04 | 5.16e-07 | 2.05e-04 |
| quorum | 0.1 | 1000 | 1.07e-08 | 8.22e-07 | 3.32e-05 | 1.67e-08 | 1.92e-05 |
| quorum | 0.1 | 10000 | 1.07e-09 | 7.96e-08 | 3.31e-06 | 1.03e-10 | 1.93e-06 |
| quorum | 0.5 | 100 | 1.05e-07 | 9.74e-06 | 3.33e-04 | 1.05e-07 | 1.70e-04 |
| quorum | 0.5 | 1000 | 1.07e-08 | 8.19e-07 | 3.36e-05 | 3.07e-09 | 1.75e-05 |
| quorum | 0.5 | 10000 | 1.07e-09 | 7.94e-08 | 3.35e-06 | 2.96e-11 | 1.76e-06 |
| noquorum | 0 | 100 | 6.83e-08 | 0.00e+00 | 3.41e-04 | 0.00e+00 | 3.44e-04 |
| noquorum | 0 | 1000 | 6.91e-09 | 0.00e+00 | 3.42e-05 | 0.00e+00 | 3.45e-05 |
| noquorum | 0 | 10000 | 6.94e-10 | 0.00e+00 | 3.42e-06 | 0.00e+00 | 3.44e-06 |
| noquorum | 0.1 | 100 | 6.63e-08 | 0.00e+00 | 3.31e-04 | 0.00e+00 | 2.05e-04 |
| noquorum | 0.1 | 1000 | 6.69e-09 | 0.00e+00 | 3.33e-05 | 0.00e+00 | 1.92e-05 |
| noquorum | 0.1 | 10000 | 6.69e-10 | 0.00e+00 | 3.32e-06 | 0.00e+00 | 1.94e-06 |
| noquorum | 0.5 | 100 | 6.60e-08 | 0.00e+00 | 3.34e-04 | 0.00e+00 | 1.70e-04 |
| noquorum | 0.5 | 1000 | 6.68e-09 | 0.00e+00 | 3.37e-05 | 0.00e+00 | 1.75e-05 |
| noquorum | 0.5 | 10000 | 6.69e-10 | 0.00e+00 | 3.36e-06 | 0.00e+00 | 1.76e-06 |
| blind | 0 | 100 | 0.00e+00 | 0.00e+00 | 3.41e-04 | 0.00e+00 | 3.44e-04 |
| blind | 0 | 1000 | 0.00e+00 | 0.00e+00 | 3.43e-05 | 0.00e+00 | 3.45e-05 |
| blind | 0 | 10000 | 0.00e+00 | 0.00e+00 | 3.42e-06 | 0.00e+00 | 3.44e-06 |
| blind | 0.1 | 100 | 0.00e+00 | 0.00e+00 | 3.31e-04 | 0.00e+00 | 2.05e-04 |
| blind | 0.1 | 1000 | 0.00e+00 | 0.00e+00 | 3.34e-05 | 0.00e+00 | 1.92e-05 |
| blind | 0.1 | 10000 | 0.00e+00 | 0.00e+00 | 3.32e-06 | 0.00e+00 | 1.94e-06 |
| blind | 0.5 | 100 | 0.00e+00 | 0.00e+00 | 3.34e-04 | 0.00e+00 | 1.69e-04 |
| blind | 0.5 | 1000 | 0.00e+00 | 0.00e+00 | 3.38e-05 | 0.00e+00 | 1.75e-05 |
| blind | 0.5 | 10000 | 0.00e+00 | 0.00e+00 | 3.37e-06 | 0.00e+00 | 1.77e-06 |

## Agent-based runs (N = 100 per slot, εN = 0.1 per slot per generation, 10⁵ generations; approach rates, not π)

| c | start | seed | encounter-level fair / intermediate / zero wage / strike / scab split / repression:strike / repression:source | majority phase fair / int / zero / strike / split / mixed | first fair phase (gen) | initial phase held (gen) | fair phases: n, mean dwell (gen) | phase switches | boss / worker payoff | efficiency |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | low | 0 | 0.001 / 0.002 / 0.560 / 0.069 / 0.354 / 0.013 / 0.000 | 0.000 / 0.000 / 0.564 / 0.065 / 0.360 / 0.002 | None | zero wage 320 | 0, 0 | 283 | 1.49 / -0.006 | 1.48 |
| 0 | low | 1 | 0.001 / 0.002 / 0.646 / 0.079 / 0.264 / 0.008 / 0.000 | 0.000 / 0.000 / 0.652 / 0.077 / 0.264 / 0.003 | 55240 | zero wage 120 | 1, 30 | 262 | 1.56 / -0.002 | 1.56 |
| 0 | low | 2 | 0.020 / 0.048 / 0.526 / 0.083 / 0.314 / 0.009 / 0.000 | 0.020 / 0.047 / 0.531 / 0.082 / 0.313 / 0.003 | 9530 | zero wage 770 | 1, 1980 | 260 | 1.46 / 0.019 | 1.50 |
| 0 | fair | 0 | 0.007 / 0.008 / 0.550 / 0.077 / 0.342 / 0.015 / 0.001 | 0.006 / 0.006 / 0.553 / 0.074 / 0.345 / 0.003 | 10 | fair 580 | 1, 580 | 304 | 1.47 / -0.002 | 1.47 |
| 0 | fair | 1 | 0.042 / 0.016 / 0.648 / 0.046 / 0.242 / 0.006 / 0.000 | 0.042 / 0.015 / 0.653 / 0.044 / 0.239 / 0.003 | 10 | fair 1130 | 3, 1407 | 236 | 1.61 / 0.022 | 1.65 |
| 0 | fair | 2 | 0.021 / 0.091 / 0.502 / 0.077 / 0.295 / 0.013 / 0.000 | 0.021 / 0.091 / 0.506 / 0.074 / 0.295 / 0.004 | 10 | fair 1350 | 5, 410 | 304 | 1.47 / 0.027 | 1.52 |
| 0.1 | low | 0 | 0.013 / 0.016 / 0.261 / 0.239 / 0.466 / 0.005 / 0.000 | 0.012 / 0.016 / 0.262 / 0.240 / 0.466 / 0.004 | 77580 | zero wage 320 | 3, 410 | 418 | 1.02 / 0.010 | 1.04 |
| 0.1 | low | 1 | 0.001 / 0.016 / 0.564 / 0.107 / 0.308 / 0.005 / 0.000 | 0.000 / 0.014 / 0.570 / 0.106 / 0.305 / 0.003 | None | zero wage 120 | 0, 0 | 298 | 1.46 / 0.003 | 1.47 |
| 0.1 | low | 2 | 0.023 / 0.093 / 0.340 / 0.137 / 0.404 / 0.004 / 0.000 | 0.022 / 0.092 / 0.343 / 0.134 / 0.405 / 0.003 | 9530 | zero wage 770 | 4, 555 | 329 | 1.24 / 0.035 | 1.31 |
| 0.1 | fair | 0 | 0.019 / 0.019 / 0.281 / 0.217 / 0.459 / 0.005 / 0.001 | 0.018 / 0.018 / 0.282 / 0.217 / 0.459 / 0.004 | 10 | fair 580 | 4, 452 | 416 | 1.07 / 0.013 | 1.09 |
| 0.1 | fair | 1 | 0.047 / 0.005 / 0.584 / 0.059 / 0.301 / 0.004 / 0.000 | 0.046 / 0.004 / 0.589 / 0.057 / 0.299 / 0.004 | 10 | fair 1130 | 2, 2325 | 274 | 1.52 / 0.023 | 1.57 |
| 0.1 | fair | 2 | 0.021 / 0.095 / 0.428 / 0.121 / 0.330 / 0.005 / 0.000 | 0.021 / 0.095 / 0.429 / 0.119 / 0.332 / 0.003 | 10 | fair 1350 | 5, 418 | 308 | 1.35 / 0.033 | 1.42 |
| 0.5 | low | 0 | 0.014 / 0.018 / 0.237 / 0.237 / 0.493 / 0.001 / 0.000 | 0.013 / 0.018 / 0.234 / 0.234 / 0.495 / 0.004 | 77580 | zero wage 320 | 4, 332 | 401 | 1.00 / 0.014 | 1.03 |
| 0.5 | low | 1 | 0.036 / 0.023 / 0.502 / 0.082 / 0.354 / 0.002 / 0.000 | 0.036 / 0.022 / 0.506 / 0.080 / 0.354 / 0.003 | 5540 | zero wage 120 | 2, 1785 | 279 | 1.43 / 0.024 | 1.48 |
| 0.5 | low | 2 | 0.022 / 0.017 / 0.376 / 0.161 / 0.423 / 0.002 / 0.000 | 0.022 / 0.015 / 0.381 / 0.158 / 0.420 / 0.004 | 9530 | zero wage 770 | 4, 540 | 355 | 1.22 / 0.017 | 1.25 |
| 0.5 | fair | 0 | 0.020 / 0.018 / 0.234 / 0.229 / 0.498 / 0.001 / 0.000 | 0.019 / 0.018 / 0.231 / 0.226 / 0.501 / 0.004 | 10 | fair 580 | 5, 382 | 390 | 1.00 / 0.019 | 1.04 |
| 0.5 | fair | 1 | 0.047 / 0.003 / 0.546 / 0.073 / 0.330 / 0.002 / 0.000 | 0.046 / 0.001 / 0.551 / 0.070 / 0.328 / 0.003 | 10 | fair 1130 | 2, 2325 | 298 | 1.47 / 0.024 | 1.52 |
| 0.5 | fair | 2 | 0.021 / 0.018 / 0.447 / 0.164 / 0.348 / 0.002 / 0.000 | 0.020 / 0.017 / 0.452 / 0.163 / 0.344 / 0.004 | 10 | fair 1350 | 5, 406 | 350 | 1.29 / 0.016 | 1.32 |

## Spatial selection on bosses (I = 16, N = 100 per slot, mN = 1, εN = 0.1, 10⁵ generations, low-wage start; approach rates)

| c | w_g (B, W1, W2) | fair | intermediate | zero wage | strike | scab split | repression:strike | repression:source | s = 1/2 (any policy) | policy strike / none / source | boss / worker payoff | efficiency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0, 0, 0 | 0.001 ± 0.000 | 0.003 ± 0.000 | 0.905 ± 0.036 | 0.009 ± 0.003 | 0.078 ± 0.032 | 0.004 ± 0.000 | 0.000 ± 0.000 | 0.001 ± 0.000 | 0.485 ± 0.090 / 0.267 ± 0.011 / 0.247 ± 0.091 | 1.897 ± 0.039 / -0.001 ± 0.000 | 1.896 ± 0.039 |
| 0 | 10, 0, 0 | 0.001 ± 0.000 | 0.002 ± 0.000 | 0.972 ± 0.002 | 0.001 ± 0.000 | 0.020 ± 0.002 | 0.004 ± 0.000 | 0.000 ± 0.000 | 0.001 ± 0.000 | 0.699 ± 0.006 / 0.161 ± 0.016 / 0.140 ± 0.019 | 1.972 ± 0.002 / -0.001 ± 0.000 | 1.971 ± 0.002 |
| 0 | 10, 10, 10 | 0.001 ± 0.000 | 0.005 ± 0.003 | 0.967 ± 0.006 | 0.001 ± 0.001 | 0.022 ± 0.006 | 0.004 ± 0.000 | 0.000 ± 0.000 | 0.001 ± 0.000 | 0.672 ± 0.032 / 0.154 ± 0.025 / 0.174 ± 0.041 | 1.968 ± 0.007 / -0.000 ± 0.001 | 1.967 ± 0.007 |
| 0.5 | 0, 0, 0 | 0.001 ± 0.001 | 0.009 ± 0.005 | 0.485 ± 0.016 | 0.100 ± 0.013 | 0.403 ± 0.006 | 0.002 ± 0.000 | 0.000 ± 0.000 | 0.004 ± 0.001 | 0.071 ± 0.020 / 0.404 ± 0.065 / 0.525 ± 0.068 | 1.386 ± 0.029 / 0.003 ± 0.001 | 1.392 ± 0.030 |
| 0.5 | 10, 0, 0 | 0.001 ± 0.000 | 0.003 ± 0.000 | 0.677 ± 0.036 | 0.067 ± 0.013 | 0.249 ± 0.023 | 0.003 ± 0.000 | 0.000 ± 0.000 | 0.002 ± 0.000 | 0.262 ± 0.040 / 0.390 ± 0.031 / 0.348 ± 0.071 | 1.609 ± 0.049 / -0.000 ± 0.000 | 1.609 ± 0.049 |
| 0.5 | 10, 10, 10 | 0.001 ± 0.000 | 0.024 ± 0.006 | 0.789 ± 0.041 | 0.025 ± 0.009 | 0.157 ± 0.026 | 0.003 ± 0.000 | 0.000 ± 0.000 | 0.002 ± 0.000 | 0.363 ± 0.031 / 0.326 ± 0.014 / 0.311 ± 0.043 | 1.773 ± 0.047 / 0.005 ± 0.002 | 1.784 ± 0.044 |

Per-seed fair and zero-wage shares: c=0 w_g=0-0-0: 0.001/0.935, 0.001/0.855, 0.001/0.926; c=0 w_g=10-0-0: 0.001/0.974, 0.001/0.972, 0.001/0.969; c=0 w_g=10-10-10: 0.001/0.976, 0.001/0.961, 0.001/0.964; c=0.5 w_g=0-0-0: 0.001/0.507, 0.002/0.475, 0.001/0.472; c=0.5 w_g=10-0-0: 0.001/0.675, 0.001/0.634, 0.001/0.723; c=0.5 w_g=10-10-10: 0.001/0.819, 0.001/0.816, 0.001/0.731
