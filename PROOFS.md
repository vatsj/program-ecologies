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
