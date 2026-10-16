# Removing rival networks: run report (2026-10-16)

Spec `specs/2026-10-15-removing-rivals.md`; notes `notes/removing-rivals.md` (§1 design by hand, §2 validation,
Part 0, costs and the addenda written before the cells they affected); predictions
`predictions/2026-10-15-removing-rivals.md` (the RS's prediction first). Summary numbers in
`runs/removing-rivals.json`; Part 0 in `runs/removing-rivals-part0.json`; the RS's criterion in
`runs/removing-rivals-drift.json`; the shadow check in `runs/removing-rivals-shadow.json`; rows in
`runs/removing_rivals/*.json(.gz)`. ε = 0 cells are lottery statistics at finite (N, I, horizon); rain cells are
finite-ε approach-rate diagnostics, never π. Universal-on-target (uot) = every island held by a unit mutual with
PrudentBot's H unit (τ 123), holders pairwise mutual.

## Validation

- 300 stored S-rule runs at N ≥ 200 reconstructed to generation 2,000: 0 differences over 11,934 trace points; the
  B1 ε = 0 branches match the stored traces beyond 2,000 (0 differences over 1,392 points); save / restore exact; rain
  rate and prior verified; the RE's static counts (2,870 / 2,222) reproduced exactly.

## Part 0 (generation 2,000, 300 runs)

| | count |
|---|---|
| universal-open runs | 185 |
| of which universal-on-target | 132 |
| rival islands in the other 168 runs: closed-open / identity / exploitable / closed-non-open | 1,492 / 770 / 260 / 0 |
| exploitable among non-identity rival islands (target definition) | 0.15 [0.10, 0.21] |
| exploitable among the stored classifier's rival islands | 260 / 260 |
| identity islands with an accessible predator | 0 / 770 |

- Closed-open holders (e.g. `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)`) are open S-guarded programs that cannot
  certify their own defection against DefectBot, so PrudentBot defects against them; FairBot (unit 3, a target unit)
  is mutual with both, and their islands flip with target islands by neutral drift (median episode 70–75
  generations, ≈ 5–8 flips per target island per 10,000 generations at ε = 0).
- Predators: anti-punisher family μ(Pred) ≈ 0.075 (≈ 960 spellings, 358 distinct phenotype units; top
  `if(CHK(me,^D,D),C,D)`, `if(CHK(them,me,D),C,D)`, `if(CHK(me,them,D),C,D)`, 5.2·10⁻⁴ each); certified-defection
  detectors (`if(or(CHK(them,them,D),CHK(me,them,D)),D,C)` …) μ ≈ 0.0056 (≈ 70 spellings). No constant is a
  predator.
- C-donor's uot at 2,000, bounded from stored spellings: ≤ 9/20, ≤ 4/10, ≤ 6/20, ≤ 5/20 at (200, 64), (400, 64),
  (200, 128), (100, 256) (lower bounds 1, 0, 0, 0).

## Part A: sponsored PrudentBot donor (ε = 0)

| cell | uot 2,000 | uot 10,000 [Wilson] | S-nonself uot 10,000 (paired: donor-only / S-only) | identity islands (S-nonself at 2,000) | exploitable | closed-open |
|---|---|---|---|---|---|---|
| (200, 64) sponsored | 15 | **15** [0.53, 0.89] | 11 (8 / 4) | 0.020 (0.056) | 0.000 | 0 |
| (400, 64) sponsored | 10 | **11** [0.34, 0.74] | 8 (7 / 4) | 0.036 (0.043) | 0.002 | 0 |
| (200, 128) sponsored | 2 | **2** [0.03, 0.30] | 3 (2 / 3) | 0.026 (0.075) | 0.030 | 0 |
| (100, 256) sponsored | 2 | **11** [0.34, 0.74] | 6 (8 / 3) | 0.002 (0.010 at 10,000) | 0.002 | 0 |
| (200, 64) empty-list PrudentBot | 12 | 12 | 11 (5 / 4) | 0.021 | 0.006 | 0 |
| (200, 128) empty-list PrudentBot | 6 | 6 | 3 (5 / 2) | 0.025 | 0.018 | 0 |

- One PrudentBot founder per island removes every closed-open rival, with or without its certificates; failures left
  are identity cliques (all A cells) and exploitable rivals (mainly (200, 128)). Pooled over the four sponsored cells
  the paired discordance is 25 donor-only against 14 S-nonself-only runs at 10,000.
- Island P(C,C) ≥ 0.95 on 0.96–0.996 of islands.

## Part B1: cure from generation-2,000 checkpoints (92 checkpoints: 86 calibrated, 6 at mN = 1), matched branches, 10,000 generations

| εN | identity resolved (cure) | exploitable resolved (cure) [run CI] | by predator step | median time | closed-open resolved (cure) | uot runs (ε = 0: 20 / 92) |
|---|---|---|---|---|---|---|
| 0.01 | 2/324 (+0.00) | 89/126 (**+0.70** [0.46, 0.85]) | 41 / 89 | 1,370 | 914/916 (−0.00) | 22 |
| 0.1 | 1/324 (−0.00) | 117/126 (**+0.92** [0.80, 0.99]) | 85 / 117 | 250 | 902/916 (−0.02) | 26 |
| 1 | 2/324 (+0.00) | 119/126 (**+0.94** [0.85, 0.99]) | 79 / 119 | 105 | 898/916 (−0.02) | 40 |

- Exploitable cure by predator mass (μ ≈ 0.0056 detectors / μ ≈ 0.075 anti-punishers): 0.38 / 0.97 at εN = 0.01,
  0.84 / 1.00 at 0.1, 0.89 / 0.99 at 1; the §1.4 formula predicts 0.14 / 0.86, 0.77 / 1.00, 1.00 / 1.00 (pooled
  0.54 / 0.90 / 1.00 against 0.70 / 0.92 / 0.94 observed). Spearman(μ, cured) 0.61 / 0.40 / 0.22.
- Closed-open islands "resolve" equally at ε = 0 (neutral flux both ways), so their matched cure is zero.
- **End state, island fractions pooled over the 92 checkpoints** (ε = 0 / 0.01 / 0.1 / 1): target 0.821 / 0.799 /
  0.788 / 0.781; **identity 0.038 / 0.059 / 0.142 / 0.218**; exploitable 0.015 / 0.017 / 0.008 / 0; closed-open
  0.126 / 0.125 / 0.061 / 0; efficient islands 0.968 / 0.956 / 0.917 / 0.739.
- **Losses of target islands** (per target island at the checkpoint, 10,000 generations): neutral flips to open
  non-target holders 7.5 / 8.3 / 8.1 / 1.6 (median 60–75 generations); to identity 0 / 0.006 / 0.029 / 0.050
  (median length 4,000–6,000, i.e. permanent); unheld 0 / 0.011 / 0.106 / 0.40; other 0 / 0.07 / 0.06 / 0.04.

## Assays

- **Injection** (6 checkpoints, one fresh predator or a matched non-predator into a rival island at 2,000; ε = 0,
  2,000 generations): predators colonize 27/110 (0.25; exact ρ ≈ 0.26), non-predators 1/110; of the 27
  colonized islands 22 end on target; 4 are taken by TwinD-family identity migrants (rs_Snon_200_128_cal 11, where
  identity holds 49 islands) and 1 elsewhere.
- **Forced triples** (8 islands, 4 X and 4 Z, N = 200; the three triples share the predator
  `if(CHK(them,me,D),C,D)` and identical payoff structure, so they are one test with three readings): the predator
  colonizes its island in 9/50 (0.18) and in every such run all four X islands go to the target; matched non-predator
  0/75; target islands lost 0.

## Part B2 (natural rain from generation 0) and B3 (sponsored + rain at εN = 0.1)

| cell | uot 2,000 | uot 10,000 | paired S-nonself at 10,000 (cell-only / S-only) | identity islands at 10,000 | efficient islands |
|---|---|---|---|---|---|
| (200, 64) εN = 0.01 | 7 | 7 | 11 (0 / 4) | 0.093 | 0.925 |
| (200, 64) εN = 0.1 | 5 | 7 | 11 (2 / 6) | 0.271 | 0.867 |
| (200, 64) εN = 1 | 3 | 7 | 11 | 0.378 | 0.673 |
| (200, 128) εN = 0.01 | 2 | 3 | 3 (1 / 1) | 0.111 | 0.928 |
| (200, 128) εN = 0.1 | 1 | 4 | 3 (1 / 0) | 0.207 | 0.874 |
| (200, 128) εN = 1 | 2 | 2 | 3 | 0.290 | 0.603 |
| (200, 64) sponsored + εN = 0.1 | 9 | **10** | sponsored alone 15 (1 / 6) | 0.115 | 0.927 |
| (200, 128) sponsored + εN = 0.1 | 3 | **4** | sponsored alone 2 (4 / 2) | 0.106 | 0.915 |

## The mechanism rain adds: exploitable shadows let identity cliques into target islands

- Replay of one B3 run: three target islands turned identity within 20–40 generations each; in every case the TwinD
  identity unit (e.g. `if(CHK(me,them,D),if(CHK(me,me,D),D,D),C)`, unit 13499) grew from migrants inside an island
  that held a minority of target units it exploits (one of them rain-descended).
- Static: **165 of the 235 target units are exploited by one of the 4 identity holders** (cooperate with it while it
  defects); fresh founders whose phenotype against a target holder is such a target unit have prior mass 0.027
  (e.g. `if(CHK(them,^C,D),C,D)`, `if(CHK(them,^D,D),C,D)`, 5.2·10⁻⁴ each). They enter target islands neutrally
  (target-compatible), and an identity migrant then gains against them.

## The RS's criterion (selected versus drift)

| εN | drift colonizations per 64 islands per 10,000 gen (N = 200 / 400) | of which on target islands (shadows) | selected colonizations | per-arrival colonization, neutral (N = 200 / 400; 1/N = 0.005 / 0.0025) | runs with a cure and no drift colonization |
|---|---|---|---|---|---|
| 0.01 | 6.8 / 3.0 | 616 / 723 | 114 | 0.0029 / 0.0014 | 1 of 17 (at N = 400) |
| 0.1 | 40 / 19 | 3,581 / 4,230 | 1,172 | 0.0020 / 0.0009 | 1 of 28 |
| 1 | 99 / 51 | 9,975 / 10,479 | 1,976 | 0.0012 / 0.0004 | 0 of 28 |

(B1 branches. B2: 5.3 / 25 / 88 per 64 islands per 10,000 at εN = 0.01 / 0.1 / 1; B3: 12.7.) Most frequent drift
colonizers: CooperateBot `C`, FairBot spellings, `if(CHK(them,^D,D),C,D)`, `if(CHK(them,^C,D),C,D)`: the target
network's own shadows. Per-arrival colonization of selected arrivals on rival islands is 0.03–0.05 at εN ≤ 0.1
(all selected types, mostly weakly selected); for the top predators the injection assays give 0.25 ≈ exact ρ, not
2s = 0.6.

## Costs

Part 0 3.6 worker-h; A 2.8; S-nonself (100, 256) 0.4; B3 1.4; injections 2.9; triples 0.1; B1 19.5; B2 5.6; about
36 worker-h in all (≈ 16 h wall on 3 workers). Dropped: B1 at mN = 1 beyond the 6 finished checkpoints, and
rs_prop_400_64_cal 9 (notes §2.5); injection replicates at N = 400 cut to 10.

## Verdicts (scored as declared in the predictions file; rival islands target-relative unless stated)

| # | prediction | outcome |
|---|---|---|
| RS | "drift should never colonize an island, only reintroduce fit programs" | **fails at every rate**: 6.8 / 40 / 99 drift colonizations per 64 islands per 10,000 generations at εN = 0.01 / 0.1 / 1 (N = 200), 85–95% of them neutral shadows of the target network on target islands |
| RE 1 | ≥ 0.8 of non-identity rivals exploitable; 0 identity | **falsifier fired** on the target definition (0.15); held on the stored classifier's rivals (1.00); identity 0/770 held |
| RE 2 | εN = 0.1 cures ≥ 0.8 of exploitable rivals, mostly by predators | **held** (+0.92 [0.80, 0.99]; 85/117 by a predator step) |
| RE 3 | ≤ 0.1 of identity islands resolve at any rate | **held** (≤ 0.01) |
| RE 4 | target-island losses ≤ 0.01 per island at εN ≤ 0.1 | **falsifier fired**: neutral open flips alone are 7.5 per island at ε = 0 and 8 under rain; excluding them, 0.09 (εN = 0.01) and 0.20 (0.1) per island against 0 at ε = 0, of which permanent identity takeovers 0.006 and 0.029 |
| RE 5 | sponsored donor: identity ≤ 0.01, uot ≥ 0.85 everywhere, ≥ C-donor | **falsifier fired** (uot 0.75 / 0.55 / 0.10 / 0.55; identity 0.020–0.036 at N ≥ 200); above C-donor's upper bound at (200, 64) and (400, 64), undecided at (200, 128) and (100, 256) |
| RE 6 | B3 ≥ 0.95 at both geometries | **falsifier fired** (0.50, 0.20) |
| Sol | cure tracks mass, many exploitable unresolved; 5 and 6 too high with geometry-dependent residue; cliques resist more | mass clause **held** (Spearman 0.40 at εN = 0.1), "many unresolved" **failed** (0.07 unresolved); 5/6 clause **held**; clique clause **held** |
| Gemini | cure at εN = 0.1 < 0.4 unless a DefectBot-like predator exists | **failed** (no constant predator; cure 0.92) |
| RE 8 | a window (cures, no drift colonization) at some εN ≤ 0.1 iff μ_pred ≳ 1/(2sN) | **falsifier fired**: at every rate ≥ 1 drift colonization per 64 islands (3–99) with μ_pred ≈ 0.075 for the anti-punishers; 2 of 45 cured checkpoint-branches at εN ≤ 0.1 had none, both at N = 400 |
| M1 | < half of universal-open runs on target | **failed** (132/185 = 0.71; falsifier ≥ 0.75 not fired) |
| M2 | closed-open ≥ 0.5 of non-identity rivals; stored-classifier rivals ≥ 0.6 exploitable | **held** (0.85; 1.00) |
| M3 | anti-punisher μ in [0.005, 0.1], DefectBot not a predator, certified ≥ 10× accessible units | mass and DefectBot **held** (0.075); the ratio **failed** (2,222 vs 358, 6×) |
| M4 | cure ≈ formula ± 0.2; ≥ 0.7 by predators; ≤ 0.05 at ε = 0 | formula **held** (0.70 / 0.92 / 0.94 vs 0.54 / 0.90 / 1.00); predator share **held at εN = 0.1** (0.73), failed at 0.01 (0.46) and 1 (0.66); ε = 0 **held** (1/126) |
| M5 | identity ≤ 0.02; closed-open ≤ 0.15 at εN = 0.1 | identity **held**; closed-open **failed as worded** (0.98 "resolve", as at ε = 0: they are not absorbing) |
| M6 | losses ≤ 0.002 at εN ≤ 0.1; ≥ 1 shadow colonization per run | losses **failed**; shadows **held** |
| M7 | sponsored: identity ≤ 0.03, uot in [0.35, 0.8] above S-nonself and C-donor, residue closed-open; empty control within 0.15 | **falsifier fired** ((200, 128) 0.10); residue is identity and exploitable, not closed-open; empty control held (+0.05, +0.15) |
| M8 | B3 in [0.5, 0.9], within +0.15 of A | **falsifier fired** ((200, 64) 0.25 below A) |
| M9 | B2 changes uot ≤ 0.15 at εN ≤ 0.1; identity not up at εN = 1 | **failed** ((200, 64) −0.20 at both rates; identity 0.29–0.38 at εN = 1 against 0.06–0.07) |
| M10 | predator arrival within 2× of ρ = 0.26; neutral within 3× of 1/N | **held at εN ≤ 0.1** (0.25; 0.0029 and 0.0020 at N = 200); neutral outside at εN = 1 (0.0012) and at N = 400 from εN = 0.1 |
| M11 | injected predator colonizes ≥ 0.15, ≥ 0.8 of those to target; non-predator ≤ 0.02 | **held** (0.25; 22/27 = 0.81; 1/110) |
