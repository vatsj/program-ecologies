# Spec: patient accepters: a victim that keeps ⅓ while waiting for an offer of ½, 2026-11-14

Status: reviewed by gemini-4-carbon (RS, 2026-11-14: carbon replaces argon; folded [after review]); and by
gpt-6.1-sol (`--mode amended`, folded [after second review]); run by an Opus subagent (RS, 2026-11-14) on Daytona. Queue 78. The RS (2026-11-09):
"shouldn't there be some programs who accept 1/3 but are waiting for an offer of 1/2? This objects to the constant 1/3,
since only compute and prior mass select out a program that reads in an attempt to negotiate 1/2"; "Go for it".

## Context

Queue 76 (RESULTS "Bully-resistant readers in arm T"): under Trojan bullies (β = 1, 3 per reader) no reader arm (firm F,
prudent P, opener O, F+O, ...) has a reader-share threshold for V\* ≥ 0.9. The unequal island (a bully on ⅔ with a
⅓-naming constant, 89–98% of unequal islands) strongly resists single-slot entry: a firm reader entering the victim's
slot abandons the ⅓ deal and gets 0 (ρ·N ≈ 10⁻¹⁰); an opener in the excluded slot offers ½ to a constant that cannot
answer. From a seeded all-unequal start no island was fair at 120N in any arm.

**The RS's program, the patient accepter R.** Read the excluded slot e (from the victim's seat: the slot that is not my
current partner). If e names me at ½, name e at ½; otherwise name my partner at ⅓. On path in a bully-held island it is
identical to the ⅓ constant it replaces, so it should enter neutrally (only prior mass and the A_f charge select
against it; reading a constant does not time out). [after second review: the two orders] R plays its response at once (it is not a later mutation), so there are two
routes, each one neutral step and one selected step: *R first*, R enters the victim's slot neutrally and an offerer
(a ½ constant naming that slot) entering the excluded slot is then selected (it gets ½ instead of 0); *offerer first*,
the offerer enters the excluded slot neutrally (0 either way) and R entering the victim's slot is then selected (½
instead of ⅓). Either way the island becomes a fair pair, the route the Theory tab gives for V\*'s external stability, one slot at a time. Under R1 it is about
6 nodes, `(if (eq readn 4) 1 3)`-shaped, the size of a fair reader or a bully.

REJECTED.md checked. Does not re-open queue 76's arms; R is a new family (a ⅓-accepting reader, which none of F, P, O
is). The RE's dropped conjecture "readers feed bullies by yielding ⅓" is relevant: R does yield ⅓, by design; whether
that feeds bullies is measured (RE 4).

## Programs (over queue 76's catalogue: T⁺ ∪ P ∪ O, `src/bully_resist*.py`, `src/tplus.py`)

- **R** (patient accepter): four variants by which partner is "current" (next or prev; the other is read) and by
  timeout convention on the read (`y`: a timed-out read counts as an offer; `n`: it does not). Main arm: the two `n`
  variants.
- **Control C⅓**: the ⅓-naming constants at the same mass (no read), to separate "a victim that can answer" from "more
  victims".
- [after review] **Mutual reads.** R reads the excluded slot; an opener O and a firm reader F read others too. Where R
  and its offerer read each other, both reads time out (the mutual regress of milestone 3 and of queue 76's nested-reads
  gate), R's `n` variant does not switch and both pay P_fail. So R may be triggerable only by non-reading offerers (½
  constants naming its slot). The gate reports, for R against each of O, F, the bully and the ½ constants in the read
  slot: whether R's read completes, what R plays, and the charges. If O and F cannot trigger R, that is a finding, not a
  defect; the arms are run as specified and the exit sequences say who made the offer.
- Gates [after second review: actions, read status and charges gated separately]: R's *action* equals the ⅓ constant's
  wherever its bounded read does not return an offer of ½ (a timed-out read is no offer for `n`, an offer for `y`), and
  names the offerer at ½ wherever it does; read status and A_f charges are tabulated beside the actions (they differ
  from the constant's wherever the read times out); nested-read report on (R ∪ O ∪ F ∪ B)³ (timeouts, A_f charges, R with R, R
  with O, R with a bully in the read slot); the T⁺ ∪ P ∪ O block unchanged.

## Step 0: assays (exact, as queue 76's step 0; A_f charges included; neutral-label controls)

1. R into the victim's slot of each bully-held unequal island (bully + ⅓ constant + each third-slot program): ρ·N,
   [after review] reported separately for third-slot programs R's read completes against (constants, clean readers:
   expected neutral) and those that time it out (expected ρ·N ≪ 1 from the 0.1 charge).
2. With R resident as the victim: an opener O, a ½ constant naming the victim's slot, and a firm reader, each into the
   excluded slot: ρ·N, and the resulting outcome when it fixes.
3. With the offerer resident: R into the victim's slot (the selected step).
[after second review] Every edge is an exact frequency-dependent fixation probability for a named resident triple,
invader and slot (both R orientations, all three role rotations); per-mutant fixation is reported separately from
prior-weighted establishment rates (fixation × arrival mass).
4. Reverse: a bully into a fair island whose pair includes R; a ⅔-demander into an island where R pairs fairly (does R
   re-yield?); R into a fair firm-reader island (does it shadow?).

## Step 1: length-prior mass

Queue 75/76's machinery, machines R0, R1 (and R2-machine only if the probe tag is needed, which it is not for R): the
exact-member lower bound and shortest spelling of R, its ratio to the fair single reader, the bully and the ⅓ constants;
the Monte Carlo upper bound.

## Step 2: dynamics (queue 76's simulator; mN = 1, Λ = 100 from the founding law, 100N + 20N, CRN, 20 runs per cell)

Law as queue 76: constants at T's main proportions, bullies at βδ, exploiters at their ratio, readers at δ split by arm;
R is added at mass γδ (γ ∈ {0.3, 1, 3}), taken from the constants.

| arm | reader share δ | plus |
|---|---|---|
| F (control; queue 76 rows) | firm | – |
| F+R | firm | R at γδ |
| F+O+R | half firm, half openers | R at γδ |
| F+C⅓ (control) | firm | extra ⅓ constants at γδ |
| R only | none (δ counts R) | – |
| F/R split [after review] | δ/2 firm, δ/2 R (total reader mass matched to F) | – |

Grid: β ∈ {1, 3}; δ ∈ {10⁻³, 3·10⁻³, 10⁻², 3·10⁻², 0.1}; γ = 1 on the full grid, γ ∈ {0.3, 3} at N = 200 only;
N ∈ {100, 200, 400}; I = 64; I = 256 at N = 200 for F+R. β = 0 rows for F+R at N = 200 (does R cost the fair state
without bullies?).

**Seeded starts** (N = 200, I = 64, δ = 0.03, β = 3, the decisive test) [after second review: exact triples]: unequal:
every island monomorphic on (bully `Bn` in slot 0 on ⅔, the ⅓ constant naming slot 0 in slot 1, excluded slot 2 holding
C8 = (ALL, ⅔), a non-offering constant), and the two rotations of it on a third of the islands each; fair: (½ constant
naming slot 1, ½ constant naming slot 0, C8), rotated likewise. Founders are identical across arms; arms differ only in
the tail law. Arms F, F+R, F+O+R, F+C⅓, [after review] and R only (are ½ constants plus R
enough, with no firm readers?). Report the fraction of islands fair at 30N, 120N and
240N, the exit hazard from unequal islands, and by which sequence (R entered the victim slot, then which offerer).

[after second review] The normalized founding and tail law of every arm and cell is published; F+R and F+C⅓ differ only
in the substituted family (same donor mass from the same constants, same slots). Add the β = 0 F rows as RE 5's
comparator (reuse queue 76's where identical). The run log records the resident triple before and after every
successful invasion on the seeded-start islands, transient fair episodes included, and classifies each exit from an
unequal island as local (R then offerer, offerer then R, other) or imported (a migrant replaced the pair). All of this
is approach-rate evidence at N = 100–400 and 120N; it is not asymptotic stability.

**Length-prior-shaped series:** as queue 76's, with R at its measured mass ratio to the fair reader, both allocations,
machines R0 and R1, N = 200 and 400.

Measurements as queue 76 (V\* at 120N with bootstrap over runs, all-islands success, consensus counts, δ\* by the full
definition, transition rates in tail window and chase at the 0.25·N debounce, dominant programs per slot on fair and
unequal islands, mean A_f charges per family). Add: the share of unequal islands whose victim is R against a constant, and
R's payoff relative to the ⅓ constant on islands where both are present.

**Cut order** (recorded before running): I = 256, then γ ∈ {0.3, 3}, then N = 400 for F+O+R. Budget ceiling 200
sandbox-CPU-hours. All long work on Daytona, detached clients, a launch log for reattachment.

## Validations

- V1: the F arm reproduces queue 76's stored rows exactly (same seeds and law).
- V2: the gates above; the T⁺ ∪ P ∪ O block of the extended table unchanged.
- V3: step 1's classification of R's members returns its family; mass accounting as before.

## Predictions (the RE's; copied to `predictions/2026-11-14-patient-accepters.md` before any counted cell)

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
- **gemini-4-carbon's counters (recorded, scored):** (a) RE 3 and RE 4 fail: F+R has < 0.3 of seeded-unequal islands
  fair at 120N and V\* < 0.5 at β = 3 with no threshold, because neutral victim turnover plus a neutral offerer arrival
  is slower than 120N and the added ⅓-yielders feed bullies in the scramble; (b) F+O+R is no better than F+R, because R
  and O time each other out; (c) every exit is triggered by a ½ constant, never by F or O.
- **gpt-6.1-sol's counter (recorded, scored):** constants dominate *direct* triggers, but some exits are multistep
  (through intermediate replacements) or imported by migration, so carbon's (c) is too absolute (scored on the exit
  classification: a nonzero share of local exits involving F or O at some step, or of imported exits).

## Required outputs

`predictions/2026-11-14-patient-accepters.md` (before any counted cell; pilots disclosed); `src/patient_accepter*.py`,
`tests/test_patient_accepter.py`; `runs/patient-accepters.md` and `.json` (step 0 tables, masses, V\* and δ\* tables,
seeded starts with sequences, controls, the length-prior series, verdicts), rows under `runs/pa_rows/`;
`notes/patient-accepters.md` (deviations, operations log, CPU-hours); drafts for RESULTS, REJECTED, NOTATION.

## Caveats known in advance

R is one hand-written program family in a hand-built library; the exploiter mass of T⁺ is kept; masses are grammar
lower bounds; finite schedules, nothing here is π.
