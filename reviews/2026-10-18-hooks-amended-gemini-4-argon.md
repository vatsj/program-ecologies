# Review of `specs/2026-10-18-hooks.md` by gemini-4-argon

**1. Errors, contradictions, and unsound mechanisms**

*   **FIFO thrashing under mutual-cooperation writes:** Amendment 1 states a program "carries at most 4 fills (FIFO eviction beyond 4)" and "after mutual cooperation, [writes] a 'cooperate' fill (a thanks); one write per encounter at most." In a cooperative population, programs write a thanks fill on *every* encounter. This will flush the 4-slot FIFO queue every 4 encounters, immediately evicting seeded, copied, contract, and grudge fills (and in Part R, triggering constant certificate re-checking per Amendment 2).
    *   *Fix:* Key deduplication/refresh (if a fill with the same `(tag, scope, key)` exists, update its action/timestamp in place without evicting, or ignore redundant writes), OR restrict history writes to unexpected/off-equilibrium outcomes (grudges only, or ablation of thanks).
*   **Part W `history` vs `behaviour` key collision:** Amendment 1 defines Part W history keys as "the partner's behaviour class (Part W)"—the exact same 8-element domain as the `behaviour` scope. Under the conflict rule (`behaviour > history`), any `behaviour` fill for a class permanently shadows any `history` fill for that class; worse, getting suckered by one program in behaviour class $X$ writes a grudge against *all* programs in class $X$, turning history into dynamic behaviour-rewriting rather than partner-specific reciprocity.
    *   *Fix:* Key Part W history on the partner's full `(base_program, fills)` tuple (or lineage/founder ID) so it tracks partners, not coarse behaviour classes.
*   **Asymmetric key domains across islands in Part R:** Amendment 1 says Part R `source` keys "are drawn from the bare sources present among the island's founders." Under migration (`mN = 1`) or fission–fusion, migrants carry fills keyed to their home island's founders, and seeded `source` fills cannot key on immigrant sources. Furthermore, on an island of size $N=100\text{–}200$, uniform draws over ~100 founder sources yield a $\le 1\%$ per-fill match rate, whereas `role` (2 keys) or `none` (1 key) match $50\text{–}100\%$ of the time.
    *   *Fix:* Draw seeded `source` keys from the global run founder pool (or include a `SELF_SOURCE` token in the domain so twin/clone recognition has non-vanishing prior mass).

**2. Design flaws or confounds**

*   **Three-player history ambiguity in SOG:** Amendment 1 defines write triggers only for 2-player PD ("partner defected while the program cooperated"). In the 3-player boss/worker game (boss, worker 1, worker 2), what triggers a grudge or thanks, and against which of the two partners' keys is it written?
    *   *Fix:* Explicitly specify SOG write triggers (e.g., worker writes grudge against boss key on wage=0 or whack; boss writes grudge against striking worker's key).
*   **Grammar-expansion confound:** The "Baseline (no hooks)" vs "Inert-hooks control" (Amendment 3) is essential because adding `HOOK` as a 1-node primitive dilutes the length/library prior over non-hook programs. However, Predictions 1, 3, 4, and 6 benchmark against the *no-hook baseline* rather than the *inert-hooks control*.
    *   *Fix:* Benchmark causal claims about hook *semantics* against the inert-hooks control; report the no-hook baseline → inert-hooks shift separately as the syntax-dilution effect.

**3. Predictions that are likely wrong**

*   **Prediction 3 (Source-keyed fills bring identity back in Part R, identity islands $\ge 0.02$):** Likely wrong under Amendment 1's prior. For a seeded `source` fill to create an identity clique, a founder must draw the `source` scope (1/6), draw *its own* bare source from the ~100–200 island founders ($\le 1/100$), draw action `C` (1/2) on a default-`D` hook, and establish. This prior mass is orders of magnitude below the ~0.009 `eq`-clique mass needed for the ~8 seeded copies threshold (RESULTS #28).
    *   *My prediction:* Unless `SELF_SOURCE` is an explicit key in the domain or self-copying/pair-contracts generate self-keyed fills endogenously, seeded `source` fills will not restore identity cliques ($\le 0.005$), and any identity restoration will come from *pair contracts* or *history thanks* among clones, not the seeded `source` scope.

**4. Missing controls or cheap additions**

*   **Grudge-only vs Grudge+Thanks ablation:** Cheaply separates whether history works via punishment of defectors or greenbeard-like mutual-cooperation reinforcement (especially in Part R where a thanks fill keyed on bare source acts like an endogenous identity certificate).
*   **Eviction rate statistic:** Log the number of FIFO evictions per encounter to verify the 4-slot cap isn't thrashing (cf. RESULTS #41: "a capped list thrashed").

**5. Alternative explanations not ruled out**

*   **Endogenous identity via `history` in Part R:** Because Part R `history` is keyed on *bare source* and writes "cooperate" after mutual cooperation, two twin programs that cooperate once write source-keyed `C` fills for each other. If `source` scope is ablated (Prediction 6), `history` (and pair contracts) can still build source-specific identity cliques. Ruling this out requires ablating `source` *and* source-keyed `history`/contracts together, or keying history on behaviour in both wings.
