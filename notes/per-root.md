# A per-root production rule for the fully realizable social organization game (notes, 2026-10-16)

Spec `specs/2026-10-16-per-root-production.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict). Parents: RESULTS "Coverage components"
(`notes/coverage-components.md`, cited CC§), "Legibility at founding" (`notes/founding-legibility.md`, FL§) and "The
social organization game, fully realizable" (`notes/sog-fully-realizable.md`, P§). Machinery imported unchanged:
`src/sog_full*.py`, `src/founding_legibility*.py`, `src/coverage_components*.py`. §1 is written by hand before any code
of this run and before any counted cell; §1.x (code, validation, static numbers, the realizability trace, fixed-trace
comparisons) is appended after the code and before any counted cell; §2 holds the cost projection before the cells and
the realized costs after them.

*Disclosure.* Before writing this section I ran one scratch computation in the scratchpad (outside the repository), not
a simulation: the alternative-writing tactic of §1.0 item 6, written symbolically beside the parent's `sym_prod3`, over
every box assignment (`EQ` = F) of every worker run tree of the eq grammar, compared with the parent's H lists and the
coverage run's classification (`coverage_components.classify`). Its content is quoted in §1.1. I also read the stored
per-run wall times of `runs/coverage_components/cell_*`, `runs/founding_legibility/cell_{Ni,N3,N6,Heq_i}` and their
kernel counters (executed encounters, table fills). The code of this run recomputes the static numbers (§1.x).

## 1. Design

### 1.0 Readings of the amended spec, fixed before any code

1. **Base.** The parent's S-nonself₃ + eq lottery: K₃′, c = 0.5, `eq` in both roles, production after the play in the
   residual fuel, cap P = K/4, vertical inheritance, founders empty, the worker gate (a worker never produces beside a
   copy of its own source). (N, I) = (100, 64), mN = 1, w = 0.3, r = N/3 encounters per Moran event, horizon 2,000
   with every run extended to 10,000 (the primary endpoint). Replicate r uses the parent's founder stream r
   (`default_rng([r, 100, 64, 20261013])`) and kernel seed, so every cell is paired replicate by replicate with the
   stored cells: development streams 0–19 (`runs/founding_legibility/cell_Ni`, S₃ + eq ideal, 0/20;
   `runs/coverage_components/cell_Hfull`, H + eq ideal, 0.300), confirmation streams 20–59
   (`runs/coverage_components/cell_Hfull` replicates 20–59, 0.299). Executed fuels K = 3·10⁶ and 10⁶ (V = P = K/4);
   the ideal table is K = 10¹² (nothing ever times out).
2. **The root.** A worker producing in slot j reads, at most, the executed values of the boss's three boxes (≥¼, =½,
   ≤¼; values T / F / TO), the co-worker's [C] and [D] boxes, and `EQ`; with the gate a producing worker always has
   `EQ` = F. Its *root* is the tuple (j, boss values, co-worker values, `EQ`): exactly the key of the parent's worker
   production row. A boss reads the executed probe values its run tree mentions and its identity bits (N1, N2, EQW):
   its root is the parent's boss production key (class-independent read positions, their values). Every quantity of
   this note that is "at the root" is a function of the program's run tree, its list and its root.
3. **Valid at the root.** A held script for set A is *valid at the root* iff the checker's root validation (`vone4`:
   `tryents3` over the list in list order, `cchk3` on each entry for A) accepts it with every nested box at its
   executed value at this encounter; Hyp nodes are accepted as hypotheses (the closure is not run), a nested TO reads as
   "not T" (RunNeg passes, Run fails), exactly the parent's `sym_check`. This is the condition under which PROD3's own
   output is certified at its root (PROD3 uses actual values for every non-Hyp-able box and Hyp-first for the
   co-worker's boxes), so a script PROD3 writes at a root is valid at that root. The closure is a joint property of the
   encounter's boxes, not of the program's list, and is left to the partners' checks.
   - **Realization and charge.** Validation is one `vone4` run by the program on its own box at the current root:
     own steps = the parent's per-entry node steps for every entry scanned plus the calibrated `vone` terms (the
     parent's `_vone` cost, without closure bookkeeping), plus every nested call it makes at that call's executed
     charge. It runs under the check cap V: if its total exceeds V + VPLUS (in particular whenever a nested call it
     makes timed out) it is a **validation timeout**, charged V + TO_CHARGE, and the set counts as lacking (the program
     cannot tell). Validation is charged at every encounter where the program may produce, for every set whose list is
     non-empty, in family order, before any production. A worker refused by the gate does neither.
4. **Order of operations (amendment 1).** At an encounter, after the play, for each participant (boss, then worker
   slot 1, then slot 2, as in the parent): (i) validation of every non-empty set at the root, in family order, in the
   residual fuel; a set is *lacking* iff its list is empty or no held script for it is valid at the root (or its
   validation timed out); (ii) the mark is consulted for each lacking set; (iii) PROD3 (or PROD3A, item 6) runs for
   each unmarked lacking set in family order in the remaining fuel, with cap P per attempt; (iv) what it returns is
   appended; (v) under a cap, eviction follows. If the fuel is exhausted in (i), nothing is attempted (a *validation
   fuel exhaustion*). Fuel exhaustion (validation or production, `fuelTO`) and cap timeouts (`capTO`, `valTO`) are
   recorded apart from completed attempts that return NONE (uncertified failure).
5. **The mark (amendment 1).** A completed attempt that returns NONE is recorded under the key **(role, spelling, set,
   root)**: everything production reads except the program's own list. PROD3's result is a deterministic function of
   the run tree, the set and the values it reads (the root), and the partners' lists enter only through those values,
   so a recorded NONE predicts NONE at the same key whatever the program's list (Lemma M of FL§1.0, with the key made
   list-free). Appending or evicting does not restart a failed attempt; a failure is retried only when its root changes
   (amendment 1). A found script, a timeout or an exhausted fuel are never recorded. **Retry bound:** at most one
   completed NONE per (spelling, set, root) per run; timeouts carry no bound (they are counted). *Population sharing,
   stated:* the mark is one table per run, shared by every individual of a spelling (as FL's type-keyed mark was), where
   a realizable program carries its own inherited cache. Because a recorded NONE is a NONE for every holder, sharing
   changes nothing at K = 10¹² (no attempt is starved; FL's Lemma M) and at executed fuel can only leave more fuel to
   later attempts of the same encounter (the mark-sensitive encounters, which the kernel counts). The mark is on in
   every cell with production, R0 included.
6. **The rules.**
   - **R0 = S₃** (reference): a set is lacking iff its list is empty; no validation; PROD3; at most one script per set.
   - **R1, per-root lack:** a set is lacking iff no held script for it is valid at the root (item 3); PROD3; the script
     returned is appended (a set may hold several).
   - **R2 = R1 + shadowed alternatives (workers):** production is **PROD3A**, PROD3 with one change: at the *first
     Hyp-first choice point of the derivation whose Hyp branch succeeds* (a co-worker box with no value yet, taken as
     true, the branch closing), the tactic also runs the F branch of that choice point (the box taken as false: RunNeg,
     then the false path), in the same attempt, without checking the box. If that branch closes, the script with the
     choice point's subtree replaced by it is the **alternative**; if it fails, the alternative is the one found
     (recursively, by the same rule) inside the Hyp subtree, if any. The primary is exactly PROD3's script. Bosses have
     no Hyp-able box, so for bosses R2 = R1. "First" is in the tactic's depth-first order: the F branch is run where
     the choice is made, and enclosing nodes combine (an enclosing ChkR takes its first subtree's alternative if there
     is one, else its second's). The alternative is valid where the co-worker is *not* certified for the box (its
     RunNeg), the primary (with its Hyp) where it is; this is the shadowed F-branch alternative of CC§1.2 (the (b)
     scripts S₃ can never write). **Cost:** the F branch's tactic steps at the calibrated per-event rates (the same
     visit-log model as PROD3, its events logged in the same attempt) plus every nested call it makes (boss boxes on
     the false path); it does not call the hypothesised box. The whole attempt is one PROD3A call under cap P.
   - **R0 + alternatives** (amendment 5, the factorial): R0's lack rule (attempt only empty sets), production PROD3A;
     so a set holds at most one *bundle*.
   - **R3 = R2 with a list cap of k bundles per set**, k ∈ {2, 3} (amendment 4). A *bundle* is what one attempt
     writes: the primary with its alternative, or the primary alone. When an append would exceed k bundles, one bundle
     is evicted. **LRU, implemented as CLOCK (second chance), a stated reading.** Exact recency order is state that
     changes at every validation, so on a stable island types would churn forever and no island would ever be quiet
     (the kernel would execute every encounter: N²I ≈ 6·10⁵ per generation); CLOCK is the standard bounded-state
     approximation. Each bundle carries a *use bit*, set when one of its scripts is the one that validates at the root
     in step (i) ("usage updated when a held script validates at the current root"); a new bundle enters with bit 0;
     on eviction the bundles are scanned oldest first, a bundle with bit 1 has it cleared and is passed over, the
     first with bit 0 is evicted (if every bit was 1, all are cleared and the oldest is evicted). Bits change only on
     0 → 1 by use and on eviction scans, so type changes between appends are bounded by k per set. **FIFO** (k = 2, one
     control cell): evict the oldest bundle, no bits.
7. **List order and checking (amendment 3).** Lists are checked in list order by the parent's checker (`tryents3`:
   the first entry valid at the root is used, then the closure). A produced bundle is **appended** at the end of its
   set's list; inside a bundle the **alternative precedes the primary**. *Why this order, stated:* a primary whose Hyp
   node passes root validation shadows every later entry for its set (the checker does not backtrack after a closure
   fails), so with the primary first the alternative would be dead exactly where it is meant to work (the co-worker
   not certified); with it first, the alternative's RunNeg fails where the co-worker is certified and the checker moves
   on to the primary. H lists (CC, H-full) are ordered by the number of Hyp nodes, which also puts these alternatives
   first; across bundles this run keeps acquisition order, so an older primary can still shadow a newer alternative
   (counted in the fixed traces). **Root-keyed dispatch** (a variant at 3·10⁶ only): the checker jumps to the entry
   written at the current root when there is one. Under R1–R3 that entry is the first valid entry in list order (at its
   own production root every earlier entry failed validation, and validity at a fixed root does not change), so
   dispatch changes no value, only the cost: the scan is charged as the selected entry alone plus a lookup, and as the
   linear scan when no entry is keyed to the root. It is implemented as a cost-model variant of the checker and the
   validation step (both the evaluator's and the kernel's validation tables) and runs only for R2.
8. **What the kernel needs.** The parent's tables are keyed by class (run tree, list, T₁ flag) and root, so every
   quantity of items 3–7 is a row of a production table: per set, the validation flag at the root (empty / valid /
   invalid), its own steps and call mask, the attempt's primary and alternative and its cost; the new class is a
   function of the per-set outcome (nothing, used, produced). A class's *lackable* bits (the parent's `BLACK` / `WLACK`,
   which let quiet islands skip encounters exactly) are, under R1–R3, the sets for which some root makes every held
   script invalid (computed by enumerating the run tree's box values); under R0 the empty sets, as the parent. Under R3
   the class also carries the bundle partition and the use bits. The kernel is generated from the parent's kernel
   source with the production functions replaced (as `founding_legibility_kern` did); everything else is the parent's
   code byte for byte.
9. **Cells (spec, amendments 5–7).**
   - **Ideal table, development streams 0–19:** R0 (5 rerun replicates for draw-for-draw validation against the stored
     `Ni`, the rest taken from the stored runs), R0 + alternatives, R1, R2, R3 (k = 2 CLOCK-LRU), R3 (k = 3 CLOCK-LRU),
     R3 (k = 2 FIFO); H-full is the stored cell. "Best R3" is the R3 cell with the highest fair share at 10,000 on these
     streams (ties: smaller k, then LRU).
   - **Ideal table, confirmation streams 20–59:** R0, R0 + alternatives, R1, R2, best R3; H-full stored. The
     confirmation set decides (amendment 7).
   - **Executed, development streams 0–19:** at K = 3·10⁶: R2, best R3, R0 and H-full rerun under this implementation
     (H-full = the parent's H mode, which has no production), and R2 with root-keyed dispatch; at K = 10⁶: R2, best R3,
     R0 (H-full at 10⁶ is the stored parent cell `H_eq`, the same implementation since H runs no production).
   - **A (200, 64) panel**: R2 on the ideal table, 12 runs, if the budget allows.
   - **Extensions:** five R2 development runs and their five H-full partners extended to 20,000.
   - **Drop order** (spec), by cost only if the projected total exceeds about 24 hours on 3 workers: the (200, 64)
     panel, then R3 at k = 3, then K = 10⁶; after those, executed cells on the confirmation streams are not run (they are
     not in the plan), then the dispatch variant, then the 20,000 extensions.
10. **Statistics (spec, amendments 7–8).**
    - **Outcomes:** fair share at 10,000 (terminal, primary) with the time averages over generations 0–10,000 and
      2,000–10,000 beside it; runs with any fair island; zero-wage and ¼-wage shares; wage-state occupancy (fraction of
      island-checks in each state: fair, ½ unfair, ¼, 0) and the island transition matrix between consecutive checks;
      first-fair generation per run (first check ≥ 20 with a fair island); losses (a run's fair share falling from ≥ ½
      to ≤ 0.1) and regrowths (rising from ≤ 0.1 to ≥ ½ after generation 20).
    - **Production and cost:** per executed encounter, attempts by outcome (primary found, alternative written,
      NONE, duplicate of a held script, marked skip, cap timeout, fuel timeout), validations (valid, invalid,
      validation timeout, validation fuel exhaustion), evictions and use-bit sets, from the kernel's counters; scripts
      per program per set (population means at generations 0, 200, 2,000, 10,000); the encounter cost relative to play
      from a stride sample of executed encounters in the kernel (play, validation and production steps per
      participant): median, 90th and 99th percentiles of (play + validation + production) / play, and the cumulative
      charged work (sum of validation and production steps over sum of play steps); upper quantiles judged separately
      from the median (amendment, RE 5).
    - **Nuclei (amendment 8).** In each run that regrows (fair share ≥ ½ at 10,000 and ≤ 0.1 somewhere in generations
      20–200; CC§1.0 item 8), the nucleus island and its first fair encounter, with every *pivotal* script (removing it
      from the members sharing its holder's run tree changes the encounter away from fair). Each pivotal script is
      tagged by **provenance class**: *first* (the first bundle of its set: what R0 could hold), *per-root* (a later
      bundle's primary: written by R1's trigger), *alternative* (an alternative: written only by R2's PROD3A); and by
      its CC component (canon, (a), (b)) and S₃^static membership. Reported: the fraction of first fair encounters whose
      pivotal scripts include a per-root script, an alternative, both, neither.
    - **Acquisition timing (amendment 8).** For every script class (per-root, alternative), the first check at which
      some individual holds one, and per run the first check at which a pivotal class of the eventual nucleus is held
      anywhere; against the **fair bosses' extinction time**: the first check ≥ 10 at which no island has a present
      boss type that pays ½ to the island's modal worker pair (and the check at which they reappear).
11. **Mechanism checks (amendment 8).**
    - **Fixed encounter traces** (no evolutionary feedback): for replicates 0–2, islands 0–7, the founders' composition
      is frozen and each island runs 3,000 encounters drawn uniformly from it (a fixed stream, the same for every rule);
      programs' lists evolve by production (each individual's list is tracked) but no selection or migration acts.
      Reported per rule at the ideal table and at 3·10⁶: roots at which a set is lacking (eligible roots), writes
      (primaries, alternatives), coverage of H by what is held (by CC component, per individual, mass-weighted), checks
      made in validation, validation and production fuel exhaustion, older-primary shadowing events (item 7).
    - **Replays:** for up to five regrowing runs per rescuing rule (a rule whose fair share at 10,000 is ≥ 0.2 on the
      development streams), the run replayed from the start with one class of the nucleus's newly written pivotal
      scripts (each pivotal script, in turn, up to three per nucleus) barred from production for every lineage. By the
      counter-based Moran stream the replay coincides with the original until the barred script would first have been
      written ("a checkpoint replay suppressing the script", amendment 8). Reported: fair share at 10,000 and whether it
      still regrows.
12. **Realizability audit (amendment 2).** PROD3A is written as code in the λ-language (a library function appended
    to K₃′ in a separate audit process; the run's library is untouched) and run by the term on sampled encounters:
    (a) it returns PROD3's primary and the symbolic alternative on every sample, with no host-supplied branch
    information (the term reads only boxes it calls); (b) its step counts against the cost model's prediction; (c) the
    validation step as code (`vone4` on the program's own box) against the model; (d) whole encounters by the term with
    lists written by R2 (alternatives first, several bundles per set, after appends and evictions): plays, check values
    and steps equal the evaluator's; (e) **soundness across list changes**: every check the term returns T for a set at
    a root is a set the subject actually plays into at that root (the parent's soundness test), on lists before and
    after each append and eviction. The steps measured are those the kernel charges.
13. **Reproduction (amendment 6, tests).** R0 in the new kernel must reproduce the stored S₃ + eq ideal runs `Ni`
    replicate by replicate in every dynamic summary field (fair masks, plays, holders, exits, the 10,000 extension);
    the mark's counters differ by construction. Checked on replicates 0–4 before any counted cell. H-full is the stored
    cell (`cell_Hfull`, 60 replicates, itself checked draw for draw against `Heq_i` by CC).

### 1.1 Static analysis: which scripts each rule can ever hold, against H

Per run tree and set: S₃^static (everything PROD3 can return at some root, `EQ` = F; CC§1.0 item 2) and Alt^static
(every alternative PROD3A can return at some root). The rules can ever hold: R0, one script of S₃^static per set (the
first written); R1, any subset of S₃^static (one per root class at which the held ones fail); R0 + alternatives, one
bundle per set from S₃^static × Alt^static; R2 and R3, any subset of S₃^static ∪ Alt^static (R3 at most k bundles at a
time). Bosses have no alternatives: every boss script of H outside the null (c) is in S₃^static (CC§1.2), so R1 can
hold every non-(c) boss script.

Scratch result (workers, prior mass of H scripts per program, the CC labels): every alternative is an H script (0 of
168 run-tree-sets with new alternatives produce a script outside H); PROD3A's primary equals PROD3's script at every
assignment; (b) ∩ S₃^static (0.512 scripts per program) and canon and (a) are fully reachable by R1; **(b) \ S₃^static
(0.328 scripts per program, the shadowed alternatives) is 0.94 reachable by R2's single alternative** (the rest needs
two flipped choice points); (c) and (d) are unreachable by construction (the gate, `EQ`-true paths), except 0.03 of (d)
that is also an alternative at an `EQ` = F root. So R2's reachable set is H's (b) up to 6% of the shadowed part, and
the coverage run's "plus (b)" grant (0.30) is the target R2 can reach if the scripts are written in time and in the
right places.

To be computed in §1.x: the same table by role and joint class from the code; the **validity cover number** per run
tree and set (the fewest scripts of S₃^static ∪ Alt^static valid, together, at every root at which some script is
valid): if it is ≤ 2 for most of the prior mass, a cap of two bundles cannot be the bind (Sol's counter-prediction).

### 1.2 By hand on named programs (CC§1.1 labels)

- **T₁** (B½ ? W : S): [D] canon (RunNeg B½) is valid at every root with the boss not certified =½; its [C] script (a)
  is written at the first root with B½ = T. R0 already writes both; R1 adds nothing for T₁.
- **U** (B½ ? W : (O:S ? S : W)): [C] canon is written on the default path (B½ F, other not striking); at a concession
  boss certified =½ it fails validation and R1 writes the Run-on-B½ script (b). R0 never does: this is a producible
  second path. [D] (Hyp on O:S) has no alternative (the false path ends in W).
- **D\*** (P₁^¼:S ? ½ : (P₁⁰:S ? ¼ : 0)): R0 writes ≤¼ on the 0 path at its first default root and is then never
  certified ≤¼ on its ¼ path; ≥¼ is written on whichever of its ½ / ¼ paths it meets first. R1 writes the others as it
  meets the roots (the "concession certified ≥¼ on its ¼ path is not certified on its ½ path" of the CC nuclei).
- **A worker with a shadowed alternative**, e.g. O:W ? W : (B½ ? W : S): [C] is Hyp on O:W (work if the other is
  certified to work); PROD3 writes it at every root; its alternative "other not certified to work, boss certified =½"
  is never written by R0 or R1. R2 writes it in the same attempt, first in the bundle.

### 1.3 Outcome regions (scored in the predictions file)

For each prediction: *supported* if the stated inequality holds at the scored endpoint on the confirmation streams
(development streams where only they run), *contradicted* if the falsifier fires, *inconclusive* otherwise (including
when the paired interval spans both the predicted effect and its absence). Observed-threshold verdicts (a number
crossing a bound) are kept apart from statistical evidence: with run-level all-or-nothing outcomes, 0/20 runs allows a
per-run success probability up to 0.16 (Wilson upper bound), 0/40 up to 0.09.

### 1.4 Hand predictions and the mechanism behind them

- **R1 is partial.** It writes the producible second paths only when a lineage meets the root, not from generation 0
  as the CC grant did; the grant of exactly these scripts gave 0.10 (3 runs). Expect R1 at 0.00–0.10 on both stream
  sets.
- **R2 is the candidate.** It reaches 0.94 of the shadowed part and all of the producible part, but later than a
  grant and in acquisition order. Concessions and militants meet the relevant roots early on mixed islands (¼-wage
  islands are half of the population), so expect R2 at 0.1–0.3: below H-full more likely than equal.
- **R0 + alternatives ≈ R0.** One bundle per set: the shadowed alternatives alone gave 0.05 as a grant.
- **The cap.** Workers meet few distinct root classes for a given set; expect the validity cover to be ≤ 2 for ≥ 0.9
  of the prior mass and k = 2 CLOCK-LRU within 0.05 of R2; FIFO k = 2 at most 0.1 below.
- **Executed fuel.** Validation charges every held set's nested calls at every encounter where a program may produce,
  so the median encounter cost rises above R0's 1.0× play (FL) to about 1.5–2× under R2, before the mark can help (the
  mark skips only failed productions). At 10⁶ R2 is near 0 (the free-certificate cell gave 0.03, and lists are longer
  here); at 3·10⁶ below H-full at 3·10⁶ and above R0 at 3·10⁶ (FL natural: 0.034).
- **Timing.** Second-path scripts appear within the first 10–20 generations; the fair bosses go extinct by about
  generation 20 in most runs (every cell collapses to ≈ 0.05 there, FL§1.4), so regrowth depends on what is held by
  the surviving ½-paying bosses' lineages at that time.

These are carried into the predictions file with falsifiers and outcome regions.
