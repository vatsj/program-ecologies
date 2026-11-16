# Queue 80 drafts for the RE (RESULTS, REJECTED, NOTATION)

Source: `runs/script-checked-offers.md`, `runs/script-checked-offers.json`, `notes/script-checked-offers.md`. Not merged into the shared
docs by the subagent.

## RESULTS draft: "Script-checked offers in arm T"

Queue 80 (spec `specs/2026-11-16-script-checked-offers.md`; predictions `predictions/2026-11-16-script-checked-offers.md`). Finite-schedule
approach-rate statistics (I = 64, mN = 1, Λ = 100, 120N), not π; N = 100–400 exploratory.

Queue 79's certificate was one fixed spelling around a shared library routine. Here a carrier is any program with a script, and a shared
checker CHKS written in L_T^code verifies the script as a derivation (a case tree over the open atoms, each leaf checked by symbolic
evaluation of the body with the partners' quotes opaque) that the program satisfies a statement: an offer S_off(d; R) with a
requirement R, or no-exploit S_nx. Soundness is a structural theorem (notes §1.4). Gates: 0 false acceptances in 7.9 million (statement
× profile) checks, executed (S0) and tabulated (S1) machines identical on 4.6 million profiles; all 100 carriers in five spellings
accepted; the worst check costs 15,141 ticks, so fuel was raised from (1,200, 400) to (384,000, 128,000); queue 78's 59 programs
behave identically at the new fuel.

1. **The threshold survives a real checker.** Canonical script carriers (A1) reach δ\* = 0.03 (φ = 0) and 0.01 (φ = ½) at β = 3,
   N = 200; the uncertified controls at the same fuel have none. A1 is queue 79's skeleton machine exactly: the tables coincide in
   actions and charges on every triple the laws use.
2. **Spellings pair; the skeleton convention did not let them.** Every mutually eligible pair forms the fair pair in all five spellings,
   with no read. Spellings are behaviourally identical, so splitting a family's mass over them (A2) is A1's law (δ\* 0.03 / 0.01;
   δ-means 0.68 / 0.90 against 0.54 / 0.88, sampling). Under the skeleton check four of five spellings are invisible, and the same split
   (K2) falls to δ-mean 0.40 at φ = 0 (δ\* 0.1).
3. **Certified prudence hands the fair islands to the certified bully.** Pc⁺ (requires S_nx) refuses Bc (which cannot hold S_nx), loses
   most partners and holds 1.7% of paired fair-island slots (A4), while Bc's share rises from 0.67 (A2) to 0.79 and V\* does not fall
   (0.95 against 0.85 at δ = 0.003). When everyone requires S_nx (A5) Bc holds 94% of paired slots, paired only with Bc, at unchanged
   V\* (δ-mean 0.88). Prudence does reclose Bc's own unequal island (Pc⁺ enters its excluded slot neutrally, 1.0 against 27.9 for Fc⁺),
   but those islands are rare (≤ 5%). Fallbacks pair with excluded programs anyway (Pc⁺–Bc in 28% of triples).
4. **Exits from the simulating bully's islands stay paced.** From the all-unequal start, 0.20 fair at 240N (four whole runs); 65 of 67
   accepter exits are imported pairs, 2 local certified routes against 0.56 predicted.
5. **The convention is expensive under a length prior.** Script carriers are 10⁻⁶⁴ (Oc) to 10⁻³⁶⁹ (Pc⁺) of the 6-node fair reader with
   scripts counted, and 10⁻²⁹·⁵ or rarer with scripts free (witnesses).

Verdicts: RE 1, 2, 3, 5, 6, 7, 11 hold; RE 8 falsified; RE 4, 9, 10, 12 fail without their falsifiers firing; E1–E5, E7–E10 hold, E6
falsified. The model can't express: profile-local prudence, exclusion beyond the certified branch, statements outside the checker's menu,
a cheap (cited) certificate, script production, a coordinated two-slot move.

## REJECTED drafts

- **RE 8 (queue 80): "certified prudence excludes the bully and buys no V\*".** Falsified on both clauses: in A4 Bc's share of paired
  fair-island slots rises (0.79 against A2's 0.67) and V\* at δ = 0.003 is higher (0.95 against 0.85). Pc⁺ is selected out (1.7% of
  paired slots), not Bc. Dropped: "prudence certificates displace the faker"; the requirement costs the prudent reader its partners.
- **RE 12 (queue 80): A5's second clause** (Bc's unequal islands more common than in A2 at δ ≤ 0.01) fails: Bc on ⅔ on 0–5% of islands in
  both arms. Bc keeps fair islands by pairing with itself (100% Bc-partnered), not by bullying.
- **RE 10's second clause (queue 80):** "script carriers are at least as abundant as the reader if the script is not charged" fails:
  even script-free they are ≤ 10⁻²⁹·⁵ of the fair reader (the rule and packaging are ≥ 20 nodes). (The first draft, "at least as
  abundant as the fair reader", was already revised before the run.)
- **RE 4's 0.1 band (queue 80):** A2 is above A1 by 0.14 at φ = 0; the two laws are identical up to copies of equivalent programs, so the
  difference is sampling. The band was too narrow for 20 runs × 5 δ, not a property of spellings.
- **RE 9's pacing ratio (queue 80):** 2 local certified routes against 0.56 predicted (factor 3.6) and 0.20 fair at 240N (> 0.15); the
  exits that occur are imported pairs.
- **E6 (subagent, queue 80): "the simulating bully cannot break carrier pairs".** With ⅔-demanding constants as third slots it enters
  pair slots of (Fc, Fc), (Fc⁺, Fc⁺), (Pc⁺, Pc⁺) neutrally in half the seat patterns, pairing with the remaining carrier's fallback;
  with every non-carrier as third, the median is 0 (queue 79's result).

## NOTATION drafts

- **CHKS** — queue 80's shared script checker (library entry): `CHKS (x . c)` is T iff the quote x carries a script whose entry for
  statement code c is a valid derivation; at most KCHK + 5 = 16,005 ticks. **CCORE** its core (L_T^code); **S0** CCORE executed,
  **S1** CCORE as a primitive with S0's exact value and tick count per (quote, code).
- **Carrier (queue 80)** — any program with a script, packaged `λme.λn.λp.(if T B SCRIPT)`.
- **S_off(d; R)** — "if d is my preferred member of E, I name d at ½", E computed with requirement R; codes 1–4 (toward next / prev, asked
  with h = ∅ or {S_nx}, accepted iff R ⊆ h). **S_nx** — "I never demand ⅔" (codes 2, 5, 8), code 5. **H_x** — x's declared holding of
  S_nx; **R_x** — x's requirement.
- **E_x (queue 80)** — s ∈ E_x iff x offers toward s, CHKS(s, OFF(toward x; H_x)) = T and (R_x = {S_nx} → CHKS(s, S_nx) = T).
- **κ_S** — the worst accepted S0 check cost (15,141). **cap', KR'** — the raised read cap and root fuel (128,000, 384,000).
- **Oc⁺, Rc⁺, Fc⁺** — Oc, Rc, Fc that also hold S_nx (H = {S_nx}, R = ∅). **Pc⁺** — Fc⁺ with R = {S_nx}. **OcR⁺, RcR⁺** — Oc⁺, Rc⁺ with
  R = {S_nx} (arm A5).
- **Spellings** — `canon` (the shared rule OFFER), `inl`, `rord`, `guard`, `noelig` (world S); `canon`, `inl`, `rord`, `guard`, `alias`
  (world K, queue 79's skeleton machine).
- **Arms** — U (uncertified F, F+R at the new fuel), K (queue 79's skeleton machine, canonical), K2 (K on A2's spelling split), A1
  (script checker, canonical), A2 (spellings split), A3 (⁺ families), A4 (Pc⁺ + Oc⁺ + Rc⁺), A5 (Pc⁺ + OcR⁺ + RcR⁺).
- **Fallback pair** — a fair pair formed by two programs' fallbacks although neither is certified-eligible for the other.
- **Closure regress key** — queue 80's evaluator extension: `capk` frames with a closure function are keyed by (cap, body, environment,
  argument), so milestone 3's regress lemma fast-forwards them.
