# Spec: the pair-worth easy case along N: coordination supply, dose, and what reading adds, 2026-11-03

Status: draft by the RE; to be reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`,
folded [after second review]); to be run by a Sonnet subagent. Queue 73. Follow-up to queue 72 (RESULTS "The pair-worth-a
game on islands"). The RS approved the run on 2026-11-03 ("Sure") after the RE proposed it: rerun the easy case at
N = 200–400 with the per-split seed count above one, to see whether bids keep helping.

## Context

Queue 72, G⅓ (pair worth ⅓, sixths, 21 actions per slot), mN = 1, Λ = 10, annealed tail, paired founders:

| N | C (constants) | C+B\* (bids on all 28 splits, δ = 0.05) | runs |
|---|---|---|---|
| 100 | 0.45 [0.25, 0.65] | 0.25 (0.25 over 60 runs) | 20 / 60 |
| 200 | 0.56 | 0.80 | 20 (exploratory) |
| 400 | 0.33 | 0.85 | 20 (exploratory) |

and at N = 100 the core share of C+B\* does **not** rise with dose: 0.35 / 0.25 / 0.11 / 0.15 / 0.09 at δ = 0.01 / 0.05 /
0.15 / 0.30 / 0.50 (mN = 1; the last four with up to 1.8 seeds per split per slot), while C+G (grand constants at
δ = 0.05, no reading) reaches 0.80. The RE's proposal ("per-split seed count above one") is therefore already refuted
at N = 100: a dose of 1.8 seeds per split gave the lowest core share. Two readings of the N = 200–400 gain remain:

- **H_supply.** Bids coordinate only when three slots hold a bid on the *same* split σ (a bid reads exactly σ_j, σ_k).
  With n_σ = δN/28 bids per slot per split, the expected number of same-σ triples on an island at founding is
  T = 28·n_σ³: 0.16, 1.3, 10 at N = 100, 200, 400 (δ = 0.05). The gain appears when T ≳ 1. At high dose, many split
  types coexist and mixed-σ bidders meet at the exclusion split (a pair), so supply can overshoot (the RE's inference
  from queue 72's agent notes; not tested).
- **H_N.** N itself is the lever (selection against drift: N·s = 5 at N = 100, 20 at N = 400 for a 1/6-dollar payoff
  gap at w = 0.3), so dose is irrelevant once N is large.

Constants compose differently: G(σ) constants (ALL, σ_i) form the grand coalition for *any* three demands summing to
at most 1, so a random triple of grand constants is compatible with probability far above 1/28² — the likely reason C+G
beats C+B\* at N = 100. A bid that read feasibility, not equality, would repair that: the **flexible bid** F below. The
queue-72 REJECTED entry says the easy-case conjecture may be re-opened "only with a bid that coordinates the split
without a menu, or at a size where per-split seed counts exceed one"; this spec does both.

**What it is for.** The RS's easy-case conjecture (every island in the core, every core point appearing) is the
cleanest test of whether the ecology selects a solution concept at all; queue 72 says it fails at N = 100 in the arm
registered for it. If the gain is a supply effect, bids are worth pursuing only where the supply exists, and constants
(which need no reading) are the benchmark any reading program must beat; if reading never beats constants, the
realizable arm's reading advantage must be argued against constants, not defection.

REJECTED.md checked. Re-opens: "The RS's easy-case conjecture … in C+B\*" at larger N and a menu-free bid, as the entry
itself allows. Does not re-open: accept-pair bids (a different object: C+A accepts pair offers; F accepts grand offers),
the ring (a grid property), or stage 2 (arm T bids and hook-written bids stay gated off: the queue-72 gate did not
fire; this run is not a gate re-test unless RE 3 or RE 4 below fires it, in which case the RE writes the stage 2 spec).

## The object

As queue 72 (`src/pair_worth*.py`; spec 2026-11-01-pair-worth §The object): three slot populations per island,
mean-field expected payoffs, Moran birth–death with fitness exp(w·payoff), w = 0.3, migration m = mN/N per birth from a
uniformly random other island, I = 64 islands, annealed tail ε(t) = (Λ/t₀)(1 + (t − 200)/t₀)⁻² from generation 200 with
t₀ = N/2, Λ ∈ {0, 10}, cut at 100·N generations followed by a 20·N tail-free chase, founders paired across arms, tails
and mN. Game: G⅓ only (sixths grid). Programs: the queue-72 catalogue, level-1 handshake bids (the repaired main arm B\*
and the exclusion bid B as in queue 72; level-0 variants are not rerun).

## Arms

- **C**, **C+B\*** (bids on all 28 grand splits), **C+B** (core-only menu, 19 splits), **C+G** (grand constants on all 28
  splits), each at dose δ as in queue 72 (δ = total seed mass per slot). Same definitions and code as queue 72.
- **C+F (new): flexible grand bid.** For slot i with others j < k and share σ_i of a split (the F family is indexed by
  σ_i alone, over the same 28 splits' per-slot shares, so the family has at most 7 distinct shares per slot; one
  program F(σ_i; c) per share and constant c):
  `if ⋁_{(a,b) : a + b ≤ 1 − σ_i} (□(j = (ALL, a)) ∧ □(k = (ALL, b))) then (ALL, σ_i)`
  `elif □(j = (i, π_j(σ_i; i, j))) then (j, π_i(σ_i; i, j))` `elif □(k = (i, π_k(σ_i; i, k))) then (k, π_i(σ_i; i, k))`
  `else c`.
  The disjunction runs over the grid's demands a, b (0…6 sixths). [after review] The two handshake lines read their
  atoms at **level 1** (`BOX_1`, PA + Con(PA)), exactly the queue-72 repair R1 (notes/pair-worth.md 1.3); at level 0 the
  fallback never fires. π is the queue-72 exclusion split, which at G⅓ is (⅙, ⅙) for every pair and every σ (the pair
  worth is two ticks, split equally), so two F's with different shares still agree on the pair. F is a reading program
  that accepts any feasible grand coalition and keeps the exclusion fallback; against constants it is on-path identical
  to the grand constant (ALL, σ_i) whenever the others' constants sum to at most 1 − σ_i. Dose δ per slot; [after
  review] σ_i is drawn from the per-slot marginal of the 28 splits, weight (7 − s)/28 for a share of s sixths (the same
  marginal as C+G and C+B\*; uniform over the 7 shares would make random F triples mostly infeasible), and c uniform.
- **C+F₄ (core-bounded F, secondary)** [after review]. F with σ_i ≤ 4/6 only (the core's per-slot bound), weights
  renormalized; separates failures from non-core grand splits from pair traps. The static question is whether the Löbian joint fixed point of three F's with feasible σ's plays the
  grand coalition (engineer: V6 below; the RE expects yes, since the disjunct containing the true tuple holds
  self-consistently, and states the play before evaluation).
- **Stored arms not rerun:** the queue-72 cells at N = 100 (60 runs for C, C+B\*, C+B; 20 for C+G, C+A and doses).

## Design

1. **Static numbers (before any counted cell).** For each arm at δ = 0.05 and each N ∈ {100, 200, 400, 800}:
   (a) the probability that a triple of founder draws (one program per slot from the arm's seed law, uniform within
   family) plays the grand coalition, by exact evaluation over the catalogue; (b) the expected number of grand-playing
   triples among the founders of one island (N per slot, seeded fraction, not requiring same-σ: T generalized, exact);
   (c) the same-σ triple count T = 28·n_σ³ for B\* and the analogue for C+B, C+F, and for dose cells δ ∈ {0.0125,
   0.025, 0.15, 0.5}. Report them next to the run results: these are the supply numbers the hypotheses use.
2. **Validation.** (V1) Re-run runs 0–2 of stored cells (G⅓ C, C+B\* at N = 200, mN = 1, both Λ) and reproduce the
   stored rows exactly (deterministic founders by run index); (V2) at N = 400 runs 0–1 of C+B\* likewise. (V6) F's
   closed-form outcome rule against direct modal evaluation (GL chain, `modal.py`) on 1,000 random triples including
   mixed σ, infeasible sums, constants that mimic F's output, and F next to B; the play of F³ at every feasible triple
   of shares, stated before evaluation (grand coalition).
3. **Counted cells** (Λ ∈ {0, 10}; each job is one (arm, N, run) with all listed mN; founders paired across arms).
   Confirmatory runs are **20–59** for the cells the predictions score at N = 200 and 400 (stored runs 0–19 of C and
   C+B\* are exploratory and are reported separately and pooled with disclosure); all other cells use runs 0–19.
   - **A. N = 200**, mN ∈ {1, 0}: C, C+B\*, C+G, C+B, C+F at δ = 0.05 (40 runs each for C, C+B\*, C+G; 20 for C+B, C+F);
     C+B\* at δ ∈ {0.025, 0.15, 0.5}, 20 runs each; [after review] C+F₄ at δ = 0.05, 20 runs.
   - **B. N = 400**, mN = 1: C, C+B\*, C+G at δ = 0.05, 40 runs each; C+B, C+F at δ = 0.05, 20 runs;
     C+B\* at δ ∈ {0.0125, 0.15, 0.5}, 20 runs each. mN = 0: C, C+B\*, C+G, C+F, 20 runs each, δ = 0.05; [after review]
     C+B\* at δ = 0.0125, 20 runs (local supply T against metapopulation supply I·T).
   - **C. N = 100**, mN ∈ {1, 0}: [after review] C+F on runs 0–59 and C+G extended to runs 20–59, so that C, C+B\*, C+B,
     C+G and C+F are all paired on 60 runs (C, C+B\*, C+B are stored at 60).
   - **D. N = 800** (cut first; pilot one run before launch and report the per-record time), mN = 1, Λ = 10 only: C,
     C+B\*, C+G, 10 runs each.
   - Cut order (report every cut): D; C+F₄; mN = 0 at N = 400; the dose cells at N = 400; C+B and C+F at N = 400; the extra
     40-run replication at N = 200. Validation, static numbers and cells A and B for C, C+B\*, C+G at δ = 0.05 (mN = 1)
     are never cut.
4. **Statistics**, per island from the modal outcome as in queue 72 (core proper / ring / efficient dominated /
   undominated wasteful / dominated wasteful / null; kind classes grand / pair), at the end and over the last 2,000
   generations, plus:
   - run-level paired differences between arms on shared founders, with percentile bootstrap intervals **over runs** (at
     mN = 1 islands synchronize, so the effective sample is runs, not islands; report consensus and the share of runs in
     which at least 0.9 of islands are in the core);
   - **supply realized**: per island, the number of same-σ bid triples (and of F, G, and C compatible grand triples) in
     the founders and the first generation at which a grand state is held (any class "grand"), and core entry and exit
     events per island-generation (debounced 25 generations) with the program families present at each event, so entry
     and exit hazards are read per N, not inferred from end shares (discipline 5; these are encounter-level, ε-free
     quantities where the debounce is not an approximation);
   - **who holds the core**: in core islands at the end, the shares of the majority triple that are bids, F, grand
     constants of the same split and other constants;
   - core coverage at mN = 0 (the RS's clause): how many of the 19 core points occur at the end on some island, pooled
     over runs, with frequencies and run-clustered simultaneous 95% intervals against the threshold 1/76; at mN = 1 the
     number of runs reaching consensus on one split;
   - the non-core grand splits (the 9 splits with a share > ⅔) held by bids at the end (dominated grand islands).
5. **Budget.** 3 workers, BLAS threads 1. From the queue-72 timings (kernel per (Λ, mN) record: N = 200 18–29 s,
   N = 400 190–280 s; N = 800 extrapolated at 40–60 min per record) the confirmatory cells cost about 16 core-hours at
   N = 400 (mN = 1), 7 at mN = 0, 9 at N = 200 and 20 at N = 800: about 20 hours at 3 workers in all. Cut in the order
   above if the pilot at N = 800 or the first N = 400 records run over by more than 1.5×.

## Required outputs

- `runs/pair-worth-n.md` and `.json`; rows under `runs/pair_worth_n/`; `notes/pair-worth-n.md` (engineer's notes, every
  deviation disclosed in the report too); `predictions/2026-11-03-pair-worth-n.md` from this spec, with the static
  numbers, committed before any counted cell; the static numbers' file, `runs/pair_worth_n/static.json`.
- Tables: static supply numbers per arm and N; end class shares with run-level intervals per cell; paired differences;
  dose–response at N = 200, 400 (and N = 100 from the stored cells, labelled stored); entry and exit hazards per N and
  arm; who holds the core; core coverage at mN = 0.
- Drafts for RESULTS, REJECTED (every failed prediction, the RE's, the RS's and the engineer's), THEORY if a claim
  moves, NOTATION (F, T, n_σ, supply).

## Predictions, with falsifiers

Scored on confirmatory runs (20–59) at mN = 1, Λ = 10 unless stated; "core" is core proper at the end of the run, paired
differences on shared founders with run-level bootstrap intervals; a bound counts as met only if the point estimate
meets it and the stated sample is complete.

**The RS's conjecture, re-scored at larger N.** G⅓: core ≥ 0.95 of islands at mN = 1 in some arm at N = 400, and at
mN = 0 every core point has island frequency ≥ 1/76 (run-clustered simultaneous 95% intervals) in C+B\*. *The RS is
invited to state his own prediction for N = 400 (does any arm reach 0.95; does the coverage clause hold).*

**RE.**

1. **Supply, not N or dose, is the lever for bids.** N = 400: C+B\* at δ = 0.05 (T ≈ 10) has core ≥ 0.7 and ≥ 0.3 above C;
   C+B\* at δ = 0.0125 (T ≈ 0.16, the N = 100 supply) has core within 0.15 of C. N = 200, δ = 0.025 (T ≈ 0.16): within
   0.15 of C. *Falsifier:* any bound violated (a violation of the δ = 0.0125 clause is the H_N reading).
2. **Dose is non-monotone at large N.** N = 400: C+B\* at δ = 0.5 (n_σ ≈ 7; mixed-σ bidders pair at the exclusion split)
   is at least 0.15 below δ = 0.05, and its pair (kind) share is at least 0.15 above δ = 0.05's. *Falsifier:* either
   gap < 0.15.
3. **Constants coordinate better than bids at every N.** C+G ≥ C+B\* − 0.05 at N = 200 and 400 (paired), and C+G core ≥ 0.8 at
   N = 400. *Falsifier:* C+B\* exceeds C+G by more than 0.05 at either N (a reading premium), or C+G < 0.8 at N = 400.
4. **A flexible bid is a constant with a fallback.** C+F is within 0.15 of C+G at N = 100, 200 and 400 (reading plus
   feasibility adds and costs nothing in the easy case), and C+F − C+B\* ≥ 0.3 at N = 100. *Falsifier:* |C+F − C+G| > 0.15
   at any N (a reading premium or penalty), or C+F − C+B\* < 0.3 at N = 100 (equality was not the bind).
5. **Local supply is enough without migration at N = 400.** mN = 0, N = 400: core ≥ 0.5 in C+B\* and in C+G, and the
   null share ≤ 0.2 (queue 72 at N = 100: core 0.02, null 0.78–0.86). *Falsifier:* core < 0.5 in either.
6. **The RS's conjecture still fails at N = 400, on the core clause.** No arm reaches core ≥ 0.95 at mN = 1 (the best
   arm ≤ 0.9; dominated pairs and non-core bid splits remain). *Falsifier:* an arm with core ≥ 0.95 and the lower
   bootstrap bound ≥ 0.9.
7. **Entry is the bind, exit is neutral drift.** At N = 100 → 400, in C+B\* the core exit hazard per island-generation
   falls by at least 2× (neutral drift out ∝ 1/N), while the entry hazard rises with T. *Falsifier:* the exit hazard
   falls by < 2× or rises.

**Reviewer counter-predictions, recorded and scored.** gemini-4-argon: (i) at mN = 1 the lever is metapopulation supply
I·T, not T: C+B\* at N = 400, δ = 0.0125 reaches core ≥ 0.50 and exceeds C by > 0.15 (against RE 1; the mN = 0 cell at
the same dose separates the two: under argon, mN = 0 stays low while mN = 1 is high); (ii) C+F with matched marginals
has an efficient-dominated share > 0.15 (F stabilizes the 9 non-core splits), scored against C+F₄.

## Notes for the engineer

- Reuse `src/pair_worth*.py`; add arm F and the job stages without editing stored kernels or stored rows. The
  `pair_worth_run.py one` pilot applies. Kernel time grows like N^2.5–3: pilot N = 800 before launching D.
- Founders and tail are deterministic by (arm family, run index, seed law); V1 checks that the stored exploratory rows
  reproduce.
- Disclose any deviation in the report and the notes. Workers ≤ 3; BLAS threads 1; do not read or source `.env`; no
  `.npz` / `.pkl` / large `.npy` committed. Commit `predictions/` before any counted cell and the notes' design section
  before code.
