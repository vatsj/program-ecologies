# Solver audit of the published ε→0 chains, with independent deep-state discovery (2026-10-05/06)

Spec `specs/2026-10-05-solver-audit.md` (reviewed by gpt-6.1-sol); predictions `predictions/2026-10-05-solver-audit.md`
(committed ddb080e, before any re-solve). Code `src/chain_log.py` (LogChain: `chain.Chain`'s transition model with
every edge also kept as a log weight; log-domain GTH; mpmath GTH; closed classes), `src/solver_audit.py` (discovery,
published re-run, rate and solver checks, seeded re-solve, twins, union and three-player commands, report), tests
`tests/test_solver_deep.py`. Per-cell JSON in `runs/solver_audit/`, merged in `runs/solver-audit.json`; generated
tables in `runs/solver-audit-tables.md`. Statistics: dollar cells P(efficient) (`eff`) and the 1/2–1/2 encounter share
(`half`); PD cells P(C,C). w = 0.3 everywhere.

## 0. What ran, what did not, and deviations

Ran: both regression tests; the controls (positive: modal dollar n = 7, N = 10⁴; negative: exhaustive {C, FairBot}
and {D, C, FairBot} in the modal PD; precision instance {S3, S5, A5}); the twelve one-population dollar cells
(`dollar5`/`dollar3` × `norole`/`role` × N = 10³, 10⁴, 3·10⁴); the PD cells (modal n = 9 at 10⁴ and 3·10⁴; weak L_6
at 10⁴; priced c = 0.01 at 10⁴ in three variants: atoms n = 6, atoms n = 8, lazy n = 8; K b = 16 at n = 8, 10⁴); the
union QUORUM cell (c = 0.5, N = 10³); the twin intervention on all four dollar arms and the modal dollar cell at
N = 10⁴ and 10⁵. The three-player modalPA cell: see §6 (status stated there).

Deviations, each forced by a result and stated as a limit:
1. **Discovery beyond three classes.** The spec's enumeration (every singleton, pair and triple, exhaustive in every
   cell, 107 M triples in the modal PD) found *no* strictly deep state and almost no trap in any dollar cell: the
   dollar traps have 4–6 classes. I added an **invasion closure** (from every monomorphic state, and with the two
   strongest invaders from every enumerated candidate: add each strictly invading class at 10⁻³, run the replicator
   on the enlarged support to rest, repeat until saturated; no chain probabilities or thresholds), cached per cell
   (N-independent). It is complete (the full-branching search exhausted) only in `dollar3 norole`; elsewhere it is
   capped at 6,000 full-branching nodes plus 18,000 two-branch nodes, so coverage of ≥ 4-class supports is
   heuristic. A random-start replicator search (200 starts on the 140-class `dollar5 role` table) found none of the
   deep 4–5-class states and was dropped as a discovery method.
2. **Deep tiers.** The spec's operational "deep" (every outside class below the resident mean by > 10⁻⁹) is empty in
   every dollar cell, because every dollar trap has a payoff twin of a member, and a twin is exactly neutral. Reported
   alongside: **deep modulo twins** (every outside class strictly deleterious or a payoff twin of a member) and
   **deep with penalty only** (the repo's older criterion, at the audit's tolerance 10⁻⁹: first-order-neutral non-twin
   classes lose at second order). The older `modal_dollar.deep_states` used 10⁻¹² against payoff tables rounded to
   9 decimals, so its classification of first-order-neutral mutants depended on rounding (the X+Z+V trap's three
   neutral mutants sit at −3.5·10⁻¹⁰); at 10⁻⁹ the modal dollar has 13 + 37 deep-tier states at ≤ 3 classes (47
   published) and 27 + 53 with the closure.
3. **Seeding.** Expanding every stable candidate costs ~1 s per polymorphic seed (16,000+ in the 140-class tables), so
   the re-solve seeds every candidate with no strictly advantageous outside class (all deep tiers are among them; one
   layer of targets each), every saturated closure support, and every state the published chain expanded; the rest
   enter by log-domain exploration. In the PD cells (K up to 863) only candidates with no strictly advantageous class
   are kept as records.
4. **Exploration threshold.** The re-solve expands every unexpanded target whose π-weighted inflow exceeds θ_log
   (relative). θ_log = 10⁻³⁰ exploded at N = 10³ (thousands of candidates per round), so the cells were run at
   10⁻¹², then the dollar cells at 10⁻¹⁴ and 10⁻¹⁶ with closure seeds ("final" = closure-seeded, 10⁻¹⁴). The modal
   dollar control ran at 10⁻³⁰. θ-insensitivity is reported, not claimed as proof (§3).
5. **Two labelled diagnostics beyond the spec**, used only to name mechanisms: an establishment floor (a class with a
   first-order advantage d gets at least 1 − e^{−wd} of reaching its replicator target, in place of the
   lumped-resident truncated product), and two-trap best paths by on-demand Dijkstra (inconclusive, §3).

## 1. Regression tests and controls

`tests/test_solver_deep.py`, 3 passed:
- **(i) underflow.** Class table E (fair convention), H, D; G = H 2/3 + D 1/3 is a deep hawk–dove polymorphism. At
  N = 10⁴, G's exits are 10⁻¹³⁵⁰ and 10⁻¹⁴⁵⁷ per event and underflow to exactly 0 (3 underflowed edges). The published
  lazy linear chain gives π(G) = 0.5; log-domain GTH gives π(G) = 1 − 10⁻²³, equal to mpmath (50 digits) to 10⁻⁹ in
  every log π_i.
- **(ii) missed state.** E, D (an accommodating shadow of E), H with prior mass 10⁻¹²; G = D 1/3 + H 2/3 is deep and
  entered only from D at 10⁻¹²·⁹ per event. The lazy chain with `eager_poly=False`, θ = 10⁻⁷ never expands G and puts
  π = 0.5 / 0.5 on E and D; the class-table enumeration finds G (the only deep candidate) and the seeded log-domain
  chain gives π(G) = 1 − 10⁻¹², equal to mpmath. Note: the dollar cells' configuration (`eager_poly=True`) finds G
  through the eager expansion of all-H's dominant successor (π(G) 0.99993), so (ii) fails the lazy configuration
  only.
- (iii) log GTH equals mpmath to 10⁻⁹ on a random 9-state chain with log rates spanning 10⁻⁷⁸⁰ to 10⁺¹⁸⁰.

**Positive control** (modal dollar n = 7, N = 10⁴; 205 classes): published lazy configuration (θ = 10⁻⁷,
`eager_poly=False`) re-run: P(efficient) 0.4445, all mass on two two-type hawk states (X + `if(BOX1(S2),S4,S2)`);
**reproduced**. Re-solve (θ_log 10⁻³⁰, 735 recurrent states, log10 cut −29.8): **0.6531**, top state X+Z+V 1.000
(exit 10⁻²⁵·⁵ per event); with the closure (226 added supports up to 6 classes, 80 deep-tier states): 0.6531 again.
On the published chain's own explored set the log solve also gives 0.4445 (TV 0.17 between the two solutions, inside
twin-equivalent states): **the modal-dollar failure was exploration, not arithmetic.** 5,952 of the published edges
underflowed, none of them carrying stationary weight.

**Negative controls** (modal PD n = 6 classes, N = 10⁴, closure of every reachable state): {C, FairBot} (2 states,
no deep state): every solver P(C,C) 1.000, log vs mpmath 10⁻¹⁶; {D, C, FairBot} (3 states, no deep state; rates
from 10⁻¹³⁰⁴ to 10⁻⁰·⁹, 2 underflowed edges): linear, log and mpmath all 0.31486288701, max |Δπ| 2·10⁻¹³.

**Precision instance** (modal dollar {S3, S5, A5}, N = 10⁴, 4 states, exhaustive): log GTH vs mpmath max |Δ log π|
7·10⁻¹⁵, including π(all-S5) = 10⁻³³⁹·⁶; the linear solve gets the statistic right (0.55553) but the small components
wrong (π(S3) 1.9·10⁻¹¹ against 1.2·10⁻¹⁴; π(S5) 6·10⁻¹⁶ against 10⁻³⁴⁰; balance residual 3.1 log units).

## 2. The three separated checks (identical rates)

In every one-population cell the LogChain re-run of the published configuration expands exactly the published set
("same explored set: True" everywhere), and:
- **rates:** on non-underflowed edges the log weights equal the published linear weights to |Δ log w| ≤ 1.2·10⁻¹³ (checked separately on normal-range weights), except
  denormal edges (|Δ log w| up to 0.40, 1–441 edges per dollar cell); underflowed edges: 0 at N = 10³, 33–8,295 in the
  dollar cells at N ≥ 10⁴, 1,020–288,799 in the PD cells (38% of the modal PD's 757 k edges);
- **solver:** log-domain GTH on the published generator reproduces the published statistic in every cell to ≤ 5·10⁻⁴
  (dollar5 role 3·10⁴: 0.4617 / 0.0735 against 0.4620 / 0.0740); the published linear routine treats **no** class
  as numerically closed in any cell (`near_closed` 0); TV between the two solutions ≤ 6·10⁻⁴ except the modal control
  (0.17) and dollar5 norole 3·10⁴ (0.20), both inside twin-equivalent states;
- **state discovery:** see the per-cell table; the published explored sets miss deep-tier states in dollar5 role
  (the 5-class R5 and two 4-class penalty states) and in the modal dollar (74 of 80).

So the arithmetic of the published solver is sound wherever it was used; the errors found are in exploration and in
the transition model.

## 3. One-population dollar cells

| cell | N | published eff / half | re-solve eff / half (final, θ_log 10⁻¹⁴, closure-seeded) | Δ eff / Δ half | absorbing state (re-solve) |
|---|---|---|---|---|---|
| dollar5 norole | 10³ | 0.9995 / 0.9990 | 0.9995 / 0.9990 | 0 / 0 | S3 |
| dollar5 norole | 10⁴ | 0.4135 / 0.0004 | 0.4134 / 0.0002 | −0.0001 / −0.0002 | G4 = S5 3/4 + flip(THEM(THEM)) 1/12 + flip(THEM(^S4)) 1/8 + flip(THEM(^S2)) 1/24 (and its twin) |
| dollar5 norole | 3·10⁴ | 0.4132 / 0.0000 | 0.4132 / 0.0000 | 0 / 0 | G4 |
| dollar5 role | 10³ | 0.9995 / 0.6928 | 0.9994 / 0.6930 | −0.0001 / +0.0002 | S3 |
| **dollar5 role** | **10⁴** | **0.9682 / 0.8062** | **0.5849 / 0.0000** | **−0.383 / −0.806** | **R5 = max(S4,ROLE) 0.55 + flip(min(S4,ROLE)) 0.10 + flip(THEM(THEM)) 0.117 + flip(THEM(^S2)) 0.058 + flip(THEM(^S4)) 0.175 (and its twin)** |
| **dollar5 role** | **3·10⁴** | 0.4620 / **0.0740** | 0.4137 / **0.0003** | −0.048 / **−0.074** | G4 (same as published) |
| dollar3 norole | 10³ | 0.9959 / 0.9853 | 0.9959 / 0.9853 | 0 / 0 | M (1/2) |
| dollar3 norole | 10⁴ | 0.6251 / 0.0000 | 0.6251 / 0.0000 | 0 / 0 | H 1/2 + flip(THEM(THEM)) 1/4 + flip(THEM(^H)) 1/4 |
| dollar3 norole | 3·10⁴ | – | 0.6250 / 0.0000 | – | same |
| dollar3 role | 10³ | 0.9992 / 0.1568 | 0.9992 / 0.1574 | 0 / +0.0006 | `ROLE` |
| dollar3 role | 10⁴ | 0.9858 / 0.7882 | 0.9858 / 0.7929 | 0 / +0.0047 | M |
| dollar3 role | 3·10⁴ | – / 0.817 (text) | 0.9898 / 0.8220 | – / +0.005 | M |

Threshold sensitivity (dollar5 role): at N = 10⁴, θ_log 10⁻¹² gives 0.9567 / 0.7442 (a missed 3-class state W,
below), 10⁻¹⁴ and 10⁻¹⁶ (2,328 states, log10 cut −19.0) and the closure-seeded final all give 0.5849 / 0.0000; at
3·10⁴, 10⁻¹² gives 0.486 / 0.033 (W on top, 0.59), 10⁻¹⁶ and the final give 0.4134–0.4137 / 0.0001–0.0003. Every
other dollar cell moves by ≤ 0.005 between 10⁻¹² and 10⁻¹⁶. At N = 10⁵ (no twins): dollar5 role 0.4132 / 0.0000
(G4), dollar5 norole 0.4132 / 0.0000, dollar3 norole 0.625 / 0.0000, dollar3 role 0.9925 / 0.8428.

**The dollar5 `role` correction at N = 10⁴, and its mechanism.** R5 is a five-class polymorphism of a role-conditioned
hawk, `max(S4,ROLE)` (demands 2/3 in one role and 5/6 in the other), with four accommodators; internally stable
(Jacobian eigenvalues −0.141, −0.058, −0.038, −0.019), every outside class strictly deleterious except the payoff
twin flip(THEM(ME)) of flip(THEM(THEM)) (deep modulo twins), efficiency 0.585 (2/3–1/3 0.357, 1/6–5/6 0.228, clash
0.398). Its total exit is 10⁻¹⁸·⁵ per mutation event at N = 10⁴ (to S3), against 10⁻¹⁴·⁵ for the greedy G4 and
10⁻⁷·⁵ for S3. Its best entry path from S3 has weight 10⁻⁴⁴·⁶, so the published θ = 10⁻⁷ exploration never expanded
it; it is outside the ≤ 3-class enumeration and was found by low-θ exploration and by the invasion closure. With R5
present it holds 1.000 of π (0.53 + 0.47 on the twin pair) and the published 50–50 (S3 0.80) goes to 0. At 3·10⁴ R5
is seeded but not recurrent in the explored set (no explored state enters it), G4 holds 0.996 as published, and the
published 1/2–1/2 share 0.074 (all-S3) falls to 3·10⁻⁴ once the states downstream of the shadows are included (the
published solve of its own generator reproduces 0.0735, so this too is exploration). Whether R5 re-enters at 3·10⁴
is open: an on-demand best-path search from G4 found no path into R5 within 2,500 expansions.

**A transition-model artefact (W).** The 3-class state W = S2 0.059 + max(S4,THEM(THEM)) 0.706 + flip(THEM(^ROLE))
0.235 took 0.59 of π at 3·10⁴ under θ_log 10⁻¹². It has a strictly advantageous invader, flip(THEM(^S4)) (+0.0196
per match), which the lumped-resident truncated product charges a barrier growing in N (10⁻¹²·¹ at 10⁴, 10⁻²²·⁸ at
3·10⁴, against ≈ μ·(1 − e^{−wd}) ≈ 10⁻⁷·³ for an established invader). With the establishment floor (diagnostic) W
loses its mass (10⁴, θ 10⁻¹²: 0.9697 / 0.7484 against 0.9567 / 0.7442 without). It carries no mass in the final
re-solves; it is reported because the chain's ρ for polymorphic targets can make a strictly invadable state sticky
(the RESULTS "Not done" item "polymorphic-target ρ beyond the truncated product").

## 4. Twin drift (labelled intervention, after the solver comparison)

Twin moves: in a polymorphic state, a payoff twin q of resident r replaces r at rate μ(q)/(x_r N), a complete
transition, in place of the lumped-resident fate. Twin-expanded stationary distributions (closure-seeded, θ_log
10⁻¹⁴; modal dollar 10⁻²⁰):

| cell | N | without twins eff / half (top state) | with twins eff / half (top state) |
|---|---|---|---|
| dollar5 norole | 10⁴ / 10⁵ | 0.4134 / 0.0002 (G4) · 0.4132 / 0 (G4) | 0.4134 / 0.0002 (G4 + twin 0.50 / 0.50) · 0.4132 / 0 (same) |
| dollar5 role | 10⁴ / 10⁵ | 0.5849 / 0 (R5) · 0.4132 / 0 (G4) | 0.5849 / 0 (R5) · 0.4132 / 0 (G4) |
| **dollar3 norole** | **10⁴ / 10⁵** | **0.6251 / 0 (greedy H state) · 0.625 / 0** | **0.9906 / 0.975 (all-M 0.958) · 0.9949 / 0.990 (all-M 0.983)** |
| dollar3 role | 10⁴ / 10⁵ | 0.9858 / 0.7929 (M) · 0.9925 / 0.8428 (M) | 0.9859 / 0.7905 (M) · 0.9925 / 0.8427 (M) |
| **modal dollar n = 7** | **10⁴** / 10⁵ | **0.6531 (X+Z+V 1.000)** · 0.6531 (X+Z+V) | **0.5448 (H5 0.91; θ_log 10⁻¹², 2,450 states; 0.5454 at 10⁻¹⁰)** · 0.4453 (θ_log 10⁻¹⁰; a twin-connected family of two-class hawk states X + `if(BOX1(S2),·,S2)`, 0.95) |

**dollar3 `norole`: the greedy polymorphism is a lumping artefact.** Its exit without twins is 10⁻¹⁷·¹ per event
(to M). Its member flip(THEM(THEM)) has two payoff twins on the support, flip(THEM(ME)) and min(THEM(ME),L); twin
drift to min(THEM(ME),L) runs at 10⁻⁷·⁵, and the relabelled state is invaded by L at 10⁻⁴·⁰ (the twin differs off
the support, sol's point), then falls to M. With twin moves the greedy state's total exit is 10⁻⁶·⁷ and all-M holds
0.96 (10⁴) and 0.98 (10⁵). In dollar5 the greedy polymorphism's twins relabel it into an equally deep twin (no new
exit), so nothing changes; in dollar3 `role` M holds either way.

**Modal dollar: twin drift replaces the published trap.** X+Z+V exits at 10⁻²⁵·⁵ per event without twins. Its
member Z = `if(BOX1(S3),S3,S2)` has the PA-level twin `if(BOX(S3),S3,S2)`, reached by drift at 10⁻⁷·²; the relabelled
state exits at 10⁻⁵·³ to X + `if(BOX1(S2),S4,S2)` and on to a five-class S4-hawk polymorphism H5 = S4 0.463 +
`if(BOX(S1),S4,S2)` 0.075 + `if(BOX(S4),S1,S4)` 0.060 + `if(BOX1(S2),S4,S2)` 0.388 + `if(BOX1(S4),S1,S4)` 0.015
(exit 10⁻⁹·³), which holds 0.91–0.98 of π. P(efficient) 0.653 → 0.545 (2/3–1/3 0.539, clash 0.215, inefficient
0.240). The published twin caveat (best paths ∝ N⁻⁵ out of the trap; a stationary solve that hit 4,000 states) is
thereby settled at N = 10⁴: with twin moves the Löbian-hawk trap is not where π sits; another hawk polymorphism is.
Convergence is weaker than in the untwinned cells (log10 cut −9.8 at θ_log 10⁻¹², 74,578 twin moves). At N = 10⁵
(θ_log 10⁻¹⁰, published states not seeded, log10 cut −9.2) π sits on a family of two-class hawk states
`if(BOX(S1),S1,S4)` or its PA + Con twin at 2/3 with a one-atom reader `if(BOX1(S2),·,S2)` at 1/3 (deep with
penalty only), linked to each other by twin moves at 10⁻⁸·³ per event; P(efficient) 0.445.

## 5. PD cells

| cell | N | published P(C,C) | re-solve | Δ | deep tiers (strict / mod twins / penalty), re-solved mass | support (re-solve) |
|---|---|---|---|---|---|---|
| modal n = 9 | 10⁴ | 0.622 | 0.6224 | +0.0004 | 0 / 5 / 0; 0.055 (P\*, PrudentBot, two conjunction provers) | D 0.377, FairBot 0.181, `BOX1(THEM(ME))` 0.180, `BOX(THEM(THEM))` 0.157 |
| modal n = 9 | 3·10⁴ | 0.727 | 0.7270 | 0.0000 | 0 / 5 / 0; 0.071 | D 0.273, FairBot 0.227, `BOX1(THEM(ME))` 0.225, `BOX(THEM(THEM))` 0.156 |
| weak L_6 | 10⁴ | 0.0073 | 0.0073 | 0.0000 | 0 / 0 / 0 | D 0.9915, `THEM(^C)` 0.0072 |
| priced atoms n = 6 | 10⁴ | 0.0150 | 0.0150 | 0.0000 | **1** / 0 / 0: **all-D strictly deep (μ 0.469), π 0.985** | D 0.985 |
| priced atoms n = 8 | 10⁴ | 0.0158 | 0.0158 | 0.0000 | **1** / 0 / 0: all-D (μ 0.466), π 0.984 | D 0.984 |
| priced lazy n = 8 | 10⁴ | 0.9985 | 0.9985 | 0.0000 | 4 / 51 / 0: three ALLC-punishing provers strictly deep (μ 1.4·10⁻⁶ each), π 0.332 each | P\*-type triple 0.996 |
| K b = 16, n = 8 | 10⁴ | 0.671 | 0.6710 | 0.0000 | 0 / 10 / 0; 0.058 | D 0.329, FairBot 0.157, `BOX1(THEM(ME))` 0.156, `BOX(THEM(THEM))` 0.148 |

Coverage: every pair and every triple of the class table (107 M triples in the modal arm, 37.6 M in priced lazy),
no polymorphic candidate without a strictly advantageous invader in any PD cell, so the PD traps are monomorphic and
seeded. Transitions as published: entry into D by FairBot-family provers (10⁻⁴·⁷ per event at 10⁴), exits from the
provers by neutral ALLC drift (10⁻⁴·³ at 10⁴, 10⁻⁴·⁸ at 3·10⁴), then D; under atom pricing D's exits are 10⁻⁵·²
(priced provers, deleterious against D); under lazy pricing the P\*-type provers exit at 10⁻¹⁰·¹ per event.

## 6. Union and three-player cells

These chains are over monomorphic slot triples with constant-selection fixation (no lumped resident). In a
multi-population replicator no interior rest point is asymptotically stable, so the candidate traps are the
monomorphic triples that are strict Nash equilibria against every admissible single-slot mutant; they were enumerated
exhaustively in the union (297 × 364 × 364 class triples) and on a pool in the three-player game.

**Union QUORUM, c = 0.5, N = 10³** (`runs/solver_audit/union-quorum_c0.5_N1000.json`). Published re-run reproduces
the summary exactly (5,565 states, core 1,103; fair 0.00323, intermediate 0.01320, zero wage 0.4758). Solver on the
identical generator: independent dense log-domain GTH (`chain_log.gth_log`) against the published `gth_scaled`
hybrid: TV 1.1·10⁻¹⁴, max |Δ log π| 2.7·10⁻¹³, global-balance residual 4.6·10⁻¹⁴. Discovery: **0 strict-NE
triples** (every state has a neutral exit; the zero-wage states drift among whack policies and worker programs).
Re-solve with θ = 10⁻¹⁰ (10× below published) and core 3,000: 17,075 states, outcome-changing cut 0.2%; fair 0.0035
(+0.0003), intermediate 0.0145 (+0.0013), zero wage 0.4784 (+0.0026), strike 0.1233, scab split 0.3802. Support:
(0, strike-targeting) | work | work 0.198, (0, source) and (0, none) with both working 0.111 each, scab/striker splits
0.088 each; transitions from the top state are neutral boss drift to other zero-wage policies (3.6·10⁻⁵ each per
event), deleterious exits 10⁻⁶⁷. Every headline moves by < 0.003.

**Three-player modalPA, N = 10³**: [status filled below]

## 7. Verdicts

[see RESULTS draft]
