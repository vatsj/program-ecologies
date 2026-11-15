# Queue 78: patient accepters in arm T (run report)

Spec `specs/2026-11-14-patient-accepters.md`; predictions `predictions/2026-11-14-patient-accepters.md` (committed before step 0 and
before any counted cell; addendum 1 discloses one non-counted timing pilot; addendum 2 discloses the exit-classifier change after half the
grid). Data: `runs/patient_accepter/` (gates, step 0, step 1, step-2 report), rows `runs/pa_rows/`, verdict inputs
`runs/patient-accepters.json` (`src/patient_accepter_verdicts.py`). Notes and operations: `notes/patient-accepters.md`. All step-2
numbers are finite-schedule approach-rate statistics (mN = 1, Λ = 100, 120N; seeded starts to 240N), not π.

## Programs and gates (`runs/patient_accepter/gates.md`)

K = 59: queue 76's 55 programs plus `Rnn`, `Rny`, `Rpn`, `Rpy` (R<d><to>: read partner d; if it names me at ½ name it at ½, else name
the other partner at ⅓; `Rnn` = `(if (eq readn 4) 1 3)` under R1).

- V2: the 55-block equals queue 76's on code, steps, timeouts, forfeits and joint codes, and the 31-block equals T+'s.
- Action gate: R follows its rule in 3,481 of 3,481 profiles per variant. The read is evaluated in R's own frame: 770 complete,
  2,652 time out (every reader partner). In the no-offer profiles the `n` variants play the ⅓ constant's action. Their charge equals
  the constant's where the read completes and adds P_fail where it times out. The reference built from partners' tables agrees in
  3,422 profiles per variant, with 0 disagreements and 59 ambiguous.
- **Mutual-read gate: can O or F trigger R? No.** In a bully-held unequal island with R (`n`, matched) as the victim, only the non-reading
  ½ constant naming R's slot (C4 for `Rn*`, C1 for `Rp*`) makes the fair pair (R, X): 3 of 3 triples for each, 0 of 24 for single
  readers, 0 of 24 two-partner readers, 0 of 24 openers, 0 of 12 F2, P_z, P_o, Q. R's read of any reader in the excluded slot times out.
  The `y` variants pair with `y`-type readers, bullies and their twins through timeouts.
- **Unexpected: R makes the victim illegible to the bully.** With R as the victim and any reader X in the excluded slot, the bully's read
  of R times out, because R's read of X re-enters a reader. The bully then names X at ½. For `Rnn` the island becomes the fair pair
  (bully, X) in 3/6 (bully X), 9/24 (single readers), 9/24 (two-partner readers), 9/24 (openers) and 6/12 (P_o) of triples, and D otherwise.
  It is never unequal and never (R, X).
- Nested reads (R ∪ O ∪ F ∪ B)³: every profile has a timeout, mean A_f charge 0.30–0.60 per profile, no forfeits.

## Step 0: exact invasion assays (`runs/patient_accepter/step0.md`, `step0_routes.json`)

ρ·N at N = 200, w = 0.3, A_f charges included; 1 = neutral. The 354 bully-held unequal triples cover both bullies, every third-slot
program and all three role rotations. Checks: the jump chain on 60 assays has max |z| 2.70; the real kernel on 16 assays (3,000 islands
each) has max |z| 1.97. The prior-weighted rate is per arrival into that slot under the reference law F+R (δ = 0.03, β = 3, γ = 1).

| edge (n variants, matched orientation unless stated) | assays | ρ·N | rate per arrival |
|---|---|---|---|
| item 1: R into v, read completes, third slot not offering | 60 | median 1 (54 exactly 1; 6 at 0.015 with junk `Jr`, whose internal failed read R pays for) | 7.5e-5 |
| item 1: R into v, third slot offers ½ (the "offerer-first" second step) | 6 | 9.75 | 7.3e-4 |
| item 1: R into v, read times out (any reader in the excluded slot) | 288 | 1.4e-10 (R pays P_fail and the bully drops it) | ~1e-14 |
| item 1: mismatched orientation | 354 | ≤ 0.015 | ≤ 7e-7 |
| item 2: ½ constant naming R into e, R resident (Bn, Rnn, C8) | 3 rotations × 2 bullies | 27.9 (outcome F) | 0.013 |
| item 2: single / two / F2 / O / P_o into e, R resident | 2,160 (with P_z) | 33% above 3: they become the bully's fair partner (outcome F with the bully). The rest are D or neutral (P_z never above 1) | ≤ 1e-4 |
| item 3: R into v with the ½ constant resident in e | 6 | 9.75 | 7.3e-4 |
| item 3: R into v with a reader resident in e | 168 | 1.4e-10 | ~1e-14 |
| RE 2 first steps on (Bn, C3, C8) and rotations: R into v; ½ constant into e | 6 + 6 | 1.0 and 1.0 | 7.5e-5 and 4.7e-4 |
| item 4: bully / C2 / C5 / C8 / C3 / C0 into the fair island (C8, Rnn, C4) | 20 | excluded slot exactly 1 (R keeps its offerer, no re-yield); pair slots ≤ 1 | - |
| item 4a: bullies into all R-paired fair islands (1,461 residents incl. readers) | 8,424 | median 1; 16% above 3 (max 22.6), where the resident paid read charges or the bully's read timed out | - |
| item 4b: R into fair firm-reader islands (FI) | pair slot 6,912 / out slot 3,456 | pair ≤ 0.075 (R's read of a reader partner times out, it names the other at ⅓); out slot median 1, 25% at 5.9 (cheaper than charged residents) | - |

Per arrival, the R-first route is 7.5e-5 × 0.013 and the offerer-first route is 4.7e-4 × 7.3e-4. Both are products of a neutral
fixation (1/N) and a rare second arrival.

## Step 1: length-prior mass (`runs/patient_accepter/step1.md`; conditional on finite trees; exact-member lower bounds)

| machine | R (`n` variants) | R (`y`) | fair single | bully | R_n / single | R_n / bully | shortest R_n / R_y / single / bully | MC 95% upper on R_n |
|---|---|---|---|---|---|---|---|---|
| R0 | 1.26e-23 | 1.1e-35 | 4.08e-24 | 1.26e-23 | 3.09 | 1.00 | 12 / 20 / 12 / 12 | 6.7e-7 (5.7·10⁶ finite draws, 0 hits) |
| R1 | 9.73e-11 | 3.8e-23 | 3.15e-11 | 9.73e-11 | 3.09 | 1.00 | 6 / 14 / 6 / 6 | 1.9e-6 (2.0·10⁶ finite draws, 0 hits; two of four shards OOM-killed) |

R_n's lower bound equals the bully's to 12 digits: same shape `(if (eq readn k) a b)`, literals of equal prior mass. R_n / (C3 + C0) is
1.9e-22 (R0) and 2.3e-9 (R1). The `to = y` variants are 12 nodes longer in R0 and 8 longer in R1, because a disjunction costs more nodes.
V3: R's canonical bodies classify as themselves under R0 and R1 (family `other_cond`, exact member R). The mass accounting is queue 75's:
R adds a member label, not a mass class.

## Step 2: dynamics (`runs/patient_accepter/step2_report.md` has every table with bootstrap intervals)

4,700 + 200 (seed2) + 920 (lps) + 40 (V1) cells. V1: 40 of 40 F cells reproduce queue 75's stored rows exactly.

**No reader-share threshold anywhere under bullies.** No arm, β ∈ {1, 3}, N ∈ {100, 200, 400}, I = 64 (and I = 256 for F+R), or γ has a
grid δ with V\* ≥ 0.9. V\* at β = 3, N = 200, I = 64, γ = 1 (δ = 0.1 / 0.03 / 0.01 / 0.003 / 0.001):

| arm | V\* |
|---|---|
| F | 0.05 / 0.00 / 0.15 / 0.20 / 0.15 |
| F+R | 0.15 / 0.15 / 0.10 / 0.15 / 0.45 |
| F+O+R | 0.00 / 0.10 / 0.35 / 0.05 / 0.30 |
| F+C⅓ | 0.05 / 0.00 / 0.10 / 0.15 / 0.20 |
| R only | 0.05 / 0.10 / 0.15 / 0.25 / 0.30 |
| F/R split | 0.15 / 0.05 / 0.00 / 0.10 / 0.31 |

V\* is bimodal by run: runs end mostly all-fair or all-unequal. Intervals are ±0.15–0.25, and no arm is separated from F at β = 3.

**γ:** at N = 200, γ = 3 is above γ = 0.3 in most F+R and F+O+R cells (up to +0.50, F+O+R β = 1 δ = 0.01). It is flat for F+C⅓.
At β = 1, γ = 3 F+R reaches 0.30–0.45 and F+O+R 0.30–0.50, against F's 0.05–0.42. More R raises V\* modestly; more ⅓ constants
do not. Still no threshold.

**β = 0 (N = 200):** F+R 1.00 / 1.00 / 0.80 / 0.80 / 0.75 against F 1.00 / 0.90 / 0.65 / 0.75 / 0.50. R costs nothing without bullies; it is higher at every δ.
Both have δ\* in (0.01, 0.03].

**Who holds what (120N majority holders, pooled over δ):** R is 10–22% of fair-island slots in every R arm (F+R β = 3: 15%, γ = 3: 20%;
R only 16%; length-prior series 16–19%), and 0.3–4% of unequal-island slots. R is the victim on 54 of 205,975 unequal islands
(0.03%). R and a ⅓ constant are co-present in the same slot on only 17 island-slots in the whole grid, with mean payoff difference −0.007.
R ends on fair islands paired with a ½ constant, with the bully excluded (the configuration step 0 shows is robust). It almost never
sits in the victim's seat of a surviving unequal island.

**Seeded starts (N = 200, I = 64, δ = 0.03, β = 3; founders identical across arms):**

| arm | unequal start: fair 30N / 120N / 240N | U→F flips to 240N (lasting to 120N) | fair start: fair 30N / 120N / 240N |
|---|---|---|---|
| F | 0.000 / 0.000 / 0.000 | 1,048 (0) | 0.90 / 0.90 / 0.90 |
| F+R | 0.056 / 0.050 / 0.050 | 1,488 (48) | 0.90 / 0.90 / 0.90 |
| F+O+R | 0.000 / 0.000 / 0.000 | 1,083 (0) | 0.85 / 0.85 / 0.85 |
| F+C⅓ | 0.000 / 0.050 / 0.050 | 1,389 (59) | 0.90 / 0.90 / 0.90 |
| R only | 0.048 / 0.050 / 0.050 | 1,411 (50) | 0.90 / 0.90 / 0.90 |

The debounced unequal-to-fair hazard is 1.7–2.6·10⁻⁵ per unequal island-generation over 240N. It is almost all transient flips.

**Exit classification (v2; roles from each island's seeded triple):** every nonzero fair share from the unequal start is one run (of 20)
sweeping to the triple (C1, Bn, Bn). That is a fair pair of a ½ constant and a bully reached by migration, labelled imported (F+R 48 lasting exits,
F+C⅓ 59, R only 50, all `bully+const|imported`), and F+C⅓ does it as often as F+R. The R route (R in v with a ½ constant in e) occurs once in
6,419 seeded-unequal exits (F+O+R, local, transient). One more R pair (R in the bully's seat with a ½ constant, R only, imported) was
also transient. Exits pairing a firm reader or opener (all starts): 14, all transient. In the fair start, lasting R pairs (R with C1/C4) appear in F+R, F+O+R and R only by import, and the arms
hold like F. The run log has every resident triple before and after each majority change; `lasting_exits` in `runs/patient-accepters.json`.

**Length-prior-shaped series** (R at its measured mass, 3.09 per fair reader, both allocations, R0 and R1, N = 200 and 400): the largest
cell is 0.50 (R0 constants N = 200 δ = 3·10⁻⁴; R1 junk N = 200 δ = 3·10⁻⁴), against 0.35 in queue 76's series. No cell is near 0.9.

## Verdicts

| prediction | result | verdict |
|---|---|---|
| RE 1 neutral entry | completed-read median 1.0 (60 assays); timed-out 1.4e-10 | holds |
| RE 2 selected step | ½ constant into e with R 27.9; R into v with ½ constant 9.75; first steps 1.0 and 1.0 | holds |
| RE 3 unequal islands leave | F+R 0.05 (one run, a bully pair), F+O+R 0.00, F 0.00, F+C⅓ 0.05 | **falsified** (F+R < 0.1) |
| RE 4 a threshold returns | F+R β = 3 N = 200: none (max 0.45 at δ = 0.001) | **falsified** |
| RE 5 cost without bullies | F+R − F at δ = 0.03: +0.10 (1.00 vs 0.90) | holds |
| RE 6 mass | R1: 6 nodes = fair reader; R_n / bully = 1.00 | holds |
| RE 7 length prior | max 0.50 | holds |
| RE 8 fair islands | F+R 0.90 vs F 0.90 | holds |
| carbon (a) | F+R seeded 0.05 < 0.3, V\* < 0.5 at every δ, no threshold | true |
| carbon (b) | seeded F+O+R − F+R = −0.05, but V\* F+O+R − F+R = +0.25 at δ = 0.01 (one cell, overlapping intervals) | false as scored |
| carbon (c) | every R pair's partner is a ½ constant (42 exits). But 14 transient exits pair a firm reader or opener (with the bully) | false (the ½-constant clause holds) |
| sol | 18 local exits involve F or O at some step; 4,822 imported exits (203 lasting) | true |
| E1 | completed non-offering exactly 1 except `Jr` (0.015); mismatched max 0.015 (> 0.01) | falsified (by the junk read-failer and the 0.01 bound) |
| E2 | readers into e with R: 33% above 3; ½ constant 27.9. The rest reach 1, not < 0.1 | fails, falsifier not fired |
| E3 | 9.75 | holds |
| E4 | bully into the clean (R, C4) island ≤ 1. But over all R-paired fair islands 16% above 3 (max 22.6); R into FI out slot up to 5.9, pair ≤ 0.075 | falsified |
| E5 | F+R 0.05, F+O+R 0.00, R 0.05, F 0.00, F+C⅓ 0.05 | holds as scored (mechanism not R's route) |
| E6 | R-pair local exits 1 of ~1,500 local | falsified |
| E7 | no threshold anywhere; F+R − F at β = 3, N = 200 up to +0.30 (δ = 0.001) | fails (> 0.15), falsifier not fired |
| E8 | \|γ3 − γ0.3\| up to 0.50 (R arms, γ = 3 higher) | falsified |
| E9 | F+R ≥ F at every δ (+0.00 to +0.25) | holds |
| E10 | 6 nodes, ratio 1.00, R0 gap 0 | holds |
| E11 | no cell ≥ 0.9; max 0.50 > 0.45 | fails, falsifier not fired |
| E12 | no co-presence in the registered cell; grid-wide −0.007 over 17 island-slots | unscorable as registered |
| E13 | 0 of 1,088 unequal islands have R as victim | holds |
| E14 | all arms 0.85–0.90; F+R = F | holds |
| E15 | carbon (b) came out false | fails, falsifier not fired |

## The model can't express

- **An offer a reader can make to R.** R can only be triggered by a program whose behaviour it can read within the cap. Every reader in
  the excluded slot (F, O, P, other R) times out under mutual reading, so only non-reading ½ constants can answer R's patience. A
  reader-to-reader offer needs a non-regressive semantics for mutual reading, such as certificates or a fixed point.
- **R staying legible to the bully.** Because R reads, a reader next to it makes R's own behaviour unreadable to the bully. The victim then
  loses its ⅓ deal (the bully pairs with the reader or the island goes to D). There is no "read only constants" or "answer the bully
  first" primitive that keeps R a constant to its current partner.
- **A two-slot move.** The route needs R in v and a ½ constant in e. The single-slot invasion dynamics can only take them one at a time,
  each step waiting on a rare tail arrival, and the tail is front-loaded.
