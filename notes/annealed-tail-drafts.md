# Drafts for the RE: annealed tail on the unequal basin (queue 71)

Drafts only. RESULTS.md, REJECTED.md, THEORY.md, NOTATION.md, DEFERRED.md and CLAUDE.md are not edited. Numbers are in `runs/annealed-tail.md`
and `.json` (rows `runs/annealed_tail/rows/`).

## A. RESULTS draft

### Annealing the unequal basin: the prior's own tail cannot rescue M or L at any dose, the tail's 1/3 constants and conditionals hold the basin, and a tail without them flips it (2026-11-02)

Spec `specs/2026-11-01-annealed-tail-dollar3.md` (queue 71; the RS: "Go ahead w the annealing run", 2026-11-01; reviewed by gemini-4-argon then gpt-6.1-sol, folded),
predictions `predictions/2026-11-01-annealed-tail.md` (committed before any counted cell), notes `notes/annealed-tail.md` (§2 lists every deviation),
report `runs/annealed-tail.md` and `.json`, rows `runs/annealed_tail/`. Run by an Opus subagent (`src/annealed_tail*.py`; 7 tests, passing).
The question: RESULTS "Where the unequal basin comes from" found M's natural start ending unequal (V\* 0.1004, U 0.8996) because its boundary (0.425) sits just
under the natural unequal share (0.429) and each outcome is a ratchet that depletes the programs that could leave it, an ε = 0 statement. The object
keeps an annealed tail that trickles in prior programs. Does the tail rescue the stable-set target, and if it does, which arrivals carry it?

**Object.** `dollar3`, N = 100, w = 0.3, ε = 0 after founding in queue 70's sense, plus prior arrivals at rate ε(t) = (Λ/t₀)(1 + (t − t_s)/t₀)⁻²
per island per migrant event (Λ = total arrivals per island, t₀ = how early, t_s = tail start), uniformly random slot, program from the slot's founding prior,
fixing with the migrant's Moran kernel: dx/dt = F(x) + ε(t) G(x; p), G linear in the donor law. Arms L and M on object P (queue 70's reflecting m = 3 truncation on the
48-conditional core) from the S₃-symmetrized post-anneal law; arm T (27 programs) on its own ODE, main dose, P\_fail 0.1 and 0. Spec grid Λ ∈ {0.1 … 300}, t₀ ∈ {1, 10², 10⁴},
four DSL starts (M and L at the natural start and at the unequal tilt 0.6) and two arm-T starts (natural, tilt 0.8); then extensions (below). 390 trajectories, 46 CPU-hours.

**Validations.** The tail-free object reproduces queue 70 (and arm T, queue 69) to 10⁻⁸; the field is linear in the donor law to 10⁻¹⁹ and conserves mass to 10⁻¹⁴ with the tail. The
tail kernel against a pool Monte Carlo agrees to 0.012 at 10² and 10³ events (0.001 at I = 16,384); **the spec's gate at 10⁴ events fails (0.20) and is uninformative**: M natural is on a sharp F → U transition at 1.2·10⁴ events in
object P and the full-dynamics chain makes it earlier (the tail-free control fails identically, 0.62), so 10⁴ compares transition timing, not the kernel. The central contrast was therefore tested against the
full-dynamics chain directly (I = 8,192, two worlds, 4·10⁴ events, Λ = 300): the victim-less tail flips M to V\* (0.66 and 0.998, rising), the full tail stays unequal (0.000, 0.000). The single-arrival assay against direct Moran simulation passes (7 strata, |z| ≤ 1.6).

**1. On the specified grid the tail changes nothing.** Every endpoint equals the tail-free one: M natural and tilt 0.6: V\* 0.1004; L natural: 0.9997; L tilt 0.6: U 0.9949; arm T: ≥ 0.99999.
No Λ\* exists for M or L at any t₀, no endpoint moves by more than 10⁻⁵, and no decrease of endpoint V\* occurs on the grid. The tail is not inert: it reshapes the approach (at Λ = 300, t₀ = 100, V\* at 10⁴ events is 0.966 against 0.980), but
the F → U transition at 1.2·10⁴ events still happens and the ratchet endpoint is the same one.

**2. Extending the dose does not help, and for the fair arm it hurts.** M natural at t₀ = 100 to Λ = 10⁵ and at t₀ = 1 to Λ = 10⁴: V\* 0.1004 throughout. A very early heavy tail builds a tail-dominated quasi-state (Λ = 10⁵: F 0.375, U 0.59 within
two events) which the migration dynamics then carries to the same unequal endpoint. For L natural, t₀ = 1 holds V\* = 0.9997 to Λ = 10⁵, but at t₀ = 100 the tail carries L into the unequal state: V\* 0.9997 → 0 between Λ = 2.4·10⁴ and 3.2·10⁴ (a step).
The late tail (from M's tail-free state at τ = 10⁶; donor mass of every offering constant and of the exit constant ≤ 3·10⁻¹⁷) leaves V\* at 0.1004 at every Λ to 10⁵ (t₀ = 1, 100) and 300 (t₀ = 10⁴); its response at Λ ≤ 0.3 is linear in Λ at t₀ = 1 (exponent 1.001, 3·10⁻¹⁰ of V\* per arrival) and below the stop tolerance (10⁻⁵) at t₀ = 100 and 10⁴. Constant rain over [0, 10⁴] to Λ = 300: unchanged. Arm T keeps V\* ≥ 0.99999 at every Λ on the grid (cell 7 included),
and at Λ = 10³ and (one cell) 10⁴.

**3. The tail's own composition decides, and the prior's composition holds the basin.** Matched-dose removal of programs from the tail's arrival law (the removed mass becomes null events; the founding law is unchanged) turns M natural to
V\* = 1.0000 above a sharp Λ\* (step functions in Λ, t₀ = 100; every bracket point reproduces at 10× tighter tolerance and half the backward-Euler step):

| tail (matched dose) | Λ\* (bracket) | removed prior mass per slot |
|---|---|---|
| full | none up to 10⁵ | 0 |
| without the two Trojan bullies | (274, 316] | 3.7·10⁻⁵ |
| without the two 1/3 constants ("victims") | (75, 87] | 0.217 |
| without bullies and victims | (48.7, 56.2] | 0.217 |
| without every conditional (constants only) | (750, 866] | 0.023 |

The bullies are 5,850 times rarer in the tail than the offering constants and still move Λ\* from none to about 295, which the static count (reviewers' and the RE's, argon's) would not predict: arrivals are
selected in unequal islands (+1/6, 4.9 times neutral), so rare ones are amplified. The pattern is not additive: both victims and conditionals impede, and the full tail has all of them. The renormalized variants at Λ = 100 give the same classes. The clean tail's Λ\* depends on t₀: (31.6, 36.5] at t₀ = 1, (48.7, 56.2] at 100, (316, 365] at 10⁴;
at the settled ratchet (t_s = 10⁶, t₀ = 1) the victim-less and the victim- and bully-less tails do not flip at any Λ ≤ 10⁴ (victim-less 10²–10⁴). On the deep tilt (u = 0.6) the clean tail flips both arms but needs much more: M (649, 750] at t₀ = 1 and (750, 866] at t₀ = 100, L (133, 154] and (178, 205], that is 13–24 times M natural's (31.6, 36.5] and (48.7, 56.2].
Just below Λ\* (victim-less 75) the endpoint is the unequal one with support four programs per slot (bully, yielder families) and an exchange of 1.24·10⁻³ per event each way between F and U islands, identical to the tail-free
endpoint's; just above (86.6) it is V\* absorbing: the fair half-constants and fair readers at 0.25 each, no flux between classes, the three pairs at ⅓.

**4. The direct tail flux cannot assign the effect.** Integrated to 10⁴ events at Λ = 100, the tail's own class-changing flux is two orders below the migrants' (U → F 0.009 against 0.98), and nearly identical for the full and the victim-less tails (within about 10%)
while their endpoints are opposite. By source category, 96% of the tail's U → F flux is the exit constant arriving in the underpaid slot of a U island whose excluded slot already holds an offering constant (the RE's mechanism, correct as a description of that small flux), and its F → U flux is carried by the 2/3 constants (94%), the 1/3 constants and bullies carrying 4%.
So the effect is a knife-edge in the donor composition that migration amplifies, not a flux balance: M natural sits 0.004 in u inside its basin and a clean tail of tens of arrivals moves it across; at the deep tilt 0.6 the clean tail needs 13–24 times more (a tilt of 0.6 is 0.175 inside M's basin, 0.05 inside L's).

**5. N.** In the hybrid object (fixation kernel at N, founding law at N = 100) the tail-free endpoint of M natural stays unequal and strengthens (V\* 0.1004, 0.0580, 0.0325 at N = 100, 200, 400), the full tail still has no Λ\*, and the victim-less tail's Λ\* is (75, 87], (2,054, 2,371] and (10,000, 11,548] at N = 100, 200, 400:
×24–32 for the first doubling and ×4.2–5.6 for the second, not proportional to N and not a power law. A fixed tail dose is therefore a vanishing remedy as N grows even for the clean tail.

**6. Objects and symmetry.** With one conditional per island (on the 48-core, or over all 1,296) the tail-free M natural is already fair (V\* 1.0000) and the tail does not move it (to Λ = 10⁴): the disagreement with object P is the truncation in m, as queue 70 found, not the core. The tail's
blocked flux in object P is 0.1% at the start and 1.6% at the tail-free endpoint (arrivals of non-core conditionals into islands that already hold one). An S₃-asymmetric perturbation (1e-3) of the rescued endpoint keeps V\* = 1.0000 and the raised pair takes over (pairs 1, 0, 0 by 10⁶ events), 10⁻⁶ stays symmetric to 10⁶; L's tail-free fair endpoint behaves the same (0.61, 0.06, 0.32 at 10⁻⁶).

**Predictions** (full table in the report): RE 1 failed (max V\* over Λ ≤ 30: 0.1004); RE 2 vacuous for the full tail and held for the clean tail (early Λ\* 31.6–36.5 against no late flip to 10⁴); RE 3 vacuous; RE 4 held on the spec grid and failed in the extension (L natural, Λ ≈ 3·10⁴);
RE 5 failed (the E-offers share 0.96 held, the second share 0.04 and the bully clause failed, the victim clause held); RE 6 failed (Λ\* ratio 115–154 for the one series that has one); RE 7 failed. Argon (a) half failed (bully), half held (victim); argon (b) failed; sol (c) held for the clean tail (M natural 18–24 times easier than M u = 0.6 at t₀ = 1, 13–18 at 100, and the settled ratchet does not flip), (d) and (e) held; engineer E1, E3, E4 failed, E2, E5, E7 held, E6 held vacuously. The static argument that bullies cannot matter in the tail (my E3 for victims, argon's and the RE's for bullies) was wrong in both directions: victims matter (the RE and argon were right), and bullies matter though 5,850 times rarer.

**What it means.** (i) The DSL arms' failure of the stable-set target is not a property of the tail-free object: the annealed tail, drawn from the arms' own prior at any dose, leaves M (and L's unequal tilt) unequal and, at a heavy early dose, moves the fair arm L to the unequal state. (ii) A tail with the programs that hold the basin removed does flip M, by tens of arrivals per island at N = 100
and by amounts growing faster than N — so the tail's arrival law is a design choice of the object, not a neutral background: which programs may be trickled in is the question. (iii) The "means of trickling in predators" reading of the tail does not survive as a rescue for these arms: the trickled predators (bullies) are what cost the rescue. The RS's admissibility rule for the tail (drift never colonizes, only reintroduces fit programs) is silent here: both the helpful and the blocking arrivals are neutral entries followed by a selected step.
Limits: object P (m = 3, 48-core) with the F → U transition timing differing from the full chain (V3); the mechanism of the block (why victims and conditionals impede) is not established, only its composition; N scaling is the hybrid object; the library is the length prior's, not a realizable library (the RE's call whether the clean-tail result transfers to arm T-style libraries, where the tail changes nothing because there is no basin).

## B. REJECTED draft

- **"The tail pushes M's natural start toward V\*: some Λ ≤ 30 gives V\* ≥ 0.99, monotone in Λ" (RE prediction 1, annealed tail, 2026-11-01).** Failed: the endpoint is the tail-free 0.1004 at every Λ to 10⁵ (t₀ = 100), to 10⁴ (t₀ = 1) and ≤ 300 (t₀ = 10⁴); a heavy early tail drives a tail-dominated quasi-state (F 0.375, U 0.59) that migration carries to the same unequal endpoint. RESULTS "Annealing the unequal basin".
- **"A late tail must rebuild a rescue supply; Λ\*(late) ≥ 10 Λ\*(t₀ = 1)" (RE prediction 2).** Unscored for the full tail (neither flips); held for the clean tail (early (31.6, 36.5], no late flip to 10⁴). Same section.
- **"Constant rain and the t₀ = 100 tail have Λ\* within a factor 3" (RE prediction 3).** Vacuous: neither flips. Same section.
- **"L natural and arm T end at V\* ≥ 0.999 at every Λ and t₀" (RE prediction 4), beyond the spec grid.** Held on the grid; the extension falsifies it for L (t₀ = 100, Λ ≈ 3·10⁴: V\* 0.9997 → 0), so "no harm to the fair arm" holds only for doses below about 10⁴ at N = 100. Same section.
- **"The rescue is carried by excluded-slot offering constants (≥ 0.7); victims with bullies carry the V\* → U flux (≥ 0.7); bully ablation < 1.25×; victim ablation ≥ 1.5×" (RE prediction 5, argon (a), engineer E3).** Failed: the offering-constants share is 0.96 of the tail's small U → F flux (held), but the F → U flux is carried by the 2/3 constants (94%), victims and bullies 4%; removing the bullies moves Λ\* from none to (274, 316] (RE and argon said < 1.25× and < 1.05×); removing the victims moves it to (75, 87] (held; my E3, that they barely matter, failed). Same section.
- **"Λ\*(400)/Λ\*(100) ∈ [2.5, 6]; both directions start neutral so Λ\* ∝ N" (RE prediction 6; argon (b), < 2.5).** Failed: no Λ\* for the full tail; for the victim-less tail the ratio is 115–154 (×24–32, then ×4.2–5.6). Same section.
- **"L at the unequal tilt flips at Λ\* ≤ 10 for t₀ = 1" (RE prediction 7).** Failed: L u = 0.6 stays at U 0.9949 at every Λ ≤ 300; the clean tail flips it at (133, 154] for t₀ = 1 and (178, 205] for t₀ = 100. Same section.
- **Engineer E1 (Λ\*(M nat, t₀ = 1) ≤ 3, t₀ = 100 ≤ 10) and E4 (the constants-only tail has Λ\* within 1.25× of the full tail's).** Failed: none to 10⁵ (t₀ = 100; to 10⁴ at t₀ = 1); constants-only (750, 866]. Same section.
- **"The tail kernel is validated by agreement of V\* at 10⁴ events (V3)" (spec gate).** Not met and uninformative: the 10⁴ point is the F → U transition's timing, which differs between object P and the full chain (the tail-free control disagrees by 0.62). Replaced by agreement at 10², 10³ and the central contrast in the full-dynamics chain (V3b). Same section.
- **"The tail is a vanishing-remedy-at-fixed-Λ in the sense Λ\* ∝ N" (spec's structural point).** Not what happens: the clean tail's Λ\* grows faster than N (×24–32 then ×4.2–5.6). Same section.

## C. THEORY note (proposed; the RE decides)

THEORY §9.2 / the stable-set target (DEFERRED 15): add, with the reason "RESULTS 'Annealing the unequal basin'": the DSL arms' failure of the stable-set target persists under the annealed tail drawn from their own prior (no Λ\* to 10⁵ for M natural, L tilt 0.6, M tilt 0.6), so it is not an ε = 0 artefact; and a tail that excludes the 1/3 constants and the conditionals flips M natural at Λ\* ≈ 35–90 at N = 100, with Λ\* growing faster than N. The
tail's arrival law is part of the object. No claim in THEORY moves otherwise.

## D. NOTATION entries

- **Annealed tail (queue 71):** **Λ** — total prior arrivals per island delivered by the tail; **t₀** — the tail's time scale, ε(τ) = (Λ/t₀)(1 + τ/t₀)⁻² (Anneal) or ε = Λ/T on [0, T] (Const, "constant rain"); **t\_s, τ = t − t\_s** — tail start and the tail clock (events per island since t\_s; t\_s = 0 at founding, 10⁶ in the late arm); **G(x; p)** — the migration field with donor law the prior p restricted to the state set (null events for programs outside it); **restricted mass** — prior mass of the programs in the state set; **Λ\*** — the smallest Λ whose endpoint has V\* ≥ 0.5 (first upward crossing), bisected in log Λ to a factor 1.25; **Λ\_harm** — the same for a fair start crossing downward; **matched-dose ablation** — programs removed from the tail's arrival law, their mass turned into null events, the rest keeping its dose (renormalized: the rest rescaled); **victims** — the two constants naming a slot partner at 1/3 (mass 0.217 per slot); **bullies** — the two `exploiter-fair` programs per slot; **clean tail** — the tail without victims and bullies; **burst protocol** — classification of a run whose remaining tail dose was still above 10⁻⁴ per island at stationarity, by continuing tail-free and with the remaining dose delivered at once (classified only if they agree); **tail-dominated quasi-state** — the law reached within a few events by a very heavy early tail (M: F 0.375, U 0.59).
