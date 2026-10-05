# Review of `specs/2026-10-05-compatibility.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **Connected components are not compatibility networks.** Mutual cooperation is not transitive: x–z–y can be connected while x and y mutually defect. The proposed conditioning misses incompatible pairs within a component, and “one heavy component” does not establish compatibility. **Fix:** condition on actual incompatible pairs; report missing-edge mass within components and the heavy-set pairwise matrix.
- **The class-level anti-coordination object is undefined.** If every establisher self-cooperates, “defection within its own class” must concern distinct programs, not literal self-play. Aggregating these into a class may erase behavior that determines selection. **Fix:** specify the class equivalence relation and report within-/between-class interaction matrices, including diagonal and distinct-member encounters. Verify aggregation preserves relevant interactions.
- **κ and island risk need explicit denominators.** Define κ conditional on both draws being establishers; separately report μ_est. Pairwise incompatibility mass is not island-level co-occurrence probability: N(N−1)/2 opportunities can amplify rare pairs substantially. **Fix:** calculate exact multinomial co-occurrence probabilities where feasible, and the probability of *any* incompatible pair without summing overlapping events.
- **“Frozen efficient” risks circular classification and premature stopping.** **Fix:** select rows by a stopping rule independent of efficiency; state payoff-based Pareto efficiency separately from P(C,C) ≥ 0.95. Report unresolved/censored runs, terminal support, transition structure, and observation horizon. A frozen polymorphism under numerical tolerance is not necessarily an absorbing state.

### 2. Predictions likely wrong

- **Prediction 2’s island-risk bound does not follow from light pair mass.** Even two individually rare classes can both be represented at N = 400. I predict co-seeding risk will be materially larger than pair-draw incompatibility suggests; the numerical bound requires actual class masses.
- **Prediction 4 overstates majority advantage.** For mutually defecting rivals that self-cooperate, positive frequency dependence can favor the initially larger population. Cross-cooperating, within-class-defecting rivals instead favor the minority and can maintain polymorphism. Exploitation and background programs can reverse either conclusion. I predict outcome depends on the interaction pattern and background, not copy count alone.
- **The stated interpretation is too strong.** High κ at three cutoffs cannot make compatibility irrelevant along a large-N path: any fixed positive incompatible mass becomes routinely co-seeded. Nor does failure of κ establish separate graph components. I predict static pair risk can rise with N even if selection usually resolves it.

### 3. Missing controls/cheap additions

- Add pair-only competitions for each consequential incompatible pair, with balanced and skewed starting counts; compare against full-μ backgrounds.
- Include ordinary iid, unconditioned islands to connect the enriched sample to lottery prevalence. Report the conditioning-event probability and achieved sample counts by pair.
- Predefine “non-negligible”; align success thresholds with falsifiers or explicitly label the intervening ranges inconclusive.
- Separate multiple classes that mutually cooperate from genuinely incompatible terminal coexistence.

### 4. Alternative explanations not ruled out

Background spoilers, asymmetric establishment timing, finite-N drift, or stopping tolerances could explain apparent winner-take-all behavior. High compatibility may reflect grammar/prior concentration or the free sound oracle, rather than a general property of realizable source readers.

### 5. Beyond this experiment

The relevant asymptotic quantity is **unresolved incompatibility risk**, combining co-seeding probability with conditional resolution failure—not κ alone. Estimate or bound that quantity along the intended (N, I) path.
