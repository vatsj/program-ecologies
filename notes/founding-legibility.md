# Legibility at founding in the fully realizable social organization game (notes, 2026-10-14)

Spec `specs/2026-10-14-founding-legibility.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict). Parent run: RESULTS "The social organization game, fully
realizable", `notes/sog-fully-realizable.md` (cited as P§), `runs/sog-fully-realizable.md`, `src/sog_full*.py`
(imported, not edited). §1 is written by hand before any code of this run and before any counted cell; §1.x (code
validation and static numbers) is appended after the code and before any counted cell; §2 (costs) before the cells
(projection) and after them (realized).

*Disclosure.* Before writing this section I read the parent's stored run summaries (`runs/sog_full/cell_*/rep_*.json`,
the baseline of this run) for three quantities quoted in §1.4: the mean fair-island share and zero-wage share at
generations 0, 10, 20, 50, 100, 200 in the cells S_eq, S_eq_ideal, S_eq_forced_empty, S_eq_forced_pre, H_eq,
H_noeq_ideal and H_noeq_K3e6, and the per-run wall times. No code of this run existed and nothing was simulated.

## 1. Design

### 1.0 Readings of the amended spec, fixed before any code

1. **Base.** S-nonself₃ + eq exactly as the parent's cell `S_eq` (K₃′, c = 0.5, `eq` in both roles, PROD3 after the
   play in the residual fuel, cap P = K/4, lack rule, vertical inheritance, the worker gate), (N, I) = (100, 64),
   mN = 1, w = 0.3, r = N/3 encounters per Moran event, horizon 2,000, every run extended to 10,000. Replicate r uses
   the parent's founder stream r (the spellings drawn by `np.random.default_rng([r, N, I, 20261013])`) and its kernel
   seed, so every cell is paired with the parent's cell of the same K replicate by replicate. "Natural founding" is the
   parent's rule: founders with empty lists.
2. **The founding pass (L1; amendment 1).** One frozen snapshot: every founder of island i with an empty list. For each
   founder f (slot s ∈ {B, W1, W2}) independently, M = 10 triples are drawn: f in its own slot, and each other slot's
   member drawn uniformly (with replacement) from island i's founders of that slot; for a worker f, the other worker is
   drawn uniformly from the other worker slot's founders **whose spelling differs from f's** ("non-self": the gate
   would refuse f's production beside a copy, so a copy is never drawn; if every founder of the other worker slot is a
   copy, f gets no triple). A boss has no non-self restriction (no participant ever shares its source). Each triple is
   an encounter at the frozen snapshot: the play is composed with f's current list and the partners' empty lists, then
   **f alone** runs S-nonself₃ production in the residual fuel K − (f's play steps), one PROD3 attempt per set it still
   lacks in family order (workers [C] then [D]; bosses ≥¼, =½, ≤¼), cap P, NONE and cap timeouts append nothing, an
   exhausted residual is a fuel timeout; a script found is appended (lack rule: at most one script per set, as in play).
   f's list accumulates over its M triples; the partners never produce and never change (no founder-order
   bootstrapping). Production is computed by the parent's kernel routines (the composed encounter and `prod_boss` /
   `prod_worker`), so a founding attempt is the same computation as an encounter's attempt. The triples are drawn from a
   separate stream `default_rng([r, N, I, 20261014, 1])`. **Cost:** the production steps charged in the pass (and the
   play steps of its triples) are reported per founder and per island; they are outside the lottery's time and charge
   nothing in the dynamics. The founders then enter the lottery with these lists (each founder's type is its spelling
   with its founding list), and play and production continue as in S₃.
3. **L1-withheld (amendment 2), a stated deviation.** The spec says "outputs withheld until after the first selection
   event". Per island there are 3N = 300 birth–death events and N² = 10⁴ encounters per generation (each individual
   takes part in ≈ N = 100), so an island's first selection event comes ≈ 1/300 generation in, after about a third of
   its founders have had one encounter: withholding until then cannot be told apart from L1 (§1.4). The kernel can
   also be stopped only at a check (every 10 generations). **Withheld = the founding lists computed exactly as in L1,
   delivered at generation 10** (the first check, after the early collapse of §1.4): every individual present at
   generation 10 receives, for each set it still lacks, the founding script of a founder of its spelling (lack rule;
   nothing is replaced). Lineages are not tracked by the kernel, so delivery is **pooled by spelling**: an individual of
   spelling σ on island i is assigned one of island i's σ-founders uniformly (by a seeded stream; if σ was not founded
   on island i, one of σ's founders on any island). Founders start empty, so up to generation 10 the run is the natural
   run of the same seed exactly. The surgery is done with the kernel's own `replace` (one individual at a time, the
   fitness cube updated incrementally, prechecked), so the state is consistent; a full recomputation of the fitness
   after the surgery is checked against the incremental one. Withheld is paired with L3 (K = 3·10⁶, the cell where the
   reviewers expected an effect), 20 runs.
4. **L2, the mark (amendment 3): the bare-source key is unsafe; the cache is keyed on what production reads.** The
   amendment keys the mark on "the tuple of bare partner sources" and asks a test to verify "that production reads
   sources only". It does not: PROD3 computes the value of every non-Hyp-able box it meets by calling the check, and a
   check reads the subject's certificate list. Example (by hand): T₁ lacking [C] beside an uncertified D\* gets NONE
   (B½ is F, the run goes to `strike`), and beside the same D\* source holding its =½ script gets `EvR*; ChkR[EvR*; Ax ·
   Run]`. A mark keyed on (D\*, other worker) recorded at the first encounter would refuse the second production
   forever (until T₁'s own list changes), so it is not a cost fix. The test is written as specified and is expected to
   **fail**; the replay check of the amendment (sampled cached failures replayed against later encounters with the same
   bare partner sources and the same own list) measures how often a bare-source mark would suppress a success. Both
   reviewers' stated aim was safety (gpt-6.1-sol: "cache only failures proved invariant under the relevant changes"),
   so **the mark run here is keyed on everything production reads**: the program's own type (spelling and list, so a
   list change invalidates it), the attempt's set, and the encounter values PROD3 reads (for a worker: its slot, the
   boss's three certification values, the other worker's two, and whether the other worker is a copy; for a boss: the
   probe and identity values its run tree reads), K fixed per cell. Only NONE is cached (cap and fuel timeouts are not).
   - **Lemma M (the safe mark is a cost fix up to fuel).** For a fixed type and key, PROD3's outcome for a set is a
     deterministic function of the key when the attempt runs to completion, so a cached NONE predicts NONE. Skipping it
     changes nothing but the residual fuel left for the encounter's later attempts. Since a success needs req ≤ rem and
     skipping only raises rem, the set of successes under any history of marks lies between the successes with no
     skip (S₃) and with every completed NONE skipped. Hence L2's dynamics equal S₃'s except at **mark-sensitive
     encounters** (where those two bounds differ: a NONE attempt earlier in the family order starves a later attempt
     that would succeed), which the kernel counts. At the ideal table no attempt is starved, so L2 = S₃ exactly there.
   - **Storage, a stated deviation.** The kernel tracks types (spelling × list), not individuals, so the mark is held
     per type: once any individual of a type records a NONE for a key, every individual of that type skips it. Under
     Lemma M this changes the dynamics only at mark-sensitive encounters.
   - **Speed.** The amendment makes L2 the base of the 3·10⁶ cells "for speed" if the pilot matches. In this kernel a
     futile retry is a table lookup and a counter, not computation, so the mark saves no wall time (production steps
     are charged, not executed). L2 is therefore not made the base of any cell whatever the pilot shows; the 5-run
     pilot (paired with the parent's `S_eq` replicates 0–4) is the L2 cell, extended to more runs only if the budget
     allows. L1 + L2 is first in the drop order.
   - **Cost under the mark.** (i) In the kernel, a stride sample of executed encounters records play steps and
     production steps with and without the mark (executed encounters are those on non-quiet islands, P§1.13 item 4);
     (ii) on the parent's population-sampled encounters (300 at each of generations 0, 50, 200, 2,000) the mark's
     steady-state cost is play plus every attempt that is not a NONE (the limit in which every lineage has met its
     keys). RE 2's cost clause is scored on (i), with (ii) beside it.
5. **Cells (amendment 2; run counts fixed in §2 after the cost projection, in the spec's drop order).**
   N₆ = natural at 10⁶ (the parent's `S_eq`, 40 stored runs; replicates 0–4 rerun for the bit-identity validation and
   the new statistics); N₃ = natural at 3·10⁶; Nᵢ = natural on the ideal table (the parent's `S_eq_ideal`, 20 stored;
   rerun for the composition statistics, which the stored summaries lack); L1₆, L3 = L1₃, L1ᵢ (the decisive cell);
   L1W₃ (withheld); L1-sham₃ (the sham grammar in place of eq, paired through the spelling bijection); the N panel
   L1₃ at (200, 64), 12 runs; L2₆ (pilot); L1+L2₆. The assay: the isolated pure coalition (D\*, T₁, T₁), one island,
   no migration, 40 replicates, with L1 lists.
6. **An added diagnostic, labelled: H + eq on the ideal table (20 runs).** The spec's decisive comparison sets L1ᵢ
   against Nᵢ (0/20) and, through the RESULTS reading, against H + no eq on the ideal table (0.50), which is a
   different grammar. Under H every founder holds its full H list and lacks nothing, so H is exactly **S₃ with the
   maximal founding list** (every script of every path, `EQ`-true ones included) and no production. H + eq ideal is the
   upper bound of founding legibility on the same grammar and seeds as Nᵢ and L1ᵢ. It costs ≈ 4 minutes per run.
7. **Statistics (amendment 5, fixed in advance).** Everything the parent's `summarize` computes (persistence at 2,000
   and at 10,000 for every run, the scored first-fair-check establishment and the 10-check window, runs ≥ ½ fair, zero
   and ¼ wage shares, productive efficiency reported separately from fairness, holders, exits, sampled encounters),
   plus:
   - **Worker-slot composition** at generations 10, 50, 200 (and 0): the share of worker individuals (both slots,
     pooled over islands) in each class of P§1.8's classification by play (unconditional / open militant /
     greenbeard), the class a property of the spelling.
   - **Manipulation checks.** (a) *Generation-0 coverage:* the share of founders holding a script, per role and set;
     the generation-0 yield on coalition triples (§1.3). (b) *First-encounter decisions:* at generation 0, the
     probability that an open-militant founder strikes in a uniformly drawn encounter on its island, and the gen-0
     distribution of plays. (c) *Militant survival:* the share of worker slots held by open militants at generations 10
     and 50, and the fraction of (island, open-militant spelling founded there) pairs whose spelling is still present
     on that island at generations 10 and 50 (a spelling-level proxy for lineage survival; migrants of the same
     spelling count). (d) *Certificate retention through first encounters:* for each founder holding a founding script,
     whether that script certifies it (the check returns T) in a uniformly drawn generation-0 encounter on its island.
   - **Production:** attempts by outcome (found, NONE, cap timeout, fuel timeout, refused), the founding pass's cost,
     and the median per-encounter cost relative to play (the parent's pooled estimator).
   - **Paired contrasts** by replicate against the matched natural cell: mean difference in persistence with a
     bootstrap interval (2,000 resamples over runs), runs ≥ ½ fair with the exact McNemar p; Wilson intervals on run
     counts; "inconclusive" where an interval spans the predicted effect and zero. All claims are finite-(N, I,
     horizon) statements at ε = 0.

### 1.1 What the founding pass writes, by hand

At the frozen snapshot every partner has an empty list, so **every check about a partner is F**: a worker's boss
boxes (B≥¼, B½, B≤¼: is the boss certified to pay in the set) are F; a boss's probes (P_j^s:a: is w_j certified to do a
at the probe wage) are F. PROD3 follows the actual value at non-Hyp-able boxes (F → RunNeg, then the F-branch) and
tries the T-branch first at Hyp-able ones (O-atoms, the other worker's encounter box). Identity atoms take their actual
values on the drawn triple: a worker's `EQ` is false by construction (non-self); a boss's `N1`, `N2`, `EQW` vary with
the triple. Hence:

- **Workers:** the pass writes the scripts of the worker's **all-boxes-F path** (with Hyp-first scripts through O-atoms),
  one for the set its path's leaf is in; the other set returns NONE. Nothing in the 10 triples changes what a worker
  reads (all partners empty, `EQ` false), so **M = 10 gives a worker exactly what M = 1 gives**, and its later 9
  attempts are NONE. T₁ = `if(B½, work, strike)`: [D] = RunNeg on the boss's =½ box (valid at every root where the boss
  is not certified =½, including the probe roots (⌜pay(s)⌝, T₁, ·)); [C] NONE. Scab: [C] = `EvR*; Ax`. Striker: [D].
  T₀ = `if(B≥¼, work, strike)`: [D]. R = `if(B≤¼, strike, work)`: [C]. Q = `if(O:S, strike, work)`: [D] by Hyp on O:S
  (the strike-pact script), and [C] by RunNeg on O:S (the other is not certified to strike: true of every empty partner),
  so Q holds both. U_eq: `EQ` false, [C] = `EvR*; Ax` (Claim N₃: its `EQ`-true scripts stay non-producible). XM: [D].
- **Bosses:** the pass writes the scripts of the boss's **all-probes-F path** for the sets its leaf is in; a boss whose
  run tree has no identity atom also gets the same result from every triple. D\* = `if(P_1^¼:S, pay(½), if(P_1^0:S,
  pay(¼), pay(0)))`: the 0 path, so ≤¼ is written and ≥¼, =½ are NONE. A constant pay(½): ≥¼ and =½ (its ≤¼ NONE).
  B_eq = `if(N1, pay(½,none), pay(0,none))`: =½ and ≥¼ on triples with w1 = ⌜T₁⌝ (probability ≈ the island's T₁ share
  of slot 1, mass 3.19·10⁻³ per founder), else ≤¼; with 10 triples it may hold both paths' scripts for disjoint sets.
  A boss reading only W-probes ("pay ½ unless w_j would work for less", e.g. `if(P_1^0:W, pay(0), pay(½))`) takes its ½
  branch at the snapshot (the probe is F) and is certified =½.

**The founding pass is, for almost every founder, its first natural encounter executed before time starts against
partners that have not yet produced.** In the natural run a founder's first encounter comes ≈ 1/N = 0.01 generation in
(exponential), against partners of whom some have already had an encounter; so L1 differs from natural founding by about
one encounter per founder, by the partners' state at that encounter (path dependence under the lack rule: a D\* whose
first encounter is with a [D]-certified militant writes ≥¼ on its ½ path in the natural run, while under L1 it holds ≤¼
from the 0 path first and writes ≥¼ on whichever path it meets next), and by identity-reading bosses' extra triples.

### 1.2 The gate-and-production trace for the isolated coalition (D\*, T₁, T₁) with L1 lists (RE 6 revised)

One island, every boss D\*, every worker T₁ (one spelling in both worker slots), no migration.
1. *Founding pass.* A T₁ founder's non-self triples need a slot-2 founder whose spelling differs from T₁: there is none,
   so T₁ gets no triple and starts empty (in the parent's terms, the gate refuses every T₁ production). A D\* founder's
   10 triples are (D\*, T₁∅, T₁∅): P_1^¼:S is the check "T₁∅ certified to strike at ¼", F (no script); P_1^0:S, F; play
   pay(0). Attempts: ≥¼ NONE (pay(0) ∉ ≥¼), =½ NONE, ≤¼ found (RunNeg, RunNeg, Ax). After the first triple D\* holds
   ≤¼ and the other 9 triples retry ≥¼ and =½, NONE.
2. *Generation 0.* (D\*{≤¼}, T₁∅, T₁∅): probes F, D\* pays 0; T₁'s B½ check is F (D\* holds no =½ script; it is also not
   paying ½), both strike: play (0; S, S).
3. *Thereafter.* Every T₁ production is refused (the other worker is always a copy); D\* retries ≥¼ and =½ on its 0 path
   (NONE) forever. No individual ever changes its list, the island is quiet at once, and (0; S, S) is absorbing.

**Hand prediction:** 0/40 fair, every replicate at (0; S, S) from generation 0; the trajectory of spelling counts is
the parent's empty assay's exactly (the plays are identical at every composition, and the Moran stream does not depend
on encounters). The isolated assay with L1 lists is the parent's empty assay after one encounter.

### 1.3 The expected generation-0 yield

A **naturally founded coalition** is a founder triple (b, x, y), x and y of different spellings, whose play with full
H lists is fair, (½; W, W), with no constant boss earning the boss more than 1 (P§1.5). It is **certified at generation
0** if its play with the generation-0 lists at the cell's K is fair.
- *Natural founding (empty lists):* every worker in a coalition that strikes against pay(0) reads a certification atom
  (a constant worker cannot punish pay(0); a worker reading `EQ` alone is not distinct-spelling), and with empty lists
  every certification atom is F. A militant's B½ is F, so it strikes. **Yield 0** for coalitions with a militant.
- *L1:* militants hold [D] only. At generation 0 the probes about a [D]-certified militant are T where its [D] script is
  valid at the probe root (for T₁, at every probe root), so **a boss that conditions on an S-probe of a militant leaves
  its all-probes-F path at generation 0**, and its =½ script (if any) was not written on the path it now takes: it pays
  ½ uncertified, the militants' B½ checks are F, they strike. A coalition is certified at generation 0 iff its boss
  pays ½ on the path it takes at generation 0 and that path is its founding path (or it reached that path on one of its
  10 identity-varied triples): bosses that pay ½ on the all-F path and read no S-probe of a [D]-holder on the way (W-probe
  readers, ½-constants, identity readers on matching triples). D\*-type concessions (pay ½ to those who would strike for
  less) are never certified at generation 0 under L1. *Hand guess:* yield 0.2–0.5 of coalition mass; computed by code in
  §1.x on the founders of the paired seeds.
- *H (the maximal founding list, §1.0 item 6):* yield 1 by definition.

So L1 makes part of the coalition mass fair at generation 0 and leaves the probe concessions, the coalitions that read
militancy, one encounter short, as natural founding does.

### 1.4 The timescale argument: why legibility at founding should not move persistence (my reading, before any cell)

- **Production is fast against selection.** Per island and generation there are 3N = 300 birth–death events and
  N² = 10⁴ encounters, so each individual takes part in ≈ 100 encounters per lifetime (≈ one generation). A founder's
  first encounter, which writes what the founding pass writes (§1.1), comes ≈ 0.01 generation in; the probe-concession
  bootstrap (militant writes [D] → boss meets a [D]-holder and writes =½ → militants work) takes two or three
  encounters per individual, ≈ 0.03 generation. In that time about 3% of each slot is replaced, with fitness
  exp(w·payoff), w = 0.3, payoffs ≤ 1. The founding pass removes this window and nothing else.
- **The collapse of the fair share is slower than that window and happens at full legibility too.** In the stored
  cells the fair-island share falls from 0.29 at generation 0 to 0.06 at 10, 0.03 at 20 and 0.02 at 50 (S_eq; S_eq_ideal
  the same), while zero wage rises 0.34 → 0.69 → 0.81 → 0.90. Under H, where every founder holds its full list at
  generation 0, the same collapse happens: H_eq 0.30 → 0.06 → 0.03 → 0.04; H_noeq_ideal 0.30 → 0.09 → 0.05 → 0.08. The
  scramble is a ~10-generation process that full founding legibility does not prevent.
- **What separates H from S₃ is regrowth, not founding.** H_noeq_ideal recovers from 0.05 at generation 20 to 0.11 at
  100, 0.15 at 200 and 0.50 at 2,000 (H_noeq_K3e6 to 0.65); S_eq_ideal stays at 0.01–0.02 throughout. The fair network
  spreads between islands under free full lists and does not under endogenous production, even on the ideal table.
  Founding lists act before the regrowth phase and are swamped by production long before it.
- **The forced cells already separate legibility from numbers.** With 20 coalition founders per slot per island the
  parent found 0.70 from empty lists and 0.60 preloaded (paired Δ −0.105): legibility at founding did not help a
  coalition seeded in numbers.

**My reading:** L1 moves persistence by less than the run-level noise at every K, and the bind is not legibility at
founding but the S₃ regrowth deficit (what full H lists provide that endogenous production does not: scripts on paths
never travelled, more than one path per set, `EQ`-true scripts, the gate on copies), together with the coalition's
mass. The H + eq ideal diagnostic (§1.0 item 6) is the maximal founding list on the same seeds; I expect it near the
H + no eq ideal value (0.50; identity moved H by ≤ 0.1 at 10⁶), which would put the whole Nᵢ − H gap on what production
cannot reach after founding, since founding lists of L1's kind (the travelled path only) add nothing production does
not add within a generation.

### 1.5 Hand predictions (carried to the predictions file)

- L1 vs natural, paired, at 10⁶, 3·10⁶ and ideal: |Δ persistence| ≤ 0.05 in each; L1₆ ≤ 0.1, L1ᵢ ≤ 0.1, L3 ≤ 0.15.
- N₃ ≤ 0.15 (S₃ at the ideal is 0/20, so fuel is not S₃'s bind).
- Unconditional workers' share at generation 50: L1 minus natural within ±0.05 in every K.
- L1W₃ within 0.05 of L3.
- The isolated assay with L1 lists: 0/40 (§1.2).
- Generation-0 yield under L1: 0.2–0.5 of coalition mass; natural 0.
- L2 (safe key): the bare-source test fails; the replay finds suppressed successes (> 0); mark-sensitive encounters
  are rare (bosses only, ≤ 10⁻³ of executed encounters at 10⁶, 0 at the ideal); L2 persistence within 0.02 of S₃ on the
  pilot (bit-identical where no mark-sensitive encounter occurs); the mark brings the executed-encounter median cost
  to ≤ 1.5× play.
- H + eq ideal ≥ 0.3.

### 1.x Code, validation, the L2 pilot and its decision (after the code, before any counted cell)

Code: `src/founding_legibility.py` (the founding pass, `FLRun`, the withheld delivery, the statistics),
`src/founding_legibility_kern.py` (the mark kernel: the parent's kernel source with `prod_boss`, `prod_worker`,
`productions` replaced and one clock line added in `run_kernel`, generated into a cache file outside the repository),
`src/founding_legibility_run.py` (driver: lottery, compare, static, replay, assay), `src/founding_legibility_report.py`,
`tests/test_founding_legibility.py` (9 tests passing and one strict xfail).

**Tests.** The founding pass never draws a copy as a worker founder's co-worker, its partners are empty founders, and
its result equals the Python evaluator's `productions` on 300 sampled triples; the founding lists enter the run exactly;
the (D\*, T₁, T₁) trace of §1.2 (every T₁ founder without a triple, D\* with ≤¼ only); **"production reads sources
only" fails as §1.0 item 4 predicted** (strict xfail: T₁ holding [D] beside the scab gets NONE for [C] against an empty
D\* and a script against the same D\* source holding its =½ script); the mark kernel in mode 0 reproduces the parent's
kernel exactly (snapshots and every counter except ctr[14], which counts quiet checks including retries after table
misses and so depends on table history); every recorded mark is an attempt whose production row has no script; the
withheld surgery keeps the incremental fitness equal to a full recomputation (error < 10⁻⁶) and only adds scripts to
lacking sets; natural founding through `make_run` reproduces a plain parent `Run`.

**Bit-identical reproduction (5 of 5).** Replicates 0–4 of the parent's `S_eq` rerun through this run's driver
(`N6`) are identical to the stored runs in every summary field at 2,000 and at 10,000 (fair masks, plays, holders,
exits, sampled encounters, all counters except ctr[14]); persistence 0, 0, 0, 0, 0.172 as stored.

**The L2 pilot (replicates 0–4, safe key, mark active).** Every run's dynamics are identical to the stored `S_eq` run:
fair masks, wage trajectories, holders, exits and sampled encounters agree in every field; the only differences are
the production counters (attempts, NONE results, cap timeouts and steps charged), which the mark is meant to change.
**Mark-sensitive productions: 0 in 5 runs**, and the Lemma M bound (every completed NONE skipped) is also 0 in
3.4·10⁷ examined productions, so on these seeds the safe mark is a pure cost fix. It records ≈ 81,000 marks per run,
skips ≈ 7.2·10⁶ attempts per run (≈ 3.7·10¹¹ steps) and cuts the charged production steps of executed encounters
≈ 8–13×; what remains is cap timeouts (not cached by design: 6.5·10⁴ boss and 6.6·10⁴ worker cap timeouts per run, each
charging P). Cost, median (play + production) / median play: on the kernel's stride sample of executed encounters
2.18 without the mark and 1.015 with it (means 1.74 and 1.07); on population-sampled encounters (generations 0, 50, 200,
2,000) 3.1–4.5 for S₃ and 1.25–2.3 at the mark's steady state, 1.0 after generation 50. **Decision:** the pilot matches
S₃ + eq, so by the amendment L2 would become the base of the 3·10⁶ cells for speed; it saves no wall time here
(L2 runs took 12–13 minutes, as S₃'s), so as fixed in §1.0 item 4 it is not made the base, the pilot stands as the L2
cell, and L1 + L2 is not run (first in the drop order, and by Lemma M with 0 sensitive productions it would equal L1 up
to counters).

**Deviation found in the code:** none of the definitions of §1.0 changed. The bare-source replay was first written to
look for later partners on the producer's own island only and found 6 replays in a whole run; it now searches the later
checks of every island for partners of the same spellings with other lists (still with the producer's own type
unchanged), before any number from it is used.

## 2. Costs

### 2.1 Projection (before any counted cell)

Measured on the validation batch with 3 workers (and sibling runs on the machine): a natural S₃ + eq run at (100, 64)
takes 13.0–13.6 minutes including the 10,000 extension and this run's statistics (setup 2.6–3.0, run 8.8–9.0, summary
0.7, extension 1.0); an L1 run adds the founding pass (≈ 1.5–2 minutes, single process, from the static run); an H run
≈ 4 minutes; (200, 64) ≈ 90 minutes (the parent). At 3 workers ≈ 13 runs per hour at (100, 64).

| cell | runs | hours on 3 workers |
|---|---|---|
| Nᵢ (rerun of the stored 20, for the composition statistics) | 20 | 1.6 |
| L1ᵢ (paired with the stored 20) | 20 | 1.7 |
| H + eq ideal (diagnostic) | 20 | 0.5 |
| N₃ | 40 | 3.1 |
| L3 = L1₃ | 40 | 3.3 |
| L1₆ (paired with the stored `S_eq` replicates 0–19) | 20 | 1.7 |
| L1W₃ (paired with L3 replicates 0–19) | 20 | 1.7 |
| static, replay, the isolated assay | – | 0.5 (1–2 processes) |
| **subtotal** | | **≈ 14.1** |
| L1 + L2 (40) | dropped first | (3.3) |
| N panel, L1₃ at (200, 64) (12) | dropped second | (6.0) |
| L1-sham₃ (20) | dropped third | (1.7) |

The projection exceeds ~12 hours before any drop, so the spec's drop order is applied in full: **L1 + L2, the N panel
and the sham cell are not run** (RE 4 and RE 5 and S14 are unscored). Run counts were already cut to 20 for L1₆, L1ᵢ,
Nᵢ and the withheld cell to keep the remaining design near 12–14 hours; the 40-run cells are the 3·10⁶ pair, where the
reviewers expected the effect. If the cells finish early the sham cell is run next (20 runs), labelled.

### 1.y Static numbers (computed after the code; written while the first counted cells ran, before any was read)

`runs/founding_legibility/static_yield_K1e+06.json`, `runs/founding_legibility/replay.json`; disclosed: the H + eq
ideal cell and plan B were launched before this section was written (the static computation is not an input to
them), and nothing from them is used here.

- **The founding pass** (founders of replicates 0–4, K = 10⁶): every founder ends with a script (coverage 1.0 in every
  slot); bosses hold ≥¼ / =½ / ≤¼ in 0.67 / 0.35 / 0.66 of founders, workers [C] / [D] in 0.58 / 0.59. Per run: ≈ 96,000
  boss attempts (10,700 found) and 121,000 worker attempts (15,000 found), no cap or fuel timeout; **no worker founder
  acquires anything after its first triple** (S13's second clause holds: 0 in 5 runs); median production steps per
  founder 3.0·10⁵ (bosses) and 2.3·10⁵ (workers), maximum 6.5·10⁵ (< K); ≈ 150 s per run on one core.
- **Generation-0 yield** (1,092 naturally founded coalitions among 64,000 sampled founder triples): fair at generation 0
  under natural founding **0.33** (not 0, as §1.3 claimed: a third of coalitions have members whose all-F path already
  plays the fair action, e.g. bosses paying ½ unless a W-probe holds and workers working unless B≤¼ is certified), under
  L1 **0.59**; among coalitions whose boss reads an S-probe (0.59 of them) 0.52, others 0.70. §1.3's claim that no
  S-probe concession is certified at generation 0 under L1 is wrong at the level of "any S-probe reader" (many such
  bosses take their ½ branch on a probe that stays F at generation 0).
- **The bare-source replay** (natural runs of replicates 0 and 1 to generation 200): 5,667 bare-source NONE keys
  recorded, 269 replayable at later checks against partners of the same spellings with other lists, **27 of 320 replays
  are successes** (23 keys): mostly bosses whose =½ (set 1) or ≤¼ (set 2) path opens once a worker partner of the same
  spelling holds a certificate, and two worker cases. A bare-source mark would have suppressed them; the safe key is
  what was run (§1.0 item 4).
