# Predictions: bully-resistant readers in arm T (queue 76), 2026-11-08

Spec: `specs/2026-11-08-bully-resistance.md` (reviewed by gemini-4-argon and gpt-6.1-sol, folded). This file is committed
before step 0's assays were run, and before any counted step-2 mass computation or step-3 cell. Verdicts go into
`runs/bully-resistance.md` against the rules below.

## Pilot runs made before this file (disclosure)

- **Step 1 gates (read).** The 51-program table (T+'s 31 programs, 8 prudent readers P, 4 lenient-probe readers Q, 8 openers O) was
  built (about 1 minute); V2 holds (the 31 x 31 x 31 block equals T+'s on code, steps, read timeouts, forfeits and joint codes);
  P, Q and O agree with a table-level reference implementation on 2,550 (P, Q) and 2,500 (O) profiles each with no disagreement
  (`runs/bully_resist/step1_gates.json`). What I read from it and what it changes: (i) P_z, strict probe, refuses `Bn` and `Bp`
  in all 58 profiles each and accepts all 45 profiles in which a fair reader or a half constant names it at 1/2 (the
  validations hold); (ii) **the nested-reads gate fires**: every read of a reader by a reader times out (mutual regress), so P_z
  with the strict probe pairs with itself in 0 of 464 profiles and with the firm readers in 2.8% of profiles (firm with firm
  20.4%); the lenient variant Q pairs with itself in 6.3% and with firm readers in 11.4%, and re-admits `Bp` in the profiles where its
  probe times out (29 of 58); P_o pairs with itself 49% only through its fallback; the opener reads both partners every time
  (2.0 timed-out reads per profile against 1.0 for a single reader), forfeits: none in the whole (P u O u F u B)^3 sub-table, the
  most expensive profile 827 steps. The caps are not changed; the lenient variant Q is carried as a variant arm (spec: "scored
  separately, the registered main arm is not replaced"). Some E-predictions below use this.
- No dynamics cell, no step-0 assay and no step-2 mass has been run or seen.

## The spec's predictions, verbatim

- **RE 1 (mechanism).** Step 0 finds that bullies hold unequal pairs with 1/3-naming constants that firm readers cannot
  pry loose (a firm reader entering such an island fixes at or below 1/N), not that bullies shadow fair readers.
  Falsifier: the bully fixes above 3/N in a homogeneous fair firm-reader island, or a firm reader fixes above 3/N in a
  bully-held unequal island.
- **RE 2 (prudence restores a threshold).** Arm P at beta = 3, N = 200, I = 64 has a threshold delta\* <= 0.1. Falsifier:
  no grid delta meets the full threshold definition (V\* >= 0.9 at that delta and every larger grid delta); isolated passing
  cells are reported but do not count.
- **RE 3 (openers alone do not).** Arm O at beta = 3, N = 200, I = 64 has no threshold (constant victims cannot answer an
  offer). Falsifier: O has delta\* <= 0.1.
- **RE 4 (prudence is long).** Under R0 the shortest prudent reader is >= 10 nodes longer than the shortest fair reader,
  and under R2 within 3 nodes. Falsifier: R0 gap < 6 nodes, or R2 gap > 6.
- **RE 5 (still not a length-prior route).** No machine's length-prior-shaped law reaches V\* >= 0.9 at any tested delta at
  N = 200 or 400. Falsifier: any cell does.
- **gpt-6.1-sol's counters:** (a) RE 2 fails: no threshold for P at beta = 3 unless P improves establishment during
  founding; (b) RE 1 is a mixture varying with family and slot.
- **gemini-4-argon's counters:** (a) on RE 1, both mechanisms operate: the bully fixes near 1/N in a homogeneous fair
  firm-reader island (a neutral shadow) and later locks onto arriving 1/3 constants; (b) RE 2 fails even for P_z, because P
  cannot invade an island already unequal from the scramble or the tail.

## Scoring rules fixed here (the spec leaves them open)

**Step 0 statistic.** In a single-island Moran process with the other two slots monomorphic, an invader's payoff is frequency
independent, so its fixation probability from one copy is exactly rho(r, N) = (1 - 1/r)/(1 - 1/r^N) with r = exp(w * d) (w = 0.3,
d = the invader's net payoff minus the resident's net payoff in that slot, A_f charges at P_fail = 0.1 included; r = 1 gives 1/N). The
exact rho * N is the scoring statistic over **all** named resident triples in the class (no sampling); 10^4-trial Monte Carlo of the
same chain (and of the full kernel where it does not stop on play identity) is the empirical check and gives the empirical 1/N
baseline through a neutral relabelled twin of the resident entering each resident configuration. Fixation is read in the
invaded slot; a trial that has neither fixed nor gone extinct at the cap is reported as persisting.
Classes (programs: 16 firm readers = T's 8 single + 8 two-partner readers; 9 constants; bullies `Bn`, `Bp`; slots 0, 1, 2):
- FRI (homogeneous fair firm-reader islands): all three resident slots are firm readers and the outcome is a fair pair; FRC: two
  firm readers forming the fair pair and a constant in the third slot. Invader: each bully into each slot.
- UBI (bully-held unequal islands): resident = a bully, a 1/3-naming constant (C0 or C3; C6 reported separately) and a constant, in
  all slot orders, outcome class unequal with the bully on 2/3. Invader: each of the 16 firm readers into each slot.
- BFI (bully-held fair islands): resident = a bully and a firm reader forming the fair pair, third slot a firm reader or a
  constant. Invader: each of C0, C3 into each slot.
- Step 0.4: the same classes with P (strict probe; P_z main, P_o variant) or O in place of the firm readers: bully into the PI / OI
  islands, P and O into the UBI islands.
**Scoring of RE 1.** The two falsifier clauses are scored on class medians of rho * N: clause A fires if the median over FRI (and,
separately, FRC) of the bully's rho * N exceeds 3; clause B fires if the median over UBI of the firm readers' rho * N exceeds 3.
RE 1 holds iff neither fires and the UBI median is <= 1; "mixed" if a median is fine but more than 10% of assays exceed 3 (the
share is reported). **argon (a)** is true iff the FRI median is in [0.5, 3] and the UBI median is <= 1. **sol (b)** is true iff the
medians (or the shares above 3) differ across invader family or slot role (bully / victim / other) by more than a factor 3 in rho * N,
or neutrality (rho * N in [0.5, 3]) and persistence (rho * N <= 1 for firm readers in UBI) are both present at class level.
**Net payoffs.** Gross and net (with charges) payoff differences and N * w * d (the 0.1 charge is N * w * dpi = 6 at N = 200) are
reported for every assay class; the verdicts use the net.

**Step 0.3 holding configurations.** From a rerun (identical to the stored rows, checked on V*) of queue 75's beta = 1 and 3 cells at
N = 200, I = 64, delta in {10^-3, 10^-2, 10^-1}, 20 runs: the dominant program per slot on islands whose modal outcome at 120N is
unequal, and on islands fair at 30N and unequal at 120N. The mechanism statement lists the winning configurations by name.

**Dynamics (step 3).** "V\* share" = mean over islands and runs of the indicator that the island's modal outcome at 120N is a fair
pair (`vshare_ts[120]`), bootstrap over runs; delta\* = the smallest grid delta with mean V\* >= 0.9 at 120N and every larger grid
delta also passing; non-monotone responses are reported as such; an "all-islands" success is a run in which every island is
fair at 120N. Seeded starts: all islands start on a fair pair held by the arm's readers, or all on a bully + 1/3-constant unequal
pair; entry hazard = share of seeded-unequal islands that are fair at 120N, exit hazard = 1 - the share of seeded-fair islands that
are still fair at 120N. Recovery means entry hazard >= 0.25.
**Scoring of the counters.** sol (a) is true iff P has no delta\* at beta = 3, N = 200, I = 64, and its entry hazard from the seeded
unequal start is < 0.25 (establishment, not invasion, is the channel only if a seeded fair start also holds: exit hazard < 0.25).
argon (b) is true iff P has no delta\* there and step 0's UBI median for P (P into bully-held unequal islands) is <= 1 and the seeded
unequal start shows no recovery. RE 2 is scored on delta\* alone.
**Step 2 / RE 4.** Gaps are in nodes between shortest exact-member spellings in the machine's grammar, as in queue 75 (the
enumeration may be a lower bound on the minimum). Masses are conditional on finite trees, exact-member lower bounds. RE 5 is scored on
the length-prior-shaped series, both allocations; a cell counts if mean V\* >= 0.9 at 120N.

## My own predictions (E)

- **E1 (step 0, exact).** (a) UBI: a firm reader fixes with rho * N <= 1 in at least 90% of assays (it enters at a payoff below the
  1/3 victim's or the bully's). (b) FRI: the bully's rho * N lies in [0.5, 3] in at least 60% of assays (equal payoff in the unpaired
  slot; the other 40% are payoff-different, below 0.5 or above 3 depending on the slot). Falsifier: either share below its bound. This
  separates the two mechanisms of RE 1 and argon (a); I expect "both present".
- **E2 (arm P has no threshold).** Because P_z is self-incompatible and nearly incompatible with the firm readers (gate), arm P at
  beta = 3 has no delta\* at N = 100, 200, 400, I = 64 (RE 2's falsifier fires), and V\* is below T0's (constants alone, queue 74)
  at the larger delta. Falsifier: P has delta\* <= 0.1 at any of the three N.
- **E3 (lenient probe).** The lenient variant Q has V\* at beta = 3, N = 200 below P's at at least 4 of the 6 grid delta (it re-admits
  `Bp` when the probe times out). Falsifier: Q at or above P at 3 or more.
- **E4 (charges).** In the beta = 0 control the mean A_f charge per reader per generation at delta = 0.1, N = 200 is at least 1.4 times
  larger for O than for the firm readers, and P's is within 1.25 times the firm readers'. Falsifier: either bound.
- **E5 (R2, step 2).** The shortest P in R2 is 6 nodes longer than the shortest fair single reader (`(if (eq readn 4) (if (eq (probe3) 2) 4 1) 4)`
  with a two-node probe call against 6 nodes), the shortest O at least 14 nodes longer than the fair reader (two reads, two pattern
  tests, a fallback). So RE 4's R2 half ("within 3") fails its first clause and survives its falsifier (gap > 6 is the falsifier)
  if the gap is exactly 6. Falsifier of E5: P gap outside 5-8 or O gap below 12 under R2.
- **E6 (length-prior-shaped).** In the length-prior-shaped series (both allocations, all machines) no cell has V\* above 0.6 (queue 75's
  maximum was 0.41); P and O masses (exact-member lower bounds) are each below the fair single reader's under every machine. Falsifier:
  any cell above 0.6, or a P or O mass above the fair reader's.
- **E7 (seeded starts).** From the all-unequal start (bully + 1/3 constant, N = 200, delta = 0.03, beta = 3) no arm F, P, O recovers
  at entry hazard >= 0.25 (the unequal state is stable against every reader), and from the seeded fair start at beta = 0 each arm
  holds >= 0.8 fair at 120N. Falsifier: any recovery above 0.25, or a seeded-fair hold below 0.8.
- **E8 (F2 control).** The matched firm control F2 (extra unused read) has V\* within 0.1 of F's at every beta = 0 grid delta at
  N = 200 (double charges alone do not matter at the 0.1 price). Falsifier: a gap above 0.1 at two or more delta.

## Addendum: pilots after this file's first commit (disclosure; no verdict depends on them)

Step 0 assays (exact and Monte Carlo, `runs/bully_resist/step0_assays.json.gz`) were run after the first commit of this file and read
before the addendum: the class summaries of rho * N (FRI, FRC, UBI, BFI for firm readers, P_z, P_o, Q, O). The scoring rules above were fixed
before they ran and are applied unchanged. Dynamics timing and reproduction pilots (4 cells of the counted grid, deterministic, re-run
identically in the counted grid): F arm (delta 0.01, beta 1, N = 100, run 0) and (0.1, 3, 100, run 1), both identical to the stored queue-75 rows
(V1, 2 of 2); P (0.03, 3, 100, run 0) V* 0.0; O (0.03, 3, 100, 0) V* 0.0; PO (0.03, 1, 400, 0) V* 0.0; FPO (0.003, 3, 200, 0) V* 0.0. The
matched control F2 was added to the catalogue (K = 55, the first 51 programs unchanged: identical code, steps and charges on the 51 block).
Step-2 pilot (read before the counted step-2 runs): one run of the prudent search for machine R2 (the grammar of `lt_prior_br.py`, which was
being debugged) and its class table: the shortest spellings of P_z / P_o variants with timeouts not accepted are 12 nodes
(`(if (eq readn 4) (if (eq (probn 3) 2) 8 1) 8)`, mass about 10^-25 to 10^-24 against T+'s fair single reader's order 10^-11), the 'y' variants
28 nodes; the table-level collisions Qnzn = Pnzn, Qpzn = Ppzn, Fnzn = Snzn, Fpzn = Spzn (identical probe tables) were found there. This
pilot leaves E5 (R2 gap 6) as registered (the gap it shows is 6; RE 4's 'within 3' fails on it) and was not used to change any other
prediction. The counted step-2 runs (R0, R1, R2 searches; R2 enumeration and Monte Carlo) follow.

## Addendum: exploratory decomposition (registered before it runs)

Added after the step-0 holding configurations (which show 99% of islands that end unequal were unequal at 30N, and the tail is front-loaded: 98% of its dose is
delivered by 30N): arms F, P, O at beta = 3, N = 200, I = 64, delta in {0.003, 0.03}, with readers and bullies in the founders only (fm = 1, tm = 0) or in the tail
only (fm = 0, tm = 1), 20 runs. **E9.** In the F arm at delta = 0.03 the founders-only V\* is below the tail-only V\* (the founding scramble carries the loss).
Falsifier: tail-only V\* <= founders-only V\*. **E10.** P and O are within 0.15 of F's V\* in each of the four decomposition cells per delta (the arms differ in neither route).
Falsifier: any |V\*(P or O) - V\*(F)| above 0.15 in two or more of the eight comparisons.
