# Spec: removing rival networks: a sponsored PrudentBot donor (prevention) and seed rain (cure), 2026-10-15

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
Follow-up to RESULTS "The realizable lottery along paths in (N, I, mN)" and the RS's decision of 2026-10-15
(DEFERRED 1): the PrudentBot network is the target; rival networks are failures to remove. REJECTED.md checked:
"propagules are not a scaling fix" stands (no propagules here); finite-εN runs are approach-rate diagnostics
(CLAUDE.md discipline 5), and seed rain below is labelled as such; nothing re-opened.

## Why

At N ≥ 200 two kinds of rival are permanent. **Identity cliques** (the TwinD family) cooperate only with their own
source. **Certificate-reading rivals** such as the anti-punisher `if(or(CHK(me,^C,C),CHK(them,^D,D)),D,C)` defect
against anyone certified to punish DefectBot; against PrudentBot no bridge exists anywhere in the language (0 of
17,394 code-plus-certificate units are mutual with both). Bridges cannot remove them. **RE static check (one run,
(200, 128), proportional control, rep 1):** the anti-punisher cooperates with 2,870 units that defect against it;
2,222 of those do not cooperate with their own copies and are defected against by every network holder. These are
*predators*: they invade a rival island strictly (the rival feeds them) and are then invaded by the network (it
cooperates with itself and defects against them). The path rival → predator → network needs no bridge. At ε = 0 it
is closed because every predator dies in the scramble long before the rivals settle. Identity cliques have no
predator of this kind (they defect against every non-copy). So: **prevention** for cliques (seed the target), **cure**
for exploitable rivals (a trickle of fresh founders that brings predators back).

## Design

**Machinery.** `src/realizable_scaling*.py`, `src/provenance*.py`, `src/lt_genes*.py` (import only; a new kernel
module may copy and extend the provenance kernel for founder re-injection, never edit it). S-nonself unless stated,
L seeds, ε = 0 except for rain, w = 0.3, calibrated mN = (N/100)^0.7, cached tables from the scaling worktree's
rebuild procedure.

**Part 0, static (notes §1, before any cell).** For every non-universal run at N ≥ 200 in the stored scaling cells
(S-nonself, proportional, ablation), classify each failing island's holder as *exploitable* (some predator exists:
the rival cooperates with it, it defects against the rival, it does not cooperate with its own copies, every target
holder defects against it) or *closed*; report the predators' prior mass and the expected predator arrivals per
island-generation under each rain rate; define the **target network** concretely (the PrudentBot run tree and every
holder mutually certified with it) and report which stored runs end on it.

**Part A, sponsored PrudentBot donor (prevention).** One PrudentBot carrier with its full certificate list per island
at founding (the "state sponsored" founder), replacing one prior draw; compared with C-donor and S-nonself on paired
streams. Cells: (200, 64), (400, 64), (200, 128), (100, 256); 20 runs; horizon 2,000 and 10,000.

**Part B, seed rain (cure; a finite-ε diagnostic, approach rates only).** At each birth, with probability ε the
newborn is a fresh founder drawn from the length prior (empty certificate list, as at seeding) instead of a copy;
ε chosen so that fresh founders per island per generation are εN ∈ {0.01, 0.1, 1}. (B1) **Cure:** rerun the stored
failing runs at N ≥ 200 deterministically to generation 2,000, then continue with rain for 10,000 generations; per
rival island: resolved or not, by which path (predator step, direct invasion, other), to which network, time.
(B2) **Natural:** S-nonself from generation 0 with rain at (200, 64) and (200, 128), 20 runs per rate. (B3) **Both:**
the sponsored donor plus rain at εN = 0.1.

**Statistics.** Universal-on-target runs (every island on the target network), universal-open runs, identity and
rival islands at each horizon, network-island losses under rain (any target island leaving the target), the path of
every resolution, and costs. Efficiency is reported, never used to select.

**Scale guard.** ≤ 3 workers (the coverage-components run uses up to 3); check `ps` first. Projected cost before
the cells; drop order: B2 at εN = 1, then (100, 256) in A, then B3.

## Required outputs

`src/removing_rivals.py` (+ `_kern.py` if needed, `_run.py`, `_report.py`), `tests/test_removing_rivals.py` (ε = 0
reproduces the stored scaling runs draw for draw; the predator classifier on the RE's example; the sponsored founder
holds PrudentBot's full list; rain draws match the prior), `notes/removing-rivals.md` (§1 static, §2 costs),
`runs/removing-rivals.md` and `.json`, predictions committed before any counted cell, and the usual hand-back.

## RE predictions (with falsifiers)

1. **Most non-identity rivals are exploitable; identity cliques are closed:** ≥ 0.8 of non-identity rival islands
   have a predator with positive prior mass; 0 identity islands do. *Falsifier:* ≤ 0.5 exploitable.
2. **Rain cures exploitable rivals:** at εN = 0.1, ≥ 0.8 of exploitable rival islands join the target by 10,000
   generations, mostly by a predator step. *Falsifier:* ≤ 0.4.
3. **Rain does not cure cliques at N ≥ 200:** ≤ 0.1 of identity islands resolve at any rate. *Falsifier:* ≥ 0.3.
4. **Rain does not break the network:** target-island losses ≤ 0.01 per island over 10,000 generations at
   εN ≤ 0.1. *Falsifier:* ≥ 0.05.
5. **The sponsored donor prevents cliques:** identity islands ≤ 0.01 and universal-on-target ≥ 0.85 in every A cell,
   at least C-donor's. *Falsifier:* below 0.7 anywhere.
6. **Both together are universal on target:** B3 ≥ 0.95 at both geometries. *Falsifier:* ≤ 0.8.

7. **Counter-predictions registered after review.** *Sol:* cure at εN = 0.1 varies sharply with the accessible
   predator mass (80% of islands even receiving a predator needs accessible mass ≥ 0.0016) and many exploitable
   rivals stay unresolved; sponsorship reduces cliques but leaves geometry-dependent residual failures, so 5 and 6
   are too high; cliques resist far more strongly than exploitable rivals without necessarily meeting 3's bound.
   *Gemini:* the cure at εN = 0.1 is < 0.4 unless a simple high-prior program such as DefectBot is itself a predator.

The RS is invited to add his own; the uncertain ones are 2 (predators must reach rival islands before the network's
migrants dilute them) and 4.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **Operational predators.** Part 0 classifies predators by the phenotype a fresh founder actually reaches: an
   empty-list arrival plus S-nonself production against the resident rival (and against target migrants), not the
   certified unit table. The predators' accessible prior mass, the top three by mass (stating whether DefectBot and
   other constants are among them), and the expected arrivals per island-generation at each rate are reported from
   that mass.
2. **Triples, not pairs.** For each (rival, predator, target) triple the frequency-dependent payoffs are computed,
   including predator–predator and target–predator play, to say whether the chain eliminates the rival or leaves a
   rival–predator mixture; the most promising triples are tested with the actual kernel on forced islands.
3. **Matched counterfactual for B1.** Every generation-2,000 checkpoint is branched into an ε = 0 continuation and
   each rain continuation; cures are differences between matched branches, conditional on the selected checkpoints.
4. **Injection assays.** From a few checkpoints, one accessible predator, and separately a matched non-predator, are
   injected into a rival island at generation 2,000, separating arrival scarcity from establishment failure.
5. **Paths and endpoints, fixed before any cell.** A *predator step* is a predator lineage reaching ≥ 0.5 of the
   rival island before the target takes it; otherwise the path is *direct invasion* or *other*. The intermediate
   holder of every resolving island is logged. Target membership is frozen as holders whose pairwise P(C,C) with the
   PrudentBot holder and with each other is ≥ 0.95. A *target-island loss* is a change of the island's majority holder
   to a non-target holder lasting ≥ 25 generations; transient contamination is reported separately. Both target →
   rival and rival → target transitions are recorded, with residence times and certificate provenance.
6. **Donor control.** A PrudentBot founder with an *empty* certificate list under S-nonself production, at (200, 64)
   and (200, 128), separates sponsoring the code from sponsoring the certificates.
7. **Uncertainty.** Run-clustered intervals (islands share migration); 20/20 is reported with its interval (lower
   bound ≈ 0.83), and near-certain thresholds are read as observed thresholds only.
