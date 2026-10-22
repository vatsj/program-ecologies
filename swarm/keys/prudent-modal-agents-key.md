# Answer key and grading notes (do not give to agents): prudent modal agents

**Expected answers.**
1. Yes. The minimal depth is 2, for example PrudentBot with plain boxes: □a ∧ □(¬□⊥ → ¬d). Here □(¬□⊥ → ψ) means
   "PA + Con(PA) proves ψ". Its outcomes: D against CooperateBot, D against DefectBot, C against FairBot, C against
   itself. This was checked on Kripke frames (RE, 2026-10-22, `scratchpad/pb_plain.py`); Barasz et al. 2014 give the
   original.
2. **Conjectured, not proved:** no depth-1 agent is prudent. Evidence:
   - exhaustive over formulas without constants up to 7 symbols (801 classes);
   - 0 of 60,000 random depth-1 formulas with up to 4 boxes, inner and outer parts up to 7 symbols, constants
     included (`scratchpad/depth1_search.py`);
   - in that sample, 303 of 40,000 meet the other three conditions, and all of them defect against themselves, which
     is stable from world 8.

   So the likely obstruction is self-cooperation.
3. Open.

**Correction history.** The first statement claimed that no level-PA agent is prudent. That is false: PrudentBot is a
plain-box depth-2 formula. The literature pass caught it (`prudent-modal-agents-literature.md`). On the RS's request
(2026-10-22) the agent-facing statement no longer mentions PrudentBot, Con(PA), the Barasz et al. paper or any
heuristic; agents must find the Con guard themselves. Caveat: Barasz et al. is well known, so recall is possible.
Grade discovery and recall the same, and note it when the answer cites the paper.

**Grading.**
- 1 point: a prudent agent of depth 2 with a correct outcome table. Verify it with a stabilized Kripke evaluation.
- 1 point: identifies the Con(PA) guard (one level up) as the mechanism.
- 2 points: a valid proof that depth 1 is impossible, checked independently; or a verified depth-1 counterexample,
  which would refute our conjecture and is worth the same.
- 1 point (bonus): a characterization of, or minimal-size bound on, the depth-2 prudent agents.
- An answer claiming that no prudent agent exists scores 0 on question 1.
