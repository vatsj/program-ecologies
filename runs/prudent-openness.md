# Run: prudent openness against identity, and the identity abundance threshold (2026-10-11)

Spec `specs/2026-10-11-prudent-openness.md`; review `reviews/2026-10-11-prudent-openness-gpt-6.1-sol.md`; notes `notes/prudent-openness.md`; predictions `predictions/2026-10-11-prudent-openness.md`; code `src/prudent_openness.py`, `src/prudent_openness_run.py`, `src/prudent_openness_report.py`, `tests/test_prudent_openness.py` (6 tests, passing); summary `runs/prudent-openness.json`; raw per-run records `runs/prudent_openness/lottery_main.json.gz`, `lottery_panel.json.gz`, chain `runs/prudent_openness/chain.json`, statics `static.json`, validation `validate.json`. Base: the identity-and-tags run (grammar, 3,974 classes, cached table, kernel, holder-based endpoint, L prior, seed streams), reused unchanged. K = 10⁶, V = K/4, PD of the modal arm, w = 0.3, mN = 1, 40 runs per cell, every run to 10,000 generations or frozen, common checkpoints 500 / 1,000 / 2,000 / 5,000 / 10,000. **All lottery numbers are ε = 0, finite (N, I, horizon) evidence; the chain is a diagnostic on a reduced support; the two are never pooled.**

## 1. Static (before any cell; notes §1)

- **CBP and CB are compatible.** CBP = `if(and(CHK(them,me,C), CHK(them,⌜C⌝,D)), C, D)` (6 nodes; class of 3 spellings, L mass 9.68·10⁻⁵, S-guarded, no strict invader). The atom `CHK(them,⌜C⌝,D)` asks about the opponent's play against the certificate-less constant ⌜C⌝ = `PROG_C`, not against the catalogue's unconditional cooperator Cc (which carries an opponent-generic C certificate). Every S-guarded carrier defects against ⌜C⌝ (it can verify nothing) and certifies it with δ, so chk_D(CB, ⌜C⌝) = T and CBP cooperates with CB; every unconditional cooperator cooperates with ⌜C⌝, so by soundness none can certify the defection and CBP refuses all of them (one exception of mass 9.7·10⁻⁵). Whole plays (6 × 6, 36/36): CBP–CB (C, C); CBP–Cc (D, C); CBP–D, CBP–EQ, CBP–XC (D, D); CBP self C.
- **CBP's family by the frozen rule** (heaviest maximal clique containing CBP): F_P = 147 classes, 537 spellings, L mass 0.01551, **contains CB**; runner-up 0.01549. Prudent core F_P^pr (members refusing Cc) 38 classes, 0.00218 (14%); nice part F_P^n 109 classes, 0.01333. 39 members S-guarded (0.0057), 108 with a strict invader (0.0098). Overlaps: F_CB 105 classes (0.0132); F_P ⊂ N(CB) ∪ {CB}; P_open read as "open and refuses Cc" (39 classes, 0.00225): 38 in F_P; P_open read as worded, "S-guarded establishers refusing Cc" (28, 0.0014; open 16, exclusive 7, tag 4, other 1): 16 in F_P; F_X: 0. CBP's bridge-connected component: 568 classes, 0.066, containing XC, not EQ.
- **CBP against XC:** (i) actions: CBP plays C against CB; CBP and XC mutually defect. (ii) certificates: CBP's list is [(C, σ_P), (D, δ)]; chk_D(CBP, ⌜CB⌝) = F (no sound script certifies a defection that does not happen), chk_C(XC, CBP) = F. (iii) paths: F_X = the exclusive label (9 classes, 5.81·10⁻⁴); 72 direct F_P–F_X edges, **all through one member of F_X, XB = `if(CHK(me,⌜CB⌝,C), D, if(CHK(them,me,C), C, D))`** (1.45·10⁻⁴, no strict invader), mutual with CBP, 71 other F_P members (18 core), XC, XC′, MC¹, OF¹, Cc, not CB; XB is the only CBP|XC bridge; 150 length-2 intermediates outside both families (0.0144), 37,000 length-3 pairs.
- **Seed payoff** (L): CBP −0.043, EQ +0.001, CB −0.441, XC −0.025, D +0.001; core −0.089, nice −0.442. Core − nice: 0.347 with cooperators, 0.106 without (P4p/P4n). Copies per run at M: 201 for every tilted block; **islands per seeded copy of a block at M is capped at 64/201 = 0.32.**

**Validation** (notes §1.14): hand table 36/36 by whole plays and table; checker facts; families and paths reproduced; every seed law exact (block errors 0, rest proportional to L to 10⁻⁹, draws within 3 s.d.); P2 = the identity run's T1c prior exactly; the kernel reproduces the identity run's replicates 0–9 of L, T1c and no-clique at 2,000 (30/30) and at 10,000 where continued (21/21); stage-logger consistency held in every run of every cell. A §1.7 slip found by the tests before any cell: the second curve's m_L point is not P1 (P1 renormalizes the identity mass to 0.00883; the scan holds it at 0.00898), so it was run as its own cell.

**Design elaborations, all before any counted cell** (notes §1.3, §1.6): because F_P is 86% nice and contains CB, the matched cells P1p (core at M) / P2n (nice part at M), P4p / P4n (the same without unconditional cooperators), P3p and P5p were added beside the spec's P1–P5 and P4′, which are run and scored as written. **After the cells, not preregistered:** the scanB refinement points (the preregistered rule, triggered: scanB's crossing fell between 2·10⁻³ and 5·10⁻³) and the panel's clique-free baseline m = 0 at the three panel (N, I) (added because the bracketing points did not locate a crossing at any panel setting).

## 2. Part 1: prudent openness (paired seeds, (100, 64))

### Outcomes at the common checkpoints (40 runs per cell; universal-open / F_P-universal / core-universal / patchwork / unresolved / failed)

| cell | @500 | @1000 | @2000 | @5000 | @10000 |
|---|---|---|---|---|---|
| L | 0 / 0 / 0 / 34 / 6 / 0 | 0 / 0 / 0 / 36 / 4 / 0 | 0 / 0 / 0 / 39 / 1 / 0 | 0 / 0 / 0 / 35 / 5 / 0 | 3 / 2 / 1 / 36 / 1 / 0 |
| P1: F_P at M | 0 / 0 / 0 / 36 / 4 / 0 | 0 / 0 / 0 / 38 / 2 / 0 | 0 / 0 / 0 / 38 / 2 / 0 | 1 / 1 / 0 / 39 / 0 / 0 | 7 / 7 / 0 / 33 / 0 / 0 |
| P2: ten CB spellings (T1c) | 0 / 0 / 0 / 38 / 2 / 0 | 0 / 0 / 0 / 38 / 2 / 0 | 1 / 1 / 0 / 37 / 2 / 0 | 2 / 2 / 0 / 35 / 3 / 0 | 7 / 7 / 0 / 32 / 1 / 0 |
| P3: F_P at M, identity removed | 18 / 10 / 0 / 22 / 0 / 0 | 21 / 12 / 0 / 18 / 1 / 0 | 21 / 12 / 0 / 18 / 1 / 0 | 24 / 15 / 1 / 16 / 0 / 0 | 28 / 19 / 2 / 12 / 0 / 0 |
| P4: F_P at M, cooperators removed | 0 / 0 / 0 / 38 / 2 / 0 | 0 / 0 / 0 / 36 / 4 / 0 | 0 / 0 / 0 / 39 / 1 / 0 | 0 / 0 / 0 / 39 / 1 / 0 | 8 / 7 / 0 / 32 / 0 / 0 |
| P4′: P2, cooperators removed | 0 / 0 / 0 / 38 / 2 / 0 | 0 / 0 / 0 / 35 / 5 / 0 | 1 / 1 / 0 / 36 / 3 / 0 | 1 / 1 / 0 / 38 / 1 / 0 | 3 / 3 / 0 / 36 / 1 / 0 |
| P5: F_P at M/2 + ten EQ at M/20 | 0 / 0 / 0 / 35 / 5 / 0 | 0 / 0 / 0 / 34 / 6 / 0 | 0 / 0 / 0 / 36 / 4 / 0 | 0 / 0 / 0 / 33 / 7 / 0 | 0 / 0 / 0 / 37 / 3 / 0 |
| P1p: core at M | 0 / 0 / 0 / 35 / 5 / 0 | 0 / 0 / 0 / 39 / 1 / 0 | 0 / 0 / 0 / 39 / 1 / 0 | 2 / 2 / 2 / 36 / 2 / 0 | 10 / 9 / 9 / 30 / 0 / 0 |
| P2n: nice part at M | 0 / 0 / 0 / 33 / 7 / 0 | 1 / 0 / 0 / 39 / 0 / 0 | 1 / 0 / 0 / 37 / 2 / 0 | 2 / 0 / 0 / 36 / 2 / 0 | 4 / 0 / 0 / 35 / 1 / 0 |
| P3p: core at M, identity removed | 13 / 12 / 12 / 27 / 0 / 0 | 17 / 16 / 16 / 23 / 0 / 0 | 21 / 19 / 19 / 19 / 0 / 0 | 25 / 23 / 23 / 15 / 0 / 0 | 31 / 29 / 29 / 9 / 0 / 0 |
| P4p: core at M, cooperators removed | 1 / 1 / 1 / 38 / 1 / 0 | 1 / 1 / 1 / 37 / 2 / 0 | 1 / 1 / 1 / 37 / 2 / 0 | 1 / 1 / 1 / 38 / 1 / 0 | 10 / 9 / 9 / 29 / 1 / 0 |
| P4n: nice at M, cooperators removed | 0 / 0 / 0 / 39 / 1 / 0 | 0 / 0 / 0 / 40 / 0 / 0 | 0 / 0 / 0 / 35 / 5 / 0 | 1 / 0 / 0 / 35 / 4 / 0 | 7 / 4 / 0 / 32 / 1 / 0 |
| P5p: core at M/2 + ten EQ at M/20 | 0 / 0 / 0 / 31 / 9 / 0 | 0 / 0 / 0 / 34 / 6 / 0 | 0 / 0 / 0 / 37 / 3 / 0 | 0 / 0 / 0 / 34 / 6 / 0 | 0 / 0 / 0 / 39 / 1 / 0 |

### Island shares at 2,000 → 10,000 (fraction of island-runs held)

| cell | F_P | core | nice | CB set | open | identity | ten EQ | XC (F_X) | XB |
|---|---|---|---|---|---|---|---|---|---|
| L | 0.40 → 0.52 | 0.10 → 0.10 | 0.30 → 0.42 | 0.11 → 0.19 | 0.51 → 0.65 | 0.41 → 0.29 | 0.05 → 0.04 | 0.01 → 0.01 | 0.000 → 0.000 |
| P1: F_P at M | 0.64 → 0.76 | 0.16 → 0.14 | 0.48 → 0.63 | 0.19 → 0.21 | 0.70 → 0.82 | 0.24 → 0.12 | 0.01 → 0.01 | 0.04 → 0.04 | 0.000 → 0.000 |
| P2: ten CB spellings (T1c) | 0.72 → 0.88 | 0.00 → 0.00 | 0.72 → 0.88 | 0.72 → 0.88 | 0.72 → 0.88 | 0.23 → 0.10 | 0.02 → 0.00 | 0.02 → 0.00 | 0.005 → 0.000 |
| P3: F_P at M, identity removed | 0.91 → 0.95 | 0.23 → 0.20 | 0.68 → 0.75 | 0.28 → 0.32 | 0.97 → 0.99 | 0.00 → 0.00 | 0.00 → 0.00 | 0.00 → 7.81e-04 | 0.000 → 0.000 |
| P4: F_P at M, cooperators removed | 0.63 → 0.76 | 0.07 → 0.09 | 0.56 → 0.68 | 0.23 → 0.24 | 0.72 → 0.84 | 0.26 → 0.12 | 0.01 → 0.00 | 0.01 → 0.03 | 0.005 → 0.025 |
| P4′: P2, cooperators removed | 0.68 → 0.85 | 0.00 → 0.00 | 0.68 → 0.85 | 0.68 → 0.85 | 0.68 → 0.85 | 0.28 → 0.13 | 0.03 → 0.02 | 0.02 → 0.01 | 0.006 → 0.002 |
| P5: F_P at M/2 + ten EQ at M/20 | 0.23 → 0.30 | 0.06 → 0.06 | 0.17 → 0.23 | 0.04 → 0.06 | 0.30 → 0.39 | 0.65 → 0.56 | 0.42 → 0.39 | 0.01 → 0.01 | 0.000 → 0.000 |
| P1p: core at M | 0.77 → 0.88 | 0.77 → 0.88 | 0.00 → 0.00 | 0.00 → 0.00 | 0.80 → 0.93 | 0.18 → 0.06 | 0.02 → 0.00 | 0.00 → 0.00 | 0.000 → 0.000 |
| P2n: nice part at M | 0.60 → 0.75 | 0.00 → 0.00 | 0.60 → 0.75 | 0.26 → 0.35 | 0.73 → 0.88 | 0.23 → 0.10 | 0.03 → 0.01 | 0.02 → 0.01 | 0.000 → 0.000 |
| P3p: core at M, identity removed | 0.94 → 0.97 | 0.94 → 0.97 | 0.00 → 0.00 | 0.00 → 0.00 | 0.97 → 1.00 | 0.00 → 0.00 | 0.00 → 0.00 | 0.02 → 0.00 | 0.000 → 0.000 |
| P4p: core at M, cooperators removed | 0.60 → 0.75 | 0.60 → 0.75 | 0.00 → 0.00 | 0.00 → 0.00 | 0.67 → 0.82 | 0.29 → 0.16 | 0.01 → 0.01 | 0.01 → 0.01 | 0.001 → 0.000 |
| P4n: nice at M, cooperators removed | 0.53 → 0.64 | 0.00 → 0.00 | 0.53 → 0.64 | 0.24 → 0.38 | 0.68 → 0.84 | 0.29 → 0.14 | 0.03 → 0.01 | 0.02 → 0.01 | 7.81e-04 → 0.000 |
| P5p: core at M/2 + ten EQ at M/20 | 0.39 → 0.52 | 0.39 → 0.52 | 0.00 → 0.00 | 0.00 → 0.00 | 0.45 → 0.63 | 0.52 → 0.34 | 0.39 → 0.25 | 0.01 → 0.02 | 0.004 → 0.013 |

### Cross-island P(C,C) at 2,000 → 10,000 (overall; among readers; over island pairs both held by F_P, with the number of runs having ≥ 2 such islands at 10,000)

| cell | overall | readers | F_P-held island pairs | island P(C,C) @10,000 | E3 success | frozen |
|---|---|---|---|---|---|---|
| L | 0.401 → 0.593 | 0.401 → 0.593 | 0.956 → 0.973 (31) | 0.965 | 40 | 3 |
| P1: F_P at M | 0.575 → 0.786 | 0.575 → 0.786 | 0.975 → 0.987 (36) | 0.981 | 40 | 7 |
| P2: ten CB spellings (T1c) | 0.587 → 0.827 | 0.587 → 0.827 | 0.978 → 0.989 (40) | 0.985 | 40 | 7 |
| P3: F_P at M, identity removed | 0.945 → 0.985 | 0.945 → 0.985 | 0.997 → 0.999 (40) | 0.999 | 40 | 28 |
| P4: F_P at M, cooperators removed | 0.596 → 0.803 | 0.596 → 0.803 | 0.972 → 0.987 (37) | 0.982 | 40 | 8 |
| P4′: P2, cooperators removed | 0.531 → 0.756 | 0.531 → 0.756 | 0.971 → 0.988 (40) | 0.980 | 40 | 3 |
| P5: F_P at M/2 + ten EQ at M/20 | 0.204 → 0.320 | 0.204 → 0.320 | 0.932 → 0.943 (33) | 0.942 | 40 | 0 |
| P1p: core at M | 0.667 → 0.890 | 0.667 → 0.890 | 0.982 → 0.994 (38) | 0.990 | 40 | 10 |
| P2n: nice part at M | 0.590 → 0.815 | 0.590 → 0.815 | 0.978 → 0.989 (39) | 0.984 | 40 | 4 |
| P3p: core at M, identity removed | 0.947 → 0.991 | 0.947 → 0.991 | 0.998 → 0.999 (40) | 0.999 | 40 | 31 |
| P4p: core at M, cooperators removed | 0.531 → 0.746 | 0.531 → 0.746 | 0.968 → 0.982 (38) | 0.980 | 40 | 10 |
| P4n: nice at M, cooperators removed | 0.552 → 0.806 | 0.552 → 0.806 | 0.971 → 0.985 (32) | 0.983 | 40 | 7 |
| P5p: core at M/2 + ten EQ at M/20 | 0.279 → 0.504 | 0.279 → 0.504 | 0.949 → 0.971 (34) | 0.959 | 40 | 0 |

Readers equal overall at both checkpoints because the constant-row classes (unconditional cooperators and defectors) are extinct everywhere by generation 2,000.

### Stages (pooled over runs; @10,000 unless marked)

| cell | family | copies / run | seed islands occupied / run | est. per occupied @2,000 / @10,000 | extinction prob. | median est. gen (q90) | persistence @10,000 | spread / run @10,000 | held / run @10,000 | islands per copy @2,000 / @10,000 |
|---|---|---|---|---|---|---|---|---|---|---|
| L | FP | 97.3 | 49.7 | 0.061 / 0.061 | 0.939 | 30 (50) | 0.803 | 30.7 | 33.2 | 0.262 / 0.341 |
| L | core | 13.0 | 11.9 | 0.055 / 0.055 | 0.945 | 30 (50) | 0.231 | 6.0 | 6.1 | 0.482 / 0.470 |
| L | nice | 84.4 | 46.7 | 0.050 / 0.050 | 0.950 | 30 (50) | 0.670 | 25.5 | 27.1 | 0.228 / 0.321 |
| L | identity | 56.6 | 38.1 | 0.106 / 0.106 | 0.894 | 30 (50) | 0.463 | 16.9 | 18.8 | 0.468 / 0.332 |
| P1 | FP | 199.1 | 61.2 | 0.113 / 0.113 | 0.887 | 30 (53) | 0.878 | 42.9 | 49.0 | 0.207 / 0.246 |
| P1 | core | 27.0 | 22.0 | 0.059 / 0.059 | 0.941 | 30 (50) | 0.154 | 8.7 | 8.8 | 0.382 / 0.327 |
| P1 | nice | 172.1 | 59.8 | 0.093 / 0.093 | 0.907 | 30 (60) | 0.752 | 35.9 | 40.1 | 0.180 / 0.233 |
| P1 | identity | 56.1 | 37.1 | 0.091 / 0.091 | 0.909 | 30 (50) | 0.326 | 6.5 | 7.5 | 0.279 / 0.135 |
| P2 | CBset | 203.1 | 62.0 | 0.130 / 0.130 | 0.870 | 30 (50) | 0.984 | 48.5 | 56.4 | 0.227 / 0.278 |
| P2 | identity | 55.4 | 36.8 | 0.096 / 0.096 | 0.904 | 30 (50) | 0.268 | 5.7 | 6.7 | 0.269 / 0.120 |
| P3 | FP | 200.1 | 61.2 | 0.125 / 0.125 | 0.875 | 30 (50) | 0.948 | 53.8 | 61.1 | 0.290 / 0.305 |
| P3 | core | 26.9 | 21.9 | 0.079 / 0.079 | 0.921 | 30 (42) | 0.290 | 12.5 | 13.0 | 0.537 / 0.484 |
| P3 | nice | 173.2 | 59.8 | 0.099 / 0.099 | 0.901 | 30 (50) | 0.789 | 43.4 | 48.1 | 0.252 / 0.278 |
| P4 | FP | 201.6 | 61.1 | 0.119 / 0.119 | 0.881 | 30 (50) | 0.866 | 42.6 | 48.9 | 0.199 / 0.242 |
| P4 | core | 28.5 | 23.2 | 0.038 / 0.038 | 0.962 | 30 (40) | 0.314 | 5.3 | 5.5 | 0.152 / 0.195 |
| P4 | nice | 173.0 | 59.5 | 0.105 / 0.105 | 0.895 | 30 (50) | 0.763 | 38.5 | 43.3 | 0.207 / 0.250 |
| P4 | identity | 89.3 | 48.0 | 0.071 / 0.071 | 0.929 | 30 (50) | 0.299 | 7.0 | 8.0 | 0.183 / 0.090 |
| P4' | CBset | 202.7 | 61.6 | 0.125 / 0.125 | 0.875 | 30 (50) | 0.968 | 46.8 | 54.3 | 0.215 / 0.268 |
| P4' | identity | 91.2 | 48.2 | 0.080 / 0.080 | 0.920 | 30 (50) | 0.299 | 7.5 | 8.6 | 0.195 / 0.095 |
| P5 | FP | 99.9 | 50.4 | 0.057 / 0.057 | 0.943 | 30 (50) | 0.684 | 17.0 | 18.9 | 0.146 / 0.189 |
| P5 | EQten | 101.3 | 51.1 | 0.130 / 0.130 | 0.870 | 30 (50) | 0.706 | 20.0 | 24.7 | 0.268 / 0.244 |
| P5 | identity | 153.6 | 58.8 | 0.175 / 0.175 | 0.825 | 30 (50) | 0.755 | 28.1 | 35.9 | 0.271 / 0.234 |
| P1p | core | 200.3 | 61.4 | 0.186 / 0.186 | 0.814 | 30 (50) | 0.928 | 46.0 | 56.6 | 0.247 / 0.283 |
| P1p | identity | 57.2 | 38.5 | 0.097 / 0.097 | 0.903 | 30 (50) | 0.228 | 2.7 | 3.6 | 0.196 / 0.062 |
| P2n | nice | 198.0 | 61.3 | 0.119 / 0.119 | 0.881 | 30 (50) | 0.822 | 42.0 | 48.0 | 0.193 / 0.242 |
| P2n | identity | 56.2 | 37.0 | 0.087 / 0.087 | 0.913 | 30 (50) | 0.264 | 5.5 | 6.4 | 0.264 / 0.114 |
| P3p | core | 199.6 | 61.0 | 0.174 / 0.174 | 0.826 | 30 (50) | 0.972 | 51.8 | 62.1 | 0.303 / 0.311 |
| P4p | core | 197.4 | 61.0 | 0.120 / 0.120 | 0.880 | 30 (50) | 0.857 | 41.7 | 48.0 | 0.196 / 0.243 |
| P4p | identity | 87.2 | 47.5 | 0.077 / 0.077 | 0.923 | 30 (50) | 0.381 | 9.1 | 10.5 | 0.210 / 0.120 |
| P4n | nice | 201.8 | 61.5 | 0.118 / 0.118 | 0.882 | 30 (50) | 0.742 | 35.5 | 41.0 | 0.169 / 0.203 |
| P4n | identity | 88.5 | 47.8 | 0.087 / 0.087 | 0.913 | 30 (50) | 0.269 | 8.0 | 9.1 | 0.206 / 0.103 |
| P5p | core | 99.8 | 50.8 | 0.098 / 0.098 | 0.902 | 30 (50) | 0.765 | 29.2 | 33.1 | 0.253 / 0.331 |
| P5p | EQten | 98.9 | 49.3 | 0.133 / 0.133 | 0.867 | 30 (50) | 0.483 | 13.1 | 16.2 | 0.253 / 0.164 |
| P5p | identity | 152.0 | 57.5 | 0.168 / 0.168 | 0.832 | 30 (50) | 0.514 | 16.5 | 21.4 | 0.218 / 0.141 |

### Largest-established-set predictor and tracked classes

| cell | decided @2,000 / @10,000 | largest-established won | largest-seeded won | XB seeded (runs) / alive at first separation / ever held | CBP seeded / ever held |
|---|---|---|---|---|---|
| L | 0 / 3 | 0 / 3 | 0 / 0 | 23 / 2 / 2 | 17 / 0 |
| P1: F_P at M | 0 / 7 | 0 / 7 | 0 / 5 | 19 / 3 / 2 | 30 / 1 |
| P2: ten CB spellings (T1c) | 1 / 7 | 1 / 7 | 1 / 7 | 27 / 3 / 2 | 0 / 0 |
| P3: F_P at M, identity removed | 21 / 28 | 20 / 27 | 2 / 7 | 20 / 2 / 1 | 28 / 5 |
| P4: F_P at M, cooperators removed | 0 / 8 | 0 / 8 | 0 / 7 | 28 / 3 / 3 | 28 / 4 |
| P4′: P2, cooperators removed | 1 / 3 | 1 / 3 | 0 / 1 | 35 / 3 / 1 | 0 / 0 |
| P5: F_P at M/2 + ten EQ at M/20 | 0 / 0 | 0 / 0 | 0 / 0 | 23 / 0 / 0 | 22 / 2 |
| P1p: core at M | 0 / 10 | 0 / 10 | 0 / 0 | 26 / 1 / 1 | 40 / 21 |
| P2n: nice part at M | 1 / 4 | 1 / 4 | 0 / 3 | 27 / 4 / 2 | 0 / 0 |
| P3p: core at M, identity removed | 21 / 31 | 21 / 31 | 6 / 8 | 21 / 2 / 2 | 40 / 16 |
| P4p: core at M, cooperators removed | 1 / 10 | 1 / 10 | 0 / 0 | 32 / 5 / 3 | 40 / 17 |
| P4n: nice at M, cooperators removed | 0 / 7 | 0 / 7 | 0 / 6 | 28 / 6 / 3 | 0 / 0 |
| P5p: core at M/2 + ten EQ at M/20 | 0 / 0 | 0 / 0 | 0 / 0 | 25 / 3 / 2 | 40 / 14 |

## 3. Part 2: the identity abundance threshold (scan in identity mass m at (100, 64); scaling panel)

### The identity abundance scan (universal-open runs of 40 at 2,000 / 10,000; A = without F_P at M, B = with F_P at M)


**scanA**

| m | copies / run | universal-open @2,000 | @10,000 | F_P-universal @10,000 | identity islands @10,000 | identity islands per run @10,000 | cross P(C,C) @10,000 | identity est. per occupied seed island |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.0 | 24 | 30 | 17 | 0.000 | 0.0 | 0.981 | – |
| 0.0002 | 1.3 | 18 | 27 | 15 | 0.020 | 1.2 | 0.938 | 0.020 |
| 0.0005 | 3.2 | 15 | 26 | 14 | 0.003 | 0.2 | 0.959 | 0.039 |
| 0.001 | 6.4 | 17 | 24 | 13 | 0.050 | 3.2 | 0.919 | 0.065 |
| 0.002 | 12.8 | 8 | 12 | 6 | 0.078 | 5.0 | 0.878 | 0.074 |
| 0.005 | 32.0 | 0 | 6 | 5 | 0.201 | 12.8 | 0.713 | 0.087 |
| 0.00898 | 57.5 | 0 | 3 | 2 | 0.294 | 18.8 | 0.593 | 0.106 |
| 0.02 | 128.0 | 0 | 0 | 0 | 0.521 | 33.4 | 0.396 | 0.164 |

**scanB** (refinement points: scanBm_0.002714, scanBm_0.003684)

| m | copies / run | universal-open @2,000 | @10,000 | F_P-universal @10,000 | identity islands @10,000 | identity islands per run @10,000 | cross P(C,C) @10,000 | identity est. per occupied seed island |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.0 | 21 | 28 | 19 | 0.000 | 0.0 | 0.985 | – |
| 0.0002 | 1.3 | 18 | 28 | 16 | 7.81e-04 | 0.1 | 0.962 | 0.043 |
| 0.0005 | 3.2 | 16 | 29 | 23 | 0.009 | 0.6 | 0.970 | 0.090 |
| 0.001 | 6.4 | 15 | 27 | 21 | 0.006 | 0.4 | 0.977 | 0.067 |
| 0.002 | 12.8 | 11 | 23 | 10 | 0.022 | 1.4 | 0.951 | 0.048 |
| 0.00271 | 17.4 | 7 | 17 | 12 | 0.025 | 1.6 | 0.945 | 0.072 |
| 0.00368 | 23.6 | 3 | 14 | 9 | 0.039 | 2.5 | 0.907 | 0.072 |
| 0.005 | 32.0 | 4 | 14 | 11 | 0.053 | 3.4 | 0.887 | 0.074 |
| 0.00898 | 57.5 | 0 | 4 | 3 | 0.150 | 9.6 | 0.778 | 0.096 |
| 0.02 | 128.0 | 0 | 0 | 0 | 0.237 | 15.2 | 0.613 | 0.145 |

**Crossings** (50% of runs universal-open; paired bootstrap 95% interval; fraction of resamples at a scan boundary):

- scanA @2000: m* = 0.000133 [0, 0.000398] (ok; boundary 0.12; on the eight preregistered points 0.000133); copies per run 0.9; fit f = e^(−6400 m q) on m ≤ 10⁻³: q = 0.2759, residuals [-0.4, -0.25, -0.04, 0.25, 0.17, -0.0, -0.0, -0.0]; fit f = f₀ e^(−6400 m q): f₀ = 0.536, q = 0.0578, residuals [0.06, -0.05, -0.07, 0.05, -0.06, -0.08, -0.02, -0.0]
- scanA @10000: m* = 0.00126 [0.000659, 0.00159] (ok; boundary 0.00; on the eight preregistered points 0.00126); copies per run 8.1; fit f = e^(−6400 m q) on m ≤ 10⁻³: q = 0.1101, residuals [-0.25, -0.19, -0.05, 0.11, 0.06, 0.12, 0.07, -0.0]; fit f = f₀ e^(−6400 m q): f₀ = 0.729, q = 0.0328, residuals [0.02, -0.02, -0.01, 0.01, -0.18, -0.11, -0.04, -0.01]
- scanB @2000: m* = 6.67e-05 [0, 0.000429] (ok; boundary 0.39; on the eight preregistered points 6.67e-05); copies per run 0.4; fit f = e^(−6400 m q) on m ≤ 10⁻³: q = 0.2845, residuals [-0.47, -0.24, -0.0, 0.21, 0.25, 0.17, 0.07, 0.1, -0.0, -0.0]; fit f = f₀ e^(−6400 m q): f₀ = 0.502, q = 0.0533, residuals [0.02, -0.02, -0.02, 0.02, 0.02, -0.02, -0.07, 0.01, -0.02, -0.0]
- scanB @10000: m* = 0.00233 [0.00141, 0.00316] (ok; boundary 0.00; on the eight preregistered points 0.00271); copies per run 14.9; fit f = e^(−6400 m q) on m ≤ 10⁻³: q = 0.0832, residuals [-0.3, -0.2, -0.04, 0.09, 0.23, 0.19, 0.21, 0.28, 0.09, -0.0]; fit f = f₀ e^(−6400 m q): f₀ = 0.709, q = 0.0049, residuals [-0.01, -0.0, 0.03, -0.01, -0.09, -0.23, -0.28, -0.26, -0.44, -0.38]
- shift factor m*_B / m*_A @10,000 = 1.85 (unrefined 2.15), paired bootstrap [1.07, 4.00]

### Scaling panel (the two bracketing scan points, 10⁻³ and 2·10⁻³, preregistered; m = 0 added after the panel)

| (N, I) | m points | universal-open @2,000 | universal-open @10,000 | identity islands @10,000 | m* @10,000 (flag) | copies per run N·I·m* |
|---|---|---|---|---|---|---|
| (100,128) | [0.0, 0.001, 0.002] | [8, 7, 3] | [19, 15, 13] | [0.0, 0.014, 0.054] | 0 (below) | 0.0 |
| (100,32) | [0.0, 0.001, 0.002] | [17, 20, 18] | [21, 26, 25] | [0.0, 0.065, 0.112] | 0.002 (above) | 6.4 |
| (100,64) | [0.0, 0.001, 0.002] | [24, 17, 8] | [30, 24, 12] | [0.0, 0.05, 0.078] | 0.00126 (ok) | 8.1 |
| (50,64) | [0.0, 0.001, 0.002] | [33, 37, 31] | [33, 37, 31] | [0.0, 0.05, 0.075] | 0.002 (above) | 6.4 |

Panel reading: the preregistered statistic (interpolation between the two bracketing points) gives no crossing at any panel setting: f stays below 0.5 at both points at (100, 128) and above 0.5 at both at (100, 32) and (50, 64). The added m = 0 baseline shows why: the clique-free universal fraction f₀ itself depends on (N, I) (10,000: 0.825 at (50, 64), 0.525 at (100, 32), 0.75 at (100, 64), 0.475 at (100, 128)); at (100, 128) it is already below one half, so no crossing exists; at N = 50 rival networks resolve by majority (0 patchworks in 120 runs) and an identity clique or the exclusive club then occasionally takes the whole metapopulation (universal-other 3–9 of 40). Compared at equal seeded clique copies per run, the panel is roughly consistent with the main scan (3.2 copies: 0.925 at (50, 64), 0.65 at (100, 32), 0.65 at (100, 64) m = 5·10⁻⁴; 12.8 copies: 0.375 at (100, 128), 0.30 at (100, 64) m = 2·10⁻³), but the 50% level is set by f₀(N, I), not by copies.

## 4. Part 3: the chain (diagnostic; reduced support)

Support: the 1,500 heaviest classes under L ∪ the 322 identity cliques ∪ F_P (all 147 present), the closed leak components removed (exactly the 322 identity cliques): 1,587 classes; `FastChain`, θ = 10⁻⁸, ≤ 4,000 states; 1,611 / 1,587 recurrent states at 10³ / 10⁴ (all monomorphic), unexplored flow 0.0020 / 0.0022.

| N | P(C,C) | π(all-D) | π by label | π(F_X) | π(core) | π(nice) | π(CBP) | π(XB) | top cooperative state | twin drift off |
|---|---|---|---|---|---|---|---|---|---|---|
| 10³ | 0.589 | 0.056 | open 0.347, exclusive 0.207, other 0.032, non-establishers 0.413 | 0.207 | 0.172 | 0.132 | 0.022 | 0.002 | `if(and(CHK(them,⌜CB⌝,D),CHK(them,me,C)),C,D)` (XC′, π 0.093) | identical (to 10⁻⁹) |
| 10⁴ | 0.800 | 0.025 | open 0.438, exclusive 0.318, other 0.043, non-establishers 0.200 | 0.318 | 0.221 | 0.160 | 0.034 | 0.004 | XC′ (π 0.143), then XC (0.141) | identical |

Transition structure (10⁴): XC and XC′ exit by neutral drift into the shadow `if(CHK(them,⌜CB⌝,D),C,D)` (log₁₀ rate −6.5; −5.5 at 10³, so ∝ 1/N); the core's states (CBP 0.034, its order twin 0.034, the ⌜D⌝ variant 0.030) exit neutrally into the shadows `if(CHK(them,⌜C⌝,D),C,D)` / `if(CHK(them,⌜D⌝,D),C,D)` (−6.5); the nice carrier `if(not(CHK(them,me,C)),D,C)` (0.069) exits into Cc (−5.1). P(C,C) is within 0.03 of the identity run's topLnoclosed (0.560 / 0.781): adding F_P's light members changes little, and the core is the second cooperative group behind the exclusive club. **Closure check:** classes outside the support that invade a top state neutrally or better: XC 35 (L mass 0.0012), core states 203–242 (0.006–0.007), the nice carrier 1,078 (0.033, mostly neutral shadows) — the omitted exits are named as the caveat; they would add neutral exits, most for the nice carriers. **Twin-drift check:** vacuous here (twin moves act only on polymorphic states, and the recurrent set has none).

## 5. Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | P1: CBP's family's islands per copy ≥ 0.35; CBP's seed payoff within 0.05 of EQ's; F_P-universal ≥ 0.5 at 10,000 | **failed, falsifier fired** (F_P-universal 7/40 = 0.175 ≤ 0.2). Islands per copy 0.246 (≥ 0.35 unreachable: the cap is 0.32; > 0.2, so that falsifier clause did not fire); the seed-payoff clause held (−0.042 vs −0.015). The premise failed statically: CBP's family is 86% nice and contains CB. On the intended object (the prudent core, P1p): core-universal 9/40, 0.283 islands per copy |
| RE 2 | CBP − CB difference in established islands per occupied seed island at least halved without cooperators (P4/P4′ against P1/P2) | **held as worded, uninformative**: F_P − CB set = −0.017 (P1/P2), −0.006 (P4/P4′), ratio 0.35; both negative and within about two standard errors. On the matched design (core − nice, scored as S3) the mechanism held strongly: 0.067 → 0.002 (ratio 0.03) |
| RE 3 | P5: F_P holds more islands than the ten EQ spellings at 10,000 (≥ 0.6 vs ≤ 0.3) | **failed, falsifier fired** (F_P 0.30, ten EQ 0.39). With the prudent core in F_P's place (P5p) the core holds 0.52 against 0.25 |
| RE 4 | CBP–CB incompatible; the tactic produces CBP's D script against ⌜CB⌝; within-family cross-island P(C,C) ≥ 0.9 under P1 | **failed, falsifier fired statically** (CBP–CB compatible; no D script against ⌜CB⌝ exists; CBP and XC mutually defect). The within-family statistic is 0.987 (≥ 0.9), nearly trivial since F_P is a clique |
| RE 5 | exponential at low m (one q), upward deviation above, crossing in [3·10⁻⁴, 3·10⁻³], panel ≤ 2× | **held at (100, 64)** (m* = 1.26·10⁻³ [6.6·10⁻⁴, 1.6·10⁻³]; one-parameter residuals −0.25, −0.19, −0.05, +0.11 at m ≤ 10⁻³, none ≥ 0.3; +0.06 / +0.12 / +0.07 above); **the panel clause failed**: no crossing at any panel setting between the bracketing points; at (100, 128) none exists (f₀ = 0.475). The ≥ 4× falsifier is not determinable from bounds (< 10⁻³ at (100, 128), > 2·10⁻³ at (100, 32) and (50, 64)). The one-parameter form misfits at m → 0 (f(0) = 0.75); f₀ e^{−6,400 m q} with f₀ = 0.73, q = 0.033 fits m ≤ 10⁻³ to 0.02 |
| RE 6 | crossing shifts right ×[1.5, 5] with F_P at M; chain top cooperative state prudent-open at 10³; XC ≥ 0.2 of π at 10⁴ | shift **held** (1.85 [1.07, 4.00]; 2.15 on the preregistered points); chain: **the 10³ clause failed** (top cooperative state XC′ at both N), the XC clause held (π(F_X) 0.32); falsifier not fired |
| S1 | P1 is a family tilt | islands per copy 0.246, universal-open 0.175, identity 0.12 held; **F_P-universal 0.175 > 0.15: number missed** (falsifier ≥ 0.3 not fired) |
| S2 | prudence pays at establishment (P1p vs P2n) | **held** (0.186 vs 0.119 per occupied seed island, ×1.56; islands 0.88 vs 0.75; identity islands 0.06 vs 0.10) |
| S3 | the advantage is mostly the cooperators (matched) | **held** (ratio 0.03) |
| S4 | RE 2 literal ill-conditioned (|P1 − P2| ≤ 0.10) | **held** (0.017) |
| S5 | identity removed: universal-open ≥ 0.7; F_P-universal ≤ 0.4; core-universal ≤ 0.3 | universal-open held (0.70, 0.775); **F_P-universal 0.475 and core-universal 0.725: numbers missed** (falsifier not fired). The prudent core holds every island in 29/40 runs without cliques |
| S6 | P5: EQ ≥ F_P; P5p: core > EQ | **held** (0.39 ≥ 0.30; 0.52 > 0.25) |
| S7 | XC ≤ 0.05 of islands in Part 1; XB seeded in 0.45–0.75 of runs | XC clause **held** (max 0.04); XB **number missed** in 2 of 13 cells (P4′ 0.875, P4p 0.80, where cooperator removal raises its mass) |
| S8 | largest-established set wins ≥ 0.9 of decided runs | **held** (117 / 118) |
| S9 | f(0) ∈ [0.65, 0.85], f(m_L) ≤ 0.15, f₀ ∈ [0.6, 0.9], q ∈ [0.02, 0.08], m* ∈ [8·10⁻⁴, 3·10⁻³] | **held** (0.75, 0.075, 0.73, 0.033, 1.26·10⁻³) |
| S10 | crossing in copies per run within 2.5× across the panel | **not determinable on the bracket**; mechanism partly contradicted: at equal copies the panel roughly matches the scan, but the 50% level is set by f₀(N, I), which ranges 0.475–0.825 (falsifier not demonstrable) |
| S11 | B ≥ A at every m ≥ 2·10⁻⁴; shift in [1.1, 2.5] | **held** (paired; 1.85) |
| S12 | chain: top XC; π(F_X) ∈ [0.2, 0.5]; π(core) ≤ 0.15; P(C,C) within 0.05 of the identity run | top state, π(F_X) 0.32 and P(C,C) (0.589 / 0.800) held; **π(core) 0.22 > 0.15: number missed**; twin-drift clause vacuous |

## 6. Reading

- **CBP is open to CB, so the question changed before any cell.** "Certified defection against plain C" reads the certificate-less constant, which every verifier refuses and every unconditional cooperator accepts. So prudence (refusing unconditional cooperators) and openness (cooperating with every S-guarded verifier) are compatible in one program, and CBP's frozen family is mostly nice carriers. The spec's literal cells test a family tilt, the added matched cells test prudence.
- **Prudence pays in the scramble, and it is the cooperators.** Within one compatible family, at equal mass on identical backgrounds, the prudent core establishes 1.56× as often per occupied seed island as the nice part (0.186 vs 0.119), keeps its islands (persistence 0.93 vs 0.82), holds more of them (0.88 vs 0.75), leaves fewer to identity cliques (0.06 vs 0.10) and is universal-open in 10/40 runs against 4/40. Removing the unconditional cooperators removes the establishment advantage (0.120 vs 0.118). The identity run's "the scramble rewards prudence" is now a matched measurement with its mechanism.
- **Openness is not the handicap; identity is.** Without identity cliques the prudent open core holds every island in 29/40 runs and the open family in 31/40. With identity cliques at L's mass even the best tilt (P1p) leaves identity islands on 6% of islands and universality at 10/40; head to head, the core beats ten EQ spellings on islands (0.52 vs 0.25) but no run is universal while identity holds 0.34.
- **The identity abundance threshold at (100, 64) is 8 seeded clique copies per run** (m* = 1.26·10⁻³ at 10,000, interval [6.6·10⁻⁴, 1.6·10⁻³]): the universal fraction falls as f₀ e^{−6,400 m q} with f₀ = 0.73 (clique-free runs universal) and q = 0.033 (the chance that a seeded clique copy leaves a persistent rival island). L sits at 57 copies, 7× past the crossing. At 2,000 the crossing is below the first scan point (f₀ only 0.6). The crossing is not a property of m: across (N, I) the clique-free baseline moves from 0.48 to 0.83; at (100, 128) there is no crossing; at N = 50 rivals resolve by majority and identity cliques sometimes take the whole metapopulation.
- **Doubling CBP's family moves the crossing right 1.85×**, by suppressing clique establishment (identity islands at L's mass 0.29 → 0.15), not by removing established cliques.
- **Chain (diagnostic):** the exclusive club still holds the top states at 10³ and 10⁴ (π 0.21 / 0.32); the prudent core is the second cooperative group (0.17 / 0.22); XB, the one CBP|XC bridge, is negligible (0.004).
- *Caveats:* certificates come from the frozen host tactic; every lottery number is finite-(N, I, horizon); stage statistics treat the identity group as one lineage per island; the chain runs on a reduced support with named omitted exits, and its recurrent set has no polymorphic state, so twin drift was not tested.
