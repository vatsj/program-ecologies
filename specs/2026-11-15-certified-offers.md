# Spec: certified offers in majority division: readers that can read each other, 2026-11-15

Status: reviewed by gemini-4-carbon (folded, [after review]) and by gpt-6.1-sol (`--mode amended`, folded [after second review]). Queue 79. The RS (2026-11-15), on the three things the model could not express after queue 78 (an offer
between two readers; a reader that is a constant to its partner while reading the other; a two-slot move): "1 sgtm".
To be reviewed by gemini-4-carbon, then gpt-6.1-sol (`--mode amended`); run by an Opus subagent on Daytona.

## Context

Queues 76 and 78 (RESULTS "Bully-resistant readers in arm T", "Patient accepters in arm T") hit the same wall. Under
Trojan bullies no reader arm has a reader-share threshold for V\* ≥ 0.9, and in both the readers could not read each
other: two programs that simulate each other under a cap time out (the mutual regress of milestone 3). Consequences
measured in queue 78: a patient accepter R in the victim's seat can be triggered only by a non-reading ½ constant;
with any reader in the excluded slot the bully's read of R also times out and the bully drops it; prudent readers are
self-incompatible (queue 76).

Milestone 4 (RESULTS "The realizable language, milestone 4") removed the same regress in the PD: a carried script is
*checked* against a shared sound checker at bounded cost, the pair rule is sound by symmetry (both checks compute the
same predicate), and no simulation of the partner's read is needed. RESULTS "The social organization game over the
realizable language" extended the checker to three players (K_3, outcome sets, the closure). This spec carries that
into majority division.

**What is and is not being tested.** Certificates supply (1) offers between readers and, as a by-product, (2) a reader
that its partner can still read. They do not supply a two-slot move: every route out of a bully–victim island is still
two single-slot steps. Queue 78 showed the plain ½ constant is already an abundant, legible offerer and the route still
completed once in 6,419 exits. So the experiment separates two readings of queues 76/78: *legibility binds* (then
certified families restore a threshold or exits) or *single-slot pacing and the founding scramble bind* (then they do
not, and the next move is the mutation law or founding). The RE expects mostly the second (predictions below).

REJECTED.md checked: no entry on certificates in majority division. Does not re-open queue 76/78 arms; their stored
rows are the simulation-read controls. "O or F can be R's offerer" (dropped in queue 78) is re-tested here only for
certified versions, on the stated ground that the regress is what blocked it.

## Semantics

Grid, payoffs, slots and conventions as arm T (`dollar3`, shares ⅓–½–⅔; A_f charge P_fail = 0.1; root fuel and read cap
as queue 76 unless the machine below changes them).

- **Certificate.** A program may carry a script. The shared checker validates, at bounded cost, a statement about the
  carrier's own action function of the form *"toward slot d: I name d at ½ whenever d's certified statement toward me
  is of this same form"* (a **conditional ½ offer**, the majority-division analogue of milestone 4's pair statement),
  and optionally *"otherwise I play a (a named constant action)"* (the **fallback clause**, which is what makes a
  certified program legible to a simulating reader: the simulation of a carrier runs the carrier's check of others'
  scripts, which is bounded and reads no one).
- [after second review: what is certified] The certified statement is the carrier's actual rule, not a bilateral
  promise: *"my eligibility set E is the partners whose certified rule makes me eligible for them; if E is non-empty I
  name my preferred member of E at ½; otherwise I play my fallback"*. Mutual naming is derived, not certified: two
  carriers form the fair pair iff each is the other's chosen member. A carrier with two eligible partners names only
  one, and that is consistent with its statement.
- [after second review] Soundness needs a structural argument, written in the notes before the gates: the script is
  bound to the carrier's executable code (as milestone 4's skeleton rule), and the argument covers fuel exhaustion,
  the fallback and competing offers. The catalogue-cube check (gate 1) is a regression test, not the proof.
- **Soundness** is unconditional: an accepted script's statement is true of the carrier's play in every profile. The
  pair rule is the symmetry of milestone 4: two carriers whose statements point at each other both check the same
  predicate and both name the other at ½.
- **Three players.** A carrier may hold statements toward both partners. When both partners hold matching statements
  toward it (three mutually pointing carriers), the tie is broken by the carrier's own fixed preference (next or prev),
  as arm T's readers already have. [after review: the rule is locked] Each carrier names, at ½, its preferred partner
  among those holding a matching statement toward it (its only such partner if there is one). With three mutually
  pointing carriers 2 of the 8 orientation triples cycle (all next, all prev: no pair, everyone 0) and 6 give a fair
  pair. The cycle share is a known cost of the local rule, reported in gate 2 with the mean payoff of each
  three-carrier triple over orientations; no slot-indexed tie-break is used (it would pick a pair by role).
- **Machines.** **C1**: `check` is a library primitive with a fixed step cost κ, [after review] set so that a simulated
  carrier's two checks plus its fallback fit inside one outer read cap (κ ≤ cap/8; the value is recorded before the
  gates) (the analogue of R1's read primitive); dynamics run on C1 tables. **C0**: checker and scripts written out in L_T^code as
  milestone 4, caps raised as needed; used statically only, to verify on the whole catalogue that C1's tables equal
  C0's actions and that soundness holds with 0 false acceptances. [after second review] If C0 cannot be built within a
  day of engineering, report the cost numbers, record V3 as not validated, and label every conclusion as holding for
  the idealized check primitive only, not for executable certificates.

## Programs (added to queue 78's 59-program catalogue; the first 59 unchanged)

- **Oc** (certified opener): carries a conditional ½ offer toward its preferred partner d; fallback names d at ½
  (it offers to constants as O does).
- **Fc** (certified firm reader): conditional ½ offers toward both partners with a preference; fallback is firm F's
  behaviour toward non-carriers via its ordinary bounded read.
- **Rc** (certified patient accepter; [after review] pure, the main variant): from the victim's seat, conditional ½
  offer toward the excluded slot e; fallback clause "otherwise name my partner at ⅓". It simulates no one, so its
  on-path play in a bully-held island is the ⅓ constant's and any read of it terminates. It is not triggered by a
  plain ½ constant (Oc is the certified offerer that plays that part).
- **Rcs** [after review] (hybrid): Rc that also reads e by simulation and accepts a plain ½ constant naming it, as R
  does. It has abundant offerers but re-creates the regress when a simulating reader sits in e. Gates, step 0, one
  seeded start and one dynamics arm at N = 200.
- **Bc** (certified Trojan bully): conditional ½ offers toward carriers (sound, so it is fair with them), ⅔ against
  ⅓-namers as the bully. The faker to beat: certificates cannot exclude it.
- **Pc** (certified prudent reader), included in the gates and step 0 only unless the gates show it self-compatible, in
  which case it gets the cut-order's last arm.
- Orientation variants as needed (next/prev), counted as in queue 78.

**Gates** (before any assay; reported in `gates.md`):
1. Soundness: 0 false acceptances over the whole catalogue cube; every forged or mismatched script rejected (a forging
   bully that carries Oc's script is included by construction).
2. Reader–reader: Oc × Rc, Oc × Fc, Fc × Fc, Rc × Rc, Fc × Rc, Pc × Pc in every seat pattern: outcome, read status,
   charges. Expected: every pointing pair is the fair pair with no timeout.
3. Legibility: the bully (simulating, `Bn`/`Bp`) and Bc with Rc as victim and each carrier or simulating reader in the
   excluded slot: does the bully's read complete; outcome. Queue 78's illegibility table is the comparator.
4. Mixed worlds: carriers against queue 78's simulating readers (F, O, R, P): which pairs still regress.
   [after review] In particular the simulating bully against Fc and Bc against F (fallback simulations inside a
   read): timeouts and cap exhaustion reported separately.
5. The first 59 programs' tables unchanged; R1-style rule conformance for each new family over all profiles.

## Step 0: exact assays (as queue 78's step 0; N = 200, w = 0.3, A_f charges; all rotations; jump-chain check)

1. Rc into the victim's seat of every bully-held unequal island, by what sits in the excluded slot (constants,
   simulating readers, carriers). Queue 78's R is the comparator (1 where its read completed, 10⁻¹⁰ beside a reader).
2. With Rc resident as victim: Oc, Fc, a ½ constant, Bc each into the excluded slot. With each of those resident in the
   excluded slot: Rc into the victim's seat.
3. Reverse edges: the bully, Bc, a ⅔-demander, a ⅓ constant into each fair carrier island ((Rc, Oc), (Fc, Fc),
   (Rcs, ½ constant), (Fc, Bc)); Bc into fair simulating-reader islands; carriers into fair simulating-reader islands.
4. Bc's own unequal island (Bc on ⅔ with a ⅓ constant): the same entries as items 1–2.
Per-mutant fixation reported separately from prior-weighted per-arrival rates under the main law.

## Step 1: length-prior mass (exact-member lower bounds only; no Monte Carlo)

Under C1 (with `check` as a primitive, as R1 had `readn`) and under R1 without it: shortest spelling and exact-member
lower bound of Oc, Fc, Rc, Bc, with ratios to the fair single reader, the simulating bully and R. C0's sizes are
reported from the written-out scripts (expected astronomically small mass; milestone 4's sizes are the guide).

## Step 2: dynamics (queue 78's simulator and law; mN = 1, Λ = 100, 100N + 20N, CRN, 20 runs per cell)

Constants at T's proportions, exploiters at their ratio, reader share δ split by arm, bullies at βδ. **φ** is the share
of bully mass that is certified (Bc): φ ∈ {0, ½, 1}.

| arm | reader share δ | notes |
|---|---|---|
| F, F+R, F+O+R (controls) | simulating | queue 78's stored rows (V1 reproduces a sample) |
| Fc | certified firm | – |
| Fc+Oc | half each | – |
| Fc+Oc+Rc | δ/2 Fc, δ/2 Oc, Rc at γδ from the constants (γ = 1) | the main arm |
| Fc+Rc | Fc, Rc at γδ | does Rc need a certified offerer? |
| Fc+Oc+Rcs [after review] | as the main arm with the hybrid accepter; N = 200 only | – |
| mixed | δ/2 certified (Fc+Oc), δ/2 simulating (F+O), Rc and R at γδ/2 each | do the two reader kinds obstruct each other? |

Grid: β ∈ {0, 1, 3}; φ = ½ on the full grid, φ ∈ {0, 1} at N = 200 for the main arm and Fc; δ ∈ {10⁻³, 3·10⁻³, 10⁻²,
3·10⁻², 0.1}; N ∈ {100, 200, 400}; I = 64; I = 256 at N = 200 for the main arm.

[after second review] **Matched controls.** The φ = 0 rows differ from queue 78's stored simulating rows only in the
substituted reader families (same bully composition, same donor mass from the same constants), so the certification
effect is read at φ = 0 and Bc's effect from φ = 0 → ½ → 1; φ ∈ {0, 1} therefore runs at N = 200 for every certified
arm, not only two. Two further controls at N = 200: **Fc+Oc+C⅓** (Rc's γδ given to ⅓ constants: Rc with its script
ablated is that constant) and **Fc\*** (Fc with cycles broken by slot index, a role-using comparator that is not a
candidate program, to bound what the 2-in-8 cycles cost during founding; β ∈ {0, 3}).

**Seeded starts** (N = 200, I = 64, δ = 0.03, β = 3, φ = ½; exact triples and rotations as queue 78): all-unequal
(simulating bully, ⅓ constant, C8); all-unequal with Bc as the bully ([after review] run at φ = 1 as well as ½, so the tail's bullies match the seed); all-fair (two ½ constants, C8); all-fair on
carriers (Fc, Fc, C8). Arms: F+R (stored), Fc, Fc+Oc+Rc, Fc+Rc, Fc+Oc+Rcs. Report fair shares at 30N, 120N, 240N, the exit hazard,
and exits classified by queue 78's v2 classifier (unchanged, fixed before the run; local Rc-route with a certified
offerer, local Rc-route with a ½ constant, other local, imported; lasting or transient).

[after second review] **Pacing against scramble.** On seeded-start and main-arm islands record: first-passage times
out of unequal, every transition (not only endpoints), Rc's resident exposure time in victim seats, and offerer
arrivals and fixations conditional on a resident Rc. From step 0's exact rates and the realized arrival counts compute
the predicted number of completed Rc routes per cell and compare with the observed number; a null is attributed to
pacing only if predicted and observed counts agree. Outcomes and fixation rates are reported per orientation as well
as averaged.

**Scramble diagnostic** (the RE's expected binding constraint): for the main arm and Fc at β = 3, N = 200, δ = 0.03,
the share of islands whose 120N outcome equals their 30N outcome, and the composition of unequal islands at 30N (who is
the ⅔-holder: simulating bully, Bc, other; who is the victim: constant, R, Rc).

Measurements as queue 78 (V\* at 120N with bootstrap over runs, δ\* by the full definition, consensus counts, dominant
programs per slot on fair and unequal islands, mean charges per family, where Rc and Bc end up).

**Cut order** (fixed before running): I = 256; φ ∈ {0, 1}; the mixed arm at N = 400; Pc's arm. Budget ceiling 200
sandbox-CPU-hours. Long work on Daytona, detached clients, launch log for reattachment, a waiter armed.

## Validations

- V1: 20 stored F and F+R cells reproduce queue 78's rows exactly.
- V2: the gates.
- V3: C1 = C0 on the catalogue (or the documented failure to build C0 within the time box).

## Predictions (the RE's; copied to `predictions/2026-11-15-certified-offers.md` before any assay or counted cell)

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

## Outputs

`predictions/2026-11-15-certified-offers.md` (before any assay or cell); `runs/certified-offers.md` and `.json`;
`runs/certified_offers/` (gates, step 0, step 1, step 2 report); rows; `notes/certified-offers.md` (operations log,
deviations, CPU-hours); drafts for RESULTS (finite-schedule approach rates, labelled so), REJECTED, NOTATION; a list
headed "the model can't express"; tests. Do not touch THEORY, RESULTS, REJECTED, CLAUDE.md or the OH doc.
