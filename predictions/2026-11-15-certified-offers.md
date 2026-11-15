# Predictions: certified offers in majority division (queue 79), 2026-11-15

Spec: `specs/2026-11-15-certified-offers.md` (reviewed by gemini-4-carbon, then gpt-6.1-sol `--mode amended`, both folded). This file
is committed before any step-0 assay, before any step-1 mass and before any counted step-2 cell. Verdicts go into
`runs/certified-offers.md` against the rules below. All step-2 statistics are finite-schedule approach-rate statistics (mN = 1,
Λ = 100, 120N; seeded starts to 240N), not π.

## What was run and seen before this file (disclosure)

- **Design and soundness argument** (`notes/certified-offers.md` §1, committed 615ff52 before the gates). The certificate is a
  three-bit literal bound to code by a skeleton: a carrier's body is `CARRY cert fb me n p`, a shared library combinator; the check
  `CHK` accepts exactly that skeleton. κ = 50 ticks (C1); C0's written-out check costs 167–168 steps on carriers.
- **Gates** (`runs/certified_offers/gates.{json,md}`, K = 87; built in 48 s (C1) and 59 s (C0) with 3 workers). What I read:
  - G1: the check map is identical in C0, C1 and the host reference on all 95 programs and forgers; all eight forgers are rejected
    (including the bully body carrying Ocp's certificate data in milestone 4's shape, a lookalike combinator, swapped variables, a
    non-value fallback, malformed and computed certificates, the skeleton under `if T`). Over the cube, 95,000 certified-branch
    profiles in each machine, **0 false**. In 448 of 116,932 fallback profiles the fallback's play differs from its standalone
    table, because inside a carrier the fallback's `me` is the carrier's quote (partners that read it see the carrier).
  - G2: every pointing pair (Oc×Rc, Oc×Fc, Fc×Fc, Rc×Rc, Fc×Rc, Pc×Pc, and Rcs, Bc pairs) is the fair pair in every seat pattern
    with every non-carrier third slot, with 0 timed-out reads by the pair (both machines). Three-carrier triples ((Fc)³, (Pc)³,
    (Bc, Fc, Fc)): non-fair share exactly 0.25 (the all-next and all-prev orientations), mean gross payoff per slot 0.25 against
    1/3 for a cycle-free rule.
  - G3: with Rc (matched) as victim the simulating bully's read completes beside every excluded-slot program (0 timeouts); the island
    becomes the fair pair (victim, e) beside Fc, Pc, Bc and the matched Oc, Rc, Rcs, and stays unequal otherwise. Queue 78's R as
    victim reproduces queue 78's illegibility table. **With the certified bully Bc holding the island**, any carrier in e that points
    at the bully pairs with it: Fc in e gives F(b, e) in 24 of 48 triples and F(v, e) in 24 (Fc's preference decides), Oc in e pairs
    with Bc or with Rc by orientation.
  - G4: every timed-out read in a triple with a carrier and a simulating reader persists with every cap and the root fuel ×20
    (0 cap exhaustions in every sampled group): the timeouts are the mutual regress, through the fallbacks of Fc, Bc, Pc and Rcs.
    Pure Oc and Rc never time out.
  - G5: the first 59 programs' tables equal queue 78's. V3: C1 and C0 agree on every action over the cube (658,503 profiles); 856
    profiles differ in a read's timeout (charges only), 0 outcome triples differ.
- Two hand evaluations of single triples and one timing row per program type (disclosed in the notes). No step-0 assay, step-1
  mass or dynamics cell has been run. Timing pilots of the step-2 kernel run after this commit use run indices ≥ 90 and are not
  reported as results.

## The spec's predictions, verbatim

- **RE 1 (the regress goes).** Every pointing carrier pair in gate 2 gives the fair pair with no timed-out read.
  Falsifier: any pointing pair times out or disagrees. (Three mutually pointing carriers may cycle; not scored.)
- **RE 2 (legibility).** [after review: stated for the pure Rc] With Rc as victim the simulating bully's read of it
  completes beside every excluded-slot program, and Rc's entry into the victim's seat has ρ·N in [0.5, 2] wherever
  its certificate stays inactive (constants, simulating readers, carriers not pointing at it); [after second review]
  beside a carrier that makes it eligible Rc activates and its entry is selected (ρ·N ≥ 5). Falsifier: ρ·N < 0.1 beside any of them. For Rcs the queue 78 pattern
  returns beside simulating readers (ρ·N < 0.1) and not beside carriers.
- **RE 3 (certified offers are selected).** With Rc resident as victim, Oc and Fc entering the excluded slot have
  ρ·N ≥ 5. Falsifier: below 2.
- **RE 4 (the faker rides along).** Bc enters fair carrier islands' pair slots at ρ·N ≤ 1.5 and is not excluded by any
  carrier; on (Fc, Bc) islands a ⅓ constant entering the third slot is not selected, but Bc's own unequal island resists
  Rc-then-offerer exactly as the simulating bully's does. Falsifier: carriers exclude Bc (ρ·N < 0.1 in a pair slot).
- **RE 5 (seeded unequal start).** Fc+Oc+Rc has more fair islands at 120N than queue 78's F+R (0.05) but below 0.3;
  the two-step pacing still binds. Falsifier (in the direction of the RS's program): ≥ 0.3. Falsifier (other side):
  ≤ 0.05, i.e. no gain from legibility at all.
- **RE 6 (no threshold at β = 3).** No certified arm has δ\* ≤ 0.1 at β = 3, any N, φ = ½. Falsifier: one does.
- **RE 7 (a threshold at β = 1 is possible).** The main arm's V\* at β = 1, N = 200, δ = 0.1 exceeds queue 78's
  F+O+R by at least 0.15. Falsifier: within 0.05 or lower.
- **RE 8 (the scramble).** At least 0.8 of islands in the main arm have their 120N outcome by 30N. Falsifier: < 0.6.
- **RE 9 (β = 0).** Certified arms cost nothing without bullies: V\* at δ = 0.03 within 0.1 of F's. Falsifier: lower by
  more than 0.2.
- **RE 10 (mixed worlds).** [after review: revised; carbon's point that pure carriers are legible to simulating
  readers is accepted] The mixed arm's V\* lies between its two pure arms' (within 0.05 outside). Falsifier: below the
  lower by 0.15 or more (sol's counter: outside both, especially lower; the claim is exploratory). The RE's first draft said "at or below the lower"; recorded.
- **RE 12 [after review] (cycles are not the story).** The mean payoff of (Fc, Fc, Fc) over orientations is ¼ of a
  slot's fair share lower than a cycle-free rule would give (2 of 8 triples cycle), and at β = 0 the Fc arm's V\* at
  δ = 0.1 is within 0.1 of F's. Falsifier: lower by more than 0.2, in which case Fc's failures under bullies cannot
  be read as scramble or pacing without a cycle-free control.
- **RE 11 (mass).** Under C1 the shortest Oc and Rc are within 4 nodes of the shortest fair reader; under C0 every
  carrier is more than 100 nodes. Falsifier: C1 gap above 8 nodes.

### Scoring rules for the RE predictions (fixed now)

- ρ·N is step 0's exact birth–death value at N = 200, w = 0.3, A_f charges. "Beside" a program X means X resident in the
  excluded slot; RE 2's Rc rows are the matched orientation (Rcn with Bn, Rcp with Bp) over all three rotations; "inactive" is
  decided by the certificates (X does not point at the victim's slot). RE 2 is scored on medians per excluded-slot class and on the
  minimum for the falsifier.
- RE 3: Fc (all 16) and the matched Oc; the mismatched Oc is reported, not scored. RE 4's clauses are scored separately; the third
  clause ("resists ... exactly as") is scored as: Fc and Oc into e of Bc's unequal island without a resident Rc have ρ·N within
  0.2 of the same entry into the simulating bully's island, and with Rc resident within 20%.
- V\*: the share of islands whose 120N modal outcome is in V\*, bootstrap over runs (queue 78's statistic). δ\*: queue 78's full
  definition (the smallest grid δ with V\* ≥ 0.9 at that δ and every larger grid δ). "Queue 78's F+O+R" and F are the stored rows.
- RE 5: the 120N fair share of the seeded all-unequal start (simulating bully), φ = ½, Fc+Oc+Rc.
- RE 8: share of islands, pooled over the main arm's cells at β = 3 (all δ, N, I = 64, φ = ½), whose 120N modal class equals the
  30N one. Also reported per β.
- RE 9: the certified arms at β = 0, N = 200, δ = 0.03 against stored F; RE 12's dynamic clause: Fc at β = 0, N = 200, δ = 0.1.
- RE 10: the mixed arm against Fc+Oc+Rc (certified pure) and F+O+R (stored simulating pure) at β ∈ {1, 3}, N ∈ {100, 200}, each δ;
  scored on the mean over cells of the signed distance outside the interval, and the falsifier on any cell's mean below the lower
  by ≥ 0.15 with bootstrap intervals not overlapping.
- RE 11: shortest node counts of the canonical spellings under the three step-1 measures (C1: R1 plus a `carry` tag; R1 with the
  skeleton written with `lib CARRY`; C0: the library inlined), as defined in the notes before step 1 is computed.

## The engineer's predictions (E), made after reading the gates, before any assay or cell

- **E1 (inactive entry is exactly neutral).** Rc entering the victim's seat of a simulating-bully-held unequal island beside any
  excluded-slot program that does not point at it has ρ·N = 1 to 10⁻⁶ (its play, steps aside, and its charges equal the ⅓
  constant's), including beside simulating readers where queue 78's R had 1.4·10⁻¹⁰. Falsifier: any such edge outside [0.99, 1.01].
- **E2 (the two selected steps).** With Rc resident, Fc and the matched Oc into e: ρ·N = 27.9 ± 0.2; with a pointing carrier resident
  in e, Rc into v: 9.75 ± 0.1 (the ½ − ⅓ gain, no charges). Falsifier: either below 5.
- **E3 (the certified bully's island is fragile).** In Bc's unequal island (Bc on ⅔ with a ⅓ constant), a carrier pointing at Bc
  (Fc, Pc, Bc, the Oc oriented at Bc) entering e without any Rc has ρ·N ≥ 20 and fixes into a fair pair containing Bc. This
  contradicts RE 4's third clause. Falsifier: ρ·N < 5.
- **E4 (Bc is neutral in fair carrier islands).** Bc entering a pair slot of (Fc, Fc, ·) or (Rc, Oc, ·) fair islands: ρ·N = 1 ± 0.01;
  a ⅓ constant into the third slot of (Fc, Bc, ·): ρ·N = 1 ± 0.01. Falsifier: any of these outside [0.5, 2].
- **E5 (the certified bully's seeded start opens).** From the all-unequal start with Bc as the bully at φ = 1, the fair share at 120N
  is ≥ 0.5 in Fc, Fc+Oc+Rc and Fc+Rc; with the simulating bully (φ = ½) it is ≤ 0.15 in the same arms. Falsifier: Bc start < 0.3
  in any of the three arms, or the simulating start > 0.3.
- **E6 (φ).** In the main arm at β = 3, N = 200, δ = 0.1, V\*(φ = 1) − V\*(φ = 0) ≥ 0.2. Falsifier: < 0.05.
- **E7 (pacing explains the simulating-bully null).** In the seeded all-unequal start (simulating bully) of Fc+Oc+Rc and Fc+Rc, the
  number of observed local Rc-route completions (v and e taken by Rc and a certified offerer on the island) agrees with the
  prediction from step 0's exact rates and the realized arrival counts within a factor 3 (or both ≤ 3). Falsifier: observed above 3×
  predicted and above 3.
- **E8 (Fc at β = 0).** At β = 0, N = 200, the mean over the five δ of V\*(Fc) − V\*(F) ≥ 0. Falsifier: ≤ −0.1.
- **E9 (the cycle-free comparator).** Fc\* − Fc, mean over the five δ at N = 200, is within 0.05 at β = 0 and β = 3. Falsifier: Fc\*
  higher by ≥ 0.15 at either β.
- **E10 (the hybrid).** In the seeded all-unequal start (simulating bully, φ = ½), Fc+Oc+Rcs's 120N fair share is at least
  Fc+Oc+Rc's minus 0.05. Falsifier: Fc+Oc+Rc higher by > 0.1.
- **E11 (the ablation control).** Fc+Oc+C⅓ and Fc+Oc+Rc have V\* within 0.1 of each other at every grid δ at β = 3, N = 200, φ = ½
  (Rc's certificate buys nothing at the population level when bullies simulate). Falsifier: Fc+Oc+Rc higher by ≥ 0.2 at some δ with
  non-overlapping intervals.
- **E12 (mass, C1 `carry` tag).** Under the C1 measure the shortest Oc and Rc are at most as long as the shortest fair single reader
  and the shortest Fc is at most 6 nodes longer; under R1 with the skeleton written out every carrier is at least 12 nodes longer
  than the fair reader. Falsifier: C1 Oc longer than the fair reader, or R1-written gap below 8.
