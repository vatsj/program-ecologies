# Pair-worth easy case along N: engineer's notes (queue 73)

Spec: `specs/2026-11-03-pair-worth-n.md` (48faf74). Reviews: `reviews/2026-11-03-pair-worth-n-gemini-4-argon.md`,
`reviews/2026-11-03-pair-worth-n-amended-gpt-6.1-sol.md`. Builds on queue 72 (`notes/pair-worth.md`, `runs/pair-worth.md`).
Code reused unedited: `src/pair_worth.py` (games, programs, Menu, evaluator, founders, tail), `src/pair_worth_kern.py`,
`src/pair_worth_run.py` (prepare, run_kernel, summarize), `src/pair_worth_assay.py` (fix_mc, fix_exact), report helpers.
New code: `src/pair_worth_n.py` (arms), `src/pair_worth_n_static.py`, `src/pair_worth_n_validate.py`,
`src/pair_worth_n_run.py` (jobs, extra statistics), `src/pair_worth_n_assay.py`, `src/pair_worth_n_report.py`. Rows:
`runs/pair_worth_n/`.

## 1. Design (written before code)

### 1.1 The flexible bid F, and F4, F-minus

All programs are queue-72 decision lists (ordered lines of at most two box atoms, first firing line decides). A disjunction
is several lines with the same action, so **F needs no evaluator change**.

- `F(sigma_i; c)` in slot i (others j < k in slot order), G1/3, sixths, share `sigma_i` in 0..6:
  one line per pair (a, b), a, b in 0..6 with a + b <= 6 - sigma_i (at most 28 lines, for sigma_i = 0):
  `[BOX_0(j = (ALL, a)), BOX_0(k = (ALL, b))] -> (ALL, sigma_i)`; then the two level-1 handshake lines of queue-72 repair R1
  (`BOX_1(j = (i, pi_j)) -> (j, pi_i)`, same for k) with `pi` the exclusion split, `(1, 1)` ticks for every pair at G1/3; then
  the default `c`. At most 30 lines (MAXL 64). The grand line stays at level 0, as in B.
- `F4`: F with sigma_i <= 4 only. `F-` (family code `FM`): the grand lines, then `else c` (no handshakes).
- **Seed law (matched marginals, argon).** F's share is drawn from the marginal of the 28 splits, weight (7 - s)/28, and c
  uniform. Implemented through the same uniform `u3` that picks the B* member: `m = floor(28 u3)` is the split index,
  `c = floor(588 u3) - 21 m` the constant (identical to B*'s decomposition `member = 21 m + c`), the share is the first
  coordinate of split `m` (slot-independent: each coordinate has the same marginal). So F and B* replace the same founder
  positions (same `u2 < delta`), carry the same constant c and a share with the same marginal. Members are unique (share, c)
  pairs, 7 x 21 = 147 (F4: 5 x 21; weights (7 - s)/25 through `m = floor(25 u3)`, `c = floor(525 u3) - 21 m`, using the first
  25 splits, those with first coordinate <= 4).
- Family codes (the kernel's `famc` has 5 slots, 0..4): F, F4, F- use code 3 (the accept-pair code, unused in these arms);
  B 1, G 4. No kernel edit.

### 1.2 Fixed-count inoculation B*_k (sol)

Founders of the C arm (a Menu with the B* family at dose 0, so the C founders are reproduced exactly); then on each island
one split sigma is drawn uniformly from the 28 and exactly k individuals per slot (positions uniform without replacement) are
replaced by `B*(sigma; c)` with c the replaced founder's own constant (a draw from C's law). Stream keyed
`('Bk', k, N, run)`, separate from the base stream. The tail is C's (constants only). k in {1, 4}.

### 1.3 Common random numbers (V7)

`PW.draw_founders(menu, base, r, I, N)` is keyed by `base = 'pw13|N<N>|I64'` and run index only, and draws four uniform
arrays of fixed shape; an arm only changes which positions (`u2 < delta`) hold which named member. So arms share every
unreplaced base founder exactly, F / B* / G share their replaced positions (nested across doses), and the tail schedule
(`PW.tail_schedule`, keyed by `base, r`) is arm-independent. This is the stored scheme (it reproduces the stored rows, V1);
the spec's "separate stream keyed by (arm, run)" for named programs is realized by the `u3` member choice being a function of
the arm's family list only. V7 diffs founder arrays of two arms on one run and the tail schedules. For B*_k the base is
C's and the replacement stream is separate, as the spec says.

### 1.4 Statistics added on top of `PR.summarize`

All from the kernel's stored outputs (no kernel edit):
- **Supply at founding**, per island, from `loc` (founder counts) and the joint table `J`: any compatible grand support
  (present triple playing a grand coalition: kind grand, any sum; and the efficient version), number of occupied named
  split types per slot, the minimum slot abundance of the best (max-min) compatible support, the individual-level triple count
  `sum counts_a counts_b counts_c` over grand-efficient triples and over all-named such triples (the realized T), and the
  founding encounter probability of grand play (`cd[0]`).
- **Establishment**: first generation at which the island's modal outcome is a grand kind (efficient or wasteful) held for 25
  generations, and the same for core proper; per island arrays (-1 if never), conditional tables built in the report.
- **Transitions**: debounced (25) core entries and exits, by phase (before the tail, tail, chase), with at-risk exposure
  (island-generations not in / in the core), ancestry from the kernel's crossing log (`xlog`: a program reaching 10% of a slot
  on that island in the preceding 200 generations, flagged arrival (`arrf = 1`), migrant (born new to the island without an
  arrival, `intro >= 0`, a type new to an island can only come by migration) or none = resident), and the named families
  present (bitmask just before). These are finite-schedule rates, not epsilon-free.
- **Who holds the core**: on core islands at the end, the majority program of each slot classified bid / F / grand constant
  (constant playing ALL) / other constant, and the share of individuals by class.
- Existing outputs reused: end class shares (A, B), occupancy, `end_ids` for coverage, consensus, efficiency.
- Run-level paired differences with percentile bootstrap over runs (2,000), share of runs with >= 0.9 of islands in the core,
  consensus.

### 1.5 Assays (cell F, ε-free)

Single island (I = 1), no migration, no tail, N in {100, 200, 400}, 2,000 Monte-Carlo replicates plus the exact two-type Moran
value, as `pair_worth_assay.assay` but with N a parameter (the stored assay hard-codes N = 100). Residents: `B*(2,2,2; c = own
grand action)^3` and `G^3 = (ALL, 2)^3`. Invaders, in each slot s in {0, 1, 2}: a matching grand constant `(ALL, 2)` (on
B*^3; on G^3 the identical program, a trivial identity check, so a reading invader B*(2,2,2; c = grand) is added as the
informative on-path-identical entry), a pair offer (constant naming each of the two other slots in turn at the exclusion split
(1, 1)), and `B*(sigma'; c = own grand action)` with sigma' = (3,2,1) rotated so that slot s has share 3. Payoffs from direct
evaluation (`table_from_programs`).

### 1.6 Job manifest and costs

A job line is `arm|N|run|delta|lams|mNs|chase`. One job = one (arm, N, run) with all listed (Lambda, mN) records. Arms: C,
CBs, CB, CG (stored definitions), CF, CF4, CFm, CBk1, CBk4. Run indices: **N = 100 as the spec (CF 0-59, CG extended to 20-59,
other new cells 0-19); N >= 200: the confirmatory cells C, CBs, CG at delta = 0.05 use runs 20-59 (N = 200 extra replication
= 40-59), every new 20-run cell uses runs 20-39 so that every scored contrast is paired with the confirmatory rows** (the spec's
manifest says "0-19" for the new cells; with 0-19 the C+F vs C+G contrast at N = 200 and 400 would have no common run, see
Deviations). N = 800: runs 20-29. Lambda in {0, 10} at N = 100 and 200; **Lambda = 10 only at N >= 400** (the predictions score
Lambda = 10; the spec's own cost table assumes one record per job at N = 400). Priority order (last cut first): cheap N = 100 and
N = 200 cells; N = 400 C, CBs, CG (40 runs, never cut); N = 400 CB, CF; dose cells; mN = 0 at N = 400; E at N = 400; G (5
runs, chase 60N); D (N = 800).

Three workers, `OPENBLAS/OMP/MKL/VECLIB/NUMBA_NUM_THREADS = 1`; one lock file per job.

## 2. Static numbers, validation, predictions, pilot

- **Static** (`runs/pair_worth_n/static.json`, exact evaluation of every catalogue triple, 21 s for the 609-program C+B* catalogue): the grand coalition is
  never scarce (constants alone: 2,600 efficient grand triples per island at N = 100); the named supply is 0.16 same-split B* triples at N = 100 against 73 feasible F
  or G triples (F and G have identical feasibility counts, 73.18); the probability of a named-only efficient support at founding in C+B* is 0.116 / 0.537 / 0.982 / 1.000
  at N = 100 / 200 / 400 / 800 (Poisson, E1).
- **Validation:** V6 (launch gate) 0 mismatches: R1-R5 stated play (hand-derived, written in the code before the first evaluation) against the numba evaluator on all
  4,741,632 triples of the F+constants catalogue and the F- catalogue; an independent explicit-equation chain (written from the action equations, not decision lists)
  on 9,811 triples incl. 1,000 random triples with mixed shares, infeasible sums, B next to F and constants mimicking F's outputs; a mutated F (grand line off by
  one on share 3) is caught (R3 84,865, R4 300, R5 45 mismatches), so the test has power. One hand rule was wrong at first: R2 said "no grand outcome when the world-0
  triple is infeasible", but a left F's fallback c (or a constant) can itself be a feasible grand triple; the rule was restated as "a grand outcome then equals the
  outcome of the fallback actions" before the first run that was kept (V6 had not yet been evaluated against the final rule; the first evaluation passed).
  V1 (N = 200, C and C+B*, runs 0-2, both Lambda, mN = 1) and V2 (N = 400, C+B*, runs 0-1) reproduce the stored rows exactly in every field except `structure`
  (the stored list was an earlier version capped at 60 entries; the stored list is a prefix of the new one, switch counts equal) and the new statistics. V7 passes
  (arms share every unreplaced founder; tails identical; F and B* replace the same positions with the same c); V8 passes.
- **Pilot** (not counted; run indices 20, written outside the rows directory): N = 400, C+B*, run 20, Lambda = 10: kernel 102 s at mN = 1 (the run closed at
  generation 37,560 of 48,000), 12.8 s at mN = 0, preparation 12.4 s; N = 800, mN = 1: kernel 967 s (96,000 generations, no early stop), preparation 17.6 s,
  1.4 GB. The spec's extrapolation was 190-280 s at N = 400 and 40-60 min at N = 800: no overrun, nothing cut on the pilot's account.
