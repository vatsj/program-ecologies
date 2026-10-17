# An identity-resistant target: run report (2026-10-17)

Spec `specs/2026-10-17-identity-resistant-target.md`; notes `notes/identity-resistant.md` (§1 design, §2 validation,
executed check, M1 assays, costs); predictions `predictions/2026-10-17-identity-resistant-target.md` (committed before
any counted cell). Summary JSON `runs/identity-resistant.json` (from `src/identity_resistant_report.py`); rows
`runs/identity_resistant/cells_{eps0,rain800,rain1600,rain1600b,rain1600c}.json.gz`, M1 rows
`runs/identity_resistant/assay_m1_{200,800}.json.gz`; static `runs/identity-resistant-{static,exec,validate}.json`.
ε = 0 cells are lottery statistics at finite (N, I, horizon); rain cells are finite-ε approach-rate diagnostics, never
π. Rm and Rp are counterfactual surgery on the mutation prior (amendment 1), not designs.

## Process and disclosures

- All three parts' L arms reproduce stored runs: Part I against Pangaea `pg_L_100_128_r100_ff200` (0 differences
  over 132 points, replicates 0–2), Part II against the scaling traces and `rr_spon_200_64`, and **all 160 Part III L
  runs equal the stored annealed rows at 12,000** (uot, identity, target, every holder spelling, arrival totals; checked
  after the cells). The L numbers below are therefore also the stored runs' numbers.
- M1 injected the heaviest spelling of each of the four TwinD run trees (500 replicates each) instead of one spelling
  (notes §2.4, before any cell); the RE 4 / RE 5 composite uses M1 at N = 800 for both rain sizes (M1 has no N = 1,600).
- The (1,600, 8) batch was split, while it ran, into three drivers on disjoint replicate ranges (0–29 on 2 workers;
  30–31 on 1; 32–39 on 2) so that a 2.8-hour straggler (`const_L_1600` replicate 31, stored at 10,618 s) did not idle
  the pool; never more than 3 workers of mine; one aborted launch wrote no rows; no run duplicated or lost.
- No drop-order step was needed: 640 counted runs, 18.9 worker-hours (projected ≈ 31).

## Static (notes §1.2–1.4, §2.2–2.3)

- 𝒯 = 235 units: **165 exploitable, 70 resistant**, the same on the ideal table and on 28,120 executed plays (0
  disagreements), and the same for every challenge set tried (4 stored holders, 8 S-nonself-reachable identity units,
  21-unit universe). No run tree mixes classes. μ_L(E) = 0.0279 (0.0268 of it suckers to certified defectors),
  μ_L(Res) = 0.0123.
- **Guard:** 50 of 70 resistant units guarded (0.714), 0 of 165 exploitable; every guarded unit is unexploitable by
  any unit of the universe; 13 unguarded resistant units are too; 7 are exploitable by non-identity units.
- Occupancy in the stored runs: exploitable members hold 355 of 23,078 target islands (0.015).

## M1: forced TwinD challenges (one island, ε = 0; takeover per arrival, 500 replicates per cell)

| holder | class | TwinD trees selected | Q-weighted takeover, N = 200 / 800 |
|---|---|---|---|
| 31 `if(CHK(them,^D,D),C,D)` | exploitable | 4 of 4 | 0.251 / 0.247 |
| 87 `if(CHK(them,me,C),C,if(CHK(them,them,C),C,D))` | exploitable | 2 of 4 (the C-listed trees) | 0.097 / 0.091 |
| 3851 `if(or(not(CHK(me,them,D)),CHK(them,them,C)),C,D)` | exploitable | 2 of 4 | 0.097 / 0.091 |
| FairBot, PrudentBot, 183 `if(or(CHK(them,me,C),CHK(me,^D,C)),C,D)` | resistant | 0 of 4 | 0 / 0 (0 of 12,000) |

A selected TwinD arrival takes the island at the predator's ρ (0.21–0.27 per tree) in a median 22–30 generations; a
deleterious one never did.

## Part I: fission–fusion, ε = 0 ((100, 128), merged at 200 into 12,800; 20 runs; horizon 2,200)

| prior | sponsor | universal-open | uot₂₃₅ | uot₇₀ | identity islands at the merge (of 2,560) | target islands held by Res / E at the merge | unheld at the merge | max identity share after the merge |
|---|---|---|---|---|---|---|---|---|
| L | no | 20 | 18 | 18 | 135 | 1,961 / 11 | 238 | 0.25 |
| Rm | no | 20 | 19 | 19 | 76 | 2,409 / 0 | 26 | 0.24 |
| Rp | no | **19** | 18 | 18 | 146 | 1,976 / 0 | 355 | **1.00** |
| L | yes | 20 | 20 | 20 | 54 | 2,366 / 16 | 38 | 0.09 |
| Rm | yes | 20 | 20 | 20 | 33 | 2,440 / 0 | 14 | 0.05 |
| Rp | yes | 20 | 20 | 20 | 98 | 2,389 / 0 | 30 | 0.16 |

- **uot₇₀ = uot₂₃₅ in every run**; the exploitable share of the merged population is 0 in every run (they never hold
  the network).
- **One clique took a whole merged population** (Rp unsponsored, replicate 8): a single TwinD quote held 68 of 128
  islands at generation 200 (0.585 of the population at the merge) and the merged population at 250. Its paired L run
  had 16 clique islands. Fission–fusion erases cliques only while they are minorities at the merge.
- Universal-open but not on target (the target's drift away): L 2 runs (a closed-open network
  `if(not(or(CHK(them,me,C),CHK(me,them,D))),D,C)`, target share 0.46–0.56), Rm 1 (target share 0.91), Rp 1.
- **M2 (per seeded copy, island held at 200 by a tree of the class seeded there):** L unsponsored Res 0.044, E 0.0001,
  TwinD 0.074, FairBot 0.127; Rm Res 0.033, TwinD 0.078.
- Paired: every prior difference is within ±1 run (McNemar p ≥ 0.5); sponsor vs not under L +0.10.

## Part II: islands (200, 64), ε = 0 (20 runs; horizon 10,000)

| prior | sponsor | uot₂₃₅ 2,000 / 10,000 | uot₇₀ 10,000 | identity islands (runs) | closed-open | exploitable rivals | Res / E target islands | unheld at 200 | islands held by PrudentBot's tree at 2,000 |
|---|---|---|---|---|---|---|---|---|---|
| L | no | 11 / 11 | 11 | 72 (7) | 202 | 14 | 992 / 0 | 146 | 0 |
| Rm | no | 11 / 11 | 11 | 14 (9) | 0 | 6 | 1,260 / 0 | 3 | 22 |
| Rp | no | 10 / 10 | 10 | 38 (8) | 174 | 9 | 1,059 / 0 | 70 | 28 |
| L | yes | 15 / 15 | 13 | 25 (5) | 0 | 0 | 1,216 / 39 | 95 | 725 |
| Rm | yes | 8 / 9 | 9 | 11 (4) | 0 | 29 | 1,240 / 0 | 4 | 314 |
| Rp | yes | 7 / 7 | 7 | 120 (11) | 0 | 23 | 1,137 / 0 | 32 | 565 |

(Counts pooled over 20 runs, at 10,000 unless stated; closed-open at 2,000 is 125 / 24 / 63 unsponsored.)

- **Paired uot₂₃₅ at 10,000:** Rm − L = 0.00 (5 gains, 5 losses) unsponsored, −0.30 (3 / 9, p = 0.15) sponsored;
  Rp − L = −0.05 unsponsored, **−0.40 sponsored (0 / 8, p = 0.008)**. Sponsor − none under L +0.20 (8 / 4).
- **Per-copy clique establishment is unchanged** (TwinD copies holding their island at 2,000: L 0.046, Rm 0.052, Rp
  0.052): R-move cuts clique *export* (identity islands 72 → 14), not clique *establishment*, and uot needs no clique at
  all, so it does not move (runs with a clique 7 → 9).
- **Without the sucker mass the sponsor's prudence has less to eat:** PrudentBot's tree holds 725 islands at 2,000 under
  L sponsored, 314 under Rm and 565 under Rp; failures are anti-punisher and detector rivals (Rm: 29 islands in 9 runs,
  0 under L; e.g. `if(CHK(them,^D,D),if(CHK(me,them,D),C,D),C)`) and identity (Rp: 120 islands in 11 runs).
  Exploitable members are suckers that every establisher exploits in the scramble; they are scramble fuel.

## Part III: rain at I = 8 (40 runs per cell; 12,000 generations)

| N | schedule | prior | uot₂₃₅ (uot₇₀) | identity islands at 200 / 12,000 | all-defect runs | identity arrivals | identity takeovers of target islands (prey) | exploitable share of target island-generations | drift colonizations of target islands |
|---|---|---|---|---|---|---|---|---|---|
| 800 | annealed | L | 21 (21) | 30 / 39 | 5 | 36 | 0 (0) | 0.014 | 7 |
| 800 | annealed | Rm | **34 (34)** | 7 / 7 | 0 | 36 | 0 | 0 | 4 |
| 800 | annealed | Rp | 26 (26) | 19 / 24 | 4 | 36 | 4 (0; one run, migrant, gen 320–350) | 0 | 3 |
| 800 | constant | L | 22 (22) | 30 / 40 | 5 | 34 | 0 | 0.023 | 9 |
| 800 | constant | Rm | **33 (33)** | 7 / 7 | 0 | 34 | 0 | 0 | 3 |
| 800 | constant | Rp | 20 (20) | 19 / 20 | 8 | 34 | 0 | 0 | 5 |
| 1,600 | annealed | L | 30 (29) | 11 / 12 | 0 | 39 | 0 | 0.031 | 5 |
| 1,600 | annealed | Rm | **40 (40)** | 0 / 0 | 0 | 39 | 0 | 0 | 1 |
| 1,600 | constant | L | 28 (28) | 11 / 20 | 1 | 39 | 8 (1; one run) | 0.015 | 4 |
| 1,600 | constant | Rm | **39 (39)** | 0 / 0 | 0 | 39 | 0 | 0 | 1 |

- **Paired uot Rm − L:** +0.325 (16 / 3, p = 0.004) and +0.275 (16 / 5, p = 0.027) at 800; +0.25 (10 / 0, p = 0.002)
  and +0.275 (12 / 1, p = 0.003) at 1,600. **Rp − L:** +0.125 (p = 0.40) and −0.05 (p = 0.82) at 800.
- **The gain is in the seed, before any arrival:** identity islands at onset 30 → 7 (800) and 11 → 0 (1,600); all-defect
  runs 5 → 0 (800). Rp, which removes the same exploitable mass without boosting the resistant establishers, keeps
  most of L's seed failures (19 clique islands, 4–8 all-defect runs) and gains nothing in uot.
- **The prey channel under L:** one event in 160 L runs, the annealed run's whole-run loss reproduced (constant rain,
  N = 1,600, replicate 7: all eight islands held by exploitable unit 87; a selected TwinD arrival at generation 6,360
  took one island, migrants the other seven within 25 generations). Exploitable holders occupy 1.4–3.1% of target
  island-generations under L, 0 under Rm and Rp.
- **Per identity arrival** (pooled over both N and schedules, 148 arrivals per prior): prey takeovers L 1 (0.0068),
  Rm 0; all identity takeovers L 8 (0.054), Rm 0; composite κ (notes §1.7) L 0.0039, Rm 0, Rp (800) 0.
- **Drift** (pooled): drift colonizations of target islands per target island-generation Rm / L = 0.28 [0.12, 0.55];
  into unconditional cooperators 0.18 [0.04, 0.43]. Counts are small (L 25, Rm 9 target-island drift colonizations).

## Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | ≥ 0.9 of resistant units guarded; no guarded unit exploitable | **inconclusive** (0.714; falsifier < 0.7 not fired; 0 guarded units exploitable) |
| RE 2 | fission–fusion universal-open ≥ 0.95 under every prior; sponsored-L uot ≥ 0.9 | **supported** (20/20/19/20/20/20; sponsored-L uot₂₃₅ 20/20) |
| RE 3 | (200, 64): Rm uot within 0.1 of L | **supported** (g = 0.00 at 2,000 and 10,000; exact interval ±0.31) |
| RE 4 | Rm prey takeovers per identity arrival ≤ 0.2 of L's | counts **inconclusive** (L 1 < 3); composite **supported** (κ_Rm / κ_L = 0), by construction: Rm has no exploitable target unit |
| RE 5 | Rp identity takeovers under rain ≥ 0.5 of L's | counts **inconclusive** (L 0 at (800, 8); Rp 4, one run); composite **contradicted** (κ_Rp / κ_L = 0): the control removes the exploitable members too |
| Sol (a) | syntax misses semantics | **held** (20 of 70 unguarded) |
| Sol (b) | prey declines but combined bounds fail (Rm uot gain < 0.1 under rain) | prey clause held; **bounds clause failed** (Rm +0.25 to +0.33 at both N) |
| Sol (c) | sponsor matters (≥ 0.15) | **held** in Part II (+0.20); Part I +0.10 |
| Sol (d) | unsponsored Rm universal-open without target | **held** (Part I, 1 run) |
| Gemini (a) | > 10% of resistant units unguarded, guard sufficient | **held** (29%) |
| Gemini (b) | R-move works by founder boosting | **not supported as scored** (Part II: no uot gain); in substance held in Part III (the gain is at the seed; Rp gains nothing) |
| S1 | executed = table | held (0 of 28,120) |
| S2 | fission–fusion unsponsored ranges | held |
| S3 | sponsored ≥ 19/20 | held (20/20 ×3) |
| S4 | uot₇₀ tracks uot₂₃₅ on the merged population | held (equal in every run; exploitable share 0) |
| S5 | Part II Rm +3 to +7 runs; closed-open −40%, identity −30% | **falsifier fired** (gain 0); the island clauses held (−81%, −81%) |
| S6 | Rp within ±2 runs of L | **falsifier fired** (sponsored −8) |
| S7 | sponsored Rm 17–20 | **falsifier fired** (9 < L's 15) |
| S8 | per-copy Res ≥ 5× E | held (≈ 400×) |
| S9 | TwinD takeover ≥ 0.2 into every exploitable holder, ≤ 0.003 into resistant | **falsifier fired** for holders 87 and 3851 (0.091–0.097); held for 31 and every resistant holder |
| S10 | L prey ≤ 3, Rm 0 | held (1, 0) |
| S11 | drift Rm ≥ L; UC drift ratio in [0.7, 1.3] | **falsifier fired** (Rm drift 0.28× L, UC drift 0.18× [0.04, 0.43]) |
| S12 | identity islands Rm ≤ L; Rp within ±30% | first clause held (14 vs 111); Rp clause failed (44 vs 79 at 800); falsifier not fired |
| S13 | rain uot Rm − L within ±0.15 | **falsifier fired** (+0.25 to +0.33) |

## Reading

- The identity-resistance partition is clean (165 / 70, executed = ideal) and the channel it names is real and narrow:
  a TwinD arrival takes an exploitable holder's island at the predator's ρ and never takes a resistant one.
- Closing that channel is not what moves universality. Removing the exploitable members (Rp) closes the prey channel
  as completely as R-move and buys nothing; R-move's gains under rain (+0.25 to +0.33) and its full universality at
  1,600 come from the seed: 3.3× more resistant establishers cut clique establishment and scramble losses at N ≥ 800.
- At (200, 64) the seed effect stops at export: per-copy clique establishment is unchanged and uot does not move; with
  the sponsored PrudentBot, removing the sucker mass costs 0.30–0.40 of uot (the sponsor's prudence eats it in the
  scramble).
- Under L at these sizes the prey channel fires once in 160 runs, the stored annealed whole-run loss.
- Fission–fusion holds under every prior except once: a clique that is a majority at the merge wins the merged
  population (Rp, 1 of 120 Part I runs).
