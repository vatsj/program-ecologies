## Script-checked offers in arm T: a real checker that accepts any spelling keeps the reader-share threshold; certified prudence costs the prudent reader its partners and leaves the fair islands to the certified bully; the witness spellings of script carriers are 10⁻⁶⁴ or rarer relative to the fair reader under a length prior (2026-11-16; queue 80)

Spec `specs/2026-11-16-script-checked-offers.md` (gemini-4-carbon, then gpt-6.1-sol, both folded). Predictions
`predictions/2026-11-16-script-checked-offers.md` (RE 1 before any code; RE 2–12 and the E-series after the gates and before any assay, mass
or counted cell). Run report `runs/script-checked-offers.md`, verdicts `runs/script-checked-offers.json`, notes
`notes/script-checked-offers.md`, data `runs/script_offers/`. **All population numbers are finite-schedule approach-rate statistics
(I = 64, mN = 1, Λ = 100, 120N; the seeded start to 240N), not π; N = 100–400 is exploratory.** 55 sandbox-CPU-hours on Daytona plus about
5 local.

**Naming.** In this section "the skeleton machine" (arm S79; the run report's "K" and "world K") is queue 79's check, which accepts one
fixed spelling. It is unrelated to the certificate convention "world K" of the PD arm, which is discussed at the end.

**Question.** Queue 79's certificate was one syntactic convention: a reader was a carrier only if it was spelled around one library
combinator. Does the threshold survive when the check is a real one, a shared checker that verifies a carried derivation for any spelling of
the program? And can a certified statement exclude the certified bully Bc (prudence)?

**Object.** A carrier is any program packaged with a script. The shared checker CHKS, written in the realizable language, accepts a script
only if it is a derivation (a case tree over the partners' check results, each leaf checked by symbolic evaluation of the carrier's body with
the partners' quotes opaque) that the program satisfies the asked statement. Two statement forms: an offer S_off(d; R), "if d is my preferred
eligible partner, I name d at ½", with an optional requirement R on the partner; and no-exploit S_nx, "I never demand ⅔". Ten carrier families
(Oc, Rc, Fc, Bc; Oc⁺, Rc⁺, Fc⁺, which also hold S_nx; Pc⁺, which requires S_nx of its partners; OcR⁺, RcR⁺ for the arm where everyone
requires it), each in two directions and five spellings (canonical, inlined, reordered, guarded, inlined with direct checker calls). Bc
cannot hold S_nx. Scripts are supplied to founders and tail arrivals with their programs; no program writes one.

**Gates.** Soundness is argued structurally (notes §1.4, written before any gate) and then tested: 0 false acceptances in 7,862,391
(accepted statement × profile) checks, with the checker executed step by step (S0) and as a primitive with S0's exact values and costs (S1);
the two machines agree on all 4,601,142 profiles. All 100 carriers are accepted for exactly their statements; 23 forgers are accepted only
for statements true of them. The dearest accepted check costs 15,141 steps, so fuel was raised from (root 1,200, read cap 400) to (384,000,
128,000). Queue 78's 59 programs behave identically at the new fuel (0 of 205,379 triples change; reader–reader regress is a regress at any
cap). Validations: stored cells of queues 75/78 and of queue 79 reproduce 20 of 20 each.

**Findings.**

1. **The threshold survives a real checker, unchanged.** At β = 3, N = 200 the canonical script carriers (A1) have δ\* = 0.03 with
   simulating bullies only (φ = 0) and 0.01 with half the bullies certified (φ = ½). The uncertified controls at the same fuel have none at β = 1 or 3
   (at β = 3, V\* ≤ 0.15 at every δ except 0.45 for F+R at δ = 0.001), so fuel alone does nothing. A1 and queue 79's skeleton machine are
   one model: their action, failed-read and forfeit tables coincide on all 300,763 triples the laws use, and their rows are identical.
2. **Spellings pair, and under the skeleton check they did not.** Statically, every mutually eligible pair forms the fair pair across all
   five spellings with no read, and every cross-spelling pair-slot entry is exactly neutral. The five spellings of a family are
   behaviourally identical, so splitting a family's mass over them (A2) is A1's law in copies: δ\* 0.03 / 0.01, δ-means 0.68 / 0.90
   against A1's 0.54 / 0.88. Under the skeleton check the same split (S79-split) leaves four of five spellings uncertified (they still call the check, so they
   offer one-sidedly toward canonical carriers and play their fallbacks among themselves) and falls to a
   δ-mean of 0.40 at φ = 0, with δ\* only at 0.1. The threshold does not rise with N (A2 δ\* 0.03 → 0.01 at φ = 0 and 0.01 → 0.003 at
   φ = ½ from N = 100 to 400).
3. **Holding no-exploit is free.** The ⁺ programs are table-equivalent to the plain ones where nobody requires S_nx, so A3 is A2's law
   (0.89 against 0.90 at β = 3, φ = ½).
4. **Requiring no-exploit costs the prudent reader its partners; the bully keeps the islands.** Pc⁺ refuses Bc, and Bc is the dominant
   pair-holder. In A4 (β = 3, φ = ½) Pc⁺ holds 1.7% of paired fair-island slots, while Bc's share is 0.79 against 0.67 in A2; V\* does
   not fall (0.95 against 0.85 at δ = 0.003; δ-means 0.88 against 0.90). When every carrier requires S_nx (A5) Bc holds 94% of paired
   slots, each paired with another Bc, at a δ-mean of 0.88. Bc is fair on these islands: it demands ⅔ on at most 5% of islands in any
   cell. Statically prudence does what it was written for: Pc⁺ enters the excluded slot of Bc's unequal island at a median ρ·N of 1.0
   (range 1–5.9) where Fc⁺ enters at a median of 27.9 (27.9–32.9) and pairs with the bully. Those islands are rare, so the protection is rarely used and the lost partnerships
   are paid for everywhere.
5. **Eligibility restrictions bind only the certified branch.** An offer certificate is conditional and says nothing about the
   fallback (S_nx, by contrast, covers every profile, fallback included). Programs that are never certified-eligible for each other still form the fair pair
   through their fallbacks: Pc⁺ with Bc in 10,050 of 35,400 triples (28%). With ⅔-demanding constants in the third slot the simulating bully
   enters pair slots of (Fc, Fc), (Fc⁺, Fc⁺) and (Pc⁺, Pc⁺) at a median ρ·N of 0.5 through such fallback pairs; with every non-carrier as third
   (post hoc; queue 79's form) the median is 0.
6. **An established simulating bully persists in sixteen of 20 seeded runs.** From the seeded all-unequal start the fair share is 0.20
   at 120N and 240N: four runs entirely fair, sixteen entirely unequal. There are 2,770 unequal→fair island flips in all; of the 67
   classified as exits through an accepter, 65 are pairs imported by migration and 2 are local
   certified routes (0.56 predicted). Islands are settled in the founding scramble (0.974–0.990 keep their 30N class to 120N).
7. **The witness spellings are astronomically rare under a length prior.** Witnesses only (no exhaustive search, no minimality or
   family-scarcity claim): with scripts counted as data, the
   cheapest carriers are 10⁻⁶⁴ (Oc) to 10⁻³⁶⁹ (Pc⁺) as likely as the 6-node fair reader; with the script free they are still 10⁻²⁹·⁵ or
   rarer, because the rule and packaging take 20 nodes or more. Scripts are 41–85% of a carrier's nodes. Queue 79's skeleton Oc was 3 nodes
   under its primitive. Generality of the check was bought with length.

**Scope.** (i) N = 100–400, I = 64, one migration rate, 20 runs per cell; bootstrap half-widths are typically 0.1–0.2 at intermediate
V\*, and the A2–A1 gap of 0.14 at φ = 0 is between laws that are identical up to copies, so it measures the sampling noise of a δ-mean.
(ii) δ is a hand-set share, as in queues 75–79; finding 7 says a length prior does not supply it. (iii) Cross-spelling success is
robustness across five listed transformations under one proof convention (the packaging, the five-code statement menu, the shared checker
entry). (iv) Lost connectivity is the supported explanation of the prudence penalty in this catalogue (the eligibility loss is exact; the
population comparison does not isolate it as the only cause), measured where the dominant pair-holder cannot hold S_nx; it is not a cost of
no-exploit as such (finding 3). (v) An evaluator extension (a regress key for closure frames, exact on actions and steps; failed-read counts
differ only in 928 profiles containing a zero-mass junk program) is used for every table here, including the validations. (vi) The checker's first version (direct style) cost up to 166,456 steps, outside RE 1's registered range; it was replaced by the
continuation-passing one before any gate, and RE 1 is scored on the latter. (vii) E6's
all-non-carrier pass and the refined local/imported exit classifier (with a deterministic local rerun of the 20 seeded cells) are post hoc.

**Predictions.** Held: RE 1 (stage 1's wording "every forger rejected" fails literally: forgers are accepted for statements true of them; the stage-2
rule, no false statement accepted, is what passes), 2, 3, 5, 6, 7 (trivially: identical laws), 11; E1–E5, E7–E10. Falsified: RE 8 on both clauses (the RE
expected prudence to exclude the bully and to lower V\* at δ = 0.003 by at least 0.1; the bully's share rose and V\* was higher) and E6. Failed without
the falsifier firing: RE 4 (A2 above A1 by 0.14, outside the 0.1 band), RE 9 (0.20 fair, above 0.15; 2 local routes against 0.56), RE 10
(script-free carriers are not as abundant as the reader), RE 12 (Bc's unequal islands are not more common in A5 at every δ ≤ 0.01: 0.05 against 0.00 at δ = 0.003, equal at 0.01 and 0.001).

**What it says about realizable source-readers.** The mechanism of queue 79 is not an artefact of a spelling convention: a sound shared
checker over carried derivations lets differently written readers find each other without reading, and that is enough at founding. Three
limits remain. Certificates sort by what programs can state, not by what they do on the island at hand, so a statement strong enough to
exclude the bully (a property of every profile) also excludes the bully's fair behaviour and with it most partners. Certificates constrain
only the branch they cover. And the derivation is a long literal: on the measured witnesses a length prior supplies almost none, so the share δ has to come from the machine,
which is the reference-machine decision of 2026-11-15 in practice (the checker and the means of carrying a script are primitives of
the stated machine, reported as a choice).

**Certificates: where the program stands** (the discussion the RS attached to this write-up; world K of the PD arm).
- *What a certificate is.* A checked derivation of a statement about the carrier's own play, under a shared sound checker. Soundness was
  unconditional in the arms that have one (RESULTS "The realizable language, milestone 4", "The social organization game over the
  realizable language", "Certified offers in arm T", and here). Checking costs about 10⁴ steps; search cost
  10⁵–10⁶ and regressed between distinct readers (milestones 3 and 4).
- *What is conventional.* Three things: the checker entry, the packaging, and the statement menu. The first two are machine primitives
  under the reference-machine decision. The menu is where every admissibility question of the last month has lived: `eq` and self-keyed
  fills (identity), self-play production (provenance), and world K.
- *World K is a line of the menu.* K says a defection certificate must name a concrete defector, and so rules out the statement "I
  defect against my own kind", which was the identity lever. Queue 80 shows the same shape from the other side: S_nx is a statement over
  every profile, and requiring it excludes by what a partner could do, not by what it does. In both cases a statement quantified over
  partners sorts programs into cliques, and a statement about the play at hand does not.
- *Recommendation (the RE's proposal, not a tested conclusion; the RS's call).* Stop treating K as a pending convention. State it as part of the machine: the statement menu admits offers,
  cooperation statements and defection against a named partner, and K is that menu's rule for D. World L stays as the reference arm. What is
  not settled is who writes the first scripts (provenance; S-nonself is the operating hypothesis) and whether a profile-local prudence
  statement can be put on the menu, which is the natural next experiment.

**The model can't express:** prudence that does not cost connectivity (a certificate about the triple at hand, not about every profile);
exclusion that reaches past the certified branch into fallbacks; statements outside the checker's five codes; a certificate cited by name
instead of carried as a literal; programs writing their own scripts; a coordinated two-slot move out of a simulating bully's island;
statements about play inside another program's simulation.
