# Predictions: legitimate detectors (a grudge rule for gentle source-readers), 2026-10-17

Spec `specs/2026-10-17-legitimate-detectors.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the amendments supersede
the earlier text). Notes `notes/detectors.md` §1 (committed before any code, ed7400d). Written and committed before any
code of this run and before any counted cell. ε = 0 cells are lottery statistics at finite (N, I, horizon); tail cells
are finite-ε diagnostics, never π.

*Disclosure.* Notes §1.1 found by table lookup that the spec's premise does not hold in the stored ecology (L): the
detector's first D step writes an opponent-generic self-hypothesis defection, so it defects against every distinct
quote except check-timeout units (a near-identity clique), and a grudge adds nothing. The run therefore uses the keyed
world K (notes §1.3, deviation 1): hypothesis-closed D certificates are keyed to the partner they were produced against.
In K the detector is predicted to be a gentle member of PrudentBot's network rather than a rival. The RS's and RE's
statements below were written for the spec's premise; they are registered verbatim and scored as worded on the cells
as amended, with the conventions stated after them.

## The RS's statements (verbatim, registered first)

> Detectors seem like a perfectly legitimate network in and of themselves- in fact, they're even gentler than
> prudentbot! They're exploitable, so if we wanted to keep em around we'd need em to evolve certificates that
> predators detect. Worth an experiment imo

> "Outnumbered networks die" makes me worry we're rigging the odds - "good reasons" to kill off network factor thru
> dynamics in robust ways.

**RS decision (2026-10-17, relayed by the RE before any cell):**

> I'd call prudence a good reason, proportionate to the presence of suckers, which is itself a live modeling decision
> by way of mutation rate / schedule

Scoring consequence (the RE's instruction): removals labelled *prudence premium* are reported with the sucker exposure
that paid for them (unconditional-cooperator encounters and island-generations, by cell and schedule); good-reason
removals (predation, inefficiency, prudence premium) are split from abundance removals in the headline; the
head-to-head cell B1 runs at the tail rates K ∈ {0, 1, 3} to show how the premium scales with the sucker supply.

## The RE's predictions (verbatim from the spec, with the revision marks)

1. **The grudge rule cuts predator establishment** [revised after review: with vertical-only inheritance a predator
   meets O(N) unmarked detectors]: with vertical inheritance alone establishment falls by at most half at N = 800; with
   horizontal copying of grudges among detectors it falls to ≤ 0.05 at both N. *Falsifier:* horizontal copying ≥ 0.15.
2. **No unjustified grudges** [revised after review: scored against encounter traces]: every grudge is written after
   a defection that actually occurred, and no grudge is ever written between two programs that cooperate with each other
   in every reachable certificate state. *Falsifier:* any unjustified grudge.
3. **At equal mass without a tail the winner is a coin flip by abundance** (detector wins in 0.3–0.7 of runs, causes
   labelled abundance) with or without the grudge rule. *Falsifier:* outside [0.2, 0.8].
4. **With the tail and no grudge, PrudentBot wins by predation** (≥ 0.8 of runs, most detector removals labelled
   predation); **with the grudge, back to near a coin flip**. *Falsifier:* PrudentBot ≤ 0.6 without the grudge, or
   ≥ 0.9 with it.
5. **At natural prior shares PrudentBot wins by abundance and prudence premium** (its seed mass is larger and it feeds
   on unconditional cooperators the detector spares), whatever the grudge rule. *Falsifier:* detectors win ≥ 0.3 of
   natural-share runs.
6. **Counter-predictions registered.** *Sol:* protection depends on inheritance coverage, encounter rate and source
   diversity, not a universal bound; outcomes are path-dependent rather than coin flips; tail predators removing
   detectors would not make PrudentBot a predator. *Gemini:* with vertical-only inheritance establishment stays ≥ 0.15
   at N = 800; with the tail and grudges PrudentBot still wins ≥ 0.75 of runs, removals shifting from predation to
   prudence premium (the tail feeds it unconditional cooperators).

## Scoring conventions (declared now; they do not change the wording above)

Definitions are notes §1.4–§1.7 (world K; DET and PBN; removal events and cause labels; winner). Two conventions are
fixed here because DET is a small family:
- **Network removal in a merged population** is *extinction*: no individual of the network's spellings remains at the
  horizon (or at the first checkpoint where that holds). §1.5's "< 0.01 sustained" applies only to a network whose peak
  share after the merge was ≥ 0.05. A run's **winner** is the network that removed the other; if neither is removed, the
  run is *coexistence* (no winner).
- "Detector" = DET, "PrudentBot" = PBN, in every RE and counter-prediction clause.

- **RE 1** (Part A, pooled over the top-3 predators): *supported* if KG's establishment at N = 800 is ≥ 0.5 of K0's
  ("falls by at most half") and KGh's is ≤ 0.05 at N = 200 and N = 800; *contradicted* if KGh ≥ 0.15 at either N
  (the falsifier); *partly* otherwise, with each clause reported.
- **RE 2** (every grudge in every cell): *supported* if every logged write followed a defection by the target in that
  encounter's play (the write trigger) and no write targets a spelling whose units are mutual with the writer's unit in
  every pair of their states reachable in the run's universe (E, natural, and every unit of the two run trees present in
  the K closure); *contradicted* by any such write. Bootstrap grudges (written while the writer was uncertified, against
  a spelling mutual with the writer's natural unit) are reported separately and are not unjustified under the wording.
- **RE 3** (B1, ε = 0, K0 and KG separately): fraction of runs DET wins, over 20. *Supported* if in [0.3, 0.7] with
  most of DET's wins' removals labelled abundance; *contradicted* if outside [0.2, 0.8] (coexistence counts as not a DET
  win); *inconclusive* in between.
- **RE 4** (B1 at K = 1): PBN-win fraction under K0 and under KG; *supported* if K0 ≥ 0.8 with most DET removals
  labelled predation and KG in [0.3, 0.7]; *contradicted* if K0 ≤ 0.6 or KG ≥ 0.9; *inconclusive* otherwise.
- **RE 5** (B2, both arms, both schedules pooled): *supported* if DET wins < 0.3 and PBN's wins carry abundance or
  prudence-premium labels; *contradicted* if DET wins ≥ 0.3; the cause clause reported separately.
- **Sol:** (i) protection varies with coverage (KG vs KGh vs KGp, N) rather than one bound: *held* if the ordering
  KGp ≤ KGh ≤ KG ≤ K0 holds with KG varying by ≥ 0.05 across N; (ii) path dependence: *held* if B's outcomes are not
  coin flips (DET-win fraction outside [0.3, 0.7] or coexistence ≥ 0.5); (iii) tail predators removing detectors are not
  PBN predation: *held* if no DET removal is labelled predation with a PBN type as the exploiter.
- **Gemini:** (i) KG at N = 800 ≥ 0.15; (ii) B1 at K = 1 with KG: PBN wins ≥ 0.75 and the removals' labels shift from
  predation (K0) to prudence premium (KG). Each clause scored separately.

## My predictions (with falsifiers)

D1. **The gate passes.** On ≥ 200 sampled existing checks the extended checker returns the same value with the same
    step count (zero differences); every gate certificate the checker accepts has a true atom; forged grudges on
    non-readers and negated readers are rejected; the L detector (unit 544) plays D against CooperateBot by execution.
    *Falsifier:* any difference in (g1), or any accepted false atom (then no cell runs).

D2. **In K the canonical detector is a member of PrudentBot's network.** Its natural unit is mutual with FairBot-H,
    PrudentBot-H and CooperateBot-H and defects against DefectBot-H; it is in 𝒯_K. *Falsifier:* PrudentBot-H defects
    against it in K.

D3. **Its predators in K weigh far more than L's timeout predators.** The accessible predator mass of the K detector
    (removing-rivals classifier on K tables, target holders FairBot-H and PrudentBot-H) is ≥ 0.02 (L: 0.0057).
    *Falsifier:* < 0.01.

D4. **Predator assays** (pooled top-3, per N): K0 establishment in [0.18, 0.34] at N = 200 and 800; KG ≤ 0.10 at
    N = 200 and ≤ 0.18 at N = 800, below K0 at both; KGh ≤ 0.05 at both; KGs within 0.06 of K0; KGp ≤ 0.03.
    *Falsifier:* KG ≥ 0.18 at N = 200, or |KGs − K0| > 0.10.

D5. **Second arrivals** (N = 200): under KG and KGh an exact-source second arrival establishes at ≤ 0.5 of the synonym's
    rate, and the synonym is within 0.08 of the first-arrival rate of its arm. *Falsifier:* exact ≥ synonym.

D6. **Retaliation scaling:** KG establishment rises with N (200 < 800 < 3,200 in point estimates) toward K0; KGh stays
    ≤ 0.08 at 3,200. *Falsifier:* KG at 3,200 ≤ KG at 200.

D7. **Head-to-head at equal mass is coexistence, not a contest.** In every B1 cell (K0, KG; K = 0, 1, 3) neither network
    is removed in ≥ 16 of 20 runs, and DET's share at 10,000 has its run median within [0.3, 0.7]. *Falsifier:* a
    removal in ≥ 8 of 20 runs of any B1 cell.

D8. **The tail's sucker supply in B1 is too small to price prudence.** Prudence-premium removals in B1: 0 at K = 1 and
    ≤ 2 of 20 at K = 3; sucker exposure rises about threefold from K = 1 to 3 (it is 0 at ε = 0, where B1 has no
    suckers). *Falsifier:* ≥ 5 prudence-premium removals at K = 3.

D9. **At natural shares (B2)** neither network is removed in ≥ 14 of 20 runs per cell; when DET goes extinct its window
    is labelled abundance (drift of a minority inside one network). *Falsifier:* DET wins ≥ 6 of 20 in any B2 cell.

D10. **Natural seeds: detectors are paid for in the scramble, then drift.** In C fission–fusion (K0 and KG, ε = 0) DET
     goes extinct by 10,000 in ≥ 15 of 20 runs; DET's share falls between the seed and the merge by more than PBN's
     (relative), with the prudence premium positive in that phase (sucker exposure reported); the extinction windows are
     labelled abundance in ≥ 0.7 of extinctions. *Falsifier:* DET extinct in ≤ 8 of 20, or prudence-premium labels on
     ≥ 0.5 of extinctions.

D11. **K is at least as universal as L.** Universal-open at 10,000 in C under K0 is ≥ L's minus 2 runs on fission–fusion
     and ≥ L's on (200, 64) (K removes a 0.03-mass family of near-cliques and adds gentle members). *Falsifier:* K0 below
     L by ≥ 4 runs on either geometry.

D12. **Grudges change little at ε = 0 on natural seeds.** KG − K0 universal-open within ±3 runs on both geometries;
     KGh and KGs within ±3 of KG on fission–fusion. *Falsifier:* |KG − K0| ≥ 6.

D13. **Grudges are cheap and mostly bootstrap.** In C (KG, ε = 0) the mean grudge list of living writers is ≤ 1.5 keys,
     ≥ 0.5 of all writes are bootstrap grudges (against spellings mutual with the writer's natural unit), and the
     verification steps of a detector check grow by < 2× from 0 to 3 grudges (gate g8). *Falsifier:* bootstrap share
     < 0.2, or ≥ 2× steps at 3 grudges.
