# Fixed-role chicken and hawk–dove without `ROLE` (spec `specs/2026-10-11-fixed-role-chicken.md`; notes `notes/fixed-role-chicken.md`; predictions `predictions/2026-10-11-fixed-role-chicken.md`)

Actions Straight (hawk) = A_0, Swerve (dove) = A_1. Games: `chicken` (St/St −10, St/Sw 2, Sw/St −1, Sw/Sw 0), `hd3` (V = 2, C = 3: −½, 2, 0, 1), `hd6` (C = 6: −2, 2, 0, 1). Exponential fitness map w = 0.3. Outcome classes by play with tolerance 0.95 (notes §1.6): R1 = role 1 wins (role 1 Straight, role 2 Swerve), R2 = role 2 wins, crash, dove (mutual swerve/dove), mixed. **The ε→0 chain (rare mutation) and the lottery (ε = 0, mutation-free absorption) are separate objects and are never pooled; the lottery panel is finite-size evidence.** In the modal arm the constants are named `D` (= Straight) and `C` (= Swerve); `BOX` reads "provably swerves", `BOXD` "provably goes straight".

## Static: catalogues and program-space closure

| arm | programs | classes | Straight / Swerve mass | bridges (classes, mass) | matchers (classes, mass) | X-mixtures | winner-seat neutral mass |
|---|---|---|---|---|---|---|---|
| weak | 1852 | 46 | 0.329 / 0.329 | 5, 0.00185 | 7, 0.0101 | 0.330 | 0.331 |
| modal | 1020 | 51 | 0.469 / 0.469 | 28, 0.03102 | 21, 0.0310 | 0.000 | 0.500 |
| W0 | 666 | 12 | 0.489 / 0.489 | 4, 0.00396 | 4, 0.0187 | 0.000 | 0.493 |
| M0 | 666 | 8 | 0.489 / 0.489 | 3, 0.00396 | 3, 0.0187 | 0.000 | 0.493 |
| const | 2 | 2 | 0.500 / 0.500 | 0, 0.00000 | 0, 0.0000 | 0.000 | 0.500 |

(Firm and swerver masses include the soft commitments that play like constants against constants, e.g. weak `and(THEM(ME),Straight)`.) Payoff classes equal play classes in every arm and game: True.

**Closed classes of the Δ ≥ 0 graph on the K² monomorphic pairs** (Lemma F; a closed class with one convention would be a drift-closed convention), and the shortest escape from (Straight | Swerve):

| arm | game | closed classes | labels in the closed class(es) | escape path from (Straight \| Swerve) |
|---|---|---|---|---|
| weak | chicken | 1 | {R1, R2, dove, mixed} | `Straight | Swerve` → `not(THEM(ME)) | Swerve` (neutral) → `not(THEM(ME)) | Straight` (strict) |
| weak | hd3 | 1 | {R1, R2, dove, mixed} | `Straight | Swerve` → `not(THEM(ME)) | Swerve` (neutral) → `not(THEM(ME)) | Straight` (strict) |
| weak | hd6 | 1 | {R1, R2, dove, mixed} | `Straight | Swerve` → `not(THEM(ME)) | Swerve` (neutral) → `not(THEM(ME)) | Straight` (strict) |
| modal | chicken | 1 | {R1, R2, dove} | `Straight | Swerve` → `BOXD(THEM(ME)) | Swerve` (neutral) → `BOXD(THEM(ME)) | Straight` (strict) |
| modal | hd3 | 1 | {R1, R2, dove} | `Straight | Swerve` → `BOXD(THEM(ME)) | Swerve` (neutral) → `BOXD(THEM(ME)) | Straight` (strict) |
| modal | hd6 | 1 | {R1, R2, dove} | `Straight | Swerve` → `BOXD(THEM(ME)) | Swerve` (neutral) → `BOXD(THEM(ME)) | Straight` (strict) |
| W0 | chicken | 1 | {R1, R2, dove} | `Straight | Swerve` → `not(THEM(ME)) | Swerve` (neutral) → `not(THEM(ME)) | Straight` (strict) |
| W0 | hd3 | 1 | {R1, R2, dove} | `Straight | Swerve` → `not(THEM(ME)) | Swerve` (neutral) → `not(THEM(ME)) | Straight` (strict) |
| W0 | hd6 | 1 | {R1, R2, dove} | `Straight | Swerve` → `not(THEM(ME)) | Swerve` (neutral) → `not(THEM(ME)) | Straight` (strict) |
| M0 | chicken | 1 | {R1, R2, dove} | `Straight | Swerve` → `not(BOX(THEM(ME))) | Swerve` (neutral) → `not(BOX(THEM(ME))) | Straight` (strict) |
| M0 | hd3 | 1 | {R1, R2, dove} | `Straight | Swerve` → `not(BOX(THEM(ME))) | Swerve` (neutral) → `not(BOX(THEM(ME))) | Straight` (strict) |
| M0 | hd6 | 1 | {R1, R2, dove} | `Straight | Swerve` → `not(BOX(THEM(ME))) | Swerve` (neutral) → `not(BOX(THEM(ME))) | Straight` (strict) |
| const | chicken | 2 | {R2}; {R1} | none (no Δ ≥ 0 path) |
| const | hd3 | 2 | {R2}; {R1} | none (no Δ ≥ 0 path) |
| const | hd6 | 2 | {R2}; {R1} | none (no Δ ≥ 0 path) |

Matched pair: the W0 and M0 play matrices differ in 2000 of 443556 program pairs (0.45%), all between self-referential readers: matcher vs bridge 772, bridge vs matcher 340, matcher vs firm 176, firm vs matcher 176, bridge vs swerver 160, firm vs bridge 160, bridge vs bridge 88, firm vs firm 64, firm vs swerver 64.

**Bridges** (conditional straights: swerve against Straight, straight against Swerve) and their self-play:

- weak: `not(THEM(ME))` (0.00080), `not(THEM(THEM))` (0.00080), `not(THEM(^Straight))` (0.00009), `not(THEM(^Swerve))` (0.00009), `not(THEM(^X))` (0.00009); self-play {'dove': 3, 'crash': 1, 'mixed': 1}.
- W0: `not(THEM(ME))` (0.00174), `not(THEM(THEM))` (0.00174), `not(THEM(^Straight))` (0.00024), `not(THEM(^Swerve))` (0.00024); self-play {'dove': 3, 'crash': 1}.
- M0: `not(BOX(THEM(ME)))` (0.00198), `not(BOX(THEM(THEM)))` (0.00174), `not(BOX(THEM(^C)))` (0.00024); self-play {'dove': 3}.
- modal: `BOXD(THEM(ME))` (0.00493), `BOXD1(THEM(ME))` (0.00493), `BOXD(THEM(THEM))` (0.00490), `BOXD1(THEM(THEM))` (0.00490), `BOXD(THEM(^C))` (0.00138), `BOXD(THEM(^D))` (0.00138), `BOXD1(THEM(^C))` (0.00138), `BOXD1(THEM(^D))` (0.00138) and 20 more; self-play {'crash': 20, 'dove': 8}.

Weak bridge–bridge table (row in role 1 against column in role 2; S[row, col] / S[col, row], 1 = swerve) and the outcome class:

| role 1 \ role 2 | `not(THEM(ME))` | `not(THEM(THEM))` | `not(THEM(^Straight))` | `not(THEM(^Swerve))` | `not(THEM(^X))` |
|---|---|---|---|---|---|
| `not(THEM(ME))` | 1.00/1.00 dove | 1.00/1.00 dove | 1.00/0.00 R2 | 0.00/1.00 R1 | 0.50/0.50 mixed |
| `not(THEM(THEM))` | 1.00/1.00 dove | 1.00/1.00 dove | 1.00/0.00 R2 | 0.00/1.00 R1 | 0.50/0.50 mixed |
| `not(THEM(^Straight))` | 0.00/1.00 R1 | 0.00/1.00 R1 | 0.00/0.00 crash | 0.00/1.00 R1 | 0.00/0.50 mixed |
| `not(THEM(^Swerve))` | 1.00/0.00 R2 | 1.00/0.00 R2 | 1.00/0.00 R2 | 1.00/1.00 dove | 1.00/0.50 mixed |
| `not(THEM(^X))` | 0.50/0.50 mixed | 0.50/0.50 mixed | 0.50/0.00 mixed | 0.50/1.00 mixed | 0.50/0.50 mixed |

Bridge–resident (every bridge, every arm, both roles): against the loser's Swerve it plays Straight (neutral in the winner's seat); against the winner's Straight it plays Swerve (neutral in the loser's seat); with a bridge in the winner's seat the loser's Straight gains T − S (3 in chicken, 2 in hawk–dove).

## The ε→0 chain, two populations (exact K² monomorphic chain; rare mutation)

N per population. π by outcome class; N·exit = N × (flux out of R1 per unit R1 mass, per mutation event); "bridge" = share of that exit flux leaving from states whose winner is a bridge; feeder = N × rate of the neutral step into bridge-winner states per unit R1 mass; the decisive edge is the largest exit edge (mutant, role, Δ, N·Δ, N·ρ). Cut = dropped jump flow (edges below 10⁻³⁰ of a row). Check = TV against dense log-domain GTH on the full generator.

| arm | game | N | π(R1) | π(R2) | dove | crash | mixed | N·exit | bridge share | N·feeder | decisive exit edge | cut | check |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| weak | chicken | 100 | 0.4997 | 0.4997 | 6.03e-04 | 4.63e-76 | 8.14e-06 | 9.71e-04 | 0.931 | 9.17e-04 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 3, NΔ 300, Nρ 59.3 | 6.68e-31 | 2.27e-15 |
| weak | chicken | 1000 | 0.4994 | 0.4994 | 1.18e-03 | 0 | 1.53e-06 | 1.06e-03 | 0.874 | 9.17e-04 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 3, NΔ 3e+03, Nρ 593 | 5.36e-33 | – |
| weak | chicken | 10000 | 0.4994 | 0.4994 | 1.16e-03 | 0 | 1.87e-07 | 1.10e-03 | 0.860 | 9.17e-04 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 3, NΔ 3e+04, Nρ 5.93e+03 | 2.64e-42 | – |
| weak | hd3 | 100 | 0.4990 | 0.4990 | 5.04e-04 | 1.86e-07 | 1.43e-03 | 2.11e-03 | 0.428 | 9.17e-04 | `Straight | Swerve` → role-2 `X`, Δ -0.25, NΔ -25, Nρ 0.00431 | 2.81e-32 | 1.43e-15 |
| weak | hd3 | 1000 | 0.4995 | 0.4995 | 9.71e-04 | 1.00e-29 | 1.48e-05 | 1.08e-03 | 0.853 | 9.17e-04 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+03, Nρ 451 | 2.12e-31 | – |
| weak | hd3 | 10000 | 0.4995 | 0.4995 | 9.66e-04 | 0 | 1.59e-06 | 1.11e-03 | 0.846 | 9.17e-04 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+04, Nρ 4.51e+03 | 2.73e-34 | – |
| weak | hd6 | 100 | 0.4997 | 0.4997 | 5.72e-04 | 1.13e-19 | 8.06e-05 | 1.02e-03 | 0.886 | 9.17e-04 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 200, Nρ 45.1 | 1.65e-32 | 4.93e-15 |
| weak | hd6 | 1000 | 0.4994 | 0.4994 | 1.17e-03 | 0 | 5.82e-06 | 1.07e-03 | 0.863 | 9.17e-04 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+03, Nρ 451 | 1.49e-31 | – |
| weak | hd6 | 10000 | 0.4994 | 0.4994 | 1.20e-03 | 0 | 6.29e-07 | 1.10e-03 | 0.852 | 9.17e-04 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+04, Nρ 4.51e+03 | 4.24e-36 | – |
| modal | chicken | 100 | 0.5000 | 0.5000 | 4.16e-05 | 0 | 0 | 1.45e-02 | 0.983 | 1.42e-02 | `BOXD(THEM(ME)) | Swerve` → role-2 `Straight`, Δ 3, NΔ 300, Nρ 59.3 | 5.89e-33 | 1.92e-15 |
| modal | chicken | 1000 | 0.5000 | 0.5000 | 1.50e-05 | 0 | 0 | 1.47e-02 | 0.982 | 1.42e-02 | `BOXD(THEM(ME)) | Swerve` → role-2 `Straight`, Δ 3, NΔ 3e+03, Nρ 593 | 5.30e-134 | – |
| modal | chicken | 10000 | 0.5000 | 0.5000 | 9.45e-06 | 0 | 0 | 1.48e-02 | 0.982 | 1.42e-02 | `BOXD(THEM(ME)) | Swerve` → role-2 `Straight`, Δ 3, NΔ 3e+04, Nρ 5.93e+03 | 0 | – |
| modal | hd3 | 100 | 0.5000 | 0.5000 | 6.29e-05 | 1.72e-07 | 0 | 1.44e-02 | 0.982 | 1.42e-02 | `BOXD(THEM(ME)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 200, Nρ 45.1 | 1.36e-32 | 2.32e-15 |
| modal | hd3 | 1000 | 0.5000 | 0.5000 | 1.84e-05 | 0 | 0 | 1.47e-02 | 0.982 | 1.42e-02 | `BOXD(THEM(ME)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+03, Nρ 451 | 4.03e-63 | – |
| modal | hd3 | 10000 | 0.5000 | 0.5000 | 1.00e-05 | 0 | 0 | 1.48e-02 | 0.982 | 1.42e-02 | `BOXD(THEM(ME)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+04, Nρ 4.51e+03 | 0 | – |
| modal | hd6 | 100 | 0.5000 | 0.5000 | 6.29e-05 | 7.90e-27 | 0 | 1.44e-02 | 0.983 | 1.42e-02 | `BOXD(THEM(ME)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 200, Nρ 45.1 | 7.19e-31 | 5.43e-15 |
| modal | hd6 | 1000 | 0.5000 | 0.5000 | 1.84e-05 | 0 | 0 | 1.47e-02 | 0.982 | 1.42e-02 | `BOXD(THEM(ME)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+03, Nρ 451 | 5.54e-128 | – |
| modal | hd6 | 10000 | 0.5000 | 0.5000 | 1.00e-05 | 0 | 0 | 1.48e-02 | 0.982 | 1.42e-02 | `BOXD(THEM(ME)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+04, Nρ 4.51e+03 | 0 | – |
| W0 | chicken | 100 | 0.4996 | 0.4996 | 7.71e-04 | 0 | 0 | 2.09e-03 | 0.918 | 1.95e-03 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 3, NΔ 300, Nρ 59.3 | 4.10e-38 | 4.39e-16 |
| W0 | chicken | 1000 | 0.4994 | 0.4994 | 1.29e-03 | 0 | 0 | 2.27e-03 | 0.868 | 1.95e-03 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 3, NΔ 3e+03, Nρ 593 | 6.66e-130 | 8.97e-16 |
| W0 | chicken | 10000 | 0.4994 | 0.4994 | 1.15e-03 | 0 | 0 | 2.36e-03 | 0.863 | 1.95e-03 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 3, NΔ 3e+04, Nρ 5.93e+03 | 0 | 1.81e-15 |
| W0 | hd3 | 100 | 0.4996 | 0.4996 | 7.88e-04 | 1.80e-07 | 0 | 2.08e-03 | 0.917 | 1.95e-03 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 200, Nρ 45.1 | 3.02e-34 | 9.00e-16 |
| W0 | hd3 | 1000 | 0.4993 | 0.4993 | 1.32e-03 | 0 | 0 | 2.26e-03 | 0.868 | 1.95e-03 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+03, Nρ 451 | 2.53e-62 | 4.69e-16 |
| W0 | hd3 | 10000 | 0.4994 | 0.4994 | 1.21e-03 | 0 | 0 | 2.34e-03 | 0.862 | 1.95e-03 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+04, Nρ 4.51e+03 | 0 | 9.13e-16 |
| W0 | hd6 | 100 | 0.4996 | 0.4996 | 7.88e-04 | 8.16e-27 | 0 | 2.08e-03 | 0.917 | 1.95e-03 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 200, Nρ 45.1 | 4.00e-39 | 6.95e-16 |
| W0 | hd6 | 1000 | 0.4993 | 0.4993 | 1.32e-03 | 0 | 0 | 2.26e-03 | 0.868 | 1.95e-03 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+03, Nρ 451 | 3.87e-127 | 4.69e-16 |
| W0 | hd6 | 10000 | 0.4994 | 0.4994 | 1.21e-03 | 0 | 0 | 2.34e-03 | 0.862 | 1.95e-03 | `not(THEM(THEM)) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+04, Nρ 4.51e+03 | 0 | 9.13e-16 |
| M0 | chicken | 100 | 0.5000 | 0.5000 | 1.64e-05 | 0 | 0 | 2.03e-03 | 0.945 | 1.95e-03 | `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight`, Δ 3, NΔ 300, Nρ 59.3 | 4.52e-38 | 8.79e-16 |
| M0 | chicken | 1000 | 0.5000 | 0.5000 | 6.82e-06 | 0 | 0 | 2.06e-03 | 0.943 | 1.95e-03 | `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight`, Δ 3, NΔ 3e+03, Nρ 593 | 4.95e-134 | 8.70e-16 |
| M0 | chicken | 10000 | 0.5000 | 0.5000 | 5.26e-06 | 0 | 0 | 2.07e-03 | 0.943 | 1.95e-03 | `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight`, Δ 3, NΔ 3e+04, Nρ 5.93e+03 | 0 | 1.28e-16 |
| M0 | hd3 | 100 | 0.5000 | 0.5000 | 2.41e-05 | 1.80e-07 | 0 | 2.02e-03 | 0.944 | 1.95e-03 | `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight`, Δ 2, NΔ 200, Nρ 45.1 | 2.01e-33 | 4.72e-16 |
| M0 | hd3 | 1000 | 0.5000 | 0.5000 | 7.83e-06 | 0 | 0 | 2.06e-03 | 0.943 | 1.95e-03 | `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+03, Nρ 451 | 2.96e-62 | 9.09e-16 |
| M0 | hd3 | 10000 | 0.5000 | 0.5000 | 5.43e-06 | 0 | 0 | 2.07e-03 | 0.943 | 1.95e-03 | `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+04, Nρ 4.51e+03 | 0 | 4.44e-16 |
| M0 | hd6 | 100 | 0.5000 | 0.5000 | 2.41e-05 | 8.17e-27 | 0 | 2.02e-03 | 0.945 | 1.95e-03 | `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight`, Δ 2, NΔ 200, Nρ 45.1 | 8.76e-41 | 4.58e-16 |
| M0 | hd6 | 1000 | 0.5000 | 0.5000 | 7.83e-06 | 0 | 0 | 2.06e-03 | 0.943 | 1.95e-03 | `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+03, Nρ 451 | 4.52e-127 | 9.09e-16 |
| M0 | hd6 | 10000 | 0.5000 | 0.5000 | 5.43e-06 | 0 | 0 | 2.07e-03 | 0.943 | 1.95e-03 | `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight`, Δ 2, NΔ 2e+04, Nρ 4.51e+03 | 0 | 4.44e-16 |
| const | chicken | 100 | 0.5000 | 0.5000 | 7.98e-27 | 0 | 0 | 1.80e-25 | 0.000 | 0 | `Straight | Swerve` → role-1 `Swerve`, Δ -2, NΔ -200, Nρ 7.2e-25 | 5.30e-91 | 2.80e-41 |
| const | chicken | 1000 | 0.5000 | 0.5000 | 2.41e-261 | 0 | 0 | 5.45e-259 | 0.000 | 0 | `Straight | Swerve` → role-1 `Swerve`, Δ -2, NΔ -2e+03, Nρ 2.18e-258 | 0 | 0 |
| const | chicken | 10000 | 0.5000 | 0.5000 | 0 | 0 | 0 | 0 | – | 0 | – | 0 | 0 |
| const | hd3 | 100 | 0.5000 | 0.5000 | 6.32e-14 | 1.78e-07 | 0 | 1.24e-06 | 0.000 | 0 | `Straight | Swerve` → role-2 `Straight`, Δ -0.5, NΔ -50, Nρ 4.95e-06 | 0 | 1.11e-16 |
| const | hd3 | 1000 | 0.5000 | 0.5000 | 0 | 4.17e-66 | 0 | 2.90e-64 | 0.000 | 0 | `Straight | Swerve` → role-2 `Straight`, Δ -0.5, NΔ -500, Nρ 1.16e-63 | 7.76e-66 | 1.74e-131 |
| const | hd3 | 10000 | 0.5000 | 0.5000 | 0 | 0 | 0 | 0 | – | 0 | – | 0 | 0 |
| const | hd6 | 100 | 0.5000 | 0.5000 | 6.32e-14 | 7.98e-27 | 0 | 8.18e-13 | 0.000 | 0 | `Straight | Swerve` → role-1 `Swerve`, Δ -1, NΔ -100, Nρ 3.27e-12 | 0 | 1.14e-28 |
| const | hd6 | 1000 | 0.5000 | 0.5000 | 3.47e-131 | 0 | 0 | 4.50e-129 | 0.000 | 0 | `Straight | Swerve` → role-1 `Swerve`, Δ -1, NΔ -1e+03, Nρ 1.8e-128 | 6.05e-131 | 1.21e-261 |
| const | hd6 | 10000 | 0.5000 | 0.5000 | 0 | 0 | 0 | 0 | – | 0 | – | 0 | 0 |

**Support and transition structure** (N = 10³, chicken):

- weak: support `Straight | Swerve` 0.4931 (R1); `Swerve | Straight` 0.4931 (R2); `not(THEM(THEM)) | Straight` 0.0024 (R2); `Straight | not(THEM(THEM))` 0.0024 (R1); `not(THEM(ME)) | Straight` 0.0024 (R2); lumped flux R1→R2 4.54e-07; R2→R1 4.54e-07; R1→dove 6.96e-08; R2→dove 6.96e-08; dove→R2 5.13e-08; dove→R1 5.13e-08.
- modal: support `Swerve | Straight` 0.4420 (R2); `Straight | Swerve` 0.4420 (R1); `BOXD(THEM(THEM)) | Straight` 0.0096 (R2); `Straight | BOXD(THEM(THEM))` 0.0096 (R1); `BOXD(THEM(ME)) | Straight` 0.0095 (R2); lumped flux R1→R2 7.22e-06; R2→R1 7.22e-06; dove→R2 1.54e-07; dove→R1 1.54e-07; R2→dove 1.54e-07; R1→dove 1.54e-07.
- W0: support `Straight | Swerve` 0.4906 (R1); `Swerve | Straight` 0.4906 (R2); `not(THEM(THEM)) | Straight` 0.0036 (R2); `Straight | not(THEM(THEM))` 0.0036 (R1); `not(THEM(ME)) | Straight` 0.0035 (R2); lumped flux R1→R2 9.67e-07; R2→R1 9.67e-07; dove→R2 1.65e-07; R2→dove 1.65e-07; dove→R1 1.65e-07; R1→dove 1.65e-07.
- M0: support `Swerve | Straight` 0.4923 (R2); `Straight | Swerve` 0.4923 (R1); `not(BOX(THEM(ME))) | Straight` 0.0038 (R2); `Straight | not(BOX(THEM(ME)))` 0.0038 (R1); `not(BOX(THEM(THEM))) | Straight` 0.0035 (R2); lumped flux R1→R2 9.70e-07; R2→R1 9.70e-07; dove→R1 6.18e-08; dove→R2 6.18e-08; R2→dove 6.18e-08; R1→dove 6.18e-08.
- const: support `Straight | Swerve` 0.5000 (R1); `Swerve | Straight` 0.5000 (R2); `Swerve | Swerve` 0.0000 (dove); `Straight | Straight` 0.0000 (crash); lumped flux dove→R1 2.72e-262; dove→R2 2.72e-262; R1→dove 2.72e-262; R2→dove 2.72e-262.

Exit edges out of R1 by share (N = 10⁴, chicken):

- weak: `not(THEM(THEM)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.350; `not(THEM(ME)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.350; `not(THEM(^X)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.039; `not(THEM(^Swerve)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.039; `not(THEM(^Straight)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.038.
- modal: `BOXD(THEM(ME)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.146; `BOXD(THEM(THEM)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.146; `BOXD1(THEM(ME)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.143; `BOXD1(THEM(THEM)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.142; `BOXD(THEM(^D)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.041.
- W0: `not(THEM(THEM)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.356; `not(THEM(ME)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.355; `and(THEM(ME),Straight) | Swerve` → role-2 `THEM(ME)` (Δ 1, Nρ 2.59e+03) 0.049; `not(THEM(^Swerve)) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.049; `and(THEM(ME),Straight) | Swerve` → role-2 `THEM(THEM)` (Δ 1, Nρ 2.59e+03) 0.049.
- M0: `not(BOX(THEM(ME))) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.453; `not(BOX(THEM(THEM))) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.412; `not(BOX(THEM(^C))) | Swerve` → role-2 `Straight` (Δ 3, Nρ 5.93e+03) 0.056; `BOX(THEM(ME)) | not(BOX(THEM(ME)))` → role-2 `Swerve` (Δ 1, Nρ 2.59e+03) 0.039; `not(BOX(THEM(ME))) | Swerve` → role-2 `BOX(THEM(ME))` (Δ 3, Nρ 5.93e+03) 0.014.

## The ε→0 chain, one population, modal arm (c) (seeded log-domain solver, twin-expanded and lumped)

| game | N | θ | twins | states | log₁₀ cut | π by class | payoff/player | efficiency | P(St,St) | P(asym) | P(Sw,Sw) | top state (π) | top exit (log₁₀ rate) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chicken | 10000 | 1e-14 | False | 384 | -31.1 | crash 0.000, dove 0.000, mixed 1.000 | -0.398 | -0.796 | 0.074 | 0.678 | 0.248 | `Swerve:0.061 + BOXD(THEM(THEM)):0.185 + BOX1(THEM(^D)):0.090 + not(BOX(THEM(ME))):0.059 + not(BOXD(THEM(^C))):0.362 + not(BOXD1(THEM(^D))):0.088 + BOXD1(THEM(^BOXD1(THEM(THEM)))):0.153` (0.289) | -465.2 via `not(BOX(THEM(^D)))` |
| chicken | 10000 | 1e-16 | True | 680 | -221.1 | crash 0.000, dove 0.000, mixed 1.000 | -0.098 | -0.196 | 0.031 | 0.425 | 0.544 | `Swerve:0.278 + BOX(THEM(^C)):0.330 + BOX(THEM(^D)):0.124 + BOXD1(THEM(^D)):0.029 + not(BOX1(THEM(ME))):0.069 + BOX(THEM(^BOXD(THEM(ME)))):0.098 + BOX(THEM(^BOXD1(THEM(ME)))):0.073` (1.000) | -380.8 via `BOX1(THEM(^C))` |
| chicken | 100 | 1e-14 | True | 2971 | -11.6 | crash 0.000, dove 0.002, mixed 0.998 | -0.476 | -0.953 | 0.080 | 0.643 | 0.277 | `Straight:0.210 + BOXD(THEM(THEM)):0.150 + BOXD1(THEM(THEM)):0.120 + not(BOX1(THEM(ME))):0.520` (0.486) | -4.0 via `BOXD(THEM(^D))` |
| chicken | 1000 | 1e-14 | True | 707 | -17.0 | crash 0.000, dove 0.000, mixed 1.000 | -0.099 | -0.198 | 0.031 | 0.425 | 0.544 | `Swerve:0.277 + BOX(THEM(^C)):0.330 + BOX(THEM(^D)):0.124 + BOXD1(THEM(^D)):0.029 + not(BOX1(THEM(ME))):0.069 + BOX(THEM(^BOXD(THEM(ME)))):0.098 + BOX(THEM(^BOXD1(THEM(ME)))):0.073` (1.000) | -41.8 via `BOX1(THEM(^C))` |
| chicken | 10000 | 1e-14 | True | 630 | -221.1 | crash 0.000, dove 0.000, mixed 1.000 | -0.098 | -0.196 | 0.031 | 0.425 | 0.544 | `Swerve:0.278 + BOX(THEM(^C)):0.330 + BOX(THEM(^D)):0.124 + BOXD1(THEM(^D)):0.029 + not(BOX1(THEM(ME))):0.069 + BOX(THEM(^BOXD(THEM(ME)))):0.098 + BOX(THEM(^BOXD1(THEM(ME)))):0.073` (1.000) | -380.8 via `BOX1(THEM(^C))` |
| chicken | 10000 | 1e-12 | True | 540 | -38.8 | crash 0.000, dove 0.000, mixed 1.000 | -0.112 | -0.225 | 0.039 | 0.554 | 0.407 | `Swerve:0.141 + BOX(THEM(^C)):0.410 + BOX1(THEM(^D)):0.124 + BOXD1(THEM(^D)):0.020 + not(BOX(THEM(ME))):0.092 + BOX(THEM(^BOXD(THEM(ME)))):0.121 + BOX(THEM(^BOXD1(THEM(ME)))):0.091` (1.000) | -409.7 via `BOX1(THEM(^C))` |
| hd3 | 100 | 1e-14 | True | 2987 | -11.2 | crash 0.000, dove 0.028, mixed 0.972 | 0.102 | 0.102 | 0.599 | 0.364 | 0.038 | `Straight:0.790 + BOXD(THEM(THEM)):0.160 + BOXD1(THEM(THEM)):0.030 + not(BOX1(THEM(ME))):0.020` (0.130) | -3.2 via `not(BOX1(THEM(THEM)))` |
| hd3 | 1000 | 1e-14 | True | 3005 | -11.1 | crash 0.000, dove 0.000, mixed 1.000 | 0.234 | 0.234 | 0.511 | 0.460 | 0.029 | `Straight:0.691 + BOXD(THEM(ME)):0.001 + not(BOX1(THEM(THEM))):0.140 + not(BOX(THEM(^D))):0.066 + BOXD(THEM(^BOXD1(THEM(THEM)))):0.085 + BOXD1(THEM(^BOXD1(THEM(THEM)))):0.017` (0.252) | -5.8 via `BOXD1(THEM(^BOXD(THEM(THEM))))` |
| hd3 | 10000 | 1e-14 | True | 3005 | -14.7 | crash 0.000, dove 0.000, mixed 1.000 | 0.016 | 0.016 | 0.656 | 0.344 | 0.000 | `Straight:0.794 + BOXD1(THEM(ME)):0.000 + BOXD(THEM(THEM)):0.158 + BOXD1(THEM(THEM)):0.031 + not(BOX1(THEM(THEM))):0.016 + BOXD(THEM(^BOXD1(THEM(THEM)))):0.001` (0.502) | -74.0 via `not(BOXD(THEM(^C)))` |
| hd6 | 100 | 1e-14 | True | 2972 | -11.3 | crash 0.000, dove 0.003, mixed 0.997 | 0.249 | 0.249 | 0.250 | 0.688 | 0.061 | `Straight:0.450 + BOXD(THEM(THEM)):0.220 + BOXD1(THEM(THEM)):0.110 + not(BOX1(THEM(ME))):0.220` (0.351) | -4.2 via `BOXD(THEM(^D))` |
| hd6 | 1000 | 1e-14 | True | 3052 | -11.2 | crash 0.000, dove 0.000, mixed 1.000 | 0.804 | 0.804 | 0.065 | 0.431 | 0.503 | `Swerve:0.389 + BOX(THEM(^C)):0.111 + BOX(THEM(^D)):0.167 + BOXD1(THEM(^D)):0.111 + not(BOX1(THEM(ME))):0.055 + BOX(THEM(^BOXD(THEM(ME)))):0.111 + BOX(THEM(^BOXD1(THEM(ME)))):0.056` (0.421) | -0.6 via `Straight`, `BOX(THEM(ME))` |
| hd6 | 10000 | 1e-14 | True | 2049 | -16.3 | crash 0.000, dove 0.000, mixed 1.000 | 0.833 | 0.833 | 0.056 | 0.395 | 0.549 | `Swerve:0.389 + BOX(THEM(^C)):0.111 + BOX(THEM(^D)):0.167 + BOXD1(THEM(^D)):0.111 + not(BOX1(THEM(ME))):0.056 + BOX(THEM(^BOXD(THEM(ME)))):0.111 + BOX(THEM(^BOXD1(THEM(ME)))):0.056` (0.500) | -0.6 via `Straight`, `BOX(THEM(ME))` |

## The lottery (ε = 0; I = 64; finite-size evidence)

Per-island establishment = share of islands established at a one-sided convention by play (held through the last tenth of the horizon), mean ± 95% t-interval over runs. R1 share = R1 among established convention islands, per-run fraction averaged over runs with its 95% t-interval (islands within a run are not independent). Patchwork = runs with islands at both conventions at the mark; resolved = runs that were patchworks at some sample and are not at the mark (median resolution generation); E3 = runs every island of which is E3-resolved (median generation). Crash/dove on = second-half time average of the islands' crash/dove probability. Cross loss = (T + S) − E[u₁ + u₂] for role 1 of island A against role 2 of island B, A ≠ B. Flips: island convention changes per run, the share reader-mediated (winner bridge share ≥ f* before the flip) and the share selection-favoured.

| set | arm | game | N | mN | mark | runs | establishment | R1 share | R1 / R2 / crash / dove / mixed | patchwork | resolved (gen) | E3 (gen) | crash on | dove on | cross loss | crash cross | flips/run | reader-med. | sel.-fav. | bridge share (r1, r2) | polymorphic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| main | weak | chicken | 100 | 0 | 2000 | 40 | 0.941 ± 0.008 | 0.502 [0.48, 0.53] | 0.472 / 0.469 / 0.000 / 0.000 / 0.059 | 1.000 | 0.000 (–) | 0.000 (–) | 0 | 2.82e-02 | 5.063 ± 0.079 | 2.29e-01 | 0.0 | 1.00 | 1.00 | 0.021, 0.019 | 0.04 |
| main | weak | chicken | 100 | 1 | 2000 | 40 | 0.784 ± 0.075 | 0.566 [0.42, 0.71] | 0.550 / 0.430 / 0.000 / 0.000 / 0.020 | 0.575 | 0.425 (590) | 0.425 (700) | 2.29e-03 | 4.44e-03 | 2.312 ± 0.717 | 1.05e-01 | 26.8 | 0.28 | 0.28 | 0.367, 0.442 | 0.76 |
| main | weak | chicken | 100 | 1 | 4000 | 40 | 0.718 ± 0.099 | 0.547 [0.40, 0.70] | 0.535 / 0.450 / 0.000 / 0.000 / 0.015 | 0.575 | 0.425 (590) | 0.425 (700) | 2.20e-03 | 4.57e-03 | 2.231 ± 0.709 | 1.01e-01 | 27.9 | 0.28 | 0.28 | 0.390, 0.444 | 0.71 |
| main | weak | hd3 | 100 | 0 | 2000 | 40 | 0.785 ± 0.018 | 0.506 [0.48, 0.53] | 0.397 / 0.388 / 0.001 / 0.000 / 0.214 | 1.000 | 0.000 (–) | 0.000 (–) | 9.93e-02 | 6.52e-03 | 0.897 ± 0.015 | 2.99e-01 | 0.0 | – | – | 0.007, 0.008 | 0.00 |
| main | weak | hd3 | 100 | 1 | 2000 | 40 | 0.518 ± 0.158 | 0.462 [0.27, 0.66] | 0.419 / 0.403 / 0.000 / 0.000 / 0.179 | 0.500 | 0.500 (540) | 0.500 (600) | 1.77e-02 | 8.55e-03 | 0.340 ± 0.116 | 1.13e-01 | 21.7 | 0.26 | 0.25 | 0.228, 0.212 | 0.83 |
| main | weak | hd3 | 100 | 1 | 4000 | 40 | 0.515 ± 0.159 | 0.478 [0.27, 0.69] | 0.415 / 0.414 / 0.000 / 0.000 / 0.171 | 0.500 | 0.500 (540) | 0.500 (600) | 1.73e-02 | 8.43e-03 | 0.330 ± 0.115 | 1.10e-01 | 22.1 | 0.25 | 0.24 | 0.232, 0.210 | 0.82 |
| main | weak | hd6 | 100 | 0 | 2000 | 40 | 0.903 ± 0.013 | 0.505 [0.49, 0.52] | 0.456 / 0.446 / 0.000 / 0.000 / 0.097 | 1.000 | 0.000 (–) | 0.000 (–) | 4.15e-04 | 4.68e-02 | 1.366 ± 0.018 | 2.28e-01 | 0.0 | – | – | 0.009, 0.010 | 0.01 |
| main | weak | hd6 | 100 | 1 | 2000 | 40 | 0.718 ± 0.139 | 0.404 [0.25, 0.56] | 0.394 / 0.550 / 0.000 / 0.000 / 0.056 | 0.325 | 0.675 (600) | 0.675 (700) | 3.24e-03 | 5.76e-03 | 0.423 ± 0.208 | 7.05e-02 | 25.1 | 0.29 | 0.28 | 0.342, 0.260 | 0.81 |
| main | weak | hd6 | 100 | 1 | 4000 | 40 | 0.704 ± 0.144 | 0.387 [0.21, 0.56] | 0.391 / 0.555 / 0.000 / 0.000 / 0.054 | 0.325 | 0.675 (600) | 0.675 (700) | 3.17e-03 | 5.80e-03 | 0.422 ± 0.208 | 7.03e-02 | 25.1 | 0.29 | 0.28 | 0.346, 0.260 | 0.80 |
| main | modal | chicken | 100 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.503 [0.49, 0.52] | 0.503 / 0.497 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 4.985 ± 0.085 | 2.33e-01 | 0.1 | 0.33 | 0.33 | 0.249, 0.238 | 0.63 |
| main | modal | chicken | 100 | 1 | 2000 | 40 | 0.982 ± 0.011 | 0.697 [0.55, 0.84] | 0.689 / 0.308 / 0.000 / 0.000 / 0.002 | 0.550 | 0.450 (940) | 0.475 (1000) | 7.02e-04 | 3.79e-08 | 0.653 ± 0.256 | 3.11e-02 | 54.6 | 0.32 | 0.36 | 0.280, 0.641 | 0.71 |
| main | modal | chicken | 100 | 1 | 4000 | 40 | 0.912 ± 0.079 | 0.630 [0.48, 0.78] | 0.639 / 0.358 / 0.000 / 0.000 / 0.002 | 0.325 | 0.675 (1150) | 0.700 (1150) | 5.48e-04 | 0 | 0.359 ± 0.207 | 1.71e-02 | 69.0 | 0.35 | 0.37 | 0.339, 0.632 | 0.50 |
| main | modal | hd3 | 100 | 0 | 2000 | 40 | 0.998 ± 0.002 | 0.484 [0.46, 0.50] | 0.482 / 0.515 / 0.002 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 2.34e-03 | 0 | 0.767 ± 0.007 | 2.56e-01 | 0.1 | 0.67 | 0.67 | 0.129, 0.126 | 0.10 |
| main | modal | hd3 | 100 | 1 | 2000 | 40 | 0.300 ± 0.108 | 0.543 [0.38, 0.71] | 0.420 / 0.407 / 0.000 / 0.000 / 0.173 | 0.825 | 0.175 (1980) | 0.075 (400) | 3.06e-02 | 3.61e-05 | 0.823 ± 0.152 | 2.74e-01 | 61.5 | 0.36 | 0.35 | 0.467, 0.474 | 0.77 |
| main | modal | hd3 | 100 | 1 | 4000 | 40 | 0.216 ± 0.106 | 0.538 [0.34, 0.73] | 0.418 / 0.425 / 0.000 / 0.000 / 0.157 | 0.875 | 0.125 (570) | 0.100 (550) | 2.77e-02 | 0 | 0.830 ± 0.156 | 2.77e-01 | 64.4 | 0.36 | 0.35 | 0.487, 0.468 | 0.74 |
| main | modal | hd6 | 100 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.508 [0.49, 0.52] | 0.508 / 0.492 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 1.483 ± 0.016 | 2.47e-01 | 0.1 | 0.75 | 0.75 | 0.140, 0.148 | 0.33 |
| main | modal | hd6 | 100 | 1 | 2000 | 40 | 0.846 ± 0.056 | 0.513 [0.35, 0.67] | 0.491 / 0.489 / 0.000 / 0.000 / 0.020 | 0.825 | 0.175 (620) | 0.125 (600) | 5.93e-03 | 1.21e-05 | 0.736 ± 0.180 | 1.23e-01 | 57.6 | 0.34 | 0.34 | 0.431, 0.437 | 0.73 |
| main | modal | hd6 | 100 | 1 | 4000 | 40 | 0.884 ± 0.039 | 0.475 [0.31, 0.64] | 0.461 / 0.524 / 0.000 / 0.000 / 0.015 | 0.800 | 0.200 (845) | 0.175 (700) | 4.53e-03 | 0 | 0.593 ± 0.157 | 9.88e-02 | 76.0 | 0.37 | 0.36 | 0.521, 0.448 | 0.49 |
| small | weak | chicken | 25 | 0 | 2000 | 40 | 0.736 ± 0.021 | 0.501 [0.48, 0.52] | 0.367 / 0.368 / 0.000 / 0.013 / 0.251 | 1.000 | 0.000 (–) | 0.000 (–) | 0 | 1.37e-01 | 4.213 ± 0.104 | 1.85e-01 | 0.0 | – | – | 0.007, 0.007 | 0.00 |
| small | weak | chicken | 25 | 1 | 2000 | 40 | 0.548 ± 0.152 | 0.643 [0.46, 0.82] | 0.511 / 0.321 / 0.000 / 0.000 / 0.169 | 0.425 | 0.575 (170) | 0.500 (200) | 8.09e-03 | 2.13e-02 | 1.972 ± 0.759 | 8.91e-02 | 23.9 | 0.12 | 0.13 | 0.160, 0.322 | 0.60 |
| small | weak | chicken | 25 | 1 | 4000 | 40 | 0.619 ± 0.150 | 0.654 [0.47, 0.84] | 0.508 / 0.342 / 0.000 / 0.000 / 0.150 | 0.375 | 0.625 (180) | 0.575 (200) | 6.91e-03 | 1.82e-02 | 1.668 ± 0.729 | 7.53e-02 | 26.0 | 0.11 | 0.12 | 0.163, 0.322 | 0.54 |
| small | weak | chicken | 50 | 0 | 2000 | 40 | 0.849 ± 0.015 | 0.508 [0.49, 0.53] | 0.432 / 0.418 / 0.000 / 0.000 / 0.151 | 1.000 | 0.000 (–) | 0.000 (–) | 0 | 7.30e-02 | 4.685 ± 0.094 | 2.10e-01 | 0.0 | – | – | 0.017, 0.012 | 0.01 |
| small | weak | chicken | 50 | 1 | 2000 | 40 | 0.604 ± 0.141 | 0.312 [0.15, 0.48] | 0.313 / 0.603 / 0.000 / 0.000 / 0.084 | 0.525 | 0.475 (290) | 0.475 (300) | 3.91e-03 | 8.66e-03 | 2.021 ± 0.728 | 9.18e-02 | 24.9 | 0.13 | 0.13 | 0.424, 0.212 | 0.64 |
| small | weak | chicken | 50 | 1 | 4000 | 40 | 0.565 ± 0.148 | 0.345 [0.17, 0.52] | 0.337 / 0.580 / 0.000 / 0.000 / 0.083 | 0.475 | 0.525 (290) | 0.500 (300) | 3.87e-03 | 8.72e-03 | 1.974 ± 0.735 | 8.95e-02 | 26.4 | 0.14 | 0.15 | 0.408, 0.236 | 0.61 |
| small | weak | hd3 | 25 | 0 | 2000 | 40 | 0.481 ± 0.020 | 0.525 [0.49, 0.55] | 0.253 / 0.229 / 0.050 / 0.006 / 0.463 | 1.000 | 0.000 (–) | 0.000 (–) | 2.11e-01 | 7.35e-02 | 0.972 ± 0.026 | 3.24e-01 | 0.0 | – | – | 0.002, 0.003 | 0.00 |
| small | weak | hd3 | 25 | 1 | 2000 | 40 | 1.000 ± 0.000 | 0.475 [0.31, 0.64] | 0.475 / 0.525 / 0.000 / 0.000 / 0.000 | 0.000 | 0.975 (160) | 1.000 (300) | 0 | 0 | 0.000 ± 0.000 | 0 | 13.3 | 0.06 | 0.05 | 0.084, 0.049 | 0.15 |
| small | weak | hd3 | 25 | 1 | 4000 | 40 | 1.000 ± 0.000 | 0.475 [0.31, 0.64] | 0.475 / 0.525 / 0.000 / 0.000 / 0.000 | 0.000 | 0.975 (160) | 1.000 (300) | 0 | 0 | 0.000 ± 0.000 | 0 | 13.3 | 0.06 | 0.05 | 0.084, 0.049 | 0.15 |
| small | weak | hd3 | 50 | 0 | 2000 | 40 | 0.627 ± 0.018 | 0.495 [0.47, 0.52] | 0.311 / 0.316 / 0.013 / 0.000 / 0.359 | 1.000 | 0.000 (–) | 0.000 (–) | 1.61e-01 | 2.93e-02 | 0.963 ± 0.017 | 3.21e-01 | 0.0 | – | – | 0.007, 0.007 | 0.00 |
| small | weak | hd3 | 50 | 1 | 2000 | 40 | 0.970 ± 0.051 | 0.359 [0.21, 0.51] | 0.357 / 0.629 / 0.000 / 0.000 / 0.014 | 0.025 | 0.975 (680) | 0.975 (900) | 3.44e-03 | 1.45e-03 | 0.020 ± 0.041 | 6.74e-03 | 27.2 | 0.05 | 0.05 | 0.149, 0.085 | 0.38 |
| small | weak | hd3 | 50 | 1 | 4000 | 40 | 1.000 ± 0.000 | 0.375 [0.22, 0.53] | 0.375 / 0.625 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (685) | 1.000 (900) | 1.29e-03 | 5.33e-04 | 0.000 ± 0.000 | 0 | 28.5 | 0.04 | 0.04 | 0.149, 0.085 | 0.35 |
| small | weak | hd6 | 25 | 0 | 2000 | 40 | 0.618 ± 0.018 | 0.493 [0.47, 0.51] | 0.304 / 0.314 / 0.000 / 0.018 / 0.364 | 1.000 | 0.000 (–) | 0.000 (–) | 2.92e-02 | 1.68e-01 | 1.118 ± 0.028 | 1.86e-01 | 0.0 | – | – | 0.007, 0.007 | 0.00 |
| small | weak | hd6 | 25 | 1 | 2000 | 40 | 1.000 ± 0.000 | 0.500 [0.34, 0.66] | 0.500 / 0.500 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (305) | 1.000 (400) | 0 | 1.39e-06 | 0.000 ± 0.000 | 0 | 25.4 | 0.02 | 0.02 | 0.052, 0.149 | 0.27 |
| small | weak | hd6 | 25 | 1 | 4000 | 40 | 1.000 ± 0.000 | 0.500 [0.34, 0.66] | 0.500 / 0.500 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (305) | 1.000 (400) | 0 | 0 | 0.000 ± 0.000 | 0 | 25.4 | 0.02 | 0.02 | 0.052, 0.149 | 0.27 |
| small | weak | hd6 | 50 | 0 | 2000 | 40 | 0.778 ± 0.017 | 0.514 [0.49, 0.54] | 0.401 / 0.377 / 0.000 / 0.003 / 0.219 | 1.000 | 0.000 (–) | 0.000 (–) | 6.52e-03 | 1.03e-01 | 1.218 ± 0.024 | 2.03e-01 | 0.0 | – | – | 0.006, 0.007 | 0.00 |
| small | weak | hd6 | 50 | 1 | 2000 | 40 | 0.603 ± 0.154 | 0.630 [0.44, 0.82] | 0.511 / 0.323 / 0.000 / 0.000 / 0.166 | 0.425 | 0.575 (310) | 0.575 (400) | 8.32e-03 | 1.49e-02 | 0.533 ± 0.219 | 8.88e-02 | 23.0 | 0.15 | 0.14 | 0.200, 0.328 | 0.74 |
| small | weak | hd6 | 50 | 1 | 4000 | 40 | 0.603 ± 0.155 | 0.640 [0.45, 0.83] | 0.519 / 0.332 / 0.000 / 0.000 / 0.150 | 0.375 | 0.625 (320) | 0.575 (400) | 8.06e-03 | 1.44e-02 | 0.495 ± 0.210 | 8.25e-02 | 24.3 | 0.15 | 0.13 | 0.196, 0.333 | 0.71 |
| small | modal | chicken | 25 | 0 | 2000 | 40 | 0.992 ± 0.003 | 0.486 [0.46, 0.51] | 0.482 / 0.510 / 0.000 / 0.008 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 8.20e-03 | 4.832 ± 0.091 | 2.22e-01 | 0.1 | 1.00 | 1.00 | 0.133, 0.131 | 0.10 |
| small | modal | chicken | 25 | 1 | 2000 | 40 | 0.964 ± 0.051 | 0.641 [0.49, 0.79] | 0.648 / 0.348 / 0.000 / 0.000 / 0.004 | 0.050 | 0.950 (265) | 0.875 (300) | 6.62e-04 | 0 | 0.130 ± 0.117 | 6.19e-03 | 68.0 | 0.23 | 0.26 | 0.324, 0.624 | 0.39 |
| small | modal | chicken | 25 | 1 | 4000 | 40 | 0.982 ± 0.018 | 0.650 [0.50, 0.80] | 0.650 / 0.348 / 0.000 / 0.000 / 0.002 | 0.075 | 0.925 (260) | 0.900 (300) | 5.07e-04 | 0 | 0.131 ± 0.118 | 6.25e-03 | 68.0 | 0.23 | 0.26 | 0.324, 0.624 | 0.39 |
| small | modal | chicken | 50 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.497 [0.48, 0.52] | 0.497 / 0.503 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 4.919 ± 0.085 | 2.28e-01 | 0.1 | 0.00 | 0.00 | 0.189, 0.181 | 0.31 |
| small | modal | chicken | 50 | 1 | 2000 | 40 | 0.977 ± 0.014 | 0.450 [0.29, 0.61] | 0.447 / 0.548 / 0.000 / 0.000 / 0.005 | 0.400 | 0.600 (875) | 0.400 (500) | 1.30e-03 | 0 | 0.530 ± 0.186 | 2.52e-02 | 58.4 | 0.23 | 0.26 | 0.517, 0.415 | 0.51 |
| small | modal | chicken | 50 | 1 | 4000 | 40 | 0.986 ± 0.006 | 0.450 [0.29, 0.61] | 0.448 / 0.547 / 0.000 / 0.000 / 0.005 | 0.400 | 0.600 (875) | 0.575 (900) | 1.07e-03 | 0 | 0.479 ± 0.192 | 2.28e-02 | 64.6 | 0.24 | 0.27 | 0.526, 0.421 | 0.39 |
| small | modal | hd3 | 25 | 0 | 2000 | 40 | 0.901 ± 0.013 | 0.504 [0.49, 0.52] | 0.454 / 0.447 / 0.084 / 0.014 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 8.44e-02 | 1.45e-02 | 0.860 ± 0.021 | 2.87e-01 | 0.0 | – | – | 0.062, 0.066 | 0.00 |
| small | modal | hd3 | 25 | 1 | 2000 | 40 | 1.000 ± 0.000 | 0.425 [0.26, 0.59] | 0.425 / 0.575 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (145) | 1.000 (300) | 0 | 0 | 0.000 ± 0.000 | 0 | 30.7 | 0.20 | 0.17 | 0.423, 0.302 | 0.69 |
| small | modal | hd3 | 25 | 1 | 4000 | 40 | 1.000 ± 0.000 | 0.425 [0.26, 0.59] | 0.425 / 0.575 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (145) | 1.000 (300) | 0 | 0 | 0.000 ± 0.000 | 0 | 30.7 | 0.20 | 0.17 | 0.423, 0.302 | 0.69 |
| small | modal | hd3 | 50 | 0 | 2000 | 40 | 0.979 ± 0.006 | 0.486 [0.47, 0.50] | 0.476 / 0.503 / 0.021 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 2.07e-02 | 3.91e-04 | 0.786 ± 0.012 | 2.62e-01 | 0.0 | – | – | 0.092, 0.089 | 0.02 |
| small | modal | hd3 | 50 | 1 | 2000 | 40 | 0.943 ± 0.057 | 0.575 [0.41, 0.74] | 0.571 / 0.423 / 0.000 / 0.000 / 0.006 | 0.025 | 0.975 (790) | 0.900 (900) | 7.96e-03 | 0 | 0.019 ± 0.020 | 6.33e-03 | 55.8 | 0.23 | 0.22 | 0.362, 0.473 | 0.58 |
| small | modal | hd3 | 50 | 1 | 4000 | 40 | 1.000 ± 0.000 | 0.575 [0.41, 0.74] | 0.575 / 0.425 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (820) | 1.000 (1000) | 1.75e-04 | 0 | 0.000 ± 0.000 | 0 | 56.0 | 0.23 | 0.22 | 0.363, 0.473 | 0.57 |
| small | modal | hd6 | 25 | 0 | 2000 | 40 | 0.980 ± 0.006 | 0.499 [0.48, 0.52] | 0.489 / 0.491 / 0.000 / 0.020 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 1.99e-02 | 1.393 ± 0.027 | 2.32e-01 | 0.0 | 1.00 | 1.00 | 0.081, 0.083 | 0.02 |
| small | modal | hd6 | 25 | 1 | 2000 | 40 | 0.979 ± 0.033 | 0.575 [0.41, 0.74] | 0.572 / 0.425 / 0.000 / 0.000 / 0.002 | 0.025 | 0.975 (460) | 0.950 (600) | 1.21e-03 | 0 | 0.016 ± 0.028 | 2.64e-03 | 51.4 | 0.19 | 0.19 | 0.352, 0.447 | 0.53 |
| small | modal | hd6 | 25 | 1 | 4000 | 40 | 1.000 ± 0.000 | 0.575 [0.41, 0.74] | 0.575 / 0.425 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (505) | 1.000 (600) | 1.64e-04 | 0 | 0.000 ± 0.000 | 0 | 51.5 | 0.19 | 0.19 | 0.351, 0.451 | 0.53 |
| small | modal | hd6 | 50 | 0 | 2000 | 40 | 0.998 ± 0.002 | 0.522 [0.50, 0.54] | 0.521 / 0.477 / 0.000 / 0.002 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 1.56e-03 | 1.457 ± 0.020 | 2.43e-01 | 0.0 | – | – | 0.108, 0.104 | 0.11 |
| small | modal | hd6 | 50 | 1 | 2000 | 40 | 0.750 ± 0.088 | 0.410 [0.25, 0.57] | 0.386 / 0.562 / 0.000 / 0.000 / 0.052 | 0.475 | 0.525 (1560) | 0.275 (600) | 6.36e-03 | 3.00e-05 | 0.457 ± 0.161 | 7.62e-02 | 71.8 | 0.28 | 0.27 | 0.541, 0.411 | 0.54 |
| small | modal | hd6 | 50 | 1 | 4000 | 40 | 0.707 ± 0.086 | 0.410 [0.25, 0.57] | 0.414 / 0.550 / 0.000 / 0.000 / 0.036 | 0.425 | 0.575 (3880) | 0.275 (600) | 5.50e-03 | 0 | 0.415 ± 0.150 | 6.91e-02 | 78.7 | 0.29 | 0.27 | 0.547, 0.431 | 0.37 |
| controls | W0 | chicken | 100 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.501 [0.48, 0.52] | 0.501 / 0.499 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 5.262 ± 0.054 | 2.41e-01 | 0.0 | – | – | 0.060, 0.055 | 0.16 |
| controls | W0 | chicken | 100 | 1 | 2000 | 40 | 0.839 ± 0.072 | 0.597 [0.45, 0.74] | 0.594 / 0.393 / 0.000 / 0.000 / 0.013 | 0.475 | 0.525 (530) | 0.525 (600) | 1.73e-03 | 3.38e-03 | 1.740 ± 0.708 | 7.93e-02 | 29.9 | 0.29 | 0.30 | 0.362, 0.519 | 0.79 |
| controls | W0 | chicken | 100 | 1 | 4000 | 40 | 0.776 ± 0.101 | 0.612 [0.46, 0.76] | 0.595 / 0.396 / 0.000 / 0.000 / 0.010 | 0.475 | 0.525 (530) | 0.525 (600) | 1.70e-03 | 3.50e-03 | 1.750 ± 0.709 | 7.96e-02 | 29.9 | 0.29 | 0.30 | 0.379, 0.523 | 0.72 |
| controls | W0 | hd3 | 100 | 0 | 2000 | 40 | 0.998 ± 0.002 | 0.505 [0.48, 0.53] | 0.504 / 0.494 / 0.002 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 1.56e-03 | 3.91e-04 | 0.748 ± 0.008 | 2.49e-01 | 0.0 | – | – | 0.024, 0.017 | 0.02 |
| controls | W0 | hd3 | 100 | 1 | 2000 | 40 | 0.628 ± 0.141 | 0.636 [0.47, 0.80] | 0.537 / 0.348 / 0.000 / 0.000 / 0.115 | 0.425 | 0.575 (540) | 0.525 (600) | 1.20e-02 | 5.67e-03 | 0.234 ± 0.099 | 7.81e-02 | 32.5 | 0.26 | 0.27 | 0.293, 0.434 | 0.83 |
| controls | W0 | hd3 | 100 | 1 | 4000 | 40 | 0.589 ± 0.147 | 0.625 [0.45, 0.80] | 0.535 / 0.347 / 0.000 / 0.000 / 0.118 | 0.400 | 0.600 (540) | 0.525 (600) | 1.21e-02 | 5.82e-03 | 0.232 ± 0.098 | 7.74e-02 | 32.8 | 0.26 | 0.27 | 0.297, 0.451 | 0.81 |
| controls | W0 | hd6 | 100 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.487 [0.47, 0.51] | 0.487 / 0.513 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 1.488 ± 0.013 | 2.48e-01 | 0.0 | 1.00 | 1.00 | 0.026, 0.030 | 0.07 |
| controls | W0 | hd6 | 100 | 1 | 2000 | 40 | 0.441 ± 0.126 | 0.461 [0.30, 0.62] | 0.461 / 0.450 / 0.000 / 0.000 / 0.089 | 0.775 | 0.225 (500) | 0.225 (600) | 6.18e-03 | 1.11e-02 | 0.826 ± 0.187 | 1.38e-01 | 24.9 | 0.30 | 0.31 | 0.462, 0.417 | 0.77 |
| controls | W0 | hd6 | 100 | 1 | 4000 | 40 | 0.358 ± 0.131 | 0.448 [0.26, 0.63] | 0.453 / 0.443 / 0.000 / 0.000 / 0.105 | 0.775 | 0.225 (500) | 0.225 (600) | 6.22e-03 | 1.12e-02 | 0.825 ± 0.187 | 1.37e-01 | 24.9 | 0.30 | 0.31 | 0.471, 0.422 | 0.73 |
| controls | M0 | chicken | 100 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.509 [0.49, 0.53] | 0.509 / 0.491 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 5.242 ± 0.058 | 2.40e-01 | 0.0 | – | – | 0.058, 0.054 | 0.15 |
| controls | M0 | chicken | 100 | 1 | 2000 | 40 | 0.586 ± 0.058 | 0.408 [0.29, 0.53] | 0.464 / 0.502 / 0.000 / 0.000 / 0.035 | 0.975 | 0.025 (450) | 0.025 (500) | 4.23e-03 | 8.90e-03 | 4.347 ± 0.482 | 1.97e-01 | 15.6 | 0.27 | 0.25 | 0.510, 0.467 | 0.79 |
| controls | M0 | chicken | 100 | 1 | 4000 | 40 | 0.428 ± 0.076 | 0.391 [0.26, 0.52] | 0.463 / 0.502 / 0.000 / 0.000 / 0.034 | 0.975 | 0.025 (450) | 0.025 (500) | 4.23e-03 | 9.10e-03 | 4.354 ± 0.480 | 1.98e-01 | 15.6 | 0.27 | 0.25 | 0.514, 0.477 | 0.77 |
| controls | M0 | hd3 | 100 | 0 | 2000 | 40 | 0.999 ± 0.001 | 0.499 [0.48, 0.52] | 0.499 / 0.500 / 0.001 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 7.81e-04 | 0 | 0.748 ± 0.005 | 2.49e-01 | 0.0 | – | – | 0.025, 0.023 | 0.02 |
| controls | M0 | hd3 | 100 | 1 | 2000 | 40 | 0.567 ± 0.144 | 0.529 [0.36, 0.70] | 0.447 / 0.421 / 0.000 / 0.000 / 0.132 | 0.450 | 0.550 (555) | 0.450 (600) | 1.38e-02 | 6.55e-03 | 0.263 ± 0.096 | 8.75e-02 | 29.9 | 0.30 | 0.29 | 0.355, 0.352 | 0.78 |
| controls | M0 | hd3 | 100 | 1 | 4000 | 40 | 0.532 ± 0.148 | 0.481 [0.29, 0.67] | 0.451 / 0.421 / 0.000 / 0.000 / 0.128 | 0.425 | 0.575 (570) | 0.450 (600) | 1.29e-02 | 6.31e-03 | 0.245 ± 0.093 | 8.17e-02 | 30.6 | 0.29 | 0.28 | 0.357, 0.360 | 0.77 |
| controls | M0 | hd6 | 100 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.511 [0.49, 0.53] | 0.511 / 0.489 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 1.481 ± 0.015 | 2.47e-01 | 0.0 | – | – | 0.027, 0.029 | 0.06 |
| controls | M0 | hd6 | 100 | 1 | 2000 | 40 | 0.450 ± 0.125 | 0.484 [0.33, 0.64] | 0.433 / 0.466 / 0.000 / 0.000 / 0.101 | 0.725 | 0.275 (610) | 0.250 (650) | 6.07e-03 | 1.08e-02 | 0.805 ± 0.190 | 1.34e-01 | 24.2 | 0.27 | 0.26 | 0.454, 0.429 | 0.80 |
| controls | M0 | hd6 | 100 | 1 | 4000 | 40 | 0.368 ± 0.132 | 0.423 [0.23, 0.62] | 0.432 / 0.467 / 0.000 / 0.000 / 0.101 | 0.750 | 0.250 (585) | 0.250 (650) | 6.06e-03 | 1.11e-02 | 0.808 ± 0.190 | 1.35e-01 | 24.2 | 0.27 | 0.26 | 0.459, 0.431 | 0.76 |
| controls | const | chicken | 25 | 0 | 2000 | 40 | 0.988 ± 0.004 | 0.508 [0.49, 0.53] | 0.502 / 0.486 / 0.000 / 0.013 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 1.25e-02 | 5.392 ± 0.049 | 2.45e-01 | 0.0 | – | – | 0.000, 0.000 | 0.00 |
| controls | const | chicken | 25 | 1 | 2000 | 40 | 0.001 ± 0.002 | 1.000 [1.00, 1.00] | 0.280 / 0.299 / 0.000 / 0.000 / 0.421 | 1.000 | 0.000 (–) | 0.000 (–) | 1.93e-02 | 5.05e-02 | 4.913 ± 0.166 | 2.22e-01 | 3.5 | 0.00 | 0.00 | 0.000, 0.000 | 0.69 |
| controls | const | chicken | 25 | 1 | 4000 | 40 | 0.013 ± 0.021 | 1.000 [1.00, 1.00] | 0.298 / 0.321 / 0.000 / 0.000 / 0.381 | 0.975 | 0.025 (3930) | 0.000 (–) | 1.83e-02 | 4.80e-02 | 4.516 ± 0.344 | 2.04e-01 | 8.2 | 0.00 | 0.00 | 0.000, 0.000 | 0.63 |
| controls | const | chicken | 50 | 0 | 2000 | 40 | 1.000 ± 0.001 | 0.490 [0.47, 0.51] | 0.489 / 0.510 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 3.91e-04 | 5.526 ± 0.019 | 2.51e-01 | 0.0 | – | – | 0.000, 0.000 | 0.00 |
| controls | const | chicken | 50 | 1 | 2000 | 40 | 0.009 ± 0.004 | 0.531 [0.29, 0.78] | 0.387 / 0.371 / 0.000 / 0.000 / 0.241 | 1.000 | 0.000 (–) | 0.000 (–) | 1.03e-02 | 2.35e-02 | 5.342 ± 0.050 | 2.42e-01 | 0.0 | – | – | 0.000, 0.000 | 0.72 |
| controls | const | chicken | 50 | 1 | 4000 | 40 | 0.000 ± 0.000 | – [–, –] | 0.377 / 0.374 / 0.000 / 0.000 / 0.249 | 1.000 | 0.000 (–) | 0.000 (–) | 1.04e-02 | 2.36e-02 | 5.332 ± 0.056 | 2.42e-01 | 0.0 | – | – | 0.000, 0.000 | 0.70 |
| controls | const | chicken | 100 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.493 [0.47, 0.51] | 0.493 / 0.507 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 5.509 ± 0.031 | 2.50e-01 | 0.0 | – | – | 0.000, 0.000 | 0.00 |
| controls | const | chicken | 100 | 1 | 2000 | 40 | 0.458 ± 0.021 | 0.491 [0.43, 0.55] | 0.480 / 0.482 / 0.000 / 0.000 / 0.037 | 1.000 | 0.000 (–) | 0.000 (–) | 5.26e-03 | 1.14e-02 | 5.410 ± 0.043 | 2.46e-01 | 0.0 | – | – | 0.000, 0.000 | 0.71 |
| controls | const | chicken | 100 | 1 | 4000 | 40 | 0.216 ± 0.021 | 0.485 [0.38, 0.59] | 0.473 / 0.475 / 0.000 / 0.000 / 0.051 | 1.000 | 0.000 (–) | 0.000 (–) | 5.24e-03 | 1.14e-02 | 5.408 ± 0.044 | 2.46e-01 | 0.0 | – | – | 0.000, 0.000 | 0.70 |
| controls | const | hd3 | 25 | 0 | 2000 | 40 | 0.896 ± 0.014 | 0.503 [0.48, 0.53] | 0.451 / 0.445 / 0.095 / 0.009 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 9.49e-02 | 8.98e-03 | 0.881 ± 0.027 | 2.94e-01 | 0.0 | – | – | 0.000, 0.000 | 0.00 |
| controls | const | hd3 | 25 | 1 | 2000 | 40 | 1.000 ± 0.000 | 0.475 [0.31, 0.64] | 0.475 / 0.525 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (150) | 1.000 (300) | 0 | 0 | 0.000 ± 0.000 | 0 | 22.2 | 0.00 | 0.00 | 0.000, 0.000 | 0.00 |
| controls | const | hd3 | 25 | 1 | 4000 | 40 | 1.000 ± 0.000 | 0.475 [0.31, 0.64] | 0.475 / 0.525 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (150) | 1.000 (300) | 0 | 0 | 0.000 ± 0.000 | 0 | 22.2 | 0.00 | 0.00 | 0.000, 0.000 | 0.00 |
| controls | const | hd3 | 50 | 0 | 2000 | 40 | 0.979 ± 0.007 | 0.512 [0.49, 0.53] | 0.502 / 0.478 / 0.021 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 2.07e-02 | 0 | 0.779 ± 0.011 | 2.60e-01 | 0.0 | – | – | 0.000, 0.000 | 0.00 |
| controls | const | hd3 | 50 | 1 | 2000 | 40 | 0.920 ± 0.075 | 0.487 [0.33, 0.65] | 0.480 / 0.496 / 0.000 / 0.000 / 0.023 | 0.025 | 0.975 (990) | 0.900 (1200) | 9.69e-03 | 4.09e-03 | 0.026 ± 0.038 | 8.58e-03 | 33.8 | 0.00 | 0.00 | 0.000, 0.000 | 0.03 |
| controls | const | hd3 | 50 | 1 | 4000 | 40 | 1.000 ± 0.000 | 0.500 [0.34, 0.66] | 0.500 / 0.500 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (995) | 1.000 (1200) | 4.57e-04 | 2.05e-04 | 0.000 ± 0.000 | 0 | 34.5 | 0.00 | 0.00 | 0.000, 0.000 | 0.00 |
| controls | const | hd3 | 100 | 0 | 2000 | 40 | 0.998 ± 0.002 | 0.498 [0.48, 0.52] | 0.498 / 0.501 / 0.002 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 1.56e-03 | 0 | 0.752 ± 0.005 | 2.51e-01 | 0.0 | – | – | 0.000, 0.000 | 0.00 |
| controls | const | hd3 | 100 | 1 | 2000 | 40 | 0.002 ± 0.002 | 0.333 [-0.32, 0.99] | 0.296 / 0.320 / 0.000 / 0.000 / 0.384 | 1.000 | 0.000 (–) | 0.000 (–) | 3.97e-02 | 1.93e-02 | 0.767 ± 0.012 | 2.56e-01 | 0.9 | 0.00 | 0.00 | 0.000, 0.000 | 0.88 |
| controls | const | hd3 | 100 | 1 | 4000 | 40 | 0.000 ± 0.000 | – [–, –] | 0.277 / 0.313 / 0.000 / 0.000 / 0.410 | 1.000 | 0.000 (–) | 0.000 (–) | 3.93e-02 | 1.92e-02 | 0.764 ± 0.015 | 2.55e-01 | 1.6 | 0.00 | 0.00 | 0.000, 0.000 | 0.88 |
| controls | const | hd6 | 25 | 0 | 2000 | 40 | 0.980 ± 0.006 | 0.502 [0.48, 0.52] | 0.492 / 0.488 / 0.000 / 0.020 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 1.99e-02 | 1.446 ± 0.018 | 2.41e-01 | 0.0 | – | – | 0.000, 0.000 | 0.00 |
| controls | const | hd6 | 25 | 1 | 2000 | 40 | 1.000 ± 0.000 | 0.450 [0.29, 0.61] | 0.450 / 0.550 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (420) | 1.000 (500) | 0 | 0 | 0.000 ± 0.000 | 0 | 31.1 | 0.00 | 0.00 | 0.000, 0.000 | 0.00 |
| controls | const | hd6 | 25 | 1 | 4000 | 40 | 1.000 ± 0.000 | 0.450 [0.29, 0.61] | 0.450 / 0.550 / 0.000 / 0.000 / 0.000 | 0.000 | 1.000 (420) | 1.000 (500) | 0 | 0 | 0.000 ± 0.000 | 0 | 31.1 | 0.00 | 0.00 | 0.000, 0.000 | 0.00 |
| controls | const | hd6 | 50 | 0 | 2000 | 40 | 0.998 ± 0.002 | 0.494 [0.47, 0.52] | 0.493 / 0.505 / 0.000 / 0.002 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 1.56e-03 | 1.492 ± 0.015 | 2.49e-01 | 0.0 | – | – | 0.000, 0.000 | 0.00 |
| controls | const | hd6 | 50 | 1 | 2000 | 40 | 0.000 ± 0.001 | 1.000 [–, –] | 0.267 / 0.266 / 0.000 / 0.000 / 0.467 | 1.000 | 0.000 (–) | 0.000 (–) | 2.18e-02 | 4.23e-02 | 1.404 ± 0.023 | 2.34e-01 | 1.9 | 0.00 | 0.00 | 0.000, 0.000 | 0.80 |
| controls | const | hd6 | 50 | 1 | 4000 | 40 | 0.000 ± 0.000 | – [–, –] | 0.271 / 0.279 / 0.000 / 0.000 / 0.450 | 1.000 | 0.000 (–) | 0.000 (–) | 2.15e-02 | 4.15e-02 | 1.358 ± 0.038 | 2.26e-01 | 4.4 | 0.00 | 0.00 | 0.000, 0.000 | 0.78 |
| controls | const | hd6 | 100 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.496 [0.47, 0.52] | 0.496 / 0.504 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 1.491 ± 0.013 | 2.48e-01 | 0.0 | – | – | 0.000, 0.000 | 0.00 |
| controls | const | hd6 | 100 | 1 | 2000 | 40 | 0.026 ± 0.005 | 0.519 [0.36, 0.67] | 0.414 / 0.407 / 0.000 / 0.000 / 0.180 | 1.000 | 0.000 (–) | 0.000 (–) | 1.11e-02 | 2.01e-02 | 1.470 ± 0.010 | 2.45e-01 | 0.0 | – | – | 0.000, 0.000 | 0.80 |
| controls | const | hd6 | 100 | 1 | 4000 | 40 | 0.001 ± 0.001 | 0.667 [0.01, 1.32] | 0.403 / 0.408 / 0.000 / 0.000 / 0.189 | 1.000 | 0.000 (–) | 0.000 (–) | 1.11e-02 | 2.01e-02 | 1.465 ± 0.009 | 2.44e-01 | 0.0 | – | – | 0.000, 0.000 | 0.80 |
| forced +bridges | weak | chicken | 100 | 1 | 2000 | 40 | 0.872 ± 0.068 | 0.455 [0.31, 0.60] | 0.480 / 0.513 / 0.000 / 0.000 / 0.007 | 0.475 | 0.525 (560) | 0.525 (600) | 1.36e-03 | 1.59e-03 | 1.327 ± 0.603 | 6.15e-02 | 42.3 | 0.31 | 0.33 | 0.456, 0.416 | 0.76 |
| forced +bridges | weak | chicken | 100 | 1 | 4000 | 40 | 0.889 ± 0.084 | 0.522 [0.37, 0.68] | 0.520 / 0.473 / 0.000 / 0.000 / 0.008 | 0.375 | 0.625 (570) | 0.650 (600) | 1.05e-03 | 1.63e-03 | 0.968 ± 0.568 | 4.44e-02 | 47.9 | 0.32 | 0.34 | 0.435, 0.470 | 0.64 |
| forced −bridges | weak | chicken | 100 | 1 | 2000 | 40 | 0.430 ± 0.018 | 0.495 [0.47, 0.52] | 0.475 / 0.481 / 0.000 / 0.000 / 0.043 | 1.000 | 0.000 (–) | 0.000 (–) | 5.35e-03 | 1.16e-02 | 5.522 ± 0.008 | 2.51e-01 | 0.0 | – | – | 0.000, 0.000 | 0.72 |
| forced −bridges | weak | chicken | 100 | 1 | 4000 | 40 | 0.189 ± 0.015 | 0.537 [0.50, 0.58] | 0.480 / 0.482 / 0.000 / 0.000 / 0.037 | 1.000 | 0.000 (–) | 0.000 (–) | 5.38e-03 | 1.16e-02 | 5.523 ± 0.008 | 2.51e-01 | 0.0 | – | – | 0.000, 0.000 | 0.71 |
| forced +bridges | weak | hd3 | 100 | 1 | 2000 | 40 | 0.614 ± 0.144 | 0.531 [0.36, 0.71] | 0.446 / 0.426 / 0.000 / 0.000 / 0.127 | 0.400 | 0.600 (620) | 0.450 (650) | 1.47e-02 | 4.50e-03 | 0.327 ± 0.138 | 1.09e-01 | 44.1 | 0.34 | 0.32 | 0.457, 0.472 | 0.86 |
| forced +bridges | weak | hd3 | 100 | 1 | 4000 | 40 | 0.587 ± 0.148 | 0.556 [0.36, 0.75] | 0.463 / 0.429 / 0.000 / 0.000 / 0.107 | 0.450 | 0.550 (600) | 0.500 (700) | 1.42e-02 | 4.52e-03 | 0.320 ± 0.138 | 1.07e-01 | 44.4 | 0.33 | 0.32 | 0.456, 0.476 | 0.83 |
| forced −bridges | weak | hd3 | 100 | 1 | 2000 | 40 | 0.000 ± 0.001 | 0.000 [–, –] | 0.296 / 0.297 / 0.000 / 0.000 / 0.406 | 1.000 | 0.000 (–) | 0.000 (–) | 4.06e-02 | 1.98e-02 | 0.793 ± 0.004 | 2.64e-01 | 0.6 | 0.00 | 0.00 | 0.000, 0.000 | 0.88 |
| forced −bridges | weak | hd3 | 100 | 1 | 4000 | 40 | 0.000 ± 0.000 | – [–, –] | 0.296 / 0.309 / 0.000 / 0.000 / 0.395 | 1.000 | 0.000 (–) | 0.000 (–) | 4.08e-02 | 1.98e-02 | 0.791 ± 0.004 | 2.64e-01 | 1.2 | 0.00 | 0.00 | 0.000, 0.000 | 0.88 |
| forced +bridges | weak | hd6 | 100 | 1 | 2000 | 40 | 0.781 ± 0.118 | 0.550 [0.39, 0.71] | 0.547 / 0.420 / 0.000 / 0.000 / 0.033 | 0.475 | 0.525 (590) | 0.500 (650) | 3.13e-03 | 4.02e-03 | 0.436 ± 0.179 | 7.27e-02 | 37.4 | 0.29 | 0.29 | 0.387, 0.502 | 0.81 |
| forced +bridges | weak | hd6 | 100 | 1 | 4000 | 40 | 0.737 ± 0.131 | 0.559 [0.39, 0.73] | 0.520 / 0.441 / 0.000 / 0.000 / 0.039 | 0.450 | 0.550 (625) | 0.500 (650) | 3.37e-03 | 4.05e-03 | 0.427 ± 0.176 | 7.12e-02 | 44.1 | 0.33 | 0.32 | 0.429, 0.490 | 0.73 |
| forced −bridges | weak | hd6 | 100 | 1 | 2000 | 40 | 0.019 ± 0.005 | 0.540 [0.38, 0.70] | 0.410 / 0.404 / 0.000 / 0.000 / 0.186 | 1.000 | 0.000 (–) | 0.000 (–) | 1.13e-02 | 2.06e-02 | 1.490 ± 0.004 | 2.48e-01 | 0.0 | – | – | 0.000, 0.000 | 0.82 |
| forced −bridges | weak | hd6 | 100 | 1 | 4000 | 40 | 0.000 ± 0.001 | 0.000 [–, –] | 0.409 / 0.421 / 0.000 / 0.000 / 0.170 | 1.000 | 0.000 (–) | 0.000 (–) | 1.13e-02 | 2.06e-02 | 1.496 ± 0.003 | 2.49e-01 | 0.0 | – | – | 0.000, 0.000 | 0.80 |
| forced +bridges | modal | chicken | 100 | 1 | 2000 | 40 | 0.955 ± 0.037 | 0.526 [0.37, 0.69] | 0.515 / 0.483 / 0.000 / 0.000 / 0.002 | 0.450 | 0.550 (660) | 0.525 (700) | 7.63e-04 | 4.52e-05 | 0.604 ± 0.261 | 2.87e-02 | 49.6 | 0.32 | 0.39 | 0.410, 0.399 | 0.72 |
| forced +bridges | modal | chicken | 100 | 1 | 4000 | 40 | 0.994 ± 0.006 | 0.450 [0.29, 0.61] | 0.450 / 0.550 / 0.000 / 0.000 / 0.000 | 0.225 | 0.775 (1050) | 0.800 (1150) | 3.64e-04 | 1.69e-05 | 0.225 ± 0.154 | 1.07e-02 | 63.0 | 0.34 | 0.39 | 0.496, 0.394 | 0.52 |
| forced −bridges | modal | chicken | 100 | 1 | 2000 | 40 | 0.420 ± 0.017 | 0.488 [0.46, 0.51] | 0.480 / 0.481 / 0.000 / 0.000 / 0.039 | 1.000 | 0.000 (–) | 0.000 (–) | 5.39e-03 | 1.16e-02 | 5.526 ± 0.007 | 2.51e-01 | 0.0 | – | – | 0.000, 0.000 | 0.73 |
| forced −bridges | modal | chicken | 100 | 1 | 4000 | 40 | 0.191 ± 0.016 | 0.517 [0.47, 0.56] | 0.479 / 0.477 / 0.000 / 0.000 / 0.044 | 1.000 | 0.000 (–) | 0.000 (–) | 5.37e-03 | 1.16e-02 | 5.524 ± 0.006 | 2.51e-01 | 0.0 | – | – | 0.000, 0.000 | 0.72 |
| forced +bridges | modal | hd3 | 100 | 1 | 2000 | 40 | 0.351 ± 0.122 | 0.394 [0.22, 0.56] | 0.345 / 0.493 / 0.000 / 0.000 / 0.163 | 0.775 | 0.225 (720) | 0.150 (750) | 2.74e-02 | 6.88e-07 | 0.782 ± 0.171 | 2.61e-01 | 61.3 | 0.38 | 0.38 | 0.533, 0.371 | 0.85 |
| forced +bridges | modal | hd3 | 100 | 1 | 4000 | 40 | 0.279 ± 0.121 | 0.423 [0.23, 0.62] | 0.341 / 0.482 / 0.000 / 0.000 / 0.177 | 0.725 | 0.275 (1280) | 0.150 (750) | 2.79e-02 | 0 | 0.805 ± 0.176 | 2.68e-01 | 68.4 | 0.38 | 0.38 | 0.547, 0.391 | 0.74 |
| forced −bridges | modal | hd3 | 100 | 1 | 2000 | 40 | 0.000 ± 0.000 | – [–, –] | 0.299 / 0.302 / 0.000 / 0.000 / 0.399 | 1.000 | 0.000 (–) | 0.000 (–) | 4.06e-02 | 1.99e-02 | 0.792 ± 0.004 | 2.64e-01 | 0.8 | 0.00 | 0.00 | 0.000, 0.000 | 0.88 |
| forced −bridges | modal | hd3 | 100 | 1 | 4000 | 40 | 0.000 ± 0.000 | – [–, –] | 0.287 / 0.300 / 0.000 / 0.000 / 0.413 | 1.000 | 0.000 (–) | 0.000 (–) | 4.04e-02 | 1.98e-02 | 0.790 ± 0.004 | 2.63e-01 | 1.4 | 0.00 | 0.00 | 0.000, 0.000 | 0.89 |
| forced +bridges | modal | hd6 | 100 | 1 | 2000 | 40 | 0.857 ± 0.059 | 0.397 [0.24, 0.56] | 0.388 / 0.596 / 0.000 / 0.000 / 0.016 | 0.725 | 0.275 (920) | 0.200 (900) | 4.36e-03 | 8.98e-05 | 0.535 ± 0.164 | 8.92e-02 | 59.8 | 0.37 | 0.37 | 0.534, 0.285 | 0.68 |
| forced +bridges | modal | hd6 | 100 | 1 | 4000 | 40 | 0.883 ± 0.066 | 0.400 [0.24, 0.56] | 0.440 / 0.549 / 0.000 / 0.000 / 0.011 | 0.700 | 0.300 (980) | 0.225 (1000) | 3.27e-03 | 3.23e-05 | 0.445 ± 0.136 | 7.42e-02 | 74.7 | 0.39 | 0.38 | 0.537, 0.392 | 0.44 |
| forced −bridges | modal | hd6 | 100 | 1 | 2000 | 40 | 0.023 ± 0.006 | 0.389 [0.25, 0.53] | 0.410 / 0.421 / 0.000 / 0.000 / 0.168 | 1.000 | 0.000 (–) | 0.000 (–) | 1.13e-02 | 2.05e-02 | 1.498 ± 0.005 | 2.50e-01 | 0.0 | – | – | 0.000, 0.000 | 0.81 |
| forced −bridges | modal | hd6 | 100 | 1 | 4000 | 40 | 0.000 ± 0.001 | 1.000 [–, –] | 0.411 / 0.409 / 0.000 / 0.000 / 0.180 | 1.000 | 0.000 (–) | 0.000 (–) | 1.12e-02 | 2.05e-02 | 1.491 ± 0.004 | 2.48e-01 | 0.0 | – | – | 0.000, 0.000 | 0.81 |
| swap | weak | chicken | 100 | 0 | 2000 | 40 | 0.935 ± 0.010 | 0.496 [0.47, 0.52] | 0.464 / 0.471 / 0.000 / 0.000 / 0.065 | 1.000 | 0.000 (–) | 0.025 (100) | 0 | 3.18e-02 | 4.984 ± 0.056 | 2.25e-01 | 0.0 | – | – | 0.023, 0.019 | 0.04 |
| swap | weak | chicken | 100 | 1 | 2000 | 40 | 0.780 ± 0.078 | 0.429 [0.29, 0.57] | 0.445 / 0.539 / 0.000 / 0.000 / 0.015 | 0.500 | 0.500 (480) | 0.500 (550) | 2.17e-03 | 4.62e-03 | 2.238 ± 0.774 | 1.02e-01 | 23.8 | 0.26 | 0.27 | 0.420, 0.342 | 0.72 |
| swap | weak | chicken | 100 | 1 | 4000 | 40 | 0.696 ± 0.109 | 0.428 [0.28, 0.58] | 0.443 / 0.542 / 0.000 / 0.000 / 0.015 | 0.500 | 0.500 (480) | 0.500 (550) | 2.18e-03 | 4.69e-03 | 2.235 ± 0.773 | 1.01e-01 | 23.8 | 0.26 | 0.27 | 0.421, 0.343 | 0.72 |
| swap | weak | hd3 | 100 | 0 | 2000 | 40 | 0.767 ± 0.017 | 0.487 [0.47, 0.50] | 0.373 / 0.394 / 0.001 / 0.001 / 0.231 | 1.000 | 0.000 (–) | 0.000 (–) | 1.06e-01 | 8.47e-03 | 0.913 ± 0.016 | 3.04e-01 | 0.0 | – | – | 0.010, 0.011 | 0.00 |
| swap | weak | hd3 | 100 | 1 | 2000 | 40 | 0.602 ± 0.154 | 0.640 [0.45, 0.83] | 0.515 / 0.336 / 0.000 / 0.000 / 0.149 | 0.400 | 0.600 (510) | 0.550 (600) | 1.54e-02 | 7.55e-03 | 0.303 ± 0.121 | 1.01e-01 | 20.1 | 0.25 | 0.25 | 0.154, 0.257 | 0.87 |
| swap | weak | hd3 | 100 | 1 | 4000 | 40 | 0.588 ± 0.155 | 0.640 [0.45, 0.83] | 0.511 / 0.335 / 0.000 / 0.000 / 0.154 | 0.425 | 0.575 (510) | 0.550 (600) | 1.56e-02 | 7.56e-03 | 0.302 ± 0.121 | 1.01e-01 | 20.5 | 0.25 | 0.24 | 0.165, 0.264 | 0.85 |
| swap | weak | hd6 | 100 | 0 | 2000 | 40 | 0.902 ± 0.011 | 0.505 [0.49, 0.52] | 0.455 / 0.447 / 0.000 / 0.000 / 0.098 | 1.000 | 0.000 (–) | 0.000 (–) | 4.39e-04 | 4.65e-02 | 1.359 ± 0.016 | 2.26e-01 | 0.0 | – | – | 0.007, 0.011 | 0.01 |
| swap | weak | hd6 | 100 | 1 | 2000 | 40 | 0.541 ± 0.145 | 0.479 [0.32, 0.64] | 0.456 / 0.445 / 0.000 / 0.000 / 0.099 | 0.525 | 0.475 (600) | 0.450 (700) | 5.16e-03 | 9.30e-03 | 0.675 ± 0.216 | 1.12e-01 | 21.6 | 0.27 | 0.26 | 0.284, 0.284 | 0.79 |
| swap | weak | hd6 | 100 | 1 | 4000 | 40 | 0.501 ± 0.154 | 0.483 [0.30, 0.67] | 0.457 / 0.458 / 0.000 / 0.000 / 0.085 | 0.525 | 0.475 (600) | 0.450 (700) | 5.11e-03 | 9.31e-03 | 0.676 ± 0.216 | 1.13e-01 | 21.6 | 0.27 | 0.26 | 0.284, 0.286 | 0.78 |
| swap | modal | chicken | 100 | 0 | 2000 | 40 | 1.000 ± 0.001 | 0.510 [0.49, 0.53] | 0.510 / 0.490 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 3.91e-04 | 5.042 ± 0.091 | 2.36e-01 | 0.1 | 0.60 | 0.60 | 0.247, 0.253 | 0.62 |
| swap | modal | chicken | 100 | 1 | 2000 | 40 | 0.954 ± 0.042 | 0.455 [0.30, 0.61] | 0.457 / 0.540 / 0.000 / 0.000 / 0.003 | 0.675 | 0.325 (1650) | 0.325 (1300) | 1.17e-03 | 2.13e-05 | 0.790 ± 0.251 | 3.76e-02 | 55.8 | 0.35 | 0.38 | 0.473, 0.405 | 0.73 |
| swap | modal | chicken | 100 | 1 | 4000 | 40 | 0.975 ± 0.017 | 0.476 [0.31, 0.64] | 0.472 / 0.524 / 0.000 / 0.000 / 0.004 | 0.500 | 0.500 (1805) | 0.525 (1800) | 6.46e-04 | 3.06e-05 | 0.577 ± 0.245 | 2.74e-02 | 66.8 | 0.36 | 0.39 | 0.483, 0.463 | 0.57 |
| swap | modal | hd3 | 100 | 0 | 2000 | 40 | 1.000 ± 0.001 | 0.485 [0.47, 0.50] | 0.484 / 0.515 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 3.91e-04 | 0 | 0.764 ± 0.006 | 2.55e-01 | 0.0 | 1.00 | 1.00 | 0.131, 0.116 | 0.11 |
| swap | modal | hd3 | 100 | 1 | 2000 | 40 | 0.366 ± 0.118 | 0.579 [0.42, 0.74] | 0.482 / 0.352 / 0.000 / 0.000 / 0.166 | 0.825 | 0.175 (690) | 0.125 (700) | 2.65e-02 | 1.13e-05 | 0.734 ± 0.162 | 2.45e-01 | 56.1 | 0.38 | 0.38 | 0.405, 0.513 | 0.81 |
| swap | modal | hd3 | 100 | 1 | 4000 | 40 | 0.233 ± 0.116 | 0.591 [0.38, 0.80] | 0.458 / 0.367 / 0.000 / 0.000 / 0.175 | 0.800 | 0.200 (920) | 0.125 (700) | 2.66e-02 | 1.58e-04 | 0.799 ± 0.156 | 2.66e-01 | 62.2 | 0.39 | 0.38 | 0.436, 0.506 | 0.74 |
| swap | modal | hd6 | 100 | 0 | 2000 | 40 | 1.000 ± 0.000 | 0.492 [0.47, 0.51] | 0.492 / 0.508 / 0.000 / 0.000 / 0.000 | 1.000 | 0.000 (–) | 1.000 (100) | 0 | 0 | 1.488 ± 0.018 | 2.48e-01 | 0.1 | 0.25 | 0.25 | 0.153, 0.160 | 0.34 |
| swap | modal | hd6 | 100 | 1 | 2000 | 40 | 0.860 ± 0.057 | 0.472 [0.31, 0.63] | 0.457 / 0.524 / 0.000 / 0.000 / 0.019 | 0.800 | 0.200 (1690) | 0.125 (800) | 5.12e-03 | 9.88e-05 | 0.670 ± 0.191 | 1.12e-01 | 54.3 | 0.37 | 0.36 | 0.490, 0.426 | 0.79 |
| swap | modal | hd6 | 100 | 1 | 4000 | 40 | 0.824 ± 0.073 | 0.524 [0.36, 0.69] | 0.477 / 0.509 / 0.000 / 0.000 / 0.014 | 0.875 | 0.125 (730) | 0.125 (800) | 4.43e-03 | 1.02e-05 | 0.636 ± 0.189 | 1.06e-01 | 65.7 | 0.39 | 0.38 | 0.506, 0.437 | 0.62 |

**One population (modal arm (c)), lottery:**

| game | mN | mark | runs | island classes | max asym | mean asym | crash end | dove end | crash 2nd half | payoff/player | efficiency | top classes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chicken | 0 | 2000 | 40 | dove 0.937, mixed 0.063 | 0.435 | 0.018 | 0.002 | 0.980 | 0.005 | -0.013 | -0.026 | `Swerve`, `not(BOX1(THEM(ME)))`, `not(BOX(THEM(ME)))` |
| chicken | 1 | 2000 | 40 | mixed 0.951, dove 0.049 | 0.749 | 0.512 | 0.070 | 0.418 | 0.070 | -0.441 | -0.882 | `not(BOX1(THEM(ME)))`, `Straight`, `not(BOX1(THEM(THEM)))` |
| chicken | 1 | 4000 | 40 | mixed 0.952, dove 0.048 | 0.742 | 0.513 | 0.070 | 0.417 | 0.069 | -0.443 | -0.886 | `not(BOX1(THEM(ME)))`, `Straight`, `not(BOX1(THEM(THEM)))` |
| hd3 | 0 | 2000 | 40 | crash 0.984, dove 0.016 | 0.000 | 0.000 | 0.984 | 0.016 | 0.984 | -0.477 | -0.477 | `Straight`, `Swerve`, `BOX1(THEM(THEM))` |
| hd3 | 1 | 2000 | 40 | mixed 0.543, dove 0.341, crash 0.116 | 0.500 | 0.198 | 0.403 | 0.399 | 0.403 | 0.395 | 0.395 | `Straight`, `BOX(THEM(THEM))`, `BOX(THEM(ME))` |
| hd3 | 1 | 4000 | 40 | mixed 0.543, dove 0.349, crash 0.108 | 0.500 | 0.198 | 0.397 | 0.405 | 0.397 | 0.404 | 0.404 | `Straight`, `BOX(THEM(THEM))`, `BOX(THEM(ME))` |
| hd6 | 0 | 2000 | 40 | dove 0.816, mixed 0.181, crash 0.003 | 0.500 | 0.075 | 0.049 | 0.876 | 0.059 | 0.853 | 0.853 | `Swerve`, `Straight`, `not(BOX(THEM(ME)))` |
| hd6 | 1 | 2000 | 40 | mixed 0.976, dove 0.024 | 0.667 | 0.506 | 0.176 | 0.318 | 0.175 | 0.472 | 0.472 | `Straight`, `not(BOX1(THEM(THEM)))`, `not(BOX1(THEM(ME)))` |
| hd6 | 1 | 4000 | 40 | mixed 0.977, dove 0.023 | 0.667 | 0.507 | 0.175 | 0.317 | 0.176 | 0.474 | 0.474 | `Straight`, `not(BOX1(THEM(THEM)))`, `not(BOX1(THEM(ME)))` |

**Matched control (W0 vs M0, paired seeds):** per-island establishment difference M0 − W0, mean over paired runs ± 95% t-interval:

| game | mN | mark | pairs | W0 | M0 | M0 − W0 | runs with a difference |
|---|---|---|---|---|---|---|---|
| chicken | 0 | 2000 | 40 | 1.000 | 1.000 | 0.000 ± 0.000 | 0 |
| chicken | 1 | 2000 | 40 | 0.839 | 0.586 | -0.254 ± 0.088 | 39 |
| chicken | 1 | 4000 | 40 | 0.776 | 0.428 | -0.348 ± 0.125 | 37 |
| hd3 | 0 | 2000 | 40 | 0.998 | 0.999 | 0.001 ± 0.002 | 5 |
| hd3 | 1 | 2000 | 40 | 0.628 | 0.567 | -0.061 ± 0.193 | 29 |
| hd3 | 1 | 4000 | 40 | 0.589 | 0.532 | -0.057 ± 0.203 | 26 |
| hd6 | 0 | 2000 | 40 | 1.000 | 1.000 | 0.000 ± 0.000 | 0 |
| hd6 | 1 | 2000 | 40 | 0.441 | 0.450 | 0.009 ± 0.157 | 35 |
| hd6 | 1 | 4000 | 40 | 0.358 | 0.368 | 0.009 ± 0.164 | 30 |

**Island flips** (natural and forced cells pooled by arm and game; winner/loser = the dominant classes before the flip):

Frozen rule (notes §1.7): reader-mediated iff the winner seat's bridge share at the last convention sample ≥ f*. Post-hoc (added after the first main-set cells, labelled): the largest winner-seat bridge share over the flip window ≥ f*; bridges present (> 0) in the winner seat at the last convention sample; flips with no bridge in the winner seat are the demographic candidates.

| cell | arm | game | N | flips | reader-mediated (frozen) | selection-favoured | winner bridge share (median) | post-hoc: window max ≥ f* | bridges present | no bridge | top winner classes before | top loser classes before |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| forced +b | modal | chicken | 100 | 2521 | 0.341 | 0.392 | 0.67 | 1.000 | 1.000 | 0 | `BOXD(THEM(THEM))` 1045, `Straight` 539, `BOXD(THEM(ME))` 268 | `Swerve` 1727, `not(BOX(THEM(ME)))` 244, `BOXD1(THEM(THEM))` 203 |
| forced +b | modal | hd3 | 100 | 2735 | 0.384 | 0.378 | 0.13 | 0.999 | 0.857 | 390 | `Straight` 2586, `BOXD(THEM(THEM))` 50, `BOXD(THEM(ME))` 37 | `Swerve` 1830, `BOXD1(THEM(THEM))` 250, `BOXD1(THEM(ME))` 209 |
| forced +b | modal | hd6 | 100 | 2987 | 0.388 | 0.379 | 0.42 | 1.000 | 0.992 | 25 | `Straight` 1934, `BOXD(THEM(THEM))` 409, `BOXD(THEM(ME))` 312 | `Swerve` 2203, `BOXD1(THEM(THEM))` 258, `BOXD1(THEM(ME))` 164 |
| forced +b | weak | chicken | 100 | 1916 | 0.325 | 0.338 | 0.66 | 1.000 | 0.999 | 1 | `not(THEM(^Straight))` 1192, `Straight` 435, `not(THEM(THEM))` 143 | `Swerve` 1117, `not(THEM(THEM))` 403, `not(THEM(ME))` 389 |
| forced +b | weak | hd3 | 100 | 1777 | 0.334 | 0.322 | 0.10 | 1.000 | 0.831 | 300 | `Straight` 1704, `not(THEM(^Straight))` 36, `not(THEM(ME))` 19 | `Swerve` 1107, `not(THEM(ME))` 332, `not(THEM(THEM))` 299 |
| forced +b | weak | hd6 | 100 | 1765 | 0.326 | 0.320 | 0.38 | 1.000 | 0.983 | 30 | `Straight` 1232, `not(THEM(^Straight))` 371, `not(THEM(ME))` 83 | `Swerve` 1092, `not(THEM(ME))` 356, `not(THEM(THEM))` 313 |
| forced −b | modal | hd3 | 100 | 57 | 0.000 | 0.000 | 0.00 | 0.000 | 0.000 | 57 | `Straight` 57 | `Swerve` 57 |
| forced −b | weak | hd3 | 100 | 47 | 0.000 | 0.000 | 0.00 | 0.000 | 0.000 | 47 | `Straight` 47 | `Swerve` 47 |
| natural | const | chicken | 25 | 328 | 0.000 | 0.000 | 0.00 | 0.000 | 0.000 | 328 | `Straight` 328 | `Swerve` 328 |
| natural | const | hd3 | 25 | 888 | 0.000 | 0.000 | 0.00 | 0.000 | 0.000 | 888 | `Straight` 888 | `Swerve` 888 |
| natural | const | hd3 | 50 | 1382 | 0.000 | 0.000 | 0.00 | 0.000 | 0.000 | 1382 | `Straight` 1382 | `Swerve` 1382 |
| natural | const | hd3 | 100 | 62 | 0.000 | 0.000 | 0.00 | 0.000 | 0.000 | 62 | `Straight` 62 | `Swerve` 62 |
| natural | const | hd6 | 25 | 1244 | 0.000 | 0.000 | 0.00 | 0.000 | 0.000 | 1244 | `Straight` 1244 | `Swerve` 1244 |
| natural | const | hd6 | 50 | 175 | 0.000 | 0.000 | 0.00 | 0.000 | 0.000 | 175 | `Straight` 175 | `Swerve` 175 |
| natural | modal | chicken | 25 | 2721 | 0.229 | 0.257 | 0.44 | 0.990 | 0.888 | 304 | `Straight` 1594, `BOXD(THEM(THEM))` 567, `BOXD(THEM(ME))` 224 | `Swerve` 1640, `BOXD1(THEM(THEM))` 312, `BOXD1(THEM(ME))` 176 |
| natural | modal | chicken | 50 | 2584 | 0.240 | 0.274 | 0.56 | 0.998 | 0.985 | 40 | `Straight` 1215, `BOXD(THEM(THEM))` 785, `BOXD(THEM(ME))` 179 | `Swerve` 1375, `BOXD1(THEM(THEM))` 408, `not(BOX(THEM(ME)))` 182 |
| natural | modal | chicken | 100 | 2761 | 0.350 | 0.368 | 0.68 | 1.000 | 1.000 | 1 | `BOXD(THEM(THEM))` 1252, `Straight` 626, `BOXD(THEM(^D))` 369 | `Swerve` 1208, `BOXD1(THEM(THEM))` 438, `not(BOX(THEM(ME)))` 306 |
| natural | modal | hd3 | 25 | 1227 | 0.196 | 0.171 | 0.00 | 0.954 | 0.429 | 701 | `Straight` 1160, `BOXD(THEM(ME))` 20, `BOXD(THEM(THEM))` 19 | `Swerve` 924, `BOXD1(THEM(ME))` 84, `BOXD1(THEM(THEM))` 50 |
| natural | modal | hd3 | 50 | 2241 | 0.231 | 0.224 | 0.02 | 0.993 | 0.629 | 832 | `Straight` 2109, `BOXD(THEM(THEM))` 54, `BOXD(THEM(ME))` 19 | `Swerve` 1296, `BOXD(THEM(THEM))` 179, `BOXD1(THEM(THEM))` 151 |
| natural | modal | hd3 | 100 | 2577 | 0.357 | 0.346 | 0.12 | 0.999 | 0.867 | 344 | `Straight` 2432, `BOXD(THEM(THEM))` 66, `BOXD(THEM(^D))` 27 | `Swerve` 1622, `BOXD1(THEM(THEM))` 238, `not(BOX1(THEM(ME)))` 206 |
| natural | modal | hd6 | 25 | 2061 | 0.192 | 0.194 | 0.12 | 0.974 | 0.695 | 628 | `Straight` 1684, `BOXD(THEM(THEM))` 187, `BOXD(THEM(ME))` 54 | `Swerve` 1300, `BOXD1(THEM(THEM))` 250, `BOXD1(THEM(ME))` 140 |
| natural | modal | hd6 | 50 | 3147 | 0.286 | 0.273 | 0.30 | 1.000 | 0.907 | 292 | `Straight` 2343, `BOXD(THEM(THEM))` 327, `BOXD(THEM(ME))` 220 | `Swerve` 1789, `BOXD1(THEM(THEM))` 387, `BOXD1(THEM(ME))` 228 |
| natural | modal | hd6 | 100 | 3041 | 0.370 | 0.362 | 0.42 | 1.000 | 0.992 | 25 | `Straight` 2036, `BOXD(THEM(THEM))` 473, `BOXD(THEM(ME))` 191 | `Swerve` 1864, `BOXD1(THEM(THEM))` 393, `not(BOX(THEM(ME)))` 237 |
| natural | weak | chicken | 25 | 1039 | 0.113 | 0.118 | 0.16 | 0.856 | 0.661 | 352 | `Straight` 775, `not(THEM(ME))` 105, `not(THEM(THEM))` 85 | `Swerve` 923, `not(THEM(ME))` 64, `not(THEM(THEM))` 43 |
| natural | weak | chicken | 50 | 1055 | 0.141 | 0.148 | 0.46 | 0.993 | 0.943 | 60 | `Straight` 599, `not(THEM(ME))` 198, `not(THEM(^Straight))` 107 | `Swerve` 1020, `not(THEM(THEM))` 19, `not(THEM(^Swerve))` 9 |
| natural | weak | chicken | 100 | 1114 | 0.283 | 0.279 | 0.64 | 1.000 | 0.999 | 1 | `not(THEM(ME))` 369, `Straight` 277, `not(THEM(THEM))` 248 | `Swerve` 1022, `not(THEM(THEM))` 71, `not(THEM(ME))` 19 |
| natural | weak | hd3 | 25 | 533 | 0.058 | 0.054 | 0.00 | 0.281 | 0.118 | 470 | `Straight` 524, `not(THEM(THEM))` 6, `not(THEM(ME))` 3 | `Swerve` 532, `not(and(X,THEM(ME)))` 1 |
| natural | weak | hd3 | 50 | 1139 | 0.044 | 0.044 | 0.00 | 0.408 | 0.182 | 932 | `Straight` 1131, `not(THEM(ME))` 3, `not(THEM(THEM))` 2 | `Swerve` 1075, `not(THEM(ME))` 46, `not(THEM(THEM))` 17 |
| natural | weak | hd3 | 100 | 886 | 0.252 | 0.243 | 0.06 | 0.977 | 0.709 | 258 | `Straight` 844, `not(THEM(ME))` 24, `not(THEM(THEM))` 13 | `Swerve` 861, `not(THEM(THEM))` 14, `not(THEM(ME))` 9 |
| natural | weak | hd6 | 25 | 1014 | 0.025 | 0.025 | 0.00 | 0.311 | 0.184 | 827 | `Straight` 988, `not(THEM(THEM))` 14, `not(THEM(ME))` 9 | `Swerve` 1002, `not(THEM(^Swerve))` 6, `not(THEM(THEM))` 4 |
| natural | weak | hd6 | 50 | 972 | 0.146 | 0.134 | 0.10 | 0.937 | 0.701 | 291 | `Straight` 838, `not(THEM(ME))` 71, `not(THEM(THEM))` 24 | `Swerve` 931, `not(THEM(THEM))` 20, `not(THEM(ME))` 12 |
| natural | weak | hd6 | 100 | 1006 | 0.285 | 0.279 | 0.37 | 1.000 | 0.973 | 27 | `Straight` 729, `not(THEM(THEM))` 150, `not(THEM(ME))` 74 | `Swerve` 955, `not(THEM(ME))` 36, `not(THEM(THEM))` 10 |


## Verdicts (against `predictions/2026-10-11-fixed-role-chicken.md`)

Numbers are from the tables above; "N = 100" lottery cells unless stated; the chain and the lottery are scored
separately.

| # | prediction | outcome |
|---|---|---|
| RS | some islands learn norms where one role wins the straight play and the other swerves (chicken; scored on per-island establishment of a one-sided norm by play) | **Held.** At mN = 0 in chicken the per-island establishment probability is 0.941 ± 0.008 (weak), 1.000 (modal), 1.000 (W0, M0, constants), and 0.74 / 0.85 at N = 25 / 50 in the weak arm; every cell of every game and arm has a positive fraction (minimum 0.481, weak hd3 N = 25). The norm is not learned through reading: the constants-only control establishes it at 0.988–1.000. With migration (mN = 1) the norms are still one-sided on 0.98–1.00 of chicken islands at the horizon, but islands flip and the metapopulation tends to one global norm (below). |
| RE 1 | mN = 0: per-island ≥ 0.6 (bet ≥ 0.9) everywhere; split in [0.25, 0.75]; constants already produce the norms; reading changes the probability by ≤ 0.1 | **Falsifier fired in one cell** (weak hd3 N = 25: 0.481 < 0.6); every other cell ≥ 0.618, the N = 100 cells ≥ 0.785. Split held everywhere ([0.46, 0.53] per cell). Constants clause held (0.896–1.000). The ≤ 0.1 reading clause **missed**: weak minus constants is −0.06 (chicken), −0.21 (hd3), −0.10 (hd6) at N = 100 and −0.41 in hd3 at N = 25. The effect is not reading but the coin: islands whose seat loses every pure class freeze on an X-mixture (e.g. `Straight` | `X`, half crash); the modal arm (no X) is at 0.998–1.000. The ≥ 0.9 bet missed in weak hd3 (0.785). |
| RE 2 | mN = 1: ≥ 0.4 of runs still patchworks at 4,000; resolutions demographic, not reader-mediated; removing bridges changes resolution by ≤ 0.1. Falsifier: ≤ 0.1 patchworks, or bridges removed cutting resolutions by ≥ 0.4 | **Falsifier fired (bridge clause).** Patchworks at 4,000: weak 0.575 / 0.500 / 0.325, modal 0.325 / 0.875 / 0.800 (chicken / hd3 / hd6): the ≥ 0.4 bet held in 4 of 6 cells and the ≤ 0.1 falsifier did not fire at N = 100 (it holds at N ≤ 50 in hawk–dove, where patchworks resolve). Forced islands: resolution with bridges 0.625 / 0.550 / 0.550 (weak), 0.775 / 0.275 / 0.300 (modal) against **0 / 0 / 0 without bridges**; the cut is ≥ 0.4 in four of six cells. Without bridges chicken and hd6 have no flip at all and hd3 has 1.2–1.4 demographic flips per run that never resolve a patchwork. Post hoc, in the natural cells the winner seat's bridge share reached f* within the flip window in 0.98–1.00 of flips. Resolution is reader-mediated at N = 100; demographic takeover operates only at N ≤ 50 in the constants control (hd3, hd6 resolve 1.00 at N = 25) and in chicken at N = 25 (8 flips per run, no resolution). |
| RE 3 | π splits between the conventions; neutral neighbourhoods; exits by neutral entry then a strict switch (∝ 1/N) in chicken, possibly through a polymorphic trap in hawk–dove; no cycle; crash ≤ 0.05 | **Held**, except the hawk–dove trap clause, which cannot occur (Lemma F: within a role selection is constant, so the two-population chain has no polymorphic states). π(R1) = π(R2) exactly; conventions 0.998–1.000 of π; crash 0; N·exit constant in N (weak 1.06–1.10·10⁻³, modal 1.47·10⁻², W0 2.26–2.36·10⁻³, M0 2.06·10⁻³ at N = 10³–10⁴, the same in the three games); the decisive path is a bridge drifting into the winner seat (N·ρ = 1), then the loser's Straight (Δ = T − S, N·ρ = 593 chicken / 451 hawk–dove at N = 10³). Constants-only exits are deleterious (N·exit 10⁻²⁵ at N = 100 in chicken, 10⁻⁶⁴ at 10³ in hd3). |
| RE 4 | matched W0/M0, paired seeds: per-island convention probabilities within 0.1 (falsifier ≥ 0.25) | **Held at mN = 0** (differences 0.000, 0.001, 0.000). **Falsifier fired at mN = 1 in chicken**: M0 − W0 = −0.254 ± 0.088 at 2,000 and −0.348 ± 0.125 at 4,000 (patchworks resolve in 0.525 of W0 runs and 0.025 of M0 runs). hd3 and hd6 within 0.06. Provable commitment does not change which norm an island learns; in chicken the provability arm's norms merge far less under migration (half the flips per run, 15.6 against 29.9). |
| RE 5 | hd6 convention probabilities within 0.1 of chicken's; a lower on-island crash rate at C = 6 (falsifier: a difference ≥ 0.25, or a higher crash rate at C = 6) | **Falsifier fired (crash clause, against chicken).** Convention probabilities: within 0.04 at mN = 0 and 0.03 at mN = 1 in both arms (held). On-island crash rate at mN = 1, second half: weak 2.2·10⁻³ (chicken) < 3.2·10⁻³ (hd6) < 1.7·10⁻² (hd3); modal 5.5·10⁻⁴ < 4.5·10⁻³ < 2.8·10⁻². The C = 6 hawk–dove crashes more than chicken and less than C = 3: crash exposure falls with the crash's cost, because a cheaper crash removes a loser-seat Straight migrant more slowly. |
| S1 | one closed Δ ≥ 0 class containing both conventions in every reader arm; two in the constants arm | **Held** (every arm and game). |
| S2 | π(R1) = π(R2) to 10⁻⁶; conventions ≥ 0.98 at N ≥ 10³, ≥ 0.95 at 10²; crash ≤ 10⁻³ | **Held** (conventions ≥ 0.997, crash 0, asymmetry < 10⁻¹²). |
| S3 | N·exit ≈ ½ μ_B within ×1.5; ≥ 0.9 of exit flux through bridge winners | **Number held** (weak 1.10·10⁻³ vs 9.3·10⁻⁴; modal 1.48·10⁻² vs 1.55·10⁻²; W0 2.34·10⁻³ and M0 2.07·10⁻³ vs 1.98·10⁻³). **Falsifier fired for the flux clause** in weak (0.85–0.87) and W0 (0.86–0.87): the rest leaves through soft commitments such as `and(THEM(THEM),Straight)` (firm against constants, swerving against readers by the minimax default) taken to mutual swerve by a role-2 reader. Modal 0.98, M0 0.94. |
| S4 | mN = 0: ≥ 0.97 at N = 100, ≥ 0.9 at N = 25; split 0.5 ± 0.06; dove/crash ≤ 0.02 | **Falsifier fired** (weak hd3 0.785 < 0.9 at N = 100; weak chicken 0.941 and hd6 0.903 miss the 0.97 bet). Modal, W0, M0 and constants held at N = 100 (≥ 0.998). Splits held. Crash islands 0.084–0.095 in hd3 at N = 25 (modal, constants). |
| S5 | ≥ 0.8 of flips reader-mediated (frozen rule); patchwork persistence ordered chicken ≥ hd6 ≥ hd3 | **Falsifier fired on both.** By the frozen rule (bridge share ≥ f* at the last convention sample) 0.25–0.37 of flips are reader-mediated: the rule samples before the coupled process starts (a few migrant Straights in the loser seat select bridges over firm Straight in the winner seat, then the loser's Straight takes over). Post hoc (window maximum) 0.98–1.00, and the forced control confirms the mechanism. The ordering failed: modal hd3 0.875 against chicken 0.325 (hd3's islands churn under a bridge load in both seats, est 0.22). |
| S6 | no flips without bridges at N = 100; flips with bridges in every modal game; difference ≥ 0.4 somewhere | **Falsifier fired** (hd3 without bridges: 1.2–1.4 demographic flips per run, in more than one run). Flips with bridges in every modal game: held. Difference ≥ 0.4: held (four cells). |
| S7 | constants: N = 100 permanent patchworks with 0 flips; hd3 N = 25 demographic flips; none in chicken or hd6 at any N | **Falsifier fired.** hd3 at N = 100 has flips (0.9–1.6 per run; patchworks stay at 1.00). Chicken at N = 25 has 8.2 flips per run (through the winner seat drifting to Swerve under migration, a route my hand estimate ignored), hd6 resolves at N = 25 (1.00, 31 flips per run) and flips at N = 50 (4.4 per run). hd3 N = 25 flips: held (22 per run, resolution 1.00). |
| S8 | W0 vs M0 within 0.03 at mN = 0 and 0.1 at mN = 1 | **mN = 0 held; mN = 1 missed** in chicken (−0.35); the stated falsifier (≥ 0.1 at mN = 0) did not fire. |
| S9 | one population, modal: no one-sided norm; π-weighted mutual dove ≤ 0.5 | No one-sided norm: **held** (no island or chain state reaches an asymmetric probability of 0.95: islands at most 0.75, chain states 0.34–0.69), but the hand reason (asymmetric outcome ≤ ½ by arithmetic) is **wrong**: distinct readers anti-coordinate pairwise, so a population of several readers can exceed ½ (up to 1 − Σx²); the chain reaches 0.64–0.69 at N = 100. **Falsifier fired** on mutual dove: chicken 0.544 and hd6 0.549 at N = 10⁴ (mutual swerve inside deep Löbian polymorphisms, not a matcher-held state); hd3 0.000 (a hawk-heavy polymorphism at payoff 0.016). |
| S10 | crash rate chicken < hd6 < hd3 | **Held** in both arms. |
| S11 | exact mirror; role-swapped role-1 share within the unswapped interval and 0.5 ± 0.06 | Mirror test **held**. The ± 0.1 falsifier **fired as worded** in individual mN = 1 cells (e.g. modal chicken 0.697 [0.55, 0.84] unswapped, 0.45 swapped; W0 hd3 0.63), because at mN = 1 islands within a run share one norm and the run is the unit; across ~30 such cells one interval excluding 0.5 is expected, the swapped and unswapped cells disagree in sign, and every mN = 0 split is in [0.46, 0.53]. No implementation asymmetry. |

## Reading

- **The RS's prediction holds, and it is plain anti-coordination.** With fixed roles every island of the seed lottery
  without migration learns a one-sided norm (≥ 0.94 in chicken, ≥ 0.998 without the coin), split evenly between
  the roles; the constants-only control does the same. Source reading neither creates nor changes the norm (W0 = M0
  at mN = 0); the weak arm's shortfall is islands frozen on a coin-flipping seat.
- **The commitment is held by firmness and opened by conditional straights.** In program space neither convention is
  drift-closed: a bridge (straight iff you would swerve, the program-equilibrium best responder) is neutral in both
  seats of both conventions, drifts into the winner's seat at μ_B/N, and lets the loser's Straight take the seat
  (Δ = T − S). Exits are ∝ 1/N with N·exit ≈ ½ μ_B; π is ½/½ by symmetry; without bridges the conventions are strict
  and exits are exponential. "Straight is credible" in the sense that the firm constant is the only uninvadable
  winner; the readers that read it are what unseat it.
- **Migration merges the norms through the bridges, not by demography.** At mN = 1, N = 100, islands flip 22–76
  times per run and 0.13–0.68 of runs (0.125–0.675 per cell) resolve to one global norm by 4,000 generations; with bridges removed from
  forced opposite-norm islands nothing resolves (chicken and hd6: no flip at all). The flip is a coupled two-seat
  process: migrant Straights in the loser seat select bridges over firm Straight in the winner seat (they swerve
  instead of crashing), and once the winner seat is bridge-rich the loser's Straight wins. Demographic takeover
  appears only in small islands (N ≤ 50) and resolves hawk–dove patchworks there. Bridges are the universality
  mechanism here as in RESULTS "Rival networks across islands"; the norm that wins is a coin flip.
- **The crash's cost sets crash exposure inversely.** Cheaper crashes (hd3) linger: on-island crash at mN = 1 is
  ordered chicken < hd6 < hd3 in both arms, and hd3's islands churn under a bridge load in both seats.
- **One population cannot learn the norm and pays for it.** Without fixed roles or `ROLE` the modal arm's ε→0 chain
  sits in many-class Löbian polymorphisms: deep in chicken and hd3 (top-state exits 10⁻³⁸¹ and 10⁻⁷⁴ per event at
  N = 10⁴), a fast-mixing mutual-swerve family in hd6; payoff per player −0.10 (chicken), 0.02 (hd3), 0.83 (hd6),
  against the fixed-role conventions' 0.5, 1, 1. Twin drift matters there (lumped chicken
  −0.40 vs twin-expanded −0.10), as in the solver audit.

