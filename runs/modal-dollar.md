# The modal arm on two-player divide-the-dollar, one population: does sound reading rescue efficiency, or help the greedy?

Spec `specs/2026-10-05-modal-dollar.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-modal-dollar-gpt-6.1-sol.md`);
predictions `predictions/2026-10-05-modal-dollar.md` (committed 07124ee, before any counted run); code
`src/modal_dollar.py`; notes and certificates `notes/modal-dollar.md`, `runs/modal_dollar/certificates.md`; per-cell
JSON under `runs/modal_dollar/` (`static.json`, `audit.json`, `deep_states_n7.json`, `chain_*.json` (lazy chains),
`limN_*.json` (seeded log-domain chains), `reduced*.json`, `fixed_*.json`, `lottery_all.json`, `lottery_summary.json`).
`dollar5`, one population without `ROLE` unless stated, w = 0.3.

**What ran.** The static go/no-go checkpoint (class counts, GLS+Def audit, certificates, invasion table of every
self-efficient class, the greedy polymorphism and fixation probabilities); paired modal/weak ε→0 chains at n = 7,
N = 10²–10⁵, first with the repo's lazy linear-domain chain at θ = 10⁻⁷ and 10⁻⁹ and then, because that chain did
not converge in θ at N ≥ 10³, with a log-domain chain seeded with every deep polymorphism; the reduced subsystems
({S3, S5, A5}, {S3, S5, A5, P′}, {S3, S5, A5, P, P′}) to N = 3·10⁵; the augmentation arm (P, P′ and their PA + Con
twins at 10⁻⁴, 10⁻³, 10⁻², paired, un-augmented kept); fixed roles (weak exact at N = 10²–10⁵; modal at N = 10², 10³);
the ε = 0 lotteries for both arms at (100, 64) and (400, 16), mN ∈ {0, 0.1}, 40 runs per cell.
**Not run:** the n = 11 chain (8,118 modal classes; augmentation instead, as the spec says); the modal fixed-role
chain at N ≥ 10⁴ (see "Fixed roles").

**Deviations.** (i) The two-player evaluators are re-implementations of `dollar3.eval_modal`/`eval_weak` restricted to
two slots (the three-slot kernels cannot be called on a two-player game), audited against GLS+Def below. (ii) The
matched weak arm ignores box levels (so its grammar and prior are identical to the modal arm's by construction) and
sends divergence to the yaml's minimax action S1. (iii) P′'s spelling in the spec reduces to the one-atom function
`if(BOX(S1), S5, S3)`, so **P′ is already in L₇**; only P needs n = 11. (iv) The lazy chain runs with
`eager_poly=False` (with `True` a single N = 10³ chain did not finish in 15 CPU-minutes on the shared machine; the
two agree at N = 10³ within the θ spread, 0.960 vs 0.953). (v) New instrument: the seeded log-domain chain
(`seeded_chain`), because the linear-domain lazy chain at N ≥ 10⁴ both underflows (a deep state's exits fall below
10⁻³⁰⁸) and prunes deep states reached by tiny flows; it expands every monomorphic state, every enumerated deep
polymorphism (≤ 3 types) and every target of their exits, then every state whose relative stationary inflow exceeds
θ, and solves π by GTH in the log domain (GTH has no subtractions). (vi) A twin-drift correction for polymorphic
states (`edge_logweights(twins=True)`), found necessary during the run (see "A caveat on deep states").

## Static checkpoint (go/no-go)

**Class counts.** a(s) = 5 (s = 1), 250 (s = 6–9), 5,250 (s = 10), 40,250 (s = 11). L₇: 205 canonical functions;
**modal 205 payoff classes, weak 77**. L₁₁: 14,605 canonical functions; **modal 8,118 classes, weak 368** — the n = 11
chain does not fit (each state expansion is 8,118 replicator fates, the deep-state enumeration is C(8118, 3) ≈ 9·10¹⁰
triples, and the lazy chain is shown below not to converge at this size of problem even at K = 205), so the
augmentation arm replaces it.

**Audit.** GLS+Def provability (`src/gl_proofs.py`'s terminating decision procedure, with five-valued definitional
constants P^a[x, y] = "x demands S_a against y") of every box atom against the evaluator's stable play: **0
disagreements in 21,321 pairs (41,814 atoms) at n = 7 plus P, and 0 in a 6,000-pair sample at n = 11** (23,936 atoms).

**Certificates** (`runs/modal_dollar/certificates.md`; sizes in sequents, Löb steps):

| encounter | plays | provable atoms |
|---|---|---|
| P′ vs P′ | (S3, S3) | none |
| P′ vs A5 | (S5, S1) | P′'s BOX(S1) (6, 2); A5's BOX(S5) (6, 2): a Löbian fixed point, P′ exploits a certified conceder |
| P′ vs P | (S3, S3) | none (P never provably concedes, P′ never provably demands 5/6) |
| P vs S5 | (S1, S5) | P's BOX(S5) (2, 0): P accepts certified greed |
| P vs A5 | (S5, S1) | P's BOX(S1) (14, 3); A5's BOX(S5) (20, 3) |
| A5 vs S5 / A5 vs A5 | (S1, S5) / (S3, S3) | BOX(S5) (2, 0) / none |
| X vs X (X = `if(BOX(S1), S1, S4)`) | (S1, S1) | both BOX(S1) by Löb: the hawk is meek with its copies |
| X vs Z, X vs V, Z vs V | (S4, S2), (S4, S2), (S2, S4) | none |

**Invasion table** (modal; every one of the 42 self-efficient classes is in `static.json`; the named ones here;
exit flows per mutation event at N = 10⁴; G = S5 2/3 + A5 1/3, mean 5/18):

| candidate | μ | strict constant invaders | exits from all-E (strict / neutral) | neutral neighbours (mass) | two-step exit into inefficiency | payoff vs G / mean | ρ(E \| G) at 10³ / 10⁴ | fate from G |
|---|---|---|---|---|---|---|---|---|
| S3 | 0.1926 | none | 0 / 6.0e-07 | 33 (0.0060) | 1.9e-07 | 0.167 / 0.278 | 7.2e-05 / 1.2e-21 | all-S3 |
| P′ = `if(BOX(S1),S5,S3)` | 0.0002 | none | 0 / 2.0e-05 | 32 (0.198, S3 incl.) | 1.2e-07 | 0.278 / 0.278 | 9.2e-03 / 2.9e-03 | all-P′ |
| P′₁ = `if(BOX1(S1),S5,S3)` | 0.0002 | none | 0 / 2.0e-05 | 30 | 7.3e-08 | 0.278 / 0.278 | 9.2e-03 / 2.9e-03 | all-P′₁ |
| A5 = `if(BOX(S5),S1,S3)` | 0.0002 | S5 | 1.8e-02 / 2.0e-05 | 31 | 1.3e-07 | (resident) | – | – |
| `if(BOX(S3),S3,S1)` | 0.0002 | S4, S5 | 2.9e-02 / 3.4e-05 | 8 | 5.5e-08 | 0.167 / 0.278 | ~0 | – |
| Z = `if(BOX1(S3),S3,S2)` | 0.0002 | S4 | 9.7e-03 / 2.6e-05 | 21 | 1.2e-07 | 0.167 / 0.278 | ~0 | – |
| P (added at 10⁻⁴) | 0.0001 | S5 (ρ 0.094 at 10³) | 1.8e-02 / 2.0e-05 | 32 | 1.1e-07 | 0.389 / 0.278 | 3.0e-02 / 3.3e-02 | S5 2/3 + P 1/3 |

Weak arm: S3 is the **only** self-efficient class; it has **no neutral neighbour** (a reader's self-play diverges to
S1, notes F1) and its exits are all deleterious (2·10⁻²⁴ per event at N = 10³, 8·10⁻²²⁰ at 10⁴); the weak G is S5 0.8
+ A5_w 0.2 (mean 1/6), whose exit to S3 is deleterious (9·10⁻¹⁰ at 10⁴).

**Verdict: go for P′, no-go for P.** P′ is not invaded by any constant, is a neutral neighbour of S3, and enters G at
exactly the mean payoff (0.2778 = 0.2778, so RE 3's "within 0.05" holds) but with ρ = √(8w/(9πN)) ≫ 1/N (9.2·10⁻³
at 10³, 2.9·10⁻³ at 10⁴; first-order neutral, positively frequency-dependent, notes F2) and fate all-P′. P is a
neutral neighbour of S3 that S5 strictly invades; it enters G strictly (+0.111) and lands on S5 2/3 + P 1/3 (sol's
x_P = 1/3, exact).

## Deep states

A state is *deep* when every outside mutant is deleterious at first order or first-order neutral with a frequency
penalty (chain's lumped resident), so every exit has a barrier linear in N. Enumerated over monomorphic, two- and
three-type interior rest points (`deep_states_n7.json`):

| arm | deep states | monomorphic | 2-type | 3-type | encounter efficiency (range) | mean payoff (range) |
|---|---|---|---|---|---|---|
| modal | 47 | 0 | 14 | 33 | 0.27–0.85 | 0.21–0.43 |
| weak | 27 | 1 (S3) | 24 | 2 | 0.32–1.00 | 0.17–0.50 |

Every modal deep state is a hawk–dove mixture of **Löbian hawks** (`if(BOX_L(S1), S1|S2|S3|S5, S4)`-type programs that
demand 2/3 but coordinate with their own copies on a meek split by Löb) with S2/S3 doves that use PA + Con boxes.
No efficient state is deep in the modal arm; S3 is deep in the weak arm.

## Paired chains at n = 7

### Lazy chain (linear domain, `src/chain.py`, eager_poly = False)

| arm | N | θ | P(efficient) | efficient set | greedy polymorphisms | E[max share] | top state (π) | expanded | cut flow |
|---|---|---|---|---|---|---|---|---|---|
| modal | 10² | 1e-7 / 1e-9 | 0.9858 / 0.9858 | 0.973 / 0.973 | 0.002 / 0.002 | 0.498 | S3 (0.948) | 287 / 796 | 3.0e-6 / 1.9e-7 |
| modal | 10³ | 1e-7 / 1e-9 | **0.9528 / 0.8896** | 0.832 / 0.672 | 0.028 / 0.019 | 0.498 / 0.492 | S3 (0.810 / 0.654) | 238 / 768 | 1.5e-6 / 6.7e-8 |
| modal | 10⁴ | 1e-7 / 1e-9 | **0.4445 / 0.7500** | 0 / 0 | 0 / 0 | 0.407 / 0.500 | X+Y (0.53) / X₁+Z (1.00) | 229 / 468 | 1.3e-15 / 1.2e-16 |
| modal | 3·10⁴ | 1e-7 / 1e-9 | 0.4445 / 0.4445 | 0 / 0 | 0 / 0 | 0.407 | X₁+Y / X+Y (1.00) | 223 / 368 | 7.3e-18 / 6.7e-19 |
| modal | 10⁵ | 1e-7 / 1e-9 | **0.4444 / 0.7500** | 0 / 0 | 0 / 0 | 0.407 / 0.500 | X+Y / X₁+Z (1.00) | 225 / 266 | 3.9e-19 / 6.1e-19 |
| weak | 10² | 1e-7 / 1e-9 | 0.9877 / 0.9876 | 0.979 / 0.979 | 0.0005 | 0.498 | S3 (0.979) | 131 / 165 | 8.0e-7 / 0 |
| weak | 10³–10⁵ | both | 1.0000 | 1.000 | 0 | 0.500 | S3 (1.000) | 77 | ≤ 7.4e-20 |

X = `if(BOX(S1),S1,S4)`, X₁ = `if(BOX1(S1),S1,S4)`, Y = `if(BOX1(S2),S4,S2)`, Z = `if(BOX1(S3),S3,S2)`,
V = `if(BOX1(S4),S2,S4)`. **The lazy chain is not θ-converged for the modal arm at N ≥ 10³** (subagent S9's falsifier
fired): its cut flow (10⁻¹⁵–10⁻¹⁹) is tiny in absolute terms but enormous next to a deep state's exit rate
(10⁻²⁵–10⁻²⁰⁰), so whichever deep state the exploration happens to reach takes all of π. The weak arm converges.

### Seeded log-domain chain (every deep state seeded)

| arm | N | θ | P(efficient) | efficient set (log₁₀ π) | deep set | greedy | E[max share] | mean payoff | top state (π) | states | log₁₀ cut | log₁₀ w(S3 → deep), best path |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| modal | 10² | 1e-7 / 1e-9 | 0.9858 / 0.9858 | 0.973 (0.0) | 0.000 | 0.002 | 0.498 | 0.496 | S3 (0.948) | 411 / 903 | −5.5 / −6.7 | −10.8 |
| modal | 10³ | 1e-7 / 1e-9 | **0.8944 / 0.8862** | 0.670 / 0.662 (−0.2) | 0.218 / 0.199 | 0.022 / 0.019 | 0.493 | 0.461 | S3 (0.65) | 352 / 899 | −5.9 / −7.2 | −11.8 |
| modal | 10⁴ | 1e-7 / 1e-9 | **0.6531 / 0.6531** | 3.3e-25 (−24.5) | 1.000 | 0 | 0.476 | 0.381 | X+Z+V (1.000) | 330 | −25.5 | −12.8 |
| modal | 3·10⁴ | 1e-7 / 1e-9 | **0.6531 / 0.6531** | 4.6e-78 (−77.3) | 1.000 | 0 | 0.476 | 0.381 | X+Z+V (1.000) | 331 | −64.7 | −13.3 |
| modal | 10⁵ | 1e-7 / 1e-9 | 0.6531 / 0.6531 | 5.7e-263 (−262.2) | 1.000 | 0 | 0.476 | 0.381 | X+Z+V (1.000) | 331 | −200.1 | −13.8 |
| weak | 10² | 1e-7 / 1e-9 | 0.9876 | 0.979 | (S3) | 0.0005 | 0.498 | 0.496 | S3 (0.979) | 135 / 165 | −6.0 | – |
| weak | 10³–10⁵ | both | 1.0000 | 1.000 | (S3) | ≤ 8e-23 | 0.500 | 0.500 | S3 (1.000) | 104 | ≤ −24 | – |

X+Z+V = X 4/7 + Z 2/7 + V 1/7 (encounter efficiency 0.653; X–X meek (1/6, 1/6), V–V clash, every cross pair an
efficient 2/3–1/3 split favouring the hawk, Z–Z 1/2–1/2). Converged in θ (10⁻⁷ vs 10⁻⁹ identical to four digits at
every N ≥ 10⁴; 0.008 apart at 10³).

**Support and transitions (modal).** N = 10²: S3 0.948, P′-type and other shadows of S3 the rest, greedy 0.002.
N = 10³: S3 0.65; the deep set 0.20–0.22 (X+Z+V 0.175, X₁+Z 0.031); S4–Z-type mixtures (S4 1/3 + an S2-conceder 2/3;
shallow) 0.05; greedy (S5) polymorphisms 0.02. N ≥ 10⁴: X+Z+V 1.000, X₁+Z 4·10⁻⁹, X+Y 2·10⁻¹¹. **The best path from
S3 into the deep set is S3 → Z (Z is a neutral PA + Con shadow of S3 that concedes 1/3 to anything not provably
fair) → X₁ + Z (the Löbian hawk invades Z strictly)**, weight 10^−11.8, 10^−12.8, 10^−13.3, 10^−13.8 at N = 10³, 10⁴,
3·10⁴, 10⁵: ∝ 1/N, a zero-cost route. The best path out of X+Z+V into efficiency (N = 10⁴) is a deleterious fixation
of `if(BOX1(S2),S4,S3)`, weight 10^−33.1.

**Entry/exit rates** (seeded chain, θ = 10⁻⁷; log₁₀ per mutation event):

| arm | N | efficient set: exit / entry | deep set: exit / entry | greedy: exit / entry |
|---|---|---|---|---|
| modal | 10² | −4.0 / −2.5 | −2.7 / −8.1 | −2.3 / −5.0 |
| modal | 10³ | −5.7 / −5.4 | −7.2 / −7.8 | −4.7 / −6.3 |
| modal | 10⁴ | −7.0 / −31.5 | −25.2 / −5.4 | – |
| modal | 3·10⁴ | −7.4 / −84.7 | −64.0 / −5.4 | – |
| modal | 10⁵ | −7.9 / −270.1 | −199.8 / −5.3 | – |
| weak | 10² | −4.1 / −2.4 | (S3 is the deep set) | −2.1 / −5.4 |
| weak | 10³ | −23.7 / −7.8 | | −3.9 / −26.0 |
| weak | 10⁴ | −219.1 / −61.6 | | −26.2 / −221.5 |
| weak | 3·10⁴ | −653.4 / −179.1 | | −80.2 / −655.8 |
| weak | 10⁵ | −2173.4 / −589.7 | | −270.0 / −2175.8 |

The modal efficient set's exit falls like 1/N (slope −1.1 over 10³–10⁵, −0.9 over 10⁴–10⁵: neutral shadows, then a
strict hawk); its entry falls exponentially (≈ 0.0027·N decades). The deep set's exit is exponential and its
entry N-independent (10^−5.4). So **within this chain the modal efficient set's odds fall like e^{−Θ(N)}, and lim_N
efficiency is that of the deep hawk–dove polymorphism (0.653)**. In the weak arm everything is exponential and S3's
barrier is the largest (its exit falls by ≈ 0.022·N decades against the greedy polymorphism's 0.0027·N).

## A caveat on deep states (twin drift)

Every one of the 47 modal deep states has a *support twin*: a program with identical payoffs against every resident
and itself (e.g. Z and its PA twin `if(BOX(S3),S3,S2)`), whose relabelled state is strictly invadable (notes F5). In a
finite Moran population the twin drifts neutrally inside its type's compartment (fixation 1/(x_r N)), so the true
exit from a "deep" state is two-step and polynomial: the shadow mechanism inside a polymorphism. The chain's
lumped-resident fixation charges the twin a frequency penalty instead (it holds the resident composition fixed while
the twin grows) and makes the state deep. The correction (twin moves at rate μ_q/(x_r N)) is in
`edge_logweights(twins=True)`;
a full stationary solve with it did not converge: at N = 10⁴, θ = 10⁻¹¹ the expansion hit its 4,000-state cap (the
twin networks of the hawk–dove mixtures are large) and the solve is not usable (`limN_modal_n7_N10000_th1e-11_twins.json`,
kept and flagged; the θ = 10⁻⁷ twin run did not expand the twin states at all and only shows the efficient set rising
from 10^−24.5 to 10^−20.9). What was computed exactly instead is the **best path** (Dijkstra with on-demand expansion,
twin moves included; `deep_exit_paths.json`) from the top deep state X+Z+V into the efficient set:

| N | 10³ | 10⁴ | 10⁵ | 3·10⁵ | 10⁶ |
|---|---|---|---|---|---|
| log₁₀ w, no twin moves | −8.7 | −33.1 | −272.9 | – | – |
| log₁₀ w, with twin moves | −8.7 | −26.8 | −46.1 | −48.5 | −51.1 |

With twin drift the route is X+Z+V → (twin Z → `if(BOX(S3),S3,S2)`) → X + Y → (twin) → X + S2 → (twin X → X₁) →
S2 + `if(BOX(S2),S4,S1)` → S3, five steps ∝ 1/N and two strict ones (edge weights recomputed at 10⁴, 10⁵, 10⁶ fall
by exactly one decade per decade on the five drift steps), so the best exit from the deep state into efficiency is
∝ N^(−5.0), against the efficient set's ∝ N^(−1) route into it (S3 → Z → X₁ + Z, unaffected by twins). **With or
without the twin correction the efficient set loses in lim_N at n = 7: exponentially in the chain as specified,
polynomially (odds ∝ N^(−4) on the best paths) once twin drift inside polymorphisms is allowed.** Which hawk–dove
mixture holds π under twin drift, and hence the limiting efficiency (0.27–0.85 over the deep set), is not determined.

## Reduced subsystems (log-domain chain, every state expanded)

Masses from L₇ plus P at 10⁻⁴, renormalized over the members; P(efficient), and the odds π(efficient set)/π(rest):

| subsystem | N = 10² | 10³ | 10⁴ | 3·10⁴ | 10⁵ | 3·10⁵ | absorbing state at large N |
|---|---|---|---|---|---|---|---|
| {S3, S5, A5} | 0.999 (734) | 0.994 (76) | **0.556 (10⁻¹⁴)** | 0.556 (10⁻⁵⁰) | 0.556 (10⁻¹⁷⁷) | 0.556 (0) | G = S5 2/3 + A5 1/3 |
| {S3, S5, A5, P′} | 0.999 (736) | 0.995 (85) | **0.985 (29)** | 0.991 (51) | 0.995 (92) | **0.997 (160)** | S3; odds ∝ N^0.500 (fit 10⁴–3·10⁵) |
| {S3, S5, A5, P, P′} | 0.999 (571) | 0.992 (52) | **0.556 (10⁻¹⁴)** | 0.556 (10⁻⁵¹) | 0.556 | 0.556 | S5 2/3 + P 1/3 |

**P′ alone rescues the greedy polymorphism at the √N rate** (first-order neutral re-entry against a 1/N exit, the
modal PD's exponent); **P undoes it**: P drifts into S3 as a neutral shadow, S5 invades P strictly, and S5/P cannot
be re-entered (P′ earns 1/2 only against P, so it is deleterious there; S3 likewise), so S5/P is deep and absorbs from
N = 10⁴ (sol's objection, confirmed). With P at 10⁻⁴ the transitions at N = 10³ are S3 → G by S5 (after A5 drift;
7.1·10⁻⁷ per event) and G → S3 by S3 (0.94 of re-entry, deleterious) and P′ (0.06).

## Augmentation (paired; P, P₁, P′, P′₁ added at swept mass; seeded log chain, θ = 10⁻⁷)

| arm | N | added mass 0 / 10⁻⁴ / 10⁻³ / 10⁻² | top state at 10⁻² (π) |
|---|---|---|---|
| modal | 10³ | 0.894 / 0.894 / 0.889 / **0.846** | S3 0.546; S5 2/3 + P₁ 1/3 0.138 |
| modal | 10⁴ | 0.653 / 0.653 / 0.653 / 0.653 | X+Z+V 1.000 |
| modal | 3·10⁴ | 0.653 / 0.653 / 0.653 / 0.653 | X+Z+V 1.000 |
| weak | 10³, 10⁴, 3·10⁴ | 1.000 at every mass | S3 1.000 |

Adding P and P′ does not rescue anything: at N = 10³ it moves π *toward* the greedy S5/P polymorphisms (greedy mass
0.022 → 0.157 at 10⁻²); from 10⁴ the deep Löbian hawk–dove state holds everything whatever the mass. P alone (P and P₁, no extra P′ mass): P(efficient) 0.881 / **0.796** at N = 10³ with 10⁻³ / 10⁻² (greedy mass 0.059 /
0.282); 0.653 at 10⁴ and 3·10⁴ at both masses.

## Fixed roles (two slot populations, N per slot)

Fixed-role chain of `src/dollar_partitions.py` (constant-selection fixation per slot, N per slot, a mutation event
picks a slot). Weak: exact dense GTH over all 77² states at N = 10², 10³; at N ≥ 10⁴ the strict-and-neutral subgraph
(deleterious fixations dropped) has a single closed class of 5,653 states, solved exactly (`fixed_poly.json`).
Modal: 205² = 42,025 states; lazily grown GTH with 8,000 states at N = 10², 10³ (cut flow 1·10⁻³ / 5·10⁻³; the same
procedure on the weak arm reproduces its exact solve to four digits); the modal N ≥ 10⁴ solve did not finish (a sparse
LU on the 42,025-state closed class ran 42 CPU-minutes and was stopped).

| arm | N | 1/2\|1/2 | 1/3\|2/3 + 2/3\|1/3 | 1/6\|5/6 + 5/6\|1/6 | ineff | P(efficient) | E[max share] | constant pairs |
|---|---|---|---|---|---|---|---|---|
| modal | 10² | 0.339 | 0.533 | 0.119 | 0.008 | 0.991 | 0.629 | 0.933 |
| modal | 10³ | 0.292 | 0.474 | 0.233 | 0 | 1.000 | 0.657 | 0.935 |
| weak | 10² | 0.340 | 0.533 | 0.118 | 0.008 | 0.991 | 0.628 | 0.934 |
| weak | 10³ | 0.293 | 0.479 | 0.228 | 0 | 1.000 | 0.656 | 0.935 |
| weak | 10⁴, 10⁵ | 0.293 | 0.480 | 0.228 | 0 | 1.000 | – | – |

**No accommodator ratchet in this grammar, in either arm.** Support at N = 10³: (S3 | S3) 0.274, (S4 | S2) and
(S2 | S4) 0.222 each, the endpoints 0.108 each; 0.935 of π on constant pairs. Every move between splits goes through
a one-atom conditional (share of label-changing flux leaving a state with a reader: 0.86–1.00): a reader that plays
the incumbent's demand against the other slot's constant and concedes to one specific other demand drifts in, and
that demand then invades strictly. One-atom accommodators concede to one demand each, so every split is two steps
from every other at comparable rates; the n = 5 weak arm's endpoint ratchet ran on universal conceders
(`flip(THEM(ME))`), which this grammar lacks. Sound reading changes nothing here: the encounters that matter are a
reader against a constant, where provability and simulation agree.

## Lotteries (ε = 0; share of islands at the horizon; run-level means with 95% t-intervals; 40 runs per cell)

| arm | (N, I) | mN | 1/2–1/2 | ineff / clash / mixed | island efficiency | runs closed / censored | median establishment (gens) |
|---|---|---|---|---|---|---|---|
| modal | (100, 64) | 0 | 0.526 [0.503, 0.550] | 0.176 / 0.298 / 0 | 0.526 | all islands monomorphic | 60 |
| weak | (100, 64) | 0 | 0.520 [0.501, 0.540] | 0.191 / 0.289 / 0 | 0.520 | all islands monomorphic | 60 |
| modal | (100, 64) | 0.1 | 1.000 [1.000, 1.000] | 0 | 1.000 | 39 / 1 | 65 |
| weak | (100, 64) | 0.1 | 1.000 | 0 | 1.000 | 40 / 0 | 65 |
| modal | (400, 16) | 0 | 0.759 [0.727, 0.792] | 0.053 / 0.075 / 0.112 | 0.813 | mixed islands at the horizon (long residence) | 105 |
| weak | (400, 16) | 0 | 0.769 [0.729, 0.809] | 0.069 / 0.078 / 0.084 | 0.808 | idem | 110 |
| modal | (400, 16) | 0.1 | 0.998 [0.995, 1.000] | 0.002 / 0 / 0 | 0.998 | 39 / 1 | 115 |
| weak | (400, 16) | 0.1 | 1.000 | 0 | 1.000 | 40 / 0 | 120 |

Identical seeds and stopping rules in both arms. 50–50 islands are held by S3 (modal: 1,296 of 1,347 at (100, 64),
m = 0, and 2,493 of 2,560 at mN = 0.1; the rest by neutral shadows of S3 such as `if(BOX1(S1),S5,S3)`); no run ends with two conventions. "Closed" is the
verified-closed stop (every present pair payoff-identical); at m = 0 a run ends when every island is monomorphic or
at the horizon (10⁵ generations), and a 'mixed' island at the horizon is long residence, not closure. **The lottery
does not distinguish the arms**: seeds are drawn from a prior that is 96% constants, against which S3 is the best
reply, and one-population migration makes 50–50 universal by risk dominance (as in the weak n = 5 arm).

## Verdicts

P(efficient) is read on the seeded log-domain chain (converged in θ); the lazy chain's numbers are given where they
differ. "Falsifier" = the stated falsifier.

| # | prediction | outcome |
|---|---|---|
| RE 1 | both arms leak by the same mechanism at n = 7; greedy polymorphism ≥ 0.8 of π by 3·10⁴ in modal and weak; falsifier modal P(eff) ≥ 0.7 at 3·10⁴ | **failed** (falsifier not fired: 0.653; lazy 0.44). Modal: one-atom accommodators are neutral shadows of S3 and S5 invades them (static), but the greedy polymorphism holds ≤ 0.03 of π at every N; π goes to Löbian hawk–dove polymorphisms. Weak: **no reader is a shadow** (self-simulation diverges), S3 holds 1.000 from N = 10³ |
| RE 2 | S5 strictly invades P; with P, P(eff) ≤ 0.6 at 3·10⁴; reduced subsystem: P enters G and ends in P/S5 near x_P = 1/3; falsifier ≥ 0.8 with P, without P′ | **mechanism held** (ρ(S5 \| P) = 0.094 at 10³; x_P = 0.333; S5/P absorbs the reduced subsystem from 10⁴); the P(eff) clause **failed narrowly for another reason** (0.653 with P, set by the hawk–dove trap, not by P); falsifier not fired |
| RE 3 | P′'s invasion payoff within 0.05 of G's mean, so at best neutral; modal with P′ keeps P(eff) ≤ 0.6 at 3·10⁴; falsifier payoff ≥ mean + 0.1 or P(eff) ≥ 0.8 | payoff clause **held** (exactly the mean, 5/18); "at best neutral" **failed**: ρ(P′ \| G) = √(8w/(9πN)) ≫ 1/N with fate all-P′, and in {S3, S5, A5, P′} P′ rescues efficiency at odds ∝ N^0.500; P(eff) ≤ 0.6 **failed narrowly** (0.653); falsifier not fired |
| RE 4 | modal fixed-role endpoints ≥ 0.9 at N ≥ 10³; modal and weak lottery 50–50 ≥ 0.8 at (100, 64), mN = 0.1, within 0.2; falsifier endpoints ≤ 0.6 at 10³ or shares ≥ 0.2 apart | **fixed-role clause failed, falsifier fired** (endpoints 0.233 at 10³, both arms; no ratchet in this grammar); **lottery clauses held** (1.000 / 1.000; the arms within 0.01 in every cell) |
| S1 | modal P(eff) ≥ 0.75 at 3·10⁴, non-decreasing 10⁴ → 10⁵, odds ∝ N^β, β ∈ [0.3, 0.7]; falsifier < 0.6 or lower at 10⁵ | **failed** (0.653, flat; the efficient odds fall like e^(−Θ(N))); falsifier not fired |
| S2 | efficient exit two-step neutral with slope ∈ [−1.1, −0.9]; re-entry at N ≥ 10⁴ carried ≥ 0.5 by P′-type programs with ρ slope ∈ [−0.6, −0.4] | exit slope **held** (−1.1 over 10³–10⁵, −0.9 over 10⁴–10⁵), but through Z and a Löbian hawk, not A5 and S5; re-entry clause **failed, falsifier fired** (re-entry into efficiency from the binding trap is a deleterious fixation, not P′; P′'s own ρ slope −0.50 held statically) |
| S3 | the matched weak arm does not leak at n = 7: P(eff) ≥ 0.9 at N ≥ 10⁴ | **held** (1.000) |
| S4 | P enters G strictly, x_P ∈ [0.31, 0.35]; P alone moves P(eff) at 3·10⁴ by < 0.05 | **held** (x_P = 0.333; 0.653 → 0.653); at N = 10³ P alone lowers it by 0.10 (0.894 → 0.796) |
| S5 | augmentation non-decreasing in mass at 3·10⁴, not below un-augmented by > 0.02; weak ≥ 0.9 | **held** (0.653 at every mass; weak 1.000) |
| S6 | reduced subsystem within 0.2 of the full chain at 10⁴, 3·10⁴; top cycle S3 → A5 → G → P′ → S3 | **failed** (within 0.2 numerically, 0.556 vs 0.653, but the cycle is broken: with P present S5/P absorbs; the cycle exists only in {S3, S5, A5, P′}, and the full chain's trap is a state the subsystem does not contain) |
| S7 | fixed-role endpoints ≥ 0.9 at N ≥ 10³ in both arms | **failed, falsifier fired** (0.233 / 0.228) |
| S8 | lottery 50–50 ≥ 0.8 at (100, 64), mN = 0.1 in both arms; arms within 0.1 in every cell | **held** |
| S9 | θ convergence within 0.01 | **failed, falsifier fired** for the lazy linear-domain chain (0.44 vs 0.75 at N = 10⁴ and 10⁵; 0.95 vs 0.89 at 10³); the seeded log-domain chain converges (identical at N ≥ 10⁴, 0.008 apart at 10³) |

## Reading

- **Sound reading does not rescue one-population bargaining efficiency at n = 7, and it is the reason the efficient
  convention leaks.** In the matched weak arm (same grammar, same prior) no reader can recognize itself, so S3 has no
  neutral neighbour and holds π = 1.000 from N = 10³; in the modal arm Löb gives every one-atom reader a
  self-recognizing shadow of S3, the efficient set's exit is ∝ 1/N, and from N ≈ 10⁴ π sits on a hawk–dove
  polymorphism of *Löbian hawks* (P(efficient) 0.653 in the chain as specified). The weak arm's n = 5 leak ran on probe
  readers; this grammar has none, so here the comparison runs the other way.
- **The trap is not the greedy S5 polymorphism.** The binding states are mixtures of `if(BOX(S1), S1, S4)`-type hawks
  (demand 2/3, but provably meek with their own copies, so self-play costs them 1/6 rather than a clash) with doves that
  concede 1/3 to anything not provably fair. Löb lets a hawk avoid fighting itself, and that is what makes hawk–dove
  mixtures invasion-resistant. 47 such deep states exist at n = 7 (efficiency 0.27–0.85); none is efficient.
- **In isolation, sol's objection and the RE's first draft are both right.** In {S3, S5, A5} the greedy polymorphism
  absorbs; adding P′ (refuse certified greed, exploit certified concession) rescues it at odds ∝ N^0.500 (the modal
  PD's exponent; P′ is first-order neutral into G and wins by self-play); adding P (accept certified greed) brings an
  S5/P polymorphism at x_P = 1/3 that P′ cannot re-enter, and it absorbs. Certified commitment helps the greedy exactly
  where a program accepts it; **unfakeability and resistance to profitable certified demands are different
  properties**, and P′ has both while P has only the first.
- **The characterization of THEORY §9.2 survives, quantified over traps.** Each trap is escaped only if some
  efficient-supporting program enters it neutrally and cannot be faked: P′ does this for G, nothing does it for S5/P or
  for the Löbian hawk–dove mixtures (every mutant is deleterious there, or only twin-neutral).
- **The chain's polymorphic approximation matters at this resolution.** Every deep state has a support twin whose
  relabelling is invadable; with twin drift the trap's exit becomes polynomial (best path ∝ N^(−5) against the
  efficient set's N^(−1)), so the lim_N failure stands but its rate and the identity of the trap are approximations.
  The repo's lazy linear-domain chain is not trustworthy once deep polymorphisms exist (it was not θ-converged here);
  the seeded log-domain chain is.
- **Distribution:** fixed roles spread π over all five splits (50–50 0.29, 1/3-type 0.48, endpoints 0.23) in both arms,
  with no endpoint ratchet in this grammar; the ε = 0 lottery makes 50–50 universal with migration in both arms
  (identical within 0.01). Distribution statistics are evaluations, not selectors.
- *Finite N:* the modal arm is 0.986 efficient at N = 10², 0.89–0.95 at 10³; these are finite-N numbers.
- *Free-box caveat:* the box is free and sound (provability decided by the GL Kripke chain, audited by GLS+Def at
  0 disagreements); the hawks' meekness with copies and P′'s exploitation of certified conceders both use Löb, which a
  realizable bounded prover provides only above its copy threshold (RESULTS "Proof length": FairBot copies from
  b = 3); the result is about what an idealized sound reader does in bargaining, not about a realizable one.
