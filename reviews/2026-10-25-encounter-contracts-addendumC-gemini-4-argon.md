# Review of `specs/2026-10-25-encounter-contracts.md` by gemini-4-argon

1. **Errors, contradictions or unsound mechanisms**

* **Arm H evaluation semantics are broken and violate the replay invariant.** Under **Evaluation of an encounter**, "Stage 1: every program plays as usual, giving the profile $p$. Stage 2: carriers whose key equals $p$ switch to their fills..." Under **Arms (H)**, "[Addendum review] In H fills are indexed by $(t, p)$... the fill is written into the hook whose evaluation produced the member's stage-1 action". However, the spec never defines how a program with a $(t, p)$-indexed fill evaluates in Stage 2 or when a responder simulates it. If a carrier in H simply switches its top-level action to the fill in Stage 2 (as in R), the hook structure and tag $t$ are ignored in play, making H identical to R except for an arbitrary genesis gate. Conversely, if the carrier re-evaluates its program in Stage 2 with `HOOK(t, a_0)` returning the fill, then (a) a fill on a non-terminal hook (if H ever allowed it) could branch into a different hook, and (b) when a responder simulates the carrier, replacing "every simulation atom of a carrier... by that carrier's fill" is ill-defined when an individual carries multiple fills for the same $p$ under different tags $t \in \{0,1\}$.
  * *Fix:* State explicitly that because `HOOK(t, a_0)` is a terminal leaf in the weak grammar, reaching $(t)$ on path in Stage 1 uniquely determines the carrier's Stage-2 action when key $p$ holds; in Stage 2, a carrier whose Stage-1 path terminated at `HOOK(t, a_0)` and who holds a fill for $(t, p)$ plays that fill (and responders substitute that active fill for simulation atoms of that carrier).
* **Arm C copying mechanism is undefined for coalition-size mismatches.** Under **Addendum 2**, "a whole contract: every member's fill, keyed as written... is offered to the coalition of the current encounter". A contract on the island may have been written by a coalition $S'$ of size 1, 2, or 3, or its fills may now sit on only a subset of slots (due to drift/extinction). In genesis, a coalition $S$ is drawn first. What happens if the sampled existing contract does not have fills for exact slots $S$?
  * *Fix:* Define a "whole contract" in the island pool by its key $p$ and the subset of slots $S'$ currently holding non-default fills for $p$ on the island (or draw the copied contract first, and set $S$ to be the slots represented in that contract).

2. **Design flaws or confounds**

* Nothing material.

3. **Predictions you think are wrong**

* **Prediction 1 (*Settled islands go quiet*):** Wrong when a settled island is a polymorphic mixture of programs that happens to yield a fixed fair-pair stage-2 action distribution, or when silent contracts drift to high frequency and alter the "committed complement" baseline during genesis. Even if the on-path Stage-2 distribution is fixed, newly arriving silent contracts change who is "committed" for off-path keys $p$, which can trigger new on-path firing contracts if the island has multiple program types mapping to the same action.
  * *My prediction:* Settled monomorphic fair islands have a 0 rate of new firing contracts, but any polymorphic settled fair island will continue to form firing contracts above $10^{-3}$ due to drift in silent/complement commitments.

4. **Missing controls or cheap additions**

* **Log Stage-1 vs Stage-2 divergence on settled islands:** Measure what fraction of settled V\* islands rely on active Stage-2 overrides on path versus islands where programs do the work in Stage 1 and contracts were merely the transient bridge. This directly answers the RS's question about whether contracts act only as rare-case deviations.

5. **Alternative explanations**

* **H vs R differences driven by prior dilution, not hook restriction:** While `H-top` and `H-inert` are included in the spec text, Prediction 7 still scores H directly against 0 and R. If H underperforms R, the text of Prediction 7 will not distinguish grammar dilution (`HOOK` leaves eating prior mass) from restricted write access unless the prediction falsifier is explicitly tied to `H` vs `H-top` and `H-inert`.
