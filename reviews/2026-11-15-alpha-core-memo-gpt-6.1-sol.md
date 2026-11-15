# Review of `notes/2026-11-15-alpha-core-memo.md` by gpt-6.1-sol

### 1. Foundational flaws and fixes — Q1

**Step 3 is not established by steps 1–2.** Fixed opponent programs define a response to rewritten *source*, not necessarily a worst-case response to the deviators’ *actions*. Reading source does not imply predicting execution, implementing arbitrary punishments, or supporting mutually consistent punishments for every coalition. “Closed under reading” alone is insufficient: programs can read and ignore their inputs.

**Fix:** define the induced program game, termination/default semantics, deviation sets, randomization and coalition coordination. Then separate:
- **Necessity:** strong program-equilibrium outcomes lie in an appropriately defined α-core, provided coalitions can execute every relevant guaranteed action deviation.
- **Sufficiency:** every α-core outcome admits one executable profile deterring *all* coalition rewrites. This needs a construction, not the max–min observation.

For NTU games, coalition worth is a **set of payoff vectors**, not a scalar maximized coalition payoff. Blocking requires one coalition strategy that strictly improves every member’s payoff against every complementary strategy.

**Literature:** Aumann (1959), *Acceptable Points in General Cooperative n-Person Games*, is foundational for α/β effectiveness and strong equilibrium. Tennenholtz (2004), *Program Equilibrium*, and Kalai–Kalai–Lehrer–Samet (2010), *A Commitment Folk Theorem*, concern specified program/commitment constructions; neither should be cited as establishing this coalitional equality without an explicit extension. I would mark that equality **unverified**, not known.

### 2. Claims I think are wrong — Q2

**C1 materially understates selection.** The grand coalition can implement any feasible improvement, so α-core membership entails **weak Pareto efficiency** under strict-all-member blocking. In the standard pure-action PD, the α-core outcome is mutual cooperation, not a broad individually rational region. With lotteries, specify the feasible payoff set; individual rationality alone still does not characterize the core.

**C4 conflates randomization with β-effectiveness.** Private randomness changes the available strategies and information; it does not automatically reverse coalition/complement quantifiers. Prediction: the relevant object may be a **mixed-strategy α-core**, not the β-core.

**C2’s neutral-shadow argument is conditional.** Identical realized actions do not establish neutrality when opponents inspect source. Require response-equivalence against the resident population.

**Most damaging:** C5, together with the missing sufficiency construction. C6 is the principal obstacle to connecting the static object to current selection dynamics.

### 3. Missing checks and literature

Cheap theory additions:
- Work through deterministic and privately randomized **RPS**, PD, chicken and one three-player externality game.
- Prove the necessity inclusion before attempting equality.
- Specify strict versus weak blocking, correlated versus independent coalition randomization, transfers and computational costs.
- Separate stable-set claims from core claims: unchanged dominance in one running example does not establish general existence or dynamic relevance.

Scarf (1971), *On the Existence of a Cooperative Solution for a General Class of N-Person Games*, is directly relevant. Distinguish its strategic-game hypotheses from Scarf’s **1967 balanced NTU-core theorem**. “Convex NTU games” is too ambiguous.

### 4. Alternative explanations

Observed acceptance of threats could reflect untested contingencies, limited mutation support or source-recognition conventions—not α-core implementation. Likewise, fair wages versus minimal wages do not independently validate either static notion; the memo changes enforcement and selection assumptions together.

### 5. Recommendation — Q3

Choose **A2 provisionally**, dropping undefined “credible” but calling the object an **α-core benchmark**, not what closed reading “literally implies.” State only proved inclusion claims for realizations. Treat credibility as an operational testing/selection property, not automatically “survives neutral drift”: the supplied record already shows drift can disarm and selection can re-arm threats. Further program-level ideas: nothing material.
