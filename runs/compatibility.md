# Compatibility among co-seeded establishers (2026-10-05)

Spec `specs/2026-10-05-compatibility.md`; predictions `predictions/2026-10-05-compatibility.md`; code `src/compatibility.py`.
Modal arm, PD, w = 0.3, eps = 0. Class data: `spoiler_conditioned.cdata` (checked equal to modal.build at n = 6, 9).

## 1. Compatibility index

| n | classes | establishers | mu_est | kappa | kappa (x != y) | mutual-defection rate | exploitation rate | components | DD pair mass / mu_est^2 |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 51 | 9 | 0.0229 | 0.9767 | 0.9711 | 0.0000 | 0.0233 | 1 | 0.0000 |
| 9 | 863 | 148 | 0.0246 | 0.9580 | 0.9487 | 0.0010 | 0.0410 | 1 | 0.0010 |
| 12 | 13514 | 2505 | 0.0253 | 0.9510 | 0.9405 | 0.0017 | 0.0473 | 1 | 0.0017 |

Denominator: two iid draws from mu that are both establishers (mu_est^2); same-class draws count as mutual cooperation.
Missing-edge mass within the single component, as a fraction of mu(C)^2/2: n = 6: 0.0233, n = 9: 0.0420, n = 12: 0.0490

### Heavy-set pairwise matrix, n = 6 (row vs column; CC mutual cooperation, DD mutual defection, exploit one-sided)

| | mu | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| 1 `BOX(THEM(ME))` | 0.00495 | self | CC | CC | CC | CC | CC | exploit | exploit |
| 2 `BOX(THEM(THEM))` | 0.00495 | CC | self | CC | CC | CC | CC | exploit | exploit |
| 3 `BOX1(THEM(ME))` | 0.00495 | CC | CC | self | CC | CC | CC | CC | exploit |
| 4 `BOX1(THEM(THEM))` | 0.00490 | CC | CC | CC | self | CC | CC | exploit | exploit |
| 5 `BOX(THEM(^C))` | 0.00138 | CC | CC | CC | CC | self | CC | exploit | exploit |
| 6 `BOX1(THEM(^C))` | 0.00138 | CC | CC | CC | CC | CC | self | CC | exploit |
| 7 `not(BOXD(THEM(^C)))` | 0.00016 | exploit | exploit | CC | exploit | exploit | CC | self | CC |
| 8 `not(BOXD1(THEM(^C)))` | 0.00016 | exploit | exploit | exploit | exploit | exploit | exploit | CC | self |

### Heavy-set pairwise matrix, n = 9 (row vs column; CC mutual cooperation, DD mutual defection, exploit one-sided)

| | mu | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 `BOX1(THEM(ME))` | 0.00513 | self | CC | CC | CC | CC | CC | CC | exploit | DD |
| 2 `BOX(THEM(ME))` | 0.00513 | CC | self | CC | CC | CC | CC | exploit | exploit | CC |
| 3 `BOX(THEM(THEM))` | 0.00510 | CC | CC | self | CC | CC | CC | exploit | exploit | CC |
| 4 `BOX1(THEM(THEM))` | 0.00510 | CC | CC | CC | self | CC | CC | exploit | exploit | exploit |
| 5 `BOX1(THEM(^C))` | 0.00158 | CC | CC | CC | CC | self | CC | CC | exploit | DD |
| 6 `BOX(THEM(^C))` | 0.00158 | CC | CC | CC | CC | CC | self | exploit | exploit | DD |
| 7 `not(BOXD(THEM(^C)))` | 0.00025 | CC | exploit | exploit | exploit | CC | exploit | self | CC | exploit |
| 8 `not(BOXD1(THEM(^C)))` | 0.00025 | exploit | exploit | exploit | exploit | exploit | exploit | CC | self | exploit |
| 9 `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 0.00000 | DD | CC | CC | exploit | DD | DD | exploit | exploit | self |

### Heavy-set pairwise matrix, n = 12 (row vs column; CC mutual cooperation, DD mutual defection, exploit one-sided)

| | mu | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 `BOX1(THEM(ME))` | 0.00518 | self | CC | CC | CC | CC | CC | exploit | CC | DD |
| 2 `BOX(THEM(ME))` | 0.00518 | CC | self | CC | CC | CC | CC | exploit | exploit | CC |
| 3 `BOX(THEM(THEM))` | 0.00514 | CC | CC | self | CC | CC | CC | exploit | exploit | CC |
| 4 `BOX1(THEM(THEM))` | 0.00514 | CC | CC | CC | self | CC | CC | exploit | exploit | exploit |
| 5 `BOX1(THEM(^C))` | 0.00169 | CC | CC | CC | CC | self | CC | exploit | CC | DD |
| 6 `BOX(THEM(^C))` | 0.00168 | CC | CC | CC | CC | CC | self | exploit | exploit | DD |
| 7 `not(BOXD1(THEM(^C)))` | 0.00029 | exploit | exploit | exploit | exploit | exploit | exploit | self | CC | exploit |
| 8 `not(BOXD(THEM(^C)))` | 0.00029 | CC | exploit | exploit | exploit | CC | exploit | CC | self | exploit |
| 9 `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 0.00000 | DD | CC | CC | exploit | DD | DD | exploit | exploit | self |

## 2. Incompatible pairs and co-seeding

| n | incompatible pairs (DD / exploit) | consequential (co-seed >= 0.01 at N = 400) | P(any incompatible) N = 100 | N = 400 | P(any DD) N = 400 | heavy set exact N = 400 | P(2+ establisher classes) N = 400 |
|---|---|---|---|---|---|---|---|
| 6 | 11 (0 / 11) | 10 | 0.0259 | 0.1189 | 0.0000 | 0.1183 | 0.9973 |
| 9 | 4360 (770 / 3590) | 10 | 0.0526 | 0.2188 | 0.0099 | 0.1829 | 0.9986 |
| 12 | 1401462 (283091 / 1118371) | 10 | 0.0630 | 0.2604 | 0.0166 | 0.2073 | 0.9989 |

Consequential pairs (exploiter | exploited), n = 12:

| exploiter | exploited | type | co-seed N = 100 | N = 400 |
|---|---|---|---|---|
| `BOX1(THEM(ME))` | `not(BOXD1(THEM(^C)))` | exploit | 0.0115 | 0.0954 |
| `BOX(THEM(ME))` | `not(BOXD1(THEM(^C)))` | exploit | 0.0114 | 0.0954 |
| `BOX(THEM(ME))` | `not(BOXD(THEM(^C)))` | exploit | 0.0114 | 0.0954 |
| `BOX(THEM(THEM))` | `not(BOXD1(THEM(^C)))` | exploit | 0.0114 | 0.0952 |
| `BOX1(THEM(THEM))` | `not(BOXD1(THEM(^C)))` | exploit | 0.0114 | 0.0952 |
| `BOX(THEM(THEM))` | `not(BOXD(THEM(^C)))` | exploit | 0.0114 | 0.0952 |
| `BOX1(THEM(THEM))` | `not(BOXD(THEM(^C)))` | exploit | 0.0114 | 0.0952 |
| `BOX1(THEM(^C))` | `not(BOXD1(THEM(^C)))` | exploit | 0.0044 | 0.0535 |
| `BOX(THEM(^C))` | `not(BOXD1(THEM(^C)))` | exploit | 0.0044 | 0.0533 |
| `BOX(THEM(^C))` | `not(BOXD(THEM(^C)))` | exploit | 0.0044 | 0.0533 |

Heaviest mutually-defecting pairs, n = 12: `BOX1(THEM(ME))` / `BOX1(THEM(^not(BOX(THEM(ME)))))` 0.0023; `BOX(THEM(ME))` / `BOX1(THEM(^not(BOX(THEM(ME)))))` 0.0023; `BOX1(THEM(ME))` / `BOX1(THEM(^not(BOX(THEM(THEM)))))` 0.0023; `BOX(THEM(ME))` / `BOX1(THEM(^not(BOX(THEM(THEM)))))` 0.0023; `BOX1(THEM(ME))` / `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` 0.0011; `BOX1(THEM(ME))` / `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` 0.0011

Along N (exact over the consequential classes and the heavy set; simulated over all establishers at n = 12):

| n | N | exact, consequential pairs | exact, heavy set | simulated, all establishers |
|---|---|---|---|---|
| 6 | 100 | 0.0263 | 0.0263 |  |
| 6 | 400 | 0.1183 | 0.1183 |  |
| 6 | 1600 | 0.3959 | 0.3959 |  |
| 6 | 6400 | 0.8668 | 0.8668 |  |
| 6 | 25600 | 0.9997 | 0.9997 |  |
| 9 | 100 | 0.0423 | 0.0424 |  |
| 9 | 400 | 0.1824 | 0.1829 |  |
| 9 | 1600 | 0.5534 | 0.5545 |  |
| 9 | 6400 | 0.9602 | 0.9606 |  |
| 9 | 25600 | 1.0000 | 1.0000 |  |
| 12 | 100 | 0.0486 | 0.0488 | 0.0633 |
| 12 | 400 | 0.2063 | 0.2073 | 0.2591 |
| 12 | 1600 | 0.6034 | 0.6054 | 0.6962 |
| 12 | 6400 | 0.9753 | 0.9758 | 0.9916 |
| 12 | 25600 | 1.0000 | 1.0000 |  |

## 3. Anti-coordinators

| n | pairs | classes involved | class mass | pair mass / mu^2 | pairs both defecting on D | P(any co-seeded) N = 400 | both defect on D | N = 100 both defect on D |
|---|---|---|---|---|---|---|---|---|
| 6 | 35 | 17 | 0.0194 | 1.20e-04 | 6 | 0.8876 | 0.0245 | 0.0022 |
| 9 | 9436 | 366 | 0.0266 | 1.47e-04 | 1104 | 0.9195 | 0.0560 | 0.0054 |
| 12 | 2197221 | 6579 | 0.0282 | 1.61e-04 | 191226 | 0.9323 | 0.0729 | 0.0069 |

Heaviest anti-coordinator pairs at n = 12: `BOXD1(THEM(THEM))` / `not(BOXD1(THEM(ME)))` 0.367 (one cooperates with D: True); `BOXD(THEM(THEM))` / `not(BOXD1(THEM(ME)))` 0.367 (one cooperates with D: True); `BOXD1(THEM(THEM))` / `not(BOXD(THEM(ME)))` 0.367 (one cooperates with D: True); `BOXD(THEM(THEM))` / `not(BOXD(THEM(ME)))` 0.367 (one cooperates with D: True)
Observed pair (seeds-in-n n = 9, unresolved): n = 9 co-seed(400) 0.0010; n = 12 co-seed(400) 0.0013

## 4. Re-analysis of existing rows (certification rule alone; horizon 1e5 generations)

| source | n | islands | certified | excluded | P(C,C) < 0.95 | Pareto-inefficient | strictly 0 < P(C,C) < 1 | frozen cooperative | of which P(C,C) < 0.95 | 2+ establishers | compatible | incompatible |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| seeds-in-n mN=0 | 6 | 1200 | 1200 | 0 | 951 | 951 | 0 | 248 | 0 | 65 | 65 | 0 |
| seeds-in-n mN=0 | 7 | 1200 | 1200 | 0 | 914 | 914 | 0 | 286 | 0 | 79 | 79 | 0 |
| seeds-in-n mN=0 | 8 | 1200 | 1200 | 0 | 914 | 914 | 0 | 286 | 0 | 69 | 69 | 0 |
| seeds-in-n mN=0 | 9 | 1200 | 1199 | 1 | 924 | 924 | 0 | 275 | 0 | 78 | 78 | 0 |
| seeds-in-n mN=1 | 6 | 640 | 640 | 0 | 172 | 172 | 0 | 468 | 0 | 271 | 271 | 0 |
| seeds-in-n mN=1 | 7 | 640 | 640 | 0 | 164 | 164 | 0 | 476 | 0 | 273 | 273 | 0 |
| seeds-in-n mN=1 | 8 | 640 | 640 | 0 | 120 | 120 | 0 | 520 | 0 | 309 | 309 | 0 |
| seeds-in-n mN=1 | 9 | 640 | 640 | 0 | 160 | 160 | 0 | 480 | 0 | 247 | 247 | 0 |
| seeds-in-n mN=1 (I>16, global support) | 6 | 14080 | 14080 | 0 | - | - | - | 0 | 0 | 0 | 0 | 0 |
| seeds-in-n mN=1 (I>16, global support) | 7 | 11520 | 11520 | 0 | - | - | - | 0 | 0 | 0 | 0 | 0 |
| seeds-in-n mN=1 (I>16, global support) | 8 | 11520 | 11520 | 0 | - | - | - | 0 | 0 | 0 | 0 | 0 |
| seeds-in-n mN=1 (I>16, global support) | 9 | 14080 | 14080 | 0 | - | - | - | 0 | 0 | 0 | 0 | 0 |
| seeds-in-n mN=1 (I>16, run level) | 6 | 100 | 100 | 0 | 0 | 0 | 0 | 100 | 0 | 99 | 99 | 0 |
| seeds-in-n mN=1 (I>16, run level) | 7 | 60 | 60 | 0 | 0 | 0 | 0 | 60 | 0 | 60 | 60 | 0 |
| seeds-in-n mN=1 (I>16, run level) | 8 | 60 | 60 | 0 | 0 | 0 | 0 | 60 | 0 | 59 | 59 | 0 |
| seeds-in-n mN=1 (I>16, run level) | 9 | 100 | 100 | 0 | 0 | 2 | 2 | 100 | 0 | 97 | 95 | 2 |
| seeds-tail mN=0 | 12 | 640 | 640 | 0 | 475 | 475 | 0 | 165 | 0 | 37 | 37 | 0 |
| seeds-tail mN=0.1 | 12 | 240 | 240 | 0 | 92 | 92 | 0 | 148 | 0 | 7 | 7 | 0 |
| seeds-tail mN=1 | 12 | 240 | 240 | 0 | 116 | 116 | 0 | 124 | 0 | 34 | 34 | 0 |
| seeds-tail mN=10 | 12 | 240 | 240 | 0 | 136 | 136 | 0 | 104 | 0 | 38 | 38 | 0 |
| spoiler forced | 6 | 175000 | 174997 | 3 | 136577 | - | 0 | 38420 | 0 | 0 | 0 | 0 |
| spoiler forced | 9 | 175000 | 174996 | 4 | 134824 | - | 0 | 40172 | 0 | 0 | 0 | 0 |
| spoiler forced | 12 | 175000 | 174999 | 1 | 135283 | - | 0 | 39716 | 0 | 0 | 0 | 0 |
| spoiler natural | 6 | 8000 | 8000 | 0 | 6898 | 6898 | 0 | 1102 | 0 | 141 | 141 | 0 |
| spoiler natural | 9 | 8000 | 8000 | 0 | 6840 | 6840 | 0 | 1160 | 0 | 154 | 154 | 0 |
| spoiler natural | 12 | 8000 | 8000 | 0 | 6880 | 6880 | 0 | 1117 | 0 | 118 | 118 | 0 |

Uncertified islands and their terminal support:

- forced spoiler n = 6 pair 4 rep 421 a3: {'not(BOXD(THEM(ME)))': 140, 'BOX1(THEM(^BOXD(THEM(ME))))': 260}, P(C,C) 0.456, pair types ['CC'], self-play [0, 0], vs D [0, 0]
- forced spoiler n = 6 pair 4 rep 421 cD3: {'not(BOXD(THEM(ME)))': 140, 'BOX1(THEM(^BOXD(THEM(ME))))': 260}, P(C,C) 0.456, pair types ['CC'], self-play [0, 0], vs D [0, 0]
- forced spoiler n = 6 pair 6 rep 908 a10: {'BOXD1(THEM(THEM))': 221, 'not(BOXD(THEM(THEM)))': 179}, P(C,C) 0.496, pair types ['CC'], self-play [0, 0], vs D [1, 0]
- forced spoiler n = 9 pair 1 rep 158 cD10: {'not(BOXD(THEM(THEM)))': 243, 'BOX1(THEM(^BOXD(THEM(ME))))': 157}, P(C,C) 0.478, pair types ['CC'], self-play [0, 0], vs D [0, 0]
- forced spoiler n = 9 pair 3 rep 674 b10: {'not(BOXD(THEM(THEM)))': 194, 'BOX1(THEM(^BOXD(THEM(THEM))))': 206}, P(C,C) 0.501, pair types ['CC'], self-play [0, 0], vs D [0, 0]
- forced spoiler n = 9 pair 4 rep 300 c1: {'not(BOXD(THEM(ME)))': 208, 'and(BOXD(THEM(THEM)),BOX1(THEM(ME)))': 192}, P(C,C) 0.500, pair types ['CC'], self-play [0, 0], vs D [0, 0]
- forced spoiler n = 9 pair 6 rep 716 c1: {'not(BOXD(THEM(ME)))': 212, 'BOX1(THEM(^BOXD(THEM(THEM))))': 188}, P(C,C) 0.499, pair types ['CC'], self-play [0, 0], vs D [0, 0]
- forced spoiler n = 12 pair 5 rep 222 c1: {'not(BOXD(THEM(ME)))': 219, 'BOX1(THEM(^BOXD1(THEM(THEM))))': 181}, P(C,C) 0.497, pair types ['CC'], self-play [0, 0], vs D [0, 0]
- seeds-in-n n = 9 (400, 4) mN = 0 rep 94 island 2: {not(BOXD(THEM(THEM))): 211, BOX1(THEM(^BOX1(THEM(^D)))): 189} (anti-coordinators)

Certified-separated runs (incompatible establishers held on different islands):

- n = 9 (100, 256) rep 3: {'BOX1(THEM(ME))': 25500, 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))': 100}; pair types ['DD']; island outcomes {'e': 256}
- n = 9 (100, 256) rep 21: {'BOX1(THEM(ME))': 25500, 'and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))': 100}; pair types ['DD']; island outcomes {'e': 256}

Natural spoiler islands split by the seed (efficiency = P(C,C) >= 0.95):

| n | N | seed | islands | efficient | share | incompatible terminal |
|---|---|---|---|---|---|---|
| 6 | 100 | no establisher | 378 | 0 | 0.000 | 0 |
| 6 | 100 | one establisher | 1175 | 51 | 0.043 | 0 |
| 6 | 100 | compatible, 2+ establishers | 2348 | 290 | 0.124 | 0 |
| 6 | 100 | incompatible (exploitation only) | 99 | 17 | 0.172 | 0 |
| 6 | 400 | one establisher | 12 | 1 | 0.083 | 0 |
| 6 | 400 | compatible, 2+ establishers | 3513 | 655 | 0.186 | 0 |
| 6 | 400 | incompatible (exploitation only) | 475 | 88 | 0.185 | 0 |
| 9 | 100 | no establisher | 331 | 0 | 0.000 | 0 |
| 9 | 100 | one establisher | 1084 | 57 | 0.053 | 0 |
| 9 | 100 | compatible, 2+ establishers | 2374 | 293 | 0.123 | 0 |
| 9 | 100 | incompatible (exploitation only) | 204 | 27 | 0.132 | 0 |
| 9 | 100 | incompatible (some DD) | 7 | 1 | 0.143 | 0 |
| 9 | 400 | one establisher | 6 | 0 | 0.000 | 0 |
| 9 | 400 | compatible, 2+ establishers | 3124 | 596 | 0.191 | 0 |
| 9 | 400 | incompatible (exploitation only) | 825 | 178 | 0.216 | 0 |
| 9 | 400 | incompatible (some DD) | 45 | 8 | 0.178 | 0 |
| 12 | 100 | no establisher | 319 | 1 | 0.003 | 0 |
| 12 | 100 | one establisher | 965 | 44 | 0.046 | 0 |
| 12 | 100 | compatible, 2+ establishers | 2466 | 292 | 0.118 | 0 |
| 12 | 100 | incompatible (exploitation only) | 241 | 33 | 0.137 | 0 |
| 12 | 100 | incompatible (some DD) | 9 | 3 | 0.333 | 0 |
| 12 | 400 | one establisher | 7 | 0 | 0.000 | 0 |
| 12 | 400 | compatible, 2+ establishers | 2980 | 537 | 0.180 | 0 |
| 12 | 400 | incompatible (exploitation only) | 961 | 196 | 0.204 | 0 |
| 12 | 400 | incompatible (some DD) | 52 | 14 | 0.269 | 0 |

## 5a. Conditioned lottery (n = 12, N = 400, single islands, horizon 1e5)

| sample | islands | draws | acceptance | certified | efficient | islands with an incompatible terminal pair | consequential-pair fates (x / y / both / neither) | DD-pair fates (x / y / both / neither) | islands polymorphic in a DD pair |
|---|---|---|---|---|---|---|---|---|---|
| conditioned on a consequential pair | 400 | 2006 | 0.1994 | 400 | 84 | 0 | 82 / 18 / 0 / 1533 | 1 / 0 / 0 / 29 | 0 |
| conditioned on a DD establisher pair (added) | 400 | 23329 | 0.0171 | 400 | 89 | 0 | 22 / 5 / 0 / 370 | 42 / 20 / 0 / 906 | 0 |
| unconditioned | 400 | 400 | 1.0000 | 400 | 68 | 0 | 11 / 0 / 0 / 281 | 1 / 0 / 0 / 19 | 0 |

Achieved counts by consequential pair (conditioned sample): BOX(THEM(ME)) | not(BOXD1(THEM(^C))) 189; BOX(THEM(THEM)) | not(BOXD1(THEM(^C))) 189; BOX1(THEM(ME)) | not(BOXD1(THEM(^C))) 188; BOX(THEM(ME)) | not(BOXD(THEM(^C))) 187; BOX(THEM(THEM)) | not(BOXD(THEM(^C))) 186; BOX1(THEM(THEM)) | not(BOXD(THEM(^C))) 186; BOX1(THEM(THEM)) | not(BOXD1(THEM(^C))) 180; BOX(THEM(^C)) | not(BOXD1(THEM(^C))) 121; BOX(THEM(^C)) | not(BOXD(THEM(^C))) 117; BOX1(THEM(^C)) | not(BOXD1(THEM(^C))) 90

## 5b. Pair competitions (n = 12, N = 400, 100 runs per start, horizon 20000 generations)

| # | x | y | type | self | vs D | pair 200:200 | 300:100 | 100:300 | bg 100:100 | 150:50 | 50:150 | larger wins at 3:1 | TV (1:1 / 3:1 / 1:3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `BOX1(THEM(ME))` | `not(BOXD1(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 99/0/0/1 | 100/0/0/0 | 0.50 | 0.00 / 0.01 / 0.00 |
| 1 | `BOX(THEM(ME))` | `not(BOXD1(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 0.50 | 0.00 / 0.00 / 0.00 |
| 2 | `BOX(THEM(ME))` | `not(BOXD(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 0.50 | 0.00 / 0.00 / 0.00 |
| 3 | `BOX(THEM(THEM))` | `not(BOXD1(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 99/0/0/1 | 100/0/0/0 | 0.50 | 0.00 / 0.01 / 0.00 |
| 4 | `BOX1(THEM(THEM))` | `not(BOXD1(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 98/0/0/2 | 96/0/0/4 | 97/0/0/3 | 0.50 | 0.02 / 0.04 / 0.03 |
| 5 | `BOX(THEM(THEM))` | `not(BOXD(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 99/0/0/1 | 100/0/0/0 | 99/1/0/0 | 0.50 | 0.01 / 0.00 / 0.01 |
| 6 | `BOX1(THEM(THEM))` | `not(BOXD(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 94/0/0/6 | 92/0/0/8 | 100/0/0/0 | 0.50 | 0.06 / 0.08 / 0.00 |
| 7 | `BOX1(THEM(^C))` | `not(BOXD1(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 85/0/0/15 | 90/0/0/10 | 87/0/0/13 | 0.50 | 0.15 / 0.10 / 0.13 |
| 8 | `BOX(THEM(^C))` | `not(BOXD1(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 87/0/0/13 | 87/0/0/13 | 87/0/0/13 | 0.50 | 0.13 / 0.13 / 0.13 |
| 9 | `BOX(THEM(^C))` | `not(BOXD(THEM(^C)))` | exploit | [1, 1] | [0, 0] | 100/0/0/0 | 100/0/0/0 | 100/0/0/0 | 90/0/0/10 | 89/0/0/11 | 92/0/0/8 | 0.50 | 0.10 / 0.11 / 0.08 |
| 10 | `BOX1(THEM(ME))` | `BOX1(THEM(^not(BOX(THEM(ME)))))` | DD | [1, 1] | [0, 0] | 44/56/0/0 | 100/0/0/0 | 0/100/0/0 | 59/34/0/7 | 95/4/0/1 | 9/67/0/24 | 1.00 | 0.22 / 0.05 / 0.33 |
| 11 | `BOX1(THEM(ME))` | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | DD | [1, 1] | [0, 0] | 54/46/0/0 | 100/0/0/0 | 0/100/0/0 | 22/78/0/0 | 93/7/0/0 | 0/100/0/0 | 1.00 | 0.32 / 0.07 / 0.00 |
| 12 | `BOX(THEM(^C))` | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | DD | [1, 1] | [0, 0] | 55/45/0/0 | 100/0/0/0 | 0/100/0/0 | 21/77/0/2 | 78/17/0/5 | 1/99/0/0 | 1.00 | 0.34 / 0.22 / 0.01 |
| 13 | `BOX1(THEM(ME))` | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | DD | [1, 1] | [0, 0] | 43/57/0/0 | 100/0/0/0 | 0/100/0/0 | 24/76/0/0 | 92/8/0/0 | 0/100/0/0 | 1.00 | 0.19 / 0.08 / 0.00 |
| 14 | `BOXD1(THEM(THEM))` | `not(BOXD1(THEM(ME)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/76/1/23 | 0/71/0/29 | 0/68/0/32 | 0.00 | 0.99 / 1.00 / 1.00 |
| 15 | `BOXD(THEM(THEM))` | `not(BOXD1(THEM(ME)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/69/0/31 | 0/66/0/34 | 0/74/0/26 | 0.00 | 1.00 / 1.00 / 1.00 |
| 16 | `BOXD1(THEM(THEM))` | `not(BOXD(THEM(ME)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/52/0/48 | 0/72/0/28 | 0/56/0/44 | 0.00 | 1.00 / 1.00 / 1.00 |
| 17 | `BOXD(THEM(THEM))` | `not(BOXD(THEM(ME)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/63/0/37 | 0/55/0/45 | 0/53/0/47 | 0.00 | 1.00 / 1.00 / 1.00 |
| 18 | `BOXD1(THEM(THEM))` | `not(BOXD(THEM(THEM)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/59/0/41 | 0/55/0/45 | 0/53/0/47 | 0.00 | 1.00 / 1.00 / 1.00 |
| 19 | `BOXD1(THEM(THEM))` | `not(BOXD1(THEM(THEM)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/58/0/42 | 0/60/0/40 | 0/41/0/59 | 0.00 | 1.00 / 1.00 / 1.00 |
| 20 | `BOXD(THEM(THEM))` | `not(BOXD(THEM(THEM)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/68/0/32 | 0/60/0/40 | 0/51/0/49 | 0.00 | 1.00 / 1.00 / 1.00 |
| 21 | `BOXD1(THEM(^D))` | `BOX(THEM(^D))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/82/0/18 | 0/76/0/24 | 0/89/0/11 | 0.00 | 1.00 / 1.00 / 1.00 |
| 22 | `BOXD1(THEM(^D))` | `not(BOXD1(THEM(ME)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/71/0/29 | 0/61/0/39 | 0/61/0/39 | 0.00 | 1.00 / 1.00 / 1.00 |
| 23 | `BOXD(THEM(^D))` | `not(BOXD1(THEM(ME)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/78/0/22 | 0/65/0/35 | 0/64/0/36 | 0.00 | 1.00 / 1.00 / 1.00 |
| 24 | `BOXD1(THEM(^D))` | `not(BOXD(THEM(ME)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/55/0/45 | 0/62/0/38 | 0/42/0/58 | 0.00 | 1.00 / 1.00 / 1.00 |
| 25 | `BOXD(THEM(^D))` | `not(BOXD(THEM(ME)))` | CC | [0, 0] | [1, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 0/56/0/44 | 0/62/0/38 | 0/55/0/45 | 0.00 | 1.00 / 1.00 / 1.00 |
| 26 | `not(BOXD(THEM(ME)))` | `BOX1(THEM(^BOXD1(THEM(ME))))` | CC | [0, 0] | [0, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 5/13/29/53 | 7/7/32/54 | 12/10/37/41 | 0.00 | 0.71 / 0.68 / 0.63 |
| 27 | `not(BOXD(THEM(THEM)))` | `BOX1(THEM(^BOX1(THEM(^D))))` | CC | [0, 0] | [0, 0] | 0/0/100/0 | 0/0/100/0 | 0/0/100/0 | 6/11/30/53 | 5/12/31/52 | 5/14/41/40 | 0.00 | 0.70 / 0.69 / 0.59 |

Cells are x only / y only / both / neither. For exploitation pairs x is the exploiter.

## Deviations from the predeclared design

- Pair competitions: the cap of 12 binds for anti-coordinators (many pairs co-seed at >= 0.01); it was applied per
  category (all 10 consequential establisher pairs; the 12 heaviest anti-coordinator pairs, plus the heaviest pair that
  both defect on D and the observed pair). No consequential pair is mutually defecting, so four mutually-defecting
  establisher pairs were added (the heaviest; PrudentBot with `BOX1(THEM(ME))` and with `BOX(THEM(^C))`; `BOX1(THEM(ME))`
  with P*, the pair of the two certified-separated runs). A second conditioned sample (400 islands conditioned on a
  mutually-defecting establisher pair) was added for prediction 4's polymorphism clause.
- Pair-competition horizon 2e4 generations (administrative; anti-coordinator polymorphisms never freeze and cost 5.7 s
  per run at 1e5). The lottery keeps 1e5.
- The 2x2 game inside every pair of one type is identical (exploitation, mutual defection, anti-coordination), so
  pair-only runs differ between pairs of a type only by random numbers.

## Unresolved incompatibility risk

- Co-seeding factor (n = 12, any incompatible establisher pair): 0.063 (N = 100), 0.26 (400), 0.70 (1600), 0.99 (6400).
  It tends to 1 along any N -> infinity path.
- Resolution-failure factor: of 3,814 single islands that co-seeded an incompatible establisher pair (2,918 natural
  spoiler islands at n = 6, 9, 12 and N = 100, 400; 896 lottery islands at n = 12, N = 400), none ended uncertified and
  none ended with an incompatible establisher pair in the terminal support: 0 / 3,814, rule-of-three 95% bound 7.9e-4.
  Efficiency is not lower when an incompatible pair is co-seeded (n = 12, N = 400: 0.204 exploitation-only, 0.269 with a
  DD pair, 0.180 compatible with 2+ establishers; conditioned lottery 84 / 400 against 68 / 400 unconditioned).
- Two-class argument: for two self-cooperating classes the diagonal is R = 0, so a stable interior rest point would need
  both off-diagonal payoffs above 0, i.e. both T, which is impossible. Establisher pairs are neutral (CC), bistable (DD)
  or dominated (exploitation); only self-defecting classes (anti-coordinators) can hold a stable two-class polymorphism.
- Bound: unresolved incompatibility risk per island <= P(co-seed) x 7.9e-4 <= 7.9e-4 at N <= 400, n <= 12. The
  resolution factor is measured only at N <= 400; uniformity in N rests on the two-class argument, not data.
- The only uncertified islands in all rows are anti-coordinator polymorphisms (no establisher present, P(C,C) ~ 0.5):
  1 / 4,800 seeds-in-n mN = 0 islands, 0 / 24,000 natural spoiler islands, 0 / 1,200 lottery islands, 8 / 525,000 forced
  spoiler islands.
- Metapopulation: mutually-defecting establishers can be held on different islands (2 / 100 runs at n = 9, (100, 256),
  `BOX1(THEM(ME))` against the P* family); every island is efficient, so this is a rival network across islands, not on
  one.

## Verdicts

1. **Held on its falsifier; the network clause holds only as written.** kappa = 0.977 / 0.958 / 0.951 (>= 0.9 at every
   n, falling with n). All establishers form one component at every n (vacuous, as the review said). Pairwise, the heavy
   set minus PrudentBot is *not* a compatible network: the two near-universal suckers `not(BOXD(THEM(^C)))`,
   `not(BOXD1(THEM(^C)))` (mu >= 1e-4) are exploited by every prover. PrudentBot (mu ~ 3e-6) mutually defects with both
   probe-readers as predicted, but also with `BOX1(THEM(ME))`, and it exploits `BOX1(THEM(THEM))`.
2. **Held.** DD pair mass / mu_est^2 = 0 / 0.0010 / 0.0017 (< 0.05). P(an island of N = 400 co-seeds an incompatible
   establisher pair) = 0.119 / 0.219 / 0.260 (in 0.1-0.4), rising with N (0.026-0.063 at N = 100; 0.70 at N = 1600 and
   0.99 at N = 6400, n = 12).
3. **Held, structurally.** In the PD, the certification rule (all present classes pairwise payoff-identical) forces an
   island to be all-CC or all-DD (T != S), so a certified island has P(C,C) in {0, 1}, P(C,C) < 0.95 coincides with
   Pareto-inefficiency, no certified cooperative island is below 0.95 and every certified island with 2+ establishers
   is mutually cooperating (0 incompatible out of 1,920 such islands with stored per-island support). The two
   certified-separated runs hold mutually-defecting establishers on different islands, each island efficient.
4. **Failed** (falsifier not triggered). Held: mutually-defecting establisher pairs are bistable (the larger class wins
   100% at 3:1 pair-only; 0 / 400 DD-conditioned islands polymorphic in a DD pair); anti-coordinators are polymorphic in
   100% of pair-only runs. Failed: anti-coordinator co-seeding at N = 400 is 0.89 / 0.92 / 0.93 for any pair and 0.024 /
   0.056 / 0.073 for pairs that both defect on D (the predicted bound was 0.02); the background changes the pair-only
   outcome by TV 0.19-0.34 for DD pairs at 1:1, up to 0.15 for exploitation pairs, and 0.6-1.0 for anti-coordinators
   (predicted < 0.2). Exploitation pairs, the only consequential ones, are a third pattern: the exploiter wins at every
   ratio.

