# The inspection game's enforcer and its shadow (notes, 2026-10-24)

Spec `specs/2026-10-24-inspection-shadow.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both folded).
Builds on `specs/2026-10-23-two-role-mixed.md`, `notes/mixed2.md`, `runs/mixed2.md` and RESULTS "Mixed actions in
two-role games". §1 is written by hand before any code of this run and before any counted cell. §2 (choices where the
spec is silent, and deviations) is appended with the code, before any counted cell. §3 records facts found while
running.

**What §1 used.** No chain was solved and no lottery was run for §1. The numbers below are evaluations of the formulas
written next to them on the static class tables of the finished two-role run (`insp`, exact arm, n = 8, D = 12; the
cached tables of that run, loaded read-only with `mixed2.get_arm`). Those evaluations were one-state calculations
(the outflow of a given class pair under the Moran fixation of `mixed2.lrho`, w = 0.3, rates per mutation event, the
mutant's role chosen with probability 1/2), made in an uncommitted scratch script before this file was written; the
code of step 3 recomputes every one of them (a test pins them). Everything about the *stationary* chain is not in §1.
The previous run's top states (`runs/mixed2/chain_insp_exact_c0_full.json`) were read for the shape of the π mass
(they are published results, not part of this run).

## 1. Hand derivations

### 1.0 Definitions

* Game: inspector (role 0) I or N, inspectee (role 1) C or K; payoffs (I, C) = (−1, 0), (I, K) = (−1, −3),
  (N, C) = (0, 0), (N, K) = (−4, 1); with inspection probability p and cheating probability q,
  U_insp = −p − 4(1 − p) q, U_ee = q (1 − 4p). A visible p > 1/4 deters cheating; q < 1/4 is tolerated by an exact
  best-responding inspector (it does not inspect unless q > 1/4).
* **E** (payoff-efficient): a class pair with both mean game payoffs ≥ −0.05. **R ⊂ E**: E states whose inspector class
  *deters* the constant cheater, P(inspect | K) > 1/4 (the functional meaning of "responsive enforcement present":
  `K` earns less than `C` against it). The strict version **R\*** has P(inspect | K) = 1 and P(inspect | C) = 0
  (`cr(THEM(ME))` and its sampled and nested relatives). **E \ R** are the efficient states whose inspector does not
  deter `K`: `N` and its twins that inspect `K` with probability ≤ 1/4.
* Rates are per mutation event; a mutant of class q arrives with probability μ_r(q)/2 (role r, prior mass μ_r) and
  fixes with Moran probability ρ_N(Δ) = (1 − e^(−wΔ))/(1 − e^(−NwΔ)), w = 0.3, ρ_N(0) = 1/N. Neutral = Δ = 0 in net
  payoff (to 10⁻⁹), strict = Δ > 0.
* Prior masses (class level, `insp` exact arm, c = 0; c = 0.01 differs in the fourth decimal): inspector `N` 0.30696,
  `I` 0.36803, `cr(THEM(ME))` class 0.00135; inspectee `C` 0.37887, `K` 0.29703.

### 1.1 Twin relations and charged costs

`CRI = cr(THEM(ME))` (inspector): one application level against a non-reader, so it is charged c once against `C`;
`N` is a constant, charged nothing.

| state | payoffs at c = 0 (inspector, inspectee) | net payoffs at c = 0.01 |
|---|---|---|
| (CRI, C) | (0, 0), cost 1 level | (−0.01, 0) |
| (N, C) | (0, 0), cost 0 | (0, 0) |

* **c = 0: exact payoff twins against `C`.** 38 inspector classes have net payoff 0 against `C` (those of `CRI`, `N` and
  their relatives), total prior mass 0.3105. They split into `N` alone 0.30696, deterring classes (P(inspect | K) > 1/4;
  the class of `cr(THEM(ME))` itself, `cr(THEM(^I))`, `cr(THEM(^N))`, `cr(THEM(^X))`, `if(THEM(ME)=C, N, I)`,
  `cr(coin(C, THEM(ME)))`, the half-strength `coin(N, cr(THEM(ME)))`, …) 0.00332, and non-deterring others (the
  constant `N`'s relatives that inspect `K` with probability 0 or exactly 1/4, e.g. `if(THEM(ME)=C, N, N)`,
  `coin(N, coin(N, cr(THEM(ME))))`) 0.00024. Against `K` they differ: `N` gets (−4, +1), `CRI` gets (−1, −3). So the drift
  `CRI → N` at (CRI, C) is selectively neutral, with rate ½ · 0.3072 / N = 0.1536/N per event, and the reverse
  `N → deterring twin` has rate ½ · 0.00332/N: the prior makes the neutral network about 93 : 1 in favour of the
  shadow. Both states are in E; only the first is in R.
* **c = 0.01: not twins.** `N` is the unique inspector class with net payoff 0 against `C` (checked on the class table:
  1 class); every reading class pays at least one level. So `N` invades (CRI, C) by *selection*, Δ = +0.01, wΔ = 0.003:
  ρ_N = 0.0116 / 0.00315 / 0.002996 / 0.002996 at N = 10² / 10³ / 10⁴ / 10⁵ against neutral 0.01 / 10⁻³ / 10⁻⁴ / 10⁻⁵
  (excess 1.2 / 3.2 / 30 / 300). Hazard of leaving R by `N`: ½ · 0.3069 · ρ_N = 1.77·10⁻³ / 4.8·10⁻⁴ / 4.6·10⁻⁴ /
  4.6·10⁻⁴: it stops falling with N at N ≈ 3/(wΔ) ≈ 10³ (slope −0.55 between 10² and 10³, ≈ 0 above).
* **The prudent inspectee against the same pair** (§1.4): against `CRI` it plays C but pays two levels (`THEM(^K)`
  runs `CRI`'s body, which runs `K`'s), against `N` it plays K and pays one. At c = 0 it is an exact payoff twin of `C`
  against `CRI` (0) and strictly better against `N` (+1 against 0). At c = 0.01, against `CRI` it earns −0.02 against
  `C`'s 0: `C` invades it by selection (wΔ = 0.006), so the shield erodes at c = 0.01 where at c = 0 it only drifts.

### 1.2 Expected exits from R and E (one-state calculations, N = 10⁴ unless stated)

**From (CRI, C), c = 0** (a state of R\*): per event,

| move | rate | scaling in N |
|---|---|---|
| inspector twin drift (mostly `N`) | 1.55·10⁻⁵ (= 0.1546/N) | ∝ 1/N, slope −1 |
| inspector strict invader | none | — |
| inspectee strict invaders | 7.4·10⁻⁵ | N-independent for N ≥ 100 |
| deleterious moves | < 10⁻⁷ at N ≥ 10³ | vanishing |

The inspectee strict invaders are **not** the constant cheater (it is deleterious against an inspecting `CRI`); they are
(a) light cheaters whose cheating probability is below the exact reader's threshold: `coin(C, coin(C, X))` (q = 1/8, mass
0.0025, rate 4.6·10⁻⁵), `coin(C, coin(C, coin(K, X)))` (q = 3/16), `coin(C, coin(C, coin(C, X)))` (q = 1/16), earning
q > 0 against an inspector that does not inspect below 1/4, and (b) readers that exploit the bounded read of `cr`
(`cr(coin(N, THEM(ME)))` et al.: Δ ≈ +0.99, mass 0.00012, rate 1.5·10⁻⁵), the "possible fakers through
mutual-reading forfeits" of the spec. **Crossover:** the neutral hazard equals the strict one at
N* ≈ 0.1546 / 7.4·10⁻⁵ ≈ 2.1·10³. Below N*, the largest exit from R is the neutral drift of `N` (Prediction 1);
above N*, the largest exit from R is a strict invasion by a light cheater or exploit reader, which is Prediction 1's
first falsifier. Both states reached by that route are outside E (inspector payoff −4q ≈ −0.5…−0.75) and are
*not* the shadow's cycle: (CRI, light cheater) has no strict inspector improver (the inspector payoff −p − 4(1−p)q is
maximal at p = 0), so it rests until `N` drifts in (neutral, 1.5·10⁻⁵/event) or an exploit reader invades (1.9·10⁻⁵):
total exit 3.5·10⁻⁵/event (mean sojourn ≈ 3·10⁴ events at N = 10⁴). This is the structure of the previous run's top states
(`CRI` against `coin(C, coin(C, X))` with payoffs (−0.5, 0.125) holds 0.10 of π at N = 10⁴).

**From (CRI, C), c = 0.01:** `N` invades by selection, 4.6·10⁻⁴/event at N ≥ 10⁴ (slope ≈ 0), plus the same inspectee
invaders (7.2·10⁻⁵). The largest exit from R is strict at c = 0.01 at every N ≥ 10³.

**From (N, C) ∈ E \ R** (both prices, N-independent): strike by strictly beneficial inspectees, 0.0609/event (`K` 0.0385,
`X` and mixers the rest). The reverse drift back to a deterring twin is 1.8·10⁻⁷/event (N = 10⁴): the shadow is left
by the cheater, not by a return to enforcement. So the stationary mass of (N, C) within E is (entry) / (strike) =
(0.1546/N)/0.0609 ≈ 2.5/N, and the E-exit flux through the shadow is the entry flux 0.1546/N (every shadow entry is
struck, with probability ≈ 1).

**From (N, K) (shadow exploited):** all inspector classes that inspect `K` with positive probability invade strictly:
0.168/event, N-independent. **Branching back** (by prior mass, because strict gains are comparable): from (N, K) the
inspector goes to a constant `I` (mass 0.368) or a committed or responsive class in proportion to prior mass; (I, K) goes
to (I, C) (`C` and compliant classes, mass ≈ 0.38) and (I, C) to (N, C) or (CRI-like, C) in proportion 0.307 : 0.0033, so
**about 1% of loops of the four-cycle (N, C) → (N, K) → (I, K) → (I, C) → (N, C) reach R**; a loop takes of the order of
10 events, so a return to R takes of the order of 10³ events, independent of N. With that return time the shadow
route alone gives P(E) ≈ 1 − (10³ × 0.15/N) at large N (odds ∝ N); the light-cheater route above adds a state that
is left only at ≈ 3.5·10⁻⁵/event.

**Engineer's expectation for the stationary chain (not binding on the registered predictions).** The shadow exit
(neutral, ∝ 1/N, O(1) return) predicts odds of P(E) rising roughly ∝ N. The light-cheater trap predicts the
opposite at large N: its entry is N-independent (7.4·10⁻⁵ per event from R), its exit about 3.5·10⁻⁵/event, so P(E) is
set by R's sojourn ≈ 1/(0.1546/N + 7.4·10⁻⁵) (4.4·10³ at N = 10³, 1.1·10⁴ at 10⁴, 1.3·10⁴ at 10⁵) against the trap's ≈ 3·10⁴
and the loops: the odds of E fall for N ≥ 10⁴. I expect Prediction 2's slope (< 0.5) to hold, and for a reason other than
the one it states, and Prediction 1's R-clause to hold at N = 10³ only.

### 1.3 Controls: what the twin relation implies for the arms

* `exact_er` (only the inspector reads): the inspectee has constants, `X`, `coin`; the light cheaters survive (they are
  non-readers); the prudent class does not exist; expect the same shadow and light-cheater structure, no punishing
  inspectee.
* `blind`: no reader, no twin of a responsive inspector; the matching-pennies cycle among constants.

### 1.4 The boosted prudent inspectees, program by program

Definition: inspectee classes that play C with probability 1 against `cr(THEM(ME))` (no forfeit) and K with probability
1 against `N` (no forfeit). On the exact arm, n = 8, there are 8 such classes (38 member spellings, total prior mass
0.000738; the same eight at c = 0 and c = 0.01), all of which read the inspector *through a probe* (`THEM(^B)`:
the inspector's action against a lifted inspectee program B), never through `THEM(ME)`, so they do not forfeit
against a reader:

| representative | members | mass | against `I` / `N` / `X` / `P14` / `P38` / `CRI` / `RI` (P(cheat)) |
|---|---|---|---|
| `cr(THEM(^K))` | 9 | 0.000306 | 0 / 1 / 0 / ½ / 0 / 0 / 0 |
| `cr(THEM(^X))` | 8 | 0.000274 | 0 / 1 / 0 / ½ / 0 / 0 / 0 |
| `if(THEM(^K)=I, C, K)` | 5 | 0.000032 | 0 / 1 / ½ / ¾ / 0.62 / 0 / 0 |
| `cr(coin(N, THEM(^K)))` | 4 | 0.000028 | 0 / 1 / ½ / 1 / 1 / 0 / 0 |
| `if(THEM(^X)=I, C, K)` | 4 | 0.000028 | 0 / 1 / ½ / ¾ / 0.62 / 0 / ½ |
| `cr(THEM(^coin(C, X)))` | 3 | 0.000025 | 0 / 1 / 0 / ½ / 0 / 0 / ½ |
| `cr(coin(N, THEM(^X)))` | 3 | 0.000025 | 0 / 1 / ½ / 1 / 1 / 0 / ½ |
| `cr(THEM(^coin(K, X)))` | 2 | 0.000021 | 0 / 1 / 0 / ½ / 0 / 0 / 0 |

Behaviour: they comply against inspectors that would inspect a probing cheater (a probe `K` or `X` is inspected by
`CRI`, `I`, `X`, `P38`), and cheat against inspectors that would not (`N`). Against `CRI` and `N` they behave exactly as
asked; against the sampled responder `RI` and a few others they mix (the table above). Costs: 2 levels against `CRI`,
1 against `N`, 1 against `I`. Payoff against `N`: +1 (strictly beats `C`); against `CRI`, `I`, `P38`: 0 (twin of `C`) at c = 0.
The shield is a probe, not the real opponent: an inspector that inspects probes but not the real inspectee would fake
it; the exit table tracks strict invasions by reading classes apart from constants, so such a faker would show there.

**Boost, exactly.** Let S be the set above, m(S) = 0.000738 the class-level prior mass (the prior is over spellings and
every spelling of a class is multiplied by the same factor). Boosted prior: m′(S) = 10 m(S) = 0.007380, added mass
Δ = 9 m(S) = 0.006642, taken from all inspectee classes outside S proportionally (so `C` also shrinks by the factor
(1 − m(S) − Δ)/(1 − m(S))). **Control:** the same Δ added to the class of `C` (all its spellings scaled by the same
factor, so m′(C) = m(C) + Δ), taken from all inspectee classes outside `C` proportionally (so S shrinks too). Both are
prior changes at the class level; in the chain they replace `A.mass[1]`, in the lottery they reweight the founder draw
(program-level weights = the class factor, size-then-quantile inverse-CDF with the same uniforms as the unboosted draw,
which reproduces the unboosted founders exactly when the factors are 1).

**Expectation.** m′(S) = 0.0074 is of the same order as the mass of deterring inspector twins (0.0033) and of the light
cheaters that exit R (0.0031). It addresses only the shadow route (it punishes `N` after the shadow enters), not the
light-cheater route, which is a cheater that a *responsive* inspector tolerates. I expect an effect on chain P(E) at
N = 10⁴ of a few points, not 0.1, and a larger one in the lottery where the shadow is the exit.

### 1.5 What this fixes for the tests

* The twin relation of `N` and `CRI` against `C` at c = 0 (payoff 0, 0, cost 1 vs 0) and at c = 0.01 (−0.01 vs 0).
* The strict-versus-neutral classification of (CRI, C) exits at N = 10⁴ (§1.2 numbers to 3 digits).
* The 8 prudent classes of §1.4, their masses, and the exactness of the boost and of the matched control (same Δ).
* The exit decomposition on a toy chain (rates sum to the total; categories partition).

## 2. Choices where the spec is silent, and deviations (written with the code, before any counted cell)

*Disclosure.* Before this section was committed I ran, besides the one-state calculations of §1: (i) the unit tests of
`tests/test_inspection_shadow.py` (solver, twin relation, priors, decomposition against brute force, lottery kernel);
(ii) scratch validations of the blocked solver on random chains, of float32 against float64 storage on a 6,400-state
sub-arm of the exact arm (80 × 80 classes, N = 10² … 10⁵; scratch only), of the (100, 64) lottery against the previous run (runs 0–2 reproduce
`lot_insp_exact_c0_primary` bit for bit at generation 2,000), of one direct-start sandbox cell, and of the exact-arm
chain at c = 0 and N = 10³ (scratch output, not in `runs/`; it is rerun as a counted cell). None changed a prediction, a
scoring convention or a cell of the spec. The predictions file was committed before any code existed.

**Choices.**
1. **The twin-expanded distribution is vacuous in this chain.** `TwoPopChain` has monomorphic states only, and its classes
   are the programs with equal net-payoff rows and columns against *every* program of the other role (`mixed2.collapse`), so
   twin spellings inside a class are exactly interchangeable and the class-level π is the twin-expanded π summed over
   spellings (spellings share a class in proportion to their prior). The twin drift that matters here, between distinct
   classes that are payoff twins *at the current state* (`N` and `CRI` against `C`), is inside the chain as a Δ = 0 move with
   fixation probability 1/N. The polymorphic-state corrections of IMPLEMENTATION §4 (lumped-resident fixation, polymorphic traps)
   do not arise because no state is polymorphic; this is also why the exit decomposition is exact.
2. **Whole state space, not exploration.** The chain is solved on all 157 × 157 (c = 0) or 167 × 167 (c = 0.01) pairs. This
   is stronger than "closure-seeded exploration with support diagnostics": there is nothing unexplored. Support diagnostics
   reported: the number of pair states carrying 0.99 of π, the balance residual of the global-balance equations in float64
   (max relative residual over states with π above 10⁻¹⁴ of the maximum), and the circulation index. The solver is a **blocked
   subtraction-free GTH** (block 128; trailing updates by GEMM) that returns the stationary vector, and in the same elimination
   pass the *censored chain* on the kept set (E ∪ named starts) with reward vectors, from which the first-passage statistics
   follow exactly (tested against dense linear algebra to 10⁻¹²). Validation against the previous run's solver is the
   positive control below. The previous run's whole-space numbers (−0.777 / −0.496 / −0.471 at c = 0, N = 10² / 10³ / 10⁴;
   −0.632 / −0.623 at c = 0.01) are reproduced as controls and reported in the table.
3. **Float32 storage of the jump-chain matrix for the whole-space solves.** The exploration audit (queue 57) runs 3 processes
   of up to 5–7 GB; the machine has 16 GB; a float64 matrix of 24,649² entries is 4.9 GB (6.2 GB at c = 0.01) and a first
   float64 attempt was killed when the system started to swap. Probabilities are stored in float32 (2.4 / 3.1 GB), the
   stationary vector, rewards and everything downstream in float64. On the 6,400-state sub-arm the float32 and float64 solutions
   differ by at most 1.9·10⁻⁶ relative on states with π > 10⁻⁹ (sum |Δπ| ≤ 3·10⁻⁷) at every N from 10² to 10⁵. The balance residual of
   every cell is reported; where a float64 re-run of a cell was possible it is reported beside the float32 one. Each
   chain file records its dtype.
4. **Sets.** E, R, R\*, E\* exactly as in the predictions file. R is defined by P(inspect | K) > 1/4 because that is what
   decides whether the constant cheater is a strict invader of (a, C); the strict version R\* (inspects K with probability 1
   and C with probability 0) is reported beside it. All set-crossing statistics use the net-payoff Δ for fate (so at c = 0.01
   the cost of reading is a selective difference) and the *gross* payoffs for membership of E.
5. **The exit categories** are those of the predictions file; "reading" means the class contains `THEM` (the mutant's
   syntactic flag `A.reader`); the forfeit-driven subset of category E is any mutant that forfeits with resident mass above 0.05 or
   whose resident inspector does. Fixation probabilities of the reference states (CRI, C), (N, C), (N, K) are reported
   per mutant class (`reference_exits`). Mean first-passage times are in mutation events (one mutation event = one arrival of
   a mutant in either role).
6. **Detours** are the exclusive categories forfeit > shadow excursion > cheater-majority (other) > light cheater > committed
   and compliant > mixing > other, defined on the pair state's mean inspection and cheating probabilities (conditional on acting);
   "light cheater" is 0.02 < q ≤ 0.25 with p ≤ 0.02; "shadow excursion" is q > 0.5 with a non-deterring inspector class;
   "committed and compliant" is p > 0.25 and q < 0.1; "mixing" is an individually mixing class on either side (non-degenerate
   probability against its partner).
7. **Lottery cells.** The (100, 64) and (400, 16) baseline cells use the previous run's founder and dynamics seed names
   (`primary`, `size`), so their dynamics up to generation 2,000 are identical to the previous run's (checked); the (800, 8)
   and (400, 64) cells have their own seed names. Horizon 20N: 2,000 / 8,000 / 16,000 / 8,000. Checkpoints: a common-t grid,
   a common t/N grid, and every N/10 generations over the last N generations. Runs: 40 at (100, 64), 20 elsewhere. Founders
   are paired across prices and arms through the shared uniforms. mN = 1 means a migration probability of 1/N per birth event.
8. **Rain.** "εN = 0.05 per generation": each birth event in the inspectee seat is, with probability 0.05/N, a newborn of the
   rain class (K or C) instead of a draw from the island; N births per island per generation, so 0.05 rain individuals per island
   per generation. The K rain and the C rain use the same random-number consumption (tested by a label-swap identity), so
   they differ in the class only. Rain applies at all times from generation 0 (founders as in the baseline).
9. **Prudent boost and control.** As in §1.4: class-level exact masses; in the chain they replace the inspectee mutation
   prior; in the lottery they reweight the founder draw with the class factor (the same uniforms as the unboosted draw: the
   reweighted size distribution, then the reweighted spelling mass within the size). The boost changes founders and mutation
   in the sense that the lottery has founders only and the chain has mutations only; the spec's "founder-only and mutation-only"
   split (gpt-6.1-sol, not folded into the design) is therefore automatic across the two objects. Not run: a boost of the
   mutation prior inside the lottery (the lottery has none).
10. **Direct starts.** Each island starts with N − n inspectors of the base class and n of the other twin (n ∈ {1, N/10,
    N/2}) and N compliant inspectees; no mutation; no migration; I = 64 islands, 20 runs; with K = 1 a single K individual
    replaces a uniformly chosen inspectee in every island at generation 100. This reads "shadow fixation, cheater establishment
    and recovery" as: twin fixation by drift (base `CRI` with `N` injected, and the reverse), K's establishment where the
    shadow holds the seat, and whether responsive inspectors hold the seat afterwards. In a closed island with no mutation
    "recovery" needs surviving responsive inspectors; it is therefore measured where the twin injection leaves some.
11. **Jobs.** `src/inspection_shadow_batch.py` runs the job file `runs/inspection_shadow/jobs.txt` as separate processes (no
    pool): at most 3 at a time and 2 while the audit's processes exist (`ps` is re-read before every launch), one whole-space
    chain at a time, gated by estimated memory against available memory.

**Cut order** (spec): N = 10⁵, (800, 8), the crossed (400, 64) cell, mN = 10, the c = 0.01 remedy cells. None cut at this point.
