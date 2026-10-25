# Zero-tolerance, suspicious and sampling inspectors (run report, 2026-10-24)

Spec `specs/2026-10-24-zero-tolerance.md`; predictions `predictions/2026-10-24-zero-tolerance.md`; notes `notes/zero-tolerance.md`; code `src/zero_tolerance*.py`; rows `runs/zero_tolerance/`. **Chain** = the ε → 0 object (π over pairs of monomorphic role classes, the whole state space of about 158 × 157 or 168 × 167–173 pairs, no exploration cap, float32 storage as in the previous run); **lottery** = the ε = 0 seed lottery at the stated (N, I), mN = 1, horizon 20N; never π. Payoffs are game payoffs (gross of the price). "Gain" = an arm's π(E) minus the control's at the same (N, c); the control is the newly computed one (the same total mass m = 0.0013517 added to `cr(THEM(ME))` itself), the stored 0.0466 at N = 10⁵ is context only. Lottery intervals are run-clustered 95% bootstrap (4,000 resamples).

## Completeness

91 of 91 jobs of the job file have an output.

## Validation (before any counted cell)

Arm `v0` (nothing added, no mass moved) against the stored runs: class table max |Δ| 0.0e+00; chain π(E) at N = 10³: 0.343201 vs stored 0.343201 (relative difference 1.3e-07); N = 10⁴: 0.156966 vs 0.156966 (1.2e-07); lottery runs 0–2 at (100, 64), generation 2,000, max |Δ| of five statistics 0.0e+00. Passed: **True**.

## Statics: classes, added mass, strict invaders of the arm's resident

| arm, c | K₀ × K₁ | added program: class (members), mass | strict invaders of (inspector, `C`): non-reading mass / reading mass | |E| / |R| |
|---|---|---|---|---|
| control, c = 0 | 157 × 157 | mass to `cr(THEM(ME))` | 0.002916 / 0.000177 | 1246 / 849 |
| uncond. I, c = 0 | 157 × 157 | mass to `I` | 0.002916 / 0.000177 | 1246 / 849 |
| ZT, c = 0 | 158 × 157 | `zt(THEM(ME))` → class `zt(THEM(ME))` (1), 0.001352 | 0.000000 / 0.000141 | 1276 / 879 |
| SUS, c = 0 | 158 × 157 | `cr_s(THEM(ME))` → class `cr_s(THEM(ME))` (1), 0.001352 | 0.002916 / 0.000000 | 1271 / 874 |
| ZT+SUS, c = 0 | 158 × 157 | `zt_s(THEM(ME))` → class `zt_s(THEM(ME))` (1), 0.001352 | 0.000000 / 0.000000 | 1269 / 872 |
| SR1, c = 0 | 157 × 157 | `sr1(THEM(ME))` → class `sr1(THEM(ME))` (12), 0.001521 | 0.002916 / 0.000155 | 1246 / 849 |
| SR4, c = 0 | 158 × 157 | `sr4(THEM(ME))` → class `sr4(THEM(ME))` (1), 0.001352 | 0.000156 / 0.000194 | 1264 / 867 |
| SR16, c = 0 | 158 × 157 | `sr16(THEM(ME))` → class `sr16(THEM(ME))` (1), 0.001352 | 0.000000 / 0.000060 | 1266 / 869 |
| control, c = 0.01 | 167 × 167 | mass to `cr(THEM(ME))` | 0.002916 / 0.000177 | 1586 / 1001 |
| uncond. I, c = 0.01 | 167 × 167 | mass to `I` | 0.002916 / 0.000177 | 1586 / 1001 |
| ZT, c = 0.01 | 168 × 167 | `zt(THEM(ME))` → class `zt(THEM(ME))` (1), 0.001352 | 0.000000 / 0.000141 | 1620 / 1035 |
| SUS, c = 0.01 | 168 × 167 | `cr_s(THEM(ME))` → class `cr_s(THEM(ME))` (1), 0.001352 | 0.002916 / 0.000000 | 1616 / 1031 |
| ZT+SUS, c = 0.01 | 168 × 167 | `zt_s(THEM(ME))` → class `zt_s(THEM(ME))` (1), 0.001352 | 0.000000 / 0.000000 | 1614 / 1029 |
| SR1, c = 0.01 | 167 × 167 | `sr1(THEM(ME))` → class `sr1(THEM(ME))` (12), 0.001521 | 0.002916 / 0.000141 | 1586 / 1001 |
| SR4, c = 0.01 | 168 × 173 | `sr4(THEM(ME))` → class `sr4(THEM(ME))` (1), 0.001352 | 0.000156 / 0.000000 | 1692 / 1087 |
| SR16, c = 0.01 | 168 × 173 | `sr16(THEM(ME))` → class `sr16(THEM(ME))` (1), 0.001352 | 0.000000 / 0.000000 | 1694 / 1089 |

## Chain: π(E), gains, odds slopes (ε → 0, whole state space)

**c = 0.** π(E) (gain over the control in parentheses); odds slope = least-squares slope of log odds on log N over N ≥ 10³.

| arm | N = 10³ | N = 10⁴ | N = 10⁵ | odds slope | π(R), N = 10⁵ | inspector payoff, N = 10⁵ | forfeit mass (insp / ee), N = 10⁵ | π on 0.99 of states, N = 10⁵ |
|---|---|---|---|---|---|---|---|---|
| control | 0.4068 | 0.1704 | 0.0475 | -0.57 | 0.0455 | -0.532 | 1.8e-04 / 2.6e-04 | 140 |
| ZT | 0.4499 (+0.043) | 0.2661 (+0.096) | 0.0882 (+0.041) | -0.46 | 0.0863 | -0.511 | 1.6e-04 / 2.5e-04 | 151 |
| SUS | 0.4153 (+0.009) | 0.1744 (+0.004) | 0.0372 (-0.010) | -0.63 | 0.0358 | -0.589 | 9.4e-05 / 1.5e-04 | 123 |
| ZT+SUS | 0.4663 (+0.059) | 0.4196 (+0.249) | 0.5344 (+0.487) | 0.06 | 0.5331 | -0.260 | 8.9e-05 / 1.4e-04 | 128 |
| SR1 | 0.4200 (+0.013) | 0.2139 (+0.043) | 0.0647 (+0.017) | -0.51 | 0.0624 | -0.523 | 1.7e-04 / 2.7e-04 | 154 |
| SR4 | 0.4531 (+0.046) | 0.3006 (+0.130) | 0.1163 (+0.069) | -0.40 | 0.1144 | -0.495 | 1.5e-04 / 2.3e-04 | 149 |
| SR16 | 0.4650 (+0.058) | 0.4055 (+0.235) | 0.3823 (+0.335) | -0.07 | 0.3809 | -0.343 | 9.6e-05 / 1.5e-04 | 132 |
| uncond. I | 0.3431 (-0.064) | 0.1568 (-0.014) | 0.0466 (-0.001) | -0.51 | 0.0440 | -0.533 | 1.8e-04 / 2.8e-04 | 158 |

**c = 0.01.** π(E) (gain over the control in parentheses); odds slope = least-squares slope of log odds on log N over N ≥ 10³.

| arm | N = 10³ | N = 10⁴ | N = 10⁵ | odds slope | π(R), N = 10⁵ | inspector payoff, N = 10⁵ | forfeit mass (insp / ee), N = 10⁵ | π on 0.99 of states, N = 10⁵ |
|---|---|---|---|---|---|---|---|---|
| control | 0.3884 | 0.3902 | 0.3827 | -0.01 | 0.2794 | -0.573 | 3.1e-06 / 4.5e-06 | 232 |
| ZT | 0.3995 (+0.011) | 0.4020 (+0.012) | 0.3944 (+0.012) | -0.00 | 0.2910 | -0.567 | 3.0e-06 / 4.4e-06 | 244 |
| SUS | 0.3909 (+0.002) | 0.3928 (+0.003) | 0.3852 (+0.003) | -0.01 | 0.2821 | -0.571 | 2.6e-06 / 4.2e-06 | 247 |
| ZT+SUS | 0.4025 (+0.014) | 0.4051 (+0.015) | 0.3974 (+0.015) | -0.00 | 0.2941 | -0.564 | 2.6e-06 / 4.2e-06 | 243 |
| SR1 | 0.3847 (-0.004) | 0.3878 (-0.002) | 0.3798 (-0.003) | -0.00 | 0.2747 | -0.580 | 3.1e-06 / 4.5e-06 | 240 |
| SR4 | 0.3494 (-0.039) | 0.3503 (-0.040) | 0.3429 (-0.040) | -0.01 | 0.2308 | -0.614 | 2.8e-06 / 4.6e-06 | 252 |
| SR16 | 0.3341 (-0.054) | 0.3355 (-0.055) | 0.3283 (-0.054) | -0.01 | 0.2142 | -0.627 | 2.9e-06 / 4.7e-06 | 250 |
| uncond. I | 0.3291 (-0.059) | 0.3307 (-0.060) | 0.3236 (-0.059) | -0.01 | 0.2090 | -0.631 | 2.9e-06 / 4.7e-06 | 246 |

Context only: the stored (unmatched) control gave π(E) = 0.3432 / 0.1570 / 0.0466 at N = 10³ / 10⁴ / 10⁵ (c = 0).

## Exit decomposition from R, c = 0 (conditional hazard per mutation event, own stationary weights)

Categories: **light cheaters** = D (strict invasion by a non-reading inspectee other than K), **bounded-read exploiters** = E (strict invasion by a reading inspectee, clean plus forfeit-driven), **shadow** = A (neutral drift of a non-deterring inspector), others = the rest. R includes the arm's added inspector. Ratios are control / arm.

**c = 0, N = 10000.** Largest exit from R; hazards (and the ratio control / arm).

| arm | total | D light | E bounded-read | A shadow | other | largest | fixed-weight D / E (control weights) |
|---|---|---|---|---|---|---|---|
| control | 1.10e-04 | 6.79e-05 | 2.98e-05 | 1.22e-05 | 2.58e-07 | D strict other nonreader | - |
| ZT | 6.86e-05 (1.6×) | 3.09e-05 (2.2×) | 2.49e-05 (1.2×) | 1.27e-05 (1.0×) | 1.64e-07 (1.6×) | D strict other nonreader | 6.79e-05 / 2.98e-05 |
| SUS | 1.01e-04 (1.1×) | 6.66e-05 (1.0×) | 2.13e-05 (1.4×) | 1.24e-05 (1.0×) | 2.25e-07 (1.1×) | D strict other nonreader | 6.79e-05 / 2.98e-05 |
| ZT+SUS | 3.97e-05 (2.8×) | 1.79e-05 (3.8×) | 8.44e-06 (3.5×) | 1.32e-05 (0.9×) | 8.99e-08 (2.9×) | D strict other nonreader | 6.79e-05 / 2.98e-05 |
| SR1 | 9.65e-05 (1.1×) | 5.54e-05 (1.2×) | 2.81e-05 (1.1×) | 1.23e-05 (1.0×) | 7.20e-07 (0.4×) | D strict other nonreader | 7.03e-05 / 3.05e-05 |
| SR4 | 5.94e-05 (1.9×) | 2.71e-05 (2.5×) | 1.93e-05 (1.5×) | 1.29e-05 (1.0×) | 1.34e-07 (1.9×) | D strict other nonreader | 6.79e-05 / 2.98e-05 |
| SR16 | 4.13e-05 (2.7×) | 1.87e-05 (3.6×) | 9.37e-06 (3.2×) | 1.32e-05 (0.9×) | 9.28e-08 (2.8×) | D strict other nonreader | 6.79e-05 / 2.98e-05 |
| uncond. I | 1.21e-04 (0.9×) | 7.38e-05 (0.9×) | 3.53e-05 (0.8×) | 1.14e-05 (1.1×) | 3.66e-07 (0.7×) | D strict other nonreader | 6.79e-05 / 2.98e-05 |

**c = 0, N = 100000.** Largest exit from R; hazards (and the ratio control / arm).

| arm | total | D light | E bounded-read | A shadow | other | largest | fixed-weight D / E (control weights) |
|---|---|---|---|---|---|---|---|
| control | 1.01e-04 | 7.27e-05 | 2.67e-05 | 1.12e-06 | 4.22e-08 | D strict other nonreader | - |
| ZT | 5.27e-05 (1.9×) | 2.93e-05 (2.5×) | 2.22e-05 (1.2×) | 1.20e-06 (0.9×) | 2.30e-08 (1.8×) | D strict other nonreader | 7.27e-05 / 2.67e-05 |
| SUS | 9.04e-05 (1.1×) | 7.04e-05 (1.0×) | 1.88e-05 (1.4×) | 1.14e-06 (1.0×) | 3.10e-08 (1.4×) | D strict other nonreader | 7.27e-05 / 2.67e-05 |
| ZT+SUS | 5.75e-06 (17.5×) | 3.20e-06 (22.7×) | 1.20e-06 (22.2×) | 1.35e-06 (0.8×) | 2.09e-09 (20.2×) | D strict other nonreader | 7.27e-05 / 2.67e-05 |
| SR1 | 8.55e-05 (1.2×) | 5.92e-05 (1.2×) | 2.51e-05 (1.1×) | 1.13e-06 (1.0×) | 8.41e-08 (0.5×) | D strict other nonreader | 7.54e-05 / 2.73e-05 |
| SR4 | 3.87e-05 (2.6×) | 2.18e-05 (3.3×) | 1.56e-05 (1.7×) | 1.24e-06 (0.9×) | 1.32e-08 (3.2×) | D strict other nonreader | 7.27e-05 / 2.67e-05 |
| SR16 | 8.67e-06 (11.6×) | 4.83e-06 (15.1×) | 2.52e-06 (10.6×) | 1.32e-06 (0.8×) | 2.98e-09 (14.2×) | D strict other nonreader | 7.27e-05 / 2.67e-05 |
| uncond. I | 1.10e-04 (0.9×) | 7.91e-05 (0.9×) | 3.03e-05 (0.9×) | 1.00e-06 (1.1×) | 4.83e-08 (0.9×) | D strict other nonreader | 7.27e-05 / 2.67e-05 |

**c = 0.01, N = 10000.** Largest exit from R; hazards (and the ratio control / arm).

| arm | total | D light | E bounded-read | A shadow | other | largest | fixed-weight D / E (control weights) |
|---|---|---|---|---|---|---|---|
| control | 5.70e-04 | 8.44e-05 | 5.11e-05 | 1.42e-08 | 4.34e-04 | F strict inspector | - |
| ZT | 5.48e-04 (1.0×) | 6.35e-05 (1.3×) | 4.93e-05 (1.0×) | 1.43e-08 (1.0×) | 4.35e-04 (1.0×) | F strict inspector | 8.44e-05 / 5.11e-05 |
| SUS | 5.63e-04 (1.0×) | 8.41e-05 (1.0×) | 4.49e-05 (1.1×) | 1.42e-08 (1.0×) | 4.34e-04 (1.0×) | F strict inspector | 8.44e-05 / 5.11e-05 |
| ZT+SUS | 5.41e-04 (1.1×) | 6.27e-05 (1.3×) | 4.30e-05 (1.2×) | 1.43e-08 (1.0×) | 4.35e-04 (1.0×) | F strict inspector | 8.44e-05 / 5.11e-05 |
| SR1 | 5.63e-04 (1.0×) | 7.73e-05 (1.1×) | 5.19e-05 (1.0×) | 1.42e-08 (1.0×) | 4.34e-04 (1.0×) | F strict inspector | 8.66e-05 / 5.25e-05 |
| SR4 | 7.35e-04 (0.8×) | 8.74e-05 (1.0×) | 6.00e-05 (0.9×) | 1.22e-08 (1.2×) | 5.87e-04 (0.7×) | F strict inspector | 8.44e-05 / 5.11e-05 |
| SR16 | 7.79e-04 (0.7×) | 9.63e-05 (0.9×) | 6.62e-05 (0.8×) | 1.34e-08 (1.1×) | 6.17e-04 (0.7×) | F strict inspector | 8.44e-05 / 5.11e-05 |
| uncond. I | 5.94e-04 (1.0×) | 9.92e-05 (0.9×) | 6.81e-05 (0.8×) | 1.38e-08 (1.0×) | 4.27e-04 (1.0×) | F strict inspector | 8.44e-05 / 5.11e-05 |

**c = 0.01, N = 100000.** Largest exit from R; hazards (and the ratio control / arm).

| arm | total | D light | E bounded-read | A shadow | other | largest | fixed-weight D / E (control weights) |
|---|---|---|---|---|---|---|---|
| control | 5.69e-04 | 8.45e-05 | 5.11e-05 | 1.42e-09 | 4.34e-04 | F strict inspector | - |
| ZT | 5.47e-04 (1.0×) | 6.35e-05 (1.3×) | 4.93e-05 (1.0×) | 1.43e-09 (1.0×) | 4.34e-04 (1.0×) | F strict inspector | 8.45e-05 / 5.11e-05 |
| SUS | 5.63e-04 (1.0×) | 8.41e-05 (1.0×) | 4.49e-05 (1.1×) | 1.42e-09 (1.0×) | 4.34e-04 (1.0×) | F strict inspector | 8.45e-05 / 5.11e-05 |
| ZT+SUS | 5.41e-04 (1.1×) | 6.28e-05 (1.3×) | 4.30e-05 (1.2×) | 1.43e-09 (1.0×) | 4.35e-04 (1.0×) | F strict inspector | 8.45e-05 / 5.11e-05 |
| SR1 | 5.63e-04 (1.0×) | 7.73e-05 (1.1×) | 5.18e-05 (1.0×) | 1.42e-09 (1.0×) | 4.33e-04 (1.0×) | F strict inspector | 8.66e-05 / 5.25e-05 |
| SR4 | 7.34e-04 (0.8×) | 8.75e-05 (1.0×) | 6.00e-05 (0.9×) | 1.22e-09 (1.2×) | 5.87e-04 (0.7×) | F strict inspector | 8.45e-05 / 5.11e-05 |
| SR16 | 7.79e-04 (0.7×) | 9.64e-05 (0.9×) | 6.61e-05 (0.8×) | 1.34e-09 (1.1×) | 6.16e-04 (0.7×) | F strict inspector | 8.45e-05 / 5.11e-05 |
| uncond. I | 5.93e-04 (1.0×) | 9.93e-05 (0.9×) | 6.81e-05 (0.8×) | 1.38e-09 (1.0×) | 4.26e-04 (1.0×) | F strict inspector | 8.45e-05 / 5.11e-05 |

**Resident-specific one-state rates per mutation event** out of (arm's inspector, `C`), c = 0, N = 10⁴ / 10⁵: strict non-reading inspectee (light cheaters), strict reading inspectee (bounded-read), neutral shadow, strict inspector; and the payoffs and charged levels at the resident.

| arm | resident | N | D light | E bounded-read | A shadow | F strict inspector | total |
|---|---|---|---|---|---|---|---|
| control | (CRI,C) | 10000 | 5.47e-05 | 1.94e-05 | 1.53e-05 | 0.00e+00 | 8.95e-05 |
| control | (CRI,C) | 100000 | 5.47e-05 | 1.94e-05 | 1.53e-06 | 0.00e+00 | 7.56e-05 |
| ZT | (CRI,C) | 10000 | 5.47e-05 | 1.94e-05 | 1.53e-05 | 0.00e+00 | 8.96e-05 |
| ZT | (zt,C) | 10000 | 0.00e+00 | 1.78e-05 | 1.53e-05 | 0.00e+00 | 3.33e-05 |
| ZT | (CRI,C) | 100000 | 5.47e-05 | 1.94e-05 | 1.53e-06 | 0.00e+00 | 7.56e-05 |
| ZT | (zt,C) | 100000 | 0.00e+00 | 1.78e-05 | 1.53e-06 | 0.00e+00 | 1.93e-05 |
| SUS | (CRI,C) | 10000 | 5.47e-05 | 1.94e-05 | 1.53e-05 | 0.00e+00 | 8.96e-05 |
| SUS | (crs,C) | 10000 | 5.47e-05 | 0.00e+00 | 1.53e-05 | 0.00e+00 | 7.02e-05 |
| SUS | (CRI,C) | 100000 | 5.47e-05 | 1.94e-05 | 1.53e-06 | 0.00e+00 | 7.56e-05 |
| SUS | (crs,C) | 100000 | 5.47e-05 | 0.00e+00 | 1.53e-06 | 0.00e+00 | 5.62e-05 |
| ZT+SUS | (CRI,C) | 10000 | 5.47e-05 | 1.94e-05 | 1.53e-05 | 0.00e+00 | 8.96e-05 |
| ZT+SUS | (zts,C) | 10000 | 0.00e+00 | 0.00e+00 | 1.53e-05 | 0.00e+00 | 1.56e-05 |
| ZT+SUS | (CRI,C) | 100000 | 5.47e-05 | 1.94e-05 | 1.53e-06 | 0.00e+00 | 7.56e-05 |
| ZT+SUS | (zts,C) | 100000 | 0.00e+00 | 0.00e+00 | 1.53e-06 | 0.00e+00 | 1.56e-06 |
| SR1 | (CRI,C) | 10000 | 5.47e-05 | 1.94e-05 | 1.53e-05 | 0.00e+00 | 8.96e-05 |
| SR1 | (sr1,C) | 10000 | 2.61e-05 | 1.73e-05 | 1.53e-05 | 0.00e+00 | 6.02e-05 |
| SR1 | (CRI,C) | 100000 | 5.47e-05 | 1.94e-05 | 1.53e-06 | 0.00e+00 | 7.56e-05 |
| SR1 | (sr1,C) | 100000 | 2.61e-05 | 1.73e-05 | 1.53e-06 | 0.00e+00 | 4.51e-05 |
| SR4 | (CRI,C) | 10000 | 5.47e-05 | 1.94e-05 | 1.53e-05 | 0.00e+00 | 8.96e-05 |
| SR4 | (sr4,C) | 10000 | 1.31e-07 | 1.03e-05 | 1.53e-05 | 0.00e+00 | 2.60e-05 |
| SR4 | (CRI,C) | 100000 | 5.47e-05 | 1.94e-05 | 1.53e-06 | 0.00e+00 | 7.56e-05 |
| SR4 | (sr4,C) | 100000 | 1.31e-07 | 1.03e-05 | 1.53e-06 | 0.00e+00 | 1.20e-05 |
| SR16 | (CRI,C) | 10000 | 5.47e-05 | 1.94e-05 | 1.53e-05 | 0.00e+00 | 8.96e-05 |
| SR16 | (sr16,C) | 10000 | 0.00e+00 | 7.55e-07 | 1.53e-05 | 0.00e+00 | 1.63e-05 |
| SR16 | (CRI,C) | 100000 | 5.47e-05 | 1.94e-05 | 1.53e-06 | 0.00e+00 | 7.56e-05 |
| SR16 | (sr16,C) | 100000 | 0.00e+00 | 7.53e-07 | 1.53e-06 | 0.00e+00 | 2.31e-06 |
| uncond. I | (CRI,C) | 10000 | 5.47e-05 | 1.94e-05 | 1.53e-05 | 0.00e+00 | 8.95e-05 |
| uncond. I | (CRI,C) | 100000 | 5.47e-05 | 1.94e-05 | 1.53e-06 | 0.00e+00 | 7.56e-05 |

## Where π sits (c = 0; exclusive detour categories of the previous run)

| arm | N | E | shadow excursion | cheater majority | light cheater | committed and compliant | mixing | forfeit | share of the added inspector (in R) |
|---|---|---|---|---|---|---|---|---|---|
| control | 10000 | 0.1704 | 0.0026 | 0.0031 | 0.2987 | 0.4949 | 0.0303 | 0.0000 | - |
| control | 100000 | 0.0475 | 0.0006 | 0.0007 | 0.2585 | 0.6438 | 0.0490 | 0.0000 | - |
| ZT | 10000 | 0.2661 | 0.0026 | 0.0031 | 0.1997 | 0.4985 | 0.0300 | 0.0000 | 0.1510 (0.1510) |
| ZT | 100000 | 0.0882 | 0.0006 | 0.0007 | 0.2154 | 0.6483 | 0.0469 | 0.0000 | 0.0550 (0.0550) |
| SUS | 10000 | 0.1744 | 0.0024 | 0.0029 | 0.4217 | 0.3719 | 0.0267 | 0.0000 | 0.2964 (0.0649) |
| SUS | 100000 | 0.0372 | 0.0004 | 0.0005 | 0.6262 | 0.3063 | 0.0294 | 0.0000 | 0.4846 (0.0133) |
| ZT+SUS | 10000 | 0.4196 | 0.0024 | 0.0028 | 0.1859 | 0.3632 | 0.0261 | 0.0000 | 0.3124 (0.3123) |
| ZT+SUS | 100000 | 0.5344 | 0.0004 | 0.0005 | 0.1468 | 0.2901 | 0.0279 | 0.0000 | 0.5116 (0.5116) |
| SR1 | 10000 | 0.2139 | 0.0030 | 0.0035 | 0.2323 | 0.5116 | 0.0357 | 0.0000 | 0.0929 (0.0902) |
| SR1 | 100000 | 0.0647 | 0.0007 | 0.0008 | 0.2630 | 0.6177 | 0.0531 | 0.0000 | 0.0279 (0.0271) |
| SR4 | 10000 | 0.3006 | 0.0025 | 0.0030 | 0.1988 | 0.4652 | 0.0298 | 0.0000 | 0.1864 (0.1859) |
| SR4 | 100000 | 0.1163 | 0.0005 | 0.0007 | 0.2116 | 0.6255 | 0.0454 | 0.0000 | 0.0837 (0.0835) |
| SR16 | 10000 | 0.4055 | 0.0024 | 0.0029 | 0.1872 | 0.3758 | 0.0263 | 0.0000 | 0.2975 (0.2975) |
| SR16 | 100000 | 0.3823 | 0.0004 | 0.0005 | 0.1584 | 0.4283 | 0.0301 | 0.0000 | 0.3578 (0.3578) |
| uncond. I | 10000 | 0.1568 | 0.0033 | 0.0040 | 0.2712 | 0.5270 | 0.0377 | 0.0000 | - |
| uncond. I | 100000 | 0.0466 | 0.0007 | 0.0009 | 0.2975 | 0.5974 | 0.0569 | 0.0000 | - |

## Realized read costs and timeouts (π-weighted, per round)

| arm | c | N | mean levels charged to the inspector | median levels (inspector + inspectee) | forfeit (timeout) mass, inspector / inspectee |
|---|---|---|---|---|---|
| control | 0 | 10000 | 8.79e-01 | 1.00 | 2.6e-04 / 3.2e-04 |
| control | 0 | 100000 | 1.33e+00 | 1.00 | 1.8e-04 / 2.6e-04 |
| ZT | 0 | 10000 | 8.74e-01 | 1.00 | 2.2e-04 / 3.0e-04 |
| ZT | 0 | 100000 | 1.34e+00 | 1.00 | 1.6e-04 / 2.5e-04 |
| SUS | 0 | 10000 | 8.64e-01 | 1.00 | 1.8e-04 / 2.6e-04 |
| SUS | 0 | 100000 | 1.12e+00 | 1.00 | 9.4e-05 / 1.5e-04 |
| ZT+SUS | 0 | 10000 | 9.22e-01 | 1.00 | 1.8e-04 / 2.6e-04 |
| ZT+SUS | 0 | 100000 | 1.23e+00 | 1.00 | 8.9e-05 / 1.4e-04 |
| SR1 | 0 | 10000 | 8.35e-01 | 1.00 | 2.4e-04 / 3.3e-04 |
| SR1 | 0 | 100000 | 1.27e+00 | 1.00 | 1.7e-04 / 2.7e-04 |
| SR4 | 0 | 10000 | 1.92e+00 | 1.00 | 2.0e-04 / 2.9e-04 |
| SR4 | 0 | 100000 | 1.87e+00 | 1.00 | 1.5e-04 / 2.3e-04 |
| SR16 | 0 | 10000 | 4.92e+01 | 1.00 | 1.8e-04 / 2.6e-04 |
| SR16 | 0 | 100000 | 6.08e+01 | 9.25 | 9.6e-05 / 1.5e-04 |
| uncond. I | 0 | 10000 | 7.95e-01 | 1.00 | 2.6e-04 / 3.7e-04 |
| uncond. I | 0 | 100000 | 1.24e+00 | 1.00 | 1.8e-04 / 2.8e-04 |
| control | 0.01 | 10000 | 3.32e-01 | 0.50 | 3.1e-06 / 4.5e-06 |
| control | 0.01 | 100000 | 3.26e-01 | 0.50 | 3.1e-06 / 4.5e-06 |
| ZT | 0.01 | 10000 | 3.32e-01 | 0.50 | 3.1e-06 / 4.5e-06 |
| ZT | 0.01 | 100000 | 3.26e-01 | 0.50 | 3.0e-06 / 4.4e-06 |
| SUS | 0.01 | 10000 | 3.35e-01 | 0.50 | 2.6e-06 / 4.3e-06 |
| SUS | 0.01 | 100000 | 3.29e-01 | 0.50 | 2.6e-06 / 4.2e-06 |
| ZT+SUS | 0.01 | 10000 | 3.35e-01 | 0.50 | 2.6e-06 / 4.3e-06 |
| ZT+SUS | 0.01 | 100000 | 3.29e-01 | 0.50 | 2.6e-06 / 4.2e-06 |
| SR1 | 0.01 | 10000 | 3.17e-01 | 0.50 | 3.2e-06 / 4.6e-06 |
| SR1 | 0.01 | 100000 | 3.11e-01 | 0.00 | 3.1e-06 / 4.5e-06 |
| SR4 | 0.01 | 10000 | 3.68e-01 | 0.00 | 2.9e-06 / 4.7e-06 |
| SR4 | 0.01 | 100000 | 3.60e-01 | 0.00 | 2.8e-06 / 4.6e-06 |
| SR16 | 0.01 | 10000 | 3.54e-01 | 0.00 | 2.9e-06 / 4.8e-06 |
| SR16 | 0.01 | 100000 | 3.46e-01 | 0.00 | 2.9e-06 / 4.7e-06 |
| uncond. I | 0.01 | 10000 | 2.48e-01 | 0.00 | 2.9e-06 / 4.8e-06 |
| uncond. I | 0.01 | 100000 | 2.43e-01 | 0.00 | 2.9e-06 / 4.7e-06 |

## Lottery (ε = 0; (N, I) = (100, 64), mN = 1, horizon 2,000; paired founders)

**n100i64, c = 0** (40 runs): efficient islands at the horizon, paired difference arm − control [95% CI], unresolved islands (a role's top class below 0.9) at the horizon, share of the added program, efficient with a responsive inspector, inspector payoff, replaced founder slots per run.

| arm | efficient | Δ vs control | unresolved | added share | efficient & responsive | efficient & shadow | light-cheater islands | inspector payoff | replaced slots |
|---|---|---|---|---|---|---|---|---|---|
| control | 0.725 [0.588, 0.852] | - | 0.297 [0.211, 0.385] | 0.5866 [0.4512, 0.7189] | 0.719 [0.583, 0.848] | 0.006 [0.000, 0.015] | 0.158 [0.058, 0.272] | -0.192 [-0.306, -0.093] | 9.0 |
| ZT | 0.751 [0.602, 0.876] | 0.026 [-0.101, 0.153] | 0.355 [0.271, 0.438] | 0.2192 [0.1183, 0.3262] | 0.742 [0.599, 0.868] | 0.009 [0.000, 0.024] | 0.175 [0.075, 0.300] | -0.158 [-0.258, -0.073] | 9.0 |
| SUS | 0.751 [0.602, 0.876] | 0.026 [-0.120, 0.167] | 0.404 [0.321, 0.484] | 0.3504 [0.2284, 0.4746] | 0.730 [0.589, 0.856] | 0.021 [0.005, 0.041] | 0.175 [0.073, 0.300] | -0.164 [-0.267, -0.074] | 9.0 |
| ZT+SUS | 0.766 [0.632, 0.886] | 0.042 [-0.089, 0.168] | 0.356 [0.273, 0.436] | 0.3186 [0.2014, 0.4443] | 0.723 [0.591, 0.844] | 0.043 [0.009, 0.091] | 0.165 [0.061, 0.285] | -0.146 [-0.236, -0.066] | 9.0 |
| SR1 | 0.699 [0.552, 0.842] | -0.026 [-0.135, 0.079] | 0.338 [0.248, 0.427] | 0.1924 [0.0932, 0.3016] | 0.681 [0.540, 0.813] | 0.018 [0.002, 0.039] | 0.129 [0.034, 0.234] | -0.219 [-0.334, -0.113] | 9.0 |
| SR4 | 0.726 [0.577, 0.851] | 0.001 [-0.117, 0.117] | 0.357 [0.266, 0.448] | 0.1775 [0.0896, 0.2774] | 0.709 [0.568, 0.838] | 0.016 [0.002, 0.036] | 0.199 [0.075, 0.324] | -0.205 [-0.323, -0.099] | 9.0 |
| SR16 | 0.776 [0.650, 0.900] | 0.051 [-0.083, 0.184] | 0.336 [0.244, 0.424] | 0.2230 [0.1227, 0.3388] | 0.766 [0.628, 0.891] | 0.009 [0.000, 0.025] | 0.175 [0.075, 0.300] | -0.146 [-0.246, -0.061] | 9.0 |
| uncond. I | 0.681 [0.538, 0.817] | -0.044 [-0.166, 0.072] | 0.319 [0.241, 0.396] | 0.0000 [0.0000, 0.0000] | 0.673 [0.531, 0.806] | 0.008 [0.000, 0.020] | 0.164 [0.064, 0.278] | -0.204 [-0.310, -0.107] | 9.0 |

**n100i64, c = 0.01** (40 runs): efficient islands at the horizon, paired difference arm − control [95% CI], unresolved islands (a role's top class below 0.9) at the horizon, share of the added program, efficient with a responsive inspector, inspector payoff, replaced founder slots per run.

| arm | efficient | Δ vs control | unresolved | added share | efficient & responsive | efficient & shadow | light-cheater islands | inspector payoff | replaced slots |
|---|---|---|---|---|---|---|---|---|---|
| control | 0.700 [0.550, 0.825] | - | 0.210 [0.135, 0.288] | 0.4862 [0.3561, 0.6216] | 0.598 [0.451, 0.741] | 0.102 [0.024, 0.192] | 0.238 [0.113, 0.369] | -0.250 [-0.381, -0.138] | 9.0 |
| ZT | 0.702 [0.553, 0.827] | 0.002 [-0.123, 0.126] | 0.285 [0.213, 0.359] | 0.1675 [0.0878, 0.2594] | 0.637 [0.497, 0.775] | 0.064 [0.014, 0.131] | 0.247 [0.125, 0.377] | -0.246 [-0.372, -0.129] | 9.0 |
| SUS | 0.652 [0.502, 0.777] | -0.048 [-0.197, 0.077] | 0.308 [0.241, 0.375] | 0.2490 [0.1431, 0.3609] | 0.565 [0.416, 0.700] | 0.086 [0.026, 0.159] | 0.263 [0.146, 0.395] | -0.291 [-0.423, -0.172] | 9.0 |
| ZT+SUS | 0.702 [0.553, 0.827] | 0.002 [-0.123, 0.126] | 0.293 [0.227, 0.361] | 0.1822 [0.0962, 0.2787] | 0.579 [0.441, 0.716] | 0.123 [0.050, 0.208] | 0.227 [0.111, 0.349] | -0.246 [-0.372, -0.129] | 9.0 |
| SR1 | 0.652 [0.502, 0.800] | -0.048 [-0.148, 0.051] | 0.270 [0.190, 0.352] | 0.1785 [0.0871, 0.2801] | 0.611 [0.461, 0.759] | 0.041 [0.000, 0.105] | 0.239 [0.122, 0.366] | -0.372 [-0.614, -0.186] | 9.0 |
| SR4 | 0.680 [0.531, 0.808] | -0.020 [-0.148, 0.106] | 0.193 [0.123, 0.271] | 0.0000 [0.0000, 0.0000] | 0.606 [0.455, 0.745] | 0.074 [0.012, 0.154] | 0.201 [0.095, 0.322] | -0.336 [-0.580, -0.154] | 9.0 |
| SR16 | 0.677 [0.527, 0.803] | -0.023 [-0.148, 0.102] | 0.165 [0.102, 0.234] | 0.0000 [0.0000, 0.0000] | 0.634 [0.485, 0.776] | 0.043 [0.000, 0.101] | 0.261 [0.140, 0.395] | -0.246 [-0.364, -0.138] | 9.0 |
| uncond. I | 0.682 [0.532, 0.825] | -0.018 [-0.160, 0.125] | 0.173 [0.101, 0.250] | 0.0000 [0.0000, 0.0000] | 0.594 [0.445, 0.735] | 0.089 [0.019, 0.171] | 0.188 [0.082, 0.310] | -0.218 [-0.336, -0.113] | 9.0 |

**n400i64, c = 0** (20 runs): efficient islands at the horizon, paired difference arm − control [95% CI], unresolved islands (a role's top class below 0.9) at the horizon, share of the added program, efficient with a responsive inspector, inspector payoff, replaced founder slots per run.

| arm | efficient | Δ vs control | unresolved | added share | efficient & responsive | efficient & shadow | light-cheater islands | inspector payoff | replaced slots |
|---|---|---|---|---|---|---|---|---|---|
| control | 0.430 [0.228, 0.641] | - | 0.419 [0.295, 0.538] | 0.5969 [0.4329, 0.7603] | 0.430 [0.228, 0.641] | 0.000 [0.000, 0.000] | 0.416 [0.230, 0.615] | -0.333 [-0.477, -0.200] | 32.6 |
| ZT | 0.685 [0.476, 0.869] | 0.255 [-0.008, 0.511] | 0.390 [0.269, 0.505] | 0.2588 [0.1120, 0.4234] | 0.685 [0.476, 0.869] | 0.000 [0.000, 0.000] | 0.237 [0.080, 0.428] | -0.209 [-0.360, -0.078] | 32.6 |
| SUS | 0.550 [0.350, 0.750] | 0.120 [-0.159, 0.381] | 0.553 [0.464, 0.638] | 0.6416 [0.5138, 0.7569] | 0.550 [0.350, 0.750] | 0.000 [0.000, 0.000] | 0.450 [0.250, 0.650] | -0.250 [-0.375, -0.125] | 32.6 |
| ZT+SUS | 0.650 [0.450, 0.850] | 0.220 [-0.080, 0.506] | 0.570 [0.442, 0.687] | 0.3101 [0.1815, 0.4555] | 0.650 [0.450, 0.850] | 0.000 [0.000, 0.000] | 0.306 [0.110, 0.506] | -0.200 [-0.324, -0.086] | 32.6 |
| SR16 | 0.750 [0.550, 0.900] | 0.320 [0.041, 0.589] | 0.432 [0.305, 0.554] | 0.2624 [0.1174, 0.4163] | 0.750 [0.550, 0.900] | 0.000 [0.000, 0.000] | 0.231 [0.078, 0.423] | -0.174 [-0.325, -0.050] | 32.6 |

**Validation at (400, 64), c = 0:** the validation arm `v0` against the stored cell of the previous run, efficient islands at generation 8,000 per run: max |Δ| = 0.0e+00 (stored mean 0.672, `v0` mean 0.672).

## D-phase control (extra, outside the spec; notes §1.3): the same arms at depth D = 11 and D = 13, c = 0

| D | arm | N = 10⁴ | N = 10⁵ | gain over the same-D control, N = 10⁵ |
|---|---|---|---|---|
| 11 | control | 0.0194 | 0.0023 | - |
| 11 | SUS | 0.0247 | 0.0029 | 0.001 |
| 11 | ZT+SUS | 0.0252 | 0.0030 | 0.001 |
| 11 | ZT | 0.0865 | 0.0659 | 0.064 |
| 11 | SR16 | 0.0814 | 0.0611 | 0.059 |
| 13 | control | 0.0061 | 0.0008 | - |
| 13 | SUS | 0.0114 | 0.0015 | 0.001 |
| 13 | ZT+SUS | 0.0277 | 0.0226 | 0.022 |
| 13 | ZT | 0.0306 | 0.0323 | 0.031 |
| 13 | SR16 | 0.0277 | 0.0236 | 0.023 |
(D = 12 gains over the control at N = 10⁵: SUS -0.010, ZT+SUS +0.487, ZT +0.041, SR16 +0.335.)

## Verdicts

Scoring rules are those of the predictions file. Chain numbers are ε → 0 quantities; lottery numbers are finite-horizon.

| # | claim | measured | verdict |
|---|---|---|---|
| 1 | ZT closes the light-cheater exit (≥ 10× at N = 10⁴ and 10⁵) and π(E)(10⁵) ≥ 0.1 [< 0.07] | D-hazard ratio control/ZT 2.2× (N = 10⁴), 2.5× (N = 10⁵); π(E)_ZT(10⁵) = 0.0882 (control 0.0475, gain +0.0407); largest exit from R: D strict other nonreader; resident (zt, C) D hazard 0.00e+00 | **partial** |
| 1c | counter (gemini-4-argon): the bounded-read exit absorbs the flow, π(E) < 0.10 | π(E)_ZT(10⁵) = 0.0882; largest exit from R: D strict other nonreader | **failed** |
| 2 | ZT+SUS ≥ 0.5 [< 0.3]; SUS within 0.1 of 0.036, i.e. ≤ 0.136 [> 0.2] (N = 10⁵) | π(E): ZT+SUS 0.5344 (gain +0.4869), SUS 0.0372 (gain -0.0103), control 0.0475 | **held** |
| 2c | counter (gpt-6.1-sol): targeted E-hazard falls ≥ 10× at both N in SUS and ZT+SUS but π(E)_ZT+SUS < 0.5 | E-hazard ratios control/arm: SUS 1.4 / 1.4, ZT+SUS 3.5 / 22.2; π(E)_ZT+SUS = 0.5344 | **failed** |
| 3 | SR16 gains ≥ 0.1 over the control, SR1 does not [SR16 < 0.05] (N = 10⁵) | gain(SR16) = +0.3349 (π(E) 0.3823), gain(SR1) = +0.0173 (π(E) 0.0647); SR16 resident D hazard 0.00e+00 | **held** |
| 3c | counter (gpt-6.1-sol): gain depends on the q grid (scored: SR16 gain < 0.1 while its resident has no light-cheater exit) | gain +0.3349; resident D = 0.00e+00 | **failed** |
| 4 | at c = 0.01 SR16 loses to ZT: π(E)_ZT − π(E)_SR16 ≥ 0.02 at N = 10⁴ and 10⁵ [≤ 0 at both] | N = 10000: +0.0665 (ZT 0.4020, SR16 0.3355); N = 100000: +0.0660 (ZT 0.3944, SR16 0.3283) | **held** |
| 5 | every arm's efficient islands at (100, 64) move by < 0.1 against the control [> 0.15] (both prices) | max |Δ| = 0.051 (SR16, c = 0; CI 0.051 [-0.083, 0.184]); 14 of 14 arm-price cells run | **held** |
| E1 | SUS and ZT+SUS cut the bounded-read (E) hazard from R by ≥ 10× at N = 10⁴ and 10⁵ | control/arm: SUS 1.4 / 1.4, ZT+SUS 3.5 / 22.2 | **failed** |
| E2 | the SUS gain at D = 11 is ≥ 0.2 below its D = 12 gain (N = 10⁵) [within 0.1] | gain D = 12: -0.0103; D = 11: +0.0006; D = 13: 0.0007 | **failed** |
| E2′ (post hoc, not registered) | gain over the same-D control at N = 10⁵, D = 12 / 11 / 13 | ZT+SUS: 0.487 / 0.001 / 0.022; SR16: 0.335 / 0.059 / 0.023 | descriptive |
| E3 | ZT occupancy of the light-cheater detour at N = 10⁵ ≥ 3× below the control's | control 0.2585, ZT 0.2154 (1.2×) | **failed** |
| E4 | the unconditional-inspector comparator gains < 0.05 at N = 10⁵ | gain -0.0009 (π(E) 0.0466) | **held** |
| E5 | the SR1 arm differs from the control by < 0.03 in π(E), N = 10³–10⁵ | N = 1000: +0.0132; N = 10000: +0.0435; N = 100000: +0.0173 | **failed** |
| E6 | SR16 is not immune: its category-E hazard from R is not zero at N = 10⁵ | aggregate E 2.52e-06; resident (sr16, C) E 7.53e-07 | **held** |

## Support, transitions and circulation (CLAUDE.md rule 4)

| arm | c | N | states carrying 0.99 of π | balance residual | circulation | mean sojourn in R | mean time outside R |
|---|---|---|---|---|---|---|---|
| control | 0 | 10000 | 198 | 1.1e-06 | 1.000 | 9.070e+03 | 4.707e+04 |
| control | 0 | 100000 | 140 | 1.2e-06 | 1.000 | 9.941e+03 | 2.084e+05 |
| ZT | 0 | 10000 | 214 | 1.5e-06 | 1.000 | 1.457e+04 | 4.204e+04 |
| ZT | 0 | 100000 | 151 | 1.7e-06 | 1.000 | 1.896e+04 | 2.008e+05 |
| SUS | 0 | 10000 | 203 | 1.2e-06 | 1.000 | 9.942e+03 | 4.990e+04 |
| SUS | 0 | 100000 | 123 | 1.3e-06 | 1.000 | 1.106e+04 | 2.979e+05 |
| ZT+SUS | 0 | 10000 | 199 | 1.2e-06 | 1.000 | 2.522e+04 | 3.607e+04 |
| ZT+SUS | 0 | 100000 | 128 | 1.5e-06 | 1.000 | 1.740e+05 | 1.524e+05 |
| SR1 | 0 | 10000 | 217 | 1.2e-06 | 1.000 | 1.036e+04 | 4.049e+04 |
| SR1 | 0 | 100000 | 154 | 1.2e-06 | 1.000 | 1.169e+04 | 1.757e+05 |
| SR4 | 0 | 10000 | 211 | 1.2e-06 | 1.000 | 1.683e+04 | 4.082e+04 |
| SR4 | 0 | 100000 | 149 | 1.5e-06 | 1.000 | 2.586e+04 | 2.002e+05 |
| SR16 | 0 | 10000 | 200 | 1.2e-06 | 1.000 | 2.421e+04 | 3.672e+04 |
| SR16 | 0 | 100000 | 132 | 1.2e-06 | 1.000 | 1.153e+05 | 1.874e+05 |
| uncond. I | 0 | 10000 | 231 | 1.4e-06 | 1.000 | 8.278e+03 | 4.860e+04 |
| uncond. I | 0 | 100000 | 158 | 1.1e-06 | 1.000 | 9.054e+03 | 1.966e+05 |
| control | 0.01 | 10000 | 234 | 1.5e-06 | 1.000 | 1.756e+03 | 4.409e+03 |
| control | 0.01 | 100000 | 232 | 1.6e-06 | 1.000 | 1.757e+03 | 4.530e+03 |
| ZT | 0.01 | 10000 | 247 | 1.2e-06 | 1.000 | 1.826e+03 | 4.332e+03 |
| ZT | 0.01 | 100000 | 244 | 1.3e-06 | 1.000 | 1.827e+03 | 4.453e+03 |
| SUS | 0.01 | 10000 | 249 | 1.3e-06 | 1.000 | 1.775e+03 | 4.398e+03 |
| SUS | 0.01 | 100000 | 247 | 1.4e-06 | 1.000 | 1.776e+03 | 4.521e+03 |
| ZT+SUS | 0.01 | 10000 | 246 | 1.6e-06 | 1.000 | 1.849e+03 | 4.318e+03 |
| ZT+SUS | 0.01 | 100000 | 243 | 1.3e-06 | 1.000 | 1.850e+03 | 4.440e+03 |
| SR1 | 0.01 | 10000 | 243 | 1.5e-06 | 1.000 | 1.776e+03 | 4.557e+03 |
| SR1 | 0.01 | 100000 | 240 | 1.4e-06 | 1.000 | 1.778e+03 | 4.695e+03 |
| SR4 | 0.01 | 10000 | 256 | 1.3e-06 | 1.000 | 1.361e+03 | 4.414e+03 |
| SR4 | 0.01 | 100000 | 252 | 1.4e-06 | 1.000 | 1.362e+03 | 4.541e+03 |
| SR16 | 0.01 | 10000 | 254 | 1.3e-06 | 1.000 | 1.284e+03 | 4.581e+03 |
| SR16 | 0.01 | 100000 | 250 | 1.4e-06 | 1.000 | 1.284e+03 | 4.712e+03 |
| uncond. I | 0.01 | 10000 | 249 | 1.5e-06 | 1.000 | 1.684e+03 | 6.201e+03 |
| uncond. I | 0.01 | 100000 | 246 | 1.3e-06 | 1.000 | 1.685e+03 | 6.376e+03 |

Return to R after the shadow-exploited state (first entry into E from (`N`, `K`) lands in R with probability; mean time to R, mutation events), c = 0:

| arm | N = 10⁴ | N = 10⁵ |
|---|---|---|
| control | 0.0280; 1.40e+04 | 0.0296; 3.33e+04 |
| ZT | 0.0280; 1.40e+04 | 0.0296; 3.29e+04 |
| SUS | 0.0280; 1.41e+04 | 0.0296; 3.38e+04 |
| ZT+SUS | 0.0280; 1.40e+04 | 0.0296; 3.30e+04 |
| SR1 | 0.0273; 1.46e+04 | 0.0288; 3.45e+04 |
| SR4 | 0.0279; 1.41e+04 | 0.0295; 3.32e+04 |
| SR16 | 0.0280; 1.40e+04 | 0.0296; 3.30e+04 |
| uncond. I | 0.0207; 1.88e+04 | 0.0223; 4.25e+04 |

