# Three-player majority divide-the-dollar: runs (2026-10-04)

## Summary and verdicts

The ε→0 chain at n = 6 is a rotating-pair chain in every arm. Pairs hold 0.98–0.99 of π, unfair pairs hold about 0.6, the grand coalition holds 0.003 among constants and 0.010–0.017 with conditional programs, and disagreement is 10⁻⁴ or less. The shares are N-independent from N = 10³ on. Provability changes nothing measurable: modalPA equals the weak arm to three decimals at N = 10² and 10³.

The mechanism is the same in every arm:
- The excluded slot drifts neutrally (rate ∝ 1/N) to an offer that pays a member more.
- That member, the pivot, takes the offer by a strict move.
- Pivots only ever move up: 1/3 → 1/2, 1/2 → 2/3, 1/3 → 2/3, and neutral 1/2 → 1/2.
- No program in a pair can stop its partner's own slot from defecting, so reading source cannot plug this exit.

There is a nonzero net current around the outcome types, fair → unfair → wasteful → fair. It is equal on each edge and ∝ 1/N: 1.9·10⁻⁵, 3.6·10⁻⁶ and 3.9·10⁻⁷ per mutation event at N = 10², 10³, 10⁴. The net circulation among the three labelled pair states is exactly 0, as relabeling symmetry requires.

The grand coalition behaves differently in the two kinds of language:
- *Constants only:* it is drift-closed, since every exit costs a member 1/3.
- *n = 6:* it is not. One-atom conditionals give it 54 bridges (108 with PA + Con), for example `if(BOX(2=(1,1/2)),(2,1/3),(ALL,1/3))`, which plays (ALL, 1/3) on path and accepts slot 2's pair offer. Their bridge mass is 3.3·10⁻⁴ per mutation event, against 0.149 for a constant pair. Readers of the form "join the grand coalition iff slot j does" open neutral-plus-strict entries. So conditionals raise the grand coalition's share 3–6×, with entry and exit both ∝ 1/N.

Status of the cells:
- **modal arm (PA + Con), full chain: not finished.** It was projected beyond 2 hours under machine load (load average up to ~260, swap full). In its place:
  - the matched modalPA arm (PA box only, the weak arm's grammar) at every N;
  - one-ring runs of modal and modalPA at N = 100, which agree within 0.01;
  - static comparisons: the named and handshake triples have identical bridge masses and exit rates in modal and modalPA.
- **Also stopped:** modalPA at N = 10⁴ (still in round 1 after 1 h 54 min) and a three-round modal N = 100 rerun (still in round 1 after 1 h 04 min). For N = 10⁴ only constants and weak are available.

| # | prediction | verdict | numbers |
|---|---|---|---|
| 1 | no efficient monomorphic triple drift-closed at n = 6 | **held** at n = 6 (language-relative) | 0 of 150 efficient states with π ≥ 10⁻⁶ closed at depth 2, in every weak/modalPA cell. Constant grand: 54 (weak, modalPA) / 108 (modal) bridges, mass 3.3·10⁻⁴; constant pairs: mass 0.149. At n = 1 (constants) the grand coalition **is** drift-closed (no strict or neutral exit), so sol's "language-dependent trapped networks" exists one language down. |
| 2 | pairs ≥ 0.6 and grand ≤ 0.2 at N = 100 (modal), nonzero net current around the three pair states | **mass clause held; current clause failed as stated** | modalPA N = 100: pairs 0.990, grand 0.0099. The net circulation around the labelled pair states is 0 (1e−20), as forced by symmetry. The nonzero current is around outcome types (fair → unfair → wasteful → fair), driven by the excluded slot bidding for a pivot. |
| 3 | unfair pairs in [0.1, 0.4] and below fair | **failed** (falsifier met) | unfair 0.59–0.63 against fair 0.36–0.38 in every arm and N. That is the 2:1 orientation multiplicity, and pivots ratchet up to 2/3. |
| 4 | E[max share] ∈ [0.45, 0.60], exclusion ≥ 0.6 | **held in modalPA (N = 10², 10³), at the upper edge; falsifier (> 0.62) not met anywhere** | E[max]: modalPA 0.5964 / 0.5998; weak 0.5964 / 0.5998 / 0.6005 (above 0.60 by 5·10⁻⁴ at N = 10⁴); constants 0.5987 / 0.6035 / 0.6043. P(some slot gets 0) 0.983–0.998; P(pair) 0.983–0.997. The interval holds only because the 2:1 unfair/fair split sits at E[max] ≈ 0.6 by arithmetic. |
| 5 | grand coalition < 0.2 at every N, exits neutral ∝ 1/N into accept-pair programs then strict pair formation, entry needs three neutral steps | **share held; mechanism half held** | grand 0.0099 / 0.0161 / not finished (modalPA) and 0.010 / 0.016 / 0.017 (weak). Exits: the constant grand coalition's only non-deleterious exits are the bridges, at rate 2.67·10⁻³/N; the next step is pair formation, strict (offer 1/2) or neutral (offer 1/3). Entry: not three neutral steps. It goes through a conditional "join iff slot j joins" reader and a strict last step, at a rate of 6.5–9.4·10⁻⁵ per event spent in disagreement, flat in N. |
| 6 | weak arm disagreement ≥ 2× modal at each N | **failed** | disagreement 4·10⁻⁴ / 1·10⁻⁴ / < 10⁻⁴ in both weak and modalPA, identical. Weak-arm handshakes diverge, but they carry no mass. |
| 7 | finite ε: pair-to-pair turnover, mean pair dwell 10²–10⁴ generations; grand start decays into pairs within 10⁴ generations in all 3 seeds | **turnover clause held; decay clause failed** | mean interior pair dwell 1.1–1.7·10³ generations (median 480–1,250); pair-to-pair switches 5–37 per run. Grand start: P(pair) first exceeds 0.5 at 26,440 and 67,100 generations, and never by 10⁵ in one seed, in both arms. |
| 8 | constants: fair pairs ≥ 0.5, grand < 0.1 | **failed** (fair clause); grand clause held | fair 0.376 / 0.371 / 0.368, unfair 0.596 / 0.624 / 0.629, grand 0.0025 / 0.0029 / 0.0029. Entry into and exit from the grand coalition both cost 1/3, so its share is N-independent, not a matter of path length. |

### Method notes

- **Solver.** At N ≥ 10³ the rates span e⁻¹⁰⁰⁰ and beyond, and sparse LU on the generator fails: on the 729-state
  constants chain at N = 10³ it puts all mass on the grand coalition, against 0.003 from GTH. Row-scaled linear GTH is
  exact through N = 10³. At N = 10⁴ only log-space GTH is right, because a rate negligible within its row can be the
  only bridge between closed classes. The non-constant cells use a "hybrid": the core (the 729 constant triples plus
  promoted states) is solved by dense GTH (log-space at N = 10⁴), and the ring of explored non-core states is
  eliminated exactly as a stochastic complement, by sparse LU on its jump chain.
- **Exploration.** New ring states are those with π-weighted inflow above θ, with θN = 10⁻⁷ throughout.
  - The outcome-changing cut (outcome-changing transitions that leave the explored set, relative to all
    outcome-changing transitions) is 0.3–1.1% in the final cells.
  - Relabeling invariance of π holds to 10⁻¹³ (top 2,000 states, all 6 permutations).
  - The grand coalition's share is sensitive to exploration depth, because the reader states that open entries into
    it have small inflow. At N = 10³, θN = 10⁻⁶ gives 0.0016 and θN = 10⁻⁷ gives 0.0161. The hybrid without
    ring-to-ring edges (`*_ringonly`) gives 0.003 at N = 100, against 0.010 with them. The ring-only method breaks down
    at N = 10⁴ and was discarded.
  - The pair shares move by ≤ 0.01 across all of these checks.
- **Handshakes** (two or three conditional slots) have zero mass in the explored sets. Their inflow is below θ, and the
  hand-built handshakes leak at least as fast as their constant counterparts (handshake table below). So leaving them
  out does not bias the outcome shares.
- **Machine load.** Load average reached ~260 and swap filled, from other jobs, so cells ran 5–10× slower than on an
  idle machine. That is why the modal (PA + Con) chain and modalPA at N = 10⁴ did not finish.

Spec `specs/2026-10-04-three-player-dollar.md`; predictions `predictions/2026-10-04-three-player-dollar.md` (committed before any run). Code: `src/dollar3*.py`. Per-cell data: `runs/dollar3/<arm>_N<N>.json` (and `_chain.npz`: explored states, log π, kept edges).

ε→0 chain over monomorphic triples of payoff classes, w = 0.3, exact constant-selection Moran fixation. n = 6 (one-atom conditionals). The chain is solved on an explored subset; "cut" is the π-weighted rate of transitions leaving it (folded into self-loops), relative to all transitions, and "outcome cut" the same for transitions that change the payoff vector. Method: constants = whole 729-state chain by GTH; others = "hybrid" (core by log-scaled GTH, ring eliminated by its stochastic complement).

## π by outcome type

| arm | N | grand | fair pair | unfair pair | wasteful pair | disagreement | efficiency | E[max share] | P(some slot 0) | P(pair) | mass on states with a conditional | states | outcome cut |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| constants | 100 | 0.0025 | 0.3759 | 0.5958 | 0.0257 | 0.0001 | 0.9955 | 0.5987 | 0.9975 | 0.9974 | 0.0000 | 729 | 0.0e+00 |
| constants | 1000 | 0.0029 | 0.3709 | 0.6240 | 0.0023 | 0.0000 | 0.9996 | 0.6035 | 0.9971 | 0.9971 | 0.0000 | 729 | 0.0e+00 |
| constants | 10000 | 0.0029 | 0.3682 | 0.6287 | 0.0002 | 0.0000 | 1.0000 | 0.6043 | 0.9971 | 0.9971 | 0.0000 | 729 | 0.0e+00 |
| weak | 100 | 0.0101 | 0.3732 | 0.5905 | 0.0258 | 0.0004 | 0.9951 | 0.5964 | 0.9899 | 0.9895 | 0.0620 | 32259 | 9.3e-03 |
| weak | 1000 | 0.0161 | 0.3664 | 0.6151 | 0.0024 | 0.0001 | 0.9995 | 0.5998 | 0.9839 | 0.9839 | 0.0634 | 31686 | 4.0e-03 |
| weak | 10000 | 0.0167 | 0.3636 | 0.6195 | 0.0002 | 0.0000 | 1.0000 | 0.6005 | 0.9833 | 0.9833 | 0.0637 | 37998 | 3.1e-03 |
| modalPA | 100 | 0.0099 | 0.3734 | 0.5906 | 0.0256 | 0.0004 | 0.9951 | 0.5964 | 0.9901 | 0.9896 | 0.0616 | 41373 | 1.1e-02 |
| modalPA | 1000 | 0.0161 | 0.3664 | 0.6151 | 0.0024 | 0.0001 | 0.9995 | 0.5998 | 0.9839 | 0.9838 | 0.0634 | 41709 | 3.2e-03 |

## Currents and dwell

C is the net circulation P12→P13→P23→P12 (π-weighted, per mutation event); it must vanish by relabeling symmetry. "bids in" = pair-to-pair moves made by the excluded slot; "pivot" = by the member that stays; "dropped" = by the member that leaves. Dwell is per visit, in mutation events. Relaxation: the lumped 5-type chain (an estimate).

| arm | N | C | pair→pair flow | bids in | pivot | dropped | entry X→G | entry X→pairs | dwell G | dwell pair | dwell X | relaxation | max rel. π asymmetry under relabeling (top 2000) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| constants | 100 | 1.5e-19 | 4.45e-04 | 0.00e+00 | 4.45e-04 | 0.00e+00 | 1.35e-04 | 1.07e-02 | 2.36e+05 | 2.24e+03 | 92.6 | 2.38e+05 | 1.1e-14 |
| constants | 1000 | 1.4e-20 | 7.31e-05 | 0.00e+00 | 7.31e-05 | 0.00e+00 | 1.29e-04 | 9.15e-03 | 2.88e+44 | 1.36e+04 | 108 | 4.5e+15 | 1.4e-14 |
| constants | 10000 | -4.9e-21 | 8.10e-06 | 0.00e+00 | 8.10e-06 | 0.00e+00 | 0.00e+00 | 0.00e+00 | inf | 1.23e+05 | inf | inf | 7.2e-15 |
| weak | 100 | 1.4e-20 | 4.41e-04 | 1.78e-06 | 4.39e-04 | 3.53e-10 | 9.36e-05 | 1.34e-02 | 2.08e+05 | 2.21e+03 | 74.2 | 2.07e+05 | 3.6e-14 |
| weak | 1000 | -2.9e-20 | 7.25e-05 | 3.32e-07 | 7.21e-05 | 3.05e-49 | 6.67e-05 | 1.12e-02 | 3.71e+06 | 1.35e+04 | 88.6 | 3.65e+06 | 5.0e-14 |
| weak | 10000 | -8.5e-21 | 8.04e-06 | 3.86e-08 | 8.00e-06 | 0.00e+00 | 6.59e-05 | 1.09e-02 | 3.69e+07 | 1.21e+05 | 91 | 3.63e+07 | 9.8e-14 |
| modalPA | 100 | 4.1e-20 | 4.40e-04 | 1.78e-06 | 4.38e-04 | 3.53e-10 | 9.16e-05 | 1.33e-02 | 2.05e+05 | 2.22e+03 | 74.6 | 2.04e+05 | 5.3e-14 |
| modalPA | 1000 | 1.4e-19 | 7.25e-05 | 3.32e-07 | 7.21e-05 | 3.05e-49 | 6.50e-05 | 1.12e-02 | 3.71e+06 | 1.35e+04 | 88.8 | 3.65e+06 | 7.1e-14 |

### constants, N = 100

Support (top 8 of 729 states):

- 0.0185 `(2,1/2) | (1,1/2) | (2,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0185 `(3,1/2) | (3,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0185 `(3,1/2) | (1,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0185 `(3,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0185 `(2,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0185 `(2,1/2) | (1,1/2) | (1,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0162 `(2,2/3) | (1,1/3) | (1,2/3)` (unfair pair, payoffs [0.667, 0.333, 0.0])
- 0.0162 `(2,2/3) | (3,2/3) | (2,1/3)` (unfair pair, payoffs [0.0, 0.667, 0.333])

Transitions out of the top states (probability per mutation event):

- `(2,1/2) | (1,1/2) | (2,2/3)` (π 0.0185): 3.70e-04 → `(2,1/2) | (1,1/2) | (ALL,2/3)`; 3.70e-04 → `(2,1/2) | (1,1/2) | (ALL,1/3)`; 3.70e-04 → `(2,1/2) | (1,1/2) | (1,2/3)`
- `(3,1/2) | (3,2/3) | (1,1/2)` (π 0.0185): 3.70e-04 → `(3,1/2) | (3,1/3) | (1,1/2)`; 3.70e-04 → `(3,1/2) | (1,1/3) | (1,1/2)`; 3.70e-04 → `(3,1/2) | (1,1/2) | (1,1/2)`
- `(3,1/2) | (1,2/3) | (1,1/2)` (π 0.0185): 3.70e-04 → `(3,1/2) | (3,1/2) | (1,1/2)`; 3.70e-04 → `(3,1/2) | (ALL,2/3) | (1,1/2)`; 3.70e-04 → `(3,1/2) | (ALL,1/2) | (1,1/2)`
- `(3,2/3) | (3,1/2) | (2,1/2)` (π 0.0185): 3.70e-04 → `(2,1/3) | (3,1/2) | (2,1/2)`; 3.70e-04 → `(2,1/2) | (3,1/2) | (2,1/2)`; 3.70e-04 → `(2,2/3) | (3,1/2) | (2,1/2)`

Efficient triples (top by π): exit decomposition by prior mass per mutation event; bridges; exit rates at this N.

| π | state | type | strict | neutral-change | neutral-keep | deleterious | bridge mass | n bridges | drift-closed (depth 2) | exit rate strict / neutral / deleterious | entry from X |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0185 | `(2,1/2) | (1,1/2) | (2,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.6e-04 |
| 0.0185 | `(3,1/2) | (3,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.6e-04 |
| 0.0185 | `(3,1/2) | (1,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.6e-04 |
| 0.0185 | `(3,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.6e-04 |
| 0.0185 | `(2,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.6e-04 |
| 0.0185 | `(2,1/2) | (1,1/2) | (1,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.6e-04 |
| 0.0162 | `(2,2/3) | (1,1/3) | (1,2/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-03 / 1.5e-05 | 1.9e-04 |
| 0.0162 | `(2,2/3) | (3,2/3) | (2,1/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-03 / 1.5e-05 | 1.9e-04 |

Bridge example from `(2,1/2) | (1,1/2) | (2,2/3)`: slot 3 drifts to `(2,1/3)` (μ 3.7e-02), then slot 2 `(3,2/3)` (strict, ρ 4.91e-02) gives payoffs [0.0, 0.667, 0.333].

Bridge example from `(3,1/2) | (3,2/3) | (1,1/2)`: slot 2 drifts to `(1,1/3)` (μ 3.7e-02), then slot 1 `(2,2/3)` (strict, ρ 4.91e-02) gives payoffs [0.667, 0.333, 0.0].

P1 sweep: 82 efficient states with π ≥ 1e-6 checked (π mass 0.9742); drift-closed at depth 2: 1 (mass 2.51e-03): `(ALL,1/3) | (ALL,1/3) | (ALL,1/3)` 2.5e-03.

### constants, N = 1000

Support (top 8 of 729 states):

- 0.0252 `(2,1/2) | (1,1/2) | (1,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0252 `(3,1/2) | (3,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0252 `(2,1/2) | (1,1/2) | (2,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0252 `(3,1/2) | (1,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0252 `(3,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0252 `(2,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0231 `(2,1/2) | (3,2/3) | (2,1/3)` (unfair pair, payoffs [0.0, 0.667, 0.333])
- 0.0231 `(2,1/3) | (1,2/3) | (2,1/2)` (unfair pair, payoffs [0.333, 0.667, 0.0])

Transitions out of the top states (probability per mutation event):

- `(2,1/2) | (1,1/2) | (1,2/3)` (π 0.0252): 3.70e-05 → `(2,1/2) | (1,1/2) | (ALL,2/3)`; 3.70e-05 → `(2,1/2) | (1,1/2) | (ALL,1/3)`; 3.70e-05 → `(2,1/2) | (1,1/2) | (1,1/2)`
- `(3,1/2) | (3,2/3) | (1,1/2)` (π 0.0252): 3.70e-05 → `(3,1/2) | (3,1/3) | (1,1/2)`; 3.70e-05 → `(3,1/2) | (1,1/3) | (1,1/2)`; 3.70e-05 → `(3,1/2) | (1,1/2) | (1,1/2)`
- `(2,1/2) | (1,1/2) | (2,2/3)` (π 0.0252): 3.70e-05 → `(2,1/2) | (1,1/2) | (ALL,2/3)`; 3.70e-05 → `(2,1/2) | (1,1/2) | (ALL,1/3)`; 3.70e-05 → `(2,1/2) | (1,1/2) | (1,2/3)`
- `(3,1/2) | (1,2/3) | (1,1/2)` (π 0.0252): 3.70e-05 → `(3,1/2) | (3,1/2) | (1,1/2)`; 3.70e-05 → `(3,1/2) | (ALL,2/3) | (1,1/2)`; 3.70e-05 → `(3,1/2) | (ALL,1/2) | (1,1/2)`

Efficient triples (top by π): exit decomposition by prior mass per mutation event; bridges; exit rates at this N.

| π | state | type | strict | neutral-change | neutral-keep | deleterious | bridge mass | n bridges | drift-closed (depth 2) | exit rate strict / neutral / deleterious | entry from X |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0252 | `(2,1/2) | (1,1/2) | (1,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 1.2e-04 |
| 0.0252 | `(3,1/2) | (3,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 1.2e-04 |
| 0.0252 | `(2,1/2) | (1,1/2) | (2,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 1.2e-04 |
| 0.0252 | `(3,1/2) | (1,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 1.2e-04 |
| 0.0252 | `(3,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 1.2e-04 |
| 0.0252 | `(2,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 1.2e-04 |
| 0.0231 | `(2,1/2) | (3,2/3) | (2,1/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-04 / 7.3e-25 | 9.1e-05 |
| 0.0231 | `(2,1/3) | (1,2/3) | (2,1/2)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-04 / 7.3e-25 | 9.1e-05 |

Bridge example from `(2,1/2) | (1,1/2) | (1,2/3)`: slot 3 drifts to `(2,1/3)` (μ 3.7e-02), then slot 2 `(3,2/3)` (strict, ρ 4.88e-02) gives payoffs [0.0, 0.667, 0.333].

Bridge example from `(3,1/2) | (3,2/3) | (1,1/2)`: slot 2 drifts to `(1,1/3)` (μ 3.7e-02), then slot 1 `(2,2/3)` (strict, ρ 4.88e-02) gives payoffs [0.667, 0.333, 0.0].

P1 sweep: 82 efficient states with π ≥ 1e-6 checked (π mass 0.9977); drift-closed at depth 2: 1 (mass 2.88e-03): `(ALL,1/3) | (ALL,1/3) | (ALL,1/3)` 2.9e-03.

### constants, N = 10000

Support (top 8 of 729 states):

- 0.0270 `(2,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0270 `(2,1/2) | (1,1/2) | (1,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0270 `(3,1/2) | (3,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0270 `(2,1/2) | (1,1/2) | (2,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0270 `(3,1/2) | (1,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0270 `(3,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0250 `(2,2/3) | (1,1/3) | (1,1/2)` (unfair pair, payoffs [0.667, 0.333, 0.0])
- 0.0250 `(3,1/3) | (3,1/2) | (1,2/3)` (unfair pair, payoffs [0.333, 0.0, 0.667])

Transitions out of the top states (probability per mutation event):

- `(2,2/3) | (3,1/2) | (2,1/2)` (π 0.0270): 3.70e-06 → `(2,1/3) | (3,1/2) | (2,1/2)`; 3.70e-06 → `(2,1/2) | (3,1/2) | (2,1/2)`; 3.70e-06 → `(3,1/3) | (3,1/2) | (2,1/2)`
- `(2,1/2) | (1,1/2) | (1,2/3)` (π 0.0270): 3.70e-06 → `(2,1/2) | (1,1/2) | (ALL,2/3)`; 3.70e-06 → `(2,1/2) | (1,1/2) | (ALL,1/3)`; 3.70e-06 → `(2,1/2) | (1,1/2) | (1,1/2)`
- `(3,1/2) | (3,2/3) | (1,1/2)` (π 0.0270): 3.70e-06 → `(3,1/2) | (3,1/3) | (1,1/2)`; 3.70e-06 → `(3,1/2) | (1,1/3) | (1,1/2)`; 3.70e-06 → `(3,1/2) | (1,1/2) | (1,1/2)`
- `(2,1/2) | (1,1/2) | (2,2/3)` (π 0.0270): 3.70e-06 → `(2,1/2) | (1,1/2) | (ALL,2/3)`; 3.70e-06 → `(2,1/2) | (1,1/2) | (ALL,1/3)`; 3.70e-06 → `(2,1/2) | (1,1/2) | (1,2/3)`

Efficient triples (top by π): exit decomposition by prior mass per mutation event; bridges; exit rates at this N.

| π | state | type | strict | neutral-change | neutral-keep | deleterious | bridge mass | n bridges | drift-closed (depth 2) | exit rate strict / neutral / deleterious | entry from X |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0270 | `(2,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 0.0e+00 |
| 0.0270 | `(2,1/2) | (1,1/2) | (1,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 0.0e+00 |
| 0.0270 | `(3,1/2) | (3,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 0.0e+00 |
| 0.0270 | `(2,1/2) | (1,1/2) | (2,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 0.0e+00 |
| 0.0270 | `(3,1/2) | (1,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 0.0e+00 |
| 0.0270 | `(3,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 0.0e+00 |
| 0.0250 | `(2,2/3) | (1,1/3) | (1,1/2)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-05 / 2.7e-220 | 0.0e+00 |
| 0.0250 | `(3,1/3) | (3,1/2) | (1,2/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.96e-01 | 5.93e-01 | 1.48e-01 | 4 | False | 0.0e+00 / 3.0e-05 / 2.7e-220 | 0.0e+00 |

Bridge example from `(2,2/3) | (3,1/2) | (2,1/2)`: slot 1 drifts to `(2,1/3)` (μ 3.7e-02), then slot 2 `(1,2/3)` (strict, ρ 4.88e-02) gives payoffs [0.333, 0.667, 0.0].

Bridge example from `(2,1/2) | (1,1/2) | (1,2/3)`: slot 3 drifts to `(2,1/3)` (μ 3.7e-02), then slot 2 `(3,2/3)` (strict, ρ 4.88e-02) gives payoffs [0.0, 0.667, 0.333].

P1 sweep: 82 efficient states with π ≥ 1e-6 checked (π mass 0.9998); drift-closed at depth 2: 1 (mass 2.88e-03): `(ALL,1/3) | (ALL,1/3) | (ALL,1/3)` 2.9e-03.

### weak, N = 100

Support (top 8 of 32259 states):

- 0.0173 `(3,1/2) | (1,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0173 `(2,1/2) | (1,1/2) | (1,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0173 `(2,1/2) | (1,1/2) | (2,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0173 `(3,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0173 `(2,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0173 `(3,1/2) | (3,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0150 `(2,2/3) | (1,1/3) | (1,2/3)` (unfair pair, payoffs [0.667, 0.333, 0.0])
- 0.0150 `(2,2/3) | (3,2/3) | (2,1/3)` (unfair pair, payoffs [0.0, 0.667, 0.333])

Top states with a conditional program: 6.17e-05 `(2,1/2) | (1,1/2) | if(SIM(2=(3,1/2)),(ALL,1/3),(2,2/3))` (fair pair); 6.17e-05 `(3,1/2) | if(SIM(1=(2,1/2)),(ALL,1/3),(1,2/3)) | (1,1/2)` (fair pair); 6.17e-05 `(2,1/2) | (1,1/2) | if(SIM(1=(3,1/2)),(ALL,1/3),(1,2/3))` (fair pair); 6.17e-05 `(3,1/2) | if(SIM(3=(2,1/2)),(ALL,1/3),(3,2/3)) | (1,1/2)` (fair pair); 6.17e-05 `if(SIM(2=(1,1/2)),(ALL,1/3),(2,2/3)) | (3,1/2) | (2,1/2)` (fair pair)

Transitions out of the top states (probability per mutation event):

- `(3,1/2) | (1,2/3) | (1,1/2)` (π 0.0173): 3.61e-04 → `(3,1/2) | (ALL,1/3) | (1,1/2)`; 3.61e-04 → `(3,1/2) | (ALL,2/3) | (1,1/2)`; 3.61e-04 → `(3,1/2) | (1,1/3) | (1,1/2)`
- `(2,1/2) | (1,1/2) | (1,2/3)` (π 0.0173): 3.61e-04 → `(2,1/2) | (1,1/2) | (1,1/3)`; 3.61e-04 → `(2,1/2) | (1,1/2) | (ALL,2/3)`; 3.61e-04 → `(2,1/2) | (1,1/2) | (ALL,1/2)`
- `(2,1/2) | (1,1/2) | (2,2/3)` (π 0.0173): 3.61e-04 → `(2,1/2) | (1,1/2) | (2,1/3)`; 3.61e-04 → `(2,1/2) | (1,1/2) | (1,1/3)`; 3.61e-04 → `(2,1/2) | (1,1/2) | (1,1/2)`
- `(3,2/3) | (3,1/2) | (2,1/2)` (π 0.0173): 3.61e-04 → `(2,1/3) | (3,1/2) | (2,1/2)`; 3.61e-04 → `(2,1/2) | (3,1/2) | (2,1/2)`; 3.61e-04 → `(2,2/3) | (3,1/2) | (2,1/2)`

Efficient triples (top by π): exit decomposition by prior mass per mutation event; bridges; exit rates at this N.

| π | state | type | strict | neutral-change | neutral-keep | deleterious | bridge mass | n bridges | drift-closed (depth 2) | exit rate strict / neutral / deleterious | entry from X |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0173 | `(3,1/2) | (1,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(2,1/2) | (1,1/2) | (1,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(2,1/2) | (1,1/2) | (2,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(3,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(2,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(3,1/2) | (3,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0150 | `(2,2/3) | (1,1/3) | (1,2/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 528 | False | 0.0e+00 / 3.0e-03 / 1.5e-05 | 9.3e-05 |
| 0.0150 | `(2,2/3) | (3,2/3) | (2,1/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 528 | False | 0.0e+00 / 3.0e-03 / 1.5e-05 | 9.3e-05 |

Bridge example from `(3,1/2) | (1,2/3) | (1,1/2)`: slot 2 drifts to `(1,1/3)` (μ 3.6e-02), then slot 1 `(2,2/3)` (strict, ρ 4.91e-02) gives payoffs [0.667, 0.333, 0.0].

Bridge example from `(2,1/2) | (1,1/2) | (1,2/3)`: slot 1 drifts to `if(SIM(3=(ALL,1/2)),(3,1/3),(2,1/2))` (μ 3.7e-05), then slot 3 `(ALL,1/2)` (neutral-change, ρ 1.00e-02) gives payoffs [0.0, 0.0, 0.0].

P1 sweep: 150 efficient states with π ≥ 1e-6 checked (π mass 0.9170); drift-closed at depth 2: 0 (mass 0.00e+00).

### weak, N = 1000

Support (top 8 of 31686 states):

- 0.0233 `(3,1/2) | (3,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0233 `(3,1/2) | (1,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0233 `(2,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0233 `(3,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0233 `(2,1/2) | (1,1/2) | (1,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0233 `(2,1/2) | (1,1/2) | (2,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0213 `(3,1/2) | (3,1/3) | (2,2/3)` (unfair pair, payoffs [0.0, 0.333, 0.667])
- 0.0213 `(2,1/2) | (3,2/3) | (2,1/3)` (unfair pair, payoffs [0.0, 0.667, 0.333])

Top states with a conditional program: 8.32e-05 `if(SIM(3=(1,1/2)),(ALL,1/3),(3,2/3)) | (3,1/2) | (2,1/2)` (fair pair); 8.32e-05 `(3,1/2) | if(SIM(3=(2,1/2)),(ALL,1/3),(3,2/3)) | (1,1/2)` (fair pair); 8.32e-05 `(2,1/2) | (1,1/2) | if(SIM(1=(3,1/2)),(ALL,1/3),(1,2/3))` (fair pair); 8.32e-05 `(2,1/2) | (1,1/2) | if(SIM(2=(3,1/2)),(ALL,1/3),(2,2/3))` (fair pair); 8.32e-05 `if(SIM(2=(1,1/2)),(ALL,1/3),(2,2/3)) | (3,1/2) | (2,1/2)` (fair pair)

Transitions out of the top states (probability per mutation event):

- `(3,1/2) | (3,2/3) | (1,1/2)` (π 0.0233): 3.61e-05 → `(3,1/2) | (3,1/2) | (1,1/2)`; 3.61e-05 → `(3,1/2) | (ALL,1/2) | (1,1/2)`; 3.61e-05 → `(3,1/2) | (ALL,2/3) | (1,1/2)`
- `(3,1/2) | (1,2/3) | (1,1/2)` (π 0.0233): 3.61e-05 → `(3,1/2) | (3,1/3) | (1,1/2)`; 3.61e-05 → `(3,1/2) | (1,1/2) | (1,1/2)`; 3.61e-05 → `(3,1/2) | (3,1/2) | (1,1/2)`
- `(2,2/3) | (3,1/2) | (2,1/2)` (π 0.0233): 3.61e-05 → `(2,1/3) | (3,1/2) | (2,1/2)`; 3.61e-05 → `(2,1/2) | (3,1/2) | (2,1/2)`; 3.61e-05 → `(3,1/3) | (3,1/2) | (2,1/2)`
- `(3,2/3) | (3,1/2) | (2,1/2)` (π 0.0233): 3.61e-05 → `(2,1/3) | (3,1/2) | (2,1/2)`; 3.61e-05 → `(2,1/2) | (3,1/2) | (2,1/2)`; 3.61e-05 → `(2,2/3) | (3,1/2) | (2,1/2)`

Efficient triples (top by π): exit decomposition by prior mass per mutation event; bridges; exit rates at this N.

| π | state | type | strict | neutral-change | neutral-keep | deleterious | bridge mass | n bridges | drift-closed (depth 2) | exit rate strict / neutral / deleterious | entry from X |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0233 | `(3,1/2) | (3,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.4e-05 |
| 0.0233 | `(3,1/2) | (1,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.4e-05 |
| 0.0233 | `(2,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.4e-05 |
| 0.0233 | `(3,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.4e-05 |
| 0.0233 | `(2,1/2) | (1,1/2) | (1,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.4e-05 |
| 0.0233 | `(2,1/2) | (1,1/2) | (2,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.4e-05 |
| 0.0213 | `(3,1/2) | (3,1/3) | (2,2/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 527 | False | 0.0e+00 / 3.0e-04 / 7.3e-25 | 4.3e-05 |
| 0.0213 | `(2,1/2) | (3,2/3) | (2,1/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 527 | False | 0.0e+00 / 3.0e-04 / 7.3e-25 | 4.3e-05 |

Bridge example from `(3,1/2) | (3,2/3) | (1,1/2)`: slot 2 drifts to `(1,1/3)` (μ 3.6e-02), then slot 1 `(2,2/3)` (strict, ρ 4.88e-02) gives payoffs [0.667, 0.333, 0.0].

Bridge example from `(3,1/2) | (1,2/3) | (1,1/2)`: slot 2 drifts to `(1,1/3)` (μ 3.6e-02), then slot 1 `(2,2/3)` (strict, ρ 4.88e-02) gives payoffs [0.667, 0.333, 0.0].

P1 sweep: 150 efficient states with π ≥ 1e-6 checked (π mass 0.9388); drift-closed at depth 2: 0 (mass 0.00e+00).

### weak, N = 10000

Support (top 8 of 37998 states):

- 0.0249 `(2,1/2) | (1,1/2) | (2,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0249 `(3,1/2) | (1,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0249 `(3,1/2) | (3,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0249 `(2,1/2) | (1,1/2) | (1,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0249 `(2,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0249 `(3,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0231 `(3,1/3) | (3,1/2) | (1,2/3)` (unfair pair, payoffs [0.333, 0.0, 0.667])
- 0.0231 `(2,1/3) | (1,2/3) | (2,1/2)` (unfair pair, payoffs [0.333, 0.667, 0.0])

Top states with a conditional program: 8.92e-05 `(2,1/2) | (1,1/2) | if(SIM(1=(3,1/2)),(ALL,1/3),(1,2/3))` (fair pair); 8.92e-05 `(2,1/2) | (1,1/2) | if(SIM(2=(3,1/2)),(ALL,1/3),(2,2/3))` (fair pair); 8.92e-05 `if(SIM(3=(1,1/2)),(ALL,1/3),(3,2/3)) | (3,1/2) | (2,1/2)` (fair pair); 8.92e-05 `if(SIM(2=(1,1/2)),(ALL,1/3),(2,2/3)) | (3,1/2) | (2,1/2)` (fair pair); 8.92e-05 `(3,1/2) | if(SIM(1=(2,1/2)),(ALL,1/3),(1,2/3)) | (1,1/2)` (fair pair)

Transitions out of the top states (probability per mutation event):

- `(2,1/2) | (1,1/2) | (2,2/3)` (π 0.0249): 3.61e-06 → `(2,1/2) | (1,1/2) | (ALL,2/3)`; 3.61e-06 → `(2,1/2) | (1,1/2) | (2,1/3)`; 3.61e-06 → `(2,1/2) | (1,1/2) | (2,1/2)`
- `(3,1/2) | (1,2/3) | (1,1/2)` (π 0.0249): 3.61e-06 → `(3,1/2) | (1,1/3) | (1,1/2)`; 3.61e-06 → `(3,1/2) | (ALL,2/3) | (1,1/2)`; 3.61e-06 → `(3,1/2) | (ALL,1/2) | (1,1/2)`
- `(3,1/2) | (3,2/3) | (1,1/2)` (π 0.0249): 3.61e-06 → `(3,1/2) | (ALL,1/2) | (1,1/2)`; 3.61e-06 → `(3,1/2) | (3,1/2) | (1,1/2)`; 3.61e-06 → `(3,1/2) | (3,1/3) | (1,1/2)`
- `(2,1/2) | (1,1/2) | (1,2/3)` (π 0.0249): 3.61e-06 → `(2,1/2) | (1,1/2) | (1,1/3)`; 3.61e-06 → `(2,1/2) | (1,1/2) | (2,1/3)`; 3.61e-06 → `(2,1/2) | (1,1/2) | (2,1/2)`

Efficient triples (top by π): exit decomposition by prior mass per mutation event; bridges; exit rates at this N.

| π | state | type | strict | neutral-change | neutral-keep | deleterious | bridge mass | n bridges | drift-closed (depth 2) | exit rate strict / neutral / deleterious | entry from X |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0249 | `(2,1/2) | (1,1/2) | (2,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 7.2e-05 |
| 0.0249 | `(3,1/2) | (1,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 7.2e-05 |
| 0.0249 | `(3,1/2) | (3,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 7.2e-05 |
| 0.0249 | `(2,1/2) | (1,1/2) | (1,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 7.2e-05 |
| 0.0249 | `(2,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 7.2e-05 |
| 0.0249 | `(3,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 520 | False | 0.0e+00 / 3.0e-05 / 4.1e-220 | 7.2e-05 |
| 0.0231 | `(3,1/3) | (3,1/2) | (1,2/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 527 | False | 0.0e+00 / 3.0e-05 / 2.7e-220 | 3.8e-05 |
| 0.0231 | `(2,1/3) | (1,2/3) | (2,1/2)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 527 | False | 0.0e+00 / 3.0e-05 / 2.7e-220 | 3.8e-05 |

Bridge example from `(2,1/2) | (1,1/2) | (2,2/3)`: slot 1 drifts to `if(SIM(3=(ALL,1/2)),(3,1/3),(2,1/2))` (μ 3.7e-05), then slot 3 `(ALL,1/2)` (neutral-change, ρ 1.00e-04) gives payoffs [0.0, 0.0, 0.0].

Bridge example from `(3,1/2) | (1,2/3) | (1,1/2)`: slot 2 drifts to `(1,1/3)` (μ 3.6e-02), then slot 1 `(2,2/3)` (strict, ρ 4.88e-02) gives payoffs [0.667, 0.333, 0.0].

P1 sweep: 150 efficient states with π ≥ 1e-6 checked (π mass 0.9407); drift-closed at depth 2: 0 (mass 0.00e+00).

### modalPA, N = 100

Support (top 8 of 41373 states):

- 0.0173 `(2,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0173 `(3,1/2) | (1,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0173 `(2,1/2) | (1,1/2) | (1,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0173 `(3,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0173 `(2,1/2) | (1,1/2) | (2,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0173 `(3,1/2) | (3,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0150 `(2,1/3) | (1,2/3) | (2,2/3)` (unfair pair, payoffs [0.333, 0.667, 0.0])
- 0.0150 `(3,1/3) | (3,2/3) | (1,2/3)` (unfair pair, payoffs [0.333, 0.0, 0.667])

Top states with a conditional program: 8.96e-06 `if(BOX(3=(1,1/3)),(3,2/3),(2,1/3)) | (1,2/3) | (1,1/3)` (unfair pair); 8.96e-06 `(2,2/3) | if(BOX(3=(2,1/3)),(3,2/3),(1,1/3)) | (2,1/3)` (unfair pair); 8.96e-06 `(3,1/3) | (3,2/3) | if(BOX(1=(3,1/3)),(1,2/3),(2,1/3))` (unfair pair); 8.96e-06 `if(BOX(2=(1,1/3)),(2,2/3),(3,1/3)) | (1,1/3) | (1,2/3)` (unfair pair); 8.96e-06 `(3,2/3) | (3,1/3) | if(BOX(2=(3,1/3)),(2,2/3),(1,1/3))` (unfair pair)

Transitions out of the top states (probability per mutation event):

- `(2,2/3) | (3,1/2) | (2,1/2)` (π 0.0173): 3.61e-04 → `(2,1/3) | (3,1/2) | (2,1/2)`; 3.61e-04 → `(2,1/2) | (3,1/2) | (2,1/2)`; 3.61e-04 → `(3,1/3) | (3,1/2) | (2,1/2)`
- `(3,1/2) | (1,2/3) | (1,1/2)` (π 0.0173): 3.61e-04 → `(3,1/2) | (ALL,2/3) | (1,1/2)`; 3.61e-04 → `(3,1/2) | (1,1/3) | (1,1/2)`; 3.61e-04 → `(3,1/2) | (1,1/2) | (1,1/2)`
- `(2,1/2) | (1,1/2) | (1,2/3)` (π 0.0173): 3.61e-04 → `(2,1/2) | (1,1/2) | (2,1/3)`; 3.61e-04 → `(2,1/2) | (1,1/2) | (2,1/2)`; 3.61e-04 → `(2,1/2) | (1,1/2) | (2,2/3)`
- `(3,2/3) | (3,1/2) | (2,1/2)` (π 0.0173): 3.61e-04 → `(2,1/3) | (3,1/2) | (2,1/2)`; 3.61e-04 → `(2,1/2) | (3,1/2) | (2,1/2)`; 3.61e-04 → `(2,2/3) | (3,1/2) | (2,1/2)`

Efficient triples (top by π): exit decomposition by prior mass per mutation event; bridges; exit rates at this N.

| π | state | type | strict | neutral-change | neutral-keep | deleterious | bridge mass | n bridges | drift-closed (depth 2) | exit rate strict / neutral / deleterious | entry from X |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0173 | `(2,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(3,1/2) | (1,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(2,1/2) | (1,1/2) | (1,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(3,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(2,1/2) | (1,1/2) | (2,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0173 | `(3,1/2) | (3,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-03 / 3.9e-05 | 1.0e-04 |
| 0.0150 | `(2,1/3) | (1,2/3) | (2,2/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 745 | False | 0.0e+00 / 3.0e-03 / 1.5e-05 | 9.4e-05 |
| 0.0150 | `(3,1/3) | (3,2/3) | (1,2/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 745 | False | 0.0e+00 / 3.0e-03 / 1.5e-05 | 9.4e-05 |

Bridge example from `(2,2/3) | (3,1/2) | (2,1/2)`: slot 1 drifts to `(2,1/3)` (μ 3.6e-02), then slot 2 `(1,2/3)` (strict, ρ 4.91e-02) gives payoffs [0.333, 0.667, 0.0].

Bridge example from `(3,1/2) | (1,2/3) | (1,1/2)`: slot 1 drifts to `if(BOX(2=(1,2/3)),(3,1/2),(ALL,1/2))` (μ 1.2e-05), then slot 2 `(1,1/3)` (neutral-change, ρ 1.00e-02) gives payoffs [0.0, 0.0, 0.0].

P1 sweep: 150 efficient states with π ≥ 1e-6 checked (π mass 0.9144); drift-closed at depth 2: 0 (mass 0.00e+00).

### modalPA, N = 1000

Support (top 8 of 41709 states):

- 0.0233 `(2,1/2) | (1,1/2) | (1,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0233 `(2,1/2) | (1,1/2) | (2,2/3)` (fair pair, payoffs [0.5, 0.5, 0.0])
- 0.0233 `(3,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0233 `(2,2/3) | (3,1/2) | (2,1/2)` (fair pair, payoffs [0.0, 0.5, 0.5])
- 0.0233 `(3,1/2) | (3,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0233 `(3,1/2) | (1,2/3) | (1,1/2)` (fair pair, payoffs [0.5, 0.0, 0.5])
- 0.0214 `(3,2/3) | (1,1/2) | (1,1/3)` (unfair pair, payoffs [0.667, 0.0, 0.333])
- 0.0214 `(2,1/2) | (3,2/3) | (2,1/3)` (unfair pair, payoffs [0.0, 0.667, 0.333])

Top states with a conditional program: 2.23e-05 `(3,2/3) | (3,1/3) | if(BOX(2=(3,1/3)),(2,2/3),(1,1/3))` (unfair pair); 2.23e-05 `if(BOX(2=(1,1/3)),(2,2/3),(3,1/3)) | (1,1/3) | (1,2/3)` (unfair pair); 2.23e-05 `if(BOX(3=(1,1/3)),(3,2/3),(2,1/3)) | (1,2/3) | (1,1/3)` (unfair pair); 2.23e-05 `(3,1/3) | (3,2/3) | if(BOX(1=(3,1/3)),(1,2/3),(2,1/3))` (unfair pair); 2.23e-05 `(2,1/3) | if(BOX(1=(2,1/3)),(1,2/3),(3,1/3)) | (2,2/3)` (unfair pair)

Transitions out of the top states (probability per mutation event):

- `(2,1/2) | (1,1/2) | (1,2/3)` (π 0.0233): 3.61e-05 → `(2,1/2) | (1,1/2) | (ALL,2/3)`; 3.61e-05 → `(2,1/2) | (1,1/2) | (ALL,1/2)`; 3.61e-05 → `(2,1/2) | (1,1/2) | (ALL,1/3)`
- `(2,1/2) | (1,1/2) | (2,2/3)` (π 0.0233): 3.61e-05 → `(2,1/2) | (1,1/2) | (ALL,2/3)`; 3.61e-05 → `(2,1/2) | (1,1/2) | (ALL,1/2)`; 3.61e-05 → `(2,1/2) | (1,1/2) | (ALL,1/3)`
- `(3,2/3) | (3,1/2) | (2,1/2)` (π 0.0233): 3.61e-05 → `(2,1/3) | (3,1/2) | (2,1/2)`; 3.61e-05 → `(2,1/2) | (3,1/2) | (2,1/2)`; 3.61e-05 → `(2,2/3) | (3,1/2) | (2,1/2)`
- `(2,2/3) | (3,1/2) | (2,1/2)` (π 0.0233): 3.61e-05 → `(2,1/3) | (3,1/2) | (2,1/2)`; 3.61e-05 → `(2,1/2) | (3,1/2) | (2,1/2)`; 3.61e-05 → `(3,1/3) | (3,1/2) | (2,1/2)`

Efficient triples (top by π): exit decomposition by prior mass per mutation event; bridges; exit rates at this N.

| π | state | type | strict | neutral-change | neutral-keep | deleterious | bridge mass | n bridges | drift-closed (depth 2) | exit rate strict / neutral / deleterious | entry from X |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0233 | `(2,1/2) | (1,1/2) | (1,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.5e-05 |
| 0.0233 | `(2,1/2) | (1,1/2) | (2,2/3)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.5e-05 |
| 0.0233 | `(3,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.5e-05 |
| 0.0233 | `(2,2/3) | (3,1/2) | (2,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.5e-05 |
| 0.0233 | `(3,1/2) | (3,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.5e-05 |
| 0.0233 | `(3,1/2) | (1,2/3) | (1,1/2)` | fair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 738 | False | 0.0e+00 / 3.0e-04 / 1.1e-24 | 7.5e-05 |
| 0.0214 | `(3,2/3) | (1,1/2) | (1,1/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 745 | False | 0.0e+00 / 3.0e-04 / 7.3e-25 | 4.4e-05 |
| 0.0214 | `(2,1/2) | (3,2/3) | (2,1/3)` | unfair pair | 0.00e+00 | 0.00e+00 | 2.99e-01 | 5.93e-01 | 1.49e-01 | 745 | False | 0.0e+00 / 3.0e-04 / 7.3e-25 | 4.4e-05 |

Bridge example from `(2,1/2) | (1,1/2) | (1,2/3)`: slot 1 drifts to `if(BOX(3=(1,2/3)),(2,1/2),(ALL,1/2))` (μ 1.2e-05), then slot 3 `(2,1/3)` (neutral-change, ρ 1.00e-03) gives payoffs [0.0, 0.0, 0.0].

Bridge example from `(2,1/2) | (1,1/2) | (2,2/3)`: slot 1 drifts to `if(BOX(3=(2,2/3)),(2,1/2),(ALL,1/2))` (μ 1.2e-05), then slot 3 `(2,1/3)` (neutral-change, ρ 1.00e-03) gives payoffs [0.0, 0.0, 0.0].

P1 sweep: 150 efficient states with π ≥ 1e-6 checked (π mass 0.9353); drift-closed at depth 2: 0 (mass 0.00e+00).

## Pair-to-pair moves and net currents between outcome types

Pair-to-pair moves that change payoffs, by the pivot's share before -> after (the pivot is the member that stays and switches partner; π-weighted flow per mutation event). Net current between outcome types: J(a->b) - J(b->a), positive entries only.

- `constants_N100`: pivot 0.333 -> 0.5 1.23e-04, pivot 0.5 -> 0.667 9.57e-05, pivot 0.333 -> 0.667 8.96e-05, pivot 0.5 -> 0.5 5.31e-05, pivot 0.333 -> 0.333 5.22e-05. Net: fair>unfair 1.91e-05, unfair>wasteful 1.88e-05, unfair>X 3.50e-07, wasteful>fair 1.90e-05, X>fair 1.55e-07, X>wasteful 1.95e-07.
- `constants_N1000`: pivot 0.333 -> 0.5 2.66e-05, pivot 0.5 -> 0.667 2.29e-05, pivot 0.333 -> 0.667 1.43e-05, pivot 0.5 -> 0.5 3.56e-06, pivot 0.333 -> 0.333 3.15e-06. Net: fair>unfair 3.64e-06, unfair>wasteful 3.64e-06, wasteful>fair 3.64e-06.
- `constants_N10000`: pivot 0.333 -> 0.5 3.07e-06, pivot 0.5 -> 0.667 2.67e-06, pivot 0.333 -> 0.667 1.53e-06, pivot 0.5 -> 0.5 3.09e-07, pivot 0.333 -> 0.333 2.65e-07. Net: fair>unfair 3.91e-07, unfair>wasteful 3.91e-07, wasteful>fair 3.91e-07.
- `modalPA_N100`: pivot 0.333 -> 0.5 1.23e-04, pivot 0.5 -> 0.667 9.54e-05, pivot 0.333 -> 0.667 8.92e-05, pivot 0.5 -> 0.5 5.18e-05, pivot 0.333 -> 0.333 5.04e-05. Net: grand>X 3.03e-10, fair>unfair 1.92e-05, fair>X 4.12e-07, unfair>grand 3.03e-10, unfair>wasteful 1.80e-05, unfair>X 1.23e-06, wasteful>fair 1.96e-05, X>wasteful 1.64e-06.
- `modalPA_N1000`: pivot 0.333 -> 0.5 2.63e-05, pivot 0.5 -> 0.667 2.26e-05, pivot 0.333 -> 0.667 1.42e-05, pivot 0.5 -> 0.5 3.54e-06, pivot 0.333 -> 0.333 3.11e-06. Net: grand>fair 1.12e-09, grand>unfair 1.27e-09, grand>wasteful 1.12e-09, fair>unfair 3.62e-06, fair>X 7.68e-08, unfair>wasteful 3.50e-06, unfair>X 1.20e-07, wasteful>fair 3.70e-06, X>grand 3.51e-09, X>wasteful 1.93e-07.
- `weak_N100`: pivot 0.333 -> 0.5 1.23e-04, pivot 0.5 -> 0.667 9.53e-05, pivot 0.333 -> 0.667 8.91e-05, pivot 0.5 -> 0.5 5.23e-05, pivot 0.333 -> 0.333 5.10e-05. Net: grand>X 3.32e-10, fair>unfair 1.92e-05, fair>X 3.75e-07, unfair>grand 3.32e-10, unfair>wasteful 1.80e-05, unfair>X 1.19e-06, wasteful>fair 1.96e-05, X>wasteful 1.57e-06.
- `weak_N1000`: pivot 0.333 -> 0.5 2.63e-05, pivot 0.5 -> 0.667 2.26e-05, pivot 0.333 -> 0.667 1.42e-05, pivot 0.5 -> 0.5 3.54e-06, pivot 0.333 -> 0.333 3.11e-06. Net: grand>fair 1.12e-09, grand>unfair 1.27e-09, grand>wasteful 1.12e-09, fair>unfair 3.62e-06, fair>X 7.48e-08, unfair>wasteful 3.51e-06, unfair>X 1.17e-07, wasteful>fair 3.70e-06, X>grand 3.50e-09, X>wasteful 1.88e-07.
- `weak_N10000`: pivot 0.333 -> 0.5 3.03e-06, pivot 0.5 -> 0.667 2.64e-06, pivot 0.333 -> 0.667 1.52e-06, pivot 0.5 -> 0.5 3.11e-07, pivot 0.333 -> 0.333 2.65e-07. Net: grand>fair 1.18e-10, grand>unfair 1.34e-10, grand>wasteful 1.17e-10, fair>unfair 3.90e-07, fair>X 8.16e-09, unfair>wasteful 3.78e-07, unfair>X 1.24e-08, wasteful>fair 3.98e-07, X>grand 3.70e-10, X>wasteful 2.02e-08.

## Hand-built handshakes (N = 1000): do conditional pairs or grand coalitions leak less than constants?

| arm | triple | outcome | strict | neutral keep | neutral change | deleterious | bridge mass | n bridges |
|---|---|---|---|---|---|---|---|---|
| weak | fair-pair handshake 12 (slot 3 (ALL,1/3)) | disagreement | 1.72e-02 | 8.17e-04 | 0.00e+00 | 0.00e+00 | 8.17e-01 | 2488 |
| weak | fair-pair constants 12 (slot 3 (ALL,1/3)) | fair pair | 0.00e+00 | 2.99e-04 | 0.00e+00 | 7.33e-25 | 1.49e-01 | 524 |
| weak | cyclic grand handshake 1<-2<-3<-1 | disagreement | 1.03e-02 | 8.92e-04 | 0.00e+00 | 0.00e+00 | 8.92e-01 | 2703 |
| weak | grand: two readers of each other + constant | disagreement | 6.96e-03 | 8.91e-04 | 0.00e+00 | 0.00e+00 | 8.16e-01 | 2412 |
| weak | grand constants | grand | 0.00e+00 | 2.67e-06 | 0.00e+00 | 3.48e-45 | 3.34e-04 | 54 |
| modalPA | fair-pair handshake 12 (slot 3 (ALL,1/3)) | fair pair | 0.00e+00 | 3.70e-04 | 0.00e+00 | 7.32e-25 | 1.48e-01 | 620 |
| modalPA | fair-pair constants 12 (slot 3 (ALL,1/3)) | fair pair | 0.00e+00 | 2.99e-04 | 0.00e+00 | 7.33e-25 | 1.49e-01 | 738 |
| modalPA | cyclic grand handshake 1<-2<-3<-1 | grand | 0.00e+00 | 1.09e-04 | 0.00e+00 | 3.49e-45 | 1.67e-04 | 27 |
| modalPA | grand: two readers of each other + constant | grand | 0.00e+00 | 7.34e-05 | 0.00e+00 | 3.48e-45 | 2.22e-04 | 36 |
| modalPA | grand constants | grand | 0.00e+00 | 2.67e-06 | 0.00e+00 | 3.48e-45 | 3.34e-04 | 54 |
| modal | fair-pair handshake 12 (slot 3 (ALL,1/3)) | fair pair | 0.00e+00 | 3.70e-04 | 0.00e+00 | 7.32e-25 | 1.49e-01 | 1260 |
| modal | fair-pair constants 12 (slot 3 (ALL,1/3)) | fair pair | 0.00e+00 | 2.99e-04 | 0.00e+00 | 7.33e-25 | 1.49e-01 | 1484 |
| modal | cyclic grand handshake 1<-2<-3<-1 | grand | 0.00e+00 | 1.09e-04 | 0.00e+00 | 3.49e-45 | 1.67e-04 | 54 |
| modal | grand: two readers of each other + constant | grand | 0.00e+00 | 7.34e-05 | 0.00e+00 | 3.48e-45 | 2.41e-04 | 78 |
| modal | grand constants | grand | 0.00e+00 | 2.67e-06 | 0.00e+00 | 3.48e-45 | 3.34e-04 | 108 |

- `modalPA_N100`: π mass by number of conditional slots {'0': 0.9384, '1': 0.0616, '2': 0.0, '3': 0.0} (states {'0': 729, '1': 40644, '2': 0, '3': 0}).
- `modalPA_N1000`: π mass by number of conditional slots {'0': 0.9366, '1': 0.0634, '2': 0.0, '3': 0.0} (states {'0': 729, '1': 40980, '2': 0, '3': 0}).

## Named efficient triples: exits, bridges, invasion tables

Exit rates are probabilities per mutation event at that N (strict = mutant gains; neutral = mutant's payoff unchanged, outcome kept or changed; deleterious). Bridge mass: prior mass per mutation event of outcome-keeping neutral entrants after which a strict or outcome-changing neutral exit exists. Drift-closed (depth 2): no strict exit, no outcome-changing neutral exit, no bridge.

| arm | N | triple | strict | neutral keep | neutral change | deleterious | bridge mass | n bridges | drift-closed |
|---|---|---|---|---|---|---|---|---|---|
| constants | 100 | grand (ALL,1/3)^3 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 4.24e-06 | 0.00e+00 | 0 | True |
| constants | 100 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.96e-03 | 0.00e+00 | 2.58e-05 | 1.48e-01 | 4 | False |
| constants | 100 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.96e-03 | 0.00e+00 | 1.45e-05 | 1.48e-01 | 4 | False |
| constants | 1000 | grand (ALL,1/3)^3 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 3.48e-45 | 0.00e+00 | 0 | True |
| constants | 1000 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.96e-04 | 0.00e+00 | 7.33e-25 | 1.48e-01 | 4 | False |
| constants | 1000 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.96e-04 | 0.00e+00 | 3.66e-25 | 1.48e-01 | 4 | False |
| constants | 10000 | grand (ALL,1/3)^3 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0 | True |
| constants | 10000 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.96e-05 | 0.00e+00 | 2.71e-220 | 1.48e-01 | 4 | False |
| constants | 10000 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.96e-05 | 0.00e+00 | 1.35e-220 | 1.48e-01 | 4 | False |
| weak | 100 | grand (ALL,1/3)^3 | 0.00e+00 | 2.67e-05 | 0.00e+00 | 4.24e-06 | 3.34e-04 | 54 | False |
| weak | 100 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-03 | 0.00e+00 | 2.58e-05 | 1.49e-01 | 524 | False |
| weak | 100 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-03 | 0.00e+00 | 1.45e-05 | 1.49e-01 | 534 | False |
| weak | 1000 | grand (ALL,1/3)^3 | 0.00e+00 | 2.67e-06 | 0.00e+00 | 3.48e-45 | 3.34e-04 | 54 | False |
| weak | 1000 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-04 | 0.00e+00 | 7.33e-25 | 1.49e-01 | 524 | False |
| weak | 1000 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-04 | 0.00e+00 | 3.66e-25 | 1.49e-01 | 534 | False |
| weak | 10000 | grand (ALL,1/3)^3 | 0.00e+00 | 2.67e-07 | 0.00e+00 | 0.00e+00 | 3.34e-04 | 54 | False |
| weak | 10000 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-05 | 0.00e+00 | 2.71e-220 | 1.49e-01 | 524 | False |
| weak | 10000 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-05 | 0.00e+00 | 1.35e-220 | 1.49e-01 | 534 | False |
| modalPA | 100 | grand (ALL,1/3)^3 | 0.00e+00 | 2.67e-05 | 0.00e+00 | 4.24e-06 | 3.34e-04 | 54 | False |
| modalPA | 100 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-03 | 0.00e+00 | 2.58e-05 | 1.49e-01 | 738 | False |
| modalPA | 100 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-03 | 0.00e+00 | 1.45e-05 | 1.49e-01 | 747 | False |
| modalPA | 1000 | grand (ALL,1/3)^3 | 0.00e+00 | 2.67e-06 | 0.00e+00 | 3.48e-45 | 3.34e-04 | 54 | False |
| modalPA | 1000 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-04 | 0.00e+00 | 7.33e-25 | 1.49e-01 | 738 | False |
| modalPA | 1000 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-04 | 0.00e+00 | 3.66e-25 | 1.49e-01 | 747 | False |
| modalPA | 10000 | grand (ALL,1/3)^3 | 0.00e+00 | 2.67e-07 | 0.00e+00 | 0.00e+00 | 3.34e-04 | 54 | False |
| modalPA | 10000 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-05 | 0.00e+00 | 2.71e-220 | 1.49e-01 | 738 | False |
| modalPA | 10000 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-05 | 0.00e+00 | 1.35e-220 | 1.49e-01 | 747 | False |
| modal | 100 | grand (ALL,1/3)^3 | 0.00e+00 | 2.67e-05 | 0.00e+00 | 4.24e-06 | 3.34e-04 | 108 | False |
| modal | 100 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-03 | 0.00e+00 | 2.58e-05 | 1.49e-01 | 1484 | False |
| modal | 100 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-03 | 0.00e+00 | 1.45e-05 | 1.49e-01 | 1503 | False |
| modal | 1000 | grand (ALL,1/3)^3 | 0.00e+00 | 2.67e-06 | 0.00e+00 | 3.48e-45 | 3.34e-04 | 108 | False |
| modal | 1000 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-04 | 0.00e+00 | 7.33e-25 | 1.49e-01 | 1484 | False |
| modal | 1000 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-04 | 0.00e+00 | 3.66e-25 | 1.49e-01 | 1503 | False |
| modal | 10000 | grand (ALL,1/3)^3 | 0.00e+00 | 2.67e-07 | 0.00e+00 | 0.00e+00 | 3.34e-04 | 108 | False |
| modal | 10000 | fair pair 12, slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-05 | 0.00e+00 | 2.71e-220 | 1.49e-01 | 1484 | False |
| modal | 10000 | unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3) | 0.00e+00 | 2.99e-05 | 0.00e+00 | 1.35e-220 | 1.49e-01 | 1503 | False |
- constants, fair pair 12, slot 3 (ALL,1/3): slot 3 drifts to `(2,1/3)` (μ 3.7e-02 per slot), then slot 2 plays `(3,2/3)` (strict, ρ 4.91e-02 at N = 100), payoffs [0.0, 0.667, 0.333].
- constants, unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3): slot 3 drifts to `(2,1/3)` (μ 3.7e-02 per slot), then slot 2 plays `(3,2/3)` (strict, ρ 9.52e-02 at N = 100), payoffs [0.0, 0.667, 0.333].
- weak, grand (ALL,1/3)^3: slot 1 drifts to `if(SIM(2=(1,1/3)),(2,1/3),(ALL,1/3))` (μ 6.2e-06 per slot), then slot 2 plays `(1,1/3)` (neutral-change, ρ 1.00e-02 at N = 100), payoffs [0.333, 0.333, 0.0].
- weak, fair pair 12, slot 3 (ALL,1/3): slot 1 drifts to `if(SIM(3=(ALL,1/2)),(3,1/3),(2,1/2))` (μ 3.7e-05 per slot), then slot 3 plays `(ALL,1/2)` (neutral-change, ρ 1.00e-02 at N = 100), payoffs [0.0, 0.0, 0.0].
- weak, unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3): slot 1 drifts to `if(SIM(3=(ALL,1/2)),(3,1/3),(2,2/3))` (μ 3.7e-05 per slot), then slot 3 plays `(ALL,1/2)` (neutral-change, ρ 1.00e-02 at N = 100), payoffs [0.0, 0.0, 0.0].
- modalPA, grand (ALL,1/3)^3: slot 1 drifts to `if(BOX(2=(1,1/3)),(2,1/3),(ALL,1/3))` (μ 6.2e-06 per slot), then slot 2 plays `(1,1/3)` (neutral-change, ρ 1.00e-02 at N = 100), payoffs [0.333, 0.333, 0.0].
- modalPA, fair pair 12, slot 3 (ALL,1/3): slot 1 drifts to `if(BOX(3=(ALL,1/3)),(2,1/2),(ALL,1/2))` (μ 1.2e-05 per slot), then slot 3 plays `(2,1/3)` (neutral-change, ρ 1.00e-02 at N = 100), payoffs [0.0, 0.0, 0.0].
- modalPA, unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3): slot 1 drifts to `if(BOX(3=(ALL,1/3)),(2,2/3),(ALL,1/2))` (μ 1.2e-05 per slot), then slot 3 plays `(2,1/3)` (neutral-change, ρ 1.00e-02 at N = 100), payoffs [0.0, 0.0, 0.0].
- modal, grand (ALL,1/3)^3: slot 1 drifts to `if(BOX(2=(1,1/3)),(2,1/3),(ALL,1/3))` (μ 3.1e-06 per slot), then slot 2 plays `(1,1/3)` (neutral-change, ρ 1.00e-02 at N = 100), payoffs [0.333, 0.333, 0.0].
- modal, fair pair 12, slot 3 (ALL,1/3): slot 1 drifts to `if(BOX(2=(1,1/2)),(2,1/2),(2,1/3))` (μ 3.1e-06 per slot), then slot 2 plays `(1,2/3)` (strict, ρ 4.91e-02 at N = 100), payoffs [0.333, 0.667, 0.0].
- modal, unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3): slot 1 drifts to `if(BOX(2=(1,1/3)),(2,2/3),(2,1/3))` (μ 3.1e-06 per slot), then slot 2 plays `(1,2/3)` (strict, ρ 9.52e-02 at N = 100), payoffs [0.333, 0.667, 0.0].

## Method checks

- `modalPA_N100_ring1` (hybrid, 19119 states): grand 0.0023, fair pair 0.3837, unfair pair 0.5896, wasteful pair 0.0243, disagreement 0.0001; E[max] 0.5977; outcome cut 6.7e-02
- `modalPA_N100_ringonly` (?, 24663 states): grand 0.0028, fair pair 0.3755, unfair pair 0.5963, wasteful pair 0.0252, disagreement 0.0001; E[max] 0.5987; outcome cut —
- `modal_N100_ring1` (hybrid, 28143 states): grand 0.0024, fair pair 0.3734, unfair pair 0.5996, wasteful pair 0.0245, disagreement 0.0001; E[max] 0.5993; outcome cut 7.1e-02
- `weak_N1000_theta1e-9` (hybrid, 3081 states): grand 0.0016, fair pair 0.3714, unfair pair 0.6246, wasteful pair 0.0023, disagreement 0.0000; E[max] 0.6038; outcome cut 1.7e-02
- `weak_N100_ringonly` (?, 19707 states): grand 0.0031, fair pair 0.3747, unfair pair 0.5965, wasteful pair 0.0255, disagreement 0.0002; E[max] 0.5987; outcome cut —

## Agent-based runs (finite εN = 0.1 per slot per generation; approach rates, not π)

N = 100 per slot, ε = 10⁻³ per birth, w = 0.3, 10⁵ generations, records every 10 generations. Dominant label: outcome of the triple of majority classes, or "mixed".

| arm | start | seed | grand | fair | unfair | wasteful | disagreement | pair runs | mean interior pair dwell (gens) | pair→pair switches | first gen with P(pair) > 0.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| modal | uniform | 1 | 0.000 | 0.586 | 0.351 | 0.048 | 0.016 | 79 | 1235 | 22 | 0 |
| modal | uniform | 2 | 0.000 | 0.059 | 0.846 | 0.075 | 0.019 | 85 | 1173 | 31 | 10 |
| modal | uniform | 3 | 0.000 | 0.469 | 0.467 | 0.052 | 0.012 | 87 | 1132 | 37 | 10 |
| modal | grand | 1 | 0.257 | 0.252 | 0.446 | 0.029 | 0.017 | 43 | 1680 | 13 | 26440 |
| modal | grand | 2 | 0.968 | 0.000 | 0.000 | 0.000 | 0.032 | 0 | — | 0 | None |
| modal | grand | 3 | 0.647 | 0.183 | 0.114 | 0.028 | 0.028 | 40 | 787 | 13 | 67100 |
| weak | uniform | 1 | 0.000 | 0.519 | 0.409 | 0.035 | 0.037 | 57 | 1684 | 12 | 170 |
| weak | uniform | 2 | 0.000 | 0.176 | 0.716 | 0.093 | 0.015 | 99 | 1009 | 36 | 110 |
| weak | uniform | 3 | 0.000 | 0.211 | 0.739 | 0.028 | 0.021 | 66 | 1488 | 13 | 900 |
| weak | grand | 1 | 0.487 | 0.223 | 0.232 | 0.014 | 0.044 | 22 | 2126 | 7 | 50180 |
| weak | grand | 2 | 0.968 | 0.000 | 0.000 | 0.000 | 0.032 | 0 | — | 0 | None |
| weak | grand | 3 | 0.647 | 0.139 | 0.176 | 0.010 | 0.028 | 27 | 1190 | 5 | 67100 |

modal: mean interior pair dwell across seeds and starts 1201 generations (range 787–1680, 5 runs).

weak: mean interior pair dwell across seeds and starts 1500 generations (range 1009–2126, 5 runs).
