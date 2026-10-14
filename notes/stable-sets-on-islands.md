# Stable sets on islands (notes, 2026-10-13)

Spec `specs/2026-10-13-stable-sets-on-islands.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the [after review] text
is the resolution). Follow-up to DEFERRED 15 (the RS's stable-set claim) and to RESULTS "Three-player majority
divide-the-dollar" and "Fixed-role chicken". §1 is written before any code of this experiment and before any counted
cell; §1.14 (code validation of §1's claims) is appended after the code exists and before any counted cell; §2
(costs, the scale guard) after that.

*Disclosure.* Before writing this section I ran one scratch query on the standing `src/dollar3.py` (no new code, no
dynamics): the n = 6 weak / modalPA catalogues have 1,305 canonical functions per slot (modal 2,601), the nine
constants carry 0.976 of the length prior (0.1084 each), and 6,400 iid draws per slot contain about 158 distinct
canonical functions (11.6 in 100). Everything else in §1 is derived by hand and is re-checked by code in §1.14.

## 1. Design

### 1.1 The game as it is implemented, and what that does to the spec's grid

`src/dollar3.py` is the game of RESULTS "Three-player majority divide-the-dollar": each slot submits (partner, demand)
with partner ∈ {the two others, ALL} and demand ∈ {1/3, 1/2, 2/3}, stored in sixths as {2, 3, 4}; a pair forms on
mutual naming with demands summing to at most 1 (the excluded slot gets 0); the grand coalition needs all three at ALL
with demands summing to at most 1, which on {2, 3, 4} sixths means (2, 2, 2) only; otherwise everyone gets 0.
"The 1/6 grid" of the spec is therefore the payoff unit, not the demand set: **demands 1/6 and 5/6 do not exist, and
the grand coalition cannot split unequally.** The realizable payoff vectors (in sixths) are

  **R** = {(0,0,0), (2,2,2)} ∪ {pair outcomes (a, b) to pair {i, j}, a, b ∈ {2, 3, 4}, a + b ≤ 6}, |R| = 2 + 3·6 = 20,

each pair outcome being one of: **fair** (3, 3), **unequal** (4, 2) / (2, 4), **wasteful** (2, 2), (2, 3), (3, 2).
Two consequences, fixed before any computation:

- **No element of R except (2, 2, 2) gives three positive payoffs.** A discriminatory element (the excluded player at
  c > 0, the other two splitting 1 − c) is not a feasible outcome of this game at any c except the degenerate
  c = 2/6 point (2, 2, 2). The asymmetric-prior cell therefore runs as the spec anticipates: a test of what the
  tilted seed does in the absence of a discriminatory set.
- Gemini's "(3/6, 2/6, 1/6)" and "c = 1/6" do not exist in this game. The spec's grid statements are about the
  classical game, which I compute alongside (§1.4) on the full grids **G6** and **G8** (all nonnegative integer
  vectors summing to at most 6, resp. 8, and the efficient subsets summing exactly to 6, 8), and in a cheap
  extension (§1.10) that makes the full grids realizable.

### 1.2 The relation M (strict majority dominance)

For outcome vectors x, y in a finite set X and a coalition S ⊆ {1, 2, 3}: **x ≻_S y** iff S is winning (|S| ≥ 2),
S is effective for x (Σ_{i∈S} x_i ≤ v(S) = 1, i.e. 6 or 8 units; automatic on every set used here), and
**x_i > y_i for every i ∈ S** (strict). x ≻ y iff x ≻_S y for some S. Under *weak* improvement the three fair pairs
are not internally stable ({1, 2} weakly improves from (3, 0, 3) to (3, 3, 0)), so weak dominance is not used.

Hand facts on R (each checked by code in §1.14):

- (M1) A pair outcome x of pair {i, j} dominates only via {i, j} (the third coordinate is 0, so no coalition
  containing the excluded player improves strictly). (2, 2, 2) dominates y iff two coordinates of y are below 2,
  i.e. only (0, 0, 0). (0, 0, 0) dominates nothing.
- (M2) **No element of R is undominated** (the core is empty): every pair outcome (a, b, 0) is dominated by an
  outcome of another pair offering the member with the lower demand more (e.g. (4, 2, 0) by (0, 3, 3) via {2, 3};
  (3, 3, 0) by (4, 0, 2) via {1, 3}); (2, 2, 2) by any fair pair.
- (M3) **The symmetric set V\* = {(3,3,0), (3,0,3), (0,3,3)} is stable on R.** Internal: two fair pairs share one
  member, who gets 3 in both, and the third coordinate of the dominator is 0 for the other. External: (2, 2, 2) and
  (0, 0, 0) are dominated by any member; a pair outcome (a, b, 0) of {1, 2} other than (3, 3) has a ≤ 2 or b ≤ 2
  (or both): if a ≤ 2 then (3, 0, 3) dominates via {1, 3}; if b ≤ 2 then (0, 3, 3) via {2, 3}; likewise for the
  other pairs.
- (M4) **Members are dominated by outsiders**: (4, 0, 2) ≻ (3, 3, 0) via {1, 3}. A stable set is not uninvadable;
  external stability says only that every outsider is dominated by some member. The chain's ratchet (an excluded
  slot buys a member with 2/3 at its own cost of 1/3) is exactly this arrow.
- (M5) **Unequal pairs: my hand bet is that they are in no stable set on R, and that V\* is the unique stable set on
  R.** Partial argument: if (4, 2, 0) ∈ V then (0, 3, 3), (0, 4, 2), (0, 3, 2) ∉ V (each dominates it via {2, 3});
  (0, 3, 3) must then be dominated by a member, i.e. (2, 4, 0) ∈ V (via {1, 2}) or (2, 0, 4) ∈ V (via {1, 3}); in the
  first case (4, 0, 2) dominates both (4, 2, 0) and (2, 4, 0) via {1, 3} and is dominated only by (0, 3, 3) (excluded)
  or (0, 2, 4), and so on through a case tree I did not close by hand. The enumeration (§1.5) decides it.

### 1.3 The relation C (commitment with credible response), on policy profiles

**Commitment set.** A coalition S (any size 1–3, singletons included) commits to a pure action profile a_S ∈ ∏_{i∈S} A_i
(A_i = the nine (partner, demand) actions; on the extended grids, 3(g − 1) actions). **Feasibility** is the game's
own rule (§1.1): the outcome of a full action profile is computed by `dollar3.outcome`. **Response.** The complement
T = {1,2,3} ∖ S responds by individual best reply: if |T| = 1, the set BR(a_S) of its best replies; if |T| = 2, the
set of pure Nash equilibria of the two-player game T plays given a_S; if T = ∅, nothing. **Ties are broken against
the committers by the "every best reply" clause:** x ≻^C_S y iff there is a_S such that x is the outcome of a_S and
some response in BR(a_S), and **every** response in BR(a_S) gives every member of S strictly more than y. (If |T| = 2
and the induced game has no pure equilibrium, a_S dominates nothing.)

**Policy profiles and invariance.** A status quo is a policy profile: on-path actions plus each program's off-path
responses (what it would do against other demands). **Lemma I (outcome-level invariance of C).** x ≻^C_S y depends
on the status quo y only through its payoff vector u(y). *Proof.* The committers' new actions a_S and the
complement's response are both recomputed (the response as a best reply to a_S, not read off the status quo's
programmed responses), so the status quo enters only through the comparison x_S > u_S(y). ∎ The invariance is a
consequence of credibility, and it fails for the relation that the ecology actually runs:

**Relation P (programmed response; the dynamic counterpart, reported, not used for stable sets).** S deviates and
the complement plays what its *resident programs* do against the deviation. P depends on off-path responses (two
statuses with the same realized division can differ: a fair pair beside an excluded constant vs. beside an excluded
conditional), and it allows singleton deviations to matter through programs (a reader that accepts an offer). The
ecology's moves are single-slot moves judged by immediate payoff against the resident programs, i.e. P with |S| = 1,
which neither M nor C contains.

Hand facts on R (checked in §1.14):

- (C1) **On R, C = M at the outcome level.** A pair S reaches every outcome of its own pair by naming each other
  (the third slot's actions are then irrelevant, every action is a best reply, and every one leaves the pair's
  outcome unchanged) and (2, 2, 2) by committing to (ALL, 1/3) twice (the third's unique best reply is (ALL, 1/3)).
  Any commitment in which the two committers do not name each other leaves the third a best reply that pairs with
  one of them and gives the other 0, so it dominates nothing. **Singletons dominate nothing**: for any a_i the
  complement's induced game has a pure equilibrium in which j and k pair with each other at (4, 2) or (2, 4) and i
  gets 0 (ties go against i by the "every" clause). The grand coalition adds nothing beyond pairs. Hence
  x ≻^C y ⟺ x ≻^M y on R, and every stable-set statement on R holds for both relations.
- (C2) Chicken (sanity case; payoffs (St/St, St/Sw, Sw/St, Sw/Sw) = (−10, 2, −1, 0)): {1} commits Straight, 2's unique
  best reply is Swerve, outcome R1 = (2, −1); R1 ≻^C_{1} every y with y_1 < 2 (crash, R2, mutual swerve); likewise
  R2 via {2}. R1 and R2 dominate each other. **The stable sets under C are exactly {R1} and {R2}** (each singleton is
  internally stable and dominates the other three outcomes; any set containing both is not internally stable, and a
  set containing neither must contain mutual swerve or crash, which do not dominate R1 or R2 strictly via {1,2}:
  (0, 0) vs (2, −1) fails for player 1). This is DEFERRED 15's reading and the fixed-role chicken result's two norms.

### 1.4 The classical grids

On G6, G8 (and their efficient subsets G6=, G8=) only M is computed with the classical effectiveness (§1.2); the
realizable extensions of §1.10 get both M and C (there C differs from M only through *inefficient* grand outcomes,
which a pair cannot reach because the third slot takes the remainder; hand claim, checked in code).

**Discriminatory sets, correctly defined.** D_k(c) = {x : x_k = c, x_i + x_j = g − c, x_i, x_j ≥ 0} (one player held
at c, the others dividing the rest in every way the grid allows: a line of three-positive allocations for c > 0).

**Lemma G (grid discreteness kills exact discriminatory lines).** On the grid of step 1/g, for every 0 ≤ c ≤ g − 1,
D_k(c) is not externally stable under M: the point y with y_k = c + 1 and y_i + y_j = g − c − 1 is dominated by no
element of D_k(c). *Proof.* Via {i, j} a dominator needs x_i ≥ y_i + 1 and x_j ≥ y_j + 1, so x_i + x_j ≥ g − c + 1;
via a coalition containing k it needs x_k = c > c + 1. ∎ In the continuum the dominator at x_i = y_i + ε/2 exists;
on a grid ε = 1 unit is too coarse. **Gemini's even-remainder fix does not rescue the exact line**: the obstruction
is the one-unit step, not the parity of 1 − c (on G8 with c = 2, y = (a, 5 − a, 3) is undominated by the line).
So "does a discriminatory stable set exist on this grid" is the question whether some stable set *contains a long
piece of* a line D_k(c), c > 0, plus whatever extra points repair external stability without breaking internal
stability. Definition used in the enumeration: a stable set V is **k-discriminatory at c** if V contains at least
three points of D_k(c) with all coordinates positive and every other point of V is outside D_k(c)'s pair-split
range; the count of such sets is reported per grid and (k, c). My hand bet: **none exists on G6** (the line has at
most 5 interior points for c = 1 and the repairing points dominate interior line points), and on G8 I have no bet.

**The symmetric set on the grids.** V\* is stable on G6= by the external-stability argument of (M3), extended: any
y ≠ member has some coordinate pair (i, j) with y_i < 3 and y_j < 3 except y ∈ V\* (if y_i ≥ 3 and y_j ≥ 3 then
y_i = y_j = 3 and y_k = 0). On G6 (sum ≤ 6) the same argument holds. On G8 the analogue {(4,4,0), …} is stable by the
same argument. Unequal pairs (x, g − x, 0) are classified as their own category (not discriminatory-line elements,
where the excluded player gets c > 0, and not V\*).

### 1.5 The enumeration (method)

A stable set is a **kernel** of the dominance digraph (x → y iff x ≻ y): an independent set (no arrow between two
members, in either direction) that absorbs every non-member (every y ∉ V has an arrow from V). All kernels are
enumerated by backtracking over the vertices with propagation (a member excludes its in- and out-neighbours; a
non-member whose undecided dominators are down to one forces it in; a non-member with no possible dominator prunes),
and each kernel found is re-verified by brute force (internal: no arrow within V; external: every y ∉ V dominated).
On R (20 vertices) the backtracking is checked against the exhaustive 2²⁰ scan. Every vertex is then classified by
membership in each stable set found (overlaps allowed), and separately by whether it is dominated at all (on R
everything is, M2): **"dominated" and "in no stable set" are kept apart.**

### 1.6 The farsighted contrast (Chwe 1994; Harsanyi 1974)

Effectiveness: S can move from any status y to any z ∈ X with Σ_{i∈S} z_i ≤ v(S) (v = 1 for |S| ≥ 2, 0 for
singletons, so a singleton can move only to vectors giving it 0: walking out). **Indirect dominance** x ≫ y: there is
a chain y = z_0, z_1, …, z_m = x (m ≥ 1) and coalitions S_1, …, S_m with S_t effective for z_{t−1} → z_t and
x_i > (z_{t−1})_i for every i ∈ S_t (each mover strictly prefers the *final* outcome to the one it leaves).
Computed by backward reachability for each x. The **farsighted stable sets** are the kernels of ≫ (vNM stability
w.r.t. ≫); Chwe's largest consistent set is computed too (iterative deletion: x survives if for every S and every z
that S can reach from x there is w in the current set with w = z or w ≫ z such that not every i ∈ S has w_i > x_i).
Hand expectation: ≫ is much denser than ≻, because a singleton walk-out (to any vector giving it 0) followed by a pair
move lets a coalition reach outcomes it cannot dominate directly. Example: (3, 3, 0) ≫ (0, 3, 3): player 1 (0 → 3 at
the end) walks out to (0, 2, 4), then {1, 2} move to (3, 3, 0) (player 2: 2 → 3). So a *single* fair pair may be a
farsighted stable set on its own, and the farsighted sets may be singletons where the myopic one is the triple; the
code decides, and prediction 6 is scored against whatever it finds.

### 1.7 The registered dynamic object

As `src/sog_lottery.py` (three slot populations per island), with the dollar3 game:

- **ε = 0, no mutation.** A program absent from a run can never appear in it; the object is absorption (and, with
  migration, metapopulation drift), not a stationary distribution.
- **Islands.** I = 64 islands, three slot populations of N = 100 per island (N panel: 50, 200).
- **Seeds.** Iid per slot from the slot's seed law (§1.8): every island-slot draws N canonical functions.
- **Moran per slot.** A birth event picks an (island, slot) unit uniformly; with probability m = mN/N the parent is
  drawn from a uniformly chosen *other* island's same slot (complete island graph, role-preserving, emigrants
  unweighted); the parent is drawn on its source island with weight count · exp(w · f), f = the expected payoff (in
  units of the dollar) of its class against the source island's other two slot populations (one uniformly drawn
  member of each); the victim is uniform in the recipient unit. **w = 0.3.** Exact event skipping (a birth in a
  monomorphic unit without a migrant changes nothing), as in `sog_lottery.kern`.
- **Generation** = 3·I·N births (N births per slot per island on average).
- **mN ∈ {0, 1}.**
- **Horizons.** Common observation horizons 500, 1,000, 2,000 generations for every run; runs not resolved at 2,000
  continue to 10,000 and are reported in a separate column. **Resolved** = closed: at mN = 0 every island locally
  closed (within each slot, all present classes give the same realized joint action against every combination of
  the other slots' present classes, so no birth can change any encounter); at mN > 0 the same test on the globally
  present classes (then nothing can change anywhere at ε = 0). Dwell times still running at the horizon are
  right-censored and reported as such.
- **Island classification by play** (every generation): the encounter distribution over payoff vectors (one uniform
  member per slot); the island's class is the payoff vector holding ≥ 0.95 of encounters (which pair at which split,
  grand, wasteful, disagreement), else **mixed**; mixed islands are further split into *member-mixed* (≥ 0.95 of
  encounters on V\* members) and *other-mixed*. Beside the class: the exact payoff support (vectors with mass
  ≥ 0.01), the time-window frequency of each class over the last 250 generations before each horizon, and efficiency
  (expected total payoff) reported separately.

### 1.8 Seed laws and cells

- **L (length prior)**: the standing prior μ over the 1,305 canonical functions (weak grammar n = 6), per slot.
  Constants 0.976 (0.1084 each, uniform over the nine (partner, demand) actions: the length prior is already uniform
  over demands among constants).
- **U (the spec's "uniform-over-demands" control, redefined here before any cell).** Because L is already uniform
  over demands, the literal control would duplicate L. The informative control that "changes demand marginals and
  prior masses" is the **uniform prior over programs**: each slot's seed is uniform over a run-specific catalogue of
  160 canonical functions drawn uniformly (without replacement) from the 1,305 (conditional-dominated: expected
  1.1 constants per catalogue); the per-run catalogue keeps the joint table at the size of an L run (§2).
- **M (matched modal)**: `modalPA`, the PA box on the same grammar, spellings and prior as the weak arm (identical
  canonical functions, so the seeds are **paired** draw for draw with the weak cells, and the dynamics seed too).
- **A (asymmetric prior)**: slot 3's seed tilts toward the smallest demand: every slot-3 canonical function whose
  table plays only demand-1/3 actions has its prior weight multiplied by 4 (for the constants: the three
  (·, 1/3) constants go from 1/3 to 2/3 of the constant mass); slots 1–2 as L.
- **K (constants only)**: the nine constants, uniform (= L restricted to constants).
- **F (forced seeds)** at targets T ∈ {fair pair P12:3|3 (a member), unequal pair P12:4|2 (slot 1 gets 4), wasteful
  pair P12:2|2, the grand coalition (2, 2, 2)} (other pairs by relabeling symmetry):
  - *F-entry* (mN = 0): every island seeded with a fraction β = 0.25 of each target slot set to the target constant
    (pair slots: the naming-each-other constants; grand: (ALL, 1/3) in all three slots), the excluded slot and the
    remainder iid from L; statistic: the fraction of islands ending at T, against the natural L rate of T (basin
    volume given founder availability).
  - *F-residence* (mN = 1): islands 0–31 start with the target's slots monomorphic on the target constants (the
    excluded slot iid from L), islands 32–63 iid from L; statistics: the time each target island first leaves T
    (exit; residence censored at 2,000), the time each L island first holds T (entry), and the class a target
    island goes to.
- **N panel**: L at N ∈ {50, 200}, mN ∈ {0, 1}, 20 runs.
- **Extended grids (§1.10)**: constants-only, uniform, on the full 1/6 and 1/8 grids, mN ∈ {0, 1}: reported as a
  different experiment.
- 40 runs per cell (F and the N panel 20); run-level uncertainty (bootstrap or t intervals over runs).

### 1.9 Statistics

Per run at each horizon: the island classes; **coverage** = every element of V\* held by some island; the fraction
of islands on each V\* element, on unequal pairs, on wasteful pairs, on (2, 2, 2) (which on R is the only
discriminatory-line point, c = 2/6), on (0, 0, 0), mixed; **selection** = the list of *all* stable sets (of the
enumeration on R) containing the run's island support (the set of non-mixed island classes; mixed islands reported
beside it); **the RS's claim** in its strong form (the run's island support lies inside some stable set) and weak form
(every element of the symmetric set appears on some island = coverage), scored per run; role symmetry across runs
(each pair's share of member islands, and of the modal member) reported separately from within-run selection;
transience (generations an island spends on non-members before first holding a member, censored); under migration,
every **flip** between held classes (a class held ≥ 25 consecutive generations), with its full intermediate sequence
of classes (mixed spells kept with their support), whether each step between consecutive non-mixed classes follows a
dominance arrow of M, and the **trigger** (§1.11); consensus (every island on one class) at each horizon and at
10,000; the myopic vs farsighted contrast; efficiency.

**Coverage baseline.** If islands independently hold a member with probability q, uniformly over the three members,
P(coverage) = 1 − 3(1 − q/3)^I + 3(1 − 2q/3)^I − (1 − q)^I (inclusion–exclusion over the missing members). At I = 64:
q = 0.1 → 0.70; q = 0.15 → 0.91; q = 0.2 → 0.97; q = 0.3 → 0.996; q = 0.6 → 1 − 1.6·10⁻⁶. **Coverage is a weak test
above q ≈ 0.15; member occupancy q is the informative number.**

### 1.10 The extended grids (cheap; a different experiment)

To give discriminatory elements a chance to be realized, a constants-only extension of the game: demands
d ∈ {1, …, g − 1} (units of 1/g), actions (partner, d), 3(g − 1) per slot; pairs as before (a + b ≤ g); the grand
coalition forms when all three name ALL with demands summing to at most g, and pays the demands (so (a, b, c) with
c > 0 and a + b = g − c is realizable: a discriminatory-line element). g = 6 (15 actions) and g = 8 (21 actions).
Seeds uniform over the constants; the same kernel. The realizable sets R6x (66 vectors) and R8x (141) get M and C
enumerations. Hand expectation: the grand coalition needs three-way coordination on ALL (seeded at 1/3 per slot) with
a compatible demand triple, so grand outcomes (discriminatory-line elements included) are rare (≤ 0.1 of islands)
and pairs dominate, as in the main game.

### 1.11 The flip-trigger taxonomy at mN = 1

For each flip on island i from held class A to held class B, let Δ be the set of slots whose dominant class
(the class with > 50% of the slot) differs between the end of A and the start of B, ordered by the generation each
new dominant class crossed 50%. For each changed slot record (from the kernel's dominance-change log): the class's
introduction (seeded, or the generation a migrant brought it into a slot where it was absent), and the class's
payoff advantage over the class it displaced at the crossing time (strict > 10⁻⁹, neutral, deleterious). Triggers:

- **conditional (single-slot)**: |Δ| = 1 and the realized play changed in a slot whose dominant class did not change
  (a conditional program already present responded to one changed slot);
- **drift-prepared**: |Δ| ≥ 2 and the first change is neutral (typically the excluded slot drifting to an offer) and
  completed before the next changed slot's new class was introduced or reached 10% (sequential);
- **two-slot coincidence**: |Δ| ≥ 2 and the new classes of two changed slots were both present at ≥ 10% at the same
  time before either crossed 50% (concurrent);
- **pure drift**: every crossing neutral (e.g. member → member: the excluded slot drifts to an offer of 3, then the
  pivot drifts across at a tie of 3 = 3);
- other / unresolved, reported.

**Hand prediction of the mechanism** (fixed now): a member-to-member flip needs two slots to change and both steps
are neutral (excluded slot 0 → 0; pivot 3 → 3), so it is *pure drift* and passes through *member-mixed* states only,
not through an outsider outcome. **Prediction 4's premise ("a flip passes through an outsider") is wrong for this
game**: internal stability forbids dominance arrows between members, not neutral drift between them. Flips into an
unequal pair from a member are drift-prepared strict moves (the chain's ratchet); flips from unequal to a member are
drift-prepared strict moves of the low-share member (2 → 3).

### 1.12 Anesi (2010), against Moran program evolution

Anesi, "Noncooperative foundations of stable sets in voting games", GEB 70 (2010) 488–493. Abstract (checked
online 2026-10-13): every stable set of the underlying simple game is the limit set of undominated pure-strategy
Markov perfect equilibria (and of strategically stable sets of undominated subgame-perfect equilibria) of a
legislative bargaining game **with farsighted voters**. Assumptions as I recall them from the bargaining literature
(not verified against the full text): a simple game over a finite set of alternatives; an endogenous status quo (the
last accepted alternative persists); a proposer recognized at random each period; a winning coalition accepts or
rejects with stage-undominated votes; voters discount with δ → 1 (farsighted); stationary Markov strategies; "limit
set" = the absorbing alternatives of the equilibrium process. Against our dynamics:

| Anesi | Moran program evolution here |
|---|---|
| voters are farsighted (δ → 1), equilibrium strategies | programs are selected by immediate payoff; no foresight, no equilibrium |
| a proposal is a whole alternative, voted on by a winning coalition at once | moves are single-slot births, one program at a time; a pair's move needs two sequential slot changes |
| status quo moves only by an accepted proposal (strict majority gain) | neutral moves (drift) change programs and can change outcomes (member → member) |
| finite alternatives, simple game | 20 realizable outcomes, but the state is a population of programs (policy profiles with off-path responses), not an outcome |
| deterministic equilibrium paths, absorbing set | stochastic, ε = 0: absorption by loss of variation, not by the absence of profitable proposals |

**The spec and DEFERRED 15 call Anesi's result "myopic"; it is farsighted.** The matching of our myopic dynamics to
the myopic stable set is therefore a hypothesis of ours, not Anesi's theorem; prediction 6 is scored as stated.

### 1.13 Hand predictions for the cells (before any code)

- mN = 0, L: islands absorb by loss of variation within ~100–300 generations; outcomes: fair pairs q ≈ 0.25–0.4 of
  islands, unequal pairs 0.3–0.5, wasteful ≤ 0.1, grand ≤ 0.05, mixed/disagreement ≤ 0.15 (the two-player fixed-role
  `dollar3` lottery at m = 0 gave 50–50 0.30 and 1/3–2/3 0.34). Coverage ≥ 0.95 of runs by the baseline. The strong
  form of the RS's claim fails in essentially every run (some unequal pair is held somewhere).
- mN = 1, L: continual flips; unequal pairs gain on fair pairs toward the chain's proportions (fair ≈ 0.35–0.4 of
  pair islands) by the ratchet, member ↔ member flips by pure drift, no consensus at 2,000; at 10,000 the global
  population (6,400 per slot) has lost much of its variation, so consensus becomes possible; I bet ≤ 0.3 of runs.
- K ≈ L (conditionals carry 2.4% of the prior); M = L to within noise (handshakes carry no mass); U differs
  (conditional-rich: more mixed and conditional-mediated outcomes); A: slot 3 at demand 1/3 is the *accommodating*
  partner, so pairs containing slot 3 shift toward the other member's 2/3 (unequal pairs with slot 3 at 2/6), not
  toward any discriminatory element.
