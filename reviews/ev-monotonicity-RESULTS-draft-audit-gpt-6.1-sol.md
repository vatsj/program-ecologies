# Review of `notes/ev-monotonicity-RESULTS-draft.md` by gpt-6.1-sol

- **“The stored and recomputed founding pools therefore agree exactly.”** Validation establishes agreement of aggregate trajectories and final pair counts, not equality of founding histograms; ODE differences reach 2.60·10⁻¹². **Correction:** “The reported aggregate validation checks agree to numerical precision; exact founding-pool identity was not established.”

- **“Penalty 0.1 … 10⁵ … 0.99999.”** The report gives 0.999998, which rounds to **1.00000** at five decimal places. **Correction:** use 0.999998 consistently, including the RE 1 discussion.

- **“The unbonused symmetric laws and the worlds start from the same raw pooled histogram, so the penalty’s finite-world gains are the speed effect.”** The supplied report does not establish histogram identity, and common initial conditions do not isolate speed from altered finite-population transition or absorption probabilities. **Correction:** describe the observed endpoint improvement; label a speed-only explanation untested.

- **“EV-monotonicity holds … never moves V* away from 1 … removes … unequal consensus.”** Only two penalties, three founding pools, and 20 finite worlds per condition were tested. Numerical convergence is not a proof of an infinite-time limit; zero observed unequal consensuses is not elimination of their probability. **Correction:** restrict the conclusion to tested trajectories and finite schedules, distinguishing numerical convergence from a proved limit.

- **“In every finite world at b ≥ 1/6”** and **“responsiveness is therefore conditional on the bonus clearing the unequal pair’s payoff.”** Only b = 1/6 was tested at or above that threshold. Moreover, b = 1/12 and 1/8 select F0 at mean-field convergence despite lying below it. The proposed invasion mechanism has no isolating control. **Correction:** “All 20 sampled worlds selected F0 at b = 1/6; a general threshold mechanism remains a hypothesis.” Distinguish eventual selection from transient robustness.

- **“A permanent … route to unequal consensus.”** At b = 1/24, two mean-field trajectories meet the numerical convergence criterion near unequal states; finite worlds stop at 10⁵ events. **Correction:** say “numerically converged unequal outcomes in two pools,” not established permanence.

- **“RE 7 half held.”** Both mean-field clauses pass; the finite-world prediction fails at b = 1/12. But the registered *falsifier* concerns only convergence V* < 0.99 and is not triggered. **Correction:** explicitly distinguish partial prediction failure from non-triggering of the stated falsifier.

- **“RE 5 held as written … F0 0.998 of islands.”** The registered checkpoint threshold concerns F0’s share **among fair-pair islands**, whereas the cited number uses all islands. Both pass, but they are different estimands. **Correction:** report the conditional share, approximately 0.998249/0.998251 ≈ 0.999998.

- **“With the 155 worlds … the pooled count is uniform.”** The registered reference counts are 44/54/57, not uniform counts. **Correction:** say “compatible with uniformity,” not “uniform.”
