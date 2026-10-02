# Ergodic islands: mutation re-injected (THEORY §9.5 (i))

Predictions: `predictions/2026-10-02-ergodic-islands.md`, committed before the runs (7700c50).

Reviews: `reviews/2026-10-02-ergodic-islands-gpt-6-astra.md` and `reviews/2026-10-02-ergodic-islands-fable.md`.

Code: `src/ergodic_islands.py`:
- `run_static`: the two-level ε→0 chain;
- `run_mc`: Monte Carlo global fixation at fixed mN;
- `run_abm`: finite-ε island runs through `islands.run_one`;
- `report`.

`src/islands.py` gains hypercube and torus island graphs, island P(C,C) by dominant class, and exits from islands
that were ≥ 90% R.

Raw data: `runs/ergodic-islands.json`.

PD, w = 0.3, w_g = 0. Weak arm L_6 with `ROLE`, where R = `THEM(^C)`. Modal arm n = 6, where R = FairBot.

## Summary

**ε→0 object, A and B.** The chain over monomorphic metapopulation states depends on three rates:
- *Entry* is set by island size N, through local relatedness.
  - It is I-independent and graph-independent at mN ≤ 1: all 24 entry cells at mN ≤ 1 contain their predicted
    bands.
  - It falls with migration: 0.50 × ρ_N at mN = 10.
- *The shadow exit* is 1/(IN), so it is set by total size M alone.
- *The faker exit* is a structural constant. The faker's Φ is 1 − 1/r, constant selection under T + S = R + P, at
  every mN from 0.1 to 10, on complete, hypercube and torus island graphs. Measured: 0.255–0.287 for `THEM(^D)`
  against 0.264, and 0.138–0.157 for `THEM(^X)` against 0.142.

Consequences:
- **The faker share of exits from all-`THEM(^C)` depends only on M = IN.** Crossover at M ≈ 860; the share is 0.88
  at every split of M = 6,400. Above M ≈ 10³ the faker is the binding exit on islands as well-mixed.
- **The weak arm does not become efficient on islands.** π(all-`THEM(^C)`) rises with I to a plateau
  p*(N) = μ_R ρ_N(R|D)/f:
  - 0.125 at N = 10–16;
  - 0.069 at N = 100;
  - 0.024 at N = 1000.

  The plateau falls like N^(−0.46). The well-mixed peak in M (0.013) becomes a plateau about 5–10× higher, never
  above 0.13.
- **The modal arm becomes efficient faster on islands.** P(C,C) is 0.90 / 0.97 / 0.99 at I = 64 / 256 / 1024
  (N = 100), against 0.54 and 0.69 well-mixed at M = 6,400 and 25,600. The log-odds slope in I is 0.97. The gain runs
  through its three unfakeable provers. Its six fakeable provers saturate, and their share of the cooperative block
  falls like I^(−0.92). Islands select for unfakeability inside the family.

**Finite ε, C: approach rates in the other order** (I → ∞ at fixed per-island εN). Here adding islands *hurts* the
weak arm. At εN = 0.1, mN = 1, N = 100:
- P(C,C) is 0.154 / 0.144 / 0.040 at I = 16 / 64 / 256, and 0.024 on the hypercube at I = 256;
- R-dominant island-time is 0.051 / 0.029 / 0.008.

The global mutation supply I·εN grows with I, so fakers are always present somewhere and spread by migration. Of
finite-ε P(C,C) at I = 64 (0.144), only 0.028 is R-dominant islands, below the chain's π_R of 0.062. The rest is:
- probe self-play (`THEM(^ROLE)` and `THEM(^X)` islands, coin-flip cooperation): 0.049;
- ALLC islands: 0.036;
- other classes: 0.015;
- islands with no dominant class: 0.017.

The modal arm is at 0.98 (εN = 0.1) and 0.998 (εN = 0.01) at every I.

## Verdicts

| # | prediction | outcome |
|---|---|---|
| 1 | weak π_R within ±5% of the reduction (N ≥ 10); non-decreasing in I; plateau slope in [−0.55, −0.38]; max over N at N ∈ [8, 25]; P(C,C) ≤ 0.15 | **Holds.** Worst deviation 4.4% at (N, I) = (10, 1). Slope −0.46. The I = 4096 plateau is 0.1253 / 0.1254 / 0.1153 at N = 10 / 16 / 25 (0.097 at N = 5). Max P(C,C) 0.127 for N ≥ 10. |
| 2 | faker share within ±0.03 of f/(f + 0.2493/M) for N ≥ 25; crossover between M = 640 and 1,000; > 0.95 for M ≥ 25,600; weak + other exits < 0.01 | **Partly.** The formula holds (worst 0.011), and so do the crossover (0.486 at M = 800, 0.533 at M = 1,000) and the large-M share (0.964–0.966 at M = 25,600). Weak + other exits are below 0.01 except at small M: (25, 1) 0.38, (50, 1) 0.11, (25, 4) 0.014, where X and `ROLE` exits remain. |
| 3 | support all-D + all-`THEM(^C)` (+ X, `ROLE` at small M); weak-faker sink 0.0029 / 0.0078 / 0.0114 at I = 4096; `THEM(^C)` ≥ 0.8 of cooperative entry; π(faker states) < 0.005 | **Partly.** Holds for N ≥ 25: the sink is 0.0029 / 0.0078 / 0.0114, exactly; `THEM(^C)` carries 0.99 of entry; π(faker states) ≤ 0.0031. It fails at N ≤ 16, I = 1: C (0.027) and `not(ROLE)` (0.026, 0.013) are in the support, and `THEM(^C)` carries 0.02 of entry at N = 10. π(faker states) is 0.0051 at N = 5. |
| 4 | modal P(C,C) at N = 100 within ±0.02 of 0.418 / 0.712 / 0.899 / 0.972 / 0.993 *(seen)*; log-odds slope in I ∈ [0.9, 1.05]; fakeable/unfakeable log-slope ∈ [−1.1, −0.9]; islands above well-mixed at equal M | **Holds.** 0.4177 / 0.7115 / 0.8993 / 0.9718 / 0.9927. Slope 0.966. Ratio slope −0.919 at N = 100 (−0.977 at 400, −0.990 at 1000; −0.863 at N = 50, outside). Island above well-mixed in 19 of 19 equal-M cells. |
| 5 | every faker cell's interval contains 1 − 1/r ± 5% | **Holds**, 11 of 11. Pooled `THEM(^D)` at N = 100: 0.270 against 0.264. |
| 6 | entry/ρ_N bands: [0.9, 1.1] at mN = 0.1; [0.75, 1.0] at mN = 1 (N = 100); [0.5, 0.85] at N = 25, mN = 1; [0.85, 1.05] at N = 400; no I trend | **Holds**, all 24 entry cells at mN ≤ 1 contain. Point estimates at mN = 0.1, N = 100 are 0.87–1.19. Pooled over both I = 4 graphs at mN = 0.1 the ratio is 0.865 (2.6σ below 1); I read this as noise across 16 cells. N = 25, mN = 1 gives 0.79 (I = 64) and 0.63 (I = 16). |
| 7 | complete/hypercube (and torus) ratio intervals contain 1 in ≥ 90% of pairs; shadow contains 1/(IN) | **Holds**, 12 of 12 ratio intervals contain 1. Shadow 0.0031 [0.0023, 0.0042] and 0.0025 [0.0019, 0.0034] against 0.0025. |
| 8 | entry falls over mN = 0.1, 1, 3, 10; 0.4–0.8 × ρ_N at mN = 3; [0.003, 0.02] at mN = 10; ladder within [0.9, 1.1] at mN ≤ 0.1; faker bands at mN = 10 | **Holds on the interval rule; the mN = 10 point fails.** Entry is 0.0431 / 0.0422 / 0.0330 / 0.0209. At mN = 3 it is 0.79×. At mN = 10 it is 0.0209 [0.0179, 0.0245]: the interval grazes the band, but the point is above it, at 3.9× the well-mixed ρ_6400 = 0.0054. The falsifier (above 0.5 × ρ_N = 0.0211) was missed by 0.0002. Ladder 0.95 / 0.95 / 0.65 / 0.61 × Φ₂ at mN = 0.01 / 0.1 / 1 / 3. Faker cells at mN = 10 are 1.01× and 1.10×. |
| 9 | patched π_R within ±25% of two-level at mN ≤ 1, N ≥ 100; at mN = 10 within ×2 of well-mixed π_R (0.0086) | **Partly.** At mN ≤ 1 the ratio is 0.86–1.18 in all 19 cells. At mN = 10 it **fails**: 0.0303, 3.5× the well-mixed value. Islands keep half their advantage at 10 migrants per island per generation. |
| 10 | finite ε, εN = 0.1: P(C,C) in [0.09, 0.19] at I = 64, 256 ([0.06, 0.19] at I = 16); \|P(256) − P(64)\| ≤ 0.04; R-dominant time at I = 64 in [0.01, 0.06] and below π_R; ≥ 0.3 of P(C,C) from no-dominant islands; hypercube within 0.05; no cell > 0.3 | **Failed.** I = 64 is 0.144 and I = 16 is 0.154, which hold. I = 256 is 0.040, and the flatness bullet fails (difference 0.104). R-dominant time at I = 64 is 0.029, below π_R = 0.062, which holds. The no-dominant share is 0.12, which fails. Hypercube is within 0.032 and 0.016, and no cell exceeds 0.3, both holding. I = 16 is indeterminate by verdict 14. |
| 11 | (descriptive) fakers + weak fakers carry ≥ half of exits from ≥ 90%-R islands at I = 64, εN = 0.1 | **Holds:** 0.78 (332 of 428). Other cells: 0.84 at I = 256; 0.68 at εN = 0.01, I = 64; 0.45 at I = 16. At N = 25 the shadow dominates: faker 243, shadow 581, of 1,322. |
| 12 | [after review, reversed] N = 25 at most N = 100 + 0.02 | **Partly.** I = 64: 0.145 against 0.144, holds. I = 256: 0.076 against 0.040, **fails**. My pre-review direction (N = 25 ≥ N = 100 − 0.03) would have held at both. |
| 13 | modal ≥ 0.95 at εN = 0.1, ≥ 0.9 at εN = 0.01 | **Holds:** 0.980–0.981 and 0.997–0.999. The first half at I = 16, εN = 0.01 is 0.83, the slow approach fable predicted. |
| 14 | halves within 0.05 at εN = 0.1; all-R and all-D starts within 0.05 | **Partly.** All εN = 0.1 cells agree except weak I = 16 (0.154 against 0.098, replicates 0.06–0.21), so verdicts 10–12 at I = 16 are indeterminate. The all-R and all-D second halves are *identical* in the weak arm at I = 64 (both εN), because the two starts coalesce onto one trajectory under common random numbers, as in E3. Modal agrees to 0.001. At εN = 0.01 the weak halves differ by 0.03–0.09, an approach that is still running. |

**No falsifier fired.** The nearest was entry at mN = 10, at 0.498 × ρ_N against a threshold of 0.5.

## Support and transitions

**Weak arm, two-level chain.**
- The support is all-D (0.85–0.99) and all-`THEM(^C)`.
- At large I and N ≤ 25 it also includes the weak-faker sink `and(X,THEM(^D))`. That state is fed only from R and
  left only by drift, so its mass grows ∝ I, to 0.011 at (10, 4096).
- At N ≤ 16 and I = 1 it also includes X, `ROLE`, C and `not(ROLE)`.
- Polymorphic states are excluded by construction. No class coexists with D or `THEM(^C)`, and at I = 1 the chain
  equals the attractor chain.
- No transition is indeterminate.

Roads:
- *In:* the `THEM(^C)` mutant into all-D, 0.99 of cooperative entry at N ≥ 25.
- *Out:* faker → faker state → all-C (ALLC strictly invades `THEM(^D)` and `THEM(^X)`) → all-D; or shadow → all-C
  → all-D.

The top flows at (100, 64) are C → D, D → `THEM(^C)`, `THEM(^X)` → C, `THEM(^ROLE)` → C, D → `THEM(^X)` and
D → `THEM(^ROLE)`. The top exits from all-`THEM(^C)` are `THEM(^D)` 1.36·10⁻⁴, `THEM(^X)` 7.0·10⁻⁵, `THEM(^ROLE)`
6.6·10⁻⁵ and C 3.9·10⁻⁵.

**Modal arm.**
- The support is all-D plus the three unfakeable provers, `BOX(THEM(ME))`, `BOX(THEM(THEM))` and `BOX1(THEM(ME))`,
  at equal weight.
- The fakeable `BOX1(THEM(THEM))` holds 0.032 at I = 1 and 0.002 at I = 1024 (N = 100).
- At I ≥ 256, exits from conditional cooperators are 0.65 neutral drift to unconditional cooperators and 0.35 strict (0.95 and 0.05 at I = 1), the strict ones
  all from fakeable provers. Both scale as 1/I at large I.

**Finite ε, weak arm.** Island dominant classes are mostly D. Probes (`THEM(^ROLE)`, `THEM(^X)`, `THEM(^and(X,ROLE))`)
hold 0.2–0.45 of island-time at I = 64, and `THEM(^D)` holds 0.07 at I = 256. Dominance-flip exits from R are
faker : shadow = 1,834 : 1,167 at I = 64, εN = 0.1, matching the multilevel anchor (6,582 : 4,286).

## Order of limits

The two objects move in opposite directions in I:
- ε → 0 first (A): π_R at N = 100 is 0.046 / 0.062 / 0.067 at I = 16 / 64 / 256.
- I → ∞ at fixed εN = 0.1 (C): R-dominant island-time is 0.051 / 0.029 / 0.008.

The ε→0 object needs ε·I·N·T_abs ≪ 1. Each extra island adds mutation supply, and with it fakers, faster than it
adds reciprocator reservoirs. At εN = 0.01 the fall is weaker: P(C,C) is 0.183 and 0.156 at I = 64 and 256, and
R-dominant time is 0.083 and 0.022. Neither order makes the weak arm efficient.

## Generated tables

PD, w = 0.3. Weak arm L_6 with `ROLE` (R = `THEM(^C)`); modal arm n = 6 (R = FairBot `BOX(THEM(ME))`). A: eps->0 two-level chain over monomorphic metapopulation states (graph-independent on regular island graphs). B: Monte Carlo global fixation at fixed mN. C: finite-eps agent-based approach runs (not pi).

### A. weak arm: P(C,C) (rows N, columns I)

| N \ I | 1 | 4 | 16 | 64 | 256 | 1024 | 4096 |
|---|---|---|---|---|---|---|---|
| 5 | 0.1365 | 0.0101 | 0.0114 | 0.0367 | 0.0706 | 0.0919 | 0.0978 |
| 10 | 0.0616 | 0.0072 | 0.0269 | 0.0654 | 0.1040 | 0.1219 | 0.1266 |
| 16 | 0.0249 | 0.0115 | 0.0364 | 0.0782 | 0.1109 | 0.1235 | 0.1267 |
| 25 | 0.0095 | 0.0156 | 0.0433 | 0.0821 | 0.1063 | 0.1145 | 0.1165 |
| 50 | 0.0066 | 0.0202 | 0.0481 | 0.0752 | 0.0876 | 0.0913 | 0.0922 |
| 100 | 0.0086 | 0.0238 | 0.0468 | 0.0621 | 0.0676 | 0.0691 | 0.0694 |
| 200 | 0.0106 | 0.0256 | 0.0410 | 0.0483 | 0.0505 | 0.0511 | 0.0512 |
| 400 | 0.0124 | 0.0247 | 0.0331 | 0.0362 | 0.0370 | 0.0373 | 0.0373 |
| 1000 | 0.0132 | 0.0200 | 0.0230 | 0.0239 | 0.0241 | 0.0242 | 0.0242 |

### A. weak arm: pi(all-R) (rows N, columns I)

| N \ I | 1 | 4 | 16 | 64 | 256 | 1024 | 4096 |
|---|---|---|---|---|---|---|---|
| 5 | 0.0007 | 0.0016 | 0.0102 | 0.0355 | 0.0694 | 0.0906 | 0.0966 |
| 10 | 0.0010 | 0.0053 | 0.0255 | 0.0640 | 0.1027 | 0.1205 | 0.1253 |
| 16 | 0.0015 | 0.0100 | 0.0350 | 0.0769 | 0.1096 | 0.1223 | 0.1254 |
| 25 | 0.0025 | 0.0142 | 0.0420 | 0.0809 | 0.1051 | 0.1133 | 0.1153 |
| 50 | 0.0051 | 0.0192 | 0.0472 | 0.0743 | 0.0868 | 0.0904 | 0.0913 |
| 100 | 0.0077 | 0.0231 | 0.0462 | 0.0615 | 0.0670 | 0.0684 | 0.0688 |
| 200 | 0.0100 | 0.0252 | 0.0405 | 0.0478 | 0.0501 | 0.0506 | 0.0508 |
| 400 | 0.0120 | 0.0243 | 0.0328 | 0.0359 | 0.0367 | 0.0369 | 0.0370 |
| 1000 | 0.0130 | 0.0198 | 0.0228 | 0.0237 | 0.0239 | 0.0240 | 0.0240 |

### A. modal arm: P(C,C) (rows N, columns I)

| N \ I | 1 | 4 | 16 | 64 | 256 | 1024 | 4096 |
|---|---|---|---|---|---|---|---|
| 5 | 0.1739 | 0.0776 | 0.2409 | 0.5280 | 0.7937 | 0.9333 | 0.9818 |
| 10 | 0.0916 | 0.1638 | 0.4144 | 0.7103 | 0.8954 | 0.9698 | 0.9921 |
| 16 | 0.0821 | 0.2252 | 0.5074 | 0.7799 | 0.9265 | 0.9796 | 0.9948 |
| 25 | 0.0979 | 0.2768 | 0.5739 | 0.8225 | 0.9440 | 0.9849 | 0.9961 |
| 50 | 0.1312 | 0.3480 | 0.6489 | 0.8661 | 0.9605 | 0.9896 | 0.9974 |
| 100 | 0.1693 | 0.4177 | 0.7115 | 0.8993 | 0.9718 | 0.9927 | 0.9982 |
| 200 | 0.2155 | 0.4874 | 0.7687 | 0.9257 | 0.9799 | 0.9949 | 0.9987 |
| 400 | 0.2681 | 0.5572 | 0.8198 | 0.9460 | 0.9858 | 0.9964 | 0.9991 |
| 1000 | 0.3452 | 0.6502 | 0.8756 | 0.9651 | 0.9910 | 0.9977 | 0.9994 |

### A. weak arm: exits from all-R (shares) and sinks

| N | I | M | faker | weak | shadow | other | formula f/(f+0.2493/M) | pi(faker states) | pi(weak-faker states) | R share of coop entry | support (top 5) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 1 | 5 | 0.003 | 0.0000 | 0.289 | 0.7075 | 0.011 | 1.5e-03 | 0.0000 | 0.007 | `D` 0.5004; `X` 0.1883; `ROLE` 0.1547; `C` 0.0841; `not(ROLE)` 0.0393 |
| 5 | 16 | 80 | 0.089 | 0.0008 | 0.753 | 0.1574 | 0.106 | 2.7e-03 | 0.0001 | 0.991 | `D` 0.9811; `THEM(^C)` 0.0102; `THEM(^X)` 0.0012; `THEM(^ROLE)` 0.0011; `X` 0.0010 |
| 5 | 64 | 320 | 0.319 | 0.0027 | 0.675 | 0.0030 | 0.321 | 3.9e-03 | 0.0002 | 0.991 | `D` 0.9553; `THEM(^C)` 0.0355; `THEM(^X)` 0.0017; `THEM(^ROLE)` 0.0017; `X` 0.0006 |
| 5 | 256 | 1280 | 0.647 | 0.0055 | 0.343 | 0.0051 | 0.654 | 4.7e-03 | 0.0007 | 0.991 | `D` 0.9198; `THEM(^C)` 0.0694; `THEM(^X)` 0.0021; `THEM(^ROLE)` 0.0020; `and(X,THEM(^X))` 0.0008 |
| 5 | 4096 | 20480 | 0.953 | 0.0080 | 0.032 | 0.0075 | 0.968 | 5.1e-03 | 0.0095 | 0.991 | `D` 0.8695; `THEM(^C)` 0.0966; `and(X,THEM(^D))` 0.0094; `and(X,THEM(ME))` 0.0081; `and(THEM(ME),X)` 0.0072 |
| 10 | 1 | 10 | 0.006 | 0.0001 | 0.364 | 0.6306 | 0.015 | 1.5e-03 | 0.0000 | 0.023 | `D` 0.6926; `X` 0.1245; `ROLE` 0.1023; `C` 0.0270; `not(ROLE)` 0.0260 |
| 10 | 16 | 160 | 0.175 | 0.0012 | 0.820 | 0.0033 | 0.176 | 3.1e-03 | 0.0001 | 0.991 | `D` 0.9656; `THEM(^C)` 0.0255; `THEM(^X)` 0.0014; `THEM(^ROLE)` 0.0013; `X` 0.0009 |
| 10 | 64 | 640 | 0.459 | 0.0031 | 0.537 | 0.0003 | 0.461 | 3.8e-03 | 0.0003 | 0.991 | `D` 0.9262; `THEM(^C)` 0.0640; `THEM(^X)` 0.0017; `THEM(^ROLE)` 0.0016; `and(X,THEM(^X))` 0.0009 |
| 10 | 256 | 2560 | 0.769 | 0.0052 | 0.225 | 0.0004 | 0.774 | 4.2e-03 | 0.0012 | 0.991 | `D` 0.8866; `THEM(^C)` 0.1027; `THEM(^X)` 0.0019; `THEM(^ROLE)` 0.0018; `and(X,THEM(^D))` 0.0012 |
| 10 | 4096 | 40960 | 0.975 | 0.0066 | 0.018 | 0.0005 | 0.982 | 4.4e-03 | 0.0114 | 0.991 | `D` 0.8533; `THEM(^C)` 0.1253; `and(X,THEM(^D))` 0.0114; `THEM(^X)` 0.0019; `THEM(^ROLE)` 0.0018 |
| 16 | 1 | 16 | 0.010 | 0.0001 | 0.461 | 0.5293 | 0.021 | 1.5e-03 | 0.0000 | 0.103 | `D` 0.8439; `X` 0.0632; `ROLE` 0.0519; `not(ROLE)` 0.0132; `C` 0.0064 |
| 16 | 16 | 256 | 0.245 | 0.0015 | 0.753 | 0.0003 | 0.246 | 2.9e-03 | 0.0001 | 0.991 | `D` 0.9559; `THEM(^C)` 0.0350; `THEM(^X)` 0.0013; `THEM(^ROLE)` 0.0013; `X` 0.0008 |
| 16 | 64 | 1024 | 0.564 | 0.0033 | 0.433 | 0.0000 | 0.566 | 3.4e-03 | 0.0004 | 0.991 | `D` 0.9138; `THEM(^C)` 0.0769; `THEM(^X)` 0.0015; `THEM(^ROLE)` 0.0014; `and(X,THEM(^X))` 0.0009 |
| 16 | 256 | 4096 | 0.835 | 0.0050 | 0.160 | 0.0000 | 0.839 | 3.7e-03 | 0.0016 | 0.991 | `D` 0.8800; `THEM(^C)` 0.1096; `THEM(^X)` 0.0016; `and(X,THEM(^D))` 0.0016; `THEM(^ROLE)` 0.0015 |
| 16 | 4096 | 65536 | 0.982 | 0.0058 | 0.012 | 0.0000 | 0.988 | 3.8e-03 | 0.0098 | 0.991 | `D` 0.8559; `THEM(^C)` 0.1254; `and(X,THEM(^D))` 0.0097; `THEM(^X)` 0.0016; `THEM(^ROLE)` 0.0016 |
| 25 | 1 | 25 | 0.019 | 0.0001 | 0.603 | 0.3786 | 0.030 | 1.5e-03 | 0.0000 | 0.558 | `D` 0.9429; `X` 0.0200; `ROLE` 0.0164; `not(ROLE)` 0.0042; `and(X,ROLE)` 0.0037 |
| 25 | 16 | 400 | 0.329 | 0.0017 | 0.669 | 0.0000 | 0.330 | 2.5e-03 | 0.0001 | 0.990 | `D` 0.9495; `THEM(^C)` 0.0420; `THEM(^X)` 0.0011; `THEM(^ROLE)` 0.0011; `and(X,THEM(^X))` 0.0009 |
| 25 | 64 | 1600 | 0.661 | 0.0034 | 0.336 | 0.0000 | 0.663 | 2.8e-03 | 0.0005 | 0.990 | `D` 0.9105; `THEM(^C)` 0.0809; `THEM(^X)` 0.0013; `THEM(^ROLE)` 0.0012; `and(X,THEM(^X))` 0.0008 |
| 25 | 256 | 6400 | 0.883 | 0.0045 | 0.112 | 0.0000 | 0.887 | 3.0e-03 | 0.0018 | 0.990 | `D` 0.8851; `THEM(^C)` 0.1051; `and(X,THEM(^D))` 0.0018; `THEM(^X)` 0.0013; `THEM(^ROLE)` 0.0013 |
| 25 | 4096 | 102400 | 0.987 | 0.0051 | 0.008 | 0.0000 | 0.992 | 3.1e-03 | 0.0078 | 0.990 | `D` 0.8689; `THEM(^C)` 0.1153; `and(X,THEM(^D))` 0.0078; `THEM(^X)` 0.0013; `THEM(^ROLE)` 0.0013 |
| 50 | 1 | 50 | 0.050 | 0.0002 | 0.843 | 0.1069 | 0.056 | 1.3e-03 | 0.0000 | 0.982 | `D` 0.9851; `THEM(^C)` 0.0051; `X` 0.0019; `ROLE` 0.0016; `C` 0.0008 |
| 50 | 16 | 800 | 0.486 | 0.0019 | 0.512 | 0.0000 | 0.487 | 1.8e-03 | 0.0001 | 0.990 | `D` 0.9460; `THEM(^C)` 0.0472; `and(X,THEM(^X))` 0.0008; `and(X,THEM(^ROLE))` 0.0008; `THEM(^X)` 0.0008 |
| 50 | 64 | 3200 | 0.789 | 0.0030 | 0.208 | 0.0000 | 0.792 | 1.9e-03 | 0.0006 | 0.990 | `D` 0.9186; `THEM(^C)` 0.0743; `THEM(^X)` 0.0008; `THEM(^ROLE)` 0.0008; `and(X,THEM(^X))` 0.0008 |
| 50 | 256 | 12800 | 0.935 | 0.0036 | 0.062 | 0.0000 | 0.938 | 2.0e-03 | 0.0018 | 0.990 | `D` 0.9051; `THEM(^C)` 0.0868; `and(X,THEM(^D))` 0.0018; `THEM(^X)` 0.0009; `THEM(^ROLE)` 0.0008 |
| 50 | 4096 | 204800 | 0.992 | 0.0038 | 0.004 | 0.0000 | 0.996 | 2.0e-03 | 0.0049 | 0.990 | `D` 0.8974; `THEM(^C)` 0.0913; `and(X,THEM(^D))` 0.0049; `THEM(^X)` 0.0009; `THEM(^ROLE)` 0.0008 |
| 100 | 1 | 100 | 0.104 | 0.0003 | 0.890 | 0.0063 | 0.104 | 9.2e-04 | 0.0001 | 0.990 | `D` 0.9866; `THEM(^C)` 0.0077; `X` 0.0008; `ROLE` 0.0007; `C` 0.0005 |
| 100 | 16 | 1600 | 0.650 | 0.0018 | 0.349 | 0.0000 | 0.651 | 1.2e-03 | 0.0002 | 0.990 | `D` 0.9486; `THEM(^C)` 0.0462; `and(X,THEM(^X))` 0.0007; `and(X,THEM(^ROLE))` 0.0006; `THEM(^X)` 0.0005 |
| 100 | 64 | 6400 | 0.880 | 0.0024 | 0.118 | 0.0000 | 0.882 | 1.3e-03 | 0.0006 | 0.990 | `D` 0.9330; `THEM(^C)` 0.0615; `and(X,THEM(^X))` 0.0006; `and(X,THEM(^ROLE))` 0.0006; `and(X,THEM(^D))` 0.0006 |
| 100 | 256 | 25600 | 0.965 | 0.0026 | 0.032 | 0.0000 | 0.968 | 1.3e-03 | 0.0015 | 0.990 | `D` 0.9266; `THEM(^C)` 0.0670; `and(X,THEM(^D))` 0.0015; `and(X,THEM(^X))` 0.0006; `and(X,THEM(^ROLE))` 0.0006 |
| 100 | 4096 | 409600 | 0.995 | 0.0027 | 0.002 | 0.0000 | 0.998 | 1.3e-03 | 0.0029 | 0.990 | `D` 0.9234; `THEM(^C)` 0.0688; `and(X,THEM(^D))` 0.0029; `and(X,THEM(^X))` 0.0006; `and(X,THEM(^ROLE))` 0.0006 |
| 200 | 1 | 200 | 0.187 | 0.0004 | 0.812 | 0.0002 | 0.187 | 6.8e-04 | 0.0001 | 0.990 | `D` 0.9853; `THEM(^C)` 0.0100; `X` 0.0005; `ROLE` 0.0004; `and(X,THEM(^X))` 0.0004 |
| 200 | 16 | 3200 | 0.786 | 0.0015 | 0.213 | 0.0000 | 0.787 | 8.4e-04 | 0.0002 | 0.990 | `D` 0.9554; `THEM(^C)` 0.0405; `and(X,THEM(^X))` 0.0005; `and(X,THEM(^ROLE))` 0.0005; `THEM(^X)` 0.0004 |
| 200 | 64 | 12800 | 0.935 | 0.0018 | 0.063 | 0.0000 | 0.937 | 8.8e-04 | 0.0005 | 0.990 | `D` 0.9478; `THEM(^C)` 0.0478; `and(X,THEM(^D))` 0.0005; `and(X,THEM(^X))` 0.0005; `and(X,THEM(^ROLE))` 0.0005 |
| 200 | 256 | 51200 | 0.981 | 0.0019 | 0.017 | 0.0000 | 0.983 | 8.9e-04 | 0.0011 | 0.990 | `D` 0.9450; `THEM(^C)` 0.0501; `and(X,THEM(^D))` 0.0011; `and(X,THEM(^X))` 0.0005; `and(X,THEM(^ROLE))` 0.0005 |
| 200 | 4096 | 819200 | 0.997 | 0.0019 | 0.001 | 0.0000 | 0.999 | 8.9e-04 | 0.0017 | 0.990 | `D` 0.9437; `THEM(^C)` 0.0508; `and(X,THEM(^D))` 0.0017; `and(X,THEM(^X))` 0.0005; `and(X,THEM(^ROLE))` 0.0005 |
| 400 | 1 | 400 | 0.314 | 0.0004 | 0.685 | 0.0000 | 0.315 | 5.1e-04 | 0.0001 | 0.990 | `D` 0.9844; `THEM(^C)` 0.0120; `and(X,THEM(^X))` 0.0004; `and(X,THEM(^ROLE))` 0.0004; `X` 0.0003 |
| 400 | 16 | 6400 | 0.879 | 0.0012 | 0.120 | 0.0000 | 0.880 | 6.1e-04 | 0.0002 | 0.990 | `D` 0.9640; `THEM(^C)` 0.0328; `and(X,THEM(^X))` 0.0004; `and(X,THEM(^ROLE))` 0.0003; `THEM(^X)` 0.0003 |
| 400 | 64 | 25600 | 0.966 | 0.0013 | 0.033 | 0.0000 | 0.967 | 6.3e-04 | 0.0005 | 0.990 | `D` 0.9607; `THEM(^C)` 0.0359; `and(X,THEM(^D))` 0.0005; `and(X,THEM(^X))` 0.0004; `and(X,THEM(^ROLE))` 0.0003 |
| 400 | 256 | 102400 | 0.990 | 0.0013 | 0.008 | 0.0000 | 0.992 | 6.3e-04 | 0.0008 | 0.990 | `D` 0.9595; `THEM(^C)` 0.0367; `and(X,THEM(^D))` 0.0008; `and(X,THEM(^X))` 0.0004; `and(X,THEM(^ROLE))` 0.0003 |
| 400 | 4096 | 1638400 | 0.998 | 0.0013 | 0.001 | 0.0000 | 0.999 | 6.3e-04 | 0.0010 | 0.990 | `D` 0.9590; `THEM(^C)` 0.0370; `and(X,THEM(^D))` 0.0010; `and(X,THEM(^X))` 0.0004; `and(X,THEM(^ROLE))` 0.0003 |
| 1000 | 1 | 1000 | 0.533 | 0.0004 | 0.466 | 0.0000 | 0.534 | 3.5e-04 | 0.0001 | 0.990 | `D` 0.9845; `THEM(^C)` 0.0130; `and(X,THEM(^X))` 0.0002; `and(X,THEM(^ROLE))` 0.0002; `and(THEM(THEM),D)` 0.0002 |
| 1000 | 16 | 16000 | 0.947 | 0.0008 | 0.052 | 0.0000 | 0.948 | 4.0e-04 | 0.0002 | 0.990 | `D` 0.9748; `THEM(^C)` 0.0228; `and(X,THEM(^X))` 0.0002; `and(X,THEM(^ROLE))` 0.0002; `and(THEM(THEM),D)` 0.0002 |
| 1000 | 64 | 64000 | 0.986 | 0.0008 | 0.013 | 0.0000 | 0.987 | 4.0e-04 | 0.0003 | 0.990 | `D` 0.9738; `THEM(^C)` 0.0237; `and(X,THEM(^D))` 0.0003; `and(X,THEM(^X))` 0.0002; `and(X,THEM(^ROLE))` 0.0002 |
| 1000 | 256 | 256000 | 0.996 | 0.0008 | 0.003 | 0.0000 | 0.997 | 4.0e-04 | 0.0004 | 0.990 | `D` 0.9734; `THEM(^C)` 0.0239; `and(X,THEM(^D))` 0.0004; `and(X,THEM(^X))` 0.0002; `and(X,THEM(^ROLE))` 0.0002 |
| 1000 | 4096 | 4096000 | 0.999 | 0.0008 | 0.000 | 0.0000 | 1.000 | 4.0e-04 | 0.0005 | 0.990 | `D` 0.9733; `THEM(^C)` 0.0240; `and(X,THEM(^D))` 0.0005; `and(X,THEM(^X))` 0.0002; `and(X,THEM(^ROLE))` 0.0002 |

### A. modal arm: cooperative block

pi of unfakeable / fakeable / unconditional cooperators; pi-weighted exits from conditional cooperators (unfakeable + fakeable) to classes outside them.

| N | I | P(C,C) | odds | pi unfakeable | pi fakeable | fakeable/unfakeable | pi unconditional | exits: strict faker / weak / neutral shadow / other | well-mixed P(C,C) at M = IN |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 1 | 0.1312 | 0.151 | 0.0814 | 0.0401 | 0.4924 | 0.0097 | 0.03 / 0.00 / 0.97 / 0.00 | 0.1312 |
| 50 | 4 | 0.3480 | 0.534 | 0.2435 | 0.0978 | 0.4017 | 0.0067 | 0.09 / 0.00 / 0.91 / 0.00 | 0.2155 |
| 50 | 16 | 0.6489 | 1.848 | 0.5224 | 0.1229 | 0.2353 | 0.0035 | 0.20 / 0.00 / 0.80 / 0.00 | 0.3256 |
| 50 | 64 | 0.8661 | 6.469 | 0.7942 | 0.0706 | 0.0889 | 0.0013 | 0.30 / 0.00 / 0.70 / 0.00 | 0.4592 |
| 50 | 256 | 0.9605 | 24.309 | 0.9362 | 0.0239 | 0.0255 | 0.0004 | 0.34 / 0.00 / 0.66 / 0.00 | 0.6149 |
| 50 | 1024 | 0.9896 | 95.379 | 0.9830 | 0.0065 | 0.0066 | 0.0001 | 0.35 / 0.00 / 0.65 / 0.00 | nan |
| 100 | 1 | 0.1693 | 0.204 | 0.1115 | 0.0512 | 0.4587 | 0.0066 | 0.05 / 0.00 / 0.95 / 0.00 | 0.1693 |
| 100 | 4 | 0.4177 | 0.717 | 0.3112 | 0.1022 | 0.3282 | 0.0043 | 0.14 / 0.00 / 0.86 / 0.00 | 0.2681 |
| 100 | 16 | 0.7115 | 2.467 | 0.6142 | 0.0952 | 0.1550 | 0.0021 | 0.25 / 0.00 / 0.75 / 0.00 | 0.3888 |
| 100 | 64 | 0.8993 | 8.929 | 0.8559 | 0.0427 | 0.0499 | 0.0007 | 0.32 / 0.00 / 0.68 / 0.00 | 0.5360 |
| 100 | 256 | 0.9718 | 34.426 | 0.9587 | 0.0129 | 0.0134 | 0.0002 | 0.35 / 0.00 / 0.65 / 0.00 | 0.6905 |
| 100 | 1024 | 0.9927 | 136.292 | 0.9893 | 0.0034 | 0.0034 | 0.0001 | 0.35 / 0.00 / 0.65 / 0.00 | nan |
| 1000 | 1 | 0.3452 | 0.527 | 0.2831 | 0.0606 | 0.2140 | 0.0016 | 0.21 / 0.00 / 0.79 / 0.00 | 0.3452 |
| 1000 | 4 | 0.6502 | 1.859 | 0.6028 | 0.0466 | 0.0773 | 0.0008 | 0.30 / 0.00 / 0.70 / 0.00 | 0.4834 |
| 1000 | 16 | 0.8756 | 7.035 | 0.8566 | 0.0186 | 0.0218 | 0.0003 | 0.34 / 0.00 / 0.66 / 0.00 | 0.6399 |
| 1000 | 64 | 0.9651 | 27.680 | 0.9597 | 0.0054 | 0.0056 | 0.0001 | 0.35 / 0.00 / 0.65 / 0.00 | nan |
| 1000 | 256 | 0.9910 | 110.238 | 0.9896 | 0.0014 | 0.0014 | 0.0000 | 0.36 / 0.00 / 0.64 / 0.00 | nan |
| 1000 | 1024 | 0.9977 | 440.466 | 0.9974 | 0.0004 | 0.0004 | 0.0000 | 0.36 / 0.00 / 0.64 / 0.00 | nan |

### B. Monte Carlo global fixation at fixed mN

Phi_MC = successes / decided trials, 95% Wilson interval; [lo_u, hi_u] counts undecided trials as failures / successes. rho_N = within-island Moran fixation; Phi_2 = two-level value.

| edge | graph | I | N | mN | Phi_MC [95%] | Phi_MC / rho_N [95%] | Phi_2 | succ / fail / undec | stop | [lo_u, hi_u] | gens per success |
|---|---|---|---|---|---|---|---|---|---|---|---|
| entry R|D | complete | 16 | 25 | 0.01 | 0.0760 [0.0652, 0.0884] | 0.923 [0.792, 1.074] | 0.0797 | 152 / 1848 / 0 | successes | [0.0652, 0.0884] | 7788 |
| entry R|D | complete | 16 | 25 | 0.1 | 0.0760 [0.0652, 0.0884] | 0.923 [0.792, 1.074] | 0.0797 | 152 / 1848 / 0 | successes | [0.0652, 0.0884] | 820 |
| entry R|D | complete | 64 | 25 | 0.1 | 0.0785 [0.0675, 0.0911] | 0.953 [0.820, 1.107] | 0.0797 | 157 / 1843 / 0 | successes | [0.0675, 0.0911] | 1243 |
| entry R|D | complete | 16 | 25 | 1 | 0.0520 [0.0446, 0.0605] | 0.632 [0.542, 0.735] | 0.0797 | 156 / 2844 / 0 | successes | [0.0446, 0.0605] | 134 |
| entry R|D | complete | 64 | 25 | 1 | 0.0650 [0.0558, 0.0756] | 0.789 [0.678, 0.918] | 0.0797 | 156 / 2244 / 0 | successes | [0.0558, 0.0756] | 190 |
| entry R|D | complete | 16 | 25 | 3 | 0.0482 [0.0415, 0.0560] | 0.586 [0.504, 0.680] | 0.0797 | 164 / 3236 / 0 | successes | [0.0415, 0.0560] | 91 |
| entry R|D | complete | 4 | 100 | 0.1 | 0.0364 [0.0312, 0.0423] | 0.865 [0.742, 1.006] | 0.0421 | 160 / 4240 / 0 | successes | [0.0312, 0.0423] | 664 |
| entry R|D | complete | 16 | 100 | 0.1 | 0.0413 [0.0354, 0.0481] | 0.982 [0.843, 1.144] | 0.0421 | 157 / 3643 / 0 | successes | [0.0354, 0.0481] | 1544 |
| entry R|D | complete | 64 | 100 | 0.1 | 0.0431 [0.0369, 0.0502] | 1.024 [0.877, 1.193] | 0.0421 | 155 / 3445 / 0 | successes | [0.0369, 0.0502] | 2266 |
| entry R|D | complete | 256 | 100 | 0.1 | 0.0436 [0.0374, 0.0508] | 1.037 [0.890, 1.207] | 0.0421 | 157 / 3443 / 0 | successes | [0.0374, 0.0508] | 3034 |
| entry R|D | hypercube | 4 | 100 | 0.1 | 0.0364 [0.0312, 0.0425] | 0.866 [0.741, 1.011] | 0.0421 | 153 / 4047 / 0 | successes | [0.0312, 0.0425] | 788 |
| entry R|D | hypercube | 16 | 100 | 0.1 | 0.0500 [0.0428, 0.0584] | 1.189 [1.017, 1.388] | 0.0421 | 150 / 2850 / 0 | successes | [0.0428, 0.0584] | 1943 |
| entry R|D | hypercube | 64 | 100 | 0.1 | 0.0395 [0.0339, 0.0460] | 0.939 [0.806, 1.094] | 0.0421 | 158 / 3842 / 0 | successes | [0.0339, 0.0460] | 2782 |
| entry R|D | hypercube | 256 | 100 | 0.1 | 0.0439 [0.0377, 0.0511] | 1.044 [0.896, 1.215] | 0.0421 | 158 / 3442 / 0 | successes | [0.0377, 0.0511] | 3625 |
| entry R|D | complete | 4 | 100 | 1 | 0.0444 [0.0380, 0.0519] | 1.056 [0.903, 1.233] | 0.0421 | 151 / 3249 / 0 | successes | [0.0380, 0.0519] | 129 |
| entry R|D | complete | 16 | 100 | 1 | 0.0375 [0.0320, 0.0438] | 0.892 [0.762, 1.042] | 0.0421 | 150 / 3850 / 0 | successes | [0.0320, 0.0438] | 241 |
| entry R|D | complete | 64 | 100 | 1 | 0.0422 [0.0361, 0.0493] | 1.004 [0.859, 1.172] | 0.0421 | 152 / 3448 / 0 | successes | [0.0361, 0.0493] | 334 |
| entry R|D | complete | 256 | 100 | 1 | 0.0390 [0.0334, 0.0455] | 0.927 [0.795, 1.081] | 0.0421 | 156 / 3844 / 0 | successes | [0.0334, 0.0455] | 422 |
| entry R|D | hypercube | 4 | 100 | 1 | 0.0395 [0.0339, 0.0460] | 0.939 [0.806, 1.094] | 0.0421 | 158 / 3842 / 0 | successes | [0.0339, 0.0460] | 133 |
| entry R|D | hypercube | 16 | 100 | 1 | 0.0360 [0.0307, 0.0420] | 0.855 [0.731, 0.999] | 0.0421 | 151 / 4049 / 0 | successes | [0.0307, 0.0420] | 268 |
| entry R|D | hypercube | 64 | 100 | 1 | 0.0397 [0.0340, 0.0464] | 0.945 [0.808, 1.104] | 0.0421 | 151 / 3649 / 0 | successes | [0.0340, 0.0464] | 390 |
| entry R|D | hypercube | 256 | 100 | 1 | 0.0403 [0.0345, 0.0470] | 0.957 [0.819, 1.117] | 0.0421 | 153 / 3647 / 0 | successes | [0.0345, 0.0470] | 499 |
| entry R|D | torus | 64 | 100 | 1 | 0.0456 [0.0391, 0.0531] | 1.084 [0.929, 1.263] | 0.0421 | 155 / 3245 / 0 | successes | [0.0391, 0.0531] | 489 |
| entry R|D | complete | 64 | 100 | 3 | 0.0330 [0.0283, 0.0386] | 0.786 [0.672, 0.918] | 0.0421 | 152 / 4448 / 0 | successes | [0.0283, 0.0386] | 187 |
| entry R|D | complete | 64 | 100 | 10 | 0.0209 [0.0179, 0.0245] | 0.498 [0.426, 0.582] | 0.0421 | 155 / 7245 / 0 | successes | [0.0179, 0.0245] | 180 |
| entry R|D | complete | 64 | 400 | 0.1 | 0.0227 [0.0194, 0.0266] | 1.062 [0.906, 1.243] | 0.0214 | 150 / 6450 / 0 | successes | [0.0194, 0.0266] | 4609 |
| entry R|D | complete | 64 | 400 | 1 | 0.0204 [0.0174, 0.0239] | 0.953 [0.814, 1.116] | 0.0214 | 151 / 7249 / 0 | successes | [0.0174, 0.0239] | 636 |
| faker THEM(^D)|R | complete | 64 | 25 | 1 | 0.2737 [0.2525, 0.2961] | 0.986 [0.910, 1.067] | 0.2774 | 438 / 1162 / 0 | successes | [0.2525, 0.2961] | 77 |
| faker THEM(^D)|R | complete | 64 | 100 | 0.1 | 0.2687 [0.2476, 0.2910] | 1.019 [0.939, 1.104] | 0.2637 | 430 / 1170 / 0 | successes | [0.2476, 0.2910] | 427 |
| faker THEM(^D)|R | hypercube | 64 | 100 | 0.1 | 0.2871 [0.2641, 0.3114] | 1.089 [1.001, 1.181] | 0.2637 | 402 / 998 / 0 | successes | [0.2641, 0.3114] | 516 |
| faker THEM(^D)|R | complete | 64 | 100 | 1 | 0.2725 [0.2512, 0.2948] | 1.034 [0.953, 1.118] | 0.2637 | 436 / 1164 / 0 | successes | [0.2512, 0.2948] | 98 |
| faker THEM(^D)|R | hypercube | 64 | 100 | 1 | 0.2550 [0.2342, 0.2769] | 0.967 [0.888, 1.050] | 0.2637 | 408 / 1192 / 0 | successes | [0.2342, 0.2769] | 116 |
| faker THEM(^D)|R | torus | 64 | 100 | 1 | 0.2731 [0.2519, 0.2955] | 1.036 [0.955, 1.121] | 0.2637 | 437 / 1163 / 0 | successes | [0.2519, 0.2955] | 144 |
| faker THEM(^D)|R | complete | 64 | 100 | 10 | 0.2650 [0.2440, 0.2872] | 1.005 [0.925, 1.089] | 0.2637 | 424 / 1176 / 0 | successes | [0.2440, 0.2872] | 58 |
| faker THEM(^X)|R | complete | 64 | 25 | 1 | 0.1538 [0.1405, 0.1682] | 1.008 [0.921, 1.102] | 0.1495 | 400 / 2200 / 0 | successes | [0.1405, 0.1682] | 138 |
| faker THEM(^X)|R | complete | 64 | 100 | 0.1 | 0.1380 [0.1261, 0.1508] | 0.973 [0.889, 1.063] | 0.1419 | 414 / 2586 / 0 | successes | [0.1261, 0.1508] | 785 |
| faker THEM(^X)|R | complete | 64 | 100 | 1 | 0.1439 [0.1314, 0.1574] | 1.014 [0.926, 1.109] | 0.1419 | 403 / 2397 / 0 | successes | [0.1314, 0.1574] | 178 |
| faker THEM(^X)|R | complete | 64 | 100 | 10 | 0.1565 [0.1431, 0.1710] | 1.103 [1.008, 1.205] | 0.1419 | 407 / 2193 / 0 | successes | [0.1431, 0.1710] | 106 |
| shadow C|R | complete | 16 | 25 | 1 | 0.0031 [0.0023, 0.0042] | 0.077 [0.057, 0.105] | 0.0025 | 40 / 12960 / 0 | successes | [0.0023, 0.0042] | 723 |
| shadow C|R | hypercube | 16 | 25 | 1 | 0.0025 [0.0019, 0.0034] | 0.063 [0.046, 0.086] | 0.0025 | 40 / 15760 / 0 | successes | [0.0019, 0.0034] | 755 |

### B. Patched chain (exploratory): two-level chain with the measured 2x2 games replaced by Phi_MC

| graph | I | N | mN | measured | P(C,C) patched | pi_R patched | pi_R two-level | ratio | faker share |
|---|---|---|---|---|---|---|---|---|---|
| complete | 4 | 100 | 0.1 | entry R|D | 0.0208 | 0.0201 | 0.0231 | 0.87 | 0.317 |
| complete | 4 | 100 | 1 | entry R|D | 0.0251 | 0.0244 | 0.0231 | 1.05 | 0.317 |
| complete | 16 | 25 | 0.01 | entry R|D | 0.0414 | 0.0402 | 0.0420 | 0.96 | 0.329 |
| complete | 16 | 25 | 0.1 | entry R|D | 0.0414 | 0.0402 | 0.0420 | 0.96 | 0.329 |
| complete | 16 | 25 | 1 | entry R|D | 0.0290 | 0.0279 | 0.0420 | 0.66 | 0.329 |
| complete | 16 | 25 | 3 | entry R|D | 0.0270 | 0.0259 | 0.0420 | 0.62 | 0.329 |
| complete | 16 | 100 | 0.1 | entry R|D | 0.0460 | 0.0454 | 0.0462 | 0.98 | 0.650 |
| complete | 16 | 100 | 1 | entry R|D | 0.0420 | 0.0414 | 0.0462 | 0.90 | 0.650 |
| complete | 64 | 25 | 0.1 | entry R|D | 0.0809 | 0.0798 | 0.0809 | 0.99 | 0.661 |
| complete | 64 | 25 | 1 | entry R|D, faker THEM(^D)|R, faker THEM(^X)|R | 0.0678 | 0.0667 | 0.0809 | 0.82 | 0.662 |
| complete | 64 | 100 | 0.1 | entry R|D, faker THEM(^D)|R, faker THEM(^X)|R | 0.0637 | 0.0630 | 0.0615 | 1.03 | 0.879 |
| complete | 64 | 100 | 1 | entry R|D, faker THEM(^D)|R, faker THEM(^X)|R | 0.0612 | 0.0605 | 0.0615 | 0.99 | 0.882 |
| complete | 64 | 100 | 3 | entry R|D | 0.0496 | 0.0490 | 0.0615 | 0.80 | 0.880 |
| complete | 64 | 100 | 10 | entry R|D, faker THEM(^D)|R, faker THEM(^X)|R | 0.0308 | 0.0303 | 0.0615 | 0.49 | 0.885 |
| complete | 64 | 400 | 0.1 | entry R|D | 0.0383 | 0.0380 | 0.0359 | 1.06 | 0.966 |
| complete | 64 | 400 | 1 | entry R|D | 0.0346 | 0.0342 | 0.0359 | 0.95 | 0.966 |
| complete | 256 | 100 | 0.1 | entry R|D | 0.0699 | 0.0692 | 0.0670 | 1.03 | 0.965 |
| complete | 256 | 100 | 1 | entry R|D | 0.0630 | 0.0624 | 0.0670 | 0.93 | 0.965 |
| hypercube | 4 | 100 | 0.1 | entry R|D | 0.0208 | 0.0201 | 0.0231 | 0.87 | 0.317 |
| hypercube | 4 | 100 | 1 | entry R|D | 0.0225 | 0.0218 | 0.0231 | 0.94 | 0.317 |
| hypercube | 16 | 100 | 0.1 | entry R|D | 0.0551 | 0.0544 | 0.0462 | 1.18 | 0.650 |
| hypercube | 16 | 100 | 1 | entry R|D | 0.0404 | 0.0397 | 0.0462 | 0.86 | 0.650 |
| hypercube | 64 | 100 | 0.1 | entry R|D, faker THEM(^D)|R | 0.0566 | 0.0560 | 0.0615 | 0.91 | 0.884 |
| hypercube | 64 | 100 | 1 | entry R|D, faker THEM(^D)|R | 0.0597 | 0.0590 | 0.0615 | 0.96 | 0.878 |
| hypercube | 256 | 100 | 0.1 | entry R|D | 0.0703 | 0.0696 | 0.0670 | 1.04 | 0.965 |
| hypercube | 256 | 100 | 1 | entry R|D | 0.0649 | 0.0643 | 0.0670 | 0.96 | 0.965 |
| torus | 64 | 100 | 1 | entry R|D, faker THEM(^D)|R | 0.0660 | 0.0654 | 0.0615 | 1.06 | 0.881 |

### C. Finite-eps agent-based approach runs (w_g = 0; 2e5 generations; second half; approach rates, not pi)

| arm | graph | I | N | mN | epsN | start | P(C,C) per rep (2nd half) | mean | 1st half | R-dominant island-time | P(C,C) by island dominant class: R / C / faker / other / none | exits from >=90%-R islands: faker / weak / shadow / other / none | dominance-flip exits from R: faker / weak / shadow / other | dominant classes (rep 0) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| weak | complete | 64 | 100 | 1 | 0.1 | allR | 0.130, 0.173, 0.129 | 0.144 | 0.153 | 0.029 | 0.028 / 0.036 / 0.049 / 0.015 / 0.017 | 332 / 0 / 54 / 1 / 41 | 1968 / 0 / 1354 / 88 | `D` 0.52, `THEM(^ROLE)` 0.21, `THEM(^and(X,ROLE))` 0.12, `C` 0.05 |
| weak | complete | 64 | 25 | 1 | 0.1 | alld | 0.140, 0.156, 0.140 | 0.145 | 0.159 | 0.027 | 0.026 / 0.024 / 0.068 / 0.014 / 0.014 | 243 / 0 / 581 / 258 / 240 | 1478 / 0 / 3128 / 1846 | `D` 0.50, `THEM(^ROLE)` 0.19, `THEM(^X)` 0.13, `THEM(^C)` 0.04 |
| weak | complete | 256 | 25 | 1 | 0.1 | alld | 0.066, 0.075, 0.088 | 0.076 | 0.066 | 0.018 | 0.016 / 0.011 / 0.033 / 0.008 / 0.009 | 2328 / 127 / 1123 / 1025 / 965 | 14130 / 479 / 5153 / 8299 | `D` 0.64, `THEM(^and(X,ROLE))` 0.12, `THEM(^X)` 0.07, `THEM(^D)` 0.03 |
| weak | complete | 16 | 100 | 1 | 0.1 | alld | 0.063, 0.192, 0.207 | 0.154 | 0.098 | 0.051 | 0.051 / 0.034 / 0.052 / 0.006 / 0.011 | 39 / 0 / 34 / 0 / 14 | 131 / 0 / 257 / 13 | `D` 0.92, `THEM(^C)` 0.05, `THEM(^X)` 0.01, `C` 0.00 |
| weak | complete | 64 | 100 | 1 | 0.1 | alld | 0.130, 0.173, 0.129 | 0.144 | 0.131 | 0.029 | 0.028 / 0.036 / 0.049 / 0.015 / 0.017 | 332 / 0 / 54 / 1 / 41 | 1834 / 0 / 1167 / 88 | `D` 0.52, `THEM(^ROLE)` 0.21, `THEM(^and(X,ROLE))` 0.12, `C` 0.05 |
| weak | complete | 256 | 100 | 1 | 0.1 | alld | 0.042, 0.050, 0.028 | 0.040 | 0.051 | 0.008 | 0.007 / 0.007 / 0.013 / 0.007 / 0.006 | 1531 / 0 / 43 / 10 / 228 | 6838 / 0 / 583 / 285 | `D` 0.82, `THEM(^D)` 0.07, `THEM(^and(X,ROLE))` 0.04, `THEM(^ROLE)` 0.02 |
| weak | hypercube | 64 | 100 | 1 | 0.1 | alld | 0.103, 0.116, 0.118 | 0.112 | 0.094 | 0.021 | 0.020 / 0.030 / 0.039 / 0.010 / 0.013 | 278 / 7 / 35 / 3 / 41 | 982 / 60 / 480 / 57 | `D` 0.40, `and(X,THEM(ME))` 0.28, `THEM(^not(ROLE))` 0.14, `THEM(^X)` 0.06 |
| weak | hypercube | 256 | 100 | 1 | 0.1 | alld | 0.023, 0.022, 0.029 | 0.024 | 0.035 | 0.000 | 0.000 / 0.005 / 0.009 / 0.003 / 0.007 | 46 / 0 / 0 / 0 / 12 | 2042 / 0 / 227 / 92 | `D` 0.77, `THEM(^and(X,ROLE))` 0.14, `THEM(^D)` 0.07, `C` 0.01 |
| weak | complete | 64 | 100 | 1 | 0.01 | allR | 0.107, 0.244, 0.199 | 0.183 | 0.141 | 0.083 | 0.082 / 0.049 / 0.040 / 0.003 / 0.008 | 120 / 0 / 49 / 0 / 7 | 472 / 0 / 535 / 3 | `D` 0.82, `THEM(^C)` 0.08, `THEM(^ROLE)` 0.07, `C` 0.02 |
| weak | complete | 64 | 100 | 0.1 | 0.01 | alld | 0.218, 0.105, 0.045 | 0.123 | 0.076 | 0.027 | 0.027 / 0.030 / 0.062 / 0.004 / 0.000 | 72 / 0 / 4 / 1 / 3 | 367 / 0 / 123 / 10 | `THEM(^X)` 0.46, `D` 0.43, `C` 0.06, `THEM(^C)` 0.04 |
| weak | complete | 16 | 100 | 1 | 0.01 | alld | 0.000, 0.285, 0.000 | 0.095 | 0.063 | 0.091 | 0.091 / 0.004 / 0.000 / 0.000 / 0.000 | 0 / 0 / 24 / 0 / 1 | 16 / 0 / 272 / 2 | `D` 1.00, `THEM(THEM)` 0.00 |
| weak | complete | 64 | 100 | 1 | 0.01 | alld | 0.107, 0.244, 0.199 | 0.183 | 0.090 | 0.083 | 0.082 / 0.049 / 0.040 / 0.003 / 0.008 | 120 / 0 / 49 / 0 / 7 | 297 / 0 / 364 / 3 | `D` 0.82, `THEM(^C)` 0.08, `THEM(^ROLE)` 0.07, `C` 0.02 |
| weak | complete | 256 | 100 | 1 | 0.01 | alld | 0.181, 0.177, 0.111 | 0.156 | 0.091 | 0.022 | 0.022 / 0.048 / 0.066 / 0.009 / 0.012 | 566 / 0 / 108 / 0 / 56 | 1715 / 0 / 834 / 15 | `D` 0.58, `THEM(^X)` 0.25, `C` 0.08, `THEM(^ROLE)` 0.05 |
| modal | complete | 16 | 100 | 1 | 0.1 | alld | 0.981, 0.981, 0.980 | 0.981 | 0.949 | 0.481 | 0.477 / 0.059 / 0.000 / 0.436 / 0.008 | 0 / 0 / 506 / 1 / 118 | 0 / 0 / 9143 / 138 | `BOX1(THEM(ME))` 0.52, `BOX(THEM(ME))` 0.40, `C` 0.06, `D` 0.01 |
| modal | complete | 64 | 100 | 1 | 0.1 | alld | 0.980, 0.978, 0.980 | 0.980 | 0.971 | 0.125 | 0.124 / 0.066 / 0.000 / 0.764 / 0.026 | 0 / 0 / 656 / 0 / 237 | 0 / 0 / 25836 / 173 | `BOX1(THEM(ME))` 0.64, `BOX(THEM(THEM))` 0.23, `C` 0.07, `BOX(THEM(ME))` 0.04 |
| modal | complete | 256 | 100 | 1 | 0.1 | alld | 0.980, 0.980, 0.981 | 0.980 | 0.971 | 0.417 | 0.414 / 0.066 / 0.000 / 0.447 / 0.053 | 0 / 0 / 10062 / 8 / 5278 | 0 / 0 / 201216 / 1023 | `BOX(THEM(THEM))` 0.69, `BOX1(THEM(ME))` 0.12, `C` 0.07, `BOX(THEM(ME))` 0.05 |
| modal | complete | 64 | 100 | 1 | 0.01 | allR | 0.998, 0.997, 0.998 | 0.998 | 0.998 | 0.950 | 0.950 / 0.043 / 0.000 / 0.004 / 0.002 | 0 / 0 / 1770 / 0 / 177 | 0 / 0 / 28254 / 56 | `BOX(THEM(ME))` 0.96, `C` 0.04, `D` 0.00, `BOX1(THEM(THEM))` 0.00 |
| modal | complete | 16 | 100 | 1 | 0.01 | alld | 0.998, 0.998, 0.998 | 0.998 | 0.826 | 0.000 | 0.000 / 0.033 / 0.000 / 0.964 / 0.001 | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 375 / 0 | `BOX1(THEM(ME))` 0.97, `C` 0.03, `D` 0.00, `BOX1(THEM(THEM))` 0.00 |
| modal | complete | 64 | 100 | 1 | 0.01 | alld | 0.999, 0.997, 0.998 | 0.998 | 0.949 | 0.005 | 0.005 / 0.044 / 0.000 / 0.947 / 0.002 | 0 / 0 / 76 / 0 / 13 | 0 / 0 / 1502 / 0 | `BOX1(THEM(ME))` 0.95, `C` 0.04, `BOX(THEM(ME))` 0.01, `D` 0.00 |
| modal | complete | 256 | 100 | 1 | 0.01 | alld | 0.997, 0.998, 0.998 | 0.998 | 0.988 | 0.317 | 0.316 / 0.050 / 0.000 / 0.628 / 0.003 | 0 / 0 / 3264 / 2 / 356 | 0 / 0 / 62844 / 117 | `BOX(THEM(ME))` 0.94, `C` 0.05, `BOX1(THEM(THEM))` 0.00, `not(BOX(THEM(THEM)))` 0.00 |
