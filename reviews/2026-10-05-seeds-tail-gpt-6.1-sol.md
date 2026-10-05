# Review of `specs/2026-10-05-seeds-tail.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes
- **The migration benchmarks may refer to different events.** \(1-(1-p)^4\approx0.50\) is the probability that **at least one** independent island succeeds, not that the entire population is efficient. With zero migration, all four succeed with probability \(p^4\approx0.00062\). Define “efficient fraction” precisely and report both run-level success and global \(P(C,C)\). State explicitly whether \(N=400\) is per island.
- **Finite enumeration cannot establish the claimed tail bound.** Cutoff-normalized priors can make \(\mu_{\rm est}(n)\) decrease through renormalization. Moreover, adding opponents can turn previously “unfakeable” residents into fakeable ones. Fix one infinite syntax prior, report retained mass and omitted mass, and separate newly added syntax from reclassification of existing residents. Provide a rigorous omitted-mass bound or label convergence extrapolative.
- **The co-seeding statistic is misconditioned.** \(N\mu_{\rm pf}P(A)\) approximates an unconditional joint quantity, not expected faker count conditional on establishment. Establishment also depends on the seeded mixture, not just singleton fixation against D. Compute \(E[K_{\rm pf}\mid A]\) and \(P(K_{\rm pf}>0\mid A)\); use resident-specific spoiler sets rather than their global union.
- **Migration rate alone does not identify “merging.”** Specify migration scheduling, time units, stopping criteria, and censoring. Measure migration events before nucleation and between nucleation and resolution. High migration approaches the well-mixed benchmark only if the update rule and observation horizon match.

### 2. Predictions likely wrong
- **Monotonicity and geometric decay are not justified.** They require fixed normalization and stable membership; neither is established. My prediction: raw mass of a fixed establishment set increases, but cutoff-normalized mass and spoiler ratios need not be monotone. Six additional shells will not establish a uniform tail.
- **Monotone decline with migration is unsupported.** Migration can spread successful cooperators as well as import spoilers or erase nucleation. My prediction: outcome depends on these competing timescales; an intermediate maximum is plausible, and convergence toward 0.383 requires verified mixing.
- **A strict invader need not contradict soundness alone.** The no-invasion claim also requires the relevant outcome-symmetry theorem and faithful evaluator semantics. Treat a counterexample first as a semantic/theorem-assumption check, not automatically a soundness failure.

### 3. Missing controls/cheap additions
- Rerun zero migration with the same horizon and pipeline; include an explicitly well-mixed 1,600-agent control. Propagate uncertainty in existing benchmark estimates.
- Forty runs per arm poorly resolve a 0.12 difference; disjoint intervals are an especially weak falsifier. Predefine a direct contrast with its interval, or describe this as a pilot.
- Log founder identity, spoiler identity, island composition, nucleation time, and terminal support—not just efficiency.
- Report establishment-weighted mass \(\sum_x\mu(x)\rho(x\mid D)\), alongside raw \(\mu_{\rm est}\).
- Commit predictions before inspecting class counts; those counts already inform tail predictions.

### 4. Alternative explanations not ruled out
Finite-horizon persistence rather than absorption; prior renormalization rather than biological tail behavior; compatibility among cooperative founders rather than faker scarcity; migration-assisted founder spread rather than independent lotteries.

### 5. Beyond this experiment
A useful theorem target is a **resident-conditioned spoiler bound**, uniform in cutoff, combined with a lower bound on founder establishment. Global faker mass alone cannot establish lottery success.
