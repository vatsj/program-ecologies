# Coverage components: which part of the full certificate lists carries the fair wage's regrowth? (notes, 2026-10-15)

Spec `specs/2026-10-15-coverage-components.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict). Parents: RESULTS "The social organization game, fully
realizable" (`notes/sog-fully-realizable.md`, cited P§) and "Legibility at founding" (`notes/founding-legibility.md`,
cited FL§). Machinery imported unchanged: `src/sog_full*.py`, `src/founding_legibility*.py`. §1 is written by hand
before any code of this run and before any counted cell; §1.x (code, validation, static numbers) is appended after the
code and before any counted cell; §2 (costs) holds the projection before the cells and the realized costs after them.

*Disclosure.* Before writing this section I ran five scratch computations in the scratchpad (outside the repository),
none of them a simulation: (i) the classification of every H-list script of every run tree of the eq grammar (602
worker and 177,318 boss run trees) by the parent's symbolic functions (`h_list`, `sym_produce`, `sym_prod3`,
`sym_check`), defined as in §1.0 below; (ii) its shares under the length prior and over the founders of replicates
0–19 and 20–59; (iii) the classification of the named programs; (iv) the probe-reachability of worker scripts; (v) the
overlap of count-matched random masks with each component under two stratifications. I also read the stored per-run
summaries and times of `runs/founding_legibility/cell_{Heq_i,Ni,L1_i}` (persistence per run and wall times). Their
content is quoted in §1.0–§1.3; the code of this run recomputes all of it and the numbers are re-reported in §1.x.

## 1. Design

### 1.0 Readings of the amended spec, fixed before any code

1. **Base.** The parent's S-nonself₃ + eq lottery on the ideal table (K = 10¹², so V = P = 2.5·10¹¹ and no check,
   play or production ever times out): K₃′, c = 0.5, `eq` in both roles, PROD3 after the play, cap P = K/4, the lack
   rule, vertical inheritance, the worker gate. (N, I) = (100, 64), mN = 1, w = 0.3, r = N/3 encounters per Moran
   event, horizon 2,000, every run extended to 10,000 (the primary endpoint; 2,000 intermediate). Replicate r uses the
   parent's founder stream r (`default_rng([r, 100, 64, 20261013])`) and kernel seed, so every cell is paired with
   the stored `Ni` (S₃ + eq ideal, 0/20) and `Heq_i` (H + eq ideal, 0.302 at 2,000, 0.300 at 10,000) replicate by
   replicate. **The invariant-key mark** (FL§1.0 item 4, Lemma M; the safe key, mode 1) is on in every cell with
   production. At K = 10¹² no attempt is ever starved, so by Lemma M the mark changes only the production counters.
2. **The static objects** (per role, per run tree t, per outcome set A of the role's family):
   - **H(t, A)**, the parent's H list (the path tactic over every assignment of the run tree's atoms, identity atoms
     included; P§1.1.4), in its order.
   - **S₃^static(t, A)**: the set of scripts PROD3 returns for (t, A) over every assignment of truth values to the
     run tree's box atoms and every identity assignment a producing root can have. Workers: `EQ` = F (the gate refuses
     every root where the other worker is a copy, and `EQ` reads exactly that). Bosses: every identity triple
     (N1, N2, EQW) except the three impossible ones (N1 ∧ N2 ∧ ¬EQW, and EQW with exactly one of N1, N2). A timeout
     reads as F in PROD3 (P§1.1.5), so {T, F} covers TO. This is the amendment's "every script S-nonself₃ can ever
     produce for a program on any encounter path", taken path-free: every box value is reachable at some actual root
     of the catalogue (every probe root's boss view is a natural view of a constant boss).
   - **S-opp^static(t, A)** (workers): the same with `EQ` free, i.e. what PROD3 writes when the gate is lifted.
   - **canon(t, A)**: PROD3 at the *default root*, every box F and every identity atom F (uncertified partners, a
     non-copy co-worker, a boss whose workers are not ⌜T₁⌝ and not one source). It is the script the founding pass
     writes (FL§1.1, "the all-F path") and the one a lineage writes first when its first encounter for A is against
     uncertified partners; NONE when the default root's path ends outside A. canon(t, A) ∈ S₃^static(t, A) always.
3. **The amendment's text is inconsistent; the reading.** The amendment asks for (a)–(d) to be a static partition of
   H \ S₃^static, and defines (b) as "scripts beyond the canonical first one per lack-set". With S₃^static as it is
   defined there (everything S₃ can ever write), every second script that the lack rule blocks lies *inside*
   S₃^static, so (b) would hold only the scripts PROD3 never writes on any path (the Hyp-first tactic's shadowed
   F-branch alternatives), contradicting its own wording; and (a) in its amended wording ("check-sets queried only on
   paths the program's own encounters never reach") is empty statically, because every probe root's values occur at
   some natural root (scratch (iv)). **Reading:** the components partition **H \ canon**, the scripts beyond S₃'s
   canonical first one; membership of S₃^static is reported as a joint-class dimension of every component (so the
   literal reading's H \ S₃^static is the "non-producible" part of each component); and the amended test holds as
   stated: S₃^static ∪ (a) ∪ (b) ∪ (c) ∪ (d) = H for every program (since canon ⊆ S₃^static and canon ∪ (a)–(d) = H).
   The RE's original question (spec "Why") separates a production-rule fix from a provenance-rule fix; under this
   reading (a) and (b) are what a production rule could supply and (c) and (d) what a provenance rule could.
4. **The components** (properties of (run tree, set, script) triples; priority (d) > (c) > {(a), (b)}; (a) and (b)
   are disjoint by construction):
   - **(d) gate copies:** s ∉ S₃^static(t, A) and s ∈ S-opp^static(t, A): written only at roots where the other
     worker is a copy, which the gate forbids (workers only; bosses are never gated, so (d) is empty for bosses).
   - **(c) identity-true:** s ∉ S₃^static(t, A), not in (d), and every assignment that generates s in the H
     enumeration sets an identity atom true: an identity-true script that even the ungated tactic never writes
     (workers: shadowed alternatives on `EQ`-true paths; bosses: scripts only on impossible identity triples, which
     are valid at no root).
   - **(a) untravelled:** canon(t, A) = NONE and s not in (c), (d): every script of a set the default root does not
     cover; the program can hold one only after its encounters take it down a non-default path (or never, if s is a
     shadowed alternative).
   - **(b) second paths:** canon(t, A) exists, s ≠ canon(t, A), s not in (c), (d): every further script of a set the
     default root already covers, which the lack rule (or the tactic's Hyp-first order) keeps out of an S₃ list once
     the canonical one is written.
   - **canon** is the remainder: S₃'s first script. It is never a component, it is granted only in the full and
     minus cells, and S₃ writes it at a program's first default encounter.
   Further flags reported with every class (joint classes): S₃^static membership; S-opp^static membership;
   identity-true (as above); **live** (some generating assignment is feasible: workers not certified both =½ and
   ≤¼ by the boss and the other worker not certified both to strike and to work; bosses not certified-strike and
   certified-work of one worker at one probe wage, no N_j with a W-probe of slot j true, a possible identity triple);
   **probe-reachable** (workers: valid at some probe root, i.e. under the boss view of ⌜pay(0)⌝ or ⌜pay(¼)⌝ with some
   values of the other atoms).
5. **What a mask does (amendment 2).** A mask gives, for each run tree t and set A, a *granted* set G(t, A) ⊆ H(t, A)
   and a *barred* set X(t, A). Every individual (founders, and so newborns and migrants by inheritance, since lists
   only grow) holds G of its own run tree from generation 0. Production is S-nonself₃ with its gate, cap, cost model
   and retry rule unchanged, and **production runs on top of the grant**:
   - **Lack rule (the reading):** a program attempts set A iff it holds no script for A outside G(t, A), i.e. iff it
     has not yet *produced* a script for A. Granted scripts never suppress production. (The literal alternative, in
     which a granted script counts as held, would make a plus cell remove S₃'s own production wherever it grants a
     script, so "plus X" would not be S₃ plus X; with this reading the plus cells are exactly S₃ with X added.)
   - **Outcomes:** a script PROD3 returns is appended if it is neither held nor barred; if it is already held (it is a
     granted script) nothing changes and the set stays lacking (logged as a *reacquisition*); if it is barred nothing
     is written (logged as *barred*); NONE as before. For the kernel, reacquisitions and barred outcomes are NONE (the
     inventory does not change); they are deterministic in the mark's key, so the mark stays safe.
   - **Logging** (amendment 2): grants (per run, the granted scripts by component), endogenous production (found),
     reacquisitions, barred outcomes, and *grant-covered attempts* (attempts at a set for which a granted script is
     held: exactly the attempts the literal lack rule would have suppressed) are reported separately, from the
     kernel's counters and from population-sampled encounters at generations 0, 50, 200, 2,000. **Copying:** this game
     has no horizontal copying (inheritance is vertical; P§1.2), so the copying count is 0 by construction.
6. **Cells (amendments 1–3).**
   - **H-full** = full mask (G = H, X = ∅): = H + eq ideal. **S₃** = empty mask: = S₃ + eq ideal.
   - **minus X** for X ∈ {a, b, c, d}: G = H \ X, barred X.
   - **plus X**: G = X, barred ∅. **Pairs:** plus (a)+(b) (the production-rule pair), plus (c)+(d) (the
     provenance-rule pair).
   - **Count-matched random controls**, one per singleton cell (read below).
   - **Lemma P (minus cells are pure grants).** In a minus cell production can return only scripts of S₃^static
     (PROD3's range), every one of which is either granted (S₃^static \ X ⊆ H \ X = G) or barred (in X). So no
     production ever changes an inventory, and the dynamics are those of the grant alone. The kernel's Moran stream
     is counter-based on the event index (P§1.13; `u01(seed, step, k)`), and encounters on islands where nothing can
     change only draw from their own stream; so a minus cell (and the full cell) run with production off (the
     parent's H mode, founders holding G) is the same process draw for draw as with production on. **Minus and full
     cells run in H mode**; a test checks the equality on small runs and on one full-size replicate.
7. **Random controls (amendment 3), a stated deviation in the stratum.** The amendment asks for count-matched random
   grants and removals stratified by host program *and check set*. Scratch (v): under that stratification a random
   draw from a stratum's non-canonical scripts is the component itself with probability 0.97–1.00 for (a) and (b)
   (the two are separated by the set's default coverage, so a stratum's pool is one of them plus a little (c), (d)),
   and 0.88 for (d); the "control" would replicate the cell. Stratifying by host program alone gives 0.64–0.90. I
   therefore draw the control from the **complement**: for each host run tree t with k = |X(t)| > 0 component scripts
   (all sets), k scripts drawn uniformly without replacement from its non-canonical scripts *not in X* (all of them if
   fewer; the shortfall is reported). The control matches the component's volume program by program with disjoint
   content: **rand-plus X** grants that draw (barred ∅); **rand-minus X** removes and bars it (G = H minus the draw).
   One draw per cell (seed fixed per cell), shared by its 20 replicates. Expected achieved volume (by hand from the
   per-program volumes of §1.2): near 1 of X's for (a) and (d); at most about 0.6 for (b) in both roles, whose
   complement pool is smaller than (b) itself. Computed exactly by code in §1.x.
8. **Statistics (fixed in advance).** Everything the parent's `summarize` computes (persistence, wage shares,
   productive efficiency separately from fairness, holders, exits, sampled encounters), at 2,000 and at 10,000, plus:
   - **Estimands (amendment 6):** the fair-island share and the number of runs with any fair island, reported
     separately, at 10,000 (primary) and 2,000; zero-wage and ¼-wage shares.
   - **Trajectory:** fair share at generations 0, 10, 20, 200, 2,000, 10,000. *Deviation:* the spec's generation 5 is
     not a check (checks are every 10 generations, and the statistics index checks by generation / 10); generation
     10 stands in for it.
   - **Regrowth.** A run *regrows* if its fair share at 10,000 is ≥ ½ and its minimum fair share over generations
     20–200 is ≤ 0.1. In a regrowing run, an island's *regrowth check* is the first check of its final uninterrupted
     fair spell (ending at the endpoint) if that check is ≥ 20; the run's *nucleus* is the island with the earliest
     regrowth check (ties by island index), and its *first fair encounter* is the nucleus's modal triple at that check.
     Reported per regrowing run: the nucleus's modal triple (spellings, run trees, holder class, and its members'
     inventories by component and by provenance, granted or produced) and the generation of regrowth.
   - **Pivotal granted scripts.** At a first fair encounter, a held script s of member m is *pivotal* if removing s
     from the lists of every member of the triple that shares m's run tree changes the encounter's play away from fair
     (probes and nested checks read the same members, so this is the script's whole effect at that encounter). Reported
     by component and by provenance.
   - **Timing log (amendment 4).** For every pivotal *granted* script s (member m, set A): whether S₃ would have written
     it there, i.e. whether PROD3 for m and A at that encounter, with m's lists for A emptied, returns s
     (*pre-populated, here*); else whether it does at the same triple after every member has applied its productions
     of this encounter (*pre-populated, next*); else *never written there*; with its S₃^static membership beside it.
   - **Mediation replays (amendment 4).** For up to five regrowing runs per rescuing cell (a plus, pair or random cell
     with fair share ≥ 0.2 at 10,000), the run is replayed with every pivotal granted script of its nucleus removed
     from the grant (production unchanged, so S₃ may still write it). By determinism (the counter-based Moran stream
     and the deterministic production rows) the replay coincides with the original run until the first moment a
     withheld script would have changed a value, so "withheld from the start" is "withheld just before its first
     use". Reported: the replay's fair share at 2,000 and 10,000 and whether it still regrows.
   - **Held scripts at the horizon** (2,000 and 10,000): per role, the share of individuals holding at least one
     script of each class (canon, (a)–(d)), split into granted and produced.
   - **Paired contrasts** by replicate against H-full and against S₃: mean difference in fair share with a bootstrap
     interval over runs (2,000 resamples), runs with any fair island compared by the exact McNemar p, Wilson
     intervals on run counts. A contrast whose interval spans both zero and the predicted effect is *inconclusive*.
     Observed-threshold verdicts (a number crossing a predicted bound) are kept apart from statistical evidence; 0/20
     runs still allows a per-run success probability up to 0.16 (Wilson upper bound).
9. **Random streams (amendment 6).** The kernel's Moran stream is event-keyed (a hash of seed, event index and draw
   slot), so altered production does not shift demographic randomness except through the state. The encounter
   stream is keyed on the executed-encounter counter, and which encounters execute depends on which islands are
   quiet, so production differences do shift it; disclosed, not changed.
10. **Confirmation and pruning.** Any plus, pair or random cell reaching fair share ≥ 0.2 at 10,000 is to be
    confirmed on 40 fresh founder streams (replicates 20–59) beside H-full on the same streams. The order of cells is
    fixed now (§2.1) and the tail is dropped by cost only: first the 40-run confirmations, then rand-(c) (whose
    volume is 0.02 scripts per worker program and 0.008 per boss, all dead for bosses, so the control is null by
    construction), then mediation replays beyond two per cell.

### 1.1 The classification by hand on named programs

Notation: per set, the H list in order, each script labelled (canon / a / b / c / d), ✱ = not in S₃^static.

| program | run tree | [C] or ≥¼ | [D] or =½ | ≤¼ |
|---|---|---|---|---|
| scab, striker | constant | canon / – | – / canon | |
| T₁ (and T₁′, T₀) | B½ ? W : S | a (Run on B½) | canon (RunNeg on B½) | |
| R | B≤¼ ? S : W | canon | a | |
| Q, Qw | O:S ? S : W | canon (RunNeg) | canon (Hyp) | |
| U | B½ ? W : (O:S ? S : W) | b (Run on B½), canon (RunNeg, RunNeg) | canon (Hyp) | |
| U_eq | EQ ? (B½ ? W : S) : W | d✱ (`EQ`-true Run), canon | d✱ (`EQ`-true RunNeg) | |
| XM | B½ ? (EQ ? W : S) : S | d✱ | b (B½ T, `EQ` F), canon (RunNeg) | |
| D\* | P₁^¼:S ? ½ : (P₁⁰:S ? ¼ : 0) | a (½ path), a (¼ path) | a (½ path) | b (¼ path), canon (0 path) |
| D₀, D14, WF, B_eq, B_id | probe or identity ? ½ : 0 | a | a | canon |
| constant pay(w) | – | canon if w ≥ ¼ | canon if w = ½ | canon if w ≤ ¼ |

So the fair coalition F\* = (D\*, T₁, T₁) under H uses canon (T₁'s strike script, read by D\*'s probe) and (a) (D\*'s
=½ script, read by T₁; D\*'s ≥¼ ½-path script). Under S₃ D\* writes its (a) scripts the first time it meets a
strike-certified militant at its ½ path (P§1.3.2), and T₁ never needs its (a) [C] script against D\* (it works on the
boss's certificate). (b) is where the lack rule bites: a U-type worker whose canonical [C] script was written on the
default path (B½ F, other not certified to strike) holds no [C] script valid where the boss *is* certified =½, and a
D\*-type boss holds no ≤¼ script on its ¼ path. (d) is the greenbeard family's `EQ`-true scripts (Claim N₃).

### 1.2 Shares under the length prior (scratch (i)–(v); recomputed by code in §1.x)

Share of H-list scripts in each class, weighting run trees by their spellings' prior mass; "any" = the prior share of
programs holding at least one script of the class in their H list. The founders of replicates 0–19 give the same
numbers to ±0.001.

| role | scripts per program | canon | (a) | (b) | (c) | (d) |
|---|---|---|---|---|---|---|
| workers | 2.54 | 0.460 | 0.110 | 0.331 | 0.007 | 0.092 |
| workers, any | | 1.00 | 0.25 | 0.65 | 0.018 | 0.18 |
| bosses | 4.43 | 0.376 | 0.236 | 0.386 | 0.0018 | 0 |
| bosses, any | | 1.00 | 0.66 | 0.83 | 0.007 | 0 |

Joint classes (shares of all H scripts of the role):
- **Workers.** (a): 0.105 in S₃^static, 0.002 not, 0.003 dead. (b): 0.196 in S₃^static, **0.129 not** (the Hyp-first
  tactic's shadowed F-branch alternatives, valid where the other worker is *not* certified), 0.006 dead. (d): 0.089
  identity-true, 0.0025 not (written only at copy roots for another reason: backtracking differs when `EQ` is true).
  (c): 0.007, all identity-true, live, not in S-opp. canon: 0.451 live, 0.009 dead (a Hyp-first double hypothesis on
  "the other strikes" and "the other works", which S₃ writes first and which is valid nowhere).
- **Bosses.** Every boss script outside (c) is in S₃^static (bosses have no Hyp-able box and no gate). (a): 0.163
  identity-free and 0.066 identity-true (e.g. B_eq's ½ path, producible since bosses are not gated); (b): 0.300 and
  0.073; dead fractions ≤ 0.008 per class. (c) = the scripts only on impossible identity triples: valid at no root.
- **Probe-reachable** worker scripts: canon 0.80, (a) 0.61, (b) 0.71, (c) 1.0, (d) 0.86.

So (c) is a negligible volume in both roles (and inert for bosses), (d) is a worker-only class of about a tenth of
worker scripts, and (a) and (b) together hold 0.44 of worker and 0.62 of boss scripts. The literal reading's
H \ S₃^static is, for workers, (b)'s shadowed alternatives (0.13), (d) (0.09), (c) (0.007) and a sliver of (a); for
bosses only (c).

### 1.3 Hand predictions and the mechanisms behind them

- **What H-full is.** H-full is the stored `Heq_i` (6 of 20 runs fully fair, two more at 1/64; 0.302 at 2,000, 0.300
  at 10,000). The full mask must reproduce it draw for draw (Lemma P), and the empty mask must reproduce `Ni` (0/20).
- **(c) is null.** Its volume is 0.007 of worker scripts and its boss part is valid nowhere: minus (c) = H-full within
  run noise, plus (c) = S₃.
- **(d) is small.** The parent found that identity decided nothing (≤ 0.1 in every paired arm, no greenbeard union
  held an island). Removing the `EQ`-true scripts should move H-full by little, and granting them to S₃ should not
  start regrowth: plus (d) ≤ 0.05.
- **(b) is the likelier carrier.** The lack rule makes certification path-specific: a lineage holds one script per set,
  written on the path its first encounter took, so a worker certified to work on its default path (other not certified
  to strike, boss not certified =½) is *uncertified* exactly where a concession boss certifies =½, and a Hyp-script
  holder whose partner is illegible holds no RunNeg alternative (0.13 of worker scripts, never producible). Both are
  what a migrant lineage meets when it reaches an island that took a different path. H has every path; S₃ one.
- **(a) is pre-populated quickly where it matters.** The (a) scripts that F\*-type coalitions need (a probe
  concession's =½ and ≥¼ scripts) are written by S₃ at the first encounter with a strike-certified militant, about a
  hundredth of a generation in; a militant's [C] script is not read by its own coalition's boss. So granting (a) should
  help less than granting (b), and removing (a) (and barring it) should hurt, because it removes the concession's
  certificate entirely: the minus (a) cell keeps only coalitions whose boss pays ½ on its default path.
- **The pair.** plus (a)+(b) is S₃ plus 0.97 of H \ canon for bosses and 0.96 for workers minus (d), (c): it should be
  near H-full (≥ 0.2).
- **Collapse is grant-independent.** Every cell collapses to ≤ 0.1 by generation 20 (H-full included, FL§1.4); the
  cells differ in regrowth after it.
- **Costs.** Minus and full cells run as H (about 5 minutes per run including the 10,000 extension); plus, pair and
  random-plus cells as S₃ (13–20 minutes).

These are carried into the predictions file with falsifiers.

### 1.x Code, validation, deviations and static numbers (after the code, before any counted cell)

Code: `src/coverage_components.py` (classification, masks, `MaskEvaluator`, `MaskRun`, statistics, the cell job),
`src/coverage_components_run.py` (driver: static, coalitions, jobs, compare, mediate), `src/coverage_components_report.py`,
`tests/test_coverage_components.py` (15 tests, passing). The parents' modules are imported unchanged; `MaskRun`
subclasses `FLRun` (so the mark kernel of `founding_legibility_kern` runs wherever production does) and overrides
`founder_inv`, the lack bits and the production rows' new-class tables; `MaskEvaluator` overrides `prod_boss`,
`prod_worker`, `productions` and `produce`.

**Tests.** (1) The partition: on every worker run tree and every boss run tree of the founders of replicates 0–2,
canon ∪ (a)–(d) = H disjointly, canon ⊆ S₃^static, S₃^static ∪ (a)–(d) = H, no boss (d), every boss (c) dead, and the
workers' S₃^static equals the parent's `producible_inv`. (2) The named programs' labels are §1.1's table. (3) The
masks: plus X grants exactly X, minus X grants H \ X and bars X, the random controls are disjoint from X and never
canonical, full = `full_inv`, empty = `empty_inv`, the pairs grant the union; the controls' inclusion probabilities
equal their definition. (4) The lack rule under grants (D\* under plus (a) attempts every set; its ½-path results are
held, its default-path ≤¼ is found; under minus (b) its ¼-path ≤¼ is barred; `produce` takes the union). (5) Draw for
draw on small runs (I = 4, N = 30, 60 generations, replicates 0 and 1): the empty mask equals the parent's S₃ run
(compositions and every counter but ctr[14]) without the mark, and the founding-legibility mark run (compositions,
counters and the mark's counters) with it; the full mask equals the parent's H run in H mode and in S mode with the
mark on and off, no production ever finding a script; minus (a), minus (b) and rand-minus (b) are identical in H mode
and S mode (Lemma P); a plus (b) run keeps every grant at every check and adds at most one produced script per set.

**Full-scale validation (before any counted cell).** The empty mask with the mark on reproduces the stored S₃ + eq
ideal runs `Ni` on replicates 0–4 in every summary field except the production counters (fair masks, plays, holders,
exits, sampled encounters with their production outcomes and steps, the 10,000 extension); replicate 0 without the
mark reproduces them with every counter but ctr[14] equal. The full mask (H mode) reproduces the stored H + eq ideal
runs `Heq_i` replicate by replicate (`runs/coverage-components-validate.json`; 20/20 reported in §2.2).

**Deviations from §1.0, stated before any counted cell.**
1. **The random controls' stratum (replaces §1.0 item 7's per-program draw).** The per-program complement draw reaches
   only 0.21–0.56 of the components' volume (many programs that hold X hold little else that is non-canonical; T₁'s
   only non-canonical script is its (a) [C] script). The control used instead takes, in each run tree, k =
   ⌊q n⌋ + Bernoulli(q n − ⌊q n⌋) of its n non-canonical non-X scripts uniformly, with q = min(1, V_X / P_X) per role
   (V_X, P_X the mean numbers of X scripts and of non-canonical non-X scripts per founder of replicates 0–19): workers
   q = 0.256 (a), 1 (b), 0.013 (c), 0.203 (d); bosses 0.609 (a), 1 (b), 0.003 (c), 0 (d). It matches volume per role,
   not per program, has no overlap with X, and cannot match (b) (the complement of (b) is smaller than (b)). Achieved
   volume ratios over the founders of replicates 0–19 (rand-plus / rand-minus): (a) 0.97 / 0.84 workers, 1.00 / 1.00
   bosses; (b) 0.63 / 0.63 workers, 0.62 / 0.62 bosses; (c) about 1; (d) 0.96 / 0.92 workers. One draw per cell (seed
   fixed per cell).
2. **S₃'s reference.** Because the empty mask reproduces `Ni` draw for draw, the S₃ cell is the 5 rerun replicates
   (which carry this run's statistics) plus the stored `Ni` runs for replicates 5–19 (fair shares and wages only).
3. **The S-mode check of Lemma P at full scale** is minus (b) replicate 0 run in S mode with the mark, compared with the
   counted H-mode run of the same replicate when it exists (the small-run tests already establish the equality).
4. **Generation 5** is replaced by generation 10 in the trajectory (§1.0 item 8).

**Static numbers** (`runs/coverage-components-static.json`; recomputed by code, equal to §1.2's scratch values to the
fourth decimal). Script shares under the length prior, workers / bosses: canon 0.460 / 0.376, (a) 0.110 / 0.236, (b)
0.331 / 0.386, (c) 0.0069 / 0.0018, (d) 0.092 / 0; programs holding any: (a) 0.25 / 0.67, (b) 0.65 / 0.83, (c) 0.018 /
0.007, (d) 0.18 / 0. Joint classes as §1.2. Probe-reachable worker scripts: canon 0.80, (a) 0.61, (b) 0.71, (c) 1.0,
(d) 0.86. The founders of replicates 0–19 and 20–59 agree with the prior to ±0.001.

## 2. Costs

### 2.1 Projection (before any counted cell)

Measured on the validation batch with 3 workers and a machine load of 11–12 on 10 cores (the sibling scaling run and
other processes): an S-mode run (production on, the mark on) takes 16–17 minutes including the 10,000 extension and the
statistics (setup 3.5, run 10.5–11, summary 1, extension 1.2–1.5); an H-mode run 5–6 minutes (setup 3–3.7, run 0.2,
summary 1, extension 1–1.3); the S-mode minus (b) check 8.5 minutes. Plus, pair and rand-plus cells are assumed to cost
as S₃.

| block, in launch order | runs | hours on 3 workers |
|---|---|---|
| minus (a)–(d), H mode | 80 | 2.5 |
| plus (a)–(d) | 80 | 7.4 |
| plus (a)+(b), plus (c)+(d) | 40 | 3.7 |
| rand-minus (a), (b), (d), H mode | 60 | 1.8 |
| rand-plus (a), (b), (d) | 60 | 5.6 |
| **subtotal** | 320 | **≈ 21** |
| rand-minus (c), rand-plus (c) | 40 | 2.5 (second in the drop order) |
| mediation replays (≤ 5 per rescuing cell) | ≤ 25 | ≤ 2.5 (beyond two per cell: third) |
| confirmations, 40 fresh streams + H-full beside | 80 per candidate | 4.9 per candidate (first) |

The budget is about 30 hours of wall time from the first counted cell; blocks past it are dropped in the stated order
(confirmations, then rand-(c), then mediation beyond two replays per cell), by cost only. A static diagnostic,
`coalitions` (founding coalitions of replicates 0–2 kept fair under each variant of their lists), runs in one process
before the cells; its numbers are reported in §2.2 and used for nothing in the cells.
