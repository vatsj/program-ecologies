# Run: the realizable language, milestone 2: populations of carriers (2026-10-06)

Spec `specs/2026-10-06-carrier-populations.md`; notes `notes/carrier-populations.md`; predictions `predictions/2026-10-06-carrier-populations.md`; code `src/carrier_populations.py`, `src/carrier_populations_run.py`, `src/carrier_populations_report.py`, `tests/test_carrier_populations.py`; raw arrays in `runs/carrier_populations/` (npz not committed). K = 10⁶, V = K/4, PD payoffs of the modal arm, w = 0.3. "Classes" are the exact lumped classes over spellings (rows and columns against every spelling, self and cross-twin cells included).

## 1. Scale guard, costs, and the ideal-verification control

| arm | spellings | τ-types | classes (split singletons) | ideal pair checks (s) | executable class checks (s) | exec ≠ ideal cells | exec TO (all at V: regress) | ideal TO | largest non-TO exec check | median |
|---|---|---|---|---|---|---|---|---|---|---|
| P | 12546 | 4162 | 588 (54) | 3828352 (194) | 122744 (247) | 0 | 14064 | 172148 | 101644 | 21962 |
| O | 23790 | 7743 | 701 (54) | 7110047 (665) | 146537 (522) | 0 | 14689 | 243320 | 101644 | 20715 |
| E | 49666 | 16514 | 3115 (108) | 79937512 (3395) | 24702 (54) | 0 | 2120 | 4402024 | 214852 | 20409 |

Executable TO counts are smaller than ideal TO counts only because the executable table is computed on class representatives and the ideal one on every τ-type pair; on the class cells the two tables are identical, so the chain and lottery under the ideal table are the same computation (RE 7 / S11).

**K sensitivity (P, every class cell, sources and lists rebuilt at each K, V = K/4):**

| K | lists equal to K = 10⁶ | cells differing from K = 10⁶ | of which between establishers | checks at the cap | largest check below the cap |
|---|---|---|---|---|---|
| 300000 | 588 / 588 | 305 | 35 | 14395 | 74722 |
| 3.00e+06 | 588 / 588 | 0 | 0 | 13982 | 101644 |

**Validation (notes §1.10):** Lemma T / composition sample 2750 pairs, 0 mismatches; class-table sample 1600 cells, 0 mismatches; empty-selection shortcut 201 checks, 0 mismatches; n ≤ 5 chain: P(C,C) unlumped / lumped / twin-expanded 0.328200897 / 0.328200897 / 0.328200898 at N = 10³ and 0.599591006 / 0.599591006 / 0.599591007 at 10⁴.

## 2. Static structure

### Arm P

| prior | establishers | S-guarded est. | prudent est. (refuse Cc) | exploited est. | self-cooperators | unconditional C | all-D rows | D class | Cc class | sucker fringe |
|---|---|---|---|---|---|---|---|---|---|---|
| L | 0.061 | 0.011 | 0.009 | 0.047 | 0.490 | 0.354 | 0.376 | 0.097 | 0.090 | 0.110 |
| U | 0.172 | 0.024 | 0.058 | 0.128 | 0.502 | 0.065 | 0.065 | 0.002 | 0.002 | 0.262 |
| Lstd | 0.008 | 0.002 | 4.45e-04 | 0.006 | 0.498 | 0.482 | 0.485 | 0.451 | 0.449 | 0.015 |

Counts: 588 classes; establishers 101 (S-guarded 14, prudent 34, exploited 75); self-cooperators 295; unconditional cooperators 38; sucker fringe 154; compatible establisher pairs 2316 of 5050. Leak test: 295 self-cooperating classes in 11 components (largest [285, 1, 1]), **10 closed**: `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)`; `if(CHK(me,them,D),if(CHK(me,me,D),D,D),C)`; `if(CHK(me,me,D),D,if(CHK(me,them,D),D,C))`; `if(not(or(CHK(me,me,D),CHK(me,them,D))),C,D)`.

Heaviest establishers (L):

| class | mass L | mass L_std | S-guarded | prudent | exploited | run tree |
|---|---|---|---|---|---|---|
| `if(CHK(them,^C,D),D,C)` | 0.0098 | 0.0018 | False | False | True | `CHK(them,^C,D)?D:C` |
| `if(CHK(them,^D,D),D,C)` | 0.0098 | 0.0018 | False | False | True | `CHK(them,^D,D)?D:C` |
| `CB` | 0.0078 | 0.0017 | True | False | False | `CHK(them,me,C)?C:D` |
| `if(CHK(them,them,D),D,C)` | 0.0056 | 0.0016 | False | False | True | `CHK(them,them,D)?D:C` |
| `if(or(CHK(them,them,D),CHK(me,me,C)),D,C)` | 0.0018 | 8.01e-05 | False | False | True | `CHK(them,them,D)?D:CHK(me,me,C)?D:C` |
| `if(and(CHK(them,me,D),CHK(them,^C,D)),D,C)` | 0.0014 | 6.98e-05 | False | False | True | `CHK(them,me,D)?CHK(them,^C,D)?D:C:C` |
| `if(and(CHK(them,me,D),CHK(them,^D,D)),D,C)` | 0.0014 | 5.21e-05 | False | False | True | `CHK(them,me,D)?CHK(them,^D,D)?D:C:C` |
| `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)` | 0.0013 | 6.64e-05 | False | False | False | `CHK(them,me,C)?C:CHK(me,them,D)?C:D` |
| `if(or(CHK(them,me,C),CHK(me,^C,D)),C,D)` | 7.78e-04 | 3.66e-05 | False | False | False | `CHK(them,me,C)?C:CHK(me,^C,D)?C:D` |
| `if(or(CHK(them,them,D),CHK(me,^C,C)),D,C)` | 7.78e-04 | 3.66e-05 | False | False | True | `CHK(them,them,D)?D:CHK(me,^C,C)?D:C` |
| `if(or(CHK(them,them,D),CHK(me,^D,C)),D,C)` | 7.78e-04 | 3.66e-05 | False | False | True | `CHK(them,them,D)?D:CHK(me,^D,C)?D:C` |
| `if(and(CHK(me,^D,D),CHK(them,me,C)),C,D)` | 7.13e-04 | 2.69e-05 | True | False | False | `CHK(me,^D,D)?CHK(them,me,C)?C:D:D` |

Exploited establishers, heaviest (strict invaders: count, mass, examples):

- `if(CHK(them,^C,D),D,C)` (mass 0.0098): 98 strict invaders of mass 0.171, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(me,^C,D),C,D)`, `if(CHK(me,them,D),C,D)`
- `if(CHK(them,^D,D),D,C)` (mass 0.0098): 57 strict invaders of mass 0.080, e.g. `if(CHK(me,them,D),C,D)`, `if(CHK(them,me,D),D,D)`, `if(CHK(them,me,D),C,D)`
- `if(CHK(them,them,D),D,C)` (mass 0.0056): 234 strict invaders of mass 0.296, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(them,^C,D),D,D)`, `if(CHK(me,me,D),C,D)`
- `if(or(CHK(them,them,D),CHK(me,me,C)),D,C)` (mass 0.0018): 244 strict invaders of mass 0.291, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(them,^C,D),D,D)`, `if(CHK(me,me,D),C,D)`
- `if(and(CHK(them,me,D),CHK(them,^C,D)),D,C)` (mass 0.0014): 98 strict invaders of mass 0.171, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(me,^C,D),C,D)`, `if(CHK(me,them,D),C,D)`
- `if(and(CHK(them,me,D),CHK(them,^D,D)),D,C)` (mass 0.0014): 72 strict invaders of mass 0.126, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(me,them,D),C,D)`, `if(CHK(them,me,D),D,D)`

### Arm O

| prior | establishers | S-guarded est. | prudent est. (refuse Cc) | exploited est. | self-cooperators | unconditional C | all-D rows | D class | Cc class | sucker fringe |
|---|---|---|---|---|---|---|---|---|---|---|
| L | 0.063 | 0.005 | 0.009 | 0.056 | 0.495 | 0.360 | 0.371 | 0.048 | 0.045 | 0.111 |
| U | 0.164 | 0.020 | 0.057 | 0.127 | 0.478 | 0.054 | 0.054 | 0.001 | 0.001 | 0.258 |
| Lstd | 0.018 | 0.002 | 0.001 | 0.016 | 0.498 | 0.461 | 0.465 | 0.195 | 0.193 | 0.035 |

Counts: 701 classes; establishers 115 (S-guarded 14, prudent 40, exploited 89); self-cooperators 335; unconditional cooperators 38; sucker fringe 181; compatible establisher pairs 3233 of 6555. Leak test: 335 self-cooperating classes in 11 components (largest [325, 1, 1]), **10 closed**: `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)`; `if(CHK(me,them,D),if(CHK(me,me,D),D,D),C)`; `if(CHK(me,me,D),D,if(CHK(me,them,D),D,C))`; `if(not(or(CHK(me,me,D),CHK(me,them,D))),C,D)`.

Heaviest establishers (L):

| class | mass L | mass L_std | S-guarded | prudent | exploited | run tree |
|---|---|---|---|---|---|---|
| `if(CHK(them,^D,D),D,C)` | 0.0108 | 0.0040 | False | False | True | `CHK(them,^D,D)?D:C` |
| `if(CHK(them,^C,D),D,C)` | 0.0105 | 0.0040 | False | False | True | `CHK(them,^C,D)?D:C` |
| `if(CHK(them,me,D),D,C)[none]` | 0.0069 | 0.0021 | False | False | True | `CHK(them,me,D)?D:C` |
| `if(CHK(them,them,D),D,C)[none]` | 0.0059 | 0.0021 | False | False | True | `CHK(them,them,D)?D:C` |
| `CB` | 0.0039 | 0.0019 | True | False | False | `CHK(them,me,C)?C:D` |
| `if(CHK(them,them,D),D,C)` | 0.0028 | 0.0017 | False | False | True | `CHK(them,them,D)?D:C` |
| `if(and(CHK(them,me,D),CHK(them,^C,D)),D,C)` | 0.0016 | 1.82e-04 | False | False | True | `CHK(them,me,D)?CHK(them,^C,D)?D:C:C` |
| `if(or(CHK(them,them,D),CHK(me,me,C)),D,C)` | 9.08e-04 | 9.75e-05 | False | False | True | `CHK(them,them,D)?D:CHK(me,me,C)?D:C` |
| `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)` | 6.48e-04 | 8.03e-05 | False | False | False | `CHK(them,me,C)?C:CHK(me,them,D)?C:D` |
| `if(CHK(them,me,C),C,if(CHK(them,them,D),D,C))[none]` | 5.84e-04 | 3.86e-05 | False | False | True | `CHK(them,me,C)?C:CHK(them,them,D)?D:C` |
| `if(CHK(them,me,C),C,if(CHK(them,^D,D),D,C))[none]` | 5.84e-04 | 3.86e-05 | False | False | True | `CHK(them,me,C)?C:CHK(them,^D,D)?D:C` |
| `if(or(CHK(them,me,C),CHK(them,them,D)),D,C)` | 5.19e-04 | 7.18e-05 | False | True | True | `CHK(them,me,C)?D:CHK(them,them,D)?D:C` |

Exploited establishers, heaviest (strict invaders: count, mass, examples):

- `if(CHK(them,^D,D),D,C)` (mass 0.0108): 130 strict invaders of mass 0.290, e.g. `D[none]`, `if(CHK(them,me,D),D,D)`, `if(CHK(them,me,D),C,D)[none]`
- `if(CHK(them,^C,D),D,C)` (mass 0.0105): 171 strict invaders of mass 0.335, e.g. `D[none]`, `if(CHK(me,^D,D),D,C)`, `if(CHK(me,^C,D),C,D)`
- `if(CHK(them,me,D),D,C)[none]` (mass 0.0069): 145 strict invaders of mass 0.313, e.g. `D[none]`, `if(CHK(me,^D,D),D,C)`, `if(CHK(them,me,D),D,D)`
- `if(CHK(them,them,D),D,C)[none]` (mass 0.0059): 311 strict invaders of mass 0.387, e.g. `D[none]`, `if(CHK(me,^D,D),D,C)`, `if(CHK(them,^C,D),D,D)`
- `if(CHK(them,them,D),D,C)` (mass 0.0028): 290 strict invaders of mass 0.398, e.g. `D[none]`, `if(CHK(me,^D,D),D,C)`, `if(CHK(them,^C,D),D,D)`
- `if(and(CHK(them,me,D),CHK(them,^C,D)),D,C)` (mass 0.0016): 171 strict invaders of mass 0.335, e.g. `D[none]`, `if(CHK(me,^D,D),D,C)`, `if(CHK(me,^C,D),C,D)`

### Arm E

| prior | establishers | S-guarded est. | prudent est. (refuse Cc) | exploited est. | self-cooperators | unconditional C | all-D rows | D class | Cc class | sucker fringe |
|---|---|---|---|---|---|---|---|---|---|---|
| L | 0.061 | 0.010 | 0.009 | 0.048 | 0.489 | 0.350 | 0.374 | 0.072 | 0.065 | 0.111 |
| U | 0.144 | 0.029 | 0.042 | 0.102 | 0.531 | 0.116 | 0.096 | 3.21e-04 | 3.21e-04 | 0.271 |
| Lstd | 0.009 | 0.002 | 6.51e-04 | 0.007 | 0.498 | 0.478 | 0.482 | 0.438 | 0.436 | 0.018 |
| Leq | 0.061 | 0.010 | 0.009 | 0.048 | 0.488 | 0.351 | 0.375 | 0.075 | 0.068 | 0.111 |

Counts: 3115 classes; establishers 448 (S-guarded 90, prudent 132, exploited 318); self-cooperators 1653; unconditional cooperators 361; sucker fringe 845; compatible establisher pairs 48612 of 100128. Leak test: 1653 self-cooperating classes in 21 components (largest [1633, 1, 1]), **20 closed**: `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)`; `if(CHK(me,them,D),if(CHK(me,me,D),D,D),C)`; `if(CHK(me,me,D),D,if(CHK(me,them,D),D,C))`; `if(not(or(CHK(me,me,D),CHK(me,them,D))),C,D)`.

Heaviest establishers (L):

| class | mass L | mass L_std | S-guarded | prudent | exploited | run tree |
|---|---|---|---|---|---|---|
| `if(CHK(them,^C,D),D,C)` | 0.0064 | 0.0015 | False | False | True | `CHK(them,^C,D)?D:C` |
| `if(CHK(them,^D,D),D,C)` | 0.0064 | 0.0015 | False | False | True | `CHK(them,^D,D)?D:C` |
| `CB` | 0.0040 | 0.0014 | True | False | False | `CHK(them,me,C)?C:D` |
| `if(CHK(them,them,D),D,C)` | 0.0037 | 0.0013 | False | False | True | `CHK(them,them,D)?D:C` |
| `if(CHK_5(them,^C,D),D,C)` | 0.0031 | 4.72e-04 | False | False | True | `CHK_5(them,^C,D)?D:C` |
| `if(CHK_5(them,^D,D),D,C)` | 0.0031 | 4.72e-04 | False | False | True | `CHK_5(them,^D,D)?D:C` |
| `if(CHK_5(them,me,C),C,D)` | 0.0020 | 3.87e-04 | True | False | False | `CHK_5(them,me,C)?C:D` |
| `if(CHK_5(them,them,D),D,C)` | 0.0019 | 3.86e-04 | False | False | True | `CHK_5(them,them,D)?D:C` |
| `if(or(CHK(them,them,D),CHK(me,me,D)),D,C)` | 4.73e-04 | 3.60e-05 | False | False | True | `CHK(them,them,D)?D:CHK(me,me,D)?D:C` |
| `if(CHK(me,them,D),C,if(CHK(them,me,D),D,C))` | 3.84e-04 | 1.56e-05 | False | False | True | `CHK(me,them,D)?C:CHK(them,me,D)?D:C` |
| `if(or(CHK(them,me,C),CHK(me,^C,D)),C,D)` | 3.55e-04 | 3.12e-05 | False | False | False | `CHK(them,me,C)?C:CHK(me,^C,D)?C:D` |
| `if(or(CHK(them,them,D),CHK(me,me,C)),D,C)` | 3.55e-04 | 3.12e-05 | False | False | True | `CHK(them,them,D)?D:CHK(me,me,C)?D:C` |

Exploited establishers, heaviest (strict invaders: count, mass, examples):

- `if(CHK(them,^C,D),D,C)` (mass 0.0064): 395 strict invaders of mass 0.136, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(me,^C,D),C,D)`, `if(CHK(me,them,D),C,D)`
- `if(CHK(them,^D,D),D,C)` (mass 0.0064): 319 strict invaders of mass 0.086, e.g. `if(CHK(me,them,D),C,D)`, `if(CHK_5(me,^D,D),D,C)`, `if(CHK(them,me,D),D,D)`
- `if(CHK(them,them,D),D,C)` (mass 0.0037): 1222 strict invaders of mass 0.275, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(me,me,D),C,D)`, `if(CHK(me,them,D),C,D)`
- `if(CHK_5(them,^C,D),D,C)` (mass 0.0031): 398 strict invaders of mass 0.116, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(me,them,D),D,C)`, `if(CHK_5(me,^D,D),D,C)`
- `if(CHK_5(them,^D,D),D,C)` (mass 0.0031): 322 strict invaders of mass 0.088, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(me,them,D),D,C)`, `if(CHK_5(them,me,D),D,D)`
- `if(CHK_5(them,them,D),D,C)` (mass 0.0019): 1220 strict invaders of mass 0.263, e.g. `if(CHK(me,^D,D),D,C)`, `if(CHK(me,them,D),D,C)`, `if(CHK_5(me,^D,D),D,C)`

**Bridges (E):** 2346 classes cooperate mutually with an entry-0 establisher and an entry-5 establisher (mass L 0.5805); 428 of them are establishers (mass 0.0604), 361 unconditional cooperators. Establisher mass by entry: entry 0 0.0340, entry 5 0.0135.

- `if(CHK(them,^C,D),D,C)` mass 0.0064, S-guarded False, strict invaders 395
- `if(CHK(them,^D,D),D,C)` mass 0.0064, S-guarded False, strict invaders 319
- `CB` mass 0.0040, S-guarded True, strict invaders 0
- `if(CHK(them,them,D),D,C)` mass 0.0037, S-guarded False, strict invaders 1222
- `if(CHK_5(them,^C,D),D,C)` mass 0.0031, S-guarded False, strict invaders 398
- `if(CHK_5(them,^D,D),D,C)` mass 0.0031, S-guarded False, strict invaders 322
- `if(CHK_5(them,me,C),C,D)` mass 0.0020, S-guarded True, strict invaders 0
- `if(CHK_5(them,them,D),D,C)` mass 0.0019, S-guarded False, strict invaders 1220

## 3. The ε→0 chain

| arm | prior | label | twins | N | P(C,C) | π(all-D) | π(coop states) | top cooperative state (π) | its exit per event: total / neutral / strict | entry from all-D (coop share) | states | cut/flow |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E | L | main | yes | 1000 | 1.0000 | 2.84e-32 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1435) | 1.34e-36 / 0 / 0 | 0.0012 (0.686) | 3115 | 0.0039 |
| E | L | main | yes | 10000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1436) | 0 / 0 / 0 | 3.03e-04 (0.875) | 3115 | – |
| E | Leq | main | yes | 1000 | 1.0000 | 3.27e-32 | 1.0000 | `if(or(CHK_5(me,me,D),CHK_5(me,them,D)),D,C):1.000` (0.0909) | 1.32e-36 / 0 / 0 | 0.0012 (0.687) | 3115 | 0.0038 |
| E | Leq | main | yes | 10000 | 1.0000 | 0 | 1.0000 | `if(or(CHK_5(me,me,D),CHK_5(me,them,D)),D,C):1.000` (0.0909) | 0 / 0 / 0 | 3.01e-04 (0.875) | 3115 | – |
| O | L | main | yes | 1000 | 1.0000 | 2.76e-32 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 1.38e-36 / 0 / 0 | 0.0012 (0.684) | 701 | 0.0059 |
| O | L | main | yes | 10000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 0 / 0 / 0 | 3.12e-04 (0.873) | 701 | – |
| O | L | main | yes | 30000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 0 / 0 / 0 | 1.71e-04 (0.923) | 701 | – |
| O | L | main | yes | 100000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 0 / 0 / 0 | 9.03e-05 (0.956) | 701 | – |
| P | L | main | yes | 1000 | 1.0000 | 2.44e-32 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 1.37e-36 / 0 / 0 | 0.0012 (0.702) | 588 | 0.0049 |
| P | L | main | yes | 10000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 0 / 0 / 0 | 3.01e-04 (0.883) | 588 | – |
| P | L | main | yes | 30000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 0 / 0 / 0 | 1.66e-04 (0.929) | 588 | – |
| P | L | main | yes | 100000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 0 / 0 / 0 | 8.79e-05 (0.960) | 588 | – |
| P | L | main | no | 1000 | 1.0000 | 2.44e-32 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 1.37e-36 / 0 / 0 | 0.0012 (0.702) | 588 | 0.0049 |
| P | L | main | no | 10000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 0 / 0 / 0 | 3.01e-04 (0.883) | 588 | – |
| P | L | main | no | 30000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 0 / 0 / 0 | 1.66e-04 (0.929) | 588 | – |
| P | L | main | no | 100000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.1818) | 0 / 0 / 0 | 8.79e-05 (0.960) | 588 | – |
| P | Lstd | main | yes | 1000 | 1.0000 | 3.78e-31 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.4246) | 1.73e-37 / 0 / 0 | 1.53e-04 (0.720) | 588 | 3.21e-04 |
| P | Lstd | main | yes | 10000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.4246) | 0 / 0 / 0 | 3.94e-05 (0.891) | 588 | – |
| P | Lstd | main | yes | 30000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.4246) | 0 / 0 / 0 | 2.17e-05 (0.934) | 588 | – |
| P | Lstd | main | yes | 100000 | 1.0000 | 0 | 1.0000 | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` (0.4246) | 0 / 0 / 0 | 1.16e-05 (0.963) | 588 | – |
| P | U | main | yes | 1000 | 1.0000 | 1.07e-34 | 1.0000 | `if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000` (0.1000) | 4.32e-36 / 0 / 0 | 0.0027 (0.872) | 588 | 0.1072 |
| P | U | main | yes | 10000 | 1.0000 | 0 | 1.0000 | `if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000` (0.1000) | 0 / 0 / 0 | 7.82e-04 (0.956) | 588 | – |
| P | U | main | yes | 30000 | 1.0000 | 0 | 1.0000 | `if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000` (0.1000) | 0 / 0 / 0 | 4.44e-04 (0.974) | 588 | – |
| P | U | main | yes | 100000 | 1.0000 | 0 | 1.0000 | `if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000` (0.1000) | 0 / 0 / 0 | 2.40e-04 (0.986) | 588 | – |
| O | L | noclosed | yes | 10000 | 0.7564 | 0.0241 | 0.7564 | `CB:1.000` (0.2413) | 1.88e-05 / 1.88e-05 / 0 | 3.10e-04 (0.873) | 705 | 0.0037 |
| O | L | noclosed | yes | 100000 | 0.9070 | 0.0086 | 0.9070 | `CB:1.000` (0.2901) | 1.88e-06 / 1.88e-06 / 0 | 8.99e-05 (0.956) | 691 | 0.0081 |
| P | L | noclosed | yes | 1000 | 0.5034 | 0.0993 | 0.5033 | `CB:1.000` (0.1521) | 3.76e-04 / 3.76e-04 / 0 | 0.0012 (0.699) | 686 | 0.0018 |
| P | L | noclosed | yes | 10000 | 0.7582 | 0.0441 | 0.7582 | `CB:1.000` (0.2347) | 3.76e-05 / 3.76e-05 / 0 | 2.99e-04 (0.881) | 593 | 0.0036 |
| P | L | noclosed | yes | 30000 | 0.8442 | 0.0277 | 0.8442 | `CB:1.000` (0.2620) | 1.25e-05 / 1.25e-05 / 0 | 1.64e-04 (0.928) | 580 | 0.0058 |
| P | L | noclosed | yes | 100000 | 0.9081 | 0.0160 | 0.9081 | `CB:1.000` (0.2822) | 3.76e-06 / 3.76e-06 / 0 | 8.70e-05 (0.959) | 578 | 0.0086 |
| P | Lstd | noclosed | yes | 10000 | 0.4162 | 0.4344 | 0.4162 | `CB:1.000` (0.0924) | 4.84e-05 / 4.84e-05 / 0 | 3.93e-05 (0.891) | 578 | 2.96e-04 |
| P | Lstd | noclosed | yes | 100000 | 0.6905 | 0.1955 | 0.6905 | `CB:1.000` (0.1552) | 4.84e-06 / 4.84e-06 / 0 | 1.15e-05 (0.963) | 578 | 3.45e-04 |
| P | U | noclosed | yes | 100000 | 0.9837 | 4.11e-04 | 0.9837 | `if(and(CHK(them,^C,D),CHK(them,me,C)),C,D):1.000` (0.1362) | 1.00e-06 / 1.00e-06 / 0 | 2.21e-04 (0.984) | 620 | 0.1086 |

**Cells with unexplored flow above 2% and their cut diagnostic** (share of the dropped flow by destination and source):

- P × U, main, N = 1000: cut/flow 0.1072 (absolute dropped flow 1.28e-35 per event): dst_poly_noncoop 1.000, n_destinations 4250, src_noncoop 1.000
- P × U, noclosed, N = 100000: cut/flow 0.1086 (absolute dropped flow 3.70e-06 per event): dst_poly_noncoop 1.000, n_destinations 4370, src_noncoop 1.000

**Support and transitions, P × L, main, N = 10⁴:**

- `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` π 0.1818, P(C,C) 1.00, log10 exit -329.5: → if(CHK(them,^D,D),D,C):1.000 (10^-330.2; if(CHK(them,^D,D),D,C)); → if(CHK(them,^C,D),D,C):1.000 (10^-330.2; if(CHK(them,^C,D),D,C)); → CB:1.000 (10^-330.3; CB)
- `if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000` π 0.0909, P(C,C) 1.00, log10 exit -329.5: → if(CHK(them,^C,D),D,C):1.000 (10^-330.2; if(CHK(them,^C,D),D,C)); → if(CHK(them,^D,D),D,C):1.000 (10^-330.2; if(CHK(them,^D,D),D,C)); → CB:1.000 (10^-330.3; CB)
- `if(CHK(me,them,D),if(CHK(me,me,D),D,D),C):1.000` π 0.0909, P(C,C) 1.00, log10 exit -329.5: → if(CHK(them,^D,D),D,C):1.000 (10^-330.2; if(CHK(them,^D,D),D,C)); → if(CHK(them,^C,D),D,C):1.000 (10^-330.2; if(CHK(them,^C,D),D,C)); → CB:1.000 (10^-330.3; CB)
- `if(CHK(me,me,D),D,if(CHK(me,them,D),D,C)):1.000` π 0.0909, P(C,C) 1.00, log10 exit -329.5: → if(CHK(them,^D,D),D,C):1.000 (10^-330.2; if(CHK(them,^D,D),D,C)); → if(CHK(them,^C,D),D,C):1.000 (10^-330.2; if(CHK(them,^C,D),D,C)); → CB:1.000 (10^-330.3; CB)
- `if(not(or(CHK(me,me,D),CHK(me,them,D))),C,D):1.000` π 0.0909, P(C,C) 1.00, log10 exit -329.5: → if(CHK(them,^D,D),D,C):1.000 (10^-330.2; if(CHK(them,^D,D),D,C)); → if(CHK(them,^C,D),D,C):1.000 (10^-330.2; if(CHK(them,^C,D),D,C)); → CB:1.000 (10^-330.3; CB)
- `if(CHK(me,me,D),C,if(CHK(me,them,D),D,C)):1.000` π 0.0909, P(C,C) 1.00, log10 exit -329.5: → if(CHK(them,^D,D),D,C):1.000 (10^-330.2; if(CHK(them,^D,D),D,C)); → if(CHK(them,^C,D),D,C):1.000 (10^-330.2; if(CHK(them,^C,D),D,C)); → CB:1.000 (10^-330.3; CB)
- decisive exits of the top cooperative state: `Dc` deleterious (Δ1 -1.00, Δ2 0, ρ 0, N·ρ –, N·Δ1 -10000.0); `Cc` deleterious (Δ1 -2.00, Δ2 -1.00, ρ 0, N·ρ –, N·Δ1 -20000.0); `if(CHK(me,^D,D),D,C)` deleterious (Δ1 -1.00, Δ2 0, ρ 0, N·ρ –, N·Δ1 -10000.0); `if(CHK(them,^C,D),D,D)` deleterious (Δ1 -1.00, Δ2 0, ρ 0, N·ρ –, N·Δ1 -10000.0)
- entry from all-D: `if(CHK(them,^C,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,^D,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `CB` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,them,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51)

**Support and transitions, P × U, main, N = 10⁴:**

- `if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000` π 0.1000, P(C,C) 1.00, log10 exit -329.0: → if(CHK(them,me,D),if(CHK(them,them,D),D,D),C):1.00 (10^-331.0; if(CHK(them,me,D),if(CHK(them,them,D),D,D),C)); → if(or(CHK(them,them,C),CHK(them,^C,D)),D,C):1.000 (10^-331.0; if(or(CHK(them,them,C),CHK(them,^C,D)),D,C)); → if(CHK(me,me,D),D,if(CHK(me,them,D),D,C)):1.000 (10^-331.0; if(CHK(me,me,D),D,if(CHK(me,them,D),D,C)))
- `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` π 0.1000, P(C,C) 1.00, log10 exit -329.0: → if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000 (10^-331.0; if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D)); → if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C)); → if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D))
- `if(CHK(me,them,D),if(CHK(me,me,D),D,D),C):1.000` π 0.1000, P(C,C) 1.00, log10 exit -329.0: → if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000 (10^-331.0; if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D)); → if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C)); → if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D))
- `if(CHK(me,me,D),D,if(CHK(me,them,D),D,C)):1.000` π 0.1000, P(C,C) 1.00, log10 exit -329.0: → if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000 (10^-331.0; if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D)); → if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C)); → if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D))
- `if(not(or(CHK(me,me,D),CHK(me,them,D))),C,D):1.000` π 0.1000, P(C,C) 1.00, log10 exit -329.0: → if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000 (10^-331.0; if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D)); → if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C)); → if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D))
- `if(CHK(me,me,D),C,if(CHK(me,them,D),D,C)):1.000` π 0.1000, P(C,C) 1.00, log10 exit -329.0: → if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000 (10^-331.0; if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D)); → if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,C),C,D),C)); → if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D):1.000 (10^-331.0; if(CHK(them,^D,D),if(CHK(them,me,D),D,C),D))
- decisive exits of the top cooperative state: `Dc` deleterious (Δ1 -1.00, Δ2 0, ρ 0, N·ρ –, N·Δ1 -10000.0); `Cc` deleterious (Δ1 -2.00, Δ2 -1.00, ρ 0, N·ρ –, N·Δ1 -20000.0); `if(CHK(me,^D,D),D,C)` deleterious (Δ1 -1.00, Δ2 0, ρ 0, N·ρ –, N·Δ1 -10000.0); `if(CHK(them,^C,D),D,D)` deleterious (Δ1 -1.00, Δ2 0, ρ 0, N·ρ –, N·Δ1 -10000.0)
- entry from all-D: `if(CHK(them,^C,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,^D,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `CB` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,them,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51)

**Support and transitions, P × Lstd, main, N = 10⁴:**

- `if(or(CHK(me,me,D),CHK(me,them,D)),D,C):1.000` π 0.4246, P(C,C) 1.00, log10 exit -330.4: → if(CHK(them,^D,D),D,C):1.000 (10^-331.0; if(CHK(them,^D,D),D,C)); → if(CHK(them,^C,D),D,C):1.000 (10^-331.0; if(CHK(them,^C,D),D,C)); → CB:1.000 (10^-331.0; CB)
- `if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D):1.000` π 0.0639, P(C,C) 1.00, log10 exit -330.4: → if(CHK(them,^D,D),D,C):1.000 (10^-331.0; if(CHK(them,^D,D),D,C)); → if(CHK(them,^C,D),D,C):1.000 (10^-331.0; if(CHK(them,^C,D),D,C)); → CB:1.000 (10^-331.0; CB)
- `if(CHK(me,them,D),if(CHK(me,me,D),D,D),C):1.000` π 0.0639, P(C,C) 1.00, log10 exit -330.4: → if(CHK(them,^C,D),D,C):1.000 (10^-331.0; if(CHK(them,^C,D),D,C)); → if(CHK(them,^D,D),D,C):1.000 (10^-331.0; if(CHK(them,^D,D),D,C)); → CB:1.000 (10^-331.0; CB)
- `if(CHK(me,me,D),D,if(CHK(me,them,D),D,C)):1.000` π 0.0639, P(C,C) 1.00, log10 exit -330.4: → if(CHK(them,^C,D),D,C):1.000 (10^-331.0; if(CHK(them,^C,D),D,C)); → if(CHK(them,^D,D),D,C):1.000 (10^-331.0; if(CHK(them,^D,D),D,C)); → CB:1.000 (10^-331.0; CB)
- `if(not(or(CHK(me,me,D),CHK(me,them,D))),C,D):1.000` π 0.0639, P(C,C) 1.00, log10 exit -330.4: → if(CHK(them,^C,D),D,C):1.000 (10^-331.0; if(CHK(them,^C,D),D,C)); → if(CHK(them,^D,D),D,C):1.000 (10^-331.0; if(CHK(them,^D,D),D,C)); → CB:1.000 (10^-331.0; CB)
- `if(CHK(me,me,D),C,if(CHK(me,them,D),D,C)):1.000` π 0.0639, P(C,C) 1.00, log10 exit -330.4: → if(CHK(them,^C,D),D,C):1.000 (10^-331.0; if(CHK(them,^C,D),D,C)); → if(CHK(them,^D,D),D,C):1.000 (10^-331.0; if(CHK(them,^D,D),D,C)); → CB:1.000 (10^-331.0; CB)
- decisive exits of the top cooperative state: `Dc` deleterious (Δ1 -1.00, Δ2 0, ρ 0, N·ρ –, N·Δ1 -10000.0); `Cc` deleterious (Δ1 -2.00, Δ2 -1.00, ρ 0, N·ρ –, N·Δ1 -20000.0); `if(CHK(me,^D,D),D,C)` deleterious (Δ1 -1.00, Δ2 0, ρ 0, N·ρ –, N·Δ1 -10000.0); `if(CHK(them,^C,D),D,D)` deleterious (Δ1 -1.00, Δ2 0, ρ 0, N·ρ –, N·Δ1 -10000.0)
- entry from all-D: `if(CHK(them,^C,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,^D,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `CB` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,them,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51)

**Support and transitions, P × L, noclosed, N = 10⁴:**

- `CB:1.000` π 0.2347, P(C,C) 1.00, log10 exit -4.4: → Cc:1.000 (10^-5.0; Cc); → if(CHK(them,^C,C),C,C):1.000 (10^-5.5; if(CHK(them,^C,C),C,C)); → if(CHK(me,^C,C),C,C):1.000 (10^-5.6; if(CHK(me,^C,C),C,C))
- `if(and(CHK(them,^C,D),CHK(them,me,C)),C,D):1.000` π 0.0918, P(C,C) 1.00, log10 exit -5.5: → CB:1.000 (10^-6.1; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.2; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.2; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,me,C),CHK(them,^C,D)),C,D):1.000` π 0.0902, P(C,C) 1.00, log10 exit -5.5: → CB:1.000 (10^-6.1; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.2; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.2; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,^D,D),CHK(them,me,C)),C,D):1.000` π 0.0803, P(C,C) 1.00, log10 exit -5.4: → CB:1.000 (10^-6.1; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.2; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.2; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,me,C),CHK(them,^D,D)),C,D):1.000` π 0.0789, P(C,C) 1.00, log10 exit -5.4: → CB:1.000 (10^-6.1; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.2; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.2; if(CHK(them,^D,D),C,D))
- `if(or(CHK(them,me,C),CHK(me,them,D)),C,D):1.000` π 0.0557, P(C,C) 1.00, log10 exit -4.5: → Cc:1.000 (10^-5.0; Cc); → if(CHK(them,^C,C),C,C):1.000 (10^-5.5; if(CHK(them,^C,C),C,C)); → if(CHK(me,^C,C),C,C):1.000 (10^-5.6; if(CHK(me,^C,C),C,C))
- decisive exits of the top cooperative state: `Cc` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0); `if(CHK(them,^C,C),C,C)` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0); `if(CHK(me,^C,C),C,C)` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0); `if(CHK(me,^D,C),C,C)` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0)
- entry from all-D: `if(CHK(them,^C,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,^D,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `CB` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,them,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51)

**Support and transitions, P × Lstd, noclosed, N = 10⁴:**

- `Dc:1.000` π 0.4344, P(C,C) 0, log10 exit -4.4: → if(CHK(them,^C,D),D,C):1.000 (10^-5.1; if(CHK(them,^C,D),D,C)); → if(CHK(them,^D,D),D,C):1.000 (10^-5.1; if(CHK(them,^D,D),D,C)); → CB:1.000 (10^-5.1; CB)
- `CB:1.000` π 0.0924, P(C,C) 1.00, log10 exit -4.3: → Cc:1.000 (10^-4.3; Cc); → if(CHK(them,^C,C),C,C):1.000 (10^-6.4; if(CHK(them,^C,C),C,C)); → if(CHK(me,^C,C),C,C):1.000 (10^-6.4; if(CHK(me,^C,C),C,C))
- `if(and(CHK(them,^C,D),CHK(them,me,C)),C,D):1.000` π 0.0721, P(C,C) 1.00, log10 exit -6.3: → CB:1.000 (10^-6.8; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.8; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.8; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,me,C),CHK(them,^C,D)),C,D):1.000` π 0.0718, P(C,C) 1.00, log10 exit -6.3: → CB:1.000 (10^-6.8; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.8; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.8; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,^D,D),CHK(them,me,C)),C,D):1.000` π 0.0694, P(C,C) 1.00, log10 exit -6.2: → CB:1.000 (10^-6.8; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.8; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.8; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,me,C),CHK(them,^D,D)),C,D):1.000` π 0.0691, P(C,C) 1.00, log10 exit -6.2: → CB:1.000 (10^-6.8; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.8; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.8; if(CHK(them,^D,D),C,D))
- decisive exits of the top cooperative state: `Cc` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0); `if(CHK(them,^C,C),C,C)` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0); `if(CHK(me,^C,C),C,C)` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0); `if(CHK(me,^D,C),C,C)` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0)
- entry from all-D: `if(CHK(them,^C,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,^D,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `CB` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,them,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51)

**Support and transitions, O × L, noclosed, N = 10⁴:**

- `CB:1.000` π 0.2413, P(C,C) 1.00, log10 exit -4.7: → Cc:1.000 (10^-5.3; Cc); → if(CHK(them,^C,C),C,C):1.000 (10^-5.8; if(CHK(them,^C,C),C,C)); → if(CHK(me,^C,C),C,C):1.000 (10^-5.9; if(CHK(me,^C,C),C,C))
- `D[none]:1.000` π 0.1426, P(C,C) 0, log10 exit -3.9: → CB:1.000 (10^-4.8; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-4.8; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-4.8; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,^C,D),CHK(them,me,C)),C,D):1.000` π 0.0910, P(C,C) 1.00, log10 exit -5.8: → CB:1.000 (10^-6.4; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.5; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.5; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,me,C),CHK(them,^C,D)),C,D):1.000` π 0.0900, P(C,C) 1.00, log10 exit -5.8: → CB:1.000 (10^-6.4; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.5; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.5; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,^D,D),CHK(them,me,C)),C,D):1.000` π 0.0795, P(C,C) 1.00, log10 exit -5.7: → CB:1.000 (10^-6.4; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.5; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.5; if(CHK(them,^D,D),C,D))
- `if(and(CHK(them,me,C),CHK(them,^D,D)),C,D):1.000` π 0.0787, P(C,C) 1.00, log10 exit -5.7: → CB:1.000 (10^-6.4; CB); → if(CHK(them,^C,D),C,D):1.000 (10^-6.5; if(CHK(them,^C,D),C,D)); → if(CHK(them,^D,D),C,D):1.000 (10^-6.5; if(CHK(them,^D,D),C,D))
- decisive exits of the top cooperative state: `Cc` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0); `if(CHK(them,^C,C),C,C)` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0); `if(CHK(me,^C,C),C,C)` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0); `if(CHK(me,^D,C),C,C)` neutral (Δ1 0, Δ2 0, ρ 1.00e-04, N·ρ 1.00, N·Δ1 0)
- entry from all-D: `if(CHK(them,^D,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,^C,D),D,C)` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,me,D),D,C)[none]` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51); `if(CHK(them,them,D),D,C)[none]` (Δ1 0, Δ2 1.00, ρ 0.0044, N·ρ 43.51)

**Local slopes** of log(π(coop)/π(all-D)) and of log(P(C,C)/(1 − P(C,C))) in log N:

| arm | prior | label | 10³→10⁴ | 10⁴→3·10⁴ | 3·10⁴→10⁵ |
|---|---|---|---|---|---|
| E | L | main | – / – |
| E | Leq | main | – / – |
| O | L | main | – / – | – / – | – / – |
| O | L | noclosed | 0.52 / 0.50 |
| P | L | main | – / – | – / – | – / – |
| P | L | noclosed | 0.53 / 0.49 | 0.52 / 0.50 | 0.51 / 0.50 |
| P | Lstd | main | – / – | – / – | – / – |
| P | Lstd | noclosed | 0.57 / 0.50 |
| P | U | main | – / – | – / – | – / – |
| P | U | noclosed |  |

## 4. The ε = 0 lottery ((N, I) = (100, 64), mN = 1, horizon 2,000 generations)

| arm | prior | runs | E1 success / fail / censored [Wilson] | E2 | E3 success / fail / censored [Wilson] | median decision gen (E3) | first island at P(C,C) ≥ 0.9: median gen, by 100 | final P(C,C) | E3 winners (top class) |
|---|---|---|---|---|---|---|---|---|---|
| E | L | 40 | 2 / 0 / 38 [0.01, 0.17] | 2 / 0 / 38 [0.01, 0.17] | 40 / 0 / 0 [0.91, 1.00] | 270 | 30, 40 | 0.978 | `CB` 13, `if(or(CHK(me,them,D),CHK(them,me,C)),C,D)` 3, `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)` 2 |
| E | Leq | 40 | 5 / 0 / 35 [0.05, 0.26] | 5 / 0 / 35 [0.05, 0.26] | 40 / 0 / 0 [0.91, 1.00] | 280 | 30, 40 | 0.977 | `CB` 9, `if(CHK_5(them,me,C),C,D)` 3, `if(CHK_5(them,me,C),if(CHK_5(them,^D,C),D,C),` 2 |
| O | L | 40 | 15 / 0 / 25 [0.24, 0.53] | 15 / 0 / 25 [0.24, 0.53] | 38 / 2 / 0 [0.83, 0.99] | 270 | 30, 40 | 0.947 | `CB` 27, `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)` 4, `if(and(CHK(me,^D,D),CHK(them,me,C)),C,D)` 2 |
| P | L | 40 | 8 / 0 / 32 [0.10, 0.35] | 8 / 0 / 32 [0.10, 0.35] | 40 / 0 / 0 [0.91, 1.00] | 250 | 30, 40 | 0.994 | `CB` 26, `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)` 4, `if(CHK(them,^C,C),D,if(CHK(them,me,C),C,D))` 2 |
| P | Lstd | 40 | 17 / 6 / 17 [0.29, 0.58] | 17 / 6 / 17 [0.29, 0.58] | 23 / 17 / 0 [0.42, 0.71] | 310 | 40, 33 | 0.573 | `CB` 15, `if(CHK(them,^D,D),D,C)` 2, `if(and(CHK(them,me,C),CHK(them,^C,D)),C,D)` 2 |
| P | U | 40 | 0 / 0 / 40 [0.00, 0.09] | 0 / 0 / 40 [0.00, 0.09] | 40 / 0 / 0 [0.91, 1.00] | 190 | 20, 40 | 0.960 | `if(CHK(them,them,D),D,if(CHK(them,me,C),C,D))` 7, `if(and(CHK(them,^D,D),CHK(them,me,C)),C,D)` 5, `if(CHK(them,me,C),C,if(CHK(them,them,D),D,D))` 4 |

E arm: both entries' establishers alive at the end in 20 / 40 runs (ever both alive: 40); an establisher bridge alive at the end in 27; merges (one entry's last establisher lost after both were present): 20, at generations [50, 100, 550, 70, 70, 20, 40, 30, 60, 30, 800, 50, 50, 910, 70, 200, 40, 50, 60, 70].

E arm: both entries' establishers alive at the end in 16 / 40 runs (ever both alive: 40); an establisher bridge alive at the end in 29; merges (one entry's last establisher lost after both were present): 24, at generations [40, 50, 1260, 60, 460, 90, 150, 110, 90, 50, 110, 60, 70, 40, 1240, 100, 130, 1630, 30, 50].

## 5. The twin clique (the chain's absorbing states)

The leak test's closed components at n = 7 are exactly ten singleton classes (P and O; twenty in E, ten per entry):
the two run trees `CHK(me,me,D)?D:CHK(me,them,D)?D:C` and `CHK(me,them,D)?CHK(me,me,D)?C:D:C` in their 10 spellings
of 6–7 nodes (mass 7.1·10⁻⁴ under L), e.g. **TwinD = `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)`**: "defect if I am
certified to defect against you, unless I am certified to defect against myself". Its produced D script is
`EvR*; ChkR[RunNeg · EvR*; ChkR[EvR*; Ax · Hyp]]`. Against any other source Y the first box ⊡(X, X, D) is not the
root's R or S and its clean value is F, so RunNeg closes the T branch, and the second box ⊡(X, Y, D) is the root's R,
closed by Hyp^self: certified defection against every Y ≠ X. In self-play the first box *is* the root's R, where
RunNeg is forbidden, the script fails, both atoms are F, and X cooperates. Whole plays (`runs/carrier_populations`
validation): TwinD self (C, C); against its own run-tree twin (another spelling) (D, D); against CB (D, D); against Cc
(D, C); against D (D, D). The checker's syntactic R/S coincidence is a quote-equality test, and the template turns it
into CliqueBot. Each spelling is its own class (split τ-type). In a TwinD population every mutant earns ≤ −1 against
0: no neutral and no strict invader; in all-D it is a neutral entrant with a second-order advantage like every
establisher. So it is drift-closed, and the ε→0 chain is absorbed by the ten cliques at every N in every arm and prior
(π split among them in proportion to their entry flux, i.e. prior mass; exits are deleterious fixations, log10 rate
−36 at N = 10³ and −330 at 10⁴).

## 6. Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | L×P lottery success interval excludes 0.5, point ≥ 0.8 (bet ≥ 0.9); establishment within 100 generations; winners CB/CBP-shaped carriers | **failed as scored on the spec's endpoint E1, falsifier fired** (8/40 [0.10, 0.35]; and 1/40 runs won by a non-carrier, `if(CHK(me,them,D),if(CHK(them,them,C),C,D),C)`). E1's censoring (32/40) is polymorphism among neutral cooperating classes at the horizon: every one of those runs is resolved cooperating under E3 (40/40 [0.91, 1.00]). Establishment clause **held** (first island at P(C,C) ≥ 0.9 by generation 100 in 40/40, median 30); winners carriers in 39/40 (CB in 26). |
| RE 2 | top cooperative state exits by neutral drift into a shadow then D, ∝ 1/N, no N-independent exit, P(C,C) rising, odds slope in [0.3, 0.6] | **mechanism failed in the specified chain**: the top cooperative state is a TwinD clique with no neutral exit (all exits deleterious, exponentially small in N), P(C,C) = 1 at every N in every arm; the falsifier as worded (an N-independent exit, or P(C,C) falling) did not fire. **In the no-clique control (not preregistered; the ten closed classes removed)** the predicted mechanism appears exactly: top state CB (0.15–0.28), exits neutral drift into Cc-type shadows with N·ρ = 1 (∝ 1/N), entry from all-D with N·ρ = 13.6 / 43.5 / 75.5 / 138 (∝ N^½), cooperative/D odds slope 0.53 / 0.52 / 0.52, P(C,C) 0.50 / 0.76 / 0.84 / 0.91 at N = 10³ / 10⁴ / 3·10⁴ / 10⁵. |
| RE 3 | (a) 0 false atoms; (b) no strict non-shadow entry into CB/CB1/CBP; (c) some establisher outside that subclass exploited | **held, all three**: (a) 72,991 true checks in the executable and in the ideal class table, 0 false atoms; (b) Lemma G: none of the 14 S-guarded establisher classes has a strict invader; (c) 75 of 101 establisher classes are strictly exploited (defection detectors such as `if(CHK(them,⌜C⌝,D),D,C)`). |
| RE 4 | certificate-less spellings refused by carriers, no neutral entry; L×O P(C,C) lower by ≤ 0.15, same exponent sign; lottery lower by establishment | **falsifier fired**: certificate-less spellings enter 78 establisher classes neutrally (all defection detectors, which never read a certificate of cooperation); none enters any of the 14 S-guarded carriers. Chain: L×O = L×P = 1 (cliques); no-clique control 0.756 vs 0.758 at 10⁴, 0.907 vs 0.908 at 10⁵ (not lower beyond 0.002). Lottery E3 38/40 vs 40/40 (two failures, one won by `Dc`); E1 15/40 vs 8/40. |
| RE 5 | bridges only unconditional cooperators or two-atom `or` templates, every bridge a shadow; ≥ 0.9 of cooperative π on one entry; both entries alive ≥ 0.3 of lottery runs | **falsifier fired** (a non-shadow bridge exists: `Bor` = `if(or(CHK(them,me,C),CHK_5(them,me,C)),C,D)` and its order twin, S-guarded, no strict invader in the E catalogue, cooperating with CB on both entries); 103 exploitable detector establishers also bridge, besides 246 unconditional-cooperator classes. Cooperative π on entry 0: 0.79 at N = 10³ and 10⁴ (E), 0.50 (E-eq): the ≥ 0.9 clause **failed**. Both entries' establishers alive at the horizon in 20/40 runs (E) and 16/40 (E-eq): that clause **held**. |
| RE 6 | U×P and L×P both ≥ 0.5 at 10⁴ | **held as worded** (1.0 and 1.0), but by the clique, not because carriers are the bulk; in the no-clique control U×P 0.984 at 10⁵ (L×P 0.908). |
| RE 7 | ideal and executable tables differ only in timeouts; chain P(C,C) within 0.1 | **held**: the two tables are identical on every class cell in P (588 classes) and O (701) and on a 291-class sample in E; the chains are the same computation. |
| S1 | 0 false atoms | **held** |
| S2 | executable = ideal everywhere; every check < 10⁵ | cells **held**; the number **failed** (largest non-timeout check 101,644) |
| S3 | Lemma G exhaustive | **held** |
| S4 | no exploited establisher | **failed, falsifier fired** (75 of 101) |
| S5 | unconditional cooperators ≥ 0.1, establishers ≤ 0.03 (L) | **failed** (0.354 held; establishers 0.061) |
| S6 | top cooperative state at 10⁴ prudent, every exit neutral | **failed in substance**: the main arm's top state (TwinD) refuses Cc and has no strict exit, so the falsifier as worded did not fire, but it is a clique with no neutral exit either; in the no-clique control the top state is CB, which accepts Cc |
| S7 | L×P P(C,C) at 10⁴ in [0.1, 0.7], slope [0.2, 0.7] | **failed** (1.0; no slope). In the no-clique control 0.758 and 0.52 |
| S8 | Bor a non-shadow bridge | **held** |
| S9 | entries share cooperative π: each ≥ 0.2 (E, entry 0 about 2:1), 0.4–0.6 (E-eq) | **held** at the N that ran (10³, 10⁴: 0.79/0.21, ratio 3.8:1 rather than 2:1 because the clique has two atoms; E-eq 0.50/0.50); not run at 10⁵ |
| S10 | certificate-less spellings D-twins or suckers, no neutral entry; L×O within 0.1 | **failed** (neutral entry into 78 detector establishers); the 0.1 clause held |
| S11 | ideal = executable chain | **held** |
| S12 | decisive cells unchanged at 3·10⁵ and 3·10⁶ | **failed at 3·10⁵** (305 class cells differ, 35 between establishers; V = 75,000 is below the largest checks, 413 more checks hit the cap); held at 3·10⁶ (0 cells) |
| S13 | U×P < L×P at 10⁴ | **failed, falsifier fired** (1.0 = 1.0; in the no-clique control U > L) |
| S14 | E3 success ≥ 0.5; E1 censors ≥ 0.5 | **held** (40/40; 32/40) |
| S15 | twin-expanded = unlumped on n ≤ 5 | **held** (to 3·10⁻¹⁰) |

Deviations: E's class table is the ideal one (the executable table was computed on a 291-class sample, 24,702 term
checks, identical; the full executable E table would have taken ≈ 3 h); E's chain ran at N = 10³ and 10⁴ only (a cell
at 10⁴ took 29 min with closed-form monomorphic fates; the absorbing structure is N-independent); the no-clique control
used θ = 10⁻⁸ and ≤ 4,000 explored states (cut ≤ 0.9% in the L cells; 11% in U×P at 10⁵, entirely from non-cooperative
states into non-cooperative polymorphisms, so its π(coop) is uncorroborated; U×P at 10⁴ was stopped unfinished after 50 min); `FastChain` (closed-form two-type fates in
monomorphic states) reproduces `LogChain` exactly on the P cells (π(D), entry rates, exits to all digits).

