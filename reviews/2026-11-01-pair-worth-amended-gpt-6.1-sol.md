# Review of `specs/2026-11-01-pair-worth.md` by gpt-6.1-sol

1. **Errors and unsound mechanisms**
   - **Bid semantics are underspecified.** “If both others provably bid σ” is not the action predicate later specified as “conjunctions of two atoms.” Recognizing a named family and proving its output are different mechanisms, especially for K’s priority override. K also says “pair with j” without resolving two eligible partners; A has the same ambiguity. **Fix:** write explicit modal action equations, partner priorities, and tie rules; validate mixed σ triples, K³, incompatible bids, and constants mimicking bid outputs—not just homogeneous handshakes.
   - **Continuous and grid claims conflict.** “The core is externally stable, hence the unique stable set” conflicts with “a one-step ring … and some wasteful splits are also undominated.” Every undominated outcome must belong to any externally stable set. **Fix:** distinguish the continuous theorem from each grid’s actual target; do not describe core-only convergence as selection of the grid’s unique stable set.
   - **Catalogue arithmetic survived the amendment incorrectly.** “G⅚ … only the equal split” conflicts with “39 + 2·273 = 585 programs.” With one σ and 39 fallbacks, there are 39 bids and 39 blockers: **117 programs**, before merging duplicates. **Fix:** regenerate catalogue sizes, memory estimates, and timing budgets.

2. **Design flaws and confounds**
   - **The scoring cannot test the stated conjecture.** “Every core point appears with positive probability” is not falsified by “a core point unobserved” in finitely many runs. Choosing “the arm that holds it best” also introduces post-selection. **Fix:** preregister a primary arm; report simultaneous frequency bounds and coverage curves. Score absence only against a prespecified minimum probability, not positivity.
   - **Majority triples can conceal the mechanism.** A majority program need not exceed 50%; its triple may poorly represent encounters in polymorphic islands. **Fix:** retain majority classification but also report exact encounter-weighted outcome probabilities, program concentration, and mixed-state occupancy.
   - **There is effectively no easy-case large-N test.** N = 200 is restricted to the hard case, although neutral entry, drift, and claimed absorption are central to the easy-case conclusion. **Fix:** add matched G⅓ C/C+B runs at two larger N, specifying horizon and tail scaling; otherwise label conclusions finite-N.

3. **Predictions likely wrong**
   - “Grand-split islands reached by bids should be absorbing” is too strong. On a homogeneous σ island, its matching ALL constant is on-path identical and can drift in; later substitutions can destroy coordination. Finite Moran populations also permit disadvantageous fixation. **Prediction:** long-lived grand states, not absorption; measure escape hazards from deliberately initialized grand islands.
   - “Cycling, not absorption” is not established by bidirectional switches or intermediate occupancy. With a cut-off tail, reversible metastable switching and finite transients are plausible. **Prediction:** transition rates depend strongly on residual family supply; genuine recurrent cycling remains unestablished.

4. **Missing controls or cheap additions**
   - Initialize pure pair and grand islands; introduce one bid/blocker, then a second in another slot. Measure neutrality, establishment probabilities, and escape times directly.
   - Add a matched non-reading coordination control and equal-total-special-program-mass controls: C+B+K otherwise doubles the special-family dose.
   - Test slot-permutation invariance; index-based rounding can bias coverage.

5. **Alternative explanations**
   - Apparent core selection may reflect the hand-seeded core-only bid menu, rather than dominance.
   - Grand occupancy may reflect abundant coordination devices and founder sorting, not provability specifically.
   - Reported switching may be migration-driven majority turnover, not local neutral-then-selected invasion.
