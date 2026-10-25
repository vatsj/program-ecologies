# Review of `specs/2026-10-25-many-islands.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **The ODE does not conserve probability.** “\(dx_c/dt = \sum_{a,b}x_ax_bK(a,b\to c)-x_c\sum_bx_b(1-K(c,b\to c))\)” includes self-transitions in inflow but excludes them from outflow. Fix: subtract \(x_c\), or restrict inflow to \(a\ne c\). Test mass conservation and nonnegativity explicitly.

- **The amended settlement rule changes the claimed rare-migration limit.** “Neutral drift in the excluded slot does not delay settlement” conflicts with “this is the \(mN\to0\) limit exactly.” Under ordinary rare migration, all slots evolve during the diverging interarrival interval; freezing nonrecipient islands also suppresses that evolution. Fix: derive the embedded kernel after full within-island relaxation, or explicitly define this as an intervention-based process and compare against decreasing finite migration rates.

- **A finite pool is not the required order of limits.** “The primary \(I\to\infty\) estimate … [uses] at least 16,384 settled islands” still has finite-population drift and eventual support loss. Fix: establish pool-size convergence at fixed times before extending time; do not identify a pool’s terminal state with \(\lim_{t\to\infty}\lim_{I\to\infty}\).

- **Annealing needs an executable endpoint.** “A decaying rate with a finite total … then a mutation-free chase” leaves the transition time undefined: integrable intensity does not end at finite deterministic time. Fix: sample the finite Poisson arrival count and arrival times directly, or truncate with a quantified residual-arrival bound.

## 2. Design flaws or confounds

- **Stopping uses the wrong hazard.** “At least \(3/K_{\max}\cdot I\) events” cannot protect against missing slow transitions: the largest kernel entry ignores rare recipients, donors and bottlenecks. Class-preserving changes can also enable later conversion. Fix: use occupancy-weighted exit hazards, track composition changes, and report finite-horizon persistence unless absorption is established.

- **The initial law is inconsistent.** Migration follows annealing, yet the ODE and limiting outputs start “from the founding shares.” Fix: initialize each migration arm from its post-anneal composition distribution.

- Replicate counts, common observation horizons and uncertainty for coverage are unspecified. Adaptive terminal times make “coverage … at the final time” incomparable. Fix: preregister replicates and fixed migration-clock checkpoints; treat budget exhaustion as censoring, not convergence.

## 3. Predictions likely wrong

- **“Fair pairs are neutral … by slot symmetry” is too strong.** Symmetry constrains a symmetry-averaged kernel, not arbitrary composition-conditioned transitions or their evolving mixture. Symmetric dynamics can also have symmetry-breaking attractors. I predict aggregate symmetry initially, but neither neutrality nor persistent coverage follows.

- **Components need not match efficiency within 0.05 at every \(C\).** Smaller components lose rare conversion-carrying programs sooner and can enter different absorbing classes. I predict component-size effects whenever readers or bridges are scarce.

## 4. Missing controls or cheap additions

- Repeat injections using compositions sampled during migration, not only immediately after annealing.
- Compare settlement windows/caps; continue capped cases rather than silently treating them as settled.
- Add **two sequential, fully separated migrants**, alongside simultaneous \(K_2\). This distinguishes cumulative hidden-state changes from genuinely overlap-dependent conversion.
- Report exact efficient-outcome frequencies alongside modal classes.

## 5. Alternative explanations not ruled out

Apparent coverage may reflect exact ensemble symmetry or finite observation time; efficiency gains may reflect seed/prior changes rather than reading; apparent trapping may reflect missed rare transitions or suppressed drift. Zero limiting inefficient share also does not establish that every island eventually remains efficient.
