# Static tables: divide-the-dollar partitions (spec specs/2026-10-05-dollar-partitions.md)

Weak arm, n = 5 in every arm, w = 0.3.  Prior masses are in the cut unit (normalized over the classes of L_n).

## dollar3, arm role: 1586 programs, 80 classes, divergent pairs 0.0005

Induced prior by kind: constant 0.5870 (3 classes), coin 0.2101 (33 classes), role-split 0.1974 (6 classes), reader 0.0055 (38 classes)

Induced prior by self-play outcome: mixed 0.2099, ineff 0.2092, clash 0.2054, 1/2-1/2 0.1883, 1/3-2/3 0.1872

Deterministic replicator from 400 multinomial(100) seeds of the prior (one population; no drift; label at >= 0.95 of encounters): 1/2-1/2 0.875, 1/3-2/3 0.120, mixed 0.005

Efficient monomorphic conventions by split: 1/2-1/2: 3 classes, mass 0.1883 (top `M` 0.1880 constant, `THEM(^M)` 0.0003 reader, `flip(THEM(^M))` 0.0000 reader); 1/3-2/3: 5 classes, mass 0.1872 (top `ROLE` 0.1496 role-split, `flip(ROLE)` 0.0373 role-split, `THEM(^ROLE)` 0.0003 reader)

Pairwise contests (row q invades column a): u(q,a) / u(a,q), crossing frequency of q (q wins above it), Moran fixation of one q at N = 100 / 1,000 / 10,000 (w = 0.3; neutral 1/N).

| q | a | u(q,a) / u(a,q) | crossing of q | rho N=100 | rho N=1000 | rho N=10000 |
|---|---|---|---|---|---|---|
| `M` | `THEM(^M)` | 0.500 / 0.500 | - | 0.01 | 0.001 | 0.0001 |
| `M` | `ROLE` | 0.250 / 0.167 | 0.429 | 0.00359 | 5.65e-10 | 2.72e-73 |
| `M` | `flip(ROLE)` | 0.250 / 0.167 | 0.429 | 0.00359 | 5.65e-10 | 2.72e-73 |
| `THEM(^M)` | `M` | 0.500 / 0.500 | - | 0.01 | 0.001 | 0.0001 |
| `THEM(^M)` | `ROLE` | 0.167 / 0.167 | 0.500 | 0.00155 | 8.04e-14 | 4.88e-112 |
| `THEM(^M)` | `flip(ROLE)` | 0.167 / 0.167 | 0.500 | 0.00155 | 8.04e-14 | 4.88e-112 |
| `ROLE` | `M` | 0.167 / 0.250 | 0.571 | 0.00103 | 2.11e-15 | 1.4e-127 |
| `ROLE` | `THEM(^M)` | 0.167 / 0.167 | 0.500 | 0.00155 | 8.04e-14 | 4.88e-112 |
| `ROLE` | `flip(ROLE)` | 0.167 / 0.167 | 0.500 | 0.00155 | 8.04e-14 | 4.88e-112 |
| `flip(ROLE)` | `M` | 0.167 / 0.250 | 0.571 | 0.00103 | 2.11e-15 | 1.4e-127 |
| `flip(ROLE)` | `THEM(^M)` | 0.167 / 0.167 | 0.500 | 0.00155 | 8.04e-14 | 4.88e-112 |
| `flip(ROLE)` | `ROLE` | 0.167 / 0.167 | 0.500 | 0.00155 | 8.04e-14 | 4.88e-112 |

Exits of each convention by destination self-play outcome (mu * rho per mutation event): direct = a non-neutral mutant; via neutral = a neutral entrant (on-path identical shadow, mu/N) followed by a strict invader of the shadow (share of the shadow state's exits).

| convention | split | shadows (mass) | N | direct | via neutral |
|---|---|---|---|---|---|
| `M` | 1/2-1/2 | 5 (0.001) | 100 | 1/3-2/3 0.00019, mixed 0.00014, ineff 9.5e-05, clash 4.1e-06 | clash 9.7e-08, ineff 2e-10, mixed 2.3e-11 |
| `M` | 1/2-1/2 | 5 (0.001) | 1000 | mixed 1e-09, ineff 4.6e-15, 1/3-2/3 3.9e-16, clash 7.4e-36 | ineff 3.1e-10, clash 3.2e-17, mixed 8.6e-24 |
| `M` | 1/2-1/2 | 5 (0.001) | 10000 | mixed 1.7e-31, ineff 8.8e-113, 1/3-2/3 2.6e-128, clash 0 | ineff 2.9e-10, clash 5.9e-115, mixed 1.8e-150 |
| `THEM(^M)` | 1/2-1/2 | 2 (0.188) | 100 | ineff 0.00035, 1/3-2/3 0.00029, mixed 0.00023, clash 4.1e-06 | clash 4.8e-08, ineff 8.3e-11, mixed 1.1e-11 |
| `THEM(^M)` | 1/2-1/2 | 2 (0.188) | 1000 | mixed 1.2e-08, ineff 8e-11, 1/3-2/3 1.5e-14, clash 7.3e-36 | ineff 1.3e-10, clash 1.6e-17, mixed 4.3e-24 |
| `THEM(^M)` | 1/2-1/2 | 2 (0.188) | 10000 | mixed 2.1e-20, ineff 3.5e-60, 1/3-2/3 9.1e-113, clash 0 | ineff 1.2e-10, clash 3e-115, mixed 8.9e-151 |
| `ROLE` | 1/3-2/3 | 2 (0.000) | 100 | 1/2-1/2 0.00068, mixed 0.00028, ineff 8.5e-05, clash 7.7e-05 | clash 9.7e-08, ineff 2e-10, mixed 2.3e-11 |
| `ROLE` | 1/3-2/3 | 2 (0.000) | 1000 | 1/2-1/2 1.1e-10, ineff 1.2e-12, mixed 9.1e-13, 1/3-2/3 3e-15 | ineff 3.1e-10, clash 3.2e-17, mixed 8.6e-24 |
| `ROLE` | 1/3-2/3 | 2 (0.000) | 10000 | ineff 5.5e-62, mixed 2.7e-67, 1/2-1/2 5.1e-74, 1/3-2/3 1.8e-113 | ineff 2.9e-10, clash 5.9e-115, mixed 1.8e-150 |
| `flip(ROLE)` | 1/3-2/3 | 2 (0.000) | 100 | 1/2-1/2 0.00068, mixed 0.00027, 1/3-2/3 0.00023, ineff 8.1e-05 | clash 9.7e-08, ineff 2e-10, mixed 2.3e-11 |
| `flip(ROLE)` | 1/3-2/3 | 2 (0.000) | 1000 | 1/2-1/2 1.1e-10, ineff 6.2e-13, mixed 1.4e-13, 1/3-2/3 1.2e-14 | ineff 3.1e-10, clash 3.2e-17, mixed 8.6e-24 |
| `flip(ROLE)` | 1/3-2/3 | 2 (0.000) | 10000 | ineff 2.7e-62, 1/2-1/2 5.1e-74, mixed 1e-80, 1/3-2/3 7.3e-113 | ineff 2.9e-10, clash 5.9e-115, mixed 1.8e-150 |

## dollar3, arm norole: 902 programs, 45 classes, divergent pairs 0.0012

Induced prior by kind: constant 0.7359 (3 classes), coin 0.2563 (15 classes), reader 0.0078 (27 classes)

Induced prior by self-play outcome: mixed 0.2568, ineff 0.2544, clash 0.2486, 1/2-1/2 0.2402

Deterministic replicator from 400 multinomial(100) seeds of the prior (one population; no drift; label at >= 0.95 of encounters): 1/2-1/2 1.000

Efficient monomorphic conventions by split: 1/2-1/2: 3 classes, mass 0.2402 (top `M` 0.2397 constant, `THEM(^M)` 0.0004 reader, `flip(THEM(^M))` 0.0000 reader)

Pairwise contests (row q invades column a): u(q,a) / u(a,q), crossing frequency of q (q wins above it), Moran fixation of one q at N = 100 / 1,000 / 10,000 (w = 0.3; neutral 1/N).

| q | a | u(q,a) / u(a,q) | crossing of q | rho N=100 | rho N=1000 | rho N=10000 |
|---|---|---|---|---|---|---|
| `M` | `THEM(^M)` | 0.500 / 0.500 | - | 0.01 | 0.001 | 0.0001 |
| `THEM(^M)` | `M` | 0.500 / 0.500 | - | 0.01 | 0.001 | 0.0001 |

Exits of each convention by destination self-play outcome (mu * rho per mutation event): direct = a non-neutral mutant; via neutral = a neutral entrant (on-path identical shadow, mu/N) followed by a strict invader of the shadow (share of the shadow state's exits).

| convention | split | shadows (mass) | N | direct | via neutral |
|---|---|---|---|---|---|
| `M` | 1/2-1/2 | 2 (0.000) | 100 | mixed 0.00018, ineff 0.00011, clash 4.8e-06 | clash 1.3e-07, ineff 2.4e-10 |
| `M` | 1/2-1/2 | 2 (0.000) | 1000 | mixed 1.6e-09, ineff 4.1e-15, clash 7.7e-36 | ineff 5.2e-10, clash 5.6e-17 |
| `M` | 1/2-1/2 | 2 (0.000) | 10000 | mixed 3e-31, ineff 8.1e-113, clash 0 | ineff 4.7e-10, clash 9.7e-115 |
| `THEM(^M)` | 1/2-1/2 | 2 (0.240) | 100 | ineff 0.00041, mixed 0.00029, clash 4.8e-06 | clash 1.3e-07, ineff 2.4e-10 |
| `THEM(^M)` | 1/2-1/2 | 2 (0.240) | 1000 | mixed 1.5e-08, ineff 2.4e-14, clash 7.5e-36 | ineff 5.2e-10, clash 5.6e-17 |
| `THEM(^M)` | 1/2-1/2 | 2 (0.240) | 10000 | mixed 3.8e-20, ineff 2e-112, clash 0 | ineff 4.7e-10, clash 9.7e-115 |

## dollar3, arm fixed: 902 programs, 45 classes, divergent pairs 0.0012

Induced prior by kind: constant 0.7359 (3 classes), coin 0.2563 (15 classes), reader 0.0078 (27 classes)

Induced prior by self-play outcome: mixed 0.2568, ineff 0.2544, clash 0.2486, 1/2-1/2 0.2402

Deterministic replicator from 400 multinomial(100) seeds of the prior (two-population; no drift; label at >= 0.95 of encounters): 1/2|1/2 1.000

Adjacent moves of each constant convention (slot 1 | slot 2), rates per mutation event (a slot drawn uniformly, then a mutant from its prior; constant-selection Moran fixation, N per slot). *direct*: one mutant fixes and changes the ordered split; *conceder*: a neutral entrant fixes, then the other slot's strict move (rate = neutral step x share of the strict move among all exits of the intermediate state). Entry = flux into the convention from the other constant conventions by these moves.

| convention | N | exit total | direct (to) | conceder (to) | entry from constant conventions | neutral entrant mass slot 1 / slot 2 |
|---|---|---|---|---|---|---|
| 1/3|2/3 `L|H` | 100 | 0.000109 | mixed 6.1e-05, ineff 4.3e-05, clash 1.2e-06 | 2/3|1/3 2.8e-06, 1/2|1/2 1.4e-06, mixed 3.6e-08, ineff 1.2e-10 | 6.74e-06 | 0.001 / 0.001 |
| 1/3|2/3 `L|H` | 1000 | 4.72e-07 | mixed 3.6e-14, ineff 1.2e-24, clash 9.8e-46 | 2/3|1/3 3.1e-07, 1/2|1/2 1.6e-07, mixed 3.5e-09, ineff 1.3e-11 | 8.23e-07 | 0.001 / 0.001 |
| 1/3|2/3 `L|H` | 10000 | 4.76e-08 | mixed 2.5e-79, ineff 4.4e-220, clash 0 | 2/3|1/3 3.2e-08, 1/2|1/2 1.6e-08, mixed 3.8e-10, ineff 1.4e-12 | 1.07e-07 | 0.001 / 0.001 |
| 1/2|1/2 `M|M` | 100 | 0.000153 | ineff 8.6e-05, mixed 5.9e-05, clash 1.2e-08 | 2/3|1/3 3.9e-06, 1/3|2/3 3.9e-06 | 2.82e-06 | 0.007 / 0.007 |
| 1/2|1/2 `M|M` | 1000 | 1.02e-06 | mixed 1.6e-09, ineff 2.5e-24, clash 2.9e-67 | 1/3|2/3 5.1e-07, 2/3|1/3 5.1e-07 | 3.11e-07 | 0.007 / 0.007 |
| 1/2|1/2 `M|M` | 10000 | 1.51e-07 | mixed 3e-31, ineff 9.1e-220, clash 0 | 1/3|2/3 7.5e-08, 2/3|1/3 7.5e-08 | 3.13e-08 | 0.007 / 0.007 |
| 2/3|1/3 `H|L` | 100 | 0.000109 | mixed 6.1e-05, ineff 4.3e-05, clash 1.2e-06 | 1/3|2/3 2.8e-06, 1/2|1/2 1.4e-06, mixed 3.6e-08, ineff 1.2e-10 | 6.74e-06 | 0.001 / 0.001 |
| 2/3|1/3 `H|L` | 1000 | 4.72e-07 | mixed 3.6e-14, ineff 1.2e-24, clash 9.8e-46 | 1/3|2/3 3.1e-07, 1/2|1/2 1.6e-07, mixed 3.5e-09, ineff 1.3e-11 | 8.23e-07 | 0.001 / 0.001 |
| 2/3|1/3 `H|L` | 10000 | 4.76e-08 | mixed 2.5e-79, ineff 4.4e-220, clash 0 | 1/3|2/3 3.2e-08, 1/2|1/2 1.6e-08, mixed 3.8e-10, ineff 1.4e-12 | 1.07e-07 | 0.001 / 0.001 |

