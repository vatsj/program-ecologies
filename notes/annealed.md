# Annealed mutation: a decaying re-injection schedule along Λ_N → 0, N·Λ_N → ∞ (notes, 2026-10-16)

Spec `specs/2026-10-16-annealed-mutation.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict, including the path, the timing and the production schedule).
§1 is written by hand before any code of this run and before any counted cell. §2 (code validation, assays, projected
costs) is appended after the code and before any counted cell.

Base, imported unchanged: the removing-rivals machinery (`src/removing_rivals*.py`: rain kernel, target 𝒯, predator
classifier, island tracker, selected-versus-drift classifier) on the realizable-scaling / provenance language
(grammar P, n = 7, 12,546 spellings, prior L, S-nonself, lack rule, w = 0.3, calibrated mN = (N/100)^0.7). Two
changes, both amendments: production encounters are fixed at **r = 100 per Moran event** at every N (2r = 200
encounters per program per generation, the (200, 64) value), and the re-injection rate is a **function of time**.
Every number from a cell with re-injection is a finite-ε approach-rate diagnostic at finite (N, I, horizon), never π;
ε = 0 cells are lottery statistics.

*Disclosure (before this section).* Before writing it I read the spec, CLAUDE.md, RESULTS "Removing rival networks"
and "The realizable lottery along paths in (N, I, mN)", `notes/removing-rivals.md`, `runs/removing-rivals.md` and the
code; copied the untracked cached tables read-only from the removing-rivals worktree and ran
`tests/test_removing_rivals.py` (5 passed: the copied tables reproduce the stored kernel); and made lookups on stored
data with existing functions: exploitable-holder counts and predator masses per class from
`runs/removing_rivals/ckpt_rows.json.gz`, the exact kernel fixation probabilities (`realizable_scaling.rho_fix`), and
the table relations A[x, 3], A[3, x] for the two rival holders chosen below. No cell of this run has been computed.

## 1. Design

### 1.1 ρ and μ_pred per rival class (recomputed from the removing-rivals Part 0 rows)

Exploitable rival islands at generation 2,000 of the 300 reconstructed runs at N ≥ 200 (260 islands) fall into two
classes with almost no spread inside each class:

| class | islands | mean accessible predator mass μ_pred | commonest holder (unit, spelling) |
|---|---|---|---|
| anti-punishers (AP: defect against anyone certified to defect against DefectBot) | 134 | **0.0741** (0.0729–0.0772) | 8077, `if(CHK(them,them,C),D,if(CHK(them,^D,D),D,C))` (17 islands) |
| certified-defection detectors (DET) | 126 | **0.00568** (0.0054–0.0058) | 12431, `if(or(CHK(them,them,D),CHK(me,them,D)),D,C)` (47 islands) |

**ρ (per-arrival predator colonization).** A predator P of X is defined by A[X, P] = 1, A[P, X] = 0 and no
self-cooperation; with the kernel's payoffs (R 0, T 1, S −2, P −1) it beats X by exactly one payoff unit against every
opponent type, so its fixation is a constant-selection Moran probability. The exact kernel formula gives
ρ_P = 0.2614 / 0.2603 / 0.2597 / 0.2595 at N = 200 / 400 / 800 / 1,600 (→ 1 − e^(−0.3) = 0.2592): **the same for both
classes and N-independent.** The removing-rivals injection assays measured 0.25 (27/110). I use ρ = 0.26.

**Second step.** After the predator fixes, the island is all-defect and the target retakes it: one FairBot-type migrant
fixes with ρ_Z(P) = 0.030 / 0.021 / 0.015 / 0.011 at N = 200 / 400 / 800 / 1,600 (∝ N^−0.5), while migrants arrive at
mN·s_Z with mN = 1.62 / 2.64 / 4.29 / 6.96; at I = 8 with 7 target islands of 8 the retake hazard is 0.043 / 0.049 /
0.057 / 0.066 per generation (15–25 generations): **the second step speeds up slightly with N** and is never the
bottleneck. Predator fixation itself takes ≈ 2 ln N / s ≈ 40–50 generations.

**Rival classes at I = 8.** Part 0 had 1.16% (N = 200) and 0.58% (N = 400) of islands exploitable, halving with N. At
I = 8 a 20-run cell has ≈ 1.9 exploitable islands at N = 200 and ≈ 0.9, 0.5, 0.2 beyond: **the natural cells cannot
measure the cure along the path.** Hence Part F below (a disclosed addition, §1.5).

### 1.2 The path

Arrivals per island are held at the cure exposure of the AP class, **A = N·Λ_N = K/(ρ·μ_pred) = 3/(0.2592·0.0741)
= 156** (K = 3), and A = 52 for K = 1. So Λ_N = A/N = 0.78 / 0.39 / 0.195 / 0.098 at N = 200 / 400 / 800 / 1,600:
Λ_N → 0 with N·Λ_N fixed at the exposure that cures (the amended path; drift colonizations per island ≈ c·A/N → 0 along
it while the cure exposure stays constant).

The same exposure gives the DET class **K_DET = A·ρ·μ_DET = 156·0.26·0.00568 = 0.23** (0.077 at K = 1): one-arrival
formula cure 1 − e^(−0.23) = 0.21. The path is tuned to the anti-punishers; the detectors are 13× harder to prey on.

I = 8 at every N; calibrated mN. Founders drawn as in the scaling run (provenance's stream), S-nonself; the sponsored
arm puts PrudentBot (CBP4, rule H, full list) at C-donor's donor slot on every island (removing-rivals' founders).

### 1.3 The schedule and its delivered fraction

Generation 0 is the seed. No arrivals before generation t_s = 200. From then on fresh founders arrive per
island-generation at

  εN(t) = a·(1 + (t − 200)/t₀)^(−2),  t₀ = N/2,  a = A/t₀ = 2A/N,

so ∫₂₀₀^∞ εN = A. The kernel uses for generation g ≥ 200 the exact integral over [g, g + 1]:
εN_g = A·[t₀/(t₀ + g − 200) − t₀/(t₀ + g + 1 − 200)], i.e. a per-Moran-event probability ε_g = εN_g/N (the sum
telescopes, so the delivered total is exact). Arrivals stop at the horizon g = 10,000; a 2,000-generation
mutation-free chase follows (end at 12,000) so that late lineages resolve.

| N | t₀ | a (εN at onset) | delivered by 10,000: A·T/(T + t₀), T = 9,800 | by 2,000 | constant-rain εN (arm iv) |
|---|---|---|---|---|---|
| 200 | 100 | 1.56 | 0.990 (154.6) | 0.947 | 0.01578 |
| 400 | 200 | 0.78 | 0.980 (153.1) | 0.900 | 0.01562 |
| 800 | 400 | 0.39 | 0.961 (150.1) | 0.818 | 0.01531 |
| 1,600 | 800 | 0.195 | **0.925** (144.5) | 0.692 | 0.01474 |

(The onset rate at N = 200 is 1.56, a little above the amendment's "≤ 1.5"; it is the rate the path implies.) **Arm
(iv)** delivers the same total as the annealed schedule delivers by 10,000, uniformly over generations 200–10,000.

**Pairing (amendment 4).** All arms of a replicate share the seed founders (provenance's stream; the sponsored arm
differs in one slot per island), the kernel's event-indexed draws, and **the sequence of fresh-founder spellings per
island**: the n-th arrival on island i has the spelling given by a counter-based draw indexed by (i, n), not by the
event, so the annealed and constant schedules (and K = 1 against K = 3) see the same founders in the same order on
each island, only at different times. The arrival coin stays event-indexed. Realized arrival counts are reported. A
flag restores removing-rivals' event-indexed spelling draw, for the validation in §1.7.

### 1.4 The drift classifier (removing-rivals §1.9, unchanged) and colonization logs

- Lineages: every fresh founder gets a lineage id; newborns copy a parent individual's id (the type-level birth resolved
  to individuals, draw 7); seeded individuals carry 0.
- **Colonization:** a rain lineage holding ≥ 0.5 of an island at a 5-generation checkpoint (first time per lineage and
  island; a lineage that migrates and colonizes another island counts there as a migrant colonization).
- **Class at arrival:** the founder's phenotype p against the island's majority type X at arrival (the kernel's own
  production repeated to a fixed point): *selected* iff pay(p, X) > pay(X, X); *neutral* if equal; *deleterious* if
  less. **Drift = neutral or deleterious.**
- Logged per colonization: arrival generation, island status at arrival (target / rival / unheld), majority share,
  class, spelling and phenotype, colonization generation, and **fate**: the lineage's maximum share, its share at the
  end, fixation (share 1 at a checkpoint) and the island's status at the end; *unresolved* if 0 < share < 1 at 12,000.
- **Shadow on target:** a drift colonization of an island that was a target island at arrival. **Drift on rival:**
  status rival at arrival. **Other:** unheld at arrival.
- **The RS's criterion per run:** zero drift colonizations from generation 200 to the end (the only arrivals are
  post-establishment). Reported per cell as the fraction of drift-free runs (Wilson intervals).

### 1.5 Cells

Common: I = 8, calibrated mN, r = 100, horizon 10,000 + 2,000 chase, snapshots at 200, 1,000, 2,000, 5,000, 10,000,
12,000; tracker every 5 generations; 20 replicates (0–19) per cell.

**Natural cells** (N ∈ {200, 400, 800, 1,600}):
- (i) S-nonself + annealed, K = 3; (ii) sponsored PrudentBot + annealed, K = 3; (iii) S-nonself and sponsored at
  ε = 0; (iv) S-nonself + constant rain, K = 3 (same total; arm (iv) is run for S-nonself, the main arm; the sponsored
  arm's schedule comparison is not run).
- K = 1: (i) and (ii) at N = 200 and 800.
- 24 cells, 480 runs. ε = 0 cells stop early when frozen (one global type whose encounters change nothing), as in
  removing-rivals.

**Part F, forced rivals (an addition to the spec, disclosed now: natural exploitable rivals are too rare at I = 8).**
An archipelago of I = 8 islands: island 0 all X (the class's commonest holder unit and spelling, rule S-nonself),
islands 1–7 all FairBot (`if(CHK(them,me,C),C,D)`, unit 3, the commonest target holder; S-nonself). X and FairBot are
mutually defecting (A = 0 both ways) and both self-cooperate, so the X island is a bridge-less rival (barrier 7·10⁻⁹ at
N = 200, smaller beyond). The annealed K = 3 schedule (onset 200), N ∈ {200, 400, 800, 1,600}, classes AP (8077) and
DET (12431), 20 replicates; K = 1 at N = 200 and 800. One X island per run matches the natural density (about one per
run at most) and avoids the correlated cures of four X islands seen in removing-rivals' triples. Outcome: the X island
resolved to target by 12,000 (removing-rivals §1.6: target for ≥ 25 generations), by path (predator step / direct /
other), direct (a predator lineage that arrived on island 0) versus migrant-mediated; and drift colonizations on the
seven FairBot islands.

**Single-arrival assays (amendment 5)** on frozen residents, ε = 0, at each N:
- *Neutral:* one fresh `C` (CooperateBot, μ = 0.0041, the commonest drift colonizer) and, separately, one fresh
  `if(CHK(them,^D,D),C,D)` (an identity-exploitable target shadow, μ = 5.2·10⁻⁴) into one all-FairBot island (I = 1,
  no migration); stopped when the lineage is lost or fixed (cap 6N generations). Colonization (≥ 0.5) and fixation
  probability against 2/N and 1/N; conditional times.
- *Predator:* the top accessible predator of each class (by prior mass) into island 0 of the Part F archipelago at
  generation 0, ε = 0; establishment (lineage ≥ 0.5), completion (island 0 a target island for ≥ 25 generations) and
  times; stopped at loss or completion (cap 3,000 generations).
Replicate counts are set in §2 from probe costs.

**Drop order** (applied only if the projected total exceeds about 24 hours on 3 workers, disclosed in §2 before any
affected cell): (1) the K = 1 natural cells; (2) the K = 1 Part F cells; (3) arm (iv) at N = 200; (4) runs at
N = 1,600 cut from 20 to 10 in arm (ii) and (iii)-sponsored.

### 1.6 Statistics and endpoints

Per cell, at 2,000, 10,000 and 12,000 (12,000 primary): drift and selected colonizations per island by class and by
status at arrival; drift-free runs; colonization fates; exploitable rival islands at onset and their cures (natural
cells, pooled); identity islands and **identity takeovers of target islands** (a target episode followed, before the
island is target again, by an identity holder for ≥ 25 generations; *late* if it starts at or after generation 2,000;
*permanent* if identity holds the island at 12,000); **secondary takeovers of shadows** (an island drift-colonized by a
shadow on target that afterwards leaves target status for ≥ 25 generations: to identity, to a rival, or unheld);
universal-on-target (uot, the removing-rivals target 𝒯 frozen there), universal-open (provenance's definition);
island efficiency (P(C,C) ≥ 0.95), reported, never used to select. Intervals are run-clustered (bootstrap over runs);
counts of runs carry Wilson intervals. **Drift scaling:** drift colonizations per island against N, the slope of a
Poisson regression of per-run counts on log N (arm (i) primary; pooled (i), (ii), (iv) with arm indicators beside it),
with a run-bootstrap interval.

### 1.7 Validation plan (before any counted cell)

1. ε = 0: the new kernel equals removing-rivals' and the scaling kernel draw for draw (states identical after 150
   generations at (200, 8) and at (400, 8) with r = 100 in both); stored scaling runs at N = 200 (r = 100 is the native
   r = N/2 there) reconstruct to generation 2,000 with 0 trace differences (the "r = 100 against native r at N = 200"
   check is this identity). A paired native-r (r = 200) cell at (400, 8), ε = 0, is run beside (iii) if §2's costs
   allow, so the effect of fixing r is reported, not assumed.
2. The schedule integrates to the table's delivered totals (test), and realized arrivals match within sampling error.
3. With the event-indexed flag and a constant rate, the kernel reproduces a stored removing-rivals B2 run (rain
   εN = 0.1, (200, 64)) draw for draw to generation 2,000, and the drift classifier gives the stored classes for every
   colonization in that window ("agreement on stored lineages").
4. Part F founders and the sponsored founders as specified (test).

### 1.8 Hand predictions

- **Drift scales as 1/N with a rate correction.** Per arrival, a drift colonization had probability c with c·N ≈ 0.21
  / 0.12 / 0.03 at εN = 0.01 / 0.1 / 1 in removing-rivals (the same at N = 200 and 400): the per-arrival rate falls at
  high εN. The annealed schedule delivers about three quarters of its arrivals at εN > 0.1 at N = 200 (onset 1.56) but
  at εN ≤ 0.2 at N = 1,600 (onset 0.195). So drift per island ≈ A·c/N ≈ 0.08 (N = 200), 0.05, 0.03, 0.015 (N = 1,600):
  **slope ≈ −0.8** for the annealed arm, ≈ −1.0 for constant rain (whose εN ≈ 0.015 everywhere, c·N ≈ 0.2: 0.16 per
  island at N = 200 → 0.018 at 1,600). Annealed/constant drift ≈ 0.5 at N = 200 and ≈ 0.85 at 1,600.
- **The RS's criterion per run** (8 islands, Poisson): drift-free runs ≈ e^(−8d) ≈ 0.5 / 0.65 / 0.8 / 0.9 at N = 200 /
  400 / 800 / 1,600 under annealing. Pooled over a 20-run cell at N = 1,600, ≈ 2–4 drift colonizations, so "never"
  fails as a cell statement at every N but holds per run with probability rising to ≈ 0.9.
- **Cures (Part F).** By the one-arrival formula, AP 1 − e^(−3) = 0.95 and DET 0.21 at every N. Removing-rivals B1
  cured more than the formula at low rates (AP 0.97, DET 0.38 at εN = 0.01 against 0.86 and 0.14), a hazard multiplier
  κ ≈ 1.8 (AP) and 1.3–3.2 (DET). So AP ≥ 0.95 and DET 0.2–0.5 at every N, N-independent; K = 1: AP ≈ 0.65–0.85, DET
  0.07–0.2. Natural-mix cure (0.52 AP, 0.48 DET) ≈ 0.6–0.75.
- **Neutral assays:** colonization ≈ 2/N and fixation ≈ 1/N for `C` on FairBot; the shadow slightly less (it is
  neutral only once its D-certificate relation to FairBot is settled). Predator establishment 0.2–0.3 at every N.
- **Identity.** At I = 8 the seed carries ≈ 1.1 / 2.3 / 4.6 / 9.1 TwinD copies per run (μ_Q = 7.1·10⁻⁴ per founder)
  with per-copy establishment falling with N; identity islands at ε = 0 ≈ 0.01–0.03 per island. Rain adds identity
  through exploitable target shadows and TwinD arrivals (μ_Q·A ≈ 0.11 per island over the schedule); at I = 8 the
  migrant supply is small, so the increase is ≤ 0.03 per island and takeovers of target islands are a few per cell,
  too few to separate the schedules.
- **uot at I = 8** is higher than at 64 islands (fewer islands to fail): S-nonself ε = 0 ≈ 0.5–0.8, sponsored ≈ 0.6–0.9.

## 2. Code validation, single-arrival assays, costs (appended after the code, before any counted cell)

Code: `src/annealed_kern.py` (removing-rivals' rain kernel copied, with a per-generation rate array and per-island
paired founder streams), `src/annealed.py` (schedules, cells, the run object with r = 100, Part F founders),
`src/annealed_run.py` (cells, assays, validation, probes), `src/annealed_report.py`; `tests/test_annealed.py`
(5 tests, passing; 4 need the cached tables and skip without them). Validation output in
`runs/annealed-validate.json`.

### 2.1 Validation

- **The schedule** integrates to A·T/(T + t₀) exactly (154.6 / 153.1 / 150.1 / 144.4 arrivals per island by 10,000 at
  N = 200 / 400 / 800 / 1,600; 0 before 200); the constant arm delivers the same total (test). Probe runs realized
  1,210 arrivals on 8 islands at N = 200 by generation 4,000 (expected 1,197) and 985 at N = 1,600 (expected 975).
- **ε = 0 is the scaling kernel and removing-rivals' kernel.** States identical after 150 generations at (200, 8) and
  at (400, 8) with r = 100 in all three kernels (test). Four stored scaling runs (S-nonself, (200, 64), calibrated,
  replicates 0–3) reconstruct to generation 2,000 with **0 differences over 160 trace points**: since r = 100 is the
  native r = N/2 at N = 200, this is the "r = 100 against native r at N = 200" check, an identity.
- **Removing-rivals' rain is reproduced draw for draw** in the event-indexed mode: arrival records, lineages and states
  identical to `RRRun` at εN = 0.1 after 250 generations (test); two stored B2 runs (rr_rain01_200_64, replicates 0
  and 1) rerun to generation 2,000 give identical snapshots at 500 / 1,000 / 2,000 and **the same 6 + 6 colonizations
  with the same arrival generation, colonization generation, class, status at arrival and spelling** (the drift
  classifier's agreement on stored lineages).
- **Paired founder streams:** the annealed and constant-rain runs of one replicate see the same spelling sequence on
  every island (prefix-equal), and are identical up to the onset (test).
- **Founders:** Part F islands as specified (island 0 all X, islands 1–7 FairBot unit 3); the sponsored arm differs
  from S-nonself in at most one slot per island, PrudentBot's H unit 123 at C-donor's donor slot (test).

### 2.2 Single-arrival assays (amendment 5; `runs/annealed/assay_*.json`)

Neutral arrivals into one all-FairBot island (I = 1, ε = 0), colonization = lineage ≥ 0.5 at a 5-generation
checkpoint:

| N | `C`: reps | colonize (÷ 2/N) | fix (÷ 1/N) | median fixation time | shadow `if(CHK(them,^D,D),C,D)`: reps | colonize (÷ 2/N) | fix (÷ 1/N) |
|---|---|---|---|---|---|---|---|
| 200 | 10,000 | 0.0091 (0.91) | 0.0050 (1.00) | 175 | 5,000 | 0.0092 (0.92) | 0.0050 (1.00) |
| 400 | 10,000 | 0.0044 (0.88) | 0.0019 (0.76) | 347 | 5,000 | 0.0044 (0.88) | 0.0020 (0.80) |
| 800 | 20,000 | 0.0023 (0.92) | 0.0011 (0.88) | 701 | 10,000 | 0.0017 (0.68) | 0.0006 (0.48) |
| 1,600 | 40,000 | 0.0016 (1.24) | 0.0009 (1.36) | 1,237 | 20,000 | 0.0017 (1.32) | 0.0009 (1.44) |

A neutral single arrival colonizes at 2/N and fixes at 1/N within sampling error at every N (none censored; fixation
takes ≈ 0.8 N generations). The shadow is as neutral as `C` (the N = 800 dip is 17 events).

Predator arrivals into island 0 of the Part F archipelago (1 X + 7 FairBot, calibrated mN, ε = 0), 400 replicates per
cell, independent seeds per class; the top accessible predators are `if(CHK(them,me,D),C,D)` (AP, μ = 5.2·10⁻⁴) and
`if(and(CHK(them,me,C),CHK(them,me,D)),C,D)` (DET, μ = 1.3·10⁻⁴):

| N | AP establish [Wilson] | DET establish | completed (island 0 target ≥ 25 gen) given establishment | median / 90% completion time |
|---|---|---|---|---|
| 200 | 0.22 [0.18, 0.27] | 0.26 [0.22, 0.31] | 1.00 / 1.00 | 75 / 98–105 |
| 400 | 0.26 [0.22, 0.30] | 0.28 [0.24, 0.32] | 1.00 / 1.00 | 85 / 105 |
| 800 | 0.26 [0.22, 0.31] | 0.25 [0.21, 0.30] | 1.00 / 1.00 | 90 / 104–110 |
| 1,600 | 0.23 [0.19, 0.27] | 0.23 [0.19, 0.27] | 1.00 / 1.00 | 95 / 105–110 |

Per-arrival predator cure = 0.22–0.28 at every N (exact ρ 0.26), every establishment completes within ≈ 110
generations, and the two classes are the same process (identical payoff structure; with common seeds the trajectories
coincide, so the classes were given independent seeds). **The single-arrival quantities behind the path are as
assumed: ρ is N-independent and neutral colonization is 2/N.** The classes differ only in predator mass.

### 2.3 Costs and an extension (declared before any cell)

Probe costs per run of 4,000 generations (one worker, while two sibling runs used 6 cores): arm (i) 3 / 18 / 57 s at
N = 200 / 800 / 1,600; arm (iv) 3 / – / 56 s; arm (iii) 23 s at 1,600; Part F DET 39 s at 1,600. Projected for the
full design (12,000 generations): natural cells ≈ 13,000 worker-s, Part F ≈ 7,000, K = 1 ≈ 5,000: about 7 worker-h,
2.5 h on 3 workers, far below the 24-hour line. **No drop-order step is applied**, and two additions are made because
the drift and cure statistics are count-limited (≈ 2–4 drift colonizations expected per 20-run cell at N = 1,600):

- **40 replicates (0–39)** in arms (i), (iii)-S-nonself and (iv) at every N and in the Part F K = 3 cells; 20
  replicates (0–19) elsewhere. Verdicts use all replicates; the 0–19 subset is reported beside the arm-(i) drift
  numbers.
- **The native-r control** (`an_iiiSnat_400`: S-nonself, (400, 8), r = 200, ε = 0, 20 replicates) runs beside (iii).

Projected total with the extension ≈ 16 worker-h, ≈ 5.5 h on 3 workers. Order: arms (i), (iv), (iii)-S (40 runs) →
Part F K = 3 (40) → arms (ii), (iii)-sponsored (20) → K = 1 cells and the native-r control (20)
(`runs/annealed/cells.sh`, resumable).
