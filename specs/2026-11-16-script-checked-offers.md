# Spec: script-checked offers in majority division (queue 80)

RE spec for an Opus subagent (own worktree, Daytona for the dynamics). Date 2026-11-16. Follows queue 79 (RESULTS
"Certified offers in arm T"), whose run report is `runs/certified-offers.md` and notes `notes/certified-offers.md`.

## Context

Queue 79 found the first reader-share threshold under Trojan bullies in arm T, but its certificate is one fixed
spelling: the check accepts exactly the skeleton around a shared library routine `CARRY`, and the only certifiable
statement is the conditional ½ offer. The RS's question (2026-11-15): can the check be folded into the program's
existing certificate convention (milestone 4: a carrier holds a script, a shared checker verifies it against the
carrier's source; RESULTS "The realizable language, milestone 4"; three-player precedent K_3 in
`src/sog_realizable.py`)? RS decisions for this run: fuel is raised to fit the checker and the uncertified controls
are rerun at the new budget; the statement language gains a no-exploit statement. World K is not at issue (no hostile
certificate exists in this game).

This re-opens a REJECTED entry: queue 76's "prudent readers restore a threshold" (falsified; "refusing the bully is
what is missing" was dropped; P was self-incompatible through mutual reads). New evidence that justifies revisiting:
queue 79 showed the binding failure of simulating readers was illegibility at founding, certified carriers are
compatible with themselves, and the certified bully is now a distinct, countable type.

**Object.** As queue 79: arm T (`dollar3`, shares ⅓–½–⅔), the current object (seed lottery with the annealed tail),
I = 64, mN = 1, Λ = 100, 120N, A_f charge P_fail = 0.1, 20 runs per cell, common random numbers with queue 79's law
where the catalogue allows. All dynamics are finite-schedule approach rates, not π.

## The machine

- **Carrier.** Any program together with a **script**. No constraint on the program's spelling.
- **Statements** (about the carrier's own action function, quantified over every profile):  - **S_off(d; R)** [after review: parametrized by the requirement; carbon's catch that a carrier demanding more
    than S_off cannot truthfully hold the unparametrized statement]: "let E be the partners that hold an offer
    statement toward me whose requirement I meet and that themselves hold every statement in my requirement R; if d
    is my preferred member of E, I name d at ½" (queue 79's rule is R = ∅; mutual naming is derived). Eligibility is
    mutual by construction: x is eligible for y iff x holds what y requires and y holds an offer toward x.
  - **S_nx**: "in no profile do I name anyone at ⅔" (no-exploit). A carrier may hold S_off toward either or both
    slots, with or without S_nx.  - A carrier's **requirement** R is ∅ (as queue 79) or {S_nx} (the certified prudent reader). [after review] In
    every arm Oc, Rc, Fc and their ⁺ versions have R = ∅; only Pc⁺ has R = {S_nx}. G2 must show (Pc⁺, Pc⁺),
    (Pc⁺, Oc⁺), (Pc⁺, Rc⁺) and (Pc⁺, Fc⁺) pair at ½ and (Pc⁺, Bc) does not.
- **Checker `CHKS`** (one shared library entry, written in L_T^code): given a quote and a script, accepts iff the
  script is a valid derivation, in the evaluation rules of L_T with the results of `CHKS` on the partners' quotes as
  the only open atoms, that the quoted program satisfies the stated statement. It reads no one and runs no one.
  Build on milestone 4's script checker and K_3's three-quote wrappers where they fit; say what was reused.
- **Soundness** must be argued structurally in the notes before any gate is run (as queue 79 §1.3): an accepted
  script's statement is true of the carrier's play in every profile, including fuel exhaustion, the fallback and
  competing offers. The catalogue check is a regression test, not the proof.
- **Two machines.** **S0**: `CHKS` and scripts executed in L_T^code, charged step by step. **S1**: `CHKS` as a
  primitive with the same input-output map, [after review] charged the exact S0 step count of that (quote, script)
  pair from a table precomputed on the catalogue (rejections included), so that S1 equals S0 in charges as well as
  actions; κ_S denotes the worst accepted cost and is used only to set the fuel. Dynamics run on S1 tables; S0 is used statically to validate that
  S1's tables equal S0's actions on the whole catalogue (V3).
- **Fuel.** Read cap' = the smallest cap at which a simulated carrier's two checks plus its fallback fit in one outer
  read (cap' ≥ 8 κ_S); root fuel KR' = 3 cap'. Both recorded before the gates. Every arm, certified or not, runs at
  (KR', cap').
- **Time box.** If S0 cannot be built in two days of engineering, stop after the gates: report what was built, the
  cost numbers and what blocked it. Do not run the dynamics on a primitive with no executable counterpart; that would
  only replicate queue 79.

## Programs

Queue 79's 87-program catalogue is kept (the first 59 are queue 78's). Added:

- **Spellings.** For each of Oc (both directions), Rc (both), Fc (with two of T's firm readers as fallback, [after review] chosen among those for which S_nx is derivable, and
  the same two in every arm, so that no arm differs from another in its fallback pool) and Bc
  (both): the queue 79 canonical spelling plus at least three others that implement the same rule and are *rejected*
  by queue 79's skeleton check: `CARRY` inlined, branches reordered, the skeleton under a trivially true guard, and
  the eligibility test written without the library. Each with a script the checker accepts.
- **No-exploit carriers.** Oc⁺, Rc⁺, Fc⁺: the same programs holding S_nx as well. Fc⁺ only for fallbacks for which
  S_nx is derivable; report which firm-reader fallbacks are and are not.
- **Certified prudent readers** Pc⁺: Fc⁺ whose requirement is S_off and S_nx.
- **Bc** cannot hold S_nx (its fallback names ⅔); gate 1 must show every attempted S_nx script for Bc is rejected.
- **Forgers** (gates only): queue 79's eight, plus a valid script attached to a different program, a script for
  S_nx on a program that names ⅔ only when fuel runs out, a script whose derivation uses a false `CHKS` atom, and a
  program that passes S_off toward d but names someone else when d is eligible.

## Gates (static; before predictions are committed)

- **G1 soundness.** 0 false acceptances over the catalogue cube on S0 and S1; every forger rejected; the structural
  argument written first.
- **G2 completeness on spellings.** Every listed spelling is accepted with its script; report script length and S0
  check cost per spelling. Cross-spelling pointing pairs are the fair pair with no read, in every seat pattern
  beside every non-carrier.
- **G3 the skeleton check on the same catalogue.** Queue 79's `CHK` rejects every non-canonical spelling (so the
  control arm below is meaningful).
- **G4 mixed worlds at the new fuel.** Whether the simulating readers' mutual-read timeouts persist at (KR', cap')
  (queue 79 G4 found they persist at 20× caps); report any outcome triple among the first 59 programs that differs
  from queue 78's table at the old fuel.
- **V3.** [after review] S1 tables equal S0 on every profile in actions and in charges; any difference is a failure
  to be fixed before the dynamics, not a footnote.

## Step 0 (exact assays, as queue 79; N = 200, w = 0.3)

Entry rates ρ·N for: a carrier of one spelling into a slot beside a pointing carrier of another spelling; Bc into
pair slots and the excluded slot of (Fc⁺, Fc⁺) and (Pc⁺, Pc⁺); Pc⁺ and Fc⁺ into the excluded slot of Bc's unequal
island (Bc on ⅔ with a ⅓ constant); the simulating bully into pair slots of fair carrier islands; ⅓ constants into
the third slot of (Pc⁺, Pc⁺) and (Fc⁺, Bc). Jump-chain check as queue 79.

## Step 1 (mass; exact-member lower bounds only)

For each family, shortest program and total mass under three measures: `CHKS` as one primitive tag with the script
counted as data nodes; the R1-written measure (library call written out); fully written out. Report the script's
share of the node count. Compare with queue 79's skeleton carriers and with the fair reader and the bully.

## Step 2 (dynamics; S1 tables; β ∈ {0, 1, 3}; δ ∈ {0.1, 0.03, 0.01, 0.003, 0.001}; N = 200 unless stated)

| arm | what | cells |
|---|---|---|
| U | uncertified controls F and F+R at (KR', cap') | φ = 0 |
| K | queue 79's skeleton machine, canonical spellings only, at (KR', cap') | φ ∈ {0, ½} |
| A1 | script checker, canonical spellings only (Fc+Oc+Rc) | φ ∈ {0, ½}; also N = 100, 400 at β = 3 |
| A2 | script checker, each family's mass split evenly over its spellings | φ ∈ {0, ½}; also N = 100, 400 at β = 3 |
| K2 | skeleton machine on A2's law (non-canonical spellings rejected, so they act as their fallbacks) | φ ∈ {0, ½} |
| A3 | no-exploit: Fc⁺+Oc⁺+Rc⁺ on A2's law and spelling split (all R = ∅) | φ ∈ {½, 1} |
| A4 | certified prudence: Pc⁺+Oc⁺+Rc⁺ on A2's law and spelling split (Pc⁺ has R = {S_nx}) | φ ∈ {0, ½, 1}; φ = 0 at β = 3 only [after review] |

δ, β, φ as queue 79 (reader share, bullies per reader, certified share of bully mass). Record per cell: V\* share,
unequal consensus, who holds fair-island slots by family and by spelling, Bc's share of fair-island slots, the share
of islands on which Bc sits on ⅔, mean read and forfeit charges, and the 30N-to-120N class agreement.

One seeded start (all-unequal, simulating bully, δ = 0.03, β = 3) for A2 only, to 240N, with queue 79's pacing record.

**Not in this run:** endogenous production of scripts (milestone 5). Scripts are genes carried by founders and tail
arrivals with their programs. Say so in the report; who writes the first scripts is a known open issue (Provenance).

## Validations

- **V1.** Arm U at the *old* fuel reproduces queue 78's stored F and F+R rows exactly on 20 cells.
- **V2.** Arm K at the old fuel reproduces queue 79's Fc+Oc+Rc rows on 20 cells.
- **V3.** As above.

## Predictions (the RE's; copy to `predictions/2026-11-16-script-checked-offers.md` after the gates and before any step-0 assay, mass or counted cell)

- **RE 1 (the checker can be built).** S0 exists, is sound (G1) and accepts every listed spelling (G2), at a worst
  accepted cost between 10³ and 10⁵ steps. Falsifier: any false acceptance, or a listed spelling with no acceptable
  script, or the time box.
- **RE 2 (fuel alone does nothing).** Arm U at (KR', cap') has no δ\* at β ≥ 1, and differs from the old-fuel rows by
  less than 0.15 on the δ-mean at β = 3. Falsifier: a δ\* in U at β = 3.
- **RE 3 (the threshold survives a real checker).** A1 has δ\* ≤ 0.03 at β = 3, φ = 0 and δ\* ≤ 0.01 at φ = ½, within
  one grid step of arm K. Falsifier: no δ\* in A1 at β = 3, φ = ½.
- **RE 4 (spellings pair).** A2 is within 0.1 of A1 on the δ-mean at β = 3 (both φ). Falsifier: A2 below A1 by 0.2 or
  more.
- **RE 5 (the convention mattered).** K2 is below A2 by at least 0.2 on the δ-mean at β = 3, φ = 0. Falsifier: K2
  within 0.1 of A2.
- **RE 6 (thresholds do not rise with N).** A2's δ\* at N = 400 is at most one grid step above its δ\* at N = 100.
- **RE 7 (no-exploit is free).** A3 is within 0.1 of A2 at φ = ½ on the δ-mean. Falsifier: below by 0.2.
- **RE 8 (certified prudence excludes the bully and buys no V\*).** In A4 at φ = ½, Bc's share of fair-island slots
  falls from A2's majority to under 0.1, while V\* at δ ≤ 0.003 is *lower* than A2's by 0.1 or more, because the
  converted bully was holding fair islands. Falsifier for the first clause: Bc above 0.3 of fair slots in A4;
  for the second: A4's V\* at δ = 0.003 at or above A2's.
- **RE 9 (the exit is still paced).** The seeded all-unequal start ends at most 0.15 fair in A2, with predicted route
  completions within a factor 3 of observed. Falsifier: 0.3 fair or more.
- **RE 10 (mass).** [after review: revised; carbon's point that a derivation over evaluation rules is tens of nodes
  is accepted] With `CHKS` as a primitive and scripts counted as data nodes, the simplest script carriers are below
  10⁻¹⁰ of a fair reader; they are at least as abundant as the reader only if the script is not charged by the
  prior. Report both measures. Falsifier: a script carrier within 10⁻³ of the reader with its script counted. The
  RE's first draft said "at least as abundant as the fair reader"; recorded.
- **RE 11 [after review] (prudence closes the bully's island again).** Pc⁺ into the excluded slot of Bc's unequal
  island enters at ρ·N within [0.5, 2], against 27.9 for Fc⁺. Falsifier: Pc⁺ above 5.

The subagent adds its own numbered expectations (E-series) for the exact assays before running them.

## Amendments after the second review (these override the text above where they differ)

- **Eligibility, one predicate.** For carriers x and y, `elig(x, y)` (x is eligible for y) holds iff x holds an offer
  statement toward y's slot and x holds every statement in y's requirement R_y. y's set is
  E_y = {x : elig(x, y) and elig(y, x)}. S_off(d; R) reads: "if d is my preferred member of E, I name d at ½". The
  same predicate is used verbatim in the statement, the code and the soundness argument. Pc⁺'s requirement is
  {S_nx}, nothing else.
- **Forger fix.** The fourth new forger passes S_off toward d but names someone else when d is eligible *and
  preferred*.
- **Interrupted checks.** In S1 a check whose remaining fuel is below its tabulated S0 cost times out exactly as S0
  does; it is not completed and charged afterwards. Fuel is sized on the worst cost of any catalogue check,
  rejections included. Test each check at residual fuel one below and at its cost; S1 must equal S0 in both.
- **Registration in two commits.** RE 1 (the checker can be built, is sound, accepts the spellings, costs 10³–10⁵
  steps) is committed before construction begins. RE 2–11 and the E-series are committed after the gates and before
  any step-0 assay, mass or counted cell.
- **Mass claims.** Step 1 gives witnesses, so RE 10 is scored on witness ratios only (the listed shortest spellings
  with their scripts against the 6-node fair reader). No minimality or family-scarcity claim without an exhaustive
  bounded search; if one is cheap at the smallest sizes, do it and say to what size.
- **Fallback pools.** V2 reproduces queue 79 on its historical catalogue (16 fallbacks). Arms K, K2 and A1–A5 all
  use the restricted two-fallback pool.
- **RE 8 revised** (sol's point accepted: in A4 only Pc⁺ refuses Bc; Oc⁺ and Rc⁺ still pair with it, and Bc pairs
  with Bc). In A4 at φ = ½ Bc's share of *paired* fair-island slots is lower than in A2 by at least 0.15 and still
  above 0.2; V\* at δ = 0.003 is lower than A2's by 0.1 or more. Falsifiers: Bc's paired share not lower than A2's;
  A4's V\* at δ = 0.003 at or above A2's. The first draft said "under 0.1"; recorded.
- **Arm A5 (everyone requires no-exploit).** As A4 with Oc⁺ and Rc⁺ also at R = {S_nx}; φ = ½, β = 3, N = 200.
  **RE 12:** in A5 at least 0.9 of Bc's paired fair-island slots have a Bc partner (the bully is excluded from
  carriers and keeps only its own pairs), and Bc's unequal islands (Bc on ⅔) are a larger share of islands than in
  A2 at δ ≤ 0.01. Falsifier: under 0.6 Bc-partnered. Cut A5 before A3 if short.
- **Occupancy records.** Report Bc's occupancy separately for paired and excluded slots, and for paired slots by the
  partner's family.
- **Extra gates.** (Pc⁺, Oc) and (Pc⁺, Rc) without S_nx do not pair; three mutually pointing carriers with mixed
  requirements (competing offers) are tabulated over all orientations, on S0 and S1.
- **Scope statements for the report.** N = 100–400 is exploratory and not a large-N result. A prudence penalty may be
  lost connectivity, not a cost of no-exploit as such. Cross-spelling success is robustness across the listed
  transformations under one proof convention with scripts supplied to founders.

## Required outputs

`runs/script-checked-offers.md` (run report: headline, gates, step 0, step 1, step 2 tables with bootstrap
intervals, verdict table, "The model can't express", deviations, budget), `runs/script-checked-offers.json`
(verdicts, scored by the registered rules), `notes/script-checked-offers.md` (the soundness argument, what was reused
from milestone 4 and K_3, engineering deviations), `predictions/2026-11-16-script-checked-offers.md`, tests, and
drafts for RESULTS, REJECTED and NOTATION. State every deviation from this spec. Report failed predictions as
failures.

## Budget and operations

200 sandbox-CPU-hours on Daytona (`tools/daytona_run.py`; 4 CPUs per sandbox; at most 3 concurrent workers locally).
Cut order if short: N = 100 and 400 cells; A5; A3; the seeded start; φ = 0 for K2. Never cut U, K, A1, A2 at N = 200 or
the gates. Leave no sandbox running (`python3 tools/daytona_run.py list` empty at the end). Do not read `.env` or
print, echo or commit any key; no `.npz`, `.pkl` or large `.npy` in git; commit on the worktree branch only and do
not push; do not edit RESULTS, REJECTED, THEORY, DEFERRED, CLAUDE.md or the operating-hypotheses doc.
