# Spec: identity-dependent results under world K (keyed self-hypothesis defection), 2026-10-18

Status: draft by the RE (Fable); to be reviewed sequentially by gemini-4-argon then gpt-6.1-sol (`--mode amended`); to
be run by an Opus subagent. The RS adopted world K as the provisional default (DEFERRED 1, 2026-10-18). Results computed
in world L receive addenda, never rewrites. REJECTED.md checked: nothing re-opened; the provenance rule (S-nonself) is
retested because its rationale (self-play production mints identity cliques) may not survive K, which is new evidence.

## Why

In world L a program's first self-hypothesis D certificate validates at every root, so own-D readers defect against
every distinct quote: the TwinD identity family and the certified-defection detector are both this accident (RESULTS
"Legitimate detectors"). In world K that certificate is keyed to its production partner. At (200, 64) universal-open
went 11 → 19 of 20 under K. Every result whose failure mode was identity cliques in the realizable PD grammar is
therefore in question: the scaling path and its copy-count law, the Pangaea continuum and its establishment law,
the removing-rivals classification, and the provenance rule. Explicit-`eq` cliques (the identity-and-tags grammar)
are a different channel that K does not touch; they are not rerun.

## Design

**Machinery.** `src/detectors*.py` (world K's tables and reading; K off reproduces L draw for draw),
`src/realizable_scaling*.py`, `src/pangaea*.py`, `src/removing_rivals*.py`, `src/provenance*.py` (import only).
Cached tables copied read-only (the detectors worktree has `runs/detectors/K/`) or rebuilt. r = 100 production
encounters per Moran event at every N in both worlds (avoiding the counter-RNG overlap above 100), with world L rerun
beside K on paired founders as the reference; ε = 0; S-nonself unless stated; calibrated mN.

**Static (notes §1, before any cell).** Under K: which run trees still behave as identity holders (cooperate only with
their own quote) and their prior mass; the K network's mass μ_net (FairBot family, PrudentBot, the gentle detectors);
gentle readers' predator mass; any new rival class (programs exploited or feuding under K that were not in L).

**Cells (20 runs, paired L / K).**
- **Scaling path** (RESULTS "The realizable lottery along paths in (N, I, mN)"): S-nonself and the proportional
  control at (100, 64), (200, 64), (400, 64), (100, 128), (200, 128), (100, 256); horizon 2,000 and 10,000.
- **Pangaea continuum** (RESULTS "Cliques on a Pangaea"): N·I = 12,800 at (200, 64), (800, 16), (3,200, 4),
  (12,800, 1); fission–fusion (100, 128) merged at 200; Pangaeas at 3,200 and 6,400 for the establishment law.
- **Provenance rule** (RESULTS "Provenance"): S-self against S-nonself at (100, 64) and (200, 64), K and L.
- **Removing-rivals classification** (RESULTS "Removing rival networks", Part 0): rerun statically on the K stored
  states of the scaling cells: closed-open, exploitable and identity rival islands.

**Statistics.** Universal-open, identity islands, rival islands by class, whole-run scramble failures, island
efficiency (reported, never selected on); per pair of cells the paired K − L difference with exact intervals; the
residue's composition under K.

**Scale guard.** ≤ 3 workers; the per-root run uses up to 3: check `ps` first; one job per process. Drop order:
(100, 256), then the Pangaea at 3,200, then the proportional control at (100, 128).

## Required outputs

`src/world_k.py` (+ `_run.py`, `_report.py`), `tests/test_world_k.py` (K off reproduces stored L runs at r = 100 where
stored; K tables match the detectors run's), `notes/world-k.md` (§1 static, hand predictions; §2 costs),
`runs/world-k.md` and `.json`, predictions committed before any counted cell, and the usual hand-back including the
addenda to append to each affected RESULTS section.

## RE predictions (with falsifiers)

1. **Identity cliques vanish under K in this grammar:** identity islands ≤ 0.005 per island in every K cell.
   *Falsifier:* ≥ 0.02 anywhere.
2. **Universality at N ≥ 200 rises to the proportional control's level:** S-nonself under K within 0.1 of the
   L proportional control (0.80–0.95) at (200, 64), (400, 64), (200, 128); the residue is bridge-less non-identity
   rivals. *Falsifier:* K S-nonself ≤ 0.6 at any of them.
3. **The copy-count law weakens** [revised after the second review: non-identity rivals, bridge loss and coverage can
   still depend on founders and geometry]: the K − L gain in universal-open is larger at (200, 128) than at (200, 64).
   *Falsifier:* K universal-open falls by ≥ 0.3 from (200, 64) to (200, 128).
4. **The provenance rule stops mattering:** S-self and S-nonself within 0.1 of each other under K (in L, S-nonself was
   better by removing minted cliques). *Falsifier:* a difference ≥ 0.2.
5. **The Pangaea establishment law strengthens:** with the gentle readers in the network, μ_net rises and all-defect
   Pangaeas fall (at 6,400: ≤ 2 of 20 under K against 5 under L). *Falsifier:* K ≥ L.
6. **Fission–fusion stays universal-open:** 20/20 in K. *Falsifier:* ≤ 17.
8. **Counter-predictions registered (gpt-6.1-sol).** Some copy-count dependence remains under K; the Pangaea
   improvement is smaller than 5 → ≤ 2 of 20, possibly undetectable; near-ceiling universality under S-self and
   S-nonself may hide reproducible differences in establishment time and founder survival.
7. **Counter-predictions registered (gemini-4-argon).** Under K, S-self turns the former TwinD templates into
   self-defectors (a self-play D certificate keyed to the own quote), so S-self and S-nonself differ in mechanism even if
   universality is near ceiling; and the Pangaea all-defect rates under K and L are indistinguishable (within 1–2 runs)
   at 6,400 and 12,800, because the identity mass moved into the network is small.

## Amendments after the first review (gemini-4-argon; these supersede the text above where they conflict)

1. **Production rate.** r = 100 is kept as the primary schedule (constant production per program, validated against
   native r in the Pangaea run), with an r = N/2 control on the overlap-free Pangaea kernel at (800, 16) and (3,200, 4),
   both worlds, so that K's keying cannot be confounded with production undersampling at large N. Logged: the fraction
   of a gentle reader's encounters in which it acts with versus without a matching keyed certificate (does it behave as
   an unconditional-cooperator shadow against unmet defector quotes?).
2. **Provenance mechanics.** Notes §1 classifies, statically, what S-self does to the former TwinD templates under K
   (self-defector, identity holder or open); the run logs the fraction of the production budget spent on self-encounters
   under S-self.
3. **Paired outcome transitions.** For every paired L / K cell, the contingency table of island outcomes (open,
   identity, non-identity rival, all-defect) at generations 200, 2,000 and 10,000, showing whether K converts L's identity
   islands to open ones during establishment or during migration.
4. **One rain cell.** Removing-rivals' rain under K at (200, 64) with the annealed schedule (K = 3 exposure), against its
   stored L numbers, to test whether rain now cures exploitable rivals without feeding a clique sink.
5. **Recorded for the certificates conversation (DEFERRED 1), not tested here:** source-keying replaces a semantic flaw
   with a combinatorial one (one keyed certificate per distinct defector quote, thrashable by quote-diverse defectors
   under a capped list); keying to the canonical sub-tree used in the proof is the structural alternative.

## Amendments after the second review (gpt-6.1-sol; these supersede the text above where they conflict)

1. **The rain cell is paired.** Rain runs in both worlds with identical settings and paired founders; stored L numbers
   are context only.
2. **Transitions, not snapshots.** Establishment times, holder transitions and migrant ancestry are logged per island, so
   conversion is attributed to establishment or migration from lineages; snapshot tables are reported as associations.
3. **Production units fixed.** Every Moran event runs r = 100 production encounters, each drawing a uniformly random
   focal individual and partners from its island (as in the Pangaea kernel), so each individual has 2r = 200 production
   opportunities per generation at every N; the r = N/2 control is added at (6,400, 1) as well, and distinct-key coverage
   and keyed-certificate evictions are logged.
4. **Inference.** Runs are the independent units; paired run-level differences with exact (McNemar or Clopper–Pearson)
   intervals at 95%; "within x" claims are equivalence claims only if the interval lies inside the band, otherwise
   inconclusive; unresolved runs are distinguished from absorbing failures, with resolution-time censoring reported.
5. **Mechanism checks.** Tests that a keyed certificate is rejected against a different quote and accepted against its
   production partner, under self-play, after copying and after eviction; identity behaviour classified on reachable
   certificate inventories, not templates; P(C,C), target-network membership and transition support reported separately
   from the "open" label; a check whether K suppresses defection generally (the share of hypothesis-closed D certificates
   live against non-partners in L and K) as an alternative to dissolving identity barriers. Conclusions are
   grammar-relative.
