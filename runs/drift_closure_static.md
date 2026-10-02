# Drift-closure static map (free modal arm, PD)

Written by src/moat_static.py for predictions/2026-10-02-drift-closure.md. Leak masses are prior masses of classes (normalized over L_n); a world's neutral exit rate to them is leak / N per mutation event.

## n = 6

- behavioural classes 51; self-cooperating 18 (μ 0.4974); components of G 1
- FairBot component: 18 classes, μ 0.0284 without ALLC (0.4974 with)
- closed components: 0, μ 0; closed components with a member that enters all-D neutrally: 0; max universality over closed classes 0
- checks: universality > 0 ⇒ in K(FB): True; K(FB) has a suckerable member: True

| component | size | μ | closed | has FB | has ALLC | suckerable members (μ) | enter all-D (μ) | max d | top members |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 18 | 0.497 | False | True | True | 15 (0.483) | 9 (0.0229) | 1.0 | `C` 0.47; `BOX(THEM(ME))` 0.005; `BOX(THEM(THEM))` 0.005 |

| class (top 25 by μ among self-cooperators) | μ | in K(FB) | suckerable | faker μ | d | universality | enters D | top fakers |
|---|---|---|---|---|---|---|---|---|
| `C` | 0.469 | True | True | 0.5 | 0.0 | 0.806 | False | `D`, `BOXD(THEM(ME))` |
| `BOX(THEM(ME))` | 0.00495 | True | False | 0 | 1.0 | 0.795 | True |  |
| `BOX(THEM(THEM))` | 0.00495 | True | False | 0 | 1.0 | 0.795 | True |  |
| `BOX1(THEM(ME))` | 0.00495 | True | False | 0 | 1.0 | 0.800 | True |  |
| `BOX1(THEM(THEM))` | 0.0049 | True | True | 0.0026 | 0.0 | 0.800 | True | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `BOX(THEM(^C))` | 0.00138 | True | True | 0.003 | 0.0 | 0.795 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `BOX1(THEM(^C))` | 0.00138 | True | True | 0.003 | 0.0 | 0.800 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `not(BOX(THEM(ME)))` | 0.00122 | True | True | 0.5 | 0.0 | 0.103 | False | `D`, `BOX(THEM(ME))` |
| `not(BOX(THEM(THEM)))` | 0.00122 | True | True | 0.5 | 0.0 | 0.103 | False | `D`, `BOXD(THEM(ME))` |
| `not(BOX1(THEM(ME)))` | 0.00122 | True | True | 0.51 | 0.0 | 0.097 | False | `D`, `BOX(THEM(ME))` |
| `not(BOX1(THEM(THEM)))` | 0.00122 | True | True | 0.49 | 0.0 | 0.097 | False | `D`, `BOXD(THEM(ME))` |
| `not(BOX(THEM(^C)))` | 0.000157 | True | True | 0.49 | 0.0 | 0.103 | False | `D`, `BOXD(THEM(ME))` |
| `not(BOX(THEM(^D)))` | 0.000157 | True | True | 0.49 | 0.0 | 0.275 | False | `D`, `BOX(THEM(ME))` |
| `not(BOXD(THEM(^C)))` | 0.000157 | True | True | 0.042 | 0.0 | 0.236 | True | `BOX(THEM(ME))`, `BOX(THEM(THEM))` |
| `not(BOX1(THEM(^C)))` | 0.000157 | True | True | 0.49 | 0.0 | 0.194 | False | `D`, `BOXD(THEM(ME))` |
| `not(BOX1(THEM(^D)))` | 0.000157 | True | True | 0.49 | 0.0 | 0.097 | False | `D`, `BOX(THEM(ME))` |
| `not(BOXD1(THEM(^C)))` | 0.000157 | True | True | 0.037 | 0.0 | 0.011 | True | `BOX(THEM(ME))`, `BOX(THEM(THEM))` |
| `BOX1(THEM(^BOX(THEM(ME))))` | 4.94e-05 | True | True | 0.0014 | 0.0 | 0.800 | True | `BOXD1(THEM(^D))` |


**Frontier (n = 6): unsuckerable self-cooperating classes, by leak**

| class | μ | universality | leak | leak not via D | ALLC-tolerant mates | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 4.95e-03 | 0.795 | 4.77e-01 | 7.71e-03 | 4.87e-01 | True | True | `C`, `BOX1(THEM(THEM))` |
| `BOX(THEM(THEM))` | 4.95e-03 | 0.795 | 4.77e-01 | 7.71e-03 | 4.87e-01 | True | True | `C`, `BOX1(THEM(THEM))` |
| `BOX1(THEM(ME))` | 4.95e-03 | 0.800 | 4.77e-01 | 7.86e-03 | 4.87e-01 | True | True | `C`, `BOX1(THEM(THEM))` |

## n = 8

- behavioural classes 471; self-cooperating 237 (μ 0.4971); components of G 1
- FairBot component: 237 classes, μ 0.0306 without ALLC (0.4971 with)
- closed components: 0, μ 0; closed components with a member that enters all-D neutrally: 0; max universality over closed classes 0
- checks: universality > 0 ⇒ in K(FB): True; K(FB) has a suckerable member: True

| component | size | μ | closed | has FB | has ALLC | suckerable members (μ) | enter all-D (μ) | max d | top members |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 237 | 0.497 | False | True | True | 228 (0.487) | 96 (0.0242) | 1.0 | `C` 0.47; `BOX1(THEM(ME))` 0.0051; `BOX(THEM(ME))` 0.0051 |

| class (top 25 by μ among self-cooperators) | μ | in K(FB) | suckerable | faker μ | d | universality | enters D | top fakers |
|---|---|---|---|---|---|---|---|---|
| `C` | 0.466 | True | True | 0.5 | 0.0 | 0.797 | False | `D`, `BOXD1(THEM(ME))` |
| `BOX1(THEM(ME))` | 0.00508 | True | False | 0 | 1.0 | 0.788 | True |  |
| `BOX(THEM(ME))` | 0.00508 | True | False | 0 | 1.0 | 0.779 | True |  |
| `BOX(THEM(THEM))` | 0.00505 | True | True | 2e-05 | 0.0 | 0.779 | True | `BOX1(THEM(^not(BOX(THEM(ME)))))`, `BOX1(THEM(^not(BOX(THEM(THEM)))))` |
| `BOX1(THEM(THEM))` | 0.00505 | True | True | 0.0029 | 0.0 | 0.787 | True | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `BOX1(THEM(^C))` | 0.00154 | True | True | 0.0034 | 0.0 | 0.788 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `BOX(THEM(^C))` | 0.00153 | True | True | 0.0034 | 0.0 | 0.778 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `not(BOX(THEM(ME)))` | 0.0013 | True | True | 0.5 | 0.0 | 0.113 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX1(THEM(ME)))` | 0.0013 | True | True | 0.51 | 0.0 | 0.104 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(THEM)))` | 0.0013 | True | True | 0.5 | 0.0 | 0.112 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX1(THEM(THEM)))` | 0.0013 | True | True | 0.49 | 0.0 | 0.103 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX(THEM(^C)))` | 0.000227 | True | True | 0.49 | 0.0 | 0.112 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX(THEM(^D)))` | 0.000227 | True | True | 0.49 | 0.0 | 0.279 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOXD(THEM(^C)))` | 0.000227 | True | True | 0.045 | 0.0 | 0.241 | True | `BOXD1(THEM(ME))`, `BOX(THEM(ME))` |
| `not(BOX1(THEM(^C)))` | 0.000227 | True | True | 0.49 | 0.0 | 0.204 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX1(THEM(^D)))` | 0.000227 | True | True | 0.49 | 0.0 | 0.104 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOXD1(THEM(^C)))` | 0.000227 | True | True | 0.04 | 0.0 | 0.019 | True | `BOX1(THEM(ME))`, `BOXD1(THEM(ME))` |
| `BOX(THEM(^BOX(THEM(THEM))))` | 3.09e-05 | True | False | 0 | 1.0 | 0.779 | True |  |
| `BOX(THEM(^BOX1(THEM(ME))))` | 3.09e-05 | True | True | 1.8e-05 | 0.0 | 0.778 | True | `BOX(THEM(^not(BOXD(THEM(ME)))))`, `BOX(THEM(^not(BOXD(THEM(THEM)))))` |
| `BOX(THEM(^BOX1(THEM(THEM))))` | 3.09e-05 | True | True | 1.8e-05 | 0.0 | 0.778 | True | `BOX(THEM(^not(BOX(THEM(ME)))))`, `BOX(THEM(^not(BOX(THEM(THEM)))))` |
| `BOX1(THEM(^BOX(THEM(ME))))` | 3.09e-05 | True | True | 0.0016 | 0.0 | 0.788 | True | `BOXD1(THEM(^D))`, `BOXD1(THEM(^not(BOXD(THEM(ME)))))` |
| `BOX1(THEM(^BOX(THEM(THEM))))` | 3.09e-05 | True | True | 0.0016 | 0.0 | 0.788 | True | `BOXD1(THEM(^D))`, `BOXD1(THEM(^not(BOXD(THEM(ME)))))` |
| `BOX1(THEM(^BOX1(THEM(THEM))))` | 3.09e-05 | True | True | 1.8e-05 | 0.0 | 0.788 | True | `BOX(THEM(^not(BOX(THEM(ME)))))`, `BOX(THEM(^not(BOX(THEM(THEM)))))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 2.28e-05 | True | False | 0 | 1.0 | 0.779 | True |  |
| `or(BOX(THEM(ME)),BOX(THEM(THEM)))` | 7.59e-06 | True | True | 2e-05 | 0.0 | 0.779 | True | `BOX1(THEM(^not(BOX(THEM(ME)))))`, `BOX1(THEM(^not(BOX(THEM(THEM)))))` |


**Frontier (n = 8): unsuckerable self-cooperating classes, by leak**

| class | μ | universality | leak | leak not via D | ALLC-tolerant mates | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 2.73e-06 | 0.102 | 3.11e-03 | 1.36e-06 | 1.09e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 1.36e-06 | 0.102 | 3.12e-03 | 1.36e-06 | 1.09e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1.36e-06 | 0.334 | 5.08e-03 | 5.08e-03 | 1.02e-02 | True | False | `BOX(THEM(THEM))`, `or(BOX(THEM(ME)),BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOX(THEM(^C)))` | 4.09e-06 | 0.778 | 4.80e-01 | 1.34e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(ME))` | 5.08e-03 | 0.779 | 4.80e-01 | 1.34e-02 | 4.85e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(THEM))))` | 3.09e-05 | 0.779 | 4.80e-01 | 1.34e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 2.28e-05 | 0.779 | 4.80e-01 | 1.34e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | 7.59e-06 | 0.779 | 4.80e-01 | 1.34e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(ME))` | 5.08e-03 | 0.788 | 4.80e-01 | 1.37e-02 | 4.85e-01 | True | True | `C`, `BOX(THEM(THEM))` |

## n = 9

- behavioural classes 863; self-cooperating 405 (μ 0.4970); components of G 1
- FairBot component: 405 classes, μ 0.0313 without ALLC (0.4970 with)
- closed components: 0, μ 0; closed components with a member that enters all-D neutrally: 0; max universality over closed classes 0
- checks: universality > 0 ⇒ in K(FB): True; K(FB) has a suckerable member: True

| component | size | μ | closed | has FB | has ALLC | suckerable members (μ) | enter all-D (μ) | max d | top members |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 405 | 0.497 | False | True | True | 392 (0.487) | 148 (0.0246) | 1.0 | `C` 0.47; `BOX1(THEM(ME))` 0.0051; `BOX(THEM(ME))` 0.0051 |

| class (top 25 by μ among self-cooperators) | μ | in K(FB) | suckerable | faker μ | d | universality | enters D | top fakers |
|---|---|---|---|---|---|---|---|---|
| `C` | 0.466 | True | True | 0.5 | 0.0 | 0.795 | False | `D`, `BOXD1(THEM(ME))` |
| `BOX1(THEM(ME))` | 0.00513 | True | False | 0 | 1.0 | 0.784 | True |  |
| `BOX(THEM(ME))` | 0.00513 | True | False | 0 | 1.0 | 0.774 | True |  |
| `BOX(THEM(THEM))` | 0.0051 | True | True | 2.8e-05 | 0.0 | 0.774 | True | `BOX1(THEM(^not(BOX(THEM(ME)))))`, `BOX1(THEM(^not(BOX(THEM(THEM)))))` |
| `BOX1(THEM(THEM))` | 0.0051 | True | True | 0.0029 | 0.0 | 0.784 | True | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `BOX1(THEM(^C))` | 0.00158 | True | True | 0.0036 | 0.0 | 0.784 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `BOX(THEM(^C))` | 0.00158 | True | True | 0.0036 | 0.0 | 0.774 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `not(BOX1(THEM(ME)))` | 0.00131 | True | True | 0.51 | 0.0 | 0.106 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(ME)))` | 0.00131 | True | True | 0.5 | 0.0 | 0.116 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(THEM)))` | 0.00131 | True | True | 0.5 | 0.0 | 0.115 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX1(THEM(THEM)))` | 0.00131 | True | True | 0.49 | 0.0 | 0.105 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX1(THEM(^D)))` | 0.000252 | True | True | 0.49 | 0.0 | 0.105 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(^C)))` | 0.000252 | True | True | 0.49 | 0.0 | 0.115 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX(THEM(^D)))` | 0.000252 | True | True | 0.49 | 0.0 | 0.280 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOXD(THEM(^C)))` | 0.000252 | True | True | 0.046 | 0.0 | 0.243 | True | `BOXD1(THEM(ME))`, `BOX(THEM(ME))` |
| `not(BOX1(THEM(^C)))` | 0.000252 | True | True | 0.49 | 0.0 | 0.206 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOXD1(THEM(^C)))` | 0.000252 | True | True | 0.041 | 0.0 | 0.023 | True | `BOX1(THEM(ME))`, `BOXD1(THEM(ME))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 3.28e-05 | True | False | 0 | 1.0 | 0.774 | True |  |
| `BOX(THEM(^BOX1(THEM(ME))))` | 3.18e-05 | True | True | 2.5e-05 | 0.0 | 0.774 | True | `BOX(THEM(^not(BOXD(THEM(ME)))))`, `BOX(THEM(^not(BOXD(THEM(THEM)))))` |
| `BOX1(THEM(^BOX(THEM(ME))))` | 3.17e-05 | True | True | 0.0016 | 0.0 | 0.784 | True | `BOXD1(THEM(^D))`, `BOXD1(THEM(^not(BOX(THEM(ME)))))` |
| `BOX(THEM(^BOX(THEM(THEM))))` | 3.16e-05 | True | False | 0 | 1.0 | 0.774 | True |  |
| `BOX(THEM(^BOX1(THEM(THEM))))` | 3.16e-05 | True | True | 2.5e-05 | 0.0 | 0.774 | True | `BOX(THEM(^not(BOX(THEM(ME)))))`, `BOX(THEM(^not(BOX(THEM(THEM)))))` |
| `BOX1(THEM(^BOX(THEM(THEM))))` | 3.16e-05 | True | True | 0.0016 | 0.0 | 0.784 | True | `BOXD1(THEM(^D))`, `BOXD1(THEM(^not(BOX(THEM(ME)))))` |
| `BOX1(THEM(^BOX1(THEM(THEM))))` | 3.16e-05 | True | True | 2.5e-05 | 0.0 | 0.784 | True | `BOX(THEM(^not(BOX(THEM(ME)))))`, `BOX(THEM(^not(BOX(THEM(THEM)))))` |
| `or(BOX(THEM(ME)),BOX(THEM(THEM)))` | 1.09e-05 | True | True | 2.8e-05 | 0.0 | 0.774 | True | `BOX1(THEM(^not(BOX(THEM(ME)))))`, `BOX1(THEM(^not(BOX(THEM(THEM)))))` |


**Frontier (n = 9): unsuckerable self-cooperating classes, by leak**

| class | μ | universality | leak | leak not via D | ALLC-tolerant mates | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 3.16e-06 | 0.103 | 3.21e-03 | 2.04e-06 | 1.63e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 1.81e-06 | 0.103 | 3.23e-03 | 2.04e-06 | 1.68e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1.58e-06 | 0.330 | 5.13e-03 | 5.13e-03 | 1.03e-02 | True | False | `BOX(THEM(THEM))`, `or(BOX(THEM(ME)),BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^D))))` | 2.28e-07 | 0.267 | 8.36e-03 | 5.15e-03 | 5.17e-03 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX(THEM(ME)),BOX(THEM(^C)))` | 4.74e-06 | 0.774 | 4.80e-01 | 1.36e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 3.28e-05 | 0.774 | 4.80e-01 | 1.36e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(ME))` | 5.13e-03 | 0.774 | 4.80e-01 | 1.36e-02 | 4.85e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(THEM))))` | 3.16e-05 | 0.774 | 4.80e-01 | 1.36e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX1(THEM(ME))))))` | 2.28e-07 | 0.774 | 4.80e-01 | 1.36e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX(THEM(THEM))))))` | 1.14e-07 | 0.774 | 4.80e-01 | 1.36e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | 1.09e-05 | 0.774 | 4.80e-01 | 1.36e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(ME))` | 5.13e-03 | 0.784 | 4.80e-01 | 1.40e-02 | 4.85e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(^BOX1(THEM(^BOX1(THEM(THEM))))))` | 1.14e-07 | 0.784 | 4.80e-01 | 1.40e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |

## n = 10

- behavioural classes 1752; self-cooperating 764 (μ 0.4969); components of G 1
- FairBot component: 764 classes, μ 0.0318 without ALLC (0.4969 with)
- closed components: 0, μ 0; closed components with a member that enters all-D neutrally: 0; max universality over closed classes 0
- checks: universality > 0 ⇒ in K(FB): True; K(FB) has a suckerable member: True

| component | size | μ | closed | has FB | has ALLC | suckerable members (μ) | enter all-D (μ) | max d | top members |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 764 | 0.497 | False | True | True | 749 (0.487) | 319 (0.0249) | 1.0 | `C` 0.47; `BOX1(THEM(ME))` 0.0051; `BOX(THEM(ME))` 0.0051 |

| class (top 25 by μ among self-cooperators) | μ | in K(FB) | suckerable | faker μ | d | universality | enters D | top fakers |
|---|---|---|---|---|---|---|---|---|
| `C` | 0.465 | True | True | 0.5 | 0.0 | 0.792 | False | `D`, `BOXD1(THEM(ME))` |
| `BOX1(THEM(ME))` | 0.00515 | True | False | 0 | 1.0 | 0.780 | True |  |
| `BOX(THEM(ME))` | 0.00515 | True | False | 0 | 1.0 | 0.769 | True |  |
| `BOX(THEM(THEM))` | 0.00511 | True | True | 3.7e-05 | 0.0 | 0.769 | True | `BOX1(THEM(^not(BOX(THEM(ME)))))`, `BOX1(THEM(^not(BOX(THEM(THEM)))))` |
| `BOX1(THEM(THEM))` | 0.00511 | True | True | 0.003 | 0.0 | 0.780 | True | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `BOX1(THEM(^C))` | 0.00163 | True | True | 0.0037 | 0.0 | 0.780 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `BOX(THEM(^C))` | 0.00162 | True | True | 0.0037 | 0.0 | 0.769 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `not(BOX1(THEM(ME)))` | 0.00134 | True | True | 0.51 | 0.0 | 0.108 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(ME)))` | 0.00134 | True | True | 0.5 | 0.0 | 0.119 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(THEM)))` | 0.00134 | True | True | 0.5 | 0.0 | 0.118 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX1(THEM(THEM)))` | 0.00134 | True | True | 0.49 | 0.0 | 0.107 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX1(THEM(^D)))` | 0.000266 | True | True | 0.49 | 0.0 | 0.108 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(^C)))` | 0.000265 | True | True | 0.49 | 0.0 | 0.118 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX(THEM(^D)))` | 0.000265 | True | True | 0.49 | 0.0 | 0.281 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOXD(THEM(^C)))` | 0.000265 | True | True | 0.046 | 0.0 | 0.245 | True | `BOXD1(THEM(ME))`, `BOX(THEM(ME))` |
| `not(BOX1(THEM(^C)))` | 0.000265 | True | True | 0.49 | 0.0 | 0.209 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOXD1(THEM(^C)))` | 0.000265 | True | True | 0.041 | 0.0 | 0.025 | True | `BOXD1(THEM(ME))`, `BOX1(THEM(ME))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 3.43e-05 | True | False | 0 | 1.0 | 0.769 | True |  |
| `BOX(THEM(^BOX1(THEM(ME))))` | 3.41e-05 | True | True | 2.8e-05 | 0.0 | 0.769 | True | `BOX(THEM(^not(BOXD(THEM(ME)))))`, `BOX(THEM(^not(BOXD(THEM(THEM)))))` |
| `BOX1(THEM(^BOX(THEM(ME))))` | 3.41e-05 | True | True | 0.0017 | 0.0 | 0.780 | True | `BOXD1(THEM(^D))`, `BOXD1(THEM(^not(BOX(THEM(THEM)))))` |
| `BOX(THEM(^BOX(THEM(THEM))))` | 3.4e-05 | True | True | 8e-08 | 0.0 | 0.769 | True | `BOX(THEM(^BOX1(THEM(^not(BOX(THEM(ME)))))))`, `BOX(THEM(^BOX1(THEM(^not(BOX(THEM(THEM)))))))` |
| `BOX(THEM(^BOX1(THEM(THEM))))` | 3.4e-05 | True | True | 2.8e-05 | 0.0 | 0.769 | True | `BOX(THEM(^not(BOX(THEM(ME)))))`, `BOX(THEM(^not(BOX(THEM(THEM)))))` |
| `BOX1(THEM(^BOX(THEM(THEM))))` | 3.4e-05 | True | True | 0.0017 | 0.0 | 0.780 | True | `BOXD1(THEM(^D))`, `BOXD1(THEM(^not(BOX(THEM(THEM)))))` |
| `BOX1(THEM(^BOX1(THEM(THEM))))` | 3.4e-05 | True | True | 2.7e-05 | 0.0 | 0.780 | True | `BOX(THEM(^not(BOX(THEM(ME)))))`, `BOX(THEM(^not(BOX(THEM(THEM)))))` |
| `not(and(BOX(THEM(ME)),BOXD(THEM(ME))))` | 1.2e-05 | True | True | 0.51 | 0.0 | 0.512 | False | `D`, `BOXD1(THEM(ME))` |


**Frontier (n = 10): unsuckerable self-cooperating classes, by leak**

| class | μ | universality | leak | leak not via D | ALLC-tolerant mates | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 4.67e-06 | 0.104 | 3.31e-03 | 2.95e-06 | 2.39e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 2.34e-06 | 0.105 | 3.35e-03 | 2.95e-06 | 2.47e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 3.07e-07 | 0.105 | 3.35e-03 | 2.95e-06 | 2.47e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 2.38e-06 | 0.326 | 5.19e-03 | 5.19e-03 | 1.04e-02 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^D))))` | 3.07e-07 | 0.267 | 8.49e-03 | 5.18e-03 | 5.20e-03 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(ME)))))` | 2.41e-07 | 0.769 | 4.79e-01 | 1.38e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^C)))` | 7.13e-06 | 0.769 | 4.79e-01 | 1.38e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 3.43e-05 | 0.769 | 4.79e-01 | 1.38e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(ME))` | 5.15e-03 | 0.769 | 4.79e-01 | 1.38e-02 | 4.84e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(THEM)))))` | 2.41e-07 | 0.769 | 4.79e-01 | 1.38e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX(THEM(THEM))))))` | 1.13e-07 | 0.769 | 4.79e-01 | 1.38e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | 1.14e-05 | 0.769 | 4.79e-01 | 1.38e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX(THEM(ME)))))` | 8.05e-08 | 0.780 | 4.80e-01 | 1.42e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(ME))` | 5.15e-03 | 0.780 | 4.80e-01 | 1.42e-02 | 4.85e-01 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX1(THEM(THEM)))))` | 8.05e-08 | 0.780 | 4.80e-01 | 1.42e-02 | 4.90e-01 | True | True | `C`, `BOX(THEM(THEM))` |

## n = 11

- behavioural classes 5545; self-cooperating 2520 (μ 0.4969); components of G 1
- FairBot component: 2520 classes, μ 0.0323 without ALLC (0.4969 with)
- closed components: 0, μ 0; closed components with a member that enters all-D neutrally: 0; max universality over closed classes 0
- checks: universality > 0 ⇒ in K(FB): True; K(FB) has a suckerable member: True

| component | size | μ | closed | has FB | has ALLC | suckerable members (μ) | enter all-D (μ) | max d | top members |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2520 | 0.497 | False | True | True | 2482 (0.486) | 1065 (0.0251) | 1.0 | `C` 0.46; `BOX1(THEM(ME))` 0.0052; `BOX(THEM(ME))` 0.0052 |

| class (top 25 by μ among self-cooperators) | μ | in K(FB) | suckerable | faker μ | d | universality | enters D | top fakers |
|---|---|---|---|---|---|---|---|---|
| `C` | 0.465 | True | True | 0.5 | 0.0 | 0.790 | False | `D`, `BOXD1(THEM(ME))` |
| `BOX1(THEM(ME))` | 0.00517 | True | False | 0 | 1.0 | 0.778 | True |  |
| `BOX(THEM(ME))` | 0.00517 | True | False | 0 | 1.0 | 0.766 | True |  |
| `BOX(THEM(THEM))` | 0.00513 | True | True | 4.5e-05 | 0.0 | 0.766 | True | `BOX1(THEM(^not(BOX(THEM(ME)))))`, `BOX1(THEM(^not(BOX(THEM(THEM)))))` |
| `BOX1(THEM(THEM))` | 0.00513 | True | True | 0.0031 | 0.0 | 0.777 | True | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `BOX1(THEM(^C))` | 0.00166 | True | True | 0.0038 | 0.0 | 0.778 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `BOX(THEM(^C))` | 0.00165 | True | True | 0.0038 | 0.0 | 0.766 | True | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `not(BOX1(THEM(ME)))` | 0.00135 | True | True | 0.51 | 0.0 | 0.110 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(ME)))` | 0.00135 | True | True | 0.5 | 0.0 | 0.121 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(THEM)))` | 0.00135 | True | True | 0.5 | 0.0 | 0.120 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX1(THEM(THEM)))` | 0.00135 | True | True | 0.49 | 0.0 | 0.108 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX1(THEM(^D)))` | 0.00028 | True | True | 0.49 | 0.0 | 0.109 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOX(THEM(^C)))` | 0.000279 | True | True | 0.49 | 0.0 | 0.120 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOX(THEM(^D)))` | 0.000279 | True | True | 0.49 | 0.0 | 0.282 | False | `D`, `BOX1(THEM(ME))` |
| `not(BOXD(THEM(^C)))` | 0.000279 | True | True | 0.047 | 0.0 | 0.247 | True | `BOXD1(THEM(ME))`, `BOX(THEM(ME))` |
| `not(BOX1(THEM(^C)))` | 0.000279 | True | True | 0.49 | 0.0 | 0.211 | False | `D`, `BOXD1(THEM(ME))` |
| `not(BOXD1(THEM(^C)))` | 0.000279 | True | True | 0.042 | 0.0 | 0.027 | True | `BOXD1(THEM(ME))`, `BOX1(THEM(ME))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 3.94e-05 | True | False | 0 | 1.0 | 0.766 | True |  |
| `BOX(THEM(^BOX1(THEM(ME))))` | 3.48e-05 | True | True | 3.2e-05 | 0.0 | 0.766 | True | `BOX(THEM(^not(BOXD(THEM(ME)))))`, `BOX1(THEM(^not(BOXD(THEM(ME)))))` |
| `BOX1(THEM(^BOX(THEM(ME))))` | 3.47e-05 | True | True | 0.0017 | 0.0 | 0.778 | True | `BOXD1(THEM(^D))`, `BOXD1(THEM(^not(BOX(THEM(ME)))))` |
| `BOX(THEM(^BOX1(THEM(THEM))))` | 3.46e-05 | True | True | 3.2e-05 | 0.0 | 0.766 | True | `BOX(THEM(^not(BOX(THEM(ME)))))`, `BOX1(THEM(^not(BOX(THEM(ME)))))` |
| `BOX1(THEM(^BOX1(THEM(THEM))))` | 3.46e-05 | True | True | 3.1e-05 | 0.0 | 0.778 | True | `BOX(THEM(^not(BOX(THEM(ME)))))`, `BOX1(THEM(^not(BOX(THEM(ME)))))` |
| `BOX(THEM(^BOX(THEM(THEM))))` | 3.46e-05 | True | True | 2.1e-07 | 0.0 | 0.766 | True | `BOX(THEM(^BOX1(THEM(^not(BOX(THEM(ME)))))))`, `BOX(THEM(^BOX1(THEM(^not(BOX(THEM(THEM)))))))` |
| `BOX1(THEM(^BOX(THEM(THEM))))` | 3.46e-05 | True | True | 0.0017 | 0.0 | 0.778 | True | `BOXD1(THEM(^D))`, `BOXD1(THEM(^not(BOX(THEM(ME)))))` |
| `not(and(BOX(THEM(ME)),BOXD(THEM(ME))))` | 1.47e-05 | True | True | 0.51 | 0.0 | 0.513 | False | `D`, `BOXD1(THEM(ME))` |


**Frontier (n = 11): unsuckerable self-cooperating classes, by leak**

| class | μ | universality | leak | leak not via D | ALLC-tolerant mates | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 2.59e-06 | 0.105 | 3.38e-03 | 3.61e-06 | 2.94e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` | 2.59e-06 | 0.105 | 3.38e-03 | 3.61e-06 | 2.94e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 2.59e-06 | 0.106 | 3.42e-03 | 3.61e-06 | 3.05e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 4.79e-07 | 0.106 | 3.42e-03 | 3.61e-06 | 3.05e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(THEM))))))` | 6.96e-09 | 0.107 | 3.43e-03 | 3.61e-06 | 3.53e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(ME))))))` | 6.96e-09 | 0.107 | 3.44e-03 | 1.91e-05 | 5.19e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(THEM))))))` | 6.96e-09 | 0.107 | 3.44e-03 | 1.91e-05 | 5.19e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(ME))))))` | 6.96e-09 | 0.107 | 3.44e-03 | 1.90e-05 | 5.08e-05 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(ME))))))` | 6.96e-09 | 0.322 | 5.20e-03 | 5.20e-03 | 1.04e-02 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(ME))))))` | 6.96e-09 | 0.323 | 5.20e-03 | 5.20e-03 | 1.04e-02 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(THEM))))))` | 6.96e-09 | 0.323 | 5.21e-03 | 5.21e-03 | 1.04e-02 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(THEM))))))` | 6.96e-09 | 0.323 | 5.21e-03 | 5.21e-03 | 1.04e-02 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD(THEM(ME))))))` | 1.39e-08 | 0.323 | 5.22e-03 | 5.21e-03 | 1.04e-02 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(THEM))))))` | 6.96e-09 | 0.323 | 5.22e-03 | 5.21e-03 | 1.04e-02 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(ME))))))` | 6.96e-09 | 0.323 | 5.22e-03 | 5.22e-03 | 1.04e-02 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 2.65e-06 | 0.323 | 5.22e-03 | 5.22e-03 | 1.04e-02 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |


**Prudence ladder against L_9 (boxes up to PA + Con^1; candidates at prior mass 0)**

| candidate | size | self-cooperates | suckerable | universality | leak | ALLC-tolerant mates | coop FB | top leaks |
|---|---|---|---|---|---|---|---|---|
| FairBot (order 0) | 3 | yes | False | 0.774 | 4.80e-01 | 4.85e-01 | True | `C`, `BOX(THEM(THEM))` |
| PrudentBot (order 1: defect on D-cooperators) | 8 | yes | False | 0.330 | 5.13e-03 | 1.03e-02 | True | `BOX(THEM(THEM))`, `or(BOX(THEM(ME)),BOX(THEM(THEM)))` |
| P2 = and(BOX1(TM),not(BOX(^C))) (order 2: defect on ALLC-cooperators) | 9 | yes | False | 0.103 | 3.23e-03 | 1.68e-05 | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| P* = and(BOX1(TM),not(BOX(TM))) | 8 | yes | False | 0.103 | 3.21e-03 | 1.63e-05 | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| P12 = and(P2, BOXD1(^D)) (orders 1 and 2) | 14 | no | | | | | | |
| P*1 = and(P*, BOXD1(^D)) | 13 | no | | | | | | |
| PB_BTT = and(PB, not(BOX(^BOX(TT)))) (order 1 plus: defect on cooperators of the self-prover) | 15 | no | | | | | | |


**Prudence ladder against L_10 (boxes up to PA + Con^1; candidates at prior mass 0)**

| candidate | size | self-cooperates | suckerable | universality | leak | ALLC-tolerant mates | coop FB | top leaks |
|---|---|---|---|---|---|---|---|---|
| FairBot (order 0) | 3 | yes | False | 0.769 | 4.79e-01 | 4.84e-01 | True | `C`, `BOX(THEM(THEM))` |
| PrudentBot (order 1: defect on D-cooperators) | 8 | yes | False | 0.326 | 5.19e-03 | 1.04e-02 | True | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| P2 = and(BOX1(TM),not(BOX(^C))) (order 2: defect on ALLC-cooperators) | 9 | yes | False | 0.105 | 3.35e-03 | 2.47e-05 | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| P* = and(BOX1(TM),not(BOX(TM))) | 8 | yes | False | 0.104 | 3.31e-03 | 2.39e-05 | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| P12 = and(P2, BOXD1(^D)) (orders 1 and 2) | 14 | no | | | | | | |
| P*1 = and(P*, BOXD1(^D)) | 13 | no | | | | | | |
| PB_BTT = and(PB, not(BOX(^BOX(TT)))) (order 1 plus: defect on cooperators of the self-prover) | 15 | no | | | | | | |


**Prudence ladder against L_8 (boxes up to PA + Con^2; candidates at prior mass 0)**

| candidate | size | self-cooperates | suckerable | universality | leak | ALLC-tolerant mates | coop FB | top leaks |
|---|---|---|---|---|---|---|---|---|
| FairBot (order 0) | 3 | yes | False | 0.777 | 4.75e-01 | 4.84e-01 | True | `C`, `BOX(THEM(THEM))` |
| PrudentBot (order 1: defect on D-cooperators) | 8 | yes | False | 0.220 | 4.15e-03 | 8.35e-03 | True | `BOX(THEM(THEM))`, `or(BOX(THEM(ME)),BOX(THEM(THEM)))` |
| P2 = and(BOX1(TM),not(BOX(^C))) (order 2: defect on ALLC-cooperators) | 9 | yes | False | 0.068 | 2.59e-03 | 1.22e-05 | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| P* = and(BOX1(TM),not(BOX(TM))) | 8 | yes | False | 0.068 | 2.57e-03 | 1.22e-05 | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| P12 = and(P2, BOXD1(^D)) (orders 1 and 2) | 14 | no | | | | | | |
| P*1 = and(P*, BOXD1(^D)) | 13 | no | | | | | | |
| PB_BTT = and(PB, not(BOX(^BOX(TT)))) (order 1 plus: defect on cooperators of the self-prover) | 15 | no | | | | | | |
| PB2 = and(BOX(TM), BOXD2(^D)) | 8 | yes | False | 0.443 | 8.44e-03 | 1.68e-02 | True | `BOX(THEM(THEM))`, `BOX1(THEM(THEM))` |
| P12b = and(P2, BOXD2(^D)) (orders 1 and 2, PA+2) | 14 | yes | False | 0.000 | 2.04e-06 | 0.00e+00 | False | `and(BOX1(THEM(THEM)),not(BOX(THEM(ME))))`, `and(BOX1(THEM(THEM)),BOXD2(THEM(^D)))` |
| P*1b = and(P*, BOXD2(^D)) (PA+2) | 13 | yes | False | 0.000 | 1.02e-06 | 0.00e+00 | False | `and(BOX1(THEM(THEM)),not(BOX(THEM(ME))))` |
| PB_BTTb = and(PB, not(BOX1(^BOX(TT)))) (PA+2 not needed?) | 15 | no | | | | | | |
| P2D2 = and(BOX2(TM), not(BOX1(^C)), BOXD2(^D)) | 14 | no | | | | | | |


**Prudence ladder against L_9 (boxes up to PA + Con^2; candidates at prior mass 0)**

| candidate | size | self-cooperates | suckerable | universality | leak | ALLC-tolerant mates | coop FB | top leaks |
|---|---|---|---|---|---|---|---|---|
| FairBot (order 0) | 3 | yes | False | 0.773 | 4.75e-01 | 4.83e-01 | True | `C`, `BOX(THEM(THEM))` |
| PrudentBot (order 1: defect on D-cooperators) | 8 | yes | False | 0.217 | 4.19e-03 | 8.44e-03 | True | `BOX(THEM(THEM))`, `or(BOX(THEM(ME)),BOX(THEM(THEM)))` |
| P2 = and(BOX1(TM),not(BOX(^C))) (order 2: defect on ALLC-cooperators) | 9 | yes | False | 0.069 | 2.69e-03 | 1.84e-05 | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| P* = and(BOX1(TM),not(BOX(TM))) | 8 | yes | False | 0.068 | 2.66e-03 | 1.81e-05 | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| P12 = and(P2, BOXD1(^D)) (orders 1 and 2) | 14 | no | | | | | | |
| P*1 = and(P*, BOXD1(^D)) | 13 | no | | | | | | |
| PB_BTT = and(PB, not(BOX(^BOX(TT)))) (order 1 plus: defect on cooperators of the self-prover) | 15 | no | | | | | | |
| PB2 = and(BOX(TM), BOXD2(^D)) | 8 | yes | False | 0.437 | 8.53e-03 | 1.70e-02 | True | `BOX(THEM(THEM))`, `BOX1(THEM(THEM))` |
| P12b = and(P2, BOXD2(^D)) (orders 1 and 2, PA+2) | 14 | yes | False | 0.000 | 2.69e-06 | 0.00e+00 | False | `and(BOX1(THEM(THEM)),not(BOX(THEM(ME))))`, `and(BOX1(THEM(THEM)),BOXD2(THEM(^D)))` |
| P*1b = and(P*, BOXD2(^D)) (PA+2) | 13 | yes | False | 0.000 | 1.51e-06 | 0.00e+00 | False | `and(BOX1(THEM(THEM)),not(BOX(THEM(ME))))`, `and(BOX1(THEM(THEM)),not(BOX(THEM(^C))))` |
| PB_BTTb = and(PB, not(BOX1(^BOX(TT)))) (PA+2 not needed?) | 15 | no | | | | | | |
| P2D2 = and(BOX2(TM), not(BOX1(^C)), BOXD2(^D)) | 14 | no | | | | | | |
