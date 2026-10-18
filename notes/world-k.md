# Identity-dependent results under world K (keyed self-hypothesis defection) (notes, 2026-10-18)

Spec `specs/2026-10-18-world-k-reruns.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; the two
amendment sections supersede the earlier text where they conflict, the later one winning). §1 is written by hand
before any code of this run and before any counted cell. §2 (code, validation, mechanism checks, projected costs) is
appended after the code and before any counted cell.

Base, imported unchanged: milestone 5's language and tables (`src/lt_genes*.py`), provenance's rules and kernel
(`src/provenance*.py`), the scaling run's founders, classifier and static absorbing check
(`src/realizable_scaling*.py`), the Pangaea founder partition, overlap-free kernel and merge (`src/pangaea*.py`), the
removing-rivals target, predator classifier and rival classes (`src/removing_rivals*.py`), the annealed rain kernel and
schedule (`src/annealed*.py`), and world K's reading and tables (`src/detectors.py`, `runs/detectors/K/`). Grammar P
(n = 7, 12,546 spellings, 4,162 run trees, prior L), w = 0.3, payoffs CC 0, CD −2, DC 1, DD −1. Every ε = 0 number is
a lottery statistic at finite (N, I, horizon), never π; the rain cell is a finite-ε diagnostic.

*Disclosure (before this section).* Before writing it I read CLAUDE.md, the spec, the RESULTS sections "Legitimate
detectors", "The realizable lottery along paths in (N, I, mN)", "Cliques on a Pangaea", "Provenance", "Removing rival
networks" and "Annealed mutation", the notes of the detectors, scaling and Pangaea runs, and the code named in the
spec. The untracked cached tables were cloned read-only (APFS copy-on-write; the source files were not modified) from
the detectors worktree: `runs/detectors/K/{static/, prod_exec.json, sets.npz, OSV.npy, SPO.npy, grudge.npz}`,
`runs/provenance/{static/, prod_exec.json, sets.npz, OSV.npy, SPO.npy}`, `runs/lt_genes/static/`. I then made table
lookups with two throwaway scripts in the session scratchpad (not committed; their outputs are quoted below): the
identity units of each world's universe and of its S-nonself and S-self closures, the natural units of every spelling
in both worlds, the Pangaea family classes at H units in both worlds, the former TwinD family's units under S-nonself
and S-self, the removing-rivals predator tables of three own-D readers in both worlds, the share of hypothesis-closed
D certificates live against non-partners, and a term-level check of the key of a population DefectBot. **No dynamics
of any kind have been run.** The lookups changed my reading of K (§1.1) and my predictions; they did not change the
cells.

## 1. Design

### 1.0 The object in one paragraph

In world L a program's hypothesis-closed D certificate (its D step's δ) validates at every root, so own-D readers
(`CHK(me,them,D)`) defect against every distinct quote: the TwinD family is a set of identity cliques and the stored
detector a near-clique. World K keys that certificate to the bare source of the partner it was produced against. The
RS adopted K as the provisional default (DEFERRED 1, 2026-10-18). This run redoes, in K and beside L on paired
founders, every result whose failure mode was an identity clique in the realizable PD grammar: the scaling path and its
copy law, the Pangaea continuum and its establishment law, the provenance rule (S-self against S-nonself), and the
removing-rivals rival classes, plus one paired rain cell. Explicit-`eq` cliques (identity-and-tags grammar) are a
different channel, untouched by K, and are not rerun.

### 1.1 What K is, as implemented: the key is the literal ⌜D⌝, which no population member has

Every producing rule runs the D step as PROD(x, ⌜D⌝, D) while the list lacks a D entry (provenance's `d_step`; the
partner never enters). So in K every hypothesis-closed D script is Key_{⌜D⌝}[δ], under S-nonself, S-self and every
other rule, and **no D certificate is ever keyed to a population member's source**. ⌜D⌝ is the literal constant
program `λme.λthem.D`; a population DefectBot is a carrier whose bare source is the grammar body
(`app(λ.D, 9100)` in the term encoding). By a term-level lookup, `key_of(D-H) ≠ KEY_D` under every marker. Hence:

- **In K an own-D atom `CHK(me,them,D)` is F against every population member, and `CHK(me,me,D)` is F at the self
  root.** Only the literal ⌜D⌝ inside a guard `CHK(x,^D,D)` reads the keyed certificate as T. An own-D reader
  defects against no one through its own box; it defects only through its other atoms.
- **PrudentBot's guard `CHK(them,^D,D)` reads the literal, not the population's defectors.** A program holding
  Key_{⌜D⌝}[δ] passes the guard although it cooperates with every population DefectBot. K therefore puts *certified
  suckers* into PrudentBot's network.
- Consequence for the spec's phrase "gentle readers": in K the own-D readers are gentle only if another atom makes them
  defect against defectors (the detector's `CHK(them,them,D)` disjunct). The TwinD family has no such atom: **in K it
  is an unconditional cooperator** (§1.4).
- **Distinct-key coverage and evictions** (amendment 2.3): every keyed certificate in the run carries the one key
  ⌜D⌝, and K0 has no grudge list or cap, so distinct-key coverage is one key per program and there are no keyed
  evictions. Both are logged (count of programs holding a keyed D script) but are fixed by the convention. The
  combinatorial concern of amendment 1.5 (one keyed certificate per distinct defector quote) does not arise in this
  implementation, because no certificate is keyed to a defector's quote at all.

This is K as defined in the detectors run and in its tables; I do not change it (the spec runs world K's tables). It is
stated here because it changes what K tests: K is not "self-certified defection against the partner it was produced
against", it is "self-certified defection is never live in play". Whether ⌜D⌝ should match population DefectBots is a
convention question for the certificates conversation (DEFERRED 1).

### 1.2 Identity holders under K (closures over each world's tables)

| | L | K |
|---|---|---|
| units / reachable (milestone-5 universe) | 17,394 / 11,365 | 17,375 / 11,260 |
| identity units in the universe (`ident`) | 21 (14 run trees, μ 0.00266) | 11 (10 run trees, μ 0.00195) |
| reachable under S-nonself / identity among them | 10,953 / **8** (4 trees, μ 7.1·10⁻⁴: the TwinD family Q) | 10,945 / **0** |
| reachable under S-self / identity among them | 11,679 / 21 (14 trees) | 11,663 / **11 (10 trees, μ 0.00195)** |
| natural unit identity, S-nonself (E → C step vs FairBot-H → D step) | μ 7.1·10⁻⁴ | **0** |
| natural unit identity, S-self founder meeting its own quote first | μ 0.00266 | **μ 0.00195** |

- **Under S-nonself, K has no identity unit at all.** No reachable unit is an identity unit, so identity islands are 0
  in every K S-nonself and proportional-control cell by construction (a theorem of the closure, checked in the runs).
- **Under S-self, K keeps the minted C-identity class.** The 10 trees are the only-self C class of provenance (e.g.
  `if(and(CHK(me,me,C),CHK(me,them,C)),C,D)`, `if(and(CHK(them,me,C),CHK(me,them,C)),C,D)`): their only producible
  C script ι is written at the self root and fails at every distinct root. K keys only D scripts, so this channel is
  untouched: L's 14 S-self identity trees are exactly these 10 plus the 4 TwinD trees. At 6,400 founders the 10 trees
  seed ≈ 12.5 copies per run, each minting once its lineage meets itself (provenance: minting happens inside
  certificate-less lineages, about 90 times per run under S-self over the whole only-self class of μ 0.018).

### 1.3 Families and μ_net (Pangaea's classes at H units, certificates saturated)

| class | L | K | moved (L → K) |
|---|---|---|---|
| D (legible defector) | 0.3786 | 0.3660 | → S 0.0110, → Eo 0.0010, → S− 0.0006 |
| Dill (illegible defector) | 0.0725 | 0.0589 | **→ APn 0.0126**, → S 0.0006, → BR, S− 0.0002 each |
| S (sucker, self-cooperating) | 0.4286 | 0.4415 (+0.0007 former TwinD) | |
| S− | 0.0592 | 0.0593 | |
| PBn | 0.0126 | 0.0122 | → S 0.0005 |
| CBo | 0.0014 | 0.0014 | |
| BR (bridges) | 0.0140 | 0.0142 | |
| APn (AP network) | 0.0316 | **0.0442** | |
| TW (identity) | 0.0007 | **0** (→ S) | |
| Eo | 0.0008 | 0.0017 | |
| **μ_net = PBn + CBo + BR** | **0.0280** | **0.0277** | |

- **μ_net does not rise.** The establishment law of a Pangaea (failure ≈ e^(−w·μ_net²·N), RESULTS "Cliques on a
  Pangaea") is unchanged to within 2%. The RE's premise for prediction 5 ("with the gentle readers in the network,
  μ_net rises") fails statically: the gentle readers that enter the network are suckers (§1.4).
- **What K moves is suckers and the AP network.** About 0.011 of former legible defectors (own-D readers like
  `if(CHK(me,them,D),D,C)`, which in L defected against everyone through the generic δ) become unconditional
  cooperators, and 0.0126 of former illegible defectors (readers of the partner's D box, e.g. `if(CHK(them,me,D),D,C)`,
  which in L met hypothesis-certified defection everywhere) become self-cooperating AP-network establishers. The AP
  network's prior mass grows by 40% and its parasite Dill shrinks by 19%.

**Natural units** (S-nonself: E unit, C step against FairBot-H, D step; mass of spellings by status L → K):
nonself → nonself 0.4826; open → open 0.3427; closed → closed 0.1070; T → T 0.0391; nonself → closed 0.0158;
nonself → T 0.0085; closed → T 0.0016; nonself → open 0.0011; closed → open 0.0009; identity → T 0.0007; T → nonself
0.0001. (T = in PrudentBot's network: self-cooperating and mutual with PrudentBot-H.)

- **The target network grows only by suckers.** Natural-unit T mass is 0.0392 (L) and 0.0499 (K), but T ∩ suckers
  (cooperate with DefectBot-H) is 0.0266 and 0.0371: the non-sucker part of the target is 0.0126 in L and 0.0128 in K.
  K's new target members are certified CooperateBots such as `if(CHK(me,them,D),D,C)` (μ 5.2·10⁻⁴), now the second
  heaviest target sucker.

### 1.4 Gentle readers and their predators

Own-D readers (run trees with `CHK(me,them,D)` that decides play; 402 spellings, μ 0.0308), by natural unit:

| | L | K |
|---|---|---|
| identity | 0.0007 | 0 |
| self-cooperating, cooperates with CooperateBot-H, defects against DefectBot-H (DET) | 0.0007 | 0.0018 |
| open (mutual with FairBot-H) | 0.0097 | 0.0226 |
| in T | 0.0023 | 0.0131 |

Removing-rivals predator tables (accessible predators against the reader's natural unit, targets FairBot-H and
PrudentBot-H):

| reader | L | K (top predators) |
|---|---|---|
| TwinD `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)` | 0 | **0.436** (5,458 spellings; DefectBot itself μ 0.0041, `if(CHK(me,^D,D),D,D)`) |
| the detector `if(or(CHK(them,them,D),CHK(me,them,D)),D,C)` | 0.0058 | 0.260 (detectors run's number reproduced) |
| `if(CHK(me,them,D),D,C)` | 0 | 0.422 (DefectBot, `if(CHK(me,me,D),D,D)`) |

**The former TwinD family in K** (S-nonself natural units, all 10 spellings): self-cooperating, cooperates with
CooperateBot-H *and DefectBot-H*, mutual with FairBot-H and PrudentBot-H, open, in T, twin cooperates. It is a
certified CooperateBot inside the target network, preyed on by every defector including the constant D. So the
"gentle readers' predator mass" is the sucker mass of the prior's defectors; these readers should die in the seed's
sucker phase like CooperateBot (Pangaea notes §1.1: suckers die logistically at rate ≈ w).

### 1.5 New rival classes (programs exploited or feuding under K that were not in L)

1. **AP-network establishers from former illegible defectors** (Dill → APn, μ 0.0126; `if(CHK(them,me,D),D,C)`,
   `if(not(CHK(them,me,D)),C,D)`, `if(or(CHK(them,them,C),CHK(them,me,D)),D,C)`, …): cooperate unless the partner is
   certified to defect against them; self-cooperating, mutual with the anti-punisher, not with FairBot. On islands they
   are rival (non-open) holders; they are exploitable by illegible defectors. **This is the one class that can make K
   less universal than L's proportional control.**
2. **Certified suckers in the target** (+0.0105 of T ∩ suckers): not rivals but exploitable members of the target,
   the K analogue of removing-rivals' "identity-exploitable target members", with DefectBot itself as predator.
3. **DET's feuding sub-family** (D → Eo 0.0010, e.g. `if(or(CHK(them,^C,D),CHK(me,them,D)),D,C)`): self-cooperating
   readers that defect against FairBot and PrudentBot (whose generic D certificates satisfy `CHK(them,me,D)`-type
   atoms), as the detectors run found.

### 1.6 What S-self does to the former TwinD templates under K (amendment 1.2)

The D step is partner-free under every rule (§1.1), so **no rule can write a self-play D certificate keyed to the
holder's own quote**: Gemini's mechanism (self-play D certificate → self-defector) cannot occur in this convention.
What S-self changes is the C step. Classifying the S-self founder whose first encounter is its own quote (C step at
the self root, D step, then FairBot-H):

- **6 of the 10 spellings (μ 4.5·10⁻⁴) become illegible suckers**: they write a C script at the self root that fails
  at distinct roots, so FairBot and PrudentBot defect against them while they cooperate with everyone (not open, not
  in T, not identity, twin cooperates).
- **4 spellings (μ 2.6·10⁻⁴) are unchanged**: open, in T, certified suckers, as under S-nonself.
- None is a self-defector and none is an identity holder.

So under K the former TwinD templates are suckers under both rules; S-self only makes 6 of them illegible. The S-self
vs S-nonself difference in K is therefore carried by the minted C-identity class (§1.2), not by the TwinD templates.

### 1.7 Does K suppress defection generally? (amendment 2.5)

- Hypothesis-closed D certificates live against non-partners (mean over 1,063 reachable units holding one, of
  CHD = T at roots (u, v), v reachable, v ≠ DefectBot-H): **0.278 in L, 0 in K** (and 0 against DefectBot-H in K,
  0.264 in L). K removes self-certified defection from play entirely.
- Prior-weighted cooperation among natural units: P(row cooperates) 0.490 → 0.503; mutual cooperation 0.243 → 0.256.
- So "K dissolves identity barriers" and "K suppresses defection" are the same operation here: the identity barrier
  was the only thing the generic δ did that a non-self-hypothesis certificate could not. The alternative explanation
  is not separable by design; what is separable is *where* the extra cooperation lands (suckers and the AP network,
  §1.3), which the cells measure.

### 1.8 Production and kernels (amendment 2.3)

- **r = 100 production encounters per Moran event** in every counted cell except the r = N/2 control, each on a
  uniformly drawn island between two uniformly drawn residents: 2r = 200 production opportunities per program per
  generation at every N. For r ≤ 100 provenance's, the Pangaea and the annealed kernels draw identically (counter
  RNG, draws 8 + 5q … 12 + 5q per encounter). The r = N/2 control uses the overlap-free Pangaea kernel.
- **Island cells** run on the annealed kernel (`segment_ann`), with ε = 0 except in the rain cell, lineage tracking on
  (every founder its own lineage id; a newborn inherits a parent individual's id, drawn with the kernel's otherwise
  unused draw 7, so tracking does not change any trajectory). This gives migrant ancestry. Lineage tracking costs
  O(N) per birth and is used for N ≤ 400; for N ≥ 800 it is off (disclosed in §2 if the cost forces it).
- **Pangaeas, fission–fusion and the r = N/2 control** run on the Pangaea run object (overlap-free kernel, merge).
- **World switch.** A run in world w is built with w's tables (L: `runs/provenance`; K: `runs/detectors/K`) by giving
  provenance's run constructor w's static set. Founder spellings are drawn from the prior L, identical in both worlds;
  units are w's E (or H) units of those spellings. Kernel seeds are the stored ones (provenance's for scaling and
  provenance cells, the Pangaea seed for Pangaea cells), identical in both worlds.

### 1.9 Cells (as amended), horizons, runs

Paired L / K everywhere; ε = 0 unless stated; calibrated mN = (N/100)^0.7 for I > 1 (mN = 1 at N = 100).

- **A. Scaling path** (scaling founders, provenance's kernel seed): (100, 64), (200, 64), (400, 64), (100, 128),
  (200, 128), (100, 256); rules S-nonself and the proportional control (L's TwinD family Q redrawn ∝ μ from the non-Q
  spellings, stream 6, the stored control's founders; the same founders in K, where Q is no longer identity);
  horizon 10,000, scored at 2,000 and 10,000. 20 runs per cell, 40 at (100, 64) for S-nonself (as in the stored runs).
  The K proportional control is the test of what the former TwinD mass contributes in K (certified suckers versus
  redrawn programs).
- **B. Provenance rule:** S-self at (100, 64) (40 runs) and (200, 64) (20 runs), both worlds, against A's S-nonself
  cells (same founders and kernel seed; only the rule differs). Horizon 10,000.
- **C. Pangaea continuum** (Pangaea founders: one list of 12,800 per replicate, nested partition, Pangaea kernel seed):
  (200, 64), (800, 16), (3,200, 4), (12,800, 1); fission–fusion (100, 128) merged at 200; Pangaeas of 3,200 and 6,400
  (their own lists). Horizon 10,000 (Pangaeas stop when frozen). 20 runs each, both worlds.
- **C′. r = N/2 control** on the overlap-free kernel at (800, 16), (3,200, 4), (6,400, 1), both worlds, horizon 2,000.
- **D. Rain** (amendments 1.4, 2.1): (200, 64), S-nonself, A's founders and kernel seed, the annealed schedule at
  K = 3 exposure (εN(t) = a(1 + (t − 200)/t₀)^−2 from generation 200, t₀ = N/2, A = 3/(ρ·μ_AP) = 156 arrivals per island,
  cut at 10,000; paired founder streams per island), horizon 10,000, both worlds, 20 runs. Paired against A's ε = 0
  cell (identical to generation 200).
- **E. Removing-rivals classification** (Part 0): at 2,000 and at the end of every A cell with N ≥ 200, both worlds:
  universal-on-target and every held non-target island labelled identity / exploitable / closed-open /
  closed-nonopen with the removing-rivals classifier on that world's tables.
- **Drop order** (spec), only if the projected total exceeds ≈ 24 hours on 3 workers, disclosed in §2 before the cells
  it affects: (100, 256), then the Pangaea at 3,200, then the proportional control at (100, 128).

### 1.10 Statistics and inference

- Per run: universal-open (the scaling classifier), its failure cause (identity / rival / inefficient / unheld),
  identity islands, rival islands by class, whole-run scramble failure (no held island), mean island P(C,C) and the
  fraction of islands ≥ 0.95 (reported, never selected on), universal-on-target, the static absorbing check at the end
  (universal / absorbing / coordination / bridged / reachable-bridge), first universal-open generation and last change
  (resolution-time censoring).
- **Per island:** establishment time (first checkpoint with P(C,C) ≥ 0.9), the holder's outcome class at every
  checkpoint (open = in the main network; identity; non-identity rival; unheld), the log of holder changes, and at each
  change and at 200 / 2,000 / 10,000 the share of the holder spelling's individuals whose founder lineage started on
  this island (*local*) or elsewhere (*migrant*).
- **Paired transitions:** for each paired L / K cell, the contingency table of island classes (L × K) at 200, 2,000
  and 10,000; conversion of an L identity island is attributed to *establishment* if the K island was held by a local
  lineage at its establishment and to *migration* if its K holder is migrant-descended. Snapshot tables are
  associations; lineage attributions are the transition evidence.
- **Gentle readers' exposure** (amendment 1.1): at 200, 2,000 and 10,000, for own-D reader individuals, the
  composition-weighted fractions of their island encounters that are mutual C, exploited (C against D), exploiting and
  mutual D; and the fraction acting through a matching keyed certificate (0 by §1.1, logged).
- **S-self budget** (amendment 1.2): at generation 0, 10, 50, 200 and 2,000, the expected share of S-self C-production
  attempts at a self root (lacking producers weighted by their quote's island frequency); minting events (entries into
  identity units, kernel counter).
- **Inference** (amendment 2.4): runs are the units. Proportions with Clopper–Pearson 95% intervals; paired run-level
  differences with McNemar exact p and a conditional exact interval for the difference (Clopper–Pearson on the
  discordant split, scaled by the discordant fraction); a "within x" claim is an equivalence claim only if the interval
  lies inside ±x, otherwise inconclusive. Unresolved runs (static label coordination / bridged / reachable-bridge, or
  universal-open changed after 2,000) are reported apart from absorbing failures.

### 1.11 Hand predictions (they become numbered predictions with falsifiers)

- K S-nonself has 0 identity islands everywhere (theorem); K S-self keeps ≈ 0.05–0.10 identity islands per island at
  (100, 64) (the minted class), so RE 1 holds for S-nonself and fails in the S-self cells.
- K S-nonself at N ≥ 200 sits at the level of L's proportional control, 0.75–0.95, residue non-identity rivals; the AP
  network gains rival islands (Dill → APn), so K may sit a little below the proportional control; the K proportional
  control equals K S-nonself to within noise (the former TwinD mass is 4.6–18 suckers per run and dies in the scramble).
- RE 3 holds: K is near-flat from (200, 64) to (200, 128) while L falls 11 → 4.
- RE 4 fails: S-self still mints C-identity in K, so S-nonself − S-self ≈ +0.15 at (100, 64) at 2,000 and ≈ +0.3 at
  (200, 64), where minted cliques are permanent.
- RE 5 fails: μ_net is unchanged, so Pangaea all-defect counts in K equal L's to within ±2 runs at 6,400 and 3,200;
  the falsifier (K ≥ L) fires with probability about one half. Gemini's counter-prediction holds.
- RE 6 holds (20/20 in K).
- The former TwinD lineages die in the scramble in K (as suckers); in L they become identity islands.
- Rain in K adds no identity (theorem: arrivals are S-nonself) and cures exploitable rivals; in L it adds identity
  islands relative to the paired ε = 0 branch.
- r = N/2 changes nothing beyond ±3 runs per cell in either world.
