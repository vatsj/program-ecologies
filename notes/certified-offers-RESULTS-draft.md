## Certified offers in arm T (2026-11-15; queue 79)

Spec `specs/2026-11-15-certified-offers.md`; predictions `predictions/2026-11-15-certified-offers.md`; run report `runs/certified-offers.md`.

**Object.** Arm T (`dollar3`, A_f at P_fail = 0.1) with certificates: a carrier's body is a shared library combinator `CARRY` applied to a
three-bit certificate (offer toward next, toward prev, preference) and a fallback; the check `CHK` accepts exactly that skeleton and reads
the partner's flag toward me, reading and running no one. The certified rule: name at ½ the preferred partner whose certificate points back,
else play the fallback. Soundness is structural (the skeleton binds the certificate to the executed code; notes/certified-offers.md §1.3);
0 false acceptances over the catalogue cube in both machines; 8 forgers rejected. Machines: C1 (check = primitive, κ = 50 ticks; dynamics)
and C0 (the check written out in L_T^code, 167–168 steps); their tables agree on every action (856 profiles differ in one timeout charge).
Families: Oc (offer one way, ½-constant fallback), Fc (offers both ways, fallback T's firm reader), Rc (pure accepter: offer to the excluded
slot, ⅓-constant fallback), Rcs (Rc with queue 78's R as fallback), Bc (offers both ways, the simulating bully as fallback), Pc. φ = the
certified share of bullies. Finite-schedule approach rates at mN = 1, Λ = 100, 120N, not π.

**Findings.**
1. The mutual-read regress is gone between carriers: every pointing pair is the fair pair with no read in every seat pattern beside every non-carrier third program (303,024
   triples). With Rc as victim the simulating bully's read completes beside every program. Three mutually pointing carriers cycle in 2 of 8
   orientations; a slot-index tie-break (Fc\*) changes nothing measurable.
2. **A reader-share threshold under bullies.** Every certified arm has δ\* ≤ 0.01 in each cell it was run at (φ = ½; β ∈ {1, 3}; Fc, Fc+Oc, Fc+Oc+Rc, Fc+Rc and the mixed arm
   at N ∈ {100, 200, 400}; Fc+Oc+Rcs, Fc+Oc+C⅓, Fc\* and Pc+Oc+Rc at N = 200 only), and δ\* in (0.01, 0.03] with simulating bullies
   only (φ = 0; Fc and Fc+Oc+Rc at β = 3, N = 200 only). F, F+R and F+O+R have none. The matched comparison (φ = 0, same bullies and
   donor mass, readers substituted by their certified versions): β = 3, N = 200, Fc 1.00 / 0.90 / 0.60 / 0.12 / 0.15 against F 0.05 / 0.00 /
   0.15 / 0.20 / 0.15 (δ = 0.1 … 0.001). No rise of δ\* was observed across N = 100–400 (I = 64; the I = 256 check was cut; not a large-N result). Certification costs nothing without bullies (β = 0: +0.11 over F on the
   δ-mean).
3. The diagnostics support a founding-scramble reading (class agreement at two times, gates, entry assays and seeded starts; no
   experiment isolates it): carriers that point at each other pair without reading, the simulating bully's entry into a pair slot of the assayed fair carrier islands has median ρ·N ≤ 10⁻¹¹, and 0.991 of islands (main arm, β = 3, φ = ½, all δ and N) keep their 30N class to 120N. Fair islands are held by carriers.
4. Exits from simulating-bully unequal islands are unchanged: the seeded all-unequal start ends at 0.05 fair in Fc+Oc+Rc, as queue 78's
   F+R. Rc is legible and, when the excluded program does not point at it, neutral in v (ρ·N = 1 exactly; 9.75 beside a pointing
   carrier) and its second step is selected (27.9), but certified offerers rarely arrive in e
   while Rc holds v: 0.66 completions predicted from the exact rates and the realized arrivals, 1 observed. Pacing, not illegibility, binds
   the exit. Rc's certificate adds little at the population level (ablated to ⅓ constants: equal at δ ≥ 0.01, −0.105 and −0.099 at δ = 0.003 and 0.001, intervals overlapping).
5. The certified bully is converted, not excluded: it is fair with every carrier that points at it, its own unequal island opens in one
   step (any carrier pointing at it into e: ρ·N = 27.9), and at φ = ½ it holds most fair-island slots. φ raises V\* at small δ (β = 3,
   N = 200, δ = 0.003: 0.21 / 0.81 / 1.00 at φ = 0 / ½ / 1).
6. Mass (canonical spellings): with the skeleton as one primitive tag (C1), Oc and Rc are 3 nodes and weigh about 10⁵ fair readers; written
   out with `lib CARRY` 18 nodes and 10⁻¹⁹ of a reader; with the library inlined (C0) 740 nodes.

**Scope and confounds.** (i) The matched comparison (φ = 0; the readers are wrapped in the certification skeleton, an executable wrapper, not metadata: in 448 of 116,932 fallback
profiles a wrapped fallback plays differently from the same program alone, because its `me` is the carrier) was run at one
cell family, β = 3, N = 200; the N = 100 and 400 thresholds are φ = ½ only. (ii) At φ = ½ and 1 part of the bully mass is certified and,
by finding 5, cooperates with carriers, so those arms mix the certificate's effect with a reduction in hostile mass; the φ = 0 rows are
the evidence that certificates on readers alone give a threshold. (iii) δ is a hand-set share, as in queues 75–78; the mass figures in
finding 6 say that under the measured canonical-spelling prior only Oc and Rc are abundant, and only if the skeleton is a primitive; Fc and Bc
are 10⁻⁵–10⁻⁴ of a fair reader even then. (iv) I = 256 and the φ ∈ {0, 1}
extension to the other arms were cut for budget. (v) The pacing prediction counts tail arrivals only and under-predicts routes completed
among founders (23 observed against 0.9 on the unseeded main grid).

**Predictions.** Held: RE 1, 2, 3, 7, 8, 9, 10 (on the registered rule: mean signed distance outside the pure arms' interval 0.010 against 0.05; the verdict
file scored it per cell, 17 of 20 inside, and records "fails"), 11, 12; E1, E2, E3, E7, E8, E9, E10, E12. Falsified: RE 5 (no gain), RE 6, E4, E6. Failed without the
falsifier firing: RE 4 (third clause false; its falsifier, carriers excluding Bc, did not fire), E5, E11. The RE expected no threshold at β = 3; there is one. E6 failed at the registered δ = 0.1 by a ceiling (1.00 at both φ); the φ
effect is at δ ≤ 0.003. E5 failed because Fc+Rc's simulating-bully start ended at 0.20, above the registered 0.15. Provenance: predictions
were committed after the gates were read and before any step-0 assay, mass or counted cell; step-0 items 1c and 4c (entries with no
accepter resident, needed for RE 4's third clause and E3) were added after the first step-0 pass.

**What it says about realizable source-readers.** A shared, sound, cheap check of a partner's stated rule is enough for readers to find each
other in the founding scramble and to hold islands against Trojan bullies; it is not enough to dislodge an established bully. The result
holds for a syntactic convention (one library combinator, one statement form); the realizable version needs either that convention or a
checker that certifies other spellings, which was not built.

**The model can't express:** a certified rule in any other spelling; a certified statement other than the conditional ½ offer (so no
certificate excludes Bc and prudence cannot be certified); a coordinated two-slot move; a reading fallback that stays legible inside reads.

