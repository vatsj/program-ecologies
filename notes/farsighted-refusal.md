# Farsighted refusal: can programs derive the guard that recovers the stable set? (notes, 2026-10-14)

Spec `specs/2026-10-14-farsighted-refusal.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict). Follow-up to RESULTS "Dominance contracts and refusal on
islands" and DEFERRED 15. §1 is written by hand before any code of this experiment and before any computation of a
fixed point; §1.9 (code validation and the static computations) is appended after the code exists and before any
counted cell; §2 (costs) after that.

## 1. Design

### 1.1 The object as it will be implemented

Everything of `src/dominance_contracts.py` is imported, nothing edited: `dollar3`, the 20 realizable outcomes R (in
sixths), the 27 pair contracts κ = (S, d_S) of which 18 are feasible, ε = 0, the length prior L, Moran with w = 0.3,
N = 100 per slot, I = 64, mN ∈ {0, 1}, the 0.95 modal-play classifier, menu F (κ uniform over the 27 at each contract
event), β = 1 (atomic installation), ν = 0.1 contract events per island per generation, proposal iff both members of
S are strictly better at x_κ than their slot-mean payoff ȳ_s, public consent (one individual drawn per S slot). L
founders paired with the stable-sets and dominance-contracts runs (`run_seed('L0' | 'L1', r)`).

A new kernel `fkern` (in `src/farsighted_refusal.py`, a copy of `dominance_contracts.dkern` restricted to menu F,
β = 1 and public consent) replaces the refusal bit r by a **guard index γ** in the genotype (program k, installed
override o, guard γ). Guards are heritable consent traits; they never change play, so fitness is the play class's
payoff as before, offspring copy γ, migrants carry it, installation keeps it.

**Consent at a contract event** (status quo y = the island's modal realized outcome, as in the dominance-contracts
run): draw one individual per S slot (by counts); the contract is installed iff both drawn individuals consent under
their own guards. **Random-number convention (fixed now):** the two draws are made iff some guard type present in
either S slot of the island would refuse κ at y; otherwise consent is certain and no number is drawn. Consequences,
checked as tests: universal g0 consumes exactly D1's random numbers (D1 had no consent step) and reproduces D1 draw
for draw; universal gV draws exactly when R2's guard fires and reproduces R2 draw for draw; universal gKR-read
reproduces universal gKR draw for draw (both refuse the same set at every event, §1.5).

### 1.2 The guards

- **g0:** consent to every proposed contract (= D1).
- **gV:** refuse iff y ∈ V\* and x_κ ∉ V\* (= R2's hand-written veto; R1-public's bit).
- **g1 (one-step exposure):** member i of S refuses iff after x some dominating contract excluding i would leave i
  below its status quo payoff: y_i > 0 and some feasible contract on the pair not containing i strictly improves both
  of its members at x. **g1-x:** the same with "below x_i" (refuse iff exposed at x, since x_i > 0 for every member).
- **gKR(δ):** member i of S consents iff W_i(x_κ) > W_i(y) (ties refuse), where W is the value of the contract
  process in which every consent decision is made by the same rule (§1.3–1.4). The program carries the **default**
  fixed point's member-level table a_i(y, κ) = [W_i(x_κ) > W_i(y)], evaluated for every (y, κ) and member i, not only
  for proposed ones (on polymorphic islands the slot means can propose κ that do not dominate the modal outcome).
- **gKR-read(δ) (a plug-in, lagged reader; amendment 3):** at a contract event a drawn gKR-read individual of slot i
  reads the guard composition of the island's slots, treats every gKR and gKR-read copy as playing the default gKR
  table, g0/gV/g1 copies as their own tables, sets each slot's consent probability per (y, κ) to the fraction of its
  individuals that consent, forms A(κ, y) = Π_{s∈S} p_s(y, κ), solves the 20-state linear system of §1.3 for W_i once
  per composition (cached by the composition vector), and consents iff W_i(x) > W_i(y). It is a best reply to the
  island's current consent process, **not a mutual fixed point** of a mixed composition (the regress is recorded for
  DEFERRED 15). Against a monomorphic gKR / gKR-read island its process is the default fixed point's, so its decision
  is gKR's by the fixed-point property.

All guards run host-side (in the numba kernel): an idealized oracle experiment. Realizability is measured separately
(§1.8).

### 1.3 The contract process and its Bellman equations (amendment 1)

Time is counted in **contract events** (one per ν-draw; the clock advances on every event, null draws, infeasible
draws and refusals included). At an event in state y the flow payoff is u(y) (the status quo's), a contract κ is drawn
uniformly from the 27, it is proposed iff x_κ strictly dominates y for both members of S (in sixths, at a homogeneous
island the slot means are u(y)), and it is installed with probability A(κ, y) (the joint consent of S, 0 or 1 under a
pure policy). Values, for each player i:

  W_i(y) = (1 − δ) u_i(y) + δ Σ_κ (1/27) [ A(κ, y) W_i(x_κ) + (1 − A(κ, y)) W_i(y) ],

with A(κ, y) = 0 for non-proposed κ. Refusal does not stop the clock. With δ = p/q and m(y) = Σ_κ A(κ, y) (the
number of installed moves out of y; every proposed κ leads to a distinct x, multiplicity 1), multiplying by 27q:

  [27(q − p) + p m(y)] W_i(y) − p Σ_κ A(κ, y) W_i(x_κ) = 27(q − p) u_i(y),

a strictly diagonally dominant M-matrix system with natural-number entries (in exact rational arithmetic for
certification; the same system is the executable benchmark, §1.8). A **KR equilibrium process** (pure, stationary,
Markov, stage-undominated, "vote as if pivotal") is a table A ∈ {0, 1}^P over the P = 90 proposed (y, κ) pairs with

  A(κ, y) = 1  iff  W_j(x_κ) > W_j(y) for both j ∈ S,   W = W(A).

(The proposal counts n(y) are 2 per fair pair, 3 per unequal pair, 4 per (3, 2)-type and 7 per (2, 2)-type wasteful
pair, 3 at (2, 2, 2) and 18 at (0, 0, 0): 6 + 18 + 24 + 21 + 3 + 18 = 90.) **Weak** fixed points (either action at an
exact tie) are reported separately; mixing is allowed only at exact indifference, so a mixed equilibrium can only
differ from a pure one on tie pairs, which the certification flags (generically there are none).

### 1.4 Certification and the frozen default-selection rule (amendment 2)

**Exhaustive search (certified).** Depth-first branch and bound over A ∈ {0, 1}^90. At a node some entries are
fixed; for each player i the minimum and maximum of W_i(y) over all completions are the values of two Markov decision
problems (the free entries are independent binary actions; the maximizer accepts a free κ at y iff W_i(x_κ) > W_i(y)),
solved by policy iteration with exact linear solves. These bounds are sharp per state. **Propagation:** a free (y, κ)
is forced to 1 if min W_j(x) > max W_j(y) for both members j, forced to 0 if max W_j(x) ≤ min W_j(y) for some member;
a node dies if a fixed 1 has some member with max W_j(x) ≤ min W_j(y), or a fixed 0 has every member with
min W_j(x) > max W_j(y). Pruning uses float bounds with a safety margin τ = 10⁻⁹ (a node dies or an entry is forced
only when the inequality holds by more than τ), so the search never prunes a fixed point. Branching order: recurrent
outcomes first (fair, then unequal, then (3, 2)-type wasteful), then the transient ones. Every leaf (all entries
fixed) is verified in exact rational arithmetic (Fractions, δ as a rational, exact Gaussian elimination): it is a
certified fixed point iff the strict rule holds exactly; leaves that fail only by exact ties are listed as weak fixed
points. The output is the complete list of pure fixed points per δ, grouped into orbits of the player-permutation
group S₃ (which acts on R, the contracts and the tables).

**Default-selection rule (frozen now, before any computation).** For each δ:
1. Simultaneous best-response iteration from the **myopic policy** (A ≡ 1 on every proposed contract: every
   dominating contract improves both members' flow, so a myopic member consents; this is g0): A_{t+1} = BR(W(A_t)),
   with ties → refuse. If it reaches a fixed point, that is the default.
2. If it cycles (A_t = A_s for some s < t without a fixed point) or runs 10⁴ iterations, restart from the myopic
   policy with asynchronous best responses: repeatedly flip the first (y, κ) in canonical order (y by its index in R,
   κ by its index in the 27) whose entry differs from its best response; if it reaches a fixed point, that is the
   default.
3. If that also cycles or runs 10⁴ flips, the default is the certified fixed point at minimum Hamming distance from
   the myopic policy, ties broken by the lexicographic order of A in the canonical order.

The endpoint of step 1 or 2 must appear in the certified list (a check). The spec's other initializations (all-refuse,
random) are run as a cross-check and reported. If the δ = 0.99 search does not terminate (or the default is not
reached), that is reported and δ = 0.95 replaces it in the cells (spec's scale guard).

**Per fixed point** (amendment 2): its absorbing set (the union of the recurrent classes of the event chain
Q_A(y, x) = Σ_κ A(κ, y)/27 [x_κ = x], null and refused draws on the diagonal) and each recurrent class; absorption
probabilities into each class from every outcome and from the **seeded outcome distribution** (the baseline L, mN = 0
islands' outcome distribution at closure, from the stored stable-sets runs: fair 0.281, unequal 0.417, wasteful 0.23,
disagreement 0.070); the stationary V\* mass (absorption-weighted stationary masses); hitting-time distributions (in
events, then generations at ν = 0.1) to the absorbing set and to V\* (mean, median, 90th percentile, by phase-type
matrix powers); the minimum consent margin min |W_j(x) − W_j(y)| over the proposed pairs and members (in sixths),
flagged when below 10⁻³ at δ = 0.99. Which fixed points correspond to the stable-sets run's farsighted sets (game
effectiveness: V\* and the held-player pairs {(4,2,0), (0,2,4)}, {(2,4,0), (2,0,4)}, {(4,0,2), (0,4,2)}) is read from
the absorbing sets.

### 1.5 Hand facts and hand predictions on the static objects

**The g1 freezing set (the RE's check, redone).** Exposure of member i at a pair outcome x: the pair not containing i
can dominate x iff the other member j can be raised (x_j ≤ 3, since the third player is at 0 and any feasible offer
improves it). So **every member of a fair or wasteful pair is exposed, and of an unequal pair only the 4-member is**
(its partner at 2 can be raised; the 2-member's partner at 4 cannot). The RE's "each pair member is exposed at every
pair outcome" is true of the 4-member and false of the 2-member, but every contract κ has a member who refuses under
g1 at every outcome where the refusing member has y_i > 0: a contract into a fair, wasteful or (2, 2) pair has two
exposed members; into an unequal pair, its 4-member is exposed and, from every outcome other than (0, 0, 0), has
y_i > 0 (the 4-member of x = (4, ·, ·) gets a positive payoff at every proposed-from outcome except disagreement, since
a contract is proposed only if it strictly improves both members, and from y = (0, 0, 0) both members have y_i = 0).
Hand result: **under g1 every outcome except (0, 0, 0) is frozen; at (0, 0, 0) all 18 proposals pass** (both members
have y_i = 0, so "below y_i" is false), and the first jump goes to a uniform feasible pair outcome (fair 3/18,
unequal 6/18, wasteful 9/18), after which the island is frozen. **Under g1-x every outcome, (0, 0, 0) included, is
frozen.** The two freezing sets differ (only at disagreement), so U-g1-x runs at mN = 0 (amendment 5; the RE's check
said they would not differ).

**gKR at δ → 1 (bias argument).** Under a candidate process with V\* absorbing, the excluded player of a fair pair
values the pair at 0 and consents to any exit; the buyer (the member offered 4) consents iff W_buyer(x) > 3. From the
exit outcome, e.g. (4, 0, 2) out of (3, 3, 0) via {1, 3}, every proposed contract is on {2, 3} and excludes the buyer
(to (0, 2, 3), (0, 3, 3), (0, 2, 4)); with these accepted, the buyer holds 4 for a geometric number of events (exit
rate 3/27) and is then excluded. Rough values with continuation values ≈ 0 / 1.75 / 1.75 for the buyer after the three
exits: W_buyer(4, 0, 2) ≈ 1.4 at δ = 0.99, 2.6 at 0.9, 3.1 at 0.8 (sixths). Every outsider has exactly one contract
into V\* and both its members prefer 3 forever to their value outside (≤ a mixture of absorbed values ≤ 3 and
current flows < 3, except the 4-member, who is not a member of that contract). So:

- **H1.** A fixed point with absorbing set exactly V\* exists at δ ∈ {0.9, 0.95, 0.99} and not at δ ∈ {0.5, 0.8}.
- **H2.** At δ = 0.5 the fixed point is unique and is the myopic policy (all proposed contracts accepted: the
  generator's walk, stationary V\* mass 1/3); at δ = 0.8 the myopic policy is a fixed point (possibly with others).
- **H3.** The default (myopic start) at δ ≤ 0.8 is the myopic policy; at δ = 0.9 it is uncertain (under the walk the
  buyer's comparison is within a few percent by my rough numbers, 2.52 vs 2.58); **at δ = 0.99 the default is the
  V\*-absorbing fixed point** (60%: under the walk at δ → 1 the bias of holding a fair pair for 13.5 events beats the
  4-then-exclusion path).
- **H4.** Multiplicity: more than one orbit of fixed points at δ ≥ 0.9; at least one absorbs on unequal pairs (a
  held-player configuration in which the 2-member refuses every exit because each exit soon excludes it) at δ = 0.99
  (50%).
- **H5.** Minimum consent margins at δ = 0.99 are small but not degenerate (≥ 10⁻⁴ sixths), and no exact ties occur.

### 1.6 Hand predictions on the cells (horizon 2,000; occupancy = islands classified ≥ 0.95 on a V\* member)

- **U-g1, mN = 0:** islands whose modal outcome is disagreement at an early contract event (most scramble islands at
  generation 0–30, where diverse demands rarely match) jump once to a uniform feasible pair outcome (fair 1/6) and
  freeze; islands that settle before their modal is ever disagreement keep the baseline's scramble outcome. **Hand:
  0.22 (0.15–0.29), below the baseline 0.281**; unequal ≈ 0.38, wasteful ≈ 0.4, disagreement ≈ 0. Support ⊆ V\* 0/40.
  **U-g1, mN = 1:** contracts act only on disagreement-modal islands; the baseline's drift-and-migration consensus is
  untouched: **0.65 (0.55–0.8)**, modal ≈ 0.8.
- **U-g1-x, mN = 0:** every proposal refused: the baseline in distribution (0.28 ± 0.03), not draw for draw (contract
  events consume random numbers).
- **U-gKR(0.99):** if the default absorbs exactly on V\* (H3), ≈ R2: **≥ 0.95 at mN = 0**; at mN = 1 modal ≥ 0.95 and
  the classifier ≈ 0.3 (R2's migration load). gKR differs from gV only off V\* (it may refuse some outsider moves), so
  hitting is slower than R2's 27 draws but the limit is the same.
- **U-gKR(0.9):** if the default is the myopic policy, = D1 in distribution (0.34 at mN = 0, 0.09 at mN = 1); if it is
  V\*-absorbing, ≈ R2.
- **U-gKR-read(0.99):** = U-gKR(0.99) draw for draw (a test, §1.1).
- **M-gKR (gKR(0.99) at ½ against g0):** as R1-public: neutral at mN = 0 (mean change within ±0.02), **rises in
  ≥ 0.8 of runs at mN = 1** by the immigrant-rescue channel, if the default is V\*-absorbing; occupancy ≈ R1-public's
  (0.85 / 0.26 at mN = 0 / 1).
- **M-g1 (g1 against g0 at ½, mN = 1):** g1 freezes islands wherever they are, member or not; it lowers churn but is
  not associated with member islands specifically, so its frequency moves less than gKR's: **rises in ≤ 0.6 of runs**
  (the generic-caution control should not spread like the V\* guard).
- **C3 (gV, gKR(0.99), g0 at ⅓; mN = 1):** both refusers rise against g0; gV and gKR are nearly identical on V\*, so
  neither displaces the other; g0 below ⅓ at 2,000 in ≥ 0.8 of runs.
- **C3-read (gKR-read, gKR, g0 at ⅓; mN = 1):** with g0 present a reader's plug-in process exits V\* more often, so
  the reader consents to more member exits than gKR and is less tied to locked islands: **the reader ends below gKR
  in more than half the runs** (uncertain, 55%).
- **M-read (gKR-read vs gKR at ½, mN = 1):** neutral by construction (Gemini's counter-prediction), mean change within
  run-level uncertainty of 0.
- **Rare invasion (gKR at 0.05 against g0, mN = 1):** rises in ≥ 0.7 of runs (the rescue channel does not need
  abundance), but slowly.
- **Forced starts, U-gKR(0.99), mN = 0:** persistence from every member 1.0; recovery from every outsider ≈ 1 by
  2,000 generations if the absorbing set is V\*.
- **N panel (U-gKR(0.99), N = 50, 200):** occupancy at mN = 0 N-free (≥ 0.95).

### 1.7 Statistics (fixed now)

As in the dominance-contracts run: occupancy (0.95 classifier) and modal-play occupancy, support ⊆ V\* (members and
member-mixed only), coverage, class distribution, consensus; contract events drawn / null / proposed / refused /
installed, and refusals by the guard of the refusing drawn individual(s); the contract-jump matrix and settled
transitions among classes; guard frequencies per slot every 10 generations (island and run means), the change by run
(rise / fall counts and the run-level 95% bootstrap interval of the mean change), the immigrant-rescue decomposition
(change of each island's guard frequency per 50-generation window by window type: refused offers, guarded offers that
went through, unguarded installations, none; member vs non-member islands); guard–outcome association at founding
(correlation across islands of the guard's island frequency at generation 0 with the island's member time-share over
generations 0–250 and 1,750–2,000) and its trajectory; placement of guards across slots at the horizon (frequency per
slot role: member slots vs the excluded slot of member islands). Efficiency reported, never a selector. Every
statement about U-gKR is about finite (N, I, horizon) islands at ε = 0.

### 1.8 Realizability benchmark (amendment 4)

The 20-state solve written in the realizable evaluator's surface syntax (`src/lt_code.py`: naturals with add, sub
(truncated), mul, div, mod, le, lt; pairs; recursion through library entries): fraction-free Gauss–Jordan (Bareiss)
elimination on the integer system of §1.3. The M-matrix sign pattern survives elimination (off-diagonals stay ≤ 0,
diagonals > 0, right-hand sides ≥ 0), so magnitudes are naturals throughout and the comparison W_i(x) > W_i(y) is a
comparison of two natural numerators over the common determinant: exact, no rounding. Measured: evaluator steps per
gKR-read decision (build the system from the composition, one solve for the reader's player, one comparison), steps
to derive the default table by best-response iteration (a gKR program that derives rather than carries its table),
the size of the integers (bits), and behaviour when fuel runs out (the call returns ⊥; a guard that fails consents or
refuses by a convention stated with the result). Prediction 8 is scored on this benchmark only. Hand: one solve ≈
10⁵ steps (≈ 20 × 20 × 21 entry updates at 10–20 steps each, plus list traversal), a reader decision 1–3·10⁵, the
derivation ≈ 10⁶–10⁷ (several best-response rounds × 3 players).

### 1.9 Code, validation and the static computations (appended after the code, before any counted cell)

Code: `src/farsighted_refusal.py` (process, exact solvers, certified search, guard tables, the kernel `fkern`),
`src/farsighted_refusal_run.py` (static driver, cells, analysis, forced starts, validation),
`src/farsighted_refusal_cost.py` (executable benchmark), `src/farsighted_refusal_report.py`,
`tests/test_farsighted_refusal.py`.

**Deviation in the certification method (disclosed before any cell).** The branch and bound of §1.4 as written
terminates at δ ≤ 0.9 (δ = 0.5: 1 node; 0.8: 15; 0.9: 1,801) but not at δ = 0.95 or 0.99 (more than 10⁶ nodes
without a leaf: at high patience the per-state value intervals over completions stay wide until most of the table is
fixed). Two changes, both preserving exactness:
1. **Decomposition.** No contract enters (0, 0, 0) or (2, 2, 2), and a (2, 2)-type pair is entered only from
   (0, 0, 0); so the values of the 15 *core* outcomes (fair, unequal and (3, 2)-type pairs; 48 proposed pairs) do not
   depend on the other 42 entries. The core is searched first; each core fixed point is then completed state by
   state (the (2, 2)-type pairs and (2, 2, 2) given the core, then (0, 0, 0) given all), by exhaustive enumeration of
   each state's decision subsets (2⁷, 2³, 2¹⁸) in exact arithmetic. Validated against the plain search at
   δ = 0.5, 0.8, 0.9 (identical strict and weak lists).
2. **Core search.** Failed-literal probing (a free entry whose 1- or 0-branch dies under propagation is forced to the
   other value) and fail-first branching, split at the root on the six member-exit bits by their 13 S₃
   representatives, with a node cap of 10⁵ per subtree. **A subtree that hits the cap is reported as not certified.**
   Alongside: exhaustive enumeration of every S₃-invariant (2⁸) and Z₃-invariant (2¹⁶) core table, and 1,500 random
   asynchronous best-response restarts per δ, every fixed point found verified exactly and merged into the list.
Also: on a polymorphic island the BLAS-threaded `numpy.linalg.solve` stalled under the sibling runs' load (200 ms
per 20 × 20 solve); every solve in this experiment uses a hand-written Gaussian elimination in numba instead.

**Static results** (`runs/farsighted-refusal-static.json`; 872 s on 3 workers).

| δ | certified complete | pure fixed points (S₃ orbits) | weak (exact ties) | default (frozen rule) | default's absorbing set | V\*-absorbing fixed point | unequal-absorbing |
|---|---|---|---|---|---|---|---|
| 0.5 | yes | 1 (1) | 0 | myopic, 0 iterations | 15 recurrent pair outcomes (V\* mass 1/3) | no | no |
| 0.8 | yes | 8 (4) | 0 | myopic, 0 iterations | the same walk (1/3) | **yes** (84 accepted) | no |
| 0.9 | yes | 5 (3) | 21 | simultaneous, 1 iteration | 9 outcomes: fair and unequal pairs (1/3) | yes (72 accepted; min margin 0, a tie on a refused pair) | no |
| 0.95 | **no** (2 of 13 subtrees capped) | ≥ 5 (≥ 2) | 0 found | asynchronous, 50 flips (simultaneous cycles) | **V\*** (56 accepted) | yes (default) | a rotating triad (P12:4\|2, P13:2\|4, P23:4\|2) |
| 0.99 | **no** (12 of 13 capped) | ≥ 4 (≥ 3) | 0 found | simultaneous, 3 iterations | **V\*** (36 accepted) | yes (default) | both rotating triads, or one |

- Every listed fixed point verified exactly on all 90 pairs; every default is in the list; the plain search and the
  decomposition agree at δ ≤ 0.9; the 1,500 restarts per δ found nothing outside the list at any δ (the one table at
  0.9 that the float screen reported and the list lacks is an exact-tie weak fixed point).
- **Hand predictions:** H1 failed in its second clause (a V\*-absorbing fixed point exists already at δ = 0.8: the
  buyer's value of the exit (4, 0, 2) is 2.94 < 3, my rough 3.1 overestimated the continuation); H2 held (unique and
  myopic at 0.5; myopic is a fixed point at 0.8); H3 held (default myopic at ≤ 0.8, the walk-like orbit at 0.9, V\* at
  0.99, and also at 0.95 through the asynchronous rule); H4 held in its first clause (3 orbits at 0.9, ≥ 2 at 0.95,
  ≥ 3 at 0.99) and **failed in kind** in its second: the unequal-absorbing fixed points are not held-player pairs but a
  *rotating triad* (4,2,0) → (0,4,2) → (2,0,4) → (4,2,0), a recurrent class of three unequal outcomes in which each
  player cycles through 4, 2, 0 (each member exit accepted, V\* transient); H5 held for the defaults (margins 0.076,
  0.0051, 0.051 at 0.9, 0.95, 0.99; no ties at the defaults) but a non-default orbit at 0.9 has a tie.
- **The farsighted sets of the stable-sets run** (V\* and the three held-player pairs) correspond to: V\* yes (an
  absorbing set of KR fixed points from δ = 0.8 up); the held-player pairs no (no listed fixed point absorbs on one);
  the rotating triads are a new object, outside the game-effectiveness farsighted sets.
- **Program choices (frozen by §1.4 and the static driver's rule):** gKR(0.99) = the V\*-absorbing default (refuses
  every member exit, accepts 36 of 90); gKR(0.9) = the walk-like default (accepts 84, every member exit accepted, the
  six (3, 2)-type → wasteful moves refused); gKRu (for M-gKR-unequal) = the δ = 0.99 orbit whose absorbing set is both
  rotating triads (78 accepted).
- **Forced starts** (U-gKR(0.99), mN = 0, 2,000 generations, 27 islands per pair outcome): every member island stays
  (persistence 1.000), every outsider island reaches V\* (recovery 1.000, median first entry 59–375 generations),
  matching the static chain (≥ 0.999). Recovery and persistence both hold on constant islands.

**Validation** (`runs/farsighted-refusal-validate.json`; 7 tests passing): universal g0 reproduces the stored D1 runs
and universal gV the stored R2 runs draw for draw (6 of 6 runs per cell at both mN: stop generation, migrant births,
contract counts, every horizon's labels); universal gKR-read reproduces universal gKR draw for draw (6 of 6 at both
mN) and its plug-in values equal the default fixed point's on any composition of gKR-like copies (1e-9).

## 2. Costs and the scale guard

- One run to 10,000 generations: 0.4 s at mN = 0, 16–26 s at mN = 1 (C3-read: 11,000 reader solves per run, 16 s).
  The design is ≈ 2.5 CPU-hours: nothing dropped. N panel at 2,000 generations as specified.
- **Executable benchmark** (`runs/farsighted-refusal-cost.json`): a gKR-read decision in the realizable evaluator
  (build the plug-in system from the composition, Bareiss solve, compare) costs **2.4–2.6·10⁵ steps** on every
  composition tried (10 compositions × 2 decisions; all agree with the host); deriving the default table as code costs
  6.7·10⁵ (δ = 0.9, 1 round), 1.3·10⁶ (0.99, 3 rounds) and 1.8·10⁷ steps (0.95, 50 asynchronous flips); the
  determinant has 386–438 bits at N = 100 (the evaluator charges one step per arithmetic operation whatever the size,
  an idealization); a reader capped below its need returns ⊥ (fail-closed by convention: refuse).
