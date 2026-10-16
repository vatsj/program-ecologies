# Cliques on a Pangaea: from many islands to one at fixed total population (notes, 2026-10-16)

Spec `specs/2026-10-16-pangaea.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after review"
supersede the earlier text where they conflict). §1 is written by hand before any code of this run and before any
counted cell. §1.8 (code validation, deterministic family dynamics) and §2 (projected and measured costs) are appended
after the code and before any counted cell.

Base, imported unchanged: provenance and the realizable-scaling run (`src/provenance*.py`, `src/realizable_scaling*.py`)
on milestone 5's language, grammar (P at n = 7, 12,546 spellings, prior L), lack rule, would-be-self adoption check,
S-nonself rule, cached tables and holder-based endpoints. ε = 0, iid L seeds, w = 0.3, calibrated mN = (N/100)^0.7
where I > 1. Time in generations of N·I Moran events. Every number here is an ε = 0 lottery statistic at finite
(N, I, horizon), never π.

*Disclosure (before any code).* The cached static tables (`runs/lt_genes/static/`, `runs/provenance/{static/, OSV.npy,
SPO.npy, sets.npz, prod_exec.json}`) are untracked. They were cloned (copy-on-write, nothing modified at the source)
from the realizable-scaling worktree, where they had been rebuilt by the stored commands and validated against the
tracked summaries; the tracked `static_ext.json`, `osv.json` and `sets.json` here are byte-identical to that copy. The
clone is validated again by draw-for-draw reproduction of stored scaling rows (§1.7) before any counted cell. The
static lookups quoted in §1.1 were made with throwaway scripts on these tables; no lottery dynamics of any kind had
been run.

## 1. Design

### 1.0 The object in one paragraph

Hold the total population N·I fixed and move along I, from the island geometry where identity cliques are known to
win locally ((200, 64): 11/20 universal-open; per-copy clique establishment ≈ 0.04 at N = 200) to one well-mixed
population of N·I (the Pangaea). The RS predicts the cliques fail on the Pangaea "where universality pays off". The
run measures where along I the clique stops winning, and checks what replaces it on the Pangaea: which network wins,
whether it is the target (PrudentBot's network), and whether the win is a frequency effect or repaired production.

### 1.1 The frequency-dependence argument, made exact for the seed's families

**Payoffs.** PAYM (row player's payoff, D = 0, C = 1) is CC 0, CD −2, DC 1, DD −1, i.e. PAYM[a][b] = −1 + 2b − a: a
donation game with b = 2, c = 1. In a well-mixed population with type frequencies x the kernel's fitness (mean payoff
against the others, N large) is exactly

  f_k = −1 + 2·(mass that cooperates with k) − (mass k cooperates with).

Selection is birth ∝ e^(w·f), so a family's growth rate relative to D is ≈ w·(f_k − f_D) per generation.

**Families** (classes of spellings by their H unit, i.e. certificates saturated; prior mass L; the class-to-class
numbers are mass-weighted cooperation probabilities, row cooperates with column, from the A table; same quote counted
as self-play):

| class | definition (H unit) | mass |
|---|---|---|
| D | non-self-cooperating, defects against D-H, AP-H defects against it (legible defector) | 0.379 |
| Dill | non-self-cooperating, defects against D-H, AP-H cooperates with it (illegible defector) | 0.073 |
| S | self-cooperating sucker (cooperates with D-H) | 0.429 |
| S− | non-self-cooperating, cooperates with D-H | 0.059 |
| PBn | establisher (self-cooperating, defects against D-H) mutual with CB-H and with PB-H, not with AP-H | 0.0126 |
| CBo | establisher mutual with CB-H, not with PB-H nor AP-H | 0.0014 |
| BR | establisher mutual with both CB-H and AP-H (bridges) | 0.0140 |
| APn | establisher mutual with AP-H, not with CB-H | 0.0316 |
| TW | the TwinD family Q (identity units: cooperate only with their own quote) | 0.0007 |
| Eo | other establishers | 0.0008 |

CB = `if(CHK(them,me,C),C,D)` (FairBot-shaped carrier), PB = `if(and(CHK(them,me,C),CHK(them,^D,D)),C,D)`
(PrudentBot), AP = `if(CHK(them,^D,D),D,C)` ("cooperate with whoever cannot certify that it defects against ^D"; it
never acquires a certificate, PD and production futile, so its H unit is its E unit). Cooperation matrix at H:

|  | D | Dill | S | S− | PBn | CBo | BR | APn | TW |
|---|---|---|---|---|---|---|---|---|---|
| **PBn** | 0.05 | 0.03 | 0.68 | 0.39 | 0.98 | 0.86 | 0.81 | 0.00 | 0.05 |
| **CBo** | 0.04 | 0.04 | 0.66 | 0.37 | 0.86 | 1.00 | 0.90 | 0.00 | 0.00 |
| **BR** | 0.39 | 0.60 | 1.00 | 0.94 | 0.99 | 1.00 | 1.00 | 1.00 | 0.87 |
| **APn** | 0.13 | **0.94** | 0.86 | 0.72 | 0.11 | 0.95 | 0.88 | 1.00 | 0.06 |
| **TW** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.29 |
| **Dill** | 0.04 | 0.10 | 0.20 | 0.19 | 0.05 | 0.20 | 0.21 | 0.20 | 0.02 |
| **S** | 0.99 | 0.93 | 0.90 | 0.94 | 0.96 | 0.91 | 0.89 | 0.93 | 1.00 |

Fitness against the prior at H (exact, all 4,162 H units): D −0.024, TW representative −0.026, PB −0.083, CB −0.449,
AP −0.597, C −1.023.

**Certification state.** At t = 0 every S-nonself founder is its E unit (empty lists). In the E state PBn, CBo and D
are defectors (no certificate to check), while AP, BR, TW and S are unconditional cooperators. Under S-nonself the D
step runs at every encounter and the C step at every encounter with another spelling. With 2r = 200 production
encounters per program per generation (§1.3) and a partner of one's own spelling with probability ≈ that spelling's
frequency (≤ 10⁻³ for all but the constants), every capable producer is certified within its first generation: the
E phase lasts a fraction of a generation and costs PBn/CBo nothing (they defect while uncertified). So the Pangaea is
the H game above to within the first generation, and the free-certificate Pangaea (H from t = 0) is its control.

**Four consequences on a Pangaea** (well-mixed, x_N = the dominant establisher network's share, x_S suckers):

1. *Prudence is never worse than defection.* f_PB − f_D ≈ x_PBnet ≥ 0: PB-shaped exploiters take the suckers like D
   and cooperate only with their own network. A scramble failure needs the whole prudent mass to die by drift, and it
   is ≈ 0.0024·N·I ≈ 30 founders at 12,800 (R, the 33 PrudentBot-family spellings) plus ≈ 160 PB-mutual establishers.
   **All-defect is not a Pangaea outcome.**
2. *The sucker phase taxes accommodators.* Suckers die logistically at rate ≈ w per generation (∫x_S dt ≈ 2.3
   generations from x_S ≈ 0.49); accommodating establishers (CB, most of PBn, BR, APn) pay ≈ w·(give − 2·received) on
   the sucker mass, i.e. they lose roughly a factor 0.5 against D and against exploiting establishers through the
   phase. The network that comes out is richer in exploiters (PB-family) than its prior mass.
3. *The rival network is parasitised.* APn cooperates with the illegible defectors Dill at 0.94, and Dill is 0.073 of
   the prior, more than APn (0.032) and BR together. So f_APn − f_Dill ≈ x_APn − x_Dill − x_S < 0 until APn outweighs
   its parasites, while the CB/PB network (S-guarded: it cooperates only with certified cooperators) gives Dill 0.03–
   0.04. Soundness is what decides the rival race: **the CB/PB network wins the Pangaea, although APn's prior mass
   (0.046 with bridges) exceeds CB's (0.028 with bridges).** This is milestone 2's "defection detectors are
   exploitable", now at the population scale.
4. *The clique is a defector with a bonus proportional to its own quote.* A TwinD identity unit defects against
   every other quote, so f_TW − f_D = (own-quote frequency)·1 ≤ 2.6·10⁻⁴ per spelling at the seed, against
   f_net − f_D ≈ x_net for the network. On a Pangaea a TwinD lineage is a neutral defector until the network grows and
   then declines with D. Its only route to ≥ 0.05 is drift, and a critical lineage from one copy reaches k copies with
   probability ≈ 1/k: with 9.1 seeded copies the chance that any lineage reaches 640 copies (0.05 of 12,800) before the
   network takes over is ≈ 9/640 ≈ 0.014, and even then the coordination barrier (one TwinD quote at x against the
   network at 1 − x) removes it at rate w·(1 − 2x). **On a Pangaea the clique cannot win; it can only linger as a
   defector remnant for the network's takeover time.**

**Takeover time on a Pangaea.** With f_net − f_D ≈ x, dx/dt ≈ w·x²·(1 − x): the network needs ≈ 1/(w·x₀) generations
from x₀ to take over, independent of N. With x₀ ≈ 0.02 after the sucker phase this is ≈ 170 generations, against 30–40
generations to the first established island on islands of 100–200 (provenance, scaling). **The Pangaea establishes
late and deterministically**; establishment time should not depend on N·I.

**Where the clique wins along I.** On an island of N a TwinD copy is at 1/N and the island's establisher network has
≈ 0.03·N members, so the clique needs a drift excursion of order 0.03·N copies before the local network takes over:
per-copy establishment ∝ 1/N (0.08 at N = 100 and 0.04 at N = 200 in the scaling run fit this; 0.04 at N = 400 does
not, so the decline may be slower). With the seeded count fixed at 9.1 per run (N·I = 12,800), expected identity
islands per run ≈ 9.1 × (8/N): 0.37 at N = 200, 0.09 at N = 800, 0.02 at N = 3,200, 0.006 on the Pangaea. Islands of
100 are absorbed by open migrants within ≈ 10⁴ generations (scaling run), so (100, 128) recovers by 10,000 and
(100, 64) earlier; from N = 200 clique islands are permanent. Bridge-less non-identity rivals (5–20% of runs at N ≥ 200
in the scaling run) add a second failure that should shrink with I and vanish on the Pangaea (majority decides in one
population).

### 1.2 Founder partition (amendment 2)

For total T ∈ {12,800, 6,400} and replicate r ∈ 0..19: one list of T founder spellings, iid from L, stream
[T, r, SALT_PG] with SALT_PG = 20261016. One uniformly random permutation of the list (stream [T, r, SALT_PG, 9]) is
cut into consecutive blocks of N for every geometry (N, I) with N·I = T: **the partitions are nested** (an island of
(800, 16) is the union of four islands of (200, 64), etc.), every geometry's partition is uniform, and the multiset of
founders, hence the seeded copies of every family and every spelling, is identical across the continuum by
construction. The founder list is recorded per replicate (spelling multiplicities, Q and R copies, individual Q
spellings). The proportional control replaces each Q entry of the list by a draw from the non-Q spellings ∝ μ (stream
[T, r, SALT_PG, 6], in list order) before partitioning, so it is paired with S-nonself at every geometry. The 6,400 and
12,800 lists are independent.

Seeded copies, by hand (μ(Q) = 7.13·10⁻⁴): 9.13 per run at 12,800 (P(none) = 1.1·10⁻⁴), 4.56 at 6,400 (P(none) =
0.010); per island λ = N·μ(Q) = 0.071 / 0.143 / 0.57 / 2.28 / 9.13 along (100, 128) / (200, 64) / (800, 16) /
(3,200, 4) / (12,800, 1), and 0.071 / 0.285 / 1.14 / 4.56 along (100, 64) / (400, 16) / (1,600, 4) / (6,400, 1).

**Other founders.** *C-donor*: every founder a copier (rule C, empty lists) except k donors (rule H, an establisher
spelling with a C script, drawn ∝ μ on the donor-eligible spellings) written over uniformly chosen positions of the
list (stream [T, r, SALT_PG, 3]); k = 1 (the main C-donor cell) and k = round(0.001·T) = 13 / 6 (the dilution control).
On a Pangaea one donor is a fraction 7.8·10⁻⁵ of the population (on islands of 100 it was 0.01). *Free certificates*
(H): every founder of the S-nonself list as its H unit, rule H (provenance's H-only). *Fission–fusion*: (100, 128)
S-nonself from the 12,800 list, calibrated mN = 1, merged into one population of 12,800 at generation 200 (variant:
1,000); the merged state keeps every individual's type and per-individual logs; the event index continues and the
kernel seed changes at the merge.

Kernel streams: every (geometry, replicate) has one kernel seed shared by every rule and production arm at that
geometry, so S-nonself, the proportional control and the native-r arm are paired draw for draw until their states
differ.

### 1.3 The production schedule (amendment 1)

The kernel runs r production encounters per Moran event, each on a uniformly drawn island between two uniformly drawn
residents, so every program has 2r production encounters per generation whatever (N, I); r does not enter fitness
(payoffs are mean payoffs against the island). The scaling run used r = N/2, so production per program grew with N.
**Primary schedule: r = 100 everywhere** (2r = 200 per program per generation, the (200, 64) baseline's value); the
stored (100, 64) and (100, 128) cells ran at r = 50 and are rerun here at r = 100. **Native arm: r = N/2** at
(100, 128) (r = 50), (100, 64) (50), (400, 16) (200) and (800, 16) (400); at (200, 64) the two arms coincide. Reported
for both: production attempts and successes per program (C and D), certified share of capable producers through the
scramble, and coverage (certified share) at establishment.

*Kernel detail (found reading the code, before any cell).* Provenance's counter RNG hashes (event, draw) as
event·512 + draw, and encounter q uses draws 8 + 5q … 12 + 5q. For r ≤ 100 every draw is distinct. For r > 100
(N = 400 in the scaling run, r = 200) encounter q ≥ 101 reuses draws of the next event: encounter 101's island draw is
the next event's migration coin and its focal/partner draws are the next event's source-island and birth uniforms, and
every later encounter's partner draw is the island draw of an encounter at the next event. The stored N = 400 cells
therefore carry a weak correlation between production encounters and the next Moran event (no effect on any reported
outcome is expected; it is a stream overlap, not a bias in any marginal). The kernel here (`src/pangaea_kern.py`, a
copy of provenance's segment) draws encounters q ≥ 100 from a separate seed per block of 100, so it is identical to
provenance for r ≤ 100 and overlap-free above.

### 1.4 Cells, horizons, drop order

Twenty replicates per cell (0–19), every run to 2,000 generations; extensions to 10,000 as below. All S-type cells
use rule S-nonself.

| block | cells | r | horizon |
|---|---|---|---|
| A (continuum, main) | 12,800: (100, 128), (200, 64), (800, 16), (3,200, 4), (12,800, 1); 6,400: (100, 64), (400, 16), (1,600, 4), (6,400, 1) | 100 | 10,000 for every run not frozen |
| B (proportional control) | the five 12,800 cells and (6,400, 1); 6,400 intermediates last in line | 100 | Pangaea 10,000; islands 10,000 if not universal at 2,000 |
| C (native r) | (100, 128), (800, 16), (100, 64), (400, 16) | N/2 | as A |
| D (C-donor) | (12,800, 1) and (6,400, 1), one donor; dilution 13 / 6 donors | 100 | 2,000 (10,000 if unresolved) |
| E (free certificates) | (12,800, 1), H | — | 2,000 |
| F (fission–fusion) | (100, 128) → (12,800, 1) at 200; variant at 1,000 | 100 | 10,000 |

Drop order (spec), applied only if the projected total exceeds ≈ 20 hours on 3 workers and disclosed in §2 before the
cells it affects: the N·I = 6,400 intermediates (A and C at (400, 16), (1,600, 4), B's 6,400 intermediates), then the
C-donor dilution, then the 10,000 extension outside the Pangaea cells.

### 1.5 Endpoints and statistics

At every checkpoint (every 10 generations to 500, then every 50; full snapshots at 200, 500, 1,000, 2,000, 5,000,
10,000) on the whole metapopulation:

- **P(C,C)**: mean over islands of the island P(C,C) (ordered pairs of distinct residents); on a Pangaea, the
  population's.
- **Network decomposition.** Living types with self-play cooperation are the cooperators. The **dominant compatible
  network** M: the cooperator h* with the largest compatible mass (the summed counts of cooperators mutually
  cooperating with it), then a greedy clique: cooperators mutual with h*, added in decreasing count if mutual with
  every member already in. Shares (of the whole population): M; cooperators outside M; **open** (M's h* mutual with
  CB-H); **target network** (cooperators mutual with PB-H, i.e. PrudentBot's network; PB's own quote included);
  **identity** (types on an identity unit) and the Q-spelling share (seeded TwinD family, certified or not);
  **AP network** (cooperators mutual with AP-H and not with CB-H); **neutral remnants** reported separately: suckers
  (cooperate with D-H), uncertified cooperators (no C entry); certified carriers (C entry) and M's share of them.
- **Pangaea endpoints** (amendment 5): (a) P(C,C) ≥ 0.95; (b) M holds ≥ 0.99 of certified carriers; (c) M's raw
  population share, with remnants beside it. **Universal (Pangaea)** = M pairwise compatible and holding ≥ 0.95 of the
  population; **universal-open** adds that M is open (spec: "one compatible network holding ≥ 0.95").
- **Islands (I > 1)**: the scaling run's classifier (universal-open, failure causes identity / rival / inefficient)
  and static absorbing check, unchanged. The global decomposition above is computed for islands too, as a robustness
  column (the island criterion and the Pangaea criterion are not the same statistic; both are reported).
- **Horizon-free events** (amendment 5): *establishment* = first checkpoint with P(C,C) ≥ 0.9 on some island (on a
  Pangaea, the population); *resolved* (Pangaea) = every living cooperator in M, M pairwise compatible, and the S-nonself
  closure of the living units against the living units containing no cooperating unit outside M's mutual set (at
  ε = 0 nothing else can arise); *lost* = no living cooperator and none reachable (all-defect, absorbing); otherwise
  *unresolved*, reported apart from losses. First resolution and loss times are recorded.
- **Early extinctions** (amendment 5): per spelling of R (prudent core), of Q (each individual clique identity) and of
  the bridge class BR, the generation at which its global count first reaches 0 and its maximum count; the Pangaea
  trajectory of P(C,C) and of every family's share every 10 generations to 500.
- **Seeded copies**: Q and R copies per run (identical across the continuum), Q copies per island.
- **Production** (C and D attempts and successes per program, certified share of capable producers) for the native
  comparison.
- **Uncertainty** (amendment 6): exact (Clopper–Pearson) binomial intervals; pass / fail / inconclusive regions for
  each threshold are declared in the predictions file.

### 1.6 Hand predictions (they become numbered predictions with falsifiers)

- *Pangaea, S-nonself, r = 100.* The CB/PB network wins every run at both totals: P(C,C) ≥ 0.95, M ≥ 0.99 of
  certified carriers and ≥ 0.95 of the population, open, at 2,000 in 20/20. The target share ≥ 0.9 in ≥ 18/20 (PB
  exploiters remove the suckers and illegible accommodators that FairBot would carry); Gemini's 0.75–0.90 band in at
  most 2 runs. Identity share at 2,000 = 0 in ≥ 19/20, maximum TwinD-lineage share over the run ≤ 0.02 in every run.
  No scramble failure. Establishment late: median 150–300 generations at both totals (against 30–40 on islands). The
  AP network peaks below 0.1 and never holds a majority.
- *Continuum at 2,000 (universal-open, S-nonself):* (100, 128) ≈ 0.35, (200, 64) ≈ 0.55, (800, 16) ≈ 0.8,
  (3,200, 4) ≈ 0.9, (12,800, 1) = 1; along 6,400: (100, 64) ≈ 0.7, (400, 16) ≈ 0.8, (1,600, 4) ≈ 0.9, (6,400, 1) = 1.
  Monotone at 2,000. At 10,000, (100, 128) and (100, 64) gain (absorption at N = 100) and (100, 128) may pass
  (200, 64): non-monotone at 10,000. Identity islands per run fall roughly as 1/N.
- *Proportional control:* universal on every Pangaea run; its gain over S-nonself shrinks to 0 along I → 1.
- *Native r vs r = 100:* no outcome difference beyond ±3 runs per cell; production per program doubles or halves with r
  but coverage at establishment is ≥ 0.95 in both arms.
- *C-donor on the Pangaea:* the single donor dies within about a generation but makes tens of copies first; universal
  ≥ 18/20; failures, if any, are donor lineages that left no copy (all-defect). Dilution (13 / 6 donors) ≥ 19/20.
- *Free certificates (H):* 20/20 universal-open; establishment earlier than S-nonself's.
- *Fission–fusion:* at 200 generations most islands are held, ≈ 5–15% by TwinD identities; merged, every clique and
  rival is a minority network on a Pangaea and dies within ≈ 100 generations: 20/20 universal-open in both variants.
- *Deterministic family dynamics (H, certificates saturated):* the CB/PB network takes over by ≈ 200 generations; APn
  peaks and is then eaten by Dill and outcompeted; TW decays with D.

### 1.7 Validation plan (code, before any counted cell)

1. **Draw for draw.** With r = N/2 and the scaling run's founders, the new runner reproduces stored scaling rows exactly
   (trace points, snapshots, establishment): S-nonself (200, 64) calibrated and (100, 64), and the proportional control
   at (200, 64), replicates 0–2.
2. **Kernel**: for r ≤ 100 the new segment equals provenance's (the same rows); for r > 100 encounter draws are
   distinct from every Moran draw (checked by enumerating the draw keys of one event).
3. **Founders**: the multiset of founders is identical across the geometries of a total (exact), the partition is
   nested, Q copies per run equal the list's, the proportional control changes exactly the Q entries, the C-donor
   counts are 1 / 13 / 6.
4. **Network decomposition** on constructed populations (all CB; CB + TwinD; CB + AP; all D; CB + suckers) gives the
   hand labels, and on islands the classifier's universal-open equals the stored flag.
5. **Fission–fusion merge**: counts, payoff sums and settled counts after the merge equal a fresh initialization from
   the merged slots.
6. **Deterministic family dynamics** written before the cells and reported in §1.8.

### 1.8 Code validation and the deterministic control (appended after the code, before any counted cell)

Code: `src/pangaea_kern.py` (provenance's segment with overlap-free encounter draws above r = 100; the mutual matrix and
the dominant-network greedy clique), `src/pangaea.py` (founders, cells, `PGRun`, the merge, the decomposition, the
closure status, the deterministic dynamics), `src/pangaea_run.py`, `src/pangaea_report.py`; `tests/test_pangaea.py`
(6 tests, passing; 4 need the cached tables and skip without them).

- **Draw for draw** (`runs/pangaea-validate.json`): the scaling run's own lottery job with the kernel swapped for the
  new one (legacy conventions: r = N/2, provenance's seed) reproduces 12 stored scaling rows (S-nonself (200, 64)
  calibrated, S-nonself (100, 64), proportional (200, 64), S-nonself (50, 64) mN = 1; replicates 0–2) with **0
  differences over 456 trace points**, the 2,000 snapshot and establishment. A pytest compares the new kernel with
  provenance's segment state for state at r = 100 and reproduces a stored row.
- **Draws** (`runs/pangaea-kernelcheck.json`): the 1,500 encounter draws of q = 100–399 at one event collide with none
  of the 1,024 base-seed draws of that event and the next; under provenance's indexing 297 of the 300 draws of
  encounters 100–199 equal draws of the next event (the stored N = 400 overlap, §1.3, confirmed).
- **Founders:** for two replicates per total, every geometry's founder multiset has the same hash (identical), the
  partitions are nested, the proportional control changes exactly the Q entries and leaves no Q spelling; C-donor
  cells have 1 / 13 / 6 donors.
- **Merge:** counts and payoff sums after merging (100, 128) at generation 30 equal a fresh initialization from the
  merged slots; the merged run advances.
- **Deterministic family dynamics** (H units, certificates saturated, infinite well-mixed population, Moran mean field;
  4,162 unit types plus identity spellings; `runs/pangaea-determ.json`):

| g | P(C,C) | target | open | AP net | identity | D | Dill | S | PBn | CBo | BR | APn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.240 | 0.040 | 0.383 | 0.102 | 0.0007 | 0.379 | 0.072 | 0.429 | 0.013 | 0.001 | 0.014 | 0.032 |
| 10 | 0.016 | 0.026 | 0.081 | 0.029 | 0.0014 | 0.746 | 0.117 | 0.069 | 0.015 | 0.002 | 0.006 | 0.019 |
| 50 | 0.003 | 0.027 | 0.031 | 0.002 | 0.0016 | 0.825 | 0.139 | 0 | 0.027 | 0.004 | 0 | 0.002 |
| 100 | 0.033 | 0.116 | 0.132 | 0 | 0.0014 | 0.741 | 0.126 | 0 | 0.116 | 0.015 | 0 | 0 |
| 150 | 0.981 | 0.885 | 0.935 | 0 | 0 | 0.064 | 0.001 | 0 | 0.885 | 0.050 | 0 | 0 |
| 200 | 0.996 | 0.948 | 0.976 | 0 | 0 | 0.024 | 0 | 0 | 0.948 | 0.028 | 0 | 0 |
| 2,000 | 1.000 | 0.996 | 0.998 | 0 | 0 | 0.002 | 0 | 0 | 0.996 | 0.002 | 0 | 0 |

  The suckers are gone by generation 20, the AP network by 50 (it is eaten with the suckers and by Dill, which grows
  from 0.072 to 0.139), bridges vanish with the accommodators, and the PrudentBot network (PBn) takes over between
  generations 100 and 150 (P(C,C) 0.83 at 130, 0.96 at 140). The TwinD identity share doubles while suckers last
  (0.0007 → 0.0016, it exploits them like D) and is gone by 150. The proportional prior gives the same trajectory to
  three decimals. The leading types at 2,000 are FairBot and FairBot-with-guards (all open and target). **S14 is
  scored on this: the control ends on the open target network; the hand estimate of the takeover (≈ 170) was a little
  slow (≈ 140).**

## 2. Costs

**Probes** (replicate 990, discarded; `runs/pangaea/smoke*.log`, plus three 200–260-generation end-to-end jobs):
S-nonself Pangaea 12,800 to 600 generations 27 s, settling to 0.01 s per generation (6 types alive by 600: selection
removes the seed's variety within a few hundred generations, so the Moran step is cheap); (800, 16) native r = 400 to
300 generations 30 s; (3,200, 4) 11 s; **C-donor Pangaea 12,800: 1.15 s per generation in steady state** (copiers that
cannot use any living donor script are never settled and retry their copy step at every one of the 1.28·10⁶
encounters per generation), 486 s for 400 generations. *Disclosure:* the (800, 16) end-to-end probe (replicate 990,
discarded, after the predictions were committed) ended all-defect at generation 110; it is not a counted run.

**Projection** (worker-hours): S-nonself and proportional continua with 10,000-generation extensions ≈ 8; native r
≈ 2; free certificates and fission–fusion ≈ 2; **C-donor one donor at 2,000 ≈ 20** (12,800: 20 × 40 min; 6,400:
20 × 20 min); C-donor dilution ≈ 20. Total ≈ 52 worker-hours ≈ 17 hours on 3 workers, under the 20-hour line, so no
drop is applied up front. **Deviation (disclosed before any cell):** the C-donor cells (one donor and dilution) are
scored at 2,000 and not extended (the spec's "10,000 if unresolved" would cost ≈ 3 hours per run); this follows the
scaling run's treatment of copying rules. Batches run in the order S cells (A, B, C, E, F) → C-donor one donor →
dilution; if the measured total overruns, the dilution control is the next cut (spec drop order), then the
10,000-generation extensions outside the Pangaea cells.
