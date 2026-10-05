# Proof-carrying contracts v1 (finite-size mechanism results)

Spec `specs/2026-10-04-proof-carrying-contracts.md`; predictions `predictions/2026-10-04-proof-carrying-contracts.md`. Code: `src/contracts.py` (alphabet, validity, evaluator, audit), `src/contracts_static.py`, `src/contracts_abm.py`, this report `src/contracts_report.py`. Raw: `runs/contracts_static.json`, `runs/contracts_grid.json`, `runs/contracts_lottery.json`, `runs/contracts_types.npz`.

Swapping is a second operator outside the ε→0 chain, so nothing here is π or a limit; finite-ε runs are approach rates at fixed N.

## Static

- Language n = 8: 19544 programs, 610 canonical sources, 471 free-game classes, free GL stable by world 7.
- Truth-table reading (all carriers, synchronous from the GL play): period 4, 58996 of 372100 entries divergent. So contracts are read through GL (predictions, semantics 1).
- Contract alphabet |C| = 471 (behavioural classes); 14 policy-duplicate groups (same stable row, different columns).
- Validity: 1022 valid (source, contract) pairs; every source is valid for its own signature (610 / 610). Sources by number of valid contracts: [0, 427, 48, 83, 10, 42] (index = count).
- Types: 1632 (610 non-carriers + valid carriers). Self-cooperating contracts: 237. Tags (C against exactly one contract, itself): 0.

### Compatibility (breadth = number of sources valid for the contract; μ = their prior mass)

| contract | breadth | μ of valid sources | μ of own class | self-coop | cooperates with (of 471) | valid sources (top by μ) |
|---|---|---|---|---|---|---|
| `<D>` | 37 | 0.4666 | 0.4665 | 0 | 0 | `D`, `and(BOX1(THEM(THEM)),BOXD1(THEM(THEM)))`, `and(BOXD(THEM(THEM)),BOX1(THEM(THEM)))`, `and(BOXD(THEM(THEM)),BOX1(THEM(ME)))`, `and(BOXD(THEM(ME)),BOX1(THEM(THEM)))` |
| `<and(BOX1(THEM(ME)),BOXD1(THEM(ME)))>` | 37 | 0.4666 | 1.79e-05 | 0 | 0 | `D`, `and(BOX1(THEM(THEM)),BOXD1(THEM(THEM)))`, `and(BOXD(THEM(THEM)),BOX1(THEM(THEM)))`, `and(BOXD(THEM(ME)),BOX1(THEM(ME)))`, `and(BOX(THEM(THEM)),BOXD1(THEM(THEM)))` |
| `<and(BOXD(THEM(ME)),BOX1(THEM(ME)))>` | 35 | 0.4666 | 2.063e-05 | 0 | 0 | `D`, `and(BOX1(THEM(THEM)),BOXD1(THEM(THEM)))`, `and(BOXD(THEM(THEM)),BOX1(THEM(THEM)))`, `and(BOXD(THEM(ME)),BOX1(THEM(ME)))`, `and(BOX(THEM(THEM)),BOXD1(THEM(THEM)))` |
| `<and(BOX(THEM(ME)),BOXD1(THEM(ME)))>` | 35 | 0.4666 | 3.58e-05 | 0 | 0 | `D`, `and(BOX1(THEM(THEM)),BOXD1(THEM(THEM)))`, `and(BOXD(THEM(THEM)),BOX1(THEM(THEM)))`, `and(BOXD(THEM(ME)),BOX1(THEM(ME)))`, `and(BOX(THEM(THEM)),BOXD1(THEM(THEM)))` |
| `<and(BOX(THEM(ME)),BOXD(THEM(ME)))>` | 35 | 0.4666 | 4.126e-05 | 0 | 0 | `D`, `and(BOX1(THEM(THEM)),BOXD1(THEM(THEM)))`, `and(BOXD(THEM(THEM)),BOX1(THEM(THEM)))`, `and(BOXD(THEM(ME)),BOX1(THEM(ME)))`, `and(BOX(THEM(THEM)),BOXD1(THEM(THEM)))` |
| `<not(and(BOX1(THEM(ME)),BOXD1(THEM(ME))))>` | 19 | 0.4665 | 2.728e-06 | 1 | 471 | `C`, `or(BOXD1(THEM(ME)),not(BOXD(THEM(ME))))`, `or(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))`, `or(BOX1(THEM(ME)),not(BOX(THEM(ME))))`, `or(BOXD(THEM(THEM)),not(BOXD(THEM(ME))))` |
| `<BOX(THEM(ME))>` | 7 | 0.005089 | 0.005084 | 1 | 126 | `BOX(THEM(ME))`, `BOX(THEM(^BOX(THEM(ME))))`, `and(BOX(THEM(ME)),BOX1(THEM(ME)))`, `and(BOX(THEM(ME)),not(BOXD(THEM(ME))))`, `and(BOX(THEM(ME)),not(BOXD(THEM(THEM))))` |
| `<C>` | 17 | 0.4665 | 0.4665 | 1 | 471 | `C`, `or(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))`, `or(BOX1(THEM(ME)),not(BOX(THEM(ME))))`, `not(and(BOX1(THEM(THEM)),BOXD1(THEM(THEM))))`, `not(and(BOX1(THEM(ME)),BOXD1(THEM(ME))))` |
| `<and(BOX1(THEM(ME)),not(BOX(THEM(ME))))>` | 2 | 2.728e-06 | 2.728e-06 | 1 | 36 | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))`, `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` |
| `<and(BOX(THEM(ME)),BOXD1(THEM(^D)))>` | 1 | 1.364e-06 | 1.364e-06 | 1 | 15 | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` |
| `<BOX1(THEM(ME))>` | 6 | 0.005088 | 0.005085 | 1 | 144 | `BOX1(THEM(ME))`, `BOX1(THEM(^BOX1(THEM(ME))))`, `or(BOX(THEM(ME)),BOX1(THEM(ME)))`, `and(BOX1(THEM(ME)),not(BOXD(THEM(ME))))`, `and(BOX1(THEM(ME)),not(BOXD1(THEM(ME))))` |
| `<BOX(THEM(THEM))>` | 6 | 0.005058 | 0.005053 | 1 | 117 | `BOX(THEM(THEM))`, `and(BOX(THEM(THEM)),BOX1(THEM(THEM)))`, `and(BOX(THEM(THEM)),not(BOXD(THEM(ME))))`, `and(BOX(THEM(THEM)),not(BOXD(THEM(THEM))))`, `and(BOX(THEM(THEM)),not(BOXD1(THEM(ME))))` |
| `<BOX1(THEM(THEM))>` | 4 | 0.005055 | 0.005053 | 1 | 153 | `BOX1(THEM(THEM))`, `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`, `and(BOX1(THEM(THEM)),not(BOXD(THEM(THEM))))`, `and(BOX1(THEM(THEM)),not(BOXD1(THEM(THEM))))` |

Broadest self-cooperating contracts (breadth, μ): `<not(and(BOX1(THEM(ME)),BOXD1(THEM(ME))))>` 19 (0.466); `<C>` 17 (0.466); `<not(and(BOX(THEM(ME)),BOXD(THEM(ME))))>` 17 (0.466); `<not(and(BOX(THEM(ME)),BOXD1(THEM(ME))))>` 17 (0.466); `<not(and(BOXD(THEM(ME)),BOX1(THEM(ME))))>` 17 (0.466); `<BOX(THEM(ME))>` 7 (0.00509); `<BOX1(THEM(ME))>` 6 (0.00509); `<BOX(THEM(THEM))>` 6 (0.00506); `<or(BOXD(THEM(ME)),not(BOX(THEM(ME))))>` 6 (0.0013); `<or(BOXD(THEM(ME)),not(BOX(THEM(THEM))))>` 6 (0.0013).

### Gate (joint fixed point) and the certified-implication audit

| b | rounds | cycle | masked type pairs | masked non-carrier pairs | self-coop non-carrier classes (of 287 free) | μ of those | FB / PrudentBot / P* self-coop as non-carriers | contract reads | box true | violations | source reads (legible / masked) | source violations | carrier pairs off-table |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| inf | 1 | False | 0 | 0 | 287 | 0.49709 | 1 / 1 / 1 | 2452800 | 566032 | 0 | 1947072 / 0 | 0 | 0 |
| 4 | 6 | True | 611289 | 169746 | 253 | 0.49699 | 1 / 1 / 1 | 2452800 | 566032 | 0 | 1308948 / 638124 | 0 | 0 |
| 2 | 7 | True | 967975 | 277479 | 212 | 0.49688 | 1 / 1 / 0 | 2452800 | 566032 | 0 | 943144 / 1003928 | 0 | 0 |

## Finite-ε runs, well-mixed, N = 6,400 (ε = 10⁻³ per birth, w = 0.3, 10⁵ generations, second half)


### Start: μ seed

| b | s | f₀ | σ | start | P(C,C) per seed | mean | carrier | FB-con share | P*-con share | max con share | top contract | FB-label share | max label share | src-ALLC load | con-ALLC load | anti-prover share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 0 | 0 | 0 | mu | 0.99, 0.99, 0.99 | 0.991 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 0.000 | 0.182 | 0.000 | 0.000 |
| 2 | 0 | 0.01 | 0 | mu | 0.96, 0.98, 0.99 | 0.979 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 0.000 | 0.208 | 0.000 | 0.000 |
| 2 | 0 | 0.01 | 0.1 | mu | 0.99, 0.99, 0.95 | 0.978 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.197 | 0.000 | 0.000 |
| 2 | 0 | 0.01 | 1 | mu | 0.99, 0.98, 0.96 | 0.977 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.202 | 0.000 | 0.000 |
| 2 | 0 | 1 | 0 | mu | 0.95, 0.99, 0.97 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.333 | 1.000 | 0.204 | 0.000 | 0.000 |
| 2 | 0 | 1 | 0.1 | mu | 0.87, 0.99, 0.99 | 0.952 | 0.044 | 0.061 | 0.000 | 0.061 | `<BOX(THEM(ME))>` 0.06 | 0.000 | 1.000 | 0.218 | 0.000 | 0.000 |
| 2 | 0 | 1 | 1 | mu | 0.99, 0.89, 0.98 | 0.956 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.155 | 0.000 | 0.000 |
| 2 | 1 | 0 | 0 | mu | 0.91, 0.99, 0.99 | 0.964 | 0.685 | 0.124 | 0.000 | 0.768 | `<C>` 0.27 | 0.124 | 0.768 | 0.189 | 0.189 | 0.000 |
| 2 | 1 | 0 | 0.1 | mu | 0.98, 0.98, 0.99 | 0.985 | 1.000 | 0.443 | 0.000 | 0.709 | `<BOX(THEM(ME))>` 0.44 | 0.002 | 0.686 | 0.235 | 0.235 | 0.000 |
| 2 | 1 | 0 | 1 | mu | 0.99, 0.98, 0.99 | 0.988 | 1.000 | 0.502 | 0.000 | 0.722 | `<BOX(THEM(ME))>` 0.50 | 0.000 | 1.000 | 0.225 | 0.225 | 0.000 |
| 2 | 1 | 0.01 | 0 | mu | 0.99, 0.99, 0.91 | 0.962 | 0.840 | 0.095 | 0.000 | 0.726 | `<BOX(THEM(THEM))>` 0.39 | 0.095 | 0.726 | 0.246 | 0.246 | 0.000 |
| 2 | 1 | 0.01 | 0.1 | mu | 0.99, 0.89, 0.99 | 0.957 | 1.000 | 0.560 | 0.000 | 0.753 | `<BOX(THEM(ME))>` 0.56 | 0.004 | 0.755 | 0.214 | 0.214 | 0.000 |
| 2 | 1 | 0.01 | 1 | mu | 0.99, 0.94, 0.94 | 0.956 | 1.000 | 0.312 | 0.000 | 0.702 | `<BOX(THEM(THEM))>` 0.36 | 0.000 | 1.000 | 0.257 | 0.257 | 0.000 |
| 2 | 1 | 1 | 0 | mu | 0.97, 0.99, 0.96 | 0.975 | 1.000 | 0.289 | 0.000 | 0.728 | `<BOX(THEM(ME))>` 0.29 | 0.289 | 0.728 | 0.241 | 0.241 | 0.000 |
| 2 | 1 | 1 | 0.1 | mu | 0.97, 0.99, 0.99 | 0.980 | 1.000 | 0.294 | 0.000 | 0.684 | `<BOX1(THEM(ME))>` 0.31 | 0.014 | 0.698 | 0.252 | 0.252 | 0.000 |
| 2 | 1 | 1 | 1 | mu | 0.99, 0.94, 0.92 | 0.952 | 1.000 | 0.281 | 0.000 | 0.717 | `<BOX(THEM(ME))>` 0.28 | 0.000 | 1.000 | 0.255 | 0.255 | 0.000 |
| 4 | 0 | 0 | 0 | mu | 0.93, 0.99, 0.97 | 0.963 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 0.000 | 0.249 | 0.000 | 0.000 |
| 4 | 0 | 0.01 | 0 | mu | 0.99, 0.98, 0.99 | 0.984 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 0.000 | 0.261 | 0.000 | 0.000 |
| 4 | 0 | 0.01 | 0.1 | mu | 0.95, 0.99, 0.94 | 0.959 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.270 | 0.000 | 0.000 |
| 4 | 0 | 0.01 | 1 | mu | 0.99, 0.99, 0.99 | 0.989 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.255 | 0.000 | 0.000 |
| 4 | 0 | 1 | 0 | mu | 0.99, 0.99, 0.98 | 0.987 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.333 | 1.000 | 0.243 | 0.000 | 0.000 |
| 4 | 0 | 1 | 0.1 | mu | 0.99, 0.99, 0.96 | 0.979 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.190 | 0.000 | 0.000 |
| 4 | 0 | 1 | 1 | mu | 0.99, 0.98, 0.84 | 0.933 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.259 | 0.000 | 0.000 |
| 4 | 1 | 0 | 0 | mu | 0.91, 0.99, 0.99 | 0.964 | 1.000 | 0.203 | 0.000 | 0.721 | `<BOX(THEM(THEM))>` 0.47 | 0.203 | 0.721 | 0.254 | 0.254 | 0.000 |
| 4 | 1 | 0 | 0.1 | mu | 0.99, 0.99, 0.99 | 0.991 | 1.000 | 0.519 | 0.000 | 0.750 | `<BOX(THEM(ME))>` 0.52 | 0.005 | 0.731 | 0.222 | 0.222 | 0.000 |
| 4 | 1 | 0 | 1 | mu | 0.99, 0.99, 0.94 | 0.975 | 1.000 | 0.431 | 0.000 | 0.737 | `<BOX(THEM(ME))>` 0.43 | 0.000 | 1.000 | 0.225 | 0.225 | 0.000 |
| 4 | 1 | 0.01 | 0 | mu | 0.92, 0.99, 0.87 | 0.925 | 1.000 | 0.527 | 0.000 | 0.736 | `<BOX(THEM(ME))>` 0.53 | 0.527 | 0.736 | 0.251 | 0.251 | 0.000 |
| 4 | 1 | 0.01 | 0.1 | mu | 0.99, 0.99, 0.97 | 0.981 | 1.000 | 0.053 | 0.000 | 0.660 | `<BOX(THEM(THEM))>` 0.33 | 0.004 | 0.692 | 0.266 | 0.266 | 0.000 |
| 4 | 1 | 0.01 | 1 | mu | 0.99, 0.99, 0.99 | 0.990 | 1.000 | 0.311 | 0.000 | 0.708 | `<BOX(THEM(ME))>` 0.31 | 0.000 | 1.000 | 0.240 | 0.240 | 0.000 |
| 4 | 1 | 1 | 0 | mu | 0.99, 0.99, 0.96 | 0.981 | 1.000 | 0.076 | 0.000 | 0.679 | `<BOX1(THEM(ME))>` 0.59 | 0.076 | 0.679 | 0.283 | 0.283 | 0.000 |
| 4 | 1 | 1 | 0.1 | mu | 0.98, 0.99, 0.99 | 0.985 | 1.000 | 0.398 | 0.000 | 0.698 | `<BOX(THEM(ME))>` 0.40 | 0.008 | 0.712 | 0.238 | 0.238 | 0.000 |
| 4 | 1 | 1 | 1 | mu | 0.89, 0.99, 0.99 | 0.958 | 1.000 | 0.468 | 0.000 | 0.733 | `<BOX(THEM(ME))>` 0.47 | 0.333 | 1.000 | 0.237 | 0.237 | 0.000 |
| inf | 0 | 0 | 0 | mu | 0.99, 0.99, 0.99 | 0.991 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 0.000 | 0.167 | 0.000 | 0.000 |
| inf | 0 | 0.01 | 0 | mu | 0.99, 0.99, 0.99 | 0.991 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 0.000 | 0.233 | 0.000 | 0.000 |
| inf | 0 | 0.01 | 0.1 | mu | 0.99, 0.99, 0.99 | 0.991 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.191 | 0.000 | 0.000 |
| inf | 0 | 0.01 | 1 | mu | 0.98, 0.94, 0.99 | 0.968 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.227 | 0.000 | 0.000 |
| inf | 0 | 1 | 0 | mu | 0.99, 0.99, 0.95 | 0.978 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.279 | 0.000 | 0.000 |
| inf | 0 | 1 | 0.1 | mu | 0.99, 0.99, 0.95 | 0.977 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.333 | 1.000 | 0.255 | 0.000 | 0.000 |
| inf | 0 | 1 | 1 | mu | 0.90, 0.91, 0.99 | 0.934 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.226 | 0.000 | 0.000 |
| inf | 1 | 0 | 0 | mu | 0.99, 0.96, 0.94 | 0.964 | 1.000 | 0.253 | 0.000 | 0.713 | `<BOX(THEM(ME))>` 0.25 | 0.253 | 0.713 | 0.250 | 0.250 | 0.000 |
| inf | 1 | 0 | 0.1 | mu | 0.99, 0.99, 0.99 | 0.990 | 1.000 | 0.189 | 0.000 | 0.681 | `<BOX1(THEM(ME))>` 0.38 | 0.017 | 0.713 | 0.259 | 0.259 | 0.000 |
| inf | 1 | 0 | 1 | mu | 0.99, 0.99, 0.99 | 0.990 | 1.000 | 0.448 | 0.000 | 0.724 | `<BOX(THEM(ME))>` 0.45 | 0.000 | 1.000 | 0.224 | 0.224 | 0.000 |
| inf | 1 | 0.01 | 0 | mu | 0.97, 0.99, 0.99 | 0.983 | 1.000 | 0.447 | 0.000 | 0.698 | `<BOX(THEM(ME))>` 0.45 | 0.447 | 0.698 | 0.233 | 0.233 | 0.000 |
| inf | 1 | 0.01 | 0.1 | mu | 0.97, 0.94, 0.98 | 0.964 | 1.000 | 0.180 | 0.000 | 0.719 | `<BOX1(THEM(ME))>` 0.48 | 0.036 | 0.721 | 0.255 | 0.255 | 0.000 |
| inf | 1 | 0.01 | 1 | mu | 0.99, 0.93, 0.94 | 0.953 | 1.000 | 0.228 | 0.000 | 0.689 | `<BOX(THEM(THEM))>` 0.34 | 0.000 | 1.000 | 0.258 | 0.258 | 0.000 |
| inf | 1 | 1 | 0 | mu | 0.99, 0.99, 0.96 | 0.980 | 1.000 | 0.577 | 0.000 | 0.745 | `<BOX(THEM(ME))>` 0.58 | 0.577 | 0.745 | 0.219 | 0.219 | 0.000 |
| inf | 1 | 1 | 0.1 | mu | 0.98, 0.99, 0.99 | 0.988 | 1.000 | 0.478 | 0.000 | 0.751 | `<BOX(THEM(ME))>` 0.48 | 0.005 | 0.697 | 0.222 | 0.222 | 0.000 |
| inf | 1 | 1 | 1 | mu | 0.94, 0.99, 0.99 | 0.974 | 1.000 | 0.009 | 0.000 | 0.701 | `<BOX1(THEM(ME))>` 0.45 | 0.000 | 1.000 | 0.273 | 0.273 | 0.000 |

### Start: all-D with f₀ carriers from μ

| b | s | f₀ | σ | start | P(C,C) per seed | mean | carrier | FB-con share | P*-con share | max con share | top contract | FB-label share | max label share | src-ALLC load | con-ALLC load | anti-prover share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### Uniform-donor control (σ = 1, μ seed)

| b | s | f₀ | σ | start | P(C,C) per seed | mean | carrier | FB-con share | P*-con share | max con share | top contract | FB-label share | max label share | src-ALLC load | con-ALLC load | anti-prover share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 0 | 0.01 | 1 | mu | 0.91, 0.98, 0.99 | 0.960 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.210 | 0.000 | 0.000 |
| 2 | 0 | 1 | 1 | mu | 0.99, 0.96, 0.99 | 0.980 | 0.124 | 0.166 | 0.000 | 0.166 | `<BOX(THEM(ME))>` 0.17 | 0.000 | 1.000 | 0.230 | 0.000 | 0.000 |
| 2 | 1 | 0.01 | 1 | mu | 0.73, 0.99, 0.99 | 0.903 | 1.000 | 0.566 | 0.000 | 0.728 | `<BOX(THEM(ME))>` 0.57 | 0.000 | 1.000 | 0.260 | 0.260 | 0.000 |
| 2 | 1 | 1 | 1 | mu | 0.99, 0.94, 0.97 | 0.968 | 1.000 | 0.253 | 0.000 | 0.693 | `<BOX(THEM(ME))>` 0.25 | 0.000 | 1.000 | 0.261 | 0.261 | 0.000 |
| 4 | 0 | 0.01 | 1 | mu | 0.94, 0.99, 0.96 | 0.961 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.244 | 0.000 | 0.000 |
| 4 | 0 | 1 | 1 | mu | 0.98, 0.99, 0.98 | 0.983 | 0.077 | 0.120 | 0.000 | 0.120 | `<BOX(THEM(ME))>` 0.12 | 0.000 | 1.000 | 0.227 | 0.000 | 0.000 |
| 4 | 1 | 0.01 | 1 | mu | 0.95, 0.99, 0.99 | 0.978 | 1.000 | 0.444 | 0.000 | 0.732 | `<BOX(THEM(ME))>` 0.44 | 0.000 | 1.000 | 0.225 | 0.225 | 0.000 |
| 4 | 1 | 1 | 1 | mu | 0.99, 0.99, 0.98 | 0.986 | 1.000 | 0.258 | 0.000 | 0.732 | `<BOX1(THEM(ME))>` 0.30 | 0.000 | 1.000 | 0.245 | 0.245 | 0.000 |
| inf | 0 | 0.01 | 1 | mu | 0.98, 0.99, 0.99 | 0.986 | 0.000 | 0.000 | 0.000 | 0.000 | - | 0.000 | 1.000 | 0.214 | 0.000 | 0.000 |
| inf | 0 | 1 | 1 | mu | 0.97, 0.98, 0.99 | 0.980 | 0.065 | 0.000 | 0.000 | 0.096 | `<BOX1(THEM(ME))>` 0.10 | 0.000 | 1.000 | 0.234 | 0.000 | 0.000 |
| inf | 1 | 0.01 | 1 | mu | 0.98, 0.99, 0.99 | 0.987 | 1.000 | 0.261 | 0.000 | 0.718 | `<BOX(THEM(ME))>` 0.26 | 0.000 | 1.000 | 0.243 | 0.243 | 0.000 |
| inf | 1 | 1 | 1 | mu | 0.99, 0.97, 0.99 | 0.982 | 1.000 | 0.144 | 0.000 | 0.701 | `<BOX1(THEM(ME))>` 0.39 | 0.000 | 1.000 | 0.263 | 0.263 | 0.000 |

### N path (b = 2, s = 0, f₀ = 0.01, μ seed)

| N | σ | P(C,C) per seed | mean | carrier | FB-con share | max con share | first sample with P(C,C) > 0.5 (gen) |
|---|---|---|---|---|---|---|---|
| 1600 | 0 | 0.99, 0.99, 0.99 | 0.987 | 0.000 | 0.000 | 0.000 | [1000, 5000, 11000] |
| 1600 | 1 | 0.98, 0.62, 0.96 | 0.854 | 0.000 | 0.000 | 0.000 | [3000, 1000, 2000] |
| 6400 | 0 | 0.96, 0.98, 0.99 | 0.979 | 0.000 | 0.000 | 0.000 | [2000, 1000, 1000] |
| 6400 | 1 | 0.99, 0.98, 0.96 | 0.977 | 0.000 | 0.000 | 0.000 | [3000, 5000, 1000] |
| 25600 | 0 | 0.99, 0.98, 0.98 | 0.984 | 0.000 | 0.000 | 0.000 | [1000, 1000, 1000] |
| 25600 | 1 | 0.99, 0.99, 0.99 | 0.992 | 0.000 | 0.000 | 0.000 | [1000, 1000, 1000] |

### Composition, transitions and swap routes (μ seed, σ > 0; pooled over seeds)

| b | s | f₀ | σ | donors | top contracts (carrier share) | top sources (population share) | dominant-contract transitions (total; top) | swaps accepted / same / rejected / donor-none | top routes (recipient's old → copied) |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 0 | 0.01 | 0.1 | payoff |  | `BOX(THEM(ME))` 0.40; `BOX1(THEM(ME))` 0.24; `C` 0.19; `BOX1(THEM(^C))` 0.10 | 3; <D>→no-carriers 3 | 17836 / 768617 / 50364 / 191190843 | none→<D> 17832; none→<C> 4 |
| 2 | 0 | 0.01 | 1 | payoff |  | `BOX(THEM(ME))` 0.44; `C` 0.19; `BOX1(THEM(^C))` 0.14; `BOX1(THEM(ME))` 0.10 | 3; <D>→no-carriers 3 | 15607 / 27676092 / 369041 / 1891939260 | none→<D> 15407; none→<C> 200 |
| 2 | 0 | 1 | 0.1 | payoff | `<BOX(THEM(ME))>` 0.06 | `BOX(THEM(ME))` 0.31; `BOX1(THEM(^C))` 0.28; `C` 0.19; `BOX1(THEM(ME))` 0.13 | 6; <D>→no-carriers 1; <D>→<BOX1(THEM(ME))> 1; <BOX1(THEM(ME))>→no-carriers 1 | 1144 / 30227819 / 9188803 / 152567982 | none→<BOX(THEM(ME))> 770; none→<BOX1(THEM(ME))> 209; none→<D> 163 |
| 2 | 0 | 1 | 1 | payoff |  | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` 0.33; `BOX(THEM(^BOX(THEM(^C))))` 0.19; `BOX1(THEM(^C))` 0.14; `C` 0.13 | 15; <BOX(THEM(THEM))>→<BOX(THEM(ME))> 4; <BOX(THEM(ME))>→no-carriers 3; <BOX(THEM(ME))>→<BOX(THEM(THEM))> 3 | 725 / 154413072 / 43504546 / 1722081657 | none→<BOX(THEM(ME))> 488; none→<D> 178; none→<C> 34 |
| 2 | 1 | 0 | 0.1 | payoff | `<BOX(THEM(ME))>` 0.44; `<BOX1(THEM(ME))>` 0.26; `<C>` 0.23 | `BOX(THEM(ME))` 0.44; `BOX1(THEM(ME))` 0.26; `C` 0.23; `BOX(THEM(THEM))` 0.02 | 452; none-dominant→<BOX(THEM(ME))> 72; <BOX(THEM(ME))>→none-dominant 72; none-dominant→<BOX1(THEM(ME))> 58 | 28501 / 120102832 / 71063250 / 795032 | none→<D> 17869; none→<BOX(THEM(ME))> 6412; none→<BOX(THEM(THEM))> 2435 |
| 2 | 1 | 0 | 1 | payoff | `<BOX(THEM(ME))>` 0.50; `<C>` 0.22; `<BOX(THEM(THEM))>` 0.19 | `BOX(THEM(ME))` 0.50; `C` 0.22; `BOX(THEM(THEM))` 0.19; `BOX1(THEM(ME))` 0.06 | 549; <BOX(THEM(ME))>→none-dominant 95; none-dominant→<BOX(THEM(ME))> 93; none-dominant→<BOX(THEM(THEM))> 88 | 29641 / 1155788207 / 763155808 / 1026344 | none→<D> 17088; none→<BOX1(THEM(THEM))> 6247; none→<BOX(THEM(THEM))> 3590 |
| 2 | 1 | 0.01 | 0.1 | payoff | `<BOX(THEM(ME))>` 0.56; `<C>` 0.19; `<BOX(THEM(THEM))>` 0.19 | `BOX(THEM(ME))` 0.56; `C` 0.19; `BOX(THEM(THEM))` 0.19; `D` 0.04 | 357; none-dominant→<BOX(THEM(ME))> 98; <BOX(THEM(ME))>→none-dominant 92; none-dominant→<BOX(THEM(THEM))> 38 | 22271 / 125276584 / 65710929 / 969856 | none→<D> 17343; none→<BOX(THEM(ME))> 4455; none→<BOX1(THEM(ME))> 281 |
| 2 | 1 | 0.01 | 1 | payoff | `<BOX(THEM(THEM))>` 0.36; `<BOX(THEM(ME))>` 0.31; `<C>` 0.23 | `BOX(THEM(THEM))` 0.36; `BOX(THEM(ME))` 0.31; `C` 0.23; `D` 0.04 | 519; <BOX(THEM(THEM))>→none-dominant 136; none-dominant→<BOX(THEM(THEM))> 134; none-dominant→<BOX(THEM(ME))> 66 | 41586 / 1133814403 / 784780701 / 1363310 | none→<D> 14794; none→<BOX(THEM(THEM))> 8583; none→<BOX1(THEM(ME))> 7502 |
| 2 | 1 | 1 | 0.1 | payoff | `<BOX1(THEM(ME))>` 0.31; `<BOX(THEM(ME))>` 0.29; `<C>` 0.24 | `BOX1(THEM(ME))` 0.31; `BOX(THEM(ME))` 0.29; `C` 0.24; `BOX(THEM(THEM))` 0.08 | 396; none-dominant→<BOX(THEM(ME))> 68; <BOX(THEM(ME))>→none-dominant 64; none-dominant→<BOX1(THEM(ME))> 53 | 389 / 117144991 / 74872162 / 0 | <D>→<and(BOX(THEM(ME)),BOXD1(THEM(ME)))> 227; <and(BOX(THEM(ME)),BOXD1(THEM(ME)))>→<D> 147; <and(BOX(THEM(ME)),not(BOXD1(THEM(THEM))))>→<BOX(THEM(ME))> 3 |
| 2 | 1 | 1 | 1 | payoff | `<BOX(THEM(ME))>` 0.28; `<C>` 0.23; `<BOX(THEM(THEM))>` 0.21 | `BOX(THEM(ME))` 0.28; `C` 0.23; `BOX(THEM(THEM))` 0.21; `BOX(THEM(^BOX1(THEM(THEM))))` 0.11 | 469; none-dominant→<BOX(THEM(ME))> 66; <BOX(THEM(ME))>→none-dominant 65; none-dominant→<BOX1(THEM(ME))> 53 | 1063 / 1173395829 / 746603108 / 0 | <D>→<and(BOX(THEM(ME)),BOXD1(THEM(ME)))> 483; <and(BOX(THEM(ME)),BOXD1(THEM(ME)))>→<D> 465; <BOX1(THEM(ME))>→<and(BOX1(THEM(ME)),not(BOXD1(THEM(ME))))> 20 |
| 4 | 0 | 0.01 | 0.1 | payoff |  | `BOX1(THEM(ME))` 0.38; `C` 0.25; `BOX(THEM(THEM))` 0.19; `BOX(THEM(ME))` 0.10 | 3; <D>→no-carriers 3 | 19184 / 755054 / 26824 / 191193018 | none→<D> 19169; none→<C> 13; none→<BOX(THEM(THEM))> 2 |
| 4 | 0 | 0.01 | 1 | payoff |  | `BOX1(THEM(ME))` 0.32; `C` 0.25; `BOX(THEM(THEM))` 0.22; `BOX(THEM(ME))` 0.17 | 3; <D>→no-carriers 3 | 15296 / 1732454 / 240323 / 1918011927 | none→<D> 15193; none→<C> 103 |
| 4 | 0 | 1 | 0.1 | payoff |  | `BOX(THEM(ME))` 0.73; `C` 0.18; `BOX(THEM(THEM))` 0.02; `D` 0.02 | 38; <BOX(THEM(THEM))>→<BOX(THEM(ME))> 17; <BOX(THEM(ME))>→<BOX(THEM(THEM))> 16; <BOX(THEM(ME))>→no-carriers 2 | 965 / 15888285 / 7358004 / 168744285 | none→<BOX(THEM(ME))> 705; none→<BOX(THEM(THEM))> 153; none→<D> 104 |
| 4 | 0 | 1 | 1 | payoff |  | `BOX(THEM(ME))` 0.34; `BOX(THEM(THEM))` 0.32; `C` 0.23; `D` 0.06 | 4; <D>→no-carriers 2; <D>→<BOX1(THEM(THEM))> 1; <BOX1(THEM(THEM))>→no-carriers 1 | 311 / 12750450 / 2827948 / 1904421291 | none→<D> 240; none→<BOX1(THEM(THEM))> 39; none→<C> 31 |
| 4 | 1 | 0 | 0.1 | payoff | `<BOX(THEM(ME))>` 0.52; `<C>` 0.22; `<BOX(THEM(THEM))>` 0.15 | `BOX(THEM(ME))` 0.52; `C` 0.22; `BOX(THEM(THEM))` 0.15; `BOX1(THEM(ME))` 0.09 | 405; none-dominant→<BOX(THEM(ME))> 75; <BOX(THEM(ME))>→none-dominant 74; none-dominant→<BOX1(THEM(ME))> 48 | 28757 / 120407212 / 70872917 / 691844 | none→<D> 18215; none→<BOX(THEM(ME))> 4795; none→<BOX(THEM(THEM))> 3348 |
| 4 | 1 | 0 | 1 | payoff | `<BOX(THEM(ME))>` 0.43; `<BOX(THEM(THEM))>` 0.30; `<C>` 0.21 | `BOX(THEM(ME))` 0.43; `BOX(THEM(THEM))` 0.30; `C` 0.21; `D` 0.02 | 392; none-dominant→<BOX(THEM(ME))> 61; none-dominant→<BOX(THEM(THEM))> 61; <BOX(THEM(THEM))>→none-dominant 60 | 23243 / 1217626770 / 701058961 / 1291026 | none→<D> 16174; none→<BOX(THEM(THEM))> 3795; none→<BOX1(THEM(THEM))> 1668 |
| 4 | 1 | 0.01 | 0.1 | payoff | `<BOX(THEM(THEM))>` 0.33; `<BOX1(THEM(ME))>` 0.31; `<C>` 0.26 | `BOX(THEM(THEM))` 0.33; `BOX1(THEM(ME))` 0.31; `C` 0.26; `BOX(THEM(ME))` 0.05 | 668; none-dominant→<BOX1(THEM(ME))> 92; <BOX1(THEM(ME))>→none-dominant 91; <BOX(THEM(ME))>→none-dominant 86 | 25775 / 108302484 / 81632809 / 2030764 | none→<D> 15659; none→<BOX1(THEM(ME))> 3793; none→<BOX1(THEM(^C))> 3745 |
| 4 | 1 | 0.01 | 1 | payoff | `<BOX(THEM(ME))>` 0.31; `<BOX1(THEM(ME))>` 0.26; `<C>` 0.24 | `BOX(THEM(ME))` 0.31; `BOX1(THEM(ME))` 0.26; `C` 0.24; `BOX(THEM(THEM))` 0.18 | 392; none-dominant→<BOX(THEM(THEM))> 69; <BOX(THEM(THEM))>→none-dominant 69; none-dominant→<BOX(THEM(ME))> 46 | 15086 / 1141622338 / 778199658 / 162918 | none→<D> 14714; none→<C> 213; none→<BOX(THEM(THEM))> 62 |
| 4 | 1 | 1 | 0.1 | payoff | `<BOX(THEM(ME))>` 0.40; `<BOX1(THEM(ME))>` 0.26; `<C>` 0.24 | `BOX(THEM(ME))` 0.40; `BOX1(THEM(ME))` 0.26; `C` 0.24; `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 0.05 | 539; <BOX1(THEM(ME))>→none-dominant 93; none-dominant→<BOX1(THEM(ME))> 92; none-dominant→<BOX(THEM(ME))> 71 | 21 / 111208427 / 80790005 / 0 | <not(and(BOX(THEM(ME)),BOXD(THEM(ME))))>→<C> 5; <D>→<and(BOX(THEM(ME)),BOXD(THEM(ME)))> 4; <and(BOX(THEM(ME)),BOXD(THEM(ME)))>→<D> 3 |
| 4 | 1 | 1 | 1 | payoff | `<BOX(THEM(ME))>` 0.47; `<BOX(THEM(THEM))>` 0.25; `<C>` 0.21 | `BOX(THEM(ME))` 0.47; `BOX(THEM(THEM))` 0.25; `C` 0.21; `D` 0.04 | 449; none-dominant→<BOX(THEM(THEM))> 120; <BOX(THEM(THEM))>→none-dominant 114; <BOX(THEM(ME))>→none-dominant 65 | 112 / 1188579691 / 731420197 / 0 | <and(BOX1(THEM(ME)),BOXD1(THEM(ME)))>→<D> 26; <D>→<and(BOX1(THEM(ME)),BOXD1(THEM(ME)))> 22; <and(BOX(THEM(ME)),not(BOXD1(THEM(ME))))>→<BOX(THEM(ME))> 13 |
| inf | 0 | 0.01 | 0.1 | payoff |  | `BOX(THEM(ME))` 0.79; `C` 0.19; `BOXD1(THEM(^D))` 0.01; `BOX(THEM(THEM))` 0.00 | 3; <D>→no-carriers 3 | 18528 / 895635 / 37514 / 191051123 | none→<D> 18518; none→<C> 10 |
| inf | 0 | 0.01 | 1 | payoff |  | `BOX(THEM(ME))` 0.44; `C` 0.21; `BOX(THEM(THEM))` 0.17; `BOX1(THEM(ME))` 0.12 | 3; <D>→no-carriers 3 | 15644 / 22592324 / 433019 / 1896959013 | none→<D> 15492; none→<C> 151; none→<BOXD(THEM(ME))> 1 |
| inf | 0 | 1 | 0.1 | payoff |  | `BOX(THEM(THEM))` 0.32; `C` 0.25; `BOX1(THEM(ME))` 0.20; `BOX(THEM(ME))` 0.19 | 16; <BOX1(THEM(ME))>→none-dominant 3; none-dominant→<BOX1(THEM(ME))> 2; none-dominant→<BOX1(THEM(THEM))> 2 | 328 / 1110971 / 509802 / 190378910 | none→<D> 294; none→<BOX1(THEM(ME))> 18; none→<BOX1(THEM(THEM))> 12 |
| inf | 0 | 1 | 1 | payoff |  | `BOX(THEM(ME))` 0.51; `C` 0.19; `BOX(THEM(THEM))` 0.15; `D` 0.06 | 4; <D>→no-carriers 2; <D>→<BOX(THEM(THEM))> 1; <BOX(THEM(THEM))>→no-carriers 1 | 336 / 51636723 / 13168805 / 1855194136 | none→<D> 172; none→<BOX(THEM(THEM))> 129; none→<C> 34 |
| inf | 1 | 0 | 0.1 | payoff | `<BOX1(THEM(ME))>` 0.38; `<C>` 0.26; `<BOX(THEM(ME))>` 0.19 | `BOX1(THEM(ME))` 0.38; `C` 0.26; `BOX(THEM(ME))` 0.19; `BOX(THEM(THEM))` 0.14 | 507; none-dominant→<BOX1(THEM(ME))> 78; <BOX1(THEM(ME))>→none-dominant 71; none-dominant→<BOX(THEM(ME))> 57 | 18127 / 115037027 / 76094950 / 841690 | none→<D> 18017; <C>→<not(and(BOX(THEM(ME)),BOXD(THEM(ME))))> 30; <not(and(BOX(THEM(ME)),BOXD(THEM(ME))))>→<C> 30 |
| inf | 1 | 0 | 1 | payoff | `<BOX(THEM(ME))>` 0.45; `<BOX(THEM(THEM))>` 0.29; `<C>` 0.22 | `BOX(THEM(ME))` 0.45; `BOX(THEM(THEM))` 0.29; `C` 0.22; `BOX1(THEM(ME))` 0.02 | 403; none-dominant→<BOX(THEM(THEM))> 71; <BOX(THEM(THEM))>→none-dominant 68; <BOX1(THEM(ME))>→none-dominant 38 | 19589 / 1199447779 / 720069157 / 463475 | none→<D> 16187; none→<BOX1(THEM(ME))> 2255; none→<BOX(THEM(ME))> 724 |
| inf | 1 | 0.01 | 0.1 | payoff | `<BOX1(THEM(ME))>` 0.48; `<C>` 0.24; `<BOX(THEM(ME))>` 0.18 | `BOX1(THEM(ME))` 0.48; `C` 0.24; `BOX(THEM(ME))` 0.18; `BOX(THEM(THEM))` 0.04 | 463; <BOX1(THEM(ME))>→none-dominant 89; none-dominant→<BOX1(THEM(ME))> 88; none-dominant→<BOX(THEM(THEM))> 36 | 28616 / 115596179 / 75542182 / 824379 | none→<D> 17664; none→<BOX(THEM(THEM))> 3914; <BOX1(THEM(ME))>→<and(BOX1(THEM(ME)),not(BOXD(THEM(ME))))> 3393 |
| inf | 1 | 0.01 | 1 | payoff | `<BOX(THEM(THEM))>` 0.34; `<C>` 0.23; `<BOX(THEM(ME))>` 0.23 | `BOX(THEM(THEM))` 0.34; `C` 0.23; `BOX(THEM(ME))` 0.23; `BOX1(THEM(ME))` 0.10 | 573; <BOX1(THEM(ME))>→none-dominant 91; none-dominant→<BOX1(THEM(ME))> 89; <BOX(THEM(THEM))>→none-dominant 65 | 25028 / 1151438512 / 767359113 / 1177347 | none→<D> 15485; none→<BOX(THEM(THEM))> 6186; none→<BOX1(THEM(^C))> 1909 |
| inf | 1 | 1 | 0.1 | payoff | `<BOX(THEM(ME))>` 0.48; `<C>` 0.22; `<BOX(THEM(THEM))>` 0.21 | `BOX(THEM(ME))` 0.47; `C` 0.22; `BOX(THEM(THEM))` 0.21; `BOX1(THEM(ME))` 0.07 | 301; none-dominant→<BOX(THEM(ME))> 58; none-dominant→<BOX(THEM(THEM))> 55; <BOX(THEM(ME))>→none-dominant 54 | 26 / 122542888 / 69457144 / 0 | <and(BOX(THEM(ME)),not(BOXD1(THEM(ME))))>→<BOX(THEM(ME))> 4; <and(BOXD(THEM(ME)),BOX1(THEM(THEM)))>→<D> 3; <D>→<and(BOX(THEM(ME)),BOXD1(THEM(ME)))> 3 |
| inf | 1 | 1 | 1 | payoff | `<BOX1(THEM(ME))>` 0.45; `<C>` 0.26; `<BOX(THEM(THEM))>` 0.24 | `BOX1(THEM(ME))` 0.45; `C` 0.26; `BOX(THEM(THEM))` 0.24; `D` 0.02 | 420; none-dominant→<BOX1(THEM(ME))> 87; <BOX1(THEM(ME))>→none-dominant 86; none-dominant→<BOX(THEM(THEM))> 46 | 14873 / 1145691126 / 774294001 / 0 | <not(and(BOXD(THEM(ME)),BOX1(THEM(ME))))>→<C> 7447; <C>→<not(and(BOXD(THEM(ME)),BOX1(THEM(ME))))> 7376; <BOX1(THEM(ME))>→<and(BOX1(THEM(ME)),not(BOXD(THEM(ME))))> 13 |
| 2 | 0 | 0.01 | 1 | uniform |  | `BOX(THEM(ME))` 0.31; `BOX1(THEM(^C))` 0.24; `BOX1(THEM(ME))` 0.19; `C` 0.19 | 3; <D>→no-carriers 3 | 15386 / 1493190 / 244724 / 1918246700 | none→<D> 15291; none→<C> 94; none→<BOXD1(THEM(THEM))> 1 |
| 2 | 0 | 1 | 1 | uniform | `<BOX(THEM(ME))>` 0.17 | `BOX1(THEM(^C))` 0.38; `C` 0.22; `BOX(THEM(ME))` 0.15; `BOX1(THEM(ME))` 0.15 | 8; none-dominant→<BOX(THEM(ME))> 2; <D>→<BOX1(THEM(ME))> 1; <BOX1(THEM(ME))>→no-carriers 1 | 891 / 310186948 / 75058644 / 1534753517 | none→<BOX(THEM(ME))> 513; none→<D> 223; none→<BOX(THEM(THEM))> 58 |
| 2 | 1 | 0.01 | 1 | uniform | `<BOX(THEM(ME))>` 0.57; `<C>` 0.20; `<D>` 0.09 | `BOX(THEM(ME))` 0.57; `C` 0.20; `D` 0.09; `BOX(THEM(THEM))` 0.05 | 438; none-dominant→<BOX(THEM(ME))> 100; <BOX(THEM(ME))>→none-dominant 98; none-dominant→<BOX1(THEM(ME))> 41 | 15540 / 1210974064 / 708853501 / 156895 | none→<D> 15067; none→<C> 258; <BOX1(THEM(ME))>→<and(BOX1(THEM(ME)),not(BOXD(THEM(ME))))> 51 |
| 2 | 1 | 1 | 1 | uniform | `<BOX(THEM(ME))>` 0.25; `<C>` 0.24; `<BOX1(THEM(ME))>` 0.23 | `BOX(THEM(ME))` 0.25; `C` 0.24; `BOX1(THEM(ME))` 0.23; `BOX(THEM(THEM))` 0.22 | 543; none-dominant→<BOX(THEM(THEM))> 73; none-dominant→<BOX1(THEM(ME))> 72; <BOX1(THEM(ME))>→none-dominant 70 | 2838 / 1125922048 / 794075114 / 0 | <C>→<not(and(BOXD(THEM(ME)),BOX1(THEM(ME))))> 1437; <not(and(BOXD(THEM(ME)),BOX1(THEM(ME))))>→<C> 1300; <not(and(BOX(THEM(ME)),BOXD(THEM(ME))))>→<C> 16 |
| 4 | 0 | 0.01 | 1 | uniform |  | `BOX(THEM(ME))` 0.39; `BOX(THEM(THEM))` 0.29; `C` 0.22; `D` 0.03 | 3; <D>→no-carriers 3 | 15941 / 28790217 / 438785 / 1890755057 | none→<D> 15640; none→<C> 301 |
| 4 | 0 | 1 | 1 | uniform | `<BOX(THEM(ME))>` 0.12 | `BOX(THEM(ME))` 0.49; `BOX1(THEM(ME))` 0.23; `C` 0.22; `BOX(THEM(THEM))` 0.02 | 45; none-dominant→<BOX(THEM(ME))> 7; <BOX(THEM(ME))>→none-dominant 6; none-dominant→<BOX1(THEM(^C))> 5 | 1764 / 450120049 / 168399504 / 1301478683 | none→<BOX(THEM(ME))> 1407; none→<D> 183; none→<BOX1(THEM(^C))> 57 |
| 4 | 1 | 0.01 | 1 | uniform | `<BOX(THEM(ME))>` 0.44; `<C>` 0.22; `<BOX(THEM(THEM))>` 0.20 | `BOX(THEM(ME))` 0.44; `C` 0.22; `BOX(THEM(THEM))` 0.20; `BOX1(THEM(ME))` 0.08 | 313; none-dominant→<BOX(THEM(ME))> 53; <BOX(THEM(ME))>→none-dominant 51; none-dominant→<BOX(THEM(THEM))> 47 | 23689 / 1214062083 / 704193618 / 1720610 | none→<D> 15240; none→<BOX(THEM(ME))> 4602; none→<BOX1(THEM(^D))> 1365 |
| 4 | 1 | 1 | 1 | uniform | `<BOX1(THEM(ME))>` 0.30; `<BOX(THEM(ME))>` 0.26; `<C>` 0.24 | `BOX1(THEM(ME))` 0.30; `BOX(THEM(ME))` 0.26; `C` 0.24; `BOX(THEM(THEM))` 0.18 | 447; none-dominant→<BOX1(THEM(ME))> 104; <BOX1(THEM(ME))>→none-dominant 102; <BOX(THEM(ME))>→none-dominant 32 | 225899 / 1161369353 / 758404748 / 0 | <D>→<and(BOX(THEM(ME)),BOXD1(THEM(ME)))> 116325; <and(BOX(THEM(ME)),BOXD1(THEM(ME)))>→<D> 109489; <D>→<and(BOXD(THEM(ME)),BOX1(THEM(ME)))> 14 |
| inf | 0 | 0.01 | 1 | uniform |  | `BOX(THEM(ME))` 0.57; `C` 0.21; `BOX(THEM(THEM))` 0.19; `D` 0.01 | 3; <D>→no-carriers 3 | 15889 / 2212851 / 242609 / 1917528651 | none→<D> 15727; none→<C> 161; none→<BOX1(THEM(THEM))> 1 |
| inf | 0 | 1 | 1 | uniform | `<BOX1(THEM(ME))>` 0.10 | `BOX(THEM(THEM))` 0.34; `BOX(THEM(ME))` 0.28; `C` 0.23; `BOX1(THEM(ME))` 0.12 | 5; <D>→no-carriers 1; <D>→<BOX(THEM(THEM))> 1; <BOX(THEM(THEM))>→no-carriers 1 | 1168 / 199960473 / 94231471 / 1625806888 | none→<BOX1(THEM(ME))> 664; none→<BOX(THEM(THEM))> 202; none→<D> 199 |
| inf | 1 | 0.01 | 1 | uniform | `<BOX(THEM(ME))>` 0.26; `<C>` 0.24; `<BOX1(THEM(ME))>` 0.24 | `BOX(THEM(ME))` 0.26; `C` 0.24; `BOX1(THEM(ME))` 0.24; `BOX(THEM(THEM))` 0.23 | 546; none-dominant→<BOX(THEM(ME))> 101; <BOX(THEM(ME))>→none-dominant 99; none-dominant→<BOX1(THEM(ME))> 80 | 27520 / 1183779164 / 733491863 / 2701453 | none→<D> 15815; none→<BOX(THEM(ME))> 6791; none→<BOX1(THEM(THEM))> 3946 |
| inf | 1 | 1 | 1 | uniform | `<BOX1(THEM(ME))>` 0.39; `<C>` 0.26; `<BOX(THEM(THEM))>` 0.19 | `BOX1(THEM(ME))` 0.39; `C` 0.26; `BOX(THEM(THEM))` 0.19; `BOX(THEM(ME))` 0.14 | 482; none-dominant→<BOX1(THEM(ME))> 119; <BOX1(THEM(ME))>→none-dominant 115; none-dominant→<BOX(THEM(THEM))> 52 | 513 / 1148956666 / 771042821 / 0 | <BOX1(THEM(ME))>→<and(BOX1(THEM(ME)),not(BOXD(THEM(ME))))> 238; <and(BOX1(THEM(ME)),not(BOXD(THEM(ME))))>→<BOX1(THEM(ME))> 213; <not(and(BOX(THEM(ME)),BOXD(THEM(ME))))>→<C> 8 |

## ε = 0 seeding lottery (iid μ seeding, complete island graph, mN = 1; efficient = final P(C,C) ≥ 0.95)

| (N, I) | b | f₀ | σ | runs | efficient | 95% Wilson | defecting | other | unresolved / metastable | median stop gen |
|---|---|---|---|---|---|---|---|---|---|---|
| (100, 256) | 2 | 0 | 0 | 40 | 1.00 | [0.91, 1.00] | 0 | 0 | 0 | 280 |
| (100, 256) | 2 | 0.01 | 0 | 39 | 1.00 | [0.91, 1.00] | 0 | 0 | 0 | 265 |
| (100, 256) | 2 | 0.01 | 1 | 12 | 1.00 | [0.76, 1.00] | 0 | 0 | 0 | 270 |

## Numbers for the verdicts (μ seed unless stated)

- **P1** b = 2, s = 0, f₀ = 0: 0.991 (pred < 0.3). b = 2, f₀ = 1: s = 0/σ = 0 0.970, s = 1/σ = 0 0.975, s = 0/σ = 1 0.956. Contract baseline b = ∞, f₀ = 1, s = 1, σ = 0: 0.980; s = 0, σ = 0: 0.978. Source oracle b = ∞, s = 0, f₀ = 0: 0.991.
- **P2** (σ = 1): b=2 s=0 f₀=0.01: FB-con 0.000, P*-con 0.000, top -; uniform FB-con 0.000 top - | b=2 s=0 f₀=1: FB-con 0.000, P*-con 0.000, top -; uniform FB-con 0.166 top ('<BOX(THEM(ME))>', 0.16626666666666667) | b=2 s=1 f₀=0: FB-con 0.502, P*-con 0.000, top ('<BOX(THEM(ME))>', 0.501834354166667); uniform FB-con n/a top - | b=2 s=1 f₀=0.01: FB-con 0.312, P*-con 0.000, top ('<BOX(THEM(THEM))>', 0.3561433750000004); uniform FB-con 0.566 top ('<BOX(THEM(ME))>', 0.5659331875000001) | b=2 s=1 f₀=1: FB-con 0.281, P*-con 0.000, top ('<BOX(THEM(ME))>', 0.2807447083333333); uniform FB-con 0.253 top ('<BOX(THEM(ME))>', 0.2532575000000002) | b=4 s=0 f₀=0.01: FB-con 0.000, P*-con 0.000, top -; uniform FB-con 0.000 top - | b=4 s=0 f₀=1: FB-con 0.000, P*-con 0.000, top -; uniform FB-con 0.120 top ('<BOX(THEM(ME))>', 0.12013333333333333) | b=4 s=1 f₀=0: FB-con 0.431, P*-con 0.000, top ('<BOX(THEM(ME))>', 0.431108625); uniform FB-con n/a top - | b=4 s=1 f₀=0.01: FB-con 0.311, P*-con 0.000, top ('<BOX(THEM(ME))>', 0.3107361666666668); uniform FB-con 0.444 top ('<BOX(THEM(ME))>', 0.4441004583333329) | b=4 s=1 f₀=1: FB-con 0.468, P*-con 0.000, top ('<BOX(THEM(ME))>', 0.46756631250000014); uniform FB-con 0.258 top ('<BOX1(THEM(ME))>', 0.30208502083333294) | b=inf s=0 f₀=0.01: FB-con 0.000, P*-con 0.000, top -; uniform FB-con 0.000 top - | b=inf s=0 f₀=1: FB-con 0.000, P*-con 0.000, top -; uniform FB-con 0.000 top ('<BOX1(THEM(ME))>', 0.09573333333333334) | b=inf s=1 f₀=0: FB-con 0.448, P*-con 0.000, top ('<BOX(THEM(ME))>', 0.44778820833333344); uniform FB-con n/a top - | b=inf s=1 f₀=0.01: FB-con 0.228, P*-con 0.000, top ('<BOX(THEM(THEM))>', 0.34467479166666676); uniform FB-con 0.261 top ('<BOX(THEM(ME))>', 0.2605106249999998) | b=inf s=1 f₀=1: FB-con 0.009, P*-con 0.000, top ('<BOX1(THEM(ME))>', 0.4470406874999999); uniform FB-con 0.144 top ('<BOX1(THEM(ME))>', 0.3856394375000003)
- **P3** key cell b = 2, s = 0, f₀ = 0.01: σ = 1 0.977, σ = 0 0.979, σ = 0.1 0.978. N path σ = 1: 0.854 / 0.977 / 0.992; σ = 0: 0.987 / 0.979 / 0.984.
- **P4** source-ALLC load over μ-seed grid cells: min 0.155, max 0.283, median 0.238; at b = ∞ min 0.167. Contract-ALLC load at f₀ = 1: inf/0/0: 0.28 vs 0.00, inf/0/0.1: 0.26 vs 0.00, inf/0/1: 0.23 vs 0.00, inf/1/0: 0.22 vs 0.22, inf/1/0.1: 0.22 vs 0.22, inf/1/1: 0.27 vs 0.27; at f₀ < 1: inf/0/0/0: 0.17 vs 0.00, inf/0/0.01/0: 0.23 vs 0.00, inf/0/0.01/0.1: 0.19 vs 0.00, inf/0/0.01/1: 0.23 vs 0.00, inf/1/0/0: 0.25 vs 0.25, inf/1/0/0.1: 0.26 vs 0.26, inf/1/0/1: 0.22 vs 0.22, inf/1/0.01/0: 0.23 vs 0.23, inf/1/0.01/0.1: 0.26 vs 0.26, inf/1/0.01/1: 0.26 vs 0.26.
- **P5** (100, 4): free nan; b=2 f₀=0 nan; b=2 f₀=1 σ=0 nan / σ=1 nan; b=2 f₀=0.01 σ=0 nan / σ=1 nan; b=∞ f₀=1 σ=0 nan | (400, 4): free nan; b=2 f₀=0 nan; b=2 f₀=1 σ=0 nan / σ=1 nan; b=2 f₀=0.01 σ=0 nan / σ=1 nan; b=∞ f₀=1 σ=0 nan | (100, 64): free nan; b=2 f₀=0 nan; b=2 f₀=1 σ=0 nan / σ=1 nan; b=2 f₀=0.01 σ=0 nan / σ=1 nan; b=∞ f₀=1 σ=0 nan | (100, 256): free nan; b=2 f₀=0 1.00; b=2 f₀=1 σ=0 nan / σ=1 nan; b=2 f₀=0.01 σ=0 1.00 / σ=1 1.00; b=∞ f₀=1 σ=0 nan
- **P6** pay b=2 s=0 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.00 | pay b=2 s=0 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.00 | pay b=2 s=1 f₀=0: max label 1.00, FB-label 0.00, FB-con 0.50, max con 0.72 | pay b=2 s=1 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.31, max con 0.70 | pay b=2 s=1 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.28, max con 0.72 | pay b=4 s=0 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.00 | pay b=4 s=0 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.00 | pay b=4 s=1 f₀=0: max label 1.00, FB-label 0.00, FB-con 0.43, max con 0.74 | pay b=4 s=1 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.31, max con 0.71 | pay b=4 s=1 f₀=1: max label 1.00, FB-label 0.33, FB-con 0.47, max con 0.73 | pay b=inf s=0 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.00 | pay b=inf s=0 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.00 | pay b=inf s=1 f₀=0: max label 1.00, FB-label 0.00, FB-con 0.45, max con 0.72 | pay b=inf s=1 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.23, max con 0.69 | pay b=inf s=1 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.01, max con 0.70 | uni b=2 s=0 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.00 | uni b=2 s=0 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.17, max con 0.17 | uni b=2 s=1 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.57, max con 0.73 | uni b=2 s=1 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.25, max con 0.69 | uni b=4 s=0 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.00 | uni b=4 s=0 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.12, max con 0.12 | uni b=4 s=1 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.44, max con 0.73 | uni b=4 s=1 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.26, max con 0.73 | uni b=inf s=0 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.00 | uni b=inf s=0 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.00, max con 0.10 | uni b=inf s=1 f₀=0.01: max label 1.00, FB-label 0.00, FB-con 0.26, max con 0.72 | uni b=inf s=1 f₀=1: max label 1.00, FB-label 0.00, FB-con 0.14, max con 0.70
- **RS-a** f₀ = 1 vs free (b = ∞, s = 0, f₀ = 0 = 0.991): b=2 s=0 σ=0 0.970; b=2 s=0 σ=0.1 0.952; b=2 s=0 σ=1 0.956; b=2 s=1 σ=0 0.975; b=2 s=1 σ=0.1 0.980; b=2 s=1 σ=1 0.952; b=4 s=0 σ=0 0.987; b=4 s=0 σ=0.1 0.979; b=4 s=0 σ=1 0.933; b=4 s=1 σ=0 0.981; b=4 s=1 σ=0.1 0.985; b=4 s=1 σ=1 0.958; b=inf s=0 σ=0 0.978; b=inf s=0 σ=0.1 0.977; b=inf s=0 σ=1 0.934; b=inf s=1 σ=0 0.980; b=inf s=1 σ=0.1 0.988; b=inf s=1 σ=1 0.974. **RS-b** anti-prover share max over cells 0.0004.
