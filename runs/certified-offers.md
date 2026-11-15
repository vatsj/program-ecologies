# Queue 79: certified offers in majority division (run report)

Spec `specs/2026-11-15-certified-offers.md` (gemini-4-carbon, then gpt-6.1-sol `--mode amended`, both folded). Predictions
`predictions/2026-11-15-certified-offers.md` (committed b081485, after the gates and before any step-0 assay, step-1 mass or counted cell;
addenda disclose the V1 fix, the budget cut and its partial restoration, and the step-0 items added after the first step-0 pass). Data:
`runs/certified_offers/` (gates, step 0, step 1, `step2_report.md`, `step2.json`, `v1.json`), rows `runs/co_rows/`, verdicts
`runs/certified-offers.json` (`src/certified_offers_verdicts.py`). Notes, deviations and operations: `notes/certified-offers.md`.
**All step-2 numbers are finite-schedule approach-rate statistics (mN = 1, Λ = 100, 120N; seeded starts to 240N), not π.**

## Headline

1. **A reader-share threshold exists under bullies, for the first time in arm T.** Every certified arm reaches V\* = 1.00 at δ = 0.1 and
   0.03 at β = 1 and β = 3 and N = 100, 200, 400, with δ\* in (0.001, 0.01] at φ = ½ and in (0.01, 0.03] with simulating bullies only
   (φ = 0). Queue 75's F, queue 78's F+R and F+O+R have no δ\* at β ≥ 1 anywhere (V\* mostly ≤ 0.4, at most 0.75). The clean comparison is φ = 0, where
   the only difference from the stored rows is the certificate on the same readers: at β = 3, N = 200, Fc gives 1.00 / 0.90 / 0.60 / 0.12 /
   0.15 (δ = 0.1 … 0.001) against F's 0.05 / 0.00 / 0.15 / 0.20 / 0.15.
2. **The mechanism is the founding scramble, not the exit route.** Carriers that point at each other form the fair pair with no read
   (G2), and a fair carrier pair is closed to the simulating bully (ρ·N ≤ 10⁻¹¹ into a pair slot). Islands are decided by 30N (main arm,
   β = 3: 0.991 of islands keep their 30N class to 120N), and at δ = 0.03, φ = ½, no island of Fc or Fc+Oc+Rc is unequal at 30N. Fair islands are held by carriers
   (Fc φ = 0, β = 3, δ = 0.03: 3,392 of 3,456 fair-island slots, excluded slots included; the other 64 are bullies; no constant).
3. **Exits from bully-held unequal islands stay paced, as the RE expected.** From the seeded all-unequal start with the simulating bully,
   Fc+Oc+Rc ends at 0.05 fair (queue 78's F+R: 0.05). Rc's certificate makes the victim legible (the bully's read of Rc always
   completes, Rc enters at ρ·N = 1 exactly, and its second step is selected at 9.75 / 27.9), but the second step needs a certified offerer
   in e while Rc holds v: 8 such arrivals in 20 runs × 64 islands, 0.66 completions predicted from the exact rates, 1 observed.
4. **The faker does not ride along; it is converted.** A certified bully (Bc) is fair with every carrier that points at it. Its own unequal
   island opens in one step (any carrier pointing at it into e: ρ·N = 27.9), which falsifies RE 4's third clause. At φ = ½ Bc holds most
   fair-island slots (FcOcRc β = 3 δ = 0.03: 3,120 of ~3,840), and φ raises V\* at low δ (β = 3, δ = 0.003: 0.21 / 0.81 / 1.00 at φ = 0 /
   ½ / 1).
5. **What the readers could not express in queue 78 is now expressed, at the cost of a convention.** The certificate is a skeleton bound to
   one shared library combinator; any other spelling of the same rule is rejected. Under the C1 measure (the skeleton as one primitive tag)
   Oc and Rc are 3 nodes and weigh 10⁵ fair readers; written out with `lib CARRY` they are 18 nodes and 10⁻²⁰ of a reader; with the library
   inlined (C0), 740 nodes.

## Programs, certificates and gates (`runs/certified_offers/gates.md`)

A **carrier** is a program whose body is `CARRY cert fb me n p`: a shared library combinator, a three-bit certificate (offer toward next,
offer toward prev, preference) and a fallback λ. The check `CHK` accepts exactly that skeleton and reads the partner's flag toward me; it
reads no one and runs no one. The certified rule is the one the spec's second review asked for: E = the partners whose certificate points
back at me; name the preferred member of E at ½, else play the fallback. Soundness is structural (notes §1.3: the skeleton binds the
certificate to the executed code; the check is a bounded total function of the partner's quote; the certified branch fits the root fuel).
The certificate is degenerate as a "script": its proof is the skeleton. **C1** charges a check κ = 50 ticks; **C0** is the check written
out in L_T^code (167–168 steps per accepted quote).

K = 87: queue 78's 59 programs, Oc (2), Fc (Fc + each of T's 16 firm readers as fallback), Rc (2, pure: fallback the ⅓ constant), Rcs (2,
fallback queue 78's R), Bc (2, fallback the simulating bully), Pc (4, fallback the four P_z).

- **G1 soundness.** The check map is identical in C0, C1 and the host reference on 95 programs and forgers; all 8 forgers rejected (the bully
  body with Ocp's certificate in milestone 4's shape, a lookalike combinator, swapped variables, a non-value fallback, malformed and computed
  certificates, the skeleton under `if T`, certificate data as a value). Certified-branch profiles 95,000 per machine, **0 false**. In 448 of
  116,932 fallback profiles a fallback plays differently from the same program standing alone, because inside a carrier its `me` is the
  carrier.
- **G2 reader–reader.** Every pointing pair (Oc×Rc, Oc×Fc, Fc×Fc, Rc×Rc, Fc×Rc, Pc×Pc, and Rcs, Bc pairs) is the fair pair in every seat
  pattern beside every non-carrier, 0 timed-out reads by the pair, both machines. Three mutually pointing carriers ((Fc)³, (Pc)³,
  (Bc, Fc, Fc)): 2 of 8 preference orientations cycle; mean gross payoff per slot 0.250 against 1/3 for a cycle-free rule.
- **G3 legibility.** With Rc as victim the simulating bully's read completes beside every excluded-slot program (0 timeouts, against queue
  78's R: timeouts beside every reader). Beside Fc, Pc, Bc and the Oc oriented at the victim the island is the fair pair (v, e); beside
  constants, simulating readers and non-pointing carriers it stays unequal. **On the certified bully's island** (Bc on ⅔), any carrier in e
  that points at Bc pairs with it: Fc gives (b, e) in 24 of 48 triples and (v, e) in 24, by its preference.
- **G4 mixed worlds.** Every timed-out read in a triple with a carrier and a simulating reader persists with all caps and the root fuel
  ×20 (0 cap exhaustions in 7,000+ sampled profiles, including the simulating bully against Fc and Bc against F): the timeouts are the mutual
  regress through the fallbacks of Fc, Bc, Pc, Rcs. Pure Oc and Rc never time out.
- **G5.** The first 59 programs' tables equal queue 78's. **V3:** C1 and C0 agree on every action over the 658,503 profiles; 856 profiles
  differ in a timeout charge only (C0's dearer check), 0 outcome triples differ. V3 holds for actions; payoffs differ in those 856 profiles
  by one P_fail.

## Step 0 (`runs/certified_offers/step0.md`; ρ·N at N = 200, w = 0.3, A_f charges; 1 = neutral)

Checks: jump chain (60 non-neutral assays) max |z| 2.63; kernel (16 assays × 3,000 islands) max |z| 2.17.

| edge | ρ·N | rate per arrival (main law) |
|---|---|---|
| Rc (matched) into v of a simulating-bully island, e not pointing at v (constants, simulating readers, junk, non-pointing carriers; 366 assays) | exactly 1 (min = max = 1) | 7.5e-5 |
| the same with e pointing at v (Fc, Pc, Bc, matched Oc, Rc, Rcs; 150) | 9.75 | 7.3e-4 |
| queue 78's R / the hybrid Rcs beside a simulating reader | 1.4e-10 | – |
| Rcs beside a pointing carrier / a ½ constant naming it | 9.75 / 9.75 | – |
| Fc / matched Oc / Bc / Pc into e with Rc resident | 27.9 (all) | 1.3e-4 / 1.0e-3 / 3.2e-3 / – |
| ½ constant, simulating readers, mismatched Oc into e with Rc resident | 1 (median) | – |
| any carrier pointing at the bully into e of the simulating bully's island, no Rc | 1 (median) | – |
| **any carrier pointing at Bc into e of Bc's island (Fc, Pc, Bc, Oc, Rc), no Rc** | **27.9**, outcome fair with Bc | 1.3e-4 (Fc) – 3.2e-3 (Bc) |
| Rc pointing at Bc into v of Bc's island | 9.75 (fair (b, v)) | 7.3e-4 |
| Bc into a pair slot of fair carrier islands ((Fc, Fc), (Rc, Oc), (Fc, Bc)) | exactly 1 | 1.1e-4 |
| Bc into the excluded slot of (Fc, Fc) | median 16.9 (52% > 3; it draws an Fc whose preference points at it) | 1.6e-3 |
| ⅓ constants into the excluded slot of (Fc, Bc) | median 1 (3% at 5.9: the resident paid charges) | – |
| simulating bully, ⅔ demanders, ⅓ constants into pair slots of fair carrier islands | ≤ 10⁻¹¹ median | – |
| Oc / Rc into the excluded slot of fair simulating-reader islands (FI) | 5.9 (uncharged against charged residents) | – |
| Fc / Pc into a pair slot of FI | median 0.015 / 3·10⁻¹² (their fallback reads time out against the readers) | – |

## Step 1 (`runs/certified_offers/step1.md`; canonical spellings, conditional on finite trees)

| family | C1 (`carry` tag) shortest / mass | R1 written (`lib CARRY`) shortest / mass | C0 written (no library) shortest / log10 mass |
|---|---|---|---|
| fair single reader | 6 / 1.3e-11 | 6 / 1.6e-11 | 12 (R0) |
| bully | 6 / 4.0e-11 | 6 / 4.9e-11 | 12 |
| R (queue 78) | 6 / 4.0e-11 | 6 / 4.9e-11 | 12 |
| Oc | 3 / 2.9e-6 | 18 / 1.6e-30 | 740 / −1251 |
| Rc | 3 / 3.5e-6 | 18 / 1.8e-30 | 740 / −1251 |
| Fc | 8 / 3.8e-16 | 23 / 2.6e-40 | 751 / −1280 |
| Bc | 8 / 8.3e-16 | 23 / 5.6e-40 | 751 / −1280 |

Ratios: under C1, Oc and Rc weigh 2–3·10⁵ fair readers and 7–9·10⁴ bullies; Fc, Bc 10⁻⁵–10⁻⁴ of the fair reader (the fallback is
itself a reader); Bc / Fc = 2.2. Written out with `lib CARRY` every carrier is 10⁻²⁰–10⁻²⁹ of the reader. The C1 measure treats the
skeleton as one primitive tag, as R1 treats the read; how much mass carriers have is therefore a statement about that primitive.

## Step 2: dynamics (`runs/certified_offers/step2_report.md` has every table with bootstrap intervals)

Cells: 6,840 counted step-2 jobs (12 chunks of 545, the mixed arm at N = 400 in two chunks of 150) plus V1 (20). The I = 256 cells and
the φ ∈ {0, 1} extension to FcOc, FcRc, FcOcRcs and mix were cut (budget; notes §3). Stored controls: F (queue 75), F+R and F+O+R (queue
78), all φ = 0.

**V1:** 20 of 20 F and F+R cells reproduce the stored rows exactly (after normalizing queue 78's arms over their 59 programs, as queue 78
did; the first pass failed 2 of 20 by a 1.4·10⁻¹⁷ normalization difference, notes §2).

**V\* at β = 3 (120N; δ = 0.1 / 0.03 / 0.01 / 0.003 / 0.001):**

| arm (φ) | N = 100 | N = 200 | N = 400 |
|---|---|---|---|
| F (stored) | 0.00 / 0.00 / 0.05 / 0.20 / 0.40 | 0.05 / 0.00 / 0.15 / 0.20 / 0.15 | 0.05 / 0.05 / 0.15 / 0.10 / 0.25 |
| F+R (stored) | 0.10 / 0.10 / 0.20 / 0.25 / 0.55 | 0.15 / 0.15 / 0.10 / 0.15 / 0.45 | 0.05 / 0.20 / 0.10 / 0.15 / 0.10 |
| F+O+R (stored) | 0.10 / 0.35 / 0.10 / 0.10 / 0.40 | 0.00 / 0.10 / 0.35 / 0.05 / 0.30 | 0.20 / 0.20 / 0.10 / 0.20 / 0.33 |
| Fc (0) | – | 1.00 / 0.90 / 0.60 / 0.12 / 0.15 | – |
| Fc+Oc+Rc (0) | – | 1.00 / 0.95 / 0.65 / 0.21 / 0.15 | – |
| Fc (½) | 1.00 / 1.00 / 1.00 / 0.85 / 0.70 | 1.00 / 1.00 / 1.00 / 0.90 / 0.35 | 1.00 / 1.00 / 1.00 / 0.95 / 0.65 |
| Fc+Oc (½) | 1.00 / 1.00 / 1.00 / 0.65 / 0.70 | 1.00 / 1.00 / 1.00 / 0.86 / 0.74 | 1.00 / 1.00 / 1.00 / 0.95 / 0.82 |
| Fc+Oc+Rc (½) | 1.00 / 1.00 / 1.00 / 0.80 / 0.50 | 1.00 / 1.00 / 1.00 / 0.81 / 0.65 | 1.00 / 1.00 / 1.00 / 0.95 / 0.69 |
| Fc+Rc (½) | 1.00 / 1.00 / 1.00 / 0.80 / 0.45 | 1.00 / 1.00 / 1.00 / 0.95 / 0.65 | 1.00 / 1.00 / 1.00 / 1.00 / 0.70 |
| mix (½) | 1.00 / 1.00 / 1.00 / 0.65 / 0.60 | 1.00 / 1.00 / 1.00 / 0.75 / 0.50 | 1.00 / 1.00 / 1.00 / 0.95 / 0.64 |
| Fc (1) | – | 1.00 / 1.00 / 1.00 / 1.00 / 0.80 | – |
| Fc+Oc+Rc (1) | – | 1.00 / 1.00 / 1.00 / 1.00 / 0.85 | – |
| Fc+Oc+Rcs (½) | – | 1.00 / 1.00 / 1.00 / 0.80 / 0.66 | – |
| Fc+Oc+C⅓ (½) | – | 1.00 / 1.00 / 1.00 / 0.70 / 0.55 | – |
| Fc\* (½) | – | 1.00 / 1.00 / 1.00 / 0.90 / 0.40 | – |
| Pc+Oc+Rc (½) | – | 1.00 / 1.00 / 1.00 / 0.75 / 0.65 | – |

**δ\*** (V\* ≥ 0.9 at that grid δ and every larger one): every certified arm has one at every (β, N) run: (0.001, 0.01] at φ = ½ and 1,
(0.01, 0.03] at φ = 0; it does not rise with N (Fc+Oc+Rc, β = 3: (0.003, 0.01] at N = 100 and 200, (0.001, 0.003] at 400). F, F+R, F+O+R:
none at β ≥ 1 (F at β = 0: (0.003, 0.01] / (0.01, 0.03] / (0.03, 0.1] at N = 100 / 200 / 400).

**β = 0 (N = 200):** certification costs nothing: at δ = 0.03 every certified arm is 0.95–1.00 against F's 0.90; mean over δ of Fc − F =
+0.11.

**Controls.** *Rc's certificate ablated* (Fc+Oc+C⅓): equal to Fc+Oc+Rc at δ ≥ 0.01, lower by 0.10 at δ = 0.003 and 0.001 (overlapping
intervals); Rc adds little at the population level. *Fc\** (cycles broken by slot index): within 0.01 of Fc on the δ-mean at β = 0 and 3; the
2-in-8 cycles cost nothing visible. *Mixed arm*: inside the interval of its two pure arms in 17 of 20 cells (β ∈ {1, 3}, N ∈ {100, 200}),
outside by 0.1–0.2 in three, never below the lower by 0.15; at δ ≥ 0.01 it is the certified arm's value.

**Who holds what (120N, β = 3, N = 200, δ = 0.03).** Fc φ = 0: fair islands 3,392 Fc slots, 64 bully slots (the excluded slot); unequal
islands (10%) held by the simulating bully with a ⅓ constant. Fc+Oc+Rc φ = 0: Fc 2,137, Rc 1,129, Oc 231, constants 94, bullies 57. φ = ½:
Bc 3,120, Fc 526, Oc 71, Rc 61. φ = 1: Bc 3,489. Mean read and forfeit charges at 120N: 0 for every family in these cells (the certified
branch reads no one).

**Scramble diagnostic (RE 8).** Main arm, β = 3, φ = ½, all δ and N: 0.991 of islands have their 120N class at 30N. At δ = 0.03 there is
no unequal island at 30N in Fc or Fc+Oc+Rc (φ = ½).

**Seeded starts** (N = 200, I = 64, δ = 0.03, β = 3; fair share at 30N / 120N / 240N; exits = debounced unequal→fair flips):

| arm | all-unequal, simulating bully (φ ½) | all-unequal, Bc (φ ½) | all-unequal, Bc (φ 1) | all-fair, constants | all-fair, (Fc, Fc, C8) |
|---|---|---|---|---|---|
| F+R (stored / φ 0) | 0.06 / 0.05 / 0.05 | 0.10 / 0.16 / 0.11 | – | 0.90 / 0.90 / 0.90 | 1.00 / 1.00 / 1.00 |
| Fc | 0.05 / 0.05 / 0.05 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0.95 / 0.90 / 0.90 | 1.00 / 1.00 / 1.00 |
| Fc+Oc+Rc | 0.05 / 0.05 / 0.05 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 |
| Fc+Rc | 0.20 / 0.20 / 0.20 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0.90 / 0.90 / 0.90 | 1.00 / 1.00 / 1.00 |
| Fc+Oc+Rcs | 0.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0.95 / 0.95 / 0.95 | 1.00 / 1.00 / 1.00 |

From the simulating-bully start every arm is near queue 78's 0.05: nonzero shares are whole runs (Fc+Rc: 4 of 20), the exits are
mostly imported (bully, constant) pairs as in queue 78, the unequal→fair hazard is 1.9–2.5·10⁻⁵ per unequal island-generation, and the local
Rc route with a certified offerer completed 1 (Fc+Oc+Rc) and 2 (Fc+Rc) times, transient. From the Bc start every certified arm is fair by
30N (hazard 1.8·10⁻²): a Bc in e (by migration or tail) or any carrier pointing at it pairs with the bully. F+R reaches only 0.16 from it
(no carriers in its tail; Bc meets Bc by migration).

**Pacing against scramble** (seeded all-unequal, simulating bully; sums over 20 runs × 64 islands to 240N):

| arm | Rc in v (island-gens) | Rc arrivals into v: n / Σρ / took v | certified offerers into e while Rc holds v: n / Σρ = predicted | observed local Rc routes |
|---|---|---|---|---|
| Fc+Oc+Rc | 6,360 | 1,241 / 5.5 / 10 | 8 / 0.66 | 1 |
| Fc+Rc | 11,867 | 1,190 / 5.3 / 11 | 21 / 1.71 | 2 |
| Fc+Oc+Rcs | 557 | 1,250 / 1.6 / 3 | 2 / 0.00 | 0 |

Prediction and observation agree: the first step happens about as often as neutral fixation predicts (10 against 5.5), Rc then sits in
the victim's seat for a few hundred generations, and in that window almost no certified offerer arrives in e (the tail is front-loaded and
the carrier mass is δ). The null is pacing, not illegibility. On the main (unseeded) grid the observed local Rc routes (23 at β = 3,
N = 200) exceed the tail prediction (0.9): they complete inside the founding scramble among founders, which the arrival-based prediction
does not count.

## Verdicts (`runs/certified-offers.json`)

| prediction | result | verdict |
|---|---|---|
| RE 1 regress goes | 303,024 pointing triples (C1 and C0): all fair, 0 timed-out reads by the pair | holds |
| RE 2 legibility | Rc beside inactive e: median 1 (min 1) in every class; beside an active carrier 9.75; bully's read of Rc never times out; Rcs beside simulating readers 1.4e-10, beside carriers 9.75 | holds |
| RE 3 certified offers selected | Fc and matched Oc into e with Rc resident: 27.9 (min 27.9) | holds |
| RE 4 faker rides along | (a) Bc into pair slots of carrier islands exactly 1; (b) ⅓ constants into (Fc, Bc)'s third slot median 1; (c) carriers pointing at the bully into e: 27.9 on Bc's island against 1 on the simulating bully's | **falsified (third clause)** |
| RE 5 seeded unequal start | Fc+Oc+Rc 0.05 (= queue 78's F+R) | **falsified (no gain from legibility)** |
| RE 6 no threshold at β = 3 | δ\* ≤ 0.01 for every certified arm at every N (φ = ½) | **falsified** |
| RE 7 threshold at β = 1 possible | Fc+Oc+Rc 1.00 vs F+O+R 0.15 at δ = 0.1, N = 200 (+0.85) | holds |
| RE 8 scramble | 0.991 | holds |
| RE 9 β = 0 | every certified arm within or above F at δ = 0.03 (+0.05 to +0.10) | holds |
| RE 10 mixed worlds | inside the pure arms' interval (±0.05) in 17 of 20 cells; never below the lower by 0.15 | fails, falsifier not fired |
| RE 12 cycles | (Fc)³ mean 0.250 against 1/3 (2 of 8 cycle); Fc − F at β = 0, δ = 0.1: +0.00 | holds |
| RE 11 mass | C1: Oc, Rc 3 nodes against the fair reader's 6; C0-written ≥ 740 nodes | holds |
| E1 inactive entry exactly neutral | 372 edges, all exactly 1 | holds |
| E2 selected steps | 27.86 and 9.755 | holds |
| E3 Bc's island fragile | min 27.9, fixes into a fair pair with Bc | holds |
| E4 Bc neutral in carrier islands | Bc into pair slots exactly 1; ⅓ constants into (Fc, Bc)'s third slot median 1 but up to 5.9 beside charged residents | falsified (by charged residents, outside [0.5, 2]) |
| E5 Bc start opens | Bc start 1.00 in all three arms; simulating start 0.05 / 0.05 / 0.20 (Fc+Rc above 0.15) | fails, falsifier not fired |
| E6 φ | β = 3, N = 200, δ = 0.1: 1.00 at both φ (ceiling); the φ effect appears at δ ≤ 0.003 | **falsified** |
| E7 pacing explains the null | predicted 0.66 / 1.71, observed 1 / 2 | holds |
| E8 Fc at β = 0 | +0.11 | holds |
| E9 cycle-free comparator | Fc\* − Fc: 0.00 (β = 0), +0.01 (β = 3) | holds |
| E10 hybrid | Fc+Oc+Rcs 0.00 against Fc+Oc+Rc 0.05 | holds (at the bound) |
| E11 ablation | Fc+Oc+Rc − Fc+Oc+C⅓: 0 / 0 / 0 / +0.105 / +0.099 | fails, falsifier not fired |
| E12 mass | C1 Oc 3, Fc 8, reader 6; R1-written gap 12 | holds |

## The model can't express

- **A certified rule in any spelling but one.** Certification is syntactic: the body must be the skeleton around the shared combinator
  `CARRY`. An inlined copy of the same rule, or the skeleton under `if T`, is rejected. A checker that certifies arbitrary spellings
  (milestone 4's script checker extended to this statement) was not built. The population results therefore hold for a convention (one
  shared library entry), not for "any program that implements the rule".
- **A certified statement other than the conditional ½ offer.** A carrier can certify only "I name at ½ a partner whose certificate points
  at me". It cannot certify prudence (what it does against a ⅓-namer), so Pc's certified part is Fc's and the certified bully Bc is
  indistinguishable from Fc to a carrier. There is no certificate a carrier could require that excludes Bc.
- **A coordinated two-slot move**, as in queue 78. The exit from a simulating bully's island still needs Rc in v and a certified offerer
  in e, one at a time; certificates removed the illegibility, not the pacing.
- **A fallback that is legible when it reads.** Fc's, Bc's, Pc's and Rcs's fallbacks are simulating reads, and every mutual read through them
  is the regress (G4: 0 cap exhaustions, all timeouts persist at 20× caps). Only constant fallbacks (Oc, Rc) are legible inside a read.

## Budget

Daytona: 14 sandbox runs (12 grid chunks, 2 mixed-arm chunks), job walls summing to 131,346 s × 4 CPUs = **146 sandbox-CPU-hours**, plus
about 3 for setup. Local: tables, gates (≈ 0.1 CPU-h), step 0 (≈ 0.1), step 1 (≈ 0.1), V1 (≈ 0.5). Total ≈ 150 of the 200 ceiling.
`python3 tools/daytona_run.py list` is empty.
