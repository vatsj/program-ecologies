# Pair-worth-a game on islands: engineer's notes (queue 72)

Spec: `specs/2026-11-01-pair-worth.md` (a7758a7). Reviews: `reviews/2026-11-01-pair-worth-gemini-4-argon.md`,
`reviews/2026-11-01-pair-worth-amended-gpt-6.1-sol.md`. Predictions: `predictions/2026-11-01-pair-worth.md`.
Code: `src/pair_worth.py` (games, programs, evaluator, catalogues), `src/pair_worth_kern.py` (kernel with the tail),
`src/pair_worth_static.py`, `src/pair_worth_validate.py`, `src/pair_worth_assay.py`, `src/pair_worth_run.py`,
`src/pair_worth_report.py`. Rows: `runs/pair_worth/`.

## 1. Design (written before code)

### 1.1 Games, actions, outcome rule

Grid `Gd` ticks (6 sixths; 12 twelfths; 24 twenty-fourths). Slot-local action `l = (Gd+1)*pi + d`, `pi` in {0, 1}
indexes the slot's two others in increasing order and `pi = 2` is ALL, `d` in 0..Gd; `3(Gd+1)` actions per slot
(21, 39, 75 as in the spec's table). This is `dollar3`'s encoding (`l = 3*pi + d`) with the demand axis widened and
demand 0 allowed (a zero-demand bidder is needed for the core points with a zero share). Pair worths: `v[i][j]`
ticks; pair-worth-a games `v = round(a*Gd)` for every pair; glove (slot 0 = R) `v(R, L) = Gd`, `v(L1, L2) = 0`.

Outcome of an action triple, as `dollar3.outcome`:

- all three name ALL: grand coalition if the demands sum to at most `Gd`, payoff = demands (waste lost), else null;
- otherwise, if two slots name each other (at most one mutual pair can exist) and their demands sum to at most
  `v[i][j]`: pair, payoff = demands, third slot 0; if the sum exceeds the worth: null;
- otherwise null.

An **outcome id** is the triple (kind, pair index, payoff vector) with all-zero vectors merged into one null id (a
pair at (0, 0) pays nothing and is a null as far as payoffs go; the glove's L1-L2 pair at (0, 0) is therefore a
null that excludes R). Payoffs in dollars are ticks/`Gd`. `OUT[a0, a1, a2]` is the outcome-id table over actions,
built once per game (75^3 = 4.2e5 entries at the largest). V1 checks it against `dollar3.outcome` at a = 1.

Classes (by payoff vector, game-level static numbers from `pair_worth_static.py`; strict coalitions-map dominance
as in `dominance_relations.py`: x dominates y if some coalition S with x(S) <= v(S) has x_i > y_i for all i in S):
null; core proper (efficient grand split with x(S) >= v(S) for every S); ring (strictly undominated efficient
vectors outside the core proper); other efficient (dominated); undominated wasteful; dominated wasteful. For G5/6
the dynamic classes are by kind (grand efficient / grand wasteful / pair / null) and the vector classes are kept in
the rows for the stable-set membership statistics. Pair and grand outcomes with the same vector (for example
(1,1,0) at a = 1/3) share a vector class; the kind is kept as a separate tag.

### 1.2 Programs: decision lists over box atoms

Every program in every arm is a **decision list**: ordered lines `(atoms, action)`, a line fires if all its atoms
(at most two, each a box atom, each optionally negated) hold; the first firing line decides; otherwise the default
action. A box atom is `BOX_L(THEM_j = a)`: slot j's action in this encounter is `a`, read at level `L`. A constant
is an empty list. The DSL of `dollar3` (`if(BOX(atom), x, y)`, and 2-atom tables) is a decision list, so the
evaluator is checked against `dollar3.eval_modal` directly on random DSL triples (V5).

**Modal semantics** (copied from `dollar3.eval_modal`, PA plus the Con(PA) level, linear GL Kripke chain): worlds
0, 1, 2, ...; the box at level L is true at world n iff the statement held at every world in [L, n) (vacuously at
the first world). Actions are computed world by world from the atoms' truth at that world; the encounter's play is
the stable action profile (`hist` unchanged from n >= 2 on). Level 1 is provability in PA + Con(PA), equivalently
PA-provability of the conditional `Con -> statement`.

### 1.3 A finding that changes the bid: the exclusion fallback does not work at level 0

Hand evaluation, confirmed by a prototype (scratchpad `proto.py`, now `pair_worth_validate.py` V4): the spec's
B(sigma; c) uses PA boxes (level 0) in all four atoms. A level-0 line-1 (`BOX(j = ALL, sigma_j) and BOX(k = ALL,
sigma_k)`) is **vacuously true at world 0**, so every bid plays its grand action at world 0 against anything. The
pair-handshake lines read `BOX(j = (i, pi_j))`, which at world n >= 1 requires j to have played (i, pi_j) at world 0
as well; j (also a bid) played the grand action at world 0, so the atom is false from world 1 on, forever (the
chain is "broken"). In GL terms: G_i <-> BOX G_j and BOX G_k, P_i <-> not G_i and BOX P_j; the chain value of
not G_i is true at every world >= 1 but is **not provable**, so no handshake closes. Result at level 0:
B, B, constant-non-grand plays (c_i, c_j, c_k): the two bidders do **not** pair; the "exclusion bid" is a bid whose
only effect is the three-way grand coordination. This falsifies the spec's design claim ("two bids facing a
non-bidder pair with each other"; "a bid in the excluded slot is then selected") **as written**.

**Repair R1 (the main arm; a deviation, disclosed in the report).** The two pair-handshake lines read their atoms
at level 1 (`BOX_1`: PA + Con(PA) provability, i.e. PA-provability of `Con -> (j = (i, pi_j))`), the grand line
stays at level 0. World 0 and world 1 are then vacuous for the pair lines, the grand line still fires at world 0,
and from world 2 on the atoms speak about j's behaviour from world 1 on, which is exactly what a handshake should
read. Hand check: B, B, c_k pairs the two bidders at the exclusion split; B^3 plays sigma; a constant matching the
bid's output is on-path identical. The same level shift is applied to the offer atoms of A (accept-pair) and to
the first-line pair atoms of K, for the same vacuity reason. This is the smallest change that makes the spec's
stated mechanism hold; it keeps "PA provability" in the sense above (no theory beyond PA is added: it is
provability of a Con-conditional in PA).

**Control B0 (as written, level 0 throughout)**, `CB0` arms (run where the budget allows): bids with no working
fallback; the grand coordination device only. It measures whether the fallback, not the grand line, is what makes
bids selected (spec RE 2, 7, 8 depend on the fallback).

### 1.4 The named families (action equations, slot i with others j < k in slot order)

Let `G_j = (ALL, sigma_j)` and `pi(sigma; i, j) = (pi_i, pi_j)` the exclusion split of pair {i, j}: pair-worth games
split v(i,j) as equally as the grid allows with the odd tick to the larger sigma share (v is even on all grids
used, so no tick is odd); glove: R-L pair split in proportion to the two sigma shares rounded down, remainder to
the larger share, L1-L2 pair at (0, 0).

- **B(sigma; c)**: `if BOX0(j = G_j) and BOX0(k = G_k): G_i;  elif BOX1(j = (i, pi_j)): (j, pi_i);  elif BOX1(k =
  (i, pi_k)): (k, pi_i);  else c`.
- **A(sigma; c)**: first line of B; then for partner p in (j, k) and every demand d of p in 0..v(i,p) ascending:
  `elif BOX1(p = (i, d)): (p, v(i,p) - d)`; else c.
- **K(sigma; c)**: `if BOX1(j = (i, pi_j)): (j, pi_i); elif BOX1(k = (i, pi_k)): (k, pi_i); else B(sigma; c)`.
- **G(sigma)**: the constant `G_i`.

The `B0`/`A0`/`K0` variants are the same lists with every atom at level 0.

### 1.5 Evaluation and catalogue: no closed-form rule is needed

Full joint tables over the catalogue are too large (609^3 = 2.3e8 for G1/3 C+B*), but a run touches few programs:
**the universe of a run is the founders plus every program in the arrival schedule**, drawn before the run (the
founder draws and the tail schedule are exogenous to the dynamics: arrivals pick the program from the slot's seed law
and the victim by a pre-drawn uniform). The universe is a few hundred programs per slot, so the joint table over
the **universe** is 10^6-10^8 triples and is built by **direct chain evaluation** of the decision lists in numba
(this is also the validated evaluator: V5 compares it with an independent pure-Python chain evaluation and with
`dollar3.eval_modal` on the DSL). No closed-form rule or behaviour-class table is introduced; V4 states the play the
equations imply (derived by hand in `pair_worth_validate.py`'s comments) before evaluating. The table stores outcome
ids (int16); `PAY[outcome, slot]` in dollars.

### 1.6 Founders, tail, pairing

Founder draws are per individual with common random numbers: for individual n of slot s on island i, `u1` picks
the constant (uniform over the slot's actions), `u2` the family (bids in `[0, delta)`, blockers in the next interval
of length delta where present, and so on), `u3` the member of the family. An arm replaces the constant by a family
member exactly when `u2` falls in its family interval, so arms that share the base law share every un-replaced
founder, and C+B, C+B+K, C+B2 nest. The kernel seed and the tail schedule are shared across mN and across arms.

**Tail.** Arrivals per island per generation `g >= g0` (g0 = 200 at N = 100, 2N when N scales): Poisson with mean
`Lambda * (1/(1 + (g - g0)/t0) - 1/(1 + (g + 1 - g0)/t0))`, the exact integral of `eps(t) = (Lambda/t0)(1 + (t -
g0)/t0)^-2`, t0 = N/2, for g < 10,000 (100N); each arrival: uniformly random slot, uniformly random individual
(victim by a pre-drawn uniform), program from the slot's seed law (same `u1, u2, u3` scheme). The schedule for
Lambda = 100 is generated first and thinned for Lambda = 10 and 1 (each arrival kept with probability Lambda/100),
so tails are nested. Arrivals are applied at the generation boundary, before that generation's births. They consume
nothing of the kernel's random stream, so Lambda = 0 is draw-for-draw the stored kernel (V2).

### 1.7 The annealed tail as a new kernel variant

`pair_worth_kern.kern_pw` is a copy of `migration_window_kernels.kern_mw` (the stored kernels are untouched) with
(a) the arrival schedule `(arr_g, arr_i, arr_s, arr_u, arr_k)` applied at generation boundaries, with the same
incremental updates as a birth (count, presence list, fitness vectors of the other slots, active set); (b) no early
stop while arrivals are pending (the closure test applies from the generation after the last arrival); (c) per
generation per island records: the modal outcome id (encounter-weighted argmax, `kern_mw`'s), the **majority-triple**
outcome, the top-outcome probability, the exact encounter-weighted class distribution, mean payoff per slot, a
bitmask of which named families are present (>= 1 individual and >= 10%) in each slot, and the crossing log
(first generation a program reaches 10% of a slot, flagged if its presence began with an arrival). With
no arrivals and the stored class tables it reproduces `kern_mw`'s `cls`, `counts`, `modal` arrays exactly (V2).

### 1.8 Statistics (as spec design 5)

Per island and generation: modal class, encounter-weighted class distribution, majority share per slot; per run
and cell: end class shares and last-2,000 occupancy (modal and encounter-weighted); core coverage per core point,
pooled over runs, reported separately for mN = 0 and 1, stratified by minimum share, with run-clustered
simultaneous 95% intervals (bootstrap over runs, Bonferroni over points); G5/6 switches per island per 10^4
generations (modal kind, debounced 25) separately in the tail (200-10,000) and the chase; the share of islands that
ever hold a named family in all three slots; transition structure (families present at >= 1 individual in two
slots before the switch); arrivals that fixed by family, and arrivals followed by a class change within 100
generations. Intervals over runs are percentile bootstrap (2,000 resamples) of the run-level mean.

### 1.9 Plan and expected cost

Static numbers and predictions file (committed before any counted cell); then code, V1-V6; invasion assays (single
islands, 2,000 replicates; the assays reuse the kernel with N = 100, I = 1, m = 0); pilot of G5/6 C and C+B for
per-run wall time; main cells; secondaries in reverse cut order. 3 workers, `OPENBLAS/OMP/MKL/VECLIB/NUMBA_NUM_THREADS = 1`.

## 2. Validation (all before any counted cell; `src/pair_worth_validate.py`, `runs/pair_worth/validation.json`)

- **V1** the generalised game at a = 1 on sixths restricted to `dollar3`'s 9 actions: 729/729 triples identical (payoff vector and kind).
- **V2** `kern_pw` with no arrivals is draw-for-draw `kern_mw` (status, stop generation, final counts, per-generation `cls`, `modal`, migrant births identical) on the stored `churn_primary` B6w founders, runs 0-5 at mN = 0 and 1 (12 of 12), and agrees with the stored rows (stop, status, nm, F) in 12 of 12.
- **V3** tail: 40 runs x 64 islands, Lambda = 10: 9.9145 arrivals per island against 9.9492 expected (the exact integral over 200..10,000), z = -0.56; arrival law against the seed law chi-square 19.6 / 17.7 / 20.9 on 21 df (p 0.55 / 0.67 / 0.46), slot choice uniform (p = 0.39); Lambda = 1, 10, 100 schedules nested; the kernel logged 619 of 619 scheduled arrivals on a test run and kept every slot population at N.
- **V4** 23 hand-built triples (G1/3, G5/6, glove), expectations written before the first evaluation: 22 of 23 matched on the first evaluation. The one mismatch (`A,A,const(0,0)`) was a mistake in the hand expectation (the constant (0,0) is a pair offer to slot 0, which A_0 accepts); the case was split into the corrected expectation and a non-offering constant, both match. Cases include B^3, B,B,const (bidders pair at (1,1); (5,5) at G5/6; (5,1) in the glove), matching and non-matching grand constants, K,K,B, K in slots 0 / 1 / 2 on a bid island, K^3, a mixed-sigma triple (collapses to the three fallbacks), A against constants and A,A, and the level-0 B0 (no handshake).
- **V5** the numba chain evaluator against an independent pure-Python chain evaluator on 8,000 random triples of named programs (including mixed sigma, level-0 variants, matching constants) over G1/3, G2/3, G5/6, glove, and against `dollar3.eval_modal` on 3,000 random triples of the DSL (levels 0 and 1): 0 mismatches.
- **V6** slot-permutation invariance. **As the spec states it, V6 fails**: with the spec's partner order (j < k in slot index) the image of a triple under a slot relabelling differs from the permuted outcome in 17% of random triples (1,656, 1,687, 1,697 of 10^4 at G1/3, G2/3, G5/6, 746 of 10^4 in the glove under permutations fixing R), all of them triples containing a handshake family (B, K, A): the first-listed handshake is index-ordered, so when two handshakes are available the relabelled program tries the other one first. With the partner priorities carried along by the relabelling (V6a) there are 0 mismatches on 10^4 triples per game, and triples without handshake families have 0 mismatches under both. So the machinery is slot-symmetric except for the spec's index-ordered tie-break; this is a design feature (it makes K slot-asymmetric, prediction E1), not an implementation fault, and it is disclosed as a deviation from "0 mismatches".
- The repair R1 (notes 1.3) is a deviation from the spec's bid; the as-written level-0 variants are run as controls `CB0` / `CBs0` / `CBK0`.

## 3. Pilot, cost and what was run

- Pilot (before the counted cells; `pair_worth_run.py one`): G5/6 C, one run, Lambda 0 and 10 at mN 1: preparation 0.4 s, kernel 4.6 s and 8.2 s; C+B 5.0 s and 13.3 s; C+B+K 4.8 s and 17.0 s. G1/3 C+B* about the same. The spec's budget worry (a 2·10^8-triple table) does not arise: the per-run universe is a few hundred programs per slot and the table is built by direct evaluation.
- Mean kernel time per (Lambda, mN) record: G5/6 C 4.5 s, C+B 5.6 s, C+B+K 7.5 s, G1/3 C+B* 6.5 s at N = 100; N = 200 18-29 s; N = 400 190-280 s. Total kernel wall time over all 7,240 records: 17.6 core-hours, about 6 hours at 3 workers, far below the 24 hours. Nothing in the spec's cut order was cut.
- Run: every job is one (game, arm, run) with Lambda in {0, 10} and mN in {1, 0, 0.1} (main), so every main cell has all three mN. Jobs: main 380 (20 runs; G1/3 C, C+B*, C+B, C+G, C+A, B0, B*0; G2/3 C, C+B; glove C, C+B; G5/6 C, C+B, C+B+K, C+B2, C+G, C+A, B0, BK0), sec1 400 (Lambda 1 and 100; doses 0.01 and 0.15; C+B= at mN 1 and 0; R and R+B; transfer cells), sec2 120 (N = 200 of G5/6 C+B and C+B+K; N = 200 and 400 of G1/3 C and C+B*), sec3 380 (engineer's additions: doses 0.3 and 0.5 on G1/3 C+B*, C+B and G5/6 C+B, dose 0.3 on G5/6 C+B+K; runs 20-59 of G1/3 C, C+B*, C+B and G5/6 C, C+B, C+B+K).
- Rows: all 7,240 records (trajectories dropped) in `runs/pair_worth/rows.jsonl.gz`; aggregation in `runs/pair-worth.{md,json}`.

## 4. Deviations from the spec (all also in the report)

1. **The bid's handshake lines read at level 1** (notes 1.3): at level 0 the exclusion fallback never fires, so the spec's mechanism cannot work as written; the as-written variants are run as controls (B0, B*0, BK0). This is a design finding, not an implementation choice.
2. **V6 as stated fails** (index-ordered partner priority, 17% of random triples); V6a with priorities carried passes with 0 mismatches. K is therefore slot-asymmetric by construction.
3. One V4 hand expectation was wrong (the constant (0,0) is a pair offer); corrected and disclosed.
4. **Extra cells** beyond the spec: B0/B*0/BK0 controls, doses 0.3 and 0.5, 60-run supplement of the key cells, a mechanism diagnostic (`pair_worth_diag.py`, majority programs of the consensus state), V7 (arrival bookkeeping).
5. Tail start and horizon scale with N as 2N and 100N + 20N (spec: t0 = N/2, horizon 100N plus chase 20N; the start 2N is my reading of "from generation 200").
6. Every main cell is run at mN in {1, 0, 0.1} (the spec has mN = 0 and 0.1 as secondaries for C and C+B only); C+B* at mN = 0 is main because the conjecture's coverage clause needs it.
7. R is the n <= 6 one-atom conditional grammar with the length prior merged to canonical functions (conditionals 2.6% of the seed law); R+B adds the bid family at 0.05. Level-0 atoms only.
8. The invasion assays use the exact two-type Moran formula alongside 2,000 Monte-Carlo replicates (every invasion is of one individual into a slot whose two neighbours are monomorphic, so the invader's fitness is frequency independent); the escape hazard is measured with the full kernel from 200 pure-B^3 islands.
9. Process: a fourth process (the diagnostic) ran alongside three workers for about ten minutes before I noticed and killed it; one worker was killed and restarted twice to reorder the queue (N = 400 jobs deferred behind sec3). The coordinator's resume message said sec3 had not launched; on disk it had run to completion (1,279 of 1,280 jobs; the last N = 400 job had a stale lock from a killed worker and was rerun).
