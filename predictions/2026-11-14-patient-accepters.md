# Predictions: patient accepters in arm T (queue 78), 2026-11-14

Spec: `specs/2026-11-14-patient-accepters.md` (reviewed by gemini-4-carbon then gpt-6.1-sol, folded). This file is committed
before step 0's assays, before any step-1 mass computation and before any counted step-2 cell. Verdicts go into
`runs/patient-accepters.md` against the rules below. All step-2 statistics are finite-schedule approach-rate statistics
(mN = 1, Λ = 100, 120N), not π.

## Pilot runs made before this file (disclosure)

- **Programs and gates (read).** The 59-program table (queue 76's 55 programs plus `Rnn`, `Rny`, `Rpn`, `Rpy`; `R<d><to>` reads
  partner d and otherwise names the other partner at 1/3) was built (31 s, 3 workers); `runs/patient_accepter/gates.{json,md}`.
  What I read:
  - V2 holds: the 55-block equals queue 76's table on code, steps, read timeouts, forfeits and joint codes (and the 31-block
    T+'s).
  - Action gate: R's action follows the rule in 3,481 of 3,481 profiles for each of the four variants (its read evaluated in
    R's own frame; a timed-out read is no offer for `n`, an offer for `y`). The read completes in 770 profiles and times out in 2,652
    (every reader partner); in the 3,372 no-offer profiles of an `n` variant the action equals the 1/3 constant's, with the
    constant's charge in 650 and an extra P_fail where the read timed out (2,652). The reference built from partners' tables
    agrees in 3,422 profiles, 0 disagreements, 59 ambiguous.
  - **Mutual-read gate: O and F cannot trigger R's `n` variants.** In a bully-held unequal island with R (matched orientation)
    as the victim, only the 1/2 constant naming R's slot (C4 for `Rn*`, C1 for `Rp*`) turns the island into the fair pair (R, X):
    3 of 3 triples each, 0 for every reader family. The `y` variants pair with any `y`-type reader, the bully and their own twins
    through mutual timeouts (Rny: 9 of 24 single-reader triples, 9 of 24 openers, 3 of 6 with a bully in the excluded slot).
  - **A finding I did not expect.** With R as the victim and *any reader* X in the excluded slot, the bully's read of R
    times out: R reads X, and X reads the bully or R, a mutual regress. The bully falls back to naming X at 1/2. For `Rnn` the island becomes
    the fair pair (bully, X) in 3 of 6 (B), 9 of 24 (single readers), 9 of 24 (two-partner readers), 9 of 24 (openers),
    6 of 12 (P_o) triples, and disagreement D in the rest. It is never the unequal outcome and never (R, X). So R makes the victim
    illegible to the bully whenever a reader is in the excluded slot: a third route out of the unequal island, through
    a fair pair that excludes R.
  - Nested reads over (R ∪ O ∪ F ∪ B)³: every profile contains a timeout (share 1.000), mean A_f charge per profile
    0.30–0.60, no forfeits; no unequal outcome among these profiles.
- No step-0 assay, no step-1 mass and no dynamics cell has been run or seen. Timing pilots of the step-2 kernel run after
  this commit use run indices outside the counted range (r ≥ 90) and are not reported as results.

## The spec's predictions, verbatim

- **RE 1 (neutral entry).** [after second review: scored by read class] Where R's read completes, R enters the victim's
  slot of a bully-held unequal island with ρ·N in [0.5, 2] (median); where it times out, ρ·N < 0.1. Falsifier: the
  completed-read median below 0.2.
- **RE 2 (the selected step).** [after second review: corrected] With R resident as victim, a ½ constant naming it
  entering the excluded slot has ρ·N ≥ 5; with that constant resident in the excluded slot, R entering the victim's slot
  has ρ·N ≥ 5; the first step of each route is neutral (ρ·N in [0.5, 2]). Falsifier: either selected step below 2.
- **RE 3 (unequal islands leave).** In the seeded all-unequal start, arm F+R has ≥ 0.3 of islands fair at 120N and
  F+O+R at least as many; F and F+C⅓ have ≤ 0.05. Falsifier: F+R below 0.1.
- **RE 4 (a threshold returns).** Arm F+R at β = 3, N = 200, I = 64, γ = 1 has δ\* ≤ 0.1 (full definition). Falsifier
  [after review]: no grid δ meets the full threshold definition. Counter-risk recorded: R also feeds bullies (it yields ⅓
  wherever no offer comes), so V\* could fall below F's.
- **RE 5 (cost without bullies).** At β = 0, N = 200, F+R's V\* at δ = 0.03 is within 0.1 of F's. Falsifier: lower by
  more than 0.2.
- **RE 6 (mass).** Under R1 the shortest R is within 2 nodes of the shortest fair reader, and its exact-member lower
  bound within a factor 10 of the bully's. Falsifier: more than 4 nodes longer.
- **RE 7 (length prior).** The length-prior-shaped law with R still reaches V\* ≥ 0.9 in no tested cell (junk and the
  constant law remain). Falsifier: any cell does.
- **RE 8 [after review] (R does not destabilize fair islands).** In the seeded all-fair start at β = 3, F+R holds at least
  F's share minus 0.1 at 120N. Falsifier: lower by more than 0.25.

Scoring notes (mine, fixed now): "the completed-read median" in RE 1 is over the matched-orientation `n`-variant assays into the
victim's slot whose third-slot program R's read completes against. The ½-offering third slots are excluded from RE 1's median because they are RE 2's
selected step; mismatched-orientation assays are reported separately. RE 2's "first step of each route" are (a) R (`n`, matched) into the victim
slot of (bully, ⅓ constant, C8) and (b) the ½ constant into the excluded slot of the same island. Each must lie in [0.5, 2]. The selected
steps use the same triples with the other member resident. RE 3 / RE 8 use the fraction of islands whose modal outcome is
fair at 120N, pooled over the 20 runs. RE 4 and RE 5 use mean V\* at 120N over 20 runs. "Holds" on a prediction with a range
means inside the range; a prediction that lands between its range and its falsifier is "fails, falsifier not fired".

## Counter-predictions (recorded, scored)

- **gemini-4-carbon (a):** RE 3 and RE 4 fail: F+R has < 0.3 of seeded-unequal islands fair at 120N and V\* < 0.5 at β = 3
  with no threshold. *Scoring:* true iff F+R's seeded-unequal fair share at 120N < 0.3 AND F+R (β = 3, N = 200, I = 64,
  γ = 1) has V\* < 0.5 at every grid δ AND no grid δ meets the full threshold definition. The stated reasons (slow neutral
  turnover; ⅓-yielders feed bullies in the scramble) are scored as "not contradicted" or "contradicted" from step 0's rates and
  the per-slot holders, not as part of the truth value.
- **gemini-4-carbon (b):** F+O+R is no better than F+R, because R and O time each other out. *Scoring:* true iff F+O+R's
  seeded-unequal fair share at 120N exceeds F+R's by at most 0.05 AND its V\* exceeds F+R's by at most 0.1 in every β = 3,
  N = 200, I = 64, γ = 1 cell. The mechanism clause is scored by the gate (R's read of O times out in every profile of the
  `n` variants: already true, disclosed above).
- **gemini-4-carbon (c):** every exit is triggered by a ½ constant, never by F or O. *Scoring:* on the seeded-start exit
  classification (all arms, β = 3), true iff every unequal-to-fair exit whose new fair pair contains R has a ½ constant as
  R's partner AND no unequal-to-fair exit's new fair pair contains a firm reader (single, two, F2) or an opener; false otherwise.
- **gpt-6.1-sol:** constants dominate direct triggers, but some exits are multistep (through intermediate replacements)
  or imported by migration, so carbon's (c) is too absolute. *Scoring (spec):* true iff on the exit classification a nonzero
  share of local exits involves F or O at some step, or a nonzero share of exits is imported.

## My predictions (E), with falsifiers

The numbers below use the gate disclosed above. Exact Moran values at N = 200, w = 0.3: Δ = ½ gives ρ·N = 27.9, Δ = ⅙ gives 9.75,
Δ = 0 gives 1.

- **E1 (step 0 item 1, by read class).** Matched `n` variants into the victim slot: every completed-read, non-offering
  third slot gives ρ·N = 1 exactly (identical play, no charge). Every ½-offering third slot (C4 for `Rnn`, C1 for `Rpn`) gives
  ρ·N in [8, 12]. Every timed-out third slot gives ρ·N < 0.01: R pays P_fail and the bully abandons it. Mismatched orientation:
  ρ·N < 0.01 everywhere. Falsifier: a completed-read non-offering assay off 1 by more than 10⁻⁶, or a timed-out assay above 0.1.
- **E2 (item 2).** With R resident as victim and C8 in the excluded slot, the ½ constant naming R enters the excluded slot
  at ρ·N in [20, 35]. Readers (single, two, F2, O, P) entering the same slot have ρ·N > 3 in at least a quarter of their
  assays: they form the fair pair with the bully, ½ against 0 minus at most 0.2 in charges. In the rest they have ρ·N < 0.1 (D).
  Falsifier: no reader assay above 3, or the ½ constant below 10.
- **E3 (item 3).** With the ½ constant resident in the excluded slot, R (`n`, matched) into the victim slot has ρ·N in
  [8, 12]. Falsifier: outside [5, 15].
- **E4 (item 4).** A bully entering a fair (R, ½-constant) island has ρ·N ≤ 1 in every slot. A ⅔-demander entering the excluded slot
  of such an island has ρ·N ≤ 1 (R does not re-yield while its partner still offers). R entering a pair slot of a fair firm-reader
  island has ρ·N < 0.01. In the unpaired slot ρ·N ≤ 1 (a shadow at best, minus its read charge). Falsifier: any of these above 3.
- **E5 (seeded unequal start, 120N).** F+R has 0.01–0.2 of islands fair, so RE 3 fails. F+O+R and R only are within 0.1 of F+R.
  F and F+C⅓ have ≤ 0.05. Falsifier: F+R ≥ 0.3 (RE 3 holds), or F+R exactly 0 in all 20 runs.
- **E6 (exit routes).** Among classified local exits from unequal to fair on the seeded-unequal runs, at least 70% end in the pair
  (R, ½ constant). Transient fair (bully, reader) episodes occur in at least one run of F+R or F+O+R; fewer than half of them last to 120N.
  Falsifier: fewer than 50% of local exits end in (R, ½ constant), or no exit at all occurs in any arm.
- **E7 (main grid).** F+R at β = 3, N = 200 has no threshold (RE 4 fails), and its V\* is within 0.15 of F's at every δ. Across the
  γ = 1 grid (all arms, β ∈ {1, 3}, N ∈ {100, 200, 400}) at most one (arm, β, N) has a threshold. Falsifier: F+R at β = 3,
  N = 200 above F by more than 0.3 at some δ, or three or more (arm, β, N) with thresholds.
- **E8 (γ).** At N = 200, |V\*(γ = 3) − V\*(γ = 0.3)| ≤ 0.15 in every cell of F+R, F+O+R and F+C⅓. Falsifier: any cell differs by
  more than 0.3.
- **E9 (β = 0).** F+R's V\* is at least F's minus 0.1 at every grid δ at N = 200 (RE 5 holds). Falsifier: lower by more than 0.2 at
  any δ.
- **E10 (mass).** Under R1 the shortest `n` R has 6 nodes, the same as the shortest fair single reader. The exact-member lower bound of
  the `n` variants is between 0.2× and 5× the bully's (same shape, different literals). Under R0 the shortest R is within 2 nodes
  of the shortest fair reader (12). Falsifier: R1 shortest R > 8 nodes, or the ratio to the bully outside [0.1, 10].
- **E11 (length prior).** No length-prior-shaped cell reaches V\* ≥ 0.9 (RE 7 holds). The largest cell mean is ≤ 0.45. Falsifier: any cell
  above 0.6.
- **E12 (R against the ⅓ constant).** On islands where both are present at 120N (F+R, β = 3, δ = 0.03, N = 200), R's mean
  per-capita payoff is within [−0.03, +0.01] of the ⅓ constant's in the same slot. Falsifier: R above the constant by more than 0.05.
- **E13 (who is the victim).** In F+R at β = 3, δ = 0.03, N = 200, at most 0.15 of the unequal islands at 120N have R as the
  victim's dominant program. Falsifier: more than 0.3.
- **E14 (seeded fair start).** All five arms hold ≥ 0.7 of islands fair at 120N. F+R is within 0.1 of F (RE 8 holds).
  Falsifier: F+R below F by more than 0.25.
- **E15 (carbon and sol).** Carbon (a) true; carbon (b) true; carbon (c) false or vacuous (no exits); sol true if any exit
  occurs. Falsifier: carbon (a) false.
