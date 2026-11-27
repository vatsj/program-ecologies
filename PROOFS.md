# PROOFS.md — statements marked "proved", with the proof or a pointer

Kept by the RE (RS, 2026-11-15: the operating-hypotheses doc says only "proved"; the proofs live here). Add an entry
whenever a statement is marked proved anywhere. Dominance is strict unless said.

## Static theory (Theory tab)

**P1. The boundary at ½** (pair-worth-a game, continuum, splits of the dollar). The core dominates every split
outside it in one step iff a ≤ ½.
*Proof.* A split y outside the core has some y_k > 1 − a, so the pair {i, j} gets less than a. A core outcome
dominates y through {i, j} only by giving that pair exactly a and k exactly 1 − a, with i and j each strictly above
their shares in y and at most 1 − a. That is possible iff y_i and y_j are both below 1 − a. At a ≤ ½ this always
holds for a short pair: two shares of at least 1 − a ≥ ½ would leave nothing for the third. At a > ½ it fails for
y = (t, 1 − 2t, t) with t in (1 − a, ½]: both short pairs contain a player above 1 − a. ∎

**P2. Core and stable sets** (classical). The core lies inside every stable set; if the core is externally stable
it is the unique stable set.
*Proof.* A core outcome is dominated by nothing, so external stability can only be met by putting it in V. The core
is internally stable; if it also dominates everything outside it, any extra outcome in V would be dominated by a
core member, which internal stability forbids. ∎

**P3. V\* is a stable set of majority division** (V\* = the three fair pairs).
*Proof.* Internal: moving from (½, ½, 0) to (½, 0, ½) needs player 1 to gain, and she is indifferent, so no fair
pair dominates another. External: any outcome outside V\* leaves at least two players below ½ (if only one were
below, the other two would hold ½ each and the outcome would be a fair pair); those two take their fair pair and
both gain strictly. ∎

**P4. Stable sets and Pareto efficiency.** No member of a stable set is strictly Pareto-dominated by a feasible
outcome. Under weak dominance every member is Pareto efficient.
*Proof.* Let y be in V and x a strict Pareto improvement on y. Then x dominates y through the grand coalition, so x
is not in V. By external stability some z in V dominates x through some coalition S. Then z gives S more than x
does, and x gives S more than y does, so z dominates y through S, contradicting internal stability. Under weak
dominance the same argument runs with ≥ and one strict gain. ∎

**P5. Shrinking preserves (strong) Nash.** If a profile is a (strong) Nash equilibrium of G, it is one of any
restriction of G that still contains it (actions removed, or players frozen at their equilibrium actions).
*Proof.* Every deviation available in the restriction is available in G. ∎ (So strong Nash technologies satisfy
the tab's independence of irrelevant alternatives and subgame-perfection.)
Remark (2026-11-27; `src/iia_examples.py`). P5 is about the game whose actions are removed. Read as technologies on
the *base* game, neither program equilibrium nor the leader-value core is independent of irrelevant base actions.
Player 1 has P, A; player 2 has Acc, C, F; payoffs (P,Acc) = (2,3), (P,C) = (0,0), (A,Acc) = (3,0), (A,C) =
(2.5,2.5). (i) With (P,F) = (0.5,−1), (A,F) = (0,3): the leader-value core is {(P,Acc), (A,C)}; F is in neither,
and it is player 2's best reply to a commitment to A. Without F the reply to A is C, player 1's leader value rises
from 2 to 2.5 and (P,Acc) is blocked. (ii) With (P,F) = (A,F) = (−5,−5): the strong Nash outcomes in program space
(punishers answering the deviator's action) are (P,Acc), (A,Acc), (A,C); F is in none and is the threat that holds
player 1 to P. Without F, (P,Acc) is lost. In (ii) the leader-value core is {(A,C)} with or without F: it uses only
followers' best replies, so a threat that hurts the threatener is not available to it.

### Strong Nash in program space and the two cores (2026-11-23; sound on-path reading, "case 3")

Setting: G a finite game in pure actions. y ≫_S a means every member of S is strictly better off at y than at a.
A nonempty coalition S **α-blocks** a if ∃x_S ∀b_{N∖S}: (x_S, b) ≫_S a, and **β-blocks** a if ∀b_{N∖S} ∃x_S:
(x_S, b) ≫_S a (for S = N both say a is strictly Pareto-dominated). The α-core (β-core) is the set of outcomes no
coalition α-blocks (β-blocks); an α-block is a β-block, so β-core ⊆ α-core. A program game is (P, o): program sets
P_i and a total outcome map o from profiles to action profiles. A profile p is strong Nash if no S and q_S give
o(q_S, p_{−S}) ≫_S o(p) (deviation without response).

**P6. Upper bound, always.** If P contains the constants (for each x_i a program that plays x_i in every profile),
every strong Nash outcome is in the α-core.
*Proof.* Let p be strong Nash with outcome a and suppose S α-blocks a with x_S. Let S deviate to the constants x_S.
The outcome is (x_S, b) for some b, and (x_S, b) ≫_S a for every b. Contradiction. ∎

**P7. Lower bound under exposure.** Axiom E: for every a and every plan (b^D), one b^D ∈ A_{N∖D} for each nonempty
D ⊊ N, there is a profile p with o(p) = a such that after any deviation q_S the outcome y is either a, or satisfies
y_{N∖D} = b^D for some nonempty D ⊆ S (the exposed deviators; D = N allowed, with no condition). Under E every
β-core outcome is a strong Nash outcome.
*Proof.* Let a be in the β-core. For each nonempty D ⊊ N, D does not β-block, so there is b^D with no x_D giving
(x_D, b^D) ≫_D a. Take the profile of axiom E for this plan. After a deviation by S: if y = a nobody gains; if
D = N then S = N and y ≫_N a is excluded because N does not block; otherwise y = (y_D, b^D), some member of D is
not strictly better off, and D ⊆ S. ∎

**P8. Upper bound when deviators read last.** Axiom R: for every profile p, coalition S and map f from A_{N∖S} to
A_S there is q_S whose outcome has the form (f(y), y). Under R every strong Nash outcome is in the β-core.
*Proof.* If S β-blocks a = o(p), let f(b) be an x_S with (x_S, b) ≫_S a and take q_S from R. ∎
So under E and R the strong Nash outcomes are exactly the β-core.

**P9. Lower bound when punishers read actions.** Axiom T: as E, but the plan may depend on the exposed deviators'
actions, y_{N∖D} = b^D(y_D). Under T every α-core outcome is a strong Nash outcome, so with P6 the strong Nash
outcomes are exactly the α-core.
*Proof.* As P7, choosing b^D(x_D) with (x_D, b^D(x_D)) not ≫_D a, which exists because D does not α-block. ∎

*Remarks.* (i) T and R cannot both hold in a game whose α-core and β-core differ (pure matching pennies: every
outcome is in the α-core and none in the β-core): a language sits at one end or between, and which end is the
question of who reads whom. (ii) For two players with a private coin each, the minimax theorem makes a player's
maxmin and minmax values equal, so the two cores coincide and the question disappears; for three or more players
nothing is claimed. (iii) Which axioms the provability arm satisfies is not proved here. Checked by enumeration
(`notes/2026-11-23-case3-static.md`): on the catalogue at n = 5–9 axiom R holds, axiom T fails, and the strong Nash
outcomes of the PD, pure matching pennies and the separating game Q are the β-core.

### The tiered fixation lemma (2026-11-23; credibility as lexicographic best response)

Setting: one slot of one island, a Moran population of N individuals with fitness 1 − w + w·(expected payoff),
0 < w ≤ 1. The resident program p earns ū against the island's residents. A variant p′ earns ū + Δ₀ against them.
**Assumption A (tester field):** independently in each encounter, the partner in some other slot is a tester of type
q with probability ε_q = m_q·T_q / N (m_q arrivals of q per generation, T_q the expected copy-generations one
arrival's lineage lives), the field is stationary and does not depend on how many variants there are, and encounters
with two testers are neglected. Δ_q is the variant's payoff minus the resident's in an encounter with q.

**P10.** Under A the variant's relative fitness is r = 1 + w(Δ₀ + Σ_q ε_q Δ_q)/f, f = 1 − w + wū, and its fixation
probability from one copy is ρ = (1 − 1/r)/(1 − r^(−N)) (ρ = 1/N if r = 1).
(i) If Δ₀ > 0, ρ → 1 − 1/r₀ > 0 as N → ∞, and if Δ₀ < 0, Nρ → 0 exponentially in N, whatever the testers
(r₀ = 1 + wΔ₀/f).
(ii) If Δ₀ = 0 (the variant is on-path equivalent), Nρ → σ/(1 − e^(−σ)) as N → ∞, with
σ = (w/f)·Σ_q m_q T_q Δ_q; this is above 1 iff σ > 0, below 1 iff σ < 0, and does not depend on N.
(iii) Split the testers into migrants and mutants, σ = σ_mig + σ_mut. As the migration dose grows with the mutation
dose fixed, Nρ → ∞ if Σ_mig m_q T_q Δ_q > 0 and Nρ → 0 if it is < 0; if it is exactly 0, Nρ = σ_mut/(1 − e^(−σ_mut)).
*Proof.* Expected payoffs are linear in the partner's type, so under A every variant has the same constant fitness
f + w(Δ₀ + Σε_qΔ_q) and every resident f; the Moran process with constant relative fitness r has the stated ρ
(the gambler's-ruin formula). (i) r → r₀ ≠ 1 since ε_q = O(1/N). (ii) r = 1 + σ/N, so r^(−N) → e^(−σ) and
N(1 − 1/r) → σ. (iii) from (ii), since x/(1 − e^(−x)) → ∞ as x → ∞ and → 0 as x → −∞. ∎

*Reading.* Selection orders a program's rivals lexicographically: first by payoff against the island's natives (at
strength N), then against migrants (at strength of the migration dose), then against the mutation prior (at
strength of the tail's dose). The order is exact only in the limit where the three strengths are well separated;
at finite doses each lower tier is a bias factor σ/(1 − e^(−σ)), not a filter. *Not proved:* assumption A for the
object (tester lineages are real individuals whose own fate depends on the mix of residents and variants); for a
tester selected against at relative fitness r_q < 1, T_q = 1/(1 − r_q). At a world in consensus migrants are
natives, Δ_q = 0 for every migrant, and the migrant tier is empty.

**P11 (factored technologies are equipotent; 2026-11-23, the RS's definitions).** Let A = A_1 × … × A_n be a product
set of programs every profile of which is a Nash equilibrium in program space. Then (i) A is weakly equipotent:
u_i(p_i, p_−i) = u_i(p_i′, p_−i) for all p_i, p_i′ ∈ A_i. (ii) If n = 2, every profile of A is also Pareto efficient
and the Pareto frontier of the feasible set is strictly decreasing (no flat segment), then A is strongly equipotent:
payoffs are constant on A.
*Proof.* (i) (p_i, p_−i) and (p_i′, p_−i) are both in A, so both are Nash, so each of p_i, p_i′ is a best reply to
p_−i; best replies earn the same. (ii) By (i) u_1 depends only on p_2 and u_2 only on p_1. On a strictly decreasing
frontier u_2 = φ(u_1) with φ injective, so g(p_1) = φ(f(p_2)) for all p_1, p_2, hence both are constant. ∎
Remarks. Battle of the sexes has two maximal strongly equipotent factorizations and no factored technology
containing both outcomes: the cross profiles would pay (1,1), dominated, and (2,2), infeasible. With n ≥ 3 weak
without strong is possible (a player's choice can move payoff between the others). Not proved: anything about
maximal factorizations in general.

**P12 (two players with coins: strong Nash is nonempty; 2026-11-23).** Setting: G a finite two-player game. The
machine gives each player a private coin (its draw unseen by the other player's program) and programs read each
other's source; a program may test whether its partner's source is a given text. Payoffs are expectations. Let
m_i = min over mixed actions σ_j of max over a_i of u_i(a_i, σ_j) (i's mixed minmax value), attained at σ_j\*. Let
Π be the set of payoff vectors of product distributions σ_1 × σ_2, and F ⊇ Π the convex hull of the pure payoff
vectors (what a public coin adds). Strong Nash: no single player and no pair can switch programs and make every
switcher strictly better off in expectation, the other program staying as written.
(i) With private coins only, the program game has a strong Nash profile. (ii) With a public coin as well, every
x ∈ F with x_i ≥ m_i for both i that is not strictly Pareto-dominated in F is a strong Nash payoff, and such x exist.
*Proof.* Take W = Π for (i) and W = F for (ii); W is compact and is exactly the set of payoff vectors any pair of
programs can produce (programs cannot see each other's private draws, so without a public coin the joint action
distribution is a product; with one it is a mixture of products). Let R = {x ∈ W : x_i ≥ m_i, i = 1, 2}. R is
nonempty: a Nash equilibrium (σ_1, σ_2) of the mixed extension exists, its payoff is in Π ⊆ W, and
u_i = max_{a_i} u_i(a_i, σ_j) ≥ m_i. R is compact, so some x ∈ R maximizes x_1 + x_2; no y ∈ W has y ≫ x, since
such y would lie in R with a larger sum. Let x be the payoff of the distribution D (a product in (i), a public-coin
mixture of products in (ii)). Programs: p_i plays its part of D if the partner's source is the text of p_j, and
otherwise plays σ_i\* on its private coin. The profile pays x. A single deviator i faces σ_j\* drawn on a coin it
cannot see, so it earns at most max_{a_i} u_i(a_i, σ_j\*) = m_i ≤ x_i: no strict gain. A joint deviation pays some
y ∈ W, and y ≫ x is excluded. ∎
Remarks. (a) Without coins the claim fails: in pure matching pennies each player's pure minmax is the winning payoff
(the deviator reads the punisher), R is empty and there is no strong Nash profile (enumeration,
`notes/2026-11-23-case3-static.md`). (b) The public coin is not needed for existence; it enlarges the set of strong
Nash payoffs from Π to F. (c) The construction identifies the partner by its text, so the supporting profile is an
identity pair; it shows existence, not openness. (d) The punishment σ_j\* may cost the punisher; nothing here says
it is a best reply to the deviator. (e) Two players only: with three, a pair's private coins and the third's reads
change the blocking sets (`notes/2026-11-23-three-players-coins.md`).

**P13 (the maximal strong Nash technology is Maskin monotonic; 2026-11-25).** Let G and G′ have the same players
and action (program) spaces. Let x be strong Nash in G under strict dominance, and suppose that for every player i
and every profile y, u_i(x) ≥ u_i(y) in G implies u′_i(x) ≥ u′_i(y) in G′. Then x is strong Nash in G′. The same
holds for Nash (singletons only), and for any fixed family of coalitions allowed to object.
*Proof.* If S objects to x in G′ through y (y_{−S} = x_{−S}, u′_i(y) > u′_i(x) for all i in S), the contrapositive
of the hypothesis gives u_i(y) > u_i(x) in G for all i in S, so S objects in G. ∎
Corollaries: x-improvement (raising only x's payoffs keeps x); lowering payoffs away from x keeps x; invariance
under any increasing transform of one player's payoffs in the pure case, and under positive affine transforms when
payoffs are expectations over coins.
Not monotone: (a) under weak dominance (nobody worse, somebody better) the claim fails: two players, x = (a, a),
y = (b, b), off-diagonal profiles worst for both; in G player 1 strictly prefers x and player 2 strictly prefers y;
in G′ player 1 is indifferent. The hypothesis holds, x is unblocked in G and weakly blocked by the pair in G′.
(b) The technology can gain members under such a change (nothing here bounds it above). (c) A selection from it
(e.g. the largest factorization) need not be monotonic, since the change can add strong Nash profiles elsewhere.
(d) Enlarging the action or program space can remove members (new deviations); shrinking keeps them (P5).
(e) **With coins the claim holds only if the hypothesis ranges over lotteries** (y any profile, u expected payoff).
Under Maskin's hypothesis on pure outcomes it fails (the RS's prediction, 2026-11-25: x-improvement but not Maskin).
Example: two players, x pays (1, 1). If player 1 deviates, player 2 can answer c1 or c2, and player 1's payoffs
against (c1, c2) are (3, −10) from one deviation and (−10, 3) from the other; player 2 is indifferent throughout.
In G the ½–½ punishment holds player 1 to −3.5 < 1, so x is strong Nash (P12's construction). G′ raises the two
−10s to ½. Every comparison of x with a pure outcome is unchanged (x is still above them, and still below the 3s),
but player 1's minmax value is now 1.75 > 1, so no program profile supports x. x-improvement survives coins when x
is a pure outcome: raising x's payoffs by Δ raises the equilibrium payoff by Δ and any deviation's by at most Δ.
(f) **In expected value Maskin's hypothesis is rescaled x-improvement.** For a pure outcome x and player i write
v(y) = u_i(y) − u_i(x), v′(y) = u′_i(y) − u′_i(x). Then "x ≥ L in G implies x ≥ L in G′ for every lottery L over
outcomes" holds iff there is λ ≥ 0 with v′(y) ≤ λ·v(y) for every outcome y.
*Proof.* If v′ ≤ λv then v′·L ≤ λ v·L ≤ 0 whenever v·L ≤ 0, L ≥ 0. Conversely the linear program
max v′·L subject to v·L ≤ 0, L ≥ 0 has value 0, so its dual is feasible: some λ ≥ 0 has λv ≥ v′. ∎
So with coins the lottery form of Maskin says only: measured from x and up to a positive rescaling, every other
outcome got weakly worse for every player. That is x-improvement together with affine invariance, and the maximal
strong Nash technology satisfies it by the proof of P13 read over lotteries.

**P14 (Condorcet winners; 2026-11-27).** Setting: an odd number n of voters with strict preferences over a finite set
of alternatives; a voting game in which any strict majority that votes unanimously for z makes z the outcome
whatever the others do (plurality with any tie rule is one). Let x be the Condorcet winner if there is one (x beats
every other alternative by a strict majority). Under strict dominance:
(i) the α-core and the β-core are both {x} if x exists and empty otherwise;
(ii) the strong Nash outcomes of the voting game, and of any program game over it that contains the constants, are
exactly {x} if x exists and none otherwise;
(iii) the leader-value core, with followers replying by a strong Nash profile of their induced game and a
commitment after which no such profile exists forcing nothing, is {x} if x exists and empty otherwise;
(iv) if x exists, {x} is the unique stable set.
*Proof.* A minority can force nothing: the majority outside it can vote unanimously. A majority M can force any z
outright. So an outcome y is α- or β-blocked iff some majority strictly prefers one alternative to y, which gives
(i). (ii): "all vote x" is strong Nash, since a deviating minority leaves x with a majority and a deviating majority
would have to prefer another alternative to x; any outcome y ≠ x is left by the majority that prefers x; in program
space the upper bound is P6 and the constants "vote x" give the same equilibrium. (iii): if x exists and y ≠ x, the
majority preferring x leads by voting x and forces {x}. Conversely suppose S leads and some follower strong Nash
outcome y is preferred to x by all of S; the majority M that prefers x to y contains no member of S, so M lies
among the followers and can switch to voting x, which makes x the outcome whatever S committed; so y was not a
strong Nash outcome of the followers' game. Hence nothing objects to x. With no Condorcet winner every y is left by
a majority acting as leader. (iv): x dominates every y through the majority preferring it, so the core is
externally stable (P2). ∎
Remarks. All these notions agree here because majority rule is tight (α = β) and a winning coalition's power does
not depend on replies; the benchmark cannot tell them apart. Not covered: even n or indifference (weak Condorcet
winners), and the reading of the leader-value equilibrium that needs a rational reply after *every* commitment,
which needs a strong Nash profile in every followers' subgame.

**P15 (existence of the leader-value core in terms of forcing; 2026-11-27; `notes/2026-11-27-forces-existence.md`).**
Finite game in pure actions, strict dominance. After a commitment a_S, a *sink* is a minimal nonempty set of
follower profiles closed under strictly improving moves by follower coalitions; S *forces* a_S × K for each sink K.
Write g_i(S, B) = min over B of u_i. An outcome x is in the core iff for every forced (S, B) some member i of S has
u_i(x) ≥ g_i(S, B), and no outcome is strictly better for everyone.
(a) Every coalition forces something after every commitment (a finite improvement graph has a terminal component).
(b) Two players: the core is nonempty iff some outcome x has u_i(x) ≥ v_i for both i, where v_i is the largest
g_i({i}, B) over the sets i forces (i's best leader payoff).
(c) Any number of players (Scarf 1967 applied to V(S) = {z : z ≤ g(S, B) for some forced B}): if for every balanced
collection of coalitions and every choice of a forced set B_S for each of them there is an outcome x with
u_i(x) ≥ the least g_i(S, B_S) over the chosen S containing i, for all i, then the core is nonempty.
*Proof.* (a) Follower profiles are finite, so the condensation of the improvement digraph has a node with no
outgoing edge. (b) If x meets both v_i, a Pareto-undominated outcome weakly above x exists and meets them too; no
single player forces a set strictly better than v_i, so it is in the core. Conversely a core outcome x has
u_i(x) ≥ g_i({i}, B) for every set i forces, since {i} has one member. (c) V(S) is nonempty by (a), closed,
comprehensive and bounded above; Scarf's theorem gives z in V(N) that no S can improve on within V(S); take x with
u(x) ≥ z; a domination of x by (S, B) would put g(S, B), strictly above z on S, in V(S). ∎
Checked on random games: (b) agrees in 20,000 of 20,000 two-player games; (c) has no counterexample in 22,000
three-player games but is far from necessary (it holds in about a quarter to a third of the games whose core is
nonempty).

## Proved elsewhere (pointers)

- Lemma D′, the scramble (any lineage, any stopping time): RESULTS "The demographic lemma".
- Establishment positive uniformly in the cutoff (μ_est ≥ 0.0207, modal arm): RESULTS "the tail in n".
- Lemma 0 (soundness buys unfakeability, Löb buys self-cooperation) and the sibling theorem (Conjecture 4):
  RESULTS "Conjecture 4: the sibling theorem".
- Universality and drift-closure are exclusive; β = ½; Proposition 3 (a price beats 1/N only through incumbency):
  RESULTS "Universality against drift-closure", THEORY §9.2.
- Corollary 1 does not bind at ε = 0: THEORY (Corollary 1), RESULTS "Almost all seeds?".
- V\* is the only stable set on every even grid; none on odd grids (Lemma G; by exhaustive search on the grids
  listed there, not a general proof): RESULTS "Stable sets on islands" and its addendum.
- Each member of V\* equally likely across worlds (rotation symmetry of game and prior): RESULTS "Arm T under
  islands to infinity before time".
- Refusing self-play production removes every self-play-only certificate: RESULTS "Provenance".
