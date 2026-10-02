# Predictions: ergodic islands, mutation re-injected (THEORY §9.5 (i)), 2026-10-02

Status: reviewed by astra (`reviews/2026-10-02-ergodic-islands-gpt-6-astra.md`) and fable
(`reviews/2026-10-02-ergodic-islands-fable.md`), then revised; changes are marked [after review]. Committed before the
runs.

**Executions before this commit** (`src/ergodic_islands.py`):
- Static single-edge fixation numbers and the three-rate reduction below (`static`).
- Smoke test of the chain at I = 1 against RESULTS "lim_N of the chain with `ROLE`" and "Modal (Löbian) arm"
  (`smoke_chain`).
- Monte Carlo smoke tests (`smoke_mc`):
  - I = 1 against `chain.fixation`;
  - a neutral pair at I = 4, N = 10;
  - one timing batch of 80 trials of the entry edge at I = 256, N = 100, mN = 0.1, with 3 successes (0.0375). This
    is a cell of the experiment; it is disclosed and not reused.
- ABM driver smokes of 400 and 2,000 generations at I = 4, N = 25 (no statistics used).
- [after review] Fable ran the two-level chain itself at 12 weak-arm (N, I) cells and at modal N ∈ {50, 100, 400,
  1000} × I ∈ {1, …, 1024}, before this commit. Those numbers are quoted where they apply and marked *(seen)*; the
  verdicts on them are checks, not blind predictions.

## Question

At ε = 0 the island model is an absorption lottery that concentrates on mutual defection as I grows, so mutation
stays in the object. With mutation re-injected at ε ≪ m, π exists. From the cooperative state, which exit dominates,
the faker or the shadow, and how does that scale with island size N, island count I and migration m? Does island
structure make the weak arm efficient in some limit, or only move its peak? Does the modal arm do better on islands
than well-mixed?

[after review] This adjudicates, under mutation, between two REJECTED entries:
- "Fakers as the spatial/island spoiler", refuted on the lattice (2026-09-18 ledger);
- its reversal for islands at ε = 0 (2026-09-23).

The 09-18 entry also says "do not re-propose faker-resistance as the fix". THEORY §9.2 re-opened that via the modal
arm. Here the modal arm is a comparison arm, not a proposal.

## The object

**Model** (as `src/islands.py`, w_g = 0). I islands of N on a regular island graph: complete, hypercube (I = 2^d,
degree d) or torus (degree 4, control). Each event a uniformly random agent dies. With probability 1 − m it is
replaced by the offspring of a parent from its own island, drawn ∝ count · exp(w · fitness); with probability m the
parent is drawn the same way on a uniformly random neighbouring island. Fitness is mean payoff against the other N − 1
on the parent's island. Each birth mutates with probability ε to a draw from μ. PD, w = 0.3.

**Migration scaling.** We fix mN, migrants per island per generation, as N varies (per-death m = mN/N). Under this
scaling island structure survives N → ∞. At fixed per-death m, dilution would eventually overwhelm the w·N^(−1/2)
selection that a lone reciprocator lineage feels.

**Order of limits.** ε → 0 first, at fixed (I, N, mN, graph). The metapopulation absorbs between mutations, and the
ε→0 object is the chain over monomorphic metapopulation states a with weights μ(q)·Φ(q | a). Φ is the probability
that one q mutant on a uniformly random island takes the whole metapopulation. Limits in I and N are taken afterwards,
along fixed graph families: hypercube d → ∞ at fixed N, with the complete graph as reference.

[after review] **Why the absorbing chain is physical here.** No pair of weak-arm classes with μ > 10⁻⁴ is bistable at
N = 100: the smallest max(ρ, ρᵀ) is exactly 1/N (fable). So the slowest island-level flip is neutral, and ε ≪ m/N
suffices. This, together with eventual absorption at positive m (astra), is the justification for monomorphic states.
It re-opens the *form* of REJECTED "Fudenberg–Imhof small-mutation chain", whose objection was exponential coexistence
times; none exist among these states. Checks:
- 0 classes coexist with D or with the reciprocator, in either arm.
- At I = 1 the monomorphic chain equals the attractor chain:
  - weak N = 100: 0.0086 / 0.9866 / 0.0077 against 0.0086 / 0.9865 / 0.0077 (P(C,C), π(D), π(`THEM(^C)`));
  - weak N = 1,000: 0.0132 / 0.9845 / 0.0130, exact;
  - modal 0.169 and 0.345 at N = 10², 10³, exact.

The agent-based runs take I → ∞ at fixed per-island εN, a different order, and measure approach rates only.

**Two estimates of Φ.**
1. **Two-level Φ₂.** The mutant fixes on its island with the within-island Moran probability ρ_N(q|a). On a regular
   island graph each discordant edge flips toward q at rate ∝ ρ_N(q|a)/d and toward a at ∝ ρ_N(a|q)/d, so the number
   of q islands is a biased walk with ratio r = ρ_N(q|a)/ρ_N(a|q). Hence Φ₂ = ρ_N(q|a)·(1 − 1/r)/(1 − r^(−I)), the same
   on every regular graph.
   - [after review] Regularity is load-bearing (fable). On an irregular graph the per-edge ratio picks up d_j/d_i.
   - Neutral pairs give exactly 1/(IN) at *every* m on a regular graph, since the replacement process is isothermal.
   - Φ₂ is the m → 0 value. For the entry edge it is already 0.99× exact at mN = 0.1 (dilution, below).
2. **Monte Carlo Φ_MC at fixed mN** (`_meta_fix`): two types, run to global absorption.
   - [after review] Stopping is adaptive on successes:
     - ≥ 150 successes for entry;
     - ≥ 400 for the faker code checks;
     - cut at 4·10⁵ trials or 40 minutes, with the stopping reason reported per cell.
   - Wilson intervals are over decided trials. Bounds that count undecided trials as failures and as successes are
     also reported (astra).
   - Inverse sampling biases s/n by about p/s, under 1% here.
   - Seeds differ by edge, graph and mN, so there are no common random numbers across cells (fable).

The full chain uses Φ₂ for all 112 × 112 (weak) or 51 × 51 (modal) pairs. The **patched chain** [after review:
exploratory, per astra] replaces every pair whose 2×2 game equals a game measured at that cell by Φ_MC. The reverse
edges cannot be measured: Φ₂(D | R) is about 10⁻⁶⁰ at N = 100, I = 64. They enter only through negligible return
flows.

There are three distinct 2×2 games among the key edges:
- *entry*, (u_qq, u_qa, u_aq, u_aa) = (0, −1, −1, −1): `THEM(^C)` into all-D, and identically FairBot into all-D.
- *faker-D*, (−1, 1, −2, 0): `THEM(^D)` into all-`THEM(^C)`, and identically D into all-C.
- *faker-X*, (−0.5, 0.5, −1, 0): `THEM(^X)` and `THEM(^ROLE)` into all-`THEM(^C)`.

The shadow, C into the reciprocator, is neutral, so its Φ is exactly 1/(IN). It is checked only as code.

**Arms.**
- *Weak L_6 with `ROLE`* (112 classes). `ROLE` is first-class (THEORY §1), and `THEM(^ROLE)` carries 0.23 of the
  faker flux, so dropping `ROLE` would bias the answer toward cooperation.
- *Modal n = 6* (51 classes). [after review] It is *not* faker-free. Its cooperative block splits into:
  - three unfakeable provers: `BOX(THEM(ME))`, `BOX(THEM(THEM))` and `BOX1(THEM(ME))`;
  - six fakeable ones: `BOX1(THEM(THEM))`, `BOX(THEM(^C))`, `BOX1(THEM(^C))`, …, which are third-party probes or
    are strictly invaded (fable);
  - unconditional cooperators.

## Static numbers (w = 0.3, PD R = 0, S = −2, T = 1, P = −1)

**Priors and classes.**
- μ(`THEM(^C)`) = 5.15·10⁻⁴ and μ(C) = 0.249.
- 9 shadow classes, μ 0.2493.
- 13 faker classes, μ 1.62·10⁻³. The main ones are `THEM(^D)` (5.15·10⁻⁴) and `THEM(^X)` / `THEM(^ROLE)`
  (4.9 / 4.7·10⁻⁴).
- Modal: μ(FairBot) = 4.95·10⁻³, μ(C) = 0.469.

**Within-island fixation ρ_N:**

| N | entry ρ(R\|D) | ρ(D\|R) | faker-D | ρ(R\|F) | faker-X | shadow 1/N |
|---|---|---|---|---|---|---|
| 10 | 0.139 | 4.2·10⁻² | 0.315 | 1.2·10⁻² | — | 0.1 |
| 25 | 0.082 | 2.6·10⁻³ | 0.278 | 1.1·10⁻⁴ | 0.153 | 0.04 |
| 100 | 0.042 | 1.7·10⁻⁸ | 0.264 | 2·10⁻¹⁴ | 0.142 | 0.01 |
| 400 | 0.021 | 3·10⁻²⁸ | 0.260 | 10⁻⁵³ | 0.140 | 0.0025 |
| 1000 | 0.0136 | 10⁻⁶⁷ | 0.260 | 10⁻¹³¹ | — | 0.001 |

**The faker's Φ is invariant to structure** [after review: sharpened by fable]. This PD has T + S = R + P, so each
faker-vs-R subgame is additive. The faker's payoff gap is the same at every within-island count, (T − R)(N + 1)/(N − 1)
for `THEM(^D)` and half that for `THEM(^X)`: constant selection. On a regular island graph every island is the source
of exactly N births per generation at any m, so every faker individual has birth rate r = e^(w·gap) and death rate 1
wherever it sits. Hence Φ(faker) = 1 − 1/r + O(r^(−N)) for every m, I and regular graph:
- 0.264 at N = 100 and 0.278 at N = 25 for `THEM(^D)`;
- 0.142 at N = 100 for `THEM(^X)`.

Scope: regular island graphs, w_g = 0, and this payoff structure. For a general PD the gap is positive at every
frequency, so the branching constant still holds at large N. Between-island selection (w_g) changes per-individual
birth rates and is outside the statement.

**Entry and the shadow, by contrast:**
- Entry is neutral at one copy. It needs the reciprocator to meet its own kind, so it is what island size and
  migration change.
- The shadow's exit is exactly 1/(IN).

**The three-rate reduction** (R = `THEM(^C)`):
- entry = μ_R·Φ₂(R | D);
- faker exit f = Σ_F μ_F·Φ(F | R), which is 2.9·10⁻⁴ for N ≥ 50, 3.3·10⁻⁴ at N = 10 for large I, and 3.8·10⁻⁴ at
  I = 1;
- shadow exit = 0.2493/(IN).

π_R/π_D ≈ entry/(f + shadow). The predicted π_R = odds/(1 + odds):

| N \ I | 1 | 4 | 16 | 64 | 256 | 1024 | 4096 (plateau p*) |
|---|---|---|---|---|---|---|---|
| 10 | 0.0010 | 0.005 | 0.026 | 0.065 | 0.104 | 0.122 | 0.128 |
| 25 | 0.0026 | 0.014 | 0.042 | 0.081 | 0.106 | 0.114 | 0.117 |
| 50 | 0.0051 | 0.019 | 0.047 | 0.075 | 0.087 | 0.091 | 0.092 |
| 100 | 0.0076 | 0.023 | 0.046 | 0.062 | 0.067 | 0.069 | 0.069 |
| 200 | 0.0100 | 0.025 | 0.041 | 0.048 | 0.050 | 0.051 | 0.051 |
| 400 | 0.0120 | 0.024 | 0.033 | 0.036 | 0.037 | 0.037 | 0.037 |
| 1000 | 0.0129 | 0.020 | 0.023 | 0.024 | 0.024 | 0.024 | 0.024 |

[after review] The plateau is not monotone below N = 10. Fable's reduction gives p* = 0.054 / 0.100 / 0.111 / 0.123 /
0.128 / 0.128 / 0.117 at N = 3 / 5 / 6 / 8 / 10 / 16 / 25, a maximum near N = 10–16. N = 5 and 16 are added to the
grid.

So p*(N) = μ_R·ρ_N(R|D)/f is the well-mixed chain at size N with the shadow exit deleted (fable). Islands act on
entry only through the choice of N.

**Faker share of exits from all-R** = f/(f + 0.2493/(IN)). It depends on M = IN alone, at every m:
- crossover (share 0.5) at M* ≈ 860;
- 0.88 at M = 6,400, whether the split is (25, 256), (100, 64) or (400, 16);
- 0.96 at M = 25,600.

**Reduced-model bound** [after review: labelled as a statement about the reduction, not the full chain (astra)].
With ρ_enter = 1, π_R/π_D ≤ μ_R/f ≈ 1.8, so π_R ≤ 0.64.

**Dilution of entry at fixed mN.** This is the within-island fixation of a lone q against immigrants from an all-a
sea, ignoring the lineage's own emigrants. As multiples of ρ_N at mN = 0.1 / 1:
- N = 100: 0.98× / 0.83×;
- N = 25: 0.96× / 0.54×;
- N = 400: 0.99× / 0.93×.

[after review] The lineage's own emigrants add about +20% at N = 25, mN = 1 (fable). At mN ≫ 1 entry tends to the
well-mixed value at size IN: ρ_6400 = 0.0054 at I = 64, N = 100.

**Modal arm** [after review: replaced]. The odds are I·o_u(N) + o_f(I, N):
- the three unfakeable provers exit only by neutral drift (∝ 1/(IN)) and enter at an I-independent rate, so their
  odds grow ∝ I;
- the fakeable provers have I-independent strict exits (7.0 and 7.8·10⁻⁴ at N = 100), so their odds saturate.

Fable's chain values *(seen)*: o_u(100) = 0.133 and o_u(1000) = 0.430; o_f saturates at 0.47 (N = 100) and 0.16
(N = 1000).
- P(C,C) at N = 100 is 0.418 / 0.712 / 0.899 / 0.972 / 0.993 at I = 4 / 16 / 64 / 256 / 1024.
- Well-mixed modal P(C,C) at the same M is 0.536 at M = 6,400 and 0.691 at M = 25,600.
- π(fakeable provers)/π(unfakeable provers) falls like 1/I, from 0.45 at I = 1 to 0.002 at I = 1024. Islands select
  for unfakeability inside the family.

## Design

**A. The ε→0 two-level chain** (`run_static`; graph-independent, so it covers the hypercube family to d = 12). Both
arms, at:
- N ∈ {5, 10, 16, 25, 50, 100, 200, 400, 1000};
- I ∈ {1, 4, 16, 64, 256, 1024, 4096}.

Reported per cell:
- P(C,C), π(all-D), π(all-R), π(faker states), [after review] π(weak-faker states) and π(all-C);
- π of the cooperative block, split unconditional / unfakeable / fakeable;
- the support (top 6) and the top probability flows;
- exits from all-R split four ways: faker, [after review] weak faker (U[q,R] = U[R,R] and U[R,q] < U[R,R]), shadow and
  other;
- [after review] π-weighted exits from the whole cooperative block, by the same four types.

**B. Monte Carlo at fixed mN** (`run_mc`, 40 jobs, 3 workers):
- *Entry, ≥ 150 successes:*
  - N = 100, mN ∈ {0.1, 1}, I ∈ {4, 16, 64, 256}, complete and hypercube;
  - N ∈ {25, 400} at I = 64, mN ∈ {0.1, 1};
  - torus 8×8 at mN = 1;
  - mN ∈ {3, 10} at I = 64, N = 100;
  - [after review] a small-m ladder at (I, N) = (16, 25), mN ∈ {0.01, 0.1, 1, 3} (astra).
- *Faker code checks* [after review: cut to one per (graph, mN) plus extremes, ≥ 400 successes (fable)]:
  - faker-D at I = 64, N = 100, complete and hypercube, mN ∈ {0.1, 1}; torus mN = 1; complete mN = 10; N = 25, mN = 1;
  - faker-X at I = 64, N = 100, complete, mN ∈ {0.1, 1, 10}; N = 25, mN = 1.
- *Shadow code check* at I = 16, N = 25, complete and hypercube.
- Then the patched chain at every cell where entry was measured.

**C. Finite-ε agent-based approach runs** (`run_abm`, `islands.run_one`, w_g = 0, 2·10⁵ generations, 3 replicates,
statistics from the second half, first half reported).
- *Weak arm* from all-D:
  - N = 100, mN = 1, εN = 0.1, I ∈ {16, 64, 256} complete and I ∈ {64, 256} hypercube;
  - εN = 0.01 at I ∈ {16, 64, 256};
  - N = 25, εN = 0.1, I ∈ {64, 256};
  - mN = 0.1, εN = 0.01, I = 64.
- *Modal n = 6* from all-D: N = 100, mN = 1, εN ∈ {0.1, 0.01}, I ∈ {16, 64, 256}.
- [after review] *All-R starts:* weak I = 64 at εN = 0.1 and 0.01; modal I = 64 at εN = 0.01 (astra, fable).

[after review] New instrumentation in `islands._run`:
- second-half island P(C,C) summed by the island's dominant class (R / C / faker or weak faker / other / none), so
  the ABM's P(C,C) can be decomposed (fable 1(c));
- exits from islands that held ≥ 90% R at the previous 20-generation sample, by the new dominant class (fable 1(d)).

Whether an invader was born by mutation or arrived as an immigrant is not recorded.

**Placement.** The island graph is over islands. There are no lattices of agents and no pricing; the sibling
experiment covers those.

## Verdicts

[after review] "Contains" means the 95% Wilson interval of Φ_MC intersects the predicted band. A multi-cell verdict
holds if at least 90% of its cells contain, and no cell fires a falsifier.

*ε→0 object (A).*
1. **The weak arm saturates in I and does not become efficient.**
   - π(all-`THEM(^C)`) is within ±5% of the reduction table in every cell with N ≥ 10 [after review: tightened from
     ±15%; fable saw 1–4% at 12 cells].
   - It is non-decreasing in I.
   - The I = 4096 plateau has log-slope in [−0.55, −0.38] over N ∈ [100, 1000] (table: −0.46).
   - The maximum over N lies at N ∈ [8, 25].
   - P(C,C) ≤ 0.15 in every cell with N ≥ 10.
2. **The exit split depends on M = IN only.** Faker share within ±0.03 of f/(f + 0.2493/M) for N ≥ 25. Crossover
   between M = 640 and 1,000. Above 0.95 for M ≥ 25,600. [after review] This holds nearly by construction once Φ₂ is
   used; its content is that weak-faker and other exits stay below 0.01 of the total.
3. **Support and transitions (weak).**
   - The support is all-D and all-`THEM(^C)`, plus all-X and all-`ROLE` at small M.
   - [after review] The weak-faker sink `and(X,THEM(^D))` grows ∝ I. It is fed only from R and left only by drift, at
     0.0029 / 0.0078 / 0.0114 at I = 4096 for N = 100 / 25 / 10 (fable). Nothing else exceeds 0.01.
   - The `THEM(^C)` mutant carries ≥ 0.8 of cooperative entry flux into all-D.
   - Exits run faker → faker state → all-C → all-D, or shadow → all-C → all-D.
   - π(faker states) < 0.005. They drain by ALLC's strict invasion, so their exit does not shrink with I.
   - [after review] At N = 10 and small I, P(C,C) is X/`ROLE` self-play and all-C, not reciprocity (fable).
4. **The modal arm becomes efficient in I, through its unfakeable provers** [after review: replaced].
   - P(C,C) at N = 100 within ±0.02 of 0.418 / 0.712 / 0.899 / 0.972 / 0.993 at I = 4 / 16 / 64 / 256 / 1024
     *(seen)*.
   - Log-odds slope in log I within [0.9, 1.05] over I ∈ [16, 1024] (fable: 0.96).
   - π(fakeable)/π(unfakeable) has log-slope in log I within [−1.1, −0.9] for I ≥ 16.
   - At equal M, island P(C,C) exceeds well-mixed in every cell with I ≥ 4 and N ≥ 50.

*Fixed m (B).*

5. **The faker's Φ is the constant-selection value.** Every faker cell contains 1 − 1/r ± 5% (0.264 / 0.278 for
   faker-D and 0.142 / 0.153 for faker-X at N = 100 / 25), for every mN up to 10 and every graph.
6. **Entry at mN ≤ 1 is island-local and I-independent.** Φ_MC(entry)/ρ_N bands:
   - [0.9, 1.1] at mN = 0.1;
   - [0.75, 1.0] at mN = 1, N = 100;
   - [0.5, 0.85] at N = 25, mN = 1 (point prediction ≈ 0.65);
   - [0.85, 1.05] at N = 400.

   No trend over I ∈ {4, …, 256} beyond what the intervals allow: the I = 4 and I = 256 intervals intersect.
7. **Graph independence** [after review: stated as a ratio test (astra)]. For entry at each (I, mN), the 95% interval
   of the complete/hypercube ratio (delta method on independent samples) contains 1 in ≥ 90% of pairs. Torus likewise
   at I = 64. Shadow cells contain 1/(IN) = 0.0025.
8. **Migration moves only entry.**
   - Entry at I = 64, N = 100 falls over mN = 0.1, 1, 3, 10: 0.4–0.8 × ρ_N at mN = 3, and [after review] in
     [0.003, 0.02] at mN = 10.
   - The faker cells at mN = 10 obey verdict 5.
   - [after review] Small-m ladder at (16, 25): Φ_MC/Φ₂ within [0.9, 1.1] at mN = 0.01 and 0.1, decreasing in mN.
9. **The patched chain stays close** (exploratory). π_R within ±25% of the two-level chain in every B cell with
   mN ≤ 1 and N ≥ 100. At mN = 10, within a factor 2 of the well-mixed π_R at M = 6,400 (0.0086).

*Finite ε, approach rates (C).*

10. **Weak islands are flat in I, and R-dominant islands are rarer than π_R** [after review: decomposition added].
    - At N = 100, mN = 1, εN = 0.1, P(C,C) is in [0.09, 0.19] at I = 64 and 256, and in [0.06, 0.19] at I = 16
      (fable: I = 16 at risk low). |P(256) − P(64)| ≤ 0.04.
    - [after review] R-dominant island-time at I = 64 is in [0.01, 0.06], below the chain's π_R = 0.062. At least 0.3
      of P(C,C) comes from islands with no dominant class.
    - Hypercube within 0.05 of complete (fable: about even odds).
    - No weak cell above 0.3.
11. **Exit composition** [after review: the directional prediction is dropped (astra, fable) and is now descriptive].
    Exits from ≥ 90%-R islands are reported by type at εN = 0.1 and 0.01. Predicted: fakers and weak fakers carry at
    least half of them at εN = 0.1, I = 64.
12. **Island size at finite ε** [after review: reversed]. At N = 25, P(C,C) is at most the N = 100 value + 0.02, at
    I = 64 and 256. At N = 25, D immigrants take R islands (ρ_25(D|R) = 2.6·10⁻³ against 1.7·10⁻⁸ at N = 100), and
    entry is diluted to 0.54–0.65×.
13. **The modal arm is near 1 on islands at finite ε.** P(C,C) ≥ 0.95 at εN = 0.1 and ≥ 0.9 at εN = 0.01, at every I.
    At I = 16, εN = 0.01 the first half is expected to be depressed by a slow approach (fable).
14. **Mixing.**
    - First and second halves within 0.05 in every C cell at εN = 0.1.
    - [after review] All-R and all-D starts within 0.05 in their second halves.
    - Cells that disagree are reported, and their verdicts 10–12 are indeterminate.

## Falsifiers

- *Of "structure cannot touch the faker":* any faker cell whose interval excludes [0.22, 0.31] (faker-D, N ≥ 100) or
  [0.11, 0.17] (faker-X, N = 100).
- *Of "the weak arm is not efficient on islands":*
  - the patched-chain P(C,C) above 0.2 in any B cell;
  - two-level P(C,C) above 0.15 at I = 4096 for N ≥ 10;
  - a finite-ε weak cell above 0.3.

  [after review] These falsify the numerical predictions of a reduction, not asymptotic inefficiency itself (astra).
- *Of "the exit split is set by M":* two splits of the same M whose faker shares differ by more than 0.05.
- *Of "islands help the modal arm through unfakeability":* modal P(C,C) at I = 256, N = 100 below 0.9; or the
  fakeable/unfakeable ratio not falling with I.
- *Of graph independence:* a complete/hypercube ratio interval excluding 1 by more than 30%.
- *Of migration acting only on entry:* entry at mN = 10 above 0.5 × ρ_N, or a faker cell at mN = 10 outside its band.

## What it would mean

- **If 1–9 hold.** Re-injecting mutation turns the ε = 0 lottery into an ergodic chain whose cooperative mass is set
  by three rates:
  - Island size N sets entry, through local relatedness.
  - Total size M sets the shadow exit.
  - No structure on a regular island graph with w_g = 0 sets the faker exit, since constant selection makes its Φ
    structure-invariant.

  The weak arm's peak in M becomes a plateau p*(N) = μ_R·ρ_N(R|D)/f, at most about 0.13 near N = 10–16, falling like
  N^(−1/2). That is up to about 10× the well-mixed peak, but not efficient along any of these families. Faker exits
  dominate for M ≳ 900, for any split into islands, any m and any regular graph.

  The modal arm's unfakeable provers grow ∝ I, its fakeable provers saturate, and P(C,C) → 1 with odds ∝ M at fixed
  island size, against M^(1/2) well-mixed. Islands select for unfakeability inside a family. This is §9.2's
  characterization seen through population structure: structure helps the neutral-entry condition and the shadow
  exit, and cannot substitute for unfakeability.

  [after review] The levers left against the faker are the prior ratio μ_R/Σμ_F, the temptation T − R,
  unfakeability, and between-island selection, which changes per-individual birth rates (fable).
- **If verdict 5 fails.** The constant-selection argument is wrong for this birth rule. Fixed-m islands would then
  suppress fakers without group selection, and THEORY §3's "the dilemma failure in lim_N is fakeability" would need a
  structural qualifier.
- **If verdict 6 fails upward** (entry grows with I through multi-island nucleation). The plateau could rise in I.
- **If 10–13 hold.** The finite-ε metapopulation in the I → ∞-at-fixed-εN order is a distinct regime, mostly
  polymorphic islands.
  - [after review] Its P(C,C) (about 0.13 at I = 64, N = 100) must not be compared with the chain's π_R (0.062). The
    comparable statistic, R-dominant island-time, is predicted *below* π_R.
  - This bears on REJECTED "Standing variance (finite εN) as the rescue": island structure would not re-open it.
  - Its large-I object would be a mean-field island-state dynamic with mutation. That is not proposed here. Adopting
    it would re-open REJECTED "the migration game", with the justification that mutation prevents the permanent
    extinctions that sank it at ε = 0.
- [after review] **Other REJECTED entries.**
  - Verdict 10 bears on "Plain islands with mutation stay below 0.1" (09-30; observed 0.13). That is not re-proposed.
  - It also bears on the I = 16 anomaly in "the multilevel threshold is flat in island count".
- **THEORY §9.5 (i)** would be answered for w_g = 0.
