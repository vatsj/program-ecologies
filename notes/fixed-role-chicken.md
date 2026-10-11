# Fixed-role chicken and hawk–dove without `ROLE` (notes, 2026-10-11)

Spec `specs/2026-10-11-fixed-role-chicken.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-11-fixed-role-chicken-gpt-6.1-sol.md`;
the [after review] text is the resolution). §1 is written before any project code of this experiment and before any
counted cell. §1.10 (code validation of the hand claims) is appended after the code exists and before any counted
cell; §2 (costs) after that.

*Disclosure.* Before writing this section I ran a scratch enumeration (the standing `src/dsl.py`, `src/evaluate.py`
and `src/modal.py`, nothing new, no dynamics) to learn the class counts and prior masses of the four n = 6 catalogues
and their plays against the two constants. Those numbers are quoted below as "enumerated"; everything else in §1 is
derived by hand from them and is re-checked by code in §1.10.

## 1. Design

### 1.1 Games, actions, fitness map

Actions in level order A_0 < A_1: **Straight** (hawk) = A_0, **Swerve** (dove) = A_1. In the DSL the weak arm names
them `Straight`/`Swerve`; the modal arm keeps its built-in names `D` (= Straight) and `C` (= Swerve), so `BOX(·)` reads
"provably swerves" and `BOXD(·)` "provably goes straight". Row player's payoff `pay[a][b]`:

| game | St/St (P) | St/Sw (T) | Sw/St (S) | Sw/Sw (R) | convention payoff sum T + S | mutual swerve 2R |
|---|---|---|---|---|---|---|
| `chicken` (games/chicken.yaml) | −10 | 2 | −1 | 0 | 1 | 0 |
| `hd3` (V = 2, C = 3) | −1/2 | 2 | 0 | 1 | 2 | 2 |
| `hd6` (V = 2, C = 6) | −2 | 2 | 0 | 1 | 2 | 2 |

The games are symmetric, so with fixed roles both populations face the same table: a role-1 program a against a
role-2 program b earns U[a, b], and b earns U[b, a], where U is the one-population matrix. With s = P(a swerves vs b)
and t = P(b swerves vs a), evaluated independently (the repo's evaluator convention),
U[a, b] = (1−s)(1−t)P + (1−s)t T + s(1−t) S + s t R.

**Minimax.** In all three games the maximin action is Swerve (Swerve's worst payoff S ≥ −1 against Straight's P ≤ −1/2
… −10). The weak evaluator resolves divergent self-reference to the minimax action of the evaluating program, so the
weak play matrix is the same for the three games (one evaluation serves all three tables). The modal arm has no
minimax default (GL fixed points are unique).

**Fitness map.** The repo's exponential map with w = 0.3: a class with mean payoff f has reproductive weight
exp(w f), so negative payoffs are allowed without shifting. Constant-selection Moran fixation of one mutant with
payoff advantage Δ in a population of N: ρ(Δ) = (1 − e^{−wΔ}) / (1 − e^{−N w Δ}) (ρ = 1/N at Δ = 0).

**Convention properties (action space).** Each game is an anti-coordination game with T > R and S > P. With fixed
roles the two pure profiles (Straight | Swerve) and (Swerve | Straight) are strict Nash equilibria: the winner's
deviation costs T − R (2, 1, 1) and the loser's S − P (9, 1/2, 2). Mutual swerve and crash are not equilibria. The
one-population (symmetric) mixed equilibrium puts Straight at x* = (T − R)/((T − R) + (S − P)) = 2/11, 2/3, 1/3 with
payoff S·x* + R(1 − x*) = −2/11, 1/3, 2/3; in the two-population game the symmetric interior point (x*, x*) is a
saddle.

### 1.2 Arms and catalogues (n = 6, no `ROLE`)

| arm | grammar | programs | classes | Straight / Swerve mass | other |
|---|---|---|---|---|---|
| **weak** | standing weak DSL with `X`, no `ROLE` | 1,852 | 46 | 0.329 / 0.329 | X-mixtures 0.330 |
| **modal** | `src/modal.py`, all four box kinds | 1,020 | 51 | 0.469 / 0.469 | |
| **W0** (matched) | weak DSL without `X` and `ROLE` | 666 | 12 | 0.488 / 0.488 | |
| **M0** (matched) | modal, PA box only | 666 | 8 | 0.489 / 0.489 | |
| **const** (control) | {Straight, Swerve} | 2 | 2 | 1/2 / 1/2 | |

Classes are identical rows and columns of the swerve-probability matrix S (S[a, b] = P(a swerves against b)); in
each game they coincide with the repo's payoff classes (rows and columns of U), checked in §1.10. Masses are the
standing length prior μ (bits = log₂ a(|p|) + 2 log₂|p| + 1, normalized over the catalogue), summed per class. The
same class set and prior serve both roles (the role is the population, and no program can read it).

**Tags by play against the two constants** (the four on-path behaviours; enumerated):

| tag | vs Straight | vs Swerve | weak (classes, mass) | modal | W0 | M0 |
|---|---|---|---|---|---|---|
| firm (commits) | Straight | Straight | 3, 0.329 | 1, 0.469 | 2, 0.489 | 1, 0.489 |
| swerver | Swerve | Swerve | 2, 0.329 | 1, 0.469 | 2, 0.489 | 1, 0.489 |
| **bridge** (conditional straight: straight iff you would swerve) | Swerve | Straight | 5, 0.00185 | 28, 0.0310 | 4, 0.00396 | 3, 0.00396 |
| matcher | Straight | Swerve | 7, 0.0101 | 21, 0.0310 | 4, 0.0187 | 3, 0.0187 |
| mixed (X) | – | – | 29, 0.330 | 0 | 0 | 0 |

The **conditional straights** are the bridges: weak `not(THEM(ME))`, `not(THEM(THEM))`, `not(THEM(^Swerve))`,
`not(THEM(^Straight))`, `not(THEM(^X))`; modal `not(BOX(THEM(ME)))` (straight iff the opponent provably swerves
against me), `BOXD(THEM(ME))` (swerve iff the opponent provably goes straight against me), their PA + Con, `THEM`
and probe variants. Against a constant Straight every conditional straight swerves (that is what makes it one).

### 1.3 Lemma F: the two-population ε→0 chain is monomorphic per role

In the rare-mutation limit a mutant q in role 1 meets a role-2 population that is monomorphic at b, so every role-1
class has the constant fitness exp(w U[·, b]) whatever the role-1 composition. Selection inside a role is constant,
the mutant's lineage fixes with ρ(U[q, b] − U[a, b]) or dies, and no polymorphic rest point exists within a role.
The chain's states are the K² monomorphic pairs (a | b); there are no polymorphic traps to discover, no threshold
exploration and no lumped-resident approximation (twin drift is inside a class by construction). The
"program-space closure" of a convention is therefore the set of pairs reachable from it by single-mutant moves with
Δ ≥ 0, and a **candidate trap** is a closed strongly connected class of that Δ ≥ 0 graph. Both are computed exactly
on all K² states. (This is the dollar-partitions fixed-role chain, `src/dollar_partitions.py::fixed_chain`; the
REJECTED.md entry against the monomorphic Fudenberg–Imhof chain concerns one population with frequency-dependent
coexistence and does not apply within a role.) The one-population modal arm (c) has polymorphic rest points and
uses the audited seeded log-domain solver (§1.8).

### 1.4 The two conventions and their program-space closure (hand derivation)

Write a convention as (winner | loser) by play: the winner plays Straight and the loser Swerve on path. Take
(Straight | Swerve), role 1 winning; the other is its mirror.

*No strict entrants.* The winner earns T, the largest entry of the table, so no role-1 mutant gains. The loser earns S
against a firm Straight; a role-2 mutant earns S if it swerves and P < S if it goes straight, so none gains.

*Neutral neighbourhoods.* Role 1: every class that plays Straight against Swerve (firm, bridge, and the X-mixtures
that are certain Straight against a swerver; mass 0.331 weak, 0.500 modal, 0.493 W0 and M0). Role 2: every class
that swerves against Straight (swerver, bridge, mixtures; the same masses by the Straight↔Swerve duality of the
tags). Each enters at ρ = 1/N.

*The escape path.* If role 1 drifts to a **bridge** B (rate ½ μ_B / N per mutation event), the winner now swerves
against Straight, so a role-2 Straight mutant earns U[St, B] = T against the incumbent loser's U[Sw, B] = S (the
bridge goes straight against a swerver): a strict move with
Δ = T − S (3 in chicken, 2 in both hawk–doves), ρ_∞ = 1 − e^{−wΔ} = 0.593 (chicken) and 0.451 (hawk–dove). The
result (B | Straight) is the **other convention by play**. A firm winner closes the path: against firm Straight the
loser's Straight earns P < S. So the convention is held by the commitment, and the commitment's own neutral
neighbourhood contains the readers that undo it.

*Closure.* In every arm with bridges, both conventions lie in one closed class of the Δ ≥ 0 graph: neither is
drift-closed, and each exits by one neutral step plus one strict step, an exit ∝ 1/N. In the constants-only control
there are no bridges, each convention is its own closed class (exits deleterious, rate ∝ e^{−cN}: the role-1 Swerve
mutant has Δ = R − T = −2/−1/−1 and the role-2 Straight Δ = P − S = −9/−1/2/−2).

*Other candidate traps (by hand).* Crash (St | St): any class swerving against Straight in either role gains S − P;
not closed. Mutual swerve (Sw | Sw): Straight gains T − R in either role; not closed. Pairs of readers: a winner that
is a bridge is open by the escape path; a winner that is a matcher (Straight against Straight, Swerve against Swerve)
is not a winner against a swerver. The only way a reader pair can be a one-sided convention without being open to
the loser's Straight is a winner that goes straight against Straight, i.e. firm against the loser's best deviation:
then it is on path a commitment. I expect no closed class other than the one containing both conventions in the four
reader arms, and two closed classes (the two conventions) in the constants arm; §1.10 checks this on all K² states.

**Hand estimate of the exit rate** (per mutation event, per unit convention mass, N ≫ 1): the winner sits in its
neutral network with weights ∝ μ; the exit is the flux into bridges times the probability that the strict step comes
before the drift back, which is → 1 (strict rate ½ μ_St ρ_∞ ≈ 0.1 against a drift back of ≈ ½·0.33/N). So
N · exit ≈ ½ μ_B: **weak 9.3·10⁻⁴, modal 1.55·10⁻², W0 and M0 1.98·10⁻³**, the same in the three games (the game enters
only through ρ_∞ of the strict step, which saturates). π splits exactly 50/50 between the conventions by the
role-exchange symmetry (identical tables and priors).

### 1.5 Bridge–resident and bridge–bridge tables (both roles)

The game is symmetric and no program can read its role, so each table below holds verbatim in role 1 and in role 2;
"row" is the bridge's population, "column" the other population.

*Bridge–resident* (every bridge, every arm, by definition of the tag): against the loser's Swerve the bridge plays
Straight (it can hold the winner's seat neutrally); against the winner's Straight it plays Swerve (it can hold the
loser's seat neutrally). So **a bridge is neutral in both seats of both conventions**: wherever a convention is
established, a bridge in the winner's seat opens it and a bridge in the loser's seat is inert. Against the X
resident a bridge's play depends on its probe (weak `not(THEM(ME))` against X: swerve with ½).

*Bridge–bridge* (enumerated; S[row, col] / S[col, row], 1 = swerve). Identical deterministic programs in opposite
roles play the same action, so the diagonal is mutual swerve or crash, never a convention. Weak:

| row \ col | `not(THEM(ME))` | `not(THEM(THEM))` | `not(THEM(^X))` | `not(THEM(^Swerve))` | `not(THEM(^Straight))` |
|---|---|---|---|---|---|
| `not(THEM(ME))` | 1/1 | 1/1 | ½/½ | 0/1 | 1/0 |
| `not(THEM(THEM))` | 1/1 | 1/1 | ½/½ | 0/1 | 1/0 |
| `not(THEM(^X))` | ½/½ | ½/½ | ½/½ | ½/1 | ½/0 |
| `not(THEM(^Swerve))` | 1/0 | 1/0 | 1/½ | 1/1 | 1/0 |
| `not(THEM(^Straight))` | 0/1 | 0/1 | 0/½ | 0/1 | 0/0 |

Hand derivation of the weak cells: `not(THEM(ME))` against q plays not(q's play against it); against itself that
regress diverges and resolves to the minimax Swerve; `not(THEM(^Swerve))` plays not(q against Swerve) = Swerve
against any bridge (bridges go straight against Swerve); `not(THEM(^Straight))` plays not(q against Straight) =
Straight against any bridge, including itself (so it crashes in self-play). Distinct probes therefore **can**
anti-coordinate: (`not(THEM(^Straight))` | `not(THEM(^Swerve))`) is a one-sided convention between two readers,
role 1 winning, and so is (`not(THEM(ME))` | `not(THEM(^Swerve))`). Both are open: the winner is a bridge, and the
loser's Straight takes it (Δ = T − S).

Modal (28 bridges): the 8 `not(BOX…)` bridges swerve against every bridge (mutual swerve among themselves); the 20
`BOXD…` bridges ("swerve iff provably the opponent goes straight against me") crash against themselves (at world 0
the box holds and they swerve, so from world 1 on the box fails and they go straight) and against each other. The
M0 bridges (`not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))`, `not(BOX(THEM(^C)))`) all swerve against each other. The
full modal table is written by the code to `runs/fixed-role-chicken.json` (static block).

*The matched pair (W0 vs M0)* has identical program counts and prior; on the 666 × 666 program pairs the two play
matrices differ in 2,000 cells (0.45%), all of them a matcher (`THEM(ME)`-type: copies the opponent's play against
me) against a bridge: the weak regress diverges to the minimax Swerve, the modal box is false and the matcher goes
straight. In the PD the weak default (D) and the Löbian fixed point (C) disagree everywhere; in chicken the weak
default is Swerve and coincides with the Löbian fixed point of the positive boxes, so simulation and provability
nearly coincide.

### 1.6 Outcome classification by play (frozen)

For role compositions x (role 1) and y (role 2) on an island, the encounter distribution is
J = Σ_ab x_a y_b J[a, b] over the four ordered action pairs (role 1 first), J[a, b] = the product of the two swerve
probabilities. An island (or a chain state) is classified:

- **R1** (role 1 wins) if J(St, Sw) ≥ 0.95; **R2** if J(Sw, St) ≥ 0.95 (together: *a one-sided convention*);
- **crash** if J(St, St) ≥ 0.95; **dove** (mutual swerve/dove) if J(Sw, Sw) ≥ 0.95;
- **mixed** otherwise.

Genotype diversity is reported separately (classes present per role; *polymorphic* = more than one class in some
role), so a polymorphic island implementing a perfect norm is R1 or R2, and two monomorphic readers that crash are
crash. Mutual dove is reported separately as well: in both hawk–dove tables it is Pareto-efficient with the same
payoff sum (2) as either convention; convention frequency is not an efficiency statistic. **Efficiency** is reported
as the mean payoff sum per encounter against the convention benchmark T + S; **loss** = (T + S) − E[u₁ + u₂].

*Establishment (per island, frozen).* An island is **established** at outcome O if its class is O at every sample in
the last tenth of the horizon (≥ 200 generations at 2,000; ≥ 400 at 4,000); its establishment generation is the first
sample after which the class never changes to the horizon. The **per-island establishment probability** of a
one-sided norm (the RS's scored quantity) is the fraction of islands, pooled over runs, established at R1 or R2;
the run-level uncertainty is the spread of the per-run fractions (mean ± 95% t-interval over the 40 runs).

*E3 resolution (milestone 2's endpoint adapted to classes by play, frozen).* For island i let Z₁, Z₂ be its present
classes per role; the entrant pool is every class present on any island at the sample if mN > 0, and the island's
own classes if mN = 0. Close Z under: a pool class q of role r joins Z_r if U[q, b] ≥ U[z, b] − 10⁻⁹ for some
z ∈ Z_r and some b ∈ Z_{3−r} (it can enter neutrally or better against some present pair). The island is
**E3-resolved at O** if every pair (a, b) ∈ Z₁ × Z₂ has class O by the 0.95 rule; a run is E3-resolved at the first
sample at which every island is; runs not resolved by the horizon are censored, with the resolution times reported.

### 1.7 The lottery law (frozen exactly as the spec states it)

- Islands: I = 64, each with two populations (role 1 and role 2) of N per role; N = 100, with a small-N panel
  N ∈ {25, 50}.
- Seeds: every slot of every role on every island iid from the arm's class prior μ (multinomial(N, μ) per island
  per role, with replacement); roles independent.
- Updating: Moran birth–death per role with the exponential fitness map (w = 0.3). An event picks an island and a
  role uniformly; a uniformly random resident of that role dies; it is replaced by an offspring of a parent of the
  same role drawn with probability ∝ count · exp(w f) from the same island (probability 1 − m) or from a uniformly
  random other island (probability m = mN/N; the complete island graph). f = the parent class's mean payoff against
  the N residents of the other role on the parent's own island (fitness evaluated at home).
- Migration at mN ∈ {0, 1}, role-preserving (a role-1 migrant replaces a role-1 resident); emigrants unweighted (the
  source island is uniform; payoff-weighted emigration is the island-selection arm and is not used).
- A generation is N birth–death events per role per island (2·I·N events).
- Horizon 2,000 generations; every mN = 1 cell is run to the doubled horizon 4,000 and reported at both.
- Samples every 10 generations. A cell is stopped early only when nothing can change: at mN = 0 when every island is
  frozen (within each role, the present classes have identical payoffs against every present class of the other
  role, both ways); at mN = 1 when that holds for the global present sets. A frozen island's play is fixed.
- 40 runs per cell; run-level uncertainty as in §1.6. The lottery panel is finite-size evidence and is labelled so.

Statistics per cell: per-run fraction of islands at R1, R2, crash, dove, mixed; per-island establishment probability;
the role-1/role-2 split among convention islands; patchworks (a run with islands at both conventions at the
horizon); resolutions (a run that was a patchwork at some sample and has one convention at the horizon), their
generation, and the classes on the islands that flipped; establishment generation; on-island crash and dove rates
(second-half time average and at the horizon); between-island crash rate and the **cross-island role-preserving
loss**: role-1 residents of island A against role-2 residents of island B, A ≠ B, averaged over ordered pairs,
against the benchmark T + S (the universality statistic).

*Flip attribution* (frozen): an island flip is a change of the island's convention (R1 → R2 or back) between samples,
possibly through mixed samples. At the last convention sample before it I record the share of bridge classes (§1.2
tag) in the then-winning role and whether selection then favoured the incumbent loser's best straight-playing class
(its fitness above the loser role's mean); a flip is **reader-mediated** if the winner's bridge share was at least
the threshold f* = (S − P)/(T − P) at which a loser's Straight beats Swerve (0.75 chicken, 0.2 hd3, 0.5 hd6), and
**demographic** otherwise.

### 1.8 The chain (ε → 0; rare mutation)

Two-population arms (weak, modal, W0, M0, const): the exact K² monomorphic chain of Lemma F, N per population
∈ {10², 10³, 10⁴}. A mutation event picks a role uniformly and draws q ~ μ; q fixes with ρ(Δ). Solved on the jump
chain by linear GTH (no subtractions; edges below 10⁻³⁰ of a row's total dropped and the dropped flow reported as the
cut), π(s) ∝ π_jump(s)/R(s) with R in the log domain; validated against dense log-domain GTH
(`chain_log.gth_log`) on full generators. Reported: π over outcome classes (§1.6), support, the lumped transition
structure between classes, each convention's exit rate per unit mass with its N-scaling (N·exit), the decisive edges
with their Δ and N·Δ (and N·ρ), the cut.

One-population modal arm (c): `chain_log.LogChain` over the modal class matrix, seeded with
`solver_audit.enumerate_candidates_fast` (≤ 3 classes) and `solver_audit.invasion_closure`; `explore_log` at
θ_log = 10⁻¹⁴ with the 10⁻¹² / 10⁻¹⁶ sensitivity; twin-expanded beside lumped; the cut diagnostic wherever the
unexplored flow exceeds 2%. Rare mutation and the lottery are separate objects, never pooled.

### 1.9 Controls (frozen)

1. **Constants-only** two-population control (catalogue {Straight, Swerve}, μ = ½, ½): chain and lottery, all games,
   N ∈ {25, 50, 100}, mN ∈ {0, 1}. Does plain anti-coordination already produce the norms?
2. **Matched grammar/prior** W0 vs M0 on paired seeds: seeds are drawn as *programs* from the common prior over the
   666 spellings, and each seeded program is mapped to its W0 class and its M0 class (the isomorphism
   `THEM(P)` ↔ `BOX(THEM(P'))`), with identical RNG streams; all games, mN ∈ {0, 1}, N = 100.
3. **Forced opposite-convention islands, bridges included vs removed at matched founder mass** (weak and modal, all
   games, mN = 1, N = 100, horizon 4,000, 40 runs): islands 0–31 founded at (Straight | Swerve), 32–63 at
   (Swerve | Straight). *Included:* in each role a fraction β = 0.1 of the founders are bridges (drawn ∝ μ among the
   arm's bridge classes), the rest the convention's constant for that seat. *Removed:* the same founder counts with
   every bridge founder replaced by that seat's constant (same on-path play). Reported: resolution rate, flips and
   their attribution.
4. **Role-swapped runs** (the payoff tables transposed, i.e. the two populations exchanged in the implementation):
   the main weak and modal cells at N = 100, mN ∈ {0, 1}, with the swap flag; the role-1 share of convention islands
   must match the unswapped cells, and both ≈ ½. A unit test checks that the swap with the same RNG seed produces the
   exact mirror image.
5. One-population modal arm (c) lottery: one population of N = 100 per island, same law otherwise, mN ∈ {0, 1}, all
   games (a one-sided norm is impossible by arithmetic: the asymmetric outcome has probability ≤ 2x(1 − x) ≤ ½).
