# Run: identity and tags in the carrier grammar, the pooling test (2026-10-10)

Spec `specs/2026-10-10-identity-and-tags.md`; review `reviews/2026-10-10-identity-and-tags-gpt-6.1-sol.md`; notes `notes/identity-tags.md`; predictions `predictions/2026-10-10-identity-and-tags.md` (with the endpoint revision); code `src/identity_tags.py`, `src/identity_tags_run.py`, `src/identity_tags_report.py`, `tests/test_identity_tags.py`; raw arrays in `runs/identity_tags/` (npz and pickles not committed). K = 10⁶, V = K/4, PD of the modal arm, w = 0.3. All lottery numbers are ε = 0, finite (N, I, horizon) evidence.

## 1. Scale guard, costs, validation

| spellings | run trees | τ′-units | lists | classes (singletons from split units) | unit-value checks | pair checks C / D (reduced keys) | TO C / D | total s (2 workers) |
|---|---|---|---|---|---|---|---|---|
| 34968 | 8558 | 17305 | 10038 | 3974 (606 from 202 units) | 74296 | 8798799 / 7862558 | 312882 / 321954 | 1214 |

Classes exceed the spec's 2,500 trigger; the full grammar is computable, so no reduced grammar was run.

**Validation (notes §1.13):** hand table 196/196 cells by whole plays; Lemma T′/R sample 4946 pairs, 0 mismatches; executable = ideal on 304 classes (92416 cells played whole), 0 mismatches; soundness: 6026729 + 5732620 true checks, 0 false atoms; milestone-2 lists changed by the extended probes: 0 of 12546; marker-reduced lists 200/200 direct productions equal; eq-clique spellings 12, classes 12 (all singletons: True); tags correct: True.

## 2. Static structure (L unless stated)

| prior | establishers | S-guarded est. | exploited est. | self-cooperators | unconditional C | D class |
|---|---|---|---|---|---|---|
| L | 0.07515 | 0.007043 | 0.05782 | 0.5186 | 0.3522 | 0.06169 |
| U | 0.224 | 0.0151 | 0.1256 | 0.5435 | 0.1059 | 2.52e-04 |

Counts: 3974 classes; 2160 self-cooperators; 890 establishers; 421 unconditional cooperators.

**Establisher classes by family label** (notes §1.10):

| label | classes | mass L | mass U |
|---|---|---|---|
| open | 329 | 0.03824 | 0.08279 |
| other | 172 | 0.0243 | 0.04328 |
| identity | 322 | 0.008979 | 0.08103 |
| tag1 | 29 | 0.001525 | 0.007297 |
| tag2 | 29 | 0.001525 | 0.007297 |
| exclusive | 9 | 5.81e-04 | 0.002265 |

**Named classes:**

| name | class representative | spellings in class | class mass L | spelling mass L | label | S-guarded | strict invaders |
|---|---|---|---|---|---|---|---|
| Cc | `C` | 2215 | 0.0682 | 0.001549 | - | False | 1891 |
| D | `D` | 2010 | 0.06169 | 0.001549 | - | True | 0 |
| D^1 | `D^1` | 371 | 0.01099 | 7.74e-04 | - | True | 0 |
| CB | `if(CHK(them,me,C),C,D)` | 1 | 1.94e-04 | 1.94e-04 | open | True | 0 |
| MC^1 | `if(CHK(them,me,C),C,D)^1` | 19 | 5.57e-04 | 9.68e-05 | open | True | 0 |
| TC1 | `if(tag1,C,D)` | 107 | 0.003195 | 1.94e-04 | - | False | 936 |
| TC1^1 | `if(tag1,C,D)^1` | 18 | 5.32e-04 | 9.68e-05 | tag1 | False | 424 |
| AF^1 | `if(and(tag1,CHK(them,me,C)),C,D)^1` | 1 | 2.42e-05 | 2.42e-05 | tag1 | True | 0 |
| OF^1 | `if(or(tag1,CHK(them,me,C)),C,D)^1` | 1 | 2.42e-05 | 2.42e-05 | open | False | 419 |
| EQ | `if(eq,C,D)` | 1 | 1.94e-04 | 1.94e-04 | identity | False | 0 |
| EQ' | `if(not(eq),D,C)` | 1 | 9.68e-05 | 9.68e-05 | identity | False | 0 |
| TwinD | `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)` | 1 | 4.84e-05 | 4.84e-05 | identity | False | 0 |
| XC | `if(and(CHK(them,me,C),CHK(them,^CB,D)),C,D)` | 3 | 9.68e-05 | 4.84e-05 | exclusive | True | 0 |
| XC' | `if(and(CHK(them,^CB,D),CHK(them,me,C)),C,D)` | 3 | 9.68e-05 | 4.84e-05 | exclusive | True | 0 |
| TC2^2 | `if(tag2,C,D)^2` | 18 | 5.32e-04 | – | tag2 | False | 424 |

**Families.** 7318 maximal cliques of the establisher compatibility graph (complete enumeration, 6 s); 323 components (largest 568). **F_CB** (the heaviest maximal clique containing CB): 216 classes, 1103 spellings, **M = 0.03144**; CB lies in 1707 maximal cliques; N(CB) (establishers mutually cooperating with CB): 329 classes, mass 0.03824. Exact-identity cliques (maximal cliques of one single-spelling class): 322, total mass 0.008979, heaviest 1.94e-04 (`if(eq,C,D)`); **M / heaviest identity clique = 162**. The eq-clique run tree: 12 spellings, mass 7.74e-04, 12 classes (CB's run tree: 12 spellings, mass 7.74e-04, 5 classes).

Heaviest pairwise-compatible sets (maximal cliques; near-duplicates differ in a few overlapping members):

| mass L | classes | spellings | labels | contains CB | rival of F_CB | bridges with F_CB (non-exploitable) | heaviest members |
|---|---|---|---|---|---|---|---|
| 0.034 | 181 | 1211 | {'other': 49, 'open': 120, 'tag1': 6, 'tag2': 6} | False | True | 90 (0) | `if(CHK(them,^C,D),D,C)`, `if(CHK(them,^D,D),D,C)`, `if(CHK(them,them,D),D,C)` |
| 0.034 | 181 | 1211 | {'other': 48, 'open': 121, 'tag1': 6, 'tag2': 6} | False | True | 91 (0) | `if(CHK(them,^C,D),D,C)`, `if(CHK(them,^D,D),D,C)`, `if(CHK(them,them,D),D,C)` |
| 0.034 | 181 | 1211 | {'other': 51, 'open': 118, 'tag1': 6, 'tag2': 6} | False | True | 88 (0) | `if(CHK(them,^C,D),D,C)`, `if(CHK(them,^D,D),D,C)`, `if(CHK(them,them,D),D,C)` |
| 0.03144 | 216 | 1103 | {'open': 216} | True | False | 216 (31) | `if(CHK(them,^CB,C),C,D)`, `if(CHK(them,them,D),D,C)`, `if(CHK(them,^CB,D),D,C)` |
| 0.03124 | 146 | 1109 | {'other': 43, 'open': 97, 'tag1': 6} | False | True | 69 (0) | `if(CHK(them,^C,D),D,C)`, `if(CHK(them,^D,D),D,C)`, `if(CHK(them,them,D),D,C)` |
| 0.03124 | 146 | 1109 | {'other': 40, 'open': 100, 'tag1': 6} | False | True | 72 (0) | `if(CHK(them,^C,D),D,C)`, `if(CHK(them,^D,D),D,C)`, `if(CHK(them,them,D),D,C)` |
| 0.03124 | 146 | 1109 | {'other': 41, 'open': 99, 'tag1': 6} | False | True | 71 (0) | `if(CHK(them,^C,D),D,C)`, `if(CHK(them,^D,D),D,C)`, `if(CHK(them,them,D),D,C)` |
| 0.03124 | 146 | 1109 | {'other': 41, 'open': 99, 'tag2': 6} | False | True | 71 (0) | `if(CHK(them,^C,D),D,C)`, `if(CHK(them,^D,D),D,C)`, `if(CHK(them,them,D),D,C)` |
| 0.03124 | 146 | 1109 | {'other': 43, 'open': 97, 'tag2': 6} | False | True | 69 (0) | `if(CHK(them,^C,D),D,C)`, `if(CHK(them,^D,D),D,C)`, `if(CHK(them,them,D),D,C)` |
| 0.03124 | 146 | 1109 | {'other': 40, 'open': 100, 'tag2': 6} | False | True | 72 (0) | `if(CHK(them,^C,D),D,C)`, `if(CHK(them,^D,D),D,C)`, `if(CHK(them,them,D),D,C)` |
| 0.03122 | 212 | 1094 | {'open': 212} | True | False | 209 (31) | `if(CHK(them,^CB,C),C,D)`, `if(CHK(them,them,D),D,C)`, `if(CHK(them,^CB,D),D,C)` |
| 0.03105 | 221 | 1089 | {'open': 221} | True | False | 212 (27) | `if(CHK(them,^CB,C),C,D)`, `if(CHK(them,them,D),D,C)`, `if(CHK(them,^CB,D),D,C)` |
| 0.03095 | 218 | 1086 | {'open': 218} | True | False | 208 (27) | `if(CHK(them,^CB,C),C,D)`, `if(CHK(them,them,D),D,C)`, `if(CHK(them,^CB,D),D,C)` |
| 0.03095 | 211 | 1086 | {'open': 211} | True | False | 209 (31) | `if(CHK(them,^CB,C),C,D)`, `if(CHK(them,them,D),D,C)`, `if(CHK(them,^CB,D),D,C)` |

**Rivals of CB** (establishers mutually defecting with CB): 531 classes, mass 0.03454, labels {'other': 150, 'tag1': 25, 'tag2': 25, 'identity': 322, 'exclusive': 9}. Heaviest: `if(CHK(them,^C,D),D,C)` (other, 0.004671, S-guarded False, 447 invaders); `if(CHK(them,^D,D),D,C)` (other, 0.004671, S-guarded False, 274 invaders); `if(CHK(them,^C,D),D,C)^1` (other, 6.05e-04, S-guarded False, 526 invaders); `if(CHK(them,^C,D),D,C)^2` (other, 6.05e-04, S-guarded False, 526 invaders); `if(CHK(them,^D,D),D,C)^1` (other, 6.05e-04, S-guarded False, 359 invaders); `if(CHK(them,^D,D),D,C)^2` (other, 6.05e-04, S-guarded False, 359 invaders).

**Pairwise bridges** (self-cooperating classes mutually cooperating with both):

| pair | bridges | mass L | establishers | non-exploitable | heaviest non-exploitable |
|---|---|---|---|---|---|
| CB|TC1^1 | 278 | 0.04935 | 44 | 10 | `if(CHK(them,me,C),C,D)^1` 5.57e-04, `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)^1` 9.68e-05, `if(CHK(them,me,C),C,D)^12` 7.26e-05 |
| CB|TC2^2 | 278 | 0.04935 | 44 | 10 | `if(CHK(them,me,C),C,D)^2` 5.57e-04, `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)^2` 9.68e-05, `if(CHK(them,me,C),C,D)^12` 7.26e-05 |
| CB|XC | 0 | 0 | 0 | 0 | – |
| CB|EQ | 0 | 0 | 0 | 0 | – |
| CB|TwinD | 0 | 0 | 0 | 0 | – |
| CB|detector | 826 | 0.3644 | 129 | 0 | – |

**Leak test:** 2160 self-cooperating classes in 343 components (largest 1818); **322 closed**, all identity cliques (labels {'identity': 322}), total mass 0.008979; heaviest: `if(eq,C,D)` 1.94e-04, `if(not(eq),D,C)` 9.68e-05, `if(eq,C,D)^1` 9.68e-05, `if(eq,C,D)^2` 9.68e-05.

**Seed payoff** (expected payoff of a class against the iid seed, f = U·μ; the scramble diagnostic):

| prior | unconditional C mass | EQ | CB | MC¹ | TC1¹ | XC | D | open (mass-weighted) | open prudent (refuse Cc): n, mass, f | identity (mass-weighted) | other |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 0.3522 | 0.001 | -0.441 | -0.424 | -0.122 | -0.025 | 0.001 | -0.544 | 39, 0.002251, -0.092 | 0.000 | -0.520 |
| U | 0.1059 | 0.010 | -0.393 | -0.390 | -0.177 | -0.014 | 0.017 | -0.499 | 39, 0.009814, -0.085 | 0.006 | -0.460 |
| T1a | 0.3412 | 0.001 | -0.458 | -0.442 | -0.149 | -0.056 | -0.030 | -0.566 | 39, 0.00218, -0.124 | -0.006 | -0.537 |
| T2 | 0.3412 | -0.030 | -0.458 | -0.411 | -0.118 | -0.056 | -0.030 | -0.561 | 39, 0.00218, -0.120 | -0.024 | -0.530 |
| T3 | 0.3412 | -0.030 | -0.458 | -0.442 | -0.149 | -0.024 | -0.030 | -0.567 | 39, 0.00218, -0.124 | -0.031 | -0.537 |
| identity | 0.3491 | -0.025 | -0.452 | -0.452 | -0.021 | -0.050 | -0.024 | -0.569 | 39, 0.002135, -0.146 | -0.027 | -0.585 |
| noclique | 0.3554 | 0.010 | -0.436 | -0.419 | -0.113 | -0.016 | 0.010 | -0.538 | 39, 0.002271, -0.083 | – | -0.515 |
| noallc | 0 | -0.542 | -0.736 | -0.736 | -0.660 | -0.582 | -0.542 | -0.907 | 39, 0.003475, -0.647 | -0.543 | -0.900 |

## 3. The ε = 0 lottery (mN = 1, 40 runs per cell; horizon 2,000, runs separated at 2,000 continued to 10,000)

Outcomes on holders (predictions, endpoint revision). "Univ-open" = every island held and every pair of holders mutually cooperating, every holder mutually cooperating with CB.

| cell | univ-open @2,000 [Wilson] | univ-other | patchwork | unresolved | failed | univ-open @10,000 | patchwork @10,000 | clique wins @2,000 / @10,000 | cross P(C,C) realized / holders @2,000 | @10,000 | island P(C,C) | open occupancy @2,000 / @10,000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L (100, 64) | 0 [0.00, 0.09] | 0 | 39 | 1 | 0 | 3 | 36 | 0 / 0 | 0.401 / 0.399 | 0.593 / 0.591 | 0.948 | 0.51 / 0.65 |
| L (200, 64) | 0 [0.00, 0.09] | 0 | 40 | 0 | 0 | 0 | 40 | 0 / 0 | 0.342 / 0.342 | 0.344 / 0.343 | 0.974 | 0.51 / 0.52 |
| L (100, 256) | 0 [0.00, 0.09] | 0 | 30 | 10 | 0 | 0 | 35 | 0 / 0 | 0.383 / 0.382 | 0.689 / 0.689 | 0.947 | 0.59 / 0.81 |
| U (100, 64) | 0 [0.00, 0.09] | 0 | 33 | 7 | 0 | 0 | 36 | 0 / 0 | 0.066 / 0.065 | 0.121 / 0.120 | 0.916 | 0.19 / 0.25 |
| T1a: M on EQ | 0 [0.00, 0.09] | 0 | 39 | 1 | 0 | 0 | 38 | 0 / 2 | 0.499 / 0.497 | 0.753 / 0.752 | 0.956 | 0.15 / 0.07 |
| T1b: M/10 on ten EQ spellings | 0 [0.00, 0.09] | 0 | 34 | 6 | 0 | 0 | 38 | 0 / 0 | 0.141 / 0.139 | 0.209 / 0.207 | 0.924 | 0.20 / 0.26 |
| T1c: M/10 on ten CB spellings, family removed | 1 [0.00, 0.13] | 0 | 37 | 2 | 0 | 7 | 32 | 0 / 0 | 0.587 / 0.586 | 0.827 / 0.826 | 0.964 | 0.72 / 0.88 |
| T2: M on TC1¹ | 0 [0.00, 0.09] | 0 | 38 | 2 | 0 | 1 | 38 | 0 / 0 | 0.397 / 0.396 | 0.583 / 0.582 | 0.946 | 0.50 / 0.62 |
| T3: M on XC | 0 [0.00, 0.09] | 0 | 37 | 3 | 0 | 0 | 37 | 0 / 0 | 0.579 / 0.578 | 0.833 / 0.832 | 0.961 | 0.13 / 0.05 |
| ablation: identity only | 0 [0.00, 0.09] | 0 | 35 | 5 | 0 | 2 | 37 | 0 / 0 | 0.300 / 0.300 | 0.487 / 0.486 | 0.940 | 0.39 / 0.52 |
| ablation: tags only | 18 [0.31, 0.60] | 3 | 19 | 0 | 0 | 26 | 10 | 1 / 1 | 0.914 / 0.914 | 0.957 / 0.956 | 0.992 | 0.87 / 0.89 |
| ablation: ⌜CB⌝ only | 22 [0.40, 0.69] | 0 | 17 | 1 | 0 | 30 | 10 | 0 / 0 | 0.902 / 0.901 | 0.968 / 0.968 | 0.991 | 0.92 / 0.94 |
| extra: identity cliques removed | 24 [0.45, 0.74] | 1 | 15 | 0 | 0 | 30 | 7 | 0 / 0 | 0.932 / 0.931 | 0.981 / 0.980 | 0.994 | 0.89 / 0.90 |
| extra: unconditional cooperators removed | 1 [0.00, 0.13] | 0 | 37 | 2 | 0 | 5 | 35 | 0 / 0 | 0.521 / 0.519 | 0.741 / 0.740 | 0.958 | 0.62 / 0.74 |

**Island shares by holder label** (fraction of all islands × runs):

| cell | @2,000: open / identity / other / tag / exclusive | @10,000: open / identity / other / tag / exclusive | top holders @10,000 (island-runs) |
|---|---|---|---|
| L (100, 64) | 0.514 / 0.414 / 0.039 / 0.021 / 0.012 | 0.648 / 0.294 / 0.026 / 0.026 / 0.006 | `if(not(CHK(them,me,C)),D,C)` 253, `if(CHK(them,^CB,C),C,D)` 247, `if(CHK(them,me,C),C,D)^1` 150 |
| L (200, 64) | 0.514 / 0.445 / 0.021 / 0.004 / 0.015 | 0.521 / 0.445 / 0.021 / 0.004 / 0.009 | `if(not(CHK(them,me,C)),D,C)` 329, `if(CHK(them,me,C),C,D)^2` 102, `if(CHK(them,^CB,C),C,D)` 90 |
| L (100, 256) | 0.588 / 0.361 / 0.029 / 0.000 / 0.022 | 0.811 / 0.166 / 0.011 / 0.000 / 0.013 | `if(not(CHK(them,me,C)),D,C)` 1223, `if(CHK(them,^CB,C),C,D)` 893, `if(CHK(them,me,C),C,D)^2` 500 |
| U (100, 64) | 0.191 / 0.730 / 0.037 / 0.017 / 0.023 | 0.248 / 0.678 / 0.038 / 0.016 / 0.020 | `if(and(CHK(them,^CB,C),CHK(them,^C,D)),C,D)^1` 39, `if(CHK(them,me,C),if(CHK(them,^C,C),D,C),D)` 38, `if(CHK(them,me,C),C,D)^12` 36 |
| T1a: M on EQ | 0.147 / 0.818 / 0.024 / 0.005 / 0.006 | 0.071 / 0.913 / 0.014 / 0.000 / 0.002 | `if(eq,C,D)` 2164, `if(CHK(them,me,C),if(CHK(them,^C,C),D,C),D)` 27, `if(and(CHK(me,^D,D),eq),C,D)^2` 26 |
| T1b: M/10 on ten EQ spellings | 0.203 / 0.777 / 0.012 / 0.002 / 0.005 | 0.264 / 0.715 / 0.011 / 0.001 / 0.009 | `if(eq,C,D)^1` 210, `if(eq,C,D)^2` 150, `if(not(eq),D,C)^2` 144 |
| T1c: M/10 on ten CB spellings, family removed | 0.721 / 0.233 / 0.027 / 0.003 / 0.016 | 0.882 / 0.104 / 0.009 / 0.001 / 0.005 | `if(CHK(them,me,C),C,D)^2` 637, `if(not(CHK(them,me,C)),D,C)` 594, `if(CHK(them,me,C),C,D)^1` 437 |
| T2: M on TC1¹ | 0.499 / 0.474 / 0.013 / 0.006 / 0.009 | 0.624 / 0.361 / 0.006 / 0.006 / 0.003 | `if(CHK(them,^CB,C),C,D)` 227, `if(CHK(them,me,C),C,D)^2` 145, `if(CHK(them,me,C),C,D)^1` 94 |
| T3: M on XC | 0.132 / 0.120 / 0.012 / 0.003 / 0.733 | 0.053 / 0.035 / 0.005 / 0.002 / 0.905 | `if(and(CHK(them,me,C),CHK(them,^CB,D)),C,D)` 2228, `if(and(CHK(them,^CB,D),CHK(them,me,C)),C,D)^1` 51, `if(CHK(them,me,C),if(CHK(them,^CB,C),D,C),D)` 39 |
| ablation: identity only | 0.391 / 0.593 / 0.016 / 0.000 / 0.000 | 0.518 / 0.471 / 0.010 / 0.000 / 0.000 | `if(not(CHK(them,me,C)),D,C)` 424, `if(eq,C,D)` 141, `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)` 117 |
| ablation: tags only | 0.873 / 0.047 / 0.007 / 0.073 / 0.000 | 0.894 / 0.039 / 0.001 / 0.066 / 0.000 | `if(not(CHK(them,me,C)),D,C)` 511, `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)` 244, `if(and(CHK(me,^D,D),CHK(them,me,C)),C,D)` 228 |
| ablation: ⌜CB⌝ only | 0.920 / 0.035 / 0.004 / 0.000 / 0.041 | 0.942 / 0.027 / 0.000 / 0.000 / 0.032 | `if(not(CHK(them,me,C)),D,C)` 550, `if(CHK(them,^CB,C),C,D)` 415, `if(and(CHK(them,me,C),CHK(them,^D,D)),C,D)` 143 |
| extra: identity cliques removed | 0.895 / 0.000 / 0.008 / 0.005 / 0.093 | 0.900 / 0.000 / 0.001 / 0.000 / 0.099 | `if(not(CHK(them,me,C)),D,C)` 622, `if(CHK(them,^CB,C),C,D)` 311, `if(or(CHK(them,me,C),CHK(them,^CB,C)),C,D)` 140 |
| extra: unconditional cooperators removed | 0.622 / 0.346 / 0.008 / 0.003 / 0.021 | 0.741 / 0.234 / 0.005 / 0.001 / 0.019 | `if(not(CHK(them,me,C)),D,C)` 255, `if(CHK(them,^CB,C),C,D)^1` 154, `if(or(CHK(them,me,C),CHK(me,them,D)),C,D)` 124 |

**Separation, resolution and hazards:**

| cell | ever separated | first separation (median gen) | h_sep per island pair | separated @2,000 | of those resolved by 10,000 | their outcome @10,000 | resolution events / separated run-gens | holder flips per island-gen (separated) |
|---|---|---|---|---|---|---|---|---|
| L (100, 64) | 40 | 20 | inf | 40 | 3 | {'patchwork': 36, 'universal-open': 3, 'unresolved': 1} | 4 / 394700 = 1.01e-05 | 3.73e-04 |
| L (200, 64) | 40 | 30 | inf | 40 | 0 | {'patchwork': 40} | 0 / 399340 = 0 | 3.21e-04 |
| L (100, 256) | 40 | 20 | inf | 40 | 0 | {'patchwork': 35, 'unresolved': 5} | 0 / 399710 = 0 | 3.73e-04 |
| U (100, 64) | 40 | 10 | inf | 40 | 0 | {'patchwork': 36, 'unresolved': 4} | 0 / 399880 = 0 | 1.85e-04 |
| T1a: M on EQ | 40 | 20 | inf | 40 | 2 | {'patchwork': 38, 'universal-other': 2} | 2 / 393880 = 5.08e-06 | 2.63e-04 |
| T1b: M/10 on ten EQ spellings | 40 | 20 | inf | 40 | 0 | {'patchwork': 38, 'unresolved': 2} | 0 / 399670 = 0 | 2.93e-04 |
| T1c: M/10 on ten CB spellings, family removed | 40 | 20 | inf | 39 | 6 | {'universal-open': 6, 'patchwork': 32, 'unresolved': 1} | 10 / 370260 = 2.70e-05 | 3.37e-04 |
| T2: M on TC1¹ | 40 | 20 | inf | 40 | 1 | {'patchwork': 38, 'universal-open': 1, 'unresolved': 1} | 2 / 399100 = 5.01e-06 | 3.53e-04 |
| T3: M on XC | 40 | 20 | inf | 40 | 3 | {'patchwork': 37, 'universal-other': 3} | 4 / 389270 = 1.03e-05 | 2.55e-04 |
| ablation: identity only | 40 | 20 | inf | 40 | 2 | {'patchwork': 37, 'unresolved': 1, 'universal-open': 2} | 2 / 397970 = 5.03e-06 | 3.65e-04 |
| ablation: tags only | 36 | 30 | 0.001142 | 19 | 8 | {'patchwork': 10, 'universal-open': 8, 'unresolved': 1} | 40 / 164780 = 2.43e-04 | 6.36e-04 |
| ablation: ⌜CB⌝ only | 37 | 30 | 0.001285 | 18 | 8 | {'universal-open': 8, 'patchwork': 10} | 44 / 150110 = 2.93e-04 | 5.77e-04 |
| extra: identity cliques removed | 35 | 30 | 0.001031 | 15 | 8 | {'patchwork': 7, 'universal-open': 6, 'universal-other': 2} | 40 / 120780 = 3.31e-04 | 7.56e-04 |
| extra: unconditional cooperators removed | 40 | 20 | inf | 39 | 4 | {'patchwork': 35, 'universal-open': 4} | 8 / 380890 = 2.10e-05 | 3.52e-04 |

**Establishment and the pooling check** (a set *won* = universal with every holder in the set; decided = some set won):

| cell | first island at P(C,C) ≥ 0.9 (median gen) | every island held (median gen; runs) | maximal cliques per run (median) | decided @2,000 / @10,000 | largest seeded set won @10,000 | largest established set won @10,000 |
|---|---|---|---|---|---|---|
| L (100, 64) | 20 | 245 (40) | 568.5 | 0 / 3 | 0 / 3 | 3 / 3 |
| L (200, 64) | 30 | 300 (40) | 1429 | 0 / 0 | 0 / 0 | 0 / 0 |
| L (100, 256) | 20 | 290 (40) | 2901 | 0 / 0 | 0 / 0 | 0 / 0 |
| U (100, 64) | 20 | 150 (40) | 4845 | 0 / 0 | 0 / 0 | 0 / 0 |
| T1a: M on EQ | 20 | 200 (40) | 598.5 | 0 / 2 | 1 / 2 | 2 / 2 |
| T1b: M/10 on ten EQ spellings | 20 | 210 (40) | 575.5 | 0 / 0 | 0 / 0 | 0 / 0 |
| T1c: M/10 on ten CB spellings, family removed | 25 | 220 (40) | 119 | 1 / 7 | 7 / 7 | 7 / 7 |
| T2: M on TC1¹ | 20 | 240 (40) | 616.5 | 0 / 1 | 0 / 1 | 1 / 1 |
| T3: M on XC | 20 | 190 (40) | 599.5 | 0 / 3 | 1 / 3 | 3 / 3 |
| ablation: identity only | 30 | 250 (40) | 161 | 0 / 2 | 0 / 2 | 2 / 2 |
| ablation: tags only | 30 | 260 (40) | 245.5 | 21 / 29 | 0 / 29 | 29 / 29 |
| ablation: ⌜CB⌝ only | 30 | 230 (40) | 134 | 22 / 30 | 1 / 30 | 29 / 30 |
| extra: identity cliques removed | 30 | 260 (40) | 496.5 | 25 / 33 | 3 / 33 | 32 / 33 |
| extra: unconditional cooperators removed | 30 | 230 (40) | 1007 | 1 / 5 | 0 / 5 | 5 / 5 |

**Tracked classes** (runs seeded / runs in which it ever held an island / runs in which it was extinct by the end; median extinction generation):

| cell | MC1 | MC2 | OF1 | AF1 | TC1^1 | XC | XC' | EQ | CB | TwinD | marked carrier alive at first separation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L (100, 64) | 39 / 10 / 35 (10) | 39 / 5 / 37 (10) | 8 / 0 / 8 (10) | 9 / 1 / 8 (10) | 40 / 3 / 40 (10) | 25 / 3 / 24 (10) | 16 / 2 / 14 (10) | 29 / 1 / 28 (10) | 26 / 1 / 26 (10) | 9 / 1 / 9 (10) | 13 / 39 |
| L (200, 64) | 40 / 11 / 36 (10) | 40 / 15 / 33 (20) | 11 / 0 / 11 (10) | 12 / 1 / 11 (10) | 40 / 2 / 39 (20) | 27 / 0 / 27 (10) | 34 / 1 / 33 (10) | 36 / 7 / 29 (10) | 38 / 4 / 37 (10) | 16 / 1 / 15 (10) | 12 / 40 |
| L (100, 256) | 40 / 21 / 35 (50) | 40 / 24 / 32 (160) | 19 / 2 / 19 (10) | 21 / 0 / 21 (10) | 40 / 10 / 40 (30) | 39 / 5 / 35 (10) | 36 / 9 / 28 (10) | 40 / 11 / 34 (15) | 40 / 5 / 38 (10) | 32 / 4 / 28 (10) | 29 / 40 |
| U (100, 64) | 39 / 2 / 38 (10) | 40 / 3 / 37 (10) | 35 / 1 / 35 (10) | 33 / 3 / 31 (10) | 29 / 1 / 29 (10) | 30 / 0 / 30 (10) | 28 / 5 / 24 (10) | 31 / 2 / 30 (10) | 31 / 2 / 30 (10) | 35 / 4 / 33 (10) | 14 / 39 |
| T1a: M on EQ | 39 / 9 / 37 (10) | 40 / 7 / 38 (10) | 8 / 0 / 8 (10) | 7 / 0 / 7 (10) | 40 / 4 / 40 (10) | 21 / 1 / 20 (10) | 17 / 2 / 17 (10) | 40 / 40 / 0 (–) | 29 / 1 / 29 (10) | 11 / 0 / 11 (10) | 11 / 39 |
| T1b: M/10 on ten EQ spellings | 39 / 6 / 39 (10) | 39 / 4 / 37 (10) | 5 / 0 / 5 (10) | 8 / 1 / 8 (10) | 40 / 1 / 40 (10) | 18 / 1 / 17 (10) | 21 / 1 / 20 (10) | 40 / 29 / 12 (20) | 29 / 0 / 29 (10) | 13 / 0 / 13 (10) | 12 / 39 |
| T1c: M/10 on ten CB spellings, family removed | 40 / 40 / 20 (3270) | 40 / 39 / 19 (3150) | 0 / 0 / 0 (–) | 7 / 0 / 7 (10) | 39 / 2 / 39 (10) | 19 / 3 / 17 (10) | 20 / 1 / 19 (10) | 26 / 2 / 26 (10) | 40 / 23 / 36 (385) | 10 / 1 / 10 (10) | 40 / 40 |
| T2: M on TC1¹ | 40 / 4 / 38 (10) | 39 / 12 / 34 (10) | 9 / 0 / 9 (10) | 8 / 0 / 8 (10) | 40 / 33 / 39 (110) | 21 / 0 / 21 (10) | 17 / 2 / 17 (10) | 28 / 4 / 24 (10) | 30 / 3 / 29 (10) | 9 / 2 / 7 (10) | 10 / 40 |
| T3: M on XC | 40 / 4 / 38 (10) | 39 / 2 / 39 (10) | 7 / 0 / 7 (10) | 5 / 1 / 4 (10) | 39 / 1 / 39 (10) | 40 / 40 / 1 (7180) | 19 / 1 / 19 (10) | 31 / 2 / 30 (10) | 31 / 2 / 30 (10) | 7 / 0 / 7 (10) | 8 / 40 |
| ablation: identity only | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 33 / 8 / 26 (10) | 36 / 1 / 36 (10) | 21 / 1 / 20 (10) | 0 / 0 |
| ablation: tags only | 38 / 5 / 37 (10) | 40 / 6 / 36 (10) | 8 / 0 / 8 (10) | 11 / 2 / 9 (10) | 40 / 3 / 39 (20) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 33 / 1 / 32 (10) | 13 / 1 / 12 (10) | 5 / 34 |
| ablation: ⌜CB⌝ only | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 0 / 0 / 0 (–) | 27 / 4 / 24 (10) | 23 / 4 / 22 (10) | 0 / 0 / 0 (–) | 35 / 4 / 32 (10) | 24 / 2 / 23 (10) | 0 / 0 |
| extra: identity cliques removed | 40 / 6 / 36 (10) | 40 / 5 / 35 (10) | 4 / 0 / 4 (10) | 11 / 0 / 11 (10) | 38 / 3 / 38 (15) | 15 / 1 / 14 (10) | 17 / 2 / 16 (10) | 0 / 0 / 0 (–) | 25 / 1 / 24 (10) | 0 / 0 / 0 (–) | 6 / 35 |
| extra: unconditional cooperators removed | 40 / 11 / 39 (10) | 40 / 13 / 36 (15) | 9 / 0 / 9 (10) | 12 / 0 / 12 (10) | 40 / 4 / 40 (10) | 20 / 2 / 18 (10) | 24 / 0 / 24 (10) | 36 / 1 / 35 (10) | 37 / 4 / 36 (10) | 16 / 0 / 16 (10) | 12 / 40 |

**Who is separated from whom** (runs with islands of both labels / with any island of the label, @2,000 → @10,000):

| cell | identity & open | identity majority | exclusive & open | any exclusive island | any tag-club island |
|---|---|---|---|---|---|
| L (100, 64) | 40 → 37 | 12 → 9 | 4 → 3 | 4 → 3 | 5 → 5 |
| L (200, 64) | 40 → 40 | 13 → 13 | 7 → 5 | 7 → 5 | 2 → 2 |
| L (100, 256) | 40 → 40 | 6 → 1 | 15 → 15 | 15 → 15 | 2 → 0 |
| U (100, 64) | 40 → 40 | 39 → 34 | 17 → 15 | 17 → 15 | 13 → 10 |
| T1a: M on EQ | 40 → 33 | 40 → 40 | 4 → 2 | 4 → 2 | 4 → 1 |
| T1b: M/10 on ten EQ spellings | 38 → 36 | 39 → 34 | 3 → 3 | 3 → 3 | 2 → 1 |
| T1c: M/10 on ten CB spellings, family removed | 39 → 29 | 4 → 3 | 9 → 6 | 9 → 6 | 2 → 1 |
| T2: M on TC1¹ | 40 → 38 | 18 → 14 | 5 → 3 | 5 → 3 | 2 → 2 |
| T3: M on XC | 39 → 24 | 0 → 0 | 40 → 31 | 40 → 40 | 3 → 2 |
| ablation: identity only | 39 → 36 | 27 → 20 | 0 → 0 | 0 → 0 | 0 → 0 |
| ablation: tags only | 11 → 6 | 1 → 1 | 0 → 0 | 0 → 0 | 9 → 7 |
| ablation: ⌜CB⌝ only | 6 → 5 | 1 → 1 | 8 → 5 | 8 → 5 | 0 → 0 |
| extra: identity cliques removed | 0 → 0 | 0 → 0 | 9 → 5 | 9 → 7 | 3 → 1 |
| extra: unconditional cooperators removed | 38 → 33 | 9 → 8 | 9 → 4 | 9 → 4 | 2 → 1 |

**Islands per seeded copy** (islands held at 2,000 / 10,000 per seeded copy of the label, all runs of the cell pooled; the pooling question by raw counts):

| cell | open | identity | other | exclusive | identity copies seeded per run | open copies per run |
|---|---|---|---|---|---|---|
| L (100, 64) | 0.136 / 0.171 | 0.469 / 0.333 | 0.016 / 0.011 | 0.204 / 0.109 | 56.6 | 241.8 |
| L (200, 64) | 0.068 / 0.069 | 0.251 / 0.251 | 0.004 / 0.004 | 0.132 / 0.078 | 113.3 | 483.6 |
| L (100, 256) | 0.153 / 0.211 | 0.408 / 0.187 | 0.012 / 0.004 | 0.372 / 0.215 | 226.3 | 985.4 |
| U (100, 64) | 0.023 / 0.030 | 0.090 / 0.083 | 0.009 / 0.009 | 0.101 / 0.090 | 521.7 | 532.1 |
| T1a: M on EQ | 0.041 / 0.020 | 0.204 / 0.228 | 0.010 / 0.006 | 0.111 / 0.030 | 256.0 | 231.6 |
| T1b: M/10 on ten EQ spellings | 0.054 / 0.071 | 0.197 / 0.181 | 0.005 / 0.005 | 0.090 / 0.147 | 252.7 | 239.7 |
| T1c: M/10 on ten CB spellings, family removed | 0.227 / 0.278 | 0.269 / 0.120 | 0.011 / 0.003 | 0.263 / 0.075 | 55.4 | 203.1 |
| T2: M on TC1¹ | 0.135 / 0.168 | 0.538 / 0.409 | 0.005 / 0.003 | 0.146 / 0.053 | 56.4 | 237.0 |
| T3: M on XC | 0.036 / 0.014 | 0.141 / 0.041 | 0.005 / 0.002 | 0.233 / 0.288 | 54.2 | 237.8 |
| ablation: identity only | 0.147 / 0.195 | 0.432 / 0.344 | 0.005 / 0.003 | – | 87.8 | 170.1 |
| ablation: tags only | 0.353 / 0.362 | 1.061 / 0.877 | 0.002 / 0.000 | – | 2.9 | 158.2 |
| ablation: ⌜CB⌝ only | 0.210 / 0.215 | 0.763 / 0.576 | 0.002 / 0.000 | 0.452 / 0.352 | 3.0 | 280.4 |
| extra: identity cliques removed | 0.230 / 0.231 | – | 0.003 / 0.000 | 1.889 / 2.008 | 0.0 | 248.8 |
| extra: unconditional cooperators removed | 0.106 / 0.126 | 0.244 / 0.165 | 0.002 / 0.001 | 0.234 / 0.204 | 90.7 | 376.9 |

## 4. The ε→0 chain (diagnostic)

*Deviation:* the full 3,974-class chain (θ = 10⁻⁸, ≤ 4,000 explored states, `FastChain`) did not finish a single cell in 90 minutes on 3 workers and was stopped (pool children killed by pid, then the driver); it is reported as not run. The cells below run on a **reduced support**: `topL` = the 1,500 heaviest classes under L plus all 322 identity cliques (1,818 classes), `top` = the 500 heaviest plus the identity cliques (821), with the no-clique control removing the closed leak components (exactly the identity cliques). θ = 10⁻⁸, ≤ 4,000 states, twin drift on. Reduced support is a different object (rare classes cannot enter); it is a diagnostic only.

| label | N | P(C,C) | π(all-D) | π by label | top states (π, labels) | states | cut/flow | s |
|---|---|---|---|---|---|---|---|---|
| top | 1000 | 1.0000 | 9.59e-34 | {'identity': 1.0} | `if(eq,C,D):1.000` 0.02118 ['identity']; `if(not(eq),D,C):1.000` 0.01059 ['identity']; `if(eq,C,D)^1:1.000` 0.009529 ['identity']; `if(eq,C,D)^2:1.000` 0.009529 ['identity'] | 821 | 0.001207 | 27 |
| top | 10000 | 1.0000 | 0 | {'identity': 1.0} | `if(eq,C,D):1.000` 0.0212 ['identity']; `if(not(eq),D,C):1.000` 0.0106 ['identity']; `if(eq,C,D)^1:1.000` 0.009522 ['identity']; `if(eq,C,D)^2:1.000` 0.009522 ['identity'] | 821 | – | 78 |
| topL | 1000 | 1.0000 | 1.26e-33 | {'identity': 1.0} | `if(eq,C,D):1.000` 0.02142 ['identity']; `if(not(eq),D,C):1.000` 0.01071 ['identity']; `if(eq,C,D)^2:1.000` 0.009827 ['identity']; `if(eq,C,D)^1:1.000` 0.009815 ['identity'] | 1818 | 0.002167 | 171 |
| topL | 10000 | 1.0000 | 0 | {'identity': 1.0} | `if(eq,C,D):1.000` 0.02145 ['identity']; `if(not(eq),D,C):1.000` 0.01072 ['identity']; `if(eq,C,D)^2:1.000` 0.009808 ['identity']; `if(eq,C,D)^1:1.000` 0.009796 ['identity'] | 1818 | – | 430 |
| topLnoclosed | 1000 | 0.5600 | 0.06058 | {'-': 0.4421, 'other': 0.0337, 'open': 0.3036, 'exclusive': 0.2199} | `if(and(CHK(them,^CB,D),CHK(them,me,C)),C,D):1.000` 0.09904 ['exclusive']; `if(and(CHK(them,me,C),CHK(them,^CB,D)),C,D):1.000` 0.09753 ['exclusive']; `D:1.000` 0.06058 ['-']; `if(not(CHK(them,me,C)),D,C):1.000` 0.04783 ['open'] | 1520 | 0.002008 | 529 |
| topLnoclosed | 10000 | 0.7810 | 0.02696 | {'-': 0.2194, 'other': 0.0465, 'open': 0.3891, 'exclusive': 0.345} | `if(and(CHK(them,^CB,D),CHK(them,me,C)),C,D):1.000` 0.1553 ['exclusive']; `if(and(CHK(them,me,C),CHK(them,^CB,D)),C,D):1.000` 0.1531 ['exclusive']; `if(not(CHK(them,me,C)),D,C):1.000` 0.07505 ['open']; `if(CHK(them,^CB,C),D,if(CHK(them,me,C),C,D)):1.000` 0.04575 ['other'] | 1496 | 0.002241 | 305 |
| topnoclosed | 1000 | 0.2643 | 0.101 | {'-': 0.7382, 'other': 0.0078, 'open': 0.2531} | `D:1.000` 0.101 ['-']; `if(not(CHK(them,me,C)),D,C):1.000` 0.08662 ['open']; `if(CHK(them,^CB,C),C,D):1.000` 0.06294 ['open']; `if(CHK(me,them,D),C,D):1.000` 0.05884 ['-'] | 552 | 6.62e-04 | 392 |
| topnoclosed | 10000 | 0.4738 | 0.0624 | {'-': 0.5267, 'other': 0.0017, 'open': 0.4714} | `if(not(CHK(them,me,C)),D,C):1.000` 0.1964 ['open']; `D:1.000` 0.0624 ['-']; `if(or(CHK(them,me,C),CHK(me,them,D)),C,D):1.000` 0.0563 ['open']; `if(CHK(me,them,D),C,D):1.000` 0.05166 ['-'] | 504 | 9.73e-04 | 71 |

## 6. Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | clique cheap (within 4× of CB) but one class; F_CB ≥ 10× any clique | **held** (EQ and CB spellings both 1.94·10⁻⁴; every eq spelling its own class; M = 0.031 = 162 × the heaviest identity clique; falsifier not fired). But the 322 identity cliques together weigh 0.009, and the heaviest pairwise-compatible set is a defection-detector set (0.034), not F_CB |
| RE 2 | open family universal on ≥ 0.7 at (100, 64); no clique win; largest established set wins ≥ 0.9 and beats raw counts | **failed, falsifier fired** (universal-open 0/40 at 2,000, 3/40 at 10,000; the largest-established set won in 3 of 40 runs because no set won the rest). No clique win (0) held; where a set won anywhere the largest-established set won 3/3 (L) and 29/29, 29/30, 32/33 (ablations, no-clique cell) against 0/3, 0/29, 1/30, 3/33 for raw counts |
| RE 3 | T1a clique wins 0.3–0.7; T1b and T1c carriers ≥ 0.8; T1b ≪ T1a | **failed, falsifier fired**: clique wins 0/40 (T1a; 2/40 by 10,000), carriers win 0/40 (T1b) and 1/40 (T1c; 7/40 by 10,000); T1b ≥ T1a on wins (0 = 0), and on islands held by eq-cliques T1b 0.78 against T1a 0.82 at 2,000 (islands per seeded copy 0.197 against 0.204): incompatible spellings establish as well as one identity. T1b < T1a only later (0.72 against 0.91 at 10,000) |
| RE 4 | tag club rivals carriers; marked carrier resolves (≤ 0.2 separated where alive); no and-form resolution | **falsifier fired as worded** (10/10 runs with a living marked carrier at the first separation were separated at 2,000), but the rivalry it addresses never formed: TC1¹ at mass M held an island in 33/40 runs and was extinct by the end in 39/40 (median generation 110), eaten by marked defectors; the separations are with identity cliques, which no bridge reaches. No resolution through the and-form (AF¹ never held an island) |
| RE 5 | XC bridge-less; ≥ 0.3 separated XC/carriers; none resolves by 10,000 | **falsifier fired**: bridge-less held (0 classes cooperate with CB and XC, by soundness); separated XC/open in 40/40 at 2,000 held; but the XC–open rivalry resolved by majority in 9 of 40 runs by 10,000 (open family lost, no bridge), XC holding 0.73 → 0.91 of islands |
| RE 6 | (200, 64) and (100, 256) within 0.15 of (100, 64); separation hazard falling in N; resolution hazard rising in I | **held as worded, vacuously** (universal 0/40 in all three; falsifier not fired); P(ever separated) = 1 in every cell so the per-pair hazard is saturated; the resolution clause **failed** (resolution events 4 at (100, 64), 0 at (100, 256), 0 at (200, 64)); N = 200 freezes the patchwork; I = 256 absorbs clique islands slowly (identity share 0.36 → 0.17) without resolving a run |
| RE 7 | chain absorbed by the eq-clique or TwinD at N = 10⁴ | **held**: top state at N = 10⁴ `if(eq,C,D):1.000` (π 0.021, labels ['identity']); π on identity cliques 1.000 (reduced support: the 1,500 heaviest classes plus all 322 identity cliques, 1,818 classes; the full 3,974-class chain did not finish in 90 min and is not run; the 500-class support gives the same top state) |
| S1 | hand table by whole plays | **held** (196/196) |
| S2 | Lemma T′/R: 0 mismatches on ≥ 2,000 pairs | **held** (0/4,946; every n ≤ 4 pair and 1,500+ at n ≤ 5 in the tests) |
| S3 | ≤ 1% of milestone-2 lists change | **held** (0/12,546) |
| S4 | classes > 2,500, full grammar computable in < 3 h | **held** (3,974 classes, 20 min on 2 workers) |
| S5 | M in [0.005, 0.05]; heaviest identity clique EQ; identity total ≤ 0.01 | **held** (0.031; EQ 1.94·10⁻⁴; 0.0090) |
| S6 | detector rivals heavier than any identity clique | **held** (`if(CHK(them,⌜C⌝,D),D,C)` 0.0047 mutually defects with CB; the heaviest set without CB 0.034 > M) |
| S7 | L: E3 ≥ 0.9; universal-open ≥ 0.5; separated ≤ 0.3; no clique win | **failed, falsifier fired** (E3 40/40 and no clique win held; universal-open 0/40 < 0.3; separated 40/40) |
| S8 | largest established set beats largest seeded set by ≥ 0.1 | **held** on the decided runs (largest-established set won 113 of 115, largest-seeded set 13 of 115, pooled over all cells at 10,000; only 3 decided runs under L) |
| S9 | T1a eq-clique holds every island in [0.2, 0.6] by 10,000; T1b ≤ 0.1; T1c universal ≥ 0.6 | **failed, falsifier fired** (T1a 2/40 < 0.1; T1b 0; T1c 7/40) |
| S10 | T2: club establishes ≥ 0.7; marked D takes its islands; marked carrier alive at first separation ≤ 0.3; club wins ≤ 0.1 | **held** (33/40; extinct 39/40; 10/40; 0) |
| S11 | T3: XC establishes ≥ 0.8; separated ≥ 0.3; ≥ 0.2 of separations resolve by majority by 10,000 | **held** (40/40; 40/40; the XC–open rivalry resolved in 9/40 = 0.23; run-level patchworks persist through identity cliques) |
| S12 | (200, 64) within 0.15; (100, 256) lower by ≥ 0.1 | first clause **held** (0 = 0); second **failed, number** (0 = 0; falsifier "higher" not fired) |
| S13 | U universal-open ≥ 0.4, clique wins ≤ 0.1; ablations within 0.2 of L | **failed** (U 0/40, identity cliques hold 0.73 of islands, clique wins 0; tags-only 18/40 and ⌜CB⌝-only 22/40 against L 0/40); falsifier (clique wins > 0.2) not fired |
| S14 | chain absorbed by identity cliques, top EQ; no-clique control: open top state, P(C,C) [0.4, 0.95], slope [0.3, 0.7] | absorption clause **held** (top state EQ, π on identity cliques 1.000 at 10³ and 10⁴ on both supports); control: P(C,C) and slope clauses **held** (no-clique control P(C,C) 0.560 / 0.781 at 10³ / 10⁴, odds slope 0.45, top state `if(and(CHK(them,^CB,D),CHK(them,me,C)),C,D):1.000` (['exclusive']); the 500-class support gives 0.264 / 0.474, slope 0.40, top state an open carrier), the "open top state" clause **failed** on the larger support, where the top states are the exclusive club and its order twin (π 0.31 at 10⁴; exits neutral into `if(CHK(them,⌜CB⌝,D),C,D)`-type shadows) |

## 7. Reading

- **The pooling argument fails at establishment.** An identity clique turns a seeded copy into 2–4 times as many islands as an open carrier in every cell (0.47 against 0.14 under L), because against the iid seed it plays like D (seed payoff 0.001; CB −0.44) while cooperating with its copies, and it is drift-closed once it holds an island. Each spelling nucleates and colonizes on its own: ten mutually incompatible eq spellings at M/10 convert copies into islands at the rate one identity at M does (0.197 against 0.204) and hold as many islands (0.78 against 0.82 at 2,000); pooling shows only as slow absorption by the largest clique afterwards (0.91 against 0.72 at 10,000).
- **With one-node identity, universality fails in the seed lottery too.** L: 0/40 universal at 2,000 (3/40 at 10,000), identity cliques hold 0.41 of islands, every island efficient (E3 40/40, island P(C,C) 0.95). Without `eq` (tags-only, ⌜CB⌝-only ablations, identity mass 5·10⁻⁴) 18–22/40 are universal (26–30 by 10,000); deleting the identity cliques from L gives 24/40 (30). Removing the unconditional cooperators does not rescue universality (1/40; 5/40), so the shadows are not the whole mechanism.
- **Established mass predicts winners; raw seeded counts do not** (113/115 against 13/115 decided runs).
- **Clubs:** the tag club at mass M is eaten by marked defectors within ~100 generations (extinct 39/40), so the marked-carrier bridge is never tested; the exclusive club at mass M takes 0.73 → 0.91 of islands (prudent and S-guarded), bridge-less but winning by majority (open family lost in 9/40 runs by 10,000).
- **Finite size:** at N = 200 the patchwork is frozen between 2,000 and 10,000; at I = 256 clique islands are absorbed slowly (0.36 → 0.17) with no run finishing. The chain (reduced support) is absorbed by the identity cliques, top state EQ, as in milestone 2.

