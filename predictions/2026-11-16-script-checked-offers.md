# Predictions: script-checked offers in majority division (queue 80), 2026-11-16

Spec: `specs/2026-11-16-script-checked-offers.md` (reviewed by gemini-4-carbon, then gpt-6.1-sol `--mode amended`, both
folded). Per the spec's amendment "Registration in two commits", this file is committed in two stages: RE 1 now, before
construction of the checker begins; RE 2–12 and the subagent's E-series after the gates and before any step-0 assay, mass or
counted step-2 cell. All step-2 statistics will be finite-schedule approach-rate statistics, not π.

## Stage 1 (committed before any construction)

Disclosure: before this commit I read the spec, the two reviews, and queue 79's run report and notes. No code for this queue
has been written or run.

- **RE 1 (the checker can be built).** S0 exists, is sound (G1) and accepts every listed spelling (G2), at a worst accepted
  cost between 10³ and 10⁵ steps. Falsifier: any false acceptance, or a listed spelling with no acceptable script, or the
  time box (two days of engineering).

Scoring rule (registered): RE 1 holds iff all three of (a) 0 false acceptances on S0 and S1 over the catalogue cube and every
forger rejected, (b) every listed spelling accepted with a script, (c) the worst accepted S0 check cost κ_S lies in
[10³, 10⁵] steps. If (a) and (b) hold and (c) fails, RE 1 fails on cost without its falsifier firing; that will be said.

## Stage 2 (committed after the gates, before any step-0 assay, step-1 mass, V1/V2 or counted step-2 cell)

### What was run and seen before this stage (disclosure)

- Construction (notes §1, committed e6517d6 before any gate): the checker in two versions (the first, direct-style, cost up to 166,456
  ticks; replaced by the continuation-passing evaluator before any gate), all carriers and forgers checked in S0 and against the host
  reference, timing rows, and the exactness test of the closure regress key (notes §2).
- Gates (`runs/script_offers/gates.{json,md}`), all passed: κ_S = 15,141 (Pc⁺Spoy.guard, S_nx), worst check over everything 15,141;
  G1 0 false acceptances over 7,862,391 (accepted statement × profile) checks in each of S0 and S1, the host reference agrees on all
  910 (program, code) entries, every forger accepted only for true statements; G2 every spelling accepted for exactly its statements,
  every certified-eligible pair the fair pair with 0 timed-out reads in every seat pattern beside every non-carrier, in both machines;
  (Pc⁺, Bc), (Pc⁺, Oc), (Pc⁺, Rc) never eligible, **but non-eligible pairs form the fair pair through their fallbacks**: Pc⁺–Bc in
  10,050 of 35,400 triples, Pc⁺–Fc 13,200, Pc⁺–Oc 12,000, OcR⁺–Bc 8,400, Fc–OcR⁺ 12,000, Oc–OcR⁺ 8,850; G3 queue 79's CHK accepts
  the 8 canonical K-world carriers, rejects the 32 others and every world-S program; G4 0 of 205,379 outcome triples among the first
  59 programs differ from queue 78's old-fuel table, and every one of the 135,168 reader–reader timeouts persists at (KR', cap'); V3
  S1 = S0 on all 4,601,142 profiles in code, steps, failed reads and forfeits, and on 3,640 residual-fuel interruption tests.
- **RE 1 holds** (scored now; its stage-1 rule): 0 false acceptances on S0 and S1, every forger rejected for its false statements,
  every listed spelling accepted, κ_S = 15,141 in [10³, 10⁵]. Disclosed: the first evaluator's worst cost (166,456) was outside the
  range; RE 1 is scored on the checker the gates ran.
- Nothing else: no step-0 assay, no step-1 mass, no V1/V2 and no step-2 cell has been run. Timing pilots of the step-2 kernel after this
  commit use run index 95 and are not reported as results.

### The spec's predictions RE 2-12 (verbatim; RE 8 in its amended form, RE 12 from the amendments; the first drafts recorded)

- **RE 2 (fuel alone does nothing).** Arm U at (KR', cap') has no δ\* at β ≥ 1, and differs from the old-fuel rows by less than 0.15
  on the δ-mean at β = 3. Falsifier: a δ\* in U at β = 3.
- **RE 3 (the threshold survives a real checker).** A1 has δ\* ≤ 0.03 at β = 3, φ = 0 and δ\* ≤ 0.01 at φ = ½, within one grid step
  of arm K. Falsifier: no δ\* in A1 at β = 3, φ = ½.
- **RE 4 (spellings pair).** A2 is within 0.1 of A1 on the δ-mean at β = 3 (both φ). Falsifier: A2 below A1 by 0.2 or more.
- **RE 5 (the convention mattered).** K2 is below A2 by at least 0.2 on the δ-mean at β = 3, φ = 0. Falsifier: K2 within 0.1 of A2.
- **RE 6 (thresholds do not rise with N).** A2's δ\* at N = 400 is at most one grid step above its δ\* at N = 100.
- **RE 7 (no-exploit is free).** A3 is within 0.1 of A2 at φ = ½ on the δ-mean. Falsifier: below by 0.2.
- **RE 8 (revised, amendments).** In A4 at φ = ½ Bc's share of *paired* fair-island slots is lower than in A2 by at least 0.15 and
  still above 0.2; V\* at δ = 0.003 is lower than A2's by 0.1 or more. Falsifiers: Bc's paired share not lower than A2's; A4's V\* at
  δ = 0.003 at or above A2's. (First draft: "falls from A2's majority to under 0.1"; recorded.)
- **RE 9 (the exit is still paced).** The seeded all-unequal start ends at most 0.15 fair in A2, with predicted route completions
  within a factor 3 of observed. Falsifier: 0.3 fair or more.
- **RE 10 (mass, revised).** With `CHKS` as a primitive and scripts counted as data nodes, the simplest script carriers are below
  10⁻¹⁰ of a fair reader; they are at least as abundant as the reader only if the script is not charged by the prior. Report both
  measures. Falsifier: a script carrier within 10⁻³ of the reader with its script counted. (First draft: "at least as abundant as the
  fair reader"; recorded.) Scored on witness ratios only (the listed spellings with their scripts against the 6-node fair reader).
- **RE 11 (prudence closes the bully's island again).** Pc⁺ into the excluded slot of Bc's unequal island enters at ρ·N within
  [0.5, 2], against 27.9 for Fc⁺. Falsifier: Pc⁺ above 5.
- **RE 12 (A5).** In A5 at least 0.9 of Bc's paired fair-island slots have a Bc partner, and Bc's unequal islands (Bc on ⅔) are a
  larger share of islands than in A2 at δ ≤ 0.01. Falsifier: under 0.6 Bc-partnered.

### Registered scoring rules (fixed now)

- V\* is the share of the 64 islands whose modal outcome is a fair pair at 120N, averaged over the 20 runs. **δ\*** (as queue 79): the
  smallest grid δ such that V\* ≥ 0.9 at that δ and every larger grid δ; "no δ\*" if V\* < 0.9 at δ = 0.1. "δ\* ≤ x" holds iff δ\* exists
  and is ≤ x. One grid step = one place on (0.1, 0.03, 0.01, 0.003, 0.001).
- **δ-mean** = the mean of V\* over the five δ of a cell row.
- RE 2: holds iff U (both UF and UFR) has no δ\* at β = 1 and β = 3 and |δ-mean(U at KR') − δ-mean(stored rows)| < 0.15 at β = 3 for
  both UF (queue 75's F) and UFR (queue 78's F+R). Falsifier fires iff a δ\* exists in UF or UFR at β = 3.
- RE 3: holds iff A1's δ\* ≤ 0.03 at (β 3, φ 0), ≤ 0.01 at (β 3, φ ½), and each within one grid step of K's δ\* in the same cell (both
  existing). Falsifier fires iff A1 has no δ\* at (β 3, φ ½).
- RE 4: holds iff |δ-mean(A2) − δ-mean(A1)| ≤ 0.1 at β = 3 for φ = 0 and φ = ½. Falsifier fires iff A2 < A1 − 0.2 in either φ.
- RE 5: holds iff δ-mean(K2) ≤ δ-mean(A2) − 0.2 at (β 3, φ 0). Falsifier fires iff |K2 − A2| ≤ 0.1 there.
- RE 6: holds iff A2's δ\* exists at N = 100 and N = 400 at β = 3 (both φ) and the N = 400 δ\* is at most one grid step above the N = 100
  one. (No falsifier written; a failure is scored as a failure.)
- RE 7: holds iff |δ-mean(A3) − δ-mean(A2)| ≤ 0.1 at φ = ½ for β = 1 and β = 3. Falsifier fires iff A3 < A2 − 0.2 at either β.
- RE 8: Bc's paired share = Bc slots among paired fair-island slots at 120N, pooled over the 20 runs, at β = 3, φ = ½, pooled over the
  five δ. Clause 1 holds iff share(A4) ≤ share(A2) − 0.15 and share(A4) > 0.2; clause 2 holds iff V\*(A4) ≤ V\*(A2) − 0.1 at
  (β 3, φ ½, δ 0.003). RE 8 holds iff both. Falsifiers: share(A4) ≥ share(A2); V\*(A4) ≥ V\*(A2) at δ = 0.003.
- RE 9: fair share at 240N of the seeded A2 start (mean over 20 runs) ≤ 0.15 and predicted local route completions (Σ fixation
  probabilities of the second steps) within a factor 3 of observed (if both are 0, "within a factor 3" holds). Falsifier fires iff the
  fair share ≥ 0.3.
- RE 10: log10 witness ratio (best spelling's M1 mass with script / the 6-node fair reader Snon's M1 mass) < −10 for every script
  family, and the same ratio with the script not charged ≥ 0 for at least one family. Falsifier fires iff some family's ratio with the
  script counted is ≥ −3.
- RE 11: median ρ·N of Pc⁺ (every spelling and fallback) into the excluded slot of Bc's unequal islands (Bc on ⅔, a ⅓ constant on ⅓,
  every seat pattern) in [0.5, 2], and Fc⁺'s median ≥ 20. Falsifier fires iff Pc⁺'s median > 5.
- RE 12: Bc-partnered share = Bc slots whose pair partner is Bc, among Bc's paired fair-island slots (β 3, φ ½, pooled over δ); clause 2:
  share of islands with Bc on ⅔ in A5 > in A2 at each δ ≤ 0.01. Holds iff share ≥ 0.9 and clause 2. Falsifier fires iff share < 0.6.
- Every prediction that fails without its falsifier firing is reported as "fails, falsifier not fired".

### The subagent's E-series (exact assays and mass witnesses; written after the gates, before any of them was computed)

Rates are ρ·N at N = 200, w = 0.3, A_f charges; "median" over every listed resident triple, seat pattern and spelling.

- **E1 (spellings pair neutrally).** A carrier of any spelling entering a pair slot of a fair island of a pointing carrier of another
  spelling (the entrant pairs with the remaining resident): ρ·N exactly 1 (min = max = 1), the same for same and cross spellings.
  Falsifier: any such edge outside [0.99, 1.01].
- **E2 (the accepter route does not see spellings).** Rc (any spelling) into the victim's seat of a simulating-bully island with a
  carrier (any spelling) pointing at v in e: median 9.75; certified offerers (Fc, Oc; any spelling) into e with Rc in v: median 27.9;
  same and cross spelling medians within 1% of each other. Falsifier: a cross-spelling median below half the same-spelling one.
- **E3 (Bc in (Fc⁺, Fc⁺)).** Bc into a pair slot: median exactly 1; into the excluded slot: median between 1 and 30 and above 3 in at
  least 40% of edges (it draws an Fc⁺ whose preference points at it, as queue 79's Fc). Falsifier: pair-slot median outside [0.9, 1.1].
- **E4 (Bc in (Pc⁺, Pc⁺)).** Bc into a pair slot: median below 1/3 (not eligible; it can pair only through fallbacks, which the
  remaining Pc⁺ offers only when its fallback read accepts); into the excluded slot: median in [0.9, 1.1]. Falsifier: pair-slot median
  ≥ 1.
- **E5 (Bc's unequal island).** Fc⁺ (and Fc) into e of Bc's island, pointing at Bc: median ≥ 20 (27.9 expected); Oc⁺ pointing at Bc:
  ≥ 20; OcR⁺ (requires S_nx): median in [0.5, 2] (as RE 11's Pc⁺). Falsifier: OcR⁺ median > 5.
- **E6 (the simulating bully cannot break carrier pairs).** The simulating bully into a pair slot of every listed fair carrier island,
  (Pc⁺, Pc⁺) included: median ≤ 10⁻¹⁰. Falsifier: a median above 10⁻³.
- **E7 (⅓ constants beside pairs).** ⅓ constants into the third slot of (Pc⁺, Pc⁺) and (Fc⁺, Bc): median in [0.9, 1.1].
- **E8 (jump chain).** max |z| < 4 over the 60 sampled non-neutral edges.
- **E9 (mass, script-free).** Even with the script not charged (M1-free), every family's best spelling is below 10⁻²⁰ of the 6-node
  fair reader (the carrier's rule and fallback alone are ≥ 20 nodes); so RE 10's second clause ("at least as abundant as the reader
  only if the script is not charged") fails in its "if" direction. Falsifier: a script-free family within 10⁻¹⁰ of the reader.
- **E10 (mass, script counted).** With the script counted, every family's best spelling is below 10⁻⁴⁰ of the fair reader, and the
  script is at least a third of the M1 node count. Falsifier: a family above 10⁻²⁰ of the reader.

