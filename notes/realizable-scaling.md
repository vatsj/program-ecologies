# The realizable lottery along paths in (N, I, mN) (notes, 2026-10-14)

Spec `specs/2026-10-14-realizable-scaling.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict). §1 is written by hand before any code of this run and before
any counted cell. §1.9 (code validation, the T_nuc calibration) and §2 (projected and measured costs) are appended
after the code and before any counted cell.

Base, imported unchanged: provenance (`notes/provenance.md` §1 with §1.12; `src/provenance*.py`) on milestone 5's
language, grammar (P at n = 7, 12,546 spellings, prior L), lack rule, would-be-self adoption check, kernel and
holder-based endpoints. *Stated:* the spec's "`eq` admitted (DEFERRED 1)" is nominal on this machinery: grammar P has
no `eq` atom, and its identity channel is the checker's R = S coincidence (the TwinD family's self-reading), exactly as
in provenance; no identity device is removed or added. ε = 0, iid seeds from L, w = 0.3, r = N/2 encounters per Moran
event, time in generations of N events per island (I·N events per generation). Every number here is an ε = 0 lottery
statistic at finite (N, I, horizon), never π.

*Disclosure (before any code).* The cached static tables the provenance run used (`runs/lt_genes/static/`,
`runs/provenance/{static/, OSV.npy, SPO.npy, sets.npz, prod_exec.json}`) are untracked and were not present in the
main checkout or any worktree. They are rebuilt in this worktree by the stored commands (`lt_genes_run.py static`,
`provenance_run.py static | osv | sets`), with no code change; the rebuild is validated by the tracked summaries
(`runs/provenance/{static_ext, osv, sets}.json`, compared and then restored) and by the draw-for-draw reproduction of
stored lottery runs (§1.8). The rebuild was started while this section was being written; no lottery run of any kind
had been made.

## 1. Design

### 1.0 The object in one paragraph

Two things can stop a realizable seed lottery from being universal as it grows: **identity abundance** (the TwinD
family, the seed's own self-reading cliques under S-nonself, is seeded μ(Q)·N·I times per run, μ(Q) = 7.13·10⁻⁴, and
each seeded copy that establishes is a bridge-less rival: it defects against every other quote) and **rival
patchworks** among non-identity carriers (frozen at N ≥ 200 under mN = 1). The run separates them by rule (S-nonself;
the mass-matched ablation, a *joint* intervention that removes Q and strengthens the prudent core; a
proportional-replacement control that only removes Q; C-donor, whose copiers cannot write TwinD's script), by path
(P1 size, P2 islands, P3 diagonal), by migration (mN = 1 and the calibrated mN), and by a crossed panel that fixes the
seeded copy count across geometries. Island-level efficiency is the claim DEFERRED 1 defends; universality is the
measured quantity.

### 1.1 Seeded copies and the per-island copy law

The seed is iid from L, so the number of TwinD-family copies on an island is Binomial(N, μ(Q)) ≈ Poisson(λ),
λ = N·μ(Q), independent across islands; the run total is Poisson(N·I·μ(Q)). Per cell (by hand, μ(Q) = 7.13·10⁻⁴):

| (N, I) | path | copies per run N·I·μ | λ per island | occupied islands I(1 − e^−λ) | islands with ≥ 2 copies I·P(≥2) | copies per occupied island | P(no copy in the run) |
|---|---|---|---|---|---|---|---|
| (50, 32) | P3 | 1.14 | 0.036 | 1.12 | 0.020 | 1.02 | 0.32 |
| (50, 64) | P1 | 2.28 | 0.036 | 2.24 | 0.040 | 1.02 | 0.10 |
| (100, 32) | P2 | 2.28 | 0.071 | 2.20 | 0.078 | 1.04 | 0.10 |
| (100, 64) | P1, P2, P3 | 4.56 | 0.071 | 4.40 | 0.155 | 1.04 | 0.010 |
| (200, 64) | P1 | 9.13 | 0.143 | 8.51 | 0.59 | 1.07 | 1.1·10⁻⁴ |
| (100, 128) | P2 | 9.13 | 0.071 | 8.81 | 0.31 | 1.04 | 1.1·10⁻⁴ |
| (400, 64) | P1 | 18.25 | 0.285 | 15.9 | 2.16 | 1.15 | ≈ 0 |
| (200, 128) | P3 | 18.25 | 0.143 | 17.0 | 1.18 | 1.07 | ≈ 0 |
| (100, 256) | P2 | 18.25 | 0.071 | 17.6 | 0.62 | 1.04 | ≈ 0 |

At matched totals (18.25) the three paths differ only in clustering: multi-copy islands are 2.16 (P1) > 1.18 (P3) >
0.62 (P2) per run, and the copy's island frequency at founding is 1/N (a quarter at N = 400 of what it is at N = 100).
So the matched-total comparison (400, 64) / (200, 128) / (100, 256) is the test of Gemini's counter-prediction (per-
island clustering, not total copies) and of sol's (no collapse on raw copies).

**What the stored provenance runs already say** (read before writing this section; mN = 1, S-nonself, universal-open
at 10,000 by seeded TwinD count): at (100, 64) the per-run count ranges 0–9 and 31/40 are universal with no visible
trend inside that range; at (200, 64) runs with ≤ 8 copies are 6/6 universal and runs with ≥ 9 are 5/14; at
(100, 128) 11/20 universal (2–16 copies). The ablation is 40/40, 18/20, 16/20 and C-donor 37/40, 20/20, 19/19. Under
C-donor no run at N = 200 or I = 128 has an identity island although the seed carries the same TwinD copies: TwinD
founders are copiers (mode C) there, and TwinD's C script τ₁ is a production (it is written by the tactic for TwinD's
own run tree); no donor carries it, so a TwinD copier never becomes the identity unit. **C-donor removes the identity
mechanism by construction, not by out-competing it** (checked in §1.9 against the unit tables).

A one-parameter reading of the stored numbers: if each seeded copy independently leaves a permanent rival with
probability q_c and clique-free runs are universal with probability f₀, f ≈ f₀·e^(−q_c·c). With f₀ from the ablation
(1.0 / 0.9 / 0.8) and f from S-nonself (0.78 / 0.55 / 0.55): q_c ≈ 0.055 / 0.054 / 0.041 per copy at (100, 64) /
(200, 64) / (100, 128). So under mN = 1 the per-copy effect is roughly geometry-independent, and the 50% crossing at
f₀ ≈ 0.9 is at c ≈ ln(1.8)/0.05 ≈ 12 copies (not the identity grammar's 8, which belongs to a grammar with `eq` and a
different baseline).

### 1.2 The calibrated migration rate and the T_nuc rule

**Calibrated mN** (spec): mN(N) = (N/100)^0.7, i.e. 0.616 / 1 / 1.625 / 2.639 at N = 50 / 100 / 200 / 400, so the
per-event migration probability m = mN/N is 0.0123 / 0.01 / 0.0081 / 0.0066. The kernel's migration coin is drawn at a
fixed event-indexed position (draw 1 of event e), so two migration arms with the same founders consume identical
numbers and diverge only where a migration event happens in one and not the other (pairing across mN arms).

**T_nuc rule (predefined; amendment 7).** At m = 0 (no migration), iid L seeds, I = 64, 20 independent replicates per
N ∈ {50, 100, 200, 400} (replicates 500–519, disjoint from every counted cell), checkpoints every 5 generations to a
horizon of 400 generations, one cell per rule (S-nonself, ablation, C-donor): an island's **nucleation time** is the
first checkpoint at which its P(C,C) ≥ 0.9 (the provenance establishment criterion applied per island). **T_nuc(N)** =
the median of the nucleation time over the islands that nucleate (pooled across the 20 runs), with a run-bootstrap
95% interval. The amendment's phrase "time to the first island-level establishment" is read **per island**, which is
how the island-path run defined T_nuc and the x ≲ 0.3 rule was derived for; the run-level time (the first island of a
run to establish, the provenance `establish_gen`) and the per-island nucleation probability p(N) are reported beside
it. **Check:** x = mN·T_nuc/N per rule and N, at both mN arms. *Decision rule (declared now):* the calibrated arm keeps
the spec's formula unless the S-nonself x exceeds 0.6 (twice the boundary) at some N, in which case that N's calibrated
mN becomes 0.3·N/T_nuc(N), disclosed before any cell.

*Hand expectation.* The provenance runs establish their first island at a median of 30 generations at N = 100 and 40
at N = 200 (run level, mN = 1). Per island the time is longer; the island-path modal arm had 45 / 55 / 70 at
N = 100 / 200 / 400 (∝ N^0.32). I expect per-island T_nuc ≈ 30–60 at N = 100 growing like N^0.2–0.4, so x ≈ 0.3–0.6 at
N = 100 under mN = 1 (the reference geometry sits at or a little above the boundary) and nearly constant along the
calibrated path (x ∝ N^(0.7 + 0.3 − 1) = N^0); under mN = 1, x falls like N^(−0.7) from N = 50 to 400.

### 1.3 Rules and founders

All founders of the producing rules start with empty lists (provenance). Founder draws are paired: replicate r at
(N, I) has founder spellings from the stream [N, I, r, 20261012] in every rule and mN arm (provenance's `founders`),
and the kernel stream `kernel_seed(N, I, r)` is shared, so every rule × mN arm at one (N, I) is paired draw for draw
until states differ.

- **S-nonself** (prior L): provenance's operating rule.
- **Ablation** (mass-matched; S-nonself): provenance's `founders(..., 'ablation')`: a founder in Q is replaced by a
  draw from R ∝ μ (R = 11 prudent open run trees, 33 spellings, μ(R) = 0.0024; stream [N, I, r, SALT, 4]). It
  removes the cliques *and* raises the prudent core's mass by 1.30×: a **joint intervention** (amendment 3).
- **Proportional control** (S-nonself, new): a founder in Q is replaced by a draw from the non-Q spellings ∝ μ
  (stream [N, I, r, SALT, 6]). This removes only the cliques: the removed mass is spread over every non-identity type
  in proportion to its prior mass. Ablation − proportional isolates the prudent-core boost; proportional − S-nonself
  isolates clique removal.
- **C-donor** (provenance's): every founder mode C with an empty list except one H donor per island (an establisher
  spelling with a C script, drawn from L restricted to such spellings; stream [N, I, r, SALT, 3]).
- **C-donor dense** (amendment 6, new): ⌈N/100⌉ donors per island at distinct uniformly drawn positions (stream
  [N, I, r, SALT, 5]); run on P1 at N = 200 and 400 (2 and 4 donors), both mN arms. At N ≤ 100 it is C-donor.
  *Dilution:* one donor is a fraction 1/N of its island, i.e. 0.02 / 0.01 / 0.005 / 0.0025 along P1; dense keeps it at
  0.01.
- **Crossed panel** (amendment 2, S-nonself, calibrated mN): the TwinD-family count is held at c ∈ {0, 4, 8, 16} per
  run. Construction, paired with S-nonself: start from the replicate's L founders; replace every Q founder by a draw
  from the non-Q spellings ∝ μ (the proportional control's stream, so **c = 0 is the proportional control**, run once
  and shared); then choose c slots uniformly without replacement among the N·I slots (stream [N, I, r, SALT, 7]; this
  is the prior's per-island law conditioned on the total: iid placement given the count) and write a Q spelling ∝ μ|Q
  into each (stream [N, I, r, SALT, 8]), displacing the founder there. The displaced founders are thus redrawn from the
  non-identity prior and the population is preserved. Geometries (100, 64), (200, 64), (100, 128), (200, 128).

### 1.4 Cells, horizons and the extension rule

**Paths:** P1 (N, 64), N ∈ {50, 100, 200, 400}; P2 (100, I), I ∈ {32, 64, 128, 256}; P3 (50, 32), (100, 64),
(200, 128). Nine geometries; at N = 100 the two mN arms coincide and are run once (four geometries), the other five
geometries are run at both arms: 14 geometry × mN combinations. Runs: 20 per cell, 40 at (100, 64) (replicates 0–39;
0–19 elsewhere).

| block | rules | combinations | cells |
|---|---|---|---|
| A (main paths) | S-nonself, ablation, C-donor | all 14 | 42 |
| B (proportional control) | proportional | the 9 geometries at calibrated mN | 9 (4 shared with the panel's c = 0) |
| C (crossed panel) | S-nonself, c ∈ {4, 8, 16} (c = 0 = B) | 4 geometries, calibrated | 12 |
| D (donor density) | C-donor dense | (200, 64), (400, 64), both arms | 4 |

**Horizons.** Every run to 2,000 generations. **Main cells** (fixed now, amendment 5): S-nonself at calibrated mN on
(100, 64), (200, 64), (400, 64), (100, 128), (200, 128), (100, 256), and the twelve crossed-panel cells plus their
shared c = 0 cells: **every run** is extended to T_ext = 10,000·(I·N^0.3)/(64·100^0.3) generations, capped at 40,000:
10,000 / 12,311 / 15,157 / 20,000 / 24,623 / 40,000 for the six S-nonself cells. Everything else: runs not
universal-open at 2,000 (or with E3 undecided) are extended to 10,000 (provenance's rule), first in the drop order. A
run whose metapopulation holds a single global type whose own encounters change nothing is stopped there (exact at
ε = 0; provenance's `frozen`). Snapshots at 500, 1,000, 2,000, 5,000, 10,000 and T_ext.

**Drop order** (spec; applied only if the projected total exceeds about 24 hours on 3 workers, disclosed in §2): the
10,000 extensions outside the main cells, then N = 400, then I = 256, then C-donor off P3.

### 1.5 Statistics and estimands

Per run, at each snapshot, island by island: P(C,C) over ordered pairs, the majority quote (holder), held (holder
self-cooperates and P(C,C) ≥ 0.5), efficient (P(C,C) ≥ 0.95), holder open (mutual with CB-H), holder an identity unit,
holder's spelling in Q (seeded) or not (minted).

- **Island efficiency** (amendment 1): mean efficient-island fraction ē; the failure probability of a randomly
  sampled island q = 1 − ē (run-bootstrap interval); all-island success = P(every island efficient) per run (Wilson).
  Island-level efficiency is reported separately from universality throughout.
- **Universality:** universal-open (provenance: every island held, every pair of holders mutually cooperating, every
  holder open), at 2,000, 10,000 and T_ext.
- **Failure decomposition** (the classifier, §1.6) per non-universal run: identity / non-identity rival (bridged or
  bridge-less) / inefficient.
- **Clustering** (amendment 4): seeded copies per island at t = 0, islands with ≥ 2 copies, occupied islands, copies
  per occupied island; *clique establishment per seeded copy* (islands ever held by an identity holder, logged every 50
  generations, per seeded copy); identity islands at the horizon by multiplicity of the island's seed (0, 1, ≥ 2
  copies); minted vs seeded identity lineages; a run-level logistic comparison of "any identity island at the horizon"
  on total copies vs on multi-copy islands.
- **Copies vs universality across cells:** the crossed panel gives f(c) per geometry; the one-parameter law
  f = f₀·e^(−q_c·c) is fitted per geometry with f₀ the panel's c = 0 value; the 50% crossing c* by linear
  interpolation in c between panel points (reported as "none" where f₀ < 0.5, amendment 2); the natural cells give
  universality against their realized counts (per-run counts, pooled across cells by geometry).
- **Patchwork resolution:** universal-open at 2,000 vs the longer horizons (resolved fraction among runs not universal
  at 2,000), the first generation at which a run becomes universal-open (time to resolution, from the 50-generation
  trace), and the bridges' survival (§1.6).
- **Costs:** wall seconds per run and per cell, modelled production steps per match (provenance's counters).

### 1.6 The failure classifier and the static absorbing check

At a snapshot, let H be the held islands' holders (one representative type per island: the majority quote). The
**plurality open holder** h* is the open holder holding the most islands; the **main network** M is the set of open
holders mutual with h* (unit-level mutual cooperation, with the twin/self distinction of `cc_pair`). An island
**fails** if it is not held, or its holder is not in M. A run is universal-open iff no island fails and M is
pairwise mutual (equal to provenance's definition; asserted in the tests). Run-level cause, hierarchical:
**identity** (some failing island is held by an identity unit), else **non-identity rival** (some failing island is
held by a non-identity holder outside M), else **inefficient** (only unheld failing islands, or no open holder at
all). Every failing island gets its own label too.

**Static absorbing check** (amendment 5), on the final support. A target-compatible type Z is one that self-
cooperates, is open, and is mutual with every holder in M. For a failing island i with majority type X_i:
- a **bridge** for i is a target-compatible Z that is mutual with X_i (so Z is exactly neutral in an X_i island);
- the island's **resolution hazard** h_i = mN·Σ_Z s_Z·ρ_N(Z → X_i) over the *living* target-compatible types Z, where
  s_Z is Z's share of the individuals on the other islands and ρ_N(Z → X) is the exact fixation probability of one Z
  in N − 1 X under the kernel's Moran step (birth ∝ e^(w·f) with f the average payoff against the N − 1 others, death
  uniform, w = 0.3; ρ = 1/N for a bridge). This treats the island as monomorphic X_i and ignores fitness weighting of
  migrants (stated approximations);
- **prior-reachable** bridges: units reachable at ε = 0 from the living units through S-nonself's own transitions
  against living partners (provenance's `nonself_closure` with the living units as both seeds and partners). At ε = 0
  nothing enters from the prior, so "prior-reachable" is read as reachable by gene acquisition from what is alive; a
  bridge present in the prior but extinct in the run is reported separately ("dead prior bridge") and does not make a
  run unresolved.

A non-universal run is **absorbing** if some failing island has no living or reachable bridge and expected resolution
time 1/h_i > 10⁶ generations (25× the longest horizon); otherwise **unresolved** (right-censored), labelled *bridged*
(every failing island has a living bridge), *reachable-bridge* (some only through gene acquisition), or
*coordination* (a bridge-less island whose 1/h_i ≤ 10⁶, which can still resolve by a coordination crossing in time,
as at N = 50 in the prudent-openness panel). By construction an identity holder (TwinD with τ₁) has no bridge
(identity units are mutual with no other reachable unit), so identity islands are absorbing or coordination-limited,
decided by ρ_N.

*Hand values of ρ for a TwinD island invaded by one open carrier* (open vs TwinD: mutual defection, −1, against 0
within each type). With j invaders f_X − f_Z = (N − 2j)/(N − 1), so Σ_k Π_j e^(w(f_X − f_Z)) = Σ_k e^(w(kN − k(k+1))/(N−1)),
a barrier of height ≈ e^(wN/4): ρ_N = 1.1·10⁻³ / 1.9·10⁻⁵ / 7.2·10⁻⁹ / 1.6·10⁻¹⁵ at N = 50 / 100 / 200 / 400 (the
N = 100 value is the island-path run's A ↔ B 1.85·10⁻⁵, the same symmetric coordination game). With s_Z ≈ 1 the
coordination time 1/(mN·ρ) is ≈ 1.4·10³ generations at N = 50 (calibrated), ≈ 5·10⁴ at N = 100, ≈ 10⁸ at N = 200 and
≈ 2·10¹⁴ at N = 400. **So identity failures are coordination-unresolved at N ≤ 100 (they can still be absorbed within
or near the horizons, as the stored (100, 64) identity islands 0.20 → 0.175 by 10,000 show) and absorbing at
N ≥ 200.**

### 1.7 Hand predictions (they become numbered predictions with falsifiers in the predictions file)

- *Island efficiency.* Islands never fail for want of an establisher once one island has established (an S-guarded
  carrier is neutral in a defector island and self-cooperates, so it enters D islands); clique islands are efficient
  internally. Island failures are migrant-load islands on rival borders and whole-run scramble failures (all-defect
  metapopulations; 1/40 in provenance's S-nonself). Migrant load per island scales with m = mN/N, which falls along
  both arms as N grows. Expect ē ≥ 0.97 in every S-nonself cell at N ≥ 100 and q decreasing in N along P1 and P3;
  all-island success ≥ 0.9 except where whole-run scramble failures occur.
- *Universality, S-nonself, calibrated:* with f₀ ≈ 0.9 and q_c ≈ 0.05: about 0.85 / 0.8 / 0.7 / 0.55 / 0.35 at
  1.1 / 2.3 / 4.6 / 9.1 / 18.3 copies, minus whatever the clique-free baseline loses with N and I (the ablation's stored
  0.9 at (200, 64) and 0.8 at (100, 128)). So ≈ 0.25–0.35 at (400, 64) and (200, 128), where identity islands are
  absorbing (§1.6). **At N = 100 the horizon matters:** a TwinD island is absorbed by coordination in ≈ 5·10⁴
  generations, so (100, 256) is ≈ 0.15 at 2,000 and ≈ 0.4–0.5 at its T_ext = 40,000; RE 2's ≤ 0.2 should hold at 2,000
  and 10,000 and is at risk at T_ext at (100, 256), and holds at (200, 128) at every horizon.
- *Calibrated vs mN = 1:* at N = 200 and 400 the calibrated arm migrates more; open networks colonize unestablished
  islands earlier and bridged rivals are absorbed faster, while a TwinD island cannot be absorbed at any mN. Expect a
  small gain (≤ +0.15) for S-nonself and the ablation at N ≥ 200, and a small loss at N = 50 (mN 0.62).
- *C-donor:* no identity islands anywhere (§1.1); universal ≥ 0.85 at every cell, including (100, 256); dense donors
  change little because copying is fast once a donor meets copiers (r = N/2 encounters per event).
- *Proportional control vs ablation:* most of the ablation's gain is clique removal; the 1.3× prudent-core boost adds
  ≤ 0.1.
- *Crossed panel:* f(0) ≥ 0.75 at the four geometries at T_ext; q_c within a factor 2 across geometries; the
  crossing near 10–15 copies where it exists.
- *Clustering:* per-copy establishment is higher on multi-copy islands, but they are a minority of identity islands
  except at (400, 64); total copies predict identity takeover about as well as multi-copy islands.

### 1.8 Validation plan (code, before any counted cell)

1. **Rebuilt tables = stored ones:** `static_ext.json`, `osv.json`, `sets.json` regenerated equal to the tracked
   versions (except wall times), Q = 10 spellings with μ(Q) = 7.13·10⁻⁴, R = 33 spellings.
2. **Draw for draw:** with mN = 1 my runner reproduces stored provenance rows exactly (the 50-generation trace and the
   2,000 / 10,000 snapshots' outcome, held, identity, open and P(C,C)): S-nonself (100, 64) and (200, 64) replicates,
   plus ablation and C-donor where cheap. Every counted cell at mN = 1 that overlaps a stored cell is compared too.
3. **mN:** m = mN/N per event, the realized migration count per island-generation equals mN within sampling error in
   a smoke run; a calibrated and an mN = 1 run with the same founders agree until the first event whose migration coin
   differs.
4. **Founders:** proportional control and panel c = 0 identical; panel counts exactly c; positions uniform (χ² over
   islands on many draws); ablation unchanged from provenance; dense donors ⌈N/100⌉ distinct positions per island.
5. **Classifier** on constructed archipelagos (hand-built count arrays): all-CB (universal), CB + a TwinD island
   (identity, absorbing at N = 100), CB + a non-open non-identity holder with and without a living bridge (bridged /
   bridge-less), CB + an all-D island (inefficient); universal-open by the classifier = provenance's snapshot flag on
   every stored-run reproduction.
6. **ρ_N** against a direct Moran simulation for one pair at N = 20 and against 1/N for a neutral pair.

### 1.9 Code validation and the calibration (appended after the code, before any counted cell)

Code: `src/realizable_scaling.py` (founders, cells, `RSRun` with mN, `rho_fix`, `classify`, `static_check`),
`src/realizable_scaling_run.py` (calibration, validation, lottery job with per-island records, clustering logs and the
static check), `src/realizable_scaling_report.py`; `tests/test_realizable_scaling.py` (7 tests, passing; 3 need the
rebuilt cache and skip without it).

- **Rebuilt tables.** `lt_genes_run.py static` (17,391 units, 29 scripts, 14,160,981 closure checks and 25,522,223 in
  all, identical counts to the stored log; 1,169 s on 3 workers), then provenance's `static` (17,394 units, +3 S-k
  units, 24,489 checks), `osv` (28,283 values, 468 tactic outputs not own-side valid at their own code) and `sets`
  (Q = 10 spellings, μ(Q) = 7.13·10⁻⁴, R = 33 spellings): every tracked summary field equal to the stored one except
  wall times and the OSV sampling check, which the stored file ran with a larger sample (4,014 pairs, 9 mismatches;
  here 404, 1). `runs/realizable_scaling/rebuild_compare.json`. The tracked files were restored.
- **Draw for draw.** 36 stored provenance runs (S-nonself, ablation, C-donor; replicates 0–5 at (100, 64) and at
  (200, 64) with mN = 1) rerun with this run's job: **0 differences** over 2,743 common trace points (P(C,C), islands
  ≥ 0.9, held, identity, open, SPO islands, type counts), the 2,000 and 10,000 snapshots and establishment times; the
  classifier's universal-open equals provenance's at every snapshot (0 mismatches). `runs/realizable-scaling-validate.json`.
  The pytest reproduction of replicate 1 passes as well.
- **Classifier and ρ:** constructed archipelagos (all-CB, CB with a TwinD island, with a non-open rival, with an
  all-D island, a clique-only metapopulation) give the hand labels; ρ = 1/N for a neutral pair, 1.85·10⁻⁵ for the
  TwinD barrier at N = 100, and a direct simulation of the birth–death step at N = 12 agrees within 4σ.
- **Founders:** the proportional control redraws exactly the Q founders and nothing else; the panel's counts are exact
  and its non-Q founders are the proportional control's; placement is uniform over islands (χ² over 300 draws);
  dense donors are ⌈N/100⌉ per island.
- **Correction to §1.1 (found in validation, before any cell).** "C-donor removes the identity mechanism by
  construction" is wrong as worded: one of the six validation C-donor runs at (100, 64) ends with TwinD-family
  identity islands (four islands, holder `if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D)`, a Q spelling, founded as a
  copier); no donor is ever in Q (the donor law gives Q zero mass, since TwinD's H unit is not a donor-eligible
  establisher). So a TwinD copier can reach its identity unit by copying, rarely (provenance's C-donor had 0.004 of
  islands). R4 stands as written and is scored as written.
- **Calibration (§1.2 rule; `runs/realizable_scaling/calib_rows.json`).** Per-island nucleation at m = 0, I = 64, 20
  replicates per N:

| rule | N | nucleating islands (p) | T_nuc [95%] | run-level first | x at mN = 1 | x calibrated |
|---|---|---|---|---|---|---|
| S-nonself | 50 | 133 / 1,280 (0.10) | 25 [20, 25] | 15 | 0.50 | 0.31 |
| S-nonself | 100 | 159 / 1,280 (0.12) | 35 [30, 35] | 20 | 0.35 | 0.35 |
| S-nonself | 200 | 204 / 1,280 (0.16) | 45 [45, 50] | 30 | 0.23 | 0.37 |
| S-nonself | 400 | 244 / 1,280 (0.19) | 55 [55, 60] | 35 | 0.14 | 0.36 |
| ablation | 50–400 | 0.10 / 0.12 / 0.16 / 0.19 | 25 / 35 / 45 / 55 | 15 / 20 / 30 / 35 | as S-nonself | as S-nonself |

  T_nuc ∝ N^0.38 (S-nonself and ablation). **The calibrated arm sits at x = 0.31–0.37 at every N** (flat, as the
  formula intends), slightly above the 0.3 boundary; the decision rule (x > 0.6) is not triggered and the spec's
  formula is kept. Under mN = 1, x falls from 0.50 (N = 50) to 0.14 (N = 400). Per-island nucleation at m = 0 is rare
  (p = 0.10–0.19): most islands are colonized, not nucleated, in every cell of this run. C-donor: see the addendum below.
  *Deviation (C-donor calibration):* at m = 0 an island whose donor lineage dies is never settled (copiers retry at
  every match), so a 400-generation C-donor run at N = 400 cost more than 10 minutes and the first launch was stopped
  with no row saved; the C-donor calibration uses a 150-generation horizon (the S-nonself nucleation times have 95th
  percentiles 45–105 and 0.2% above 200 at N = 400, so the median is unaffected) and 10 replicates at N = 400.
- **C-donor calibration (addendum, written after it finished and before any C-donor cell had reported; the S cells
  had run).** Nucleating islands 114 / 68 / 76 / 41 of 1,280 / 1,280 / 1,280 / 640 (p = 0.09 / 0.05 / 0.06 / 0.06),
  T_nuc = 25 / 30 / 40 / 50 at N = 50 / 100 / 200 / 400 (∝ N^0.34), run-level first 15 / 22.5 / 25 / 37.5; x on the
  calibrated arm 0.31 / 0.30 / 0.32 / 0.33, at mN = 1 0.50 / 0.30 / 0.20 / 0.12. The calibration holds for C-donor
  too. Worker time 3.4 h (7,210 s for the ten N = 400 runs alone). The N ≤ 200 C-donor calibration ran between the
  code commit and the first counted cell; the N = 400 part ran after the S cells (batch order, `batches.sh`).
- **Report detail (found while reading the first cells, no dynamics affected):** T_ext is not a multiple of the
  10-generation step, so main-cell runs end at T_ext rounded up (≤ 9 generations later) and their final state is read
  as T_ext's.

## 2. Costs

**Probes** (one discarded replicate, 990, per cell; `runs/realizable_scaling/smoke_rows.json`): S-nonself
calibrated (400, 64) to T_ext 211 s (frozen at 13,320), S-nonself (100, 256) to 40,000 277 s, C-donor calibrated
(400, 64) to 2,000 875 s, C-donor (100, 256) to 2,000 319 s. The stored provenance cells give 8–17 s per S-nonself run
at (100, 64), 30 s at (200, 64), 200–380 s per C-donor run at (100, 64) / (200, 64) with a tail to 10× the mean.

**Projection** (worker-seconds, mean-based): S-nonself 24,500; ablation 12,000; proportional 11,500; panel 26,600
(S rules ≈ 75,000, 21 worker-h); C-donor without extensions ≈ 101,000 (28 worker-h; (400, 64) both arms 36,000,
(200, 128) both arms 26,000); dense donors ≈ 50,000 (14 worker-h). Total ≈ 226,000 worker-s ≈ 21 h on 3 workers
without C-donor extensions, ≈ 23–25 h with them and well over 24 h if C-donor's tail repeats at N = 400.

**Drop order applied (disclosed before any cell):** step 1, the 10,000-generation extensions outside the main cells,
is applied **to the C-donor and dense-donor cells only**, where it buys the margin; the S rules' extensions to 10,000
are kept (they cost under 5% of the total and RE 4, R10 and the resolution statistics need them). C-donor and dense
cells are therefore scored at 2,000 (runs universal-open at 2,000 are mostly frozen or settled; provenance's C-donor
moved 37 → 37 and 18 → 19 between 2,000 and 10,000). N = 400, I = 256 and C-donor off P3 are kept; the batches run in
the order main S-nonself cells and the panel → the other S cells → C-donor → dense donors, so that if the total
overruns the next drop step (C-donor off P3, then dense donors last in line) falls on the cheapest-to-lose cells.
Measured costs are reported per cell in the run report.

**Addendum (drop-order step 2, applied after the S cells and the C-donor calibration, before any C-donor or dense
cell had reported except one replicate).** Measured: the S cells took 20.6 worker-h (projected 21); the C-donor
calibration 3.4 worker-h; the first C-donor (400, 64) replicate 1,847 s, twice the probe. Re-projected, the C-donor and
dense blocks would take ≈ 65 worker-h (≈ 22 h on 3 workers) against ≈ 14 h left in the budget. The spec's next step
drops N = 400; the S cells at N = 400 had already run and are kept. For the copying rules, **C-donor (400, 64) at
mN = 1 and dense donors at (400, 64) on both arms are dropped**; **C-donor (400, 64) calibrated is kept** (20 runs,
last in line) because RE 6 and Gemini's G2 are scored only there, so G2 is scored on that one arm. The one finished
replicate of the dropped C-donor cell (replicate 1: not universal, a bridge-less rival, 1,847 s) is kept in the rows
and not reported in the cell tables. The three runs in flight were stopped (pool children killed by pid before the
driver). Remaining order: C-donor (all other cells) → dense (200, 64) both arms → C-donor (400, 64) calibrated.

