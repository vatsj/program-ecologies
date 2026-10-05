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

### Start: all-D with f₀ carriers from μ

| b | s | f₀ | σ | start | P(C,C) per seed | mean | carrier | FB-con share | P*-con share | max con share | top contract | FB-label share | max label share | src-ALLC load | con-ALLC load | anti-prover share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### Uniform-donor control (σ = 1, μ seed)

| b | s | f₀ | σ | start | P(C,C) per seed | mean | carrier | FB-con share | P*-con share | max con share | top contract | FB-label share | max label share | src-ALLC load | con-ALLC load | anti-prover share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### N path (b = 2, s = 0, f₀ = 0.01, μ seed)

| N | σ | P(C,C) per seed | mean | carrier | FB-con share | max con share | first sample with P(C,C) > 0.5 (gen) |
|---|---|---|---|---|---|---|---|
| 6400 | 0 | 0.96, 0.98, 0.99 | 0.979 | 0.000 | 0.000 | 0.000 | [2000, 1000, 1000] |
| 25600 | 0 | 0.99, 0.98, 0.98 | 0.984 | 0.000 | 0.000 | 0.000 | [1000, 1000, 1000] |
| 25600 | 1 | 0.99, 0.99, 0.99 | 0.992 | 0.000 | 0.000 | 0.000 | [1000, 1000, 1000] |

### Composition, transitions and swap routes (μ seed, σ > 0; pooled over seeds)

| b | s | f₀ | σ | donors | top contracts (carrier share) | top sources (population share) | dominant-contract transitions (total; top) | swaps accepted / same / rejected / donor-none | top routes (recipient's old → copied) |
|---|---|---|---|---|---|---|---|---|---|

## Numbers for the verdicts (μ seed unless stated)

- **P1** b = 2, s = 0, f₀ = 0: 0.991 (pred < 0.3). b = 2, f₀ = 1: s = 0/σ = 0 n/a, s = 1/σ = 0 n/a, s = 0/σ = 1 n/a. Contract baseline b = ∞, f₀ = 1, s = 1, σ = 0: n/a; s = 0, σ = 0: n/a. Source oracle b = ∞, s = 0, f₀ = 0: n/a.
- **P2** (σ = 1): 
- **P3** key cell b = 2, s = 0, f₀ = 0.01: σ = 1 n/a, σ = 0 0.979, σ = 0.1 n/a. N path σ = 1: n/a / n/a / 0.992; σ = 0: n/a / 0.979 / 0.984.
- **P4** source-ALLC load over μ-seed grid cells: min 0.182, max 0.208, median 0.195; at b = ∞ min nan. Contract-ALLC load at f₀ = 1: ; at f₀ < 1: .
- **P6** 
- **RS-a** f₀ = 1 vs free (b = ∞, s = 0, f₀ = 0 = n/a): b=2 s=0 σ=0 n/a; b=2 s=0 σ=0.1 n/a; b=2 s=0 σ=1 n/a; b=2 s=1 σ=0 n/a; b=2 s=1 σ=0.1 n/a; b=2 s=1 σ=1 n/a; b=4 s=0 σ=0 n/a; b=4 s=0 σ=0.1 n/a; b=4 s=0 σ=1 n/a; b=4 s=1 σ=0 n/a; b=4 s=1 σ=0.1 n/a; b=4 s=1 σ=1 n/a; b=inf s=0 σ=0 n/a; b=inf s=0 σ=0.1 n/a; b=inf s=0 σ=1 n/a; b=inf s=1 σ=0 n/a; b=inf s=1 σ=0.1 n/a; b=inf s=1 σ=1 n/a. **RS-b** anti-prover share max over cells 0.0000.
