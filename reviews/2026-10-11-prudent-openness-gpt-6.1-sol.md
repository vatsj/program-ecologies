# Review of `specs/2026-10-11-prudent-openness.md` by gpt-6.1-sol

### 1. Design flaws or confounds, and fixes

- **P4 does not identify the effect of refusing unconditional cooperators.** It compares CBP without cooperators to CB with cooperators; removal also changes the entire competitive environment. Add CB’s matched-mass tilt with cooperators removed, using identical redistribution. Estimate the CBP–CB difference with and without cooperators.
- **The XC exclusion is not established by soundness.** Your own CBP–CB argument implies CBP defects against CB, precisely the behavior XC requires certified. Soundness prohibits false certificates, not certificates of true defection. Check executable actions and certificate availability separately. Direct CBP–XC incompatibility also does not exclude intermediate bridges; enumerate compatibility paths and their seed mass.
- **“CBP’s pairwise-compatible set” is underspecified.** Compatibility need not be transitive; there may be several maximal sets containing CBP. Freeze an explicit membership rule, report overlaps with CB/P_open/XC, and distinguish a mutually compatible set from a bridge-connected component. Do not select the family after observing winners.
- **The scan changes identity abundance, not identity’s syntactic price.** Renormalization simultaneously changes all competitors. Call this an abundance threshold; specify how the CBP mass remains exactly M while identity mass varies, including overlaps and redistribution.
- **Fixed N, I and horizon cannot establish a large-population threshold.** “Extend separated runs” also conditions observation time on outcome. Report all cells at common checkpoints, label unresolved runs, and add a small scaling panel around the apparent transition.

### 2. Predictions likely wrong

- **Prediction 2’s comparison is invalid**, and the claimed convergence need not occur even after matching backgrounds: CBP and CB differ in compatibility and exploitation by other readers. I predict a residual difference after cooperator removal, with uncertain sign.
- **Prediction 4’s reasoning about XC is wrong**, and “universal among verifiers” overstates the target: it explicitly excludes verifying nice carriers. Predict universality only within a precisely defined prudent compatibility family; its reader-wide P(C,C) need not exceed 0.9.
- **Prediction 5’s exponential is only a special case.** With independent founders and constant establishment probability q, it is approximately exp(−6,400mq). Competition, multiple founders per island and establishment saturation can make q mass-dependent. I predict approximate exponential behavior only at low m, with deviations elsewhere. Forty runs cannot reliably support the proposed smoothness criterion.
- **Prediction 6’s ≥5× shift is unsupported.** Better establishment does not eliminate incompatible identities once established. I predict improved prudent coverage, but potentially a modest universality shift and persistent XC competition in the chain.

### 3. Missing controls or cheap additions

- Log initial clique copies, occupied islands, family copies and early establishment times. Separate **arrival → establishment → persistence → island spread**.
- Report extinction probability and established islands per occupied seed island alongside “islands per seeded copy”; pooling and migration make the latter a poor founder-success estimator.
- Specify the threshold statistic—e.g. the 50% crossing—and confidence intervals. Refine nearby scan points only if needed.
- For the reduced chain, report support, transition structure and closure/twin-drift checks, not merely the highest-weight state.

### 4. Alternative explanations not ruled out

Prudent success could reflect seed payoff, family composition, certificate/checking costs, concentrated founders, or bridge survival rather than openness. A threshold could reflect founder occupancy or finite observation time rather than a selection transition. Reduced-support chain dominance could result from omitted exits.

### 5. Beyond this experiment

nothing material
