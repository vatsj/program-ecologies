# An annealed mutation tail on the unequal basin of majority division (queue 71): run report

**Question and design (reminder).** Queue 70 found the length-prior arms L (weak evaluator) and M (modalPA) bistable in the tail-free
islands-to-infinity chain: M's natural start ends unequal (V* 0.1004, U 0.8996) because its boundary u* = 0.425 sits just under the natural
unequal share 0.429; two Trojan-bully programs per slot pull the boundary down, and each outcome is a ratchet that depletes the programs that could
leave it. The ratchet is an eps = 0 statement. This run adds the annealed prior tail the object keeps: after founding, prior arrivals at rate
eps(t) = (Lam/t0)(1 + t/t0)^-2 per island per migrant event (Lam = total arrivals per island, t0 = how early), uniformly random slot, program drawn from
the slot's founding prior, fixing with the migrant kernel: dx/dt = F(x) + eps(t) G(x; p). N = 100, w = 0.3, object P (the reflecting m = 3 truncation on
queue 70's 48-conditional core), arms L and M; arm T (27 programs) on its own ODE. RS 2026-11-01: "Go ahead w the annealing run". Spec
`specs/2026-11-01-annealed-tail-dollar3.md`, predictions `predictions/2026-11-01-annealed-tail.md` (committed before any counted cell), notes
`notes/annealed-tail.md`, code `src/annealed_tail*.py`, rows `runs/annealed_tail/`.

## Validations

- **V1 (Lam = 0 reproduces queue 70 / 69).** Maximum endpoint difference to the stored rows: M0 nat 5.5e-09, L0 nat 1.6e-10, M0 u:0.6 1.0e-08, L0 u:0.6 3.9e-10; trajectories (1e2, 1e3, 1e4 events) within 5e-8. Arm T natural endpoints (P_fail 0.1 and 0) within 6.2e-12 of the stored ODE.
- **V2.** Linearity of the field in the donor law: max abs deviation 4.7e-19 on a field of scale 8.9e-05; mass conservation of F + eps G: <= 1.4e-14 at eps up to 300; S3 equivariance of G: 6.8e-21; arm T mass conservation <= 1.8e-16. Prior law and the restricted prior S3-invariant to 0.0 (static.json).
- **V3 (Lam = 10, t0 = 100, M natural, I = 4096, 4 worlds).** max |ODE - MC| over the five classes: 100: 0.0027, 1000: 0.0115, 3000: 0.0220; at 1e4 events 0.199.
- **V3 (Lam = 100, t0 = 100, M natural, I = 4096, 4 worlds).** max |ODE - MC| over the five classes: 100: 0.0040, 1000: 0.0047, 3000: 0.0156; at 1e4 events 0.015.
- **V3 (Lam = 0 control, t0 = 100, M natural, I = 4096, 4 worlds).** max |ODE - MC| over the five classes: 100: 0.0048, 1000: 0.0100, 3000: 0.0278; at 1e4 events 0.624.
- **V3 (Lam = 10, I = 16,384, t0 = 100, M natural, I = 16384, 4 worlds).** max |ODE - MC| over the five classes: 100: 0.0010, 1000: 0.0007, 3000: 0.0013; at 1e4 events 0.718.
  The gate times 1e2 and 1e3 pass (<= 0.012 at I = 4,096, <= 0.001 at I = 16,384). The 1e4 gate is **not informative and fails even at Lam = 0**: M natural passes through a sharp F -> U transition at about 1.2e4 events in the ODE (V* 0.98 -> 0.27 in 3e3 events) and the full-dynamics chain makes it earlier (V* at 1e4: 0.36 at I = 4,096, 0.26 at I = 16,384, tail-free), so any comparison at 1e4 measures transition timing, not the tail kernel. Lam = 100 at I = 4,096 agrees at 1e4 (0.015) by coincidence of timing.
- **V3b (the central contrast against the full-dynamics chain, no truncation).** tail = full, Lam = 300, t0 = 100, I = 8192: V*/U at 40000 events: ODE 0.100 / 0.898; MC worlds 0.000 / 0.997; 0.000 / 0.997.
- **V3b (the central contrast against the full-dynamics chain, no truncation).** tail = victim, Lam = 300, t0 = 100, I = 8192: V*/U at 40000 events: ODE 0.997 / 0.000; MC worlds 0.662 / 0.335; 0.998 / 0.000.
- **V4 (single-arrival assay, prior arrivals into M's endpoint triples, direct Moran simulation of the island).** 7 strata with a testable fixation probability, |z| max 1.59: passed.

## Static numbers

- Prior mass per slot: nine constants 0.9760 (0.10844 each), conditionals in the S3-union support 0.02299 (1,240 of 1,296), of them 8.90e-04 in the 48-core; mass outside the union support (always a null event) 1.04e-03; mass restricted to the state set 0.99896.
- Offering constants (E toward Lw at 1/3 or 1/2): 0.2169; exit constant (Lw toward E at 1/2): 0.1084; victim constants (name a slot partner at 1/3, either partner): 0.2169; Trojan bullies: 3.707e-05; ratio offering : bullies = 5850 : 1.
- Blocked flux (null events of the reflecting truncation), object P, at the natural start: migrants 1.01e-03 of their flux, tail 1.05e-03 of its flux; at the tail-free endpoint: migrants 1.7e-09, tail 0.016.
- Blocked flux (null events of the reflecting truncation), object m1core, at the natural start: migrants 6.21e-06 of their flux, tail 3.94e-06 of its flux.
- Blocked flux (null events of the reflecting truncation), object m1full, at the natural start: migrants 1.01e-03 of their flux, tail 1.06e-03 of its flux.

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

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = None, bracket None, evaluations None

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = 316.22776601683796, bracket [273.8419634264361, 316.22776601683796], evaluations {'316.22776601683796': 0.9999999815271055, '177.82794100389228': 0.10040966506222193, '237.13737056616552': 0.1004096650633924, '273.8419634264361': 0.1004096650623789}

**Bisection** (mode rescue, series "L0" u:0.6 t0=100.0): Lam* = 205.3525026457146, bracket [177.82794100389228, 205.3525026457146], evaluations {'316.22776601683796': 0.9997368896609329, '177.82794100389228': -7.40066924321444e-28, '237.13737056616552': 0.9997368900847892, '205.3525026457146': 0.9997368902003683}

**Bisection** (mode harm, series "L0" nat t0=100.0): Lam* = 31622.776601683792, bracket [23713.737056616552, 31622.776601683792], evaluations {'31622.776601683792': -6.40262962622179e-22, '17782.794100389227': 0.9997368893257242, '23713.737056616552': 0.9997368888316123}

**Bisection** (mode rescue, series "M0" u:0.6 t0=1.0): Lam* = 749.8942093324558, bracket [649.3816315762114, 749.8942093324558], evaluations {'316.22776601683796': 0.10040966360078674, '562.3413251903492': 0.10040966482695761, '749.8942093324558': 0.9999999816063766, '649.3816315762114': 0.10040966482600445}

**Bisection** (mode rescue, series "M0" nat t0=1.0): Lam* = 36.51741272548377, bracket [31.622776601683793, 36.51741272548377], evaluations {'31.622776601683793': 0.1004096634270329, '56.23413251903491': 0.9999999814061815, '42.169650342858226': 0.9999999814050636, '36.51741272548377': 0.9999999813950423}

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = 11547.819846894581, bracket [10000.0, 11547.819846894581], evaluations {'17782.794100389227': 0.9938519981629511, '13335.21432163324': 0.9940838485825273, '11547.819846894581': 0.9941820668878188}

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = 865.9643233600654, bracket [749.8942093324558, 865.9643233600654], evaluations {'1000.0': 0.9999999816628414, '316.22776601683796': 0.10040966506398419, '562.3413251903492': 0.10040966506273012, '749.8942093324558': 0.10040966506188603, '865.9643233600654': 0.9999999816415083}

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = 86.59643233600653, bracket [74.98942093324558, 86.59643233600653], evaluations {'31.622776601683793': 0.10040966506316124, '56.23413251903491': 0.10040966506410383, '74.98942093324558': 0.10040966506332444, '86.59643233600653': 0.9999999816294854}

**Bisection** (mode rescue, series "M0" u:0.6 t0=100.0): Lam* = 865.9643233600654, bracket [749.8942093324558, 865.9643233600654], evaluations {'316.22776601683796': 0.10040966506158407, '562.3413251903492': 0.1004096650638877, '749.8942093324558': 0.1004096650609089, '865.9643233600654': 0.9999999816047254}

**Bisection** (mode rescue, series "L0" u:0.6 t0=1.0): Lam* = 153.9926526059492, bracket [133.3521432163324, 153.9926526059492], evaluations {'316.22776601683796': 0.9997368898082838, '177.82794100389228': 0.999736889777744, '133.3521432163324': 3.9979907326742184e-25, '153.9926526059492': 0.999736889496819}

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = 2371.3737056616555, bracket [2053.5250264571464, 2371.3737056616555], evaluations {'3162.2776601683795': 0.9949348651837037, '1778.2794100389228': 0.05782924861846995, '2371.3737056616555': 0.9951703397360295, '2053.5250264571464': 0.05782016988254648}

**Bisection** (mode rescue, series "M0" nat t0=100.0): Lam* = 56.23413251903491, bracket [48.696752516586315, 56.23413251903491], evaluations {'31.622776601683793': 0.10040966506193862, '56.23413251903491': 0.9999999816034874, '42.169650342858226': 0.10040966506171108, '48.696752516586315': 0.10040966506225728}

**Bisection** (mode rescue, series "M0" nat t0=10000.0): Lam* = 365.17412725483774, bracket [316.22776601683796, 365.17412725483774], evaluations {'316.22776601683796': 0.100409665061172, '562.3413251903492': 0.999999981544585, '421.6965034285823': 0.9999999814919138, '365.17412725483774': 0.9999999817190993}

## Late tail: from M's tail-free state at tau = t_s = 1e6

Tail-free state at t_s: class shares F/U/G/W/D = [0.100399, 0.899521, 8e-05, 0.0, 1e-06]; donor marginal mass of the nine constants in slot 0 (action index 0..8):

`[6.6e-18, -2.66e-17, -4.15e-18, -7.37e-18, 1.42e-17, 2.08e-18, 0.000104, -6.96e-19, -3.34e-18]`

Offering constants (name the underpaid member at 1/3 or 1/2) and the exit constant (names the excluded slot at 1/2) are at 1e-17 or below;
the baseline donor supply is zero, so the baseline-zero rerun is vacuous (same state).

**M0 late (V*)**

| series | 0 | 0.01 | 0.03 | 0.1 | 0.3 | 1 | 3 | 10 | 30 | 100 | 300 | 1000 | 10000 | 100000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| late t0=1 | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* |
| late t0=100 | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* |
| late t0=10000 | 0.1004 U | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | 0.1004 U* | - | - | - |

**Small-Lam response of the late tail** (endpoint V* minus the tail-free V*, Lam in 0.01, 0.03, 0.1, 0.3):

- t0=1: 0.01: 3.05e-12, 0.03: 9.19e-12, 0.1: 3.06e-11, 0.3: 9.19e-11; log-log slope 1.001 (response 3.05e-10 per arrival)
- t0=100: 0.01: -1.82e-11, 0.03: -5.47e-11, 0.1: -1.82e-10, 0.3: 6.81e-06
- t0=10000: 0.01: 7.20e-06, 0.03: 7.45e-06, 0.1: 7.61e-06, 0.3: 7.70e-06; log-log slope 0.020 (response 7.20e-04 per arrival)

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

**Lam = 100** (status capped, V* at the end of the integration 0.9984)

- integrated to tau = 1000. direct tail flux by class transition: {'W->U': 0.02887, 'W->F': 0.02218, 'F->U': 0.009057, 'U->F': 0.00845, 'D->F': 0.005688, 'U->W': 0.004707, 'D->U': 0.002996, 'D->W': 0.002298}
  migrant flux by class transition: {'U->F': 0.1865, 'W->F': 0.1857, 'W->U': 0.1496, 'F->U': 0.1308, 'U->W': 0.1029, 'F->W': 0.05402, 'D->U': 0.02543, 'D->W': 0.02009}
  U->F by arriving family: tail {'c1': 0.00413, 'c4': 0.00413, 'other-cond': 0.000177, 'fair-reader': 1.22e-05, 'exploiter': 2.67e-06}; migrants {'c1': 0.0915, 'c4': 0.0915, 'other-cond': 0.00304, 'fair-reader': 0.000327, 'exploiter': 0.000145}
  F->U by arriving family: tail {'c2': 0.00442, 'c5': 0.00442, 'other-cond': 0.000191, 'exploiter': 1.31e-05, 'yielder': 3.12e-06}; migrants {'c2': 0.0625, 'c5': 0.0625, 'other-cond': 0.00234, 'c0': 0.00138, 'c3': 0.00138}
  F->W by arriving family: tail {'c1': 0.000914, 'c4': 0.000914, 'other-cond': 6.42e-05, 'c6': 5.14e-06, 'c2': 4.11e-06}; migrants {'c1': 0.0192, 'c4': 0.0192, 'c0': 0.00731, 'c3': 0.00731, 'other-cond': 0.000893}
  W->U by arriving family: tail {'c2': 0.0141, 'c5': 0.0141, 'other-cond': 0.000612, 'exploiter': 4.09e-05, 'yielder': 9.44e-06}; migrants {'c2': 0.0712, 'c5': 0.0712, 'other-cond': 0.00278, 'c0': 0.0018, 'c3': 0.0018}
  U->F tail flux by source category: {'E-offers': 0.0081, 'E-other': 0.000346}
  U->F migrants flux by source category: {'E-offers': 0.179, 'E-other': 0.00778}
- integrated to tau = 10000. direct tail flux by class transition: {'W->U': 0.02912, 'W->F': 0.02244, 'F->U': 0.009768, 'U->F': 0.009002, 'D->F': 0.005693, 'U->W': 0.004855, 'D->U': 0.002998, 'D->W': 0.002299}
  migrant flux by class transition: {'U->F': 0.9075, 'W->F': 0.5472, 'F->U': 0.461, 'F->W': 0.3237, 'U->W': 0.2586, 'W->U': 0.2365, 'D->U': 0.02679, 'D->F': 0.02481}
  U->F by arriving family: tail {'c1': 0.0044, 'c4': 0.0044, 'other-cond': 0.000188, 'fair-reader': 1.3e-05, 'exploiter': 2.85e-06}; migrants {'c1': 0.443, 'c4': 0.443, 'other-cond': 0.011, 'exploiter': 0.00532, 'fair-reader': 0.00529}
  F->U by arriving family: tail {'c2': 0.00477, 'c5': 0.00477, 'other-cond': 0.000205, 'exploiter': 1.41e-05, 'yielder': 3.67e-06}; migrants {'c2': 0.184, 'c5': 0.184, 'exploiter': 0.0257, 'yielder': 0.021, 'c0': 0.0195}
  F->W by arriving family: tail {'c1': 0.000981, 'c4': 0.000981, 'other-cond': 7.17e-05, 'c6': 5.68e-06, 'c7': 4.45e-06}; migrants {'c1': 0.128, 'c4': 0.128, 'c0': 0.0297, 'c3': 0.0297, 'other-cond': 0.00398}
  W->U by arriving family: tail {'c2': 0.0142, 'c5': 0.0142, 'other-cond': 0.000617, 'exploiter': 4.13e-05, 'yielder': 9.52e-06}; migrants {'c2': 0.111, 'c5': 0.111, 'other-cond': 0.00415, 'exploiter': 0.0031, 'c0': 0.00281}
  U->F tail flux by source category: {'E-offers': 0.00863, 'E-other': 0.000373}
  U->F migrants flux by source category: {'E-offers': 0.857, 'E-other': 0.0509}
- integrated to tau = 100000. direct tail flux by class transition: {'W->U': 0.02912, 'W->F': 0.02244, 'F->U': 0.009864, 'U->F': 0.009023, 'D->F': 0.005693, 'U->W': 0.004855, 'D->U': 0.002998, 'D->W': 0.002299}
  migrant flux by class transition: {'U->F': 3.884, 'F->U': 3.408, 'W->F': 0.5507, 'F->W': 0.327, 'U->W': 0.2588, 'W->U': 0.2366, 'D->U': 0.0268, 'D->F': 0.02614}
  U->F by arriving family: tail {'c1': 0.00441, 'c4': 0.00441, 'other-cond': 0.000188, 'fair-reader': 1.3e-05, 'exploiter': 2.85e-06}; migrants {'c1': 1.14, 'c4': 1.14, 'fair-reader': 1.09, 'exploiter': 0.288, 'yielder': 0.206}
  F->U by arriving family: tail {'c2': 0.00482, 'c5': 0.00482, 'other-cond': 0.000205, 'exploiter': 1.42e-05, 'yielder': 3.9e-06}; migrants {'yielder': 1.55, 'exploiter': 1.44, 'c2': 0.184, 'c5': 0.184, 'c0': 0.0197}
  F->W by arriving family: tail {'c1': 0.000981, 'c4': 0.000981, 'other-cond': 7.2e-05, 'c6': 5.68e-06, 'c7': 4.45e-06}; migrants {'c1': 0.129, 'c4': 0.129, 'c0': 0.0297, 'c3': 0.0297, 'other-cond': 0.00399}
  W->U by arriving family: tail {'c2': 0.0142, 'c5': 0.0142, 'other-cond': 0.000617, 'exploiter': 4.13e-05, 'yielder': 9.52e-06}; migrants {'c2': 0.111, 'c5': 0.111, 'other-cond': 0.00415, 'exploiter': 0.00317, 'c0': 0.00281}
  U->F tail flux by source category: {'E-offers': 0.00864, 'E-other': 0.000387}
  U->F migrants flux by source category: {'E-offers': 1.94, 'E-other': 1.95}

**Lam = 100** (status capped, V* at the end of the integration 0.1002)

- integrated to tau = 1000. direct tail flux by class transition: {'W->U': 0.03065, 'W->F': 0.02256, 'F->U': 0.009958, 'D->U': 0.008515, 'U->F': 0.008345, 'U->W': 0.007744, 'D->W': 0.00696, 'D->F': 0.004954}
  migrant flux by class transition: {'W->F': 0.189, 'U->F': 0.1821, 'W->U': 0.1589, 'F->U': 0.1402, 'U->W': 0.1102, 'F->W': 0.05543, 'D->U': 0.02161, 'D->W': 0.0182}
  U->F by arriving family: tail {'c1': 0.00408, 'c4': 0.00408, 'other-cond': 0.000175, 'fair-reader': 1.2e-05, 'yielder': 1.35e-06}; migrants {'c1': 0.0893, 'c4': 0.0893, 'other-cond': 0.00296, 'fair-reader': 0.000321, 'exploiter': 0.00014}
  F->U by arriving family: tail {'c2': 0.00478, 'c5': 0.00478, 'other-cond': 0.000207, 'c0': 8.2e-05, 'c3': 8.2e-05}; migrants {'c2': 0.0671, 'c5': 0.0671, 'other-cond': 0.00251, 'c0': 0.00137, 'c3': 0.00137}
  F->W by arriving family: tail {'c1': 0.000987, 'c4': 0.000987, 'c0': 0.000525, 'c3': 0.000525, 'other-cond': 6.75e-05}; migrants {'c1': 0.0198, 'c4': 0.0198, 'c0': 0.00738, 'c3': 0.00738, 'other-cond': 0.000896}
  W->U by arriving family: tail {'c2': 0.0146, 'c5': 0.0146, 'other-cond': 0.000636, 'c0': 0.000338, 'c3': 0.000338}; migrants {'c2': 0.0757, 'c5': 0.0757, 'other-cond': 0.00295, 'c0': 0.00194, 'c3': 0.00194}
  U->F tail flux by source category: {'E-other': 0.000344, 'E-offers': 0.008}
  U->F migrants flux by source category: {'E-offers': 0.174, 'E-other': 0.00765}
- integrated to tau = 10000. direct tail flux by class transition: {'W->U': 0.03092, 'W->F': 0.02283, 'F->U': 0.01094, 'U->F': 0.008921, 'D->U': 0.008521, 'U->W': 0.008042, 'D->W': 0.006965, 'D->F': 0.004959}
  migrant flux by class transition: {'U->F': 0.9586, 'W->F': 0.5717, 'F->U': 0.5215, 'F->W': 0.3393, 'U->W': 0.2828, 'W->U': 0.257, 'D->U': 0.02307, 'D->F': 0.02112}
  U->F by arriving family: tail {'c1': 0.00436, 'c4': 0.00436, 'other-cond': 0.000187, 'fair-reader': 1.29e-05, 'yielder': 1.44e-06}; migrants {'c1': 0.466, 'c4': 0.466, 'other-cond': 0.0113, 'exploiter': 0.00684, 'fair-reader': 0.00663}
  F->U by arriving family: tail {'c2': 0.00514, 'c5': 0.00514, 'other-cond': 0.000222, 'c0': 0.00021, 'c3': 0.00021}; migrants {'c2': 0.2, 'c5': 0.2, 'exploiter': 0.035, 'yielder': 0.032, 'c0': 0.0231}
  F->W by arriving family: tail {'c1': 0.00106, 'c4': 0.00106, 'c0': 0.00062, 'c3': 0.00062, 'other-cond': 7.48e-05}; migrants {'c1': 0.134, 'c4': 0.134, 'c0': 0.0313, 'c3': 0.0313, 'other-cond': 0.00402}
  W->U by arriving family: tail {'c2': 0.0148, 'c5': 0.0148, 'other-cond': 0.000642, 'c0': 0.000343, 'c3': 0.000343}; migrants {'c2': 0.121, 'c5': 0.121, 'other-cond': 0.00449, 'exploiter': 0.00365, 'c0': 0.00313}
  U->F tail flux by source category: {'E-other': 0.000372, 'E-offers': 0.00855}
  U->F migrants flux by source category: {'E-offers': 0.902, 'E-other': 0.0569}
- integrated to tau = 100000. direct tail flux by class transition: {'W->U': 0.03092, 'W->F': 0.02283, 'F->U': 0.01146, 'U->F': 0.009116, 'D->U': 0.008521, 'U->W': 0.008079, 'D->W': 0.006965, 'D->F': 0.004959}
  migrant flux by class transition: {'F->U': 109.3, 'U->F': 108.7, 'W->F': 0.5753, 'F->W': 0.3419, 'U->W': 0.2847, 'W->U': 0.2581, 'D->F': 0.02527, 'D->U': 0.02439}
  U->F by arriving family: tail {'c1': 0.00446, 'c4': 0.00446, 'other-cond': 0.000187, 'fair-reader': 1.29e-05, 'yielder': 1.48e-06}; migrants {'exploiter': 58.3, 'yielder': 48.7, 'c1': 0.827, 'c4': 0.827, 'fair-reader': 0.122}
  F->U by arriving family: tail {'c2': 0.00522, 'c5': 0.00522, 'c0': 0.000394, 'c3': 0.000394, 'other-cond': 0.000222}; migrants {'yielder': 73.1, 'exploiter': 35.7, 'c2': 0.2, 'c5': 0.2, 'c0': 0.025}
  F->W by arriving family: tail {'c1': 0.00106, 'c4': 0.00106, 'c0': 0.000625, 'c3': 0.000625, 'other-cond': 7.5e-05}; migrants {'c1': 0.135, 'c4': 0.135, 'c0': 0.0314, 'c3': 0.0314, 'other-cond': 0.00403}
  W->U by arriving family: tail {'c2': 0.0148, 'c5': 0.0148, 'other-cond': 0.000642, 'c0': 0.000343, 'c3': 0.000343}; migrants {'c2': 0.121, 'c5': 0.121, 'other-cond': 0.00449, 'exploiter': 0.00437, 'c0': 0.00313}
  U->F tail flux by source category: {'E-other': 0.000558, 'E-offers': 0.00856}
  U->F migrants flux by source category: {'E-offers': 1.61, 'E-other': 107.0}

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

- N=100: tail-free endpoint (late0 row) F/U = 0.1004 / 0.8996; natural t0=100: 0.1: 0.1004, 0.3: 0.1004, 1: 0.1004, 3: 0.1004, 10: 0.1004, 30: 0.1004, 100: 0.1004, 300: 0.1004, 1000: 0.1004, 10000: 0.1004, 100000: 0.1004; late t0=1: 0: 0.1004, 0.01: 0.1004, 0.03: 0.1004, 0.1: 0.1004, 0.3: 0.1004, 1: 0.1004, 3: 0.1004, 10: 0.1004, 30: 0.1004, 100: 0.1004, 300: 0.1004, 1000: 0.1004, 10000: 0.1004, 100000: 0.1004
- N=200: tail-free endpoint (late0 row) F/U = 0.0580 / 0.9397; natural t0=100: 10: 0.0580, 300: 0.0580, 10000: 0.0579; late t0=1: 0: 0.0580, 300: 0.0580, 10000: 0.0580
- N=400: tail-free endpoint (late0 row) F/U = 0.0325 / 0.9651; natural t0=100: 10: 0.0325, 300: 0.0324, 10000: 0.0324; late t0=1: 0: 0.0325, 300: 0.0325, 10000: 0.0325

Single-island neutral entry probability per arrival at N: 1/N = 0.01 (N=100), 0.005 (N=200), 0.0025 (N=400)

## Object variants (6b), numerics and symmetry checks

- obj m1core: 0: V*=1.0000 U=0.0000 (F), 100: V*=1.0000 U=0.0000 (F), 10000: V*=1.0000 U=-0.0000 (F)
- obj m1full: 0: V*=1.0000 U=0.0000 (F), 100: V*=1.0000 U=-0.0000 (F), 10000: V*=1.0000 U=-0.0000 (F)
- asymmetric perturbation delta=1e-06 of the L natural endpoint, unprojected, to tau=1000: V*=0.999737, pairs [0.333246, 0.333245, 0.333246]
- asymmetric perturbation delta=0.001 of the L natural endpoint, unprojected, to tau=316228: V*=1.000000, pairs [0.622786, 0.137694, 0.23952]

## Lam* of the composition-ablated tails (matched dose; M natural, t0 = 100, N = 100 unless the series says otherwise)

| series (cell, start, tail, N, t0) | grid / evaluations (Lam: endpoint V*) | Lam* (smallest Lam with V* >= 0.5) | bracket |
|---|---|---|---|
| L0 u:0.6 bully+victim N=100 t0=1 | 100: 0.000, 133.4: 0.000, 154: 1.000, 177.8: 1.000, 316.2: 1.000, 1000: 1.000 | 154 | (133.4, 154] |
| L0 u:0.6 bully+victim N=100 t0=100 | 100: 0.000, 177.8: -0.000, 205.4: 1.000, 237.1: 1.000, 316.2: 1.000, 1000: 1.000 | 205.4 | (177.8, 205.4] |
| M0 nat bully N=100 t0=100 | 100: 0.100, 177.8: 0.100, 237.1: 0.100, 273.8: 0.100, 316.2: 1.000, 1000: 1.000, 1e+04: 1.000 | 316.2 | (273.8, 316.2] |
| M0 nat bully+victim N=100 t0=1 | 10: 0.100, 31.62: 0.100, 36.52: 1.000, 42.17: 1.000, 56.23: 1.000, 100: 1.000, 1000: 1.000 | 36.52 | (31.62, 36.52] |
| M0 nat bully+victim N=100 t0=100 | 0.1: 0.100, 1: 0.100, 10: 0.100, 31.62: 0.100, 42.17: 0.100, 48.7: 0.100, 56.23: 1.000, 100: 1.000 | 56.23 | (48.7, 56.23] |
| M0 nat bully+victim N=100 t0=10000 | 10: 0.100, 100: 0.100, 316.2: 0.100, 365.2: 1.000, 421.7: 1.000, 562.3: 1.000, 1000: 1.000 | 365.2 | (316.2, 365.2] |
| M0 nat cond N=100 t0=100 | 100: 0.100, 316.2: 0.100, 562.3: 0.100, 749.9: 0.100, 866: 1.000, 1000: 1.000, 1e+04: 1.000, 1e+05: 1.000 | 866 | (749.9, 866] |
| M0 nat victim N=100 t0=100 | 0.1: 0.100, 1: 0.100, 10: 0.100, 31.62: 0.100, 56.23: 0.100, 74.99: 0.100, 86.6: 1.000, 100: 1.000 | 86.6 | (74.99, 86.6] |
| M0 nat victim N=200 t0=100 | 10: 0.058, 100: 0.058, 1000: 0.058, 1778: 0.058, 2054: 0.058, 2371: 0.995, 3162: 0.995, 1e+04: 0.994 | 2371 | (2054, 2371] |
| M0 nat victim N=400 t0=100 | 10: 0.032, 100: 0.032, 1000: 0.032, 1e+04: 0.032, 1.155e+04: 0.994, 1.334e+04: 0.994, 1.778e+04: 0.994, 3.162e+04: 0.993, 1e+05: 0.990 | 1.155e+04 | (1e+04, 1.155e+04] |
| M0 u:0.6 bully+victim N=100 t0=1 | 100: 0.100, 316.2: 0.100, 562.3: 0.100, 649.4: 0.100, 749.9: 1.000, 1000: 1.000 | 749.9 | (649.4, 749.9] |
| M0 u:0.6 bully+victim N=100 t0=100 | 100: 0.100, 316.2: 0.100, 562.3: 0.100, 749.9: 0.100, 866: 1.000, 1000: 1.000 | 866 | (749.9, 866] |

Full tail: no Lam* up to 1e5 (M natural, t0 = 1 and 100). Ablated endpoints reproduce at 10x tighter tolerance and half the backward-Euler step at both bracket points (validation table).

**Numerics check (rtol 1e-10, backward-Euler step halved) at the bracket points**

| tail | Lam | class (tight) | V* (tight) | class (base) | V* (base) |
|---|---|---|---|---|---|
| bully | 273.8 | U | 0.100410 | U | 0.100410 |
| bully | 316.2 | F | 1.000000 | F | 1.000000 |
| bully+victim | 48.7 | U | 0.100410 | U | 0.100410 |
| bully+victim | 56.23 | F | 1.000000 | F | 1.000000 |
| cond | 749.9 | U | 0.100410 | U | 0.100410 |
| cond | 866 | F | 1.000000 | F | 1.000000 |
| victim | 74.99 | U | 0.100410 | U | 0.100410 |
| victim | 86.6 | F | 1.000000 | F | 1.000000 |

## Endpoint support and transition structure (M natural, t0 = 100)

- tail=full, Lam=0: endpoint class U, F/U = 0.10041 / 0.89959; programs with donor mass > 1e-9 per slot: [5, 5, 5] (> 1e-12: [103, 103, 103]); pairs [0.0335, 0.0335, 0.0335]; leading donors (slot 0): if(BOX(2=(1,1/3)),(2,2/3),(3,1/2)) 0.279; if(BOX(3=(1,1/3)),(3,2/3),(2,1/2)) 0.279; if(BOX(2=(1,2/3)),(2,1/3),(2,1/2)) 0.221; if(BOX(3=(1,2/3)),(3,1/3),(3,1/2)) 0.221; (ALL,1/3) 1.22e-08; migrants' class flux per event: F>U 0.00124, F>D 3.2e-10, U>F 0.00124, U>D 4.87e-08, D>F 3.76e-08, D>U 1.14e-08.
- tail=full, Lam=100: endpoint class U, F/U = 0.10041 / 0.89959; programs with donor mass > 1e-9 per slot: [4, 4, 4] (> 1e-12: [4, 4, 4]); pairs [0.0335, 0.0335, 0.0335]; leading donors (slot 0): if(BOX(2=(1,1/3)),(2,2/3),(3,1/2)) 0.279; if(BOX(3=(1,1/3)),(3,2/3),(2,1/2)) 0.279; if(BOX(3=(1,2/3)),(3,1/3),(3,1/2)) 0.221; if(BOX(2=(1,2/3)),(2,1/3),(2,1/2)) 0.221; (3,1/2) 1.72e-17; migrants' class flux per event: F>U 0.00124, F>D 3.2e-10, U>F 0.00124, U>D 4.87e-08, D>F 3.76e-08, D>U 1.14e-08.
- tail=victim, Lam=74.99: endpoint class U, F/U = 0.10041 / 0.89959; programs with donor mass > 1e-9 per slot: [4, 4, 4] (> 1e-12: [4, 4, 4]); pairs [0.0335, 0.0335, 0.0335]; leading donors (slot 0): if(BOX(3=(1,1/3)),(3,2/3),(2,1/2)) 0.279; if(BOX(2=(1,1/3)),(2,2/3),(3,1/2)) 0.279; if(BOX(3=(1,2/3)),(3,1/3),(3,1/2)) 0.221; if(BOX(2=(1,2/3)),(2,1/3),(2,1/2)) 0.221; (2,1/2) 8.15e-17; migrants' class flux per event: F>U 0.00124, F>D 3.2e-10, U>F 0.00124, U>D 4.87e-08, D>F 3.76e-08, D>U 1.14e-08.
- tail=victim, Lam=86.6: endpoint class F, F/U = 1.00000 / -0.00000; programs with donor mass > 1e-9 per slot: [4, 4, 4] (> 1e-12: [4, 4, 4]); pairs [0.3333, 0.3333, 0.3333]; leading donors (slot 0): if(BOX(2=(1,1/2)),(2,1/2),(3,1/2)) 0.25; if(BOX(3=(1,1/2)),(3,1/2),(2,1/2)) 0.25; (2,1/2) 0.25; (3,1/2) 0.25; (2,1/3) 9.77e-18; migrants' class flux per event: F>D 1.91e-09, D>F 1.91e-09.

## Prediction verdicts

| prediction | claim | verdict | number that scores it |
|---|---|---|---|
| RE1 | M natural: some Lam <= 30 reaches V* >= 0.99 at t0 = 1 and 100, V* non-decreasing | FAILED | max V* over Lam <= 30: 0.1004; over every Lam tested (to 1e5 at t0 = 100, to 1e4 at t0 = 1): 0.1004; M nat endpoint is the tail-free 0.1004 at every Lam |
| RE2 | Lam*(late) >= 10 Lam*(t0 = 1) | UNSCORED for the full tail (neither flips); HELD for the clean tail | full tail: no Lam* early or late; victim+bully-less tail: early Lam*(t0 = 1) in [31.622776601683793, 36.51741272548377], Lam*(t0 = 100) in [48.696752516586315, 56.23413251903491], Lam*(t0 = 1e4) in [316.22776601683796, 365.17412725483774], settled-ratchet late tail (t_s = 1e6) does not flip at any Lam tested (max V* 0.1004, Lam up to 1e4), ratio > 250 |
| RE3 | constant rain and t0 = 100 annealed within a factor 3 in Lam* | UNSCORED (vacuous) | constant rain: V* = 0.1004 at every Lam <= 300; no Lam* either way |
| RE4 | L natural and arm T keep V* >= 0.999 at every Lam, t0 on the grid (Lam <= 300), cell 7 included | HELD on the spec grid; FAILS in extension (L natural) | min V* on the grid: L natural 0.9997, arm T 0.999993; extension: L natural t0 = 100 falls to U at Lam in (2.4e4, 3.2e4] (V* 0.9997 -> 0), t0 = 1 holds to 1e5 |
| RE5 | rescue carried by excluded-slot offering constants (>= 0.7) and by victims with bullies (>= 0.7); bully ablation < 1.25x; victim ablation >= 1.5x | FAILED (bully clause and second share) | direct tail flux at Lam = 100, tau = 1e4: U->F through sources whose excluded slot holds an offering constant 0.958 of the U->F flux; F->U carried by the 1/3 constants (c0, c3) and bullies: 0.040 (the 2/3 constants c2, c5: 0.937); bully-less tail Lam* in [273.8419634264361, 316.22776601683796] against none for the full tail (moves it by far more than 1.25x); victim-less tail Lam* in [74.98942093324558, 86.59643233600653] (lowers it) |
| RE6 | Lam*(400)/Lam*(100) in [2.5, 6] at t0 = 100 | FAILED | full tail: no Lam* at any N; victim-less tail (the series that has one): Lam* in [74.98942093324558, 86.59643233600653], [2053.5250264571464, 2371.3737056616555], [10000.0, 11547.819846894581] at N = 100, 200, 400, ratio 400/100 in [115, 154] |
| RE7 | L at u = 0.6 flips to V* at Lam* <= 10 for t0 = 1 | FAILED | full tail: L u = 0.6 stays at U 0.9949 at every Lam <= 300 and every t0 (V* = 0.0000); clean tail: Lam* in [133.3521432163324, 153.9926526059492] at t0 = 1 |
| argon a | bully tail ablation < 1.05x; victim ablation >= 1.5x | FAILED / HELD | bully ablation: none -> (274, 316]; victim ablation: none -> (75, 87] (held) |
| argon b | Lam*(400)/Lam*(100) < 2.5 for the early tail | FAILED (on the victim-less tail) | ratio 400/100 in [115, 154]; the full tail has no Lam* |
| sol c | early M-natural rescue substantially easier than deep-U rescue (M u = 0.6, late arm); the prior's constant share alone will not predict the latter | HELD (for the clean tail; the full tail rescues nothing) | clean tail, t0 = 1: M natural Lam* in [31.622776601683793, 36.51741272548377]; M u = 0.6 in [649.3816315762114, 749.8942093324558] (ratio 18-24); L u = 0.6 in [133.3521432163324, 153.9926526059492]; t0 = 100: M u = 0.6 in [749.8942093324558, 865.9643233600654], L u = 0.6 in [177.82794100389228, 205.3525026457146]; settled late tail: no flip to 1e4; constants-only tail flips early at (750, 866] and has no late flip tested |
| sol d | no clean proportional scaling of Lam* across N | HELD | victim-less tail: 100 -> 200 multiplies Lam* by [24, 32], 200 -> 400 by [4.2, 5.6]; not a power law in N, and nowhere near proportional |
| sol e | V* non-monotone in Lam somewhere | HELD (extension only) | L natural, t0 = 100: V* 0.9997 -> 0 between Lam 2.4e4 and 3.2e4; no decrease > 0.01 on the spec grid |
| E1 | Lam*(M nat, t0 = 1) <= 3 and Lam*(t0 = 100) <= 10 | FAILED | none to 1e5 (t0 = 100), to 1e4 (t0 = 1) |
| E2 | no late Lam <= 300 has V* >= 0.5 | HELD | late V* = 0.1004 at every Lam to 1e5 (t0 = 1, 100), to 300 (t0 = 1e4), and for the victim-less and victim+bully-less tails at 1e2-1e4 |
| E3 | victim ablation moves Lam* by < 1.25x | FAILED | victim-less tail Lam* in (75, 87] against none; the 1/3 constants carry the full tail's block |
| E4 | constants-only tail has Lam* within 1.25x of the full tail | FAILED | constants-only Lam* in (750, 866] against none |
| E5 | M natural tail-free hybrid endpoint is U-dominated at N = 200 and 400 | HELD | tail-free V*: N = 200: 0.0580, N = 400: 0.0325 |
| E6 | monotone to within 0.01 on every series with a Lam* in the grid | HELD (vacuous for the full tail) | no full-tail series has a Lam*; the ablated bisection series are monotone (step functions) |
| E7 | arm T at Lam = 300, t0 = 1: V* >= 0.999 | HELD | min V* over the four arm-T series at Lam = 300, t0 = 1: 0.9999998258638438 |

## RE addendum (2026-11-01): the cell-8 rows at 10⁶ events

The symmetry lines above are earlier stops. The four `asym2` rows, integrated tail-free without projection to τ = 10⁶ (notes §2.8):
`d1fbb72c3536` M natural rescued endpoint (victim-less tail, Λ = 100), δ = 1e-6: class F, pairs 0.333 / 0.333 / 0.333;
`f1c7011fc0f9` same, δ = 1e-3: class F, pairs 1.0 / 0.0 / 0.0;
`c5633adec135` L natural tail-free endpoint, δ = 1e-6: class F, pairs 0.611 / 0.064 / 0.324;
`ec202849cf64` same, δ = 1e-3: class F, pairs 0.623 / 0.138 / 0.240.
