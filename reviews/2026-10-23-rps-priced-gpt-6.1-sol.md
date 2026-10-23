# Review of `specs/2026-10-23-rps-priced.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **Old payoff classes may no longer be valid classes.** Programs identical in game payoffs can differ in runtime, including runtime against third parties. Importing the unpriced partition can therefore create false neutrality and incorrect transition rates. **Fix:** establish equivalence using the complete priced payoff rows and columns; retain source multiplicities, mutation masses and twin drift. Test whether any imported class splits before running dynamics.

- **The charge is not operationally unambiguous.** “Application levels” could mean maximum nesting depth or total applications across branches. Exact reading may perform substantial distributional computation at shallow depth. **Fix:** specify a trace-level accounting recurrence covering sequential calls, branches, nested simulations, randomization and cap exhaustion. Call this a *depth price*, not runtime pricing, unless it measures total work. Include hand examples where depth and work differ.

- **The solver requirement does not establish adequate polymorphic coverage.** Closure-seeded exploration is necessary but does not guarantee discovery of higher-support attractors; reporting three-type fates is insufficient given the documented four–six-class failures. **Fix:** require multi-start replicator searches, support-size diagnostics, exploration-threshold sensitivity and twin-expanded results. Mark unresolved cycles or attractors indeterminate rather than assigning stationary weights.

- **Generation 2,000 is an endpoint, not necessarily a lottery outcome.** Pricing changes selection and absorption times; paired founders do not solve censoring. **Fix:** report unresolved fractions and trajectories; extend unresolved runs under a preregistered stopping rule.

## 2. Predictions likely wrong

- **Prediction 4: monotone mixing is not implied by monotone penalization.** Cost removes readers that exploit constants as well as readers that forfeit. Increasing the price can favor constant-dominated, population-level mixtures without increasing individual mixing. **My prediction:** forfeits decline more reliably than individual mixing rises; mixing need not be monotone.

- **Prediction 3: eliminating one bottleneck does not establish rapid chain convergence.** Free constants and `X` remain neutral against one another, and entry rates, prior mass and other reader transitions can still bind. **My prediction:** forfeits respond sooner than stationary individual-mixing mass; convergence by \(N=10^3\) is substantially less secure than the brief suggests.

- **Prediction 5 conflates individual and population mixing.** A coinless population can contain a balanced polymorphism of constants with zero game exploitability. **My prediction:** individual mixing stays absent, but the population exploitability floor of 0.3 is not justified.

Prediction 1’s invasion claim is plausible, but distinguish invasion from dominance throughout a two-type contest. Also verify “`X` earns 0 against everyone”: under ordinary unilateral-forfeit rules, it earns positive payoff against forfeiting opponents.

## 3. Missing controls / cheap additions

- Add a **forfeit-only penalty**, matched to \(cD\), to separate removing free non-play from penalizing successful reading.
- Report **net-payoff exploitability** alongside game-only exploitability. A costly game exploiter need not be an evolutionary threat.
- Add a small \(D\)-sensitivity panel: hold \(cD\) fixed while changing \(D\), distinguishing timeout penalties from changes in available reasoning.
- Specify paired, run-clustered uncertainty for all lottery contrasts; islands are not independent replicates.

## 4. Alternative explanations not ruled out

Success could reflect the privileged zero-cost `X` primitive, changed prior mass after class splitting, or expensive-reader suppression—not a general advantage of realizable randomization. Low exploitability could come from constant polymorphisms rather than individually unexploitable programs.

## 5. Broader research-program ideas

RPS game value is not Pareto efficiency: before pricing, all zero-sum outcomes are Pareto-efficient. Report aggregate net payoff separately; this experiment tests resource waste and exploitability, not the general efficiency conjecture directly.
