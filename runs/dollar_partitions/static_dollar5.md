# Static tables: divide-the-dollar partitions (spec specs/2026-10-05-dollar-partitions.md)

Weak arm, n = 5 in every arm, w = 0.3.  Prior masses are in the cut unit (normalized over the classes of L_n).

## dollar5, arm norole: 2550 programs, 78 classes, divergent pairs 0.0003

Induced prior by kind: constant 0.8181 (5 classes), coin 0.1778 (34 classes), reader 0.0041 (39 classes)

Induced prior by self-play outcome: ineff 0.3352, clash 0.3324, mixed 0.1701, 1/2-1/2 0.1622

Deterministic replicator from 400 multinomial(100) seeds of the prior (one population; no drift; label at >= 0.95 of encounters): 1/2-1/2 0.993, mixed 0.007

Efficient monomorphic conventions by split: 1/2-1/2: 3 classes, mass 0.1622 (top `S3` 0.1620 constant, `THEM(^S3)` 0.0002 reader, `flip(THEM(^S3))` 0.0000 reader)

Pairwise contests (row q invades column a): u(q,a) / u(a,q), crossing frequency of q (q wins above it), Moran fixation of one q at N = 100 / 1,000 / 10,000 (w = 0.3; neutral 1/N).

| q | a | u(q,a) / u(a,q) | crossing of q | rho N=100 | rho N=1000 | rho N=10000 |
|---|---|---|---|---|---|---|
| `S3` | `THEM(^S3)` | 0.500 / 0.500 | - | 0.01 | 0.001 | 0.0001 |
| `THEM(^S3)` | `S3` | 0.500 / 0.500 | - | 0.01 | 0.001 | 0.0001 |

Exits of each convention by destination self-play outcome (mu * rho per mutation event): direct = a non-neutral mutant; via neutral = a neutral entrant (on-path identical shadow, mu/N) followed by a strict invader of the shadow (share of the shadow state's exits).

| convention | split | shadows (mass) | N | direct | via neutral |
|---|---|---|---|---|---|
| `S3` | 1/2-1/2 | 2 (0.000) | 100 | ineff 6e-05, mixed 3.3e-05, clash 6.5e-06 | clash 1.1e-07, ineff 2.7e-11 |
| `S3` | 1/2-1/2 | 2 (0.000) | 1000 | mixed 1.1e-11, ineff 1.5e-16, clash 1e-35 | clash 1.2e-08, ineff 2.7e-12 |
| `S3` | 1/2-1/2 | 2 (0.000) | 10000 | mixed 9.2e-51, ineff 2.9e-114, clash 0 | clash 1.2e-09, ineff 2.8e-13 |
| `THEM(^S3)` | 1/2-1/2 | 2 (0.162) | 100 | ineff 0.00029, mixed 8.7e-05, clash 6.4e-06 | clash 1.1e-07, ineff 2.7e-11 |
| `THEM(^S3)` | 1/2-1/2 | 2 (0.162) | 1000 | mixed 4.4e-10, ineff 1.3e-14, clash 1e-35 | clash 1.2e-08, ineff 2.7e-12 |
| `THEM(^S3)` | 1/2-1/2 | 2 (0.162) | 10000 | mixed 3.8e-30, ineff 8.1e-113, clash 0 | clash 1.2e-09, ineff 2.8e-13 |

## dollar5, arm fixed: 2550 programs, 78 classes, divergent pairs 0.0003

Induced prior by kind: constant 0.8181 (5 classes), coin 0.1778 (34 classes), reader 0.0041 (39 classes)

Induced prior by self-play outcome: ineff 0.3352, clash 0.3324, mixed 0.1701, 1/2-1/2 0.1622

Deterministic replicator from 400 multinomial(100) seeds of the prior (two-population; no drift; label at >= 0.95 of encounters): 1/2|1/2 0.917, 1/3|2/3 0.028, 2/3|1/3 0.025, 5/6|1/6 0.018, 1/6|5/6 0.013

Adjacent moves of each constant convention (slot 1 | slot 2), rates per mutation event (a slot drawn uniformly, then a mutant from its prior; constant-selection Moran fixation, N per slot). *direct*: one mutant fixes and changes the ordered split; *conceder*: a neutral entrant fixes, then the other slot's strict move (rate = neutral step x share of the strict move among all exits of the intermediate state). Entry = flux into the convention from the other constant conventions by these moves.

| convention | N | exit total | direct (to) | conceder (to) | entry from constant conventions | neutral entrant mass slot 1 / slot 2 |
|---|---|---|---|---|---|---|
| 1/6|5/6 `S1|S5` | 100 | 0.000213 | clash 0.00012, mixed 6.6e-05, ineff 2.9e-05 | 5/6|1/6 8.1e-07, 2/3|1/3 6.1e-07, 1/2|1/2 4.2e-07, 1/3|2/3 2.1e-07 | 5.08e-06 | 0.000 / 0.000 |
| 1/6|5/6 `S1|S5` | 1000 | 2.22e-07 | mixed 2.9e-18, clash 3.3e-24, ineff 8e-25 | 5/6|1/6 8.3e-08, 2/3|1/3 6.2e-08, 1/2|1/2 4.3e-08, 1/3|2/3 2.2e-08 | 5.81e-07 | 0.000 / 0.000 |
| 1/6|5/6 `S1|S5` | 10000 | 2.23e-08 | mixed 2.1e-118, clash 1.2e-219, ineff 3e-220 | 5/6|1/6 8.3e-09, 2/3|1/3 6.3e-09, 1/2|1/2 4.3e-09, 1/3|2/3 2.2e-09 | 6.9e-08 | 0.000 / 0.000 |
| 1/3|2/3 `S2|S4` | 100 | 8.25e-05 | ineff 5.8e-05, mixed 2e-05, clash 1.2e-06 | 1/6|5/6 1.8e-06, 5/6|1/6 1.1e-06, 2/3|1/3 7e-07, 1/2|1/2 3.6e-07 | 2.23e-06 | 0.000 / 0.000 |
| 1/3|2/3 `S2|S4` | 1000 | 4.45e-07 | mixed 4.8e-09, ineff 1.6e-24, clash 9.8e-46 | 1/6|5/6 2.2e-07, 5/6|1/6 1.1e-07, 2/3|1/3 7.3e-08, 1/2|1/2 3.7e-08 | 2.44e-07 | 0.000 / 0.000 |
| 1/3|2/3 `S2|S4` | 10000 | 4.45e-08 | mixed 5.1e-17, ineff 6e-220, clash 0 | 1/6|5/6 2.2e-08, 5/6|1/6 1.1e-08, 2/3|1/3 7.3e-09, 1/2|1/2 3.8e-09 | 3.23e-08 | 0.000 / 0.000 |
| 1/2|1/2 `S3|S3` | 100 | 7.12e-05 | ineff 5.8e-05, mixed 9.2e-06, clash 1.6e-08 | 1/6|5/6 1.4e-06, 5/6|1/6 1.4e-06, 1/3|2/3 7e-07, 2/3|1/3 7e-07 | 1.56e-06 | 0.004 / 0.004 |
| 1/2|1/2 `S3|S3` | 1000 | 5.25e-07 | mixed 1.1e-11, ineff 1.6e-24, clash 3.9e-67 | 5/6|1/6 1.7e-07, 1/6|5/6 1.7e-07, 2/3|1/3 8.6e-08, 1/3|2/3 8.6e-08 | 1.6e-07 | 0.004 / 0.004 |
| 1/2|1/2 `S3|S3` | 10000 | 9.26e-08 | mixed 9.2e-51, ineff 5.9e-220, clash 0 | 5/6|1/6 2.7e-08, 1/6|5/6 2.7e-08, 1/3|2/3 1.6e-08, 2/3|1/3 1.6e-08 | 1.61e-08 | 0.004 / 0.004 |
| 2/3|1/3 `S4|S2` | 100 | 8.25e-05 | ineff 5.8e-05, mixed 2e-05, clash 1.2e-06 | 5/6|1/6 1.8e-06, 1/6|5/6 1.1e-06, 1/3|2/3 7e-07, 1/2|1/2 3.6e-07 | 2.23e-06 | 0.000 / 0.000 |
| 2/3|1/3 `S4|S2` | 1000 | 4.45e-07 | mixed 4.8e-09, ineff 1.6e-24, clash 9.8e-46 | 5/6|1/6 2.2e-07, 1/6|5/6 1.1e-07, 1/3|2/3 7.3e-08, 1/2|1/2 3.7e-08 | 2.44e-07 | 0.000 / 0.000 |
| 2/3|1/3 `S4|S2` | 10000 | 4.45e-08 | mixed 5.1e-17, ineff 6e-220, clash 0 | 5/6|1/6 2.2e-08, 1/6|5/6 1.1e-08, 1/3|2/3 7.3e-09, 1/2|1/2 3.8e-09 | 3.23e-08 | 0.000 / 0.000 |
| 5/6|1/6 `S5|S1` | 100 | 0.000213 | clash 0.00012, mixed 6.6e-05, ineff 2.9e-05 | 1/6|5/6 8.1e-07, 1/3|2/3 6.1e-07, 1/2|1/2 4.2e-07, 2/3|1/3 2.1e-07 | 5.08e-06 | 0.000 / 0.000 |
| 5/6|1/6 `S5|S1` | 1000 | 2.22e-07 | mixed 2.9e-18, clash 3.3e-24, ineff 8e-25 | 1/6|5/6 8.3e-08, 1/3|2/3 6.2e-08, 1/2|1/2 4.3e-08, 2/3|1/3 2.2e-08 | 5.81e-07 | 0.000 / 0.000 |
| 5/6|1/6 `S5|S1` | 10000 | 2.23e-08 | mixed 2.1e-118, clash 1.2e-219, ineff 3e-220 | 1/6|5/6 8.3e-09, 1/3|2/3 6.3e-09, 1/2|1/2 4.3e-09, 2/3|1/3 2.2e-09 | 6.9e-08 | 0.000 / 0.000 |

