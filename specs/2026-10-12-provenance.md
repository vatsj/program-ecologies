# Spec: provenance: who writes the first certificate, and against whom, 2026-10-12

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol; to be run by an Opus subagent. Follow-up to RESULTS
"The realizable language, milestone 5" and DEFERRED 11 (the RE's open decision on self-play production).

## Why

Milestone 5 found that endogenous production is parochial-biased: a producer whose first partner is its own copy
writes a self-play-only script (valid only at R = S) and keeps it for life under the lack rule, so endogenous
search mints identity cliques (identity islands 0.06 → 0.22, universal-open runs 25 → 13 of 40), while one
external host donor per island with copy-only production gave the most universal cell measured (33/40). The RE's
decision is whether self-play production is admissible. Rather than rule by fiat, the run measures the provenance
rules side by side on milestone 5's machinery, and asks which rule, if any, recovers the single-donor cell's
universality without an external donor: that is the realizable version of "almost all seeds" with endogenous
certificates.

## Design

Milestone 5's language, grammar, lack rule, would-be-self adoption check, kernel, lottery law and endpoints
(`src/lt_genes*.py`), unchanged; (N, I) = (100, 64), mN = 1, horizon 2,000, 40 runs per cell, paired seeds, run-level
uncertainty; the frozen-inventory chain is not run.

**Provenance rules** (production mode S or CS, the rule a trait or a cell-wide law as stated):
- **S-self** (milestone 5's S): produce against the first partner, whoever it is.
- **S-nonself:** produce only against a partner whose source is not one's own (structural `eq`), keep searching
  until one is met; self-play scripts are never written.
- **S-k** [after review, specified]: produce a candidate script against each of the first k *source-distinct*
  partners (distinctness by structural `eq` on the behavioural source, so at most one of them can equal the
  producer's own spelling), k ∈ {2, 3}; candidates with zero validity are inadmissible; keep the candidate that
  validates against at least two source-distinct partners, ties broken by the earliest candidate; if k distinct
  partners never arrive within 50 encounters, keep the best candidate so far and log it as "k not reached". The
  safeguard is "validates against two distinct sources", not a binomial argument about own copies.
- **S-gate+cache** [after review, contract]: milestone 5's gate rule (one's own check against each partner) with a
  negative-result cache keyed by every input the gate reads (the partner's source and script, one's own list state,
  the budgets), distinguishing rejection from timeout, invalidated on any change of one's own list; lookup, storage
  and repeated misses charged at the evaluator's cost of the corresponding primitives; run as one cell to see
  whether the cache makes the gate feasible.
- **S-self-delayed** [after review, the timing control]: S-self with acquisition delayed to the encounter at which
  S-nonself would first produce (the matched nonself encounter), then produced against whatever partner is present,
  self included; this separates certificate generality from acquisition timing and opportunity.
- **C-donor** (reference): one H donor per island with copy-only production, the milestone-5 cell, rerun on these
  seeds.
- **H-only** (reference).

[after review] **Identity bookkeeping.** The rule trait and the acquired inventory are provenance metadata and
mutable state, *not* part of the quoted behavioural source and not read by structural `eq`, so assigning rules
cannot split formerly identical copies; equality-class frequencies are reported per cell. "Self-play-only" is
defined by script validity (valid at R = S and at no distinct-source root), audited over the full supported carrier
set including scripts that enter by copying, not by observed encounters. Attempts, waiting encounters, candidate
validity and first acquisition are logged separately per producer. Paired seeds use event-indexed random streams,
and every contrast is reported as a paired difference with an interval beside the marginal Wilson intervals.

**Mixed-provenance cell:** the rule as a heritable trait with prior ¼ each over {S-self, S-nonself, S-2, CS-nonself},
so that selection among rules is measured; full rule frequencies are reported beside cooperative-holder
frequencies, stratified by carrier and by initial equality class.

**Static, before any cell:** for each rule, the scripts it writes for the named carriers (CB, CB1, CBP₄, CBPr, the
eq-clique spellings) against each first-partner type (self, twin spelling, distinct carrier, C, D), by hand and by
the tactic as code; which rules can write a self-play-only script at all; the expected number of first-partner
self-encounters per island under the seed (the chance that a producer's first partner is its own copy, ≈ the
spelling's seeded frequency); the production cost per rule and the fraction of signatures timing out at P = K/4.

**Cells:** S-self, S-nonself, S-2, S-3, S-gate+cache, CS-nonself, the mixed-provenance cell, C-donor, H-only. Report,
per cell: E3 success, universal-open with Wilson intervals, identity islands, the fraction of held scripts that are
self-play-only, host ancestry, establishment with censoring-aware times, per-match and per-acquisition cost by
rule, timeouts, the mode/rule composition of cooperative holders over time, and the stage statistics of the
identity run (arrival → establishment → persistence → spread), and island-level efficiency reported separately
from global universality. **Ablation** [after review, mass-matched]: S-nonself with the identity-clique classes'
mass moved onto a specified set of non-clique carriers (the open prudent core of RESULTS "Prudent openness", in
proportion), not silently renormalized, so the ablation changes clique abundance and nothing else named. **Size:**
the main contrast (S-self vs S-nonself vs C-donor) also at (200, 64) and (100, 128), 20 runs each, labelled
finite-size, with unresolved runs extended to 10,000 generations and reported as censored at 2,000. **Primary
contrasts, predeclared:** (a) S-nonself vs S-self on universal-open and identity islands; (b) S-nonself vs
S-self-delayed on the same; (c) S-nonself vs C-donor; everything else is secondary. Indeterminate endpoints
(polymorphic islands at the horizon) are censored as in the milestone-2 endpoint E3.

**Scale guard.** Milestone 5's tables are reused; the new cost is the rule logic and the cells. ≤ 3 workers; kill
pool children by pid before any driver; no other experiment is running.

## Required outputs

`src/provenance.py` (+ `_run.py`, `_report.py`, importing `lt_genes*`), `tests/test_provenance.py` (the rules on the
named carriers against each first-partner type; S-nonself never writes a self-play-only script; S-k's majority
selection; the cache's effect on the gate rule's cost), `notes/provenance.md` (§1 the rules, the hand scripts, the
self-encounter arithmetic, before any cell; §2 costs), `runs/provenance.md` and `.json`, a predictions file from the
spec committed before any counted cell, the usual hand-back (draft RESULTS, REJECTED, THEORY §9.2 and §9 item 12 /
DEFERRED 1 and 11 edits, NOTATION, ≤ 5 lines, branch name, commits).

## RE predictions (with falsifiers)

1. **S-nonself removes the minted cliques and recovers most of the donor cell's universality:** identity islands
   ≤ 0.08 (S-self 0.22) and universal-open ≥ 25/40 (S-self 13, C-donor 33, H-only 25); the self-play-only script
   fraction is 0. *Falsifier:* identity islands ≥ 0.15, or universal-open ≤ 18/40, or any self-play-only script
   under S-nonself.
2. **The residual gap to the donor cell is mostly the identity cliques the seed itself contains** [revised after
   review] (≈ 57 copies per run at this prior): the mass-matched ablation of S-nonself improves universal-open by
   ≥ 6 runs over S-nonself (my bet: to ≥ 28/40). *Falsifier:* an improvement ≤ 2 runs.
3. **The majority rule depends on coverage, not on an ordering** [revised after review]: S-3 retains a script that
   validates against two distinct sources and lands within 6 runs of S-nonself on universal-open; S-2 ties
   systematically (two candidates, each valid against one partner) and its tie-break makes it within 6 runs of
   S-self; no monotone ordering is predicted. *Falsifier:* S-3 differing from S-nonself by ≥ 12 runs, or S-2 ≥
   S-nonself.
4. **The nonself rule's median cost is low and its tail is heavy** [revised after review]: median per-acquisition
   cost within 1.5× of S-self's, but acquisition delays heavy-tailed, with ≥ 5% of producers in near-monoclonal
   islands waiting ≥ 20 encounters and ≥ 1% never acquiring by the horizon; the timing control S-self-delayed
   recovers ≤ half of S-nonself's gain over S-self in identity islands (the gain is generality, not timing).
   *Falsifier:* median cost ≥ 3×, or no producer waiting ≥ 20 encounters, or S-self-delayed recovering ≥ 0.8 of the
   gain.
5. **The mixed-provenance cell enriches faster-acquiring rules among cooperative holders** [revised after review]:
   S-self and S-2 are over-represented relative to ¼ at establishment (founder and linkage effects), the full-rule
   frequencies drift back toward the prior by the horizon, and the cell's universality sits between S-self's and
   S-nonself's. *Falsifier:* every rule within 0.05 of ¼ among cooperative holders at establishment, or a rule ≥ 0.7
   at the horizon.
6. **The gate rule with a negative cache is feasible and twins-biased:** the cell finishes within the budget, and
   its identity islands are ≥ S-self's. *Falsifier:* the cell not finishing within the budget, or identity islands
   ≤ S-nonself's.

The RS is invited to add predictions; the uncertain ones are 2 and 5.
