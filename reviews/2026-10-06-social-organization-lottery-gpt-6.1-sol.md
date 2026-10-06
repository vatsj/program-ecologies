# Review of `specs/2026-10-06-social-organization-lottery.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The causal lever is not isolated.** Relative to rare mutation, the lottery changes worker abundance, boss diversity, and simultaneous availability of conditional programs. The hostile-boss control freezes the boss strategy, so it cannot establish whether worker numbers defeat an *evolvable* threat. **Fix:** cross low/high striker seed mass with monomorphic/diverse boss seeds, keeping conditional-worker mass fixed. Include a mostly hostile boss seed with a small, fixed non-whacking competitor share.
- **The cost argument conflates population size with encounter size.** There are two workers per encounter, not N: independent constant strikers contribute approximately 0.96 expected strike targets per encounter, before conditional responses. Larger N changes sampling and extinction, not mechanically the boss’s per-encounter cost. **Fix:** preregister the exact payoff table, production rule, matching normalization, and update kernel; calculate whacking/non-whacking payoff differences against identical wages.
- **The stopping criterion is insufficient.** Payoff identity on current local support need not survive migration, and neutral drift can change responses to future migrants. **Fix:** verify closure against globally surviving classes, including migration and neutral transitions. Otherwise label results horizon-censored; do not call a patchwork permanent.
- **The normative statistic is not an efficiency or scaling test.** Payoff shares can be undefined or misleading with zero/negative surplus; three fixed roles cannot establish Θ(1/n). **Fix:** report raw payoff vectors, production, enforcement losses, and Pareto domination separately. Define share eligibility explicitly and call ≥1/6 a three-role distribution threshold.

## 2. Predictions likely wrong

- **Prediction 1 overstates elimination.** Initial selection against whacking can disappear as strikers die; surviving whackers then become neutral relative to otherwise identical non-whackers. Source-dependent worker responses can also reverse comparisons. **My prediction:** early whacker decline at c = 0.5, but residual whacking policies on appreciably more islands than realized repression. “None on ≥0.8” is unsupported without the coupled trajectory.
- **Prediction 3’s twofold advantage is not justified.** A single-worker variant changes production, bargaining leverage, prior mass, and the meaning of “fair,” not just quorum availability. Moreover, near-zero fair frequencies make a ratio uninformative. **My prediction:** no robust numerical advantage can be forecast before matched no-quorum static calculations.
- **Prediction 5’s merging claim is too strong.** Higher migration does not guarantee resolution of incompatible or invasion-resistant wage states. **My prediction:** faster merging only where the cross-island invasion matrix permits it; otherwise a longer-lived patchwork remains possible.

## 3. Missing controls or cheap additions

- Add **two workers with QUORUM disabled**, retaining matched seed weights; this isolates the handshake better than deleting a role.
- Sweep initial constant-striker mass at fixed conditional-worker and boss composition. Measure the threshold for non-whacker establishment.
- Record cumulative whack costs, production lost to strikes, extinction times, and conditional-program lineages—not just policy labels.
- Compute reciprocal invasion payoffs between observed terminal island states.
- Align falsifiers with every quantitative claim; several currently leave large inconclusive gaps. Continue a small subset beyond 10⁵ generations to test censoring.

## 4. Alternative explanations not ruled out

Fair wages could reflect seeded reader-family abundance, finite-N founder luck, or transient strike persistence rather than collective bargaining. Zero wages could result from conditional workers disappearing before boss turnover, rather than intrinsically dominant zero-wage policies. Apparent patchworks could be metastability rather than closed coexistence. CC/RR differences could reflect changed worker incentives, not merely removal of boss commitment.

## 5. Beyond this experiment

Nothing material.
