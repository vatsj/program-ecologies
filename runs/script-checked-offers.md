# Queue 80: script-checked offers in majority division (run report)

Spec `specs/2026-11-16-script-checked-offers.md` (gemini-4-carbon, then gpt-6.1-sol `--mode amended`, both folded; the amendments
override). Predictions `predictions/2026-11-16-script-checked-offers.md`: RE 1 committed before any code (8d6bfb3); RE 2–12, the
registered scoring rules and the E-series committed after the gates and before any assay, mass, V1/V2 or counted cell (2030c95).
Notes (soundness argument, reuse, deviations, operations): `notes/script-checked-offers.md`. Data: `runs/script_offers/` (gates,
exactness, step 0, step 1, V1, V2, step-2 aggregates and tables), rows `runs/sco_rows/`, verdicts `runs/script-checked-offers.json`
(`src/script_offers_verdicts.py`, `src/script_offers_report.py`). **All step-2 numbers are finite-schedule approach-rate statistics
(I = 64, mN = 1, Λ = 100, 120N; the seeded start to 240N), not π. N = 100–400 is exploratory, not a large-N result.**

## Headline

1. **The checker was built, and it is sound.** CHKS is a shared library entry written in L_T^code that verifies a carried script as a
   derivation (a case tree over the open atoms, each leaf checked by symbolic evaluation of the carrier's body with the partners'
   quotes opaque) that the program satisfies a statement, for any spelling of the program. Soundness is a structural theorem (notes
   §1.4). Gates: 0 false acceptances in 7,862,391 (accepted statement × profile) checks in each of S0 (the checker executed step by
   step) and S1 (a primitive with S0's exact map and tick counts); all 100 carriers in five spellings accepted for exactly their
   statements; every forger accepted only for statements that are true of it. The worst accepted check costs **κ_S = 15,141 ticks**,
   so fuel was raised from (KR, cap) = (1,200, 400) to **(384,000, 128,000)**. RE 1 holds.
2. **The threshold survives the real checker, unchanged.** At β = 3, N = 200 the canonical script carriers (A1) have δ\* = 0.03
   (φ = 0) and 0.01 (φ = ½); the uncertified controls at the same fuel (U) have none (V\* ≤ 0.2 at every δ). A1 equals queue 79's
   skeleton machine (K) cell for cell: the two machines' tables are identical in actions, failed reads and forfeits on every triple
   the laws use (only tick counts differ). Fuel alone changes nothing (U's tables equal the old-fuel tables on its support).
3. **Spellings pair, and that is why the convention mattered.** Every pair of carriers whose certificates make them mutually eligible
   forms the fair pair across all five spellings, with no read (static, every seat pattern). In the dynamics the five spellings of a
   family are behaviourally identical, so A2 (mass split over spellings) is A1's law in disguise; it reaches δ\* = 0.03 / 0.01, with
   δ-means 0.68 / 0.90 against A1's 0.54 / 0.88 (sampling). Under the skeleton check (K2) the same split leaves four of five spellings
   invisible and the arm falls to δ-mean 0.40 at φ = 0 (δ\* only at 0.1).
4. **Certified prudence excludes the certified bully from its own partnerships and hands it the fair islands.** Pc⁺ (requires S_nx)
   refuses Bc, and Bc cannot hold S_nx; but Pc⁺ thereby loses most of its partners: it holds 1.7% of paired fair-island slots in A4
   (φ = ½, β = 3), while Bc's share rises from 0.67 (A2) to 0.79, and V\* does not fall (0.95 against 0.85 at δ = 0.003). When every
   carrier requires S_nx (A5) Bc holds 94% of paired slots, every one of them paired with another Bc, and V\* is unchanged (δ-mean
   0.88). Statically, Pc⁺ entering the excluded slot of Bc's unequal island is neutral (ρ·N = 1.0, against 27.9 for Fc⁺), so prudence
   does close the bully's own island again, but those islands are rare (Bc holds ⅔ on ≤ 5% of islands in any cell).
5. **The convention is expensive under a length prior.** With scripts counted as data, the cheapest script carriers are 10⁻⁶⁴ (Oc)
   to 10⁻³⁶⁹ (Pc⁺) of the 6-node fair reader; even with scripts free they are 10⁻²⁹·⁵ or rarer (the rule plus packaging is ≥ 20
   nodes). Scripts are 41–85% of a carrier's nodes.

## The checker and the programs

A **carrier** is any program with a script, packaged as `λme.λn.λp.(if T B SCRIPT)` (the root evaluation never reads SCRIPT; B is any
L_T^code term). **CHKS** = `(if (eq (capk 16000 CCORE (x . c)) T) T F)` (at most 16,005 ticks in any context). **CCORE** (L_T^code)
reads x's script entry for the asked statement and walks its case tree (LEAF / SPLIT / VAC), resuming a continuation-passing symbolic
evaluation of x's body with the partners' quotes opaque; the open atoms are CHKS's own results on the partners (and, inside a partner
read, equality tests on the read's unknown result); every operation it does not model rejects (inspecting a partner's quote,
self-checks, identity tests, recursion, concrete `run`/`capk`). A leaf is accepted iff the statement's premise is false on the path
(Kleene logic) or the counted ticks fit KR' and the value is in the statement's mask. CCORE reads no one and runs no one.

Statements (codes asked of the checked program): **S_off(d; R)**, R ⊆ h (codes 1–4) and **S_nx** (code 5: never a ⅔ demand, the
timeout action 8 included). Eligibility, one predicate in code, statement and proof: s ∈ E_x iff x offers toward s and
CHKS(s, OFF(toward x; h = H_x)) = T and (R_x = {S_nx} → CHKS(s, S_nx) = T). S1 replaces CCORE by a primitive with S0's value and S0's
exact tick count per (quote, code), interrupted exactly as S0 when the remaining fuel is below the count.

Reused from milestone 4: the architecture (a carried script, a shared checker entry, case splits on check atoms between evaluation
segments, the checker as a bounded `capk`). Not reused: milestone 4's `cstep` self-interpreter (it cannot keep a partner opaque and
costs about 20 ticks per object step) and K_3's three-quote wrappers (they certify play against given partners).

Programs. World S (K = 159): queue 78's 59 at cap' and ten families × two directions or fallbacks × five spellings (`canon` the shared
rule OFFER; `inl` inlined, eligibility through `lib ELIG`; `rord` inlined, reordered; `guard` the canonical call under `if T`; `noelig`
inlined with direct CHKS calls): Oc, Rc, Fc (fallbacks Snoy, Spoy in every arm), Bc (fallback the simulating bully), Oc⁺, Rc⁺, Fc⁺
(also hold S_nx), Pc⁺ (requires S_nx), OcR⁺, RcR⁺ (require S_nx; A5). S_nx is derivable for T's four fallback-o single readers, not
for fallback z (they play 8) nor for the two-partner readers (two worst-case reads exceed KR'). World K (K = 99): the 59, queue 79's
8 canonical skeleton carriers with the same fallbacks, and four spellings of each that queue 79's CHK rejects. Scripts are 23–209 data
nodes, produced by a host tactic and checked by S0.

Engineering change to the evaluator (notes §2): at cap' a mutual read is a tower of closure `capk` frames that lt_code does not key
(about 90 ms per profile). A regress key for closure frames lets milestone 3's regress lemma fast-forward them; it is exact on actions
and steps on all 205,379 old-fuel profiles and changes failed-read counts only in 928 profiles that contain the zero-mass junk program
Jr. V1 and V2 below were run with it.

## Gates (`runs/script_offers/gates.{json,md}`)

- **G1 soundness.** S0, S1 and an independent Python reference agree on all 910 (program, code) checks. Cube (every accepted statement
  of 159 programs and 23 forgers against every (next, prev) of the catalogue): **0 false acceptances** in 7,862,391 checks per machine.
  Forgers: queue 79's eight are rejected (no packaging); the fifteen script forgers (a valid script on another program; Fc⁺'s script
  on Bc's body; a lookalike rule; swapped partners; S_nx on a program whose read can exhaust the root fuel; an atom-asserting tree node;
  VAC where the guard can hold; a program naming prev when next is the preferred eligible partner; malformed and computed scripts;
  self-certification; an identity test; recursion; inspection of the partner's quote) are accepted only for statements true of them
  (e.g. Fc⁺'s offers on Bc's body yes, its S_nx no; the ½ constant naming next with a one-leaf tree yes).
- **G2 completeness.** All 100 carriers accepted for exactly their statements; S0 check costs 1,668–15,141 ticks (Oc/Rc 1.7–3.9k,
  Fc/Bc 3.1–7.2k, Fc⁺ 4.0–7.6k, Pc⁺ 10.6–15.1k; canonical and guard spellings dearest). Every certified-eligible pair is the fair pair
  in every seat pattern beside every non-carrier, 0 timed-out reads, in S0 and S1; (Pc⁺, Pc⁺), (Pc⁺, Oc⁺), (Pc⁺, Rc⁺), (Pc⁺, Fc⁺)
  pair; (Pc⁺, Bc), (Pc⁺, Oc), (Pc⁺, Rc) are never eligible. **Ineligible pairs still pair through their fallbacks**: Pc⁺–Bc in 10,050
  of 35,400 triples, Pc⁺–Fc 13,200, Pc⁺–Oc 12,000, OcR⁺–Bc 8,400 (Pc⁺'s firm-reader fallback accepts anyone naming it at ½; the bully's
  fallback names its prev at ½ unless its next names it at ⅓). Three-carrier triples are tabulated by family (gates.json), S0 = S1.
- **G3.** Queue 79's CHK accepts the 8 canonical K-world carriers and rejects the 32 other K-world spellings and all 100 world-S carriers.
- **G4.** Among queue 78's 59 programs, 0 of 205,379 outcome triples change between the old and the new fuel, and all 135,168
  reader–reader timeouts persist (the regress is a regress at any cap). A simulating reader times out reading a carrier in 29% of
  profiles.
- **V3.** S1 = S0 on all 4,601,142 profiles in action, steps, failed reads and forfeits, and in 3,640 interruption tests (each check at
  residual fuel one below and at its cost, at root and inside a frame).
- **V1.** Arm U at the old fuel reproduces queue 75's F and queue 78's F+R rows in 20 of 20 cells (also after restricting each cell's
  local catalogue to its law's support). **V2.** Queue 79's machine and historical catalogue (16 fallbacks) reproduce its Fc+Oc+Rc
  rows in 20 of 20 cells.

## Step 0 (`runs/script_offers/step0.json`; ρ·N at N = 200, w = 0.3, A_f; 1 = neutral; 521,790 edges; jump chain max |z| 2.60 on 60)

| edge | median ρ·N (min–max) | fixes into |
|---|---|---|
| a carrier of one spelling into a pair slot of a fair island of another spelling's pointing carrier (Fc–Fc, Oc–Rc, Fc–Oc, Fc⁺–Fc⁺, Pc⁺–Pc⁺, Pc⁺–Oc⁺; 12,960 edges, 10,440 cross-spelling) | exactly 1 (1–1), same = cross | the fair pair |
| Rc (any spelling) into v of a simulating-bully island with a carrier (any spelling) pointing at v in e | 9.75 (9.75–9.75), same = cross | fair (v, e) |
| Fc / Oc (any spelling) into e with Rc (any spelling) in v | 27.9 (27.9–32.9), same = cross | fair (v, e) |
| Bc into a pair slot / the excluded slot of (Fc⁺, Fc⁺) | 1 exactly / 16.9 (1–32.9; > 3 in 52%) | fair (with Bc) |
| Bc into a pair slot / the excluded slot of (Pc⁺, Pc⁺) | 0.0 (0–9.75) / 1.0 (1–5.9) | fair 54%, disagreement 42% / fair |
| **Pc⁺ into e of Bc's unequal island** (Bc on ⅔ with a ⅓ constant) | **1.0** (1–5.9) | stays unequal |
| OcR⁺ into e of Bc's island | 1.0 (1–5.9) | stays unequal |
| Fc⁺, Fc, Oc⁺, Rc⁺, Oc (pointing at Bc) into e of Bc's island | 27.9 (27.9–32.9) | fair with Bc |
| simulating bully into pair slots of carrier islands, ⅔-demanding constants as thirds (registered) | 0.5 for (Fc, Fc), (Fc⁺, Fc⁺), (Pc⁺, Pc⁺); 0.0 otherwise (max 1) | fair through the fallbacks, or disagreement |
| the same, every non-carrier as third (post hoc; queue 79's form) | 0.0 (ρ·N < ⅓ in 80–93%; max 9.75) | — |
| ⅓ constants into the third slot of (Pc⁺, Pc⁺), (Fc⁺, Bc), (Fc, Bc) | 1 exactly | fair |

## Step 1 (`runs/script_offers/step1.{json,md}`; log10 mass, conditional on finite trees; witnesses, not minima)

M1: R1's tags plus a primitive `chks` tag, scripts counted as data nodes; "script free": the script replaced by one node; M2: R1 with
CHKS a library leaf; "fully written": the body plus every library entry it reaches, counted once (the checker's helpers recurse through
`lib`, so they cannot be inlined as a tree). The 6-node fair single reader Snon: log10 M1 −11.67.

| family | best spelling | M1 nodes | M1 / reader | script free / reader | M2 / reader | fully written nodes (≥) |
|---|---|---|---|---|---|---|
| Oc | Ocn.canon | 47 | 10⁻⁶⁴·³ | 10⁻²⁹·⁵ | 10⁻⁶³·⁵ | 1,811 |
| Rc | Rcn.canon | 47 | 10⁻⁶⁴·⁹ | 10⁻²⁹·⁵ | 10⁻⁶⁴·¹ | 1,811 |
| Fc | FcSnoy.canon | 94 | 10⁻¹⁴²·⁶ | 10⁻⁵²·³ | 10⁻¹⁴⁰·⁷ | 1,871 |
| Bc | Bcn.canon | 86 | 10⁻¹³⁰·⁰ | 10⁻³⁹·¹ | 10⁻¹²⁸·³ | 1,863 |
| Oc⁺ / Rc⁺ | canon | 61 | 10⁻⁸⁸ | 10⁻³⁰·¹ | 10⁻⁸⁷ | 1,825 |
| Fc⁺ | Fc+Snoy.canon | 132 | 10⁻²⁰⁴·⁶ | 10⁻⁵²·⁹ | 10⁻²⁰¹·⁹ | 1,909 |
| Pc⁺ | Pc+Snoy.canon | 234 | 10⁻³⁶⁹·³ | 10⁻⁵³·⁵ | 10⁻³⁶⁴·⁴ | 2,019 |
| OcR⁺ / RcR⁺ | canon | 73 | 10⁻¹⁰⁹ | 10⁻³⁰·⁷ | 10⁻¹⁰⁷ | 1,841 |

Scripts are 41–85% of a carrier's M1 nodes. Queue 79's skeleton Oc was 3 nodes and 10⁵ fair readers under its `carry` primitive, 18
nodes written with `lib CARRY`. No exhaustive search was run: these are witness ratios, with no minimality or family-scarcity claim.

## Step 2 (`runs/script_offers/step2_tables.md`, `step2.json`, `step2_details.json`; 4,620 cells × 20 runs; 95% bootstrap intervals)

V\* at 120N, N = 200 (δ = 0.1 / 0.03 / 0.01 / 0.003 / 0.001; δ\*; δ-mean):

| arm (φ) | β = 0 | β = 1 | β = 3 |
|---|---|---|---|
| U: F (0) | 1.00 / 0.90 / 0.65 / 0.70 / 0.50; 0.03; 0.75 | 0.15 / 0.05 / 0.05 / 0.10 / 0.42; –; 0.15 | 0.05 / 0.00 / 0.15 / 0.05 / 0.15; –; 0.08 |
| U: F+R (0) | 1.00 / 1.00 / 0.80 / 0.80 / 0.75; 0.03; 0.87 | 0.15 / 0.05 / 0.10 / 0.30 / 0.50; –; 0.22 | 0.15 / 0.15 / 0.10 / 0.15 / 0.45; –; 0.20 |
| K (0) | – | 1.00 / 1.00 / 0.75 / 0.45 / 0.35; 0.03; 0.71 | 1.00 / 0.95 / 0.45 / 0.10 / 0.20; 0.03; 0.54 |
| K (½) | 1.00 / 1.00 / 1.00 / 0.75 / 0.45; 0.01; 0.84 | 1.00 / 1.00 / 0.95 / 0.70 / 0.50; 0.01; 0.83 | 1.00 / 1.00 / 1.00 / 0.80 / 0.60; 0.01; 0.88 |
| K2 (0) | – | 0.95 / 0.55 / 0.25 / 0.20 / 0.50; 0.1; 0.49 | 0.90 / 0.45 / 0.25 / 0.00 / 0.40; 0.1; 0.40 |
| K2 (½) | 1.00 / 1.00 / 0.75 / 0.75 / 0.65; 0.03; 0.83 | 1.00 / 0.95 / 0.50 / 0.30 / 0.40; 0.03; 0.63 | 1.00 / 1.00 / 0.80 / 0.30 / 0.20; 0.03; 0.66 |
| A1 (0) | – | = K (0) | = K (0) |
| A1 (½) | = K (½) | = K (½) | = K (½) |
| A2 (0) | – | 1.00 / 1.00 / 0.55 / 0.35 / 0.50; 0.03; 0.68 | 1.00 / 0.95 / 0.85 / 0.20 / 0.40; 0.03; 0.68 |
| A2 (½) | 1.00 / 1.00 / 1.00 / 0.80 / 0.50; 0.01; 0.86 | 1.00 / 1.00 / 0.90 / 0.60 / 0.60; 0.01; 0.82 | 1.00 / 1.00 / 1.00 / 0.85 / 0.65; 0.01; 0.90 |
| A3 (½) | = A2 (½) at β 0 | 1.00 / 1.00 / 0.95 / 0.70 / 0.40; 0.01; 0.81 | 1.00 / 1.00 / 1.00 / 0.85 / 0.60; 0.01; 0.89 |
| A3 (1) | – | 1.00 / 1.00 / 1.00 / 1.00 / 0.65; 0.003; 0.93 | 1.00 / 1.00 / 1.00 / 1.00 / 0.85; 0.003; 0.97 |
| A4 (0) | – | – | 1.00 / 0.95 / 0.85 / 0.20 / 0.40; 0.03; 0.68 (= A2 (0)) |
| A4 (½) | = A2 (½) at β 0 | 1.00 / 1.00 / 0.85 / 0.55 / 0.45; 0.03; 0.77 | 1.00 / 1.00 / 1.00 / 0.95 / 0.45; 0.003; 0.88 |
| A4 (1) | – | 1.00 / 1.00 / 1.00 / 0.81 / 0.60; 0.01; 0.88 | 1.00 / 1.00 / 1.00 / 1.00 / 0.85; 0.003; 0.97 |
| A5 (½) | – | – | 1.00 / 1.00 / 1.00 / 0.90 / 0.50; 0.003; 0.88 |

Stored old-fuel rows (β = 3): F 0.05 / 0.00 / 0.15 / 0.20 / 0.15 (δ-mean 0.11), F+R 0.15 / 0.15 / 0.10 / 0.15 / 0.45 (0.20). Bootstrap
intervals for every cell: `step2_tables.md` (typical half-width 0.1–0.2 at intermediate V\*).

N-scaling (β = 3; exploratory): A2 at N = 100 / 200 / 400: φ = 0 δ\* 0.03 / 0.03 / 0.01, δ-mean 0.60 / 0.68 / 0.69; φ = ½ δ\* 0.01 / 0.01 /
0.003, δ-mean 0.83 / 0.90 / 0.94. A1: φ = 0 δ\* 0.03 at all three; φ = ½ 0.01 / 0.01 / 0.003.

**Equivalences (static, exact).** A1 and K have identical action, failed-read and forfeit tables on the 67 programs their laws use
(`a1_vs_k.json`; 300,763 triples), so they are one model and their rows are identical under common random numbers. Every spelling is
table-equivalent to its canonical spelling on A2's support (32 of 32), and every ⁺ program to its plain version on A3's support (30 of
30) (`equiv.json`): A2 and A3 are A1's law with programs split into identical copies, and their differences from A1 are sampling. A4 at
φ = 0 equals A2 at φ = 0 (no Bc; Pc⁺'s requirement never binds against non-carriers).

**Who holds the fair islands** (β = 3, φ = ½, N = 200, pooled over δ; share of paired fair-island slots): A2: Bc 0.67, Fc 0.19, Rc 0.04,
½ constants 0.07; A3: Bc 0.69, Fc⁺ 0.21; **A4: Bc 0.79, Rc⁺ 0.09, Oc⁺ 0.05, Pc⁺ 0.017**; A4 (φ = 1): Bc 0.91, Pc⁺ 0.015; **A5: Bc 0.94,
every Bc partner a Bc**; K: Bc 0.70–0.77. Spellings in A2's carrier-held paired slots: canon 0.21, guard 0.22, inl 0.21, noelig 0.17,
rord 0.20. Bc on ⅔: at most 0.05 of islands in any of these cells; the simulating bully on ⅔: 0.75 of islands in A2 at φ = 0,
δ = 0.003. Bc's share of the excluded slot of fair islands: 0.64 (A2, δ = 0.03), 0.92 (A4), 1.00 (A5). Mean read and forfeit charges
per slot at 120N: 10⁻⁶ averaged over all runs, at most 0.004 in any run (the certified branch reads no one; fair islands are carrier-
or constant-held).

**Scramble.** 0.974–0.990 of islands keep their 30N class to 120N in every arm (cell means). Islands are decided in the founding
scramble, as in queue 79.

**Seeded all-unequal start** (A2, simulating bully, δ = 0.03, β = 3, φ = ½, to 240N): fair share 0.20 at 120N and 240N; four of 20
runs are fully fair, sixteen fully unequal. 2,770 debounced unequal→fair flips over the runs (hazard 5.5·10⁻⁵ per unequal
island-generation). Accepter-route exits: 67, of which **65 are imported pairs** (both pair holders arrived by migration) and 2 local
certified routes, against 0.56 predicted from the exact second-step rates (4 certified offerers arrived in e while an accepter held v;
1,240 accepter arrivals into v, Σρ = 5.6).

## Verdicts (`runs/script-checked-offers.json`, registered rules)

| prediction | result | verdict |
|---|---|---|
| RE 1 the checker can be built | 0 false acceptances (S0, S1), every spelling accepted, κ_S = 15,141 | holds |
| RE 2 fuel alone does nothing | U: no δ\* at β = 1, 3; β = 3 δ-mean new / old F 0.08 / 0.11, F+R 0.20 / 0.20 | holds |
| RE 3 the threshold survives | A1 δ\* 0.03 (φ 0), 0.01 (φ ½); K the same (A1 = K identically) | holds |
| RE 4 spellings pair (A2 within 0.1 of A1) | δ-mean A2 / A1: 0.68 / 0.54 (φ 0), 0.90 / 0.88 (φ ½); A2 above A1 by 0.14 at φ 0, a sampling difference between identical laws | **fails, falsifier not fired** |
| RE 5 the convention mattered | K2 0.40 against A2 0.68 (β 3, φ 0) | holds |
| RE 6 thresholds do not rise with N | A2 δ\* N 100 → 400: 0.03 → 0.01 (φ 0), 0.01 → 0.003 (φ ½) | holds |
| RE 7 no-exploit is free | A3 / A2 at φ ½: 0.81 / 0.82 (β 1), 0.89 / 0.90 (β 3); A3 is A2's law | holds |
| RE 8 prudence excludes the bully and buys no V\* | Bc paired share A4 0.79 against A2 0.67 (higher); V\* at δ 0.003 A4 0.95 against A2 0.85 (higher) | **falsified (both clauses)** |
| RE 9 the exit is still paced | fair 0.20 at 240N (> 0.15, < 0.3); local certified routes 2 observed against 0.56 predicted (factor 3.6) | **fails, falsifier not fired** |
| RE 10 mass | with scripts: every family ≤ 10⁻⁶⁴ of the reader (clause 1 holds); script-free: none at or above the reader (best 10⁻²⁹·⁵) | **fails, falsifier not fired** |
| RE 11 prudence closes the bully's island | Pc⁺ into e of Bc's island median 1.0; Fc⁺ 27.9 | holds |
| RE 12 A5 | Bc-partnered share of Bc's paired slots 1.00; Bc on ⅔ in A5 / A2 at δ 0.01, 0.003, 0.001: 0.00 / 0.00, 0.05 / 0.00, 0.00 / 0.00 (not larger at every δ ≤ 0.01) | **fails, falsifier not fired** |
| E1 spellings pair neutrally | every cross- and same-spelling pair-slot edge exactly 1 | holds |
| E2 the accepter route does not see spellings | 9.75 and 27.9, same = cross | holds |
| E3 Bc in (Fc⁺, Fc⁺) | pair slot 1; excluded slot 16.9, > 3 in 52% | holds |
| E4 Bc in (Pc⁺, Pc⁺) | pair slot 0.0; excluded slot 1.0 | holds |
| E5 Bc's island | Fc⁺, Fc, Oc⁺ 27.9; OcR⁺ 1.0 | holds |
| E6 the simulating bully cannot break carrier pairs | registered assay (⅔-demanding thirds): median 0.5 for (Fc, Fc), (Fc⁺, Fc⁺), (Pc⁺, Pc⁺) through fallback pairs; post hoc with every non-carrier third: median 0.0 | **falsified** |
| E7 ⅓ constants beside pairs | 1 exactly | holds |
| E8 jump chain | max |z| 2.60 | holds |
| E9 mass, script free | best 10⁻²⁹·⁵ of the reader | holds |
| E10 mass, script counted | ≤ 10⁻⁶⁴; script share ≥ 0.41 | holds |

## The model can't express

- **Prudence that does not cost connectivity.** S_nx is a statement about every profile; a requirement of S_nx excludes the certified
  bully even on islands where it plays fair, and with it most partners. There is no profile-local certificate ("I do not exploit a ⅓
  offer in this triple") that a prudent carrier could require instead.
- **Exclusion beyond the certified branch.** Certificates constrain only what a carrier does when its certified branch fires; its
  fallback still pairs with programs it excludes (Pc⁺–Bc pair through their fallbacks in 28% of triples). No S_nx-derivable fallback in
  T's catalogue refuses a bully.
- **Statements outside a fixed menu.** A carrier can ask a partner only the five statement codes the checker knows (two offers, each
  with two requirement levels, and S_nx); it cannot ask about an arbitrary property of the partner's action function.
- **A cheap certificate.** Under a length prior a script is a long data literal (41–85% of the carrier); there is no way to cite a
  shared derivation by name.
- **Who writes the scripts.** Scripts are genes supplied to founders and tail arrivals with their programs; endogenous production
  (milestone 5) is not in this run, and who writes the first scripts remains the open issue (Provenance).
- **A coordinated two-slot move** out of a simulating bully's island (still); and statements about play inside another program's
  simulation (only root play is certified).

## Scope

N = 100–400 is exploratory. A prudence penalty here may be lost connectivity, not a cost of no-exploit as such: Pc⁺ loses partners
because the dominant pair-holder (Bc) cannot hold S_nx. Cross-spelling success is robustness across the five listed transformations
under one proof convention (the packaging, the statement menu and the shared checker entry), with scripts supplied to founders.

## Deviations from the spec

- The checker's first version (direct style) cost up to 166,456 ticks; it was replaced by the continuation-passing one before any gate
  (RE 1 is scored on the latter; disclosed in the predictions).
- An evaluator extension, the closure regress key (exact on actions and steps; changes failed-read counts only in zero-mass Jr
  profiles), is installed for every table of this queue, V1 and V2 included.
- Each step-2 cell runs on its law's support (per-slot local catalogues); V1 confirmed nothing changes.
- G2's "pointing pairs" is scored on certified eligibility; fair pairs that form through fallbacks are reported separately. The extra
  gate "(Pc⁺, Oc) and (Pc⁺, Rc) do not pair" holds for eligibility; (Pc⁺, Oc) still pairs through fallbacks.
- K2's non-canonical programs are written as their authors would write them (they call CHK on partners): toward canonical carriers they
  offer one-sidedly; among themselves they play their fallbacks. The spec's "they act as their fallbacks" holds only among themselves.
- The fully written-out measure counts each reachable library entry once (the checker's helpers are recursive and cannot be inlined as
  a tree); it is a lower bound on any closed spelling's size.
- E6's registered assay used ⅔-demanding constants as third slots; a post-hoc pass with every non-carrier third is reported beside it.
- RE 9's "observed local routes": the first classifier counted every accepter exit (67); it was refined to queue 79's local/imported
  split and the 20 seeded cells were rerun locally (deterministic; only the new field differs); RE 9 is scored on local certified
  routes (2).
- The timing pilot's table build briefly ran three local workers beside two other processes (about six minutes above the three-worker
  rule). The first S0 table build was killed for memory and restarted with recycled workers.
- No cut was needed; every stage of the spec ran.

## Budget

Daytona: 15 sandbox runs (4 CPUs each), walls summing to 49,683 s = **55 sandbox-CPU-hours** (setup and table builds included; job walls
54 CPU-hours) of the 200 ceiling. Local (3 workers): tables (S1 4 min, K 1 min, S0 31 min), gates (1 min plus a discarded partial
rebuild), V1 and V2 (about 40 CPU-minutes), step 0 (6 min), step 1 (1 min), the seeded rerun (about 30 CPU-minutes), exactness tests,
pilots: about 5 CPU-hours. `python3 tools/daytona_run.py list` is empty.
