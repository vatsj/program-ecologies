# Review of `specs/2026-10-23-two-role-mixed.md` by gpt-6.1-sol

1. **Errors / contradictions and fixes**
   - **Poker’s blind arm excludes private information.** “*blind (constants and coins only, no application: no program reads)*” conflicts with the equilibrium program requiring `card`. Literally implemented, blind I cannot condition on its card, confounding source access with private-information access. **Fix:** retain `card` in every Endgame arm; remove only opponent-reading primitives.
   - **The bounded oracle is not necessarily a best response to actual play.** “*the exact best response to the opponent’s exact action distribution against me*” conflicts with “*computes the opponent’s exact distribution on the remaining budget D − d*.” A depth-sensitive opponent can behave differently in simulation and actual play. **Fix:** specify root-relative evaluation semantics and test simulated versus actual distributions for nested readers and cap-boundary programs. Unless they agree, call `cr` a bounded simulated-response operator, not an exact best response.
   - **The neutrality claim is false.** “*blind mixers at the equilibrium probabilities are neutral against every opponent in the zero-sum Endgame*” conflicts with allowing “*a program that checks a winner*.” II’s equilibrium coin strictly benefits when I checks winners. **Fix:** test minimax inequalities, with equality against equilibrium-support strategies—not universal neutrality.

2. **Design flaws / confounds and fixes**
   - **The stated targets do not test Pareto efficiency.** Inspection’s commitment payoff \((-3/8,0)\) is dominated by \((0,0)\) from \(N,C\); every feasible payoff in a zero-sum game is Pareto-efficient. **Fix:** frame these as commitment and exploitability experiments, not evidence that selection reaches Pareto efficiency.
   - **The matched arm is unspecified.** “*a simulating counterpart of the same size*” does not define sample count, branching, charges, or induced prior. **Fix:** give its executable definition and verify matching syntax weights, size, and accounting. Separately report oracle computational work: one-depth exact enumeration is a substantial subsidy.
   - **No large-population lottery inference is available.** Only the diagnostic chain varies \(N\); the primary lottery fixes \(N=100\). **Fix:** add a small lottery size panel or explicitly limit conclusions to finite populations.

3. **Predictions likely wrong**
   - “*simulating inspectees … cannot tell 3/8 from 1/4*” is false: repeated independent simulations distinguish them statistically. Finite-budget sampling is noisy, not informationally impossible. I predict a graded exact-versus-sample advantage depending on sample budget, not a categorical requirement for exact reading or a justified ≥0.2 gap.
   - Zero price removes strict displacement by C, but does not positively select readers over their compliant shadows. Thus “*readers hold at least 0.5*” has no mechanism-backed basis. I predict strong founder/prior dependence and possible transient commitment even at \(c=0\), rather than robust reader dominance.

4. **Missing controls / cheap additions**
   - Add pairwise invasion tests for reader → C → N → K, recording actual transition rates rather than inferring this sequence from shares.
   - Test repeated-sample responders at several fixed budgets.
   - Report encounter-conditioned inspection distributions, action correlations, and poker winner-betting rates; marginal probabilities alone cannot identify equilibrium in source-responsive populations.
   - Preselect continuation runs randomly and specify whether verdicts use terminal values or fixed averaging windows.

5. **Alternative explanations not ruled out**
   - Apparent commitment could be founder abundance, neutral reader persistence, or a long transient.
   - Near-zero poker value could conceal mutually exploitable populations.
   - Exact-arm gains could reflect the oracle subsidy or depth-cap artefacts rather than realizable source-reading advantages.
