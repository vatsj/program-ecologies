# Predictions: where does the leader-value core exist? (2026-10-14)

Spec `specs/2026-10-14-core-existence-sweep.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict). Committed before any code of this experiment and before any
family is computed. A static computation, no ecology: nothing here is about π, the lottery or evolutionary
accessibility (amendment 7).

*Provenance of the subagent's predictions.* They are informed by hand analysis done before this file (closed-form
leader values for linear Cournot with one cost deviation, the n = 2 Cournot NTU frontier to second order, symmetric
public goods with square-root, logarithmic and CRRA production, the symmetric linear-quadratic leader problem), not by
any computation of a family. The hand derivations go into `notes/core-existence-sweep.md` with the code check beside
them.

## Definitions fixed now (the notes restate them)

Game (N, A_i, u_i). For a coalition S ⊊ N and a commitment a_S, the complement C = N∖S responds by
- **individual** (default, the γ-convention): E_C(a_S) = the pure Nash equilibria of the complement subgame;
- **coordinated** (panel variant): E_C(a_S) = argmax over a_C of Σ_{j∈C} u_j.

Selection: **pess** (S faces the worst element of E_C(a_S)) and **opt** (the best). TU leader value
v(S) = sup_{a_S} min (pess) or max (opt) over E_C(a_S) of Σ_{i∈S} u_i; v(N) = max Σ_i u_i. TU core
{x : Σ x = v(N), x(S) ≥ v(S)}; the least-core value ε\* = max_x min_S (x(S) − v(S)) decides it:
**nonempty** ε\* ≥ 1e-9·scale, **tight** |ε\*| < 1e-9·scale (nonempty, a knife edge), **empty** ε\* ≤ −1e-9·scale.
Empty cases carry the dual's balanced collection (weights re-checked in exact rationals); nonempty cases carry the
least-core allocation and its minimum slack.

NTU: a profile a\* is blocked by S ⊊ N iff some a_S makes every member of S strictly better under every (pess) / some
(opt) element of E_C(a_S); by N iff some profile is strictly better for everyone. The NTU core is the set of unblocked
profiles (no transfers). Labels: **nonempty** (a profile with every blocking margin certified ≤ 0), **empty**
(certified by a branch-and-bound over profiles, or by the singleton bound Σ_i v({i}) > max Σ u, which implies NTU
emptiness), **unresolved** otherwise.

First-mover advantage (timing sense, RE 6): FMA(S) = v(S) − v_F(S), where v_F(S) is S's payoff at the outcome
realizing v(C) when C leads (ties among C's optimal commitments broken in S's favour). "S gains from moving first"
iff FMA(S) > 1e-9·scale. **Follower dominance** at S (a payoff comparison, not timing): at S's leader outcome the mean
payoff of C's members is at least the mean payoff of S's members.

Simultaneous-partition control (amendment 6): v_sim(S) = S's joint payoff in the pure Nash equilibrium of the game in
which S acts as one player (maximizing its sum) against the complement's members as singletons (the Chander–Tulkens
γ-worth); reported where that equilibrium is unique, with pess/opt bounds otherwise.

## Grids fixed now (shares below are over these)

- **Cournot**, p = 1 − Q, c₁ = 0 (scale normalization: costs enter only through a − c), the other costs sorted
  multisets from {0, 0.025, …, 0.5}: n = 2, 3, 4 (21, 231, 1,771 points; TU). NTU on the step-0.05 subgrid (11, 66,
  286). Capacity variant: common capacity k ∈ {0.1, 0.2, 0.3, 0.4}, costs from {0, 0.1, …, 0.5} with c₁ = 0, TU.
- **Bertrand, differentiated**: q_i = 1 − p_i + (g/(n−1)) Σ_{j≠i} p_j, g ∈ {0.2, 0.4, 0.6, 0.8}, c₁ = 0, others from
  {0, 0.1, …, 0.5}; n = 2, 3, 4. Points where some quantity would be negative at a computed outcome are excluded and
  counted. **Homogeneous**: demand 1 − p, lowest price serves the market, ties split equally, costs as Cournot's
  step-0.05 grid; leader values as suprema where the optimum is not attained (labelled).
- **Public goods**: u_i = θ_i f(G) − g_i, g_i ≥ 0, f ∈ {2√G, ln(1+G), CRRA ρ = ½: 2(√(1+G) − 1), ρ = 2: 1 − 1/(1+G)},
  θ sorted multisets from {0.5, 1, 1.5, 2, 3, 4}: n = 3, 4, 5 (56, 126, 252 per f); n = 2 (21 per f) added as an
  extension (not in the spec).
- **Supermodular (linear-quadratic)**: u_i = b_i x_i − x_i²/2 + γ x_i X_{−i} + σ X_{−i}, x_i ≥ 0,
  γ(n−1) ∈ {0.1, 0.2, 0.3, 0.4}, σ ∈ {−1, −0.5, −0.25, 0, 0.25, 0.5}, b sorted multisets from {0.5, 1, 1.5, 2};
  n = 2, 3, 4. Spillover class per point: positive (σ ≥ 0), negative (γ·x_max + σ ≤ 0 at every computed outcome),
  mixed otherwise.
- **Allocation games**: exchange economies, n = 3, 4, m = 2, 3 goods, Cobb–Douglas and CES (elasticities ½ and 2),
  50 random instances per (n, m, utility), seed fixed in the code; plus a zero-weight variant (some goods worthless
  to their owner) for the selection bounds.
- **Catalogue**: PD, chicken, hd3, hd6, `dollar5`, the SOG one-shot normal form, `dollar3` majority division.

## The RE's predictions (verbatim from the spec, with the revisions after review)

1. ~~Cournot empty for n ≥ 3 at every cost profile~~ [withdrawn after review by sol: with p = a − Q and common cost,
   a k-coalition leading against independent Nash followers gets v(S) = m²/(4(n − k + 1)), m = a − c, and the equal
   monopoly split gives each m²/(4n), which meets every coalition since k(n − k + 1) ≥ n; the core is nonempty for
   every n]. **Revised:** symmetric linear Cournot nonempty for every n (verified analytically first); with
   asymmetric costs, empty somewhere for n ≥ 3 in the NTU core (uncertain). *Falsifier:* nonempty on the whole
   asymmetric grid.
2. **Differentiated Bertrand (complements in prices): nonempty** (second-mover advantage caps leader values).
   *Falsifier:* empty at a positive share of the grid.
3. ~~Concave public goods nonempty~~ [withdrawn after review by gemini-4-argon: contributions are substitutes, a
   coalition leading by free-riding raises the complement's contributions, which is the conjecture's failure case].
   **Revised:** empty on a substantial share of the grid, with free-riding leadership the violating coalitions.
   *Falsifier:* nonempty everywhere.
4. **Supermodular with positive spillovers: nonempty, with a proof;** with negative spillovers, empty somewhere.
   *Falsifier:* empty for positive spillovers at some parameter.
5. **Continuous allocation games: nonempty for convex preferences** (the classical core by Scarf). *Falsifier:*
   empty at some parameter.
6. **The characterization, weakened** [after review by sol: timing advantage is not incompatibility of claims]:
   some coalition's first-mover advantage is necessary for emptiness, not sufficient; the sufficient condition is
   sought as a balancedness statement. *Falsifier:* one certified empty case in which no coalition gains from moving
   first.

*Scoring notes for the RE's predictions (fixed now).* RE 1 is scored on the TU and the NTU core separately (the
revised text names NTU); "symmetric nonempty" includes "tight". RE 2's "positive share" = any certified empty point
on the differentiated grid (TU or NTU, reported separately). RE 3's "substantial share" is scored as ≥ 0.25 of the
public-goods grid at n ∈ {3, 4, 5} pooled over f (TU), and its second clause as: every empty point's violating
collection contains a coalition whose leader commitment is zero contribution while the complement contributes. RE
4's positive clause is scored on σ ≥ 0, its negative clause on the negative class (and on the mixed class reported
beside it). RE 5 on pessimistic selection (the RS's allocation games have strictly increasing utilities except in
the zero-weight variant). RE 6 on every family *and* the catalogue, under each selection.

## The subagent's predictions

S1. **Symmetric Cournot, closed form.** For n = 2, 3, 4 (and the analytic statement for every n): v(S) =
m²/(4(n − |S| + 1)), the TU core is the single point (m²/(4n), …) with every singleton constraint binding (verdict
"tight"), and the NTU core is the single profile q_i = m/(2n). *Falsifier:* any other verdict or core.

S2. **Cournot TU with asymmetric costs.** Nonempty at every n = 2 point (strict slack when c₂ > 0). Empty on a band of
moderate asymmetry at n = 3 and 4, certified by the singleton partition; along the ray c = (0, …, 0, h) emptiness
starts at h\* = 2n/((n+1)²(n−1) + 1) (0.182 at n = 3, 0.105 at n = 4). Empty share between 0.05 and 0.7 at n = 3 and
at n = 4. *Falsifier:* an empty n = 2 point; no empty point at n = 3 or at n = 4; the onset along the ray off by more
than one grid step; or an empty point whose only violating collections exclude the singleton partition at every
dual optimum (reported, not a falsifier for the band itself).

S3. **Cournot NTU.** At n = 2 the NTU core is empty at every grid point with 0 < c₂ < ½ (a second-order effect: the
singleton leader values move outward at second order in c₂ while the no-transfer frontier moves inward), nonempty at
c₂ = 0 and c₂ ≥ ½. The NTU-empty share is at least the TU-empty share at every n and is ≥ 0.5 at n = 3 and n = 4.
*Falsifier:* a certified nonempty n = 2 point with 0 < c₂ < ½; NTU share below TU share at some n; NTU share < 0.5 at
n = 3 or 4.

S4. **Differentiated Bertrand.** TU nonempty at every included point; NTU nonempty on ≥ 0.9 of included points;
every coalition at every symmetric point has a second-mover advantage (FMA < 0) and follower dominance. *Falsifier:*
any certified TU-empty point; NTU-nonempty share < 0.9; a symmetric point with FMA ≥ 0 for some proper coalition.

S5. **Homogeneous Bertrand.** Nonempty at every point (TU and NTU): v(S) = 0 whenever C contains a firm with cost
≤ min_S c, and giving everything to the lowest-cost firm is in the core. *Falsifier:* any empty point.

S6. **Public goods (TU), curvature decides.** Under f = 2√G: nonempty at every n ≥ 3 point (n = 2 symmetric is tight);
under ln(1+G): n = 2 symmetric is empty iff θ > 1/(2(1 − ln 2)) ≈ 1.63; at n = 3 the empty share is between 0.03 and
0.5 and is concentrated where the two largest valuations are large and close; the empty share is non-increasing in n
(n = 3 ≥ 4 ≥ 5) for each f; ρ = 2 is empty on at least the log share at every n. Every violating collection contains
a free-riding coalition (zero contribution, complement contributing). *Falsifier:* any empty sqrt point at n ≥ 3; log
share at n = 3 outside [0.03, 0.5]; a strict increase in n for some f; a violating collection with no free-riding
coalition at some dual optimum.

S7. **The timing control.** The simultaneous-partition (γ) core is nonempty at every generic point (unique
equilibrium) of every family; so every leader-core emptiness in the sweep is a timing effect, not a coalition-size
effect. Under public goods this is the Chander–Tulkens/Helm γ-core (the game maps to their emissions game with linear
benefits and convex damages). *Falsifier:* an empty γ-core at a generic point of any family.

S8. **Supermodular (LQ).** TU and NTU nonempty at every σ ≥ 0 point; at every symmetric point (all b equal) nonempty for
every σ, with follower dominance at every coalition (the "aligned distortion" lemma in the notes: the leader distorts
in the direction its spillover favours the followers). Negative-spillover asymmetric points: TU nonempty on ≥ 0.9.
*Falsifier:* any empty σ ≥ 0 point (TU or NTU); an empty symmetric point; negative-class TU-nonempty share < 0.9.

S9. **Allocation games.** Under pessimistic selection both the TU and the NTU (classical) core are nonempty in every
instance, the NTU certificate being the competitive allocation, unblocked by every coalition. In the zero-weight
variant under optimistic selection (an owner gifts a good it does not value), at least one instance is empty.
*Falsifier:* any empty pessimistic instance; no empty optimistic zero-weight instance.

S10. **Factorial panel.** Coordinated followers (the complement as one coalition) make symmetric Cournot TU-empty at
n ≥ 3 (a singleton leader then faces one merged follower: m²/8 > m²/(4n)) and enlarge the public-goods empty set;
pess vs opt differs only at ties (symmetric public goods, homogeneous Bertrand, the SOG, majority division).
*Falsifier:* symmetric Cournot nonempty under coordinated followers at n = 3; a pess/opt difference at a point
without ties in E_C.

S11. **RE 6 on the controls.** Under pessimistic selection three-player majority division is TU- and NTU-empty with
FMA(S) = 0 for every coalition, so RE 6's falsifier fires on the catalogue; inside the sweep's families every
certified empty point has some coalition with FMA > 0. *Falsifier:* some coalition with FMA > 0 in pessimistic
majority division; a certified empty family point with no FMA > 0.

S12. **Symmetric bracket (theorems, checked as implementation consistency).** In every symmetric family point
(i) if follower dominance holds at every proper coalition the core is nonempty, and (ii) if the core is empty, some
violating coalition's leader outcome pays its members more per capita than the followers. *Falsifier:* any
symmetric point violating (i) or (ii) (would mean a code error, since both are proved in the notes).

S13. **Catalogue reproduced exactly:** PD exists uniquely at (C, C); chicken, hd3, hd6 and `dollar5` empty; the SOG
one-shot NTU core is {(0, work)} under ties for the leader and {(0, work), (¼, work)} under ties against, never ½;
majority division empty. *Falsifier:* any difference.

Uncertain (the subagent's list): S2's share band, S3's n ≥ 3 share, S6's log share, S7 for asymmetric Cournot (γ-core
results for asymmetric linear Cournot are not something I can state from memory), S8's negative clause, S10's
public-goods clause.
