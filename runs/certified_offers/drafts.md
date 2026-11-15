# Queue 79 drafts for the RE (RESULTS, REJECTED, NOTATION)

Source: `runs/certified-offers.md` (run report), `runs/certified-offers.json` (verdicts), `predictions/2026-11-15-certified-offers.md`.
All step-2 numbers are finite-schedule approach-rate statistics (mN = 1, Λ = 100, 120N), not π.

## RESULTS draft: "Certified offers in arm T"

Spec `specs/2026-11-15-certified-offers.md`; predictions `predictions/2026-11-15-certified-offers.md`; run report `runs/certified-offers.md`.

**Object.** Arm T (`dollar3`, A_f at P_fail = 0.1) with certificates: a carrier's body is a shared library combinator `CARRY` applied to a
three-bit certificate (offer toward next, toward prev, preference) and a fallback; the check `CHK` accepts exactly that skeleton and reads
the partner's flag toward me, reading and running no one. The certified rule: name at ½ the preferred partner whose certificate points back,
else play the fallback. Soundness is structural (the skeleton binds the certificate to the executed code; notes/certified-offers.md §1.3);
0 false acceptances over the catalogue cube in both machines; 8 forgers rejected. Machines: C1 (check = primitive, κ = 50 ticks; dynamics)
and C0 (the check written out in L_T^code, 167 steps); their tables agree on every action (856 profiles differ in one timeout charge).
Families: Oc (offer one way, ½-constant fallback), Fc (offers both ways, fallback T's firm reader), Rc (pure accepter: offer to the excluded
slot, ⅓-constant fallback), Rcs (Rc with queue 78's R as fallback), Bc (offers both ways, the simulating bully as fallback), Pc. φ = the
certified share of bullies. Finite-schedule approach rates at mN = 1, Λ = 100, 120N, not π.

**Findings.**
1. The mutual-read regress is gone between carriers: every pointing pair is the fair pair with no read in every seat pattern (303,024
   triples). With Rc as victim the simulating bully's read completes beside every program. Three mutually pointing carriers cycle in 2 of 8
   orientations; a slot-index tie-break (Fc\*) changes nothing measurable.
2. **A reader-share threshold under bullies.** Every certified arm has δ\* ≤ 0.01 at β ∈ {1, 3} and N ∈ {100, 200, 400} (φ = ½), and
   δ\* in (0.01, 0.03] with simulating bullies only (φ = 0). F, F+R and F+O+R have none. The matched comparison (φ = 0, same bullies and
   donor mass, readers substituted by their certified versions): β = 3, N = 200, Fc 1.00 / 0.90 / 0.60 / 0.12 / 0.15 against F 0.05 / 0.00 /
   0.15 / 0.20 / 0.15 (δ = 0.1 … 0.001). δ\* does not rise with N. Certification costs nothing without bullies (β = 0: +0.11 over F on the
   δ-mean).
3. The mechanism is the founding scramble: carriers that point at each other pair without reading, a fair carrier pair is closed to the
   simulating bully (ρ·N ≤ 10⁻¹¹ into a pair slot), and 0.991 of islands keep their 30N class to 120N. Fair islands are held by carriers.
4. Exits from simulating-bully unequal islands are unchanged: the seeded all-unequal start ends at 0.05 fair in Fc+Oc+Rc, as queue 78's
   F+R. Rc is legible and neutral in v (ρ·N = 1 exactly) and its second step is selected (27.9), but certified offerers rarely arrive in e
   while Rc holds v: 0.66 completions predicted from the exact rates and the realized arrivals, 1 observed. Pacing, not illegibility, binds
   the exit. Rc's certificate adds little at the population level (ablated to ⅓ constants: equal at δ ≥ 0.01, −0.10 below).
5. The certified bully is converted, not excluded: it is fair with every carrier that points at it, its own unequal island opens in one
   step (any carrier pointing at it into e: ρ·N = 27.9), and at φ = ½ it holds most fair-island slots. φ raises V\* at small δ (β = 3,
   N = 200, δ = 0.003: 0.21 / 0.81 / 1.00 at φ = 0 / ½ / 1).
6. Mass (canonical spellings): with the skeleton as one primitive tag (C1), Oc and Rc are 3 nodes and weigh about 10⁵ fair readers; written
   out with `lib CARRY` 18 nodes and 10⁻²⁰ of a reader; with the library inlined (C0) 740 nodes.

**What it says about realizable source-readers.** A shared, sound, cheap check of a partner's stated rule is enough for readers to find each
other in the founding scramble and to hold islands against Trojan bullies; it is not enough to dislodge an established bully. The result
holds for a syntactic convention (one library combinator, one statement form); the realizable version needs either that convention or a
checker that certifies other spellings, which was not built.

**The model can't express:** a certified rule in any other spelling; a certified statement other than the conditional ½ offer (so no
certificate excludes Bc and prudence cannot be certified); a coordinated two-slot move; a reading fallback that stays legible inside reads.

## REJECTED draft

- **RE 6 (no certified threshold at β = 3)**, queue 79: falsified. Every certified arm has δ\* ≤ 0.01 at β = 3, every N (φ = ½), δ\* ≤ 0.03 at
  φ = 0. The RE's reading "single-slot pacing and the founding scramble bind" was half right: the scramble decides, and certificates win it.
- **RE 5 (legibility lifts the seeded unequal start to (0.05, 0.3))**, queue 79: falsified on the "no gain" side (0.05 = queue 78's F+R). The
  exit route is paced (0.66 predicted, 1 observed completion).
- **RE 4, third clause (Bc's own unequal island resists like the simulating bully's)**: falsified. Any carrier pointing at Bc enters its
  excluded slot at ρ·N = 27.9 and pairs with it (1 on the simulating bully's island). Dropped reading: "the certified bully is a faker that
  carriers must exclude"; it is a cooperator among carriers.
- **E4 (exact neutrality of ⅓ constants in the third slot of (Fc, Bc))**: falsified by residents that paid read charges (ρ·N up to 5.9).
- **E6 (φ = 1 above φ = 0 by ≥ 0.2 at δ = 0.1)**: falsified at the ceiling (both 1.00); the φ effect is at δ ≤ 0.003.
- **Dropped reading (queues 76/78):** "no reader arm can have a threshold under Trojan bullies in arm T." It held for simulating readers only;
  it was illegibility at founding.
- **Dropped reading (queue 78):** "O or F can be R's offerer" is now true for their certified versions in the gates and step 0, but buys
  nothing at the population level (pacing); not re-opened further.

## NOTATION draft (queue 79)

- **Certified offers (queue 79):** **carrier** — a program whose body is `CARRY cert fb me n p`; **certificate** (fn, fp, pref) — offer
  toward next / prev (bits), preference (0 next, 1 prev); **CARRY** — the shared library combinator executing the certified rule;
  **CHK** — the skeleton check (T iff the partner is a carrier whose flag toward me is 1); **skeleton** — λme. λn. λp.
  (((((lib CARRY) CERT) FB) me) n) p with CERT a literal of three bits and FB a λ; **E** — the eligibility set (partners whose certificate
  points back); **pointing** — x's certificate offers toward y's slot; **active / inactive** — whether the excluded slot's certificate
  points at the victim; **S(t)** — a carrier's certified statement; **C0 / C1** — the check written out in L_T^code / a primitive charged
  **κ** = 50 ticks; **forger** — a program built to pass the check without the skeleton (gate only).
- **Families:** **Oc** (Ocn, Ocp) certified opener (offer one way, ½-constant fallback); **Fc** (Fc + each of T's 16 firm readers)
  certified firm reader; **Rc** (Rcn, Rcp) pure certified accepter (offer to the excluded slot, ⅓-constant fallback); **Rcs** hybrid (fallback
  queue 78's R); **Bc** (Bcn, Bcp) certified Trojan bully (offers both ways, the simulating bully as fallback); **Pc** certified prudent
  reader (fallback P_z); **Fc\*** — the comparator with three-carrier cycles broken by slot index (slots 0 and 1 pair); **φ** — the certified
  share of bully mass; **Fc+Oc+C⅓** — the main arm with Rc's mass given to C3 and C0.
- **Step-1 measures:** **C1 measure** — R1 plus an arity-2 tag `carry(c, B)` (c = fn + 2 fp + 4 pref); **R1-written** — the skeleton with
  `lib CARRY`; **C0-written** — the library inlined, R0 tags.
- **Pacing records:** Rc victim-seat exposure (island-generations), first steps (Rc into v) and second steps (a certified offerer into e
  with Rc in v, or Rc into v beside one), each with Σρ from the exact formula in its resident majority triple; predicted completions = Σρ
  of second steps.
