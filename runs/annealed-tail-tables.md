## Main grid: endpoint V* by (arm, start, t0, Lam)

Cells are V* (the F share) and the class of the endpoint (F = V*-dominated, U = unequal-dominated); a star marks the burst or censored
protocol (the tail was still delivering more than 1e-4 arrivals per island when criterion (a) held, or the cap bound), "-" = not run.
Lam = 0 is the tail-free object (V1).

**M0 nat**

| series | 0 | 0.01 | 0.03 | 0.1 | 0.3 | 1 | 3 | 10 | 30 | 100 | 300 | 1000 | 10000 | 100000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t0=1 | 0.1004 U | - | - | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U* | - |
| t0=100 | 0.1004 U | - | - | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* |
| t0=10000 | 0.1004 U | - | - | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | - | - | - |

**L0 nat**

| series | 0 | 0.01 | 0.03 | 0.1 | 0.3 | 1 | 3 | 10 | 30 | 100 | 300 | 1000 | 10000 | 100000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t0=1 | 0.9997 F | - | - | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F* | 0.9997 F* |
| t0=100 | 0.9997 F | - | - | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F | 0.9997 F* | 0.9997 F* | 0.9997 F* | 0.9997 F* | 0.9997 F* | -0.0000 U* |
| t0=10000 | 0.9997 F | - | - | 0.9997 F | 0.9997 F* | 0.9997 F* | 0.9997 F* | 0.9997 F* | 0.9997 F* | 0.9997 F* | 0.9997 F* | - | - | - |

**M0 u:0.6**

| series | 0 | 0.01 | 0.03 | 0.1 | 0.3 | 1 | 3 | 10 | 30 | 100 | 300 | 1000 | 10000 | 100000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t0=1 | 0.1004 U | - | - | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | - | - | - |
| t0=100 | 0.1004 U | - | - | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | - | - | - |
| t0=10000 | 0.1004 U | - | - | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | - | - | - |

**L0 u:0.6**

| series | 0 | 0.01 | 0.03 | 0.1 | 0.3 | 1 | 3 | 10 | 30 | 100 | 300 | 1000 | 10000 | 100000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t0=1 | -0.0000 U | - | - | 0.0000 U | 0.0000 U | 0.0000 U | 0.0000 U | 0.0000 U | 0.0000 U | 0.0000 U | 0.0000 U | - | - | - |
| t0=100 | -0.0000 U | - | - | 0.0000 U | 0.0000 U | 0.0000 U | 0.0000 U | 0.0000 U | -0.0000 U* | -0.0000 U* | -0.0000 U* | - | - | - |
| t0=10000 | -0.0000 U | - | - | 0.0000 U | 0.0000 U* | 0.0000 U* | -0.0000 U* | -0.0000 U* | 0.0000 U* | 0.0000 U* | 0.0000 U* | - | - | - |

**Thresholds (first Lam on the grid, ascending, whose endpoint crosses V* = 0.5)**

| arm, start | t0 | rescue Lam* (V* >= 0.5 from a start below) | harm Lam (V* < 0.5 from a start above) | max Lam tested |
|---|---|---|---|---|
| M0 nat | 1 | none | - | 10000 |
| M0 nat | 100 | none | - | 100000 |
| M0 nat | 10000 | none | - | 300 |
| L0 nat | 1 | - | none | 100000 |
| L0 nat | 100 | - | 31622.8 | 100000 |
| L0 nat | 10000 | - | none | 300 |
| M0 u:0.6 | 1 | none | - | 300 |
| M0 u:0.6 | 100 | none | - | 300 |
| M0 u:0.6 | 10000 | none | - | 300 |
| L0 u:0.6 | 1 | none | - | 300 |
| L0 u:0.6 | 100 | none | - | 300 |
| L0 u:0.6 | 10000 | none | - | 300 |

**Non-monotone series (a decrease of endpoint V* by more than 0.01 between adjacent grid points)**

- ('L0', 'nat', 100.0): 23713.7 -> 31622.8: 0.9997 -> -0.0000

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = 316.22776601683796, bracket [273.8419634264361, 316.22776601683796], evaluations {'316.22776601683796': 0.9999999815271055, '177.82794100389228': 0.10040966506222193, '237.13737056616552': 0.1004096650633924, '273.8419634264361': 0.1004096650623789}

**Bisection** (mode harm, series "L0" nat t0=100.0): Lam* = 31622.776601683792, bracket [23713.737056616552, 31622.776601683792], evaluations {'31622.776601683792': -6.40262962622179e-22, '17782.794100389227': 0.9997368893257242, '23713.737056616552': 0.9997368888316123}

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = 86.59643233600653, bracket [74.98942093324558, 86.59643233600653], evaluations {'31.622776601683793': 0.10040966506316124, '56.23413251903491': 0.10040966506410383, '74.98942093324558': 0.10040966506332444, '86.59643233600653': 0.9999999816294854}

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = 56.23413251903491, bracket [48.696752516586315, 56.23413251903491], evaluations {'31.622776601683793': 0.10040966506193862, '56.23413251903491': 0.9999999816034874, '42.169650342858226': 0.10040966506171108, '48.696752516586315': 0.10040966506225728}

## Late tail: from M's tail-free state at tau = t_s = 1e6

Tail-free state at t_s: class shares F/U/G/W/D = [0.100399, 0.899521, 8e-05, 0.0, 1e-06]; donor marginal mass of the nine constants in slot 0 (action index 0..8):

`[6.6e-18, -2.66e-17, -4.15e-18, -7.37e-18, 1.42e-17, 2.08e-18, 0.000104, -6.96e-19, -3.34e-18]`

Offering constants (name the underpaid member at 1/3 or 1/2) and the exit constant (names the excluded slot at 1/2) are at 1e-17 or below;
the baseline donor supply is zero, so the baseline-zero rerun is vacuous (same state).

**M0 late (V*)**

| series | 0 | 0.01 | 0.03 | 0.1 | 0.3 | 1 | 3 | 10 | 30 | 100 | 300 | 1000 | 10000 | 100000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| late t0=1 | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | - |
| late t0=100 | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | - | - | - |
| late t0=10000 | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | - | - | - |

**Small-Lam response of the late tail** (endpoint V* minus the tail-free V*, Lam in 0.01, 0.03, 0.1, 0.3):

- t0=1: 0.01: -7.76e-06, 0.03: -7.76e-06, 0.1: -7.76e-06, 0.3: -7.76e-06
- t0=100: 0.01: -7.76e-06, 0.03: -7.76e-06, 0.1: -7.76e-06, 0.3: -9.50e-07
- t0=10000: 0.01: -5.66e-07, 0.03: -3.10e-07, 0.1: -1.52e-07, 0.3: -6.49e-08

## Constant rain: eps = Lam/1e4 on [0, 1e4], M natural

**M0 nat, constant rain**

| series | 0 | 0.01 | 0.03 | 0.1 | 0.3 | 1 | 3 | 10 | 30 | 100 | 300 | 1000 | 10000 | 100000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rain T=1e4 | - | - | - | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | - | - | - |

## Arm T (27 programs), main dose

**arm T endpoint V***

| series | 0.1 | 0.3 | 1 | 3 | 10 | 30 | 100 | 300 | 1000 | 10000 |
|---|---|---|---|---|---|---|---|---|---|---|
| main|0.1|0 nat t0=1 | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F* | - |
| main|0.1|0 nat t0=100 | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* |
| main|0.1|0 nat t0=10000 | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | - | - |
| main|0.1|0 u:0.8 t0=1 | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F* | - |
| main|0.1|0 u:0.8 t0=100 | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | - |
| main|0.1|0 u:0.8 t0=10000 | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | - | - |
| main|0|0 nat t0=1 | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F* | - |
| main|0|0 nat t0=100 | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | - |
| main|0|0 nat t0=10000 | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | - | - |
| main|0|0 u:0.8 t0=1 | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F* | - |
| main|0|0 u:0.8 t0=100 | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | - |
| main|0|0 u:0.8 t0=10000 | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | 1.0000 F* | - | - |

Minimum endpoint V* per series: {"main|0.1|0 nat t0=1": 1.0, "main|0.1|0 nat t0=100": 0.999993, "main|0.1|0 nat t0=10000": 1.0, "main|0.1|0 u:0.8 t0=1": 1.0, "main|0.1|0 u:0.8 t0=100": 1.0, "main|0.1|0 u:0.8 t0=10000": 1.0, "main|0|0 nat t0=1": 1.0, "main|0|0 nat t0=100": 1.0, "main|0|0 nat t0=10000": 1.0, "main|0|0 u:0.8 t0=1": 1.0, "main|0|0 u:0.8 t0=100": 1.0, "main|0|0 u:0.8 t0=10000": 1.0}

## Attribution (M natural, t0 = 100)

**Lam = 0** (status capped, V* at the end of the integration 0.1002)

- integrated to tau = 1000. direct tail flux by class transition: {}
  migrant flux by class transition: {'W->F': 0.2143, 'U->F': 0.187, 'W->U': 0.1791, 'F->U': 0.1419, 'U->W': 0.1115, 'F->W': 0.05724, 'D->U': 0.02893, 'D->W': 0.02499}
  U->F by arriving family: tail {}; migrants {'c1': 0.0917, 'c4': 0.0917, 'other-cond': 0.00303, 'fair-reader': 0.000325, 'exploiter': 0.000153}
  F->U by arriving family: tail {}; migrants {'c2': 0.0679, 'c5': 0.0679, 'other-cond': 0.00255, 'c0': 0.00141, 'c3': 0.00141}
  F->W by arriving family: tail {}; migrants {'c1': 0.0206, 'c4': 0.0206, 'c0': 0.00745, 'c3': 0.00745, 'other-cond': 0.000928}
  W->U by arriving family: tail {}; migrants {'c2': 0.0853, 'c5': 0.0853, 'other-cond': 0.00334, 'c0': 0.00217, 'c3': 0.00217}
  U->F migrants flux by source category: {'E-offers': 0.179, 'E-other': 0.00786}
- integrated to tau = 10000. direct tail flux by class transition: {}
  migrant flux by class transition: {'U->F': 0.9484, 'W->F': 0.5876, 'F->U': 0.5172, 'F->W': 0.3352, 'U->W': 0.2753, 'W->U': 0.2716, 'D->U': 0.03029, 'D->F': 0.02687}
  U->F by arriving family: tail {}; migrants {'c1': 0.461, 'c4': 0.461, 'other-cond': 0.0112, 'exploiter': 0.00721, 'fair-reader': 0.00633}
  F->U by arriving family: tail {}; migrants {'c2': 0.194, 'c5': 0.194, 'exploiter': 0.0374, 'yielder': 0.0354, 'c0': 0.0238}
  F->W by arriving family: tail {}; migrants {'c1': 0.133, 'c4': 0.133, 'c0': 0.0307, 'c3': 0.0307, 'other-cond': 0.00399}
  W->U by arriving family: tail {}; migrants {'c2': 0.128, 'c5': 0.128, 'other-cond': 0.0048, 'exploiter': 0.00377, 'c0': 0.00329}
  U->F migrants flux by source category: {'E-offers': 0.892, 'E-other': 0.0564}
- integrated to tau = 100000. direct tail flux by class transition: {}
  migrant flux by class transition: {'F->U': 109.8, 'U->F': 109.3, 'W->F': 0.5903, 'F->W': 0.3374, 'U->W': 0.2763, 'W->U': 0.2722, 'D->U': 0.03158, 'D->F': 0.03094}
  U->F by arriving family: tail {}; migrants {'exploiter': 58.6, 'yielder': 48.9, 'c1': 0.822, 'c4': 0.822, 'fair-reader': 0.0995}
  F->U by arriving family: tail {}; migrants {'yielder': 73.5, 'exploiter': 35.8, 'c2': 0.194, 'c5': 0.194, 'c0': 0.025}
  F->W by arriving family: tail {}; migrants {'c1': 0.133, 'c4': 0.133, 'c0': 0.0308, 'c3': 0.0308, 'exploiter': 0.00401}
  W->U by arriving family: tail {}; migrants {'c2': 0.128, 'c5': 0.128, 'other-cond': 0.0048, 'exploiter': 0.00418, 'c0': 0.00329}
  U->F migrants flux by source category: {'E-offers': 1.6, 'E-other': 108.0}

**Lam = 10000** (status capped, V* at the end of the integration 0.1001)

- integrated to tau = 1000. direct tail flux by class transition: {'F->U': 0.8863, 'U->W': 0.7115, 'U->F': 0.7051, 'W->U': 0.6748, 'W->F': 0.558, 'F->W': 0.2901, 'D->U': 0.054, 'D->W': 0.04184}
  migrant flux by class transition: {'F->U': 0.1314, 'U->F': 0.1299, 'U->W': 0.1098, 'W->F': 0.08251, 'W->U': 0.08061, 'F->W': 0.04564, 'U->D': 0.00375, 'D->U': 0.003248}
  U->F by arriving family: tail {'c1': 0.344, 'c4': 0.344, 'other-cond': 0.0148, 'fair-reader': 0.00102, 'exploiter': 0.000223}; migrants {'c1': 0.0637, 'c4': 0.0637, 'other-cond': 0.00221, 'fair-reader': 0.000267, 'exploiter': 8.3e-05}
  F->U by arriving family: tail {'c2': 0.426, 'c5': 0.426, 'other-cond': 0.0185, 'c0': 0.00739, 'c3': 0.00739}; migrants {'c2': 0.0633, 'c5': 0.0633, 'other-cond': 0.00231, 'c0': 0.00101, 'c3': 0.00101}
  F->W by arriving family: tail {'c1': 0.0874, 'c4': 0.0874, 'c0': 0.0533, 'c3': 0.0533, 'other-cond': 0.00634}; migrants {'c1': 0.0155, 'c4': 0.0155, 'c0': 0.00682, 'c3': 0.00682, 'other-cond': 0.00076}
  W->U by arriving family: tail {'c2': 0.32, 'c5': 0.32, 'other-cond': 0.014, 'c0': 0.00969, 'c3': 0.00969}; migrants {'c2': 0.0384, 'c5': 0.0384, 'other-cond': 0.00141, 'c0': 0.00107, 'c3': 0.00107}
  U->F tail flux by source category: {'E-offers': 0.675, 'E-other': 0.0305}
  U->F migrants flux by source category: {'E-offers': 0.124, 'E-other': 0.00564}
- integrated to tau = 10000. direct tail flux by class transition: {'F->U': 0.9896, 'U->F': 0.7694, 'U->W': 0.7552, 'W->U': 0.7116, 'W->F': 0.5924, 'F->W': 0.3214, 'D->U': 0.05505, 'D->W': 0.04266}
  migrant flux by class transition: {'U->F': 1.278, 'F->U': 0.9155, 'W->F': 0.6593, 'F->W': 0.4642, 'U->W': 0.4313, 'W->U': 0.2763, 'U->D': 0.01179, 'D->F': 0.01026}
  U->F by arriving family: tail {'c1': 0.376, 'c4': 0.376, 'other-cond': 0.0161, 'fair-reader': 0.00111, 'exploiter': 0.000244}; migrants {'c1': 0.608, 'c4': 0.608, 'exploiter': 0.0227, 'fair-reader': 0.0205, 'other-cond': 0.0138}
  F->U by arriving family: tail {'c2': 0.465, 'c5': 0.465, 'other-cond': 0.0202, 'c0': 0.0185, 'c3': 0.0185}; migrants {'c2': 0.294, 'c5': 0.294, 'yielder': 0.103, 'exploiter': 0.1, 'c0': 0.0562}
  F->W by arriving family: tail {'c1': 0.0952, 'c4': 0.0952, 'c0': 0.0608, 'c3': 0.0608, 'other-cond': 0.00703}; migrants {'c1': 0.181, 'c4': 0.181, 'c0': 0.0434, 'c3': 0.0434, 'exploiter': 0.00769}
  W->U by arriving family: tail {'c2': 0.337, 'c5': 0.337, 'other-cond': 0.0147, 'c0': 0.0103, 'c3': 0.0103}; migrants {'c2': 0.128, 'c5': 0.128, 'exploiter': 0.00785, 'other-cond': 0.00439, 'c0': 0.00364}
  U->F tail flux by source category: {'E-offers': 0.736, 'E-other': 0.0338}
  U->F migrants flux by source category: {'E-offers': 1.17, 'E-other': 0.111}
- integrated to tau = 100000. direct tail flux by class transition: {'F->U': 1.044, 'U->F': 0.7915, 'U->W': 0.7594, 'W->U': 0.7117, 'W->F': 0.5925, 'F->W': 0.3222, 'D->U': 0.05505, 'D->W': 0.04266}
  migrant flux by class transition: {'F->U': 110.8, 'U->F': 110.1, 'W->F': 0.7528, 'U->W': 0.5743, 'F->W': 0.4865, 'W->U': 0.3551, 'U->D': 0.01684, 'D->F': 0.01493}
  U->F by arriving family: tail {'c1': 0.387, 'c4': 0.387, 'other-cond': 0.0161, 'fair-reader': 0.00111, 'exploiter': 0.00025}; migrants {'exploiter': 59.0, 'yielder': 49.1, 'c1': 0.944, 'c4': 0.944, 'fair-reader': 0.0902}
  F->U by arriving family: tail {'c2': 0.473, 'c5': 0.473, 'c0': 0.0381, 'c3': 0.0381, 'other-cond': 0.0202}; migrants {'yielder': 73.8, 'exploiter': 36.0, 'c2': 0.322, 'c5': 0.322, 'c0': 0.201}
  F->W by arriving family: tail {'c1': 0.0952, 'c4': 0.0952, 'c0': 0.0611, 'c3': 0.0611, 'other-cond': 0.00703}; migrants {'c1': 0.185, 'c4': 0.185, 'c0': 0.0458, 'c3': 0.0458, 'exploiter': 0.0124}
  W->U by arriving family: tail {'c2': 0.337, 'c5': 0.337, 'other-cond': 0.0147, 'c0': 0.0104, 'c3': 0.0104}; migrants {'c2': 0.128, 'c5': 0.128, 'exploiter': 0.0609, 'yielder': 0.0253, 'other-cond': 0.00439}
  U->F tail flux by source category: {'E-offers': 0.737, 'E-other': 0.0548}
  U->F migrants flux by source category: {'E-offers': 1.86, 'E-other': 108.0}

**Lam = 100** (status capped, V* at the end of the integration 0.1002)

- integrated to tau = 1000. direct tail flux by class transition: {'W->U': 0.03066, 'W->F': 0.02256, 'F->U': 0.009961, 'D->U': 0.008515, 'U->F': 0.008346, 'U->W': 0.007744, 'D->W': 0.00696, 'D->F': 0.004955}
  migrant flux by class transition: {'W->F': 0.189, 'U->F': 0.1821, 'W->U': 0.1589, 'F->U': 0.1402, 'U->W': 0.1102, 'F->W': 0.05543, 'D->U': 0.02161, 'D->W': 0.0182}
  U->F by arriving family: tail {'c1': 0.00408, 'c4': 0.00408, 'other-cond': 0.000175, 'fair-reader': 1.2e-05, 'exploiter': 2.64e-06}; migrants {'c1': 0.0893, 'c4': 0.0893, 'other-cond': 0.00296, 'fair-reader': 0.000321, 'exploiter': 0.000147}
  F->U by arriving family: tail {'c2': 0.00478, 'c5': 0.00478, 'other-cond': 0.000207, 'c0': 8.28e-05, 'c3': 8.28e-05}; migrants {'c2': 0.0671, 'c5': 0.0671, 'other-cond': 0.00251, 'c0': 0.00138, 'c3': 0.00138}
  F->W by arriving family: tail {'c1': 0.000987, 'c4': 0.000987, 'c0': 0.000525, 'c3': 0.000525, 'other-cond': 6.75e-05}; migrants {'c1': 0.0198, 'c4': 0.0198, 'c0': 0.00738, 'c3': 0.00738, 'other-cond': 0.000896}
  W->U by arriving family: tail {'c2': 0.0146, 'c5': 0.0146, 'other-cond': 0.000636, 'c0': 0.000338, 'c3': 0.000338}; migrants {'c2': 0.0757, 'c5': 0.0757, 'other-cond': 0.00295, 'c0': 0.00194, 'c3': 0.00194}
  U->F tail flux by source category: {'E-other': 0.000344, 'E-offers': 0.008}
  U->F migrants flux by source category: {'E-offers': 0.174, 'E-other': 0.00766}
- integrated to tau = 10000. direct tail flux by class transition: {'W->U': 0.03093, 'W->F': 0.02284, 'F->U': 0.01097, 'U->F': 0.008923, 'D->U': 0.008521, 'U->W': 0.008043, 'D->W': 0.006965, 'D->F': 0.004959}
  migrant flux by class transition: {'U->F': 0.9757, 'W->F': 0.5736, 'F->U': 0.5473, 'F->W': 0.341, 'U->W': 0.2834, 'W->U': 0.2573, 'D->U': 0.02307, 'D->F': 0.02112}
  U->F by arriving family: tail {'c1': 0.00436, 'c4': 0.00436, 'other-cond': 0.000187, 'fair-reader': 1.29e-05, 'exploiter': 2.82e-06}; migrants {'c1': 0.474, 'c4': 0.474, 'other-cond': 0.0113, 'exploiter': 0.00818, 'fair-reader': 0.00742}
  F->U by arriving family: tail {'c2': 0.00514, 'c5': 0.00514, 'c0': 0.000222, 'c3': 0.000222, 'other-cond': 0.000222}; migrants {'c2': 0.2, 'c5': 0.2, 'yielder': 0.044, 'exploiter': 0.044, 'c0': 0.0254}
  F->W by arriving family: tail {'c1': 0.00106, 'c4': 0.00106, 'c0': 0.000619, 'c3': 0.000619, 'other-cond': 7.48e-05}; migrants {'c1': 0.135, 'c4': 0.135, 'c0': 0.0314, 'c3': 0.0314, 'other-cond': 0.00402}
  W->U by arriving family: tail {'c2': 0.0148, 'c5': 0.0148, 'other-cond': 0.000642, 'c0': 0.000343, 'c3': 0.000343}; migrants {'c2': 0.121, 'c5': 0.121, 'other-cond': 0.00449, 'exploiter': 0.00391, 'c0': 0.00315}
  U->F tail flux by source category: {'E-other': 0.000372, 'E-offers': 0.00855}
  U->F migrants flux by source category: {'E-offers': 0.915, 'E-other': 0.0603}
- integrated to tau = 100000. direct tail flux by class transition: {'W->U': 0.03093, 'W->F': 0.02284, 'F->U': 0.01151, 'U->F': 0.009131, 'D->U': 0.008521, 'U->W': 0.008082, 'D->W': 0.006965, 'D->F': 0.004959}
  migrant flux by class transition: {'F->U': 110.2, 'U->F': 109.6, 'W->F': 0.5774, 'F->W': 0.3435, 'U->W': 0.2859, 'W->U': 0.2588, 'D->F': 0.02527, 'D->U': 0.0244}
  U->F by arriving family: tail {'c1': 0.00446, 'c4': 0.00446, 'other-cond': 0.000187, 'fair-reader': 1.29e-05, 'exploiter': 2.88e-06}; migrants {'exploiter': 58.8, 'yielder': 49.0, 'c1': 0.842, 'c4': 0.842, 'fair-reader': 0.0969}
  F->U by arriving family: tail {'c2': 0.00522, 'c5': 0.00522, 'c0': 0.000413, 'c3': 0.000413, 'other-cond': 0.000222}; migrants {'yielder': 73.7, 'exploiter': 36.0, 'c2': 0.201, 'c5': 0.201, 'c0': 0.0281}
  F->W by arriving family: tail {'c1': 0.00106, 'c4': 0.00106, 'c0': 0.000624, 'c3': 0.000624, 'other-cond': 7.49e-05}; migrants {'c1': 0.135, 'c4': 0.135, 'c0': 0.0315, 'c3': 0.0315, 'exploiter': 0.00431}
  W->U by arriving family: tail {'c2': 0.0148, 'c5': 0.0148, 'other-cond': 0.000642, 'c0': 0.000343, 'c3': 0.000343}; migrants {'c2': 0.121, 'c5': 0.121, 'exploiter': 0.00488, 'other-cond': 0.00449, 'c0': 0.00315}
  U->F tail flux by source category: {'E-other': 0.00057, 'E-offers': 0.00856}
  U->F migrants flux by source category: {'E-offers': 1.64, 'E-other': 108.0}

## Tail-composition ablations (M natural, t0 = 100; the removed prior mass becomes null events unless renorm)

**ablations**

| series | 100 | 10000 |
|---|---|---|
| tail=full | 0.1004 U* | 0.1004 U* |
| tail=bully | 0.1004 U* | 1.0000 F* |
| tail=bully (renorm) | 0.1004 U* | - |
| tail=victim | 1.0000 F* | 1.0000 F* |
| tail=victim (renorm) | 1.0000 F* | - |
| tail=bully+victim | 1.0000 F* | 1.0000 F* |
| tail=bully+victim (renorm) | 1.0000 F* | - |
| tail=cond | 0.1004 U* | 1.0000 F* |
| tail=cond (renorm) | 0.1004 U* | - |

## N scaling of the tail (hybrid object: fixation kernel at N, founding law of N = 100)

- N=100: tail-free endpoint (late0 row) F/U = 0.1004 / 0.8996; natural t0=100: 0.1: 0.1004, 0.3: 0.1004, 1: 0.1004, 3: 0.1004, 10: 0.1004, 30: 0.1004, 100: 0.1004, 300: 0.1004, 1000: 0.1004, 10000: 0.1004, 100000: 0.1004; late t0=1: 0.01: 0.1004, 0.03: 0.1004, 0.1: 0.1004, 0.3: 0.1004, 1: 0.1004, 3: 0.1004, 10: 0.1004, 30: 0.1004, 100: 0.1004, 300: 0.1004, 1000: 0.1004, 10000: 0.1004
- N=200: tail-free endpoint (late0 row) F/U = n/a; natural t0=100: n/a; late t0=1: n/a
- N=400: tail-free endpoint (late0 row) F/U = n/a; natural t0=100: n/a; late t0=1: n/a

Single-island neutral entry probability per arrival at N: 1/N = 0.01 (N=100), 0.005 (N=200), 0.0025 (N=400)

## Object variants (6b), numerics and symmetry checks

- obj m1core: 0: V*=1.0000 U=0.0000 (F), 100: V*=1.0000 U=0.0000 (F), 10000: V*=1.0000 U=-0.0000 (F)
- obj m1full: 0: V*=1.0000 U=0.0000 (F), 100: V*=1.0000 U=-0.0000 (F), 10000: V*=1.0000 U=-0.0000 (F)
- asymmetric perturbation delta=1e-06 of the L natural endpoint, unprojected, to tau=1000: V*=0.999737, pairs [0.333246, 0.333245, 0.333246]
- asymmetric perturbation delta=0.001 of the L natural endpoint, unprojected, to tau=316228: V*=1.000000, pairs [0.622786, 0.137694, 0.23952]
