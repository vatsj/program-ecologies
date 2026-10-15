# Review of `specs/2026-10-15-coverage-components.md` by gpt-6.1-sol

### 1. Design flaws or confounds, and fixes

- **Masks may be defined by treatment-dependent history.** “Untravelled” and “second” depend on encounters, inventory, and script ordering; grants themselves change these. Define classification against a specified reference state, including when it is evaluated and how ties are resolved. Otherwise the intervention changes its own component definition. Report the joint membership classes, not just marginal shares.
- **Grants can change subsequent production.** A granted script may satisfy the lack rule and suppress production of another script. Thus “S₃ plus (a)” need not be S₃’s inventory plus (a), and a minus-one component may be regenerated. Specify whether masks restrict grants only or all acquisition. Log grants, endogenous production, copying, suppression, and reacquisition separately; interpret grant-only cells as supply-policy interventions, not clean component removal.
- **Resolve S₃ versus S-nonself₃ explicitly.** The motivating baseline is S-nonself₃, but the design says production runs as S₃. Freeze the gate, copying, retry, and cost rules across cells. Require endpoint equivalence throughout trajectories, including production counters and charges—not merely identical final outcomes.
- **The outcome’s denominator is ambiguous.** “0.30 of islands (6 of 20 runs)” conflates island share with run success unless runs have reached consensus. Define both separately, with a fair-state threshold and persistence criterion. Use generation 10,000 as the primary endpoint; 2,000 is an intermediate observation.

### 2. Predictions I think are wrong

- **Prediction 1 overstates what “production coverage” establishes.** It does not distinguish missing encounter opportunities from alternative proofs, gate restrictions, or their interactions. My weak prediction: plus (a) alone will fall below 0.2, and at least one combined grant will outperform every singleton. The reason is that regrowth may require complementary certificates across coalition members.
- **Prediction 3’s justification is weak.** Small aggregate effects of identity do not imply that `EQ`-true certificates are dispensable during rare nucleation events. I predict a larger effect on regrowth latency or successful coalition composition than on early fair share; necessity remains unresolved.
- With 20 runs, the stated numerical bands are not sharp falsifiers of underlying probabilities. For example, 0/20 still permits a success probability around 0.14 at the one-sided 95% bound. Separate observed-threshold verdicts from statistical evidence.

### 3. Missing controls or cheap additions

- Add script-count-matched random grants/removals, preferably stratified by host program, script length, and check set. Otherwise component identity is confounded with coverage volume.
- If no singleton rescues, test selected pairs before concluding “neither”; plus/minus-one cells cannot resolve complementarity.
- Do not drop plus-one cells because minus-one is near H-full: redundancy can make a component sufficient but unnecessary. Base pruning on cost, not that inference.
- Confirm candidates on fresh streams; the existing seeds already motivated the hypothesis. Use event-keyed random streams so altered production does not shift demographic randomness.
- For a few successful runs, replay with the implicated granted script withheld immediately before first use. First-use tracing alone is not causal mediation.

### 4. Alternative explanations not ruled out

Larger lists may alter lookup priority, tie-breaking, copying opportunities, or effective costs. Grants may preserve rare coalition types rather than directly enable fair encounters. Apparent failure may be delayed nucleation beyond the horizon, not inaccessible regrowth.

### 5. Ideas beyond this experiment

Nothing material.
