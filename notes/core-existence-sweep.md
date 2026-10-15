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
