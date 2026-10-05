# Divide-the-dollar partitions across islands, with `ROLE`, without `ROLE`, and with fixed roles

Spec `specs/2026-10-05-dollar-partitions.md`; predictions `predictions/2026-10-05-dollar-partitions.md`; code `src/dollar_partitions.py`. Weak arm, n = 5 in every arm, w = 0.3. Static tables: `runs/dollar_partitions/static_dollar5.md`, `static_dollar3.md`. Per-cell JSON under `runs/dollar_partitions/`.

**Deviations from the spec and predictions file.** (i) n = 5 in every arm (fallback): at n = 6 `dollar5` has 19,036 programs with `ROLE` and the value array would be 29 GB. (ii) Island labels use >= 0.95 of encounters (the predictions file says 0.99): one migrant lineage alone moves an island of 100 by about 2%. (iii) An escape is an island locally closed on one convention at one check and locally closed on a different one at a later check; label losses are counted at checks where every island is locally closed; both after the partition-frozen check. (iv) At m = 0 a run stops when every island-slot is monomorphic (nothing can change); "closed" in the tables refers to the global verified-closed rule, which m = 0 runs never need. (v) Not run: `dollar3` at (400, 16) and at mN = 1. Addenda beyond the spec: N = 3·10³ and 3·10⁴ chains, an N scan, and a joint simulation at N = 300.

## ε → 0 chains: dollar5

### dollar5, role (one population of N)

Encounter-level π-weighted outcome shares (per ordered split: slot 1 | slot 2 for fixed roles; the focal program first otherwise).

| N | 1/6\|5/6 | 1/3\|2/3 | 1/2\|1/2 | 2/3\|1/3 | 5/6\|1/6 | ineff | clash | P(efficient) | E[max share] | ex ante max | E[max norm. share \| compatible] | dwl | cut |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.0253 | 0.0047 | 0.9207 | 0.0047 | 0.0253 | 0.0106 | 0.0087 | 0.9807 | 0.513 | 0.494 | 0.519 | 0.0061 | 1.5e-06 |
| 1000 | 0.1512 | 0.0022 | 0.6928 | 0.0022 | 0.1512 | 0.0000 | 0.0005 | 0.9995 | 0.601 | 0.500 | 0.602 | 0.0003 | 4.3e-10 |
| 3000 | 0.0724 | 0.0236 | 0.7584 | 0.0236 | 0.0724 | 0.0066 | 0.0430 | 0.9504 | 0.532 | 0.476 | 0.559 | 0.0237 | 2.3e-09 |
| 10000 | 0.0486 | 0.0324 | 0.8062 | 0.0324 | 0.0486 | 0.0054 | 0.0263 | 0.9682 | 0.528 | 0.485 | 0.544 | 0.0150 | 6.1e-10 |
| 30000 | 0.1747 | 0.0194 | 0.0740 | 0.0194 | 0.1747 | 0.0083 | 0.5296 | 0.4620 | 0.356 | 0.233 | 0.761 | 0.2673 | 1.9e-11 |

Support (top states, π, label):

- N = 100: `S3:1.00` 0.9193 (1/2-1/2); `ROLE:1.00` 0.0393 (1/6-5/6); `S2:0.50 + S4:0.50` 0.0168 (mixed); `flip(ROLE):1.00` 0.0098 (1/6-5/6); `S2:1.00` 0.0032 (ineff); `X:1.00` 0.0025 (mixed) — polymorphic mass 0.0206, monomorphic-constant mass 0.9239, states 246, indeterminate 11
- N = 1000: `S3:1.00` 0.6920 (1/2-1/2); `ROLE:1.00` 0.2400 (1/6-5/6); `flip(ROLE):1.00` 0.0611 (1/6-5/6); `max(S2,min(S4,ROLE)):1.00` 0.0044 (1/3-2/3); `THEM(^S3):1.00` 0.0007 (1/2-1/2); `THEM(^ROLE):1.00` 0.0007 (1/6-5/6) — polymorphic mass 0.0011, monomorphic-constant mass 0.6920, states 215, indeterminate 8
- N = 3000: `S3:1.00` 0.7512 (1/2-1/2); `ROLE:1.00` 0.0783 (1/6-5/6); `S5:0.67 + flip(THEM(^S3)):0.33` 0.0571 (mixed); `max(S2,min(S4,ROLE)):1.00` 0.0459 (1/3-2/3); `S5:0.67 + flip(THEM(^ROLE)):0.33` 0.0386 (mixed); `flip(ROLE):1.00` 0.0188 (1/6-5/6) — polymorphic mass 0.0980, monomorphic-constant mass 0.7512, states 235, indeterminate 4
- N = 10000: `S3:1.00` 0.8014 (1/2-1/2); `max(S2,min(S4,ROLE)):1.00` 0.0640 (1/3-2/3); `ROLE:1.00` 0.0547 (1/6-5/6); `S5:0.67 + flip(THEM(^S3)):0.33` 0.0351 (mixed); `S5:0.67 + flip(THEM(^ROLE)):0.33` 0.0234 (mixed); `flip(ROLE):1.00` 0.0130 (1/6-5/6) — polymorphic mass 0.0600, monomorphic-constant mass 0.8014, states 252, indeterminate 3
- N = 30000: `S5:0.75 + flip(THEM(THEM)):0.08 + flip(THEM(^S2)):0.04 + flip(THEM(^S4)):0.12` 0.4572 (mixed); `S5:0.75 + flip(THEM(ME)):0.08 + flip(THEM(^S2)):0.04 + flip(THEM(^S4)):0.12` 0.4566 (mixed); `S3:1.00` 0.0737 (1/2-1/2); `ROLE:1.00` 0.0041 (1/6-5/6); `max(S2,min(S4,ROLE)):1.00` 0.0038 (1/3-2/3); `S5:0.67 + flip(THEM(^S3)):0.33` 0.0018 (mixed) — polymorphic mass 0.9169, monomorphic-constant mass 0.0737, states 258, indeterminate 7

Transitions between state labels (largest fluxes; rate = flux / label mass, relative units within a row of N; "via" = share of the flux leaving from a state with a non-constant program, i.e. a shadow or conceder path):

- N = 100: mixed → 1/2-1/2 0.00262 (via 1.00); 1/2-1/2 → ineff 5.24e-05 (via 0.00); 1/2-1/2 → 1/6-5/6 5.22e-05 (via 0.00); ineff → mixed 0.0108 (via 0.03); 1/6-5/6 → 1/2-1/2 0.000657 (via 1.00); 1/2-1/2 → mixed 2.8e-05 (via 0.00); ineff → 1/2-1/2 0.00634 (via 0.09); 1/6-5/6 → clash 0.000478 (via 1.00)
- N = 1000: 1/2-1/2 → 1/6-5/6 1.54e-07 (via 0.00); 1/6-5/6 → 1/2-1/2 3.43e-07 (via 1.00); mixed → 1/2-1/2 9.78e-06 (via 1.00); 1/2-1/2 → mixed 1.14e-08 (via 1.00); 1/6-5/6 → mixed 2.61e-08 (via 1.00); mixed → 1/6-5/6 4.58e-06 (via 1.00); ineff → 1/2-1/2 4.28e-06 (via 0.92); mixed → ineff 9.55e-08 (via 1.00)
- N = 3000: 1/2-1/2 → 1/6-5/6 5.12e-08 (via 0.00); 1/6-5/6 → 1/2-1/2 3.75e-07 (via 1.00); mixed → ineff 5.41e-08 (via 1.00); ineff → 1/2-1/2 5.53e-07 (via 0.88); 1/2-1/2 → mixed 3.16e-09 (via 1.00); 1/6-5/6 → mixed 2.43e-08 (via 1.00); ineff → mixed 2.77e-07 (via 0.51); mixed → 1/2-1/2 5.97e-09 (via 1.00)
- N = 10000: 1/2-1/2 → 1/6-5/6 1.54e-08 (via 0.00); 1/6-5/6 → 1/2-1/2 1.71e-07 (via 1.00); mixed → ineff 3.59e-08 (via 1.00); ineff → 1/2-1/2 2.25e-07 (via 0.88); ineff → mixed 1.85e-07 (via 0.71); 1/2-1/2 → mixed 9.31e-10 (via 1.00); 1/6-5/6 → mixed 1.09e-08 (via 1.00); mixed → 1/2-1/2 2e-09 (via 1.00)
- N = 30000: 1/2-1/2 → 1/6-5/6 5.12e-09 (via 0.00); 1/6-5/6 → 1/2-1/2 6.99e-08 (via 1.00); mixed → ineff 7.67e-11 (via 1.00); ineff → 1/2-1/2 9.23e-08 (via 0.88); ineff → mixed 8.71e-08 (via 0.75); 1/2-1/2 → mixed 2.99e-10 (via 1.00); 1/6-5/6 → mixed 4.29e-09 (via 1.00); mixed → 1/2-1/2 4e-12 (via 1.00)

Top exits of the heaviest states (probability per mutation event; mutants):

- N = 100, from `S3:1.00`: `S2:1.00` (ineff) 4.7e-05 by `S2`; `ROLE:1.00` (1/6-5/6) 4.1e-05 by `ROLE`; `X:1.00` (mixed) 2e-05 by `X`; `flip(ROLE):1.00` (1/6-5/6) 1e-05 by `flip(ROLE)`
- N = 100, from `ROLE:1.00`: `S3:1.00` (1/2-1/2) 0.00065 by `S3`; `S5:1.00` (clash) 0.00035 by `S5`; `X:1.00` (mixed) 0.00015 by `X`; `S2:1.00` (ineff) 0.00014 by `S2`
- N = 100, from `S2:0.50 + S4:0.50`: `S3:1.00` (1/2-1/2) 0.002 by `S3`; `X:1.00` (mixed) 0.00028 by `X`; `ROLE:1.00` (1/6-5/6) 0.00026 by `ROLE`; `flip(ROLE):1.00` (1/6-5/6) 6.5e-05 by `flip(ROLE)`
- N = 1000, from `S3:1.00`: `THEM(^S3):1.00` (1/2-1/2) 1.5e-07 by `THEM(^S3)`; `THEM(^ROLE):1.00` (1/6-5/6) 1.4e-07 by `THEM(^ROLE)`; `THEM(^flip(ROLE)):1.00` (1/6-5/6) 8e-09 by `THEM(^flip(ROLE))`; `flip(THEM(^S3)):1.00` (1/2-1/2) 8e-09 by `flip(THEM(^S3))`
- N = 1000, from `ROLE:1.00`: `flip(THEM(^S3)):1.00` (1/2-1/2) 8e-09 by `flip(THEM(^S3))`; `flip(THEM(^ROLE)):1.00` (1/6-5/6) 8e-09 by `flip(THEM(^ROLE))`; `S3:1.00` (1/2-1/2) 6.2e-10 by `S3`; `max(S2,min(S4,ROLE)):1.00` (1/3-2/3) 2.7e-10 by `max(S2,min(S4,ROLE))`
- N = 1000, from `flip(ROLE):1.00`: `flip(THEM(^S3)):1.00` (1/2-1/2) 8e-09 by `flip(THEM(^S3))`; `flip(THEM(^ROLE)):1.00` (1/6-5/6) 8e-09 by `flip(THEM(^ROLE))`; `S3:1.00` (1/2-1/2) 6.2e-10 by `S3`; `max(THEM(THEM),S5):1.00` (ineff) 4.6e-11 by `max(THEM(THEM),S5)`
- N = 3000, from `S3:1.00`: `THEM(^S3):1.00` (1/2-1/2) 4.9e-08 by `THEM(^S3)`; `THEM(^ROLE):1.00` (1/6-5/6) 4.6e-08 by `THEM(^ROLE)`; `THEM(^flip(ROLE)):1.00` (1/6-5/6) 2.7e-09 by `THEM(^flip(ROLE))`; `flip(THEM(^S3)):1.00` (1/2-1/2) 2.7e-09 by `flip(THEM(^S3))`
- N = 3000, from `ROLE:1.00`: `flip(THEM(^S3)):1.00` (1/2-1/2) 2.7e-09 by `flip(THEM(^S3))`; `flip(THEM(^ROLE)):1.00` (1/6-5/6) 2.7e-09 by `flip(THEM(^ROLE))`; `max(THEM(THEM),ROLE):1.00` (ineff) 9.9e-17 by `max(THEM(THEM),ROLE)`; `max(THEM(THEM),S5):1.00` (ineff) 9.9e-17 by `max(THEM(THEM),S5)`
- N = 3000, from `S5:0.67 + flip(THEM(^S3)):0.33`: `max(THEM(THEM),S5):1.00` (ineff) 2.1e-08 by `max(THEM(THEM),S5)`; `max(THEM(ME),S5):1.00` (ineff) 2.1e-08 by `max(THEM(ME),S5)`; `S3:1.00` (1/2-1/2) 1.3e-09 by `S3`; `ROLE:1.00` (1/6-5/6) 5e-10 by `ROLE`
- N = 10000, from `S3:1.00`: `THEM(^S3):1.00` (1/2-1/2) 1.5e-08 by `THEM(^S3)`; `THEM(^ROLE):1.00` (1/6-5/6) 1.4e-08 by `THEM(^ROLE)`; `THEM(^flip(ROLE)):1.00` (1/6-5/6) 8e-10 by `THEM(^flip(ROLE))`; `flip(THEM(^S3)):1.00` (1/2-1/2) 8e-10 by `flip(THEM(^S3))`
- N = 10000, from `max(S2,min(S4,ROLE)):1.00`: `flip(THEM(^S3)):1.00` (1/2-1/2) 8e-10 by `flip(THEM(^S3))`; `flip(THEM(^ROLE)):1.00` (1/6-5/6) 8e-10 by `flip(THEM(^ROLE))`; `S3:1.00` (1/2-1/2) 3.7e-74 by `S3`; `min(S3,max(X,ROLE)):1.00` (mixed) 1.5e-82 by `min(S3,max(X,ROLE))`
- N = 10000, from `ROLE:1.00`: `flip(THEM(^S3)):1.00` (1/2-1/2) 8e-10 by `flip(THEM(^S3))`; `flip(THEM(^ROLE)):1.00` (1/6-5/6) 8e-10 by `flip(THEM(^ROLE))`; `max(THEM(THEM),ROLE):1.00` (ineff) 5.4e-36 by `max(THEM(THEM),ROLE)`; `max(THEM(THEM),S5):1.00` (ineff) 5.4e-36 by `max(THEM(THEM),S5)`
- N = 30000, from `S5:0.75 + flip(THEM(THEM)):0.08 + flip(THEM(^S2)):0.04 + flip(THEM(^S4)):0.12`: `ROLE:1.00` (1/6-5/6) 2.5e-15 by `ROLE`; `flip(ROLE):1.00` (1/6-5/6) 6.2e-16 by `flip(ROLE)`; `S3:1.00` (1/2-1/2) 2.8e-34 by `S3`; `max(S2,min(S4,ROLE)):1.00` (1/3-2/3) 1.3e-37 by `max(S2,min(S4,ROLE))`
- N = 30000, from `S5:0.75 + flip(THEM(ME)):0.08 + flip(THEM(^S2)):0.04 + flip(THEM(^S4)):0.12`: `ROLE:1.00` (1/6-5/6) 2.5e-15 by `ROLE`; `flip(ROLE):1.00` (1/6-5/6) 6.2e-16 by `flip(ROLE)`; `S3:1.00` (1/2-1/2) 2.8e-34 by `S3`; `THEM(^S2):1.00` (ineff) 5.6e-36 by `THEM(^S2)`
- N = 30000, from `S3:1.00`: `THEM(^S3):1.00` (1/2-1/2) 4.9e-09 by `THEM(^S3)`; `THEM(^ROLE):1.00` (1/6-5/6) 4.6e-09 by `THEM(^ROLE)`; `THEM(^flip(ROLE)):1.00` (1/6-5/6) 2.7e-10 by `THEM(^flip(ROLE))`; `flip(THEM(^S3)):1.00` (1/2-1/2) 2.7e-10 by `flip(THEM(^S3))`

### dollar5, norole (one population of N)

Encounter-level π-weighted outcome shares (per ordered split: slot 1 | slot 2 for fixed roles; the focal program first otherwise).

| N | 1/6\|5/6 | 1/3\|2/3 | 1/2\|1/2 | 2/3\|1/3 | 5/6\|1/6 | ineff | clash | P(efficient) | E[max share] | ex ante max | E[max norm. share \| compatible] | dwl | cut |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.0002 | 0.0044 | 0.9741 | 0.0044 | 0.0002 | 0.0096 | 0.0069 | 0.9835 | 0.497 | 0.495 | 0.502 | 0.0051 | 8.4e-07 |
| 1000 | 0.0002 | 0.0000 | 0.9990 | 0.0000 | 0.0002 | 0.0000 | 0.0005 | 0.9995 | 0.500 | 0.500 | 0.500 | 0.0002 | 6.3e-11 |
| 3000 | 0.0136 | 0.0010 | 0.9384 | 0.0010 | 0.0136 | 0.0046 | 0.0278 | 0.9675 | 0.494 | 0.485 | 0.510 | 0.0154 | 2.0e-09 |
| 10000 | 0.1874 | 0.0191 | 0.0004 | 0.0191 | 0.1874 | 0.0087 | 0.5779 | 0.4135 | 0.340 | 0.208 | 0.811 | 0.2915 | 3.3e-13 |
| 30000 | 0.1875 | 0.0191 | 0.0000 | 0.0191 | 0.1875 | 0.0087 | 0.5781 | 0.4132 | 0.340 | 0.208 | 0.811 | 0.2917 | 1.2e-20 |

Support (top states, π, label):

- N = 100: `S3:1.00` 0.9724 (1/2-1/2); `S2:0.50 + S4:0.50` 0.0164 (mixed); `S2:1.00` 0.0028 (ineff); `X:1.00` 0.0021 (mixed); `S4:0.25 + X:0.75` 0.0015 (mixed); `min(S3,X):1.00` 0.0011 (mixed) — polymorphic mass 0.0194, monomorphic-constant mass 0.9757, states 143, indeterminate 6
- N = 1000: `S3:1.00` 0.9977 (1/2-1/2); `THEM(^S3):1.00` 0.0012 (1/2-1/2); `S5:0.67 + flip(THEM(^S3)):0.33` 0.0010 (mixed); `max(THEM(THEM),S5):1.00` 0.0000 (ineff); `max(THEM(ME),S5):1.00` 0.0000 (ineff); `S2:0.33 + max(S4,THEM(THEM)):0.67` 0.0000 (mixed) — polymorphic mass 0.0010, monomorphic-constant mass 0.9977, states 130, indeterminate 6
- N = 3000: `S3:1.00` 0.9304 (1/2-1/2); `S5:0.67 + flip(THEM(^S3)):0.33` 0.0608 (mixed); `max(THEM(THEM),S5):1.00` 0.0023 (ineff); `max(THEM(ME),S5):1.00` 0.0017 (ineff); `S2:0.17 + S4:0.50 + flip(THEM(THEM)):0.07 + flip(THEM(^S5)):0.27` 0.0014 (mixed); `THEM(^S3):1.00` 0.0011 (1/2-1/2) — polymorphic mass 0.0645, monomorphic-constant mass 0.9304, states 146, indeterminate 2
- N = 10000: `S5:0.75 + flip(THEM(THEM)):0.08 + flip(THEM(^S4)):0.12 + flip(THEM(^S2)):0.04` 0.7958 (mixed); `S5:0.75 + flip(THEM(ME)):0.08 + flip(THEM(^S4)):0.12 + flip(THEM(^S2)):0.04` 0.2038 (mixed); `S3:1.00` 0.0004 (1/2-1/2); `S5:0.67 + flip(THEM(^S3)):0.33` 0.0000 (mixed); `S5:0.80 + flip(THEM(THEM)):0.04 + flip(THEM(^S5)):0.16` 0.0000 (mixed); `max(THEM(THEM),S5):1.00` 0.0000 (ineff) — polymorphic mass 0.9996, monomorphic-constant mass 0.0004, states 159, indeterminate 0
- N = 30000: `S5:0.75 + flip(THEM(THEM)):0.08 + flip(THEM(^S4)):0.12 + flip(THEM(^S2)):0.04` 1.0000 (mixed); `max(THEM(THEM),X):1.00` 0.0000 (ineff); `S5:0.78 + flip(THEM(^X)):0.22` 0.0000 (mixed); `S1:0.20 + S5:0.80` 0.0000 (mixed); `S2:0.17 + S4:0.50 + flip(THEM(THEM)):0.07 + flip(THEM(^S5)):0.27` 0.0000 (mixed); `S2:0.08 + S4:0.50 + flip(THEM(THEM)):0.17 + flip(THEM(^S4)):0.25` 0.0000 (mixed) — polymorphic mass 1.0000, monomorphic-constant mass 0.0000, states 164, indeterminate 2

Transitions between state labels (largest fluxes; rate = flux / label mass, relative units within a row of N; "via" = share of the flux leaving from a state with a non-constant program, i.e. a shadow or conceder path):

- N = 100: mixed → 1/2-1/2 0.00308 (via 1.00); 1/2-1/2 → ineff 6.04e-05 (via 0.00); ineff → mixed 0.014 (via 0.02); 1/2-1/2 → mixed 3.36e-05 (via 0.01); ineff → 1/2-1/2 0.00809 (via 0.07); clash → mixed 0.0183 (via 0.03); mixed → ineff 0.00031 (via 1.00); 1/2-1/2 → clash 6.46e-06 (via 0.00)
- N = 1000: 1/2-1/2 → mixed 1.22e-08 (via 1.00); mixed → 1/2-1/2 1.16e-05 (via 1.00); mixed → ineff 1.17e-07 (via 1.00); ineff → 1/2-1/2 3.54e-06 (via 0.91); ineff → mixed 1.32e-06 (via 0.53); 1/2-1/2 → ineff 1.23e-12 (via 1.00); clash → mixed 0.0115 (via 0.00); mixed → clash 2.14e-13 (via 1.00)
- N = 3000: mixed → ineff 8.04e-08 (via 1.00); 1/2-1/2 → mixed 4.08e-09 (via 1.00); ineff → 1/2-1/2 7.08e-07 (via 0.85); ineff → mixed 5.88e-07 (via 0.65); mixed → 1/2-1/2 1.51e-08 (via 1.00); 1/2-1/2 → ineff 4.04e-13 (via 1.00); ineff → clash 1.43e-16 (via 1.00); mixed → clash 4.7e-21 (via 1.00)
- N = 10000: mixed → ineff 7.64e-13 (via 1.00); 1/2-1/2 → mixed 1.23e-09 (via 1.00); ineff → mixed 2.64e-07 (via 0.71); ineff → 1/2-1/2 2.55e-07 (via 0.85); mixed → 1/2-1/2 8.16e-14 (via 1.00); 1/2-1/2 → ineff 1.21e-13 (via 1.00); ineff → clash 3.04e-32 (via 1.00); mixed → clash 1.78e-48 (via 1.00)
- N = 30000: mixed → 1/2-1/2 3.37e-34 (via 1.00); mixed → ineff 5.2e-42 (via 1.00); mixed → clash 2.31e-247 (via 1.00)

Top exits of the heaviest states (probability per mutation event; mutants):

- N = 100, from `S3:1.00`: `S2:1.00` (ineff) 5.6e-05 by `S2`; `X:1.00` (mixed) 2.3e-05 by `X`; `min(S3,X):1.00` (mixed) 6e-06 by `min(S3,X)`; `S5:1.00` (clash) 3.2e-06 by `S5`
- N = 100, from `S2:0.50 + S4:0.50`: `S3:1.00` (1/2-1/2) 0.0023 by `S3`; `X:1.00` (mixed) 0.00033 by `X`; `S5:1.00` (clash) 3.1e-05 by `S5`; `min(S3,X):1.00` (mixed) 2.6e-05 by `min(S3,X)`
- N = 100, from `S2:1.00`: `S2:0.50 + S4:0.50` (mixed) 0.012 by `S4`; `S3:1.00` (1/2-1/2) 0.008 by `S3`; `X:1.00` (mixed) 0.0013 by `X`; `S2:0.57 + max(S4,X):0.43` (mixed) 0.00019 by `max(S4,X)`
- N = 1000, from `S3:1.00`: `THEM(^S3):1.00` (1/2-1/2) 2e-07 by `THEM(^S3)`; `flip(THEM(^S3)):1.00` (1/2-1/2) 1.2e-08 by `flip(THEM(^S3))`; `min(S3,max(X,X)):1.00` (mixed) 1.1e-11 by `min(S3,max(X,X))`; `max(S2,min(S3,X)):1.00` (mixed) 4.1e-15 by `max(S2,min(S3,X))`
- N = 1000, from `THEM(^S3):1.00`: `S3:1.00` (1/2-1/2) 0.00016 by `S3`; `flip(THEM(^S3)):1.00` (1/2-1/2) 1.2e-08 by `flip(THEM(^S3))`; `min(S3,max(X,X)):1.00` (mixed) 4.2e-10 by `min(S3,max(X,X))`; `max(S2,min(S3,X)):1.00` (mixed) 1.6e-11 by `max(S2,min(S3,X))`
- N = 1000, from `S5:0.67 + flip(THEM(^S3)):0.33`: `S3:1.00` (1/2-1/2) 1.2e-05 by `S3`; `max(THEM(ME),S5):1.00` (ineff) 5.7e-08 by `max(THEM(ME),S5)`; `max(THEM(THEM),S5):1.00` (ineff) 5.7e-08 by `max(THEM(THEM),S5)`; `THEM(^S3):1.00` (1/2-1/2) 1.4e-08 by `THEM(^S3)`
- N = 3000, from `S3:1.00`: `THEM(^S3):1.00` (1/2-1/2) 6.6e-08 by `THEM(^S3)`; `flip(THEM(^S3)):1.00` (1/2-1/2) 4.1e-09 by `flip(THEM(^S3))`; `min(S3,max(X,X)):1.00` (mixed) 2.3e-20 by `min(S3,max(X,X))`; `max(S2,min(S3,X)):1.00` (mixed) 1.7e-32 by `max(S2,min(S3,X))`
- N = 3000, from `S5:0.67 + flip(THEM(^S3)):0.33`: `max(THEM(ME),S5):1.00` (ineff) 3.3e-08 by `max(THEM(ME),S5)`; `max(THEM(THEM),S5):1.00` (ineff) 3.3e-08 by `max(THEM(THEM),S5)`; `S3:1.00` (1/2-1/2) 1.6e-09 by `S3`; `THEM(^S3):1.00` (1/2-1/2) 2e-12 by `THEM(^S3)`
- N = 3000, from `max(THEM(THEM),S5):1.00`: `THEM(ME):1.00` (ineff) 3.4e-07 by `THEM(ME)`; `THEM(THEM):1.00` (ineff) 3.4e-07 by `THEM(THEM)`; `flip(THEM(THEM)):1.00` (ineff) 6.2e-08 by `flip(THEM(THEM))`; `flip(THEM(ME)):1.00` (ineff) 6.2e-08 by `flip(THEM(ME))`
- N = 10000, from `S5:0.75 + flip(THEM(THEM)):0.08 + flip(THEM(^S4)):0.12 + flip(THEM(^S2)):0.04`: `S3:1.00` (1/2-1/2) 3.2e-14 by `S3`; `max(THEM(ME),S5):1.00` (ineff) 8.6e-20 by `max(THEM(ME),S5)`; `max(THEM(THEM),S5):1.00` (ineff) 8.6e-20 by `max(THEM(THEM),S5)`; `S5:0.80 + flip(THEM(THEM)):0.04 + flip(THEM(^S5)):0.16` (mixed) 2e-20 by `flip(THEM(^S5))`
- N = 10000, from `S5:0.75 + flip(THEM(ME)):0.08 + flip(THEM(^S4)):0.12 + flip(THEM(^S2)):0.04`: `S3:1.00` (1/2-1/2) 3.2e-14 by `S3`; `THEM(^S2):1.00` (ineff) 9.3e-17 by `THEM(^S2)`; `max(THEM(ME),S5):1.00` (ineff) 8.6e-20 by `max(THEM(ME),S5)`; `max(THEM(THEM),S5):1.00` (ineff) 8.6e-20 by `max(THEM(THEM),S5)`
- N = 10000, from `S3:1.00`: `THEM(^S3):1.00` (1/2-1/2) 2e-08 by `THEM(^S3)`; `flip(THEM(^S3)):1.00` (1/2-1/2) 1.2e-09 by `flip(THEM(^S3))`; `min(S3,max(X,X)):1.00` (mixed) 9.2e-51 by `min(S3,max(X,X))`; `max(S2,min(S3,X)):1.00` (mixed) 2.7e-93 by `max(S2,min(S3,X))`
- N = 30000, from `S5:0.75 + flip(THEM(THEM)):0.08 + flip(THEM(^S4)):0.12 + flip(THEM(^S2)):0.04`: `S3:1.00` (1/2-1/2) 3.4e-34 by `S3`; `max(THEM(ME),S5):1.00` (ineff) 2.6e-42 by `max(THEM(ME),S5)`; `max(THEM(THEM),S5):1.00` (ineff) 2.6e-42 by `max(THEM(THEM),S5)`; `S5:0.80 + flip(THEM(THEM)):0.04 + flip(THEM(^S5)):0.16` (mixed) 4.7e-47 by `flip(THEM(^S5))`
- N = 30000, from `max(THEM(THEM),X):1.00`: `S3:1.00` (1/2-1/2) 0.0064 by `S3`; `S2:0.75 + max(THEM(THEM),X):0.25` (mixed) 0.0048 by `S2`; `min(S3,X):1.00` (mixed) 0.00011 by `min(S3,X)`; `min(S2,X):0.46 + max(THEM(THEM),X):0.54` (?) 9.1e-05 by `min(S2,X)`
- N = 30000, from `S5:0.78 + flip(THEM(^X)):0.22`: `max(THEM(ME),S5):1.00` (ineff) 1.1e-08 by `max(THEM(ME),S5)`; `max(THEM(THEM),S5):1.00` (ineff) 1.1e-08 by `max(THEM(THEM),S5)`; `S5:0.79 + flip(THEM(^S4)):0.05 + flip(THEM(^X)):0.16` (?) 6.5e-10 by `flip(THEM(^S4))`; `S3:1.00` (1/2-1/2) 1e-26 by `S3`

### dollar5, fixed (N per slot)

Encounter-level π-weighted outcome shares (per ordered split: slot 1 | slot 2 for fixed roles; the focal program first otherwise).

| N | 1/6\|5/6 | 1/3\|2/3 | 1/2\|1/2 | 2/3\|1/3 | 5/6\|1/6 | ineff | clash | P(efficient) | E[max share] | ex ante max | E[max norm. share \| compatible] | dwl | cut |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.0424 | 0.2649 | 0.3748 | 0.2649 | 0.0424 | 0.0092 | 0.0014 | 0.9894 | 0.616 | 0.616 | 0.618 | 0.0015 | 0.0e+00 |
| 1000 | 0.4958 | 0.0028 | 0.0027 | 0.0028 | 0.4958 | 0.0000 | 0.0000 | 1.0000 | 0.831 | 0.831 | 0.831 | 0.0000 | 3.3e-26 |
| 10000 | 0.4983 | 0.0010 | 0.0013 | 0.0010 | 0.4983 | 0.0000 | 0.0000 | 1.0000 | 0.833 | 0.833 | 0.833 | 0.0000 | 4.7e-28 |

Support (top states, π, label):

- N = 100: `S3 | S3` 0.3591 (1/2|1/2); `S4 | S2` 0.2623 (2/3|1/3); `S2 | S4` 0.2623 (1/3|2/3); `S1 | S5` 0.0404 (1/6|5/6); `S5 | S1` 0.0404 (5/6|1/6); `S3 | S2` 0.0024 (ineff) — constant pairs 0.9722; slot 1 gets more 0.3126, slot 2 0.3126, equal 0.3748
- N = 1000: `S1 | S5` 0.4930 (1/6|5/6); `S5 | S1` 0.4930 (5/6|1/6); `S4 | S2` 0.0028 (2/3|1/3); `S2 | S4` 0.0028 (1/3|2/3); `S3 | S3` 0.0026 (1/2|1/2); `flip(THEM(THEM)) | S5` 0.0011 (1/6|5/6) — constant pairs 0.9943; slot 1 gets more 0.4986, slot 2 0.4986, equal 0.0027
- N = 10000: `S5 | S1` 0.4955 (5/6|1/6); `S1 | S5` 0.4955 (1/6|5/6); `S3 | S3` 0.0012 (1/2|1/2); `flip(THEM(THEM)) | S5` 0.0011 (1/6|5/6); `S5 | flip(THEM(THEM))` 0.0011 (5/6|1/6); `flip(THEM(ME)) | S5` 0.0011 (1/6|5/6) — constant pairs 0.9943; slot 1 gets more 0.4994, slot 2 0.4994, equal 0.0013

Transitions between state labels (largest fluxes; rate = flux / label mass, relative units within a row of N; "via" = share of the flux leaving from a state with a non-constant program, i.e. a shadow or conceder path):

- N = 100: 1/2|1/2 → ineff 0.247 (via 0.04); ineff → 1/2|1/2 11.9 (via 0.02); 2/3|1/3 → ineff 0.246 (via 0.00); 1/3|2/3 → ineff 0.246 (via 0.00); ineff → 2/3|1/3 8.6 (via 0.01); ineff → 1/3|2/3 8.6 (via 0.01); mixed → 1/3|2/3 3.17 (via 1.00); mixed → 2/3|1/3 3.17 (via 1.00)
- N = 1000: 2/3|1/3 → 5/6|1/6 11.5 (via 1.00); 1/3|2/3 → 1/6|5/6 11.5 (via 1.00); 1/6|5/6 → 5/6|1/6 0.0615 (via 1.00); 5/6|1/6 → 1/6|5/6 0.0615 (via 1.00); 1/6|5/6 → 2/3|1/3 0.0462 (via 1.00); 5/6|1/6 → 1/3|2/3 0.0462 (via 1.00); 1/6|5/6 → 1/2|1/2 0.0318 (via 1.00); 5/6|1/6 → 1/2|1/2 0.0318 (via 1.00)
- N = 10000: 2/3|1/3 → 5/6|1/6 32.7 (via 1.00); 1/3|2/3 → 1/6|5/6 32.7 (via 1.00); 1/6|5/6 → 5/6|1/6 0.062 (via 1.00); 5/6|1/6 → 1/6|5/6 0.062 (via 1.00); 1/6|5/6 → 2/3|1/3 0.0465 (via 1.00); 5/6|1/6 → 1/3|2/3 0.0465 (via 1.00); 1/6|5/6 → 1/2|1/2 0.0321 (via 1.00); 5/6|1/6 → 1/2|1/2 0.0321 (via 1.00)

Convention-to-convention moves (exact, from the generator): from each efficient constant pair, the next different efficient constant pair hit, the expected time to it, and the exact exit time from its label (mutation events).

| N | from | next convention hit | time to next | exit time from label | first label after exit |
|---|---|---|---|---|---|
| 100 | 1/6\|5/6 | 1/3\|2/3 0.32, 1/2\|1/2 0.31, 2/3\|1/3 0.24, 5/6\|1/6 0.13 | 6.47e+03 | 4.71e+03 | clash 0.55, mixed 0.31, ineff 0.13, 5/6\|1/6 0.00 |
| 100 | 1/3\|2/3 | 1/6\|5/6 0.46, 1/2\|1/2 0.45, 5/6\|1/6 0.06, 2/3\|1/3 0.04 | 2.8e+04 | 1.21e+04 | ineff 0.70, mixed 0.24, 1/6\|5/6 0.02, clash 0.01 |
| 100 | 1/2\|1/2 | 1/3\|2/3 0.44, 2/3\|1/3 0.44, 1/6\|5/6 0.06, 5/6\|1/6 0.06 | 3.01e+04 | 1.4e+04 | ineff 0.81, mixed 0.13, 5/6\|1/6 0.02, 1/6\|5/6 0.02 |
| 100 | 2/3\|1/3 | 5/6\|1/6 0.46, 1/2\|1/2 0.45, 1/6\|5/6 0.06, 1/3\|2/3 0.04 | 2.8e+04 | 1.21e+04 | ineff 0.70, mixed 0.24, 5/6\|1/6 0.02, clash 0.01 |
| 100 | 5/6\|1/6 | 2/3\|1/3 0.32, 1/2\|1/2 0.31, 1/3\|2/3 0.24, 1/6\|5/6 0.13 | 6.47e+03 | 4.71e+03 | clash 0.55, mixed 0.31, ineff 0.13, 1/6\|5/6 0.00 |
| 1000 | 1/6\|5/6 | 5/6\|1/6 0.98, 2/3\|1/3 0.01, 1/2\|1/2 0.01, 1/3\|2/3 0.00 | 4.52e+06 | 4.51e+06 | 5/6\|1/6 0.37, 2/3\|1/3 0.28, 1/2\|1/2 0.19, 1/3\|2/3 0.10 |
| 1000 | 1/3\|2/3 | 5/6\|1/6 0.50, 1/6\|5/6 0.50, 2/3\|1/3 0.00, 1/2\|1/2 0.00 | 2.29e+06 | 2.25e+06 | 1/6\|5/6 0.49, 5/6\|1/6 0.25, 2/3\|1/3 0.16, 1/2\|1/2 0.08 |
| 1000 | 1/2\|1/2 | 1/6\|5/6 0.49, 5/6\|1/6 0.49, 1/3\|2/3 0.01, 2/3\|1/3 0.01 | 2.08e+06 | 1.94e+06 | 1/6\|5/6 0.32, 5/6\|1/6 0.32, 2/3\|1/3 0.16, 1/3\|2/3 0.16 |
| 1000 | 2/3\|1/3 | 1/6\|5/6 0.50, 5/6\|1/6 0.50, 1/3\|2/3 0.00, 1/2\|1/2 0.00 | 2.29e+06 | 2.25e+06 | 5/6\|1/6 0.49, 1/6\|5/6 0.25, 1/3\|2/3 0.16, 1/2\|1/2 0.08 |
| 1000 | 5/6\|1/6 | 1/6\|5/6 0.98, 1/3\|2/3 0.01, 1/2\|1/2 0.01, 2/3\|1/3 0.00 | 4.52e+06 | 4.51e+06 | 1/6\|5/6 0.37, 1/3\|2/3 0.28, 1/2\|1/2 0.19, 2/3\|1/3 0.10 |
| 10000 | 1/6\|5/6 | 5/6\|1/6 0.99, 1/2\|1/2 0.00, 2/3\|1/3 0.00, 1/3\|2/3 0.00 | 4.51e+07 | 4.5e+07 | 5/6\|1/6 0.37, 2/3\|1/3 0.28, 1/2\|1/2 0.19, 1/3\|2/3 0.10 |
| 10000 | 1/3\|2/3 | 5/6\|1/6 0.50, 1/6\|5/6 0.50, 1/2\|1/2 0.00, 2/3\|1/3 0.00 | 2.26e+07 | 2.25e+07 | 1/6\|5/6 0.50, 5/6\|1/6 0.25, 2/3\|1/3 0.16, 1/2\|1/2 0.08 |
| 10000 | 1/2\|1/2 | 5/6\|1/6 0.48, 1/6\|5/6 0.48, 2/3\|1/3 0.02, 1/3\|2/3 0.02 | 1.25e+07 | 1.1e+07 | 5/6\|1/6 0.30, 1/6\|5/6 0.30, 1/3\|2/3 0.18, 2/3\|1/3 0.18 |
| 10000 | 2/3\|1/3 | 1/6\|5/6 0.50, 5/6\|1/6 0.50, 1/2\|1/2 0.00, 1/3\|2/3 0.00 | 2.26e+07 | 2.25e+07 | 5/6\|1/6 0.50, 1/6\|5/6 0.25, 1/3\|2/3 0.16, 1/2\|1/2 0.08 |
| 10000 | 5/6\|1/6 | 1/6\|5/6 0.99, 1/2\|1/2 0.00, 1/3\|2/3 0.00, 2/3\|1/3 0.00 | 4.51e+07 | 4.5e+07 | 1/6\|5/6 0.37, 1/3\|2/3 0.28, 1/2\|1/2 0.19, 2/3\|1/3 0.10 |

## ε → 0 chains: dollar3

### dollar3, role (one population of N)

Encounter-level π-weighted outcome shares (per ordered split: slot 1 | slot 2 for fixed roles; the focal program first otherwise).

| N | 1/3\|2/3 | 1/2\|1/2 | 2/3\|1/3 | ineff | clash | P(efficient) | E[max share] | ex ante max | E[max norm. share \| compatible] | dwl | cut |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.1214 | 0.7341 | 0.1214 | 0.0155 | 0.0077 | 0.9768 | 0.535 | 0.494 | 0.542 | 0.0058 | 1.3e-06 |
| 1000 | 0.4212 | 0.1568 | 0.4212 | 0.0003 | 0.0005 | 0.9992 | 0.640 | 0.500 | 0.640 | 0.0003 | 5.5e-10 |
| 10000 | 0.0988 | 0.7882 | 0.0988 | 0.0082 | 0.0059 | 0.9858 | 0.529 | 0.496 | 0.533 | 0.0043 | 1.5e-10 |

Support (top states, π, label):

- N = 100: `M:1.00` 0.7297 (1/2-1/2); `ROLE:1.00` 0.1870 (1/3-2/3); `flip(ROLE):1.00` 0.0463 (1/3-2/3); `L:0.18 + X:0.82` 0.0090 (mixed); `L:0.50 + H:0.50` 0.0076 (mixed); `X:1.00` 0.0074 (mixed) — polymorphic mass 0.0186, monomorphic-constant mass 0.7320, states 130, indeterminate 0
- N = 1000: `ROLE:1.00` 0.6716 (1/3-2/3); `flip(ROLE):1.00` 0.1673 (1/3-2/3); `M:1.00` 0.1555 (1/2-1/2); `H:0.33 + flip(THEM(^M)):0.67` 0.0025 (mixed); `H:0.33 + flip(THEM(^ROLE)):0.67` 0.0025 (mixed); `THEM(^M):1.00` 0.0002 (1/2-1/2) — polymorphic mass 0.0050, monomorphic-constant mass 0.1555, states 117, indeterminate 0
- N = 10000: `M:1.00` 0.7724 (1/2-1/2); `ROLE:1.00` 0.1317 (1/3-2/3); `H:0.33 + flip(THEM(^M)):0.67` 0.0319 (mixed); `flip(ROLE):1.00` 0.0314 (1/3-2/3); `H:0.33 + flip(THEM(^ROLE)):0.67` 0.0213 (mixed); `max(THEM(THEM),H):1.00` 0.0045 (ineff) — polymorphic mass 0.0546, monomorphic-constant mass 0.7724, states 121, indeterminate 0

Transitions between state labels (largest fluxes; rate = flux / label mass, relative units within a row of N; "via" = share of the flux leaving from a state with a non-constant program, i.e. a shadow or conceder path):

- N = 100: 1/3-2/3 → 1/2-1/2 0.00068 (via 1.00); 1/2-1/2 → 1/3-2/3 0.000196 (via 0.00); mixed → 1/2-1/2 0.00409 (via 1.00); 1/2-1/2 → mixed 0.00014 (via 0.00); mixed → 1/3-2/3 0.00295 (via 1.00); 1/2-1/2 → ineff 9.49e-05 (via 0.00); 1/3-2/3 → mixed 0.000275 (via 1.00); ineff → mixed 0.0116 (via 0.10)
- N = 1000: 1/3-2/3 → 1/2-1/2 7.33e-08 (via 1.00); 1/2-1/2 → 1/3-2/3 3.06e-07 (via 0.01); mixed → 1/3-2/3 6.66e-06 (via 1.00); 1/2-1/2 → mixed 1.25e-07 (via 0.99); 1/3-2/3 → mixed 2.29e-08 (via 1.00); mixed → 1/2-1/2 9.47e-07 (via 1.00); mixed → ineff 2.33e-07 (via 1.00); ineff → 1/2-1/2 3.39e-06 (via 1.00)
- N = 10000: 1/2-1/2 → 1/3-2/3 3.03e-08 (via 0.00); 1/3-2/3 → 1/2-1/2 1.35e-07 (via 1.00); mixed → ineff 9.15e-08 (via 1.00); ineff → 1/2-1/2 4.03e-07 (via 1.00); 1/3-2/3 → mixed 1.14e-08 (via 1.00); 1/2-1/2 → mixed 2.43e-09 (via 1.00); ineff → mixed 2.29e-07 (via 1.00); mixed → 1/3-2/3 7.68e-09 (via 1.00)

Top exits of the heaviest states (probability per mutation event; mutants):

- N = 100, from `M:1.00`: `ROLE:1.00` (1/3-2/3) 0.00015 by `ROLE`; `X:1.00` (mixed) 0.0001 by `X`; `L:1.00` (ineff) 6.9e-05 by `L`; `flip(ROLE):1.00` (1/3-2/3) 3.8e-05 by `flip(ROLE)`
- N = 100, from `ROLE:1.00`: `M:1.00` (1/2-1/2) 0.00068 by `M`; `X:1.00` (mixed) 0.00023 by `X`; `H:1.00` (clash) 7.5e-05 by `H`; `L:1.00` (ineff) 6.9e-05 by `L`
- N = 100, from `flip(ROLE):1.00`: `M:1.00` (1/2-1/2) 0.00068 by `M`; `X:1.00` (mixed) 0.00023 by `X`; `ROLE:1.00` (1/3-2/3) 0.00023 by `ROLE`; `H:1.00` (clash) 7.5e-05 by `H`
- N = 1000, from `ROLE:1.00`: `flip(THEM(^ROLE)):1.00` (1/3-2/3) 2e-08 by `flip(THEM(^ROLE))`; `flip(THEM(^M)):1.00` (1/2-1/2) 2e-08 by `flip(THEM(^M))`; `M:1.00` (1/2-1/2) 1.1e-10 by `M`; `min(ROLE,max(X,X)):1.00` (mixed) 5.2e-13 by `min(ROLE,max(X,X))`
- N = 1000, from `flip(ROLE):1.00`: `flip(THEM(^ROLE)):1.00` (1/3-2/3) 2e-08 by `flip(THEM(^ROLE))`; `flip(THEM(^M)):1.00` (1/2-1/2) 2e-08 by `flip(THEM(^M))`; `M:1.00` (1/2-1/2) 1.1e-10 by `M`; `max(THEM(ME),H):1.00` (ineff) 3.1e-13 by `max(THEM(ME),H)`
- N = 1000, from `M:1.00`: `THEM(^M):1.00` (1/2-1/2) 2.8e-07 by `THEM(^M)`; `THEM(^ROLE):1.00` (1/3-2/3) 2.6e-07 by `THEM(^ROLE)`; `THEM(^flip(ROLE)):1.00` (1/3-2/3) 2e-08 by `THEM(^flip(ROLE))`; `flip(THEM(^ROLE)):1.00` (1/3-2/3) 2e-08 by `flip(THEM(^ROLE))`
- N = 10000, from `M:1.00`: `THEM(^M):1.00` (1/2-1/2) 2.8e-08 by `THEM(^M)`; `THEM(^ROLE):1.00` (1/3-2/3) 2.6e-08 by `THEM(^ROLE)`; `THEM(^flip(ROLE)):1.00` (1/3-2/3) 2e-09 by `THEM(^flip(ROLE))`; `flip(THEM(^ROLE)):1.00` (1/3-2/3) 2e-09 by `flip(THEM(^ROLE))`
- N = 10000, from `ROLE:1.00`: `flip(THEM(^ROLE)):1.00` (1/3-2/3) 2e-09 by `flip(THEM(^ROLE))`; `flip(THEM(^M)):1.00` (1/2-1/2) 2e-09 by `flip(THEM(^M))`; `max(THEM(THEM),ROLE):1.00` (ineff) 1.4e-62 by `max(THEM(THEM),ROLE)`; `max(THEM(ME),H):1.00` (ineff) 1.4e-62 by `max(THEM(ME),H)`
- N = 10000, from `H:0.33 + flip(THEM(^M)):0.67`: `max(THEM(ME),H):1.00` (ineff) 2.9e-08 by `max(THEM(ME),H)`; `max(THEM(THEM),H):1.00` (ineff) 2.9e-08 by `max(THEM(THEM),H)`; `ROLE:1.00` (1/3-2/3) 8.7e-23 by `ROLE`; `flip(ROLE):1.00` (1/3-2/3) 2.2e-23 by `flip(ROLE)`

### dollar3, norole (one population of N)

Encounter-level π-weighted outcome shares (per ordered split: slot 1 | slot 2 for fixed roles; the focal program first otherwise).

| N | 1/3\|2/3 | 1/2\|1/2 | 2/3\|1/3 | ineff | clash | P(efficient) | E[max share] | ex ante max | E[max norm. share \| compatible] | dwl | cut |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.0070 | 0.9545 | 0.0070 | 0.0209 | 0.0107 | 0.9685 | 0.495 | 0.492 | 0.503 | 0.0081 | 6.9e-07 |
| 1000 | 0.0053 | 0.9853 | 0.0053 | 0.0014 | 0.0026 | 0.9959 | 0.500 | 0.498 | 0.502 | 0.0016 | 5.3e-10 |
| 10000 | 0.3125 | 0.0000 | 0.3125 | 0.0625 | 0.3125 | 0.6251 | 0.438 | 0.333 | 0.652 | 0.1666 | 8.7e-19 |

Support (top states, π, label):

- N = 100: `M:1.00` 0.9478 (1/2-1/2); `L:0.50 + H:0.50` 0.0162 (mixed); `L:0.18 + X:0.82` 0.0136 (mixed); `X:1.00` 0.0077 (mixed); `min(M,X):1.00` 0.0059 (mixed); `L:1.00` 0.0022 (ineff) — polymorphic mass 0.0321, monomorphic-constant mass 0.9503, states 71, indeterminate 0
- N = 1000: `M:1.00` 0.9729 (1/2-1/2); `H:0.33 + flip(THEM(^M)):0.67` 0.0239 (mixed); `THEM(^M):1.00` 0.0018 (1/2-1/2); `max(THEM(THEM),H):1.00` 0.0007 (ineff); `max(THEM(ME),H):1.00` 0.0007 (ineff); `H:0.50 + flip(THEM(THEM)):0.50` 0.0000 (mixed) — polymorphic mass 0.0239, monomorphic-constant mass 0.9729, states 65, indeterminate 0
- N = 10000: `H:0.50 + flip(THEM(THEM)):0.25 + flip(THEM(^H)):0.25` 1.0000 (mixed); `M:1.00` 0.0000 (1/2-1/2); `H:0.33 + flip(THEM(^M)):0.67` 0.0000 (mixed); `max(THEM(THEM),H):1.00` 0.0000 (ineff); `max(THEM(ME),H):1.00` 0.0000 (ineff); `THEM(^M):1.00` 0.0000 (1/2-1/2) — polymorphic mass 1.0000, monomorphic-constant mass 0.0000, states 68, indeterminate 0

Transitions between state labels (largest fluxes; rate = flux / label mass, relative units within a row of N; "via" = share of the flux leaving from a state with a non-constant program, i.e. a shadow or conceder path):

- N = 100: mixed → 1/2-1/2 0.00498 (via 1.00); 1/2-1/2 → mixed 0.000177 (via 0.00); 1/2-1/2 → ineff 0.000107 (via 0.01); ineff → mixed 0.0183 (via 0.07); ineff → 1/2-1/2 0.0105 (via 0.34); clash → mixed 0.0264 (via 0.00); mixed → clash 0.000115 (via 1.00); mixed → ineff 0.000109 (via 1.00)
- N = 1000: 1/2-1/2 → mixed 3.73e-08 (via 0.96); mixed → 1/2-1/2 1.23e-06 (via 1.00); mixed → ineff 3.39e-07 (via 1.00); ineff → 1/2-1/2 4.91e-06 (via 1.00); ineff → mixed 7.78e-07 (via 0.91); 1/2-1/2 → ineff 1.1e-11 (via 1.00); mixed → clash 2.92e-21 (via 1.00); ineff → clash 1.8e-22 (via 1.00)
- N = 10000: mixed → ineff 5.85e-17 (via 1.00); ineff → mixed 1.33e-07 (via 1.00); mixed → 1/2-1/2 8.59e-18 (via 1.00); 1/2-1/2 → mixed 6.89e-23 (via 1.00); ineff → 1/2-1/2 6.7e-91 (via 1.00); 1/2-1/2 → ineff 8.13e-113 (via 0.00); mixed → clash 3.37e-151 (via 1.00); ineff → clash 4.93e-221 (via 1.00)

Top exits of the heaviest states (probability per mutation event; mutants):

- N = 100, from `M:1.00`: `X:1.00` (mixed) 0.00013 by `X`; `L:1.00` (ineff) 8.6e-05 by `L`; `min(M,X):1.00` (mixed) 3.1e-05 by `min(M,X)`; `THEM(THEM):1.00` (ineff) 7.1e-06 by `THEM(THEM)`
- N = 100, from `L:0.50 + H:0.50`: `M:1.00` (1/2-1/2) 0.0035 by `M`; `X:1.00` (mixed) 0.0019 by `X`; `min(M,X):1.00` (mixed) 9.3e-05 by `min(M,X)`; `L:0.33 + max(M,X):0.67` (mixed) 8.9e-05 by `max(M,X)`
- N = 100, from `L:0.18 + X:0.82`: `M:1.00` (1/2-1/2) 0.0059 by `M`; `L:0.50 + H:0.50` (mixed) 0.0034 by `H`; `min(M,X):1.00` (mixed) 0.00014 by `min(M,X)`; `L:0.33 + max(M,X):0.67` (mixed) 0.00012 by `max(M,X)`
- N = 1000, from `M:1.00`: `THEM(^M):1.00` (1/2-1/2) 4.4e-07 by `THEM(^M)`; `flip(THEM(^M)):1.00` (1/2-1/2) 3.6e-08 by `flip(THEM(^M))`; `min(M,max(X,X)):1.00` (mixed) 1.6e-09 by `min(M,max(X,X))`; `min(M,X):1.00` (mixed) 7.8e-12 by `min(M,X)`
- N = 1000, from `H:0.33 + flip(THEM(^M)):0.67`: `M:1.00` (1/2-1/2) 1.1e-06 by `M`; `max(THEM(ME),H):1.00` (ineff) 1.7e-07 by `max(THEM(ME),H)`; `max(THEM(THEM),H):1.00` (ineff) 1.7e-07 by `max(THEM(THEM),H)`; `THEM(^M):1.00` (1/2-1/2) 2e-09 by `THEM(^M)`
- N = 1000, from `THEM(^M):1.00`: `M:1.00` (1/2-1/2) 0.00024 by `M`; `flip(THEM(^M)):1.00` (1/2-1/2) 3.6e-08 by `flip(THEM(^M))`; `min(M,max(X,X)):1.00` (mixed) 8.7e-09 by `min(M,max(X,X))`; `min(M,X):1.00` (mixed) 6.4e-09 by `min(M,X)`
- N = 10000, from `H:0.50 + flip(THEM(THEM)):0.25 + flip(THEM(^H)):0.25`: `M:1.00` (1/2-1/2) 8.1e-18 by `M`; `THEM(^M):1.00` (1/2-1/2) 5.1e-19 by `THEM(^M)`; `H:0.33 + flip(THEM(^M)):0.67` (mixed) 6.1e-22 by `flip(THEM(^M))`; `THEM(THEM):1.00` (ineff) 1.9e-24 by `THEM(THEM)`
- N = 10000, from `M:1.00`: `THEM(^M):1.00` (1/2-1/2) 4.4e-08 by `THEM(^M)`; `flip(THEM(^M)):1.00` (1/2-1/2) 3.6e-09 by `flip(THEM(^M))`; `min(M,max(X,X)):1.00` (mixed) 3e-31 by `min(M,max(X,X))`; `max(M,min(X,X)):1.00` (mixed) 4.8e-75 by `max(M,min(X,X))`
- N = 10000, from `H:0.33 + flip(THEM(^M)):0.67`: `max(THEM(ME),H):1.00` (ineff) 5.3e-08 by `max(THEM(ME),H)`; `max(THEM(THEM),H):1.00` (ineff) 5.3e-08 by `max(THEM(THEM),H)`; `M:1.00` (1/2-1/2) 3.1e-33 by `M`; `THEM(^M):1.00` (1/2-1/2) 5.7e-36 by `THEM(^M)`

### dollar3, fixed (N per slot)

Encounter-level π-weighted outcome shares (per ordered split: slot 1 | slot 2 for fixed roles; the focal program first otherwise).

| N | 1/3\|2/3 | 1/2\|1/2 | 2/3\|1/3 | ineff | clash | P(efficient) | E[max share] | ex ante max | E[max norm. share \| compatible] | dwl | cut |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.3134 | 0.3615 | 0.3134 | 0.0105 | 0.0011 | 0.9884 | 0.604 | 0.604 | 0.605 | 0.0016 | 0.0e+00 |
| 1000 | 0.4972 | 0.0056 | 0.4972 | 0.0000 | 0.0000 | 1.0000 | 0.666 | 0.666 | 0.666 | 0.0000 | 1.1e-25 |
| 10000 | 0.4991 | 0.0019 | 0.4991 | 0.0000 | 0.0000 | 1.0000 | 0.666 | 0.666 | 0.666 | 0.0000 | 1.2e-28 |

Support (top states, π, label):

- N = 100: `M | M` 0.3393 (1/2|1/2); `L | H` 0.3086 (1/3|2/3); `H | L` 0.3086 (2/3|1/3); `M | THEM(ME)` 0.0030 (1/2|1/2); `THEM(ME) | M` 0.0030 (1/2|1/2); `M | THEM(THEM)` 0.0030 (1/2|1/2) — constant pairs 0.9613; slot 1 gets more 0.3208, slot 2 0.3208, equal 0.3584
- N = 1000: `L | H` 0.4931 (1/3|2/3); `H | L` 0.4931 (2/3|1/3); `M | M` 0.0053 (1/2|1/2); `H | flip(THEM(THEM))` 0.0016 (2/3|1/3); `flip(THEM(THEM)) | H` 0.0016 (1/3|2/3); `flip(THEM(ME)) | H` 0.0016 (1/3|2/3) — constant pairs 0.9915; slot 1 gets more 0.4972, slot 2 0.4972, equal 0.0056
- N = 10000: `L | H` 0.4950 (1/3|2/3); `H | L` 0.4950 (2/3|1/3); `M | M` 0.0018 (1/2|1/2); `flip(THEM(THEM)) | H` 0.0016 (1/3|2/3); `H | flip(THEM(THEM))` 0.0016 (2/3|1/3); `flip(THEM(ME)) | H` 0.0016 (1/3|2/3) — constant pairs 0.9917; slot 1 gets more 0.4991, slot 2 0.4991, equal 0.0019

Transitions between state labels (largest fluxes; rate = flux / label mass, relative units within a row of N; "via" = share of the flux leaving from a state with a non-constant program, i.e. a shadow or conceder path):

- N = 100: 1/2|1/2 → ineff 0.244 (via 0.05); ineff → 1/2|1/2 17 (via 0.01); mixed → 1/2|1/2 5.63 (via 1.00); 1/2|1/2 → mixed 0.167 (via 0.06); 1/3|2/3 → mixed 0.172 (via 0.01); 2/3|1/3 → mixed 0.172 (via 0.01); mixed → 1/3|2/3 3.51 (via 1.00); mixed → 2/3|1/3 3.51 (via 1.00)
- N = 1000: 2/3|1/3 → 1/3|2/3 0.114 (via 1.00); 1/3|2/3 → 2/3|1/3 0.114 (via 1.00); 1/2|1/2 → 2/3|1/3 5.11 (via 1.00); 1/2|1/2 → 1/3|2/3 5.11 (via 1.00); 1/3|2/3 → 1/2|1/2 0.0571 (via 1.00); 2/3|1/3 → 1/2|1/2 0.0571 (via 1.00); 2/3|1/3 → mixed 0.00133 (via 1.00); 1/3|2/3 → mixed 0.00133 (via 1.00)
- N = 10000: 1/3|2/3 → 2/3|1/3 0.116 (via 1.00); 2/3|1/3 → 1/3|2/3 0.116 (via 1.00); 1/2|1/2 → 2/3|1/3 15.7 (via 1.00); 1/2|1/2 → 1/3|2/3 15.7 (via 1.00); 1/3|2/3 → 1/2|1/2 0.0586 (via 1.00); 2/3|1/3 → 1/2|1/2 0.0586 (via 1.00); 1/3|2/3 → mixed 0.00142 (via 1.00); 2/3|1/3 → mixed 0.00142 (via 1.00)

Convention-to-convention moves (exact, from the generator): from each efficient constant pair, the next different efficient constant pair hit, the expected time to it, and the exact exit time from its label (mutation events).

| N | from | next convention hit | time to next | exit time from label | first label after exit |
|---|---|---|---|---|---|
| 100 | 1/3\|2/3 | 1/2\|1/2 0.78, 2/3\|1/3 0.22 | 2.31e+04 | 9.14e+03 | mixed 0.56, ineff 0.39, 2/3\|1/3 0.03, 1/2\|1/2 0.01 |
| 100 | 1/2\|1/2 | 1/3\|2/3 0.50, 2/3\|1/3 0.50 | 1.73e+04 | 6.53e+03 | ineff 0.56, mixed 0.39, 1/3\|2/3 0.03, 2/3\|1/3 0.03 |
| 100 | 2/3\|1/3 | 1/2\|1/2 0.78, 1/3\|2/3 0.22 | 2.31e+04 | 9.14e+03 | mixed 0.56, ineff 0.39, 1/3\|2/3 0.03, 1/2\|1/2 0.01 |
| 1000 | 1/3\|2/3 | 2/3\|1/3 0.99, 1/2\|1/2 0.01 | 2.13e+06 | 2.12e+06 | 2/3\|1/3 0.66, 1/2\|1/2 0.33, mixed 0.01, ineff 0.00 |
| 1000 | 1/2\|1/2 | 2/3\|1/3 0.50, 1/3\|2/3 0.50 | 1.05e+06 | 1e+06 | 1/3\|2/3 0.50, 2/3\|1/3 0.50, mixed 0.00, ineff 0.00 |
| 1000 | 2/3\|1/3 | 1/3\|2/3 0.99, 1/2\|1/2 0.01 | 2.13e+06 | 2.12e+06 | 1/3\|2/3 0.66, 1/2\|1/2 0.33, mixed 0.01, ineff 0.00 |
| 10000 | 1/3\|2/3 | 2/3\|1/3 0.99, 1/2\|1/2 0.01 | 2.12e+07 | 2.1e+07 | 2/3\|1/3 0.66, 1/2\|1/2 0.33, mixed 0.01, ineff 0.00 |
| 10000 | 1/2\|1/2 | 1/3\|2/3 0.50, 2/3\|1/3 0.50 | 7.4e+06 | 6.77e+06 | 2/3\|1/3 0.50, 1/3\|2/3 0.50, mixed 0.00, ineff 0.00 |
| 10000 | 2/3\|1/3 | 1/3\|2/3 0.99, 1/2\|1/2 0.01 | 2.12e+07 | 2.1e+07 | 1/3\|2/3 0.66, 1/2\|1/2 0.33, mixed 0.01, ineff 0.00 |

## Addendum: N scan (fixed), not a specified cell

- dollar5_N150: o:1/2|1/2 0.3114, o:1/3|2/3 0.2437, o:1/6|5/6 0.0998, o:2/3|1/3 0.2437, o:5/6|1/6 0.0998; P(efficient) 0.9984; E[max share] 0.648
- dollar5_N200: o:1/2|1/2 0.1557, o:1/3|2/3 0.1303, o:1/6|5/6 0.2917, o:2/3|1/3 0.1303, o:5/6|1/6 0.2917; P(efficient) 0.9996; E[max share] 0.738
- dollar5_N300: o:1/2|1/2 0.0103, o:1/3|2/3 0.0117, o:1/6|5/6 0.4831, o:2/3|1/3 0.0117, o:5/6|1/6 0.4831; P(efficient) 1.0000; E[max share] 0.826
- dollar5_N500: o:1/2|1/2 0.0036, o:1/3|2/3 0.0049, o:1/6|5/6 0.4933, o:2/3|1/3 0.0049, o:5/6|1/6 0.4933; P(efficient) 1.0000; E[max share] 0.830
- dollar5_N700: o:1/2|1/2 0.0031, o:1/3|2/3 0.0037, o:1/6|5/6 0.4947, o:2/3|1/3 0.0037, o:5/6|1/6 0.4947; P(efficient) 1.0000; E[max share] 0.831
- dollar3_N150: o:1/2|1/2 0.2158, o:1/3|2/3 0.3915, o:2/3|1/3 0.3915; P(efficient) 0.9987; E[max share] 0.630
- dollar3_N200: o:1/2|1/2 0.0578, o:1/3|2/3 0.4710, o:2/3|1/3 0.4710; P(efficient) 0.9998; E[max share] 0.657
- dollar3_N300: o:1/2|1/2 0.0140, o:1/3|2/3 0.4930, o:2/3|1/3 0.4930; P(efficient) 1.0000; E[max share] 0.664
- dollar3_N500: o:1/2|1/2 0.0090, o:1/3|2/3 0.4955, o:2/3|1/3 0.4955; P(efficient) 1.0000; E[max share] 0.665
- dollar3_N700: o:1/2|1/2 0.0071, o:1/3|2/3 0.4965, o:2/3|1/3 0.4965; P(efficient) 1.0000; E[max share] 0.665

## Addendum: N scan (onepop), not a specified cell

- dollar5_norole_N5000: 1/2-1/2 0.9161, 1/3-2/3 0.0035, 1/6-5/6 0.0340, clash 0.0418, ineff 0.0046, o:1/2|1/2 0.9161, o:1/3|2/3 0.0018, o:1/6|5/6 0.0170, o:2/3|1/3 0.0018, o:5/6|1/6 0.0170; P(efficient) 0.9536; E[max share] 0.490; top states `S3:1.00` 0.910; `S5:0.67 + flip(THEM(^S3)):0.33` 0.048; `S5:0.75 + flip(THEM(THEM)):0.08 + flip(THEM(^S4)):0.12 + flip(THEM(^S2)):0.04` 0.028
- dollar5_norole_N7000: 1/2-1/2 0.2219, 1/3-2/3 0.0299, 1/6-5/6 0.2922, clash 0.4483, ineff 0.0077, o:1/2|1/2 0.2219, o:1/3|2/3 0.0149, o:1/6|5/6 0.1461, o:2/3|1/3 0.0149, o:5/6|1/6 0.1461; P(efficient) 0.5440; E[max share] 0.376; top states `S5:0.75 + flip(THEM(THEM)):0.08 + flip(THEM(^S4)):0.12 + flip(THEM(^S2)):0.04` 0.614; `S3:1.00` 0.220; `S5:0.75 + flip(THEM(ME)):0.08 + flip(THEM(^S4)):0.12 + flip(THEM(^S2)):0.04` 0.153
- dollar5_role_N20000: 1/2-1/2 0.8310, 1/3-2/3 0.0575, 1/6-5/6 0.0849, clash 0.0216, ineff 0.0049, o:1/2|1/2 0.8310, o:1/3|2/3 0.0288, o:1/6|5/6 0.0425, o:2/3|1/3 0.0288, o:5/6|1/6 0.0425; P(efficient) 0.9735; E[max share] 0.525; top states `S3:1.00` 0.827; `max(S2,min(S4,ROLE)):1.00` 0.057; `ROLE:1.00` 0.050
- dollar5_role_N100000: 1/2-1/2 0.0000, 1/3-2/3 0.0382, 1/6-5/6 0.3750, clash 0.5781, ineff 0.0087, o:1/2|1/2 0.0000, o:1/3|2/3 0.0191, o:1/6|5/6 0.1875, o:2/3|1/3 0.0191, o:5/6|1/6 0.1875; P(efficient) 0.4132; E[max share] 0.340; top states `S5:0.75 + flip(THEM(THEM)):0.08 + flip(THEM(^S2)):0.04 + flip(THEM(^S4)):0.12` 0.926; `S5:0.75 + flip(THEM(ME)):0.08 + flip(THEM(^S2)):0.04 + flip(THEM(^S4)):0.12` 0.074; `THEM(^flip(ROLE)):1.00` 0.000
- dollar3_role_N30000: 1/2-1/2 0.8173, 1/3-2/3 0.1725, clash 0.0035, ineff 0.0067, o:1/2|1/2 0.8173, o:1/3|2/3 0.0863, o:2/3|1/3 0.0863; P(efficient) 0.9898; E[max share] 0.526; top states `M:1.00` 0.807; `ROLE:1.00` 0.122; `flip(ROLE):1.00` 0.029
- dollar3_norole_N3000: 1/2-1/2 0.9523, 1/3-2/3 0.0317, clash 0.0093, ineff 0.0067, o:1/2|1/2 0.9523, o:1/3|2/3 0.0159, o:2/3|1/3 0.0159; P(efficient) 0.9840; E[max share] 0.500; top states `M:1.00` 0.924; `H:0.33 + flip(THEM(^M)):0.67` 0.059; `H:0.50 + flip(THEM(THEM)):0.25 + flip(THEM(^H)):0.25` 0.008
- dollar3_norole_N5000: 1/2-1/2 0.2216, 1/3-2/3 0.4868, clash 0.2421, ineff 0.0496, o:1/2|1/2 0.2216, o:1/3|2/3 0.2434, o:2/3|1/3 0.2434; P(efficient) 0.7083; E[max share] 0.452; top states `H:0.50 + flip(THEM(THEM)):0.25 + flip(THEM(^H)):0.25` 0.771; `M:1.00` 0.216; `H:0.33 + flip(THEM(^M)):0.67` 0.011

## Validation of the fixed-role reduction (joint two-slot simulation, N = 50 per slot, ε = 10⁻³ per birth, 10 seeds × 20000000 generations)

| category | chain | simulation (± s.e. over seeds) |
|---|---|---|
| 1/6\|5/6 | 0.0439 | 0.0430 ± 0.0017 |
| 1/3\|2/3 | 0.2219 | 0.2045 ± 0.0035 |
| 1/2\|1/2 | 0.3417 | 0.3433 ± 0.0051 |
| 2/3\|1/3 | 0.2219 | 0.2150 ± 0.0043 |
| 5/6\|1/6 | 0.0439 | 0.0394 ± 0.0014 |
| ineff | 0.0992 | 0.1157 ± 0.0008 |
| clash | 0.0276 | 0.0391 ± 0.0005 |

Total variation 0.0296; slot-checks with the largest class below 0.9: 0.0385 (mean over seeds).

## Addendum: joint simulation in the endpoint regime (N = 300 per slot, ε = 10⁻⁴, 6 seeds × 30000000 generations from (S3 | S3); approach rates, not π)

Chain at N = 300: 1/6|5/6 0.4831, 1/3|2/3 0.0117, 1/2|1/2 0.0103, 2/3|1/3 0.0117, 5/6|1/6 0.4831, ineff 0.0000, clash 0.0000. Simulation (mean ± s.e. over seeds): 1/6|5/6 0.2581 ± 0.0990, 1/3|2/3 0.0001 ± 0.0000, 1/2|1/2 0.1611 ± 0.0634, 2/3|1/3 0.0542 ± 0.0342, 5/6|1/6 0.5241 ± 0.1688, ineff 0.0010 ± 0.0000, clash 0.0016 ± 0.0001.

Per-seed share of checks by dominant ordered label (>= 0.99): 1/6|5/6 0.60, 1/2|1/2 0.34, mixed 0.05 / 1/2|1/2 0.34, 1/6|5/6 0.29, 5/6|1/6 0.17 / 5/6|1/6 0.78, 1/6|5/6 0.12, mixed 0.06 / 5/6|1/6 0.92, mixed 0.06, 1/2|1/2 0.02 / 5/6|1/6 0.82, 1/2|1/2 0.06, 1/6|5/6 0.06 / 1/6|5/6 0.40, 5/6|1/6 0.28, 2/3|1/3 0.16.

## ε = 0 lotteries: dollar5

### Lottery dollar5 at (N, I) = (400, 16)

Island partition labels at the horizon (share of islands; mean over runs with run-level 95% t-intervals); fixed roles: ordered slot 1 | slot 2, with the unordered view.

**role, mN = 0** (40 runs): 1/2-1/2 0.634 [0.596, 0.672]; mixed 0.144 [0.114, 0.173]; 1/6-5/6 0.097 [0.073, 0.121]; clash 0.073 [0.053, 0.094]; ineff 0.052 [0.034, 0.070]
  Efficient islands 0.731 [0.696, 0.766]; encounter efficiency 0.785 [0.756, 0.814]; dwl 0.075 [0.064, 0.087]; E[max share] 0.469 [0.456, 0.483]; ex ante max 0.428 [0.417, 0.439]; conventions per run 1.82 [1.70, 1.95]; runs with ≥ 2 conventions 0.825 [0.680, 0.913]; closed 0.000 [0.000, 0.088]; censored 0.000 [0.000, 0.088]; partition-frozen in 9 runs (median generation 45300); escapes after it 0 (0 per island-generation); label losses 0 (0 per generation); island establishment median 130 generations (58 islands never locally closed); holders `S3` 0.63, `S4` 0.12, `S2` 0.09, `ROLE` 0.09, `X` 0.04.

**role, mN = 0.1** (40 runs): 1/2-1/2 0.939 [0.917, 0.961]; 1/6-5/6 0.056 [0.034, 0.078]; mixed 0.005 [0.000, 0.010]
  Efficient islands 0.989 [0.980, 0.998]; encounter efficiency 0.999 [0.999, 1.000]; dwl 0.000 [0.000, 0.000]; E[max share] 0.520 [0.512, 0.527]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.57 [1.41, 1.74]; runs with ≥ 2 conventions 0.575 [0.422, 0.715]; closed 0.400 [0.263, 0.554]; censored 0.600 [0.446, 0.737]; partition-frozen in 40 runs (median generation 3662); escapes after it 22 (5.4e-07 per island-generation); label losses 6 (2.4e-06 per generation); island establishment median 130 generations (0 islands never locally closed); holders `S3` 0.94, `ROLE` 0.05, `flip(ROLE)` 0.01.

**role, mN = 1** (40 runs): 1/2-1/2 0.994 [0.981, 1.000]; mixed 0.006 [0.000, 0.019]
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [-0.000, 0.000]; E[max share] 0.501 [0.499, 0.502]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 858); escapes after it 14 (2.2e-05 per island-generation); label losses 14 (0.00035 per generation); island establishment median 140 generations (0 islands never locally closed); holders `S3` 1.00, `flip(THEM(^ROLE))` 0.00.

**norole, mN = 0** (40 runs): 1/2-1/2 0.702 [0.670, 0.733]; mixed 0.147 [0.121, 0.173]; clash 0.092 [0.071, 0.113]; ineff 0.059 [0.036, 0.083]
  Efficient islands 0.702 [0.670, 0.733]; encounter efficiency 0.761 [0.735, 0.787]; dwl 0.085 [0.074, 0.095]; E[max share] 0.427 [0.416, 0.437]; ex ante max 0.419 [0.409, 0.430]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 0.000 [0.000, 0.088]; censored 0.000 [0.000, 0.088]; partition-frozen in 5 runs (median generation 63300); escapes after it 0 (0 per island-generation); label losses 0 (0 per generation); island establishment median 115 generations (65 islands never locally closed); holders `S3` 0.70, `S4` 0.13, `S2` 0.11, `X` 0.03, `S5` 0.01.

**norole, mN = 0.1** (40 runs): 1/2-1/2 1.000 [1.000, 1.000]
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [0.000, 0.000]; E[max share] 0.500 [0.500, 0.500]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 3288); escapes after it 1 (0.00018 per island-generation); label losses 0 (0 per generation); island establishment median 130 generations (0 islands never locally closed); holders `S3` 1.00.

**norole, mN = 1** (40 runs): 1/2-1/2 1.000 [1.000, 1.000]
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl -0.000 [-0.000, 0.000]; E[max share] 0.500 [0.500, 0.500]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 415); escapes after it 0 (- per island-generation); label losses 0 (- per generation); island establishment median 135 generations (0 islands never locally closed); holders `S3` 1.00, `flip(THEM(^S3))` 0.00.

**fixed, mN = 0** (40 runs): 1/2|1/2 0.539 [0.503, 0.575]; 1/3|2/3 0.217 [0.191, 0.244]; 2/3|1/3 0.209 [0.174, 0.245]; ineff 0.011 [0.003, 0.019]; 5/6|1/6 0.009 [0.002, 0.017]; 1/6|5/6 0.008 [0.001, 0.015]; mixed 0.006 [0.000, 0.012]
  unordered: 1/2-1/2 0.539 [0.503, 0.575]; 1/3-2/3 0.427 [0.394, 0.459]; 1/6-5/6 0.017 [0.006, 0.028]; ineff 0.011 [0.003, 0.019]; mixed 0.006 [0.000, 0.012]. Slot 1 gets more on 0.223 [0.186, 0.261] of islands, slot 2 on 0.237 [0.211, 0.264]; mean slot-1 minus slot-2 payoff -0.002 [-0.020, 0.017]; mean slot payoff 0.498 [0.497, 0.500].
  Efficient islands 0.983 [0.973, 0.993]; encounter efficiency 0.987 [0.979, 0.995]; dwl 0.002 [0.000, 0.003]; E[max share] 0.577 [0.570, 0.584]; ex ante max 0.577 [0.570, 0.584]; conventions per run 3.27 [3.10, 3.45]; runs with ≥ 2 conventions 1.000 [0.912, 1.000]; closed 0.000 [0.000, 0.088]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 230); escapes after it 0 (0 per island-generation); label losses 0 (0 per generation); island establishment median 125 generations (0 islands never locally closed); holders `S3 | S3` 0.52, `S2 | S4` 0.21, `S4 | S2` 0.21, `THEM(ME) | S3` 0.01, `S5 | S1` 0.01.

**fixed, mN = 0.1** (40 runs): 1/2|1/2 0.470 [0.397, 0.543]; 1/3|2/3 0.208 [0.157, 0.259]; 2/3|1/3 0.175 [0.134, 0.216]; 5/6|1/6 0.078 [0.000, 0.163]; 1/6|5/6 0.058 [0.000, 0.128]; mixed 0.011 [0.003, 0.019]
  unordered: 1/2-1/2 0.470 [0.397, 0.543]; 1/3-2/3 0.383 [0.317, 0.449]; 1/6-5/6 0.136 [0.030, 0.242]; mixed 0.011 [0.003, 0.019]. Slot 1 gets more on 0.292 [0.212, 0.372] of islands, slot 2 on 0.295 [0.222, 0.369]; mean slot-1 minus slot-2 payoff 0.005 [-0.075, 0.085]; mean slot payoff 0.499 [0.499, 0.500].
  Efficient islands 0.917 [0.891, 0.944]; encounter efficiency 0.997 [0.996, 0.998]; dwl 0.001 [0.000, 0.001]; E[max share] 0.609 [0.581, 0.638]; ex ante max 0.609 [0.581, 0.638]; conventions per run 2.85 [2.58, 3.12]; runs with ≥ 2 conventions 0.875 [0.739, 0.945]; closed 0.125 [0.055, 0.261]; censored 0.875 [0.739, 0.945]; partition-frozen in 38 runs (median generation 812); escapes after it 95 (1.9e-06 per island-generation); label losses 16 (5e-06 per generation); island establishment median 130 generations (0 islands never locally closed); holders `S3 | S3` 0.47, `S2 | S4` 0.18, `S4 | S2` 0.18, `S5 | flip(THEM(THEM))` 0.05, `flip(THEM(^S3)) | S5` 0.03.

**fixed, mN = 1** (40 runs): 1/2|1/2 0.523 [0.427, 0.620]; mixed 0.184 [0.136, 0.233]; 1/3|2/3 0.138 [0.066, 0.209]; 2/3|1/3 0.105 [0.035, 0.174]; 1/6|5/6 0.050 [0.000, 0.121]
  unordered: 1/2-1/2 0.523 [0.427, 0.620]; 1/3-2/3 0.242 [0.151, 0.333]; mixed 0.184 [0.136, 0.233]; 1/6-5/6 0.050 [0.000, 0.121]. Slot 1 gets more on 0.287 [0.203, 0.372] of islands, slot 2 on 0.459 [0.364, 0.554]; mean slot-1 minus slot-2 payoff -0.047 [-0.107, 0.012]; mean slot payoff 0.494 [0.493, 0.495].
  Efficient islands 0.470 [0.370, 0.571]; encounter efficiency 0.973 [0.967, 0.979]; dwl 0.006 [0.005, 0.007]; E[max share] 0.572 [0.548, 0.596]; ex ante max 0.572 [0.548, 0.596]; conventions per run 2.08 [1.82, 2.33]; runs with ≥ 2 conventions 0.725 [0.572, 0.839]; closed 0.150 [0.071, 0.291]; censored 0.850 [0.709, 0.929]; partition-frozen in 6 runs (median generation 2182); escapes after it 0 (- per island-generation); label losses 0 (- per generation); island establishment median 228 generations (0 islands never locally closed); holders `S3 | S3` 0.55, `S2 | S4` 0.16, `S4 | S2` 0.12, `S4 | flip(THEM(THEM))` 0.03, `flip(THEM(^S5)) | S5` 0.03.

### Lottery dollar5 at (N, I) = (100, 64)

Island partition labels at the horizon (share of islands; mean over runs with run-level 95% t-intervals); fixed roles: ordered slot 1 | slot 2, with the unordered view.

**role, mN = 0** (40 runs): 1/2-1/2 0.366 [0.345, 0.388]; clash 0.226 [0.210, 0.241]; 1/6-5/6 0.157 [0.144, 0.170]; ineff 0.136 [0.122, 0.151]; mixed 0.114 [0.103, 0.126]; 1/3-2/3 0.000 [0.000, 0.001]
  Efficient islands 0.523 [0.500, 0.547]; encounter efficiency 0.547 [0.524, 0.569]; dwl 0.166 [0.157, 0.175]; E[max share] 0.397 [0.386, 0.409]; ex ante max 0.334 [0.325, 0.343]; conventions per run 2.02 [1.97, 2.08]; runs with ≥ 2 conventions 1.000 [0.912, 1.000]; closed 0.000 [0.000, 0.088]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 482); escapes after it 0 (0 per island-generation); label losses 0 (0 per generation); island establishment median 65 generations (0 islands never locally closed); holders `S3` 0.37, `S4` 0.13, `ROLE` 0.13, `S2` 0.12, `X` 0.10.

**role, mN = 0.1** (40 runs): 1/2-1/2 1.000 [1.000, 1.000]
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [0.000, 0.000]; E[max share] 0.500 [0.500, 0.500]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 1635); escapes after it 312 (2.4e-05 per island-generation); label losses 40 (0.0002 per generation); island establishment median 70 generations (0 islands never locally closed); holders `S3` 1.00.

**role, mN = 1** (40 runs): 1/2-1/2 1.000 [0.999, 1.000]; mixed 0.000 [0.000, 0.001]
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [-0.000, 0.000]; E[max share] 0.500 [0.500, 0.500]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 382); escapes after it 3 (7e-05 per island-generation); label losses 3 (0.0045 per generation); island establishment median 120 generations (0 islands never locally closed); holders `S3` 1.00, `flip(THEM(^ROLE))` 0.00.

**norole, mN = 0** (40 runs): 1/2-1/2 0.452 [0.432, 0.472]; clash 0.242 [0.226, 0.257]; ineff 0.165 [0.151, 0.179]; mixed 0.141 [0.128, 0.154]
  Efficient islands 0.452 [0.432, 0.472]; encounter efficiency 0.482 [0.463, 0.500]; dwl 0.187 [0.179, 0.194]; E[max share] 0.325 [0.317, 0.332]; ex ante max 0.313 [0.306, 0.321]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 0.000 [0.000, 0.088]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 408); escapes after it 0 (0 per island-generation); label losses 0 (0 per generation); island establishment median 65 generations (0 islands never locally closed); holders `S3` 0.45, `S2` 0.16, `S4` 0.15, `X` 0.12, `S5` 0.09.

**norole, mN = 0.1** (40 runs): 1/2-1/2 1.000 [1.000, 1.000]
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [0.000, 0.000]; E[max share] 0.500 [0.500, 0.500]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 1018); escapes after it 104 (8e-05 per island-generation); label losses 0 (0 per generation); island establishment median 70 generations (0 islands never locally closed); holders `S3` 1.00, `THEM(^S3)` 0.00.

**norole, mN = 1** (40 runs): 1/2-1/2 1.000 [1.000, 1.000]
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [-0.000, 0.000]; E[max share] 0.500 [0.500, 0.500]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 292); escapes after it 0 (- per island-generation); label losses 0 (- per generation); island establishment median 105 generations (0 islands never locally closed); holders `S3` 1.00, `flip(THEM(^S3))` 0.00.

**fixed, mN = 0** (40 runs): 1/2|1/2 0.225 [0.210, 0.241]; ineff 0.180 [0.165, 0.196]; mixed 0.167 [0.153, 0.181]; 1/3|2/3 0.154 [0.138, 0.169]; 2/3|1/3 0.146 [0.133, 0.160]; 5/6|1/6 0.055 [0.045, 0.064]; 1/6|5/6 0.051 [0.042, 0.060]; clash 0.021 [0.016, 0.027]
  unordered: 1/3-2/3 0.300 [0.283, 0.317]; 1/2-1/2 0.225 [0.210, 0.241]; ineff 0.180 [0.165, 0.196]; mixed 0.167 [0.153, 0.181]; 1/6-5/6 0.106 [0.095, 0.116]; clash 0.021 [0.016, 0.027]. Slot 1 gets more on 0.362 [0.346, 0.379] of islands, slot 2 on 0.370 [0.347, 0.394]; mean slot-1 minus slot-2 payoff -0.003 [-0.018, 0.012]; mean slot payoff 0.432 [0.427, 0.436].
  Efficient islands 0.631 [0.611, 0.652]; encounter efficiency 0.673 [0.654, 0.691]; dwl 0.068 [0.064, 0.073]; E[max share] 0.554 [0.547, 0.561]; ex ante max 0.552 [0.545, 0.559]; conventions per run 4.95 [4.88, 5.02]; runs with ≥ 2 conventions 1.000 [0.912, 1.000]; closed 0.000 [0.000, 0.088]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 230); escapes after it 0 (0 per island-generation); label losses 0 (0 per generation); island establishment median 75 generations (0 islands never locally closed); holders `S3 | S3` 0.22, `S2 | S4` 0.15, `S4 | S2` 0.15, `S3 | S2` 0.05, `S5 | S1` 0.05.

**fixed, mN = 0.1** (40 runs): 1/2|1/2 0.766 [0.637, 0.895]; 5/6|1/6 0.099 [0.003, 0.196]; 1/6|5/6 0.075 [0.000, 0.160]; 1/3|2/3 0.029 [0.000, 0.064]; 2/3|1/3 0.024 [0.000, 0.057]; mixed 0.006 [0.001, 0.012]
  unordered: 1/2-1/2 0.766 [0.637, 0.895]; 1/6-5/6 0.174 [0.052, 0.297]; 1/3-2/3 0.054 [0.000, 0.109]; mixed 0.006 [0.001, 0.012]. Slot 1 gets more on 0.128 [0.027, 0.229] of islands, slot 2 on 0.110 [0.019, 0.201]; mean slot-1 minus slot-2 payoff 0.014 [-0.077, 0.105]; mean slot payoff 0.500 [0.499, 0.500].
  Efficient islands 0.977 [0.957, 0.998]; encounter efficiency 0.999 [0.997, 1.000]; dwl 0.000 [0.000, 0.001]; E[max share] 0.567 [0.527, 0.608]; ex ante max 0.567 [0.527, 0.608]; conventions per run 1.25 [1.06, 1.44]; runs with ≥ 2 conventions 0.175 [0.087, 0.320]; closed 0.825 [0.680, 0.913]; censored 0.175 [0.087, 0.320]; partition-frozen in 36 runs (median generation 53250); escapes after it 203 (4.9e-06 per island-generation); label losses 58 (8.9e-05 per generation); island establishment median 85 generations (0 islands never locally closed); holders `S3 | S3` 0.77, `S5 | flip(THEM(THEM))` 0.07, `flip(THEM(ME)) | S5` 0.05, `S2 | S4` 0.03, `S4 | S2` 0.03.

**fixed, mN = 1** (40 runs): 1/2|1/2 0.775 [0.640, 0.910]; 5/6|1/6 0.125 [0.018, 0.232]; 2/3|1/3 0.050 [0.000, 0.121]; 1/3|2/3 0.025 [0.000, 0.076]; 1/6|5/6 0.025 [0.000, 0.076]
  unordered: 1/2-1/2 0.775 [0.640, 0.910]; 1/6-5/6 0.150 [0.034, 0.266]; 1/3-2/3 0.075 [0.000, 0.160]. Slot 1 gets more on 0.175 [0.052, 0.298] of islands, slot 2 on 0.050 [-0.021, 0.121]; mean slot-1 minus slot-2 payoff 0.075 [-0.010, 0.160]; mean slot payoff 0.500 [0.500, 0.500].
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [0.000, 0.000]; E[max share] 0.562 [0.523, 0.602]; ex ante max 0.562 [0.523, 0.602]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 930); escapes after it 0 (- per island-generation); label losses 0 (- per generation); island establishment median 245 generations (0 islands never locally closed); holders `S3 | S3` 0.77, `S5 | flip(THEM(ME))` 0.05, `S4 | flip(THEM(THEM))` 0.05, `S5 | flip(THEM(THEM))` 0.05, `flip(THEM(^S1)) | S5` 0.03.

## ε = 0 lotteries: dollar3

### Lottery dollar3 at (N, I) = (100, 64)

Island partition labels at the horizon (share of islands; mean over runs with run-level 95% t-intervals); fixed roles: ordered slot 1 | slot 2, with the unordered view.

**role, mN = 0** (40 runs): 1/2-1/2 0.362 [0.342, 0.381]; 1/3-2/3 0.303 [0.286, 0.320]; mixed 0.173 [0.158, 0.189]; ineff 0.098 [0.085, 0.110]; clash 0.064 [0.052, 0.076]
  Efficient islands 0.665 [0.646, 0.684]; encounter efficiency 0.724 [0.707, 0.740]; dwl 0.083 [0.077, 0.089]; E[max share] 0.477 [0.471, 0.484]; ex ante max 0.417 [0.411, 0.423]; conventions per run 2.00 [2.00, 2.00]; runs with ≥ 2 conventions 1.000 [0.912, 1.000]; closed 0.000 [0.000, 0.088]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 415); escapes after it 0 (0 per island-generation); label losses 0 (0 per generation); island establishment median 65 generations (0 islands never locally closed); holders `M` 0.36, `ROLE` 0.25, `X` 0.15, `L` 0.09, `H` 0.06.

**role, mN = 0.1** (40 runs): 1/2-1/2 1.000 [1.000, 1.000]
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [0.000, 0.000]; E[max share] 0.500 [0.500, 0.500]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 5262); escapes after it 529 (2.6e-05 per island-generation); label losses 40 (0.00012 per generation); island establishment median 70 generations (0 islands never locally closed); holders `M` 1.00.

**norole, mN = 0** (40 runs): 1/2-1/2 0.519 [0.502, 0.535]; mixed 0.236 [0.221, 0.250]; ineff 0.139 [0.126, 0.152]; clash 0.107 [0.094, 0.120]
  Efficient islands 0.519 [0.502, 0.535]; encounter efficiency 0.599 [0.585, 0.613]; dwl 0.123 [0.117, 0.129]; E[max share] 0.390 [0.384, 0.396]; ex ante max 0.377 [0.371, 0.383]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 0.000 [0.000, 0.088]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 422); escapes after it 0 (0 per island-generation); label losses 0 (0 per generation); island establishment median 65 generations (0 islands never locally closed); holders `M` 0.52, `X` 0.21, `L` 0.13, `H` 0.11, `min(M,X)` 0.01.

**norole, mN = 0.1** (40 runs): 1/2-1/2 1.000 [1.000, 1.000]
  Efficient islands 1.000 [1.000, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [0.000, 0.000]; E[max share] 0.500 [0.500, 0.500]; ex ante max 0.500 [0.500, 0.500]; conventions per run 1.00 [1.00, 1.00]; runs with ≥ 2 conventions 0.000 [0.000, 0.088]; closed 1.000 [0.912, 1.000]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 1028); escapes after it 114 (5.7e-05 per island-generation); label losses 0 (0 per generation); island establishment median 75 generations (0 islands never locally closed); holders `M` 1.00, `THEM(^M)` 0.00.

**fixed, mN = 0** (40 runs): 1/2|1/2 0.302 [0.286, 0.318]; mixed 0.255 [0.234, 0.276]; 2/3|1/3 0.179 [0.168, 0.189]; 1/3|2/3 0.161 [0.145, 0.178]; ineff 0.102 [0.090, 0.113]; clash 0.002 [0.000, 0.004]
  unordered: 1/3-2/3 0.340 [0.320, 0.360]; 1/2-1/2 0.302 [0.286, 0.318]; mixed 0.255 [0.234, 0.276]; ineff 0.102 [0.090, 0.113]; clash 0.002 [0.000, 0.004]. Slot 1 gets more on 0.335 [0.321, 0.350] of islands, slot 2 on 0.319 [0.302, 0.336]; mean slot-1 minus slot-2 payoff 0.005 [-0.002, 0.012]; mean slot payoff 0.453 [0.449, 0.457].
  Efficient islands 0.642 [0.619, 0.664]; encounter efficiency 0.732 [0.715, 0.749]; dwl 0.047 [0.043, 0.051]; E[max share] 0.533 [0.527, 0.538]; ex ante max 0.530 [0.525, 0.536]; conventions per run 3.00 [3.00, 3.00]; runs with ≥ 2 conventions 1.000 [0.912, 1.000]; closed 0.000 [0.000, 0.088]; censored 0.000 [0.000, 0.088]; partition-frozen in 40 runs (median generation 210); escapes after it 1 (3.9e-09 per island-generation); label losses 0 (0 per generation); island establishment median 75 generations (0 islands never locally closed); holders `M | M` 0.29, `H | L` 0.18, `L | H` 0.16, `L | X` 0.05, `L | M` 0.05.

**fixed, mN = 0.1** (40 runs): 1/2|1/2 0.749 [0.609, 0.889]; 1/3|2/3 0.150 [0.035, 0.266]; 2/3|1/3 0.100 [0.003, 0.196]; mixed 0.001 [0.000, 0.002]
  unordered: 1/2-1/2 0.749 [0.609, 0.889]; 1/3-2/3 0.250 [0.110, 0.390]; mixed 0.001 [0.000, 0.002]. Slot 1 gets more on 0.100 [0.004, 0.197] of islands, slot 2 on 0.150 [0.035, 0.266]; mean slot-1 minus slot-2 payoff -0.017 [-0.070, 0.037]; mean slot payoff 0.500 [0.500, 0.500].
  Efficient islands 0.999 [0.997, 1.000]; encounter efficiency 1.000 [1.000, 1.000]; dwl 0.000 [-0.000, 0.000]; E[max share] 0.542 [0.518, 0.565]; ex ante max 0.542 [0.518, 0.565]; conventions per run 1.07 [0.99, 1.16]; runs with ≥ 2 conventions 0.075 [0.026, 0.199]; closed 0.900 [0.769, 0.960]; censored 0.100 [0.040, 0.231]; partition-frozen in 40 runs (median generation 42050); escapes after it 207 (3.8e-06 per island-generation); label losses 53 (6.2e-05 per generation); island establishment median 85 generations (0 islands never locally closed); holders `M | M` 0.75, `H | flip(THEM(THEM))` 0.07, `flip(THEM(THEM)) | H` 0.05, `flip(THEM(^H)) | H` 0.05, `H | flip(THEM(ME))` 0.02.

## Merges

### Merges (`role` arm, one population, 50–50 share s; fraction ending on 1/2–1/2, Wilson 95%)

| kind | N | s = 0.25 | s = 0.3 | s = 0.35 | s = 0.375 | s = 0.4 | s = 0.45 | s = 0.5 |
|---|---|---|---|---|---|---|---|---|
| pure | 100 | 0.29 [0.21, 0.39] | 0.26 [0.18, 0.35] | 0.49 [0.39, 0.59] | 0.54 [0.44, 0.63] | 0.54 [0.44, 0.63] | 0.53 [0.43, 0.62] | 0.76 [0.67, 0.83] |
| pure | 400 | 0.16 [0.10, 0.24] | 0.22 [0.15, 0.31] | 0.41 [0.32, 0.51] | 0.48 [0.38, 0.58] | 0.60 [0.50, 0.69] | 0.75 [0.66, 0.82] | 0.86 [0.78, 0.91] |
| sampled | 100 | 0.27 [0.19, 0.36] | 0.42 [0.33, 0.52] | 0.47 [0.38, 0.57] | 0.43 [0.34, 0.53] | 0.62 [0.52, 0.71] | 0.66 [0.56, 0.75] | 0.67 [0.57, 0.75] |
| sampled | 400 | 0.12 [0.07, 0.20] | 0.23 [0.16, 0.32] | 0.45 [0.36, 0.55] | 0.49 [0.39, 0.59] | 0.64 [0.54, 0.73] | 0.83 [0.74, 0.89] | 0.89 [0.81, 0.94] |
| exact (pure) | 100 | 0.25 | 0.34 | 0.43 | 0.49 | 0.52 | 0.62 | 0.70 |
| exact (pure) | 400 | 0.13 | 0.25 | 0.41 | 0.50 | 0.59 | 0.75 | 0.87 |

