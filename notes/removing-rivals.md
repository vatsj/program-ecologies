# Removing rival networks: a sponsored PrudentBot donor (prevention) and seed rain (cure) (notes, 2026-10-15)

Spec `specs/2026-10-15-removing-rivals.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after review"
supersede the earlier text where they conflict). §1 is written by hand before any code of this run and before any
counted cell. §2 (code validation, Part 0 static results, projected costs) is appended after the code and before any
counted cell.

Base, imported unchanged: the realizable-scaling machinery (`src/realizable_scaling*.py`) on provenance's language,
grammar P (n = 7, 12,546 spellings, prior L), S-nonself rule, lack rule, kernel and cached tables (17,394 units),
ε = 0 except for rain, w = 0.3, r = N/2 encounters per Moran event, calibrated mN = (N/100)^0.7. The cached tables
are copied from the scaling worktree's rebuild (untracked, unchanged). Every number from a rain cell is a finite-ε
approach-rate diagnostic at finite (N, I, horizon), never π; every number from an ε = 0 cell is a lottery statistic.

*Disclosure (before this section).* Before writing it I read the spec, the two RESULTS sections, the scaling notes and
code, ran the RE's example script (rs_prop_200_128_cal rep 1 to generation 2,000, a reproduction of a stored run, not
a cell), and made table lookups: the PrudentBot run trees (τ 123, the `CHK(them,me,C)`-first tree, H unit 123 with
one C and one D script; τ 963, the `CHK(them,^D,D)`-first tree, mutual with 123), and the per-tree status of the
stored holders' spellings against the target defined in §1.1 (counts of stored runs by spelling-level status). That
lookup already showed that many stored universal-open runs hold open spellings with no self-cooperating unit mutual
with PrudentBot (e.g. `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)`, unit (159, C (2,), no D script)). It informs my
own predictions and is reported properly in §2.

## 1. Design

### 1.0 The object in one paragraph

At N ≥ 200 every non-universal stored run is absorbing by the scaling run's static check. Two removal mechanisms are
tested. **Prevention:** a state-sponsored PrudentBot carrier with its full certificate list on every island at
founding, so the target network is present everywhere before the scramble decides. **Cure (finite ε):** a trickle of
fresh founders from the length prior (empty lists, S-nonself), which can bring back *predators*: programs that
exploit a rival holder, do not cooperate with their own copies, and are defected against by every target holder. The
path rival → predator → target needs no bridge: the predator takes the rival island by dominance, leaves an all-defect
island, and the target enters a defector island as establishers always do. At ε = 0 the path is closed because every
predator dies in the scramble long before rivals settle.

### 1.1 The target network (frozen now)

- **Reference holder.** u_PB = the H unit of the PrudentBot run tree τ 123, `if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)`
  (provenance's named CBP4), with its full list (one C script, one D script). It self-cooperates and is mutual with
  the other PrudentBot tree (τ 963).
- **Target units** 𝒯 = {u : u self-cooperates (same quote) and A[u, u_PB] = A[u_PB, u] = 1} (a holder of unit u_PB
  itself, twin or same quote, is in 𝒯). This is the amendment's "pairwise P(C,C) ≥ 0.95 with the PrudentBot holder":
  between two holder types P(C,C) is 0 or 1, so ≥ 0.95 means mutual cooperation.
- **Target island:** held (the majority quote self-cooperates and the island's P(C,C) ≥ 0.5, the scaling run's rule)
  and its majority quote's unit ∈ 𝒯. **Universal-on-target run:** every island is a target island and every pair of
  holders is mutual (cc_pair = 1; "with each other"). 𝒯 need not be pairwise mutual as a set; a run whose holders are
  all in 𝒯 but contain a non-mutual pair is not universal-on-target and is labelled *split target*.
- **Rival island:** a held island whose holder is not in 𝒯. Labels (hierarchical): *identity* (holder unit an
  identity unit, provenance's `ident`), else *exploitable* (some accessible predator, §1.2, has positive prior mass),
  else *closed*. Closed non-identity rivals are split into *open* (mutual with CooperateBot-H, i.e. the FairBot-family
  open network: bridged to the target through FairBot-type units) and *non-open*. Unheld islands are *unheld*.
- Universal-open (provenance's definition) is reported beside universal-on-target throughout; it is not the target.
- **Network-island loss** (amendment 5): an island whose majority quote is in 𝒯 changes to a majority quote outside 𝒯
  and stays outside for ≥ 25 generations (checked every 5 generations: six consecutive checkpoints spanning 25
  generations). Shorter episodes are *transient contamination*, reported separately. Rival → target and target →
  rival transitions are both logged with the residence time and the new holder's certificate provenance (seeded
  lineage, or a spelling first present after a rain arrival).

### 1.2 The operational predator classifier

For a rival holder X (unit x, spelling s_X) on an island, and the run's target holders 𝒯_run (the target units held on
any island at the checkpoint, plus u_PB):

- A **fresh founder** of spelling s starts at the empty unit e = E_u[τ(s)] under S-nonself. Its **phenotype against
  X** u_X(s) is the unit reached by repeating the kernel's own side procedure against X (C production if lacking a C
  entry and s ≠ s_X, then the D step), until it stops changing (at most a few steps: production is deterministic in
  (unit, partner)). The procedure calls the kernel's numba functions (`c_produce`, `c_append`, `d_step`), so the
  phenotype is exactly what the kernel would produce.
- s is an **accessible predator of X** iff, with p = u_X(s): A[x, p] = 1 (X cooperates with it), A[p, x] = 0 (it
  defects against X), it does not cooperate with its own copies (selfa[p] = 0), and A[t, p] = 0 for every t in 𝒯_run.
- **Reported for each X:** the accessible predator mass μ(Pred_X) = Σ_s μ_L(s)·1[s predator], the number of
  predator spellings, the top three by mass (stating whether DefectBot `D` or another constant is among them), and
  the certified-table count (units p with the four relations, regardless of reachability), for comparison with the
  RE's 2,870 / 2,222.
- **Reactions.** X's own phenotype after meeting p (X may lack an entry and produce against p) and p's phenotype after
  meeting each target holder (S-nonself production against a target migrant) are computed; a predator whose relations
  fail after these reactions is reported as *reaction-fragile*.
- The classifier is applied to every failing island at generation 2,000 of every stored non-universal-on-target run at
  N ≥ 200 (S-nonself, proportional, ablation; both mN arms), reconstructed draw for draw (§1.6), and to the RE's
  example (rs_prop_200_128_cal rep 1, anti-punisher on 7 islands).
- *By construction identity holders are closed:* a TwinD unit cooperates only with its own quote, so nothing outside
  its quote is cooperated with, and its own quote self-cooperates. An S-guarded holder (cooperates only with partners
  certified to cooperate with it, through a sound checker) is closed too: it cooperates with p only if p is certified
  to cooperate with it, and soundness makes p cooperate. So exploitable rivals are exactly the holders that cooperate
  with some uncertified partner; the anti-punisher (cooperate unless certified to punish DefectBot) is the type case.

### 1.3 Triples (amendment 2), by hand

Payoffs (kernel): R = 0 (C,C), T = 1, S = −2, P = −1. For a triple (X rival, P predator, Z target holder) with the
predator relations of §1.2 and the bridge-less rival (X and Z defect against each other, Z self-cooperates, X
self-cooperates):

| row vs column | X | P | Z |
|---|---|---|---|
| X | 0 | −2 | −1 |
| P | +1 | −1 | −1 or +1 |
| Z | −1 | −1 | 0 |

(P vs Z is −1 if P defects against Z, +1 if P cooperates with nothing; Z defects against P by definition, so Z's entry
against P is −1 when P defects against Z and +1... no: Z defects against P, so Z gets −1 if P defects and +1 if P
cooperates with Z, and P gets −2 in that case.)

- *X–P:* P beats X against every opponent type by exactly 1 (P vs P −1 > X vs P −2; P vs X +1 > X vs X 0): **strict
  dominance, no X–P mixture.** One P in N − 1 X fixes with ρ ≈ 0.26 at N = 100–400 (exact kernel formula), while one X
  in a P island has ρ ≈ 10⁻²⁷ at N = 200.
- *P–Z:* with P defecting against Z, one Z in a P island is neutral at first (−1 against P either way) and favoured as
  it grows (0 vs −1 among Z's): ρ = 0.042 / 0.030 / 0.021 at N = 100 / 200 / 400 (6× the neutral 1/N). If P
  cooperates with Z, ρ ≈ 0.45. One P in a Z island has ρ ≈ 4·10⁻¹⁵ at N = 200: **predators cannot break target
  islands.**
- *X–Z:* the bridge-less coordination barrier, ρ ≈ 7·10⁻⁹ at N = 200 (scaling notes §1.6).
- So under the stated relations the chain eliminates the rival through an all-defect island; a mixture can arise only
  through *reactions* (X or P changing unit on meeting the other or a migrant), which §1.2 checks per triple, and
  through other entrants taking the all-defect island first (any self-cooperating establisher enters a defector island
  the same way Z does; with mN·s_Z ≫ εN·μ(establishers) the target wins the race wherever it is the main network).
- **Kernel test on forced islands.** For the most promising triples (largest μ(Pred_X)·ρ), an archipelago of I = 8
  islands, N = 200, calibrated mN: four islands all X and four all Z (the run's quotes and units), one fresh P founder
  injected into one X island, ε = 0, 2,000 generations, 50 replicates (kernel seeds distinct from every cell). Recorded:
  P reaches ≥ 0.5 of its island, the X islands' fates (to Z, to P then Z, unchanged), times. A matched non-predator
  (the non-predator spelling closest in prior mass to P whose phenotype against X is self-cooperating or cooperating
  with X) is injected in separate replicates.

### 1.4 Rain

- At each Moran birth, with probability ε the newborn is a **fresh founder**: spelling drawn from L, empty lists,
  S-nonself (unit E_u[τ(s)], ancestry 0), placed in the victim's slot of the victim's island (the same island and slot
  the copy would have taken). Each island receives N births per generation in expectation, so fresh founders per island
  per generation = ε·N; **ε = εN/N with εN ∈ {0.01, 0.1, 1}**.
- Draws: the rain coin is the event's draw 5 and the spelling draw 6 (inverse CDF of L), both counter-based and unused
  by the kernel (it uses draws 0–4 for the birth and 8 + 5q onward for encounters). **At ε = 0 the coin is not tested,
  so the rain kernel reproduces the scaling kernel draw for draw.** Under rain the birth's own draws are still
  consumed, so two rain rates share every draw until their states differ.
- **Expected arrivals.** Predators of X arrive at εN·μ(Pred_X) per rival island-generation; succeed with ρ_P ≈ 0.26;
  so the cure hazard per island is h ≈ 0.26·εN·μ(Pred_X) (plus predators migrating from islands they already took),
  and P(cured within 10,000 generations) ≈ 1 − exp(−2,600·εN·μ). At εN = 0.1: μ = 10⁻³ → 0.23, 4·10⁻³ → 0.65,
  10⁻² → 0.93. Sol's "80% of islands receive a predator at μ ≥ 0.0016" ignores ρ_P; with it the 80% point is
  μ ≈ 6·10⁻³ at εN = 0.1, ≈ 6·10⁻⁴ at εN = 1. After the predator, the target retakes the all-defect island at hazard
  ≈ mN·s_Z·ρ_Z(P) ≈ 1.6·0.9·0.03 ≈ 0.045 per generation at N = 200 (≈ 25 generations).
- **Losses.** A target island is entered by fresh founders at εN per generation; S-guarded target holders cannot be
  exploited, so a loss needs a coordination crossing (ρ ≈ 10⁻⁸ at N = 200) or an *exploitable target member* (a unit in
  𝒯 that cooperates with some uncertified partner). §2 reports the exploitable target members and their predator mass.
  Rain also creates transient contamination (defectors living a few generations), which keeps islands unsettled and
  costs wall time, not islands.

### 1.5 Cells

Common: S-nonself unless stated, L seeds, w = 0.3, calibrated mN, horizon 10,000, snapshots at 500, 1,000, 2,000,
5,000, 10,000; per-island holder tracking every 5 generations in rain cells and B1 branches (target / rival / predator
share), traces every 10.

- **Part A, sponsored donor.** At founding, island i's slot j_i is the C-donor position (provenance's donor stream
  [N, I, r, SALT, 3], first draw `integers(N)`), so donors sit where C-donor's donors sit and all other founders are the
  replicate's L draws: paired with S-nonself and C-donor on identical founder and kernel streams. The donor is the
  PrudentBot spelling above, rule H (it keeps its full list, its offspring are H copies of it). Cells (200, 64),
  (400, 64), (200, 128), (100, 256), replicates 0–19. **Donor control** (amendment 6): the same spelling at the same
  position with an empty list under S-nonself, at (200, 64) and (200, 128). Baselines: the stored S-nonself
  calibrated runs and C-donor calibrated runs at those cells, reconstructed by rerunning them with this run's job (draw
  for draw, checked against the stored traces) so that target membership is measured on units; C-donor baselines to
  2,000 only (the stored C-donor horizon; C-donor (400, 64) calibrated has 10 stored runs).
- **Part B1, cure.** Every stored S-rule run at N ≥ 200 (S-nonself, proportional, ablation; both mN arms) that is not
  universal-on-target at generation 2,000 is reconstructed to generation 2,000 (checkpoint). Each checkpoint is
  branched into an ε = 0 continuation and rain continuations at εN = 0.01, 0.1, 1 (amendment 3), each for 10,000
  generations, same kernel stream: cures are differences between matched branches. Per rival island at the
  checkpoint: resolved to target, resolved elsewhere, or not; path; intermediate holders; time.
- **Injection assays** (amendment 4). From up to 6 checkpoints with exploitable rival islands (the largest μ(Pred_X)
  first, at most two per cell): one fresh founder of the top accessible predator spelling, and separately the matched
  non-predator, replaces a random individual of one rival island at generation 2,000; ε = 0 continuation for 2,000
  generations; 20 replicates each with distinct kernel seeds. Separates arrival scarcity (the predator works when it
  arrives) from establishment failure (it does not).
- **Part B2, natural.** S-nonself from generation 0 with rain at (200, 64) and (200, 128), εN ∈ {0.01, 0.1, 1},
  replicates 0–19, horizon 10,000. Paired with the stored S-nonself runs (identical until the first rain arrival).
- **Part B3, both.** The sponsored donor plus rain at εN = 0.1 at (200, 64) and (200, 128), replicates 0–19.
- **Drop order** (spec): B2 at εN = 1, then (100, 256) in A, then B3; applied only if the projected total exceeds
  about 20 hours on 3 workers, disclosed in §2 before any affected cell.

### 1.6 Paths and endpoints (amendment 5, fixed now)

For a rival island with holder X at generation 2,000 (B1) or at its first rival snapshot (B2/B3):
- **Resolution:** the island becomes a target island and stays one for ≥ 25 generations (six 5-generation checkpoints).
- **Predator step:** before resolution, the share of the island's individuals whose unit is a predator of X (§1.2
  relations evaluated on units, not spellings) reaches ≥ 0.5 at some checkpoint. Lineages are identified by phenotype
  (the kernel's birth step chooses types, not individuals, so descent below the type is not defined).
- **Direct invasion:** resolution with no checkpoint at which a quote other than X's and target quotes holds the
  majority, and no predator step.
- **Other:** any other resolving path (some non-target, non-predator majority in between); the intermediate holders
  are logged.
- **Resolved elsewhere:** the island ends held by a non-target quote different from X (e.g. another rival).
- Statistics per run: universal-on-target and universal-open at 2,000 and 10,000 (B1: at 2,000 + 2,000 and
  2,000 + 10,000), identity and rival islands, target-island losses and transient contamination, the paths, costs.
  Uncertainty: run-clustered (bootstrap over runs) intervals; 20/20 is reported with its Wilson interval (lower bound
  ≈ 0.84), and near-certain thresholds are read as observed thresholds only (amendment 7).
- Efficiency (island P(C,C)) is reported, never used to select.

### 1.7 Validation plan (code, before any counted cell)

1. ε = 0: the rain kernel equals the scaling kernel draw for draw (states identical after 200 generations on a
   (200, 64) run), and reconstructed stored runs match their stored traces to generation 2,000 and, after a checkpoint
   save and restore, beyond it.
2. Rain: the realized fresh-founder rate per island-generation equals εN within sampling error, and the founders'
   spellings match L (χ² on the top spellings, total variation on the rest).
3. The sponsored founder holds PrudentBot's full list (unit 123, C (9,), D (3,)) on every island and is the only
   founder changed relative to S-nonself; the empty control differs only in its unit.
4. The predator classifier on the RE's example: the anti-punisher (unit 9430 in that run) is exploitable; the
   classifier's certified-table counts are compared with the RE's 2,870 / 2,222.

### 1.8 Hand predictions

- *Target vs open.* PrudentBot defects against every partner that cannot certify its own defection against
  DefectBot, so 𝒯 is much smaller than the open network: open S-guarded spellings whose D production fails (their
  defection against DefectBot is not provable by their own tactic) are off-target. I expect a large share of stored
  universal-open runs at N ≥ 200 to be off-target, and the closed-open label to be the most common non-identity rival
  label (≥ 0.5 of non-identity rival islands), which makes RE 1 fail as worded on the target definition while
  holding (or nearly) for the certificate-reading rivals of the stored classifier.
- *Exploitable rivals.* Predator mass: junk programs (not self-cooperating, defecting against X, with no provable D
  certificate) are a large part of L; for the anti-punisher I expect μ(Pred) ≈ 0.01–0.05, so at εN = 0.1 a cure
  probability ≥ 0.9 in 10,000 generations, ≥ 0.6 at εN = 0.01 (μ ≥ 0.01 gives 1 − e^{−0.26} ≈ 0.23 at εN = 0.01 —
  so rather 0.2–0.7 at εN = 0.01), ≈ 1 at εN = 1. DefectBot is not a predator (its first D step certifies it, and the
  anti-punisher defects against certified punishers).
- *Closed rivals:* identity islands do not resolve (≤ 0.02 at any rate); closed open rivals resolve only through
  FairBot-type bridges drifting in (neutral, ∝ 1/N), a few per cent per 10,000 generations at εN ≤ 0.1.
- *Losses:* ≈ 0 target-island losses at εN ≤ 0.1 (only coordination crossings or exploitable target members).
- *Sponsored donor:* identity islands fall (the donor's network colonizes islands before TwinD lineages acquire their
  script) but not to ≤ 0.01 at (200, 128) and (400, 64); universal-on-target 0.4–0.8, limited by closed open rivals
  (bridged, slow), not by identity. The empty-list control is close to S-nonself (one prudent founder per island among
  N is lost in the scramble about as often as any other).
- *B3:* sponsorship plus rain removes the exploitable residue, not the closed open one: 0.5–0.85.

### 1.9 Selected versus drift (the RS's criterion, added on the RE's instruction before any code)

The RS (2026-10-15): "trickle and drift are distinguished only by scale - a small trickle over infinite time brings
back the shadow. The divide I wanna draw is that drift should never colonize an island, only reintroduce fit
programs." Operationalized:

- **Lineages.** Every fresh founder gets a lineage id (seeded individuals have id 0). At a birth the child copies the
  lineage id of a parent individual chosen uniformly among the source island's individuals of the chosen type (the
  kernel's birth chooses a type with probability ∝ count·fitness, and individuals of one type have equal fitness, so
  this is the type-level birth resolved to individuals; it uses the event's draw 7 and does not change the dynamics).
  A slot keeps its id when its occupant changes unit by gene acquisition. So lineage = descent from one fresh founder,
  below the type.
- **Colonization:** a rain lineage holding ≥ 0.5 of an island at a 5-generation checkpoint (first time per lineage
  and island).
- **Selected vs drift at arrival.** At each arrival the kernel records the island's majority type X (and its share)
  and the founder's own empty-unit fitness against the island and the island's mean fitness. The founder's phenotype
  p = u_X(s) (§1.2) is computed afterwards. **Primary:** *selected* iff pay(p, X) > pay(X, X) (a rare p's fitness
  against the resident majority exceeds the residents'), *neutral* iff equal, *deleterious* iff less; *drift* =
  neutral or deleterious. Exact for a near-monomorphic island; the majority share at arrival is reported, and the
  empty-unit comparison (the founder's actual fitness at the instant of arrival against the whole island) is reported
  beside it.
- **Reported per rain rate:** drift colonizations per island-generation; selected colonizations; the **shadow case**
  (a drift-classified lineage colonizing an island that was a target island at arrival); per-arrival colonization
  probabilities by class (selected / neutral / deleterious), at N = 200 and N = 400 (B1's (400, 64) checkpoints),
  against the ≈ 2s versus ≈ 1/N picture (s = w·(pay(p, X) − pay(X, X)) under the kernel's exp(w f) birth weight;
  for a predator of a cooperative rival s = 0.3, so 2s = 0.6 against the exact ρ ≈ 0.26 of §1.3, since the Moran
  birth–death with s = 0.3 is not in the weak-selection regime); and the per-predator-arrival cure probability (rain
  runs and injection assays).
- **Admissible window:** for each rain rate, whether rival cures occur with zero drift colonizations over the horizon
  (per cell and pooled), and the ratio cures / drift colonizations per island.
- *By hand:* a neutral arrival fixes with 1/N = 0.005 at N = 200, so drift colonizations ≈ εN·μ(neutral)/N per
  island-generation; on a target island almost every arrival that is not a junk defector is deleterious (no
  certificate yet) and the neutral ones are other target-compatible establishers (FairBot-type shadows), μ ≈ 10⁻³
  (FairBot's tree mass) to 10⁻², so ≈ 0.1·0.005·0.005 = 2.5·10⁻⁶ per island-generation at εN = 0.1, i.e. ≈ 1.6 per
  64 islands per 10,000 generations. They are shadows inside the target (same behaviour), not losses. A cure needs a
  selected predator arrival: ≈ 0.26·εN·μ_pred per rival island-generation. So the window (cures, no drift
  colonization) needs μ_pred·0.26 ≫ μ(neutral)/N, and over a fixed horizon it shrinks as εN grows; I expect drift
  colonizations of target islands by FairBot-family shadows at every rate with εN ≥ 0.1 over 64–128 islands, hence no
  strict window at εN = 0.1 or 1, and a window at εN = 0.01 only if μ_pred is ≳ 10⁻².

## 2. Code validation, Part 0 static results, costs (appended after the code, before any counted cell)

Code: `src/removing_rivals_kern.py` (provenance's `segment` copied and extended at the birth step: rain, lineages,
arrival records), `src/removing_rivals.py` (target, founders, `RRRun` with checkpoint save / restore and injection, the
predator classifier, island status), `src/removing_rivals_run.py` (checkpoints, B1 branches, lottery cells, assays),
`src/removing_rivals_report.py`, `src/removing_rivals_probe.py` (cost probes); `tests/test_removing_rivals.py`
(5 tests, passing; all need the cached tables and skip without them).

*Correction to §1.3 (wording only).* The parenthesis under the triple table is garbled; it should read: Z defects
against P by definition, so Z's payoff against P is −1 if P defects against Z and +1 if P cooperates with Z (P then
gets −2). The table's P-row entry against Z is −1 or −2 accordingly (not "+1"). The conclusions below the table are
unchanged.

### 2.1 Validation

- **ε = 0 is the scaling kernel.** The rain kernel with ε = 0 (lineage tracking on or off) gives identical slots,
  presence lists and type tables to the scaling kernel after 150 generations (test); lineage tracking leaves the
  dynamics unchanged.
- **Stored runs reproduce draw for draw.** All 300 stored S-rule runs at N ≥ 200 (S-nonself, proportional,
  ablation; both mN arms) were reconstructed to generation 2,000: **0 differences over 11,934 trace points**
  (P(C,C), islands ≥ 0.9, held, identity, open, SPO islands, type counts, universal-open, efficient islands).
- **Checkpoints are exact.** A saved and restored state continues identically to the uninterrupted run (slots,
  presence order and the payoff sums of present types bit for bit, test). The B1 ε = 0 branch is additionally compared
  with the stored trace every 500 generations beyond 2,000.
- **Rain.** At εN = 20 for 40 generations on (200, 64) the realized rate is εN within sampling error and the
  spellings of the top 15 prior spellings pass χ² against L (test); at εN = 1 on (200, 64) the rate was 0.998 per
  island-generation. The type table saturates under rain (≈ 27,000 types at εN = 1 after 1,500 generations on
  (200, 64); cap 150,000).
- **Sponsored founder.** One founder per island differs from S-nonself's founders, at C-donor's donor position, with
  PrudentBot's spelling, rule H and unit 123 = (τ 123, C (9,), D (3,)); the empty control differs from it only in rule
  (S-nonself) and unit (the empty unit 4268) (test).
- **Predator classifier.** On the RE's example (anti-punisher, unit 9430) the certified-table counts are exactly the
  RE's: 2,870 units it cooperates with that defect against it, 2,222 of them non-self-cooperating and defected against
  by every target holder. Identity holders have 0 accessible predator mass (test).

### 2.2 Part 0 (static, generation 2,000 of the 300 reconstructed runs)

`runs/removing-rivals-part0.json`; per-island rows in `runs/removing_rivals/ckpt_rows.json.gz`.

- **The target is strict.** 𝒯 has 235 units (PrudentBot's two trees included; all open; 2,232 of its 27,495 pairs
  not mutual). Of the 185 runs universal-open at generation 2,000, **132 are universal-on-target**, which is every universal-on-target run (𝒯 is open), so 132 of 300 runs
  are universal-on-target in all (5 more have only target holders with a non-mutual pair, *split*).
- **Rival islands at generation 2,000** (non-universal-on-target runs, pooled): **closed-open 1,492**, identity 770,
  exploitable 260, closed-non-open 0, unheld 0.
  - *The stored classifier's rivals are exactly the exploitable ones:* all 260 islands it called non-identity rivals
    are exploitable (1.00), and its identity islands are my identity islands (770, none with a predator).
  - *The closed-open class is new to the target definition:* 1,492 islands the stored classifier counted inside the
    main network (mutual with the plurality open holder) are held by open S-guarded holders that PrudentBot defects
    against because they cannot certify their own defection against DefectBot: e.g.
    `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)` (unit 159, 297 islands + 111 under its `not` spelling),
    `if(or(CHK(them,me,C),CHK(me,^D,D)),C,D)` (unit 191), `if(or(CHK(me,them,D),CHK(them,me,C)),C,D)` (unit 1479),
    `if(or(CHK(me,^D,D),CHK(them,me,C)),C,D)` (unit 1991). They are closed (cooperate only with certified
    cooperators) and **bridged to the target by FairBot** (unit 3, a target unit that holds the most target islands
    and is mutual with both), so their islands exchange holders with target islands by neutral drift of the bridge,
    at ε = 0 as under rain. 171 of the 300 runs have different holder spellings at the stored final snapshot than at
    2,000, consistent with this drift.
  - **RE 1 on the target definition: 260 / 1,752 = 0.15 exploitable** among non-identity rival islands (run-clustered
    95% interval [0.10, 0.21]): the falsifier (≤ 0.5) fires. On the stored-classifier rivals it is 1.00. Identity
    islands with a predator: 0 of 770.
- **Predators.** 29 distinct exploitable holders, in two families:
  - *the anti-punisher family* (`if(or(CHK(me,^C,C),CHK(them,^D,D)),D,C)`, `if(CHK(them,them,C),D,if(CHK(them,^D,D),D,C))`,
    …: defect against anyone certified to defect against DefectBot): μ(Pred) = 0.073–0.077, about 950 predator
    spellings, top three `if(CHK(me,^D,D),C,D)`, `if(CHK(them,me,D),C,D)`, `if(CHK(me,them,D),C,D)` (5.2·10⁻⁴ each);
    certified counts ≈ 2,850–2,940 / 2,100–2,230; reaction-fragile mass 0.003–0.005;
  - *the certified-defection detectors* (`if(or(CHK(them,them,D),CHK(me,them,D)),D,C)` and its spellings: defect
    against anyone certified to defect against itself, or against whom I am certified to defect): μ(Pred) =
    0.0054–0.0058, about 70 predator spellings of 1.3·10⁻⁴ each (e.g. `if(and(CHK(me,them,C),CHK(me,^C,D)),C,D)`),
    certified ≈ 115 / 100, no fragile mass. This family holds 117 of the 260 exploitable islands.
  - **No constant is a predator** (DefectBot certifies its own defection at its first D step, and every exploitable
    rival defects against certified punishers); Gemini's condition for a cure is therefore not met.
  - Over the 260 exploitable islands μ(Pred) has median 0.073, quartiles 0.0058 / 0.074, minimum 0.0054.
- **Expected arrivals and cures** (§1.4 formula, mean over exploitable islands): εN·μ = 4.1·10⁻⁴ / 4.1·10⁻³ / 0.041
  predator arrivals per island-generation at εN = 0.01 / 0.1 / 1, and P(cure within 10,000 generations) ≈ 0.51 /
  0.89 / 1.00 (anti-punishers ≈ 0.86 / 1.00 / 1.00; detectors ≈ 0.14 / 0.77 / 1.00).
- **Exploitable target members:** none among the 25 most common target holders (0 accessible predator mass against
  each, with every other target holder defecting): the target network has no predators of its own under §1.2's
  definition. (The RE-example probe at εN = 1 nevertheless showed target islands turning unheld for 30–65 generations
  under junk arrivals; losses are measured, not assumed.)

### 2.3 Deviations and scoring consequences (declared before any cell)

- **B1's population.** "The stored failing runs at N ≥ 200" is read on the target definition: every reconstructed run
  not universal-on-target at generation 2,000 (168 checkpoints, including runs whose only failures are closed-open
  rivals or a split target). Rival-island statistics are reported per label, so the RE's exploitable rivals are read
  off their own rows.
- **Baselines.** S-nonself calibrated at (200, 64), (400, 64), (200, 128): generation 2,000 from the checkpoints;
  generation 10,000 from the B1 ε = 0 branch's snapshot at absolute generation 10,000 (runs universal-on-target at
  2,000 are taken as unchanged at ε = 0). S-nonself (100, 256) calibrated is rerun with this run's job (cell
  `rs_Snon_100_256_cal`, the stored replicates, to 10,000). **C-donor is not rerun** (its stored runs cost
  350–3,200 s each): its universal-on-target at 2,000 is bounded from the stored holder spellings (a universal-open
  run is on target iff every holder's unit is in 𝒯; a spelling whose tree has no self-cooperating unit in 𝒯 decides
  "off", one whose tree has only target units decides "on", others are ambiguous); RE 5's "at least C-donor's" is
  scored against the upper bound, and called undecided if the sponsored value falls inside the bounds.
- **Injection assays** use the 6 checkpoints with the largest exploitable predator mass, at most two per cell; the
  forced triples the 3 exploitable holders with the largest mass, each against the most common target holder of its
  checkpoint, 50 predator and 25 matched non-predator replicates.

### 2.4 Costs

Part 0 (300 reconstructions) took 13,086 worker-seconds. Probes (`runs/removing_rivals/probes.json`): one B1
checkpoint at (200, 128) for 2,000 generations costs 26 / 31 / 36 / 64 s at εN = 0 / 0.01 / 0.1 / 1; a sponsored
(200, 128) run to 2,000 generations 36 s; a rain εN = 1 (200, 128) run to 2,000 generations 77 s. Projection
(linear in generations, (400, 64) as (200, 128), (200, 64) and (100, 256) at half and equal cost): **B1 ≈ 114,000
worker-s**, A ≈ 15,000, B2 ≈ 17,000, B3 ≈ 4,500, S-nonself (100, 256) baseline ≈ 3,000, assays ≈ 9,500: about
163,000 worker-s ≈ 45 worker-h ≈ 15 h on 3 workers, under the 20-hour line: **no drop-order step is applied.** Order of
batches: A and the baseline → B3 → injection assays and triples → B1 → B2 (εN = 1 last).

### 2.5 Addenda while the cells ran (each written before the cells it affects)

- **Injection assays at N = 400** (written after 86 of the injection jobs had finished): the two (400, 64) checkpoints
  chosen by mass (rs_Snon_400_64_m1 8, rs_abl_400_64_cal 9) are among the slowest stored runs (≈ 220 s per
  2,000-generation injection), so their replicates are cut from 20 to 10 per arm (rows already finished beyond 10 are
  kept). The four (200, 128) checkpoints keep 20.
- **A diagnostic before B1** (post hoc, not predicted): B3 showed more identity islands than A (0.11 vs 0.02 per
  island). To find out why, the batch was stopped after B3 (the injection driver restarted with 2 workers) and one B3
  run was replayed (`src/removing_rivals_diag.py`); a static check followed (`src/removing_rivals_shadow.py`,
  `runs/removing-rivals-shadow.json`). Reported with the results; no cell's design changed.
- **Budget step for B1** (written after 17 of 168 checkpoints, all at (400, 64)): B1 ran at ≈ 1 checkpoint per
  6–7 minutes, projecting ≈ 17 h for B1 alone. B1 is restricted to the **calibrated arm** (87 checkpoints); the
  17 finished checkpoints (11 calibrated, 6 at mN = 1) are kept, the 6 mN = 1 ones reported as extra rows. The slowest
  calibrated checkpoint (rs_prop_400_64_cal 9, stored cost ≈ 5,200 s per 10,000 generations at ε = 0) is moved to the
  end, after B2, on one worker, and is dropped if the total runs past the budget. The three branches in flight when
  the driver was stopped were discarded (no row written).
