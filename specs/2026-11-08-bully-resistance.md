# Spec: bully-resistant readers in arm T: why bullies beat firm readers, and whether prudent readers and openers restore the stable set, 2026-11-08

Status: reviewed by gemini-4-argon (folded [after review]) and gpt-6.1-sol (`--mode amended`, folded [after second
review]); run by a Sonnet
subagent on Daytona. Queue 76. The RS (2026-11-08), after queue 75: "I'm excited about 3 too - can we test all 3? I
claim they all exist in our prior", on the RE's three bully-resistant designs (firm, prudent, opener); "Sg" to the plan.

## Context

Queue 75 (RESULTS "From arm T to a length prior"): over T⁺ (arm T's 27 programs plus two Trojan bullies `Bn`, `Bp`:
"if the partner I read names me at ⅓, name it at ⅔, else name the other slot at ½"), in the current object (mN = 1,
Λ = 100, 120N, I = 64 and 256), with bullies at β ≥ 0.3 per reader no cell has a reader-share threshold for V\* ≥ 0.9,
and V\* generally falls as the reader share δ grows. A length prior over L_T puts bully spellings at 3.09 per reader
spelling of the same size, so any length-prior route needs readers that survive bullies.

**A fact that reshapes the RS's design 1 (firm).** Arm T's readers already never offer ⅓
(`churn_primary_t.src_single`, `src_two`): they name a partner at ½ when it names them at ½, else fall back to the
other slot at ½ (`o`), to null (`z`, code 8 = (ALL, ⅔)), or to the first partner at ½ (`f`). So the firm reader (never
accommodate) is already in T⁺, and queue 75 is its test: firm readers alone do not survive bullies. Design 1 is kept
as the control (the existing readers), not as a new family. The mechanism by which bullies beat firm readers was not
isolated in queue 75; step 0 isolates it before the new families are judged.

**The RS's claim "they all exist in our prior".** True in law: a length prior over a Turing-complete syntax gives every
program positive mass. The question is how much, which step 2 measures as queue 75 did.

REJECTED.md checked. Re-opens nothing; the RE's queue-75 conjecture "readers feed bullies by yielding ⅓" is dropped
before the run (T's readers never yield) and goes to REJECTED.

## Step 0: why bullies beat firm readers (diagnosis, cheap)

On T⁺ at N = 200, w = 0.3, A_f at P_fail = 0.1:
1. **Outcome table:** for each triple of (bully, firm-reader family, constant) programs, the outcome class, from the
   T⁺ joint table. List the triples in which a bully is on an unequal pair and the triples in which a bully and a fair
   reader coexist on a fair pair.
2. **Invasion assays** (single-island Moran, no migration, no tail, 10⁴ trials each; fixation probability against 1/N):
   a bully into a homogeneous fair island held by each firm reader family; a firm reader into a homogeneous unequal
   island held by a bully and each ⅓-naming constant; the ⅓-naming constant into a bully-held fair island.
3. **Holding configurations:** in queue 75's β = 1 and 3 rows at N = 200, I = 64 (stored in `runs/lpt_rows/`), the
   dominant program per slot on islands ending unequal, and on islands that were fair at 30N and unequal at 120N.
[after second review] **Assay definition:** every resident configuration is a named triple (slot 0, 1, 2 programs); for
each, the invading program, the slot it enters, and the probability that it fixes in that slot are listed; every
assay is paired with a neutral-label control (a relabelled copy of the resident) giving the empirical 1/N baseline.
Neutral shadowing (fixation in a fair island) and unequal-state persistence (invasion of an unequal island) are scored
separately.
4. [after review] **The new families in the same assays:** a bully into a homogeneous P island and an O island; P and O
   into a bully-plus-⅓-constant unequal island. Step 1's programs are built first so these run before step 3.
5. [after review] **Net payoffs:** every outcome in 1–4 is reported with the A_f charges included (a 0.1 charge is
   N·w·Δπ = 6 at N = 200, w = 0.3, larger than drift).
Output: a short mechanism statement with its supporting numbers. If the mechanism is not one of the two the RE
anticipates (bullies hold unequal pairs with ⅓-naming constants that no firm reader can pry loose; or bullies are
neutral shadows of fair readers that later exploit drifting-in ⅓ constants), say so; the new families are still run.

## Step 1: two new families in L_T

- **Prudent reader P** (design 2). For the read partner j: does j name me at ½ (the existing read), and, run against a
  probe in which the third slot is the ⅓-naming constant toward j, does j take ⅔ from it? Pair with j at ½ iff the first
  answer is yes and the second no; else fall back to the other slot at ½. The probe is a second read of j's source with
  a constant program in the third argument, under the same read cap 400 and A_f charge. Variants: read direction n or
  p; timeout-accepting or not (as T's `y`/`n`); fallback o or z. Up to 8 programs. [after review] The main arm uses the
  null fallback z only (**P_z**): with fallback o a refusal names the other slot at ½, which can pair with a second bully
  (a bully not reading a ⅓-offerer names its other slot at ½); **P_o** is run as a variant and the step-1 check reports
  whether (P_o, B, B) and (P_o, B, C) pair P_o with a bully.
- **Opener O** (design 3). Read both others, each in the actual current triple (the same arguments the arm-T frame
  passes in play). [after review: the rule exactly] If j names k at ⅔ and k names j at ⅓, name k at ½; symmetrically if
  k names j at ⅔ and j names k at ⅓, name j at ½; otherwise behave as the two-partner reader D (`Dn`/`Dp`, fallback f or
  z). Up to 8 programs.
- **Firm control F** = T's existing single- and two-partner readers.
- Validations: behavioural tables of P and O on the 29 × 29 probe table plus a bully: P refuses `Bn`/`Bp` and accepts
  every fair reader and the ½ constants toward it; O offers ½ to the ⅓-holder on every unequal-pair profile. Steps to
  completion within root fuel 1,200 on every triple (count forfeits; any forfeit is reported, as A_f charges it).
  [after review] **Nested reads gate:** P and O read readers that themselves read; on the full (P ∪ O ∪ F ∪ B)³ sub-table
  report read timeouts, forfeits, A_f charges, and self- and mutual compatibility (does P_z pair with P_z, with F, with
  ½ constants; does O pair with O). If a family is self-incompatible through timeouts at cap 400 / fuel 1,200, report it
  before step 3; caps are not changed (they are part of arm T's object). [after second review] Timeout rules are
  separate for P's two reads: the cooperation read follows T's `y`/`n` convention, and an inconclusive bully probe
  counts as **refuse** in the main arm (accepting an untested partner is not bully resistance) and as accept in a
  variant; both are scored separately and the registered main arm (P_z, strict probe) is not replaced. Bully resistance
  is re-validated after the gate (P_z refuses `Bn`/`Bp` in every profile it completes).

## Step 2: length-prior mass of P and O

Queue 75's machinery (`src/lt_prior*.py`), machines R0 and R1 as in queue 75, plus **R2 = R1 + a probe tag** (arity 1:
evaluate the read partner with its third argument replaced by the given constant code, same cap) so a prudent reader has
a short spelling. [after second review] The probe tag must not get cheaper execution than its written-out counterpart:
verify identical arguments, nested caps, root-fuel accounting, actions and charges against an explicit implementation on
the full probe table. For each machine: the exact-member lower bound (decision-tree grammar) and the shortest spelling of P
and O, their ratio to the fair single reader and to the bully, and the Monte Carlo upper bound on the classes. R2 is a
bracket on how short prudence can be, as R1 was for reading.

## Step 3: dynamics

Queue 75's simulator (`src/length_prior_t*.py`), mN = 1, Λ = 100 from the founding law, 100N + 20N chase, CRN, 20 runs
per cell. Law: constants at T's main within-family proportions, bullies at βδ, and the reader share δ split by arm:

| arm | readers in δ |
|---|---|
| F (control) | T's single and two-partner readers at 2 : 1 (queue 75's law) |
| P | prudent readers only |
| O | openers only |
| P+O | half prudent, half openers |
| F+P+O | thirds |

Grid: β ∈ {1, 3}; δ ∈ {3·10⁻⁴, 10⁻³, 3·10⁻³, 10⁻², 3·10⁻², 0.1} (where constants stay positive); N ∈ {100, 200, 400};
I = 64; plus I = 256 at N = 200 for P and P+O. The F rows at β ∈ {1, 3} reuse queue 75's stored rows where the law is
identical (V1 checks this). Threshold δ\* as in queue 75 (smallest grid δ with mean V\* ≥ 0.9 at 120N, all larger
passing; non-monotone responses reported as such).

[after second review] **Controls:** bully-free rows (β = 0) for P, O and P+O at N = 200, I = 64; a matched two-read firm
control F2 (T's single reader plus a second, unused read of the same partner, so it pays P's read costs without
discriminating); seeded starts at N = 200, I = 64 (all islands on a fair pair held by each arm's readers, and all on a
bully–⅓-constant unequal pair) under the same tail, giving entry and exit hazards separately; the boundary cells
continued to 240N. Besides mean V\*, report the fraction of runs with every island on a fair pair and the fair-pair
frequencies across worlds; bootstrap over runs.
[after review] Record mean A_f charges per family per cell, so a family that fails by paying double read charges (two
reads against junk and tail arrivals) is distinguished from one that fails strategically.

**Length-prior-shaped series (2b-type).** For each machine R0, R1, R2: junk, constants, bullies, F, P and O at their
measured masses (exact-member lower bounds; the rest in their measured proportions), scaled so that the reader share
(F + P + O) takes the grid values δ above with the measured within-reader ratio; N = 200 and 400, I = 64. [after second
review] The normalized probability vector of every cell is published; the bully mass is β·(reader mass) with β from the
measured lower-bound ratio, and unclassified mass is allocated two ways (to junk; to constants in proportion) as a
sensitivity. These are **grammar-conditioned projections** onto T⁺ ∪ P ∪ O, labelled so; ratios of lower bounds are not
bounds on true ratios.
[after second review] **Diagnostics (not the object):** a replay of selected cells with identical capped actions and the
A_f charges suppressed, and an idealized uncapped behavioural table for P and O, to separate strategic failure from
timeout-induced behaviour.

**Cut order** (recorded before running): I = 256 cells, then N = 400 for F+P+O, then δ = 3·10⁻⁴. Budget ceiling 250
sandbox-CPU-hours. Long work runs on Daytona (two container restarts in queue 75); local runs only for short jobs.

## Validations

- **V1:** the F arm at β ∈ {1, 3} reproduces queue 75's stored rows exactly (same seeds, same law).
- **V2:** P and O behave as specified on the probe table (step 1), and the T⁺ block of the extended table is
  unchanged.
- **V3:** step 2's mass accounting sums to 1 within 10⁻⁹ on the exhaustive part for R2, as in queue 75.
- **V4:** an exact-member classification of P and O members by the step-2 classifier returns their own family.

## Predictions (the RE's; copied to `predictions/2026-11-08-bully-resistance.md` before any counted cell)

- **RE 1 (mechanism).** Step 0 finds that bullies hold unequal pairs with ⅓-naming constants that firm readers cannot
  pry loose (a firm reader entering such an island fixes at or below 1/N), not that bullies shadow fair readers.
  Falsifier: the bully fixes above 3/N in a homogeneous fair firm-reader island, or a firm reader fixes above 3/N in a
  bully-held unequal island.
- **RE 2 (prudence restores a threshold).** Arm P at β = 3, N = 200, I = 64 has a threshold δ\* ≤ 0.1. Falsifier
  [after second review]: no grid δ meets the full threshold definition (V\* ≥ 0.9 at that δ and every larger grid δ);
  isolated passing cells are reported but do not count.
- **RE 3 (openers alone do not).** Arm O at β = 3, N = 200, I = 64 has no threshold (constant victims cannot answer an
  offer). Falsifier: O has δ\* ≤ 0.1.
- **RE 4 (prudence is long).** Under R0 the shortest prudent reader is ≥ 10 nodes longer than the shortest fair reader,
  and under R2 within 3 nodes. Falsifier: R0 gap < 6 nodes, or R2 gap > 6.
- **RE 5 (still not a length-prior route).** No machine's length-prior-shaped law reaches V\* ≥ 0.9 at any tested δ at
  N = 200 or 400. Falsifier: any cell does.

- **gpt-6.1-sol's counters (recorded, scored):** (a) RE 2 fails: no threshold for P at β = 3 unless P improves
  establishment during founding (scored together with the seeded-start hazards: if the seeded unequal start shows no
  recovery under P, establishment is the channel); (b) RE 1 is a mixture varying with family and slot (scored: neutrality
  and unequal persistence each judged separately, and both present).
- **gemini-4-argon's counters (recorded, scored):** (a) on RE 1, both mechanisms operate: the bully fixes near 1/N in
  a homogeneous fair firm-reader island (a neutral shadow) and later locks onto arriving ⅓ constants (scored: bully
  fixation in [0.5/N, 3/N] and the firm-reader invasion of a bully-held unequal island ≤ 1/N); (b) RE 2 fails even for
  P_z, because P cannot invade an island already unequal from the scramble or the tail.

## Required outputs

- `predictions/2026-11-08-bully-resistance.md` (before any counted cell; pilots disclosed).
- `src/bully_resist*.py` (P, O, the extended table, laws, the step-0 assays), extensions to `src/lt_prior*.py` for R2,
  `tests/test_bully_resist.py`.
- `runs/bully-resistance.md` and `.json` (step 0's mechanism statement and numbers; step 2's masses per machine with
  method and bound direction; step 3's V\* per cell with bootstrap intervals, consensus counts, δ\* table, transition
  rates in the tail window and chase; the length-prior-shaped series; the verdict table), rows under
  `runs/bully_resist/`.
- `notes/bully-resistance.md`: deviations, operations log, CPU-hours.
- Drafts for the RE: RESULTS, REJECTED (including the dropped yielding conjecture), NOTATION.

## Caveats known in advance

- P's probe uses one ⅓ constant as the sucker; prudence against other exploit patterns is not tested.
- O is defined by its reaction to an unequal pair; it does not punish.
- The masses above enumerated sizes are lower bounds; the length-prior series is a projection.
- Finite schedules; nothing here is π.
