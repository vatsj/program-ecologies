# Where does the leader-value core exist? (2026-10-14)

Spec `specs/2026-10-14-core-existence-sweep.md` (its "Amendments after review" supersede earlier text); predictions
`predictions/2026-10-14-core-existence-sweep.md` (committed first). Companion to `notes/leader-value-core.md` and
DEFERRED 15. A static compatibility computation: nothing here is about evolutionary accessibility (amendment 7).

## 1. Definitions

**Game.** Players N = {1, …, n}, action sets A_i, payoffs u_i. For a coalition S ⊊ N with complement C = N∖S and a
commitment a_S ∈ A_S, the complement's **response set** E_C(a_S) is
- *individual* (default; the γ-convention of Chander–Tulkens 1997, here with S moving first): the pure Nash
  equilibria of the complement subgame in which each j ∈ C best-replies to (a_S, a_{C∖j});
- *coordinated* (panel variant): argmax over a_C of Σ_{j∈C} u_j(a_S, a_C), the complement as one player.

When E_C(a_S) has several elements: **pess** (S faces the worst element) and **opt** (the best); in TU "worst" is S's
sum, in NTU it is quantified per element (below). When a supremum is not attained (homogeneous Bertrand), v(S) is the
supremum and the case is labelled.

**TU leader-value game.** v(S) = sup_{a_S} sel_{a_C ∈ E_C(a_S)} Σ_{i∈S} u_i(a_S, a_C), sel = min (pess) or max (opt);
v(N) = max_a Σ_i u_i(a). TU core: {x ∈ ℝⁿ : Σ_i x_i = v(N), x(S) ≥ v(S) for all S}. **Least-core value**
ε\* = max_x min_{S ≠ ∅, N} (x(S) − v(S)) subject to Σ x = v(N); the core is nonempty iff ε\* ≥ 0. By LP duality
(Bondareva–Shapley) ε\* < 0 iff some balanced collection {λ_S} (Σ_S λ_S 1_S = 1_N, λ ≥ 0) has Σ λ_S v(S) > v(N).
Verdicts: **nonempty** ε\* ≥ 1e-9·scale; **tight** |ε\*| < 1e-9·scale (nonempty, knife edge); **empty**
ε\* ≤ −1e-9·scale, with scale = max(|v(N)|, 1). Certificates: the dual's balanced collection, its weights
rationalized and the balancing identity re-checked in exact arithmetic, and the gap Σ λ_S v(S) − v(N); for nonempty
and tight cases the least-core allocation and its minimum slack.

**NTU leader-value core.** A profile a\* is *blocked* by S ⊊ N iff there is a_S with
- pess: for every a_C ∈ E_C(a_S) and every i ∈ S, u_i(a_S, a_C) > u_i(a\*);
- opt: for some a_C ∈ E_C(a_S), u_i(a_S, a_C) > u_i(a\*) for every i ∈ S;

and by N iff some profile is strictly better for every player. The NTU core is the set of unblocked profiles (no
transfers; outcomes are action profiles, as in the RS's f(∅)). *Blocking margin* B_S(z) = sup over commitments of
min_{i∈S}(u_i − z_i) at the selected response (a payoff-unit number; S blocks z iff B_S(z) > 0). Verdicts:
**nonempty** when a profile is found whose every B_S is certified ≤ 0 (strict when all < 0); **empty** when certified
(the singleton bound below, or a branch-and-bound over profiles that proves every box blocked); **unresolved**
otherwise. *Singleton bound:* singletons have the same leader values in TU and NTU, and every NTU payoff vector sums
to at most the TU v(N); so Σ_i v({i}) > v(N) implies an empty NTU core as well.

**First-mover advantage** (timing; RE 6): FMA(S) = v(S) − v_F(S), where v_F(S) is S's payoff at the outcome that
realizes v(C) when C leads (C's leader-optimal commitment with its selected response; ties among C's optimal
commitments broken in S's favour). "S gains from moving first" iff FMA(S) > 1e-9·scale. **Follower dominance** at S
(a payoff comparison inside one outcome, not timing): at S's leader outcome the mean payoff of C's members is at least
the mean payoff of S's members.

**Simultaneous-partition control** (amendment 6; the merger-paradox control). v_sim(S) = S's joint payoff in the pure
Nash equilibrium of the game with players {S as one player maximizing Σ_S u} ∪ {each j ∈ C}; this is the
Chander–Tulkens γ-worth. The leader can commit to S's equilibrium action, to which the complement's equilibrium
actions are a response; where that response is the unique element of E_C (or under opt) S gets at least v_sim(S), so v(S) ≥ v_sim(S) and **the leader-value core is contained in the γ-core** (TU). Emptiness of the
leader core with a nonempty γ-core is therefore a timing effect; emptiness of both is a coalition-size effect.

**Identities.** With individual responses and pess/opt the TU object is the γ-core with S as Stackelberg leader (the
sequential characteristic function in the sense of Currarini–Marini; we have not checked our numbers against theirs).
It equals the Chander–Tulkens γ-core only where leading and moving simultaneously give the same worth (e.g. games with
dominant-strategy responses). The identity with the RS's notion (DEFERRED 15) is the claude.ai session's
characterization; this sweep checks implementation consistency on the catalogue, not that equivalence.

**Symmetric games.** If the game is symmetric, v(S) depends on |S| only and the TU core is convex and
permutation-invariant, so it is nonempty iff the equal split v(N)/n is in it, i.e. iff v(s)/s ≤ v(n)/n for every s.

## 2. Symmetric linear Cournot, verified analytically (amendment 5)

p = a − Q, common marginal cost c, m = a − c > 0, n firms, individual (Cournot) followers.

1. **Grand coalition.** v(N) = max_Q Q(m − Q) = m²/4 at Q = m/2.
2. **Coalition of size k leading** against r = n − k followers. With constant marginal cost S's joint profit depends
   on Q_S only. Given Q_S < m the followers' unique Cournot equilibrium is q_f = (m − Q_S)/(r + 1), so
   p − c = (m − Q_S)/(r + 1) and S earns Q_S(m − Q_S)/(r + 1), maximal at Q_S = m/2 (where the followers are active).
   Q_S ≥ m gives p ≤ c. Hence **v(S) = m²/(4(n − k + 1))**, the classical Stackelberg profit against r followers.
3. **Equal split.** x_i = m²/(4n). For |S| = k: x(S) − v(S) = (m²/4)·[k/n − 1/(n − k + 1)]
   = (m²/4)·(k − 1)(n − k)/(n(n − k + 1)) ≥ 0, because k(n − k + 1) − n = (k − 1)(n − k). Equality iff k = 1 or k = n.
   So the equal split is in the core and **every singleton constraint binds**.
4. **Uniqueness.** Σ_i v({i}) = n·m²/(4n) = v(N); any core allocation has x_i ≥ m²/(4n) and sums to m²/4, so the TU
   core is the single point (m²/(4n), …, m²/(4n)) for every n ≥ 2 (verdict "tight": ε\* = 0).
5. **NTU.** Total profit is Q(m − Q) ≤ m²/4 with equality iff Q = m/2. A profile meeting every singleton value
   m²/(4n) must therefore have Q = m/2 and π_i = q_i·m/2 = m²/(4n), i.e. q_i = m/(2n). It is unblocked: singletons
   can only tie; a coalition of size k ≥ 2 earns at most m²/(4(n − k + 1)) ≤ k·m²/(4n) under any commitment, so not
   all its members can strictly gain; N cannot (Q = m/2 maximizes the total). **NTU core = {q_i = m/(2n)}.**
6. **Coordinated followers** (panel): the complement acts as one firm, so every proper S earns the one-follower
   Stackelberg profit m²/8. Singletons then claim n·m²/8 > m²/4 for n ≥ 3: **empty** for n ≥ 3, tight at n = 2.
7. **Simultaneous partition.** S as one firm against r singletons is Cournot with r + 1 firms: v_sim(S) =
   m²/(n − k + 2)². The equal split meets it iff k(n − k + 2)² ≥ 4n, true for 1 ≤ k ≤ n − 1 (at k = 1:
   (n + 1)² > 4n); the γ-core is nonempty with strict slack. So the symmetric leader core's tightness is a timing
   effect: moving first raises a singleton from m²/(n + 1)² to exactly its per-capita share.

The code reproduces items 1–7 (tests `test_symmetric_cournot_*`).

## 3. Hand analysis behind the predictions (before any computation)

**3.1 Cournot TU, one cost deviation (S2).** a = 1, costs c_i = c̄ + e_i, Σ e_i = 0, m̄ = 1 − c̄. A singleton leader
facing n − 1 active followers earns v({i}) = (1 + C − (n + 1)c_i)²/(4n), C = Σ_j c_j, so Σ_i v({i}) =
m̄²/4 + (n + 1)² Σ e_i²/(4n), while v(N) = (1 − c_min)²/4. On the ray c = (0, …, 0, h):
Σ e² = (n − 1)h²/n and v(N) − m̄²/4 = (2h/n − h²/n²)/4, so Σ v({i}) > v(N) iff h > h\* = 2n/((n + 1)²(n − 1) + 1)
(0.1818 at n = 3, 0.1053 at n = 4). The formula needs the high-cost follower active against a low-cost leader,
h < 1/(2n − 1) (0.2 at n = 3, 0.143 at n = 4), so the singleton partition certifies emptiness at least on
(h\*, 1/(2n − 1)). At n = 2 the same computation gives Σ v({i}) ≤ v(N) iff c₂ ≤ 0.4, and c₂ ≤ 1/3 in the interior
regime (above it firm 1 deters and v({1}) = (1 − c₂)c₂, still below v(N)), so n = 2 is never TU-empty.

**3.2 Cournot NTU at n = 2 (S3).** m₁ = 1, d = c₂ ∈ (0, 1/3): v₁ = (1 + d)²/8, v₂ = (1 − 2d)²/8, and
v₁ + v₂ = 1/4 − d/4 + 5d²/8. Write q₁ = 1/4 + αd + O(d²), q₂ = 1/4 + βd + O(d²). To first order π₁ ≥ v₁ needs
α − β ≥ 1 and π₂ ≥ v₂ needs α − β ≤ 1, so α = β + 1. The sum constraint π₁ + π₂ = Q(1 − Q) − d·q₂ ≥ v₁ + v₂ at order
d² reads −(α + β)² − β ≥ 5/8, i.e. 4β² + 5β + 13/8 ≤ 0 with α = β + 1, whose discriminant 25 − 26 < 0: no solution.
So for small d > 0 no profile meets both singleton leader values: **the NTU core is empty** near the symmetric
point, though the TU core is not. For d ∈ [1/3, 1/2) the deterrence regime (v₁ = (1 − d)d, v₂ = (1 − 2d)²/8) is
also short (the slack of firm 1 buys firm 2 only O(ε³) profit with ε = ½ − d against v₂ = ε²/2); at d ≥ ½ firm 2
has no leader value and the monopoly profile is in the core.

**3.3 Public goods (S6).** u_i = θ_i f(G) − g_i. The complement's equilibrium total given S's total G_S is
max(G_S, G_C) with G_C = argmax θ_{C,max} f(G) − G (only the complement's largest valuation contributes), so
v(S) = max(θ_S f(G_C), max_{G ≥ G_C} θ_S f(G) − G): **free-ride** or **take over**. Symmetric n = 2, f = ln(1 + G):
v({i}) = θ ln θ (θ > 1), v(N) = 2θ ln 2θ − 2θ + 1, empty iff θ > 1/(2(1 − ln 2)) ≈ 1.629. f = 2√G: v({i}) = 2θ²
= v(N)/2, tight; for n ≥ 3 the singleton sum is max(θ₁², 2θ₁θ₂) + 2θ₁(θ_N − θ₁) ≤ θ_N² (AM–GM), equality only at
n = 2 symmetric. ρ = 2, symmetric n = 3: empty for θ > 4.64 (just outside the grid's θ ≤ 4).

**3.4 Lemma SMA (follower dominance ⇒ the equal split is in the core; symmetric games).** *Proof.* Let (a_S, a_C) be S's
leader outcome and suppose C's mean payoff is at least S's. Then v(S)/|S| ≤ (Σ_S u + Σ_C u)/n ≤ v(N)/n. If this holds
for every proper S, the equal split meets every constraint; it is also an NTU core point when the efficient profile
is symmetric (S's total ≤ |S|·v(N)/n means not every member can strictly exceed v(N)/n). ∎ *Converse direction:* if a
symmetric core is empty, some S has v(S)/|S| > v(N)/n ≥ (total at its leader outcome)/n, so S's members out-earn the
followers on average at that outcome. **Aligned distortion.** In a symmetric game with leader members at a and
followers at b (follower b a best reply), u_F = u(b | s·a, (n−s−1)·b) ≥ u(a | s·a, (n−s−1)·b), and replacing one
"a" among the others by "b" moves a leader member's payoff by the spillover times (b − a); so u_F ≥ u_L whenever
(b − a)·∂u_i/∂x_j ≤ 0 along the segment, i.e. the leader distorts in the direction its spillover favours the
followers. In the linear-quadratic family with σ ≥ 0 the symmetric leader stationary point satisfies a ≥ b (from the
two first-order conditions: (a − b)(1 + γ) = γ r k a + σ r k ≥ 0 for |S| = 1, with k = γ s/(1 − γ(r − 1)) the
followers' response slope; for |S| ≥ 2, a − b = γ((s − 2)a + b + r k a) + σ(s − 1 + r k) ≥ 0); the spillover is
γ x_i + σ ≥ 0; so follower dominance holds. With σ ≤ −γ·x_max the same equations give a ≤ b and a negative
spillover, again aligned. This is a **partial proof** of RE 4 (symmetric points, interior symmetric leader optimum
with a concave induced problem); the sweep checks the rest.

## 4. Methods as run (`src/core_sweep.py`, `src/core_sweep_report.py`; tests `tests/test_core_sweep.py`)

**TU.** Leader values in closed form or exactly: Cournot by the piecewise-linear price response p(Q_S) (exact
kinks where followers enter or exit or capacities bind) with S's joint profit concave quadratic on each piece;
homogeneous Bertrand by suprema (limit pricing); public goods by "free-ride or take over" (§3.3); quadratic games
(linear-quadratic supermodular, differentiated Bertrand) by the affine follower response substituted into S's
quadratic and active-set enumeration on S's bounds (followers are interior throughout under individual responses:
best replies b_j + γX_{−j} > 0 in LQ; no bounds in Bertrand); exchange economies by a concave program (SLSQP from
several starts; the program is concave, so local is global up to solver tolerance). The least-core LP (HiGHS) and
the Bondareva–Shapley dual give verdicts and certificates; every empty verdict's collection was re-checked as
balanced in exact rationals.

**NTU.**
1. *Cournot* (§4.1). At grand total Q every candidate payoff vector is z ≥ 0 with Σ z_i/μ_i(Q) = Q, μ_i = 1 − c_i − Q,
   and S fails to block z iff Σ_{i∈S} z_i/m_i(Q_S) ≥ Q_S for every S-total Q_S with all margins m_i(Q_S) > 0, which is
   linear in z. A grid in Q_S (200 points) relaxes the coalition constraints and an interval relaxation in Q
   (1/μ_i monotone) gives an LP whose infeasibility on every interval certifies emptiness; a found z is verified
   with the exact one-dimensional blocking margins. Breakpoints at μ_i = 0 keep intervals regular.
2. *Homogeneous Bertrand*: an analytic certificate (the min-cost firms share the monopoly profit; no coalition
   can improve all its members).
3. *Public goods and quadratic games*: (a) the singleton bound (Σ v({i}) > v(N) ⇒ NTU empty); (b) a profile whose
   payoff vector lies in the TU core (z(S) ≥ v(S) for all S ⇒ no S can make all members strictly better), an LP in
   z for each G in public goods (value concave in G), SLSQP over profiles in quadratic games; (c) for quadratic
   games, weighted-utilitarian candidates x(w) = argmax Σ w_i u_i checked with the weighted bound
   B̃_S(z) = min_λ (max Σ_{i∈S} λ_i u_i − λ·z_S) ≤ 0 (which rules out blocking), then a branch-and-bound over a box
   that provably contains every candidate (the welfare ellipsoid Σ u ≥ Σ v({i})), killing boxes by singleton
   interval bounds or by coalition menus (weighted-leader payoff vectors), then a direct search; (d) for public
   goods a direct search with exact water-filling blocking margins. A case none of these settles is
   **unresolved**.
4. *Exchange economies*: the competitive allocation (Cobb–Douglas by the linear price system, CES by root
   finding) and, for every coalition, the concave program max t s.t. u_i(y_i) ≥ u_i(x_i) + t, Σ y ≤ ω_S; the
   allocation is certified when every margin is ≤ 1e-7. Under opt (gifts of worthless goods) the singleton bound,
   a TU-core allocation, or the competitive allocation is tried.

**Grids** as fixed in the predictions file; the panel and catalogue as listed there. Workers: 2.

## 5. Results (`runs/core-existence-sweep.json`; tables in `runs/core-existence-sweep.md`)

Verdict counts are nonempty / tight / empty (/ unresolved); "tight" is a nonempty core with zero least-core slack
(symmetric knife edges, and dummy firms whose leader value is exactly 0). Every empty TU verdict carries a balanced
collection re-checked in exact rationals.

**Cournot** (p = 1 − Q, c₁ = 0).

| n | points | TU n/t/e | TU empty share | violating collection | γ-core empty | NTU (0.05 grid) n/t/e | NTU empty share |
|---|---|---|---|---|---|---|---|
| 2 | 21 | 19 / 2 / 0 | 0 | – | 0 | 0 / 2 / 9 | 0.82 (every 0 < c₂ < ½) |
| 3 | 231 | 196 / 28 / 7 | 0.030 | singletons (7/7) | 0 | 0 / 6 / 60 | 0.91 |
| 4 | 1,771 | 1,423 / 256 / 92 | 0.052 | singletons (92/92) | 0 | 0 / 18 / 268 | 0.94 |

TU emptiness needs at least two (near-)efficient firms and a moderately inefficient one (n = 3: c = (0, 0, h) for
h ∈ [0.2, 0.325] and (0, 0.025, 0.25); n = 4: c₂ ≤ 0.025); the violations are small (ε\* ≥ −0.0027 against
v(N) = 0.25). Along the ray the first empty grid point is h = 0.2 at n = 3 and 0.125 at n = 4 (h\* = 0.182, 0.105).
NTU emptiness is the rule: the NTU core survives only at the symmetric point, when the efficient firms are
symmetric and the others are priced out (c ≥ 0.35 at n = 3), and at c₂ = ½ (n = 2); 24 NTU empties follow from the
singleton bound and 313 from the interval-LP certificate. Capacity variant (common k ∈ {0.1, …, 0.4}, costs on the
0.1 grid): 0 empty of 332 (tight at k = 0.1, where capacities bind the leader).

**Homogeneous Bertrand**: 0 empty of 363 (TU and NTU); 360 points have an unattained leader value (a supremum).

**Public goods** (u = θf(G) − g; TU empty share; the NTU verdict equals the TU verdict at every point: empties by the
singleton bound, nonempties by a TU-core profile).

| f | n = 2 | n = 3 | n = 4 | n = 5 |
|---|---|---|---|---|
| 2√G | 0 (6 tight) | 0 | 0 | 0 |
| 2(√(1+G) − 1) | 0 | 0 | 0 | 0 |
| ln(1 + G) | 0.238 | 0.125 | 0.032 | 0.004 |
| 1 − 1/(1 + G) | 0.381 | 0.321 | 0.183 | 0.075 |

Every empty point (85) is certified by the singleton partition, and every one contains free-riding coalitions
(zero contribution against a contributing complement). Symmetric n = 2: log empty from θ = 2 (threshold 1.63),
ρ = 2 from θ = 1.5; at n ≥ 3 no symmetric point is empty. Log n = 3 empties are exactly the profiles with the two
largest valuations in {3, 4} (and (1.5, 4, 4)). The γ-core is nonempty at all 1,820 points (3 tight, at ties).

**Linear-quadratic supermodular** (1,560 points; classes by the realized spillover sign).

| spillover | points | TU n/t/e | γ-core empty | NTU n/t/e/u | symmetric points |
|---|---|---|---|---|---|
| positive (σ ≥ 0) | 780 | 780 / 0 / 0 | 0 | 780 / 0 / 0 / 0 | 144 nonempty, follower dominance at all |
| negative (γx_max + σ ≤ 0) | 643 | 641 / 2 / 0 | 0 | 641 / 2 / 0 / 0 | 117 nonempty, dominance at all |
| mixed | 137 | 119 / 3 / 15 | 13 | 93 / 4 / 0 / 40 | 27 nonempty, dominance at all |

The 15 empty points are all at σ ∈ {−0.25, −0.5} with heterogeneous b; their violating collections are pairs at ½,
partitions into two blocks, or a triple plus a singleton (not singletons), and the γ-core is empty at 13 of them
(unique simultaneous equilibria): a coalition-size effect, verified by brute force at b = (0.5, 1, 2), γ = 0.15,
σ = −0.25 (pairs ½(−0.090 + 1.827 + 2.504) = 2.120 > v(N) = 2.115). FMA at n = 2 is negative for every positive
point (second-mover advantage), but at n ≥ 3 coalitions of size n − 1 gain from leading. 40 mixed NTU cases are
unresolved (singleton-feasible region nonempty, no unblocked profile found, branch-and-bound unfinished).

**Differentiated Bertrand**: 332 points, none excluded (all quantities positive), TU and NTU nonempty everywhere,
γ-core nonempty; at symmetric points follower dominance holds at every coalition, singletons have a second-mover
advantage, and coalitions of size n − 1 a first-mover advantage at n ≥ 3 (0.002–0.53).

**Allocation games**: 800 instances under pess (Cobb–Douglas, CES ½ and 2, zero-weight Cobb–Douglas; n = 3, 4;
m = 2, 3): TU certified nonempty (primal and dual coalition values) and NTU certified nonempty (competitive
allocation unblocked) in every one. Under opt (gifts of goods worthless to their owner) 84/200 are TU-empty and 48
NTU-empty by the singleton bound (two players each count the same gift); 127 NTU cases unresolved. A first pass
reported 19 spurious TU-empty pess instances; the cause was an infeasible SLSQP output accepted as a coalition value,
fixed (infeasible outputs rejected, dual bounds added) before the counted run.

**Factorial panel** (TU ε\* ; NTU). Coordinated followers empty symmetric Cournot (ε\* = −0.042) and every public
goods panel point (log (1, 1, 1): +0.43 → −0.26), and keep LQ and Bertrand nonempty; pess and opt coincide at every
panel point (no ties in the response sets); TU and NTU differ at Cournot (0, 0.1, 0.3) (TU +0.005, NTU empty).

**Catalogue**: reproduced exactly (PD unique (C, C); chicken, hd3, hd6, `dollar5`, `dollar3` empty; SOG
{(0, work), (¼, work)} under pess and {(0, work)} under opt).

## 6. Proofs, partial proofs and counterexamples

**6.1 Proposition (symmetric linear Cournot; proof, §2).** For every n ≥ 2 the TU leader-value core is the equal
split and the NTU core the symmetric monopoly profile; both are knife edges (every singleton constraint binds).
Coordinated followers empty it for n ≥ 3; the simultaneous-partition (γ) core contains the equal split with strict
slack.

**6.2 Proposition (Cournot, n = 2, TU; proof).** a = 1, c = (0, d). For d ≤ 1/3, v₁ = (1 + d)²/8 (accommodation),
v₂ = (1 − 2d)²/8 and v₁ + v₂ = 1/4 − d/4 + 5d²/8 ≤ 1/4 = v(N) iff d ≤ 2/5. For d ∈ [1/3, ½) the leader-optimal
accommodation output (1 + d)/2 exceeds the deterrence output 1 − d, so v₁ = (1 − d)d and
v₁ + v₂ = 1/8 + d/2 − d²/2 = 1/4 − (d − ½)²/2 ≤ 1/4. For d ≥ ½, v₂ = 0 and v₁ = 1/4. So the two-firm TU core is never
empty (strict slack for 0 < d < ½). ∎

**6.3 Proposition (Cournot, n ≥ 3, TU emptiness; proof of a sufficient condition, counterexample to "Cournot TU is
always nonempty").** On the ray c = (0, …, 0, h) the singleton partition is a violating balanced collection for
h ∈ (h\*, 1/(2n − 1)), h\* = 2n/((n + 1)²(n − 1) + 1) (§3.1; the leader values used are attained commitments with
all followers active, so they are lower bounds on v and the violation is certified). The sweep finds the band wider
than the proven window (to h = 0.325 at n = 3, 0.225 at n = 4) and every empty point certified by the singleton
partition.

**6.4 Proposition (Cournot, n = 2, NTU; proof).** For c = (0, d), a = 1, the NTU leader-value core is empty for
every d ∈ (0, ½) and is the monopoly profile for d = 0 (with q_i = ¼) and d ≥ ½. *Proof.* With two players the NTU
core is nonempty iff some profile gives π_i ≥ v_i for both. Writing Q = q₁ + q₂, the profile exists iff
Q − v₁/(1 − Q) − v₂/(1 − d − Q) ≥ 0 for some Q < 1 − d, i.e. iff P(Q) = Q(1 − Q)(1 − d − Q) − v₁(1 − d − Q) − v₂(1 − Q) ≥ 0
(firm 2 earns ≤ 0 < v₂ when Q ≥ 1 − d). Put Q = ½ + t.
(i) d ∈ (0, ⅓], v₁ = (1 + d)²/8, v₂ = (1 − 2d)²/8: P = t²(t + d − ½) + t·d(5d − 2)/8 − d²(1 − 2d)/16. For t ≥ 0 every
term is ≤ 0 and the last < 0. For t = −s < 0, P ≤ −(½ − d)s² + s·d(2 − 5d)/8 − d²(1 − 2d)/16, whose maximum over s is
−d²(4 − 12d + 7d²)/(128(1 − 2d)) < 0 because 7d² − 12d + 4 > 0 for d < 0.453.
(ii) d ∈ [⅓, ½), e = ½ − d ∈ (0, ⅙], v₁ = (1 − d)d (deterrence), v₂ = (1 − 2d)²/8: P = t²(t − e) − (e²/2)t + e³ − e²/4.
For t ≥ 0 (and t < e) every term is ≤ 0 and the constant < 0; for t = −s < 0, P ≤ −e s² + (e²/2)s + e³ − e²/4 with
maximum (17/16)e³ − e²/4 < 0 for e < 4/17. So P < 0 throughout and the core is empty. ∎ Near the symmetric point
the shortfall is d²/32 to leading order (matches the second-order argument of §3.2 and the interval-LP slack). The
mechanism is the absence of transfers: the leader-value point moves outward at second order while the no-transfer
frontier, which must keep the inefficient firm producing to pay it, bends inward. The interval-LP method certifies
the same on the grid (d = 0.05, …, 0.45 empty; 0 and 0.5 tight).

**6.5 Proposition (allocation games; proof).** In an allocation game (own-bundle utilities, nonnegative marginal
utilities, gift actions) the complement's "keep" is a best reply to every commitment, and the unique one when
utilities are strictly increasing; under pess with zero weights the complement's keeping is the worst case for S
(gifts can only help S). So v(S) = max over reallocations of ω_S. *TU:* with concave utilities v is a market game
(Shapley–Shubik 1969): for a balanced collection λ and S-optimal allocations y^S, the allocation
y_i = Σ_{S∋i} λ_S y_i^S is feasible for N and concavity gives Σ_i u_i(y_i) ≥ Σ_S λ_S v(S), so v(N) ≥ Σ λ_S v(S): the
game is (totally) balanced and the TU core is nonempty. *NTU:* every competitive allocation is unblocked (if S could
make all members strictly better with ω_S, each member's new bundle would cost more than its endowment at the
equilibrium prices, contradicting Σ y = ω_S), and a competitive equilibrium exists under continuous, convex,
monotone preferences with positive endowments; so the NTU core is nonempty (Scarf 1967 gives the same through
balancedness). *Optimistic selection* breaks this: an owner indifferent about a good may gift it to S, two
coalitions can each count the same worthless-to-its-owner good, and the core can be empty (§5).

**6.6 Counterexample to RE 6 (certified).** Three-player majority division (`dollar3`) under pess: v({i}) = 0,
v(pair) = 1, v(N) = 1, TU and NTU empty (balanced collection: the three pairs at ½, gap ½), and FMA(S) = 0 for
every coalition: a pair is decisive whether it moves first or second, and a singleton gets 0 either way. Emptiness
here comes from the incompatibility of decisive claims, not from timing. Under opt a singleton gains from moving
first (2/3 against 0), so this counterexample is pessimistic-selection only. *A second one inside the sweep
(analytic):* in an allocation game a coalition's payoff does not depend on who moves first (the complement keeps,
or under opt gifts its worthless goods, whatever the order; ties in S's favour), so FMA ≡ 0, and the opt
zero-weight instances give 84 certified TU-empty and 48 certified NTU-empty cases (two coalitions each count the same
gift). In the timing families (Cournot, public goods, LQ, Bertrand) every certified empty point (199) has some
coalition with FMA > 0 (§5), including the mixed-spillover LQ points whose γ-core is also empty.

**6.7 Lemma SMA and the symmetric bracket (proof; §3.4).** In a symmetric game the core is nonempty iff
v(s)/s ≤ v(n)/n for every s. If at every coalition's leader outcome the followers earn at least the leaders per
capita (follower dominance), the equal split is in the TU core (and the symmetric efficient profile in the NTU core
when it is symmetric). Conversely, emptiness implies a coalition whose leader outcome pays its members more per
capita than its followers. *Partial proof of RE 4:* in the symmetric linear-quadratic family with σ ≥ 0 the
symmetric leader stationary point has a ≥ b and a positive spillover, so follower dominance holds; the proof assumes
an interior, symmetric leader optimum and a concave induced problem (checked numerically on the grid).

**6.8 Counterexample to "negative spillovers give emptiness" and to "the γ-core is always nonempty" (certified).**
With strategic complements and uniformly negative spillovers (σ ≤ −γ·x_max) no point of the grid is empty (643);
emptiness appears only when spillovers have mixed signs across players (σ = −0.25, −0.5 with heterogeneous b), via
pairs or two-block partitions, and at 13 of those 15 points the simultaneous-partition (γ) core is empty as well
(unique equilibria). That is a coalition-size effect (partial coalitions that internalize part of a mixed-sign
externality are worth more, in balance, than the grand coalition), not a timing effect.

**6.9 Open (no proof).** (a) Nonemptiness for asymmetric supermodular games with aligned spillovers (sweep: 0 empty of
1,423 positive or negative points, TU and NTU). (b) Public goods: emptiness iff the singleton partition violates
(true on all 1,820 points, unproven); for f = 2√G the singleton inequality holds by AM–GM for n ≥ 3 but the full core
is not proved. (c) Cournot TU emptiness beyond the proven window (h up to 0.325 at n = 3). (d) The 40 unresolved
mixed-spillover NTU cases and 127 opt allocation NTU cases.

## 7. Characterization

**Exact (TU).** The leader-value core is nonempty iff Σ_S λ_S v(S) ≤ v(N) for every balanced collection
(Bondareva–Shapley); for symmetric games iff v(s)/s ≤ v(n)/n for every s.

**Sufficient (symmetric, proved):** follower dominance at every coalition (Lemma SMA). It holds whenever the leader's
distortion helps its followers: strategic complements with spillovers of one sign (proved for symmetric LQ; 288/288
symmetric LQ points and all symmetric Bertrand points). **Necessary (symmetric, proved):** some coalition's leader
outcome pays its members more per capita than its followers.

**Empirical map (the sweep).** Three distinct routes to emptiness, and the RE's conjecture covers only the first:
1. *Timing on unowned surplus (substitutes).* Every player's Stackelberg or free-ride claim, summed over the singleton
   partition, exceeds the grand surplus; the γ-core stays nonempty. It needs heterogeneity or curvature: symmetric
   linear Cournot is a knife edge (tight), square-root public goods are never empty for n ≥ 3, and the violations
   are small in Cournot (≤ 1% of v(N)). Without transfers it is the rule rather than the exception (Cournot NTU
   empty on 0.82–0.94 of the grid, and at every two-firm point with 0 < c₂ < ½): the frontier cannot pay an inefficient
   firm its leader value without keeping it in production.
2. *Coalition size (mixed-sign externalities).* Pairs or blocks are worth more in balance than the grand coalition;
   the γ-core is empty too. Timing is not the cause (though some coalition still has FMA > 0).
3. *Incompatible claims without timing.* Majority division (decisive pairs, pess) and gifts counted twice
   (allocation games, opt): FMA ≡ 0 and the core is empty.

Nonempty classes: complements with aligned spillovers (differentiated Bertrand, LQ positive and uniformly negative),
owned endowments with "keep" (allocation games under pess: TU by Shapley–Shubik, NTU by competitive equilibrium),
homogeneous Bertrand. **Reading of the RE's conjecture:** "existence where every leader value is bounded by a held
default" is confirmed for owned endowments and for aligned complements; "failure where unowned surplus is claimed
by moving first" is a necessary-style tendency, not a criterion (symmetric Cournot and square-root public goods have
unowned surplus and nonempty cores); and failure also occurs without unowned surplus or timing (routes 2 and 3).
In the timing families, first-mover advantage is necessary for emptiness (199/199); in general it is not (RE 6).

## 8. Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 (revised) | symmetric Cournot nonempty for every n; NTU empty somewhere at n ≥ 3 with asymmetric costs | **held** (tight at every n, proved; NTU empty on 0.91 / 0.94 of the n = 3 / 4 grid, and at every asymmetric n = 2 point, proved); TU also empty on 0.03 / 0.05 |
| RE 2 | differentiated Bertrand nonempty | **held** (332/332, TU and NTU) |
| RE 3 (revised) | public goods empty on a substantial share, free-riding leadership violating | falsifier did not fire; **share clause failed** (0.041 pooled over n = 3–5 and f against the 0.25 scoring line; 0 under 2√G and CRRA ½); free-riding clause held (85/85, singleton partitions) |
| RE 4 | supermodular positive spillovers nonempty with a proof; negative spillovers empty somewhere | positive clause **held** (780/780 TU and NTU; partial proof, symmetric); **negative clause failed** on the negative class (0/643); emptiness occurs only with mixed-sign spillovers (15/137), as a coalition-size effect |
| RE 5 | continuous allocation games nonempty | **held** (800/800 certified, TU and NTU; proof); fails under opt with zero weights (not the claim) |
| RE 6 | some coalition's first-mover advantage necessary for emptiness | **falsified** (majority division under pess; allocation games under opt, FMA ≡ 0); holds within the timing families (199/199) |
| S1 | symmetric Cournot closed form, tight, NTU single profile | held |
| S2 | Cournot TU: n = 2 never empty; band at n = 3, 4 by singletons; onset h\*; share 0.05–0.7 | held except the **share clause at n = 3 (0.030 < 0.05)** |
| S3 | Cournot NTU empty at every 0 < c₂ < ½ (n = 2); NTU ≥ TU share, ≥ 0.5 at n = 3, 4 | held (proved for n = 2) |
| S4 | Bertrand TU nonempty, NTU ≥ 0.9, second-mover advantage for every coalition at symmetric points | TU, NTU and follower dominance held; **the FMA clause failed** (coalitions of size n − 1 gain from leading at n ≥ 3) |
| S5 | homogeneous Bertrand nonempty | held |
| S6 | public goods: curvature decides; sqrt never empty n ≥ 3; log n = 2 threshold 1.63; log n = 3 share 0.03–0.5; non-increasing in n; ρ = 2 ≥ log; free riders in every collection | held |
| S7 | γ-core nonempty at every generic point | **failed** (13 mixed-spillover LQ points) |
| S8 | LQ: σ ≥ 0 nonempty TU and NTU; symmetric points nonempty with dominance; negative ≥ 0.9 | held |
| S9 | allocation games pess nonempty; some opt zero-weight instance empty | held |
| S10 | coordinated followers empty symmetric Cournot n ≥ 3, enlarge public-goods emptiness; pess = opt off ties | held |
| S11 | majority division pess: empty with FMA ≡ 0; inside the families every empty point has FMA > 0 | first clause held; **second clause failed** (allocation games under opt) |
| S12 | symmetric bracket | held (no violation) |
| S13 | catalogue reproduced | held |
