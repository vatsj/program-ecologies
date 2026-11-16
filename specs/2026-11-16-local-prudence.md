# Spec (draft, not reviewed, not launched): a profile-local prudence statement in arm T (queue 81)

Status: draft for the RS. The static reading in the first section is the RE's derivation from queue 80's definitions
and step-0 tables; nothing new was run. The RE's recommendation is at the end of that section.

Re-opens REJECTED entries: queue 76's "prudent readers restore a threshold" and queue 80's RE 8 ("certified prudence
excludes the bully"). New evidence that would justify it: queue 80 named the missing piece as a prudence statement
about the triple at hand rather than about every profile. The derivation below says that piece does not exist in the
form proposed.

## The statement, and why the obvious form is empty

Queue 80's machine (notes §1.2): a carrier x with partners n, p holds offers S_off(d; R) and may hold S_nx ("in no
profile do I demand ⅔"). The prudent carrier Pc⁺ requires S_nx of its partners. The certified bully Bc cannot hold
S_nx, because its fallback is the simulating bully. Pc⁺ therefore refuses Bc everywhere, including on the many
islands where Bc plays fair.

**Form 1, at hand: S_here = "in this triple (me, n, p) I do not demand ⅔".** A prudent carrier would require S_here
of a partner in place of S_nx.

- For a carrier, "this triple" has two cases. If its certified branch fires (some partner is eligible), it names that
  partner at ½. That is exactly what S_off already states. If no partner is eligible, its fallback plays, and for Bc
  the fallback may demand ⅔.
- So Bc holds S_here in the triple with a prudent carrier y iff y is eligible for Bc, and y is eligible for Bc iff Bc
  meets y's requirement, which is S_here. The statement is true if they pair and false if they do not. A derivation
  can only establish it conditionally ("if you are eligible for me, I do not demand ⅔ here"), and that conditional
  is S_off.
- **Consequence: a carrier that requires S_here is Fc⁺.** Form 1 adds nothing to the offer certificate. Any partner
  whose offer you accept is, by that offer, fair to you in this triple.

Prudence has content only as a counterfactual: what the partner would do to someone else, or in my absence. That is
never a statement about the play at hand.

**Form 2, about the third player present: S_k = "whoever sits in the asker's seat, I do not demand ⅔ from the third
player k in this triple".** This is S_nx restricted to the one potential victim who is actually there.

- The checker runs no one, so S_k is derivable for Bc only if k itself carries a statement that bounds its play. The
  natural one is **S_firm = "I never offer ⅓"** (a one-leaf script for a ½ constant; derivable for the carriers, Bc
  included, whose actions are ½ or ⅔ demands). The checker gains two codes: S_firm, and S_k with the atom
  chk(k, S_firm).
- A carrier **Pk** that requires S_k then behaves as Fc⁺ toward Bc beside any certified-firm third, and as Pc⁺ toward
  Bc beside any other third (⅓ constants, uncertified ½ constants, simulating readers).
- This restores most of the connectivity Pc⁺ lost: on fair islands the excluded slot is held by Bc in 0.64–0.92 of
  cases (queue 80, "who holds the fair islands").

**Where form 2 binds, it helps the bully.** The binding case is Bc's unequal island: Bc on ⅔, a ⅓ constant as
victim, the carrier arriving in the excluded slot. Queue 80's step 0 already has both behaviours there:

| arrival in the excluded slot | ρ·N (median) | island becomes |
|---|---|---|
| Fc⁺ (pairs with Bc) | 27.9 | fair, Fc⁺ and Bc on ½ each |
| Pc⁺ (refuses Bc), and so Pk | 1.0 | stays unequal, Bc keeps ⅔ |

Refusing leaves the bully on ⅔ where accepting moves it to ½ and the island into the stable set. The refuser earns
0 in place of ½. Nothing in the catalogue is protected by the refusal: a ⅓ constant arriving beside a (carrier, Bc)
pair does not break the pair (queue 80, E7: exactly neutral), so Bc does not abandon a carrier partner for a victim.

**Static predictions (no run):** Pk equals Fc⁺ on fair islands and is strictly worse than Fc⁺ on Bc's unequal
islands (entry 1.0 against 27.9, and the island stays outside V\*). In a population Pk is therefore never favoured
over Fc⁺, and V\* with Pk is at or below V\* with Fc⁺, by an amount bounded by the share of Bc-unequal islands
(≤ 0.05 in every queue 80 cell).

**Recommendation: do not build it.** In this game the certified bully is a cooperator among carriers ("converted, not
excluded", queue 79). Excluding it has no beneficiary, and the only refusal that binds rewards it. The PD analogy
misled the RE: PrudentBot is the one that exploits unconditional cooperators, so the PrudentBot of this game is the
bully itself, and "prudence against the bully" is a different thing with no counterpart in the target.

What the two open problems of queues 79–80 actually are:
1. **An established simulating bully.** It reads by simulation, so no certificate reaches it; exits need the victim's
   seat and the excluded seat to change together (the two-slot move the model cannot express), or imported pairs.
2. **Who supplies scripts.** Witness carriers are 10⁻⁶⁴ or rarer under a length prior; the machine must supply them
   (reference-machine decision), and who writes the first ones is open (Provenance).

## If the RS wants it run anyway: minimal design

Static stage only, gated; about 2 CPU-hours local, no Daytona.

- **Machine.** Queue 80's S0/S1 with two added codes: 6 = S_firm (root play never an action offering ⅓), 7 = S_k
  (root play never demands ⅔ from the third, in any profile whose third holds S_firm; atom chk(k, 6)). Soundness
  argued structurally before any gate, as queue 80 notes §1.4.
- **Programs.** Queue 80's world-S catalogue plus: Pk (Fc⁺ with R = {S_k}), in two directions and the canonical and
  inlined spellings; firm-certified ½ constants; Bc with S_firm scripts.
- **Gates.** G1 soundness cube over the new codes (0 false acceptances); G2 completeness; G3: S_k rejected for Bc
  beside every third without S_firm.
- **Step 0.** Entry rates of Pk and Fc⁺ into: pair slots of (Fc⁺, Fc⁺), (Bc, Bc), (Fc⁺, Bc) beside firm and non-firm
  thirds; the excluded slot of Bc's unequal island; and the table-equivalence test Pk ≡ Fc⁺ on triples whose third
  holds S_firm, Pk ≡ Pc⁺ on the rest.
- **Gate to dynamics.** Run A-arms (Pk replacing Pc⁺ in queue 80's A4, β = 3, φ = ½, N = 200, five δ, 20 runs) only
  if some step-0 edge has Pk entering where Fc⁺ does not, or Pk displacing Fc⁺ at ρ·N > 3.

## Predictions (the RE's)

- **RE 1.** Form 1 needs no code: a carrier requiring S_here is table-equivalent to Fc⁺ on the whole catalogue (by
  the argument above). Falsifier: any sound derivation system in which S_here is accepted for Bc unconditionally in
  a triple where Bc's fallback demands ⅔.
- **RE 2.** S_firm is derivable for every carrier family and for ½ and ⅔ constants given a script; S_k is derivable
  for Bc. Falsifier: either rejected for a program of which it is true, with no sound script found in a day.
- **RE 3.** Pk ≡ Fc⁺ on every triple whose third holds S_firm, and Pk ≡ Pc⁺ toward Bc on every other triple.
  Falsifier: any triple outside this partition.
- **RE 4.** No step-0 edge favours Pk over Fc⁺: Pk's entry rate is ≤ Fc⁺'s on every assayed edge, and 1.0 against
  27.9 (medians) on Bc's unequal island. Falsifier: one edge with Pk above Fc⁺ by a factor of 1.5.
- **RE 5.** The gate to dynamics does not fire.

## The model can't express (as it stands)

- A two-slot move out of a simulating bully's island.
- A statement that reaches a program that reads by simulation and checks nothing.
- A refusal that costs the bully something: here the refused bully keeps its victim.
